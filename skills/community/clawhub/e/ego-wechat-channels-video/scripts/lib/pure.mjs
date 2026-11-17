// Pure helpers for wechat-channels-video. No browser, no process.exit.

export const BASE = "https://channels.weixin.qq.com";
export const LOGIN_HINT = "login.html";
export const DEFAULT_SERVE_PORT = 18765;

export const HOW_TO_LOGIN = [
  "Open the Ego Lite app (the same profile ego-browser drives).",
  "Visit https://channels.weixin.qq.com — if you land on login.html, scan the QR with WeChat.",
  "Ignore any “加载失败，点击重试” near WeChat quick-login; that probe fails when the desktop WeChat client is offline. The QR lives in a cross-origin iframe.",
  "Confirm the correct Channels account, leave Ego logged in, then re-run this skill’s login-check (and only then publish).",
  "Ego Lite upgrades that bump Chromium can wipe the session — always login-check before each publish.",
];

export const HOW_TO_LOGIN_ZH = [
  "打开 Ego Lite（ego-browser 驱动的同一个配置档）。",
  "访问 https://channels.weixin.qq.com；若跳到 login.html，用微信扫二维码登录。",
  "忽略「加载失败，点击重试」：那是探本地微信客户端失败，二维码在跨域 iframe 里，点重试没用。",
  "确认是正确的视频号账号，保持 Ego 登录，再重新跑 login-check；通过后才继续发布。",
  "升级 Ego Lite（尤其 Chromium 大版本）可能清掉登录态——每次发布前都要先检查。",
];

export const LOGIN_TIP =
  "Tell the user: WeChat Channels sessions in Ego expire quickly. Before every publish, run login-check. If exit 2, ask them to open Ego Lite, scan the QR on channels.weixin.qq.com, then re-run. Never type a password or paste cookies.";

export const LOGIN_TIP_ZH =
  "请告诉用户：视频号助手在 Ego 里的登录态过期很快。每次发布前先跑 login-check。若 exit 2，请人在 Ego Lite 打开 channels.weixin.qq.com 扫码登录后再跑。不要代填密码，不要粘贴 Cookie。";

export const USAGE = `wechat-channels-video — WeChat Channels helpers via Ego Lite

Install Ego Lite and put ego-browser on PATH first. Missing ego-browser soft-fails (exit 2) with install hints.

  node scripts/check-login.mjs
  node scripts/check-login.mjs --keep
  node scripts/serve-file.mjs --file /path/to/video.mp4 --port 18765

check-login:
  Opens channels.weixin.qq.com in ego-browser, reports logged_in JSON.
  Exit 0 when logged in. Exit 2 when login required or ego-browser missing.
  Always print login_tip; on soft-fail also print how_to_login.

serve-file:
  Serves one local file over http://127.0.0.1:<port>/ with CORS * for page.evaluate fetch + DataTransfer inject.
  Prints JSON { ok, url, file, bytes, port } then stays until SIGINT.

The publish/draft UI flow (wujie form, cover chooser, location) stays in SKILL.md for the agent — too brittle for a full script.
`;

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function parseCheckArgs(argv) {
  const out = { keep: false, help: false, taskName: "wechat-channels-login-check" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") out.help = true;
    else if (a === "--keep") out.keep = true;
    else if (a === "--task-name") out.taskName = String(argv[++i] || out.taskName);
    else throw new Error(`Unknown arg: ${a}`);
  }
  return out;
}

export function parseServeArgs(argv) {
  const out = { file: null, port: DEFAULT_SERVE_PORT, help: false, name: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") out.help = true;
    else if (a === "--file" || a === "-f") out.file = argv[++i];
    else if (a === "--port" || a === "-p") out.port = Number(argv[++i]);
    else if (a === "--name") out.name = argv[++i];
    else throw new Error(`Unknown arg: ${a}`);
  }
  if (!out.help) {
    if (!out.file) throw new Error("--file is required");
    if (!Number.isInteger(out.port) || out.port < 1 || out.port > 65535) {
      throw new Error("--port must be an integer 1-65535");
    }
  }
  return out;
}

/** Classify Channels login from URL + optional page text/signals. */
export function classifyLogin({ url = "", title = "", text = "", signals = {} } = {}) {
  const u = String(url || "");
  const blob = `${u}\n${title}\n${text}`;
  const onLoginPage = /login\.html/i.test(u) || /\/login(\?|$)/i.test(u);
  const hasQrHint = /扫码|二维码|微信扫一扫|登录/.test(blob) && onLoginPage;
  const platformHint =
    /\/platform\//i.test(u) ||
    /内容管理|发表视频|草稿|视频号助手/.test(blob) ||
    Boolean(signals.platformChrome);
  const loggedIn = !onLoginPage && (platformHint || Boolean(signals.loggedInCookie));
  return strip({
    logged_in: loggedIn,
    login_required: !loggedIn,
    on_login_page: onLoginPage,
    has_qr_hint: hasQrHint || undefined,
    url: u || undefined,
    title: title || undefined,
  });
}

export function contentTypeFor(filePath) {
  const lower = String(filePath || "").toLowerCase();
  if (lower.endsWith(".mp4")) return "video/mp4";
  if (lower.endsWith(".mov")) return "video/quicktime";
  if (lower.endsWith(".webm")) return "video/webm";
  if (lower.endsWith(".jpg") || lower.endsWith(".jpeg")) return "image/jpeg";
  if (lower.endsWith(".png")) return "image/png";
  if (lower.endsWith(".webp")) return "image/webp";
  return "application/octet-stream";
}

export function publicUrl(port, leaf) {
  const name = encodeURIComponent(leaf || "file");
  return `http://127.0.0.1:${port}/${name}`;
}

export function egoMissingSummary() {
  return strip({
    skill: "wechat-channels-video",
    command: "check-login",
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
