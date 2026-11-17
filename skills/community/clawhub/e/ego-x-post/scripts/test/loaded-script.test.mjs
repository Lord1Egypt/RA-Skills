import assert from "node:assert/strict";
import test from "node:test";
import {
  decodeCdpBody,
  decodeIoChunk,
  frameNodes,
  injectClientScript,
  loadClientWebBytes,
  readIoStream,
  readLoadedClientScript,
  readNetworkResource,
  sameClientScript,
  warmClientScript,
} from "../lib/loaded-script.mjs";

const ONDEMAND = "https://abs.twimg.com/responsive-web/client-web/ondemand.s.h4sha.js";
const MAIN = "https://abs.twimg.com/responsive-web/client-web/main.live.js";

function pageWith({ scripts = [], resources = [], cdp } = {}) {
  const calls = [];
  return {
    calls,
    async evaluate(fn) {
      globalThis.document = { scripts };
      globalThis.performance = {
        getEntriesByType(type) {
          if (type !== "resource") return [];
          return resources.map((name) => ({ name }));
        },
      };
      return fn();
    },
    async cdp(method, args) {
      calls.push({ method, args });
      if (cdp) return cdp(method, args);
      return {};
    },
  };
}

test("client script identity ignores query strings", () => {
  assert.equal(sameClientScript(`${ONDEMAND}?x=1`, ONDEMAND), true);
  assert.equal(sameClientScript("https://x.com/main.js", MAIN), false);
  assert.equal(sameClientScript("not a url", ONDEMAND), false);
  assert.equal(decodeCdpBody(null), "");
  assert.equal(decodeCdpBody({ content: "abc" }), "abc");
  assert.equal(decodeCdpBody({ body: Buffer.from("indices").toString("base64"), base64Encoded: true }), "indices");
  assert.equal(decodeCdpBody({ content: "" }), "");
  assert.equal(frameNodes(null).length, 0);
  assert.equal(frameNodes({ frameTree: { frame: { id: "A" }, childFrames: [{ frame: { id: "B" } }] } }).length, 2);
});

test("script textContent is used when the page already holds the source", async () => {
  const page = pageWith({
    scripts: [{ src: ONDEMAND, textContent: "(a[0], 16)(a[1], 16)" }],
  });
  const text = await readLoadedClientScript(page, ONDEMAND);
  assert.equal(text, "(a[0], 16)(a[1], 16)");
  assert.equal(page.calls.length, 0);
  assert.equal(await readLoadedClientScript(page, "https://x.com/home"), "");
  assert.equal(await readLoadedClientScript(null, ONDEMAND), "");
});

test("performance resource URL is read with Page.getResourceContent", async () => {
  const loaded = `${MAIN}?cb=1`;
  const page = pageWith({
    resources: [loaded],
    cdp(method, args) {
      if (method === "Page.getResourceTree") {
        return { frameTree: { frame: { id: "main" }, resources: [], childFrames: [{ frame: { id: "child" }, resources: [] }] } };
      }
      if (method === "Page.getResourceContent") {
        assert.equal(args.frameId, "main");
        assert.equal(args.url, loaded);
        return { content: 'queryId:"FromCacheQueryId123",operationName:"CreateNoteTweet"' };
      }
      return {};
    },
  });
  const text = await readLoadedClientScript(page, MAIN);
  assert.match(text, /FromCacheQueryId123/);
  assert.equal(page.calls.some((call) => call.method === "Network.getResponseBody"), false);
});

test("Network.getResponseBody supplies bytes when resource content is empty", async () => {
  const page = pageWith({
    cdp(method, args) {
      if (method === "Page.getResourceTree") {
        return {
          frameTree: {
            frame: { id: "main" },
            resources: [{ url: ONDEMAND, type: "Script", requestId: "req-1" }],
          },
        };
      }
      if (method === "Page.getResourceContent") {
        if (page.calls.filter((call) => call.method === "Page.getResourceContent").length === 1) {
          throw new Error("content evicted");
        }
        return { content: "" };
      }
      if (method === "Network.getResponseBody") {
        assert.equal(args.requestId, "req-1");
        return { body: Buffer.from("(a[0], 16)(a[1], 16)").toString("base64"), base64Encoded: true };
      }
      return {};
    },
  });
  // First getResourceContent throws, so the body comes from Network.getResponseBody.
  const text = await readLoadedClientScript(page, ONDEMAND);
  assert.equal(text, "(a[0], 16)(a[1], 16)");
  assert.equal(page.calls.filter((call) => call.method === "Network.getResponseBody").length, 1);

  const down = pageWith({
    cdp() { throw new Error("cdp down"); },
  });
  assert.equal(await readLoadedClientScript(down, ONDEMAND), "");
});

test("IO chunks decode and a stalled browser fetch is abandoned", async () => {
  assert.equal(decodeIoChunk(null), "");
  assert.equal(decodeIoChunk({ data: "" }), "");
  assert.equal(decodeIoChunk({ data: "plain" }), "plain");
  assert.equal(decodeIoChunk({ data: Buffer.from("indices").toString("base64"), base64Encoded: true }), "indices");
  assert.equal(await readIoStream(null, "h"), "");
  assert.equal(await readIoStream({ cdp() { return {}; } }, ""), "");

  const chunks = [
    { data: "aa", eof: false },
    { data: Buffer.from("bb").toString("base64"), base64Encoded: true, eof: true },
  ];
  let cursor = 0;
  let closed = 0;
  const text = await readIoStream({
    async cdp(method) {
      if (method === "IO.close") {
        closed += 1;
        throw new Error("already closed");
      }
      const chunk = chunks[cursor];
      cursor += 1;
      return chunk;
    },
  }, "stream-1");
  assert.equal(text, "aabb");
  assert.equal(closed, 1);

  let partialClosed = 0;
  let partialReads = 0;
  const partial = await readIoStream({
    async cdp(method) {
      if (method === "IO.close") {
        partialClosed += 1;
        throw new Error("close broke");
      }
      partialReads += 1;
      if (partialReads === 1) return { data: "abc", eof: false };
      throw new Error("read broke");
    },
  }, "stream-2");
  assert.equal(partial, "abc");
  assert.equal(partialClosed, 1);
});

test("Network.loadNetworkResource returns client-web bytes through the browser", async () => {
  assert.equal(await readNetworkResource(null, ONDEMAND), "");
  assert.equal(await readNetworkResource({ async cdp() { return {}; } }, "https://x.com/home"), "");

  const calls = [];
  const page = {
    async cdp(method, args) {
      calls.push(method);
      if (method === "Page.getResourceTree") {
        if (calls.filter((name) => name === "Page.getResourceTree").length === 1) {
          return { frameTree: { frame: {}, childFrames: [{ frame: { id: "child" }, resources: [] }] } };
        }
        return { frameTree: { frame: { id: "main" }, resources: [] } };
      }
      if (method === "Network.loadNetworkResource") {
        assert.equal(args.options.includeCredentials, false);
        if (args.frameId === "child") return { resource: { success: false, netErrorName: "ERR_FAILED" } };
        if (calls.filter((name) => name === "Network.loadNetworkResource").length === 2) {
          return { success: false };
        }
        if (calls.filter((name) => name === "Network.loadNetworkResource").length === 3) {
          return { resource: { success: true, httpStatusCode: 404, stream: "missing" } };
        }
        if (calls.filter((name) => name === "Network.loadNetworkResource").length === 4) {
          return { resource: { success: true, httpStatusCode: 200 } };
        }
        return {
          resource: { success: true, httpStatusCode: 200, streamId: "body" },
        };
      }
      if (method === "IO.read") {
        assert.equal(args.handle, "body");
        return { data: "(a[0], 16)(a[1], 16)", eof: true };
      }
      if (method === "IO.close") return {};
      return null;
    },
  };
  assert.equal(await readNetworkResource(page, ONDEMAND), "");
  assert.equal(await readNetworkResource(page, ONDEMAND), "");
  assert.equal(await readNetworkResource(page, ONDEMAND), "");
  assert.equal(await readNetworkResource(page, ONDEMAND), "");
  assert.equal(await readNetworkResource(page, ONDEMAND), "(a[0], 16)(a[1], 16)");

  const stalled = {
    async cdp(method) {
      if (method === "Page.getResourceTree") return { frameTree: { frame: { id: "main" } } };
      if (method === "Network.loadNetworkResource") return new Promise(() => {});
      return {};
    },
  };
  assert.equal(await readNetworkResource(stalled, ONDEMAND, 30), "");
  const stopped = new AbortController();
  stopped.abort();
  const idle = {
    async cdp(method) {
      if (method === "Page.getResourceTree") return { frameTree: { frame: { id: "main" }, resources: [] } };
      return {};
    },
  };
  assert.equal(await readNetworkResource(idle, ONDEMAND, 1000, stopped.signal), "");
  const broken = { async cdp() { throw new Error("cdp down"); } };
  assert.equal(await readNetworkResource(broken, ONDEMAND), "");
});

function warmingPage({ content = "(a[0], 16)(a[1], 16)", network = "fail", armOnInject = true } = {}) {
  let armed = false;
  let injected = 0;
  const page = {
    get injected() { return injected; },
    async evaluate(fn, ...args) {
      if (args.length) injected += 1;
      const scripts = [];
      globalThis.document = {
        scripts,
        head: {
          appendChild(node) {
            scripts.push(node);
            if (armOnInject) armed = true;
          },
        },
        createElement() {
          return { src: "", async: false };
        },
      };
      globalThis.performance = {
        getEntriesByType() {
          return armed ? [{ name: ONDEMAND }] : [];
        },
      };
      return fn(...args);
    },
    async cdp(method, args) {
      if (method === "Page.getResourceTree") {
        return { frameTree: { frame: { id: "main" }, resources: [] } };
      }
      if (method === "Network.loadNetworkResource") {
        if (network === "bytes") {
          return { resource: { success: true, httpStatusCode: 200, stream: "warm" } };
        }
        if (network === "hang") return new Promise((resolve) => setTimeout(() => resolve({ resource: { success: false } }), 40));
        return { resource: { success: false, netErrorName: "ERR_METHOD_NOT_FOUND" } };
      }
      if (method === "IO.read") {
        assert.equal(args.handle, "warm");
        return { data: content, eof: true };
      }
      if (method === "IO.close") return {};
      if (method === "Page.getResourceContent") {
        return { content: armed ? content : "" };
      }
      return {};
    },
  };
  return page;
}

test("warmClientScript loads ondemand.s in the page when the cache is empty", async () => {
  assert.equal(await warmClientScript(null, "https://x.com/no.js"), "");
  assert.equal(await injectClientScript(null, ONDEMAND), "unavailable");
  assert.equal(await injectClientScript({ async evaluate() { throw new Error("eval down"); } }, ONDEMAND), "unavailable");
  assert.equal(await injectClientScript({ async evaluate() { return "nope"; } }, "https://x.com/no.js"), "skipped");
  const present = {
    async evaluate(fn, ...args) {
      globalThis.document = {
        scripts: [{ src: args[0] }],
        head: { appendChild() { throw new Error("should not append"); } },
        createElement() { return { src: "" }; },
      };
      return fn(...args);
    },
  };
  assert.equal(await injectClientScript(present, ONDEMAND), "pending");

  const cached = pageWith({
    scripts: [{ src: ONDEMAND, textContent: "(a[0], 16)(a[1], 16)" }],
  });
  assert.equal(await warmClientScript(cached, ONDEMAND), "(a[0], 16)(a[1], 16)");
  assert.equal(cached.calls.some((call) => call.method === "Network.loadNetworkResource"), false);

  const viaNetwork = warmingPage({ network: "bytes" });
  assert.equal(await warmClientScript(viaNetwork, ONDEMAND), "(a[0], 16)(a[1], 16)");
  assert.equal(viaNetwork.injected, 0);

  let ready = false;
  const viaTag = warmingPage({ network: "fail" });
  const original = viaTag.cdp.bind(viaTag);
  viaTag.cdp = async (method, args) => {
    if (method === "Page.getResourceContent") return { content: ready ? "(a[0], 16)(a[1], 16)" : "" };
    return original(method, args);
  };
  const text = await warmClientScript(viaTag, ONDEMAND, {
    wait: async () => { ready = true; },
  });
  assert.equal(text, "(a[0], 16)(a[1], 16)");
  assert.equal(viaTag.injected, 1);

  const controller = new AbortController();
  let waits = 0;
  const aborted = warmingPage({ network: "fail", armOnInject: false });
  assert.equal(await warmClientScript(aborted, ONDEMAND, {
    signal: controller.signal,
    wait: async () => {
      waits += 1;
      controller.abort();
    },
  }), "");
  assert.equal(waits, 1);

  const thrown = warmingPage({ network: "fail", armOnInject: false });
  assert.equal(await warmClientScript(thrown, ONDEMAND, {
    wait: async () => { throw new Error("browser warm aborted"); },
  }), "");

  const liveSignal = new AbortController();
  const liveWait = warmingPage({ network: "fail", armOnInject: false });
  const started = Date.now();
  const pending = warmClientScript(liveWait, ONDEMAND, { signal: liveSignal.signal, timeoutMs: 2_000 });
  setTimeout(() => liveSignal.abort(), 80);
  assert.equal(await pending, "");
  const elapsed = Date.now() - started;
  assert.ok(elapsed < 500, `browser warm abort took ${elapsed}ms`);
});

test("loadClientWebBytes races Node and the browser, then keeps the first bytes", async () => {
  let warmed = 0;
  let loaded = 0;
  assert.equal(await loadClientWebBytes({
    url: ONDEMAND,
    readCached: async () => "already",
    warm: async () => { warmed += 1; return ""; },
    loadPublic: async () => { loaded += 1; return ""; },
  }), "already");
  assert.equal(warmed, 0);
  assert.equal(loaded, 0);

  let aborted = false;
  const fromBrowser = await loadClientWebBytes({
    url: ONDEMAND,
    readCached: async () => "",
    warm: async () => "from-browser",
    loadPublic: (_url, options) => new Promise((resolve, reject) => {
      const timer = setTimeout(() => resolve("from-node"), 5_000);
      options.signal.addEventListener("abort", () => {
        clearTimeout(timer);
        aborted = true;
        reject(new Error("public JS aborted"));
      });
    }),
  });
  assert.equal(fromBrowser, "from-browser");
  assert.equal(aborted, true);

  const nodePage = warmingPage({ network: "hang" });
  const fromNode = await loadClientWebBytes({
    url: ONDEMAND,
    readCached: async () => "",
    warm: (url, options) => warmClientScript(nodePage, url, {
      ...options,
      timeoutMs: 1_000,
    }),
    loadPublic: async () => "(a[0], 16)(a[1], 16)",
  });
  assert.equal(fromNode, "(a[0], 16)(a[1], 16)");
  await new Promise((resolve) => setTimeout(resolve, 80));
  assert.equal(nodePage.injected, 0);

  await assert.rejects(
    () => loadClientWebBytes({
      url: ONDEMAND,
      readCached: async () => { throw new Error("cache broke"); },
      warm: async () => { throw new Error("warm down"); },
      loadPublic: async () => { throw new Error("connect ECONNREFUSED 10.0.0.1:443"); },
    }),
    /cache broke.*warm down.*ECONNREFUSED.*browser cache empty/,
  );
  await assert.rejects(
    () => loadClientWebBytes({
      url: ONDEMAND,
      readCached: async () => "",
      warm: async () => "  ",
      loadPublic: async () => "  ",
    }),
    /browser warm empty; empty body; browser cache empty/,
  );

  let reads = 0;
  const late = await loadClientWebBytes({
    url: ONDEMAND,
    readCached: async () => {
      reads += 1;
      return reads > 1 ? "late-bytes" : "";
    },
    warm: async () => "",
    loadPublic: async () => { throw new Error("connect ECONNREFUSED"); },
  });
  assert.equal(late, "late-bytes");
  await assert.rejects(
    () => loadClientWebBytes({
      url: ONDEMAND,
      readCached: async () => "",
      loadPublic: async () => "",
    }),
    /browser warm empty; empty body; browser cache empty/,
  );
});
