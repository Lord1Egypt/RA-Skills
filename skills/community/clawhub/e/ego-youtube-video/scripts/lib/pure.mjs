// Pure helpers for youtube-video. No browser, no process.exit.

export const SKILL = "youtube-video";
export const STUDIO_URL = "https://studio.youtube.com/";
export const PUBLISH_CONFIG_PATH = "/tmp/youtube-video-publish.json";
export const PUBLISH_FAIL_SHOT = "/tmp/youtube-video-publish-failed.png";

export const VISIBILITIES = ["private", "unlisted", "public"];
export const VIDEO_EXT_RE = /\.(mp4|mov|webm|mkv|m4v|avi|mpeg|mpg|wmv|flv|3gp)$/i;
export const THUMB_EXT_RE = /\.(jpg|jpeg|png|webp|gif)$/i;

// Body text, not the document title. A signed-out tab can still be titled YouTube Studio.
export const PLATFORM_CHROME_RE = /YouTube Studio|Upload videos|Channel content|Analytics|Dashboard|上传视频|YouTube 工作室|频道内容|数据分析|信息中心/;
export const LOGIN_WALL_RE = /Sign in to YouTube|Choose an account|Use your Google Account|使用 Google 账号登录|使用您的 Google 账号|选择账号|登录以继续|扫码登录/;
export const LOGIN_COOKIE_RE = /(?:^|;\s*)(?:LOGIN_INFO|SAPISID|__Secure-1PSID|__Secure-3PSID)=/;

export const HOW_TO_LOGIN = [
  "Install Ego Lite and put ego-browser on PATH. Open the Ego Lite app (the same profile ego-browser drives).",
  "Visit https://studio.youtube.com/ and sign in to the Google account that owns the YouTube channel.",
  "Confirm the channel switcher shows the channel you want. Leave that YouTube session signed in inside Ego.",
  "Re-run this skill’s login-check. Publish only after exit 0. Being signed in to YouTube in Ego gives the best results.",
  "Sessions can expire. Login-check before every publish. Never type a password or paste cookies.",
];

export const HOW_TO_LOGIN_ZH = [
  "先安装 Ego Lite，并把 ego-browser 放进 PATH。打开 Ego Lite（ego-browser 驱动的同一个配置档）。",
  "访问 https://studio.youtube.com/ ，登录拥有该 YouTube 频道的 Google 账号。",
  "确认频道切换器是要发布的频道，并保持 Ego 里的 YouTube 为登录状态。",
  "重新跑 login-check。只有退出码 0 之后才发布。在 Ego 里登录 YouTube 效果最好。",
  "登录态会过期。每次发布前都要先检查。不要代填密码，不要粘贴 Cookie。",
];

export const LOGIN_TIP =
  "Tell the user: being logged in to YouTube inside Ego Lite gives the best results. Before every publish, run login-check. If exit 2, ask them to open Ego Lite, sign in at https://studio.youtube.com, then re-run. Never type a password or paste cookies. Default visibility is private. Made for kids stays No unless the caller says otherwise.";

export const LOGIN_TIP_ZH =
  "请告诉用户：在 Ego Lite 里登录 YouTube 效果最好。每次发布前先跑 login-check。若 exit 2，请人在 Ego Lite 打开 studio.youtube.com 登录后再跑。不要代填密码，不要粘贴 Cookie。公开范围默认 private。未另外说明时，儿童向选项保持「否」。";

export const USAGE = `youtube-video — publish a local video to YouTube Studio via Ego Lite

Install Ego Lite and put ego-browser on PATH first. Missing ego-browser soft-fails (exit 2) with install hints.
This skill does not download video. The caller supplies a local file. There is no yt-dlp step.

  node scripts/check-login.mjs
  node scripts/check-login.mjs --keep
  bash scripts/publish.sh /absolute/path/to/video.mp4 "Title" "Description"
  bash scripts/publish.sh --video /absolute/path/to/video.mp4 --title "Title" \\
    --description "Description" --tags "one,two" --visibility private \\
    --thumbnail /absolute/path/to/thumbnail.jpg --made-for-kids no

Visibility defaults to private. Made for kids defaults to no. Do not pass public unless the caller asked.

check-login:
  Opens https://studio.youtube.com/ in ego-browser.
  Exit 0 when logged in. Exit 2 when login is required or ego-browser is missing.
  Always print login_tip. On soft-fail also print how_to_login / how_to_login_zh.
  Default finish({ keep: [] }). --keep leaves the page and calls handOff().

publish:
  Writes /tmp/youtube-video-publish.json (ego's Node does not inherit shell env),
  then runs publish.js inside ego-browser.
  Success JSON includes videoId, videoUrl, and a processing status
  (Uploading, Upload complete, Processing, Checks complete, Saved, or Published).
  Exit 0 ok, 1 flow error, 2 login required.
  Default finish({ keep: [] }). Pass --keep to leave the Studio tab open.
`;

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function parseCheckArgs(argv) {
  const out = { keep: false, help: false, taskName: "youtube-login-check" };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") out.help = true;
    else if (arg === "--keep") out.keep = true;
    else if (arg === "--task-name") out.taskName = String(argv[++i] || out.taskName);
    else throw new Error(`Unknown arg: ${arg}`);
  }
  return out;
}

function takeValue(args, index, flag) {
  if (index >= args.length || args[index] == null || String(args[index]).startsWith("--")) {
    throw new Error(`${flag} requires a value`);
  }
  return args[index];
}

export function parseTags(raw) {
  if (raw == null || raw === "") return [];
  const parts = Array.isArray(raw) ? raw : String(raw).split(",");
  const out = [];
  for (const part of parts) {
    const tag = String(part).trim();
    if (!tag || out.includes(tag)) continue;
    out.push(tag);
  }
  return out;
}

export function parseVisibility(raw) {
  const value = String(raw ?? "private").trim().toLowerCase();
  if (!VISIBILITIES.includes(value)) {
    throw new Error("visibility must be private, unlisted, or public");
  }
  return value;
}

export function parseMadeForKids(raw) {
  const value = String(raw ?? "no").trim().toLowerCase();
  if (["no", "false", "0", "n"].includes(value)) return false;
  if (["yes", "true", "1", "y"].includes(value)) return true;
  throw new Error("made-for-kids must be yes or no");
}

export function parsePublishArgs(argv) {
  const expanded = [];
  for (const raw of argv || []) {
    const arg = String(raw);
    if (arg.startsWith("--") && arg.includes("=")) {
      const index = arg.indexOf("=");
      expanded.push(arg.slice(0, index), arg.slice(index + 1));
    } else {
      expanded.push(arg);
    }
  }

  const out = {
    video: "",
    title: "",
    description: "",
    tags: [],
    visibility: "private",
    thumbnail: "",
    madeForKids: false,
    spaceId: null,
    keep: false,
  };
  const positional = [];
  for (let i = 0; i < expanded.length; i++) {
    const arg = expanded[i];
    if (arg === "--video") out.video = String(takeValue(expanded, ++i, "--video"));
    else if (arg === "--title") out.title = String(takeValue(expanded, ++i, "--title"));
    else if (arg === "--description" || arg === "--desc") {
      out.description = String(takeValue(expanded, ++i, arg));
    } else if (arg === "--tags") out.tags = parseTags(takeValue(expanded, ++i, "--tags"));
    else if (arg === "--visibility") out.visibility = parseVisibility(takeValue(expanded, ++i, "--visibility"));
    else if (arg === "--thumbnail") out.thumbnail = String(takeValue(expanded, ++i, "--thumbnail"));
    else if (arg === "--made-for-kids") {
      out.madeForKids = parseMadeForKids(takeValue(expanded, ++i, "--made-for-kids"));
    } else if (arg === "--space-id") out.spaceId = parseSpaceId(takeValue(expanded, ++i, "--space-id"));
    else if (arg === "--keep") out.keep = true;
    else if (arg === "--no-keep") out.keep = false;
    else if (arg.startsWith("--")) throw new Error(`Unknown arg: ${arg}`);
    else positional.push(arg);
  }

  const slots = ["video", "title", "description"];
  let slot = 0;
  for (const value of positional) {
    while (slot < slots.length && out[slots[slot]]) slot += 1;
    if (slot >= slots.length) throw new Error("too many arguments");
    out[slots[slot]] = value;
    slot += 1;
  }

  if (!out.video || !String(out.title || "").trim()) {
    throw new Error('usage: publish.sh <video> <title> [description] [--visibility private] [--tags a,b] [--thumbnail file] [--made-for-kids no] [--space-id N] [--keep]');
  }
  return out;
}

function parseSpaceId(raw) {
  if (raw == null || raw === "") return null;
  if (!/^\d+$/.test(String(raw))) throw new Error("spaceId must be an integer");
  return Number(raw);
}

export function validatePublishInput({
  video,
  title,
  description = "",
  tags = [],
  visibility = "private",
  thumbnail = "",
  madeForKids = false,
  exists,
  thumbExists = true,
  sizeBytes = 0,
} = {}) {
  if (!video || !exists) return { ok: false, error: `视频文件不存在: ${video || ""}` };
  if (!VIDEO_EXT_RE.test(String(video))) return { ok: false, error: `不是支持的视频文件: ${video}` };
  if (!Number(sizeBytes)) return { ok: false, error: `视频文件是空的: ${video}` };
  const trimmedTitle = String(title || "").trim();
  if (!trimmedTitle) return { ok: false, error: "标题不能为空" };
  if ([...trimmedTitle].length > 100) return { ok: false, error: "标题不能超过 100 个字符" };
  if ([...String(description || "")].length > 5000) return { ok: false, error: "简介不能超过 5000 个字符" };
  const audience = String(visibility || "private").toLowerCase();
  if (!VISIBILITIES.includes(audience)) {
    return { ok: false, error: `公开范围必须是 private、unlisted 或 public: ${visibility}` };
  }
  const tagList = parseTags(tags);
  if (tagList.join(",").length > 500) return { ok: false, error: "标签总长度不能超过 500 个字符" };
  if (thumbnail) {
    if (!thumbExists) return { ok: false, error: `缩略图不存在: ${thumbnail}` };
    if (!THUMB_EXT_RE.test(String(thumbnail))) return { ok: false, error: `不是支持的缩略图: ${thumbnail}` };
  }
  const sizeMB = Math.round((Number(sizeBytes) / 1048576) * 10) / 10;
  return {
    ok: true,
    sizeMB,
    visibility: audience,
    madeForKids: Boolean(madeForKids),
    tags: tagList,
  };
}

export function isLoginWall({ url = "", title = "", text = "" } = {}) {
  const pageUrl = String(url || "");
  const blob = `${pageUrl}\n${title}\n${text}`;
  if (/accounts\.google\.com/i.test(pageUrl)) return true;
  if (/\/signin(\b|[/?#]|$)/i.test(pageUrl)) return true;
  if (/ServiceLogin/i.test(pageUrl)) return true;
  return LOGIN_WALL_RE.test(blob);
}

export function detectSignals({ url = "", title = "", text = "", cookie = "" } = {}) {
  const body = String(text || "");
  return {
    platformChrome: PLATFORM_CHROME_RE.test(body),
    onLoginWall: isLoginWall({ url, title, text }),
    loggedInCookie: LOGIN_COOKIE_RE.test(String(cookie || "")),
  };
}

/** Google sign-in vs YouTube Studio. Platform chrome is body text only, not the document title. */
export function classifyLogin({ url = "", title = "", text = "", cookie = "", signals = {} } = {}) {
  const pageUrl = String(url || "");
  const body = String(text || "");
  const loginWall = Boolean(signals.onLoginWall) || isLoginWall({ url: pageUrl, title, text: body });
  const platformHint = PLATFORM_CHROME_RE.test(body) || Boolean(signals.platformChrome);
  const cookieIn = LOGIN_COOKIE_RE.test(String(cookie || "")) || Boolean(signals.loggedInCookie);
  const loggedIn = !loginWall && (platformHint || cookieIn);
  return strip({
    logged_in: loggedIn,
    login_required: !loggedIn,
    on_login_page: loginWall,
    login_wall: loginWall,
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
    cookie: detected.cookie,
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
    error: error || "YouTube Studio login required in Ego Lite",
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    how_to_login: HOW_TO_LOGIN,
    how_to_login_zh: HOW_TO_LOGIN_ZH,
  };
}

export function flowErrorBody(error, extra = {}) {
  return { ok: false, error: String(error), exitCode: 1, ...extra };
}

export function metadataWriteOk(result, expected = {}) {
  if (!result || !result.ok) return false;
  const norm = (value) => String(value || "").replace(/\u00a0/g, " ").trim();
  if (norm(result.title) !== norm(expected.title)) return false;
  const description = norm(expected.description);
  if (!description) return true;
  return norm(result.description) === description;
}

export function uploadSignals(text) {
  const body = String(text || "");
  const status = classifyProcessingStatus(body);
  const started = Boolean(status) || /Uploading|正在上传|上传中|Processing|正在处理|Upload complete|上传完成|上传完毕/.test(body);
  return {
    started,
    uploading: /Uploading|正在上传|上传中/.test(body) && !/Upload complete|上传完成|上传完毕/.test(body),
    status,
  };
}

const STATUS_RULES = [
  [/Checks complete|检查完毕|检查完成|No issues found/i, "Checks complete"],
  [/Processing will begin|处理即将开始|正在处理|Video processing|\bProcessing\b/i, "Processing"],
  [/Upload complete|上传完毕|上传完成/i, "Upload complete"],
  [/Uploading|正在上传|上传中/i, "Uploading"],
  [/Video published|视频已发布|Your video is public/i, "Published"],
  [/saved as private|已保存|Video saved|Share your video|分享你的视频|Video link/i, "Saved"],
];

export function classifyProcessingStatus(text) {
  const body = String(text || "");
  for (const [pattern, status] of STATUS_RULES) {
    if (pattern.test(body)) return status;
  }
  return null;
}

export function extractVideoId(blob) {
  const text = String(blob || "");
  const patterns = [
    /youtu\.be\/([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])/,
    /[?&]v=([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])/,
    /studio\.youtube\.com\/video\/([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])/,
    /\/(?:video|shorts|live|embed)\/([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])/,
  ];
  for (const pattern of patterns) {
    const matched = text.match(pattern);
    if (matched) return matched[1];
  }
  return null;
}

export function videoUrlFor(videoId) {
  if (!videoId) return null;
  return `https://youtu.be/${videoId}`;
}

export function studioUrlFor(videoId) {
  if (!videoId) return null;
  return `https://studio.youtube.com/video/${videoId}/edit`;
}

export function verifyPublished({ text = "", href = "", pageUrl = "" } = {}) {
  const blob = `${href}\n${pageUrl}\n${text}`;
  const videoId = extractVideoId(blob);
  const status = classifyProcessingStatus(text);
  const ok = Boolean(videoId && status);
  return strip({
    ok,
    status: ok ? status : undefined,
    videoId: videoId || undefined,
    videoUrl: videoUrlFor(videoId) || undefined,
    studioUrl: studioUrlFor(videoId) || undefined,
  });
}

export function publishSuccessBody({
  videoId,
  videoUrl,
  studioUrl,
  status,
  visibility,
  title,
  description = "",
  madeForKids = false,
  tags = [],
  spaceId,
} = {}) {
  return {
    ok: true,
    status,
    videoId,
    videoUrl,
    studioUrl,
    visibility: visibility || "private",
    title,
    description: description || "",
    madeForKids: Boolean(madeForKids),
    tags: tags || [],
    spaceId,
  };
}

export function uploadLimitHit(text) {
  return /daily upload limit|upload limit reached|上传次数已达上限|已达到上传上限/i.test(String(text || ""));
}

export function visibilitySelector(visibility) {
  const name = { private: "PRIVATE", unlisted: "UNLISTED", public: "PUBLIC" }[visibility] || "PRIVATE";
  return `tp-yt-paper-radio-button[name="${name}"]`;
}

export function audienceSelector(madeForKids) {
  const name = madeForKids ? "VIDEO_MADE_FOR_KIDS_MFK" : "VIDEO_MADE_FOR_KIDS_NOT_MFK";
  return `tp-yt-paper-radio-button[name="${name}"]`;
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
