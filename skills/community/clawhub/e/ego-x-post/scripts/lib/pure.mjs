// Pure helpers for x-post. No browser, no process.exit.
// CreateTweet and CreateNoteTweet match the 2026-11-04 Ego captures
// (main.0a76dc3677efe2b2a.js). Do not add other operation query ids here.

import { MAX_IMAGES, mediaTypeForName } from "./media.mjs";

export const SKILL = "x-post";
export const HOME_URL = "https://x.com/home";
export const COMPOSE_URL = "https://x.com/compose/post";
export const SPACE_NAME = "x-post";
export const LOGIN_TASK = "x-post-login-check";
export const RESULT_TAG = "XPOST";
export const STANDARD_POST_CHARS = 280;
export const MAX_TEXT_CHARS = 25000;

// Captured 2026-11-04 from the live web client. Re-read the loaded bundle first.
export const CAPTURED_CREATE_TWEET_QUERY_ID = "l4hk8uVGvR-a8kzQ4nOhPA";
export const CAPTURED_CREATE_NOTE_TWEET_QUERY_ID = "seOZkIS8AysCGfPo6yYPVA";
export const CAPTURED_QUERY_SOURCE = "captured-2026-11-04";
export const CAPTURED_NOTE_QUERY_SOURCE = "captured-note-2026-11-04";
export const MAX_WEIGHTED_TWEET_LENGTH = 280;

// Public web-client bearer (prefix AAAA…ANRILg…), not a user secret.
// Prefer the value read from the loaded bundle. Never print it beside ct0.
export const PUBLIC_WEB_BEARER =
  "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA";

export const SMOKE_TEXT =
  "ego-skills x-post: post on X from a logged-in Ego Lite session (page.fetch CreateTweet). Login-check first. Nothing sends without --yes. https://github.com/terryso/ego-skills";

// Feature flags copied from the verified CreateTweet UI body. Do not add keys.
export const CAPTURED_FEATURES = {
  premium_content_api_read_enabled: false,
  communities_web_enable_tweet_community_results_fetch: true,
  c9s_tweet_anatomy_moderator_badge_enabled: true,
  responsive_web_grok_analyze_button_fetch_trends_enabled: false,
  responsive_web_grok_analyze_post_followups_enabled: true,
  rweb_cashtags_composer_attachment_enabled: true,
  responsive_web_jetfuel_frame: true,
  rweb_sports_post_context_enabled: true,
  x_elections_post_context_enabled: true,
  responsive_web_grok_share_attachment_enabled: true,
  responsive_web_grok_annotations_enabled: true,
  responsive_web_edit_tweet_api_enabled: true,
  rweb_conversational_replies_downvote_enabled: false,
  graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
  view_counts_everywhere_api_enabled: true,
  longform_notetweets_consumption_enabled: true,
  responsive_web_twitter_article_tweet_consumption_enabled: true,
  content_disclosure_indicator_enabled: true,
  content_disclosure_ai_generated_indicator_enabled: true,
  responsive_web_grok_show_grok_translated_post: true,
  responsive_web_grok_analysis_button_from_backend: true,
  post_ctas_fetch_enabled: false,
  longform_notetweets_rich_text_read_enabled: true,
  longform_notetweets_inline_media_enabled: false,
  profile_label_improvements_pcf_label_in_post_enabled: true,
  responsive_web_profile_redirect_enabled: true,
  rweb_tipjar_consumption_enabled: false,
  verified_phone_label_enabled: false,
  responsive_web_nested_quote_preview_enabled: true,
  articles_preview_enabled: true,
  rweb_cashtags_enabled: true,
  responsive_web_grok_community_note_auto_translation_is_enabled: true,
  freedom_of_speech_not_reach_fetch_enabled: true,
  standardized_nudges_misinfo: true,
  tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
  responsive_web_grok_image_annotation_enabled: true,
  responsive_web_grok_imagine_annotation_enabled: true,
  responsive_web_made_on_x_label_enabled: false,
  responsive_web_graphql_timeline_navigation_enabled: true,
};

const RESERVED_SCREEN_NAMES = new Set([
  "home", "explore", "search", "compose", "settings", "messages", "notifications",
  "i", "intent", "share", "login", "signup", "tos", "privacy", "hashtag",
]);

export const HOW_TO_LOGIN = [
  "Install Ego Lite and put ego-browser on PATH (often ~/.local/bin). Open the Ego Lite app.",
  "Visit https://x.com/home and sign in to the X account that should post.",
  "Leave that x.com session signed in inside Ego. Do not paste cookies or a bearer token.",
  "Re-run this skill's login-check. Post only after exit 0, and only with --yes after the draft is shown.",
  "Sessions expire. Login-check before posting. Never type a password.",
];

export const HOW_TO_LOGIN_ZH = [
  "先安装 Ego Lite，并把 ego-browser 放进 PATH（常见 ~/.local/bin）。打开 Ego Lite。",
  "访问 https://x.com/home ，登录要发帖的 X 账号。",
  "保持 Ego 里的 x.com 为登录状态。不要粘贴 Cookie，也不要粘贴 bearer。",
  "重新跑 login-check。只有退出码 0 之后才发帖，而且要先给人看草稿，确认后再加 --yes。",
  "登录态会过期。每次发帖前都要先检查。不要代填密码。",
];

export const LOGIN_TIP =
  "Tell the user: sign in to x.com inside Ego Lite before posting. Posts use the browser session (page.fetch CreateTweet), not an X API key. If login-check exits 2, ask them to open Ego Lite, sign in, then re-run. Show the draft and wait for confirmation before --yes. Never type a password or paste cookies.";

export const LOGIN_TIP_ZH =
  "请告诉用户：在 Ego Lite 里登录 x.com 之后才能发帖。发帖走浏览器会话的 page.fetch CreateTweet，不用 X API key。若 login-check 退出码是 2，请人在 Ego Lite 打开 x.com 登录后再跑。先展示草稿，等人确认后再加 --yes。不要代填密码，不要粘贴 Cookie。";

export const USAGE = `x-post — post on X via the logged-in Ego Lite session (page.fetch CreateTweet, or CreateNoteTweet when the weighted length is over 280)

Install Ego Lite and put ego-browser on PATH first. Missing ego-browser soft-fails (exit 2).
Nothing is sent without --yes. Show the draft to the user first.
--image is repeatable (up to 4 png/jpeg/webp, each <= 5 MiB). GIF is rejected.
Without --yes the draft lists each image's bytes and md5 and nothing is uploaded.
Reply (--reply-to) is best-effort: a live page.fetch reply returned GraphQL 226 and was not verified.

  node scripts/check-login.mjs
  node scripts/check-login.mjs --keep
  node scripts/post.mjs --text "..."
  node scripts/post.mjs --text "..." --yes [--json] [--reply-to <statusId>]
  node scripts/post.mjs --text "..." --image /absolute/path/to/image.png
  node scripts/post.mjs --text "..." --image /absolute/path/to/image.png --yes
  node scripts/cleanup.mjs

check-login exits 0 when x.com is signed in, 2 when login is required or ego-browser is missing.
post without --yes prints the draft and exits 3. post --yes prints https://x.com/<screen_name>/status/<id>.
A missing, empty, oversized, or unsupported image exits 1 before any network call.
Default finish({ keep: [] }). --keep leaves the page.
cleanup closes the x-post browser space. It does not delete a post.
`;

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function charCount(text) {
  return Array.from(String(text || "")).length;
}

export function parseCheckArgs(argv) {
  const out = { keep: false, help: false, taskName: LOGIN_TASK };
  return parseFlags(argv, out, {
    "--keep": () => { out.keep = true; },
    "--task-name": (value) => { out.taskName = value || out.taskName; },
  });
}

export function parseCleanupArgs(argv) {
  const out = { help: false, taskName: SPACE_NAME };
  return parseFlags(argv, out, {
    "--task-name": (value) => { out.taskName = value || out.taskName; },
  });
}

export function parsePostArgs(argv) {
  const out = {
    help: false,
    yes: false,
    json: false,
    keep: false,
    long: false,
    text: "",
    replyTo: "",
    queryId: "",
    transactionId: "",
    taskName: SPACE_NAME,
    images: [],
  };
  const parsed = parseFlags(argv, out, {
    "--text": (value) => { out.text = value == null ? "" : String(value); },
    "--reply-to": (value) => { out.replyTo = String(value || ""); },
    "--image": (value) => { out.images.push(String(value == null ? "" : value)); },
    "--yes": () => { out.yes = true; },
    "--json": () => { out.json = true; },
    "--keep": () => { out.keep = true; },
    "--long": () => { out.long = true; },
    "--query-id": (value) => { out.queryId = String(value || ""); },
    "--transaction-id": (value) => { out.transactionId = String(value || ""); },
    "--task-name": (value) => { out.taskName = value || out.taskName; },
  });
  if (parsed.help) return parsed;
  out.text = out.text.trim();
  out.images = out.images.map((value) => value.trim());
  if (!out.text) throw new Error("Missing --text");
  if (charCount(out.text) > MAX_TEXT_CHARS) throw new Error("--text is longer than 25000 characters");
  if (out.replyTo && !/^\d{1,25}$/.test(out.replyTo)) throw new Error("--reply-to must be a numeric status id");
  if (out.queryId && !isQueryId(out.queryId)) throw new Error("--query-id is not a web-client query id");
  if (out.images.length > MAX_IMAGES) throw new Error(`At most ${MAX_IMAGES} --image files`);
  if (out.images.some((value) => !value)) throw new Error("Missing value for --image");
  for (const image of out.images) mediaTypeForName(image);
  return out;
}

function parseFlags(argv, out, handlers) {
  const args = argv || [];
  if (args.includes("--help") || args.includes("-h")) {
    out.help = true;
    return out;
  }
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const handler = handlers[arg];
    if (!handler) throw new Error(`Unknown arg: ${arg}`);
    const takesValue = arg === "--text" || arg === "--reply-to" || arg === "--image" || arg === "--query-id" || arg === "--task-name" || arg === "--transaction-id";
    if (takesValue) {
      const value = args[i + 1];
      if (value == null || String(value).startsWith("--")) throw new Error(`Missing value for ${arg}`);
      handler(value);
      i += 1;
    } else {
      handler();
    }
  }
  return out;
}

export function draftOf({ text = "", replyTo = "", long = false, images = [] } = {}) {
  const chars = charCount(text);
  const weighted = weightedLength(text);
  const note = needsNoteTweet(text, { long });
  const media = (images || []).map((image) => {
    if (typeof image === "string") return { path: image };
    return strip({
      path: image && image.path ? image.path : "",
      bytes: image && image.bytes,
      md5: image && image.md5,
    });
  });
  return {
    text: String(text),
    reply_to: replyTo || null,
    chars,
    weighted,
    long_text: note,
    operation: note ? "CreateNoteTweet" : "CreateTweet",
    reply_best_effort: Boolean(replyTo),
    media,
  };
}

export function confirmationSummary(args) {
  return {
    skill: SKILL,
    command: "post",
    ok: false,
    sent: false,
    confirmation_required: true,
    exitCode: 3,
    draft: draftOf(args),
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    error: "Refusing to post without --yes. Show this draft to the user, then re-run with --yes only after they confirm.",
  };
}

export function formatDraftText(summary) {
  const draft = summary.draft || { text: "", chars: 0, reply_to: null };
  const lines = [
    "draft (not sent)",
    `chars: ${draft.chars}`,
    `reply_to: ${draft.reply_to || "(none)"}`,
  ];
  if (draft.reply_to) {
    lines.push("reply: best-effort; page.fetch reply was not verified (GraphQL 226 on the 2026-11-04 capture).");
  }
  if (draft.long_text) {
    lines.push(`note: weighted length ${draft.weighted ?? "?"} is over ${MAX_WEIGHTED_TWEET_LENGTH}, or --long was set. --yes sends CreateNoteTweet.`);
  }
  const media = draft.media || [];
  if (media.length) {
    lines.push("media (not uploaded):");
    for (const item of media) {
      const size = item.bytes == null ? "size unknown" : `${item.bytes} bytes`;
      const hash = item.md5 ? `, md5 ${item.md5}` : "";
      lines.push(`- ${item.path} (${size}${hash})`);
    }
  } else {
    lines.push("media: (none)");
  }
  lines.push("---", draft.text, "---", summary.error || "");
  return `${lines.join("\n")}\n`;
}

export function formatResult(summary, { asJson = false } = {}) {
  if (!summary || typeof summary !== "object") return "";
  if (!asJson && summary.exitCode === 0 && summary.sent && summary.url) return `${summary.url}\n`;
  if (!asJson && summary.confirmation_required) return formatDraftText(summary);
  return `${JSON.stringify(summary, null, 2)}\n`;
}

export function isLoginWall({ url = "", title = "", text = "" } = {}) {
  const pageUrl = String(url || "");
  if (/\/i\/flow\/(?:login|signup)|\/login(?:\b|[/?#]|$)/i.test(pageUrl)) return true;
  return /Sign in to X|Log in to X|登录 X|登入 X|Create account/.test(`${title}\n${text}`);
}

export function hasHomeTitle(title) {
  return /主页|(?:^|\s)Home(?:\s|\/|$)/.test(String(title || ""));
}

export function onHome(url) {
  try {
    const parsed = new URL(String(url || ""));
    return /^(?:www\.)?(?:x|twitter)\.com$/i.test(parsed.hostname) && /^\/home\/?$/.test(parsed.pathname);
  } catch {
    return false;
  }
}

export function isScreenName(value) {
  const name = String(value || "");
  if (!/^[A-Za-z0-9_]{1,15}$/.test(name)) return false;
  return !RESERVED_SCREEN_NAMES.has(name.toLowerCase());
}

export function screenNameFromPath(href) {
  const raw = String(href || "").trim();
  if (!raw) return "";
  let path = raw;
  if (/^https?:\/\//i.test(raw)) {
    try {
      path = new URL(raw).pathname;
    } catch {
      return "";
    }
  }
  const match = path.match(/^\/([A-Za-z0-9_]{1,15})\/?$/);
  if (!match || !isScreenName(match[1])) return "";
  return match[1];
}

export function cookieHeaderNames(header) {
  const names = [];
  for (const part of String(header || "").split(";")) {
    const name = part.split("=")[0].trim();
    if (name) names.push(name);
  }
  return names;
}

export function detectSignals({ url = "", title = "", text = "", profileHref = "", authCookie = false, csrfCookie = false, jarRead = false } = {}) {
  return {
    onLoginWall: isLoginWall({ url, title, text }),
    platformChrome: /发帖|个人资料|For you|为你推荐/.test(String(text || "")) || hasHomeTitle(title),
    authCookie: Boolean(authCookie),
    csrfCookie: Boolean(csrfCookie),
    jarRead: Boolean(jarRead),
    profileHref: profileHref || "",
  };
}

export function classifyLogin(input = {}) {
  const pageUrl = String(input.url || "");
  const wall = Boolean(input.onLoginWall) || isLoginWall(input);
  const profile = screenNameFromPath(input.profileHref);
  const chrome = Boolean(input.platformChrome) || hasHomeTitle(input.title);
  const authCookie = Boolean(input.authCookie);
  const jarRead = Boolean(input.jarRead);
  let loggedIn = false;
  if (!wall && authCookie) loggedIn = true;
  else if (!wall && !jarRead && profile && (chrome || onHome(pageUrl))) loggedIn = true;
  return strip({
    logged_in: loggedIn,
    login_required: !loggedIn,
    on_login_page: wall || undefined,
    screen_name: profile || undefined,
    url: pageUrl || undefined,
    title: input.title || undefined,
  });
}

export function needsRepaint(detected = {}) {
  if (detected.authCookie) return false;
  if (detected.onLoginWall || isLoginWall(detected)) return false;
  if (detected.platformChrome || hasHomeTitle(detected.title)) return false;
  if (screenNameFromPath(detected.profileHref)) return false;
  return true;
}

export function egoMissingSummary(command = "check-login") {
  return strip({
    skill: SKILL,
    command,
    ok: false,
    sent: false,
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

export function parseLooseJson(text) {
  if (text == null || text === "") return null;
  const source = String(text);
  try {
    return JSON.parse(source);
  } catch {
    // X occasionally returns unescaped control characters.
  }
  try {
    return JSON.parse(source.replace(/[\u0000-\u001F]+/g, " "));
  } catch {
    return null;
  }
}

export function isQueryId(value) {
  return /^[A-Za-z0-9_-]{8,80}$/.test(String(value || ""));
}

export function graphqlUrl(queryId, operation) {
  if (!isQueryId(queryId)) return "";
  if (operation !== "CreateTweet" && operation !== "CreateNoteTweet") return "";
  return `https://x.com/i/api/graphql/${queryId}/${operation}`;
}

export function createTweetUrl(queryId) {
  return graphqlUrl(queryId, "CreateTweet");
}

const WEIGHT_RANGES = [
  [0, 4351, 100],
  [8192, 8205, 100],
  [8208, 8223, 100],
  [8242, 8247, 100],
];

function codePointWeight(codePoint) {
  for (const [start, end, weight] of WEIGHT_RANGES) {
    if (codePoint >= start && codePoint <= end) return weight;
  }
  return 200;
}

function weightSlice(slice) {
  let sum = 0;
  for (const char of String(slice || "")) {
    sum += codePointWeight(char.codePointAt(0)) / 100;
  }
  return sum;
}

// twitter-text v3: maxWeightedTweetLength 280, scale 100, default weight 200,
// transformed URL length 23. The X client uses this same limit in tC().
export function weightedLength(text) {
  const source = String(text || "");
  const urlRe = /https?:\/\/[^\s]+/gi;
  let total = 0;
  let last = 0;
  for (const match of source.matchAll(urlRe)) {
    total += weightSlice(source.slice(last, match.index));
    total += 23;
    last = match.index + match[0].length;
  }
  return total + weightSlice(source.slice(last));
}

export function needsNoteTweet(text, { long = false } = {}) {
  if (long) return true;
  return weightedLength(text) > MAX_WEIGHTED_TWEET_LENGTH;
}

export function extractScriptUrls(html) {
  const source = String(html || "");
  const urls = [];
  const add = (value) => {
    if (value && !urls.includes(value)) urls.push(value);
  };
  const quoted = /(?:src|href)=["'](https:\/\/abs\.twimg\.com\/responsive-web\/client-web[^"']+\.js)["']/g;
  for (const match of source.matchAll(quoted)) add(match[1]);
  const loose = /https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/[A-Za-z0-9._-]+\.js/g;
  for (const match of source.matchAll(loose)) add(match[0]);
  return urls;
}

export function rankScriptUrls(urls) {
  return [...(urls || [])].sort((a, b) => scriptScore(b) - scriptScore(a)).slice(0, 6);
}

function scriptScore(url) {
  const value = String(url || "");
  if (/\/main\.[^/]+\.js/.test(value)) return 5;
  if (/\/bundle\./.test(value)) return 2;
  return 1;
}

export function extractOperationQueryId(source, operationName) {
  const text = String(source || "");
  const name = String(operationName || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  if (!name) return "";
  const forward = new RegExp(`queryId:\\s*"([A-Za-z0-9_-]{8,80})"([^}]{0,220})operationName:\\s*"${name}"`, "g");
  for (const match of text.matchAll(forward)) {
    if (!/operationName/.test(match[2])) return match[1];
  }
  const reverse = new RegExp(`operationName:\\s*"${name}"([^}]{0,220})queryId:\\s*"([A-Za-z0-9_-]{8,80})"`, "g");
  for (const match of text.matchAll(reverse)) {
    if (!/operationName/.test(match[1])) return match[2];
  }
  const wide = new RegExp(`queryId:\\s*"([A-Za-z0-9_-]{8,80})"([\\s\\S]{0,800}?)operationName:\\s*"${name}"`, "g");
  for (const match of text.matchAll(wide)) {
    if (!/operationName:\s*"/.test(match[2])) return match[1];
  }
  return "";
}

export function orderScriptUrls(urls) {
  const unique = [];
  for (const url of urls || []) {
    const value = String(url || "").split("?")[0];
    if (value && !unique.includes(value)) unique.push(value);
  }
  const mains = unique.filter((url) => /\/main\.[A-Za-z0-9_-]+\.js$/.test(url));
  const rest = rankScriptUrls(unique.filter((url) => !mains.includes(url)));
  return [...mains, ...rest].slice(0, 8);
}

export function extractCreateTweetQueryId(source) {
  return extractOperationQueryId(source, "CreateTweet");
}

export function extractWebBearer(source) {
  const match = String(source || "").match(/AAAAAAAAAAAAAAAAAAAAANRILg[A-Za-z0-9%]{8,120}/);
  return match ? match[0] : "";
}

export function normalizeLanguage(value) {
  const text = String(value || "").trim().toLowerCase().replace(/_/g, "-");
  if (!/^[a-z]{2}(?:-[a-z0-9]{2,8})?$/.test(text)) return "";
  return text;
}

export function buildStatusBody({ text, replyTo = "", queryId, features = CAPTURED_FEATURES, note = false, mediaIds = [] } = {}) {
  const variables = {
    tweet_text: String(text || ""),
    media: {
      media_entities: (mediaIds || []).filter(Boolean).map((id) => ({
        media_id: String(id),
        tagged_users: [],
      })),
      possibly_sensitive: false,
    },
    semantic_annotation_ids: [],
    disallowed_reply_options: null,
    semantic_annotation_options: note
      ? { composition_signal_1: true, source: "UniversalLink" }
      : { source: "UniversalLink" },
  };
  if (replyTo) {
    variables.reply = {
      in_reply_to_tweet_id: String(replyTo),
      exclude_reply_user_ids: [],
    };
  }
  return {
    variables,
    features: { ...features },
    queryId,
  };
}

export function buildCreateTweetBody(options = {}) {
  return buildStatusBody({ ...options, note: false });
}

export function buildCreateNoteTweetBody(options = {}) {
  return buildStatusBody({ ...options, note: true });
}

export function buildHeaders({ bearer, csrfToken, language, note = false } = {}) {
  const headers = {
    authorization: `Bearer ${bearer || PUBLIC_WEB_BEARER}`,
    "content-type": "application/json",
    origin: "https://x.com",
    referer: COMPOSE_URL,
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-active-user": "yes",
  };
  if (csrfToken) headers["x-csrf-token"] = csrfToken;
  if (language) headers["x-twitter-client-language"] = language;
  return headers;
}

export function graphqlErrors(payload) {
  if (!payload || typeof payload !== "object" || !Array.isArray(payload.errors)) return [];
  return payload.errors.filter(Boolean);
}

export function errorText(errors) {
  return (errors || []).filter(Boolean).map((error) => {
    const code = error.code ?? error.extensions?.code;
    const message = error.message || "";
    return code == null || code === "" ? message : `${code} ${message}`.trim();
  }).filter(Boolean).join("; ");
}

export function isAutomatedBlock(errors) {
  return (errors || []).filter(Boolean).some((error) => {
    const code = error.code ?? error.extensions?.code;
    return Number(code) === 226 || /automated/i.test(error.message || "");
  });
}

export function isRateLimited(status, errors) {
  if (Number(status) === 429) return true;
  return (errors || []).some((error) => Number(error.code) === 88 || /rate limit/i.test(error.message || ""));
}

export function isTooLong(errors) {
  return (errors || []).filter(Boolean).some((error) => {
    const code = error.code ?? error.extensions?.code;
    return Number(code) === 186 || /too long/i.test(error.message || "");
  });
}

export function explainGraphqlFailure({ status, errors, replyTo, note = false, hadTransactionId = false } = {}) {
  const text = errorText(errors);
  if (isRateLimited(status, errors)) return `Rate limited by X. Not retried. ${text}`.trim();
  if (isTooLong(errors)) {
    return `GraphQL 186: text is over the short-post limit. Long text must use CreateNoteTweet. ${text}`.trim();
  }
  if (isAutomatedBlock(errors)) {
    if (replyTo) {
      return `GraphQL 226: X rejected this reply as automated. Reply via page.fetch is best-effort and was not verified (capture on 2026-11-04). This skill does not click the composer and does not retry. ${text}`.trim();
    }
    if (note && !hadTransactionId) {
      return `GraphQL 226: CreateNoteTweet page.fetch without x-client-transaction-id was rejected as automated (capture on 2026-11-04). Not retried. ${text}`.trim();
    }
    if (note) {
      return `GraphQL 226: X rejected CreateNoteTweet as automated even with x-client-transaction-id. Not retried. ${text}`.trim();
    }
    return `GraphQL 226: X rejected CreateTweet as automated. A short post can succeed without x-client-transaction-id; this one did not. Not retried. ${text}`.trim();
  }
  if (Number(status) === 401) return "X login required in Ego Lite";
  return text || `HTTP ${status || 0}`;
}

export function tweetResult(payload) {
  const data = payload?.data;
  const result = data?.notetweet_create?.tweet_results?.result || data?.create_tweet?.tweet_results?.result;
  if (!result || typeof result !== "object") return null;
  if (result.rest_id || result.legacy?.id_str) return result;
  if (result.tweet && typeof result.tweet === "object") return result.tweet;
  return result;
}

export function fullTextFromResult(result) {
  const note = result?.note_tweet?.note_tweet_results?.result?.text;
  if (typeof note === "string" && note) return note;
  const legacy = result?.legacy?.full_text;
  return typeof legacy === "string" ? legacy : "";
}

export function restIdFromResult(result) {
  const id = result?.rest_id || result?.legacy?.id_str || "";
  return /^\d{1,25}$/.test(String(id)) ? String(id) : "";
}

export function screenNameFromResult(result) {
  const user = result?.core?.user_results?.result;
  const fromCore = user?.core?.screen_name;
  if (typeof fromCore === "string" && isScreenName(fromCore)) return fromCore;
  const legacy = user?.legacy?.screen_name;
  if (typeof legacy === "string" && isScreenName(legacy)) return legacy;
  return "";
}

export function statusUrl(screenName, restId) {
  if (!/^\d{1,25}$/.test(String(restId || ""))) return "";
  if (isScreenName(screenName)) return `https://x.com/${screenName}/status/${restId}`;
  return `https://x.com/i/web/status/${restId}`;
}

export function interpretCreateTweetResponse(status, body, { replyTo = "", note = false, hadTransactionId = false } = {}) {
  const payload = typeof body === "string" || body == null ? parseLooseJson(body) : body;
  if (!payload || typeof payload !== "object") {
    return { ok: false, error: `non-JSON response (HTTP ${status || 0})` };
  }
  const errors = graphqlErrors(payload);
  if (errors.length || Number(status) === 401) {
    return {
      ok: false,
      loginRequired: Number(status) === 401,
      automated: isAutomatedBlock(errors),
      tooLong: isTooLong(errors),
      error: explainGraphqlFailure({ status, errors, replyTo, note, hadTransactionId }),
    };
  }
  if (status && Number(status) !== 200) return { ok: false, error: `HTTP ${status}` };
  const result = tweetResult(payload);
  const id = restIdFromResult(result);
  if (!id) return { ok: false, error: `response had no rest_id (HTTP ${status || 0})` };
  const screenName = screenNameFromResult(result);
  const fullText = fullTextFromResult(result);
  return {
    ok: true,
    id,
    screenName,
    url: statusUrl(screenName, id),
    note: Boolean(result?.note_tweet) || note,
    fullText,
  };
}

export function extractTaggedJson(combined, tag = RESULT_TAG) {
  const lines = String(combined || "").split(/\n/);
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i].trim();
    const at = line.indexOf(tag);
    if (at === -1) continue;
    try {
      return JSON.parse(line.slice(at + tag.length));
    } catch {
      // keep scanning
    }
  }
  return null;
}

export function resolveProcessExit(combined, code) {
  const matched = String(combined || "").match(/nodejs process exited with code (\d+)/);
  if (matched) return Number(matched[1]);
  if (code === 0) return 0;
  return code ?? 1;
}
