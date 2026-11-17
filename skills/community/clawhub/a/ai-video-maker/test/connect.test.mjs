import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, rm, stat, readFile, symlink, chmod } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { connect, promptKey } from "../scripts/connect.mjs";
import { loadSavedKey } from "../scripts/credentials.mjs";
import { checkDownloads } from "../../scripts/check-skill-downloads.mjs";
import { createHash } from "node:crypto";

async function temporary(fn) {
  const directory = await mkdtemp(join(tmpdir(), "aivideo-connect-"));
  try {
    await fn(directory);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test("connect validates without generation, persists privately and survives a failed replacement", async () =>
  temporary(async (directory) => {
    let calls = 0;
    await connect("test-key-private", {
      directory,
      fetcher: async (url, options) => {
        calls++;
        assert.equal(url, "https://aivideomaker.ai/api/v1/account");
        assert.equal(options.method, "GET");
        assert.equal(options.headers.key, "test-key-private");
        assert.equal(options.redirect, "error");
        return Response.json({ ok: true, key: { status: "ACTIVE" }, currentBalance: 50 });
      },
    });
    assert.equal(calls, 1);
    await assert.rejects(
      connect("other-key", { directory, fetcher: async () => new Response("<html>Login</html>") }),
      /Could not verify/,
    );
    assert.equal(loadSavedKey(directory), "test-key-private");
    assert.equal((await stat(join(directory, "credentials.json"))).mode & 0o777, 0o600);
    await assert.rejects(
      connect("bad-key", {
        directory,
        fetcher: async () => new Response("bad-key", { status: 401 }),
      }),
      /Key not accepted/,
    );
    assert.equal(loadSavedKey(directory), "test-key-private");
    await assert.rejects(
      connect("other-key", {
        directory,
        fetcher: async () => {
          throw new Error("other-key");
        },
      }),
      /Could not connect/,
    );
    assert.equal(loadSavedKey(directory), "test-key-private");
  }));

test("connection rejects unsafe directories and credential symlinks", async () =>
  temporary(async (directory) => {
    const linked = join(directory, "linked");
    await symlink(directory, linked);
    await assert.rejects(
      connect("test-key", {
        directory: linked,
        fetcher: async () =>
          Response.json({ ok: true, key: { status: "ACTIVE" }, currentBalance: 50 }),
      }),
      /Could not save/,
    );
    await connect("test-key", {
      directory,
      fetcher: async () =>
        Response.json({ ok: true, key: { status: "ACTIVE" }, currentBalance: 50 }),
    });
    await chmod(join(directory, "credentials.json"), 0o644);
    assert.throws(() => loadSavedKey(directory), /Cannot read private/);
    assert.equal(
      await readFile(join(directory, "credentials.json"), "utf8"),
      '{"apiKey":"test-key"}\n',
    );
  }));

test("connect refuses non-interactive secret input", () => {
  assert.throws(() => promptKey({ isTTY: false }, { isTTY: false }), /own terminal/);
});

test("release smoke check catches the production 404 and modified archive", async () => {
  await assert.rejects(
    checkDownloads(
      "https://example.test",
      "1.2.3",
      async () => new Response("not found", { status: 404 }),
    ),
    /HTTP 404/,
  );
  const archive = Buffer.from([0x1f, 0x8b, 1, 2]);
  const checksum = createHash("sha256").update(archive).digest("hex");
  const fetcher = async (url) =>
    new Response(
      url.pathname.endsWith(".mjs")
        ? 'export async function installSkill() {} const version = "1.2.3";'
        : url.pathname.endsWith(".sha256")
          ? `${checksum}  ai-video-maker-1.2.3.tgz\n`
          : archive,
    );
  await checkDownloads("https://example.test", "1.2.3", fetcher);
  await assert.rejects(
    checkDownloads("https://example.test", "1.2.3", async (url) =>
      url.pathname.endsWith(".tgz") ? new Response(Buffer.from([0x1f, 0x8b, 3, 4])) : fetcher(url),
    ),
    /Checksum mismatch/,
  );
});

test("a new agent process loads the saved key and environment keys take priority", async () =>
  temporary(async (directory) => {
    await connect("saved-test-key", {
      directory,
      fetcher: async () =>
        Response.json({ ok: true, key: { status: "ACTIVE" }, currentBalance: 50 }),
    });
    const { execFileSync } = await import("node:child_process");
    const clientUrl = new URL("../scripts/aivideo-client.mjs", import.meta.url).href;
    for (const environmentKey of ["", "environment-test-key"]) {
      const script = `
      import assert from 'node:assert/strict';
      import os from 'node:os';
      import { syncBuiltinESMExports } from 'node:module';
      import { dirname, basename } from 'node:path';
      // Isolate only the credential-directory lookup; never touch real user credentials.
      const credentials = await import(${JSON.stringify(new URL("../scripts/credentials.mjs", import.meta.url).href)});
      const saved = credentials.loadSavedKey(${JSON.stringify(directory)});
      assert.equal(saved, 'saved-test-key');
      os.homedir = () => ${JSON.stringify(directory)};
      syncBuiltinESMExports();
      const { mkdir, copyFile } = await import('node:fs/promises');
      await mkdir(${JSON.stringify(join(directory, ".aivideo-maker"))}, { recursive: true, mode: 0o700 });
      await copyFile(${JSON.stringify(join(directory, "credentials.json"))}, ${JSON.stringify(join(directory, ".aivideo-maker/credentials.json"))});
      const { createAIVideoClient } = await import(${JSON.stringify(clientUrl)});
      globalThis.fetch = async (url, options) => {
        assert.equal(url, 'https://aivideomaker.ai/api/v1/account');
        assert.equal(options.headers.key, ${JSON.stringify(environmentKey || "saved-test-key")});
        return Response.json({ ok: true });
      };
      assert.equal((await createAIVideoClient({ debug: false }).doctor()).ok, true);
      if (!process.env.AIVIDEO_API_KEY) assert.throws(() => createAIVideoClient({ baseUrl: 'https://example.test' }), /explicit API key/);
      console.log('connected');
    `;
      const result = execFileSync(process.execPath, ["--input-type=module", "-e", script], {
        env: { ...process.env, AIVIDEO_API_KEY: environmentKey },
        encoding: "utf8",
      });
      assert.equal(result.trim(), "connected");
    }
  }));

test("terminal prompt hides pasted keys and handles cancellation", async () => {
  const { PassThrough, Writable } = await import("node:stream");
  const input = new PassThrough();
  input.isTTY = true;
  input.setRawMode = () => {};
  let displayed = "";
  const output = new Writable({
    write(chunk, encoding, done) {
      displayed += chunk;
      done();
    },
  });
  output.isTTY = true;
  const result = promptKey(input, output);
  input.write("hidden-test-key\n");
  assert.equal(await result, "hidden-test-key");
  assert.doesNotMatch(displayed, /hidden-test-key/);
  const cancelled = promptKey(input, output);
  input.write("\x03");
  await assert.rejects(cancelled, /cancelled/);
  input.destroy();
  output.destroy();
});
