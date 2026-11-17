// Comment from the Kuaishou creator backend (runs inside ego-browser).
// Arguments come from /tmp/kuaishou-video-comment.json written by comment.sh.
// The public www site does not share this login. Exit 0 ok, 1 flow error, 2 login required.

import { readConfigSync } from "./lib/config-file.mjs";
import {
  COMMENT_CONFIG_PATH,
  COMMENT_FAIL_SHOT,
  COMMENT_URL,
  classifyLogin,
  commentComposerReady,
  commentTargetOk,
  commentTypedOk,
  extractSelectedVideoTitle,
  flowErrorBody,
  loginRequiredBody,
  validateCommentInput,
  verifyCommentPosted,
} from "./lib/pure.mjs";

let spaceId;
const fail = (msg, extra = {}) => {
  console.error(JSON.stringify(flowErrorBody(msg, { spaceId, ...extra })));
  process.exit(1);
};

if (typeof taskSpace !== "function") {
  fail("comment.js must run inside ego-browser. Use scripts/comment.sh.");
}

let cfg = null;
try {
  cfg = readConfigSync(COMMENT_CONFIG_PATH);
} catch {
  cfg = null;
}
if (!cfg) {
  fail(`配置文件不存在: ${COMMENT_CONFIG_PATH}。请通过 comment.sh 调用,不要直接跑 comment.js`);
}

const comment = cfg.comment || "";
const titleHint = cfg.titleHint || "";
const checked = validateCommentInput({ comment });
if (!checked.ok) fail(checked.error);

const task = cfg.spaceId ? await taskSpace(cfg.spaceId) : await taskSpace("comment on kuaishou video");
spaceId = task.spaceId;
const page = task.page("p1");
console.error(JSON.stringify({ spaceId, comment }));

await page.goto(COMMENT_URL);
await page.waitForLoadState();
await page.waitForTimeout(2500);

const probe = await page.evaluate(() => ({
  text: (document.body.innerText || "").slice(0, 8000),
  url: location.href,
  title: document.title || "",
}));
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

const videoTitle = extractSelectedVideoTitle(probe.text);
const target = commentTargetOk({ videoTitle, titleHint });
if (!target.ok) fail(target.error);
if (!commentComposerReady(probe.text)) {
  fail("未找到评论输入区(占位文本「有爱评论」),页面结构可能已变化");
}

await page.click("text=有爱评论", { label: "点击评论输入框" });
await page.waitForTimeout(500);
await page.keyboard.type(comment);
await page.waitForTimeout(500);
const typed = await page.evaluate((value) => {
  const els = [...document.querySelectorAll("[contenteditable=true], textarea, input")];
  const el = els.find((node) => ((node.value || node.innerText || "")).includes(value.slice(0, 4)));
  return el ? (el.value || el.innerText).trim() : null;
}, comment);
if (!commentTypedOk(typed, comment)) fail(`评论输入异常: 期望「${comment}」实际「${typed}」`);

const receipt = await page.click('text="发送"', { label: "点击发送评论" });
if (receipt && receipt.dialog) await page.acceptDialog();
await page.waitForTimeout(2500);

const after = await page.evaluate(() => document.body.innerText || "");
const verify = verifyCommentPosted(after, comment);
if (verify.ok) {
  console.log(JSON.stringify({ ok: true, comment, spaceId }));
  if (!cfg.keep) await task.finish({ keep: [] });
} else {
  let shot = COMMENT_FAIL_SHOT;
  try {
    shot = await page.screenshot({ path: COMMENT_FAIL_SHOT });
  } catch {
    // Keep the planned path in the error.
  }
  fail(`发送后未确认成功(toast=${verify.toast})。截图: ${shot}`);
}
