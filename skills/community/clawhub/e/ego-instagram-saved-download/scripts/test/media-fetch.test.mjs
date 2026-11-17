import assert from "node:assert/strict";
import fs from "node:fs/promises";
import http from "node:http";
import test from "node:test";
import {
  browserSave,
  browserTimeout,
  fetchMediaBytes,
  requestBytes,
  shouldTryAlternateFetch,
  usefulMedia,
} from "../lib/media-fetch.mjs";

function jpeg(size = 120) {
  const buf = Buffer.alloc(size, 7);
  buf[0] = 0xff;
  buf[1] = 0xd8;
  buf[2] = 0xff;
  return buf;
}

function mp4(size = 180) {
  const buf = Buffer.alloc(size, 3);
  buf.write("ftyp", 4, "ascii");
  return buf;
}

function listen(handler) {
  const server = http.createServer(handler);
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      resolve({
        url: `http://127.0.0.1:${port}`,
        close: () => new Promise((done) => server.close(done)),
      });
    });
  });
}

test("alternate fetch is only for transport failures and non-media 200s", () => {
  const image = { ok: true, status: 200, type: "image/jpeg", buf: jpeg(), error: null };
  assert.equal(usefulMedia(image), true);
  assert.equal(shouldTryAlternateFetch(image), false);
  assert.equal(shouldTryAlternateFetch(null), true);
  assert.equal(shouldTryAlternateFetch({ ok: false, status: 404, type: "text/html", buf: Buffer.alloc(0), error: "HTTP 404" }), false);
  assert.equal(shouldTryAlternateFetch({ ok: false, status: 0, type: "", buf: Buffer.alloc(0), error: "fetch failed" }), true);
  const html = { ok: true, status: 200, type: "text/html", buf: Buffer.from("not-an-image!!"), error: null };
  assert.equal(shouldTryAlternateFetch(html), true);
  const typed = { ok: true, status: 200, type: "video/mp4", buf: Buffer.alloc(16, 1), error: null };
  assert.equal(usefulMedia(typed), true);
  assert.equal(browserTimeout("https://v1.pinimg.com/a.mp4"), 120_000);
  assert.equal(browserTimeout("https://i.pinimg.com/a.jpg"), 20_000);
});

test("fetchMediaBytes falls through to HTTP/1.1 and then the browser after fetch failed", async () => {
  const calls = [];
  const transport = new Error("fetch failed");
  transport.cause = { code: "ENETUNREACH" };
  const onlyNode = await fetchMediaBytes({
    url: "https://v1.pinimg.com/clip.mp4",
    nodeFetch: async () => {
      throw transport;
    },
  });
  assert.match(onlyNode.error, /ENETUNREACH/);

  const viaDirect = await fetchMediaBytes({
    url: "https://v1.pinimg.com/clip.mp4",
    nodeFetch: async () => {
      throw transport;
    },
    directFetch: async () => {
      calls.push("direct");
      return { ok: true, status: 200, type: "video/mp4", buf: mp4(), error: null };
    },
    browserFetch: async () => {
      calls.push("browser");
      throw new Error("should not run");
    },
  });
  assert.equal(viaDirect.type, "video/mp4");
  assert.deepEqual(calls, ["direct"]);

  calls.length = 0;
  const denied = await fetchMediaBytes({
    url: "https://i.pinimg.com/originals/a.jpg",
    nodeFetch: async () => ({ ok: false, status: 404, type: "text/html", buf: Buffer.alloc(0), error: "HTTP 404" }),
    directFetch: async () => {
      calls.push("direct");
      return null;
    },
  });
  assert.equal(denied.error, "HTTP 404");
  assert.deepEqual(calls, []);

  const viaBrowser = await fetchMediaBytes({
    url: "https://scontent.cdninstagram.com/a.jpg",
    nodeFetch: async () => {
      throw new Error("fetch failed");
    },
    directFetch: async () => {
      throw new Error("timeout");
    },
    browserFetch: async () => ({ ok: true, status: 200, type: "image/jpeg", buf: jpeg(), error: null }),
  });
  assert.equal(viaBrowser.ok, true);
  assert.equal(sniff(viaBrowser.buf), "image/jpeg");

  const browserError = await fetchMediaBytes({
    url: "https://v1.pinimg.com/clip.mp4",
    nodeFetch: async () => null,
    browserFetch: async () => ({ ok: false, status: 0, type: "", buf: Buffer.alloc(0), error: "page blocked" }),
  });
  assert.equal(browserError.error, "page blocked");

  const keepNode = await fetchMediaBytes({
    url: "https://v1.pinimg.com/clip.mp4",
    nodeFetch: async () => {
      throw new Error("fetch failed");
    },
    browserFetch: async () => ({ ok: false, status: 0, type: "", buf: Buffer.alloc(0) }),
  });
  assert.match(keepNode.error, /fetch failed/);

  const browserThrew = await fetchMediaBytes({
    url: "https://v1.pinimg.com/clip.mp4",
    nodeFetch: async () => {
      throw new Error("fetch failed");
    },
    directFetch: async () => ({ ok: false, status: 0, type: "", buf: Buffer.alloc(0), error: "still down" }),
    browserFetch: async () => {
      throw new Error("cors blocked");
    },
  });
  assert.equal(browserThrew.error, "cors blocked");
});

function sniff(buf) {
  return buf[0] === 0xff && buf[1] === 0xd8 ? "image/jpeg" : "";
}

test("browserSave accepts the file the page wrote and reports a transport error", async () => {
  const image = jpeg();
  const page = {
    async fetch(_url, options) {
      assert.equal(options.timeout, 120_000);
      await fs.writeFile(options.saveAs, image);
    },
  };
  const saved = await browserSave(page, "https://v1.pinimg.com/videos/a.mp4", { referer: "https://www.pinterest.com/" });
  assert.equal(saved.ok, true);
  assert.equal(saved.type, "image/jpeg");

  const html = await browserSave(
    {
      async fetch(_url, options) {
        await fs.writeFile(options.saveAs, Buffer.from("definitely not media"));
      },
    },
    "https://i.pinimg.com/a.jpg",
    {},
  );
  assert.match(html.error, /not image or video/);

  const huge = await browserSave(
    {
      async fetch(_url, options) {
        await fs.writeFile(options.saveAs, jpeg(200));
      },
    },
    "https://i.pinimg.com/a.jpg",
    { maxBytes: 50 },
  );
  assert.match(huge.error, /larger than 50/);

  const failed = await browserSave(
    {
      async fetch() {
        const error = new Error("fetch failed");
        error.cause = { code: "ECONNRESET" };
        throw error;
      },
    },
    "https://cdninstagram.com/a.jpg",
    {},
  );
  assert.match(failed.error, /ECONNRESET/);
});

test("requestBytes follows a redirect and enforces the size cap", async () => {
  const server = await listen((req, res) => {
    if (req.url === "/go") {
      res.writeHead(302, { location: "/file.jpg" });
      res.end();
      return;
    }
    if (req.url === "/big") {
      res.writeHead(200, { "content-type": "video/mp4", "content-length": "99999" });
      res.end(jpeg());
      return;
    }
    if (req.url === "/overflow") {
      res.writeHead(200, { "content-type": "image/jpeg" });
      res.end(jpeg(80));
      return;
    }
    if (req.url === "/missing") {
      res.writeHead(404, { "content-type": "text/plain" });
      res.end("no");
      return;
    }
    if (req.url === "/loop") {
      res.writeHead(302, { location: "/loop" });
      res.end();
      return;
    }
    res.writeHead(200, { "content-type": "image/jpeg" });
    res.end(jpeg());
  });
  try {
    const saved = await requestBytes(`${server.url}/go`);
    assert.equal(saved.ok, true);
    assert.equal(saved.type, "image/jpeg");
    assert.equal(saved.buf[0], 0xff);
    const capped = await requestBytes(`${server.url}/big`, { maxBytes: 10 });
    assert.match(capped.error, /larger than 10/);
    const overflow = await requestBytes(`${server.url}/overflow`, { maxBytes: 10 });
    assert.match(overflow.error, /larger than 10/);
    const missing = await requestBytes(`${server.url}/missing`);
    assert.equal(missing.status, 404);
    assert.equal(shouldTryAlternateFetch(missing), false);
    const loop = await requestBytes(`${server.url}/loop`, { redirects: 0 });
    assert.match(loop.error, /too many redirects/);
  } finally {
    await server.close();
  }
});

test("requestBytes rejects when the socket fails", async () => {
  await assert.rejects(requestBytes("http://127.0.0.1:1/", { timeoutMs: 400 }));
});

test("ego-deps does not return video URLs before the browser fallback", async () => {
  const source = await fs.readFile(new URL("../lib/ego-deps.mjs", import.meta.url), "utf8");
  assert.match(source, /fetchMediaBytes\(/);
  assert.match(source, /directFetch:/);
  assert.match(source, /browserFetch:/);
  assert.doesNotMatch(source, /mp4\|m3u8\|cmfv/);
  assert.match(source, /finish\(\{ keep: keepBrowser \? \["p1"\] : \[\] \}\)/);
});
