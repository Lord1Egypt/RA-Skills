import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import test from "node:test";
import { fetchPublicJs, isPublicClientWeb, isRetryablePublicJsError, publicJsBackoffMs } from "../lib/fetch-public.mjs";

function response({ status = 200, body = "", headers = {} } = {}) {
  const res = new EventEmitter();
  res.statusCode = status;
  res.headers = headers;
  res.resume = () => {};
  queueMicrotask(() => {
    if (body) res.emit("data", Buffer.from(body));
    res.emit("end");
  });
  return res;
}

test("only abs.twimg.com client-web scripts are public fetches", () => {
  assert.equal(isPublicClientWeb("https://abs.twimg.com/responsive-web/client-web/ondemand.s.abc.js"), true);
  assert.equal(isPublicClientWeb("https://abs.twimg.com/responsive-web/client-web/main.abc.js"), true);
  assert.equal(isPublicClientWeb("https://x.com/i/api/graphql/abc/CreateNoteTweet"), false);
  assert.equal(isPublicClientWeb("http://abs.twimg.com/responsive-web/client-web/main.abc.js"), false);
  assert.equal(isPublicClientWeb("not a url"), false);
});

test("fetchPublicJs reads a 200 body and follows one redirect", async () => {
  const seen = [];
  const request = (url, _opts, cb) => {
    seen.push(url);
    const req = new EventEmitter();
    req.end = () => {};
    req.destroy = () => {};
    queueMicrotask(() => {
      if (String(url).includes("main.old")) {
        cb(response({ status: 302, headers: { location: "https://abs.twimg.com/responsive-web/client-web/main.new.js" } }));
        return;
      }
      cb(response({ body: `queryId:"Abcdefghijklmnop",operationName:"CreateNoteTweet"` }));
    });
    return req;
  };
  const body = await fetchPublicJs("https://abs.twimg.com/responsive-web/client-web/main.old.js", { request });
  assert.match(body, /CreateNoteTweet/);
  assert.equal(seen.length, 2);
  await assert.rejects(
    () => fetchPublicJs("https://x.com/home", { request }),
    /non public client-web/,
  );
});

test("fetchPublicJs reports HTTP errors and timeouts", async () => {
  const request = (_url, _opts, cb) => {
    const req = new EventEmitter();
    req.end = () => {};
    req.destroy = (error) => req.emit("error", error);
    queueMicrotask(() => cb(response({ status: 404, body: "missing" })));
    return req;
  };
  await assert.rejects(
    () => fetchPublicJs("https://abs.twimg.com/responsive-web/client-web/ondemand.s.missing.js", { request, attempts: 4, sleep: async () => { throw new Error("404 must not retry"); } }),
    /HTTP 404/,
  );
  const timingOut = (_url, _opts, cb) => {
    const req = new EventEmitter();
    req.end = () => {};
    req.destroy = (error) => req.emit("error", error);
    queueMicrotask(() => req.emit("timeout"));
    return req;
  };
  await assert.rejects(
    () => fetchPublicJs("https://abs.twimg.com/responsive-web/client-web/main.slow.js", { request: timingOut, attempts: 1 }),
    /timeout/,
  );
  const failing = () => {
    const req = new EventEmitter();
    req.end = () => {};
    req.destroy = () => {};
    queueMicrotask(() => req.emit("error", new Error("socket down")));
    return req;
  };
  await assert.rejects(
    () => fetchPublicJs("https://abs.twimg.com/responsive-web/client-web/main.down.js", { request: failing, attempts: 1 }),
    /socket down/,
  );
});

test("fetchPublicJs retries a reset, then returns the body", async () => {
  const sleeps = [];
  let n = 0;
  const request = (_url, _opts, cb) => {
    n += 1;
    const req = new EventEmitter();
    req.end = () => {};
    req.destroy = () => {};
    queueMicrotask(() => {
      if (n < 3) {
        const error = new Error("read ECONNRESET");
        error.code = "ECONNRESET";
        req.emit("error", error);
        return;
      }
      cb(response({ body: "[38], 16[39], 16" }));
    });
    return req;
  };
  const body = await fetchPublicJs("https://abs.twimg.com/responsive-web/client-web/ondemand.s.retry.js", {
    request,
    sleep: async (ms) => { sleeps.push(ms); },
  });
  assert.equal(body, "[38], 16[39], 16");
  assert.equal(n, 3);
  assert.deepEqual(sleeps, [publicJsBackoffMs(0), publicJsBackoffMs(1)]);
  assert.equal(isRetryablePublicJsError(new Error("public JS HTTP 502 for x")), true);
  assert.equal(isRetryablePublicJsError(new Error("public JS HTTP 404 for x")), false);
  await assert.rejects(
    () => fetchPublicJs("https://abs.twimg.com/responsive-web/client-web/ondemand.s.reset.js", {
      request: () => {
        const req = new EventEmitter();
        req.end = () => {};
        req.destroy = () => {};
        queueMicrotask(() => req.emit("error", new Error("read ECONNRESET")));
        return req;
      },
      attempts: 2,
      sleep: async () => {},
    }),
    /ECONNRESET/,
  );
});

test("fetchPublicJs aborts the socket instead of retrying", async () => {
  const url = "https://abs.twimg.com/responsive-web/client-web/ondemand.s.hang.js";
  const already = new AbortController();
  already.abort();
  let called = 0;
  await assert.rejects(
    () => fetchPublicJs(url, {
      signal: already.signal,
      request: () => { called += 1; throw new Error("request should not run"); },
    }),
    /abort/i,
  );
  assert.equal(called, 0);

  let destroyed = 0;
  const inflight = new AbortController();
  const pending = fetchPublicJs(url, {
    signal: inflight.signal,
    attempts: 4,
    sleep: async () => { throw new Error("must not retry after abort"); },
    request: () => {
      const req = new EventEmitter();
      req.end = () => {};
      req.destroy = (error) => {
        destroyed += 1;
        queueMicrotask(() => req.emit("error", error || new Error("read ECONNRESET")));
      };
      queueMicrotask(() => inflight.abort());
      return req;
    },
  });
  await assert.rejects(pending, /abort/i);
  assert.equal(destroyed, 1);

  const duringSleep = new AbortController();
  let tries = 0;
  const sleeping = fetchPublicJs(url, {
    signal: duringSleep.signal,
    attempts: 4,
    request: () => {
      tries += 1;
      const req = new EventEmitter();
      req.end = () => {};
      req.destroy = () => {};
      queueMicrotask(() => req.emit("error", new Error("read ECONNRESET")));
      return req;
    },
  });
  setTimeout(() => duringSleep.abort(), 20);
  await assert.rejects(sleeping, /abort/i);
  assert.equal(tries, 1);
});
