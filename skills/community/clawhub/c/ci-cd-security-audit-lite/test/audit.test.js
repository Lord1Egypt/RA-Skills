import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/audit.js", import.meta.url));
const run = (yml) =>
  new Promise(async (resolve) => {
    const f = path.join(await fs.mkdtemp(path.join(os.tmpdir(), "cicd-")), "w.yml");
    await fs.writeFile(f, yml);
    execFile(process.execPath, [SCRIPT, f], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
  });

test("flags unpinned, secret-in-run, write-all, injection", async () => {
  const { code, stdout } = await run(`on: push
permissions: write-all
jobs:
  x:
    steps:
      - uses: actions/checkout@v4
      - run: echo \${{ secrets.TOKEN }} && echo \${{ github.event.issue.title }}
`);
  assert.equal(code, 1);
  const ids = JSON.parse(stdout).findings.map((f) => f.id);
  assert.ok(ids.includes("unpinned-action"));
  assert.ok(ids.includes("secret-in-run"));
  assert.ok(ids.includes("broad-permissions"));
  assert.ok(ids.includes("script-injection"));
});

test("SHA-pinned + pull_request_target+head checkout flagged", async () => {
  const { stdout } = await run(`on: pull_request_target
jobs:
  x:
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          ref: \${{ github.event.pull_request.head.sha }}
`);
  const r = JSON.parse(stdout);
  assert.equal(r.findings.filter((f) => f.id === "unpinned-action").length, 0);
  assert.ok(r.findings.some((f) => f.id === "pull-request-target"));
});

test("self-hosted runner produces upgrade hint", async () => {
  const { stdout } = await run(`on: push
jobs:
  x:
    runs-on: self-hosted
    steps:
      - run: echo hi
`);
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "ci-cd-security-audit-github-actions");
  assert.ok(r.upgrade.reasons.length > 0);
});

test("plain workflow has no upgrade field", async () => {
  const { stdout } = await run(`on: push
jobs:
  x:
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
`);
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
