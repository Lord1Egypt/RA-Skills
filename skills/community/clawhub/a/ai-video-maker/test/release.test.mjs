import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = fileURLToPath(new URL("../..", import.meta.url));
test("downloadable release has consistent metadata and runs H3 from outside the repository", async () => {
  const dir = await mkdtemp(resolve(tmpdir(), "aivideo-artifact-test-"));
  try {
    execFileSync(process.execPath, [resolve(root, "scripts/build-skill-release.mjs"), dir]);
    const sourcePackage = JSON.parse(
      await readFile(resolve(root, "ai-video-maker/package.json"), "utf8"),
    );
    const name = `ai-video-maker-${sourcePackage.version}.tgz`;
    const archive = await readFile(resolve(dir, name));
    const checksum = await readFile(resolve(dir, `${name}.sha256`), "utf8");
    assert.equal(checksum.split(" ")[0], createHash("sha256").update(archive).digest("hex"));
    const files = execFileSync("tar", ["-tzf", resolve(dir, name)], { encoding: "utf8" });
    assert.doesNotMatch(files, /\.env|node_modules|\/test\/|verify-release/);
    execFileSync("tar", ["-xzf", resolve(dir, name), "-C", dir]);
    const packedRoot = resolve(dir, "package");
    for (const file of ["package.json", "_meta.json", "clawhub.manifest.json"]) {
      const json = JSON.parse(await readFile(resolve(packedRoot, file), "utf8"));
      assert.equal(json.version, sourcePackage.version, file);
    }
    const originalSkill = await readFile(resolve(root, "ai-video-maker/SKILL.md"), "utf8");
    assert.equal(await readFile(resolve(packedRoot, "SKILL.md"), "utf8"), originalSkill);
    // Import a network stub explicitly: no credentials, providers, or paid tasks are used.
    const mockPath = resolve(root, "ai-video-maker/test/mock-release-fetch.mjs");
    function run(args, scenario = "success") {
      const result = spawnSync(
        process.execPath,
        ["--import", mockPath, resolve(packedRoot, "scripts/run-workflow.mjs"), ...args],
        {
          cwd: dir,
          encoding: "utf8",
          env: {
            ...process.env,
            AIVIDEO_API_KEY: "artifact-test-only",
            AIVIDEO_AGENT_PLATFORM: "codex",
            AIVIDEO_TEST_SCENARIO: scenario,
            AIVIDEO_MAX_RETRIES: "0",
          },
        },
      );
      assert.equal(result.stderr, "");
      assert.doesNotMatch(result.stdout, /artifact-test-only/);
      return { code: result.status, output: JSON.parse(result.stdout) };
    }
    assert.equal(run(["--action", "doctor"]).output.ok, true);
    const payload = JSON.stringify({
      content: "A cinematic candle on a wooden table",
      duration: 5,
      resolution: "720p",
      tier: "turbo",
      aspectRatio: "16:9",
    });
    const quote = run(["--action", "quote", "--model", "minimax", "--payload", payload]);
    assert.equal(quote.code, 0);
    assert.equal(quote.output.data.credits, 15);
    const args = [
      "--model",
      "minimax",
      "--payload",
      payload,
      "--maxCredits",
      "15",
      "--idempotencyKey",
      "artifact-first-video",
    ];
    const generated = run(args);
    assert.equal(generated.code, 0);
    assert.equal(generated.output.data.output.url, "https://example.test/video.mp4");
    assert.equal(generated.output.taskId, "artifact-task");
    const overBudget = run(args, "expensive");
    assert.equal(overBudget.code, 1);
    assert.equal(overBudget.output.errorCode, "BUDGET_EXCEEDED");
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});
