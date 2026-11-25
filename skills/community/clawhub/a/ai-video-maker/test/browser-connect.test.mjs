import assert from "node:assert/strict";
import { test } from "node:test";
import {
  chmod,
  mkdir,
  mkdtemp,
  readdir,
  readFile,
  rm,
  stat,
  symlink,
  writeFile,
} from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { browserConnect, verifyConnection } from "../scripts/browser-connect.mjs";
import {
  checkPrivate,
  checkPrivateStorage,
  loadPendingConnection,
  loadSavedKey,
  saveKey,
  savePendingConnection,
} from "../scripts/credentials.mjs";

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
    const { firstVideo, ...verification } = result;
    assert.match(firstVideo.flowId, /^[0-9a-f-]{36}$/);
    assert.deepEqual(
      firstVideo.scenarios.map((item) => item.id),
      ["product", "social", "custom"],
    );
    assert.deepEqual(verification, {
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

test("rate-limited polls wait again and local timeout does not exchange after expiry", () =>
  isolated(async (directory) => {
    let time = 0;
    let polls = 0;
    await assert.rejects(
      browserConnect({
        directory,
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
    assert.equal(loadPendingConnection(directory), null);
  }));

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

const connected = async (url, options, seen = {}) => {
  if (url.endsWith("/start")) {
    seen.starts = (seen.starts ?? 0) + 1;
    return Response.json(start);
  }
  if (url.endsWith("/token")) {
    const body = JSON.parse(options.body);
    (seen.deviceCodes ??= []).push(body.deviceCode);
    return Response.json(
      body.acknowledge ? { status: "ACKNOWLEDGED" } : { status: "CONNECTED", apiKey },
    );
  }
  if (url.endsWith("/account")) return Response.json(account);
  return Response.json({ credits: 15, billable: false });
};

test("a stopped helper resumes the same link and code instead of stranding the approval", () =>
  isolated(async (directory) => {
    const seen = {};
    const shown = [];
    const fetcher = (url, options) => connected(url, options, seen);
    // First run hands over the link and stops before the user approves.
    const first = await browserConnect({
      directory,
      fetcher,
      waitForApproval: false,
      onApproval: (value) => shown.push(value),
    });
    assert.equal(first.status, "PENDING");
    assert.equal(loadSavedKey(directory), "");
    assert.equal((await stat(join(directory, "pending-connection.json"))).mode & 0o777, 0o600);
    assert.equal(loadPendingConnection(directory).deviceCode, deviceCode);

    const delays = [];
    const result = await browserConnect({
      directory,
      fetcher,
      sleep: async (ms) => {
        delays.push(ms);
      },
      onApproval: (value) => shown.push(value),
    });
    assert.equal(result.status, "VERIFIED");
    assert.equal(seen.starts, 1, "resuming must not start a second connection");
    assert.ok(seen.deviceCodes.every((code) => code === deviceCode));
    assert.equal(shown[1].url, shown[0].url);
    assert.equal(shown[0].resumed, false);
    assert.equal(shown[1].resumed, true);
    assert.equal(delays[0], 0, "an approval given while stopped is collected at once");
    assert.ok(!JSON.stringify(shown).includes(deviceCode));
    assert.equal(loadSavedKey(directory), apiKey);
    assert.equal(loadPendingConnection(directory), null);
  }));

test("expired, unsafe or declined pending state starts a new connection", () =>
  isolated(async (directory) => {
    const stale = { deviceCode: "c".repeat(64), userCode: "AAAA-BBBB-CCCC" };
    for (const scenario of ["expired", "unsafe", "reconnect"]) {
      await savePendingConnection(
        { ...stale, expiresAt: scenario === "expired" ? Date.now() - 1 : Date.now() + 60000 },
        directory,
      );
      if (scenario === "unsafe") await chmod(join(directory, "pending-connection.json"), 0o644);
      const seen = {};
      await browserConnect({
        directory,
        resume: scenario !== "reconnect",
        sleep: async () => {},
        fetcher: (url, options) => connected(url, options, seen),
      });
      assert.equal(seen.starts, 1, scenario);
      assert.ok(
        seen.deviceCodes.every((code) => code === deviceCode),
        scenario,
      );
      assert.equal(loadPendingConnection(directory), null, scenario);
    }
  }));

test("a session finished by another helper run verifies the saved key", () =>
  isolated(async (directory) => {
    await saveKey(apiKey, directory);
    await savePendingConnection(
      { deviceCode, userCode: start.userCode, expiresAt: Date.now() + 300000 },
      directory,
    );
    const result = await browserConnect({
      directory,
      sleep: async () => {},
      fetcher: async (url, options) => {
        assert.ok(!url.endsWith("/start"));
        if (url.endsWith("/token")) return Response.json({ error: "CONSUMED" }, { status: 409 });
        assert.equal(options.headers.key, apiKey);
        if (url.endsWith("/account")) return Response.json(account);
        return Response.json({ credits: 15, billable: false });
      },
    });
    assert.equal(result.status, "VERIFIED");
    assert.equal(loadPendingConnection(directory), null);
  }));

test("the CLI prints the link with --start and finishes on the next run", () =>
  isolated(async (directory) => {
    const mock = join(directory, "mock-cli.mjs");
    const log = join(directory, "calls.log");
    await writeFile(
      mock,
      `
    import { appendFileSync } from 'node:fs';
    globalThis.fetch = async (url, options) => {
      appendFileSync(${JSON.stringify(log)}, new URL(url).pathname + '\\n');
      if (url.endsWith('/start')) return Response.json(${JSON.stringify(start)});
      if (url.endsWith('/token')) {
        return Response.json(JSON.parse(options.body).acknowledge
          ? {status:'ACKNOWLEDGED'} : {status:'CONNECTED',apiKey:${JSON.stringify(apiKey)}});
      }
      if (url.endsWith('/api/v1/account')) return Response.json({ok:true,key:{status:'ACTIVE'},currentBalance:50});
      return Response.json({credits:15,billable:false});
    };
  `,
    );
    const command = fileURLToPath(new URL("../scripts/connect.mjs", import.meta.url));
    const env = { ...process.env, HOME: directory, USERPROFILE: directory };
    delete env.AIVIDEO_API_KEY;
    const run = (...args) =>
      spawnSync(process.execPath, ["--import", mock, command, ...args], { encoding: "utf8", env });

    const started = run("--start");
    assert.equal(started.status, 0, started.stderr);
    assert.match(started.stdout, /connect\/ai-video-maker\?code=ABCD-1234-5678/);
    assert.match(started.stdout, /Run connect again without --start/);
    assert.doesNotMatch(started.stdout, /Connected and verified/);

    const finished = run();
    assert.equal(finished.status, 0, finished.stderr);
    assert.match(finished.stdout, /Resuming your pending connection/);
    assert.match(finished.stdout, /Connected and verified/);
    assert.doesNotMatch(started.stdout + finished.stdout + finished.stderr, new RegExp(apiKey));
    assert.doesNotMatch(started.stdout + finished.stdout, new RegExp(deviceCode));
    const calls = (await readFile(log, "utf8")).trim().split("\n");
    assert.equal(calls.filter((path) => path.endsWith("/start")).length, 1);
  }));

test("the original helper accepts a key saved by a later run of the same session", () =>
  isolated(async (directory) => {
    await saveKey("previous-key", directory);
    const result = await browserConnect({
      directory,
      sleep: async () => {},
      fetcher: async (url, options) => {
        if (url.endsWith("/start")) return Response.json(start);
        if (url.endsWith("/token")) {
          // A re-run exchanged and acknowledged the session before this poll.
          await saveKey(apiKey, directory);
          return Response.json({ error: "CONSUMED" }, { status: 409 });
        }
        assert.equal(options.headers.key, apiKey);
        if (url.endsWith("/account")) return Response.json(account);
        return Response.json({ credits: 15, billable: false });
      },
    });
    assert.equal(result.status, "VERIFIED");
    assert.equal(loadPendingConnection(directory), null);
  }));

test("a passing fault keeps the approval so the next run resumes it", () =>
  isolated(async (directory) => {
    const seen = {};
    let blocked = true;
    const fetcher = async (url, options) => {
      if (url.endsWith("/token") && blocked)
        return new Response("<html>Blocked by proxy</html>", { status: 403 });
      return connected(url, options, seen);
    };
    await assert.rejects(
      browserConnect({ directory, sleep: async () => {}, fetcher }),
      /Run connect again to resume/,
    );
    assert.equal(loadPendingConnection(directory).deviceCode, deviceCode);
    blocked = false;
    const result = await browserConnect({ directory, sleep: async () => {}, fetcher });
    assert.equal(result.status, "VERIFIED");
    assert.equal(seen.starts, 1, "the same link must stay valid across the fault");
  }));

test("a denied approval is final and frees the next run to start over", () =>
  isolated(async (directory) => {
    await assert.rejects(
      browserConnect({
        directory,
        sleep: async () => {},
        fetcher: async (url) =>
          url.endsWith("/start")
            ? Response.json(start)
            : Response.json({ error: "DENIED" }, { status: 403 }),
      }),
      /cancelled/,
    );
    assert.equal(loadPendingConnection(directory), null);
  }));

test("server pacing is not treated as a fault to back off from", () =>
  isolated(async (directory) => {
    const delays = [];
    let polls = 0;
    await browserConnect({
      directory,
      sleep: async (ms) => {
        delays.push(ms);
      },
      fetcher: async (url, options) => {
        if (url.endsWith("/token") && !JSON.parse(options.body).acknowledge && ++polls <= 3)
          return Response.json(
            { error: "SLOW_DOWN" },
            { status: 429, headers: { "Retry-After": "5" } },
          );
        return connected(url, options);
      },
    });
    assert.deepEqual(delays.slice(0, 4), [5500, 5500, 5500, 5500]);
  }));

test("a link about to expire is not handed out again", () =>
  isolated(async (directory) => {
    const old = { deviceCode: "c".repeat(64), userCode: "AAAA-BBBB-CCCC" };
    // Still pending: start a new session rather than show a link with seconds left.
    await savePendingConnection({ ...old, expiresAt: Date.now() + 10000 }, directory);
    const seen = {};
    const shown = [];
    await browserConnect({
      directory,
      sleep: async () => {},
      onApproval: (value) => shown.push(value),
      fetcher: async (url, options) => {
        if (url.endsWith("/token") && JSON.parse(options.body).deviceCode === old.deviceCode)
          return Response.json({ status: "PENDING" });
        return connected(url, options, seen);
      },
    });
    assert.equal(seen.starts, 1);
    assert.equal(shown[0].code, start.userCode);
    assert.equal(shown[0].resumed, false);

    // Already approved: collect it without issuing another link.
    await rm(join(directory, "credentials.json"));
    await savePendingConnection({ ...old, expiresAt: Date.now() + 10000 }, directory);
    const late = {};
    const result = await browserConnect({
      directory,
      sleep: async () => {},
      onApproval: () => assert.fail("no new link is needed"),
      fetcher: (url, options) => connected(url, options, late),
    });
    assert.equal(result.status, "VERIFIED");
    assert.equal(late.starts, undefined);
    assert.deepEqual(new Set(late.deviceCodes), new Set([old.deviceCode]));
  }));

// Runs the real CLI with HOME pointed at a private temporary directory.
async function cli(directory, steps) {
  const mock = join(directory, "mock-cli.mjs");
  await writeFile(
    mock,
    `
    globalThis.fetch = async (url, options) => {
      if (url.endsWith('/start')) return Response.json(${JSON.stringify(start)});
      if (url.endsWith('/token')) {
        return Response.json(JSON.parse(options.body).acknowledge
          ? {status:'ACKNOWLEDGED'} : {status:'CONNECTED',apiKey:${JSON.stringify(apiKey)}});
      }
      if (url.endsWith('/api/v1/account')) return Response.json({ok:true,key:{status:'ACTIVE'},currentBalance:50});
      return Response.json({credits:15,billable:false});
    };
  `,
  );
  const command = fileURLToPath(new URL("../scripts/connect.mjs", import.meta.url));
  const env = { ...process.env, HOME: directory, USERPROFILE: directory };
  delete env.AIVIDEO_API_KEY;
  return steps.map((args) =>
    spawnSync(process.execPath, ["--import", mock, command, ...args], { encoding: "utf8", env }),
  );
}

test("a reconnect started with --start is finished by the next plain run", () =>
  isolated(async (directory) => {
    const home = join(directory, ".aivideo-maker");
    await saveKey("old-account-key", home);
    const [started, finished] = await cli(directory, [["--reconnect", "--start"], []]);
    assert.equal(started.status, 0, started.stderr);
    assert.match(started.stdout, /Run connect again without --start/);
    assert.doesNotMatch(started.stdout, /Connected and verified/);
    assert.equal(finished.status, 0, finished.stderr);
    assert.match(finished.stdout, /Resuming your pending connection/);
    assert.match(finished.stdout, /Connected and verified/);
    assert.equal(loadSavedKey(home), apiKey, "the new account must replace the old key");
    assert.equal(loadPendingConnection(home), null);
  }));

test("an interrupted reconnect resumes, and an ordinary pending approval yields to --reconnect", () =>
  isolated(async (directory) => {
    const home = join(directory, ".aivideo-maker");
    const other = { deviceCode: "c".repeat(64), userCode: "AAAA-BBBB-CCCC" };
    await savePendingConnection(
      { ...other, expiresAt: Date.now() + 300000, replacing: true },
      home,
    );
    const [resumed] = await cli(directory, [["--reconnect", "--start"]]);
    assert.match(resumed.stdout, /Resuming your pending connection/);
    assert.match(resumed.stdout, /code=AAAA-BBBB-CCCC/);

    await savePendingConnection({ ...other, expiresAt: Date.now() + 300000 }, home);
    const [replaced] = await cli(directory, [["--reconnect", "--start"]]);
    assert.match(replaced.stdout, /code=ABCD-1234-5678/);
    assert.equal(loadPendingConnection(home).replacing, true);
  }));

test("state left by an abandoned approval is removed once a key is saved", () =>
  isolated(async (directory) => {
    const home = join(directory, ".aivideo-maker");
    await saveKey(apiKey, home);
    await savePendingConnection(
      { deviceCode, userCode: start.userCode, expiresAt: Date.now() - 1000 },
      home,
    );
    const [verified] = await cli(directory, [[]]);
    assert.equal(verified.status, 0, verified.stderr);
    assert.match(verified.stdout, /Connected and verified/);
    await assert.rejects(stat(join(home, "pending-connection.json")), { code: "ENOENT" });
  }));

// Records every request; the server would create a session on /start and a key on /token.
function recorder(onStart = async () => {}) {
  const calls = [];
  const fetcher = async (url) => {
    calls.push(new URL(url).pathname);
    if (url.endsWith("/start")) {
      await onStart();
      return Response.json(start);
    }
    return Response.json({ status: "CONNECTED", apiKey });
  };
  return { calls, fetcher };
}

// Connects in both modes and expects each to stop before anything reaches the user or server.
async function refused(directory, pattern, options = {}) {
  const { calls, fetcher } = recorder();
  let shown = false;
  for (const waitForApproval of [true, false]) {
    await assert.rejects(
      browserConnect({
        directory,
        fetcher,
        waitForApproval,
        sleep: async () => {},
        onApproval: () => {
          shown = true;
        },
        ...options,
      }),
      pattern,
    );
  }
  assert.deepEqual(calls, []);
  assert.equal(shown, false);
}

// Root ignores permission bits and Windows has none, so a folder cannot be made unwritable.
const unixOnly = process.platform === "win32" && "Windows has no Unix permission bits";
const ownerBound =
  unixOnly || (process.getuid?.() === 0 && "root is not stopped by permission bits");

test(
  "no approval is requested when the private folder cannot be written, as in a sandbox",
  { skip: ownerBound },
  () =>
    isolated(async (directory) => {
      await chmod(directory, 0o500);
      try {
        await refused(
          join(directory, ".aivideo-maker"),
          /cannot save a connection: it is not allowed to write.*sandbox.*No approval link was shown and nothing was approved.*--manual/,
        );
      } finally {
        await chmod(directory, 0o700);
      }
    }),
);

test(
  "no approval is requested when other users can read the private folder",
  { skip: unixOnly },
  () =>
    isolated(async (directory) => {
      await chmod(directory, 0o755);
      await refused(
        directory,
        /is not private to you.*owner-only access.*No approval link was shown/,
      );
    }),
);

test("no approval is requested when the saved key could not be replaced", () =>
  isolated(async (directory) => {
    // The folder itself is writable, so only a check of the real target catches this.
    await mkdir(join(directory, "credentials.json"));
    await refused(directory, /credentials\.json in ~\/\.aivideo-maker cannot be replaced/);
  }));

test("a read-only saved key is caught on Windows, where it cannot be replaced", () =>
  isolated(async (directory) => {
    await saveKey(apiKey, directory);
    await chmod(join(directory, "credentials.json"), 0o400);
    await assert.rejects(checkPrivateStorage(directory, "win32"), { code: "NOT_REPLACEABLE" });
    // Elsewhere a rename replaces it regardless, as saving a key does.
    await checkPrivateStorage(directory, "linux");
    await saveKey(apiKey, directory);
  }));

test("a failure that is not about permissions is not reported as one", () =>
  isolated(async (directory) => {
    const file = join(directory, "not-a-folder");
    await writeFile(file, "");
    await refused(
      join(file, ".aivideo-maker"),
      /could not be written \(ENOTDIR\)\. Check free disk space/,
    );
    await assert.rejects(
      browserConnect({ directory: join(file, ".aivideo-maker"), fetcher: recorder().fetcher }),
      (error) => !/sandbox|not private/.test(error.message),
    );
  }));

test(
  "an approval already under way is reported as kept, not as never requested",
  { skip: ownerBound },
  () =>
    isolated(async (directory) => {
      const pending = { deviceCode, userCode: start.userCode, expiresAt: Date.now() + 300000 };
      await savePendingConnection(pending, directory);
      // First run could write here (for example outside a sandbox); this run cannot.
      await chmod(directory, 0o500);
      try {
        await refused(
          directory,
          (error) =>
            /Your pending approval is kept: fix this and run connect again to resume the same link and code/.test(
              error.message,
            ) && !/nothing was approved|No approval link/.test(error.message),
        );
        assert.equal(loadPendingConnection(directory).userCode, start.userCode);
      } finally {
        await chmod(directory, 0o700);
      }
    }),
);

test("the storage check leaves nothing behind", () =>
  isolated(async (directory) => {
    const home = join(directory, ".aivideo-maker");
    const { calls, fetcher } = recorder();
    await browserConnect({ directory: home, fetcher, waitForApproval: false });
    assert.deepEqual(calls, ["/api/skill-connect/start"]);
    assert.deepEqual(await readdir(home), ["pending-connection.json"]);
  }));

test(
  "--start shows no link when the approval cannot be kept for the next run",
  { skip: ownerBound },
  () =>
    isolated(async (directory) => {
      const home = join(directory, ".aivideo-maker");
      await mkdir(home, { mode: 0o700 });
      // The folder stops being writable after the first check, just before the session is saved.
      const { calls, fetcher } = recorder(() => chmod(home, 0o500));
      let shown = false;
      try {
        await assert.rejects(
          browserConnect({
            directory: home,
            fetcher,
            waitForApproval: false,
            onApproval: () => {
              shown = true;
            },
          }),
          /cannot save a connection.*No approval link was shown/,
        );
      } finally {
        await chmod(home, 0o700);
      }
      assert.deepEqual(calls, ["/api/skill-connect/start"]);
      assert.equal(shown, false);
    }),
);

test("Windows files pass the privacy check that their mode bits would fail", () => {
  // Node reports 0666 for every writable file and folder on Windows.
  const entry = (directory) => ({
    isDirectory: () => directory,
    isFile: () => !directory,
    mode: (directory ? 0o40000 : 0o100000) | 0o666,
    uid: 0,
  });
  assert.doesNotThrow(() => checkPrivate(entry(true), true, "win32"));
  assert.doesNotThrow(() => checkPrivate(entry(false), false, "win32"));
  // A symlink or the wrong kind of entry is still refused there.
  assert.throws(() => checkPrivate(entry(false), true, "win32"), { code: "WRONG_TYPE" });
  for (const platform of ["linux", "darwin"]) {
    assert.throws(() => checkPrivate(entry(true), true, platform), { code: "NOT_PRIVATE" });
  }
});

test(
  "the command line stops before showing a link when the home folder is not writable",
  { skip: ownerBound },
  () =>
    isolated(async (directory) => {
      await cli(directory, []); // Writes the fetch mock while the folder is still writable.
      await chmod(directory, 0o500);
      try {
        for (const args of [[], ["--start"], ["--reconnect"]]) {
          const [run] = await cli(directory, [args]);
          assert.equal(run.status, 1);
          assert.match(run.stderr, /cannot save a connection: it is not allowed to write/);
          assert.doesNotMatch(run.stdout, /Open https|Confirm this code|Connected and verified/);
        }
      } finally {
        await chmod(directory, 0o700);
      }
    }),
);

test(
  "the command line names a way out when saved credentials are unsafe or unreadable",
  { skip: unixOnly },
  () =>
    isolated(async (directory) => {
      const home = join(directory, ".aivideo-maker");
      await saveKey(apiKey, home);
      await chmod(home, 0o755);
      const [loose] = await cli(directory, [[]]);
      assert.equal(loose.status, 1);
      assert.match(
        loose.stderr,
        /owner-only access \(folder 700, file 600\)\. Fix the permissions/,
      );
      assert.doesNotMatch(loose.stdout, /Open https/);

      // A damaged file is replaced by a new connection instead of looping on the same error.
      await chmod(home, 0o700);
      await writeFile(join(home, "credentials.json"), "not json", { mode: 0o600 });
      const [damaged, replaced] = await cli(directory, [[], ["--reconnect"]]);
      assert.equal(damaged.status, 1);
      assert.match(damaged.stderr, /Run connect\.mjs --reconnect to replace them/);
      assert.equal(replaced.status, 0, replaced.stderr);
      assert.match(replaced.stdout, /Connected and verified/);
      assert.equal(loadSavedKey(home), apiKey);
    }),
);

test("a link or wrong kind of entry is not reported as a permissions problem", () =>
  isolated(async (directory) => {
    // The folder is a link to a real, private folder: chmod on it would change nothing.
    const real = join(directory, "real");
    await mkdir(real, { mode: 0o700 });
    const linked = join(directory, "linked");
    await symlink(real, linked);
    await refused(linked, (error) => {
      assert.match(error.message, /is not a regular folder \(for example, it is a link\)/);
      assert.doesNotMatch(error.message, /700|owner-only|sandbox/);
      return true;
    });

    // A folder where the key file belongs stops the command line with the same kind of advice.
    const home = join(directory, ".aivideo-maker");
    await mkdir(join(home, "credentials.json"), { recursive: true, mode: 0o700 });
    await chmod(home, 0o700);
    const [run] = await cli(directory, [[]]);
    assert.equal(run.status, 1);
    assert.match(
      run.stderr,
      /credentials\.json a regular file, not a link or another kind of entry/,
    );
    assert.doesNotMatch(run.stderr, /Fix the permissions|--reconnect/);
  }));
