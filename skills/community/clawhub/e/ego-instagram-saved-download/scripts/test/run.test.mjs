import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { execute } from "../lib/run.mjs";

function jpeg(size = 160) {
  const buf = Buffer.alloc(size, 8);
  buf[0] = 0xff;
  buf[1] = 0xd8;
  buf[2] = 0xff;
  return buf;
}

function mp4(size = 180) {
  const buf = Buffer.alloc(size, 2);
  buf.write("ftyp", 4, "ascii");
  return buf;
}

function photo(code, caption, extra = {}) {
  return {
    pk: code,
    code,
    media_type: 1,
    caption: { text: caption },
    user: { username: "ada" },
    image_versions2: { candidates: [{ url: `https://scontent.cdninstagram.com/${code}.jpg`, width: 1080, height: 1080 }] },
    ...extra,
  };
}

function base(dir, extra = {}) {
  return {
    command: "saved",
    query: "",
    limit: 2,
    outDir: dir,
    media: "image",
    keepBrowser: false,
    taskName: "ig-unit",
    maxVideoBytes: 500,
    maxPages: 4,
    ...extra,
  };
}

const loggedOut = { url: "https://www.instagram.com/accounts/login/", title: "Instagram", password: true, inbox: false, saved: false, dsUser: false };
const loggedIn = { url: "https://www.instagram.com/saved/all-posts/", title: "Instagram", password: false, inbox: true, saved: true, dsUser: true };

function harness(impl) {
  const calls = { open: 0, finish: 0, urls: [] };
  const browser = {
    async open() {
      calls.open += 1;
      const session = impl(calls);
      return {
        spaceId: 3,
        detect: async () => session.detect,
        fetchJson: async (url) => {
          calls.urls.push(url);
          return session.fetchJson(url);
        },
        domImages: async () => (session.dom ? session.dom() : []),
        fetchBytes: async (url, options) => session.fetchBytes(url, options),
        finish: async () => {
          calls.finish += 1;
          if (session.finishError) throw new Error(session.finishError);
        },
      };
    },
  };
  return { browser, calls };
}

async function withDir(fn) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "ig-saved-unit-"));
  try {
    await fn(dir);
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
}

test("logged-out Saved soft-fails before the feed call", async () => {
  await withDir(async (dir) => {
    const { browser, calls } = harness(() => ({
      detect: loggedOut,
      fetchJson() {
        throw new Error("should not fetch");
      },
    }));
    const summary = await execute(base(dir), { browser, fs, path });
    assert.equal(summary.login_required, true);
    assert.equal(summary.exitCode, 2);
    assert.equal(summary.downloads.length, 0);
    assert.match(summary.login_tip, /Saved/);
    assert.match(summary.login_tip_zh, /收藏/);
    assert.ok(summary.how_to_login.length >= 3);
    assert.equal(calls.urls.length, 0);
    assert.equal(calls.finish, 1);
  });
});

test("logged-in Saved downloads images and can filter by query across pages", async () => {
  await withDir(async (dir) => {
    const pages = [
      { items: [photo("A1", "city"), photo("A2", "beach day")], next: "p2" },
      { items: [photo("A2", "beach day"), photo("A3", "beach night")], next: null },
    ];
    const { browser, calls } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        const page = pages.shift();
        return {
          ok: true,
          status: 200,
          body: { items: page.items, more_available: Boolean(page.next), next_max_id: page.next },
        };
      },
      fetchBytes: async (url) => {
        if (url.includes("missing")) return { ok: false, status: 404, type: "text/html", buf: Buffer.alloc(0) };
        return { ok: true, status: 200, type: "image/jpeg", buf: jpeg(), error: null };
      },
    }));
    const summary = await execute(base(dir, { query: "beach", limit: 2 }), { browser, fs, path });
    assert.equal(summary.ok, true);
    assert.equal(summary.exitCode, 0);
    assert.equal(summary.method, "feed/saved/posts");
    assert.equal(summary.posts_saved, 2);
    assert.equal(summary.downloads.length, 2);
    assert.equal(calls.urls.length, 2);
    assert.match(calls.urls[1], /max_id=p2/);
    const names = (await fs.readdir(dir)).filter((name) => name.endsWith(".jpg"));
    assert.equal(names.length, 2);
  });
});

test("video media saves an mp4 and a later login_required response soft-fails", async () => {
  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return {
          ok: true,
          status: 200,
          body: {
            items: [
              photo("VID1", "clip", {
                media_type: 2,
                video_versions: [{ url: "https://scontent.cdninstagram.com/VID1.mp4", width: 720 }],
              }),
            ],
            more_available: false,
          },
        };
      },
      fetchBytes: async (url) =>
        url.endsWith(".mp4")
          ? { ok: true, status: 200, type: "video/mp4", buf: mp4(), error: null }
          : { ok: true, status: 200, type: "image/jpeg", buf: jpeg(), error: null },
    }));
    const summary = await execute(base(dir, { media: "any", limit: 1 }), { browser, fs, path });
    assert.equal(summary.ok, true);
    assert.ok(summary.downloads.some((row) => row.kind === "video"));
    assert.ok(summary.downloads.some((row) => row.kind === "image"));
  });

  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return { ok: true, status: 200, body: { message: "login_required", status: "fail" } };
      },
    }));
    const summary = await execute(base(dir), { browser, fs, path });
    assert.equal(summary.login_required, true);
    assert.equal(summary.exitCode, 2);
    assert.equal(summary.downloads.length, 0);
  });
});

test("API failure falls back to CDN images already on the page", async () => {
  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return { ok: false, status: 500, body: "" };
      },
      dom: () => ["https://scontent.cdninstagram.com/dom.jpg", "https://evil.example/no.jpg"],
      fetchBytes: async () => ({ ok: true, status: 200, type: "image/jpeg", buf: jpeg(), error: null }),
    }));
    const summary = await execute(base(dir, { limit: 1 }), { browser, fs, path });
    assert.equal(summary.method, "dom");
    assert.equal(summary.downloads.length, 1);
    const queried = await execute(base(dir, { query: "beach" }), { browser, fs, path });
    assert.equal(queried.ok, false);
    assert.equal(queried.method, null);
  });
});

test("a video that is too large is recorded and the browser open failure is caught", async () => {
  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      finishError: "finish failed",
      fetchJson() {
        return {
          ok: true,
          status: 200,
          body: {
            more_available: false,
            items: [photo("BIG", "big", { media_type: 2, video_versions: [{ url: "https://scontent.cdninstagram.com/big.mp4", width: 720 }] })],
          },
        };
      },
      fetchBytes: async () => ({ ok: true, status: 200, type: "video/mp4", buf: mp4(400), error: null }),
    }));
    const summary = await execute(base(dir, { media: "video", limit: 1, maxVideoBytes: 50 }), { browser, fs, path });
    assert.equal(summary.ok, false);
    assert.match(summary.failures[0].error, /larger than 50/);
    assert.equal(summary.failures.at(-1).stage, "finish");
  });

  await withDir(async (dir) => {
    const summary = await execute(base(dir), {
      browser: {
        async open() {
          throw new Error("ego unavailable");
        },
      },
      fs,
      path,
    });
    assert.match(summary.error, /ego unavailable/);
    assert.equal(summary.exitCode, 1);
  });
});
