#!/usr/bin/env node
/**
 * birdx — X/Twitter CLI via direct API (no browser required)
 *
 * Auth: cookies cached in ~/.config/bird/birdx-cookies.json
 *       Auto-reads from Chrome on disk (no browser needed)
 *       birdx auth: force refresh cookie cache from Chrome
 *       birdx auth --cdp: use openclaw browser CDP instead
 *
 * Commands:
 *   birdx auth                       Refresh cookie cache from Chrome disk
 *   birdx read <url|id>              Full tweet with viewCount + bookmarkCount
 *   birdx replies <url|id>           Thread + all replies
 *   birdx search "<query>"           Search with full metrics
 *   birdx followers <@username>      Followers list
 *   birdx following <@username>      Following list
 *
 * No browser needed at all — reads Chrome cookies directly from disk.
 */

'use strict';

const http  = require('http');
const https = require('https');
const crypto = require('crypto');
const sqlite = require('node:sqlite');
const { execSync } = require('child_process');
const WebSocket = require('ws');
const path  = require('path');
const fs    = require('fs');

// ── deps (from rettiwt-api project's node_modules) ────────────────────────────

const RETTIWT_MODULES = process.env.BIRDX_MODULES || require('path').join(process.env.HOME, 'clawd', 'node_modules');

let ClientTransaction, JSDOM;
try {
  ({ ClientTransaction } = require(path.join(RETTIWT_MODULES, 'x-client-transaction-id/script/mod.js')));
  ({ JSDOM } = require(path.join(RETTIWT_MODULES, 'jsdom')));
} catch {
  // Will fail gracefully if search is attempted without deps
}

// ── constants ─────────────────────────────────────────────────────────────────

const BEARER      = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA';
const CDP_URL     = 'http://127.0.0.1:18800/json/list';
const BIRD_CACHE  = path.join(process.env.HOME, '.config/bird/query-ids-cache.json');
const COOKIE_FILE = path.join(process.env.HOME, '.config/bird/birdx-cookies.json');

// Cookie TTL: ct0 rotates every ~6h on active sessions, auth_token lasts months
// We refresh proactively after 5h to avoid mid-session expiry
const COOKIE_TTL_MS = 5 * 60 * 60 * 1000;

const BASE_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Origin': 'https://x.com',
  'Referer': 'https://x.com/',
  'x-twitter-active-user': 'yes',
  'x-twitter-auth-type': 'OAuth2Session',
  'x-twitter-client-language': 'en',
};

// ── cache ─────────────────────────────────────────────────────────────────────

let _cookies = null; // { cookieStr, ct0, authToken }
let _xcomDoc  = null; // cached x.com DOM document

// ── Cookie persistence ────────────────────────────────────────────────────────

function saveCookies(cookies) {
  fs.mkdirSync(path.dirname(COOKIE_FILE), { recursive: true });
  fs.writeFileSync(COOKIE_FILE, JSON.stringify({ ...cookies, savedAt: Date.now() }, null, 2));
}

function loadCookiesFromFile() {
  try {
    const data = JSON.parse(fs.readFileSync(COOKIE_FILE, 'utf8'));
    if (!data.ct0 || !data.authToken) return null;
    if (Date.now() - data.savedAt > COOKIE_TTL_MS) return null; // expired
    return data;
  } catch { return null; }
}

// ── Chrome direct disk reader (no browser needed) ─────────────────────────────

/**
 * Derives the AES key from macOS Keychain (bird's A$ function).
 * Uses raw password string bytes (NOT base64-decoded) with PBKDF2.
 */
function deriveChromeCookieKey(password) {
  return crypto.pbkdf2Sync(password, 'saltysalt', 1003, 16, 'sha1');
}

/**
 * Decrypts a single Chrome v10-encrypted cookie value (bird's G2 + i4 + _2).
 * @param {Buffer} encBuf  - raw encrypted_value bytes (WITH v10 prefix)
 * @param {Buffer} key     - 16-byte AES key
 * @param {boolean} stripHashPrefix - true when db version >= 24
 */
function decryptChromeCookie(encBuf, key, stripHashPrefix) {
  if (encBuf.length < 3) return null;
  const prefix = encBuf.slice(0, 3).toString('utf8');
  if (!/^v\d\d$/.test(prefix)) {
    // Not encrypted — treat as plaintext
    return encBuf.toString('utf8').replace(/^[\x00-\x1f]+/, '');
  }
  try {
    const IV = Buffer.alloc(16, 0x20); // 16 space chars
    const decipher = crypto.createDecipheriv('aes-128-cbc', key, IV);
    decipher.setAutoPadding(false);
    let dec = Buffer.concat([decipher.update(encBuf.slice(3)), decipher.final()]);
    // Custom PKCS7 unpad (bird's _2)
    const pad = dec[dec.length - 1];
    if (pad && pad <= 16) dec = dec.slice(0, dec.length - pad);
    // Skip 32-byte random prefix if version >= 24 (bird's stripHashPrefix)
    if (stripHashPrefix && dec.length >= 32) dec = dec.slice(32);
    return dec.toString('utf8').replace(/^[\x00-\x1f]+/, '');
  } catch {
    return null;
  }
}

/**
 * Reads auth_token and ct0 directly from Chrome's SQLite cookie database.
 * No browser required — works while Chrome is running or closed.
 */
async function loadCookiesFromChrome() {
  // 1. Get Chrome Safe Storage password from macOS Keychain
  let pw;
  try {
    pw = execSync('security find-generic-password -w -s "Chrome Safe Storage" -a "Chrome"',
      { encoding: 'utf8', timeout: 5000 }).trim();
  } catch (e) {
    throw new Error(`Failed to read Chrome Safe Storage from Keychain: ${e.message}`);
  }
  if (!pw) throw new Error('Chrome Safe Storage password is empty');

  const key = deriveChromeCookieKey(pw);

  // 2. Locate and copy the Cookies database
  const chromeCookieDb = path.join(
    process.env.HOME,
    'Library/Application Support/Google/Chrome/Default/Cookies'
  );
  if (!fs.existsSync(chromeCookieDb)) {
    throw new Error(`Chrome Cookies DB not found at ${chromeCookieDb}`);
  }
  const tmpDb = `/tmp/birdx_chrome_cookies_${Date.now()}.db`;
  // Copy WAL files too (needed for accurate reads while Chrome is running)
  try {
    fs.copyFileSync(chromeCookieDb, tmpDb);
    for (const ext of ['-wal', '-shm']) {
      const src = chromeCookieDb + ext;
      if (fs.existsSync(src)) fs.copyFileSync(src, tmpDb + ext);
    }
  } catch (e) {
    throw new Error(`Failed to copy Chrome Cookies DB: ${e.message}`);
  }

  // 3. Read encrypted cookies with node:sqlite
  try {
    const db = new sqlite.DatabaseSync(tmpDb, { readonly: true });

    // Check db version to determine if stripHashPrefix applies
    const verRow = db.prepare("SELECT value FROM meta WHERE key='version'").get();
    const dbVersion = Number(verRow?.value ?? 0);
    const stripHashPrefix = dbVersion >= 24;

    const rows = db.prepare(
      "SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%x.com' AND name IN ('auth_token', 'ct0')"
    ).all();
    db.close();

    // 4. Decrypt
    const results = {};
    for (const row of rows) {
      const encBuf = Buffer.isBuffer(row.encrypted_value)
        ? row.encrypted_value
        : Buffer.from(row.encrypted_value);
      const value = decryptChromeCookie(encBuf, key, stripHashPrefix);
      if (value && !results[row.name]) {
        results[row.name] = value;
      }
    }

    const { auth_token: authToken, ct0 } = results;
    if (!authToken || !ct0) {
      throw new Error(
        `Chrome cookies decrypted but missing ${!authToken ? 'auth_token' : 'ct0'}. ` +
        'Make sure you are logged into x.com in Chrome.'
      );
    }

    // Build full cookie string for x.com (reuse all cookies)
    const fullDb = new sqlite.DatabaseSync(tmpDb, { readonly: true });
    const allRows = fullDb.prepare(
      "SELECT name, encrypted_value, value FROM cookies WHERE host_key LIKE '%x.com' OR host_key LIKE '%twitter.com'"
    ).all();
    fullDb.close();

    const cookiePairs = [];
    for (const row of allRows) {
      const encBuf = Buffer.isBuffer(row.encrypted_value)
        ? row.encrypted_value
        : Buffer.from(row.encrypted_value);
      let val = row.value || '';
      if (!val && encBuf.length > 0) {
        val = decryptChromeCookie(encBuf, key, stripHashPrefix) || '';
      }
      if (val) cookiePairs.push(`${row.name}=${val}`);
    }
    const cookieStr = cookiePairs.join('; ');

    return { cookieStr, ct0, authToken, source: 'chrome-disk' };
  } finally {
    // Cleanup temp files
    for (const ext of ['', '-wal', '-shm']) {
      try { fs.unlinkSync(tmpDb + ext); } catch {}
    }
  }
}

// ── CDP: get x.com cookies from any tab ───────────────────────────────────────

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}

async function fetchCookiesViaCDP() {
  let targets;
  try { targets = await fetchJson(CDP_URL); } catch {
    throw new Error(
      'openclaw browser not running.\n' +
      'Either open the browser and run `birdx auth`, or\n' +
      'run `birdx auth` once to save cookies for offline use.'
    );
  }
  const anyPage = targets.find(t => t.type === 'page');
  if (!anyPage) throw new Error('No browser tabs open. Open any page in openclaw browser.');

  return new Promise((resolve, reject) => {
    const ws = new WebSocket(anyPage.webSocketDebuggerUrl);
    const timer = setTimeout(() => { ws.close(); reject(new Error('CDP timeout')); }, 10000);

    ws.on('open', () => {
      ws.send(JSON.stringify({ id: 1, method: 'Network.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Network.getAllCookies' }));
    });
    ws.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.id === 2) {
        clearTimeout(timer);
        ws.close();
        const xCookies = (msg.result?.cookies || [])
          .filter(c => c.domain.includes('x.com') || c.domain.includes('twitter.com'));
        const cookieStr = xCookies.map(c => `${c.name}=${c.value}`).join('; ');
        const ct0       = xCookies.find(c => c.name === 'ct0')?.value       || '';
        const authToken = xCookies.find(c => c.name === 'auth_token')?.value || '';
        if (!ct0 || !authToken) {
          reject(new Error('No x.com auth cookies in browser. Log in to X first.'));
        } else {
          resolve({ cookieStr, ct0, authToken });
        }
      }
    });
    ws.on('error', (e) => { clearTimeout(timer); reject(e); });
  });
}

async function loadCookies() {
  if (_cookies) return _cookies;

  // 1. Try cookie file cache first (fastest path)
  const cached = loadCookiesFromFile();
  if (cached) {
    _cookies = cached;
    return _cookies;
  }

  // 2. Try reading Chrome cookies directly from disk (no browser needed)
  try {
    process.stderr.write('Cookie cache expired — reading from Chrome disk...\n');
    _cookies = await loadCookiesFromChrome();
    saveCookies(_cookies);
    process.stderr.write(`Cookies saved to ${COOKIE_FILE}\n`);
    return _cookies;
  } catch (chromeErr) {
    process.stderr.write(`Chrome disk read failed: ${chromeErr.message}\n`);
  }

  // 3. Fall back to CDP (browser must be running)
  process.stderr.write('Falling back to CDP (openclaw browser must be running)...\n');
  _cookies = await fetchCookiesViaCDP();
  saveCookies(_cookies);
  process.stderr.write(`Cookies saved to ${COOKIE_FILE}\n`);
  return _cookies;
}

async function cmdAuth(useCDP = false) {
  let cookies;
  if (useCDP) {
    process.stderr.write('Reading cookies from openclaw browser CDP...\n');
    cookies = await fetchCookiesViaCDP();
  } else {
    process.stderr.write('Reading cookies from Chrome disk (no browser needed)...\n');
    try {
      cookies = await loadCookiesFromChrome();
    } catch (e) {
      process.stderr.write(`Chrome disk read failed: ${e.message}\nFalling back to CDP...\n`);
      cookies = await fetchCookiesViaCDP();
    }
  }
  saveCookies(cookies);
  console.log(`✅ Cookies saved to ${COOKIE_FILE}`);
  console.log(`   source:     ${cookies.source || 'unknown'}`);
  console.log(`   auth_token: ${cookies.authToken.slice(0, 8)}...`);
  console.log(`   ct0:        ${cookies.ct0.slice(0, 8)}...`);
  console.log('\nbirdx now works without any browser open.');
}

// ── Auth headers builder ───────────────────────────────────────────────────────

async function authHeaders(extraHeaders = {}) {
  const { cookieStr, ct0 } = await loadCookies();
  return {
    ...BASE_HEADERS,
    'Authorization': `Bearer ${BEARER}`,
    'x-csrf-token': ct0,
    'Cookie': cookieStr,
    ...extraHeaders,
  };
}

// ── Transaction ID (needed for SearchTimeline) ─────────────────────────────────

async function getXcomDocument() {
  if (_xcomDoc) return _xcomDoc;
  if (!JSDOM || !ClientTransaction) throw new Error('JSDOM/x-client-transaction-id not available. Search requires these deps.');

  const res = await fetch('https://x.com', { headers: { 'User-Agent': BASE_HEADERS['User-Agent'] } });
  const html = await res.text();
  _xcomDoc = new JSDOM(html).window.document;
  return _xcomDoc;
}

async function getTransactionId(method, apiPath) {
  const document = await getXcomDocument();
  const tx = await ClientTransaction.create(document);
  return tx.generateTransactionId(method.toUpperCase(), apiPath);
}

// ── Query ID cache ─────────────────────────────────────────────────────────────

function getQueryIds() {
  try { return JSON.parse(fs.readFileSync(BIRD_CACHE, 'utf8')).ids || {}; } catch { return {}; }
}

// ── Tweet API call ─────────────────────────────────────────────────────────────

const TWEET_FEATURES = {
  view_counts_everywhere_api_enabled: true,
  longform_notetweets_consumption_enabled: true,
  responsive_web_graphql_timeline_navigation_enabled: true,
  responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
  premium_content_api_read_enabled: false,
  communities_web_enable_tweet_community_results_fetch: true,
  rweb_tipjar_consumption_enabled: true,
  creator_subscriptions_tweet_preview_api_enabled: true,
  responsive_web_edit_tweet_api_enabled: true,
  graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
  tweet_awards_web_tipping_enabled: false,
  freedom_of_speech_not_reach_fetch_enabled: true,
  standardized_nudges_misinfo: true,
  tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
  longform_notetweets_rich_text_read_enabled: true,
  longform_notetweets_inline_media_enabled: true,
  responsive_web_enhance_cards_enabled: false,
};

const SEARCH_FEATURES = {
  ...TWEET_FEATURES,
  responsive_web_graphql_exclude_directive_enabled: true,
  verified_phone_label_enabled: false,
};

const USER_FEATURES = {
  hidden_profile_likes_enabled: true,
  hidden_profile_subscriptions_enabled: true,
  rweb_tipjar_consumption_enabled: true,
  responsive_web_graphql_exclude_directive_enabled: true,
  verified_phone_label_enabled: false,
  subscriptions_verification_info_is_identity_verified_enabled: true,
  highlights_tweets_tab_ui_enabled: true,
  responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
  responsive_web_graphql_timeline_navigation_enabled: true,
};

async function apiFetch(url, extraHeaders = {}) {
  const headers = await authHeaders(extraHeaders);
  const res = await fetch(url, { headers });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status}${body ? ': ' + body.slice(0, 100) : ''}`);
  }
  return res.json();
}

async function tweetDetailFetch(tweetId, sortMode = 'Recency') {
  const ids = getQueryIds();
  if (!ids.TweetDetail) throw new Error('TweetDetail query ID missing. Run: bird query-ids --fresh');
  const qid = ids.TweetDetail;
  const variables = {
    focalTweetId: tweetId, referrer: 'tweet', count: 40,
    rankingMode: sortMode, with_rux_injections: false,
    includePromotedContent: false, withCommunity: true,
    withQuickPromoteEligibilityTweetFields: false,
    withBirdwatchNotes: true, withVoice: true, withV2Timeline: true,
  };
  const url = `https://x.com/i/api/graphql/${qid}/TweetDetail?variables=${encodeURIComponent(JSON.stringify(variables))}&features=${encodeURIComponent(JSON.stringify(TWEET_FEATURES))}`;
  return apiFetch(url);
}

async function searchFetch(query, product = 'Top', count = 20, cursor) {
  const ids = getQueryIds();
  if (!ids.SearchTimeline) throw new Error('SearchTimeline query ID missing. Run: bird query-ids --fresh');
  const qid = ids.SearchTimeline;
  const variables = { rawQuery: query, count, querySource: 'typed_query', product, ...(cursor ? { cursor } : {}) };
  const apiPath = `/i/api/graphql/${qid}/SearchTimeline`;
  const url = `https://x.com${apiPath}?variables=${encodeURIComponent(JSON.stringify(variables))}&features=${encodeURIComponent(JSON.stringify(SEARCH_FEATURES))}`;

  // SearchTimeline requires x-client-transaction-id
  const tid = await getTransactionId('GET', apiPath);
  return apiFetch(url, { 'x-client-transaction-id': tid });
}

async function userListFetch(opName, userId, count = 20, cursor) {
  const ids = getQueryIds();
  const qid = ids[opName];
  if (!qid) throw new Error(`${opName} query ID missing. Run: bird query-ids --fresh`);
  const variables = { userId, count, includePromotedContent: false, ...(cursor ? { cursor } : {}) };
  const url = `https://x.com/i/api/graphql/${qid}/${opName}?variables=${encodeURIComponent(JSON.stringify(variables))}&features=${encodeURIComponent(JSON.stringify(USER_FEATURES))}`;
  return apiFetch(url);
}

// ── Data extractors ────────────────────────────────────────────────────────────

function extractTweet(result) {
  if (!result || result.__typename !== 'Tweet') return null;
  const l = result.legacy || {};
  const v = result.views || {};
  const userResult = result.core?.user_results?.result;
  const uCore   = userResult?.core   || {};
  const uLegacy = userResult?.legacy || {};
  const text = (result.note_tweet?.note_tweet_results?.result?.text || l.full_text || '')
    .replace(/https:\/\/t\.co\/\S+/g, '').trim();
  return {
    id: l.id_str || result.rest_id,
    text,
    createdAt: l.created_at,
    author: {
      id: userResult?.rest_id,
      username: uCore.screen_name || uLegacy.screen_name,
      name: uCore.name || uLegacy.name,
      verified: userResult?.is_blue_verified || uLegacy.verified || false,
      followersCount: uLegacy.followers_count,
    },
    replyCount: l.reply_count,
    retweetCount: l.retweet_count,
    quoteCount: l.quote_count,
    likeCount: l.favorite_count,
    bookmarkCount: l.bookmark_count,
    viewCount: v.count ? parseInt(v.count) : null,
    replyTo: l.in_reply_to_status_id_str || null,
    conversationId: l.conversation_id_str,
  };
}

function parseTweetsFromInstructions(instructions) {
  const tweets = [];
  let nextCursor = null;
  for (const inst of (instructions || [])) {
    for (const entry of (inst.entries || [])) {
      const c = entry.content;
      if (!c) continue;
      if (c.cursorType === 'Bottom') nextCursor = c.value;
      const r = c.itemContent?.tweet_results?.result;
      if (r) { const t = extractTweet(r); if (t) tweets.push(t); }
      for (const item of (c.items || [])) {
        const r2 = item.item?.itemContent?.tweet_results?.result;
        if (r2) { const t = extractTweet(r2); if (t) tweets.push(t); }
      }
    }
  }
  return { tweets, nextCursor };
}

function extractUser(result) {
  if (!result) return null;
  const l = result.legacy || {};
  const c = result.core  || {};
  return {
    id: result.rest_id,
    username: c.screen_name || l.screen_name,
    name: c.name || l.name,
    bio: (l.description || '').replace(/\n/g, ' '),
    location: l.location,
    verified: result.is_blue_verified || l.verified || false,
    followersCount: l.followers_count,
    followingCount: l.friends_count,
    tweetsCount: l.statuses_count,
  };
}

function parseUsersFromInstructions(instructions) {
  const users = [];
  let nextCursor = null;
  for (const entry of (instructions.find(i => i.entries)?.entries || [])) {
    const c = entry.content;
    if (!c) continue;
    if (c.cursorType === 'Bottom') nextCursor = c.value;
    if (c.itemContent?.user_results?.result) {
      const u = extractUser(c.itemContent.user_results.result);
      if (u) users.push(u);
    }
  }
  return { users, nextCursor };
}

// ── Commands ───────────────────────────────────────────────────────────────────

function extractTweetId(input) {
  const match = input.match(/status\/(\d+)/);
  if (match) return match[1];
  if (/^\d+$/.test(input)) return input;
  return null;
}

async function cmdRead(input, opts = {}) {
  const tweetId = extractTweetId(input);
  if (!tweetId) throw new Error(`Invalid tweet URL or ID: ${input}`);

  const j = await tweetDetailFetch(tweetId);
  const instructions = j?.data?.threaded_conversation_with_injections_v2?.instructions || [];
  const { tweets } = parseTweetsFromInstructions(instructions);
  const focal = tweets.find(t => t.id === tweetId) || tweets[0];

  if (!focal) throw new Error('Tweet not found');
  if (opts.json) { console.log(JSON.stringify(focal, null, 2)); return; }
  console.log('');
  printTweet(focal);
  console.log('');
}

async function cmdReplies(input, opts = {}) {
  const tweetId = extractTweetId(input);
  if (!tweetId) throw new Error(`Invalid tweet URL or ID: ${input}`);

  const sortMode = opts.sort === 'relevance' ? 'Relevance' : 'Recency';
  const j = await tweetDetailFetch(tweetId, sortMode);
  const instructions = j?.data?.threaded_conversation_with_injections_v2?.instructions || [];
  const { tweets, nextCursor } = parseTweetsFromInstructions(instructions);

  const focal   = tweets.find(t => t.id === tweetId) || tweets[0];
  const replies = tweets.filter(t => t.id !== tweetId);

  if (opts.json) { console.log(JSON.stringify({ focal, replies, nextCursor }, null, 2)); return; }
  console.log('\n═══ Original Tweet ═══\n');
  printTweet(focal);
  console.log(`\n═══ Replies (${replies.length}, sort: ${sortMode}) ═══\n`);
  for (const r of replies) { printTweet(r, { indent: '  ' }); console.log(''); }
  if (nextCursor) console.log(`📄 cursor: ${nextCursor}`);
}

async function cmdSearch(query, opts = {}) {
  if (!query) throw new Error('Usage: birdx search "<query>" [--sort top|latest] [--total N]');
  const total   = parseInt(opts.total || opts.count || '20');
  const product = (opts.sort || 'top') === 'latest' ? 'Latest' : 'Top';

  process.stderr.write(`Searching "${query}" (sort=${product}, total=${total})...\n`);

  // Auto-paginate until we have enough or no more cursor
  const allTweets = [];
  let cursor = opts.cursor || undefined;
  let page = 0;
  while (allTweets.length < total) {
    page++;
    if (page > 1) process.stderr.write(`  page ${page}: fetching more (have ${allTweets.length}/${total})...\n`);
    const j = await searchFetch(query, product, 20, cursor);
    const instructions = j?.data?.search_by_raw_query?.search_timeline?.timeline?.instructions || [];
    const { tweets, nextCursor } = parseTweetsFromInstructions(instructions);
    if (!tweets.length) break;
    allTweets.push(...tweets);
    cursor = nextCursor;
    if (!cursor) break;
    await new Promise(r => setTimeout(r, 500));
  }

  const results = allTweets.slice(0, total);
  if (opts.json) { console.log(JSON.stringify({ tweets: results, count: results.length }, null, 2)); return; }
  console.log(`\n🔍 "${query}" — ${results.length} results (${product})\n`);
  for (const t of results) { printTweet(t); console.log(''); }
}

async function resolveUsernameToId(username) {
  const handle = username.replace(/^@/, '');
  try {
    const out = execSync(`bird user-tweets ${handle} -n 1 --json 2>/dev/null`, { timeout: 15000 }).toString().trim();
    const data = JSON.parse(out);
    const tweet = Array.isArray(data) ? data[0] : data;
    if (tweet?.authorId) return tweet.authorId;
  } catch {}
  throw new Error(`Cannot resolve userId for @${handle}`);
}

async function cmdFollowers(username, opts = {}) {
  const handle = username.replace(/^@/, '');
  process.stderr.write(`Resolving @${handle}...\n`);
  const userId = await resolveUsernameToId(handle);
  process.stderr.write(`userId: ${userId}\n`);

  const j = await userListFetch('Followers', userId, parseInt(opts.count || '20'), opts.cursor);
  const instructions = j?.data?.followers_timeline?.timeline?.instructions || [];
  const { users, nextCursor } = parseUsersFromInstructions(instructions);

  if (opts.json) { console.log(JSON.stringify({ users, nextCursor }, null, 2)); return; }
  console.log(`\n👥 Followers of @${handle} (${users.length} shown)\n`);
  for (const u of users) printUser(u);
  if (nextCursor) console.log(`📄 cursor: ${nextCursor}`);
}

async function cmdFollowing(username, opts = {}) {
  const handle = username.replace(/^@/, '');
  process.stderr.write(`Resolving @${handle}...\n`);
  const userId = await resolveUsernameToId(handle);
  process.stderr.write(`userId: ${userId}\n`);

  const j = await userListFetch('Following', userId, parseInt(opts.count || '20'), opts.cursor);
  const instructions = j?.data?.following_timeline?.timeline?.instructions
    || j?.data?.followers_timeline?.timeline?.instructions || [];
  const { users, nextCursor } = parseUsersFromInstructions(instructions);

  if (opts.json) { console.log(JSON.stringify({ users, nextCursor }, null, 2)); return; }
  console.log(`\n➡️  Following of @${handle} (${users.length} shown)\n`);
  for (const u of users) printUser(u);
  if (nextCursor) console.log(`📄 cursor: ${nextCursor}`);
}

// ── Formatters ─────────────────────────────────────────────────────────────────

function fmt(n) {
  if (n == null) return 'N/A';
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000)     return (n / 1_000).toFixed(1) + 'K';
  return String(n);
}

function fmtDate(str) {
  if (!str) return '';
  try { return new Date(str).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false }); } catch { return str; }
}

function printTweet(t, opts = {}) {
  if (!t) return;
  const { indent = '', showUrl = true } = opts;
  const tick = t.author?.verified ? ' ✓' : '';
  console.log(`${indent}👤 @${t.author?.username || '?'}${tick}  ${t.author?.name || ''}`);
  console.log(`${indent}${t.text}`);
  console.log(`${indent}📅 ${fmtDate(t.createdAt)}`);
  console.log(`${indent}👁 ${fmt(t.viewCount)}  ❤️ ${fmt(t.likeCount)}  🔁 ${fmt(t.retweetCount)}  💬 ${fmt(t.replyCount)}  🔖 ${fmt(t.bookmarkCount)}`);
  const url = t.author?.username ? `https://x.com/${t.author.username}/status/${t.id}` : null;
  if (showUrl && url) console.log(`${indent}🔗 ${url}`);
}

function printUser(u) {
  if (!u) return;
  const tick = u.verified ? ' ✓' : '';
  console.log(`@${u.username}${tick}  ${u.name}`);
  if (u.bio) console.log(`  ${u.bio}`);
  console.log(`  👥 ${fmt(u.followersCount)} followers · ${fmt(u.followingCount)} following · ${fmt(u.tweetsCount)} tweets`);
  if (u.location) console.log(`  📍 ${u.location}`);
  console.log('');
}

// ── CLI ────────────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const cmd = args[0];
  const positional = [];
  const opts = {};
  for (let i = 1; i < args.length; i++) {
    const a = args[i];
    if (a === '--json') opts.json = true;
    else if ((a === '--sort' || a === '--count' || a === '--cursor' || a === '--total') && args[i + 1]) opts[a.slice(2)] = args[++i];
    else if (!a.startsWith('-')) positional.push(a);
  }
  return { cmd, positional, opts };
}

function printHelp() {
  console.log(`
birdx — X/Twitter CLI (direct API, no browser required after auth)

Setup (one-time, browser must be open):
  birdx auth                          Save cookies → no browser needed after this

Commands (browser NOT required after auth):
  birdx read <tweet-url|id>           Full tweet with viewCount + bookmarkCount
  birdx replies <tweet-url|id>        Replies (--sort relevance shows thread first)
  birdx followers <@username>         Followers list
  birdx following <@username>         Following list
  birdx search "<query>"              Search tweets with full metrics

Options:
  --json    Raw JSON output
  --sort    top|latest (search) | relevance|latest (replies)
  --total   Total results to collect, default 20 (auto-paginates internally)
  --count   Alias for --total (legacy)
  --cursor  Start from this pagination cursor

Examples:
  birdx read https://x.com/user/status/123
  birdx search "nano banana 2" --sort top --count 20
  birdx search "openclaw" --sort top --total 80
  birdx replies 123456 --sort relevance
  birdx followers @andrewchen --count 50
`);
}

async function main() {
  const { cmd, positional, opts } = parseArgs(process.argv);
  try {
    if (cmd === 'auth') {
      await cmdAuth(!!opts.cdp);
    } else if (cmd === 'read') {
      if (!positional[0]) throw new Error('Usage: birdx read <url|id>');
      await cmdRead(positional[0], opts);
    } else if (cmd === 'replies') {
      if (!positional[0]) throw new Error('Usage: birdx replies <url|id>');
      await cmdReplies(positional[0], opts);
    } else if (cmd === 'search') {
      await cmdSearch(positional.join(' '), opts);
    } else if (cmd === 'followers') {
      if (!positional[0]) throw new Error('Usage: birdx followers <@username>');
      await cmdFollowers(positional[0], opts);
    } else if (cmd === 'following') {
      if (!positional[0]) throw new Error('Usage: birdx following <@username>');
      await cmdFollowing(positional[0], opts);
    } else {
      printHelp();
    }
  } catch (err) {
    console.error(`\n❌ ${err.message}`);
    process.exit(1);
  }
}

main();
