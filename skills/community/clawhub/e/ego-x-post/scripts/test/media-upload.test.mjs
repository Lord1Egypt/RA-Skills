import assert from "node:assert/strict";
import crypto from "node:crypto";
import test from "node:test";
import { MAX_STATUS_POLLS, buildUploadHeaders, uploadImagesOnPage, uploadOneImage, uploadStepInPage } from "../lib/media-upload.mjs";

function imageOf(bytes, extra = {}) {
  const data = Buffer.from(bytes);
  return {
    path: Object.prototype.hasOwnProperty.call(extra, "path") ? extra.path : "/tmp/card.png",
    bytes: extra.bytes == null ? data.length : extra.bytes,
    md5: extra.md5 || crypto.createHash("md5").update(data).digest("hex"),
    mediaType: extra.mediaType || "image/png",
    data,
  };
}

function scripted(handler) {
  const calls = [];
  return {
    calls,
    async evaluate(fn, step) {
      calls.push({ fn, step });
      return handler(step, calls);
    },
  };
}

function ready(id, finalize = {}) {
  return scripted((step) => {
    if (step.command === "INIT") {
      return { status: 202, body: JSON.stringify({ media_id_string: id, expires_after_secs: 86400 }) };
    }
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return { status: 201, body: JSON.stringify({ media_id_string: id, ...finalize }) };
    }
    throw new Error(`unexpected ${step.command}`);
  });
}

const auth = { bearer: "TOKEN", csrfToken: "csrf-secret", sleep: async () => {}, chunkBytes: 4 };

test("buildUploadHeaders mirrors the captured upload headers", () => {
  assert.deepEqual(buildUploadHeaders({ bearer: "Bearer TOKEN", csrfToken: "ct0" }), {
    authorization: "Bearer TOKEN",
    csrfToken: "ct0",
  });
  assert.throws(() => buildUploadHeaders({ bearer: "   ", csrfToken: "ct0" }), /bearer missing/);
  assert.throws(() => buildUploadHeaders({ bearer: "TOKEN" }), /ct0 missing/);
});

test("uploadStepInPage posts one media blob and does not set content-type", async () => {
  const seen = [];
  const previous = globalThis.fetch;
  globalThis.fetch = async (url, init) => {
    const part = init.body && typeof init.body.get === "function" ? init.body.get("media") : null;
    const bytes = part ? Buffer.from(await part.arrayBuffer()) : null;
    seen.push({
      url,
      method: init.method,
      credentials: init.credentials,
      headers: { ...init.headers },
      hasBody: init.body != null,
      name: part && part.name,
      type: part && part.type,
      bytes: bytes && [...bytes],
      signal: Boolean(init.signal),
    });
    return { status: init.body ? 204 : 202, async text() { return init.body ? "" : "{\"ok\":true}"; } };
  };
  try {
    const appended = await uploadStepInPage({
      command: "APPEND",
      url: "https://upload.x.com/i/media/upload.json?command=APPEND",
      authorization: "Bearer TOKEN",
      csrfToken: "ct0",
      b64: Buffer.from([1, 2, 3, 4]).toString("base64"),
      "x-client-transaction-id": "must-not-be-sent",
    });
    assert.equal(appended.status, 204);
    assert.equal(appended.body, "");
    assert.equal(seen[0].method, "POST");
    assert.equal(seen[0].credentials, "include");
    assert.equal(seen[0].name, "blob");
    assert.equal(seen[0].type, "application/octet-stream");
    assert.deepEqual(seen[0].bytes, [1, 2, 3, 4]);
    assert.deepEqual(Object.keys(seen[0].headers).sort(), ["authorization", "x-csrf-token", "x-twitter-auth-type"]);
    assert.equal(seen[0].headers["x-csrf-token"], "ct0");
    assert.equal(seen[0].signal, true);

      const saved = globalThis.AbortSignal;
    try {
      globalThis.AbortSignal = undefined;
      await uploadStepInPage({
        command: "INIT",
        method: "POST",
        url: "https://upload.x.com/i/media/upload.json?command=INIT",
        authorization: "Bearer TOKEN",
        csrfToken: "ct0",
      });
      globalThis.AbortSignal = {};
      await uploadStepInPage({
        command: "APPEND",
        method: "POST",
        url: "https://upload.x.com/i/media/upload.json?command=APPEND",
        authorization: "Bearer TOKEN",
        csrfToken: "ct0",
      });
    } finally {
      globalThis.AbortSignal = saved;
    }
    assert.equal(seen[1].hasBody, false);
    assert.equal(seen[1].signal, false);
    assert.equal(seen[2].bytes.length, 0);
    assert.equal(seen[2].signal, false);
    globalThis.fetch = async () => { throw new Error("network down"); };
    await assert.rejects(uploadStepInPage({
      command: "INIT",
      url: "https://upload.x.com/i/media/upload.json?command=INIT",
      authorization: "Bearer TOKEN",
      csrfToken: "ct0",
    }), /network down/);
  } finally {
    globalThis.fetch = previous;
  }
});

test("a png uploads in one segment and does not call STATUS", async () => {
  const page = ready("2117874109082427392");
  const image = imageOf([9, 8, 7, 6]);
  const id = await uploadOneImage(page, image, auth);
  assert.equal(id, "2117874109082427392");
  assert.deepEqual(page.calls.map((call) => call.step.command), ["INIT", "APPEND", "FINALIZE"]);
  assert.equal(page.calls[0].fn, uploadStepInPage);
  assert.equal(page.calls[0].step.url, "https://upload.x.com/i/media/upload.json?command=INIT&total_bytes=4&media_type=image%2Fpng&media_category=tweet_image");
  assert.equal(page.calls[0].step.authorization, "Bearer TOKEN");
  assert.equal(page.calls[0].step.csrfToken, "csrf-secret");
  assert.equal(page.calls[0].step["x-client-transaction-id"], undefined);
  assert.match(page.calls[1].step.url, /segment_index=0/);
  assert.match(page.calls[2].step.url, new RegExp(`original_md5=${image.md5}`));
});

test("multi-segment APPEND uses segment_index 0,1,2", async () => {
  const page = ready("99");
  const image = imageOf([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  await uploadOneImage(page, image, { ...auth, chunkBytes: 3 });
  const appends = page.calls.filter((call) => call.step.command === "APPEND");
  assert.deepEqual(appends.map((call) => call.step.url.match(/segment_index=(\d)/)[1]), ["0", "1", "2"]);
  const bytes = Buffer.concat(appends.map((call) => Buffer.from(call.step.b64, "base64")));
  assert.deepEqual([...bytes], [1, 2, 3, 4, 5, 6, 7, 8, 9]);
});

test("retries follow the captured attempt counts and stop on 4xx", async () => {
  let initFails = 1;
  const retried = scripted((step) => {
    if (step.command === "INIT" && initFails) {
      initFails -= 1;
      return { status: 500, body: "later" };
    }
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"5\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"5\"}" };
  });
  assert.equal(await uploadOneImage(retried, imageOf([1]), auth), "5");
  assert.equal(retried.calls.filter((call) => call.step.command === "INIT").length, 2);

  let thrown = 0;
  const flaky = scripted((step) => {
    if (step.command === "APPEND" && thrown < 1) {
      thrown += 1;
      throw new Error("socket");
    }
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"6\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"6\"}" };
  });
  assert.equal(await uploadOneImage(flaky, imageOf([1, 2]), auth), "6");

  const bad = scripted(() => ({ status: 400, body: "bad\nsegment" }));
  await assert.rejects(uploadOneImage(bad, imageOf([1]), auth), /INIT failed \(HTTP 400\): bad segment/);
  assert.equal(bad.calls.length, 1);

  const limited = scripted(() => ({ status: 429, body: "slow down" }));
  await assert.rejects(uploadOneImage(limited, imageOf([1]), auth), /Not retried/);
  assert.equal(limited.calls.length, 1);

  const denied = scripted(() => ({ status: 401, body: "{\"error\":\"Could not authenticate you.\"}" }));
  await assert.rejects(uploadOneImage(denied, imageOf([1]), auth), (error) => {
    assert.equal(error.loginRequired, true);
    assert.match(error.message, /HTTP 401/);
    return true;
  });
  assert.equal(denied.calls.length, 1);

  const forbidden = scripted(() => ({ status: 403, body: "" }));
  await assert.rejects(uploadOneImage(forbidden, imageOf([1]), auth), /HTTP 403/);
  assert.equal(forbidden.calls.length, 1);

  let timeouts = 1;
  const once = scripted((step) => {
    if (step.command === "INIT" && timeouts) {
      timeouts -= 1;
      return { status: 408, body: "" };
    }
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"7\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"7\"}" };
  });
  assert.equal(await uploadOneImage(once, imageOf([1]), auth), "7");

  let blanks = 1;
  const blank = scripted((step) => {
    if (step.command === "INIT" && blanks) {
      blanks -= 1;
      return null;
    }
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"8\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"8\"}" };
  });
  assert.equal(await uploadOneImage(blank, imageOf([1]), auth), "8");
  assert.equal(blank.calls.filter((call) => call.step.command === "INIT").length, 2);

  const nothing = scripted(() => null);
  await assert.rejects(uploadOneImage(nothing, imageOf([1]), auth), /no response/);
  assert.equal(nothing.calls.length, 2);

  let sockets = 0;
  const dead = scripted(() => { sockets += 1; throw new Error("socket"); });
  await assert.rejects(uploadOneImage(dead, imageOf([1]), auth), /socket/);
  assert.equal(sockets, 2);

  const weird = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "not-json" };
    return { status: 500, body: "" };
  });
  await assert.rejects(uploadOneImage(weird, imageOf([1]), auth), /non-JSON/);

  const emptyBody = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "" };
    return { status: 500, body: "" };
  });
  await assert.rejects(uploadOneImage(emptyBody, imageOf([1]), auth), /empty body/);

  const numeric = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":2117874109082427392}" };
    return { status: 500, body: "" };
  });
  await assert.rejects(uploadOneImage(numeric, imageOf([1]), auth), /no media_id_string/);

  const longBody = scripted(() => ({ status: 400, body: `x\n${"y".repeat(400)}` }));
  await assert.rejects(uploadOneImage(longBody, imageOf([1]), auth), /y{10,}\.\.\./);
});

test("FINALIZE prefers its media_id_string and polls STATUS only with processing_info", async () => {
  const sleeps = [];
  let polls = 0;
  const page = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"111\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return {
        status: 201,
        body: JSON.stringify({
          media_id_string: "222",
          processing_info: { state: "pending", check_after_secs: 2 },
        }),
      };
    }
    polls += 1;
    assert.equal(step.method, "GET");
    assert.match(step.url, /command=STATUS&media_id=222/);
    if (polls === 1) return { status: 500, body: "again" };
    if (polls === 2) {
      return { status: 200, body: JSON.stringify({ processing_info: { state: "in_progress", check_after_secs: "0" } }) };
    }
    return { status: 200, body: JSON.stringify({ media_id_string: "222", processing_info: { state: "succeeded" } }) };
  });
  const id = await uploadOneImage(page, imageOf([1, 2, 3, 4]), {
    ...auth,
    sleep: async (ms) => { sleeps.push(ms); },
  });
  assert.equal(id, "222");
  assert.deepEqual(sleeps, [2000, 0]);
  assert.equal(page.calls.filter((call) => call.step.command === "STATUS").length, 3);

  const inherited = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"333\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") return { status: 201, body: "{\"image\":{\"image_type\":\"image/jpeg\"}}" };
    throw new Error("status");
  });
  assert.equal(await uploadOneImage(inherited, imageOf([1]), auth), "333");

  const failed = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: JSON.stringify({ media_id_string: "4", processing_info: { state: "failed", error: { code: 2 } } }) };
  });
  await assert.rejects(uploadOneImage(failed, imageOf([1]), auth), /FILE_TOO_LARGE/);
  assert.equal(failed.calls.some((call) => call.step.command === "STATUS"), false);

  const unknown = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{\"state\":\"weird\"}}" };
  });
  await assert.rejects(uploadOneImage(unknown, imageOf([1]), auth), /ended in weird/);

  const nameless = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{}}" };
  });
  await assert.rejects(uploadOneImage(nameless, imageOf([1]), auth), /unknown state/);

  const cleared = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{\"state\":\"pending\",\"check_after_secs\":-1}}" };
    }
    return { status: 200, body: "{\"media_id_string\":\"4\"}" };
  });
  const waited = [];
  assert.equal(await uploadOneImage(cleared, imageOf([1]), {
    ...auth,
    sleep: async (ms) => { waited.push(ms); },
  }), "4");
  assert.deepEqual(waited, [10000]);

  let spins = 0;
  const stuck = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{\"state\":\"pending\",\"check_after_secs\":0}}" };
    }
    spins += 1;
    return { status: 200, body: "{\"processing_info\":{\"state\":\"pending\",\"check_after_secs\":0}}" };
  });
  await assert.rejects(uploadOneImage(stuck, imageOf([1]), auth), /timed out/);
  assert.equal(spins, MAX_STATUS_POLLS);

  let statusTries = 0;
  const statusAuth = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{\"state\":\"in_progress\",\"check_after_secs\":1}}" };
    }
    statusTries += 1;
    if (statusTries === 1) return { status: 401, body: "nope" };
    return { status: 200, body: "{\"processing_info\":{\"state\":\"succeeded\"}}" };
  });
  await assert.rejects(uploadOneImage(statusAuth, imageOf([1]), {
    bearer: "TOKEN",
    csrfToken: "ct0",
    sleep: async () => {},
  }), (error) => {
    assert.equal(error.loginRequired, true);
    return true;
  });
  assert.equal(statusTries, 1);

  const quiet = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{\"state\":\"succeeded\"}}" };
    }
    throw new Error("status");
  });
  assert.equal(await uploadOneImage(quiet, imageOf([1]), {
    bearer: "TOKEN",
    csrfToken: "ct0",
  }), "4");

  const dozed = scripted((step) => {
    if (step.command === "INIT") return { status: 202, body: "{\"media_id_string\":\"4\"}" };
    if (step.command === "APPEND") return { status: 204, body: "" };
    if (step.command === "FINALIZE") {
      return { status: 201, body: "{\"media_id_string\":\"4\",\"processing_info\":{\"state\":\"pending\",\"check_after_secs\":0}}" };
    }
    return { status: 200, body: "{\"processing_info\":{\"state\":\"succeeded\"}}" };
  });
  assert.equal(await uploadOneImage(dozed, imageOf([1]), { bearer: "TOKEN", csrfToken: "ct0" }), "4");
});

test("several images stay in order and a later failure names the file", async () => {
  let inits = 0;
  const ordered = scripted((step) => {
    if (step.command === "INIT") {
      inits += 1;
      if (inits === 2) return { status: 400, body: "second failed" };
      return { status: 202, body: "{\"media_id_string\":\"1\"}" };
    }
    if (step.command === "APPEND") return { status: 204, body: "" };
    return { status: 201, body: "{\"media_id_string\":\"1\"}" };
  });
  await assert.rejects(uploadImagesOnPage(ordered, {
    ...auth,
    images: [imageOf([1], { path: "/tmp/a.png" }), imageOf([2], { path: "/tmp/b.png" })],
  }), (error) => {
    assert.match(error.message, /\/tmp\/b.png: INIT failed/);
    assert.match(error.message, /earlier image was uploaded/);
    assert.equal(error.loginRequired, undefined);
    return true;
  });

  const both = scripted((step) => {
    if (step.command === "INIT") {
      const id = step.url.includes("total_bytes=1") ? "11" : "22";
      return { status: 202, body: JSON.stringify({ media_id_string: id }) };
    }
    if (step.command === "APPEND") return { status: 204, body: "" };
    const id = step.url.includes("media_id=11") ? "11" : "22";
    return { status: 201, body: JSON.stringify({ media_id_string: id }) };
  });
  const uploaded = await uploadImagesOnPage(both, {
    ...auth,
    images: [imageOf([1], { path: "/tmp/a.png" }), imageOf([2, 3], { path: "/tmp/b.jpg" })],
  });
  assert.deepEqual(uploaded, [
    { path: "/tmp/a.png", media_id: "11", bytes: 1 },
    { path: "/tmp/b.jpg", media_id: "22", bytes: 2 },
  ]);
  assert.deepEqual(await uploadImagesOnPage(both, { ...auth, images: [] }), []);

  await assert.rejects(uploadOneImage({}, imageOf([1]), auth), /page.evaluate is required/);
  await assert.rejects(uploadOneImage({ evaluate() {} }, null, auth), /Image is empty/);
  await assert.rejects(uploadOneImage({ evaluate() {} }, imageOf([1, 2], { bytes: 1 }), auth), /byte count/);
  await assert.rejects(uploadOneImage({ evaluate() {} }, imageOf([1], { md5: "NOPE" }), auth), /md5 is missing/);
  await assert.rejects(uploadOneImage({ evaluate() {} }, imageOf([1], { mediaType: "image/gif" }), auth), /Unsupported image type/);

  const authed = scripted(() => ({ status: 401, body: "" }));
  await assert.rejects(uploadImagesOnPage(authed, { ...auth, images: [imageOf([1], { path: "" })] }), (error) => {
    assert.equal(error.loginRequired, true);
    assert.match(error.message, /^image: INIT failed/);
    return true;
  });
});
