import assert from "node:assert/strict";
import { test } from "node:test";
import { deflateSync } from "node:zlib";
import {
  COVER_MATCH_MIN,
  bestFingerprintScore,
  classifyLogin,
  coverSlotEvidence,
  declareChoice,
  egoMissingSummary,
  flowErrorBody,
  imageDimsFromBuffer,
  judgeCoverIdentity,
  lumaGridFromRgba,
  pngFingerprint,
  coverSampleFromPng,
  loginRequiredBody,
  manuscriptFromText,
  archivesSearchUrls,
  manuscriptFromArchives,
  pickManuscriptFromArchivePayloads,
  mayClickSubmit,
  parseCheckArgs,
  parsePublishArgs,
  parseTags,
  optionClickReady,
  partitionChoice,
  syncGate,
  planBody,
  publishMode,
  publishSuccessBody,
  ratioWithin,
  resolveEgoExit,
  validatePublishInput,
} from "../lib/pure.mjs";

// --- parsePublishArgs ---

test("parsePublishArgs: required flags and comma tags", () => {
  const r = parsePublishArgs([
    "--video", "/tmp/v.mp4",
    "--title", "标题",
    "--desc", "描述 #话题",
    "--tags", "a,b，c",
    "--yes",
  ]);
  assert.equal(r.ok, true);
  assert.equal(r.args.video, "/tmp/v.mp4");
  assert.equal(r.args.title, "标题");
  assert.equal(r.args.yes, true);
  assert.equal(r.args.tags, "a,b，c");
});

test("parsePublishArgs: inline = syntax and covers", () => {
  const r = parsePublishArgs([
    "--video=/tmp/v.mp4",
    "--title=t",
    "--cover-4x3=/a.png",
    "--cover-16x9=/b.jpg",
    "--space-id=42",
  ]);
  assert.equal(r.ok, true);
  assert.equal(r.args.cover43, "/a.png");
  assert.equal(r.args.cover169, "/b.jpg");
  assert.equal(r.args.spaceId, 42);
});

test("parsePublishArgs: rejects unknown flag and missing value", () => {
  assert.ok(parsePublishArgs(["--nope"]).error);
  assert.ok(parsePublishArgs(["--video"]).error);
  assert.ok(parsePublishArgs(["--space-id", "x"]).error);
});

test("parseCheckArgs", () => {
  assert.deepEqual(parseCheckArgs(["--keep"]), { keep: true, taskName: "", help: false });
  const withName = parseCheckArgs(["--task-name", "s1"]);
  assert.equal(withName.taskName, "s1");
  assert.throws(() => parseCheckArgs(["--bogus"]), /未知参数/);
});

// --- validatePublishInput ---

const good = {
  video: "/tmp/v.mp4",
  title: "t",
  desc: "",
  tags: "",
  cover43: "",
  cover169: "",
  videoExists: true,
  videoSize: 1024 * 1024,
};

test("validatePublishInput: happy path with tag list", () => {
  const r = validatePublishInput({ ...good, tags: "a,b" });
  assert.equal(r.ok, true);
  assert.deepEqual(r.tagList, ["a", "b"]);
  assert.equal(r.sizeMB, 1);
});

test("validatePublishInput: title required and length-capped", () => {
  assert.match(validatePublishInput({ ...good, title: "" }).error, /title|标题/);
  assert.ok(validatePublishInput({ ...good, title: "x".repeat(81) }).error);
});

test("validatePublishInput: desc max 2000", () => {
  assert.ok(validatePublishInput({ ...good, desc: "x".repeat(2001) }).error);
});

test("validatePublishInput: video checks", () => {
  assert.ok(validatePublishInput({ ...good, video: "" }).error);
  assert.match(validatePublishInput({ ...good, videoExists: false }).error, /不存在/);
  assert.match(validatePublishInput({ ...good, video: "/tmp/v.txt" }).error, /格式/);
  assert.ok(validatePublishInput({ ...good, videoSize: 17 * 1024 ** 3 }).error);
});

test("validatePublishInput: covers must come as a pair with right ratios", () => {
  assert.match(validatePublishInput({ ...good, cover43: "/a.png" }).error, /两张/);
  assert.match(validatePublishInput({ ...good, cover169: "/b.jpg" }).error, /两张/);
  const pairOk = validatePublishInput({
    ...good,
    cover43: "/a.png",
    cover169: "/b.jpg",
    cover43Dims: { width: 1080, height: 810 },
    cover169Dims: { width: 1080, height: 608 },
  });
  assert.equal(pairOk.ok, true);
  assert.match(
    validatePublishInput({
      ...good,
      cover43: "/a.png",
      cover169: "/b.jpg",
      cover43Dims: { width: 500, height: 500 },
    }).error,
    /不是目标比例/,
  );
  assert.match(
    validatePublishInput({ ...good, cover43: "/a.gif", cover169: "/b.jpg" }).error,
    /只支持 png\/jpg/,
  );
});

test("validatePublishInput: tag limits", () => {
  assert.ok(validatePublishInput({ ...good, tags: "1,2,3,4,5,6,7,8,9,10,11" }).error);
  assert.ok(validatePublishInput({ ...good, tags: "x".repeat(21) }).error);
  assert.deepEqual(parseTags(" a ，b,,c ").filter(Boolean), ["a", "b", "c"]);
});

// --- imageDimsFromBuffer ---

test("imageDimsFromBuffer: png IHDR", () => {
  const buf = Buffer.alloc(33);
  buf[0] = 0x89; buf[1] = 0x50; buf[2] = 0x4e; buf[3] = 0x47;
  buf.writeUInt32BE(1080, 16);
  buf.writeUInt32BE(810, 20);
  assert.deepEqual(imageDimsFromBuffer(buf), { width: 1080, height: 810, format: "png" });
});

test("imageDimsFromBuffer: jpeg SOF0 with EXIF (APP1) before it", () => {
  const parts = [
    Buffer.from([0xff, 0xd8]),
    Buffer.from([0xff, 0xe1, 0x00, 0x10, ...Array(14).fill(0)]), // APP1
    Buffer.from([0xff, 0xc0, 0x00, 0x11, 0x08, 0x02, 0x60, 0x04, 0x38]),
  ];
  const dims = imageDimsFromBuffer(Buffer.concat(parts));
  assert.deepEqual(dims, { height: 0x0260, width: 0x0438, format: "jpeg" });
});

test("imageDimsFromBuffer: junk returns null", () => {
  assert.equal(imageDimsFromBuffer(Buffer.from("not an image at all!!!!!!!")), null);
  assert.equal(imageDimsFromBuffer(Buffer.alloc(4)), null);
});

test("ratioWithin tolerance", () => {
  assert.equal(ratioWithin(1080, 810, 4 / 3), true);
  assert.equal(ratioWithin(1080, 608, 16 / 9), true);
  assert.equal(ratioWithin(1080, 1440, 4 / 3), false);
  assert.equal(ratioWithin(0, 810, 4 / 3), false);
});

// --- classifyLogin ---

test("classifyLogin: logged in on creator page", () => {
  const r = classifyLogin({
    url: "https://member.bilibili.com/platform/upload/video/frame",
    text: "创作中心 投稿 内容管理 上传视频",
  });
  assert.equal(r.logged_in, true);
});

test("classifyLogin: login wall wins", () => {
  const r = classifyLogin({
    url: "https://passport.bilibili.com/login",
    text: "扫码登录",
  });
  assert.equal(r.logged_in, false);
  const wall = classifyLogin({ url: "https://member.bilibili.com/x", text: "请扫码登录后操作" });
  assert.equal(wall.logged_in, false);
});

// --- bodies / exits ---

test("loginRequiredBody and egoMissingSummary shape", () => {
  const b = loginRequiredBody({ spaceId: 7, url: "u" });
  assert.equal(b.exit_code, 2);
  assert.equal(b.login_required, true);
  assert.ok(b.how_to_login);
  const e = egoMissingSummary("publish");
  assert.equal(e.exit_code, 2);
  assert.match(e.error, /ego-browser/);
});

test("flowErrorBody and planBody and publishSuccessBody", () => {
  assert.deepEqual(flowErrorBody("x", { a: 1 }), { ok: false, error: "x", a: 1 });
  const plan = planBody({ video: "v", sizeMB: 1, title: "t", desc: "", tags: "a,b", cover43: "", cover169: "", spaceId: null });
  assert.equal(plan.exit_code, 3);
  assert.equal(plan.cover_mode, "none");
  assert.match(plan.note, /不打开浏览器/);
  const planC = planBody({ video: "v", sizeMB: 1, title: "t", desc: "", tags: "", cover43: "/a", cover169: "/b", type: "知识" });
  assert.equal(planC.cover_mode, "two-ratio");
  assert.equal(planC.type, "知识");
  const ok = publishSuccessBody({ title: "t", type: "科技数码", tags: ["a"], coverApplied: { "4x3": { width: 1280, height: 960 }, "16x9": { width: 1280, height: 720 } } });
  assert.equal(ok.status, "审核中");
  assert.equal(ok.identity, "unconfirmed");
  assert.equal(ok.url, null);
  const identified = publishSuccessBody({ title: "t", bvid: "BV1uVW46QEZn" });
  assert.equal(identified.url, "https://www.bilibili.com/video/BV1uVW46QEZn/");
  assert.equal(identified.identity, "bvid");
});

test("partitionChoice does not keep a remembered partition for an unknown name", () => {
  assert.deepEqual(partitionChoice({ requested: "", current: "音乐" }), { action: "keep", reason: "remembered", type: "音乐" });
  assert.equal(partitionChoice({ requested: "", current: "" }).action, "fail");
  assert.equal(partitionChoice({ requested: "音乐", current: "音乐" }).action, "keep");
  assert.equal(partitionChoice({ requested: "知识", current: "音乐", options: ["影视", "音乐"] }).reason, "unsupported");
  assert.equal(partitionChoice({ requested: "知识", current: "音乐", options: ["知识", "音乐"] }).action, "select");
});

test("an already displayed declaration is kept and submit cannot be combined with the stop flag", () => {
  assert.equal(declareChoice({ requested: "内容无需标注", current: "内容无需标注", options: [] }).action, "keep");
  assert.equal(declareChoice({ requested: "含AI生成内容", current: "内容无需标注", options: ["含AI生成内容"] }).action, "select");
  assert.equal(declareChoice({ requested: "含AI生成内容", current: "内容无需标注", options: [] }).reason, "closed-or-missing");
  assert.equal(publishMode({ yes: false, stopBeforeSubmit: false }), "plan");
  assert.equal(publishMode({ yes: true, stopBeforeSubmit: true }), "stop-before-submit");
  assert.equal(mayClickSubmit({ yes: true, stopBeforeSubmit: true }).allow, false);
  assert.equal(mayClickSubmit({ yes: true, stopBeforeSubmit: false }).allow, true);
  assert.equal(mayClickSubmit({ yes: false, stopBeforeSubmit: true }).allow, false);
});

test("the sync checkbox stays off only after two consecutive readings", () => {
  assert.equal(syncGate({ readings: [true], clicks: 0 }), "click");
  assert.equal(syncGate({ readings: [true, false], clicks: 1 }), "wait");
  assert.equal(syncGate({ readings: [true, false, false], clicks: 1 }), "ready");
  assert.equal(syncGate({ readings: [false, true], clicks: 1 }), "click");
  assert.equal(syncGate({ readings: [true, true, true, true], clicks: 4 }), "fail");
});

test("a declaration option is clicked only after its row stops moving", () => {
  assert.equal(optionClickReady({ y: 540, height: 36 }), "wait");
  assert.equal(optionClickReady({ previousY: 520, y: 540, height: 36 }), "wait");
  assert.equal(optionClickReady({ previousY: 540, y: 540.4, height: 36 }), "click");
  assert.equal(optionClickReady({ previousY: 540, y: 540, height: 8 }), "wait");
});

test("the 4:3 phone check reads the visible home preview", async () => {
  const { readFile } = await import("node:fs/promises");
  const { fileURLToPath } = await import("node:url");
  const source = await readFile(fileURLToPath(new URL("../post-video.mjs", import.meta.url)), "utf8");
  const show = source.indexOf("显示首页推荐预览");
  const visible = source.indexOf("previewStyle.visibility===\"hidden\"");
  const recheck = source.indexOf("上传 16:9 后未能确认 4:3 槽仍是原图");
  assert.ok(show > 0 && visible > show && recheck > visible);
});

test("the partition list is polled before an unknown name is refused", async () => {
  const { readFile } = await import("node:fs/promises");
  const { fileURLToPath } = await import("node:url");
  const source = await readFile(fileURLToPath(new URL("../post-video.mjs", import.meta.url)), "utf8");
  const open = source.indexOf("打开分区列表");
  const apply = source.indexOf("await applyDeclare()");
  const finalRead = source.indexOf("停投前创作声明回读");
  const refuse = source.indexOf("不在人选列表里");
  assert.ok(open > 0 && refuse > open && apply > refuse && finalRead > apply);
});

test("the submit click stays behind the stop gate", async () => {
  const { readFile } = await import("node:fs/promises");
  const { fileURLToPath } = await import("node:url");
  const source = await readFile(fileURLToPath(new URL("../post-video.mjs", import.meta.url)), "utf8");
  const gate = source.indexOf("mayClickSubmit");
  const click = source.indexOf("点击立即投稿");
  assert.ok(gate > 0 && click > gate);
});

function paintPng(width, height, pixel) {
  const rawRows = [];
  for (let y = 0; y < height; y += 1) {
    const row = Buffer.alloc(1 + width * 3);
    for (let x = 0; x < width; x += 1) {
      const [r, g, b] = pixel(x, y, width, height);
      row[1 + x * 3] = r;
      row[2 + x * 3] = g;
      row[3 + x * 3] = b;
    }
    rawRows.push(row);
  }
  const idat = deflateSync(Buffer.concat(rawRows));
  const chunk = (kind, body) => {
    const type = Buffer.from(kind);
    const length = Buffer.alloc(4);
    length.writeUInt32BE(body.length);
    const crc = Buffer.alloc(4);
    crc.writeUInt32BE(crc32(Buffer.concat([type, body])));
    return Buffer.concat([length, type, body, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8;
  ihdr[9] = 2;
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk("IHDR", ihdr),
    chunk("IDAT", idat),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}

test("cover identity uses the spatial grid, not the average color", () => {
  const blocks = (x, y, width, height) => {
    const left = x < width / 2;
    const top = y < height / 2;
    if (left && top) return [20, 40, 90];
    if (!left && top) return [210, 170, 60];
    if (left && !top) return [40, 40, 40];
    return [120, 70, 90];
  };
  const swapped = (x, y, width, height) => blocks(y * width / height, x * height / width, height, width);
  const gray = (x, y, width) => {
    const value = x < width / 3 ? 20 : x < (2 * width) / 3 ? 140 : 230;
    return [value, value, value];
  };
  const source = pngFingerprint(paintPng(32, 24, blocks));
  const same = pngFingerprint(paintPng(16, 12, blocks));
  const otherLayout = pngFingerprint(paintPng(32, 24, swapped));
  const graySource = pngFingerprint(paintPng(32, 24, gray));
  const grayCopy = pngFingerprint(paintPng(24, 18, gray));
  assert.ok(bestFingerprintScore(same.full, source) >= COVER_MATCH_MIN);
  assert.ok(bestFingerprintScore(otherLayout.full, source) < COVER_MATCH_MIN);
  assert.ok(bestFingerprintScore(grayCopy.full, graySource) >= COVER_MATCH_MIN);
  const unread = judgeCoverIdentity({
    samples: [{ w: 0, h: 0, grid: null }],
    target: 4 / 3,
    source,
    slot: "cover-phone-view-home-video-img",
    requireRatio: true,
  });
  assert.equal(unread.status, "unread");
  const wrongRatio = judgeCoverIdentity({
    samples: [{ w: 500, h: 281, grid: source.full }],
    target: 4 / 3,
    source,
    slot: "cover-phone-view-home-video-img",
    requireRatio: true,
  });
  assert.equal(wrongRatio.status, "mismatch");
  const wrongPicture = judgeCoverIdentity({
    samples: [{ w: 500, h: 375, grid: otherLayout.full }],
    target: 4 / 3,
    source,
    other: otherLayout,
    slot: "cover-phone-view-home-video-img",
    requireRatio: true,
  });
  assert.equal(wrongPicture.status, "identity");
  const matched = judgeCoverIdentity({
    samples: [{ w: 8, h: 8 }, { w: 500, h: 375, grid: same.full }],
    target: 4 / 3,
    source,
    other: otherLayout,
    slot: "cover-phone-view-home-video-img",
    requireRatio: true,
  });
  assert.equal(matched.status, "ok");
  assert.equal(matched.evidence.height, 375);
  const staleHidesOverwrite = judgeCoverIdentity({
    samples: [
      { w: 80, h: 60, grid: same.full },
      { w: 500, h: 375, grid: otherLayout.full },
    ],
    target: 4 / 3,
    source,
    other: otherLayout,
    slot: "editor_4_3",
    requireRatio: true,
  });
  assert.equal(staleHidesOverwrite.status, "identity");
  assert.equal(staleHidesOverwrite.width, 500);
});

test("visible PNG samples can crop a 16:9 viewport to the centered 4:3 picture", () => {
  const blocks = (x, y, width, height) => {
    const left = x < width / 2;
    const top = y < height / 2;
    if (left && top) return [20, 40, 90];
    if (!left && top) return [210, 170, 60];
    if (left && !top) return [40, 40, 40];
    return [120, 70, 90];
  };
  const source = pngFingerprint(paintPng(32, 24, blocks));
  const letterboxed = paintPng(48, 24, (x, y, width, height) => {
    const side = (48 - 32) / 2;
    if (x < side || x >= 48 - side) return [160, 160, 160];
    return blocks(x - side, y, 32, 24);
  });
  const cropped = coverSampleFromPng(letterboxed, { centerRatio: 4 / 3 });
  assert.ok(cropped);
  assert.equal(cropped.w, 32);
  assert.equal(cropped.h, 24);
  const matched = judgeCoverIdentity({
    samples: [cropped],
    target: 4 / 3,
    source,
    slot: "editor_4_3",
  });
  assert.equal(matched.status, "ok");
  const uncropped = coverSampleFromPng(letterboxed);
  const wide = judgeCoverIdentity({
    samples: [uncropped],
    target: 4 / 3,
    source,
    slot: "editor_4_3",
  });
  assert.equal(wide.status, "identity");
});

test("coverSampleFromPng can crop a rect out of a larger PNG", () => {
  const blocks = (x, y, width, height) => {
    const left = x < width / 2;
    const top = y < height / 2;
    if (left && top) return [20, 40, 90];
    if (!left && top) return [210, 170, 60];
    if (left && !top) return [40, 40, 40];
    return [120, 70, 90];
  };
  const source = pngFingerprint(paintPng(32, 24, blocks));
  const padded = paintPng(80, 48, (x, y) => {
    const ox = 12;
    const oy = 8;
    if (x >= ox && x < ox + 32 && y >= oy && y < oy + 24) return blocks(x - ox, y - oy, 32, 24);
    return [160, 160, 160];
  });
  const sample = coverSampleFromPng(padded, { rect: { x: 12, y: 8, width: 32, height: 24 } });
  assert.ok(sample);
  assert.equal(sample.w, 32);
  assert.equal(sample.h, 24);
  const matched = judgeCoverIdentity({
    samples: [sample],
    target: 4 / 3,
    source,
    slot: "editor_4_3",
  });
  assert.equal(matched.status, "ok");
});

test("same-art 4:3 and 16:9 letterboxes pass when this slot is the better match", () => {
  const cream = [247, 241, 227];
  const blocks = (x, y, width, height) => {
    const left = x < width / 2;
    const top = y < height / 2;
    if (left && top) return [20, 40, 90];
    if (!left && top) return [210, 170, 60];
    if (left && !top) return [40, 40, 40];
    return [120, 70, 90];
  };
  const letterbox = (canvasW, canvasH, artW, artH) => {
    const ox = Math.round((canvasW - artW) / 2);
    const oy = Math.round((canvasH - artH) / 2);
    return paintPng(canvasW, canvasH, (x, y) => {
      if (x >= ox && x < ox + artW && y >= oy && y < oy + artH) return blocks(x - ox, y - oy, artW, artH);
      return cream;
    });
  };
  const png43 = letterbox(80, 60, 45, 60);
  const png169 = letterbox(106, 60, 45, 60);
  const source43 = pngFingerprint(png43);
  const source169 = pngFingerprint(png169);
  assert.ok(bestFingerprintScore(source43.full, source169) >= COVER_MATCH_MIN);
  const matched = judgeCoverIdentity({
    samples: [{ w: 80, h: 60, grid: source43.full }],
    target: 4 / 3,
    source: source43,
    other: source169,
    slot: "editor_4_3",
  });
  assert.equal(matched.status, "ok");
  const wrongSlot = judgeCoverIdentity({
    samples: [{ w: 106, h: 60, grid: source169.full }],
    target: 4 / 3,
    source: source43,
    other: source169,
    slot: "editor_4_3",
  });
  assert.equal(wrongSlot.status, "identity");
});

function crc32(buf) {
  let crc = 0xffffffff;
  for (const byte of buf) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) crc = (crc >>> 1) ^ (crc & 1 ? 0xedb88320 : 0);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

test("cover slots keep their own measurements and a BV id is read from text", () => {
  assert.deepEqual(coverSlotEvidence({ slot: "cover-phone-view-home-video-img", width: 1280, height: 960, target: 4 / 3 }).height, 960);
  assert.equal(coverSlotEvidence({ slot: "cover-phone-view-space-video-img", width: 1280, height: 960, target: 16 / 9 }), null);
  assert.equal(manuscriptFromText("稿件投递成功").identity, "unconfirmed");
  assert.equal(manuscriptFromText("https://www.bilibili.com/video/BV1uVW46QEZn/").bvid, "BV1uVW46QEZn");
});

test("archives search URLs and exact title lookup recover a BV", () => {
  const urls = archivesSearchUrls("同一个模型，两个名字");
  assert.match(urls.keyword, /status=is_pubing%2Cpubed%2Cnot_pubed/);
  assert.match(urls.keyword, /keyword=%E5%90%8C%E4%B8%80%E4%B8%AA%E6%A8%A1%E5%9E%8B%EF%BC%8C%E4%B8%A4%E4%B8%AA%E5%90%8D%E5%AD%97/);
  assert.match(urls.pubing, /status=is_pubing/);
  assert.doesNotMatch(urls.pubing, /keyword=/);
  assert.match(urls.all, /status=is_pubing%2Cpubed%2Cnot_pubed/);

  const title = "同一个模型，两个名字";
  const hit = manuscriptFromArchives({
    data: {
      archives: [{ title: "其它稿件", bvid: "BV1aaaaaaaa1" }],
      arc_audits: [{ Archive: { title, bvid: "BV1ihWu6jEx5" } }],
    },
  }, title);
  assert.equal(hit.bvid, "BV1ihWu6jEx5");
  assert.equal(hit.url, "https://www.bilibili.com/video/BV1ihWu6jEx5/");
  assert.equal(hit.identity, "bvid");

  const wrapped = manuscriptFromArchives({
    json: { data: { archives: [{ title, bvid: "BV1ihWu6jEx5" }] } },
  }, title);
  assert.equal(wrapped.bvid, "BV1ihWu6jEx5");

  assert.equal(manuscriptFromArchives({ data: { archives: [{ title, bvid: "" }] } }, title).identity, "unconfirmed");
  assert.equal(manuscriptFromArchives({ data: { archives: [{ title: "同一个模型", bvid: "BV1ihWu6jEx5" }] } }, title).identity, "unconfirmed");
  assert.equal(manuscriptFromArchives(null, title).identity, "unconfirmed");

  const picked = pickManuscriptFromArchivePayloads([
    { data: { archives: [{ title: "其它稿件", bvid: "BV1aaaaaaaa1" }] } },
    { data: { archives: [{ title, bvid: "BV1ihWu6jEx5" }] } },
  ], title);
  assert.equal(picked.bvid, "BV1ihWu6jEx5");
  assert.equal(pickManuscriptFromArchivePayloads([], title).identity, "unconfirmed");
});

test("resolveEgoExit maps login_required JSON to 2", () => {
  const line = JSON.stringify(loginRequiredBody({ spaceId: 1 }));
  assert.equal(resolveEgoExit({ stdout: `${line}\n`, stderr: "", code: 0 }), 2);
  assert.equal(resolveEgoExit({ stdout: "", stderr: "boom", code: 1 }), 1);
  assert.equal(resolveEgoExit({ stdout: "", stderr: "", code: 0 }), 0);
});
