// Pure Pinterest helpers. No browser, no process.exit.
// Resource shapes follow the public pinterest.com JSON endpoints
// (same surface as @sunkimkk/pinterest-mcp): search, related, board, pin, download, preview.

export const BASE = "https://www.pinterest.com";
export const UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36";
export const SIZES = new Set(["originals", "736x", "474x", "236x"]);
export const MEDIAS = new Set(["image", "video", "any"]);
export const COMMANDS = new Set(["search", "related", "board", "pin", "preview", "download"]);
export const MAX_PAGES = 4;
export const MAX_PREVIEWS = 8;
export const MAX_PREVIEW_BYTES = 120_000;
export const DEFAULT_MAX_VIDEO_BYTES = 200 * 1024 * 1024;
const MP4_KEYS = ["V_720P", "V_EXP7", "V_EXP6", "V_EXP5", "V_EXP4", "V_EXP3"];

export const HOW_TO_LOGIN = [
  "Open the Ego Lite app and use the same profile ego-browser drives.",
  "Go to https://www.pinterest.com/login/ and sign in once. Do not automate the password.",
  "Leave that profile logged in. Cookies stay in Ego for later ego-browser runs.",
  "Re-run this skill without --allow-anonymous.",
  "Optional: if Chrome is already signed in, import that profile (ego-browser import --browser chrome --profile Default) and confirm Pinterest in the Ego window.",
];

export const HOW_TO_LOGIN_ZH = [
  "打开 Ego Lite，使用 ego-browser 正在驱动的同一个配置档。",
  "访问 https://www.pinterest.com/login/ 手动登录一次。不要自动填写密码。",
  "保持该配置档处于登录状态，Cookie 会留给之后的 ego-browser 任务。",
  "去掉 --allow-anonymous 后重新运行本技能。",
  "可选：若 Chrome 已登录 Pinterest，可执行 ego-browser import --browser chrome --profile Default，再在 Ego 窗口里确认已登录。",
];

export const LOGIN_TIP =
  "Tell the user: signing in to Pinterest inside Ego Lite improves results compared with anonymous mode. Logged-in results include real numeric pin ids, related pins, and boards the account can open. Anonymous mode still returns public images, but ids are often obfuscated (e1_…) and related or board lookups are weaker.";

export const LOGIN_TIP_ZH =
  "请告诉用户：在 Ego Lite 里登录 Pinterest，结果会好于匿名模式。登录后能拿到真实数字 pin id、相关推荐，以及该账号能打开的画板。匿名模式仍可下载公开图片，但 id 常是 e1_…，相关推荐和画板会更弱。";

export const USAGE = `pinterest-download — Pinterest via the Ego Lite session

ego-browser nodejs does not forward shell argv. This CLI inlines the config and runs ego-browser.

  node skills/pinterest-download/scripts/download.mjs --query wallpaper --count 2 --out /tmp/pins
  node skills/pinterest-download/scripts/download.mjs search --query wallpaper --count 2 --out /tmp/pins --previews 2
  node skills/pinterest-download/scripts/download.mjs related --pin 123456789 --count 4 --out /tmp/pins
  node skills/pinterest-download/scripts/download.mjs board --board https://www.pinterest.com/user/board/ --count 4 --out /tmp/pins
  node skills/pinterest-download/scripts/download.mjs pin --pin https://www.pinterest.com/pin/123456789/
  node skills/pinterest-download/scripts/download.mjs preview --url https://i.pinimg.com/originals/aa/bb/cc/x.jpg
  node skills/pinterest-download/scripts/download.mjs download --url https://i.pinimg.com/... --url https://v.pinimg.com/...mp4 --out /tmp/pins

Options:
  --query, --keyword     Search text (search)
  --pin                  Pin id or URL (related, pin)
  --board                Board URL or /user/slug/ (board)
  --url                  Image or video URL; repeatable (preview, download)
  --count, --limit       How many pins to save (1-100, default 10)
  --out, --out-dir       Output directory (default ~/Downloads/pinterest-ego)
  --size                 originals | 736x | 474x | 236x
  --min-width            Skip pins narrower than this many pixels (0 or omit = no floor)
  --min-height           Skip pins shorter than this many pixels (0 or omit = no floor)
  --media                image | video | any
  --previews             Embed up to 8 small thumbnails (base64) for the model
  --bookmark             Continue a previous resource page
  --keep                 Leave the Pinterest tab open
  --allow-anonymous      Run logged out (default: soft-fail, exit 2)
  --task-name            Ego task space name

Logged-out runs exit 2 with how_to_login. Every result includes login_tip: tell the user that an Ego login improves results.

Resolution: set one of --min-width / --min-height to enforce that side. Set both and the pin must be known on both sides and at least those sizes. Video saves use video_width / video_height when present, otherwise the cover image size. Pins with an unknown required side are skipped. Direct download --url targets are not filtered. Skips are listed on skipped[].
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

export function clampPreviews(value) {
  if (value === undefined || value === null || value === "") return 0;
  const n = Number(value);
  if (!Number.isFinite(n)) return null;
  const i = Math.floor(n);
  if (i < 0 || i > MAX_PREVIEWS) return null;
  return i;
}

export function clampPixels(value) {
  if (value === undefined || value === null || value === "") return 0;
  if (!/^\d+$/.test(String(value).trim())) return null;
  const n = Number(value);
  if (!Number.isSafeInteger(n)) return null;
  return n;
}

export function defaultOut(home = process.env.HOME || "/tmp") {
  return `${home.replace(/\/$/, "")}/Downloads/pinterest-ego`;
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
    command: "search",
    query: "",
    pin: "",
    board: "",
    urls: [],
    count: null,
    outDir: "",
    size: "originals",
    media: "image",
    previews: null,
    bookmark: "",
    keepBrowser: false,
    allowAnonymous: false,
    taskName: "",
    minWidth: 0,
    minHeight: 0,
    help: false,
  };
  let args = [...argv];
  if (args[0] && COMMANDS.has(args[0])) {
    out.command = args[0];
    args = args.slice(1);
  }
  const positionals = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--help" || arg === "-h") out.help = true;
    else if (arg === "--query" || arg === "--keyword") out.query = take(args, ++i, arg);
    else if (arg === "--pin") out.pin = take(args, ++i, arg);
    else if (arg === "--board") out.board = take(args, ++i, arg);
    else if (arg === "--url") out.urls.push(take(args, ++i, arg));
    else if (arg === "--count" || arg === "--limit") {
      const parsed = clampCount(take(args, ++i, arg));
      if (parsed === null) throw new Error("--count must be an integer from 1 to 100");
      out.count = parsed;
    }
    else if (arg === "--out" || arg === "--out-dir" || arg === "--outdir" || arg === "--dir") out.outDir = take(args, ++i, arg);
    else if (arg === "--size") out.size = take(args, ++i, arg);
    else if (arg === "--min-width") {
      const parsed = clampPixels(take(args, ++i, arg));
      if (parsed === null) throw new Error("--min-width must be a non-negative integer (pixels)");
      out.minWidth = parsed;
    }
    else if (arg === "--min-height") {
      const parsed = clampPixels(take(args, ++i, arg));
      if (parsed === null) throw new Error("--min-height must be a non-negative integer (pixels)");
      out.minHeight = parsed;
    }
    else if (arg === "--media") out.media = take(args, ++i, arg);
    else if (arg === "--previews") {
      const parsed = clampPreviews(take(args, ++i, arg));
      if (parsed === null) throw new Error(`--previews must be an integer from 0 to ${MAX_PREVIEWS}`);
      out.previews = parsed;
    }
    else if (arg === "--bookmark") out.bookmark = take(args, ++i, arg);
    else if (arg === "--task-name") out.taskName = take(args, ++i, arg);
    else if (arg === "--keep") out.keepBrowser = true;
    else if (arg === "--allow-anonymous") out.allowAnonymous = true;
    else if (arg.startsWith("-")) throw new Error(`Unknown option ${arg}`);
    else positionals.push(arg);
  }
  const positionalCount = (value) => {
    const parsed = clampCount(value);
    if (parsed === null) throw new Error("--count must be an integer from 1 to 100");
    return parsed;
  };
  if (out.command === "search") {
    if (!out.query && positionals[0]) out.query = positionals[0];
    if (out.count === null && positionals[1] !== undefined) out.count = positionalCount(positionals[1]);
    if (!out.outDir && positionals[2]) out.outDir = positionals[2];
  } else if (out.command === "related" || out.command === "pin") {
    if (!out.pin && positionals[0]) out.pin = positionals[0];
    if (out.count === null && positionals[1] !== undefined) out.count = positionalCount(positionals[1]);
    if (!out.outDir && positionals[2]) out.outDir = positionals[2];
  } else if (out.command === "board") {
    if (!out.board && positionals[0]) out.board = positionals[0];
    if (out.count === null && positionals[1] !== undefined) out.count = positionalCount(positionals[1]);
    if (!out.outDir && positionals[2]) out.outDir = positionals[2];
  } else if (!out.urls.length) {
    out.urls.push(...positionals);
  }
  if (out.count === null) out.count = out.command === "preview" || out.command === "download" ? Math.max(out.urls.length, 1) : 10;
  if (out.previews === null) out.previews = 0;
  return out;
}

export function toConfig(args, { resolve = (value) => value, home, now = Date.now() } = {}) {
  if (!SIZES.has(args.size)) throw new Error(`--size must be one of: ${[...SIZES].join(", ")}`);
  if (!MEDIAS.has(args.media)) throw new Error(`--media must be one of: ${[...MEDIAS].join(", ")}`);
  if (!args.count) throw new Error("--count must be an integer from 1 to 100");
  if (args.previews === null) throw new Error(`--previews must be an integer from 0 to ${MAX_PREVIEWS}`);
  const command = args.command || "search";
  if (!COMMANDS.has(command)) throw new Error(`Unknown command ${command}`);
  if (command === "search" && !String(args.query || "").trim()) throw new Error("query is required (--query wallpaper)");
  if ((command === "related" || command === "pin") && !String(args.pin || "").trim()) {
    throw new Error("--pin is required");
  }
  if (command === "board" && !String(args.board || "").trim()) throw new Error("--board is required");
  if ((command === "preview" || command === "download") && !(args.urls || []).length) {
    throw new Error("--url is required");
  }
  return {
    command,
    query: String(args.query || "").trim(),
    pin: String(args.pin || "").trim(),
    board: String(args.board || "").trim(),
    urls: [...(args.urls || [])],
    limit: args.count,
    outDir: assertSafeOutDir(args.outDir || defaultOut(home), resolve),
    size: args.size,
    media: args.media,
    previews: args.previews,
    bookmark: String(args.bookmark || ""),
    keepBrowser: Boolean(args.keepBrowser),
    allowAnonymous: Boolean(args.allowAnonymous),
    taskName: String(args.taskName || `pinterest-download-${now}`),
    minWidth: clampPixels(args.minWidth) || 0,
    minHeight: clampPixels(args.minHeight) || 0,
    maxVideoBytes: args.maxVideoBytes || DEFAULT_MAX_VIDEO_BYTES,
    maxPages: args.maxPages || MAX_PAGES,
  };
}

export function pickImage(images, ...keys) {
  for (const key of keys) if (images?.[key]?.url) return images[key];
  return undefined;
}

const IHT_MP4_WIDTHS = ["720w", "540w", "360w", "240w"];
const IHT_CMFV_WIDTHS = ["720w", "540w", "360w"];

// iht HLS is a byte-range playlist. The single progressive file (video + audio, ftyp isom)
// lives at /videos/iht/expMp4/<id>_<width>w.mp4. /videos/iht/720p/<id>.mp4 is access-denied.
// The *_720w.cmfv sibling is the video-only CMAF track, kept as a fallback.
export function ihtVideoId(url) {
  const path = String(url || "").split("?")[0];
  const match = path.match(/^(https:\/\/[^/]+)\/videos\/iht\/(?:hls|expMp4|720p|mp4)\/(.+)$/i);
  if (!match) return null;
  let id = match[2];
  id = id.replace(/_\d+w\.(?:m3u8|cmfv|cmfa|mp4)$/i, "");
  id = id.replace(/\.(m3u8|cmfv|cmfa|mp4)$/i, "");
  if (!id) return null;
  return { origin: match[1], id };
}

export function hlsDerivedMp4(url) {
  if (!url) return undefined;
  const iht = ihtVideoId(url);
  if (iht) return `${iht.origin}/videos/iht/expMp4/${iht.id}_720w.mp4`;
  const derived = String(url).replace(/\/videos\/mc\/hls\/(.+)\.m3u8(?:\?.*)?$/, "/videos/mc/720p/$1.mp4");
  return derived === url ? undefined : derived;
}

export function pickVideo(pin) {
  const lists = [];
  if (pin?.videos?.video_list) lists.push(pin.videos.video_list);
  for (const page of pin?.story_pin_data?.pages || []) {
    for (const block of page?.blocks || []) {
      if (block?.video?.video_list) lists.push(block.video.video_list);
    }
  }
  const all = [];
  for (const list of lists) {
    for (const [key, value] of Object.entries(list || {})) {
      if (value?.url) all.push({ key, ...value });
    }
  }
  if (!all.length) return undefined;
  const mp4 =
    MP4_KEYS.map((key) => all.find((item) => item.key === key)).find(Boolean) ||
    all.find((item) => /\.mp4($|\?)/i.test(item.url));
  const hls = all.find((item) => /\.m3u8($|\?)/i.test(item.url));
  const derived = hls ? hlsDerivedMp4(hls.url) : undefined;
  const best = mp4 || hls;
  if (!best) return undefined;
  return strip({
    video_url: mp4?.url || derived || hls?.url,
    video_hls: hls?.url,
    video_width: best.width,
    video_height: best.height,
    video_seconds: best.duration ? Math.round(best.duration / 1000) : undefined,
  });
}

export function isVideoPin(pin) {
  return Boolean(pickVideo(pin)?.video_url);
}

export function normalizePin(raw) {
  if (!raw || raw.is_promoted) return null;
  if (raw.type && raw.type !== "pin") return null;
  const image = pickImage(raw.images, "orig", "736x", "564x", "474x", "236x");
  if (!image?.url) return null;
  const numeric = /^\d+$/.test(String(raw.id));
  const video = pickVideo(raw);
  return strip({
    id: numeric ? String(raw.id) : undefined,
    pin_url: numeric ? `${BASE}/pin/${raw.id}/` : undefined,
    title: String(raw.title || raw.grid_title || "").trim().slice(0, 140) || undefined,
    description: String(raw.description || "").trim().slice(0, 180) || undefined,
    image_url: image.url,
    width: image.width,
    height: image.height,
    low_res: Number(image.width) > 0 && Number(image.width) < 500 ? true : undefined,
    dominant_color: raw.dominant_color || undefined,
    is_video: video?.video_url ? true : undefined,
    ...(video || {}),
  });
}

export function acceptMedia(pin, media) {
  const video = Boolean(pin?.video_url || pin?.is_video);
  if (media === "video") return video;
  if (media === "image") return !video;
  return true;
}

export function mediaDimensions(pin, kind = "image") {
  const imageW = Number(pin?.width) || 0;
  const imageH = Number(pin?.height) || 0;
  if (kind === "video") {
    return {
      width: Number(pin?.video_width) || imageW,
      height: Number(pin?.video_height) || imageH,
    };
  }
  return { width: imageW, height: imageH };
}

// ok when every requested side is known and >= its floor. 0 means that side is not checked.
// Both floors set: both sides must pass. One floor set: only that side is checked.
export function meetsMinResolution(pin, minWidth = 0, minHeight = 0, kind = "image") {
  const minW = clampPixels(minWidth) || 0;
  const minH = clampPixels(minHeight) || 0;
  const { width, height } = mediaDimensions(pin, kind);
  if (minW <= 0 && minH <= 0) return { ok: true, width, height, reason: "" };
  const reasons = [];
  if (minW > 0) {
    if (!(width > 0)) reasons.push("width unknown");
    else if (width < minW) reasons.push(`width ${width} < ${minW}`);
  }
  if (minH > 0) {
    if (!(height > 0)) reasons.push("height unknown");
    else if (height < minH) reasons.push(`height ${height} < ${minH}`);
  }
  return { ok: reasons.length === 0, width, height, reason: reasons.join("; ") };
}

export function resizeUrl(url, size) {
  const swapped = String(url).replace(/(pinimg\.com\/)(originals|\d+x\d*(?:_RS)?)\//, `$1${size}/`);
  return size === "originals" ? swapped : swapped.replace(/\.(png|gif|webp)$/i, ".jpg");
}

export function toOriginals(url) {
  if (!url || typeof url !== "string") return null;
  if (!/pinimg\.com/i.test(url)) return url;
  return url.replace(/\/\d+x\d*(?:_RS)?\//, "/originals/");
}

export function assertPinimg(raw) {
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new Error(`Invalid image URL: ${raw}`);
  }
  if (url.protocol !== "https:" || !/(^|\.)pinimg\.com$/.test(url.hostname)) {
    throw new Error(`Only https://*.pinimg.com URLs are allowed: ${raw}`);
  }
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

export function isVideoUrl(url) {
  return /\.(mp4|m3u8|cmfv)($|\?)/i.test(String(url || ""));
}

export function sizeCandidates(url, size) {
  const sizes = size === "originals" ? ["originals", "736x"] : [size, "736x", "originals"];
  return [...new Set(sizes.map((item) => resizeUrl(url, item)).concat(url))];
}

export function previewCandidates(url) {
  return [...new Set(["236x", "474x"].map((size) => resizeUrl(url, size)).concat(url))];
}

export function videoTryUrls(url) {
  const raw = String(url || "");
  const iht = ihtVideoId(raw);
  if (iht) {
    const urls = [];
    const push = (value) => {
      if (value && !urls.includes(value)) urls.push(value);
    };
    for (const width of IHT_MP4_WIDTHS) push(`${iht.origin}/videos/iht/expMp4/${iht.id}_${width}.mp4`);
    for (const width of IHT_CMFV_WIDTHS) push(`${iht.origin}/videos/iht/hls/${iht.id}_${width}.cmfv`);
    return urls;
  }
  if (/\.m3u8($|\?)/i.test(raw)) {
    const derived = hlsDerivedMp4(raw);
    return derived ? [derived] : [];
  }
  if (/_\d+w\.cmfv($|\?)/i.test(raw)) {
    return ["720w", "540w", "360w"].map((width) => raw.replace(/_\d+w\.cmfv/i, `_${width}.cmfv`));
  }
  return raw ? [raw] : [];
}

export function outputName(index, url, ext) {
  let base = "file";
  try {
    const leaf = new URL(url).pathname.split("/").filter(Boolean).pop() || "";
    base = leaf.replace(/\.[a-z0-9]+$/i, "") || base;
  } catch {
    base = "file";
  }
  base = base.replace(/[^a-zA-Z0-9._-]+/g, "").slice(0, 80) || "file";
  return `${String(index + 1).padStart(2, "0")}_${base}.${ext}`;
}

export function readFetchResponse(response, maxBytes) {
  const type = String(response.headers?.get?.("content-type") || "").split(";")[0];
  const len = Number(response.headers?.get?.("content-length") || 0);
  if (maxBytes && len > maxBytes) {
    return { ok: false, status: response.status, type, buf: Buffer.alloc(0), error: `larger than ${maxBytes} bytes` };
  }
  return { type, len };
}

export async function bufferFetchResponse(response, maxBytes) {
  const head = readFetchResponse(response, maxBytes);
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

export function previewPayload(buf, maxBytes = MAX_PREVIEW_BYTES) {
  const sniffed = sniffImage(buf);
  if (!sniffed) throw new Error("not an image");
  if (buf.length > maxBytes) throw new Error("preview too large");
  if (buf.length < 100) throw new Error("preview too small");
  return { mimeType: sniffed, data: buf.toString("base64"), bytes: buf.length };
}

export function readBody(body) {
  if (typeof body === "string") return JSON.parse(body);
  return body;
}

export function resourceItems(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
}

export function parseResourceResponse(response) {
  if (!response || response.ok === false) {
    return { error: `HTTP ${response?.status || "error"}`, items: [], bookmark: undefined, data: null };
  }
  let body;
  try {
    body = readBody(response.body);
  } catch {
    return { error: "Pinterest returned non-JSON", items: [], bookmark: undefined, data: null };
  }
  const resource = body?.resource_response || {};
  if ((Number(resource.http_status) || 0) >= 400 || resource.status === "failure") {
    return {
      error: `Pinterest ${resource.http_status || resource.status}`,
      items: [],
      bookmark: undefined,
      data: resource.data || null,
    };
  }
  const bookmark = resource.bookmark && resource.bookmark !== "-end-" ? resource.bookmark : undefined;
  return { error: null, items: resourceItems(resource.data), bookmark, data: resource.data ?? null };
}

export function resourcePath(request, now = Date.now()) {
  const qs = new URLSearchParams({
    source_url: request.sourceUrl,
    data: JSON.stringify({ options: request.options, context: {} }),
    _: String(now),
  });
  return `/resource/${request.name}/get/?${qs}`;
}

export function searchRequest(query, bookmark) {
  const sourceUrl = `/search/pins/?q=${encodeURIComponent(query)}&rs=typed`;
  const options = { query, scope: "pins", rs: "typed", redux_normalize_feed: true };
  if (bookmark) options.bookmarks = [bookmark];
  return { name: "BaseSearchResource", sourceUrl, handler: "www/search/[scope].js", options };
}

export function relatedRequest(id, bookmark) {
  const options = {
    pin_id: String(id),
    context_pin_ids: [],
    search_query: "",
    source: "deep_linking",
    top_level_source: "deep_linking",
    top_level_source_depth: 1,
    is_pdp: false,
  };
  if (bookmark) options.bookmarks = [bookmark];
  return {
    name: "RelatedModulesResource",
    sourceUrl: `/pin/${id}/`,
    handler: "www/pin/[id].js",
    options,
  };
}

export function pinRequest(id) {
  return {
    name: "PinResource",
    sourceUrl: `/pin/${id}/`,
    handler: "www/pin/[id].js",
    options: { id: String(id), field_set_key: "detailed" },
  };
}

export function boardRequest(username, slug) {
  const path = `/${username}/${slug}/`;
  return {
    name: "BoardResource",
    sourceUrl: path,
    handler: "www/[username]/[slug].js",
    options: { username, slug, field_set_key: "detailed" },
  };
}

export function boardFeedRequest(boardId, boardPath, bookmark) {
  const options = {
    board_id: String(boardId),
    board_url: boardPath,
    page_size: 25,
    field_set_key: "react_grid_pin",
  };
  if (bookmark) options.bookmarks = [bookmark];
  return {
    name: "BoardFeedResource",
    sourceUrl: boardPath,
    handler: "www/[username]/[slug].js",
    options,
  };
}

export function parseBoard(input) {
  const raw = String(input || "").trim();
  if (!raw) throw new Error("board url is required");
  let pathname = raw;
  if (/^https?:\/\//.test(raw) || /pinterest\./.test(raw)) {
    const url = new URL(/^https?:\/\//.test(raw) ? raw : `https://${raw}`);
    pathname = url.pathname;
  }
  const parts = pathname.split("/").filter(Boolean).map((part) => decodeURIComponent(part));
  if (parts.length < 2) throw new Error(`Expected a board URL like pinterest.com/<user>/<board>/, got: ${input}`);
  return { username: parts[0], slug: parts[1], path: `/${parts[0]}/${parts[1]}/` };
}

export function pinIdFromInput(input) {
  const value = String(input || "").trim();
  if (!value) return { error: "pin id or url is required" };
  if (/^e1_/.test(value)) {
    return {
      error:
        "Anonymous id e1_… cannot be opened. Pass a numeric pin id or a pinterest.com/pin/ URL. Logging in to Pinterest in Ego Lite returns numeric ids.",
    };
  }
  if (/^\d+$/.test(value)) return { id: value };
  let url;
  try {
    url = new URL(/^https?:\/\//.test(value) ? value : `https://${value}`);
  } catch {
    return { error: `Not a pin id or pin URL: ${value}` };
  }
  if (url.hostname === "pin.it") return { redirect: url.href };
  const match = url.pathname.match(/\/pin\/(?:[^/]*--)?(\d+)/);
  if (!match) return { error: `Could not find a pin id in ${value}` };
  return { id: match[1] };
}

export function interpretSession(flags = {}) {
  const loginUrl = /pinterest\.[^/]+\/(login|signup)\b/i.test(flags.url || "");
  const loggedIn = !flags.unauth && !loginUrl && Boolean(flags.profile || flags.authCookie);
  return {
    url: flags.url || "",
    title: flags.title || "",
    unauth: Boolean(flags.unauth),
    profile: Boolean(flags.profile),
    authCookie: Boolean(flags.authCookie),
    loginUrl,
    loggedIn,
  };
}

export function foldDomUrls(urls, limit) {
  const pins = [];
  const seen = new Set();
  for (const url of urls || []) {
    if (pins.length >= limit) break;
    const imageUrl = toOriginals(url) || url;
    if (!imageUrl || seen.has(imageUrl)) continue;
    seen.add(imageUrl);
    pins.push({ image_url: imageUrl, source: "dom" });
  }
  return pins;
}

export function readSummary(text) {
  const marker = '"skill":"pinterest-download"';
  const pretty = '"skill": "pinterest-download"';
  const at = text.indexOf(marker) >= 0 ? text.indexOf(marker) : text.indexOf(pretty);
  if (at < 0) return null;
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
  summary.error = "Pinterest is not logged in inside this Ego Lite profile. Sign in once, then re-run. No password was entered.";
  summary.how_to_login = HOW_TO_LOGIN;
  summary.how_to_login_zh = HOW_TO_LOGIN_ZH;
  return attachLoginCopy(summary);
}
