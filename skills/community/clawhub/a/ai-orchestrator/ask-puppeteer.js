#!/usr/bin/env node

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ═══ Новые модули диагностики ══════════════════════════════════════════════
const { Diagnostics } = require('./diagnostics.js');
const { requireAuth } = require('./auth-check.js');

// ═══ Базовая директория ═══
const SCRIPT_DIR = path.dirname(process.argv[1]);
const BASE_DIR = path.resolve(SCRIPT_DIR);

// ═══ Конфиг: .deepseek.json overrides defaults ═══════════════════
const CONFIG_PATH = path.join(BASE_DIR, '.deepseek.json');
const DEFAULT_CONFIG = {
  browserLaunchTimeout: 30000,
  answerTimeout: 600000,
  composerTimeout: 10000,
  navigationTimeout: 30000,
  idleTimeout: 15000,
  heartbeatInterval: 15000,
  domErrorIdleMs: 25000,
  shortAnswerStableMs: 300,
  minResponseLength: 50,
  maxContinueRounds: 30,
  deltaThreshold: 100,
  minTextForContinue: 2000,
  maxTextForContinue: 6000,
  rateLimitMs: 5000,
  preferredChatMode: 'expert',
  debugMode: false,
  logToFile: false,
  logPath: '.logs/deepseek.log',
};

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const userConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return { ...DEFAULT_CONFIG, ...userConfig };
    }
  } catch (e) { /* ignore */ }
  return DEFAULT_CONFIG;
}

const CONFIG = loadConfig();

const TIMEOUT_ANSWER = CONFIG.answerTimeout;
const TIMEOUT_BROWSER = CONFIG.browserLaunchTimeout;
const IDLE_TIMEOUT = CONFIG.idleTimeout;
const HEARTBEAT_INTERVAL = CONFIG.heartbeatInterval;
const DOM_ERROR_IDLE = CONFIG.domErrorIdleMs;
const SHORT_STABLE = CONFIG.shortAnswerStableMs;
const MIN_RESPONSE = CONFIG.minResponseLength;
const DELTA_THRESHOLD = CONFIG.deltaThreshold;
const RATE_LIMIT_MS = CONFIG.rateLimitMs;
const OVERSIZE_RETRY_MIN_CHARS = 4000;
const OVERSIZE_RETRY_KEEP_RATIO = 0.85;
const OVERSIZE_MAX_RETRIES = 6;

if (CONFIG.logToFile) {
  const logPath = path.resolve(BASE_DIR, CONFIG.logPath);
  try {
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    const origLog = console.log;
    console.log = (...args) => {
      const line = args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ');
      fs.appendFileSync(logPath, `[${new Date().toISOString()}] ${line}\n`);
      origLog(...args);
    };
  } catch (e) { console.error('⚠️ Log file setup failed:', e.message); }
}

// ═══ CDP Interceptor (module-level state) ═══════════════════════════
var cdpInterceptor = null;

const argv = process.argv.slice(2);
const isVisible = argv.includes('--visible');
const waitForAuth = argv.includes('--wait');
const shouldClose = argv.includes('--close');
const endSession = argv.includes('--end-session');
const newChat = argv.includes('--new-chat');
const useDaemon = argv.includes('--daemon');
const dryRun = argv.includes('--dry-run');
const searchMode = argv.includes('--search');
const thinkMode = argv.includes('--think');
const VERBOSE = argv.includes('--verbose');
const preferredChatMode = String(CONFIG.preferredChatMode || 'expert').toLowerCase();
const FILE_ARG_IDX = argv.indexOf('--file');
const FILE_PROMPT_PATH = FILE_ARG_IDX !== -1 ? (argv[FILE_ARG_IDX + 1] || '') : null;
if (FILE_PROMPT_PATH) debugLog('[DEBUG] --file=' + FILE_PROMPT_PATH + ', exists=' + fs.existsSync(FILE_PROMPT_PATH));

// ═══ Авто-детект пути к Chromium/Chrome ═══
let executablePath;

// Пробуем bundled Chromium от puppeteer (предпочтительно)
try {
  const bundledPath = require('puppeteer').executablePath();
  if (bundledPath && fs.existsSync(bundledPath)) {
    executablePath = bundledPath;
    log(`✅ Используем bundled Chromium: ${executablePath}`);
  }
} catch (e) {}

// Если bundled не найден, ищем system chromium
if (!executablePath) {
  log('⚠️ Bundled Chromium не найден, ищем system chromium...');
  try {
    const which = require('child_process').execSync('which chromium 2>/dev/null || which chromium-browser 2>/dev/null || which google-chrome 2>/dev/null || echo ""', { encoding: 'utf8' }).trim();
    if (which && fs.existsSync(which)) {
      executablePath = which;
      log(`✅ Найден system chromium: ${executablePath}`);
    }
  } catch (e) {}
}

// ═══ Вспомогательные функции для исправления locked profile ═══

/**
 * Убивает все процессы Chrome, использующие указанный profileDir
 */
async function killChromeProcessesForProfile(profilePath) {
  try {
    const { execSync } = require('child_process');
    const grepCmd = `ps aux | grep -i chrome | grep "${profilePath}" | grep -v grep | awk '{print $2}'`;
    const pids = execSync(grepCmd, { encoding: 'utf8' })
      .split('\n')
      .filter(pid => pid.trim())
      .map(pid => pid.trim());

    if (pids.length > 0) {
      debugLog(`🔪 Убиваем процессы Chrome: ${pids.join(', ')}`);
      for (const pid of pids) {
        try { process.kill(pid, 'SIGKILL'); } catch (e) {}
      }
      // Даем время на завершение
      await new Promise(resolve => setTimeout(resolve, 1000));
      // Очистка /dev/shm и /tmp
      try {
        execSync(`rm -rf /dev/shm/.com.google.Chrome.* 2>/dev/null || true`);
        execSync(`rm -rf /tmp/.com.google.Chrome.* 2>/dev/null || true`);
      } catch (e) {}
    }
  } catch (err) {
    // grep может вернуть ошибку если нет процессов — игнорируем
  }
}

/**
 * Запуск браузера с таймаутом и очисткой lock-файлов
 */
async function launchWithTimeout(options, timeoutMs = 30000) {
  const profileDir = options.userDataDir;
  // Очищаем lock-файлы перед запуском
  if (profileDir && fs.existsSync(profileDir)) {
    const locksToRemove = ['SingletonLock', 'SingletonSocket', 'SingletonCookie'];
    for (const lock of locksToRemove) {
      const lockPath = path.join(profileDir, lock);
      if (fs.existsSync(lockPath)) {
        try {
          fs.unlinkSync(lockPath);
          debugLog(`🧹 Удалён lock-файл: ${lock}`);
        } catch (err) {
          // Может быть permission denied, игнорируем
        }
      }
    }
  }

  log(`🚀 Запуск браузера (timeout: ${timeoutMs}ms)...`);
  const launchPromise = puppeteer.launch(options);
  const timeoutPromise = new Promise((_, reject) => 
    setTimeout(() => {
      debugLog(`⏰ Таймаут launch через ${timeoutMs}ms`);
      reject(new Error(`Launch timeout after ${timeoutMs}ms`));
    }, timeoutMs)
  );

  try {
    const browser = await Promise.race([launchPromise, timeoutPromise]);
    log('✅ Браузер запущен');
    return browser;
  } catch (err) {
    log('❌ Ошибка launch:', err.message);
    throw err;
  }
}

// Извлекаем имя сессии: --session work
const sessionIdx = argv.indexOf('--session');
const sessionName = sessionIdx !== -1 ? (argv[sessionIdx + 1] || 'default') : null;

// Вопрос — всё что не флаг
const question = FILE_PROMPT_PATH ? fs.readFileSync(FILE_PROMPT_PATH, 'utf8').trim() : argv.filter(a =>
 !a.startsWith('--') &&
 (sessionIdx === -1 || argv.indexOf(a) !== sessionIdx + 1)
).join(' ');

if (!question && !endSession) {
 console.error(`Usage:
 node ask-puppeteer.js "вопрос" — одиночный (закроет браузер)
 node ask-puppeteer.js "вопрос" --session work — сессия "work" (держит контекст)
 node ask-puppeteer.js "ещё вопрос" --session work — продолжение в той же сессии
 node ask-puppeteer.js --session work --new-chat "вопрос" — новый чат в сессии
 node ask-puppeteer.js --session work --end-session — завершить сессию
 node ask-puppeteer.js "вопрос" --visible --wait — с видимым браузером
 node ask-puppeteer.js "вопрос" --daemon — использовать демон (если запущен)
`);
 process.exit(1);
}

let browser = null;
let dsPage = null;
let browserLaunchedByUs = false;
let browserConnectionMode = 'local';

// Используем BASE_DIR
const PROFILE_DIR = path.join(BASE_DIR, '.profile');
const SESSIONS_DIR = path.join(BASE_DIR, '.sessions');
const DAEMON_ENDPOINT_FILE = path.join(BASE_DIR, '.daemon-ws-endpoint');

const DS_URL = 'https://chat.deepseek.com/';
const COMPOSER = [
  // DeepSeek Chat selectors (latest)
  'textarea[data-deepseek="chat-input"]',
  'textarea[placeholder*="Введите"]', 'textarea[placeholder*="Message"]', 'textarea[placeholder*="Type"]', 'textarea[placeholder]', 'textarea',
  'div[contenteditable="true"]', 'div[role="textbox"]', 'div[contenteditable]',
  'div[class*="input" i]', 'div[class*="composer" i]', 'div[class*="editor" i]',
  'div[class*="text-area" i]', 'div[class*="textbox" i]',
  '[contenteditable="true"]', 'p[contenteditable]', '[data-editor]', '[data-composer]', 'div.editor',
  // Web-standard
  'div[aria-label*="message" i]', 'div[aria-label*="input" i]'
];
const RESPONSE_SELECTORS = [
 '.ds-markdown', '.ds-markdown--block', 'div[class*="ds-markdown"]',
 'div[class*="markdown"]', '[class*="message-content"]',
 '[class*="assistant"] [class*="content"]', '[class*="answer-content"]',
 '[data-message-author-role="assistant"]', '.prose',
 '[class*="message"][class*="assistant"]', '[class*="message"][class*="ai"]',
 '[class*="message"]',
];
const API_PATTERNS = ['/chat/completions', '/completion', '/chat/completion'];

// ─── Утилиты ────────────────────────────────────────────────
function log(...a) { console.log(...a); }
function debugLog(...a) { if (VERBOSE) console.log(...a); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function ensureDirSync(d) { try { fs.mkdirSync(d, { recursive: true }); } catch {} }

function shortenPromptForRetry(prompt, attempt) {
 if (typeof prompt !== 'string') return prompt;
 const lines = prompt.split('\n');
 if (lines.length <= 6) {
   const hardMax = Math.max(OVERSIZE_RETRY_MIN_CHARS, Math.floor(prompt.length * Math.pow(OVERSIZE_RETRY_KEEP_RATIO, attempt)));
   return prompt.slice(0, hardMax).trimEnd();
 }
 const header = lines.slice(0, Math.min(6, lines.length)).join('\n');
 const body = lines.slice(Math.min(6, lines.length)).join('\n');
 const targetLen = Math.max(OVERSIZE_RETRY_MIN_CHARS, Math.floor(body.length * Math.pow(OVERSIZE_RETRY_KEEP_RATIO, attempt)));
 return `${header}\n\n[TRUNCATED_FOR_SUBMIT_RETRY: prompt shortened after silent oversize submit block]\n\n${body.slice(0, targetLen).trimEnd()}`;
}

// Отключает CSS-анимации и transition для стабилизации DOM
async function disableAnimations(page) {
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.textContent = `
      *, *::before, *::after {
        animation-duration: 0s !important;
        animation-delay: 0s !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
      }
    `;
    document.head.appendChild(style);
    // Удаляем классы анимаций/typewriter
    document.querySelectorAll('[class*="typewriter"], [class*="typing"], [class*="cursor"], [class*="animation"]').forEach(el => {
      el.classList.remove('typewriter', 'typing', 'cursor', 'animation');
      el.style.animation = 'none';
    });
  });
}

// Проверяет, жив ли браузер по wsEndpoint (health check)
async function isBrowserAlive(wsEndpoint) {
  try {
    const browser = await puppeteer.connect({
      browserWSEndpoint: wsEndpoint,
      timeout: 5000 // короткий таймаут для быстрой проверки
    });
    const pages = await browser.pages();
    await browser.disconnect();
    return pages.length > 0;
  } catch (err) {
    debugLog('Health check failed:', err.message);
    return false;
  }
}

// Retry logic for transient failures
async function withRetry(fn, options = {}) {
   const { maxRetries = 3, baseDelay = 1000, retryOn = [404, 429, 500, 502, 503] } = options;
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === maxRetries) throw err;
      const shouldRetry = retryOn.includes(err.statusCode) ||
                          err.message.includes('timeout') ||
                          err.message.includes('ECONNRESET') ||
                          err.message.includes('network') ||
                          err.message.includes('EAI_AGAIN') ||
                          err.message.includes('Rate limit');
      if (!shouldRetry) throw err;
      const delay = baseDelay * Math.pow(2, i);
      debugLog(`⚠️ Retry ${i+1}/${maxRetries} after ${delay}ms: ${err.message}`);
      await sleep(delay);
    }
  }
}

// ─── Демон и оптимизации ────────────────────────────────────────
function shouldExitAsDeepSeekUnreachable(err) {
  const msg = String(err?.message || err || '');
  const code = String(err?.code || '');
  return (
    /Демон не запущен|Демон недоступен|ECONNREFUSED|ETIMEDOUT|ERR_CONNECTION_REFUSED|ERR_CONNECTION_CLOSED|ERR_CONNECTION_RESET|ERR_NAME_NOT_RESOLVED|ERR_INTERNET_DISCONNECTED|ERR_NETWORK_CHANGED|ERR_TIMED_OUT|ERR_ADDRESS_UNREACHABLE|ERR_PROXY_CONNECTION_FAILED/i.test(msg) ||
    /ECONNREFUSED|ETIMEDOUT/i.test(code)
  );
}

async function connectToDaemon() {
  let wsEndpoint = '';
  if (fs.existsSync(DAEMON_ENDPOINT_FILE)) {
    wsEndpoint = fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim();
  } else {
    try {
      const daemonSessionPath = getSessionFile('daemon');
      if (fs.existsSync(daemonSessionPath)) {
        const daemonSession = JSON.parse(fs.readFileSync(daemonSessionPath, 'utf8'));
        if (daemonSession?.browserWSEndpoint) {
          wsEndpoint = daemonSession.browserWSEndpoint.trim();
          try { fs.writeFileSync(DAEMON_ENDPOINT_FILE, wsEndpoint); } catch {}
        }
      }
    } catch {}
  }
  if (!wsEndpoint) {
    const err = new Error('Демон не запущен. Запусти: node deepseek-daemon.js');
    err.exitCode = 2;
    throw err;
  }
  log('🔗 Подключаюсь к демону:', wsEndpoint);
  try {
    const browser = await puppeteer.connect({
      browserWSEndpoint: wsEndpoint,
      defaultViewport: null,
    });
    browserConnectionMode = 'daemon';
    return browser;
  } catch (e) {
    // Демон не отвечает — удаляем stale endpoint file
    try { fs.unlinkSync(DAEMON_ENDPOINT_FILE); } catch {}
    const err = new Error(`Демон недоступен: ${e.message}`);
    err.exitCode = 2;
    throw err;
  }
}

// ─── Управление сессиями ────────────────────────────────────

function getSessionFile(name) {
 ensureDirSync(SESSIONS_DIR);
 return path.join(SESSIONS_DIR, `${name}.json`);
}

function loadSession(name) {
 try {
 const f = getSessionFile(name);
 if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
 } catch {}
 return { name, messageCount: 0, created: null, lastUsed: null, chatUrl: null, browserPid: null };
}

function saveSession(name, data) {
 try {
 ensureDirSync(SESSIONS_DIR);
 fs.writeFileSync(getSessionFile(name), JSON.stringify(data, null, 2));
 } catch {}
}

function deleteSession(name) {
 try { fs.unlinkSync(getSessionFile(name)); } catch {}
}

function listSessions() {
 try {
 ensureDirSync(SESSIONS_DIR);
 return fs.readdirSync(SESSIONS_DIR)
 .filter(f => f.endsWith('.json'))
 .map(f => {
 try { return JSON.parse(fs.readFileSync(path.join(SESSIONS_DIR, f), 'utf8')); }
 catch { return null; }
 })
 .filter(Boolean);
 } catch { return []; }
}

// ─── Кэш селекторов ────────────────────────────────────────
const CACHE_FILE = path.join(BASE_DIR, 'working-selectors.json');

// Очистка кэша при каждом запуске (защита от старого мусора)
if (fs.existsSync(CACHE_FILE)) {
  try {
    fs.unlinkSync(CACHE_FILE);
    debugLog('[Cache] working-selectors.json удалён (чистый старт)');
  } catch (e) {}
}

function loadCachedSelectors() {
 try {
 if (fs.existsSync(CACHE_FILE)) return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8')).deepseek || [];
 } catch {}
 return [];
}

function saveCachedSelector(sel) {
 try {
 // Валидация: только чистые CSS-селекторы
 if (!sel || typeof sel !== 'string') return;
 const trimmed = sel.trim();
 if (!trimmed) return;

 // Игнорируем auto-last:, auto-first:, treewalker, body-fallback
 const invalidPrefixes = ['auto-last:', 'auto-first:', 'treewalker', 'body-fallback', '__'];
 if (invalidPrefixes.some(p => trimmed.startsWith(p))) {
   return;
 }

 // Сохраняем только селекторы, которые выглядят как CSS (содержат [a-zA-Z] или начинаются с . # [ *)
 if (!/[a-zA-Z#.[\[]/.test(trimmed)) {
   return;
 }

 const cache = { deepseek: loadCachedSelectors() };
 if (!cache.deepseek.includes(trimmed)) {
   cache.deepseek.unshift(trimmed);
   cache.deepseek = cache.deepseek.slice(0, 20);
   ensureDirSync(path.dirname(CACHE_FILE));
   fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
 }
 } catch {}
}

// ─── Диагностика ────────────────────────────────────────────
async function dumpArtifacts(page, reason) {
 ensureDirSync(BASE_DIR);
 const ts = Date.now();
 const safe = String(reason).replace(/[^a-z0-9]/gi, '_').substring(0, 40);
 try { await page.screenshot({ path: path.join(BASE_DIR, `ds-${safe}-${ts}.png`), fullPage: true }); } catch {}
 try { await fs.promises.writeFile(path.join(BASE_DIR, `ds-${safe}-${ts}.html`), await page.content().catch(() => ''), 'utf8'); } catch {}
}

async function discoverDOM(page) {
 const found = await page.evaluate(() => {
 const r = [];
 for (const el of document.querySelectorAll('div, article, section, p, span')) {
 const t = el.innerText?.trim();
 if (!t || t.length < 30) continue;
 let s = el.tagName.toLowerCase();
 if (el.className && typeof el.className === 'string')
 s += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
 const kids = el.querySelectorAll('div, article, section').length;
 r.push({ s, len: t.length, preview: t.slice(0, 60), density: t.length / (kids + 1) });
 }
 r.sort((a, b) => b.density - a.density);
 return r.slice(0, 4);
 }).catch(() => []);
 if (found.length) {
 log('🔍 DOM:');
 for (const d of found) log(` ${d.s} (${d.len}ch) "${d.preview}"`);
 }
}

// ─── Состояние страницы ─────────────────────────────────────
async function waitUntilReady(page, timeout = 45000) {
 const start = Date.now();
 let i = 0;
 while (Date.now() - start < timeout) {
   i++;

   // Проверяем URL — не на странице логина?
   try {
     const url = page.url();
     if (/login|auth|signup/i.test(url)) {
       throw new Error('Требуется авторизация — запусти с --visible --wait');
     }
   } catch (e) {
     if (e.message && e.message.includes('Требуется авторизация')) throw e;
     // Страница может быть в процессе навигации
   }

   // Ищем composer
   for (const sel of COMPOSER) {
     try {
       const el = await page.$(sel);
       if (el) {
         log(`✅ Composer: ${sel} (${i} checks, ${((Date.now()-start)/1000).toFixed(1)}s)`);
         return sel;
       }
     } catch {}
   }

   // Первые 3 итерации — быстрая проверка (500мс)
   // Потом — стандартная (1с)
   if (i <= 3) {
     log(`⏳ waiting (${i})...`);
     await sleep(500);
   } else {
     await sleep(1000);
   }
 }

 throw new Error(`Not usable after ${timeout}ms`);
}

// ─── Подсчёт сообщений в чате ───────────────────────────────
async function countMessages(page) {
 return page.evaluate(() => {
 // Считаем пары (user + assistant)
 const msgs = document.querySelectorAll(
 '[class*="message"], [data-message-author-role], .ds-markdown'
 );
 return msgs.length;
 }).catch(() => 0);
}

// ─── Браузер ────────────────────────────────────────────────
async function cleanup() {
 try {
   if (browser) {
     if (browserLaunchedByUs) {
       await browser.close().catch(() => {});
       // В обычном happy-path НЕ убиваем процессы по shared profile:
       // daemon использует тот же .profile, и агрессивная зачистка может убить его Chrome.
       // Жёсткий kill остаётся только в recovery/launch-путях, где он нужен осознанно.
     } else {
       // Daemon/session browser: не закрываем сам Chrome, только отключаемся
       try { browser.disconnect(); } catch (e) {}
     }
   }
 } finally {
   browser = null;
   dsPage = null;
 }
}

async function connectToExistingBrowser(session) {
 // Пробуем подключиться к уже запущенному браузеру
 if (session.wsEndpoint) {
 try {
 browser = await puppeteer.connect({ browserWSEndpoint: session.wsEndpoint });
 browserConnectionMode = 'session';
 const pages = await browser.pages();
 dsPage = pages.find(p => p.url().includes('deepseek')) || pages[0];
 if (dsPage) {
 log('🔗 Подключились к существующему браузеру');
 return true;
 }
 } catch {
 log('⚠️ Не удалось подключиться, запускаю новый');
 }
 }
 return false;
}

/**
 * Создает CDP-перехватчик для получения полного ответа от API DeepSeek.
 */
async function setupDeepSeekInterceptor(page) {
  const client = await page.target().createCDPSession();
  await client.send('Network.enable');

  // ═══ Per-request state (private) ═══
  let requestIdCounter = 0;
  let expectedRequestIds = new Set();
  let windowOpen = false;
  let pendingResolve = null;
  let pendingTimer = null;
  let responseState = { resolved: false, result: null };

  function parseDeepSeekBody(raw) {
    if (!raw || typeof raw !== 'string') return null;
    const trimmed = raw.trim();
    if (!trimmed) return null;

    // Check if this is a DeepSeek custom event-stream format
    const isDeepSeekEvent = trimmed.includes('event:') || trimmed.includes('"v":');
    
    if (isDeepSeekEvent || trimmed.startsWith('data:') || trimmed.startsWith(':')) {
      return parseDeepSeekEventStream(raw);
    }

    // Fallback: try standard OpenAI JSON format
    try {
      const obj = JSON.parse(trimmed);
      const msg = obj.choices?.[0]?.message?.content;
      if (msg) return msg;
      const delta = obj.choices?.[0]?.delta?.content;
      if (delta) return delta;
      if (obj.text) return obj.text;
      if (obj.output) return obj.output;
      if (obj.content) return obj.content;
      debugLog('[CDP] Unknown JSON keys:', Object.keys(obj));
      return null;
    } catch {
      debugLog('[CDP] Body is not valid JSON, length:', trimmed.length);
      return null;
    }
  }

  /**
   * Parse DeepSeek custom event-stream format.
   * 
   * Observed format:
   *   data: {"v":{"response":{"fragments":[{"content":"2","stage_id":1}]}}
   *   data: {"p":"response/fragments/-1/content","o":"APPEND","v":" +"}
   *   data: {"v":" "}
   *   data: {"v":"4"}
   *   data: {"p":"response/status","o":"SET","v":"FINISHED"}
   */
  function parseDeepSeekEventStream(raw) {
    const lines = raw.split('\n');
    let accumulated = '';

    for (const line of lines) {
      if (!line.startsWith('data:') || line.startsWith('data: []')) continue;
      const payload = line.slice(5).trim();
      if (!payload || payload === '[DONE]') continue;

      try {
        const obj = JSON.parse(payload);

        // Skip non-content operations (BATCH, SET status, etc.)
        if (['BATCH', 'SET', 'REMOVE', 'DELETE'].includes(obj.o)) continue;

        // Case 1: direct string value {"v":"text"}
        if (typeof obj.v === 'string') {
          accumulated += obj.v;
          continue;
        }

        // Case 2: fragment append {"p":"response/fragments/...","o":"APPEND","v":"text"}
        if (obj.p && obj.o === 'APPEND' && typeof obj.v === 'string') {
          accumulated += obj.v;
          continue;
        }

        // Case 3: full response object {"v":{"response":{...}}}
        if (obj.v && typeof obj.v === 'object' && obj.v.response) {
          const resp = obj.v.response;
          if (resp.accumulated_content) {
            return resp.accumulated_content; // Return immediately
          }
          // 3b: fragments — collect FIRST fragment content as seed
          if (resp.fragments && Array.isArray(resp.fragments)) {
            const fragment = resp.fragments.find(f => f.content);
            if (fragment && accumulated.length === 0) { // Only seed if empty
              accumulated = fragment.content;
            }
          }
        }

        // Case 4: Standard OpenAI format inside event stream
        const msg = obj.choices?.[0]?.message?.content;
        if (msg) return msg;
        const delta = obj.choices?.[0]?.delta?.content;
        if (delta) {
          accumulated += delta;
        }
      } catch {
        continue;
      }
    }

    return accumulated.length > 0 ? accumulated : null;
  }

  function doResolve(result) {
    if (pendingResolve) {
      const r = pendingResolve;
      pendingResolve = null;
      if (pendingTimer) { clearTimeout(pendingTimer); pendingTimer = null; }
      r(result);
    }
  }

  function cleanupState() {
    expectedRequestIds.clear();
    responseState = { resolved: false, result: null };
    if (pendingTimer) { clearTimeout(pendingTimer); pendingTimer = null; }
    pendingResolve = null;
    windowOpen = false;
  }

  function prepareForRequest() {
    if (pendingResolve) {
      pendingResolve = null;
      if (pendingTimer) { clearTimeout(pendingTimer); pendingTimer = null; }
    }
    responseState = { resolved: false, result: null };
    requestIdCounter++;
    windowOpen = true;
    debugLog(`[CDP] prepareForRequest: correlation #${requestIdCounter}`);
    return requestIdCounter;
  }

  client.on('Network.requestWillBeSent', async (event) => {
    const url = event.request.url;
    if ((url.includes('/chat/completion') || url.includes('/completion'))
        && event.request.method === 'POST') {
      if (!windowOpen) return;
      if (responseState.resolved) return;
      try {
        if (event.request.hasPostData && event.request.postData
            && typeof event.request.postData === 'string'
            && event.request.postData.length < 10) return;
      } catch {}
      windowOpen = false;
      expectedRequestIds.add(event.requestId);
      debugLog(`[CDP] caught: ${event.requestId}`);
    }
  });

  client.on('Network.loadingFinished', async (event) => {
    if (!expectedRequestIds.has(event.requestId)) return;
    if (responseState.resolved) return;
    try {
      debugLog(`[CDP] loadingFinished: ${event.requestId}`);
      const resp = await client.send('Network.getResponseBody', { requestId: event.requestId });
      let body = resp.body;
      if (resp.base64Encoded) body = Buffer.from(body, 'base64').toString('utf8');
      debugLog(`[CDP] Тело: ${body.length} chars`);
      const parsedText = parseDeepSeekBody(body);
      if (parsedText) debugLog(`[CDP] Текст: ${parsedText.length} chars`);
      else debugLog(`[CDP] Parse returned null — format not recognized`);
      if (responseState.resolved) return;
      responseState.resolved = true;
      responseState.result = { raw: body, text: parsedText, format: parsedText ? 'parsed' : 'raw', correlation: requestIdCounter };
      doResolve(responseState.result);
      expectedRequestIds.delete(event.requestId);
    } catch (err) {
      debugLog(`[CDP] Ошибка: ${err.message}`);
      if (responseState.resolved) return;
      responseState.resolved = true;
      responseState.result = { raw: null, text: null, format: 'failed', error: err.message };
      doResolve(responseState.result);
      expectedRequestIds.delete(event.requestId);
    }
  });

  client.on('Network.loadingFailed', (event) => {
    if (!expectedRequestIds.has(event.requestId)) return;
    if (responseState.resolved) return;
    debugLog(`[CDP] requestFailed: ${event.requestId}`);
    responseState.resolved = true;
    responseState.result = { raw: null, text: null, format: 'failed', error: 'network_failed' };
    doResolve(responseState.result);
    expectedRequestIds.delete(event.requestId);
  });

  async function waitForResponse(timeoutMs = 120000) {
    if (responseState.resolved && responseState.result) {
      cleanupState();
      return responseState.result;
    }
    return new Promise((resolve) => {
      pendingResolve = resolve;
      pendingTimer = setTimeout(() => {
        if (pendingResolve) { pendingResolve = null; if (pendingTimer) { clearTimeout(pendingTimer); pendingTimer = null; } resolve(null); }
      }, timeoutMs);
    });
  }

  function consumeResponse() {
    if (!responseState.resolved || !responseState.result) return null;
    const r = responseState.result;
    cleanupState();
    return r;
  }

  return { prepareForRequest, waitForResponse, consumeResponse, cleanupState, get state() { return { resolved: responseState.resolved, expectedCount: expectedRequestIds.size, correlation: requestIdCounter }; } };
}




async function ensureBrowser(session, diag = null) {
 debugLog(`[DEBUG] ensureBrowser() start, session:`, session);
 debugLog(`[DEBUG] browser=${!!browser}, dsPage=${!!dsPage}`);
 // Уже подключены — проверяем жива ли страница
 if (browser && dsPage) {
   try {
     const url = await dsPage.url();
     debugLog(`[DEBUG] Existing page alive, url=${url.substring(0, 50)}`);
     return dsPage;
   } catch (e) {
     debugLog(`[DEBUG] Existing page dead: ${e.message}`);
     browser = null;
     dsPage = null;
   }
 } else {
   debugLog(`[DEBUG] No existing browser/page, will launch new`);
 }

 // ═══ Попытка 1: подключиться к демону (только при явном --daemon, либо когда НЕ нужен visible browser) ═══
 const shouldUseDaemon = useDaemon || (!isVisible && fs.existsSync(DAEMON_ENDPOINT_FILE));
 debugLog(`[DEBUG] Checking daemon: useDaemon=${useDaemon}, isVisible=${isVisible}, shouldUseDaemon=${shouldUseDaemon}, DAEMON_ENDPOINT_FILE exists=${fs.existsSync(DAEMON_ENDPOINT_FILE)}`);
 if (diag) diag.start('DAEMON_CONNECT');
 if (shouldUseDaemon) {
   try {
     debugLog('[DEBUG] Connecting to daemon...');
     browser = await connectToDaemon();
     const pages = await browser.pages();

     if (session?.chatUrl && !newChat) {
       const exactSessionPage = pages.find(p => {
         try { return p.url() === session.chatUrl; } catch { return false; }
       });
       dsPage = exactSessionPage || pages.find(p => {
         try { return p.url().includes('deepseek'); } catch { return false; }
       }) || pages[0] || await browser.newPage();

       const currentUrl = dsPage.url();
       if (currentUrl !== session.chatUrl) {
         if (!exactSessionPage) {
           log('⚠️ Session fallback used: exact chat tab not found, navigating to saved chatUrl');
         }
         log(`📂 Восстанавливаю чат сессии: ${session.chatUrl.substring(0, 50)}`);
         await dsPage.goto(session.chatUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
       }
     } else {
       dsPage = pages.find(p => {
         try { return p.url().includes('deepseek'); } catch { return false; }
       }) || pages[0] || await browser.newPage();

       // Если страница не на DeepSeek — переходим
       const currentUrl = dsPage.url();
       if (!currentUrl.includes('deepseek')) {
         log('📍 Навигация на DeepSeek...');
         await dsPage.goto(DS_URL, { waitUntil: 'domcontentloaded', timeout: 20000 });
       }
     }

     log(`🔗 Подключился к демону (URL: ${dsPage.url().substring(0, 50)})`);
     if (diag) diag.succeed('DAEMON_CONNECT', { url: dsPage.url() });
     return dsPage;
   } catch (e) {
     debugLog(`[DEBUG] Daemon connection failed: ${e.message}`);
     if (diag) diag.fail('DAEMON_CONNECT', e.message);
     if (useDaemon) {
       // При --daemon НЕ падаем в fallback
       throw new Error('Демон недоступен. Запусти: cd ~/.openclaw/workspace/skills/ai-orchestrator && node deepseek-daemon.js');
     } else {
       // Демон найден, но не отвечает — логируем и продолжаем
       log(`⚠️ Демон найден, но недоступен: ${e.message}`);
       // Daemon auto-recovery: пробуем перезапустить через PM2
       try {
         log('🔄 Daemon auto-recovery: pm2 restart...');
         require('child_process').execSync('pm2 restart deepseek-daemon', { stdio: 'pipe' });
         log('⏳ Ждём 8 сек поднятия...');
         await new Promise(r => setTimeout(r, 8000));
         const newEp = fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim();
         log(`🔗 Повторное подключение: ${newEp.substring(0, 60)}...`);
         browser = await puppeteer.connect({ browserWSEndpoint: newEp, defaultViewport: null });
         const pages = await browser.pages();
         dsPage = pages.find(p => { try { return p.url().includes('deepseek'); } catch { return false; } }) || pages[0];
         if (dsPage) {
           log(`✅ Демон восстановлен (URL: ${dsPage.url().substring(0, 60)})`);
           return dsPage;
         }
       } catch (err) {
         log(`⚠️ Auto-recovery не удался: ${err.message}`);
       }
     }
   }
 } else {
   if (diag) diag.skip('DAEMON_CONNECT', 'daemon mode not used');
 }

 // ═══ Попытка 2: подключиться к существующему браузеру через сессию ═══
 if (diag) diag.start('SESSION_RESTORE');
 if (session) {
   const wsEndpoint = session.wsEndpoint;
   if (wsEndpoint) {
     if (await isBrowserAlive(wsEndpoint)) {
       if (await connectToExistingBrowser(session)) {
         if (diag) diag.succeed('SESSION_RESTORE', { url: dsPage.url() });
         return dsPage;
       }
     } else {
       debugLog('⚠️ Сессия неактивна, удаляем файл сессии');
       const sessionPath = path.join(BASE_DIR, '.sessions', sessionName + '.json');
       try { fs.unlinkSync(sessionPath); } catch (e) { debugLog('Ошибка удаления сессии:', e.message); }
     }
   }
   if (diag) diag.skip('SESSION_RESTORE', 'no session or session dead');
 } else {
   if (diag) diag.skip('SESSION_RESTORE', 'no session requested');
 }

 // ═══ Попытка 3: запустить новый браузер ═══
 if (diag) diag.start('BROWSER_LAUNCH');  // NOTE: nested within parent's BROWSER_LAUNCH phase
 await cleanup();
 ensureDirSync(PROFILE_DIR);

 // Для одноразовых запросов (не сессий) убиваем процессы и очищаем locks
 if (!session && shouldClose) {
   await killChromeProcessesForProfile(PROFILE_DIR);
   await new Promise(resolve => setTimeout(resolve, 1000)); // даем время на завершение
 }

 const launchOptions = {
   headless: isVisible ? false : 'new',
   userDataDir: PROFILE_DIR,
   args: [
     '--no-sandbox', '--disable-setuid-sandbox',
     '--disable-blink-features=AutomationControlled',
     '--no-first-run', '--no-default-browser-check',
     '--disable-gpu', '--window-size=1280,800',
   ],
 };
 if (executablePath) {
   launchOptions.executablePath = executablePath;
 }

 log('🚀 Запуск нового браузера...');
 browser = await launchWithTimeout(launchOptions, TIMEOUT_BROWSER);
 browserLaunchedByUs = true;
 browserConnectionMode = 'local';

 const pages = await browser.pages();
 dsPage = pages[0] || await browser.newPage();

 await dsPage.setUserAgent(
   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
 );
 await dsPage.setViewport({ width: 1280, height: 800 });
 await dsPage.evaluateOnNewDocument(() => {
   Object.defineProperty(navigator, 'webdriver', { get: () => false });
 });

 // Логируем только API
 dsPage.on('response', resp => {
   const url = resp.url();
   if (API_PATTERNS.some(p => url.includes(p)))
     debugLog(`🌐 API ${resp.status()}: ${url.split('?')[0].split('/').pop()}`);
 });

 // Открываем DeepSeek (или сохранённый чат)
 if (diag) diag.start('PAGE_NAVIGATE');
 if (session?.chatUrl && !newChat) {
   log(`📂 Открываю чат: ${session.chatUrl.substring(0, 50)}`);
   await dsPage.goto(session.chatUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
 } else {
   log('📍 Открываем DeepSeek...');
   await dsPage.goto(DS_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
 }
 if (diag) diag.succeed('PAGE_NAVIGATE', { url: dsPage.url() });

 // Отключаем анимации для стабилизации DOM
 await disableAnimations(dsPage);
 await sleep(150); // достаточно для стабилизации DOM

 // Авторизация если нужно
 if (isVisible && waitForAuth) {
   log('\n⚠️ Авторизуйтесь и нажмите Enter...');
   if (process.stdin.isTTY) {
     await new Promise(r => { process.stdin.resume(); process.stdin.once('data', () => r()); });
   } else {
     await sleep(60000);
   }
 }

 // Сохраняем wsEndpoint для будущих подключений (сессии)
 if (session) {
   session.wsEndpoint = browser.wsEndpoint();
   saveSession(session.name, session);
 }

 return dsPage;
}

// ─── Новый чат ──────────────────────────────────────────────
async function startNewChat(page, forceNewSession = false) {
 log('🆕 Начинаю новый чат...');

 // Проверяем, находимся ли мы уже в чате
 // Если --new-chat НЕ запрошен И это не новая сессия — пропускаем.
 // Новая сессия всегда начинается с нового чата, даже если daemon был на старом.
 try {
   const url = page.url();
   if (url.includes('/a/chat/s/') && !newChat && !forceNewSession) {
     log('🆕 Уже в чате — продолжаем в этом');
     return;
   }
   if (url.includes('/a/chat/s/') && forceNewSession) {
     log('⚠️ Daemon на старом чате, принудительно создаю новый для новой сессии');
   }
 } catch (e) {
   // ignore, продолжим
 }

 const clicked = await page.evaluate(() => {
 // Ищем кнопку "New chat"
 const candidates = document.querySelectorAll('button, [role="button"], a');
 for (const el of candidates) {
 const text = (el.textContent || el.innerText || '').trim().toLowerCase();
 const aria = (el.getAttribute('aria-label') || '').toLowerCase();
 if ((text.includes('new chat') || text.includes('новый чат') || aria.includes('new chat'))
 && el.offsetWidth > 0) {
 el.click();
 return text || aria;
 }
 }
 return null;
 }).catch(() => null);

 if (clicked) {
 log(`🆕 New chat: "${clicked}"`);
 await sleep(1500);
 } else {
 // Fallback: goto main page
 try {
   await page.goto(DS_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
 } catch (e) {
   if (!String(e.message || '').includes('ERR_ABORTED')) throw e;
   log('⚠️ Навигация на новый чат была прервана UI-переходом, продолжаю');
 }
 await sleep(1500);
 }
}

// ─── Включение Search ───────────────────────────────────────
async function clickToggleByLabel(page, label, options = {}) {
 const normalizedLabel = String(label || '').trim().toLowerCase();
 const targetState = options.targetState || 'enable';
 const result = await page.evaluate(({ normalizedLabel, targetState }) => {
   const isVisible = (el) => !!(el && el.offsetWidth > 0 && el.offsetHeight > 0);
   const normalize = (s) => String(s || '').trim().toLowerCase();
   const candidates = [...document.querySelectorAll('button, [role="button"], div, span, a')]
     .filter(el => isVisible(el))
     .filter(el => normalize(el.textContent) === normalizedLabel || normalize(el.getAttribute('aria-label')) === normalizedLabel);

   function findClickable(el) {
     let cur = el;
     for (let i = 0; i < 5 && cur; i++, cur = cur.parentElement) {
       if (!isVisible(cur)) continue;
       const cls = typeof cur.className === 'string' ? cur.className : '';
       const role = normalize(cur.getAttribute('role'));
       if (cur.tagName === 'BUTTON' || role === 'button' || cls.includes('ds-toggle-button') || cls.includes('ds-atom-button') || cls.includes('_9f2341b') || cls.includes('dfb78875')) {
         return cur;
       }
     }
     return el;
   }

   for (const raw of candidates) {
     if (raw.closest('[data-role="measure"]')) continue;
     const el = findClickable(raw);
     const cls = typeof el.className === 'string' ? el.className : '';
     const selected = cls.includes('ds-toggle-button--selected') || cls.includes('_31a22b0') || normalize(el.getAttribute('aria-selected')) === 'true' || normalize(el.getAttribute('aria-pressed')) === 'true';
     if ((targetState === 'enable' && selected) || (targetState === 'disable' && !selected)) {
       return { changed: false, already: true, text: normalize(el.textContent), cls };
     }
     el.click();
     return { changed: true, already: false, text: normalize(el.textContent), cls };
   }
   return null;
 }, { normalizedLabel, targetState }).catch(() => null);

 if (result?.changed) {
   await sleep(600);
 }
 return result;
}

async function ensureExpertMode(page) {
 if (preferredChatMode !== 'expert') {
   debugLog(`⚙️ preferredChatMode=${preferredChatMode}, skip Expert enforcement`);
   return false;
 }

 log('🎯 Проверяю режим DeepSeek: Expert');
 const result = await clickToggleByLabel(page, 'Expert', { targetState: 'enable' });
 if (!result) {
   log('⚠️ Переключатель Expert не найден');
   return false;
 }
 if (result.already) {
   log('🎯 Expert уже активен');
   return true;
 }
 log('🎯 Переключил DeepSeek в Expert');
 return true;
}

async function enableSearch(page) {
 log('🔍 Активирую Search...');
 const result = await clickToggleByLabel(page, 'Search', { targetState: 'enable' });
 if (result) { log(`🔍 Search: ${result.already ? 'уже активен' : 'включён'}`); }
 else log('⚠️ Кнопка Search не найдена');
}

async function enableDeepThink(page) {
 log('🧠 Активирую DeepThink...');
 const result = await clickToggleByLabel(page, 'DeepThink', { targetState: 'enable' });
 if (result) { log(`🧠 DeepThink: ${result.already ? 'уже активен' : 'включён'}`); }
 else log('⚠️ Кнопка DeepThink не найдена');
}

// ─── Отправка ───────────────────────────────────────────────
async function inspectSubmitOutcome(page, composerSelector, prompt, timeoutMs = 5000) {
 const started = Date.now();
 let sawExpectedRequest = false;
 while (Date.now() - started < timeoutMs) {
   const network = cdpInterceptor?.consumeResponse ? cdpInterceptor.consumeResponse() : null;
   if (network) sawExpectedRequest = true;
   const snapshot = await page.evaluate((sel, promptStart) => {
     const el = document.querySelector(sel);
     const value = el ? ('value' in el ? el.value : (el.textContent || '')) : '';
     const body = document.body?.innerText || '';
     return {
       valueLen: value.length,
       userPromptVisible: !!(promptStart && body.includes(promptStart)),
       articleCount: document.querySelectorAll('article').length,
       url: location.href,
     };
   }, composerSelector, prompt.slice(0, 40)).catch(() => ({ valueLen: 0, userPromptVisible: false, articleCount: 0, url: page.url() }));

   const textareaCleared = snapshot.valueLen < Math.max(16, Math.floor(prompt.length * 0.05));
   const accepted = sawExpectedRequest || textareaCleared || snapshot.userPromptVisible || snapshot.articleCount > 0;
   if (accepted) {
     return {
       accepted: true,
       reason: sawExpectedRequest ? 'network-request' : textareaCleared ? 'textarea-cleared' : snapshot.userPromptVisible ? 'prompt-visible' : 'article-visible',
       sawExpectedRequest,
       ...snapshot,
     };
   }
   await sleep(150);
 }

 const finalSnapshot = await page.evaluate((sel, promptStart) => {
   const el = document.querySelector(sel);
   const value = el ? ('value' in el ? el.value : (el.textContent || '')) : '';
   const body = document.body?.innerText || '';
   return {
     valueLen: value.length,
     userPromptVisible: !!(promptStart && body.includes(promptStart)),
     articleCount: document.querySelectorAll('article').length,
     url: location.href,
   };
 }, composerSelector, prompt.slice(0, 40)).catch(() => ({ valueLen: 0, userPromptVisible: false, articleCount: 0, url: page.url() }));

 return {
   accepted: false,
   reason: 'silent-submit-block',
   sawExpectedRequest,
   ...finalSnapshot,
 };
}

async function sendPrompt(page, composerSelector, prompt) {
 let workingPrompt = prompt;
 for (let attempt = 0; attempt <= OVERSIZE_MAX_RETRIES; attempt++) {
   log(`📝 "${workingPrompt.substring(0, 60)}..."`);

   // ═══ CDP: prepare ДО отправки ═══
   if (cdpInterceptor) {
     const corrId = cdpInterceptor.prepareForRequest();
     debugLog(`[CDP] Prepared for request, correlation #${corrId}`);
   }

   await ensureExpertMode(page);
   if (searchMode || /\[РЕЖИМ: ПОИСК/i.test(workingPrompt)) await enableSearch(page);
   if (thinkMode || /\[РЕЖИМ: DEEP THINK/i.test(workingPrompt)) await enableDeepThink(page);

   const element = await page.waitForSelector(composerSelector, { visible: true, timeout: 10000 });
   const textBefore = workingPrompt;

   await element.evaluate((el, text) => {
   el.focus();
   if (el.isContentEditable || el.getAttribute('contenteditable') === 'true') {
     el.textContent = text;
     el.dispatchEvent(new Event('input', { bubbles: true }));
     el.dispatchEvent(new Event('change', { bubbles: true }));
   } else if (el instanceof HTMLTextAreaElement || el instanceof HTMLInputElement) {
     const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
     const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
     if (setter) {
       setter.call(el, text);
     } else {
       el.value = text;
     }
     el.dispatchEvent(new Event('input', { bubbles: true }));
     el.dispatchEvent(new Event('change', { bubbles: true }));
   } else {
     el.textContent = text;
     el.dispatchEvent(new Event('input', { bubbles: true }));
   }

   const enter = { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true };
   el.dispatchEvent(new KeyboardEvent('keydown', enter));
   el.dispatchEvent(new KeyboardEvent('keypress', enter));
   el.dispatchEvent(new KeyboardEvent('keyup', enter));

   let btn = null;
   for (const sel of ['button[type="submit"]', '[data-testid="send"]', 'button[aria-label*="send" i]']) {
   const b = (el.closest('form') || document).querySelector(sel);
   if (b && b.offsetWidth > 0 && !b.disabled) { b.click(); btn = sel; break; }
   }
   if (!btn) {
   const nearby = el.parentElement?.querySelector('button, [role="button"]');
   if (nearby && nearby.offsetWidth > 0 && !nearby.disabled) { nearby.click(); btn = 'nearby'; }
   }
   const len = (el.value || el.textContent || '').length;
   return { len, btn };
   }, workingPrompt);

   await sleep(20);
   const outcome = await inspectSubmitOutcome(page, composerSelector, workingPrompt, 5000);
   if (outcome.accepted) {
     return { textBefore, promptUsed: workingPrompt, shortened: attempt > 0, submitOutcome: outcome };
   }

   log(`⚠️ Submit did not actually leave the page (${outcome.reason}); promptLen=${workingPrompt.length}; valueLen=${outcome.valueLen}; url=${outcome.url}`);
   if (attempt >= OVERSIZE_MAX_RETRIES || workingPrompt.length <= OVERSIZE_RETRY_MIN_CHARS) {
     const err = new Error(`DEEPSEEK_SUBMIT_BLOCKED_OVERSIZE_PROMPT: silent submit block after ${attempt + 1} attempt(s); final promptLen=${workingPrompt.length}`);
     err.exitCode = 3;
     err.submitOutcome = outcome;
     throw err;
   }
   workingPrompt = shortenPromptForRetry(workingPrompt, attempt + 1);
   log(`✂️ Retry with shortened prompt: newLen=${workingPrompt.length} (attempt ${attempt + 1}/${OVERSIZE_MAX_RETRIES})`);
   await sleep(500);
 }
}

// ─── Чтение ответа ──────────────────────────────────────────
async function getTexts(page, selectors, prompt, opts = {}) {
 const minLen = opts.minLen || 50; // порог символов
 const results = [];
 
 // 1. Прямые селекторы: используем $$eval (один вызов, безопасно)
 for (const sel of selectors) {
   try {
     const texts = await page.$$eval(sel, (elements, prompt, minLen) => {
       return elements
         .filter(el => {
           if (el.closest('.sidebar, nav, aside, .history, .conversation-list, [class*="sidebar"], [class*="nav"], [class*="history"], [class*="list"][class*="conversation"]')) return false;
           if (el.closest('textarea, [contenteditable], [role="textbox"], [data-editor], div[class*="input"], div[class*="composer"]')) return false;
           const txt = el.innerText?.trim();
           return txt && txt.length >= minLen;
         })
         .map(el => el.innerText.trim())
         .filter(txt => txt.length >= minLen)
         .slice(0, 1); // только первый/наилучший
     }, prompt, minLen);
     
     if (texts.length > 0) {
       results.push({ selector: sel, text: texts[0] });
     }
   } catch (e) {
     // Detached frames ожидаемы при DOM churn
   }
 }
 
 // 2. Если не нашли — auto-last с ретраями (защита от detached frame)
 if (results.length === 0) {
   try {
     const best = await extractWithRetry(page, prompt, { minLen });
     if (best) results.push(best);
   } catch (e) {
     // Detached frames ожидаемы
   }
 }
 
 return results;
}

function isValid(t, minLen = 50, prompt = '') {
 if (!t || t.trim().length < minLen) return false;
 const trimmed = t.trim();
 const promptTrimmed = (prompt || '').trim();
 if (/captcha|verify you are human|rate limit/i.test(trimmed)) return false;
 if (promptTrimmed) {
   if (trimmed === promptTrimmed) return false;
   if (Math.abs(trimmed.length - promptTrimmed.length) < 10 && trimmed.startsWith(promptTrimmed.slice(0, 20))) return false;
 }
 return true;
}

// ─── Извлечение с ретраями (защита от detached Frame) ─────────────────────
async function extractWithRetry(page, prompt, opts = {}) {
 const minLen = opts.minLen || 3;
 const maxRetries = opts.maxRetries || 3;
 for (let i = 0; i < maxRetries; i++) {
   try {
     return await page.evaluate((prompt, minLen) => {
       let candidates = [];
       const byRole = document.querySelectorAll('[data-message-author-role="assistant"]');
       if (byRole.length) candidates = Array.from(byRole);
       
       if (candidates.length === 0) {
         const classSelectors = '[class*="assistant"], [class*="ai"], [class*="bot"], [class*="message"]';
         candidates = Array.from(document.querySelectorAll(classSelectors));
       }
       
       const filtered = candidates.filter(el => {
         if (el.closest('.sidebar, nav, aside, .history, .conversation-list, [class*="sidebar"], [class*="nav"], [class*="history"], [class*="list"][class*="conversation"]')) return false;
         if (el.closest('textarea, [contenteditable], [role="textbox"], [data-editor], div[class*="input"], div[class*="composer"]')) return false;
         const txt = el.innerText?.trim();
         if (!txt || txt.length < minLen) return false;
         if (txt.length < 100) return true; // короткие — без density check
         const kids = el.querySelectorAll('div, article, section').length;
         const density = txt.length / (kids + 1);
         return density > 30;
       });
       
       if (filtered.length === 0) return null;
       
       const last = filtered[filtered.length - 1];
       const text = last.innerText.trim().slice(0, 5000);
       
       if (prompt && text.length > 0 && Math.abs(text.length - prompt.length) < 10) {
         if (text.startsWith(prompt.substring(0, 20))) return null;
       }
       
       return {
         selector: `auto-last:${last.tagName.toLowerCase()}${last.className ? '.'+last.className.split(/\s+/)[0] : ''}`,
         text: text
       };
     }, prompt, minLen);
   } catch (err) {
     if (err.message.includes('detached Frame') || err.message.includes('Execution context was destroyed')) {
       // Detached frames ожидаемы при DOM churn — не логируем как проблему
       await new Promise(r => setTimeout(r, 500)); // было 2000ms — оптимизировано
     } else {
       throw err;
     }
   }
 }
 return null;
}

// ─── Извлечение ответа из DOM (чистый текст) ───────────────────────────────
async function extractAnswerFromDOM(page, textBefore, opts = {}) {
 const minLen = opts.minLen || 50;
 try {
   // Ищем блоки ответов ассистента
   const answerText = await page.evaluate((minLen) => {
     // Приоритет 1: сообщения с атрибутом data-message-author-role="assistant"
     let blocks = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
     
     // Приоритет 2: классы, связанные с ответами ассистента
     if (blocks.length === 0) {
       const classSelectors = [
         '.ds-markdown',
         '.markdown-body',
         'div[class*="assistant"]:not([class*="user"])',
         'div[class*="ai"]:not([class*="user"])',
         'div[class*="bot"]:not([class*="user"])',
         'div[class*="response"]',
         'article'
       ];
       for (const sel of classSelectors) {
         const els = document.querySelectorAll(sel);
         if (els.length) blocks.push(...Array.from(els));
       }
     }
     
     // Убираем интерфейсные элементы и пользовательские сообщения
     const filtered = blocks.filter(el => {
       // Исключаем risen через родителя
       if (el.closest('textarea, [contenteditable], [role="textbox"], [data-editor], div[class*="input"], div[class*="composer"], nav, aside, .sidebar, .header, .footer, [class*="toolbar"]')) {
         return false;
       }
       // Исключаем пользовательские сообщения (role=user)
       if (el.closest('[data-message-author-role="user"]')) {
         return false;
       }
       const txt = el.innerText?.trim();
       return txt && txt.length >= minLen;
     });
     
     if (filtered.length === 0) return null;
     
     // Берем самый последний блок (текущий ответ)
     const lastMessage = filtered[filtered.length - 1];
     return lastMessage.innerText.trim();
   }, minLen);
   
   if (!answerText || answerText.length < minLen) return null;
   
   // Убираем промпт если есть
   let cleaned = answerText;
   if (textBefore && answerText.includes(textBefore)) {
     cleaned = answerText.replace(textBefore, '').trim();
   }
   if (textBefore && cleaned.trim() === textBefore.trim()) {
     return null;
   }
   if (cleaned.length < minLen && answerText.length > 100) {
     const ratio = textBefore ? (textBefore.length / answerText.length) : 0;
     if (ratio < 0.3) {
       cleaned = answerText.slice(Math.floor(answerText.length * 0.3)).trim();
     }
   }
   if (textBefore && cleaned.startsWith(textBefore.slice(0, 20)) && Math.abs(cleaned.length - textBefore.length) < 10) {
     return null;
   }
   return cleaned.length >= minLen ? cleaned : null;
 } catch (e) {
   return null;
 }
}

// ─── Обработка кнопки "Продолжить" ─────────────────────────────────────────
/**
 * Проверяет и кликает кнопку "Continue generating" / "Продолжить" если она есть.
 * Возвращает дополнительный контент (пустую строку если кнопки нет или таймаут).
 * @param {import('puppeteer').Page} page
 * @param {string} existingText — уже извлечённый текст (чтобы отличить новое)
 * @returns {Promise<string>}追加 текст или пустая строка
 */
// Helper: extract the last/best assistant message text from the page
async function extractBestText(page, minLength = 0) {
  return page.evaluate((minLen) => {
    const els = document.querySelectorAll('[class*="message"], [class*="content"], [class*="answer"], article, main');
    let best = { text: '', len: 0 };
    for (const el of els) {
      const t = (el.textContent || '').trim();
      if (t.length > best.len && t.length >= minLen) best = { text: t, len: t.length };
    }
    return best;
  }, minLength);
}

async function handleContinueButton(page, existingText) {
  // ═══ 1. Поиск кнопки — один evaluate() ═══
  const continueBtnData = await page.evaluate(() => {
    const allElements = document.querySelectorAll('button, [role="button"], a');
    for (const el of allElements) {
      if (el.offsetWidth === 0 || el.offsetHeight === 0) continue;
      const rect = el.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) continue;
      const text = (el.textContent || el.innerText || '').trim().toLowerCase();
      const isContinue = text.includes('continue') || text.includes('продолжить') ||
                         text.includes('generate') || text.includes('regenerate');
      const isDisabled = el.disabled || el.getAttribute('aria-disabled') === 'true' ||
                         el.classList.contains('disabled') || el.getAttribute('disabled') !== null;
      if (isContinue && !isDisabled) {
        const r = el.getBoundingClientRect();
        return { found: true, x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), label: text.substring(0, 40) };
      }
    }
    return { found: false };
  }).catch(() => ({ found: false, error: 'evaluate failed' }));

  if (!continueBtnData.found) {
    // === FALLBACK: кнопка не найдена ===
    // Если ответ длинный или явно обрезан, пробуем отправить "Продолжи" через composer
    const shouldFallback = existingText.length > 8000 ||
      (existingText.length >= 2000 && existingText.length <= 6000);
    if (shouldFallback) {
      log('⚠️ Кнопка "Продолжить" не найдена, пробуем fallback (отправка "Продолжи")');
      try {
        const composerSelectors = [
          'textarea[placeholder*="Message"]',
          'textarea[placeholder*="message"]',
          'div[contenteditable="true"]',
          'textarea',
        ];
        let composer = null;
        for (const sel of composerSelectors) {
          try {
            const el = await page.$(sel);
            if (el) { composer = el; break; }
          } catch {}
        }
        if (!composer) {
          log('❌ Composer не найден для fallback');
          return '';
        }

        await composer.click({ clickCount: 3 });
        await page.keyboard.press('Backspace');
        await sleep(200);
        await composer.type('Продолжи');
        await sleep(300);
        // Отправляем через Enter (не через кнопку)
        await page.keyboard.press('Enter');
        log('✅ Отправили "Продолжи" через Enter');

        await sleep(2000);
        const newCandidates = await extractBestText(page);

        if (newCandidates.len > existingText.length + CONFIG.deltaThreshold) {
          // Защита: новый текст должен быть хотя бы на 100 символов больше
          // (защита от "pseudo-update" где добавляется 1-2 символа)
          log(`📈 Fallback вернул +${newCandidates.len - existingText.length} символов`);
          return newCandidates.text.substring(existingText.length);
        } else {
          log(`⚠️ Fallback: текст не изменился существенно (${newCandidates.len - existingText.length} символов delta)`);
          return '';
        }
      } catch (e) {
        log(`❌ Fallback ошибка: ${e.message}`);
        return '';
      }
    }
    return '';
  }

  // Кликаем и ждём нового контента
  try {
    await page.mouse.click(continueBtnData.x, continueBtnData.y);
    log('✅ Кликнули "Продолжить", ждём новый контент...');
    await sleep(1000); // было 3000ms — оптимизировано для скорости

    // Ждём появления НОВОГО текста (больше чем existingText)
    const maxWaitMs = 300000; // 5 минут на каждое продолжение
    const startTime = Date.now();
    let newText = existingText;
    let lastLen = 0;

    while (Date.now() - startTime < maxWaitMs) {
      await sleep(250);
      const candidates = await extractBestText(page);

      if (candidates.len > newText.length) {
        newText = candidates.text;
        if (candidates.len !== lastLen) {
          log(`📈 Продолжение: +${candidates.len - existingText.length} символов (всего ${candidates.len})`);
          lastLen = candidates.len;
        }
      }

      // Проверяем: может текст стабилизировался
      if (newText.length === lastLen && lastLen > 0) {
        await sleep(2000);
        const final = await extractBestText(page);
        if (final.len === lastLen) {
          log(`✅ Продолжение завершено (${final.len - existingText.length} новых символов)`);
          return final.text.slice(existingText.length); // возвращаем ТОЛЬКО追加 часть
        }
      }
    }

    // Таймаут — возвращаем что успели набрать
    log(`⚠️ Таймаут продолжения, возвращаем ${newText.length - existingText.length} новых символов`);
    return newText.slice(existingText.length);
  } catch (e) {
    log(`⚠️ Не удалось кликнуть Continue: ${e.message}`);
    return '';
  }
}

async function waitForAnswer(page, prompt, textBefore, timeoutMs = 600000, diag = null) {
  log('⏳ Жду ответ...');
  const startTime = Date.now();

  // ═══ STAGE 1: Network-first (CDP) ═══
  if (cdpInterceptor) {
    log('🌐 Network-first mode: жду ответ через CDP...');
    const networkTimeout = Math.min(timeoutMs * 0.8, 480000);
    const networkResult = await cdpInterceptor.waitForResponse(networkTimeout);

    if (networkResult && networkResult.text && networkResult.text.length >= 2) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      log(`✅ Network extraction: ${networkResult.text.length} символов за ${elapsed}s (${networkResult.format})`);
      if (diag) {
        diag.networkExtracted = true;
      }
      cdpInterceptor.cleanupState();
      return { selector: 'cdp-network', text: networkResult.text, fromNetwork: true };
    }

    if (networkResult) {
      log(`⚠️ Network response не распаршен (${networkResult.format}), fallback DOM`);
      if (networkResult.error) debugLog(`[CDP] Error: ${networkResult.error}`);
      if (networkResult.text) log(`[CDP] Parser returned text=${networkResult.text.length} chars: "${networkResult.text.substring(0, 100)}"`);
      if (networkResult.raw) debugLog(`[CDP] Raw: ${networkResult.raw.substring(0, 200)}`);
    } else {
      log('⚠️ Network timeout — CDP не поймал ответ, fallback DOM');
    }
    cdpInterceptor.cleanupState();
  } else {
    debugLog('[CDP] Interceptor не установлен, skip network');
  }

  // ═══ STAGE 2: DOM fallback — чистый path, без network state ═══
  log('📄 Fallback: DOM extraction...');
  const domPrecheck = await extractAnswerFromDOM(page, textBefore, { minLen: 50 });
  if (domPrecheck && domPrecheck.length >= 50) {
    log(`✅ Ответ уже в DOM: ${domPrecheck.length} символов`);
    return { selector: 'answer-dom', text: domPrecheck };
  }

  const domTimeout = Math.min(timeoutMs * 0.3, 45000);
  return await _waitForAnswerDOM(page, prompt, textBefore, domTimeout, diag);
}

/**
 * DOM-only ожидание — полностью отдельный path.
 * НЕ читает и НЕ пишет network state.
 */
async function _waitForAnswerDOM(page, prompt, textBefore, timeoutMs = 45000, diag = null) {
  const idleTimeoutMsIdle = IDLE_TIMEOUT;
  const heartbeatIntervalMs = HEARTBEAT_INTERVAL;
  const domErrorIdleMsLocal = DOM_ERROR_IDLE;
  let lastText = '';
  let lastChangeTime = Date.now();
  let lastHeartbeatTime = Date.now();
  let lastSuccessfulExtraction = Date.now();
  let foundSelector = null;
  let consecutiveExtractionErrors = 0;

  const cached = loadCachedSelectors();
  const prioritySels = ['[data-message-author-role="assistant"]', '.ds-markdown', '.ds-markdown--block'];
  const remainingSels = RESPONSE_SELECTORS.filter(s => !prioritySels.includes(s));
  const allSels = [...new Set([...prioritySels, ...cached, ...remainingSels])];

  const domStart = Date.now();

  while (true) {
    if (Date.now() - domStart > timeoutMs) { log(`⏰ DOM timeout после ${timeoutMs}ms`); break; }

    // OPTIM: adaptive polling backoff
    const domElapsed = Date.now() - domStart;
    await sleep(domElapsed < 2000 ? 50 : 200);

    let currentText = null;
    let answerText = await extractAnswerFromDOM(page, textBefore, { minLen: 50 });
    if (!answerText || answerText.length < 50) answerText = await extractAnswerFromDOM(page, textBefore, { minLen: 2 });
    if (answerText && isValid(answerText, 2, prompt)) {
      currentText = answerText;
      foundSelector = 'answer-dom';
    }

    if (!currentText) {
      let texts = await getTexts(page, allSels, prompt, { minLen: 50 });
      let valid = texts.filter(x => isValid(x.text, 50, prompt));
      if (!valid.length) { texts = await getTexts(page, allSels, prompt, { minLen: 3 }); valid = texts.filter(x => isValid(x.text, 2, prompt)); }
      if (valid.length) {
        valid.sort((a, b) => b.text.length - a.text.length);
        currentText = valid[0].text;
        foundSelector = valid[0].selector;
      }
    }

    if (currentText && currentText.length >= 2) {
      consecutiveExtractionErrors = 0;
      if (currentText !== lastText) {
        lastText = currentText;
        lastChangeTime = Date.now();
        lastSuccessfulExtraction = Date.now();
        log(`📈 Текст обновился: ${currentText.length} символов`);
      }
      const now = Date.now();
      if (now - lastHeartbeatTime > heartbeatIntervalMs) {
        log(`[Progress] Сгенерировано ${currentText.length} символов...`);
        lastHeartbeatTime = now;
      }
      if (currentText.length >= 50 && now - lastChangeTime > idleTimeoutMsIdle) {
        log(`✅ Стабильный текст (${lastText.length} символов)`);
        break;
      }
      if (currentText.length < 50 && (now - lastChangeTime) >= 300) {
        log(`✅ Короткий ответ: "${currentText}"`);
        break;
      }
    } else {
      consecutiveExtractionErrors++;
    }

    const now = Date.now();
    if (consecutiveExtractionErrors > 0 && (now - lastSuccessfulExtraction > domErrorIdleMsLocal)) {
      log(`⚠️ Длительный период ошибок (${Math.round((now - lastSuccessfulExtraction)/1000)}s)`);
      if (lastText && lastText.length >= 50) break;
      throw new Error('Нет успешных извлечений (DOM churn)');
    }
  }

  // Continue loop
  let finalText = lastText || '';
  let continueRound = 0;
  const maxContinueRounds = CONFIG.maxContinueRounds;
  while (continueRound < maxContinueRounds) {
    if (finalText.length < 50) break;
    continueRound++;
    if (diag) diag.start('CONTINUE');
    log(`🔍 Continue раунд ${continueRound}...`);
    const addedText = await handleContinueButton(page, finalText);
    if (!addedText || addedText.length < 50) {
      if (diag) diag.succeed('CONTINUE', { rounds: continueRound, found: false });
      break;
    }
    finalText += addedText;
    if (diag) diag.succeed('CONTINUE', { rounds: continueRound, addedChars: addedText.length });
  }

  if (diag) diag.continueRounds = continueRound;

  if (finalText && finalText.length >= 2) {
    if (cdpInterceptor) cdpInterceptor.cleanupState();
    return { selector: foundSelector || 'final', text: finalText };
  }
  throw new Error('Ответ не найден (таймаут)');
}



/**
 * Слойная дедупликация для Continue ответов.
 * L0: prefix match → L1: suffix overlap (word boundary) → L2: paragraph split →
 * L3: strip list markers → L4: code fence boundaries → L5: fallback
 */
function _dedupeDelta(existing, newText, minOverlap = 30) {
  if (!existing || !newText) return '';
  if (newText.length <= existing.length) return '';

  // L0: exact prefix
  if (newText.startsWith(existing)) return newText.slice(existing.length).trimStart();

  // L1: suffix overlap на границах слов
  const maxCheck = Math.min(existing.length, newText.length, 300);
  for (let len = maxCheck; len >= minOverlap; len--) {
    const bp = existing.length - len;
    if (bp > 0 && !/\s/.test(existing[bp - 1])) continue;
    const suffix = existing.slice(-len);
    if (newText.startsWith(suffix)) {
      const delta = newText.slice(len).trimStart();
      if (delta.length > 50 || newText.length > existing.length + (CONFIG?.deltaThreshold || 100)) return delta;
      return '';
    }
  }

  // L2: paragraph-level overlap
  const exParas = existing.split(/\n\s*\n/);
  const nwParas = newText.split(/\n\s*\n/);
  if (exParas.length >= 2 && nwParas.length >= 2) {
    const lastEx = exParas[exParas.length - 1].trim();
    for (let i = 0; i < nwParas.length; i++) {
      if (lastEx && nwParas[i].trim().startsWith(lastEx.substring(Math.min(30, lastEx.length / 2)))) {
        const delta = nwParas.slice(i).join('\n\n').trim();
        if (delta.length > 50) return delta;
      }
    }
  }

  // L3: strip list markers
  const stripLM = (t) => t.replace(/^(\s*[-*•]\s+|\s*\d+\.\s+)/gm, '');
  const sEx = stripLM(existing);
  const sNw = stripLM(newText);
  if (sNw.length > sEx.length + 50) {
    const sMax = Math.min(sEx.length, sNw.length, 200);
    for (let len = sMax; len >= 20; len--) {
      if (sNw.startsWith(sEx.slice(-len))) {
        const ratio = len / sEx.length;
        const origPos = Math.round(existing.length * ratio);
        const delta = newText.slice(origPos).trimStart();
        if (delta.length > 50) return delta;
      }
    }
  }

  // L4: code fence boundaries
  const codeFC = (t) => (t.match(/^```/gm) || []).length;
  if (codeFC(existing) % 2 !== 0) {
    const lastFence = existing.lastIndexOf('\n```');
    if (lastFence > 0) {
      const fc = existing.slice(lastFence).trim();
      const fcMax = Math.min(fc.length, newText.length, 100);
      for (let len = fcMax; len >= 10; len--) {
        if (newText.startsWith(fc.slice(-len))) {
          const delta = newText.slice(len).trimStart();
          if (delta.length > 50) return delta;
        }
      }
    }
  }

  // L5: fallback
  if (newText.length > existing.length + (CONFIG?.deltaThreshold || 100)) {
    const fbMax = Math.min(existing.length, newText.length, 100);
    for (let len = fbMax; len >= 10; len--) {
      if (newText.startsWith(existing.slice(-len))) return newText.slice(len).trimStart();
    }
    const pos = newText.indexOf(existing.substring(0, 100));
    if (pos >= 0) return newText.slice(pos + 100).trimStart();
  }
  return '';
}

async function ask(q) {
 // ═══ Инициализация диагностики ════════════════════════════════════════════
 const LOG_DIR = path.join(BASE_DIR, '.diagnostics');
 const diag = new Diagnostics({
   traceId: `tr-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
   sessionName,
   promptPreview: q.substring(0, 80),
   logDir: LOG_DIR,
 });

 diag.start('INIT');
 diag.phaseStart('init');
 diag.snapMemory('start');

 // ═══ Rate limit (smart: exponential backoff on repeated 429s) ═══════
 const RL = path.join(BASE_DIR, 'rate-limit.json');
 try {
 const now = Date.now();
 let lim = { t: 0, backoff: 0, consecutive: 0 };
 if (fs.existsSync(RL)) lim = { ...lim, ...JSON.parse(fs.readFileSync(RL, 'utf8')) };
 // Dry run does not send a prompt, so do not gate auth/composer checks behind request backoff.
 if (!dryRun) {
   const effectiveDelay = lim.backoff || RATE_LIMIT_MS;
   const elapsed = now - (lim.t || 0);
   if (elapsed < effectiveDelay) {
     const remaining = Math.ceil((effectiveDelay - elapsed) / 1000);
     if (effectiveDelay > RATE_LIMIT_MS) {
       log(`⏳ Smart rate limit: backing off ${remaining}s (attempt #${lim.consecutive + 1}, ${effectiveDelay}ms)`);
     }
     const rateLimitError = new Error(`Rate limit: wait ${effectiveDelay}ms (backoff ${lim.consecutive})`);
     rateLimitError.exitCode = 3;
     throw rateLimitError;
   }
   lim.t = now;
   ensureDirSync(BASE_DIR);
   fs.writeFileSync(RL, JSON.stringify(lim));
 }
 } catch (e) { if (e.message.includes('Rate limit:')) throw e; }
 diag.succeed('INIT', { rateLimit: 'passed' });
 diag.phaseEnd('init');

 // ═══ Определяем режим ═══
 const isSession = !!sessionName;
 const session = isSession ? loadSession(sessionName) : null;

 debugLog(`[DEBUG] ask() started, q=${q.substring(0, 50)}`);
 debugLog(`[DEBUG] sessionName=${sessionName}, isSession=${isSession}`);
 debugLog(`[DEBUG] loaded session:`, session ? {chatUrl: session.chatUrl, messageCount: session.messageCount} : null);

 if (isSession) {
 log(`\n🔄 Сессия: "${sessionName}" (сообщений: ${session.messageCount})`);
 } else {
 log(`\n🤖 Одиночный запрос`);
 }
 log(`📝 "${q}"`);
 log(`🔖 Trace: ${diag.traceId}`);

 // ═══ Запуск / подключение браузера ════════════════════════════════════════
 diag.start('BROWSER_LAUNCH');
 diag.phaseStart('browser_launch');
 try {
   var page = await ensureBrowser(session, diag);
   diag.succeed('BROWSER_LAUNCH', { url: page.url().substring(0, 80) });
   diag.phaseEnd('browser_launch');
   diag.snapMemory('after_browser');
 } catch (err) {
   diag.fail('BROWSER_LAUNCH', err);
   throw err;
 }

 // ═══ Auth check (критично — до отправки промпта) ══════════════════════════
 diag.start('AUTH_CHECK');
 diag.phaseStart('auth_check');
 const authOk = await requireAuth(page, diag, log.bind(null, '\x1b[36m[AUTH]\x1b[0m'));
 diag.phaseEnd('auth_check');
 diag.snapMemory('after_auth');
 if (!authOk) {
   diag.fail('AUTH_CHECK', 'Not authenticated');
   await cleanup();
   throw new Error('AUTH_REQUIRED: Требуется авторизация в DeepSeek. Запусти демон вручную и авторизуйся. Инструкция в auth-check.js');
 }
 diag.succeed('AUTH_CHECK', { url: page.url() });

 // CDP Interceptor setup (once per page)
 cdpInterceptor = await setupDeepSeekInterceptor(page);
 debugLog("[CDP] Interceptor configured");


 // Если сессия без chatUrl, но страница уже в чате (демон), используем текущий
 // ВАЖНО: не переиспользуем старые чаты от предыдущих сессий — всегда начинаем новый чат
 // чтобы избежать перемешивания контекста между разными запросами
 if (sessionName && !session.chatUrl) {
   try {
     const currentUrl = page.url();
     if (currentUrl.includes('/a/chat/s/')) {
       log(`⚠️ Демон на старом чате (${currentUrl.substring(0, 40)}...), создаём новый`);
       // НЕ устанавливаем session.chatUrl — чтобы needNewChat сработал
     }
   } catch (e) {}
 }

 // Новый чат если запрошено
 // Определяем, нужен ли новый чат
 const isNewSession = !session || !session.chatUrl;
 const needNewChat = !sessionName || newChat || (session && !session.chatUrl);
 if (needNewChat) {
 await startNewChat(page, isNewSession);  // pass isNewSession to force new chat when session is new
 // Ждём завершения навигации, если она произошла
 try { await page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 12000 }).catch(() => {}); } catch {}
 await sleep(150); // чуть быстрее, без потери стабильности
 if (session) {
   session.messageCount = 0;
   session.chatUrl = null;
 }
 }

 diag.start('COMPOSER_WAIT');
 diag.phaseStart('composer_wait');
 const composerSel = await waitUntilReady(page);
 diag.succeed('COMPOSER_WAIT', { selector: composerSel });
 diag.phaseEnd('composer_wait');
 diag.snapMemory('after_composer');

 // ═══ Dry run: проверяем авторизацию, композер, навигацию — без отправки ═══
 if (dryRun) {
   log('\n✅ Dry run: браузер запущен, авторизация OK, composer найден');
   log(`📍 URL: ${page.url()}`);
   log(`🔧 Composer: ${composerSel}`);
   log('🟢 Всё работает. Пропускаем отправку промпта.');
   diag.start('DRY_RUN');
   diag.succeed('DRY_RUN', { composer: composerSel, url: page.url() });
   if (!isSession) { await cleanup(); }
   diag.save();
   return { selector: 'dry-run', text: 'Dry run OK — авторизация и интерфейс работают' };
 }

 // ═══ Отправка промпта ══════════════════════════════════════════════════════
 diag.start('PROMPT_SEND');
 diag.phaseStart('prompt_send');
 const sendMeta = await sendPrompt(page, composerSel, q);
 const { textBefore } = sendMeta;
 diag.succeed('PROMPT_SEND', { promptLength: q.length, promptUsedLength: sendMeta?.promptUsed?.length || q.length, shortened: !!sendMeta?.shortened, submitReason: sendMeta?.submitOutcome?.reason || null });
 diag.phaseEnd('prompt_send');
 diag.increment('apiRequests', 1);
 diag.snapMemory('after_prompt');

 // ═══ Ожидание и извлечение ответа ═══════════════════════════════════════════
 diag.start('ANSWER_WAIT');
 diag.phaseStart('answer_wait');
 let result = await waitForAnswer(page, q, textBefore, TIMEOUT_ANSWER, diag);
 diag.succeed('ANSWER_WAIT', { selector: result.selector, textLength: result.text.length });
 diag.phaseEnd('answer_wait');
 diag.charactersExtracted = result.text.length;
 diag.answerComplete = !result.incomplete;
 if (result.incomplete) diag.incompleteReason = result.incompleteReason;
 diag.snapMemory('after_answer');

 diag.start('ANSWER_EXTRACT');
 saveCachedSelector(result.selector);
 if (diag) diag.succeed('ANSWER_EXTRACT', { selector: result.selector, textLength: result.text.length });
 if (isSession) {
 session.messageCount++;
 session.lastUsed = new Date().toISOString();
 if (!session.created) session.created = session.lastUsed;
 // Сохраняем URL чата для будущего подключения
 session.chatUrl = page.url();
 session.wsEndpoint = browser.wsEndpoint();
 session.browserMode = browserConnectionMode;
 saveSession(sessionName, session);
 log(`📊 Сессия "${sessionName}": ${session.messageCount} сообщений, URL: ${session.chatUrl}`);
 }

 // ═══ Вывод ═══
 log('\n════════════════════════════════════════════');
 if (isSession) {
 log(`ОТВЕТ DeepSeek [сессия: ${sessionName}, #${session.messageCount}]:`);
 } else {
 log('ОТВЕТ DeepSeek:');
 }
 log('════════════════════════════════════════════');
 log(result.text);
 log('════════════════════════════════════════════\n');

 // Статус лимита — пробуем reload + продолжить если сессия
 if (result.text && result.text.length > 8000) {
   log('\n⚠️  СТАТУС: INCOMPLETE_LIMIT_REACHED — пробуем reload + продолжить...');
   if (isSession && session && session.chatUrl) {
     try {
       log('🔄 Перезагружаем страницу для появления кнопки "Продолжить"...');
       await dsPage.reload({ waitUntil: 'networkidle2', timeout: 30000 });
       await sleep(3000);

       // Ищем кнопку продолжения на перезагруженной странице
       const moreText = await handleContinueButton(dsPage, result.text);
       if (moreText && moreText.length > 100) {
         const combinedText = result.text + moreText;
         if (diag) {
           diag.continueRounds = Math.max(diag.continueRounds || 0, 1);
           diag.charactersExtracted = combinedText.length;
         }
         log(`📦 После reload: +${moreText.length} символов → итого ${combinedText.length}`);
         result = { selector: 'after-reload', text: combinedText };
         // Показываем обновлённый результат
         log('\n════════════════════════════════════════════');
         log(`ОТВЕТ DeepSeek [после продолжения]:`);
         log('════════════════════════════════════════════');
         log(combinedText);
         log('════════════════════════════════════════════\n');
       } else {
         log('⚠️  Кнопка "Продолжить" не появилась и после reload');
       }
     } catch (e) {
       log(`⚠️  Reload не помог: ${e.message}`);
     }
   } else {
     log('💡 Для продолжения используйте --session (контекст сохраняется)');
   }
 }

 // ═══ Закрытие ═══
 if (isSession) {
 // Сессионный: сохраняем контекст, но обязательно отключаем локальный клиент,
 // иначе процесс может зависнуть на открытом DevTools/CDP соединении.
 log(`🟢 Сессия "${sessionName}" активна. Браузер открыт.`);
 await cleanup();
 } else if (shouldClose || !isVisible) {
 // Одиночный: закрываем
 log('🔒 Закрываю...');
 await cleanup();
 } else {
 log('🟢 Браузер открыт.');
 }

 // ═══ Итоговый отчёт ═════════════════════════════════════════════════════════
 diag.finish();
 diag.snapMemory('final');
 const summaryData = diag.summary();
 diag.printSummary(result.text.length);
 const metricsFile = diag.save();
 if (diag.logDir) {
   try {
     const summaryFile = path.join(diag.logDir, `summary-${diag.traceId}.json`);
     fs.writeFileSync(summaryFile, JSON.stringify({
       traceId: diag.traceId,
       summary: summaryData,
       promptLength: q.length,
       answerLength: result.text.length,
       answerComplete: diag.answerComplete,
       incompleteReason: diag.incompleteReason,
       networkExtracted: !!diag.networkExtracted,
       timestamps: { finishedAt: new Date().toISOString() }
     }, null, 2));
     log(`📁 Summary: ${summaryFile}`);
   } catch (e) {
     log(`⚠️ Не удалось записать summary json: ${e.message}`);
   }
 }
 if (metricsFile) log(`📁 Метрики: ${metricsFile}`);
 log(`🔖 Trace ID: ${diag.traceId}`);

 // Reset rate-limit backoff on success
 try {
   if (fs.existsSync(RL)) {
     const lim = JSON.parse(fs.readFileSync(RL, 'utf8'));
     if (lim.consecutive > 0) {
       lim.backoff = RATE_LIMIT_MS;
       lim.consecutive = 0;
       fs.writeFileSync(RL, JSON.stringify(lim));
       log('🔄 Smart rate limit: backoff reset (success)');
     }
   }
 } catch (e) {}

 log('');
 return result;
}

async function handleEndSession() {
 if (!sessionName) { console.error('Укажите --session <имя>'); process.exit(1); }

 const session = loadSession(sessionName);
 log(`\n🛑 Завершаю сессию "${sessionName}" (${session.messageCount} сообщений)`);

 // Попытка подключиться и закрыть
 if (session.wsEndpoint) {
 try {
 browser = await puppeteer.connect({ browserWSEndpoint: session.wsEndpoint });
 const daemonEndpoint = fs.existsSync(DAEMON_ENDPOINT_FILE) ? fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim() : '';
 const isDaemonSession = session.browserMode === 'daemon' || (daemonEndpoint && session.wsEndpoint === daemonEndpoint);
 if (isDaemonSession) {
 browser.disconnect();
 log('🔌 Сессия была в daemon-режиме, только отключаемся');
 } else {
 await browser.close();
 log('🔒 Браузер закрыт');
 }
 } catch {
 log('⚠️ Браузер уже закрыт');
 }
 }

 deleteSession(sessionName);
 log(`✅ Сессия "${sessionName}" удалена`);
}

// ─── Сигналы ────────────────────────────────────────────────
process.on('SIGINT', async () => {
 // В сессионном режиме НЕ закрываем браузер при Ctrl+C
 if (sessionName) {
 log('\n⚠️ Ctrl+C. Браузер остаётся (сессия активна). Для закрытия: --end-session');
 } else {
 await cleanup().catch(() => {});
 }
 process.exit(130);
});
process.on('SIGTERM', async () => { await cleanup().catch(() => {}); process.exit(143); });
process.on('unhandledRejection', e => console.error('❌', e));


// ─── Запуск ─────────────────────────────────────────────────
(async () => {
  // Graceful shutdown при непойманных ошибках
  process.on('uncaughtException', async (e) => {
    console.error(`\x1b[31m❌ UNCAUGHT EXCEPTION: ${e.message}\x1b[0m`);
    console.error(e.stack);
    if (dsPage && browser) {
      try {
        const dumpFile = path.join(BASE_DIR, `.diagnostics`, `crash-${Date.now()}.png`);
        require('fs').mkdirSync(path.join(BASE_DIR, '.diagnostics'), { recursive: true });
        await dsPage.screenshot({ path: dumpFile, fullPage: true }).catch(() => {});
        console.error(`📸 Screenshot saved: ${dumpFile}`);
      } catch {}
    }
    await cleanup().catch(() => {});
    process.exit(1);
  });

  try {
    if (endSession) await handleEndSession();
    else await ask(question);
  } catch (e) {
    // Пробуем записать артефакты при ошибке
    if (dsPage) {
      try {
        const diagnosticsDir = path.join(BASE_DIR, '.diagnostics');
        require('fs').mkdirSync(diagnosticsDir, { recursive: true });
        const ts = Date.now();
        await dsPage.screenshot({ path: path.join(diagnosticsDir, `error-${ts}.png`), fullPage: true }).catch(() => {});
        await require('fs').promises.writeFile(
          path.join(diagnosticsDir, `error-${ts}.html`),
          await dsPage.content().catch(() => ''),
          'utf8'
        ).catch(() => {});
        console.error(`\x1b[33m📸 Артефакты ошибки сохранены в .diagnostics/\x1b[0m`);
      } catch {}
    }
    if (!e.exitCode && shouldExitAsDeepSeekUnreachable(e)) {
      e.exitCode = 2;
    }
    console.error(`\x1b[31m❌ ${e.message}\x1b[0m`);
    try {
      if (e && /rate limit/i.test(String(e.message || ''))) {
        const now = Date.now();
        let lim = { t: 0, backoff: RATE_LIMIT_MS, consecutive: 0 };
        if (fs.existsSync(RL)) lim = { ...lim, ...JSON.parse(fs.readFileSync(RL, 'utf8')) };
        lim.consecutive = (lim.consecutive || 0) + 1;
        lim.backoff = Math.min((lim.backoff || RATE_LIMIT_MS) * 2, 60000);
        lim.t = now;
        fs.writeFileSync(RL, JSON.stringify(lim));
      }
    } catch {}
    if (!sessionName || shouldClose) await cleanup().catch(() => {});
    process.exit(e.exitCode || 1);
  }
})();