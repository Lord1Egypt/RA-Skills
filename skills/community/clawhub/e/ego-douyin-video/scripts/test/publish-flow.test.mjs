import assert from "node:assert/strict";
import test from "node:test";
import { executePublish } from "../lib/publish-flow.mjs";
import { douyinAct } from "../lib/douyin-dom.mjs";
import { createDocument, element, textNode, withDocument } from "./dom-fixture.mjs";

function formParts(state) {
  const input = element("input", { placeholder: "填写作品标题，为作品获得更多流量" });
  const editor = state.hideDesc
    ? null
    : element("div", { contentEditable: true, children: [textNode("")] });
  const publish = element("button", {
    hidden: state.hidePublish,
    children: [textNode("发布")],
    rect: { x: 50, y: 400, width: 80, height: 36 },
  });
  const decoy = element("button", { children: [textNode("立即发布")] });
  const children = [decoy, publish];
  if (!state.hideTitle) children.unshift(input);
  if (editor) children.unshift(editor);
  let text = "作品描述\n添加作品简介";
  let href = "https://creator.douyin.com/creator-micro/content/post/video";
  if (state.mode === "manage") {
    text = "发布成功";
    href = "https://creator.douyin.com/creator-micro/content/manage?enter_from=publish";
  } else if (state.mode === "success-text") {
    text = "发布成功";
  } else if (state.mode === "upload") {
    text = "点击上传 上传视频";
    href = "https://creator.douyin.com/creator-micro/content/upload";
  } else if (state.mode === "login") {
    text = "扫码登录";
    href = "https://creator.douyin.com/creator-micro/content/upload";
  }
  const upload = element("button", {
    hidden: state.hideUpload,
    children: [textNode("上传"), textNode("\n"), textNode("视频")],
    rect: { x: 10, y: 30, width: 100, height: 40 },
  });
  const bodyChildren = state.mode === "upload" || state.mode === "login"
    ? (state.mode === "upload" ? [upload] : [])
    : children;
  return {
    body: element("div", { innerText: text, children: bodyChildren }),
    editor,
    href,
  };
}

function harness(options = {}) {
  const state = {
    mode: options.mode || "upload",
    files: [],
    dialogs: 0,
    clicks: [],
    gotos: 0,
    shots: 0,
    hideUpload: Boolean(options.hideUpload),
    hidePublish: Boolean(options.hidePublish),
    hideTitle: Boolean(options.hideTitle),
    hideDesc: Boolean(options.hideDesc),
    badTitle: Boolean(options.badTitle),
    badDesc: Boolean(options.badDesc),
  };
  const stdout = [];
  const stderr = [];
  const taskCalls = { finish: 0, handOff: 0, keep: null };
  const page = {
    async goto() {
      state.gotos += 1;
      if (options.gotoError) throw new Error(options.gotoError);
      if (state.mode !== "login") state.mode = "upload";
    },
    async waitForLoadState() {},
    async waitForTimeout() {},
    async waitForURL() {
      if (options.urlReject) throw new Error("url wait failed");
    },
    async waitForFunction(fn) {
      if (options.formTimeout) throw new Error("form timeout");
      const parts = formParts(state);
      const built = createDocument(parts.body, { href: parts.href });
      const ready = withDocument(built, () => fn());
      if (!ready) throw new Error("form not ready");
    },
    async evaluate(fn, arg) {
      if (options.hrefError && arg && arg.op === "href") throw new Error(options.hrefError);
      const parts = formParts(state);
      const built = createDocument(parts.body, { href: parts.href });
      if (state.badTitle) built.doc._badTitle = true;
      if (state.badDesc) built.doc._badDesc = true;
      if (parts.editor) {
        parts.editor.focus = () => {
          built.doc._activeEditor = parts.editor;
        };
      }
      return withDocument(built, () => (arg ? fn(arg) : fn()));
    },
    waitForFileChooser() {
      return {
        then(resolve, reject) {
          if (options.chooserError) {
            reject(new Error(options.chooserError));
            return;
          }
          resolve({
            async setFiles(file) {
              state.files.push(file);
              state.mode = "form";
              return options.dialog ? { dialog: true } : {};
            },
          });
        },
      };
    },
    async acceptDialog() {
      state.dialogs += 1;
    },
    mouse: {
      async click(x, y, opts) {
        state.clicks.push({ x, y, label: opts && opts.label });
        if (options.clickThrows) throw new Error(options.clickThrows);
        if (opts && opts.label === "点击发布" && !options.noSuccess) {
          state.mode = options.textOnly ? "success-text" : "manage";
        }
        return options.publishDialog && opts && opts.label === "点击发布" ? { dialog: true } : {};
      },
    },
    async screenshot() {
      state.shots += 1;
      if (options.shotError) throw new Error(options.shotError);
      return "/tmp/douyin-video-publish-failed.png";
    },
  };
  if (options.omitWaitUrl) delete page.waitForURL;
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
      if (options.taskError) throw new Error(options.taskError);
      return task;
    },
  };
  return { state, stdout, stderr, taskCalls, names, deps, page };
}

function cfg(extra = {}) {
  return {
    video: "/absolute/path/to/video.mp4",
    title: "三十字内标题",
    desc: "简介 #话题",
    spaceId: null,
    keep: false,
    ...extra,
  };
}

test("a public upload fills the title and description, then closes the space", async () => {
  const h = harness({ dialog: true, publishDialog: true });
  const code = await executePublish(cfg(), h.deps);
  assert.equal(code, 0);
  const body = JSON.parse(h.stdout.at(-1));
  assert.equal(body.ok, true);
  assert.equal(body.title, "三十字内标题");
  assert.equal(body.manageUrl, "https://creator.douyin.com/creator-micro/content/manage");
  assert.equal(body.spaceId, 7);
  assert.equal(h.taskCalls.finish, 1);
  assert.deepEqual(h.taskCalls.keep, []);
  assert.equal(h.taskCalls.handOff, 0);
  assert.equal(h.names[0], "publish video to douyin");
  assert.deepEqual(h.state.files, ["/absolute/path/to/video.mp4"]);
  assert.equal(h.state.dialogs, 2);
  assert.equal(h.state.clicks[0].label, "点击上传视频");
  assert.equal(h.state.clicks[1].label, "点击发布");
  assert.match(h.stderr.join("\n"), /文件已交给浏览器/);
});

test("success text without a manage URL still counts, and --keep leaves the space open", async () => {
  const h = harness({ textOnly: true, spaceId: 4, omitWaitUrl: true });
  const code = await executePublish(cfg({ spaceId: 4, keep: true }), h.deps);
  assert.equal(code, 0);
  assert.equal(h.names[0], 4);
  assert.equal(h.taskCalls.finish, 0);
  assert.match(h.stdout.at(-1), /"ok":true/);
});

test("an existing publish form skips the upload", async () => {
  const h = harness({ mode: "form", spaceId: 6 });
  const code = await executePublish(cfg({ spaceId: 6 }), h.deps);
  assert.equal(code, 0);
  assert.equal(h.state.files.length, 0);
  assert.equal(h.state.gotos, 0);
  assert.equal(h.state.clicks.length, 1);
  assert.match(h.stderr.join("\n"), /跳过上传/);
});

test("login required hands the page over and does not close the space", async () => {
  const h = harness({ mode: "login", handOffError: "busy" });
  const code = await executePublish(cfg(), h.deps);
  assert.equal(code, 2);
  assert.equal(h.taskCalls.handOff, 1);
  assert.equal(h.taskCalls.finish, 0);
  const body = JSON.parse(h.stdout.at(-1));
  assert.equal(body.login_required, true);
  assert.equal(body.exitCode, 2);
  assert.match(body.login_tip, /works better/);
});

test("a location-permission interrupt stays resumable", async () => {
  const h = harness({ clickThrows: "ego user-control: geolocation permission", spaceId: 9 });
  const code = await executePublish(cfg({ spaceId: 9 }), h.deps);
  assert.equal(code, 1);
  assert.equal(h.taskCalls.finish, 0);
  assert.match(h.stderr.join("\n"), /spaceId 9/);
  assert.match(h.stderr.join("\n"), /位置权限/);
  assert.match(h.stderr.join("\n"), /"resume":true/);
});

test("a file-chooser permission error also stays resumable", async () => {
  const h = harness({ chooserError: "NotAllowedError: permission" });
  const code = await executePublish(cfg(), h.deps);
  assert.equal(code, 1);
  assert.equal(h.taskCalls.finish, 0);
  assert.match(h.stderr.join("\n"), /resume/);
});

test("input and browser failures exit 1 and close the space", async () => {
  const missingCfg = harness();
  assert.equal(await executePublish(null, missingCfg.deps), 1);
  assert.match(missingCfg.stderr.join("\n"), /配置文件不存在/);
  assert.equal(missingCfg.taskCalls.finish, 0);

  const missingFile = harness({ existsSync: () => false });
  assert.equal(await executePublish(cfg(), missingFile.deps), 1);
  assert.match(missingFile.stderr.join("\n"), /视频文件不存在/);

  const longTitle = harness();
  assert.equal(await executePublish(cfg({ title: "字".repeat(31) }), longTitle.deps), 1);
  assert.match(longTitle.stderr.join("\n"), /超过30字/);

  const outside = harness({ taskSpace: null });
  assert.equal(await executePublish(cfg(), outside.deps), 1);
  assert.match(outside.stderr.join("\n"), /publish\.sh/);

  const noButton = harness({ hideUpload: true });
  assert.equal(await executePublish(cfg(), noButton.deps), 1);
  assert.match(noButton.stderr.join("\n"), /上传视频/);
  assert.equal(noButton.taskCalls.finish, 1);
  assert.deepEqual(noButton.taskCalls.keep, []);

  const badTitle = harness({ badTitle: true, urlReject: true });
  assert.equal(await executePublish(cfg(), badTitle.deps), 1);
  assert.match(badTitle.stderr.join("\n"), /标题写入异常/);

  const badDesc = harness({ badDesc: true });
  assert.equal(await executePublish(cfg(), badDesc.deps), 1);
  assert.match(badDesc.stderr.join("\n"), /简介写入异常/);

  const noPublish = harness({ hidePublish: true });
  assert.equal(await executePublish(cfg(), noPublish.deps), 1);
  assert.match(noPublish.stderr.join("\n"), /未找到「发布」按钮/);

  const noTitleBox = harness({ hideTitle: true });
  assert.equal(await executePublish(cfg(), noTitleBox.deps), 1);
  assert.match(noTitleBox.stderr.join("\n"), /标题写入异常/);
});

test("a publish that never confirms success records a screenshot and closes", async () => {
  const h = harness({ noSuccess: true });
  const code = await executePublish(cfg(), h.deps);
  assert.equal(code, 1);
  assert.equal(h.state.shots, 1);
  assert.match(h.stderr.join("\n"), /发布后未确认成功/);
  assert.equal(h.taskCalls.finish, 1);

  const blind = harness({ noSuccess: true, shotError: "shot failed" });
  assert.equal(await executePublish(cfg(), blind.deps), 1);
  assert.match(blind.stderr.join("\n"), /douyin-video-publish-failed\.png/);
});

test("a thrown navigation still finishes, and a href probe error continues", async () => {
  const crashed = harness({ gotoError: "navigation failed", shotError: "no shot" });
  assert.equal(await executePublish(cfg(), crashed.deps), 1);
  assert.match(crashed.stderr.join("\n"), /navigation failed/);
  assert.equal(crashed.taskCalls.finish, 1);

  const href = harness({ hrefError: "href unread" });
  assert.equal(await executePublish(cfg(), href.deps), 0);

  const deadPage = harness({ pageError: "page dead" });
  assert.equal(await executePublish(cfg(), deadPage.deps), 1);
  assert.match(deadPage.stderr.join("\n"), /page dead/);
  assert.equal(deadPage.taskCalls.finish, 1);

  const finish = harness({ finishError: "space already closed" });
  assert.equal(await executePublish(cfg(), finish.deps), 0);
  assert.match(finish.stderr.join("\n"), /finish_error/);

  const opened = harness({ taskError: "task space down" });
  assert.equal(await executePublish(cfg(), opened.deps), 1);
  assert.match(opened.stderr.join("\n"), /task space down/);
  assert.equal(opened.taskCalls.finish, 0);

  const form = harness({ formTimeout: "form timeout" });
  assert.equal(await executePublish(cfg(), form.deps), 1);
  assert.match(form.stderr.join("\n"), /form timeout/);
});

test("douyinAct is the function the flow evaluates", () => {
  assert.equal(typeof douyinAct, "function");
});
