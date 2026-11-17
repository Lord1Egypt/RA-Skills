import { existsSync, statSync } from "node:fs";
import {
  PUBLISH_FAIL_SHOT,
  STUDIO_URL,
  audienceSelector,
  flowErrorBody,
  loginRequiredBody,
  metadataWriteOk,
  needsRepaint,
  classifyLogin,
  detectSignals,
  publishSuccessBody,
  uploadLimitHit,
  uploadSignals,
  validatePublishInput,
  verifyPublished,
  visibilitySelector,
  extractVideoId,
} from "./pure.mjs";
import { studioAct } from "./studio-dom.mjs";

async function clickSelector(page, selector, label) {
  try {
    await page.click(selector, { label });
    return { ok: true, via: "click", selector };
  } catch (error) {
    const viaEval = await page.evaluate(studioAct, { op: "click", selector });
    if (viaEval && viaEval.ok) return { ok: true, via: "evaluate", selector };
    return {
      ok: false,
      error: (viaEval && viaEval.error) || String(error.message || error),
      selector,
    };
  }
}

async function chooseFile(page, attempts, file) {
  let lastError = "未打开文件选择器";
  for (const attempt of attempts) {
    try {
      const chooserPromise = page.waitForFileChooser({ timeout: 20000 });
      await page.click(attempt.selector, { label: attempt.label });
      const chooser = await chooserPromise;
      const picked = await chooser.setFiles(file);
      if (picked && picked.dialog) await page.acceptDialog();
      return { ok: true, via: attempt.selector };
    } catch (error) {
      lastError = String(error.message || error);
    }
  }
  return { ok: false, error: lastError };
}

async function openUploadDialog(page) {
  let entry = await page.evaluate(studioAct, { op: "upload-entry" });
  if (entry.hasSelectFiles) return { ok: true };
  if (!entry.hasCreate && !entry.hasUploadItem) {
    return { ok: false, error: "已登录但未找到创建或上传按钮" };
  }
  if (entry.hasCreate && !entry.hasUploadItem) {
    const created = await clickSelector(page, "#create-icon", "Create");
    if (!created.ok) return created;
    await page.waitForTimeout(800);
    entry = await page.evaluate(studioAct, { op: "upload-entry" });
  }
  if (!entry.hasSelectFiles) {
    const menu = await page.evaluate(studioAct, { op: "click-upload-menu" });
    if (!menu.ok) {
      const trusted = await clickSelector(
        page,
        'tp-yt-paper-item[test-id="upload-beta"]',
        "Upload videos",
      );
      if (!trusted.ok) return { ok: false, error: menu.error || trusted.error };
    }
    await page.waitForTimeout(800);
    entry = await page.evaluate(studioAct, { op: "upload-entry" });
  }
  if (!entry.hasSelectFiles) return { ok: false, error: "未找到选择文件按钮" };
  return { ok: true };
}

async function waitForUploadStart(page) {
  for (let i = 0; i < 60; i++) {
    const surface = await page.evaluate(studioAct, { op: "surface" });
    const blob = `${surface.error || ""}\n${surface.text || ""}`;
    if (uploadLimitHit(blob)) return { ok: false, error: surface.error || "已达到上传上限" };
    const signals = uploadSignals(surface.text);
    const videoId = extractVideoId(`${surface.href || ""}\n${surface.url || ""}\n${surface.text || ""}`);
    if (signals.started || videoId) return { ok: true, videoId, status: signals.status || null };
    await page.waitForTimeout(1000);
  }
  return { ok: false, error: "上传未开始：没有看到进度或视频链接" };
}

async function advanceToVisibility(page) {
  for (let i = 0; i < 4; i++) {
    const wizard = await page.evaluate(studioAct, { op: "wizard" });
    if (wizard.hasVisibility) return { ok: true, steps: i };
    if (!wizard.hasNext) return { ok: false, error: "未找到下一步按钮" };
    if (!wizard.nextEnabled) {
      await page.waitForTimeout(500);
      continue;
    }
    const clicked = await clickSelector(page, "#next-button", "Next");
    if (!clicked.ok) return { ok: false, error: clicked.error || "下一步按钮点击失败" };
    await page.waitForTimeout(400);
  }
  return { ok: false, error: "未能进入公开范围步骤" };
}

async function uploadThumbnail(page, file) {
  return chooseFile(page, [
    { selector: "#file-loader", label: "Upload thumbnail" },
    { selector: "loc=role:button[name='Upload thumbnail']", label: "Upload thumbnail" },
    { selector: "loc=role:button[name='上传缩略图']", label: "上传缩略图" },
  ], file);
}

export async function executePublish(cfg, deps = {}) {
  const log = deps.log || ((line) => console.log(line));
  const error = deps.error || ((line) => console.error(line));
  const exists = deps.existsSync || existsSync;
  const stat = deps.statSync || statSync;
  let task = null;
  let spaceId;
  let exitCode = 1;

  const reportFail = (msg, extra = {}) => {
    error(JSON.stringify(flowErrorBody(msg, { spaceId, ...extra })));
    return 1;
  };

  try {
    exitCode = await run();
  } catch (err) {
    let shot = PUBLISH_FAIL_SHOT;
    try {
      if (task) {
        const page = task.page("p1");
        const saved = await page.screenshot({ path: PUBLISH_FAIL_SHOT });
        if (saved) shot = saved;
      }
    } catch {
      // Keep the planned screenshot path in the error.
    }
    exitCode = reportFail(`${err.message || err}。截图: ${shot}`);
  } finally {
    if (task && !(cfg && cfg.keep)) {
      try {
        await task.finish({ keep: [] });
      } catch (finishError) {
        error(JSON.stringify({ finish_error: String(finishError.message || finishError) }));
      }
    }
  }
  return exitCode;

  async function run() {
    if (!cfg) {
      return reportFail("配置文件不存在: /tmp/youtube-video-publish.json。请通过 publish.sh 调用,不要直接跑 publish.js");
    }

    const video = cfg.video || "";
    const videoExists = Boolean(video) && exists(video);
    const thumbnail = cfg.thumbnail || "";
    const thumbExists = !thumbnail || exists(thumbnail);
    const checked = validatePublishInput({
      video,
      title: cfg.title,
      description: cfg.description || "",
      tags: cfg.tags || [],
      visibility: cfg.visibility || "private",
      thumbnail,
      madeForKids: Boolean(cfg.madeForKids),
      exists: videoExists,
      thumbExists,
      sizeBytes: videoExists ? stat(video).size : 0,
    });
    if (!checked.ok) return reportFail(checked.error);

    if (typeof deps.taskSpace !== "function") {
      return reportFail("publish.js must run inside ego-browser. Use scripts/publish.sh.");
    }

    task = cfg.spaceId ? await deps.taskSpace(cfg.spaceId) : await deps.taskSpace("publish video to youtube");
    spaceId = task.spaceId;
    const page = task.page("p1");
    error(JSON.stringify({
      spaceId,
      video,
      sizeMB: checked.sizeMB,
      visibility: checked.visibility,
      madeForKids: checked.madeForKids,
    }));

    await page.goto(STUDIO_URL);
    await page.waitForLoadState();
    await page.waitForTimeout(2500);

    let raw = await page.evaluate(studioAct, { op: "probe" });
    let detected = { ...raw, ...detectSignals(raw) };
    if (needsRepaint(detected)) {
      await page.goto(STUDIO_URL);
      await page.waitForLoadState();
      raw = await page.evaluate(studioAct, { op: "probe" });
      detected = { ...raw, ...detectSignals(raw) };
    }
    const classified = classifyLogin({
      url: detected.url,
      title: detected.title,
      text: detected.text,
      cookie: detected.cookie,
      signals: detected,
    });
    if (!classified.logged_in) {
      log(JSON.stringify(loginRequiredBody({ spaceId })));
      if (cfg.keep) {
        try { await task.handOff(); } catch { /* exit 2 is what agents must honor */ }
      }
      return 2;
    }

    const opened = await openUploadDialog(page);
    if (!opened.ok) return reportFail(opened.error);

    const videoFile = await chooseFile(page, [
      { selector: "#select-files-button", label: "Select files" },
    ], video);
    if (!videoFile.ok) return reportFail(videoFile.error || "视频文件选择器没有打开");

    const started = await waitForUploadStart(page);
    if (!started.ok) return reportFail(started.error);

    const filled = await page.evaluate(studioAct, {
      op: "fill",
      title: cfg.title,
      description: cfg.description || "",
    });
    if (!metadataWriteOk(filled, { title: cfg.title, description: cfg.description || "" })) {
      return reportFail(`标题或简介写入异常: ${filled.error || filled.title || ""}`.trim());
    }

    if (thumbnail) {
      const thumb = await uploadThumbnail(page, thumbnail);
      if (!thumb.ok) return reportFail(thumb.error || "缩略图上传失败");
    }

    if (checked.tags.length) {
      const tagged = await page.evaluate(studioAct, { op: "tags", tags: checked.tags });
      if (!tagged.ok) return reportFail(tagged.error || "未能写入标签");
    }

    const audience = await page.evaluate(studioAct, {
      op: "audience",
      madeForKids: checked.madeForKids,
    });
    if (!audience.ok) {
      const fallback = await clickSelector(page, audienceSelector(checked.madeForKids), "Made for kids");
      if (!fallback.ok) return reportFail(audience.error || fallback.error || "未能选择观众设置");
    }

    const advanced = await advanceToVisibility(page);
    if (!advanced.ok) return reportFail(advanced.error);

    const visibility = checked.visibility;
    const selected = await page.evaluate(studioAct, { op: "visibility", visibility });
    if (!selected.ok) {
      const fallback = await clickSelector(page, visibilitySelector(visibility), visibility);
      if (!fallback.ok) return reportFail(selected.error || fallback.error || "未能选择公开范围");
    }

    const wizard = await page.evaluate(studioAct, { op: "wizard" });
    if (!wizard.doneEnabled && !wizard.hasDone) {
      return reportFail("未找到发布/保存按钮");
    }
    const before = await page.evaluate(studioAct, { op: "surface" });
    const done = await clickSelector(page, "#done-button", visibility === "public" ? "Publish" : "Save");
    if (!done.ok) return reportFail(done.error || "未能点击发布/保存");
    await page.waitForTimeout(2000);
    const after = await page.evaluate(studioAct, { op: "surface" });
    const limitBlob = `${before.error || ""}\n${after.error || ""}\n${after.text || ""}`;
    if (uploadLimitHit(limitBlob)) return reportFail(after.error || before.error || "已达到上传上限");

    const published = verifyPublished({
      text: `${before.text || ""}\n${after.text || ""}`,
      href: `${before.href || ""}\n${after.href || ""}`,
      pageUrl: after.url || before.url || "",
    });
    if (!published.ok) {
      let shot = PUBLISH_FAIL_SHOT;
      try {
        const saved = await page.screenshot({ path: PUBLISH_FAIL_SHOT });
        if (saved) shot = saved;
      } catch {
        // Keep the planned path.
      }
      return reportFail(`发布后未确认到视频链接或处理状态(url=${after.url || ""}). 截图: ${shot}`);
    }

    log(JSON.stringify(publishSuccessBody({
      ...published,
      title: cfg.title,
      description: cfg.description || "",
      visibility,
      madeForKids: checked.madeForKids,
      tags: checked.tags,
      spaceId,
    })));
    return 0;
  }
}
