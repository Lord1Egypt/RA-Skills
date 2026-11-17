/**
 * What has to hold about the recorder registry, checked on every run of
 * `npm run validate` (scripts/check-pipelines.mjs executes this file).
 *
 * The invariant no type can express, and whose violation is silent: a
 * registry key must equal its recorder's `provider`, because that slug is
 * written into every capture's `source:` line and compiled into the regex that
 * reads those lines back. Filed under the wrong key, the collector stops
 * recognising what it captured and re-captures the window every morning
 * without ever erroring.
 *
 * The per-adapter checks serve one canned response shaped the way that vendor
 * documents it. They cannot prove the documentation is right — only
 * `--dry-run` against a real workspace does — but they do prove a refactor has
 * not changed which field an adapter reads.
 *
 * No network: `fetch` is replaced, and an unrecognised URL fails the eval
 * rather than escaping to a vendor.
 */
import assert from "node:assert/strict";
import {
  cpSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Read at module load in recorder.ts, so it has to be set before the import.
process.env["CALL_CAPTURE_PACE_MS"] = "0";
process.env["CALL_RECORDER_API_KEY"] = "test-key";

const { RECORDER } = await import("../scripts/collect/config.ts");
const { backoffSeconds, checkFlags, ConfigError, pageGuard, recorderKeyPair } =
  await import("../scripts/collect/recorder.ts");
const { renderTurns } = await import("../scripts/collect/recorders/turns.ts");
const { RECORDERS, RECORDER_SLUGS, recorderTable, resolve } = await import(
  "../scripts/collect/recorders/index.ts"
);

const checks = [];
const check = (name, run) => checks.push([name, run]);

// ---------------------------------------------------------------- the registry

check("every registry key is its recorder's provider slug", () => {
  for (const [slug, entry] of Object.entries(RECORDERS)) {
    assert.equal(
      entry.recorder.provider,
      slug,
      `${slug} is filed under a recorder whose provider is "${entry.recorder.provider}": ` +
        `the dedup key and the source: line would drift apart`,
    );
  }
});

check("every entry carries what the CLI and a reader need", () => {
  for (const [slug, entry] of Object.entries(RECORDERS)) {
    for (const field of ["label", "credential", "docs"]) {
      assert.ok(
        typeof entry[field] === "string" && entry[field].length > 0,
        `${slug} has no ${field}`,
      );
    }
    assert.ok(
      ["live", "docs"].includes(entry.written),
      `${slug} has written: "${entry.written}", which is neither live nor docs`,
    );
    assert.match(entry.docs, /^https:\/\//, `${slug} has no docs URL`);
    for (const method of ["listReady", "transcript", "notes"]) {
      assert.equal(
        typeof entry.recorder[method],
        "function",
        `${slug} does not satisfy Recorder: ${method} is missing`,
      );
    }
  }
});

check("the shipped recorders are listed for a human to choose from", () => {
  const table = recorderTable();
  for (const slug of RECORDER_SLUGS) {
    assert.ok(table.includes(slug), `--list does not mention ${slug}`);
  }
  assert.ok(
    table.includes("config.ts") && table.includes("--recorder="),
    "--list does not say how to pick",
  );
});

// ------------------------------------------------------------------ selection

check("the code selection is what runs when no flag is passed", () => {
  const { entry, recorder } = resolve([]);
  assert.equal(recorder.provider, RECORDER);
  assert.equal(entry.recorder, recorder);
});

check("an unknown slug stops the run and names the alternatives", () => {
  // Only reachable through the flag; the same typo in config.ts does not
  // compile.
  assert.throws(
    () => resolve(["--recorder=zoom"]),
    (error) =>
      error instanceof ConfigError && error.message.includes("granola"),
  );
});

check("the flag overrides the code selection for one run", () => {
  assert.equal(resolve(["--recorder=granola"]).entry.label, "Granola");
  // Typed by a human at a terminal, so the slug is not case-sensitive.
  assert.equal(resolve(["--recorder=Granola"]).recorder.provider, "granola");
});

check("the collector's configuration is not in the agent's spec", () => {
  // Both spellings typecheck, so the regression would otherwise surface at
  // someone else's deploy: a `secret()` credential blocks it on whoever runs
  // it having the key exported, and a choice in `env` is one no compiler
  // checks and no reader of the collector sees.
  const agent = readFileSync(
    new URL("../infra/agents/call-scribe.ts", import.meta.url),
    "utf8",
  );
  const declarations = agent
    .split("\n")
    .filter((line) => line.trim().startsWith("//") === false);
  for (const forbidden of ["secret(", "env:", "CALL_RECORDER"]) {
    assert.ok(
      declarations.every((line) => line.includes(forbidden) === false),
      `call-scribe.ts declares ${forbidden} — the recorder and the internal ` +
        `domain belong in scripts/collect/config.ts, and the credential in the ` +
        `workspace catalog (cargo-ai workspaceManagement envVar create)`,
    );
  }
});

check("an argument the collector does not know stops the run", () => {
  checkFlags(["--dry-run", "--recorder=granola", "--list"]);
  for (const argv of [["--dryrun"], ["--recorder", "granola"], ["-n"]]) {
    assert.throws(
      () => checkFlags(argv),
      ConfigError,
      `${argv.join(" ")} was accepted, and would have run something else`,
    );
  }
});

// --------------------------------------------------------------- the transport

check("a 429 with no Retry-After backs off rather than retrying at once", () => {
  // `Number(null)` is 0 and `Number.isFinite(0)` is true, so reading the
  // header without a null check spent four retries in the same second.
  assert.equal(backoffSeconds(null, 0), 8);
  assert.equal(backoffSeconds("", 1), 16);
  assert.equal(backoffSeconds("0", 0), 8);
  assert.equal(backoffSeconds("not-a-number", 0), 8);
  assert.equal(backoffSeconds("45", 0), 45);
  // An hour, asked for by the vendor, would hold the whole run open.
  assert.equal(backoffSeconds("3600", 0), 300);
});

check("a pagination loop that never terminates is stopped", () => {
  const guard = pageGuard("probe", 3);
  guard();
  guard();
  guard();
  assert.throws(guard, /probe: pagination did not terminate after 3 pages/);
});

// -------------------------------------------------------------- the pipeline
//
// `capture()` against a fake recorder, in a copy of the collector under a
// temporary root — so `cadence/log/` resolves there and these checks write
// real files. This half is what every adapter shares, and it is where the
// dedup key, the internal-domain rule and the file layout actually live.

const tree = mkdtempSync(join(tmpdir(), "call-capture-contract-"));
cpSync(
  new URL("../scripts/collect", import.meta.url),
  join(tree, "scripts", "call-capture", "collect"),
  { recursive: true },
);
const pipeline = await import(
  join(tree, "scripts", "call-capture", "collect", "recorder.ts")
);

// Each check captures on a day of its own, so one of them failing cannot
// renumber another's files: everything here writes into one tree, because one
// tree is what the collector has.
const call = (day, id, attendees) => ({
  id,
  startAt: `${day}T10:00:00Z`,
  subject: "a call",
  attendees,
});

const fake = (calls) => ({
  provider: "probe",
  listReady: async () => calls,
  transcript: async () => "**Ada:** hello",
  notes: async () => null,
});

const raw = (day) => {
  const dir = join(tree, "cadence", "log", "raw", "calls");
  try {
    return readdirSync(dir)
      .filter((name) => name.startsWith(day))
      .sort();
  } catch {
    return [];
  }
};

check("an address the vendor mangled is survived, not fatal", async () => {
  // Every adapter passes the vendor's value through with at most a `??`, so
  // `""` and a bare label both reach here. They used to throw a TypeError out
  // of accountSlug and take the whole morning's run with them.
  await pipeline.capture(
    fake([
      call("2026-09-10", "mangled", [
        { email: "", name: "No address" },
        { email: "not-an-address", name: "No at sign" },
        { email: "her@acme.com", name: "Real" },
      ]),
    ]),
  );
  assert.deepEqual(raw("2026-09-10"), ["2026-09-10-acme.md"]);
});

check("the internal-domain rule matches a domain, not a suffix", async () => {
  // `endsWith("example.com")` read notexample.com as internal and dropped the
  // call in silence; a short internal domain makes that routine, since
  // "me.com" swallows every acme.com contact.
  await pipeline.capture(
    fake([
      call("2026-09-11", "lookalike", [
        { email: "us@example.com" },
        { email: "her@notexample.com" },
      ]),
      call("2026-09-11", "subdomain", [
        { email: "us@example.com" },
        { email: "them@mail.example.com" },
      ]),
      call("2026-09-11", "internal", [{ email: "us@example.com" }]),
    ]),
  );
  // The lookalike domain is a customer; the subdomain and the internal-only
  // call are colleagues, and a call with no customer on it is not captured.
  assert.deepEqual(raw("2026-09-11"), ["2026-09-11-notexample.md"]);
});

check("a call already anywhere under cadence/log/ is not captured again", async () => {
  // The scribed entry, not the raw file: a raw capture that has been scribed
  // and archived must still count as captured.
  mkdirSync(join(tree, "cadence", "log", "calls"), { recursive: true });
  writeFileSync(
    join(tree, "cadence", "log", "calls", "2026-09-14-scribed.md"),
    "---\nsource: probe already-done\n---\n",
  );
  await pipeline.capture(
    fake([call("2026-09-12", "already-done", [{ email: "her@acme.com" }])]),
  );
  assert.deepEqual(raw("2026-09-12"), []);
});

check("two calls with one account on one day both keep a file", async () => {
  await pipeline.capture(
    fake([
      call("2026-09-13", "one-acme", [{ email: "her@acme.com" }]),
      call("2026-09-13", "two-acme", [{ email: "him@acme.com" }]),
    ]),
  );
  assert.deepEqual(raw("2026-09-13"), [
    "2026-09-13-acme-2.md",
    "2026-09-13-acme.md",
  ]);
});

check("an id the dedup key cannot round-trip fails loudly", async () => {
  // Written into `source:` and read back with a regex, so an id carrying
  // anything outside that class reads as never-captured and is re-captured
  // every morning without ever erroring.
  await assert.rejects(
    pipeline.capture(
      fake([call("2026-09-14", "has spaces", [{ email: "her@acme.com" }])]),
    ),
    /deduplication key cannot round-trip/,
  );
});

check("--dry-run writes nothing", async () => {
  process.argv.push("--dry-run");
  try {
    await pipeline.capture(
      fake([call("2026-09-15", "dry", [{ email: "her@beta.io" }])]),
    );
    assert.deepEqual(raw("2026-09-15"), []);
  } finally {
    process.argv.splice(process.argv.indexOf("--dry-run"), 1);
  }
});

check("a two-value credential splits on the first colon only", () => {
  process.env["CALL_RECORDER_API_KEY"] = "key:pa:ss";
  try {
    assert.deepEqual(recorderKeyPair("<a>:<b>"), ["key", "pa:ss"]);
  } finally {
    process.env["CALL_RECORDER_API_KEY"] = "test-key";
  }
  assert.throws(() => recorderKeyPair("<a>:<b>"), ConfigError);
});

// -------------------------------------------------------------------- shaping

check("consecutive segments from one speaker become one turn", () => {
  assert.equal(
    renderTurns([
      { speaker: "Ada", text: "Hello." },
      { speaker: "Ada", text: "One more thing." },
      { speaker: "Grace", text: "Noted." },
      { speaker: "Grace", text: "   " },
    ]),
    "**Ada:** Hello. One more thing.\n\n**Grace:** Noted.",
  );
  assert.equal(renderTurns([{ text: "unattributed" }]), "**Speaker:** unattributed");
  assert.equal(renderTurns([{ speaker: "Ada", text: "  " }]), null);
  assert.equal(renderTurns([]), null);
});

// ------------------------------------------------------------------- adapters
//
// One canned response per adapter, shaped the way the vendor documents it, and
// an assertion about what the adapter made of it.

const routes = new Map();
const seen = [];

globalThis.fetch = async (url, init = {}) => {
  const key = `${init.method ?? "GET"} ${String(url).split("?")[0]}`;
  seen.push({ url: String(url), init });
  const handler = routes.get(key);
  assert.ok(handler, `adapter called an unrouted endpoint: ${key}`);
  const body = await handler(String(url), init);
  return {
    ok: true,
    status: 200,
    headers: new Map(),
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
};

const route = (key, handler) => routes.set(key, handler);
const lastRequest = () => seen[seen.length - 1];
const header = (name) => {
  const headers = lastRequest().init.headers ?? {};
  return headers[name];
};

check("avoma: readiness flags, speakers joined, blocks walked to text", async () => {
  const { avoma } = await import("../scripts/collect/recorders/avoma.ts");
  routes.clear();
  route("GET https://api.avoma.com/v1/meetings/", () => ({
    results: [
      {
        uuid: "av-1",
        state: "completed",
        transcript_ready: true,
        start_at: "2026-01-02T09:00:00Z",
        subject: "Acme call",
        attendees: [{ name: "Ada", email: "ada@acme.com" }],
      },
      // Still processing: the flag is absent rather than false, which is the
      // whole reason the collector's window overlaps.
      { uuid: "av-2", state: "completed", start_at: "2026-01-02T10:00:00Z" },
      // Ready, but the meeting never happened.
      {
        uuid: "av-3",
        state: "cancelled",
        transcript_ready: true,
        start_at: "2026-01-02T11:00:00Z",
      },
    ],
    next: null,
  }));
  route("GET https://api.avoma.com/v1/transcriptions/", () => ({
    speakers: [{ id: 7, name: "Ada" }],
    transcript: [
      { speaker_id: 7, transcript: "We need SSO." },
      { speaker_id: 9, transcript: "Noted." },
    ],
  }));
  route("GET https://api.avoma.com/v1/notes/", () => ({
    results: [
      {
        data: [
          { object: "block", text: "They asked about SSO." },
          { children: [{ text: " Twice." }] },
        ],
      },
    ],
  }));

  const calls = await avoma.listReady("2026-01-01", "2026-01-03");
  assert.deepEqual(
    calls.map((call) => call.id),
    ["av-1"],
  );
  assert.equal(header("Authorization"), "Bearer test-key");
  // An unmapped speaker id falls back rather than dropping the line.
  assert.equal(
    await avoma.transcript("av-1"),
    "**Ada:** We need SSO.\n\n**Speaker:** Noted.",
  );
  // Blocks become lines: `object: "block"` is what ends one.
  assert.equal(await avoma.notes("av-1"), "They asked about SSO.\n Twice.");
});

check("grain: two headers, bare-array transcript, summary from the list", async () => {
  const { grain } = await import("../scripts/collect/recorders/grain.ts");
  routes.clear();
  route("POST https://api.grain.com/_/public-api/v2/recordings", (_url, init) => {
    const body = JSON.parse(init.body);
    assert.equal(body.include.participants, true);
    assert.equal(body.filter.after_datetime, "2026-01-01T00:00:00Z");
    return {
      recordings: [
        {
          id: "gr-1",
          title: "Acme call",
          start_datetime: "2026-01-02T13:00:00Z",
          participants: [{ name: "Ada", email: "ada@acme.com", scope: "external" }],
          ai_summary: { text: "They want SSO." },
        },
      ],
      cursor: null,
    };
  });
  route(
    "GET https://api.grain.com/_/public-api/v2/recordings/gr-1/transcript",
    () => [
      { start: 0, end: 1, text: "We need SSO.", speaker: "Ada" },
      { start: 1, end: 2, text: "By March.", speaker: "Ada" },
    ],
  );

  const calls = await grain.listReady("2026-01-01", "2026-01-03");
  assert.equal(calls[0].startAt, "2026-01-02T13:00:00Z");
  assert.equal(header("Public-Api-Version"), "2025-10-31");
  assert.equal(await grain.transcript("gr-1"), "**Ada:** We need SSO. By March.");
  assert.equal(await grain.notes("gr-1"), "They want SSO.");
});

check("tldv: x-api-key, page/pages paging, notes as markdown", async () => {
  const { tldv } = await import("../scripts/collect/recorders/tldv.ts");
  routes.clear();
  route("GET https://pasta.tldv.io/v1alpha1/meetings", (url) => {
    const page = Number(new URL(url).searchParams.get("page"));
    return {
      page,
      pages: 2,
      results: [
        {
          id: `td-${page}`,
          name: "Acme call",
          happenedAt: "2026-01-02T16:00:00Z",
          invitees: [{ name: "Ada", email: "ada@acme.com" }],
          organizer: { name: "Rep", email: "rep@ourco.com" },
        },
      ],
    };
  });
  route("GET https://pasta.tldv.io/v1alpha1/meetings/td-1/transcript", () => ({
    data: [{ speaker: "Ada", text: "We need SSO." }],
  }));
  route("GET https://pasta.tldv.io/v1alpha1/meetings/td-1/notes", () => ({
    markdownContent: "- SSO asked for",
    structuredNotes: [],
  }));

  const calls = await tldv.listReady("2026-01-01", "2026-01-03");
  // Both pages walked, and the organizer counts as an attendee.
  assert.deepEqual(
    calls.map((call) => call.id),
    ["td-1", "td-2"],
  );
  assert.equal(calls[0].attendees.length, 2);
  assert.equal(header("x-api-key"), "test-key");
  assert.equal(await tldv.transcript("td-1"), "**Ada:** We need SSO.");
  assert.equal(await tldv.notes("td-1"), "- SSO asked for");
});

check("tldv: a window with no `pages` field is still walked to the end", async () => {
  // `pages` is not a documented field name. Defaulting it to 1 meant an
  // absent or renamed one captured the newest page of a busy window and
  // reported a clean run.
  const { tldv } = await import("../scripts/collect/recorders/tldv.ts");
  routes.clear();
  route("GET https://pasta.tldv.io/v1alpha1/meetings", (url) => {
    const page = Number(new URL(url).searchParams.get("page"));
    return {
      results:
        page > 2
          ? []
          : [
              {
                id: `td-${page}`,
                name: "Acme call",
                happenedAt: "2026-01-02T16:00:00Z",
                invitees: [{ name: "Ada", email: "ada@acme.com" }],
              },
            ],
    };
  });

  const calls = await tldv.listReady("2026-01-01", "2026-01-03");
  assert.deepEqual(
    calls.map((one) => one.id),
    ["td-1", "td-2"],
  );
});

check("modjo: expand always passed, content not text, retention respected", async () => {
  const { modjo } = await import("../scripts/collect/recorders/modjo.ts");
  routes.clear();
  route("GET https://api.modjo.ai/v2/calls", (url) => {
    const query = new URL(url).searchParams;
    // Without this the response carries contactIds instead of contacts, and
    // the adapter would see no attendees at all.
    assert.equal(query.get("expand"), "contacts,users");
    return {
      data: [
        {
          id: 4021,
          title: "Acme call",
          startDate: "2026-01-02T17:00:00Z",
          transcriptRetentionStatus: "available",
          contacts: [{ name: "Ada", email: "ada@acme.com" }],
          users: [{ firstName: "Rep", lastName: "One", email: "rep@ourco.com" }],
        },
        {
          id: 4022,
          startDate: "2026-01-02T18:00:00Z",
          transcriptRetentionStatus: "deleted",
        },
      ],
      pagination: { page: 1, size: 100, total: 2 },
    };
  });
  route("GET https://api.modjo.ai/v2/calls/4021/transcript", () => ({
    data: [{ content: "We need SSO.", speaker: { name: "Ada", type: "contact" } }],
  }));
  route("GET https://api.modjo.ai/v2/calls/4021/summaries", () => ({
    data: [
      { templateTitle: "MEDDIC", answer: "Champion identified." },
      { templateTitle: "Pending", answer: null },
    ],
  }));

  const calls = await modjo.listReady("2026-01-01", "2026-01-03");
  // The reaped transcript is skipped; ids are strings from here on.
  assert.deepEqual(
    calls.map((call) => call.id),
    ["4021"],
  );
  assert.deepEqual(calls[0].attendees[1], {
    name: "Rep One",
    email: "rep@ourco.com",
  });
  assert.equal(await modjo.transcript("4021"), "**Ada:** We need SSO.");
  assert.equal(
    await modjo.notes("4021"),
    "**MEDDIC**\n\nChampion identified.",
  );
});

check("modjo: a window with no `pagination.total` is still walked", async () => {
  const { modjo } = await import("../scripts/collect/recorders/modjo.ts");
  routes.clear();
  route("GET https://api.modjo.ai/v2/calls", (url) => {
    const page = Number(new URL(url).searchParams.get("page"));
    return {
      data:
        page > 2
          ? []
          : [
              {
                id: 5000 + page,
                title: "Acme call",
                startDate: "2026-01-02T17:00:00Z",
                transcriptRetentionStatus: "available",
                contacts: [{ name: "Ada", email: "ada@acme.com" }],
              },
            ],
    };
  });

  const calls = await modjo.listReady("2026-01-01", "2026-01-03");
  assert.deepEqual(
    calls.map((one) => one.id),
    ["5001", "5002"],
  );
});

check("granola: thin list, detail for attendees, paged transcript", async () => {
  const { granola } = await import("../scripts/collect/recorders/granola.ts");
  routes.clear();
  route("GET https://public-api.granola.ai/v1/notes", (url) => {
    assert.ok(url.includes("created_after=2026-01-01T00%3A00%3A00Z"), url);
    return { notes: [{ id: "not_abc", title: "Acme call" }], hasMore: false };
  });
  route("GET https://public-api.granola.ai/v1/notes/not_abc", () => ({
    id: "not_abc",
    created_at: "2026-01-02T09:00:00Z",
    attendees: [{ name: "Ada", email: "ada@acme.com" }],
    summary_markdown: "## Summary\n\nThey liked it.",
  }));
  route(
    "GET https://public-api.granola.ai/v1/notes/not_abc/transcript",
    () => ({
      transcript: [
        { speaker: { name: "Ada" }, text: "We need SSO." },
        { speaker: { diarization_label: "Speaker B" }, text: "By when?" },
      ],
      hasMore: false,
    }),
  );

  const calls = await granola.listReady("2026-01-01", "2026-01-03");
  assert.deepEqual(calls, [
    {
      id: "not_abc",
      startAt: "2026-01-02T09:00:00Z",
      subject: "Acme call",
      attendees: [{ name: "Ada", email: "ada@acme.com" }],
    },
  ]);
  assert.equal(header("Authorization"), "Bearer test-key");
  assert.equal(
    await granola.transcript("not_abc"),
    "**Ada:** We need SSO.\n\n**Speaker B:** By when?",
  );
  // The summary came back on the detail fetch listReady already made.
  assert.equal(await granola.notes("not_abc"), "## Summary\n\nThey liked it.");
});

check("fathom: X-Api-Key, integer ids as strings, invitees as attendees", async () => {
  const { fathom } = await import("../scripts/collect/recorders/fathom.ts");
  routes.clear();
  route("GET https://api.fathom.ai/external/v1/meetings", () => ({
    items: [
      {
        recording_id: 8814,
        title: "Acme <> us",
        recording_start_time: "2026-01-02T15:00:00Z",
        calendar_invitees: [
          { name: "Ada", email: "ada@acme.com", is_external: true },
        ],
      },
      { recording_id: 8815, title: "no timestamp anywhere" },
    ],
    next_cursor: null,
  }));
  route(
    "GET https://api.fathom.ai/external/v1/recordings/8814/transcript",
    () => ({
      transcript: [
        { speaker: { display_name: "Ada" }, text: "Pricing is the issue." },
      ],
    }),
  );
  route("GET https://api.fathom.ai/external/v1/recordings/8814/summary", () => ({
    summary: { markdown_formatted: "- they want annual billing" },
  }));

  const calls = await fathom.listReady("2026-01-01", "2026-01-03");
  // The second meeting resolved to no timestamp, so it is dropped rather than
  // filed under today.
  assert.deepEqual(
    calls.map((call) => call.id),
    ["8814"],
  );
  assert.equal(header("X-Api-Key"), "test-key");
  assert.equal(
    await fathom.transcript("8814"),
    "**Ada:** Pricing is the issue.",
  );
  assert.equal(await fathom.notes("8814"), "- they want annual billing");
});

check("gong: basic pair, cursor only when more, speakerId joined to a party", async () => {
  const { gong } = await import("../scripts/collect/recorders/gong.ts");
  routes.clear();
  process.env["CALL_RECORDER_API_KEY"] = "ak:secret";
  try {
    let page = 0;
    route("POST https://api.gong.io/v2/calls/extensive", (_url, init) => {
      const body = JSON.parse(init.body);
      assert.equal(body.filter.fromDateTime, "2026-01-01T00:00:00Z");
      assert.equal(body.contentSelector.exposedFields.parties, true);
      page += 1;
      if (page === 1) {
        return {
          calls: [
            {
              metaData: {
                id: "7782342029982",
                started: "2026-01-02T10:00:00Z",
                title: "Acme discovery",
              },
              parties: [
                {
                  name: "Ada",
                  emailAddress: "ada@acme.com",
                  speakerId: "sp-1",
                  affiliation: "External",
                },
              ],
              content: { brief: "They evaluate us against Gong." },
            },
          ],
          records: { cursor: "page-2" },
        };
      }
      assert.equal(body.cursor, "page-2");
      return { calls: [], records: {} };
    });
    route("POST https://api.gong.io/v2/calls/transcript", (_url, init) => {
      assert.deepEqual(JSON.parse(init.body).filter.callIds, ["7782342029982"]);
      return {
        callTranscripts: [
          {
            callId: "7782342029982",
            transcript: [
              {
                speakerId: "sp-1",
                sentences: [{ text: "We looked at two others." }, { text: "Both lost." }],
              },
            ],
          },
        ],
      };
    });

    const calls = await gong.listReady("2026-01-01", "2026-01-03");
    assert.equal(calls.length, 1);
    assert.equal(calls[0].id, "7782342029982");
    assert.equal(
      header("Authorization"),
      `Basic ${Buffer.from("ak:secret").toString("base64")}`,
    );
    assert.equal(
      await gong.transcript("7782342029982"),
      "**Ada:** We looked at two others. Both lost.",
    );
    assert.equal(
      await gong.notes("7782342029982"),
      "They evaluate us against Gong.",
    );
  } finally {
    process.env["CALL_RECORDER_API_KEY"] = "test-key";
  }
});

check("fireflies: a GraphQL 200 carrying errors is not an empty window", async () => {
  const { fireflies } = await import(
    "../scripts/collect/recorders/fireflies.ts"
  );
  routes.clear();
  let answer = () => ({ errors: [{ message: "invalid api key" }] });
  route("POST https://api.fireflies.ai/graphql", () => answer());

  await assert.rejects(
    () => fireflies.listReady("2026-01-01", "2026-01-03"),
    /invalid api key/,
  );

  answer = () => ({
    data: {
      transcripts: [
        {
          id: "ff-1",
          title: "Acme call",
          dateString: "2026-01-02T11:00:00Z",
          meeting_attendees: [{ displayName: "Ada", email: "ada@acme.com" }],
          meeting_info: { summary_status: "processed" },
        },
        {
          id: "ff-2",
          dateString: "2026-01-02T12:00:00Z",
          meeting_info: { summary_status: "processing" },
        },
      ],
    },
  });
  const calls = await fireflies.listReady("2026-01-01", "2026-01-03");
  // ff-2 is still being processed, so it is not ready.
  assert.deepEqual(
    calls.map((call) => call.id),
    ["ff-1"],
  );
});

check("clari: two headers, status filter, personId joined to a participant", async () => {
  const { clari } = await import("../scripts/collect/recorders/clari.ts");
  routes.clear();
  process.env["CALL_RECORDER_API_KEY"] = "key:password";
  try {
    route("GET https://rest-api.copilot.clari.com/calls", () => ({
      calls: [
        {
          id: "call-1",
          status: "PROCESSED",
          title: "Acme renewal",
          time: "2026-01-02T14:00:00Z",
          externalParticipants: [
            { name: "Ada", email: "ada@acme.com", personId: 4211 },
          ],
        },
        { id: "call-2", status: "UNABLE_TO_JOIN", time: "2026-01-02T15:00:00Z" },
      ],
      pagination: { hasMore: false },
    }));
    route("GET https://rest-api.copilot.clari.com/call-details", () => ({
      call: {
        id: "call-1",
        externalParticipants: [
          { name: "Ada", email: "ada@acme.com", personId: 4211 },
        ],
        transcript: [{ text: "Renewal is approved.", personId: 4211 }],
        summary: { full_summary: "Renewal approved, paperwork next week." },
      },
    }));

    const calls = await clari.listReady("2026-01-01", "2026-01-03");
    assert.deepEqual(
      calls.map((call) => call.id),
      ["call-1"],
    );
    assert.equal(header("X-Api-Key"), "key");
    assert.equal(header("X-Api-Password"), "password");
    assert.equal(
      await clari.transcript("call-1"),
      "**Ada:** Renewal is approved.",
    );
    // The detail response was cached by transcript(), so notes() is free.
    assert.equal(
      await clari.notes("call-1"),
      "Renewal approved, paperwork next week.",
    );
  } finally {
    process.env["CALL_RECORDER_API_KEY"] = "test-key";
  }
});

let failed = 0;
for (const [name, run] of checks) {
  try {
    await run();
    console.log(`ok   ${name}`);
  } catch (error) {
    failed += 1;
    console.error(`FAIL ${name}\n     ${error.message.split("\n").join("\n     ")}`);
  }
}

if (failed > 0) {
  console.error(`${failed} contract check(s) failed`);
  console.error(`the pipeline checks left their tree at ${tree}`);
  process.exit(1);
}
rmSync(tree, { recursive: true, force: true });
console.log(`${checks.length} contract checks passed`);
