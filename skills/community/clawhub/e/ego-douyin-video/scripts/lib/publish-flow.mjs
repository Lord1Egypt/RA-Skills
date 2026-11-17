import { existsSync, statSync } from "node:fs";
import { douyinAct } from "./douyin-dom.mjs";
import {
  PUBLISH_FAIL_SHOT,
  UPLOAD_URL,
  classifyLogin,
  descWriteOk,
  flowErrorBody,
  isPublishFormUrl,
  isUserControlInterrupt,
  loginRequiredBody,
  publishSuccessBody,
  resumeAfterInterrupt,
  titleWriteOk,
  validatePublishInput,
  verifyPublished,
} from "./pure.mjs";

async function readHref(page) {
  const probed = await page.evaluate(douyinAct, { op: "href" });
  if (typeof probed === "string") return probed;
  return String((probed && (probed.href || probed.url)) || "");
}

export async function executePublish(cfg, deps = {}) {
  const log = deps.log || ((line) => console.log(line));
  const error = deps.error || ((line) => console.error(line));
  const exists = deps.existsSync || existsSync;
  const stat = deps.statSync || statSync;
  let task = null;
  let spaceId;
  let leaveOpen = false;

  const reportFail = (msg, extra = {}) => {
    error(JSON.stringify(flowErrorBody(msg, { spaceId, ...extra })));
    return 1;
  };

  try {
    return await run();
  } catch (err) {
    if (isUserControlInterrupt(err)) {
      leaveOpen = true;
      return reportFail(resumeAfterInterrupt(spaceId), { resume: true });
    }
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
    return reportFail(`${err.message || err}。截图: ${shot}`);
  } finally {
    if (task && !(cfg && cfg.keep) && !leaveOpen) {
      try {
        await task.finish({ keep: [] });
      } catch (finishError) {
        error(JSON.stringify({ finish_error: String(finishError.message || finishError) }));
      }
    }
  }

  async function run() {
    if (!cfg) {
      return reportFail("配置文件不存在: /tmp/douyin-video-publish.json。请通过 publish.sh 调用,不要直接跑 publish.js");
    }

    const video = cfg.video || "";
    const title = cfg.title || "";
    const desc = cfg.desc || "";
    const videoExists = Boolean(video) && exists(video);
    const checked = validatePublishInput({
      video,
      title,
      desc,
      exists: videoExists,
      sizeBytes: videoExists ? stat(video).size : 0,
    });
    if (!checked.ok) return reportFail(checked.error);

    if (typeof deps.taskSpace !== "function") {
      return reportFail("publish.js must run inside ego-browser. Use scripts/publish.sh.");
    }

    task = cfg.spaceId ? await deps.taskSpace(cfg.spaceId) : await deps.taskSpace("publish video to douyin");
    spaceId = task.spaceId;
    const page = task.page("p1");
    error(JSON.stringify({ spaceId, video, sizeMB: checked.sizeMB, titleLength: checked.titleLength }));

    let href = "";
    try {
      href = await readHref(page);
    } catch {
      href = "";
    }
    const onForm = isPublishFormUrl(href);
    if (!onForm) {
      await page.goto(UPLOAD_URL);
      await page.waitForLoadState();
      await page.waitForTimeout(3000);
      const probe = await page.evaluate(douyinAct, { op: "probe" });
      const classified = classifyLogin({
        url: probe.url,
        title: probe.title,
        text: probe.text,
      });
      if (!classified.logged_in) {
        log(JSON.stringify(loginRequiredBody({ spaceId })));
        leaveOpen = true;
        try {
          await task.handOff();
        } catch {
          // Exit 2 is what agents must honor. The space stays for a QR scan.
        }
        return 2;
      }

      const upload = await page.evaluate(douyinAct, { op: "upload-point" });
      if (!upload || !upload.ok) {
        return reportFail(upload && upload.error ? upload.error : "未找到「上传视频」按钮,页面结构可能已变化");
      }
      const chooserPromise = page.waitForFileChooser({ timeout: 20000 });
      await page.mouse.click(upload.x, upload.y, { label: "点击上传视频" });
      const chooser = await chooserPromise;
      const picked = await chooser.setFiles(video);
      if (picked && picked.dialog) await page.acceptDialog();
      error("文件已交给浏览器,等待表单出现…");
    } else {
      error("检测到已在发布表单(续跑),跳过上传");
    }

    if (typeof page.waitForURL === "function") {
      await page.waitForURL(/content\/post\/video/, undefined, { timeout: 60000 }).catch(() => {});
    }
    await page.waitForFunction(
      () => /作品描述|添加作品简介/.test((document.body && document.body.innerText) || ""),
      undefined,
      { timeout: 60000 },
    );
    await page.waitForTimeout(2000);

    const titleResult = await page.evaluate(douyinAct, { op: "fill-title", title });
    if (!titleWriteOk(titleResult, title)) {
      return reportFail(`标题写入异常: 期望「${title}」实际「${titleResult && titleResult.value != null ? titleResult.value : titleResult && titleResult.error}」`);
    }

    const descResult = await page.evaluate(douyinAct, { op: "fill-desc", desc });
    if (!descWriteOk(descResult, desc)) {
      return reportFail("简介写入异常(回读不一致)");
    }

    const publish = await page.evaluate(douyinAct, { op: "publish-point" });
    if (!publish || !publish.ok) return reportFail("未找到「发布」按钮");
    await page.waitForTimeout(500);
    const receipt = await page.mouse.click(publish.x, publish.y, { label: "点击发布" });
    if (receipt && receipt.dialog) await page.acceptDialog();

    let verified = { ok: false, url: "" };
    for (let i = 0; i < 20; i++) {
      await page.waitForTimeout(3000);
      const surface = await page.evaluate(douyinAct, { op: "success" });
      verified = verifyPublished({
        url: surface && surface.url,
        text: surface && surface.text,
      });
      if (verified.ok) break;
    }

    if (verified.ok) {
      log(JSON.stringify(publishSuccessBody({ title, spaceId })));
      return 0;
    }

    let shot = PUBLISH_FAIL_SHOT;
    try {
      const saved = await page.screenshot({ path: PUBLISH_FAIL_SHOT });
      if (saved) shot = saved;
    } catch {
      // Keep the planned path.
    }
    return reportFail(`发布后未确认成功。截图: ${shot}`);
  }
}
