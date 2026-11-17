// Publish one local video on https://cp.kuaishou.com (runs inside ego-browser).
// Arguments come from /tmp/kuaishou-video-publish.json written by publish.sh.
// Exit 0: work is 审核中. Exit 1: flow error. Exit 2: login required (handOff done).

import { existsSync, statSync } from "node:fs";
import { readConfigSync } from "./lib/config-file.mjs";
import {
  PUBLISH_CONFIG_PATH,
  PUBLISH_FAIL_SHOT,
  PUBLISH_URL,
  classifyLogin,
  descWriteOk,
  flowErrorBody,
  loginRequiredBody,
  publishClickPoint,
  publishSuccessBody,
  uploadSignals,
  validatePublishInput,
  verifyPublished,
} from "./lib/pure.mjs";

let spaceId;
const fail = (msg, extra = {}) => {
  console.error(JSON.stringify(flowErrorBody(msg, { spaceId, ...extra })));
  process.exit(1);
};

if (typeof taskSpace !== "function") {
  fail("publish.js must run inside ego-browser. Use scripts/publish.sh.");
}

let cfg = null;
try {
  cfg = readConfigSync(PUBLISH_CONFIG_PATH);
} catch {
  cfg = null;
}
if (!cfg) {
  fail(`配置文件不存在: ${PUBLISH_CONFIG_PATH}。请通过 publish.sh 调用,不要直接跑 publish.js`);
}

const video = cfg.video || "";
const desc = cfg.desc || "";
const exists = Boolean(video) && existsSync(video);
const checked = validatePublishInput({
  video,
  desc,
  exists,
  sizeBytes: exists ? statSync(video).size : 0,
});
if (!checked.ok) fail(checked.error);

const task = cfg.spaceId ? await taskSpace(cfg.spaceId) : await taskSpace("publish video to kuaishou");
spaceId = task.spaceId;
const page = task.page("p1");
console.error(JSON.stringify({ spaceId, video, sizeMB: checked.sizeMB }));

await page.goto(PUBLISH_URL);
await page.waitForLoadState();
await page.waitForTimeout(2500);

const probe = await page.evaluate(() => {
  const text = document.body.innerText || "";
  const hasUploadBtn = !!Array.from(document.querySelectorAll("*")).find(
    (el) => el.childElementCount === 0
      && el.textContent.trim() === "上传视频"
      && el.closest('[role="button"]'),
  );
  return { text: text.slice(0, 4000), url: location.href, title: document.title || "", hasUploadBtn };
});
const classified = classifyLogin({ url: probe.url, title: probe.title, text: probe.text });
if (!classified.logged_in) {
  console.log(JSON.stringify(loginRequiredBody({ spaceId })));
  try {
    await task.handOff();
  } catch {
    // The JSON exit code is what the wrapper returns.
  }
  process.exit(2);
}
if (!probe.hasUploadBtn) {
  fail("登录正常但未找到「上传视频」按钮,页面结构可能已变化,请人工检查");
}

const chooserPromise = page.waitForFileChooser({ timeout: 20000 });
await page.click("loc=role:button[name='上传视频']", { label: "点击上传视频" });
const chooser = await chooserPromise;
const picked = await chooser.setFiles(video);
if (picked && picked.dialog) await page.acceptDialog();
console.error("文件已交给浏览器,等待上传…");

await page.waitForFunction(
  () => (document.body.innerText || "").includes("重新上传"),
  undefined,
  { timeout: 120000 },
);
for (let i = 0; i < 60; i++) {
  await page.waitForFunction(
    () => !(document.body.innerText || "").includes("上传中"),
    undefined,
    { timeout: 60000 },
  );
  await page.waitForTimeout(2000);
  const mid = await page.evaluate(() => document.body.innerText || "");
  if (!uploadSignals(mid).uploading) break;
}
console.error("上传完成");

const descResult = await page.evaluate((value) => {
  const editors = [...document.querySelectorAll('[contenteditable="true"]')];
  const editor = editors.find((el) => !el.textContent.trim()) || editors[0];
  if (!editor) return { ok: false, error: "未找到描述编辑器" };
  editor.focus();
  document.execCommand("selectAll", false, null);
  document.execCommand("insertText", false, value);
  editor.blur();
  return { ok: true, text: editor.innerText.trim() };
}, desc);
if (!descWriteOk(descResult, desc)) {
  fail(`描述写入异常: 期望「${desc}」实际「${descResult.text || descResult.error}」`);
}

const rect = await page.evaluate(() => {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  while (walker.nextNode()) {
    const el = walker.currentNode;
    const ownText = [...el.childNodes]
      .filter((node) => node.nodeType === 3)
      .map((node) => node.textContent.trim())
      .join("");
    if (ownText === "发布" && el.offsetParent !== null) {
      el.scrollIntoView({ block: "center" });
      const box = el.getBoundingClientRect();
      return { x: box.x, y: box.y, width: box.width, height: box.height };
    }
  }
  return null;
});
const btnPos = publishClickPoint(rect);
if (!btnPos) fail("未找到「发布」按钮");
await page.waitForTimeout(500);
const receipt = await page.mouse.click(btnPos.x, btnPos.y, { label: "点击发布" });
if (receipt && receipt.dialog) await page.acceptDialog();

try {
  await page.waitForURL(/article\/manage\/video/, undefined, { timeout: 60000 });
} catch {
  // verifyPublished decides.
}
await page.waitForTimeout(3000);
const verify = await page.evaluate(() => ({
  url: location.href,
  text: document.body.innerText || "",
}));
const published = verifyPublished(verify);

if (published.ok) {
  console.log(JSON.stringify(publishSuccessBody({ desc, spaceId })));
  if (!cfg.keep) await task.finish({ keep: [] });
} else {
  let shot = PUBLISH_FAIL_SHOT;
  try {
    shot = await page.screenshot({ path: PUBLISH_FAIL_SHOT });
  } catch {
    // Keep the planned path in the error.
  }
  fail(`发布后未确认到成功状态(url=${verify.url})。截图: ${shot}`);
}
