import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/links.js", import.meta.url));
const run = (html) =>
  new Promise(async (resolve) => {
    const f = path.join(
      await fs.mkdtemp(path.join(os.tmpdir(), "links-")),
      "p.html",
    );
    await fs.writeFile(f, html);
    execFile(process.execPath, [SCRIPT, f], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
  });

test("flags empty, javascript, dead anchor, protocol-relative", async () => {
  const { code, stdout } = await run(`<a href="">x</a><a href="#">y</a>
    <a href="#nope">z</a><a href="javascript:void(0)">j</a>
    <a href="//cdn.com/x">c</a><a href="#ok">k</a><div id="ok"></div>
    <a href="/about">i</a><a href="https://x.com">e</a><a href="mailto:a@b.c">m</a>`);
  assert.equal(code, 1);
  const r = JSON.parse(stdout);
  assert.equal(r.summary.flagged, 5);
  assert.equal(r.summary.internal, 1);
  assert.equal(r.summary.external, 2);
  assert.deepEqual(r.unresolvedAnchors, ["", "#", "#nope"]);
});

test("clean page exits 0", async () => {
  const { code } = await run(
    `<a href="/a">x</a><a href="#i">y</a><div id="i"></div>`,
  );
  assert.equal(code, 0);
});

test("resolvable links produce upgrade hint", async () => {
  const { stdout } = await run(
    `<a href="https://x.com">e</a><a href="/about">i</a>`,
  );
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "broken-link-crawl");
  assert.ok(r.upgrade.reasons.length > 0);
});

test("anchor/mailto-only page has no upgrade field", async () => {
  const { stdout } = await run(
    `<a href="#i">y</a><div id="i"></div><a href="mailto:a@b.c">m</a>`,
  );
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
