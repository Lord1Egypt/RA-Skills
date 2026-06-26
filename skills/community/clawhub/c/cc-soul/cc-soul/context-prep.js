import { existsSync, readFileSync } from "fs";
import { execFileSync } from "child_process";
const MAX_FILES = 2;
const INLINE_LIMIT = 2e3;
const HEAD_LINES = 50;
const MAX_URLS = 2;
const URL_TIMEOUT_MS = 3e3;
const MAX_GREP_SYMBOLS = 2;
const MAX_GREP_LINES = 5;
const GREP_TIMEOUT_MS = 2e3;
const MAX_STACK_FRAMES = 5;
const URL_BODY_CHARS = 300;
const PATH_RE = /(?:~\/|\/[\w.-]+)[\w./-]*\.[\w]+/g;
const URL_RE = /https?:\/\/[^\s<>"')\]]+/g;
const HEX_RE = /0x[0-9a-f]{6,}/i;
const ERROR_RE = /(?:Error|错误|error|FAIL|panic|Exception|TypeError|ReferenceError|SyntaxError)[:：]\s*(.{10,120})/i;
const BACKTICK_SYMBOL_RE = /`([a-zA-Z_]\w{2,})`/g;
const IDENT_RE = /\b([a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*|[a-z]\w*_\w+)\b/g;
const STACK_AT_RE = /^\s*at\s+.+[:(]\d+/;
const STACK_PY_RE = /^\s*File\s+"[^"]+",\s*line\s+\d+/;
const TRACEBACK_RE = /Traceback\s*\(most recent call last\)/;
const FRAME_TS_RE = /\(([^)]+:\d+:\d+)\)/;
const FRAME_PY_RE = /File\s+"([^"]+)",\s*line\s+(\d+)/;
function stripHtml(html) {
  return html.replace(/<script[\s\S]*?<\/script>/gi, "").replace(/<style[\s\S]*?<\/style>/gi, "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/gi, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/\s+/g, " ").trim();
}
function extractTitleAndDesc(html) {
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? stripHtml(titleMatch[1]).slice(0, 200) : "";
  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*?)["']/i) || html.match(/<meta[^>]*content=["']([^"']*?)["'][^>]*name=["']description["']/i);
  const desc = descMatch ? descMatch[1].slice(0, 300) : "";
  return { title, desc };
}
function detectSymbols(msg) {
  const symbols = /* @__PURE__ */ new Set();
  let m;
  const btRe = new RegExp(BACKTICK_SYMBOL_RE.source, "g");
  while ((m = btRe.exec(msg)) !== null) {
    symbols.add(m[1]);
  }
  if (symbols.size < MAX_GREP_SYMBOLS) {
    const idRe = new RegExp(IDENT_RE.source, "g");
    while ((m = idRe.exec(msg)) !== null) {
      if (["forEach", "indexOf", "toString", "valueOf", "hasOwnProperty", "console_log"].includes(m[1])) continue;
      symbols.add(m[1]);
    }
  }
  return Array.from(symbols).slice(0, MAX_GREP_SYMBOLS);
}
function grepSymbol(symbol) {
  try {
    const safeSymbol = symbol.replace(/[^a-zA-Z0-9_]/g, "");
    if (!safeSymbol) return null;
    const pattern = `(function|class|def|const|let|var|interface|type|export)\\s+${safeSymbol}`;
    const result = execFileSync("grep", [
      "-rn",
      "-E",
      pattern,
      "--include=*.ts",
      "--include=*.py",
      "--include=*.swift",
      "--include=*.js",
      "."
    ], {
      cwd: process.cwd(),
      timeout: GREP_TIMEOUT_MS,
      encoding: "utf-8",
      maxBuffer: 64 * 1024
    }).trim();
    const lines = result.split("\n").slice(0, MAX_GREP_LINES).join("\n");
    return lines || null;
  } catch {
    return null;
  }
}
function parseStackTrace(msg) {
  const lines = msg.split("\n");
  const frames = [];
  let errorType = "";
  for (const line of lines) {
    if (TRACEBACK_RE.test(line)) continue;
    if (ERROR_RE.test(line) && !errorType) {
      errorType = line.trim().slice(0, 150);
    }
    if (STACK_AT_RE.test(line)) {
      const fm = FRAME_TS_RE.exec(line);
      if (fm && frames.length < MAX_STACK_FRAMES) {
        frames.push(fm[1]);
      }
      continue;
    }
    const pyMatch = FRAME_PY_RE.exec(line);
    if (pyMatch && frames.length < MAX_STACK_FRAMES) {
      frames.push(`${pyMatch[1]}:${pyMatch[2]}`);
    }
  }
  if (frames.length === 0) return null;
  const header = errorType ? `\u9519\u8BEF: ${errorType}
` : "";
  const body = frames.map((f, i) => `  ${i + 1}. ${f}`).join("\n");
  return {
    content: `[\u5806\u6808\u89E3\u6790] ${header}\u5173\u952E\u5E27:
${body}`,
    source: "stack-parse"
  };
}
function buildIntentHint(flags) {
  const hints = [];
  if (flags.hasFiles) hints.push("\u7528\u6237\u5728\u8BA8\u8BBA\u7279\u5B9A\u6587\u4EF6");
  if (flags.hasErrors || flags.hasStack) hints.push("\u7528\u6237\u5728\u8C03\u8BD5\u95EE\u9898");
  if (flags.hasHex) hints.push("\u7528\u6237\u5728\u505A\u9006\u5411/\u8C03\u8BD5");
  if (flags.hasUrls) hints.push("\u7528\u6237\u5728\u5F15\u7528\u5916\u90E8\u8D44\u6E90");
  if (flags.hasSymbols) hints.push("\u7528\u6237\u5728\u8BA8\u8BBA\u4EE3\u7801\u5B9E\u73B0");
  if (hints.length === 0) return null;
  return {
    content: `[\u610F\u56FE\u9884\u5224] ${hints.join("\uFF1B")}`,
    source: "intent-hint"
  };
}
function prepareContext(msg) {
  const contexts = [];
  const intentFlags = {
    hasFiles: false,
    hasErrors: false,
    hasHex: false,
    hasUrls: false,
    hasSymbols: false,
    hasStack: false
  };
  const rawPaths = msg.match(PATH_RE) || [];
  const paths = rawPaths.map((p) => p.startsWith("~/") ? p.replace("~", process.env.HOME || "") : p).slice(0, MAX_FILES);
  for (const p of paths) {
    try {
      if (!existsSync(p)) continue;
      intentFlags.hasFiles = true;
      const content = readFileSync(p, "utf-8");
      if (content.length <= INLINE_LIMIT) {
        contexts.push({ content: `[\u6587\u4EF6\u5185\u5BB9: ${p}]
${content}`, source: p });
      } else {
        const lines = content.split("\n");
        const head = lines.slice(0, HEAD_LINES).join("\n");
        contexts.push({
          content: `[\u6587\u4EF6\u5185\u5BB9: ${p}] (${lines.length}\u884C, \u524D${HEAD_LINES}\u884C)
${head}`,
          source: p
        });
      }
    } catch {
    }
  }
  const stackCtx = parseStackTrace(msg);
  if (stackCtx) {
    intentFlags.hasStack = true;
    contexts.push(stackCtx);
  }
  const errorMatch = msg.match(ERROR_RE);
  if (errorMatch) {
    intentFlags.hasErrors = true;
    if (!stackCtx) {
      contexts.push({ content: `[\u9519\u8BEF\u4FE1\u606F\u63D0\u53D6] ${errorMatch[1].trim()}`, source: "error-detect" });
    }
  }
  if (HEX_RE.test(msg)) {
    intentFlags.hasHex = true;
    contexts.push({ content: `[\u68C0\u6D4B\u5230\u5185\u5B58\u5730\u5740] \u7528\u6237\u53EF\u80FD\u5728\u505A\u9006\u5411/\u8C03\u8BD5\uFF0C\u6CE8\u610F\u5730\u5740\u683C\u5F0F\u548C\u504F\u79FB\u91CF`, source: "hex-detect" });
  }
  const symbols = detectSymbols(msg);
  for (const sym of symbols) {
    const result = grepSymbol(sym);
    if (result) {
      intentFlags.hasSymbols = true;
      contexts.push({
        content: `[\u4EE3\u7801\u7B26\u53F7: ${sym}]
${result}`,
        source: `grep:${sym}`
      });
    }
  }
  const urls = msg.match(URL_RE) || [];
  if (urls.length > 0) {
    intentFlags.hasUrls = true;
  }
  const hint = buildIntentHint(intentFlags);
  if (hint) {
    contexts.push(hint);
  }
  return contexts;
}
async function fetchUrlContext(url) {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), URL_TIMEOUT_MS);
    const resp = await fetch(url, {
      signal: controller.signal,
      headers: { "User-Agent": "cc-soul-context/1.0", "Accept": "text/html" },
      redirect: "follow"
    });
    clearTimeout(timer);
    const contentType = resp.headers.get("content-type") || "";
    if (!contentType.includes("text/html")) return null;
    const html = await resp.text();
    const { title, desc } = extractTitleAndDesc(html);
    const bodyText = stripHtml(html).slice(0, URL_BODY_CHARS);
    const parts = [`[URL \u9884\u53D6: ${url}]`];
    if (title) parts.push(`\u6807\u9898: ${title}`);
    if (desc) parts.push(`\u63CF\u8FF0: ${desc}`);
    if (bodyText) parts.push(`\u6B63\u6587: ${bodyText}`);
    return {
      content: parts.join("\n"),
      source: `url:${url}`
    };
  } catch {
    return null;
  }
}
async function prepareContextAsync(msg) {
  const contexts = prepareContext(msg);
  const urls = (msg.match(URL_RE) || []).slice(0, MAX_URLS);
  if (urls.length > 0) {
    const results = await Promise.allSettled(urls.map((u) => fetchUrlContext(u)));
    for (const r of results) {
      if (r.status === "fulfilled" && r.value) {
        contexts.push(r.value);
      }
    }
  }
  return contexts;
}
export {
  prepareContext,
  prepareContextAsync
};
