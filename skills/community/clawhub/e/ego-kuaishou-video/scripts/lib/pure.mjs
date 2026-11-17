// Pure helpers for kuaishou-video. No browser, no process.exit.

export const SKILL = "kuaishou-video";
export const BASE = "https://cp.kuaishou.com";
export const PUBLISH_URL = `${BASE}/article/publish/video`;
export const MANAGE_URL = `${BASE}/article/manage/video?status=2&from=publish`;
export const COMMENT_URL = `${BASE}/article/comment`;
export const PUBLISH_CONFIG_PATH = "/tmp/kuaishou-video-publish.json";
export const COMMENT_CONFIG_PATH = "/tmp/kuaishou-video-comment.json";
export const PUBLISH_FAIL_SHOT = "/tmp/kuaishou-video-publish-failed.png";
export const COMMENT_FAIL_SHOT = "/tmp/kuaishou-video-comment-failed.png";

// Body text, not the document title. The login page title can already say 创作者服务平台.
export const PLATFORM_CHROME_RE = /上传视频|发布作品|评论管理|作品管理|创作者服务平台/;
export const LOGIN_WALL_RE = /扫码登录|二维码登录|请登录/;
export const LOGIN_COOKIE_RE = /(?:^|;\s*)kuaishou\.server\.web_st=/;

export const HOW_TO_LOGIN = [
  "Open the Ego Lite app (the same profile ego-browser drives).",
  "Visit https://cp.kuaishou.com/article/publish/video — if the page shows 扫码登录, scan the QR with the Kuaishou app.",
  "Confirm the correct creator account and leave Ego logged in.",
  "Re-run this skill’s login-check. Continue to publish only after exit 0.",
  "Sessions can expire. Login-check before every publish. Never type a password or paste cookies.",
];

export const HOW_TO_LOGIN_ZH = [
  "打开 Ego Lite（ego-browser 驱动的同一个配置档）。",
  "访问 https://cp.kuaishou.com/article/publish/video；若页面是扫码登录，用快手 App 扫二维码。",
  "确认是正确的创作者账号，并保持 Ego 登录。",
  "重新跑 login-check。只有退出码 0 之后才发布。",
  "登录态会过期。每次发布前都要先检查。不要代填密码，不要粘贴 Cookie。",
];

export const LOGIN_TIP =
  "Tell the user: Kuaishou creator sessions live in Ego Lite. Before every publish, run login-check. If exit 2, ask them to open Ego Lite, scan the QR on cp.kuaishou.com, then re-run. Never type a password or paste cookies.";

export const LOGIN_TIP_ZH =
  "请告诉用户：快手创作者平台的登录态在 Ego Lite 里。每次发布前先跑 login-check。若 exit 2，请人在 Ego Lite 打开 cp.kuaishou.com 扫码登录后再跑。不要代填密码，不要粘贴 Cookie。";

export const USAGE = `kuaishou-video — publish a local video to the Kuaishou creator platform via Ego Lite

Install Ego Lite and put ego-browser on PATH first. Missing ego-browser soft-fails (exit 2) with install hints.
This skill does not download video. The caller supplies a local file.

  node scripts/check-login.mjs
  node scripts/check-login.mjs --keep
  bash scripts/publish.sh /absolute/path/to/video.mp4 "描述 #话题"
  bash scripts/publish.sh /absolute/path/to/video.mp4 "描述" <spaceId> 1
  bash scripts/comment.sh "评论内容" "标题片段"

check-login:
  Opens https://cp.kuaishou.com/article/publish/video in ego-browser.
  Exit 0 when logged in. Exit 2 when login is required or ego-browser is missing.
  Always print login_tip. On soft-fail also print how_to_login / how_to_login_zh.
  Default finish({ keep: [] }). --keep leaves the page and calls handOff().

publish:
  Writes /tmp/kuaishou-video-publish.json (ego's Node does not inherit shell env),
  then runs publish.js inside ego-browser.
  Success JSON: { "ok": true, "status": "审核中" }.
  Exit 0 ok, 1 flow error, 2 login required.

comment (optional):
  Posts from the creator comment manager at /article/comment.
  Same exit codes. The public www site does not share this login.
`;

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function parseCheckArgs(argv) {
  const out = { keep: false, help: false, taskName: "kuaishou-login-check" };
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
  if (args.length < 2 || !args[0]) {
    throw new Error("usage: publish.sh <video-file> <description> [spaceId] [keep=1]");
  }
  if (args.length > 4) throw new Error("too many arguments");
  return {
    video: String(args[0]),
    desc: String(args[1] ?? ""),
    spaceId: parseSpaceId(args[2]),
    keep: parseKeep(args[3]),
  };
}

export function parseCommentArgs(argv) {
  const args = argv || [];
  if (args.length < 1 || args[0] == null || args[0] === "") {
    throw new Error("usage: comment.sh <comment> [title-hint] [spaceId] [keep=1]");
  }
  if (args.length > 4) throw new Error("too many arguments");
  return {
    comment: String(args[0]),
    titleHint: String(args[1] || ""),
    spaceId: parseSpaceId(args[2]),
    keep: parseKeep(args[3]),
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

export function validatePublishInput({ video, desc, exists, sizeBytes = 0 } = {}) {
  if (!video || !exists) return { ok: false, error: `视频文件不存在: ${video || ""}` };
  if (!String(desc || "").trim()) return { ok: false, error: "描述不能为空: 快手要求作品描述" };
  const sizeMB = Math.round((Number(sizeBytes) / 1048576) * 10) / 10;
  return { ok: true, sizeMB };
}

export function validateCommentInput({ comment } = {}) {
  if (!String(comment || "").trim()) return { ok: false, error: "评论内容不能为空" };
  return { ok: true };
}

/** 扫码登录 vs 创作者后台. Platform chrome is body text only, not the document title. */
export function classifyLogin({ url = "", title = "", text = "", signals = {} } = {}) {
  const pageUrl = String(url || "");
  const body = String(text || "");
  const blob = `${pageUrl}\n${title}\n${body}`;
  const onLoginUrl = /\/login(\b|[/?#]|$)/i.test(pageUrl) || /passport\.kuaishou\.com/i.test(pageUrl);
  const qrText = /扫码登录|二维码登录/.test(blob);
  const loginWall = LOGIN_WALL_RE.test(blob) || onLoginUrl || Boolean(signals.onLoginWall);
  const platformHint = PLATFORM_CHROME_RE.test(body) || Boolean(signals.platformChrome);
  const loggedIn = !loginWall && (platformHint || Boolean(signals.loggedInCookie));
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
  if (detected.platformChrome) return false;
  if (detected.onLoginWall) return false;
  const classified = classifyLogin({
    url: detected.url,
    title: detected.title,
    text: detected.text,
    signals: {
      platformChrome: detected.platformChrome,
      loggedInCookie: detected.loggedInCookie,
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
    error: error || "Kuaishou creator login required in Ego Lite",
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    how_to_login: HOW_TO_LOGIN,
    how_to_login_zh: HOW_TO_LOGIN_ZH,
  };
}

export function flowErrorBody(error, extra = {}) {
  return { ok: false, error: String(error), exitCode: 1, ...extra };
}

export function descWriteOk(result, expected) {
  if (!result || !result.ok) return false;
  return String(result.text || "").trim() === String(expected || "").trim();
}

export function uploadSignals(text) {
  const body = String(text || "");
  return {
    accepted: body.includes("重新上传"),
    uploading: body.includes("上传中"),
  };
}

/** The publish control's own text is exactly 发布. 立即发布 / 定时发布 are different controls. */
export function isPublishOwnText(ownText) {
  return ownText === "发布";
}

export function publishClickPoint(rect) {
  if (!rect) return null;
  const { x, y, width, height } = rect;
  if (![x, y, width, height].every((n) => typeof n === "number" && Number.isFinite(n))) return null;
  if (width <= 0 || height <= 0) return null;
  return { x: x + width / 2, y: y + height / 2 };
}

export function verifyPublished({ url = "", text = "" } = {}) {
  const underReview = String(text).includes("审核中");
  const onManage = String(url).includes("article/manage/video");
  const ok = onManage && underReview;
  return strip({
    ok,
    status: ok ? "审核中" : undefined,
    url: String(url || "") || undefined,
    underReview,
  });
}

export function publishSuccessBody({ desc, spaceId, manageUrl = MANAGE_URL } = {}) {
  return {
    ok: true,
    status: "审核中",
    desc,
    manageUrl,
    spaceId,
  };
}

export function extractSelectedVideoTitle(text) {
  const matched = String(text || "").match(/\n([^\n]{4,80})\n(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/);
  return (matched?.[1] || "").trim();
}

export function commentComposerReady(text) {
  return /有爱评论|发表评论/.test(String(text || ""));
}

export function commentTargetOk({ videoTitle = "", titleHint = "" } = {}) {
  if (!titleHint) return { ok: true, videoTitle };
  if (String(videoTitle || "").includes(titleHint)) return { ok: true, videoTitle };
  return {
    ok: false,
    videoTitle,
    error: `当前选中的视频是「${videoTitle}」,与标题片段「${titleHint}」不符。请在页面右上「选择视频」切换后,带 spaceId 重跑`,
  };
}

export function commentTypedOk(actual, expected) {
  return actual === expected;
}

export function verifyCommentPosted(text, comment) {
  const body = String(text || "");
  const expected = String(comment || "");
  const inList = expected.length > 0 && body.includes(expected) && !body.includes("暂无评论");
  const toast = body.includes("发送成功");
  return { ok: Boolean(inList && toast), inList, toast };
}

export function extractPhotoId(html) {
  const matched = String(html || "").match(/3x[a-z0-9]{9,15}/);
  return matched ? matched[0] : null;
}

export function shortVideoUrl(photoId) {
  if (!photoId) return null;
  return `https://www.kuaishou.com/short-video/${photoId}`;
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
