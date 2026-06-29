import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import path from "node:path";

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cliPath = path.join(rootDir, "bin", "apitweet.js");

function runCli(args) {
  return spawnSync(process.execPath, [cliPath, ...args], {
    cwd: rootDir,
    encoding: "utf8",
  });
}

test("trending tweets builds the global trending tweets request", () => {
  const result = runCli([
    "--dry-run",
    "trending",
    "tweets",
    "--country",
    "United States",
    "--topic",
    "Sports",
    "--content",
    "NFL",
    "--count",
    "50",
  ]);

  assert.equal(result.status, 0, result.stderr);
  const preview = JSON.parse(result.stdout);
  assert.equal(preview.method, "GET");
  assert.equal(
    preview.url,
    "https://apitweet.com/api/twitter/global-trending/tweets?country=United+States&topic=Sports&content=NFL&count=50",
  );
});
