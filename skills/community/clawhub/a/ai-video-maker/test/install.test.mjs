import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { promisify } from "node:util";
import { before, after, test } from "node:test";

const exec = promisify(execFile);
const root = fileURLToPath(new URL("../..", import.meta.url));
let installSkill;
let archive;
let checksum;
let releaseDir;
let version;
before(async () => {
  releaseDir = await mkdtemp(resolve(tmpdir(), "skill-release-"));
  await exec(process.execPath, [resolve(root, "scripts/build-skill-release.mjs"), releaseDir]);
  ({ version } = JSON.parse(await readFile(resolve(root, "ai-video-maker/package.json"), "utf8")));
  archive = await readFile(resolve(releaseDir, `ai-video-maker-${version}.tgz`));
  checksum = await readFile(resolve(releaseDir, `ai-video-maker-${version}.tgz.sha256`), "utf8");
  ({ installSkill } = await import(
    pathToFileURL(resolve(releaseDir, `install-${version}.mjs`)).href
  ));
});
after(async () => {
  if (releaseDir) await rm(releaseDir, { recursive: true, force: true });
});
const fetcher = async (url) => new Response(url.endsWith(".sha256") ? checksum : archive);

for (const platform of ["codex", "claude", "openclaw"]) {
  test(`${platform} installs safely and quotes from a fresh directory`, async () => {
    const directory = await mkdtemp(resolve(tmpdir(), "skill install test "));
    try {
      const destination = await installSkill(platform, { baseDirectory: directory, fetcher });
      assert.match(
        await readFile(resolve(destination, "SKILL.md"), "utf8"),
        /First-video onboarding/,
      );
      await assert.rejects(
        installSkill(platform, { baseDirectory: directory, fetcher }),
        /Already installed/,
      );
      const { connect } = await import(
        pathToFileURL(resolve(destination, "scripts/connect.mjs")).href
      );
      await connect("artifact-test-only", {
        directory: resolve(directory, "private-connection"),
        fetcher: async (url) => {
          assert.equal(url, "https://aivideomaker.ai/api/v1/account");
          return Response.json({ ok: true, key: { status: "ACTIVE" }, currentBalance: 50 });
        },
      });
      const result = await exec(
        process.execPath,
        [
          "--import",
          resolve(root, "ai-video-maker/test/mock-release-fetch.mjs"),
          resolve(destination, "scripts/run-workflow.mjs"),
          "--action",
          "quote",
          "--model",
          "minimax",
          "--payload",
          JSON.stringify({ content: "A candle", duration: 5, resolution: "720p", tier: "turbo" }),
        ],
        {
          cwd: directory,
          env: {
            ...process.env,
            AIVIDEO_API_KEY: "artifact-test-only",
            AIVIDEO_AGENT_PLATFORM: platform,
            AIVIDEO_MAX_RETRIES: "0",
          },
        },
      );
      assert.equal(JSON.parse(result.stdout).data.credits, 15);
      assert.doesNotMatch(result.stdout, /artifact-test-only/);
    } finally {
      await rm(directory, { recursive: true, force: true });
    }
  });
}

test("rejects altered downloads and unsupported clients without installing", async () => {
  const directory = await mkdtemp(resolve(tmpdir(), "skill-checksum-"));
  try {
    await assert.rejects(
      installSkill("codex", {
        baseDirectory: directory,
        fetcher: async (url) => new Response(url.endsWith(".sha256") ? "0".repeat(64) : archive),
      }),
      /Checksum mismatch/,
    );
    await assert.rejects(readFile(resolve(directory, ".agents/skills/ai-video-maker/SKILL.md")));
    await assert.rejects(
      installSkill("other", { baseDirectory: directory, fetcher }),
      /Choose codex, claude, or openclaw/,
    );
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("the piped Node installer works without network access", async () => {
  const directory = await mkdtemp(resolve(tmpdir(), "skill cli test "));
  try {
    const mock = resolve(directory, "mock-download.mjs");
    await writeFile(
      mock,
      `import { readFile } from 'node:fs/promises';
      globalThis.fetch = async (url) => {
        if (!String(url).startsWith('https://aivideomaker.ai/skills/')) throw new Error('Unexpected URL');
        return new Response(await readFile(${JSON.stringify(releaseDir)} + '/' + new URL(url).pathname.split('/').pop()));
      };`,
    );
    const installer = await readFile(resolve(releaseDir, `install-${version}.mjs`));
    const { spawn } = await import("node:child_process");
    const child = spawn(process.execPath, ["--input-type=module", "-", "codex"], {
      cwd: directory,
      env: { ...process.env, NODE_OPTIONS: `--import=${pathToFileURL(mock).href}` },
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (data) => {
      stdout += data;
    });
    child.stderr.on("data", (data) => {
      stderr += data;
    });
    const exit = new Promise((resolveExit, reject) => {
      child.on("error", reject);
      child.on("close", resolveExit);
    });
    child.stdin.end(installer);
    assert.equal(await exit, 0, stderr);
    assert.ok(stdout.includes(`Installed AI Video Maker v${version}`));
    const installed = JSON.parse(
      await readFile(resolve(directory, ".agents/skills/ai-video-maker/package.json"), "utf8"),
    );
    assert.equal(installed.version, version);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});
