// Pure helpers for douyin-video. No browser, no process.exit.

export const SKILL = "douyin-video";
export const BASE = "https://creator.douyin.com";
export const UPLOAD_URL = `${BASE}/creator-micro/content/upload`;
export const FORM_PATH = "/content/post/video";
export const MANAGE_URL = `${BASE}/creator-micro/content/manage`;
export const PUBLISH_CONFIG_PATH = "/tmp/douyin-video-publish.json";
export const PUBLISH_FAIL_SHOT = "/tmp/douyin-video-publish-failed.png";
export const TITLE_LIMIT = 30;

// Body text, not the document title. The login page title can already say 抖音.
export const PLATFORM_CHROME_RE = /点击上传|上传视频|作品描述|添加作品简介|内容管理|发布成功/;
export const UPLOAD_CHROME_RE = /点击上传|上传视频/;
export const LOGIN_WALL_RE = /扫码登录|二维码登录|请登录/;
// Recorded for the login summary only. Body text decides logged_in, matching the working uploader.
export const LOGIN_COOKIE_RE = /(?:^|;\s*)(?:sessionid|sessionid_ss)=/;

export const HOW_TO_LOGIN = [
  "Install Ego Lite and put ego-browser on PATH. Open the Ego Lite app (the same profile ego-browser drives).",
  "Visit https://creator.douyin.com/creator-micro/content/upload — if the page shows 扫码登录, scan the QR with the Douyin app.",
  "Confirm the correct creator account and leave Ego logged in. Being logged into Douyin in Ego works better.",
  "Re-run this skill’s login-check. Continue to publish only after exit 0.",
  "Sessions can expire. Login-check before every publish. Never type a password or paste cookies.",
];

export const HOW_TO_LOGIN_ZH = [
  "先安装 Ego Lite，并把 ego-browser 放进 PATH。打开 Ego Lite（ego-browser 驱动的同一个配置档）。",
  "访问 https://creator.douyin.com/creator-micro/content/upload；若页面是扫码登录，用抖音 App 扫二维码。",
  "确认是正确的创作者账号，并保持 Ego 登录。在 Ego 里登录抖音效果更好。",
  "重新跑 login-check。只有退出码 0 之后才发布。",
  "登录态会过期。每次发布前都要先检查。不要代填密码，不要粘贴 Cookie。",
];

export const LOGIN_TIP =
  "Tell the user: being logged into Douyin inside Ego Lite works better. Before every publish, run login-check. If exit 2, ask them to open Ego Lite, scan the QR on creator.douyin.com, then re-run. Never type a password or paste cookies. Defaults stay public, allow save, and publish immediately.";

export const LOGIN_TIP_ZH =
  "请告诉用户：在 Ego Lite 里登录抖音效果更好。每次发布前先跑 login-check。若 exit 2，请人在 Ego Lite 打开 creator.douyin.com 扫码登录后再跑。不要代填密码，不要粘贴 Cookie。默认保持公开、允许保存、立即发布。";

export const USAGE = `douyin-video — publish a local video to the Douyin creator center via Ego Lite

Install Ego Lite and put ego-browser on PATH first. Missing ego-browser soft-fails (exit 2) with install hints.
This skill does not download video. The caller supplies a local file. There is no yt-dlp step.
Being logged into Douyin in Ego works better.

  node scripts/check-login.mjs
  node scripts/check-login.mjs --keep
  bash scripts/publish.sh /absolute/path/to/video.mp4 "标题" "简介 #话题"
  bash scripts/publish.sh /absolute/path/to/video.mp4 "标题" "简介" <spaceId>
  bash scripts/publish.sh /absolute/path/to/video.mp4 "标题" "简介" <spaceId> 1

check-login:
  Opens https://creator.douyin.com/creator-micro/content/upload in ego-browser.
  Exit 0 when logged in. Exit 2 when login is required or ego-browser is missing.
  Always print login_tip. On soft-fail also print how_to_login / how_to_login_zh.
  Default finish({ keep: [] }). --keep leaves the page and calls handOff().

publish:
  Writes /tmp/douyin-video-publish.json (ego's Node does not inherit shell env),
  then runs publish.js inside ego-browser.
  Title is a separate input, at most 30 Unicode code points. Description is required.
  Success JSON: { "ok": true, "manageUrl": "https://creator.douyin.com/creator-micro/content/manage" }.
  Exit 0 ok, 1 flow error, 2 login required.
  Default finish({ keep: [] }). Pass keep 1 to leave the tab open.
  A location-permission interrupt leaves the space open. Re-run with that spaceId.
`;

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function codePointLength(value) {
  return [...String(value ?? "")].length;
}

export function parseCheckArgs(argv) {
  const out = { keep: false, help: false, taskName: "douyin-login-check" };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") out.help = true;
    else if (arg === "--keep") out.keep = true;
    else if (arg === "--task-name") out.taskName = String(argv[++i] || out.taskName);
    else throw new Error(`Unknown arg: ${arg}`);
  }
  return out;
}

export function parsePublishArgs(argv) {
  const args = argv || [];
  if (args.length < 3 || !args[0]) {
    throw new Error("usage: publish.sh <video-file> <title> <description> [spaceId] [keep=1]");
  }
  if (args.length > 5) throw new Error("too many arguments");
  return {
    video: String(args[0]),
    title: String(args[1] ?? ""),
    desc: String(args[2] ?? ""),
    spaceId: parseSpaceId(args[3]),
    keep: parseKeep(args[4]),
  };
}

function parseSpaceId(raw) {
  if (raw == null || raw === "") return null;
  if (!/^\d+$/.test(String(raw))) throw new Error("spaceId must be an integer");
  return Number(raw);
}

function parseKeep(raw) {
  if (raw == null || raw === "" || raw === "0" || raw === "false") return false;
  if (raw === "1" || raw === "true") return true;
  throw new Error("keep must be 1 or 0");
}

export function validatePublishInput({ video, title, desc, exists, sizeBytes = 0 } = {}) {
  if (!video || !exists) return { ok: false, error: `视频文件不存在: ${video || ""}` };
  const rawTitle = String(title ?? "");
  if (!rawTitle.trim()) {
    return { ok: false, error: "标题不能为空: 抖音标题是独立输入框(限30字),必填以获得流量" };
  }
  const titleLength = codePointLength(rawTitle);
  if (titleLength > TITLE_LIMIT) {
    return { ok: false, error: `标题超过30字(当前 ${titleLength} 字),请精简` };
  }
  if (!String(desc ?? "").trim()) {
    return { ok: false, error: "简介不能为空: 简介承载话题标签" };
  }
  const sizeMB = Math.round((Number(sizeBytes) / 1048576) * 10) / 10;
  return { ok: true, sizeMB, titleLength };
}

/** 扫码登录 vs 创作者上传页. Platform chrome is body text only, not the document title. */
export function classifyLogin({ url = "", title = "", text = "", signals = {} } = {}) {
  const pageUrl = String(url || "");
  const body = String(text || "");
  const blob = `${pageUrl}\n${title}\n${body}`;
  const onLoginUrl = /\/login(\b|[/?#]|$)/i.test(pageUrl) || /passport\.douyin\.com|sso\.douyin\.com/i.test(pageUrl);
  const qrText = /扫码登录|二维码登录/.test(blob);
  const loginWall = LOGIN_WALL_RE.test(blob) || onLoginUrl || Boolean(signals.onLoginWall);
  const uploadChrome = UPLOAD_CHROME_RE.test(body) || Boolean(signals.uploadChrome);
  const platformHint = PLATFORM_CHROME_RE.test(body) || Boolean(signals.platformChrome) || uploadChrome;
  const loggedIn = !loginWall && platformHint;
  return strip({
    logged_in: loggedIn,
    login_required: !loggedIn,
    on_login_page: Boolean(onLoginUrl || qrText || loginWall),
    login_wall: loginWall || undefined,
    has_qr_hint: qrText || undefined,
    url: pageUrl || undefined,
    title: title || undefined,
  });
}

export function needsRepaint(detected = {}) {
  if (detected.platformChrome || detected.uploadChrome) return false;
  if (detected.onLoginWall) return false;
  const classified = classifyLogin({
    url: detected.url,
    title: detected.title,
    text: detected.text,
    signals: {
      platformChrome: detected.platformChrome,
      uploadChrome: detected.uploadChrome,
      onLoginWall: detected.onLoginWall,
    },
  });
  return !classified.logged_in && !classified.on_login_page;
}

export function egoMissingSummary(command = "check-login") {
  return strip({
    skill: SKILL,
    command,
    ok: false,
    logged_in: false,
    login_required: true,
    exitCode: 2,
    error: "ego-browser not found on PATH",
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    how_to_login: [
      "Install Ego Lite, then ensure `ego-browser` is on PATH (often ~/.local/bin).",
      ...HOW_TO_LOGIN,
    ],
    how_to_login_zh: [
      "先安装 Ego Lite，并把 ego-browser 放进 PATH（常见 ~/.local/bin）。",
      ...HOW_TO_LOGIN_ZH,
    ],
  });
}

export function loginRequiredBody({ spaceId, error } = {}) {
  return {
    ok: false,
    skill: SKILL,
    logged_in: false,
    login_required: true,
    exitCode: 2,
    spaceId,
    error: error || "Douyin creator login required in Ego Lite",
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    how_to_login: HOW_TO_LOGIN,
    how_to_login_zh: HOW_TO_LOGIN_ZH,
  };
}

export function flowErrorBody(error, extra = {}) {
  return { ok: false, error: String(error), exitCode: 1, ...extra };
}

export function isUploadVideoLabel(text) {
  return String(text || "").replace(/\s/g, "") === "上传视频";
}

export function titleWriteOk(result, expected) {
  if (!result || result.ok === false && result.value == null) return false;
  return String(result.value ?? "") === String(expected ?? "");
}

export function descWriteOk(result, expected) {
  if (!result || !result.ok) return false;
  return String(result.text || "").trim() === String(expected || "").trim();
}

/** The publish control is a BUTTON whose own text is exactly 发布. */
export function isPublishOwnText(ownText, tagName = "BUTTON") {
  return String(tagName || "").toUpperCase() === "BUTTON" && ownText === "发布";
}

export function clickPoint(rect) {
  if (!rect) return null;
  const { x, y, width, height } = rect;
  if (![x, y, width, height].every((n) => typeof n === "number" && Number.isFinite(n))) return null;
  if (width <= 0 || height <= 0) return null;
  return { x: x + width / 2, y: y + height / 2 };
}

export function isPublishFormUrl(url) {
  return String(url || "").includes(FORM_PATH);
}

export function isUserControlInterrupt(error) {
  const msg = String((error && (error.message || error)) || "");
  return /user-control|位置权限|geolocation|NotAllowedError|permission/i.test(msg);
}

export function resumeAfterInterrupt(spaceId) {
  const id = spaceId == null || spaceId === "" ? "" : ` ${spaceId}`;
  return `位置权限或用户确认打断了本次调用。请在浏览器里处理弹窗（建议拒绝），然后带 spaceId${id} 重跑。点击通常已生效，脚本探测到发布表单后会跳过重复上传。`;
}

export function verifyPublished({ url = "", text = "" } = {}) {
  const onManage = /content\/manage/.test(String(url));
  const successText = /发布成功/.test(String(text));
  const ok = Boolean(onManage || successText);
  return strip({
    ok,
    url: String(url || "") || undefined,
    onManage: onManage || undefined,
    successText: successText || undefined,
  });
}

export function publishSuccessBody({ title, spaceId, manageUrl = MANAGE_URL } = {}) {
  return {
    ok: true,
    title,
    manageUrl,
    spaceId,
  };
}

export function resolveEgoExit({ stdout = "", stderr = "", code = 1 } = {}) {
  const combined = `${stdout}\n${stderr}`;
  const lines = combined.split(/\n/).map((line) => line.trim()).filter(Boolean).reverse();
  for (const line of lines) {
    if (!line.startsWith("{")) continue;
    try {
      const obj = JSON.parse(line);
      if (typeof obj.exitCode === "number") return obj.exitCode;
    } catch {
      // keep scanning
    }
  }
  const matched = combined.match(/nodejs process exited with code (\d+)/);
  if (matched) return Number(matched[1]);
  if (code === 0) return 0;
  return code ?? 1;
}
