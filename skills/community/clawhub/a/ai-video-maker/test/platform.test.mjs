import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

// PowerShell and cmd cannot run `AIVIDEO_AGENT_PLATFORM=codex node ...`, so the client is
// named with an argument. These run the real CLIs against a stub; nothing reaches the network.
const script = (name) => fileURLToPath(new URL(`../scripts/${name}`, import.meta.url));

async function run(command, args, environment = {}) {
  const directory = await mkdtemp(join(tmpdir(), "aivideo-platform-"));
  try {
    const log = join(directory, "requests.log");
    const mock = join(directory, "mock.mjs");
    await writeFile(
      mock,
      `import { appendFileSync } from 'node:fs';
      globalThis.fetch = async (url, options = {}) => {
        const path = new URL(url).pathname;
        appendFileSync(${JSON.stringify(log)}, JSON.stringify({
          path,
          header: options.headers?.['X-AIVideo-Agent-Platform'],
          body: options.body ? JSON.parse(options.body) : undefined,
        }) + '\\n');
        if (path === '/api/skill-connect/start')
          return Response.json({ deviceCode: 'a'.repeat(64), userCode: 'ABCD-1234-5678', expiresIn: 600, interval: 5 });
        return Response.json({ ok: true, key: { status: 'ACTIVE' }, currentBalance: 50 });
      };`,
    );
    const env = { ...process.env, HOME: directory, USERPROFILE: directory, ...environment };
    for (const name of ["AIVIDEO_API_KEY", "AIVIDEO_AGENT_PLATFORM"])
      if (!(name in environment)) delete env[name];
    const result = spawnSync(process.execPath, ["--import", mock, script(command), ...args], {
      encoding: "utf8",
      env,
    });
    const requests = await readFile(log, "utf8").then(
      (text) => text.trim().split("\n").map(JSON.parse),
      () => [],
    );
    return { ...result, requests };
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test("connect --platform names the client without an environment variable", async () => {
  const started = await run("connect.mjs", ["--platform", "codex", "--start"]);
  assert.equal(started.status, 0, started.stderr);
  assert.match(started.stdout, /connect\/ai-video-maker\?code=ABCD-1234-5678/);
  assert.deepEqual(started.requests, [
    { path: "/api/skill-connect/start", body: { platform: "codex" } },
  ]);

  // The argument may follow other flags, and wins over the variable.
  const overridden = await run("connect.mjs", ["--start", "--platform", "claude"], {
    AIVIDEO_AGENT_PLATFORM: "openclaw",
  });
  assert.equal(overridden.status, 0, overridden.stderr);
  assert.equal(overridden.requests[0].body.platform, "claude");

  const variable = await run("connect.mjs", ["--start"], { AIVIDEO_AGENT_PLATFORM: "openclaw" });
  assert.equal(variable.requests[0].body.platform, "openclaw");

  // Clients the server does not list are still accepted and reported as "other".
  const unlisted = await run("connect.mjs", ["--platform", "cursor", "--start"]);
  assert.equal(unlisted.status, 0, unlisted.stderr);
  assert.equal(unlisted.requests[0].body.platform, "other");
});

test("connect rejects a missing or malformed --platform before contacting the server", async () => {
  for (const args of [["--platform"], ["--platform", "--start"], ["--platform", "Not A Name"]]) {
    const result = await run("connect.mjs", args);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /Use --platform codex/);
    assert.deepEqual(result.requests, []);
  }
  const unknown = await run("connect.mjs", ["--plaform", "codex"]);
  assert.equal(unknown.status, 1);
  assert.match(unknown.stderr, /Add --platform <codex\|claude\|openclaw>/);
  assert.deepEqual(unknown.requests, []);
});

test("run-workflow --platform sets the attribution header and wins over the variable", async () => {
  const key = { AIVIDEO_API_KEY: "platform-test-only", AIVIDEO_MAX_RETRIES: "0" };
  const named = await run("run-workflow.mjs", ["--platform", "claude", "--action", "doctor"], key);
  assert.equal(named.status, 0, named.stdout);
  assert.equal(named.requests[0].header, "claude");

  const overridden = await run("run-workflow.mjs", ["--action", "doctor", "--platform", "codex"], {
    ...key,
    AIVIDEO_AGENT_PLATFORM: "openclaw",
  });
  assert.equal(overridden.requests[0].header, "codex");

  const variable = await run("run-workflow.mjs", ["--action", "doctor"], {
    ...key,
    AIVIDEO_AGENT_PLATFORM: "openclaw",
  });
  assert.equal(variable.requests[0].header, "openclaw");

  const missing = await run("run-workflow.mjs", ["--platform", "--action", "doctor"], key);
  assert.equal(missing.status, 1);
  assert.match(JSON.parse(missing.stdout).errorMessage, /Use --platform codex/);
  assert.deepEqual(missing.requests, []);
});
