/**
 * The recorder contract, and the provider-agnostic half of call capture.
 *
 * Nothing in this file knows which vendor records your calls. It defines what
 * a recorder must be able to do, and it holds everything that is the same
 * whoever answers: deduplication, account slugging, file layout, the rolling
 * window, and the run itself.
 *
 * To support a recorder that is not in `recorders/`, write one object
 * satisfying `Recorder` beside the ones there and register it. The type is
 * what keeps the boundary honest, in both directions: an adapter that cannot
 * satisfy it is telling you something real about the API, and no adapter can
 * reach into the pipeline below because none of them import it.
 */
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { join, relative, resolve } from "node:path";

import { INTERNAL_DOMAIN } from "./config";

/** One call, normalized. Producing these is the adapter's job. */
export type Call = {
  /** The recorder's own id. The only idempotency key this system has. */
  id: string;
  /** ISO timestamp. Its date half becomes the filename and the frontmatter. */
  startAt: string;
  subject: string;
  attendees: { email?: string; name?: string }[];
};

export type Recorder = {
  /**
   * A slug, and load-bearing in a way that is easy to miss: it is written into
   * every file's `source:` line AND compiled into the regex that reads those
   * lines back for deduplication. One field feeds both, so they cannot drift.
   * Two literals that drift is the failure that re-captures the whole window
   * every morning without ever erroring.
   */
  provider: string;

  /**
   * Every call in the window whose transcript the recorder has finished
   * processing, normalized. Readiness is decided HERE, in the recorder's own
   * vocabulary, because there is no portable spelling of it: Avoma has `state`
   * plus `transcript_ready`, Gong has neither.
   *
   * Both dates are YYYY-MM-DD. Paginate to the end before returning.
   */
  listReady(from: string, to: string): Promise<Call[]>;

  /** The transcript as markdown, speaker-attributed, or null if there is none. */
  transcript(id: string): Promise<string | null>;

  /** The recorder's own AI notes, or null. The fallback when there is no transcript. */
  notes(id: string): Promise<string | null>;
};

// Auth is NOT in this file on purpose. Bearer, Basic and a signed GraphQL POST
// are three different things, and pretending otherwise is how the "agnostic"
// half ends up carrying one vendor's header. What IS shared is the retrying:
// rate limits and timeouts behave the same everywhere, and every adapter
// should get the backoff for free rather than reinventing it badly.
export class HttpError extends Error {
  constructor(
    readonly status: number,
    body: string,
  ) {
    super(`HTTP ${status}: ${body}`);
  }
}

/**
 * Something about the run's configuration is wrong — a missing credential, an
 * unknown slug passed to `--recorder=`. Separate from every other error so
 * `calls.ts` can print it as a message and exit 1: a stack trace pointing into
 * an adapter is the wrong thing to read when the answer is "create the
 * workspace variable".
 */
export class ConfigError extends Error {}

/**
 * The recorder's credential, read when a request is about to be made rather
 * than at import — `recorders/index.ts` imports every adapter to resolve a
 * slug, so an import-time check in one would fail the runs of the other eight.
 */
export function recorderKey(): string {
  const key = process.env["CALL_RECORDER_API_KEY"];
  if (key === undefined || key === "") {
    throw new ConfigError(
      "CALL_RECORDER_API_KEY is not set. Deployed, it is a workspace environment " +
        "variable the harness inherits: `cargo-ai workspaceManagement envVar list` " +
        "shows whether the workspace holds one. Export it to run this by hand.",
    );
  }
  return key;
}

/**
 * The same credential where the recorder wants two values — Gong's access key
 * and secret, Clari Copilot's key and password. Set it as `<first>:<second>`,
 * keeping one variable name whatever records your calls. Split on the FIRST
 * colon only: the second half is a secret and secrets contain colons.
 */
export function recorderKeyPair(shape: string): [string, string] {
  const raw = recorderKey();
  const split = raw.indexOf(":");
  if (split < 1 || split === raw.length - 1) {
    throw new ConfigError(
      `CALL_RECORDER_API_KEY must be ${shape} for this recorder, and this one ` +
        `has no colon with a value on both sides of it.`,
    );
  }
  return [raw.slice(0, split), raw.slice(split + 1)];
}

export const sleep = (ms: number): Promise<void> =>
  new Promise((done) => setTimeout(done, ms));

/**
 * Every argument the collector accepts, checked before anything runs.
 *
 * A flag it does not know is a stop rather than something to ignore:
 * `--dry-run` typed as `--dryrun` was a real capture, and `--recorder granola`
 * without the `=` ran whatever `config.ts` names. Both are a run that did the
 * wrong thing while looking exactly like the one that was asked for.
 */
export function checkFlags(argv: readonly string[]): void {
  const unknown = argv.filter(
    (argument) =>
      !["--list", "--dry-run"].includes(argument) &&
      !argument.startsWith("--recorder="),
  );
  if (unknown.length > 0) {
    throw new ConfigError(
      `unknown argument(s): ${unknown.join(", ")}\n` +
        `this takes --list, --dry-run and --recorder=<slug>.`,
    );
  }
}

/**
 * How long to wait after a 429. Most vendors send no `Retry-After` at all, and
 * `Number(null)` is 0 — so reading the header without this would retry four
 * times instantly and spend the rest of the rate limit. Clamped at the top
 * end too: a vendor asking for an hour would hold the whole run open.
 */
export function backoffSeconds(header: string | null, attempt: number): number {
  const asked = header === null ? Number.NaN : Number(header);
  if (Number.isFinite(asked) && asked > 0) return Math.min(asked, 300);
  return 2 ** (attempt + 3);
}

/**
 * Fetch JSON with 429 backoff and a timeout. The caller supplies the whole
 * request — method, headers, body — so the auth scheme stays the adapter's.
 */
export async function fetchJson<T>(
  url: string,
  init: RequestInit,
  maxAttempts = 5,
): Promise<T> {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const response = await fetch(url, {
      ...init,
      signal: AbortSignal.timeout(120_000),
    });

    if (response.status === 429 && attempt < maxAttempts - 1) {
      const waitSeconds = backoffSeconds(
        response.headers.get("retry-after"),
        attempt,
      );
      console.error(`429, backing off ${waitSeconds.toFixed(0)}s`);
      await sleep(waitSeconds * 1000);
      continue;
    }

    if (!response.ok)
      throw new HttpError(response.status, await response.text());
    return (await response.json()) as T;
  }

  throw new Error(`request exhausted retries: ${url}`);
}

/**
 * A page counter that stops a paginated read that never terminates. Every
 * loop here ends when the vendor stops handing back a cursor, so a vendor that
 * echoes one — or ignores an offset and returns a full page for ever — would
 * otherwise spin until someone notices the quota is gone.
 *
 * Call it once per request. It throws rather than returning what it has: a
 * truncated window that looks complete is the failure this whole collector is
 * arranged to avoid.
 */
export function pageGuard(provider: string, limit = 200): () => void {
  let pages = 0;
  return () => {
    pages++;
    if (pages > limit) {
      throw new Error(
        `${provider}: pagination did not terminate after ${limit} pages. ` +
          `The window is too wide for one run, or the vendor is repeating a ` +
          `cursor — either way this run captured nothing rather than part.`,
      );
    }
  };
}

/** Space out requests: a 429 storm on a backfill day half-captures the run. */
export const PACE_MS = Number(process.env["CALL_CAPTURE_PACE_MS"] ?? "1000");

// This file sits at scripts/<cookbook>/collect/, so the repo root is three up.
// Resolved from the file rather than from cwd: the agent may run it from
// anywhere in the working tree, and a cwd-relative path would then write the
// cadence layer into a subdirectory nobody reads.
const ROOT = resolve(import.meta.dirname, "..", "..", "..");
const LOG_DIR = join(ROOT, "cadence", "log");
const RAW_DIR = join(LOG_DIR, "raw", "calls");

// Three days, not one. A transcript is not ready when a call ends, so a
// one-day window drops every call the recorder was still processing at the
// cron minute — and because the window only ever moves forward, those calls
// are never seen again. The overlap costs nothing: ids already on disk are
// skipped before any transcript is fetched.
const LOOKBACK_DAYS = Number(process.env["CALL_CAPTURE_LOOKBACK_DAYS"] ?? "3");

// Applied here rather than in an adapter because it has to mean the same thing
// whoever recorded the call. `config.ts` is where the domain is set.

// A personal address is not an account. Slugging by domain would file every
// unrelated gmail.com guest under one "gmail" account, and the scribe would
// then read a stranger's history as this account's.
const CONSUMER_DOMAINS = new Set([
  "gmail.com",
  "googlemail.com",
  "outlook.com",
  "hotmail.com",
  "yahoo.com",
  "icloud.com",
  "me.com",
  "proton.me",
  "protonmail.com",
]);

function isoDateOffset(days: number): string {
  const date = new Date();
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

/** The characters an id may use, because the reader below is a regex. */
const ID_PATTERN = /^[\w.@|-]+$/;

/**
 * Every id already recorded anywhere under cadence/log/ — raw captures AND
 * scribed entries. Reading both is what stops a call being re-captured months
 * after it was scribed and its raw file archived away.
 */
function capturedIds(provider: string): Set<string> {
  // Escaped: a slug carrying a `.` would otherwise match any character there
  // and recognise another recorder's captures as this one's.
  const slug = provider.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`source: ${slug} ([\\w.@|-]+)`, "g");
  const seen = new Set<string>();
  if (!existsSync(LOG_DIR)) return seen;

  for (const entry of readdirSync(LOG_DIR, {
    recursive: true,
    withFileTypes: true,
  })) {
    if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
    const text = readFileSync(join(entry.parentPath, entry.name), "utf8");
    for (const match of text.matchAll(pattern)) seen.add(match[1]!);
  }

  return seen;
}

/**
 * The domain half of an address, or undefined when there is nothing usable
 * there. Vendors send `""`, a display name, or a bare label for a participant
 * they never identified, and every adapter passes the value through — so this
 * is where that has to be survivable rather than nine places.
 */
function emailDomain(attendee: { email?: string }): string | undefined {
  const address = attendee.email ?? "";
  const at = address.lastIndexOf("@");
  if (at < 1 || at === address.length - 1) return undefined;
  return address.slice(at + 1).toLowerCase();
}

/**
 * Matched on the domain, not as a suffix of the address. `endsWith` here would
 * read `her@notexample.com` as internal, and a short internal domain makes
 * that routine: `me.com` swallows every `acme.com` contact. A subdomain of
 * your own domain IS you, so those still count as internal.
 */
function isInternal(domain: string): boolean {
  return domain === INTERNAL_DOMAIN || domain.endsWith(`.${INTERNAL_DOMAIN}`);
}

function externalAttendees(call: Call): { email?: string; name?: string }[] {
  return call.attendees.filter((attendee) => {
    const domain = emailDomain(attendee);
    return domain !== undefined && !isInternal(domain);
  });
}

function accountSlug(call: Call): string {
  const domains = [
    ...new Set(
      externalAttendees(call)
        .map((attendee) => emailDomain(attendee))
        .filter(
          (domain): domain is string =>
            domain !== undefined && !CONSUMER_DOMAINS.has(domain),
        ),
    ),
  ].sort();

  const base = domains[0]?.split(".")[0] ?? "unknown";
  return base.replace(/[^a-z0-9-]/g, "") || "unknown";
}

/** Never overwrite: two calls with one account on one day both keep their file. */
function freePath(day: string, slug: string): string {
  let path = join(RAW_DIR, `${day}-${slug}.md`);
  for (let n = 2; existsSync(path); n++) {
    path = join(RAW_DIR, `${day}-${slug}-${n}.md`);
  }
  return path;
}

function writeRaw(provider: string, call: Call, body: string): string {
  // Written now, read back by capturedIds() with a regex. An id carrying
  // anything outside that class would be read back truncated, which reads as
  // "never captured" and re-captures the call every morning.
  if (!ID_PATTERN.test(call.id)) {
    throw new Error(
      `${provider} id "${call.id}" has characters the deduplication key cannot ` +
        `round-trip. Widen ID_PATTERN and capturedIds() together, or normalize ` +
        `the id in the adapter.`,
    );
  }

  const day = call.startAt.slice(0, 10);
  const path = freePath(day, accountSlug(call));
  const attendees = call.attendees
    .map((attendee) => attendee.name ?? attendee.email ?? "unknown")
    .join(", ");

  const frontmatter = [
    "---",
    `title: "RAW: ${call.subject.replace(/"/g, "'")}"`,
    `date: ${day}`,
    `attendees: [${attendees}]`,
    // The written half of the idempotency key. Its reader is capturedIds(),
    // and both are built from `provider` so they cannot disagree.
    `source: ${provider} ${call.id}`,
    "status: raw, awaiting scribe",
    "---",
    "",
  ].join("\n");

  writeFileSync(path, `${frontmatter}\n${body}\n`);
  return relative(ROOT, path);
}

/**
 * Run one capture pass. `--dry-run` reports what it would take and writes
 * nothing: the first thing to run against a freshly written adapter, because
 * it exercises the list call and the readiness filter without putting anything
 * in the repository you would then have to unpick.
 */
export async function capture(recorder: Recorder): Promise<void> {
  const dryRun = process.argv.includes("--dry-run");
  if (!dryRun) mkdirSync(RAW_DIR, { recursive: true });

  const from = isoDateOffset(-LOOKBACK_DAYS);
  const to = isoDateOffset(0);
  const captured = capturedIds(recorder.provider);
  const ready = await recorder.listReady(from, to);

  const pending = ready.filter((call) => {
    if (captured.has(call.id)) return false;

    // Said out loud, because the alternative is a call quietly filed as
    // internal on the strength of an address the vendor mangled.
    const unusable = call.attendees.filter(
      (attendee) =>
        attendee.email !== undefined &&
        attendee.email !== "" &&
        emailDomain(attendee) === undefined,
    );
    if (unusable.length > 0) {
      console.error(
        `${call.id}: ${unusable.length} attendee address(es) are not addresses, ignored`,
      );
    }

    return externalAttendees(call).length > 0;
  });

  console.log(
    `${recorder.provider} ${from}..${to}: ${ready.length} ready, ` +
      `${captured.size} already captured, ${pending.length} pending`,
  );

  if (dryRun) {
    for (const call of pending) {
      console.log(
        `would capture: ${call.startAt.slice(0, 10)}-${accountSlug(call)} — ${call.subject}`,
      );
    }
    console.log("dry run, nothing written");
    return;
  }

  let written = 0;
  for (const call of pending) {
    const body =
      (await recorder.transcript(call.id)) ?? (await recorder.notes(call.id));
    if (body === null) {
      console.error(
        `skip ${call.id}: no transcript or notes, next run retries`,
      );
      continue;
    }
    console.log(`raw: ${writeRaw(recorder.provider, call, body)}`);
    written++;
  }

  console.log(`captured ${written} new call(s) into cadence/log/raw/calls/`);
}
