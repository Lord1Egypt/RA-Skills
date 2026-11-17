import assert from "node:assert/strict";
import test from "node:test";
import { resolveOperationQuery } from "../lib/post-flow.mjs";
import { HOME_URL } from "../lib/pure.mjs";
import { bodyText, createXSession, readCookieJar } from "../lib/session.mjs";

function installDocument(partial = {}) {
  const links = partial.links || [];
  globalThis.document = {
    body: partial.body === null ? null : { innerText: partial.text ?? "发帖" },
    documentElement: partial.documentElement === null ? null : { lang: partial.lang ?? "zh-CN", outerHTML: partial.html ?? "<html>ok</html>" },
    cookie: partial.cookie ?? "",
    querySelector(selector) {
      if (String(selector).includes("AppTabBar_Profile_Link")) return partial.profile ?? null;
      return null;
    },
    querySelectorAll(selector) {
      if (String(selector).includes("loading-x-anim")) return partial.frames || [];
      return links;
    },
  };
}

function link(label, href) {
  return { innerText: label, getAttribute() { return href; } };
}

function fakePage(overrides = {}) {
  const calls = { goto: [], fetch: [], idle: 0, timeout: 0, finish: [] };
  const state = { response: overrides.response ?? { status: 200, body: '{"ok":true}' } };
  const page = {
    async url() { return overrides.url ?? "https://x.com/home"; },
    async title() { return overrides.title ?? "主页 / X"; },
    async goto(url) { calls.goto.push(url); },
    async waitForLoadState() { calls.idle += 1; },
    async waitForTimeout(ms) { calls.timeout = ms; },
    async evaluate(fn) {
      if (overrides.evaluateThrows) throw new Error("evaluate down");
      if (overrides.evaluateNull) return null;
      return fn();
    },
    async fetch(url, opts) {
      calls.fetch.push({ url, opts });
      return state.response;
    },
    async cdp() {
      return overrides.cdp ?? { cookies: [{ name: "auth_token", value: "auth-secret" }, { name: "ct0", value: "jar-secret" }] };
    },
  };
  const task = {
    spaceId: 19,
    async finish(arg) { calls.finish.push(arg); },
    async handOff() { calls.hand = (calls.hand || 0) + 1; },
  };
  return { page, task, calls, state };
}

test("readCookieJar falls back and reports a failed read", async () => {
  assert.deepEqual(await readCookieJar(null), { cookies: [], read: false });
  assert.deepEqual(await readCookieJar({}), { cookies: [], read: false });
  const direct = await readCookieJar({
    async cdp(_method, args) {
      assert.deepEqual(args, undefined);
      return { cookies: [{ name: "auth_token", value: "s" }] };
    },
  });
  assert.equal(direct.read, true);
  let calls = 0;
  const fallback = await readCookieJar({
    async cdp() {
      calls += 1;
      if (calls === 1) return { cookies: null };
      return { cookies: [{ name: "ct0", value: "s" }] };
    },
  });
  assert.equal(fallback.cookies[0].name, "ct0");
  const thrown = await readCookieJar({
    async cdp() { throw new Error("cdp down"); },
  });
  assert.equal(thrown.read, false);
  let n = 0;
  const second = await readCookieJar({
    async cdp() {
      n += 1;
      if (n === 1) throw new Error("scoped");
      return { nope: true };
    },
  });
  assert.equal(second.read, false);
});

test("createXSession requires a task and a page", () => {
  assert.throws(() => createXSession(), /requires task and page/);
  assert.throws(() => createXSession({ task: {} }), /requires task and page/);
});

test("detect reads profile chrome without returning cookie values", async () => {
  installDocument({
    cookie: "ct0=doc-secret; auth_token=also-secret",
    profile: { getAttribute() { return "/Suchuanyi"; } },
  });
  const harness = fakePage();
  const session = createXSession(harness);
  const detected = await session.detect();
  assert.equal(detected.authCookie, true);
  assert.equal(detected.csrfCookie, true);
  assert.equal(detected.profileHref, "/Suchuanyi");
  assert.equal(detected.lang, "zh-CN");
  assert.equal(JSON.stringify(detected).includes("secret"), false);
  const named = await session.screenName();
  assert.equal(named, "/Suchuanyi");
  const csrf = await session.csrfToken();
  assert.equal(csrf, "doc-secret");
  assert.match(await session.pageSource(), /<html>/);
});

test("profile label fallback, empty document, and thrown probes", async () => {
  installDocument({
    profile: null,
    links: [link("Home", "/home"), link("个人资料", "/Suchuanyi")],
    cookie: "guest=1",
  });
  const harness = fakePage({ cdp: { cookies: [] } });
  const session = createXSession(harness);
  const detected = await session.detect();
  assert.equal(detected.profileHref, "/Suchuanyi");
  assert.equal(detected.authCookie, false);
  assert.equal(await session.screenName(), "/Suchuanyi");
  installDocument({ profile: null, links: [link("Home", "/home")], cookie: "" });
  assert.equal(await createXSession(fakePage()).screenName(), "");

  installDocument({
    profile: { getAttribute() { return ""; } },
    links: [link("Profile", null)],
    body: null,
    documentElement: null,
    cookie: "",
    html: "",
  });
  const empty = createXSession(fakePage({
    cdp: { cookies: [{ name: "ct0", value: "jar-secret" }] },
  }));
  const blank = await empty.detect();
  assert.equal(blank.text, "");
  assert.equal(blank.profileHref, "");
  assert.equal(await empty.pageSource(), "");
  assert.equal(await empty.csrfToken(), "jar-secret");

  const broken = fakePage({
    evaluateThrows: true,
    url: "about:blank",
    cdp: { cookies: [{ name: "ct0", value: "from-jar" }] },
  });
  broken.page.url = async () => { throw new Error("no url"); };
  broken.page.title = async () => { throw new Error("no title"); };
  const recovered = createXSession(broken);
  const detectedBroken = await recovered.detect();
  assert.equal(detectedBroken.url, "");
  assert.equal(detectedBroken.title, "");
  assert.equal(await recovered.csrfToken(), "from-jar");

  installDocument({ cookie: "" });
  const noCsrf = createXSession(fakePage({ evaluateThrows: true, cdp: { cookies: [{ name: "guest" }] } }));
  assert.equal(await noCsrf.csrfToken(), "");
});

test("animation paths and a client transaction id come from the live document", async () => {
  const pathD = "M 10 20 C 1 2 3 4 5 6 7 8 9 10 11";
  installDocument({
    html: `<meta name="twitter-site-verification" content="AAAAAAAA"><script>12:"ondemand.s" })[e]||e)+"."+({12:"h4sh"</script>`,
    frames: [
      { children: [{ children: [{}, { getAttribute() { return pathD; } }] }] },
      { children: [] },
    ],
  });
  const harness = fakePage();
  const publicCalls = [];
  const session = createXSession({
    ...harness,
    fetchPublicJs: async (url) => {
      publicCalls.push(url);
      return "(a[0], 16)(a[1], 16)";
    },
  });
  const paths = await session.animationPaths();
  assert.equal(paths[0], pathD);
  assert.equal(paths[1], "");
  const id = await session.clientTransaction({ method: "POST", path: "/i/api/graphql/abc/CreateNoteTweet" });
  assert.equal(id.source, "generated");
  assert.equal(String(id.id).includes("="), false);
  assert.match(publicCalls.at(-1), /ondemand\.s\.h4sha\.js/);
  assert.equal(harness.calls.fetch.some((call) => String(call.url).includes("abs.twimg.com")), false);

  const empty = createXSession(fakePage({ evaluateNull: true }));
  assert.deepEqual(await empty.animationPaths(), []);
});

test("js bytes decode, and a live header is reused when indices are missing", () => {
  assert.equal(bodyText(Buffer.from("[38], 16")), "[38], 16");
  assert.equal(bodyText(new Uint8Array(Buffer.from("abc"))), "abc");
  assert.equal(bodyText({ a: 1 }), '{"a":1}');
  assert.equal(bodyText(null), "");
});

test("bytes already in the Ego page are used without another Node fetch", async () => {
  const pathD = "M 10 20 C 1 2 3 4 5 6 7 8 9 10 11";
  const ondemand = "https://abs.twimg.com/responsive-web/client-web/ondemand.s.h4sha.js";
  const main = "https://abs.twimg.com/responsive-web/client-web/main.live.js";
  const html = `<meta name="twitter-site-verification" content="AAAAAAAA"><svg id="loading-x-anim-0"><path d="M 0 0"/><path d="${pathD}"/></svg><script src="${ondemand}"></script><script src="${main}"></script>`;
  installDocument({ html });
  const harness = fakePage({ response: { status: 200, body: html } });
  const cdpCalls = [];
  harness.page.cdp = async (method, args) => {
    cdpCalls.push(method);
    if (method === "Page.getResourceTree") {
      return {
        frameTree: {
          frame: { id: "main" },
          resources: [
            { url: ondemand, type: "Script" },
            { url: main, type: "Script", requestId: "req-main" },
          ],
        },
      };
    }
    if (method === "Page.getResourceContent") {
      if (String(args.url).includes("ondemand")) return { content: "(a[0], 16)(a[1], 16)" };
      return { content: "" };
    }
    if (method === "Network.getResponseBody") {
      assert.equal(args.requestId, "req-main");
      return {
        body: Buffer.from('queryId:"LiveNoteQueryId123",operationName:"CreateNoteTweet"').toString("base64"),
        base64Encoded: true,
      };
    }
    return { cookies: [] };
  };
  const nodeCalls = [];
  const session = createXSession({
    ...harness,
    fetchPublicJs: async (url) => {
      nodeCalls.push(url);
      throw new Error("read ECONNRESET");
    },
  });
  const id = await session.clientTransaction({ method: "POST", path: "/i/api/graphql/abc/CreateNoteTweet" });
  assert.equal(id.source, "generated");
  assert.equal(nodeCalls.length, 0);
  assert.equal(harness.calls.fetch.some((call) => String(call.url).includes("abs.twimg.com")), false);
  assert.equal(cdpCalls.includes("Page.getResourceContent"), true);
  const discovered = await resolveOperationQuery(session, "CreateNoteTweet", "");
  assert.equal(discovered.queryId, "LiveNoteQueryId123");
  assert.equal(discovered.source, "bundle");
  assert.equal(cdpCalls.includes("Network.getResponseBody"), true);

  const bare = fakePage({ response: { status: 200, body: html } });
  bare.page.cdp = async () => { throw new Error("cdp down"); };
  const failed = createXSession({
    ...bare,
    fetchPublicJs: async () => { throw new Error("read ECONNRESET"); },
  });
  await assert.rejects(
    () => failed.clientTransaction({ method: "POST", path: "/i/api/graphql/abc/CreateNoteTweet" }),
    /read ECONNRESET; browser cache empty/,
  );
});

test("an empty page cache is filled through the Ego browser when Node is refused", async () => {
  const pathD = "M 10 20 C 1 2 3 4 5 6 7 8 9 10 11";
  const ondemand = "https://abs.twimg.com/responsive-web/client-web/ondemand.s.h4sha.js";
  const html = `<meta name="twitter-site-verification" content="AAAAAAAA"><svg id="loading-x-anim-0"><path d="M 0 0"/><path d="${pathD}"/></svg><script src="${ondemand}"></script>`;
  installDocument({ html });
  const harness = fakePage({ response: { status: 200, body: html } });
  const cdpCalls = [];
  const indices = "(a[0], 16)(a[1], 16)";
  harness.page.cdp = async (method, args) => {
    cdpCalls.push(method);
    if (method === "Page.getResourceTree") {
      return { frameTree: { frame: { id: "main" }, resources: [] } };
    }
    if (method === "Network.loadNetworkResource") {
      assert.equal(args.frameId, "main");
      assert.equal(args.url, ondemand);
      assert.equal(args.options.includeCredentials, false);
      return { resource: { success: true, httpStatusCode: 200, stream: "ondemand-stream" } };
    }
    if (method === "IO.read") {
      assert.equal(args.handle, "ondemand-stream");
      return { base64Encoded: true, data: Buffer.from(indices).toString("base64"), eof: true };
    }
    if (method === "IO.close") return {};
    return { cookies: [] };
  };
  const nodeCalls = [];
  const session = createXSession({
    ...harness,
    fetchPublicJs: async (url) => {
      nodeCalls.push(url);
      throw new Error("connect ECONNREFUSED 127.0.0.1:443");
    },
  });
  const id = await session.clientTransaction({ method: "POST", path: "/i/api/graphql/abc/CreateTweet" });
  assert.equal(id.source, "generated");
  assert.equal(String(id.id).includes("="), false);
  assert.equal(cdpCalls.includes("Network.loadNetworkResource"), true);
  assert.equal(cdpCalls.includes("IO.read"), true);
  assert.equal(harness.calls.fetch.some((call) => String(call.url).includes("abs.twimg.com")), false);
  assert.equal(harness.calls.goto.includes("https://x.com/compose/post"), false);
});

test("a header from another GraphQL call is not reused when indices are missing", async () => {
  installDocument({ html: "<html>logged-in home without shell</html>" });
  const harness = fakePage();
  const session = createXSession(harness);
  await assert.rejects(
    () => session.clientTransaction({ method: "POST", path: "/i/api/graphql/abc/CreateNoteTweet" }),
    /ondemand\.s|transaction materials/,
  );
});

test("fetch, navigation, and finish", async () => {
  installDocument();
  const harness = fakePage();
  const session = createXSession(harness);
  await session.ensureSite();
  assert.deepEqual(harness.calls.goto, []);
  harness.page.url = async () => "https://twitter.com/home";
  await session.ensureSite();
  assert.deepEqual(harness.calls.goto, []);
  harness.page.url = async () => "";
  await session.ensureSite();
  assert.equal(harness.calls.goto[0], HOME_URL);
  assert.equal(harness.calls.timeout, 800);

  const elsewhere = fakePage();
  elsewhere.page.url = async () => { throw new Error("no url"); };
  elsewhere.page.waitForLoadState = async () => { throw new Error("sockets"); };
  delete elsewhere.page.waitForTimeout;
  const moved = createXSession(elsewhere);
  await moved.ensureSite();
  assert.equal(elsewhere.calls.goto[0], HOME_URL);
  await moved.goto("https://x.com/home");

  await assert.rejects(
    () => session.fetchText("https://abs.twimg.com/responsive-web/client-web/main.js"),
    /Node, not page\.fetch/,
  );
  harness.state.response = { status: 200, body: { queryId: "abc" } };
  assert.match(await session.fetchText("https://x.com/bundle"), /queryId/);
  harness.state.response = { status: 200, body: null };
  assert.equal(await session.fetchText("https://x.com/empty"), "");

  const posted = await session.postJson({
    url: "https://x.com/i/api/graphql/abc/CreateTweet",
    headers: { "x-csrf-token": "secret" },
    body: { variables: { tweet_text: "hi" } },
  });
  assert.equal(posted.status, 200);
  const sent = harness.calls.fetch.at(-1);
  assert.equal(sent.opts.method, "POST");
  assert.equal(sent.opts.credentials, "include");
  assert.match(sent.opts.body, /tweet_text/);
  harness.state.response = null;
  const emptyPost = await session.postJson({ url: "https://x.com/i/api/graphql/abc/CreateTweet", headers: {}, body: {} });
  assert.equal(emptyPost.status, 0);
  harness.state.response = { status: 200, body: "{\"ok\":true}" };
  assert.deepEqual((await session.postJson({ url: "https://x.com/x", headers: {}, body: {} })).body, { ok: true });

  await session.finish();
  await session.finish();
  assert.deepEqual(harness.calls.finish, [{ keep: [] }]);
  const kept = createXSession({ ...harness, keep: true });
  await kept.finish();
  assert.deepEqual(harness.calls.finish.at(-1), { keep: ["p1"] });
  await session.cleanup();
  await session.handOff();
  assert.equal(harness.calls.hand, 1);
});

test("uploadImages runs INIT APPEND FINALIZE inside page.evaluate", async () => {
  const calls = [];
  const page = {
    async evaluate(_fn, step) {
      calls.push(step);
      if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"2117874109082427392\"}" };
      if (step.command === "APPEND") return { status: 204, body: "" };
      if (step.command === "FINALIZE") return { status: 201, body: "{\"media_id_string\":\"2117874109082427392\"}" };
      throw new Error(step.command);
    },
  };
  const task = { spaceId: 3, async finish() {} };
  const data = Buffer.from([1, 2, 3, 4]);
  const uploaded = await createXSession({ task, page }).uploadImages({
    bearer: "TOKEN",
    csrfToken: "ct0",
    images: [{
      path: "/tmp/card.png",
      bytes: data.length,
      md5: "81dc9bdb52d04dc20036dbd8313ed055",
      mediaType: "image/png",
      data,
    }],
  });
  assert.deepEqual(uploaded, [{ path: "/tmp/card.png", media_id: "2117874109082427392", bytes: 4 }]);
  assert.deepEqual(calls.map((step) => step.command), ["INIT", "APPEND", "FINALIZE"]);
  assert.equal(calls[0]["x-client-transaction-id"], undefined);
  assert.equal(calls[1].authorization, "Bearer TOKEN");
  assert.match(calls[1].url, /command=APPEND&media_id=2117874109082427392&segment_index=0/);
  assert.equal(calls.some((step) => step.command === "STATUS"), false);
});
