import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), ".."),
  tool = path.join(root, "scripts/calibredb_apply.mjs");
function fixture(t, control = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibre-apply-test-")),
    lib = path.join(dir, "library 日本語");
  fs.mkdirSync(lib);
  fs.writeFileSync(path.join(lib, "metadata.db"), "");
  const fake = path.join(dir, "calibredb");
  fs.copyFileSync(path.join(root, "tests/fixtures/fake-calibredb.mjs"), fake);
  fs.chmodSync(fake, 0o700);
  const config = path.join(dir, "config.json");
  fs.writeFileSync(config, JSON.stringify({ reading_script: "katakana" }));
  const db = path.join(lib, "fake.json");
  const book = {
    id: 1,
    uuid: "u1",
    title: "Old",
    authors: "Alice & Bob",
    author_sort: "Alice & Bob",
    title_sort: "Old",
    series: "S",
    series_index: 1,
    tags: ["Keep"],
    publisher: "P",
    pubdate: "2020-01-02T00:00:00Z",
    languages: ["eng"],
    comments: "<p>Existing $& comment</p>",
  };
  fs.writeFileSync(
    db,
    JSON.stringify({
      books: { 1: book, 2: { ...book, id: 2, uuid: "u2" } },
      sets: 0,
      calls: [],
      ...control,
    }),
  );
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const env = { PATH: process.env.PATH, HOME: dir, LANG: "C.UTF-8" };
  const base = [
    tool,
    "--config",
    config,
    "--with-library",
    lib,
    "--state-dir",
    path.join(dir, "state"),
    "--calibredb",
    fake,
  ];
  function run(input = "", args = [], extra = {}) {
    return spawnSync(process.execPath, [...base, ...args], {
      input,
      encoding: "utf8",
      env: { ...env, ...extra },
      timeout: 20000,
    });
  }
  function plan(record, name = "plan.json", extra = {}) {
    const p = path.join(dir, name),
      r = run(
        (Array.isArray(record) ? record : [record]).map((x) => JSON.stringify(x)).join("\n"),
        ["--plan-file", p],
        extra,
      );
    return { p, r };
  }
  return {
    dir,
    lib,
    db,
    run,
    plan,
    state: () => JSON.parse(fs.readFileSync(db)),
    apply: (p) => run("", ["--apply", "--plan-file", p]),
  };
}
function json(r) {
  assert.ok(r.stdout, r.stderr);
  return JSON.parse(r.stdout);
}
test("full input validation prevents all writes and rejects duplicates/unknowns", (t) => {
  const f = fixture(t);
  for (const rows of [
    [
      { id: 1, title: "New" },
      { id: 2, bogus: true },
    ],
    [
      { id: 1, title: "A" },
      { id: 1, title: "B" },
    ],
    [{ id: 0, title: "bad" }],
    [{ id: "9007199254740993", title: "bad" }],
    [{ id: 1, tags_merge: false }],
  ]) {
    assert.notEqual(f.plan(rows, Math.random() + ".json").r.status, 0);
  }
  assert.equal(f.state().calls.length, 0);
});
test("plan, approved apply, receipt and no-op plan preserve comments/tags", (t) => {
  const f = fixture(t);
  const { p, r } = f.plan({
    id: 1,
    authors: ["Doe, Jane", "Research Team"],
    analysis: { summary: "<unsafe> & $1", highlights: ["A&B"] },
    tags: ["new"],
  });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /&lt;unsafe&gt;/);
  assert.match(r.stdout, /Research Team/);
  assert.equal(f.state().sets, 0);
  const applied = f.apply(p);
  assert.equal(applied.status, 0, applied.stdout + applied.stderr);
  assert.equal(json(applied).summary.applied, 1);
  const receipt = json(applied).receipt_file;
  const events = fs.readFileSync(receipt, "utf8").trim().split("\n").map(JSON.parse);
  assert.ok(events.some((x) => x.event === "intent"));
  assert.equal(events.at(-1).event, "finished");
  assert.match(f.state().books[1].comments, /Existing \$& comment/);
  assert.deepEqual(f.state().books[1].tags, ["Keep", "new"]);
  assert.notEqual(f.apply(p).status, 0);
  assert.equal(f.state().sets, 1);
  const noop = f.plan({ id: 1, tags: [] }, "noop.json");
  assert.equal(json(noop.r).summary.no_op, 1);
  assert.equal(f.apply(noop.p).status, 0);
  assert.equal(f.state().sets, 1);
});
test("tags_merge false clears/replaces, with no lost flag", (t) => {
  const f = fixture(t);
  const { p, r } = f.plan({ id: 1, tags: [], tags_merge: false });
  assert.equal(r.status, 0, r.stderr);
  assert.equal(f.apply(p).status, 0);
  assert.deepEqual(f.state().books[1].tags, []);
});
test("ISO aliases, explicit UTC dates and quoted sort survive readback", (t) => {
  const f = fixture(t);
  const { p, r } = f.plan({
    id: 1,
    languages: ["ja", "en"],
    pubdate: "2024-02-29",
    title_sort: "O'Neil 日本語",
  });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /2024-02-29T00:00:00Z/);
  assert.equal(f.apply(p).status, 0);
  assert.deepEqual(f.state().books[1].languages, ["jpn", "eng"]);
});
test("invalid dates, language codes, marker pairs and ambiguous delimiters fail before reading", (t) => {
  const f = fixture(t);
  for (const rec of [
    { pubdate: "2023-02-29" },
    { languages: ["xxx"] },
    { tags: ["one,two"] },
    { tags_merge: "false", tags: [] },
    { comments_html: "<b>no markers</b>" },
    { comments: "<!-- OC_ANALYSIS_START -->" },
    { title: "bad\0value" },
    { authors: ["Research & Development"] },
    { authors: ["Research | Development"] },
  ])
    assert.notEqual(f.plan({ id: 1, ...rec }, Math.random() + ".json").r.status, 0);
  assert.equal(f.state().calls.length, 0);
});
test("changed unrelated title and later-row UUID stop the whole batch", (t) => {
  const f = fixture(t);
  const { p, r } = f.plan([
    { id: 1, tags: ["x"] },
    { id: 2, tags: ["y"] },
  ]);
  assert.equal(r.status, 0, r.stderr);
  const s = f.state();
  s.books[2].uuid = "changed";
  s.books[1].title = "Changed";
  fs.writeFileSync(f.db, JSON.stringify(s));
  const applied = f.apply(p);
  assert.notEqual(applied.status, 0);
  assert.equal(json(applied).phase, "preflight");
  assert.equal(f.state().sets, 0);
});
test("tampered plan rejected without mutation", (t) => {
  const f = fixture(t);
  const { p } = f.plan({ id: 1, title: "New" });
  const s = JSON.parse(fs.readFileSync(p));
  s.rows[0].after.title = "tamper";
  fs.writeFileSync(p, JSON.stringify(s));
  assert.notEqual(f.apply(p).status, 0);
  assert.equal(f.state().sets, 0);
});
test("proposal library/UUID binding rejects cross-target input", (t) => {
  const f = fixture(t);
  assert.notEqual(f.plan({ id: 1, expected_uuid: "wrong", title: "New" }).r.status, 0);
  assert.equal(f.state().sets, 0);
});
test("write failure/lying success retained and no automatic retry", (t) => {
  for (const control of [{ failSet: true }, { lieSet: true }]) {
    const f = fixture(t, control);
    const { p, r } = f.plan([
      { id: 1, title: "New" },
      { id: 2, title: "Other" },
    ]);
    assert.equal(r.status, 0, r.stderr);
    const applied = f.apply(p);
    assert.notEqual(applied.status, 0);
    assert.equal(json(applied).summary.skipped, 1);
    assert.equal(f.state().sets, 1);
    assert.notEqual(f.apply(p).status, 0);
    assert.equal(f.state().sets, 1);
  }
});
test("password only travels through stdin, and missing executable is not success", (t) => {
  const f = fixture(t);
  let { r } = f.plan({ id: 1, title: "New" }, "secret.json", {
    CALIBRE_USERNAME: "user",
    CALIBRE_PASSWORD: "synthetic-secret",
  });
  assert.equal(r.status, 0, r.stderr);
  assert.ok(!r.stdout.includes("synthetic-secret"));
  assert.ok(!JSON.stringify(f.state().calls).includes("synthetic-secret"));
  assert.equal(f.state().stdin, "synthetic-secret\n");
  r = f.run('{"id":1,"title":"New"}', ["--calibredb", path.join(f.dir, "missing")]);
  assert.notEqual(r.status, 0);
  assert.equal(f.state().sets, 0);
});
