import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, rm, stat, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { browserConnect, verifyConnection } from "../scripts/browser-connect.mjs";
import { loadSavedKey, saveKey } from "../scripts/credentials.mjs";

const deviceCode = "b".repeat(64);
const apiKey = `ak_${"a".repeat(64)}`;
const start = { deviceCode, userCode: "ABCD-1234-5678", interval: 5, expiresIn: 600 };
const account = { ok: true, currentBalance: 50, key: { status: "ACTIVE" } };
async function isolated(fn) {
  const directory = await mkdtemp(join(tmpdir(), "browser-connect-"));
  try {
    await fn(directory);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test("browser approval saves privately, verifies automatically, and never generates", () =>
  isolated(async (directory) => {
    const calls = [];
    let polls = 0;
    let shown;
    const result = await browserConnect({
      directory,
      sleep: async () => {},
      onApproval: (value) => {
        shown = value;
      },
      fetcher: async (url, options) => {
        calls.push(url);
        assert.equal(options.redirect, "error");
        if (url.endsWith("/start")) return Response.json(start);
        if (url.endsWith("/token")) {
          assert.equal(JSON.parse(options.body).deviceCode, deviceCode);
          if (JSON.parse(options.body).acknowledge) {
            assert.equal(loadSavedKey(directory), apiKey);
            return Response.json({ status: "ACKNOWLEDGED" });
          }
          return Response.json(
            ++polls === 1 ? { status: "PENDING" } : { status: "CONNECTED", apiKey },
          );
        }
        assert.equal(options.headers.key, apiKey);
        if (url.endsWith("/account")) return Response.json(account);
        assert.ok(url.endsWith("/quote/minimax"));
        return Response.json({ credits: 15, billable: false });
      },
    });
    assert.deepEqual(result, {
      status: "VERIFIED",
      currentBalance: 50,
      sampleQuoteCredits: 15,
      creditsSpent: 0,
    });
    assert.equal(loadSavedKey(directory), apiKey);
    assert.equal((await stat(join(directory, "credentials.json"))).mode & 0o777, 0o600);
    assert.equal(shown.url, "https://aivideomaker.ai/connect/ai-video-maker?code=ABCD-1234-5678");
    assert.ok(!JSON.stringify(shown).includes(deviceCode));
    assert.ok(!JSON.stringify(result).includes(apiKey));
    assert.ok(calls.every((url) => !url.includes("/generate/")));
  }));

for (const [code, status] of [
  ["DENIED", 403],
  ["EXPIRED", 410],
  ["CONSUMED", 409],
]) {
  test(`${code} preserves the previous connection and stops polling`, () =>
    isolated(async (directory) => {
      await saveKey("previous-key", directory);
      let calls = 0;
      await assert.rejects(
        browserConnect({
          directory,
          sleep: async () => {},
          fetcher: async (url) => {
            calls++;
            return url.endsWith("/start")
              ? Response.json(start)
              : Response.json({ error: code }, { status });
          },
        }),
      );
      assert.equal(calls, 2);
      assert.equal(loadSavedKey(directory), "previous-key");
    }));
}

test("quote outage retains exchanged credentials so verification can resume", () =>
  isolated(async (directory) => {
    await assert.rejects(
      browserConnect({
        directory,
        sleep: async () => {},
        fetcher: async (url) => {
          if (url.endsWith("/start")) return Response.json(start);
          if (url.endsWith("/token")) return Response.json({ status: "CONNECTED", apiKey });
          if (url.endsWith("/account")) return Response.json(account);
          return Response.json({ error: apiKey }, { status: 503 });
        },
      }),
      /sample quote could not be verified/,
    );
    assert.equal(loadSavedKey(directory), apiKey);
  }));

test("rate-limited polls wait again and local timeout does not exchange after expiry", async () => {
  let time = 0;
  let polls = 0;
  await assert.rejects(
    browserConnect({
      now: () => time,
      sleep: async () => {
        time += 300000;
      },
      fetcher: async (url) => {
        if (url.endsWith("/start")) return Response.json(start);
        polls++;
        return Response.json({ error: "SLOW_DOWN" }, { status: 429 });
      },
    }),
    /expired/,
  );
  assert.equal(polls, 1);
});

test("untrusted network errors and malformed credentials never reach user output", () =>
  isolated(async (directory) => {
    await assert.rejects(
      verifyConnection(apiKey, {
        fetcher: async () => {
          throw new Error(apiKey);
        },
      }),
      (error) => !error.message.includes(apiKey),
    );
    await assert.rejects(
      browserConnect({
        directory,
        sleep: async () => {},
        fetcher: async (url) =>
          Response.json(
            url.endsWith("/start") ? start : { status: "CONNECTED", apiKey: "malformed-secret" },
          ),
      }),
      /Invalid connection response/,
    );
    assert.equal(loadSavedKey(directory), "");
  }));

test("the noninteractive CLI verifies an environment key without printing it or starting a new connection", () =>
  isolated(async (directory) => {
    const mock = join(directory, "mock-cli.mjs");
    await writeFile(
      mock,
      `
    globalThis.fetch = async (url, options) => {
      if (options.headers.key !== 'cli-private-test-key') throw new Error('wrong key');
      if (url.endsWith('/api/v1/account')) return Response.json({ok:true,key:{status:'ACTIVE'},currentBalance:50});
      if (url.endsWith('/api/v1/quote/minimax')) return Response.json({credits:15,billable:false});
      throw new Error('Unexpected endpoint');
    };
  `,
    );
    const command = fileURLToPath(new URL("../scripts/connect.mjs", import.meta.url));
    const options = {
      encoding: "utf8",
      env: { ...process.env, AIVIDEO_API_KEY: "cli-private-test-key" },
    };
    const result = spawnSync(process.execPath, ["--import", mock, command], options);
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /Connected and verified/);
    assert.doesNotMatch(result.stdout + result.stderr, /cli-private-test-key/);
    const reconnect = spawnSync(
      process.execPath,
      ["--import", mock, command, "--reconnect"],
      options,
    );
    assert.equal(reconnect.status, 1);
    assert.match(reconnect.stderr, /takes priority/);
    assert.doesNotMatch(reconnect.stdout + reconnect.stderr, /cli-private-test-key/);
  }));

for (const failure of ["network", "503", "429", "truncated"]) {
  test(`recovers a ${failure} polling failure with the same device secret`, () =>
    isolated(async (directory) => {
      let attempts = 0;
      const delays = [];
      let acknowledged = false;
      const result = await browserConnect({
        directory,
        sleep: async (ms) => {
          delays.push(ms);
        },
        fetcher: async (url, options) => {
          if (url.endsWith("/start")) return Response.json(start);
          if (url.endsWith("/token")) {
            const request = JSON.parse(options.body);
            assert.equal(request.deviceCode, deviceCode);
            if (request.acknowledge) {
              assert.equal(loadSavedKey(directory), apiKey);
              acknowledged = true;
              return Response.json({ status: "ACKNOWLEDGED" });
            }
            if (++attempts === 1) {
              if (failure === "network") throw new Error("socket closed after server commit");
              if (failure === "truncated") return new Response('{"status":"CONNECTED",');
              return Response.json(
                { error: "UNAVAILABLE" },
                { status: Number(failure), headers: { "Retry-After": "20" } },
              );
            }
            return Response.json({ status: "CONNECTED", apiKey });
          }
          if (url.endsWith("/account")) return Response.json(account);
          assert.ok(url.endsWith("/quote/minimax"));
          return Response.json({ credits: 15, billable: false });
        },
      });
      assert.equal(result.status, "VERIFIED");
      assert.equal(attempts, 2);
      assert.ok(acknowledged);
      assert.ok(delays[1] >= (failure === "503" || failure === "429" ? 20000 : 11000));
    }));
}

test("a lost acknowledgement is retried without exchanging another key", () =>
  isolated(async (directory) => {
    let exchanges = 0;
    let acknowledgements = 0;
    await browserConnect({
      directory,
      sleep: async () => {},
      fetcher: async (url, options) => {
        if (url.endsWith("/start")) return Response.json(start);
        if (url.endsWith("/token")) {
          if (JSON.parse(options.body).acknowledge) {
            assert.equal(loadSavedKey(directory), apiKey);
            if (++acknowledgements === 1) throw new Error("lost acknowledgement");
            return Response.json({ status: "ACKNOWLEDGED" });
          }
          exchanges++;
          return Response.json({ status: "CONNECTED", apiKey });
        }
        if (url.endsWith("/account")) return Response.json(account);
        return Response.json({ credits: 15, billable: false });
      },
    });
    assert.equal(exchanges, 1);
    assert.equal(acknowledgements, 2);
  }));

test("persistent transient errors stop at the deadline without replacing saved credentials", () =>
  isolated(async (directory) => {
    await saveKey("old-key", directory);
    let time = 0;
    let polls = 0;
    await assert.rejects(
      browserConnect({
        directory,
        now: () => time,
        sleep: async (ms) => {
          time += ms;
        },
        fetcher: async (url) => {
          if (url.endsWith("/start")) return Response.json(start);
          polls++;
          return Response.json({ error: "UNAVAILABLE" }, { status: 503 });
        },
      }),
      /expired/,
    );
    assert.ok(polls > 1 && polls < 30);
    assert.equal(time, 600000);
    assert.equal(loadSavedKey(directory), "old-key");
  }));
