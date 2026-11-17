#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

const VERSION = 2;
const PROCESS_TIMEOUT_MS = 125000;
const MAX_IO_BYTES = 16 * 1024 * 1024;
const OC_START = "<!-- OC_ANALYSIS_START -->";
const OC_END = "<!-- OC_ANALYSIS_END -->";
const DIRECT_FIELDS = new Set([
  "title",
  "title_sort",
  "authors",
  "author_sort",
  "series",
  "series_index",
  "tags",
  "publisher",
  "pubdate",
  "languages",
  "comments",
]);
const DERIVED_FIELDS = new Set([
  "comments_html",
  "analysis",
  "analysis_tags",
  "tags_merge",
  "tags_remove",
]);
const ALL_FIELDS = new Set([
  ...DIRECT_FIELDS,
  ...DERIVED_FIELDS,
  "id",
  "expected_library",
  "expected_uuid",
]);
const ANALYSIS_FIELDS = new Set([
  "summary",
  "highlights",
  "reread",
  "tags",
  "lang",
  "generated_at",
  "file_hash",
  "coverage",
]);
const REREAD_FIELDS = new Set(["section", "page", "chunk_id", "reason"]);
const CONFIG_FIELDS = new Set([
  "with_library",
  "library_id",
  "username",
  "password_env",
  "state_dir",
  "reading_script", // Legacy human sorting preference; never executed.
]);
const CLI_OPTIONS = new Set([
  "apply",
  "plan-file",
  "with-library",
  "library-id",
  "username",
  "password-env",
  "config",
  "state-dir",
  "calibredb",
  "lang",
  "help",
  "version",
]);
const READ_FIELDS = [
  "uuid",
  "title",
  "authors",
  "author_sort",
  "series",
  "series_index",
  "tags",
  "publisher",
  "pubdate",
  "languages",
  "comments",
];
const SECRET_RE = /(?:password|passwd|secret|token)\s*[:=]\s*[^\s,}]+/gi;

function fail(message) {
  throw new Error(message);
}
function isObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v);
}
function canonical(value) {
  if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
  if (isObject(value))
    return (
      "{" +
      Object.keys(value)
        .sort()
        .map((k) => JSON.stringify(k) + ":" + canonical(value[k]))
        .join(",") +
      "}"
    );
  return JSON.stringify(value);
}
function sha256(value) {
  return crypto
    .createHash("sha256")
    .update(typeof value === "string" ? value : canonical(value))
    .digest("hex");
}
function nowIso() {
  return new Date().toISOString();
}
function escapeRegExp(s) {
  return s.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
}
function markerCount(s, marker) {
  return String(s).split(marker).length - 1;
}
function markerState(s) {
  const text = String(s || "");
  const starts = markerCount(text, OC_START),
    ends = markerCount(text, OC_END);
  if (!starts && !ends) return "none";
  if (starts !== 1 || ends !== 1 || text.indexOf(OC_START) > text.indexOf(OC_END))
    fail("comments contain malformed OC analysis markers");
  return "valid";
}
function assertNoMarkers(v) {
  if (String(v).includes(OC_START) || String(v).includes(OC_END))
    fail("analysis values must not contain OC analysis markers");
}
function escapeHtml(value) {
  return String(value).replace(
    /[&<>"']/g,
    (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch],
  );
}
function decodeXml(value) {
  return String(value).replace(/&(?:amp|lt|gt|quot|apos);|&#x[0-9a-f]+;|&#[0-9]+;/gi, (token) => {
    if (token === "&amp;") return "&";
    if (token === "&lt;") return "<";
    if (token === "&gt;") return ">";
    if (token === "&quot;") return '"';
    if (token === "&apos;") return "'";
    const n = token.startsWith("&#x")
      ? parseInt(token.slice(3, -1), 16)
      : parseInt(token.slice(2, -1), 10);
    return Number.isFinite(n) ? String.fromCodePoint(n) : token;
  });
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) {
      out._.push(a);
      continue;
    }
    const key = a.slice(2);
    if (key.startsWith("password=")) fail("--password is forbidden; use --password-env");
    if (Object.hasOwn(out, key)) fail("duplicate option --" + key);
    if (!CLI_OPTIONS.has(key)) {
      if (key === "password")
        fail("--password is forbidden; use --password-env so the secret never appears in argv");
      if (key === "save-auth" || key === "save-plain-password")
        fail("--save-auth was removed; use the configured password environment variable");
      if (key === "server-hosts")
        fail(
          "--server-hosts and implicit host discovery were removed; use one explicit --with-library endpoint",
        );
      if (key === "auth-mode" || key === "auth-scheme")
        fail("--auth-mode/--auth-scheme are unsupported; use calibredb documented authentication");
      fail("unknown option --" + key.split("=")[0]);
    }
    if (key === "apply" || key === "help" || key === "version") {
      out[key] = true;
      continue;
    }
    if (i + 1 >= argv.length || argv[i + 1].startsWith("--"))
      fail("--" + key + " requires a value");
    out[key] = argv[++i];
  }
  if (out._.length) fail("unexpected positional arguments");
  return out;
}
function first(...values) {
  for (const v of values)
    if (v !== undefined && v !== null && String(v).trim() !== "") return String(v).trim();
  return "";
}
function expandHome(v) {
  const s = String(v || "").trim();
  if (s === "~") return os.homedir();
  return s.startsWith("~/") ? path.join(os.homedir(), s.slice(2)) : s;
}
function loadConfig(args) {
  const file = path.resolve(
    args.config
      ? String(args.config)
      : path.join(os.homedir(), ".config", "calibre-metadata-apply", "config.json"),
  );
  if (!fs.existsSync(file)) {
    if (args.config) fail("config file not found: " + file);
    return {};
  }
  let cfg;
  try {
    cfg = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    fail("invalid config JSON: " + file);
  }
  if (!isObject(cfg)) fail("config must be a JSON object: " + file);
  for (const k of Object.keys(cfg))
    if (!CONFIG_FIELDS.has(k)) fail("unknown config option " + k + " in " + file);
  if (Object.values(cfg).some((v) => typeof v !== "string")) fail("config values must be strings");
  return cfg;
}
function normalizeEndpoint(raw, libraryId) {
  let value = expandHome(raw);
  if (!value)
    fail("missing --with-library; configure an explicit endpoint or CALIBRE_WITH_LIBRARY");
  if (/^https?:\/\//i.test(value)) {
    let u;
    try {
      u = new URL(value);
    } catch {
      fail("invalid --with-library URL");
    }
    if (u.username || u.password) fail("--with-library must not contain credentials");
    if (!u.hostname) fail("--with-library URL must include an explicit host and port");
    if (!u.hash || u.hash === "#" || u.hash === "#-") {
      if (!libraryId)
        fail("content server URL must include #LIBRARY_ID (or --library-id/config library_id)");
      u.hash = "#" + libraryId;
    }
    if (u.hash.length <= 1) fail("content server URL must include a non-empty library id");
    if (u.search || decodeURIComponent(u.hash.slice(1)).startsWith("library_id="))
      fail("use a calibre CLI URL with #LIBRARY_ID, not a browser URL");
    return u.toString();
  }
  const local = path.resolve(value);
  if (!fs.existsSync(path.join(local, "metadata.db")))
    fail("local library must already contain metadata.db");
  return fs.realpathSync(local);
}
function resolveEndpoint(args, cfg) {
  return normalizeEndpoint(
    first(
      args["with-library"],
      process.env.CALIBRE_WITH_LIBRARY,
      process.env.CALIBRE_LIBRARY_URL,
      process.env.CALIBRE_CONTENT_SERVER_URL,
      cfg.with_library,
    ),
    first(args["library-id"], process.env.CALIBRE_LIBRARY_ID, cfg.library_id),
  );
}
function resolveAuth(args, cfg) {
  const username = first(args.username, process.env.CALIBRE_USERNAME, cfg.username);
  const passwordEnv = first(
    args["password-env"],
    process.env.CALIBRE_PASSWORD_ENV,
    cfg.password_env,
    "CALIBRE_PASSWORD",
  );
  return {
    username: username || "",
    passwordEnv,
    password: String(process.env[passwordEnv] || ""),
  };
}
function resolveStateDir(args, cfg) {
  const raw = first(
    args["state-dir"],
    process.env.CALIBRE_METADATA_APPLY_STATE_DIR,
    cfg.state_dir,
    process.env.XDG_STATE_HOME
      ? path.join(process.env.XDG_STATE_HOME, "calibre-metadata-apply")
      : path.join(os.homedir(), ".local", "state", "calibre-metadata-apply"),
  );
  return path.resolve(expandHome(raw));
}
function safeEnv() {
  return {
    PATH: process.env.PATH || "",
    HOME: process.env.HOME || "",
    LANG: process.env.LANG || "C.UTF-8",
    LC_ALL: process.env.LC_ALL || "",
    LC_CTYPE: process.env.LC_CTYPE || "",
    SYSTEMROOT: process.env.SYSTEMROOT || "",
    WINDIR: process.env.WINDIR || "",
    CALIBRE_CONFIG_DIRECTORY:
      process.env.CALIBRE_CONFIG_DIRECTORY || path.join(os.homedir(), ".config", "calibre"),
  };
}
function scrub(value, secret = "") {
  let s = String(value || "");
  if (secret) s = s.split(secret).join("********");
  return s.replace(SECRET_RE, "********");
}
function redactedCommand(cmd) {
  return cmd
    .map((x, i) =>
      i && cmd[i - 1] === "--password"
        ? "********"
        : /\s/.test(String(x))
          ? JSON.stringify(String(x))
          : String(x),
    )
    .join(" ");
}
function runCalibre(binary, args, auth) {
  let cp;
  try {
    cp = spawnSync(binary, args, {
      encoding: "utf8",
      input: auth.password ? auth.password + "\n" : undefined,
      env: safeEnv(),
      timeout: PROCESS_TIMEOUT_MS,
      killSignal: "SIGKILL",
      maxBuffer: MAX_IO_BYTES,
    });
  } catch (e) {
    return { rc: 127, out: "", err: scrub(e.message, auth.password) };
  }
  if (cp.error)
    return {
      rc: Number.isInteger(cp.status) ? cp.status : 127,
      out: cp.stdout || "",
      err: scrub(cp.error.message, auth.password),
    };
  return {
    rc: Number.isInteger(cp.status) ? cp.status : 128,
    out: cp.stdout || "", // Successful metadata is data, not a diagnostic to rewrite.
    err: scrub(cp.stderr || "", auth.password),
  };
}
function commonArgs(endpoint, auth) {
  const cliEndpoint = /^https?:/.test(endpoint)
    ? endpoint.replace(/#(.*)$/, (_, id) => "#" + decodeURIComponent(id))
    : endpoint;
  const out = ["--with-library", cliEndpoint, "--timeout", "120"];
  if (auth.username) out.push("--username", auth.username);
  if (auth.password) out.push("--password", "<stdin>");
  return out;
}
function runOk(binary, cmd, auth) {
  const r = runCalibre(binary, cmd, auth);
  if (r.rc !== 0)
    fail(
      "calibredb failed (" +
        r.rc +
        ")\\nCMD: " +
        redactedCommand(cmd) +
        "\\nERR: " +
        scrub(r.err || r.out, auth.password),
    );
  return r.out;
}
function parseMachineRows(out, cmd) {
  let p;
  try {
    p = JSON.parse(out);
  } catch {
    fail("calibredb returned invalid machine JSON for " + redactedCommand(cmd));
  }
  if (!Array.isArray(p)) fail("calibredb list returned a non-array machine result");
  return p;
}
function idString(v) {
  if (typeof v === "number") {
    if (!Number.isSafeInteger(v) || v <= 0) fail("id must be a positive safe integer");
    return String(v);
  }
  if (typeof v === "string" && /^[1-9]\d*$/.test(v) && Number.isSafeInteger(Number(v))) return v;
  fail("id must be a positive integer without leading zeros");
}
function parseTags(v, name) {
  if (v === null) return [];
  if (Array.isArray(v)) {
    if (!v.every((x) => typeof x === "string")) fail(name + " array must contain strings");
    if (v.some((x) => x.includes(",") || x.includes("\0")))
      fail(name + " cannot contain a comma or NUL inside one item");
    return v.map((x) => x.trim()).filter(Boolean);
  }
  if (typeof v !== "string") fail(name + " must be a string or string array");
  return v
    .split(/[,;\n]/)
    .map((x) => x.trim())
    .filter(Boolean);
}
function stringField(v, name, { required = false } = {}) {
  if (v === null) {
    if (required) fail(name + " cannot be null");
    return "";
  }
  if (typeof v !== "string") fail(name + " must be a string or null");
  if (v.includes("\0")) fail(name + " must not contain NUL");
  const s = name === "comments" ? v : v.trim();
  if (required && !s) fail(name + " cannot be empty");
  return s;
}
function authorList(v) {
  if (Array.isArray(v)) return v.map((x) => String(x).trim()).filter(Boolean);
  return String(v ?? "")
    .replaceAll("&&", "\0")
    .split("&")
    .map((x) => x.replaceAll("\0", "&").trim())
    .filter(Boolean);
}
function authorField(v) {
  if (v === null || (!Array.isArray(v) && typeof v !== "string"))
    fail("authors must be a string or array");
  if (Array.isArray(v) && !v.every((x) => typeof x === "string" && x.trim()))
    fail("authors array requires non-empty strings");
  if ((Array.isArray(v) ? v : [v]).some((x) => x.includes("\0")))
    fail("authors must not contain NUL");
  if (
    (Array.isArray(v) && v.some((x) => x.includes("&") || x.includes("|"))) ||
    (!Array.isArray(v) && (v.includes("&&") || v.includes("|")))
  )
    fail(
      "literal & or | in one author cannot be represented safely by Calibre --field; no metadata changed",
    );
  const authors = authorList(v);
  if (!authors.length) fail("authors cannot be empty");
  return authors;
}
function validateDate(v) {
  const s = stringField(v, "pubdate");
  if (!s) return s;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) fail("pubdate must be YYYY-MM-DD");
  const d = new Date(s + "T00:00:00Z");
  if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== s)
    fail("pubdate is not a real calendar date");
  return s;
}
function validateLanguages(v) {
  const vals =
    v === null ? [] : Array.isArray(v) ? v : typeof v === "string" ? v.split(/[,;\n]/) : null;
  if (!vals || !vals.every((x) => typeof x === "string"))
    fail("languages must be an ISO639 string or string array");
  const names = new Intl.DisplayNames(["en"], { type: "language", fallback: "none" });
  const out = vals.map((x) => x.trim().toLowerCase()).filter(Boolean);
  for (const x of out)
    if (!/^[a-z]{2,3}$/.test(x) || names.of(x) === undefined)
      fail("unsupported ISO639 language code: " + x);
  return [...new Set(out.map((x) => new Intl.Locale(x).language))];
}
function validateSeriesIndex(v) {
  if (
    (typeof v !== "number" && typeof v !== "string") ||
    typeof v === "boolean" ||
    String(v).trim() === ""
  )
    fail("series_index must be a finite non-negative number");
  const n = Number(v);
  if (!Number.isFinite(n) || n < 0) fail("series_index must be a finite non-negative number");
  return String(n);
}
function validateAnalysis(v) {
  if (!isObject(v)) fail("analysis must be an object");
  for (const k of Object.keys(v)) if (!ANALYSIS_FIELDS.has(k)) fail("unknown analysis field: " + k);
  const o = { ...v };
  if (typeof o.summary !== "string" || !o.summary.trim())
    fail("analysis.summary is required and non-empty");
  if (
    o.file_hash !== undefined &&
    (typeof o.file_hash !== "string" || !/^sha256:[0-9a-f]{64}$/.test(o.file_hash))
  )
    fail("analysis.file_hash must be a SHA256 digest");
  if (
    o.generated_at !== undefined &&
    (typeof o.generated_at !== "string" || Number.isNaN(Date.parse(o.generated_at)))
  )
    fail("analysis.generated_at must be a date-time");
  if (o.coverage !== undefined) {
    const c = o.coverage;
    if (
      !isObject(c) ||
      Object.keys(c).sort().join(",") !== "expected_files,mode,part_ids,read_chars,read_files" ||
      !["full", "partial"].includes(c.mode) ||
      !Number.isSafeInteger(c.expected_files) ||
      c.expected_files < 1 ||
      !Number.isSafeInteger(c.read_files) ||
      c.read_files < 1 ||
      c.read_files > c.expected_files ||
      !Number.isSafeInteger(c.read_chars) ||
      c.read_chars < 1 ||
      !Array.isArray(c.part_ids) ||
      c.part_ids.length !== c.read_files ||
      new Set(c.part_ids).size !== c.read_files ||
      !c.part_ids.every((x) => typeof x === "string" && /^part-[0-9]+$/.test(x)) ||
      (c.mode === "full") !== (c.read_files === c.expected_files)
    )
      fail("invalid analysis.coverage");
  }
  if (o.summary !== undefined) o.summary = stringField(o.summary, "analysis.summary");
  if (o.highlights !== undefined) {
    if (!Array.isArray(o.highlights) || !o.highlights.every((x) => typeof x === "string"))
      fail("analysis.highlights must be a string array");
    o.highlights = o.highlights.map((x) => x.trim()).filter(Boolean);
  }
  if (o.tags !== undefined) o.tags = parseTags(o.tags, "analysis.tags");
  if (o.lang !== undefined) {
    o.lang = stringField(o.lang, "analysis.lang").toLowerCase();
    if (!["ja", "en"].includes(o.lang)) fail("analysis.lang must be ja|en");
  }
  if (o.generated_at !== undefined)
    o.generated_at = stringField(o.generated_at, "analysis.generated_at");
  if (o.file_hash !== undefined) o.file_hash = stringField(o.file_hash, "analysis.file_hash");
  if (o.reread !== undefined) {
    if (!Array.isArray(o.reread)) fail("analysis.reread must be an array");
    o.reread = o.reread.map((item, i) => {
      if (!isObject(item)) fail("analysis.reread[" + i + "] must be an object");
      for (const k of Object.keys(item))
        if (!REREAD_FIELDS.has(k)) fail("unknown analysis.reread field: " + k);
      const x = {};
      for (const k of REREAD_FIELDS)
        if (item[k] !== undefined) x[k] = stringField(item[k], "analysis.reread." + k);
      return x;
    });
  }
  for (const v of Object.values(o)) if (typeof v === "string") assertNoMarkers(v);
  return o;
}
function renderAnalysisHtml(a, defaultLang = "ja") {
  const en = (a.lang || defaultLang) === "en";
  const t = en
    ? {
        title: "OpenClaw Analysis",
        summary: "Summary",
        points: "Key points",
        reread: "Reread guide",
        generated: "generated_at",
        hash: "file_hash",
        tags: "analysis_tags",
        section: "section",
        page: "page",
        chunk: "chunk",
      }
    : {
        title: "OpenClaw解析",
        summary: "要約",
        points: "重要ポイント",
        reread: "再読ガイド",
        generated: "生成日時",
        hash: "ファイルハッシュ",
        tags: "解析タグ",
        section: "章/節",
        page: "ページ",
        chunk: "チャンク",
      };
  const lines = [OC_START, '<div class="openclaw-analysis">', "<h3>" + t.title + "</h3>"];
  if (a.summary)
    lines.push("<p><strong>" + t.summary + ":</strong> " + escapeHtml(a.summary) + "</p>");
  if (a.highlights?.length)
    lines.push(
      "<h4>" + t.points + "</h4><ul>",
      ...a.highlights.map((x) => "<li>" + escapeHtml(x) + "</li>"),
      "</ul>",
    );
  if (a.reread?.length) {
    lines.push("<h4>" + t.reread + "</h4><ul>");
    for (const i of a.reread) {
      const p = [];
      if (i.section) p.push(t.section + ": " + i.section);
      if (i.page) p.push(t.page + ": " + i.page);
      if (i.chunk_id) p.push(t.chunk + ": " + i.chunk_id);
      if (i.reason) p.push(i.reason);
      if (p.length) lines.push("<li>" + escapeHtml(p.join(" | ")) + "</li>");
    }
    lines.push("</ul>");
  }
  const meta = [t.generated + ": " + escapeHtml(a.generated_at || nowIso())];
  if (a.coverage)
    meta.push(
      (en ? "Coverage" : "解析範囲") +
        ": " +
        a.coverage.mode +
        " (" +
        a.coverage.read_files +
        "/" +
        a.coverage.expected_files +
        ")",
    );
  if (a.file_hash) meta.push(t.hash + ": " + escapeHtml(a.file_hash));
  if (a.tags?.length) meta.push(t.tags + ": " + escapeHtml(a.tags.join(", ")));
  lines.push("<p><em>" + meta.join(" / ") + "</em></p>", "</div>", OC_END);
  return lines.join("\n");
}
function validateCommentsHtml(v) {
  const s = stringField(v, "comments_html", { required: true });
  if (
    markerCount(s, OC_START) !== 1 ||
    markerCount(s, OC_END) !== 1 ||
    s.indexOf(OC_START) > s.indexOf(OC_END)
  )
    fail("comments_html must contain exactly one valid OC marker block");
  return s;
}
function upsertOcBlock(existing, block) {
  markerState(existing);
  const re = new RegExp(escapeRegExp(OC_START) + "[\\s\\S]*?" + escapeRegExp(OC_END));
  if (re.test(existing)) return existing.replace(re, () => block);
  return existing.trim() ? existing.replace(/\s+$/, "") + "\n\n" + block : block;
}
function validateRecord(record, defaultLang = "ja") {
  if (!isObject(record)) fail("each JSONL row must be an object");
  for (const k of Object.keys(record)) if (!ALL_FIELDS.has(k)) fail("unknown input field: " + k);
  if (!Object.hasOwn(record, "id")) fail("id is required");
  const id = idString(record.id);
  if (Object.keys(record).length < 2) fail("row " + id + " has no updatable fields");
  if (record.tags_merge !== undefined && typeof record.tags_merge !== "boolean")
    fail("tags_merge must be boolean");
  if (
    record.comments !== undefined &&
    (record.comments_html !== undefined || record.analysis !== undefined)
  )
    fail("comments conflicts with comments_html/analysis");
  if (record.comments_html !== undefined && record.analysis !== undefined)
    fail("comments_html conflicts with analysis");
  const r = { id };
  if (record.expected_library !== undefined)
    r.expected_library = stringField(record.expected_library, "expected_library", {
      required: true,
    });
  if (record.expected_uuid !== undefined)
    r.expected_uuid = stringField(record.expected_uuid, "expected_uuid", { required: true });
  if (record.tags_merge !== undefined) r.tags_merge = record.tags_merge;
  if (record.title !== undefined) r.title = stringField(record.title, "title", { required: true });
  if (record.title_sort !== undefined) r.title_sort = stringField(record.title_sort, "title_sort");
  if (record.authors !== undefined) r.authors = authorField(record.authors);
  if (record.author_sort !== undefined)
    r.author_sort = stringField(record.author_sort, "author_sort");
  if (record.series !== undefined) r.series = stringField(record.series, "series");
  if (record.series_index !== undefined) r.series_index = validateSeriesIndex(record.series_index);
  if (record.publisher !== undefined) r.publisher = stringField(record.publisher, "publisher");
  if (record.pubdate !== undefined) r.pubdate = validateDate(record.pubdate);
  if (record.languages !== undefined) r.languages = validateLanguages(record.languages);
  if (record.comments !== undefined) {
    r.comments = stringField(record.comments, "comments");
    markerState(r.comments);
  }
  if (record.tags !== undefined) r.tags = parseTags(record.tags, "tags");
  if (record.tags_remove !== undefined)
    r.tags_remove = parseTags(record.tags_remove, "tags_remove");
  if (record.analysis_tags !== undefined)
    r.analysis_tags = parseTags(record.analysis_tags, "analysis_tags");
  if (record.comments_html !== undefined)
    r.comments_html = validateCommentsHtml(record.comments_html);
  if (record.analysis !== undefined) r.analysis = validateAnalysis(record.analysis);
  if (r.analysis) {
    r.analysis_tags = [...(r.analysis_tags || []), ...(r.analysis.tags || [])];
    r.comments_html = renderAnalysisHtml(r.analysis, defaultLang);
  }
  if (!requestedFields(r).length) fail("row " + id + " has no updatable fields");
  return r;
}
function parseInput(text, defaultLang = "ja") {
  const rows = [];
  for (const [i, raw] of String(text).split(/\r?\n/).entries()) {
    if (!raw.trim()) continue;
    let p;
    try {
      p = JSON.parse(raw);
    } catch {
      fail("line " + (i + 1) + " is not valid JSON");
    }
    try {
      rows.push({ line: i + 1, request: validateRecord(p, defaultLang) });
    } catch (e) {
      fail("line " + (i + 1) + ": " + e.message);
    }
  }
  if (!rows.length) fail("input JSONL is empty");
  const ids = new Set();
  for (const x of rows) {
    if (ids.has(x.request.id)) fail("duplicate id " + x.request.id);
    ids.add(x.request.id);
  }
  return rows;
}
function listCommand(endpoint, auth, id) {
  return [
    "list",
    "--for-machine",
    "--fields",
    READ_FIELDS.join(","),
    "--search",
    "id:" + id,
    "--limit",
    "2",
    ...commonArgs(endpoint, auth),
  ];
}
function titleSortCommand(endpoint, auth, id) {
  return ["show_metadata", "--as-opf", id, ...commonArgs(endpoint, auth)];
}
function parseTitleSort(opf) {
  for (const match of String(opf).matchAll(/<meta\b[^>]*>/gi)) {
    const attrs = Object.fromEntries(
      [...match[0].matchAll(/([\w:.-]+)\s*=\s*(["'])(.*?)\2/gs)].map((x) => [
        x[1],
        decodeXml(x[3]),
      ]),
    );
    if (attrs.name === "calibre:title_sort" && Object.hasOwn(attrs, "content"))
      return attrs.content;
  }
  fail("title_sort missing from OPF; refusing unverified value");
}
function fetchCurrent(binary, endpoint, auth, id, needTitleSort = false) {
  const cmd = listCommand(endpoint, auth, id);
  const rows = parseMachineRows(runOk(binary, cmd, auth), cmd);
  const matches = rows.filter((r) => String(r?.id) === id);
  if (matches.length !== 1) fail("id " + id + " is missing or ambiguous in the selected library");
  const row = { ...matches[0], id };
  const opf = runOk(binary, titleSortCommand(endpoint, auth, id), auth);
  const authors = [...opf.matchAll(/<dc:creator\b[^>]*>([\s\S]*?)<\/dc:creator>/gi)].map((x) =>
    decodeXml(x[1]),
  );
  if (!authors.length) fail("authors missing from OPF");
  row.authors = authors;
  if (needTitleSort) row.title_sort = parseTitleSort(opf);
  return row;
}
function normList(v) {
  if (Array.isArray(v)) return v.map((x) => String(x).trim()).filter(Boolean);
  if (v == null || String(v).trim() === "" || String(v) === "None") return [];
  return String(v)
    .split(/[,;\n]/)
    .map((x) => x.trim())
    .filter(Boolean);
}
function normField(field, v) {
  if (field === "tags") return normList(v);
  if (field === "languages") return normList(v).map((x) => new Intl.Locale(x).language);
  if (field === "authors") return authorList(v);
  if (field === "series_index")
    return v == null || String(v).trim() === "" ? "" : String(Number(v));
  if (field === "pubdate")
    return v == null || String(v).startsWith("0101-") ? "" : String(v).slice(0, 10);
  return v == null ? "" : String(v);
}
function equalField(field, a, b) {
  let left = normField(field, a),
    right = normField(field, b);
  if (field === "tags" || field === "languages") {
    left = [...left].sort();
    right = [...right].sort();
  }
  return JSON.stringify(left) === JSON.stringify(right);
}
function requestedFields(r) {
  const f = new Set();
  for (const k of Object.keys(r)) if (DIRECT_FIELDS.has(k)) f.add(k);
  if (r.comments_html !== undefined || r.analysis !== undefined) f.add("comments");
  if (r.tags !== undefined || r.tags_remove !== undefined || r.analysis_tags?.length) f.add("tags");
  return [...f].sort();
}
function cliFieldName(f) {
  return f === "title_sort" ? "sort" : f;
}
function cliValue(f, v) {
  if (f === "pubdate") return v ? v + "T00:00:00Z" : "0101-01-01T00:00:00Z";
  if (f === "authors")
    return authorList(v)
      .map((x) => x.replaceAll("&", "&&"))
      .join(" & ");
  return f === "authors"
    ? v
    : f === "tags" || f === "languages"
      ? Array.isArray(v)
        ? v.join(",")
        : String(v)
      : String(v ?? "");
}
function makePlanRow(binary, endpoint, auth, item) {
  if (
    item.request.expected_library !== undefined &&
    normalizeEndpoint(item.request.expected_library, "") !== endpoint
  )
    fail("proposal library identity differs from selected endpoint");
  const need = item.request.title_sort !== undefined;
  const current = fetchCurrent(binary, endpoint, auth, item.request.id, need);
  if (!current.uuid) fail("book UUID is missing");
  if (item.request.expected_uuid !== undefined && item.request.expected_uuid !== current.uuid)
    fail("proposal book UUID differs from selected target");
  if (item.request.series_index !== undefined && !(item.request.series ?? current.series))
    fail("series_index requires a non-empty series");
  if (item.request.series === "" && item.request.series_index !== undefined)
    fail("clearing series conflicts with series_index");
  const before = {};
  for (const f of requestedFields(item.request)) before[f] = normField(f, current[f]);
  const after = { ...before };
  for (const f of [
    "title",
    "title_sort",
    "authors",
    "author_sort",
    "series",
    "series_index",
    "publisher",
    "pubdate",
    "languages",
    "comments",
  ])
    if (item.request[f] !== undefined) after[f] = item.request[f];
  if (item.request.comments_html !== undefined || item.request.analysis !== undefined)
    after.comments = upsertOcBlock(String(current.comments || ""), item.request.comments_html);
  if (
    item.request.tags !== undefined ||
    item.request.tags_remove !== undefined ||
    item.request.analysis_tags?.length
  ) {
    const existing = item.request.tags_merge === false ? [] : normList(current.tags),
      remove = new Set((item.request.tags_remove || []).map((x) => x.toLowerCase())),
      vals = [];
    for (const x of [
      ...existing,
      ...(item.request.tags || []),
      ...(item.request.analysis_tags || []),
    ])
      if (!vals.some((y) => y.toLowerCase() === x.toLowerCase())) vals.push(x);
    after.tags = vals.filter((x) => !remove.has(x.toLowerCase()));
  }
  const cli_fields = [];
  for (const f of Object.keys(after).sort())
    if (!equalField(f, before[f], after[f]))
      cli_fields.push({ name: cliFieldName(f), value: cliValue(f, after[f]) });
  return {
    line: item.line,
    id: item.request.id,
    book: {
      id: item.request.id,
      uuid: String(current.uuid),
      title: current.title,
      authors: current.authors,
    },
    guard: Object.fromEntries(
      [...READ_FIELDS, ...(need ? ["title_sort"] : [])].map((f) => [f, normField(f, current[f])]),
    ),
    fields: Object.keys(after).sort(),
    before,
    after,
    cli_fields,
    before_digest: sha256(before),
    intent_digest: sha256({ id: item.request.id, before, after, cli_fields }),
  };
}
function planWithoutDigest(p) {
  const c = { ...p };
  delete c.plan_digest;
  return c;
}
function addPlanDigest(p) {
  p.plan_digest = sha256(planWithoutDigest(p));
  return p;
}
function writeNewFile(file, content) {
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  if (fs.existsSync(file)) fail("refusing to overwrite existing plan/state file: " + file);
  const temp = file + ".tmp-" + process.pid + "-" + crypto.randomBytes(4).toString("hex");
  try {
    fs.writeFileSync(temp, content, { encoding: "utf8", mode: 0o600, flag: "wx" });
    fs.linkSync(temp, file); // Atomic no-clobber publication, including concurrent creators.
  } finally {
    try {
      fs.unlinkSync(temp);
    } catch {}
  }
}
function defaultPlanFile(dir, p) {
  return path.join(
    dir,
    "plans",
    "plan-" +
      new Date().toISOString().replace(/[:.]/g, "-") +
      "-" +
      p.plan_digest.slice(0, 12) +
      ".json",
  );
}
function validatePlan(p) {
  if (!isObject(p) || p.kind !== "calibre-metadata-apply-plan" || p.version !== VERSION)
    fail("unsupported or malformed plan");
  if (typeof p.plan_digest !== "string" || sha256(planWithoutDigest(p)) !== p.plan_digest)
    fail("plan digest mismatch; refusing apply");
  if (
    !isObject(p.library) ||
    typeof p.library.endpoint !== "string" ||
    !Array.isArray(p.rows) ||
    !p.rows.length
  )
    fail("malformed plan");
  if (p.library.identity_digest !== sha256(p.library.endpoint))
    fail("library identity digest mismatch");
  const seen = new Set();
  for (const r of p.rows) {
    if (!isObject(r) || typeof r.id !== "string" || !/^[1-9]\d*$/.test(r.id) || seen.has(r.id))
      fail("malformed or duplicate plan row");
    seen.add(r.id);
    if (
      !isObject(r.book) ||
      r.book.id !== r.id ||
      typeof r.book.uuid !== "string" ||
      !r.book.uuid ||
      !isObject(r.guard) ||
      !Array.isArray(r.fields) ||
      r.fields.some((f) => !DIRECT_FIELDS.has(f)) ||
      !isObject(r.before) ||
      !isObject(r.after) ||
      !Array.isArray(r.cli_fields)
    )
      fail("malformed plan row " + r.id);
    if (
      sha256(r.before) !== r.before_digest ||
      sha256({ id: r.id, before: r.before, after: r.after, cli_fields: r.cli_fields }) !==
        r.intent_digest
    )
      fail("plan row digest mismatch for id " + r.id);
    const fields = Object.keys(r.after).sort();
    validateRecord({ id: r.id, ...r.after });
    if (
      canonical(fields) !== canonical(r.fields) ||
      canonical(Object.keys(r.before).sort()) !== canonical(fields)
    )
      fail("plan fields differ from shown before/after");
    if (
      canonical(Object.keys(r.guard).sort()) !==
        canonical(
          [...READ_FIELDS, ...(fields.includes("title_sort") ? ["title_sort"] : [])].sort(),
        ) ||
      r.guard.uuid !== r.book.uuid
    )
      fail("incomplete plan guard");
    const expected = fields
      .filter((f) => !equalField(f, r.before[f], r.after[f]))
      .map((f) => ({ name: cliFieldName(f), value: cliValue(f, r.after[f]) }));
    if (canonical(expected) !== canonical(r.cli_fields))
      fail("plan CLI intent differs from shown after values");
    for (const f of r.cli_fields)
      if (
        !isObject(f) ||
        ![
          "title",
          "sort",
          "authors",
          "author_sort",
          "series",
          "series_index",
          "tags",
          "publisher",
          "pubdate",
          "languages",
          "comments",
        ].includes(f.name) ||
        typeof f.value !== "string"
      )
        fail("malformed plan field for id " + r.id);
  }
  return p;
}
function planCommand(endpoint, auth, row) {
  const c = ["set_metadata", row.id];
  for (const f of row.cli_fields) c.push("--field", f.name + ":" + f.value);
  c.push(...commonArgs(endpoint, auth));
  return c;
}
function comparePlanCurrent(row, current) {
  if (String(current.id) !== row.id) return "book id changed";
  if (String(current.uuid || "") !== row.book.uuid) return "book UUID changed";
  for (const [f, value] of Object.entries(row.guard))
    if (!equalField(f, value, current[f])) return "field changed: " + f;
  return null;
}
function compareAfter(row, current) {
  if (String(current.uuid || "") !== row.book.uuid) return "book UUID changed during apply";
  for (const f of row.fields)
    if (!equalField(f, row.after[f], current[f])) return "readback mismatch: " + f;
  return null;
}
function output(v) {
  process.stdout.write(JSON.stringify(v, null, 2) + "\n");
}
function applyPlan(binary, endpoint, auth, plan, stateDir) {
  const dir = path.join(stateDir, "attempts");
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  const receipt = path.join(dir, plan.plan_digest + ".jsonl");
  const lock = path.join(dir, "library-" + sha256(endpoint) + ".lock");
  let lockFd;
  try {
    lockFd = fs.openSync(lock, "wx", 0o600);
  } catch (e) {
    if (e.code === "EEXIST")
      fail(
        "library apply lock exists; inspect active work/receipts before manual recovery: " + lock,
      );
    throw e;
  }
  let fd;
  const append = (value) => {
    fs.writeSync(fd, JSON.stringify({ at: nowIso(), ...value }) + "\n");
    fs.fsyncSync(fd);
  };
  try {
    try {
      fd = fs.openSync(receipt, "wx", 0o600);
    } catch (e) {
      if (e.code === "EEXIST")
        fail("plan already attempted; reconcile receipt, then create a new plan: " + receipt);
      throw e;
    }
    append({ event: "started", plan_digest: plan.plan_digest, endpoint });
    const results = [];
    const fetch = (row) =>
      fetchCurrent(binary, endpoint, auth, row.id, row.fields.includes("title_sort"));
    for (const row of plan.rows) {
      try {
        const mismatch = comparePlanCurrent(row, fetch(row));
        if (mismatch) results.push({ id: row.id, action: "stale", error: mismatch });
      } catch (e) {
        results.push({
          id: row.id,
          action: "unverifiable",
          error: scrub(e.message, auth.password),
        });
      }
    }
    let halted = results.length > 0;
    const preflight = halted;
    for (const row of plan.rows) {
      if (preflight && results.some((r) => r.id === row.id)) continue;
      let result;
      if (halted)
        result = {
          id: row.id,
          action: "skipped",
          reason: "earlier failure; no blind continuation",
        };
      else {
        try {
          const mismatch = comparePlanCurrent(row, fetch(row));
          if (mismatch) result = { id: row.id, action: "stale", error: mismatch };
          else if (!row.cli_fields.length) result = { id: row.id, action: "no-op" };
          else {
            append({ event: "intent", id: row.id, intent_digest: row.intent_digest });
            const run = runCalibre(binary, planCommand(endpoint, auth, row), auth);
            if (run.rc !== 0)
              result = {
                id: row.id,
                action: "failed",
                rc: run.rc,
                error: scrub(run.err, auth.password),
                reconciliation_required: true,
              };
            else {
              const mismatchAfter = compareAfter(row, fetch(row));
              result = mismatchAfter
                ? {
                    id: row.id,
                    action: "unverifiable",
                    error: mismatchAfter,
                    reconciliation_required: true,
                  }
                : {
                    id: row.id,
                    action: "applied",
                    changed_fields: row.cli_fields.map((f) => f.name),
                  };
            }
          }
        } catch (e) {
          result = {
            id: row.id,
            action: "unverifiable",
            error: scrub(e.message, auth.password),
            reconciliation_required: true,
          };
        }
      }
      results.push(result);
      append({ event: "result", ...result });
      if (!["applied", "no-op"].includes(result.action)) halted = true;
    }
    const summary = { total: plan.rows.length };
    for (const action of ["applied", "no-op", "stale", "failed", "unverifiable", "skipped"])
      summary[action.replace("-", "_")] = results.filter((r) => r.action === action).length;
    const outcome = {
      ok: !halted,
      mode: "apply",
      phase: preflight ? "preflight" : "complete",
      plan_digest: plan.plan_digest,
      receipt_file: receipt,
      summary,
      results,
    };
    append({ event: "finished", ...outcome });
    return outcome;
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
    fs.closeSync(lockFd);
    fs.unlinkSync(lock);
  }
}
async function readStdin() {
  const c = [];
  let bytes = 0;
  for await (const x of process.stdin) {
    bytes += x.length;
    if (bytes > MAX_IO_BYTES) fail("input exceeds 16 MiB");
    c.push(x);
  }
  return Buffer.concat(c).toString("utf8");
}
async function main() {
  const args = parseArgs(process.argv);
  if (args.lang !== undefined && !["ja", "en"].includes(String(args.lang)))
    fail("--lang must be ja|en");
  if (args.help) {
    output({
      usage:
        "JSONL | node calibredb_apply.mjs [--with-library ENDPOINT] [--plan-file FILE] [--apply]",
      notes: "dry-run persists a plan; --apply consumes only a verified saved plan",
    });
    return;
  }
  if (args.version) {
    console.log("calibre-metadata-apply plan-schema=" + VERSION);
    return;
  }
  const cfg = loadConfig(args),
    auth = resolveAuth(args, cfg),
    binary = String(args.calibredb || process.env.CALIBREDB || "calibredb"),
    stateDir = resolveStateDir(args, cfg);
  if (args.apply) {
    if (args.lang || (args["library-id"] && !args["with-library"]))
      fail("apply uses the saved plan, not a new language/library selector");
    if (!args["plan-file"])
      fail("--apply requires --plan-file; apply never consumes a fresh JSONL request");
    const planFile = path.resolve(String(args["plan-file"]));
    let plan;
    try {
      plan = validatePlan(JSON.parse(fs.readFileSync(planFile, "utf8")));
    } catch (e) {
      fail(e.message);
    }
    const endpoint = args["with-library"]
      ? resolveEndpoint(args, cfg)
      : normalizeEndpoint(plan.library.endpoint, "");
    const input = await readStdin();
    if (input.trim()) fail("--apply refuses JSONL input; use the exact saved --plan-file");
    if (endpoint !== plan.library.endpoint)
      fail("endpoint/library identity differs from saved plan");
    const outcome = applyPlan(binary, endpoint, auth, plan, stateDir);
    output(outcome);
    if (!outcome.ok) process.exitCode = 1;
    return;
  }
  const endpoint = resolveEndpoint(args, cfg);
  const items = parseInput(await readStdin(), String(args.lang || "ja")),
    rows = items.map((x) => makePlanRow(binary, endpoint, auth, x)),
    library = {
      endpoint,
      library_id: /^https?:/i.test(endpoint) ? new URL(endpoint).hash.slice(1) : null,
      identity_digest: sha256(endpoint),
    },
    plan = addPlanDigest({
      kind: "calibre-metadata-apply-plan",
      version: VERSION,
      created_at: nowIso(),
      library,
      rows,
    }),
    file = path.resolve(args["plan-file"] || defaultPlanFile(stateDir, plan));
  writeNewFile(file, JSON.stringify(plan, null, 2) + "\n");
  output({
    ok: true,
    mode: "dry-run",
    plan_file: file,
    plan_digest: plan.plan_digest,
    summary: {
      total: rows.length,
      changed: rows.filter((x) => x.cli_fields.length).length,
      no_op: rows.filter((x) => !x.cli_fields.length).length,
    },
    rows: rows.map((x) => ({
      id: x.id,
      before: x.before,
      after: x.after,
      changed_fields: x.cli_fields.map((f) => f.name),
      command: redactedCommand(planCommand(endpoint, auth, x)),
    })),
  });
}
main().catch((e) => {
  console.error(scrub(e?.stack || e));
  process.exitCode = 1;
});
