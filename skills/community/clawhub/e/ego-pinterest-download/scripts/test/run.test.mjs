import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { execute } from "../lib/run.mjs";

function jpeg(size = 180) {
  const buf = Buffer.alloc(size, 9);
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

function pin(id, extra = {}) {
  return {
    type: "pin",
    id: String(id),
    title: `Pin ${id}`,
    images: { orig: { url: `https://i.pinimg.com/originals/aa/bb/${id}.jpg`, width: 1080, height: 1920 } },
    ...extra,
  };
}

function baseConfig(dir, extra = {}) {
  return {
    command: "search",
    query: "wallpaper",
    pin: "",
    board: "",
    urls: [],
    limit: 2,
    outDir: dir,
    size: "originals",
    media: "image",
    previews: 0,
    bookmark: "",
    keepBrowser: false,
    allowAnonymous: false,
    taskName: "unit",
    maxVideoBytes: 5_000,
    maxPages: 4,
    ...extra,
  };
}

function harness(impl) {
  const calls = { open: 0, finish: 0, urls: [], bytes: [], keep: null };
  const browser = {
    async open(opts) {
      calls.open += 1;
      calls.keep = opts.keepBrowser;
      calls.startUrl = opts.startUrl;
      const session = impl(calls, opts);
      return {
        spaceId: 11,
        goto: async (url) => {
          calls.goto = url;
        },
        url: async () => session.currentUrl || "https://www.pinterest.com/pin/88/",
        detect: async () => session.detect,
        fetchJson: async (url) => {
          calls.urls.push(url);
          return session.fetchJson(url, calls);
        },
        domImages: async () => (session.dom ? session.dom() : []),
        fetchBytes: async (url, options) => {
          calls.bytes.push(url);
          return session.fetchBytes(url, options);
        },
        finish: async () => {
          calls.finish += 1;
          if (session.finishError) throw new Error(session.finishError);
        },
      };
    },
  };
  return { browser, calls };
}

const loggedOut = { url: "https://www.pinterest.com/search/pins/?q=wallpaper", title: "Pinterest", unauth: true, profile: false, authCookie: false };
const loggedIn = { url: "https://www.pinterest.com/search/pins/?q=wallpaper", title: "Pinterest", unauth: false, profile: true, authCookie: true };

function imageBytes() {
  return { ok: true, status: 200, type: "image/jpeg", buf: jpeg(), error: null };
}

async function withDir(fn) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "pinterest-unit-"));
  try {
    await fn(dir);
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
}

test("logged-out search soft-fails and still tells the user to sign in", async () => {
  await withDir(async (dir) => {
    const { browser, calls } = harness(() => ({ detect: loggedOut, fetchJson() { throw new Error("should not search"); } }));
    const summary = await execute(baseConfig(dir), { browser, fs, path, now: () => 1 });
    assert.equal(summary.login_required, true);
    assert.equal(summary.exitCode, 2);
    assert.equal(summary.ok, false);
    assert.equal(summary.downloads.length, 0);
    assert.match(summary.login_tip, /Ego Lite/);
    assert.match(summary.login_tip_zh, /登录/);
    assert.ok(summary.how_to_login.length >= 3);
    assert.equal(calls.finish, 1);
    assert.equal(calls.bytes.length, 0);
    const manifest = JSON.parse(await fs.readFile(path.join(dir, "manifest.json"), "utf8"));
    assert.equal(manifest.login_required, true);
  });
});

test("anonymous search downloads originals and keeps the login tip", async () => {
  await withDir(async (dir) => {
    const pages = [
      { items: [pin(1), { type: "story", id: "x" }, pin("e1_hidden")], bookmark: "page-2" },
      { items: [pin(1), pin(2, { is_promoted: true }), pin(3)], bookmark: "-end-" },
    ];
    const { browser, calls } = harness(() => ({
      detect: loggedOut,
      fetchJson() {
        const page = pages.shift();
        return { ok: true, status: 200, body: { resource_response: { message: "确定", data: { results: page.items }, bookmark: page.bookmark } } };
      },
      fetchBytes: async (url) => (url.includes("/originals/") ? { ok: false, status: 404, type: "text/html", buf: Buffer.from("no"), error: "HTTP 404" } : imageBytes()),
    }));
    const summary = await execute(baseConfig(dir, { allowAnonymous: true, limit: 2 }), { browser, fs, path, now: () => 2 });
    assert.equal(summary.ok, true);
    assert.equal(summary.exitCode, 0);
    assert.equal(summary.anonymous, true);
    assert.equal(summary.method, "BaseSearchResource");
    assert.equal(summary.downloads.length, 2);
    assert.match(summary.login_tip, /anonymous/i);
    assert.ok(calls.bytes.some((url) => url.includes("/736x/")));
    const saved = await fs.readdir(dir);
    assert.ok(saved.some((name) => name.endsWith(".jpg")));
  });
});

test("search falls back to the DOM when the resource call fails", async () => {
  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return { ok: false, status: 500, body: "" };
      },
      dom: () => ["https://i.pinimg.com/236x/aa/bb/cc.jpg", "https://i.pinimg.com/236x/aa/bb/dd.jpg"],
      fetchBytes: async () => imageBytes(),
    }));
    const summary = await execute(baseConfig(dir, { allowAnonymous: true, limit: 1 }), { browser, fs, path, now: () => 3 });
    assert.equal(summary.method, "dom");
    assert.equal(summary.downloads.length, 1);
    assert.equal(summary.failures[0].stage, "BaseSearchResource");
  });
});

test("related pins, a single pin, and a board feed", async () => {
  await withDir(async (dir) => {
    const { browser, calls } = harness(() => ({
      detect: loggedIn,
      fetchJson(url) {
        if (url.includes("RelatedModulesResource")) {
          return { ok: true, status: 200, body: { resource_response: { data: [pin(9)], bookmark: "-end-" } } };
        }
        return { ok: true, status: 200, body: "" };
      },
      fetchBytes: async () => imageBytes(),
    }));
    const related = await execute(baseConfig(dir, { command: "related", pin: "https://www.pinterest.com/pin/nice--9/", limit: 1 }), {
      browser,
      fs,
      path,
      now: () => 4,
    });
    assert.equal(related.ok, true);
    assert.equal(related.method, "RelatedModulesResource");
    assert.equal(related.pin_id, "9");
    assert.match(calls.startUrl, /\/pin\/9\//);
  });

  await withDir(async (dir) => {
    const { browser, calls } = harness(() => ({
      detect: loggedIn,
      currentUrl: "https://www.pinterest.com/pin/88/",
      fetchJson() {
        return { ok: true, status: 200, body: { resource_response: { data: pin(88) } } };
      },
      fetchBytes: async () => imageBytes(),
    }));
    const one = await execute(baseConfig(dir, { command: "pin", pin: "https://pin.it/abc" }), { browser, fs, path, now: () => 5 });
    assert.equal(one.pin_id, "88");
    assert.equal(one.method, "PinResource");
    assert.equal(calls.goto, "https://pin.it/abc");
  });

  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson(url) {
        if (url.includes("BoardResource")) {
          return { ok: true, status: 200, body: { resource_response: { data: { id: "b1", name: "Walls", pin_count: 3, owner: { username: "ada" } } } } };
        }
        return { ok: true, status: 200, body: { resource_response: { data: { results: [pin(5)] }, bookmark: "-end-" } } };
      },
      fetchBytes: async () => imageBytes(),
    }));
    const board = await execute(baseConfig(dir, { command: "board", board: "https://www.pinterest.com/ada/walls/", limit: 1, keepBrowser: true }), {
      browser,
      fs,
      path,
      now: () => 6,
    });
    assert.equal(board.board_info.name, "Walls");
    assert.equal(board.downloads.length, 1);
    assert.equal(board.method, "BoardFeedResource");
  });
});

test("anonymous ids and bad boards fail before opening a browser", async () => {
  await withDir(async (dir) => {
    const { browser, calls } = harness(() => ({ detect: loggedIn }));
    const summary = await execute(baseConfig(dir, { command: "related", pin: "e1_secret" }), { browser, fs, path, now: () => 7 });
    assert.equal(calls.open, 0);
    assert.equal(summary.exitCode, 2);
    assert.match(summary.error, /e1_/);
    const bad = await execute(baseConfig(dir, { command: "board", board: "/nope" }), { browser, fs, path, now: () => 8 });
    assert.match(bad.error, /board URL/);
    assert.equal(bad.exitCode, 2);
  });
});

test("previews, direct video download, and size caps", async () => {
  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedOut,
      fetchBytes: async (url) => {
        if (url.endsWith(".mp4")) return { ok: true, status: 200, type: "video/mp4", buf: mp4(), error: null };
        if (url.includes("/236x/")) return { ok: false, status: 404, type: "text/html", buf: Buffer.from("x"), error: "HTTP 404" };
        return imageBytes();
      },
    }));
    const preview = await execute(
      baseConfig(dir, {
        command: "preview",
        allowAnonymous: true,
        urls: ["https://i.pinimg.com/originals/aa/bb/cc.jpg", "https://evil.example/a.jpg"],
      }),
      { browser, fs, path, now: () => 9 },
    );
    assert.equal(preview.previews.length, 1);
    assert.equal(preview.previews[0].mimeType, "image/jpeg");
    assert.equal(preview.ok, true);
    assert.equal(preview.failures.length, 1);

    const video = await execute(
      baseConfig(dir, {
        command: "download",
        allowAnonymous: true,
        media: "image",
        urls: ["https://v.pinimg.com/videos/mc/720p/abc.mp4"],
      }),
      { browser, fs, path, now: () => 10 },
    );
    assert.equal(video.downloads[0].kind, "video");
    assert.equal(video.downloads[0].contentType, "video/mp4");

    const huge = await execute(
      baseConfig(dir, {
        command: "download",
        allowAnonymous: true,
        maxVideoBytes: 50,
        urls: ["https://v.pinimg.com/videos/mc/720p/big.mp4"],
      }),
      { browser, fs, path, now: () => 11 },
    );
    assert.equal(huge.ok, false);
    assert.match(huge.failures[0].error, /larger than 50/);
  });
});

test("video media saves the mp4 and a finish error stays on the summary", async () => {
  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      finishError: "finish failed",
      fetchJson() {
        return {
          ok: true,
          status: 200,
          body: {
            resource_response: {
              data: {
                results: [
                  pin(4, {
                    videos: { video_list: { V_720P: { url: "https://v.pinimg.com/videos/mc/720p/clip.mp4", duration: 1000 } } },
                  }),
                ],
              },
              bookmark: "-end-",
            },
          },
        };
      },
      fetchBytes: async (url) =>
        String(url).includes(".mp4")
          ? { ok: true, status: 200, type: "video/mp4", buf: mp4(), error: null }
          : imageBytes(),
    }));
    const summary = await execute(baseConfig(dir, { allowAnonymous: true, media: "video", limit: 1, previews: 1 }), {
      browser,
      fs,
      path,
      now: () => 12,
    });
    assert.equal(summary.downloads[0].kind, "video");
    assert.equal(summary.previews.length, 1);
    assert.equal(summary.ok, true);
    assert.equal(summary.failures.at(-1).stage, "finish");
  });
});

test("a manifest write failure does not hide the result", async () => {
  let fsCalls = 0;
  const { browser } = harness(() => ({
    detect: loggedIn,
    fetchJson() {
      return { ok: true, status: 200, body: { resource_response: { data: { results: [pin(1)] }, bookmark: "-end-" } } };
    },
    fetchBytes: async (url) => {
      if (String(url).includes("throw")) throw new Error("network down");
      if (String(url).includes("/originals/")) return { ok: false, status: 418, type: "text/html", buf: Buffer.alloc(0) };
      return imageBytes();
    },
  }));
  const summary = await execute(baseConfig("/no-such-dir-for-manifest"), {
    browser,
    fs: {
      mkdir: async () => {
        fsCalls += 1;
        if (fsCalls > 1) throw new Error("read only");
      },
      writeFile: async () => {},
    },
    path,
    now: () => 14,
  });
  assert.equal(summary.ok, true);
  assert.equal(summary.exitCode, 0);
});

test("min resolution skips small pins and iht video URLs try expMp4 first", async () => {
  await withDir(async (dir) => {
    const pages = [
      {
        items: [pin(1, { images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/1.jpg", width: 400, height: 800 } } })],
        bookmark: "page-2",
      },
      {
        items: [pin(2, { images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/2.jpg", width: 1200, height: 800 } } })],
        bookmark: "-end-",
      },
    ];
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        const page = pages.shift();
        return { ok: true, status: 200, body: { resource_response: { data: { results: page.items }, bookmark: page.bookmark } } };
      },
      fetchBytes: async () => imageBytes(),
    }));
    const summary = await execute(baseConfig(dir, { allowAnonymous: true, limit: 1, minWidth: 800 }), { browser, fs, path, now: () => 20 });
    assert.equal(summary.ok, true);
    assert.equal(summary.downloads.length, 1);
    assert.equal(summary.skipped.length, 1);
    assert.match(summary.skipped[0].reason, /width 400 < 800/);
    assert.equal(summary.min_width, 800);
  });

  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return {
          ok: true,
          status: 200,
          body: {
            resource_response: {
              data: {
                results: [
                  pin(3, { images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/3.jpg", width: 1000, height: 400 } } }),
                ],
              },
              bookmark: "-end-",
            },
          },
        };
      },
      fetchBytes: async () => imageBytes(),
    }));
    const summary = await execute(baseConfig(dir, { allowAnonymous: true, limit: 1, minWidth: 800, minHeight: 700 }), {
      browser,
      fs,
      path,
      now: () => 21,
    });
    assert.equal(summary.ok, false);
    assert.equal(summary.exitCode, 1);
    assert.equal(summary.downloads.length, 0);
    assert.match(summary.error, /minimum resolution/);
    assert.match(summary.skipped[0].reason, /height 400 < 700/);
  });

  await withDir(async (dir) => {
    const { browser, calls } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return {
          ok: true,
          status: 200,
          body: {
            resource_response: {
              data: {
                results: [
                  pin(8, {
                    images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/8.jpg", width: 1080, height: 1080 } },
                    videos: {
                      video_list: {
                        V_HLSV4: {
                          url: "https://v1.pinimg.com/videos/iht/hls/ab/cd/ef/abcd.m3u8",
                          width: 320,
                          height: 320,
                        },
                      },
                    },
                  }),
                  pin(9, {
                    images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/9.jpg", width: 1080, height: 1080 } },
                    videos: {
                      video_list: {
                        V_720P: { url: "https://v.pinimg.com/videos/mc/720p/wide.mp4", width: 1280, height: 720, duration: 1000 },
                      },
                    },
                  }),
                ],
              },
              bookmark: "-end-",
            },
          },
        };
      },
      fetchBytes: async (url) =>
        String(url).includes(".mp4") ? { ok: true, status: 200, type: "video/mp4", buf: mp4(), error: null } : imageBytes(),
    }));
    const summary = await execute(baseConfig(dir, { allowAnonymous: true, media: "video", limit: 1, minWidth: 500 }), {
      browser,
      fs,
      path,
      now: () => 22,
    });
    assert.equal(summary.downloads.length, 1);
    assert.equal(summary.downloads[0].kind, "video");
    assert.equal(summary.skipped.length, 1);
    assert.match(summary.skipped[0].reason, /width 320 < 500/);
    assert.equal(calls.bytes[0], "https://v.pinimg.com/videos/mc/720p/wide.mp4");
  });

  await withDir(async (dir) => {
    const cmfv = "https://v1.pinimg.com/videos/iht/hls/f9/91/17/f99117a3c598ab87cd1233848fe90011_720w.cmfv";
    const { browser, calls } = harness(() => ({
      detect: loggedIn,
      fetchBytes: async (url) => {
        if (String(url).includes("/expMp4/") && String(url).includes("_720w.mp4")) {
          return { ok: true, status: 200, type: "video/mp4", buf: mp4(), error: null };
        }
        return { ok: false, status: 404, type: "application/xml", buf: Buffer.alloc(0), error: "HTTP 404" };
      },
    }));
    const summary = await execute(
      baseConfig(dir, { command: "download", allowAnonymous: true, minWidth: 9000, minHeight: 9000, urls: [cmfv] }),
      { browser, fs, path, now: () => 23 },
    );
    assert.equal(summary.ok, true);
    assert.equal(summary.downloads[0].kind, "video");
    assert.equal(summary.skipped.length, 0);
    assert.equal(calls.bytes[0], "https://v1.pinimg.com/videos/iht/expMp4/f9/91/17/f99117a3c598ab87cd1233848fe90011_720w.mp4");
    const saved = await fs.readFile(summary.downloads[0].path);
    assert.equal(saved.slice(4, 8).toString("ascii"), "ftyp");
  });

  await withDir(async (dir) => {
    const { browser } = harness(() => ({
      detect: loggedIn,
      fetchJson() {
        return { ok: true, status: 200, body: { resource_response: { data: pin(4, { images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/4.jpg", width: 200, height: 200 } } }) } } };
      },
      fetchBytes: async () => imageBytes(),
    }));
    const summary = await execute(baseConfig(dir, { command: "pin", pin: "4", minWidth: 500 }), { browser, fs, path, now: () => 24 });
    assert.equal(summary.exitCode, 1);
    assert.equal(summary.downloads.length, 0);
    assert.equal(summary.pins.length, 1);
    assert.equal(summary.skipped.length, 1);
  });
});

test("a browser open failure is reported without a stack escape", async () => {
  await withDir(async (dir) => {
    const browser = {
      async open() {
        throw new Error("ego unavailable");
      },
    };
    const summary = await execute(baseConfig(dir, { allowAnonymous: true }), { browser, fs, path, now: () => 13 });
    assert.equal(summary.ok, false);
    assert.match(summary.error, /ego unavailable/);
    assert.equal(summary.exitCode, 1);
  });
});
