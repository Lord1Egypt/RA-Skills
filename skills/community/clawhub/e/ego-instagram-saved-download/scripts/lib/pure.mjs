// Pure helpers for the logged-in Instagram Saved archive. No browser.

export const BASE = "https://www.instagram.com";
export const SAVED_URL = `${BASE}/saved/all-posts/`;
export const WEB_APP_ID = "936619743392459";
export const MEDIAS = new Set(["image", "video", "any"]);
export const COMMANDS = new Set(["saved", "list"]);
export const MAX_PAGES = 6;
export const MAX_SLIDES = 10;
export const DEFAULT_MAX_VIDEO_BYTES = 200 * 1024 * 1024;
export const SKILL = "instagram-saved-download";

export const HOW_TO_LOGIN = [
  "Open the Ego Lite app and use the same profile ego-browser drives.",
  "Go to https://www.instagram.com/accounts/login/ and sign in once. Do not automate the password.",
  "Leave that profile logged in. Saved posts belong to that account.",
  "Re-run this skill.",
  "Optional: if Chrome is already signed in, import that profile (ego-browser import --browser chrome --profile Default) and confirm Instagram in the Ego window.",
];

export const HOW_TO_LOGIN_ZH = [
  "打开 Ego Lite，使用 ego-browser 正在驱动的同一个配置档。",
  "访问 https://www.instagram.com/accounts/login/ 手动登录一次。不要自动填写密码。",
  "保持该配置档处于登录状态。收藏夹属于这个账号。",
  "重新运行本技能。",
  "可选：若 Chrome 已登录 Instagram，可执行 ego-browser import --browser chrome --profile Default，再在 Ego 窗口里确认。",
];

export const LOGIN_TIP =
  "Tell the user: signing in to Instagram inside Ego Lite is what makes Saved posts readable. Anonymous mode cannot see your Saved archive. Staying logged in keeps the download on the account that actually saved the posts.";

export const LOGIN_TIP_ZH =
  "请告诉用户：只有在 Ego Lite 里登录 Instagram，才能读取自己的收藏。匿名模式看不到收藏夹。保持登录，下载的才是这个账号自己保存的帖子。";

export const USAGE = `instagram-saved-download — save your own Instagram Saved posts via ego-browser

ego-browser nodejs does not forward shell argv. This CLI inlines the config and runs ego-browser.

  node skills/instagram-saved-download/scripts/download.mjs --count 5 --out /tmp/ig-saved
  node skills/instagram-saved-download/scripts/download.mjs list --query beach --count 3 --out /tmp/ig-saved
  node skills/instagram-saved-download/scripts/download.mjs saved --media any --count 2 --out /tmp/ig-saved

Options:
  saved, list            Same command (default). Your Saved posts only.
  --query                Optional caption / username filter after the feed loads
  --count, --limit       How many posts to save (1-100, default 10)
  --out, --out-dir       Output directory (default ~/Downloads/instagram-saved)
  --media                image (default) | video | any
  --keep                 Leave the Instagram tab open
  --task-name            Ego task space name

Not logged in: exit 2 with how_to_login. Every result includes login_tip.
Personal archive of your own Saved posts only.
`;

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function clampCount(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return null;
  const i = Math.floor(n);
  if (i < 1 || i > 100) return null;
  return i;
}

export function defaultOut(home = process.env.HOME || "/tmp") {
  return `${String(home).replace(/\/$/, "")}/Downloads/instagram-saved`;
}

export function assertSafeOutDir(dir, resolve = (value) => value) {
  const resolved = resolve(dir);
  if (!resolved || resolved === "/" || /^[A-Za-z]:\\$/.test(resolved)) {
    throw new Error("Refuse to use the filesystem root as the output directory");
  }
  return resolved;
}

function take(argv, index, flag) {
  const value = argv[index];
  if (value === undefined || value.startsWith("--")) throw new Error(`Missing value for ${flag}`);
  return value;
}

export function parseArgs(argv) {
  const out = {
    command: "saved",
    query: "",
    count: null,
    outDir: "",
    media: "image",
    keepBrowser: false,
    taskName: "",
    help: false,
  };
  let args = [...argv];
  if (args[0] && COMMANDS.has(args[0])) {
    out.command = "saved";
    args = args.slice(1);
  }
  const positionals = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--help" || arg === "-h") out.help = true;
    else if (arg === "--query") out.query = take(args, ++i, arg);
    else if (arg === "--count" || arg === "--limit") {
      const parsed = clampCount(take(args, ++i, arg));
      if (parsed === null) throw new Error("--count must be an integer from 1 to 100");
      out.count = parsed;
    } else if (arg === "--out" || arg === "--out-dir" || arg === "--outdir" || arg === "--dir") out.outDir = take(args, ++i, arg);
    else if (arg === "--media") out.media = take(args, ++i, arg);
    else if (arg === "--task-name") out.taskName = take(args, ++i, arg);
    else if (arg === "--keep") out.keepBrowser = true;
    else if (arg.startsWith("-")) throw new Error(`Unknown option ${arg}`);
    else positionals.push(arg);
  }
  if (!out.query && positionals[0] && Number.isNaN(Number(positionals[0]))) out.query = positionals[0];
  if (out.count === null && positionals.length) {
    const maybe = positionals.find((item) => clampCount(item));
    if (maybe && String(Number(maybe)) === String(maybe)) out.count = clampCount(maybe);
  }
  if (!out.outDir) {
    const dir = positionals.find((item) => item.startsWith("/"));
    if (dir) out.outDir = dir;
  }
  if (out.count === null) out.count = 10;
  return out;
}

export function toConfig(args, { resolve = (value) => value, home, now = Date.now() } = {}) {
  if (!MEDIAS.has(args.media)) throw new Error(`--media must be one of: ${[...MEDIAS].join(", ")}`);
  if (!args.count) throw new Error("--count must be an integer from 1 to 100");
  return {
    command: "saved",
    query: String(args.query || "").trim(),
    limit: args.count,
    outDir: assertSafeOutDir(args.outDir || defaultOut(home), resolve),
    media: args.media,
    keepBrowser: Boolean(args.keepBrowser),
    taskName: String(args.taskName || `instagram-saved-${now}`),
    maxVideoBytes: args.maxVideoBytes || DEFAULT_MAX_VIDEO_BYTES,
    maxPages: args.maxPages || MAX_PAGES,
  };
}

export function interpretSession(flags = {}) {
  const url = flags.url || "";
  const loginUrl = /instagram\.com\/accounts\/login/i.test(url);
  const password = Boolean(flags.password || flags.username);
  // A /saved link exists on the logged-out Saved URL too. Inbox or ds_user_id means a session.
  const chrome = Boolean(flags.inbox || flags.dsUser);
  const loggedIn = !loginUrl && !password && chrome;
  return {
    url,
    title: flags.title || "",
    password,
    username: Boolean(flags.username),
    inbox: Boolean(flags.inbox),
    saved: Boolean(flags.saved),
    dsUser: Boolean(flags.dsUser),
    loginUrl,
    loggedIn,
  };
}

export function savedPath(maxId) {
  if (!maxId) return "/api/v1/feed/saved/posts/";
  return `/api/v1/feed/saved/posts/?max_id=${encodeURIComponent(maxId)}`;
}

export function assertCdn(raw) {
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new Error(`Invalid media URL: ${raw}`);
  }
  const host = url.hostname;
  const allowed = host === "cdninstagram.com" || host.endsWith(".cdninstagram.com") || host === "fbcdn.net" || host.endsWith(".fbcdn.net");
  if (url.protocol !== "https:" || !allowed) throw new Error(`Only https Instagram CDN URLs are allowed: ${raw}`);
  return url;
}

export function sniffImage(buf) {
  if (!buf || buf.length < 12) return null;
  if (buf[0] === 0xff && buf[1] === 0xd8) return "image/jpeg";
  if (buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47) return "image/png";
  if (buf.slice(0, 3).toString("ascii") === "GIF") return "image/gif";
  if (buf.slice(0, 4).toString("ascii") === "RIFF" && buf.slice(8, 12).toString("ascii") === "WEBP") return "image/webp";
  return null;
}

export function sniffVideo(buf) {
  return Boolean(buf && buf.length >= 12 && buf.slice(4, 8).toString("ascii") === "ftyp");
}

export const EXT = {
  "image/jpeg": "jpg",
  "image/png": "png",
  "image/gif": "gif",
  "image/webp": "webp",
  "video/mp4": "mp4",
};

function rankedUrls(list, urlKey = "url") {
  return [...(list || [])]
    .filter((item) => item?.[urlKey])
    .sort((a, b) => (b.width || 0) - (a.width || 0))
    .map((item) => item[urlKey]);
}

export function imageAttempts(slide) {
  const urls = rankedUrls(slide?.image_versions2?.candidates);
  for (const extra of slide?.display_resources || []) if (extra?.src) urls.push(extra.src);
  if (slide?.display_url) urls.push(slide.display_url);
  return [...new Set(urls)];
}

export function videoAttempts(slide) {
  const urls = rankedUrls(slide?.video_versions);
  if (typeof slide?.video_url === "string") urls.push(slide.video_url);
  return [...new Set(urls)];
}

export function normalizeSavedItem(raw) {
  const media = raw?.media && typeof raw.media === "object" ? raw.media : raw;
  if (!media || typeof media !== "object" || Array.isArray(media)) return null;
  const slides = Array.isArray(media.carousel_media) && media.carousel_media.length ? media.carousel_media : [media];
  const images = [];
  const videos = [];
  for (const slide of slides) {
    const urls = imageAttempts(slide);
    if (urls.length) {
      const top = slide?.image_versions2?.candidates?.slice().sort((a, b) => (b.width || 0) - (a.width || 0))[0];
      images.push(strip({ urls, width: top?.width, height: top?.height }));
    }
    const vurls = videoAttempts(slide);
    if (vurls.length) videos.push({ urls: vurls });
  }
  if (!images.length && !videos.length) return null;
  const code = media.code || media.shortcode;
  const caption = String(media.caption?.text || media.accessibility_caption || "").trim();
  return strip({
    id: media.pk || media.id ? String(media.pk || media.id) : undefined,
    code,
    permalink: code ? `${BASE}/p/${code}/` : undefined,
    username: media.user?.username || media.owner?.username,
    caption: caption ? caption.slice(0, 180) : undefined,
    media_type: media.media_type,
    images: images.slice(0, MAX_SLIDES),
    videos: videos.slice(0, MAX_SLIDES),
  });
}

export function matchesQuery(post, query) {
  const needle = String(query || "").trim().toLowerCase();
  if (!needle) return true;
  const hay = [post?.caption, post?.username, post?.code].filter(Boolean).join("\n").toLowerCase();
  return hay.includes(needle);
}

export function acceptPost(post, media) {
  const hasImage = (post?.images || []).length > 0;
  const hasVideo = (post?.videos || []).length > 0;
  if (media === "video") return hasVideo;
  if (media === "image") return hasImage;
  return hasImage || hasVideo;
}

export function filesForPost(post, media) {
  const files = [];
  if (media !== "video") {
    for (const image of (post.images || []).slice(0, MAX_SLIDES)) files.push({ kind: "image", urls: image.urls, width: image.width, height: image.height });
  }
  if (media !== "image") {
    for (const video of (post.videos || []).slice(0, MAX_SLIDES)) files.push({ kind: "video", urls: video.urls });
  }
  return files;
}

export function readBody(body) {
  if (typeof body === "string") return JSON.parse(body);
  return body;
}

export function parseSavedResponse(response) {
  if (typeof response?.body === "string" && response.body.trim().startsWith("<")) {
    return {
      error: "Instagram returned HTML instead of the Saved feed",
      posts: [],
      nextMaxId: undefined,
      loginRequired: true,
    };
  }
  if (!response || response.ok === false) {
    return { error: `HTTP ${response?.status || "error"}`, posts: [], nextMaxId: undefined, loginRequired: response?.status === 401 };
  }
  let body;
  try {
    body = readBody(response.body);
  } catch {
    return { error: "Instagram returned non-JSON", posts: [], nextMaxId: undefined, loginRequired: false };
  }
  const message = String(body?.message || "");
  if (body?.require_login || message === "login_required" || (/login/i.test(message) && body?.status === "fail")) {
    return { error: message || "login_required", posts: [], nextMaxId: undefined, loginRequired: true };
  }
  const rawItems = body?.items || [];
  const posts = [];
  for (const item of rawItems) {
    const post = normalizeSavedItem(item);
    if (post) posts.push(post);
  }
  const nextMaxId = body?.more_available === false ? undefined : body?.next_max_id || undefined;
  return { error: null, posts, nextMaxId, loginRequired: false };
}

export function outputName(postIndex, slideIndex, code, ext) {
  const base = String(code || "saved").replace(/[^a-zA-Z0-9._-]+/g, "").slice(0, 40) || "saved";
  const slide = slideIndex > 0 ? `_s${String(slideIndex + 1).padStart(2, "0")}` : "";
  return `${String(postIndex + 1).padStart(2, "0")}_${base}${slide}.${ext}`;
}

export function readSummary(text) {
  const markers = [`"skill":"${SKILL}"`, `"skill": "${SKILL}"`];
  const at = markers.map((marker) => text.indexOf(marker)).find((index) => index >= 0);
  if (at === undefined || at < 0) return null;
  const start = text.lastIndexOf("{", at);
  if (start < 0) return null;
  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let i = start; i < text.length; i++) {
    const char = text[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (char === "\\") escaped = true;
      else if (char === '"') inString = false;
      continue;
    }
    if (char === '"') inString = true;
    else if (char === "{") depth++;
    else if (char === "}") {
      depth--;
      if (depth === 0) {
        try {
          return JSON.parse(text.slice(start, i + 1));
        } catch {
          return null;
        }
      }
    }
  }
  return null;
}

export function exitCodeFor(summary, reported) {
  if (summary?.ok) return 0;
  if (summary?.login_required) return 2;
  if (summary) return summary.exitCode || 1;
  if (reported !== null && reported !== undefined) return reported;
  return 1;
}

export function attachLoginCopy(summary) {
  summary.login_tip = LOGIN_TIP;
  summary.login_tip_zh = LOGIN_TIP_ZH;
  return summary;
}

export function loginRequiredSummary(summary) {
  summary.login_required = true;
  summary.ok = false;
  summary.exitCode = 2;
  summary.error = "Instagram is not logged in inside this Ego Lite profile. Sign in once, then re-run. No password was entered.";
  summary.how_to_login = HOW_TO_LOGIN;
  summary.how_to_login_zh = HOW_TO_LOGIN_ZH;
  return attachLoginCopy(summary);
}

export function domPosts(urls) {
  const posts = [];
  const seen = new Set();
  for (const url of urls || []) {
    if (!url || seen.has(url)) continue;
    seen.add(url);
    try {
      assertCdn(url);
    } catch {
      continue;
    }
    posts.push({ images: [{ urls: [url] }], videos: [], source: "dom" });
  }
  return posts;
}

export function readFetchHead(response, maxBytes) {
  const type = String(response.headers?.get?.("content-type") || "").split(";")[0];
  const len = Number(response.headers?.get?.("content-length") || 0);
  if (maxBytes && len > maxBytes) {
    return { ok: false, status: response.status, type, buf: Buffer.alloc(0), error: `larger than ${maxBytes} bytes` };
  }
  return { type, len, error: null };
}

export async function bufferFetchResponse(response, maxBytes) {
  const head = readFetchHead(response, maxBytes);
  if (head.error) return head;
  const buf = Buffer.from(await response.arrayBuffer());
  if (maxBytes && buf.length > maxBytes) {
    return { ok: false, status: response.status, type: head.type, buf: Buffer.alloc(0), error: `larger than ${maxBytes} bytes` };
  }
  return {
    ok: response.ok,
    status: response.status,
    type: head.type,
    buf,
    error: response.ok ? null : `HTTP ${response.status}`,
  };
}
