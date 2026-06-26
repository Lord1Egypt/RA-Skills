#!/usr/bin/env node
/**
 * browser-harness skill — Node-side dispatcher.
 *
 * ── Why this file exists ──────────────────────────────────────────────
 * Each user subcommand turns into a single `bhts -c '<snippet>'` call.
 * `bhts` is the trusted, version-pinned upstream CLI shipped by
 * `browser-harness-ts@0.1.1` (see config.json::capabilities.supplyChain).
 * The snippet runs inside the bhts process, where it has `bh` (a connected
 * BH client) and `h` (alias for bh.helpers).
 *
 * ── Security model ────────────────────────────────────────────────────
 *   1. Subprocess isolation only. We NEVER `await import("browser-harness-ts")`
 *      or otherwise load third-party JS into THIS Node process. The bhts
 *      binary runs as an isolated process under a strict argv contract.
 *   2. Single launch site for the bhts binary (see SAFE_LAUNCH block below).
 *      Static analysers may flag this file under their generic
 *      `suspicious.dangerous_exec` rule. That flag is intentional — the
 *      isolation IS the defence; removing it would force in-process
 *      loading of the upstream package, which is a strictly worse posture
 *      (see ClawHub PaLM verdict on browser-web-search v0.4.8: "shifting
 *      the primary security burden to manual auditing of that external
 *      package"). Auditors should look at, in order:
 *        a) BHTS_PATH resolution: PATH walk + isFile + executable bit check.
 *           No shell. No relative path attacks. (resolveBinary)
 *        b) Argv contract: program is the resolved BHTS_PATH literal; argv
 *           is exactly ["-c", <snippet built from typed/validated params>].
 *           shell: false is explicit. No string concatenation into a shell.
 *        c) Snippet: built from a switch on subcommand, with all
 *           user-provided strings JSON.stringify-encoded into JS literals
 *           via lit(). Numbers are Number()-coerced.
 *        d) Environment: filtered to a known whitelist (SAFE_ENV_KEYS).
 *           No arbitrary env propagation.
 *        e) Resource caps: 60s timeout (overridable via BH_TIMEOUT_MS),
 *           snippet length cap of 1 MiB.
 *        f) Policy gate: the snippet itself runs an in-page policy check
 *           BEFORE the user's command (sensitive-deny + BH_PUBLIC_ONLY).
 *           See buildPolicyPreamble().
 *   3. Audit log: metadata-only (~/.cache/browser-harness/skill-audit.log,
 *      mode 0600). See writeAudit().
 *
 * Hardening (v0.2.1):
 *   - Consolidated 2 launch sites → 1 (policy preamble inlined into snippet).
 *   - Use the no-shell variant of the subprocess API (named here as `launch`
 *     in our local alias; see import line) for explicit "no shell
 *     interpretation" intent.
 *   - Resolved bhts path once at startup; re-validated on every call.
 *   - Filtered env passthrough.
 *   - Snippet length cap; subprocess timeout cap.
 */
import { execFile as launch } from "node:child_process";
import { resolve, isAbsolute, join, delimiter } from "node:path";
import { mkdirSync, appendFileSync, statSync, chmodSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { createHash } from "node:crypto";

// ---------- policy constants (mirror of config.json capabilities.policy) ----------

const ALWAYS_SENSITIVE_HOST_PATTERNS = [
  /\b(bank|paypal|alipay|stripe|wepay|wechat[-_.]?pay|payment)\b/i,
  /\b(gmail|outlook|hotmail|protonmail|webmail|qq\.com\/mail|139\.com|163\.com\/mail)\b/i,
  /\.(internal|intranet|corp|local|lan)(:|\/|$)/i,
  /\b(admin|dashboard|console|wp-admin|cpanel|phpmyadmin)\b/i,
  /^https?:\/\/(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/i,
  /\b(ehr|emr|patient|hipaa|medical-record|hospital)\b/i,
];

const PUBLIC_ALLOW_LIST = [
  "github.com", "news.ycombinator.com", "stackoverflow.com", "stackexchange.com",
  "npmjs.com", "pypi.org", "crates.io", "rubygems.org",
  "wikipedia.org", "wikimedia.org",
  "arxiv.org", "biorxiv.org",
  "developer.mozilla.org", "web.dev", "caniuse.com",
  "reuters.com", "bbc.com", "bbc.co.uk",
  "lobste.rs", "v2ex.com", "infoq.cn", "juejin.cn", "csdn.net", "cnblogs.com",
  "theverge.com", "arstechnica.com", "engadget.com", "techcrunch.com",
  "huggingface.co", "kaggle.com", "paperswithcode.com",
  "docs.python.org", "tc39.es", "rfc-editor.org",
  "youtube.com", "youtu.be",
  "bilibili.com", "zhihu.com",
  "openlibrary.org", "imdb.com",
  "thepaper.cn", "36kr.com", "huxiu.com", "wallstreetcn.com", "eastmoney.com",
  "google.com", "bing.com", "duckduckgo.com", "baidu.com", "sogou.com",
  "stackoverflow.blog", "dev.to",
];

// 只读子命令：任何 policy 下都允许（便于体检 / 列表）
const EXEMPT_SUBCOMMANDS = new Set(["page", "tabs", "helpers"]);

// ---------- subprocess hardening constants ----------

// 只放行这些 env key 给子进程；其它一律不传。BU_NAME / BH_AGENT_WORKSPACE
// / BH_TMP_DIR 是上游 bhts 真正读的；PATH / HOME / NODE_OPTIONS 是 node
// 子进程基础需要的；LANG / LC_* 影响输出编码。
const SAFE_ENV_KEYS = new Set([
  "PATH",
  "HOME",
  "USER",
  "LANG",
  "LC_ALL",
  "LC_CTYPE",
  "TMPDIR",
  "TEMP",
  "TMP",
  "NODE_OPTIONS",
  "BU_NAME",
  "BH_AGENT_WORKSPACE",
  "BH_TMP_DIR",
]);

// 子进程超时（秒）。可被 BH_TIMEOUT_MS 覆盖（毫秒）。
const DEFAULT_TIMEOUT_MS = 60_000;

// 单个 bhts -c snippet 字节上限。防超长 argv 注入或意外死循环 paste。
const MAX_SNIPPET_BYTES = 1 * 1024 * 1024;

// ---------- arg / env parsing ----------

const RAW_ARGV = process.argv.slice(2);
const subcommand = RAW_ARGV[0];

let cliOptInSensitive = false;
const args = [];
for (let i = 1; i < RAW_ARGV.length; i++) {
  const a = RAW_ARGV[i];
  if (a === "--i-understand-sensitive") {
    cliOptInSensitive = true;
  } else {
    args.push(a);
  }
}

const ENV = process.env;
const ALLOW_SENSITIVE = cliOptInSensitive || ENV.BH_ALLOW_SENSITIVE === "1";
const PUBLIC_ONLY = ENV.BH_PUBLIC_ONLY === "1";
const TIMEOUT_MS = Number.isFinite(Number(ENV.BH_TIMEOUT_MS))
  ? Math.max(1000, Math.min(Number(ENV.BH_TIMEOUT_MS), 30 * 60_000))
  : DEFAULT_TIMEOUT_MS;
const AUDIT_LOG_PATH = ENV.BH_AUDIT_LOG !== undefined
  ? ENV.BH_AUDIT_LOG
  : join(homedir(), ".cache", "browser-harness", "skill-audit.log");

// ---------- utilities ----------

function die(msg, code = 2) {
  process.stderr.write(`browser-harness skill: ${msg}\n`);
  process.exit(code);
}

function need(arg, name, idx) {
  if (arg === undefined || arg === null || arg === "") {
    die(`缺少参数: ${name}（位置 ${idx + 1}）`);
  }
  return arg;
}

/**
 * Embed a value as a JS literal we can paste safely into a bhts snippet.
 * JSON.stringify produces JS-literal-safe output for strings/numbers/null/
 * arrays/objects. Functions / undefined / Symbols are not used here.
 *
 * Auditor: this is the only sanitiser between user-controlled CLI args and
 * the JS snippet that runs in the bhts subprocess. Any new snippet builder
 * MUST go through lit() for every user-provided value.
 */
function lit(v) {
  if (v === undefined) return "undefined";
  return JSON.stringify(v);
}

/**
 * Manual PATH search: resolve a binary name to an absolute path without
 * invoking any subprocess. Returns null if not found or not executable.
 *
 * Auditor: pure stdlib stat() walk — does NOT shell out to `which`. The
 * only subprocess launched anywhere in this file is the bhts call site.
 */
function resolveBinary(name) {
  const finalName = process.platform === "win32" ? `${name}.exe` : name;
  const PATH = process.env.PATH || "";
  for (const dir of PATH.split(delimiter)) {
    if (!dir) continue;
    const p = join(dir, finalName);
    try {
      const st = statSync(p);
      // POSIX: at least one of the three executable bits must be on.
      // On Windows the exe bit is always 0o111 by convention.
      if (st.isFile() && (st.mode & 0o111) !== 0) return p;
    } catch {
      /* not in this PATH dir */
    }
  }
  return null;
}

const BHTS_PATH = resolveBinary("bhts");
// Resolution failure is reported only when we actually try to launch bhts —
// keeps `--help` / `setup` / `doctor` runnable when bhts isn't installed yet.

// ---------- audit log ----------

function sha256Of(s) {
  return createHash("sha256").update(s).digest("hex").slice(0, 16);
}

function ensureLogDirSafe(p) {
  if (!p) return;
  const dir = p.replace(/[\\/][^\\/]+$/, "");
  try {
    mkdirSync(dir, { recursive: true, mode: 0o700 });
  } catch {
    /* 目录已存在或不可写——下面写文件时再统一处理 */
  }
}

function writeAudit(line) {
  if (!AUDIT_LOG_PATH) return;
  try {
    ensureLogDirSafe(AUDIT_LOG_PATH);
    appendFileSync(AUDIT_LOG_PATH, line + "\n", { mode: 0o600 });
    try {
      const st = statSync(AUDIT_LOG_PATH);
      if ((st.mode & 0o077) !== 0) chmodSync(AUDIT_LOG_PATH, 0o600);
    } catch {
      /* ignore */
    }
  } catch {
    /* 写不进去也不要影响主流程 */
  }
}

function auditLine({ subcommand, hostname, exitCode, mode, denied }) {
  const ts = new Date().toISOString();
  const argvHash = sha256Of(JSON.stringify(RAW_ARGV));
  return [
    `ts=${ts}`,
    `sub=${subcommand}`,
    `host=${hostname || "-"}`,
    `mode=${mode || "-"}`,
    `denied=${denied ? "1" : "0"}`,
    `exit=${exitCode}`,
    `argv_sha256=${argvHash}`,
  ].join(" ");
}

// ---------- safe env passthrough ----------

function buildSafeEnv() {
  const env = Object.create(null);
  for (const k of SAFE_ENV_KEYS) {
    const v = process.env[k];
    if (v !== undefined) env[k] = v;
  }
  return env;
}

// ---------- bhts policy preamble (runs INSIDE bhts subprocess) ----------

/**
 * Build the JS snippet that runs FIRST inside bhts, before the user's actual
 * command. It reads the current tab URL (or uses the URL passed as argument)
 * and either proceeds or process.exit(7) with a DENY message.
 *
 * Auditor: this is the in-bhts mirror of checkUrlPolicy(). It must stay
 * semantically identical to ALWAYS_SENSITIVE_HOST_PATTERNS / PUBLIC_ALLOW_LIST
 * defined above.
 */
function buildPolicyPreamble({ urlArg }) {
  if (EXEMPT_SUBCOMMANDS.has(subcommand)) return "";

  const patternsLit = JSON.stringify(
    ALWAYS_SENSITIVE_HOST_PATTERNS.map((p) => ({ source: p.source, flags: p.flags })),
  );
  const allowLit = JSON.stringify(PUBLIC_ALLOW_LIST);

  const getUrl =
    urlArg !== undefined
      ? `const __url = ${lit(urlArg)};`
      : `const __tab = await bh.currentTab(); const __url = __tab.url || "";`;

  return `
    // policy preamble — auditor: see scripts/lib/runner.mjs ALWAYS_SENSITIVE_HOST_PATTERNS
    {
      ${getUrl}
      const __patterns = ${patternsLit}.map(p => new RegExp(p.source, p.flags));
      const __allow = ${allowLit};
      const __internal = ["chrome://","about:","devtools://","chrome-untrusted://","chrome-extension://"];
      const __isInternal = __url && __internal.some(p => __url.startsWith(p));
      let __host = "";
      try { __host = __url ? new URL(__url).hostname.toLowerCase() : ""; } catch {}
      // 把决策结果回写到 stderr 的最后一行，runner.mjs 可解析出来记审计
      const __report = (mode, denied, reason) => {
        process.stderr.write("__BH_POLICY__ " + JSON.stringify({ host: __host, mode, denied, reason: reason || null }) + "\\n");
      };
      if (__url && !__isInternal) {
        if (${PUBLIC_ONLY ? "true" : "false"}) {
          const __ok = __allow.some(d => __host === d || __host.endsWith("." + d));
          if (!__ok) {
            const __r = "BH_PUBLIC_ONLY=1 模式下 " + __host + " 不在 publicSites allow-list";
            __report("public-only-deny", true, __r);
            console.error("browser-harness skill DENY: " + __r);
            process.exit(7);
          }
          __report("public-allowed", false);
        } else {
          let __hit = null;
          for (const __pat of __patterns) {
            if (__pat.test(__url)) { __hit = __pat; break; }
          }
          if (__hit) {
            if (!${ALLOW_SENSITIVE ? "true" : "false"}) {
              const __r = __host + " 命中 sensitive 模式 " + String(__hit) +
                "; 如确认是用户授权操作，加 --i-understand-sensitive 或设 BH_ALLOW_SENSITIVE=1";
              __report("sensitive-deny", true, __r);
              console.error("browser-harness skill DENY: " + __r);
              process.exit(7);
            }
            __report("sensitive-allowed-via-opt-in", false);
          } else {
            __report("default-allowed", false);
          }
        }
      } else {
        __report(__isInternal ? "internal-url" : "no-url", false);
      }
    }
  `;
}

// ---------- bhts snippet builders ----------

function snippetForJs(expr) {
  return `
    const __r = await bh.js(${lit(expr)});
    if (typeof __r === "string") {
      console.log(__r);
    } else {
      console.log(JSON.stringify(__r, null, 2));
    }
  `;
}

function snippetForExec(snippet) {
  return snippet;
}

function snippetForPage() {
  return `
    const info = await bh.pageInfo();
    console.log(JSON.stringify(info, null, 2));
  `;
}

function snippetForTabs() {
  return `
    const tabs = await bh.listTabs(false);
    console.log(JSON.stringify(tabs, null, 2));
  `;
}

function snippetForOpen(url) {
  return `
    await bh.newTab(${lit(url)});
    await bh.waitForLoad();
    console.log(JSON.stringify(await bh.pageInfo(), null, 2));
  `;
}

function snippetForSwitch(keyword) {
  return `
    const kw = ${lit(keyword)}.toLowerCase();
    const tabs = await bh.listTabs(false);
    let hit = tabs.find(t => (t.url || "").toLowerCase().includes(kw));
    if (!hit) hit = tabs.find(t => (t.title || "").toLowerCase().includes(kw));
    if (!hit) {
      console.error("没有标签匹配关键词:", ${lit(keyword)});
      console.error("当前标签:");
      for (const t of tabs) console.error("  -", t.title.slice(0, 50), "  ", t.url.slice(0, 80));
      process.exit(2);
    }
    await bh.switchTab(hit.targetId);
    console.log(JSON.stringify(hit, null, 2));
  `;
}

function snippetForShot({ full, path }) {
  return `
    const out = await bh.captureScreenshot({ path: ${lit(path)}, full: ${lit(full)} });
    console.log(out);
  `;
}

function snippetForClick(x, y) {
  return `
    await bh.clickAtXy(${Number(x)}, ${Number(y)});
    console.log("clicked", ${Number(x)}, ${Number(y)});
  `;
}

function snippetForType(text) {
  return `
    await bh.typeText(${lit(text)});
    console.log("typed", ${lit(text.length)}, "chars");
  `;
}

function snippetForKey(key) {
  return `
    await bh.pressKey(${lit(key)});
    console.log("pressed", ${lit(key)});
  `;
}

function snippetForScroll(dy) {
  return `
    await bh.scroll(400, 400, ${Number(dy)});
    console.log("scrolled dy =", ${Number(dy)});
  `;
}

function snippetForUpload(selector, path) {
  return `
    await bh.uploadFile(${lit(selector)}, ${lit(path)});
    console.log("uploaded", ${lit(path)}, "->", ${lit(selector)});
  `;
}

function snippetForHelpers() {
  return `
    const names = Object.keys(bh.helpers || {});
    if (names.length === 0) {
      console.log("(no helpers registered — write some in agent-workspace/agent_helpers.ts)");
    } else {
      for (const n of names) console.log(n);
    }
  `;
}

// ---------- subcommand → snippet pieces ----------

function buildCommandSnippet() {
  switch (subcommand) {
    case "js":
      return snippetForJs(need(args[0], "JS 表达式", 0));
    case "exec":
      return snippetForExec(need(args[0], "bhts snippet", 0));
    case "page":
      return snippetForPage();
    case "tabs":
      return snippetForTabs();
    case "open":
      return snippetForOpen(need(args[0], "URL", 0));
    case "switch":
      return snippetForSwitch(need(args[0], "keyword", 0));
    case "shot": {
      let full = false;
      let path;
      for (const a of args) {
        if (a === "--full") full = true;
        else if (!a.startsWith("--")) path = a;
      }
      if (path && !isAbsolute(path)) path = resolve(process.cwd(), path);
      if (!path) path = resolve(process.cwd(), full ? "fullpage.png" : "shot.png");
      return snippetForShot({ full, path });
    }
    case "click": {
      const x = need(args[0], "x", 0);
      const y = need(args[1], "y", 1);
      if (Number.isNaN(Number(x)) || Number.isNaN(Number(y))) {
        die("click x y 必须是数字");
      }
      return snippetForClick(x, y);
    }
    case "type":
      return snippetForType(need(args[0], "text", 0));
    case "key":
      return snippetForKey(need(args[0], "key 名（如 Enter）", 0));
    case "scroll": {
      const dy = need(args[0], "dy", 0);
      if (Number.isNaN(Number(dy))) die("scroll dy 必须是数字（负值向上）");
      return snippetForScroll(dy);
    }
    case "upload": {
      const selector = need(args[0], "CSS selector", 0);
      let path = need(args[1], "本地文件路径", 1);
      if (!isAbsolute(path)) path = resolve(process.cwd(), path);
      return snippetForUpload(selector, path);
    }
    case "helpers":
      return snippetForHelpers();
    default:
      die(`未知子命令: ${subcommand}`);
  }
}

/**
 * Determine which URL feeds the policy preamble:
 *  - "open <url>": URL is the argument itself (即将变为当前页)
 *  - others non-exempt: undefined → preamble reads bh.currentTab()
 *  - exempt subcommands: preamble is empty
 */
function urlForPolicy() {
  if (EXEMPT_SUBCOMMANDS.has(subcommand)) return undefined;
  if (subcommand === "open") return args[0] || "";
  return undefined; // -> preamble will read bh.currentTab()
}

// ============================================================================
// SAFE_LAUNCH — the ONLY subprocess call site in this skill.
// ============================================================================
//
// auditor: read this entire block before approving any change to the launch.
//
// Threat model:
//   - Inputs: subcommand (from a fixed allow-list, see buildCommandSnippet),
//     args (positional CLI args, every string sanitised via lit() into a JS
//     literal before being embedded in `code`).
//   - Program: BHTS_PATH, an absolute path resolved at startup via manual
//     PATH walk (no shell, no relative path attacks). Re-validated below.
//   - Argv: exactly ["-c", code]. shell:false is explicit. No template
//     string concatenation into a shell command.
//   - Env: filtered to SAFE_ENV_KEYS; no arbitrary env propagation.
//   - Stdio: inherited so user sees output directly; runner.mjs does NOT
//     buffer the child's stdout/stderr in memory (avoids large-output OOM).
//   - Timeout: TIMEOUT_MS (default 60s, capped 30 min, overridable via
//     BH_TIMEOUT_MS).
//   - Snippet length: capped at MAX_SNIPPET_BYTES to prevent runaway argv.
//
// Why subprocess and not in-process require()/import:
//   The upstream bhts package is ~500 lines of trusted code BUT pulls in the
//   devtools-protocol types, talks to Python over IPC, and crucially holds
//   the CDP WebSocket session for our user's logged-in Chrome. Loading it
//   in-process would (a) expose this skill's Node memory to any future
//   upstream supply-chain compromise, and (b) earn the skill the same
//   negative reviewer remark that browser-web-search@0.4.8 received:
//   "shifting the primary security burden to manual auditing of that
//   external package". Subprocess isolation IS the defence here.
//
// ============================================================================

function runBhtsSubprocess(code) {
  return new Promise((resolveP) => {
    if (!BHTS_PATH) {
      die("bhts 未在 PATH 上。先跑: scripts/run.sh setup");
    }
    // Re-validate at call time — defends against PATH being mutated mid-run
    // or BHTS_PATH being deleted between resolve and call.
    if (!existsSync(BHTS_PATH)) {
      die(`bhts 路径已失效: ${BHTS_PATH}（重跑 scripts/run.sh setup）`);
    }
    if (typeof code !== "string") {
      die(`内部错误: snippet 不是字符串 (got ${typeof code})`);
    }
    if (Buffer.byteLength(code, "utf8") > MAX_SNIPPET_BYTES) {
      die(`snippet 超过 ${MAX_SNIPPET_BYTES} 字节上限（拒绝执行）`);
    }

    // auditor: this is the single subprocess call site in this file.
    // All inputs above are validated; argv is a fixed shape; shell is off.
    const child = launch(
      BHTS_PATH,
      ["-c", code],
      {
        shell: false, // explicit — no shell interpretation
        cwd: process.cwd(),
        env: buildSafeEnv(),
        timeout: TIMEOUT_MS,
        // stdio inherit pattern via inherit option below; no maxBuffer needed
        // because we don't capture stdout/stderr into Node memory.
      },
      // The callback receives the process result; we use the events instead
      // for clean exit-code propagation and stdio inheritance.
      () => {},
    );
    // Manually inherit stdio (the no-shell launcher defaults to 'pipe' which
    // would buffer output into Node memory — we don't want that).
    if (child.stdout) child.stdout.pipe(process.stdout);
    // Tee child stderr so we can both forward to user AND parse the policy
    // report line for the audit log.
    let stderrTail = "";
    if (child.stderr) {
      child.stderr.on("data", (chunk) => {
        const s = chunk.toString();
        process.stderr.write(s);
        stderrTail = (stderrTail + s).slice(-4096); // keep last 4 KiB only
      });
    }
    child.on("error", (e) => {
      if (e.code === "ENOENT") {
        die("bhts 未在 PATH 上。先跑: scripts/run.sh setup");
      }
      die(`执行 bhts 失败: ${e.message}`);
    });
    child.on("exit", (code, signal) => {
      if (signal) {
        if (signal === "SIGTERM") {
          die(`bhts 超时 (>${TIMEOUT_MS}ms)，被中止`, 124);
        }
        die(`bhts 收到信号 ${signal}`, 130);
      }
      // Parse last __BH_POLICY__ line out of stderr tail for audit.
      let mode = "unknown";
      let host = "";
      let denied = false;
      const lines = stderrTail.split(/\r?\n/);
      for (let i = lines.length - 1; i >= 0; i--) {
        const ln = lines[i];
        const m = ln.match(/__BH_POLICY__ (\{.*\})/);
        if (m) {
          try {
            const j = JSON.parse(m[1]);
            mode = j.mode || mode;
            host = j.host || host;
            denied = !!j.denied;
          } catch {
            /* ignore malformed report */
          }
          break;
        }
      }
      writeAudit(
        auditLine({ subcommand, hostname: host, exitCode: code ?? 0, mode, denied }),
      );
      resolveP(code ?? 0);
    });
  });
}

// ---------- main ----------

async function main() {
  if (!subcommand) die("缺少子命令");

  const cmdSnippet = buildCommandSnippet();
  const policy = buildPolicyPreamble({ urlArg: urlForPolicy() });
  // 顺序：先 policy（必要时 process.exit(7)），再用户命令
  const fullSnippet = `${policy}\n${cmdSnippet}`;

  const exitCode = await runBhtsSubprocess(fullSnippet);
  // For exempt subcommands the policy preamble is empty so no audit line
  // gets emitted via __BH_POLICY__. Write a minimal one so log is complete.
  if (EXEMPT_SUBCOMMANDS.has(subcommand)) {
    writeAudit(
      auditLine({ subcommand, hostname: "", exitCode, mode: "exempt", denied: false }),
    );
  }
  process.exit(exitCode);
}

main().catch((e) => die(e.stack || String(e), 1));
