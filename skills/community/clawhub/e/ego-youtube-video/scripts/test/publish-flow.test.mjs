import assert from "node:assert/strict";
import test from "node:test";
import { executePublish } from "../lib/publish-flow.mjs";
import { createStudio } from "./dom-fixture.mjs";

function harness(initial = {}, options = {}) {
  const studio = createStudio(initial);
  const stdout = [];
  const stderr = [];
  const clicks = [];
  let gotos = 0;
  const taskCalls = { finish: 0, handOff: 0, keep: null };
  const page = {
    async goto() {
      gotos += 1;
      if (studio.state.repaint && gotos >= 2) studio.state.mode = "studio";
      if (options.gotoError) throw new Error(options.gotoError);
    },
    async waitForLoadState() {},
    async waitForTimeout() {},
    async evaluate(fn, arg) {
      const built = studio.build();
      studio.state._lastDoc = built;
      if (options.failOps && arg && options.failOps[arg.op]) {
        return { ok: false, error: options.failOps[arg.op] };
      }
      if (arg && arg.op === "click" && options.failClick) {
        return { ok: false, error: "click miss" };
      }
      const prevDoc = globalThis.document;
      const prevLoc = globalThis.location;
      globalThis.document = built.doc;
      globalThis.location = built.location;
      try {
        return await fn(arg);
      } finally {
        globalThis.document = prevDoc;
        globalThis.location = prevLoc;
      }
    },
    async click(selector, opts) {
      clicks.push({ selector, label: opts && opts.label });
      if (options.clickThrows && options.clickThrows.has(selector)) {
        throw new Error(`cannot click ${selector}`);
      }
      const doc = studio.state._lastDoc && studio.state._lastDoc.doc;
      const found = doc && typeof doc.querySelector === "function" ? doc.querySelector(selector) : null;
      if (found && found.disabled) throw new Error(`disabled ${selector}`);
      if (!found && !String(selector).startsWith("loc=")) throw new Error(`missing ${selector}`);
      if (String(selector).startsWith("loc=") && options.rejectRole) throw new Error(`missing ${selector}`);
      studio.transition(selector);
    },
    async waitForFileChooser() {
      return {
        async setFiles(file) {
          studio.state.files.push(file);
          if (options.chooserError) throw new Error(options.chooserError);
          if (studio.state.limitOnUpload) {
            studio.state.error = "daily upload limit reached";
            studio.state.bodyText = "daily upload limit reached";
            return {};
          }
          if (!studio.state.stallUpload) {
            studio.state.uploadStarted = true;
            studio.state.bodyText = "Uploading 40%";
            if (!studio.state.suppressId) studio.state.videoHref = "https://youtu.be/AaBbCcDdEe1";
          }
          return studio.state.dialog ? { dialog: true } : {};
        },
      };
    },
    async acceptDialog() {
      studio.state.dialogs += 1;
    },
    async screenshot() {
      if (options.shotError) throw new Error(options.shotError);
      return "/tmp/youtube-video-publish-failed.png";
    },
  };
  const task = {
    spaceId: options.spaceId ?? 7,
    page() {
      if (options.pageError) throw new Error(options.pageError);
      return page;
    },
    async handOff() {
      taskCalls.handOff += 1;
      if (options.handOffError) throw new Error(options.handOffError);
    },
    async finish(opts) {
      taskCalls.finish += 1;
      taskCalls.keep = opts.keep;
      if (options.finishError) throw new Error(options.finishError);
    },
  };
  const names = [];
  const deps = {
    log: (line) => stdout.push(line),
    error: (line) => stderr.push(line),
    existsSync: options.existsSync || (() => true),
    statSync: options.statSync || (() => ({ size: options.size ?? 1048576 })),
    taskSpace: options.taskSpace === null ? undefined : async (name) => {
      names.push(name);
      return task;
    },
  };
  return { studio, stdout, stderr, clicks, taskCalls, names, deps, gotos: () => gotos };
}

function cfg(extra = {}) {
  return {
    video: "/absolute/path/to/video.mp4",
    title: "A title",
    description: "A description",
    tags: [],
    visibility: "private",
    thumbnail: "",
    madeForKids: false,
    spaceId: null,
    keep: false,
    ...extra,
  };
}

function stderrText(h) {
  return h.stderr.join("\n");
}

test("a private upload reports the video id and closes the space", async () => {
  const h = harness({ dialog: true });
  const code = await executePublish(cfg({ description: "" }), h.deps);
  assert.equal(code, 0);
  const body = JSON.parse(h.stdout.at(-1));
  assert.equal(body.ok, true);
  assert.equal(body.videoId, "AaBbCcDdEe1");
  assert.equal(body.videoUrl, "https://youtu.be/AaBbCcDdEe1");
  assert.equal(body.status, "Checks complete");
  assert.equal(body.visibility, "private");
  assert.equal(body.madeForKids, false);
  assert.equal(body.description, "");
  assert.equal(body.spaceId, 7);
  assert.equal(h.taskCalls.finish, 1);
  assert.deepEqual(h.taskCalls.keep, []);
  assert.equal(h.taskCalls.handOff, 0);
  assert.equal(h.names[0], "publish video to youtube");
  assert.equal(h.studio.state.dialogs, 1);
  assert.equal(h.clicks.some((click) => click.selector === "#done-button" && click.label === "Save"), true);
  assert.match(stderrText(h), /"visibility":"private"/);
});

test("public, tags, kids, and a thumbnail fallback stay on the handed-off space", async () => {
  const h = harness({}, {
    clickThrows: new Set(["#create-icon", "#next-button", "#file-loader"]),
    failOps: { visibility: "visibility miss" },
    spaceId: 4,
  });
  const code = await executePublish(cfg({
    description: "A description",
    tags: ["one", "two"],
    visibility: "public",
    thumbnail: "/absolute/path/to/thumbnail.jpg",
    madeForKids: true,
    spaceId: 4,
    keep: true,
  }), h.deps);
  assert.equal(code, 0);
  const body = JSON.parse(h.stdout.at(-1));
  assert.equal(body.visibility, "public");
  assert.equal(body.madeForKids, true);
  assert.deepEqual(body.tags, ["one", "two"]);
  assert.equal(body.description, "A description");
  assert.equal(h.names[0], 4);
  assert.equal(h.taskCalls.finish, 0);
  assert.equal(h.clicks.some((click) => click.label === "Publish"), true);
  assert.equal(h.clicks.some((click) => String(click.selector).includes("Upload thumbnail")), true);
  assert.equal(h.studio.state.files.includes("/absolute/path/to/thumbnail.jpg"), true);
});

test("an already-open Chinese upload menu can start the file chooser", async () => {
  const h = harness({
    hasCreate: false,
    menuOpen: true,
    menuByText: true,
    menuText: "上传视频",
    stallUpload: true,
  });
  const code = await executePublish(cfg(), h.deps);
  assert.equal(code, 1);
  assert.match(stderrText(h), /上传未开始/);
  assert.equal(h.clicks.some((click) => click.selector === "#create-icon"), false);
  assert.equal(h.taskCalls.finish, 1);
});

test("login required closes the space unless --keep hands it off", async () => {
  const closed = harness({ mode: "login" });
  assert.equal(await executePublish(cfg(), closed.deps), 2);
  assert.match(closed.stdout[0], /login_required/);
  assert.match(closed.stdout[0], /how_to_login/);
  assert.equal(closed.taskCalls.handOff, 0);
  assert.equal(closed.taskCalls.finish, 1);
  assert.deepEqual(closed.taskCalls.keep, []);

  const kept = harness({ mode: "login" }, { handOffError: "user declined" });
  assert.equal(await executePublish(cfg({ keep: true }), kept.deps), 2);
  assert.equal(kept.taskCalls.handOff, 1);
  assert.equal(kept.taskCalls.finish, 0);
});

test("a blank Studio paint is reloaded once", async () => {
  const h = harness({ mode: "blank", repaint: true, hasCreate: false });
  assert.equal(await executePublish(cfg(), h.deps), 1);
  assert.match(stderrText(h), /创建或上传按钮/);
  assert.ok(h.gotos() >= 2);
});

test("input and browser failures exit 1 before or after the space opens", async () => {
  const missing = harness({}, { existsSync: () => false });
  assert.equal(await executePublish(cfg(), missing.deps), 1);
  assert.match(stderrText(missing), /视频文件不存在/);
  assert.equal(missing.taskCalls.finish, 0);

  const empty = harness({}, { statSync: () => ({ size: 0 }) });
  assert.equal(await executePublish(cfg(), empty.deps), 1);
  assert.match(stderrText(empty), /视频文件是空的/);
  assert.equal(empty.taskCalls.finish, 0);

  const thumb = harness({}, {
    existsSync: (file) => !String(file).endsWith(".jpg"),
  });
  assert.equal(await executePublish(cfg({ thumbnail: "/absolute/path/to/thumbnail.jpg" }), thumb.deps), 1);
  assert.match(stderrText(thumb), /缩略图不存在/);

  const noTask = harness({}, { taskSpace: null });
  assert.equal(await executePublish(cfg(), noTask.deps), 1);
  assert.match(stderrText(noTask), /ego-browser/);
  assert.equal(noTask.taskCalls.finish, 0);

  const absent = harness();
  assert.equal(await executePublish(null, absent.deps), 1);
  assert.match(stderrText(absent), /配置文件不存在/);
  assert.equal(absent.taskCalls.finish, 0);
});

test("upload limit, stalled progress, and a save without a video id", async () => {
  const limit = harness({ limitOnUpload: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), limit.deps);
    return limit;
  })()), /daily upload limit|上传上限/);

  const blocked = harness({ blockMenu: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), blocked.deps);
    return blocked;
  })()), /上传视频/);

  const noButton = harness({ blockSelect: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), noButton.deps);
    return noButton;
  })()), /选择文件按钮/);

  const chooser = harness({}, { clickThrows: new Set(["#select-files-button"]) });
  chooser.studio.state.hasSelect = true;
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), chooser.deps);
    return chooser;
  })()), /cannot click #select-files-button/);

  const noId = harness({ suppressId: true }, { shotError: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), noId.deps);
    return noId;
  })()), /视频链接或处理状态/);

  const lateLimit = harness({ limitOnDone: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), lateLimit.deps);
    return lateLimit;
  })()), /daily upload limit|上传上限/);
});

test("wizard and metadata failures stay on exit 1", async () => {
  const title = harness({ includeTitle: false });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), title.deps);
    return title;
  })()), /标题或简介/);

  const desc = harness({ lockDescription: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), desc.deps);
    return desc;
  })()), /标题或简介/);

  const kids = harness({}, {
    failOps: { audience: "audience miss" },
    clickThrows: new Set(['tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]']),
    failClick: true,
  });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), kids.deps);
    return kids;
  })()), /观众|面向儿童|click miss|audience/);

  const stuck = harness({ nextEnabled: false });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), stuck.deps);
    return stuck;
  })()), /公开范围步骤/);

  const noNext = harness({ hideNext: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), noNext.deps);
    return noNext;
  })()), /下一步/);

  const noDone = harness({ hideDone: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), noDone.deps);
    return noDone;
  })()), /发布\/保存/);

  const disabled = harness({ doneDisabled: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), disabled.deps);
    return disabled;
  })()), /不可点击|发布\/保存/);

  const thumbs = harness({}, {
    clickThrows: new Set(["#file-loader"]),
    rejectRole: true,
  });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg({ thumbnail: "/absolute/path/to/thumbnail.jpg" }), thumbs.deps);
    return thumbs;
  })()), /missing|缩略图|file-loader/);

  const create = harness({}, {
    clickThrows: new Set(["#create-icon"]),
    failClick: true,
  });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), create.deps);
    return create;
  })()), /click miss|创建/);
});

test("a thrown navigation still finishes and records the screenshot path", async () => {
  const crashed = harness({}, { gotoError: "navigation failed" });
  assert.equal(await executePublish(cfg(), crashed.deps), 1);
  assert.match(stderrText(crashed), /navigation failed/);
  assert.match(stderrText(crashed), /截图/);
  assert.equal(crashed.taskCalls.finish, 1);

  const dead = harness({}, { pageError: "page dead", shotError: true });
  assert.match(stderrText(await (async () => {
    await executePublish(cfg(), dead.deps);
    return dead;
  })()), /page dead/);

  const closed = harness({}, { finishError: "space already closed" });
  assert.equal(await executePublish(cfg({ description: "" }), closed.deps), 0);
  assert.match(stderrText(closed), /finish_error/);
  assert.match(stderrText(closed), /space already closed/);
});
