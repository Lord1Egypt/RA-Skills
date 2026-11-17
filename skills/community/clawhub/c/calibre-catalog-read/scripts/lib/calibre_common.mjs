import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

export const BUILTIN_FIELDS = new Set([
  "author_sort",
  "authors",
  "comments",
  "cover",
  "formats",
  "identifiers",
  "isbn",
  "languages",
  "last_modified",
  "pubdate",
  "publisher",
  "rating",
  "series",
  "series_index",
  "size",
  "tags",
  "template",
  "timestamp",
  "title",
  "uuid",
]);
export const MAX_OUTPUT = 2 * 1024 * 1024;
export const DEFAULT_CONFIG = path.join(
  os.homedir(),
  ".config",
  "calibre-catalog-read",
  "config.json",
);

export function parseArgs(argv, allowed, booleans = new Set()) {
  const out = { _: [] };
  const allowedSet = new Set(allowed);
  for (let i = 0; i < argv.length; i += 1) {
    const raw = String(argv[i]);
    if (!raw.startsWith("--")) {
      out._.push(raw);
      continue;
    }
    const eq = raw.indexOf("=");
    const key = eq >= 0 ? raw.slice(2, eq) : raw.slice(2);
    if (!key || !allowedSet.has(key)) throw new Error("unknown option --" + key);
    if (Object.prototype.hasOwnProperty.call(out, key))
      throw new Error("duplicate option --" + key);
    if (booleans.has(key)) {
      if (eq >= 0) throw new Error("option --" + key + " does not take a value");
      out[key] = true;
      continue;
    }
    let value;
    if (eq >= 0) value = raw.slice(eq + 1);
    else if (i + 1 < argv.length && !String(argv[i + 1]).startsWith("--"))
      value = String(argv[++i]);
    else throw new Error("missing value for --" + key);
    if (!value) throw new Error("empty value for --" + key);
    out[key] = value;
  }
  return out;
}

export function parseJsonFile(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (e) {
    throw new Error("invalid JSON in " + file + ": " + e.message);
  }
}

export function configPath(args = {}) {
  return path.resolve(String(args.config || process.env.CALIBRE_CATALOG_CONFIG || DEFAULT_CONFIG));
}

export function loadConfig(args = {}) {
  const file = configPath(args);
  if (!fs.existsSync(file)) {
    if (args.config || process.env.CALIBRE_CATALOG_CONFIG)
      throw new Error("config file does not exist");
    return { config: {}, path: file };
  }
  const config = parseJsonFile(file);
  if (!config || typeof config !== "object" || Array.isArray(config))
    throw new Error("config must be a JSON object: " + file);
  for (const [k, v] of Object.entries(config))
    if (
      !["with_library", "library_id", "username", "password_env", "reading_script"].includes(k) ||
      typeof v !== "string"
    )
      throw new Error("invalid catalog config key/value: " + k);
  return { config, path: file };
}

function firstNonEmpty(...values) {
  for (const value of values) {
    const s = String(value ?? "").trim();
    if (s) return s;
  }
  return "";
}

function expandHome(value) {
  const s = String(value || "").trim();
  if (s === "~") return os.homedir();
  if (s.startsWith("~/")) return path.join(os.homedir(), s.slice(2));
  return s;
}

export function resolveLibraryId(args = {}, config = {}) {
  return firstNonEmpty(args["library-id"], process.env.CALIBRE_LIBRARY_ID, config.library_id);
}

export function resolveEndpoint(args = {}, loaded = loadConfig(args)) {
  const config = loaded.config || {};
  const explicit = Object.prototype.hasOwnProperty.call(args, "with-library");
  const raw = explicit
    ? String(args["with-library"] || "").trim()
    : firstNonEmpty(
        process.env.CALIBRE_WITH_LIBRARY,
        process.env.CALIBRE_LIBRARY_URL,
        process.env.CALIBRE_CONTENT_SERVER_URL,
        config.with_library,
      );
  if (!raw)
    throw new Error(
      "missing --with-library (or configured CALIBRE_WITH_LIBRARY / config.with_library); automatic discovery is disabled",
    );
  const libraryId = resolveLibraryId(args, config);
  const endpoint = expandHome(raw);
  if (/^https?:\/\//i.test(endpoint)) {
    const u = new URL(endpoint);
    if (u.username || u.password || u.search)
      throw new Error("endpoint must not contain credentials/query");
    const fragment = decodeURIComponent(u.hash.slice(1) || libraryId);
    if (!fragment || fragment.startsWith("library_id="))
      throw new Error("use CLI #LIBRARY_ID, not a browser URL");
    u.hash = encodeURIComponent(fragment);
    return u.toString();
  }
  if (/^[a-z][a-z0-9+.-]*:/i.test(endpoint))
    throw new Error("with-library must be an http(s) URL or a local library path");
  if (!fs.existsSync(endpoint)) throw new Error("local library path not found: " + endpoint);
  const st = fs.statSync(endpoint);
  if (st.isFile() && path.basename(endpoint).toLowerCase() === "metadata.db")
    throw new Error("use the library directory, not metadata.db");
  if (st.isDirectory() && fs.existsSync(path.join(endpoint, "metadata.db")))
    return fs.realpathSync(endpoint);
  throw new Error("local library path does not contain metadata.db: " + endpoint);
}

export function resolveUsername(args = {}, config = {}) {
  return String(args.username || process.env.CALIBRE_USERNAME || config.username || "").trim();
}

export function validateFields(raw, fallback) {
  const value = String(raw || fallback);
  const fields = value
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean);
  if (!fields.length) throw new Error("fields must not be empty");
  for (const field of fields) {
    if (field === "all") continue;
    if (field.startsWith("*") && /^\*[A-Za-z_][A-Za-z0-9_]*$/.test(field)) continue;
    if (!BUILTIN_FIELDS.has(field)) throw new Error("unknown Calibre field: " + field);
  }
  return fields.join(",");
}

function redact(value, secret, secretFile) {
  let s = String(value || "")
    .replace(/\s+/g, " ")
    .trim();
  if (secret) s = s.split(secret).join("[REDACTED]");
  if (secretFile) s = s.split(secretFile).join("[PASSWORD_FILE]");
  return s.length > 800 ? s.slice(0, 797) + "..." : s;
}

export function runCalibre(
  commandArgs,
  args = {},
  { endpoint, config = {}, timeoutSeconds = 120 } = {},
) {
  if (!endpoint) throw new Error("internal error: missing resolved endpoint");
  const passwordEnv = String(args["password-env"] || config.password_env || "CALIBRE_PASSWORD");
  const secret = String(process.env[passwordEnv] || "");
  let tempDir = "";
  let secretFile = "";
  try {
    // Calibre treats the fragment as a literal library ID, not a URL-escaped ID.
    const cliEndpoint = /^https?:/.test(endpoint)
      ? endpoint.replace(/#(.*)$/, (_, id) => "#" + decodeURIComponent(id))
      : endpoint;
    const argv = [
      ...commandArgs,
      "--with-library",
      cliEndpoint,
      "--timeout",
      String(timeoutSeconds),
    ];
    const username = resolveUsername(args, config);
    if (username) argv.push("--username", username);
    if (secret) {
      tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "calibre-catalog-read-"));
      secretFile = path.join(tempDir, "password");
      fs.writeFileSync(secretFile, secret, { encoding: "utf8", mode: 0o600 });
      fs.chmodSync(secretFile, 0o600);
      argv.push("--password", "<f:" + secretFile + ">");
    }
    const cp = spawnSync("calibredb", argv, {
      encoding: "utf8",
      timeout: Math.max(1, Number(timeoutSeconds || 120)) * 1000,
      maxBuffer: MAX_OUTPUT,
      killSignal: "SIGKILL",
      env: Object.fromEntries(
        ["PATH", "HOME", "LANG", "LC_ALL", "SYSTEMROOT", "WINDIR", "CALIBRE_CONFIG_DIRECTORY"]
          .filter((k) => process.env[k] !== undefined)
          .map((k) => [k, process.env[k]]),
      ),
    });
    if (cp.error) {
      const detail =
        cp.error.code === "ENOENT" ? "calibredb executable not found" : cp.error.message;
      throw new Error(redact(detail, secret, secretFile));
    }
    if (cp.status !== 0) {
      const signal = cp.signal ? ", signal=" + cp.signal : "";
      const detail = redact(cp.stderr || cp.stdout || "no diagnostic output", secret, secretFile);
      throw new Error(
        "calibredb failed (exit=" + (cp.status ?? "unknown") + signal + "): " + detail,
      );
    }
    return String(cp.stdout || "");
  } finally {
    if (secretFile) {
      try {
        fs.rmSync(secretFile, { force: true });
      } catch {}
    }
    if (tempDir) {
      try {
        fs.rmSync(tempDir, { recursive: true, force: true });
      } catch {}
    }
  }
}

export function machineJson(text) {
  try {
    return JSON.parse(text);
  } catch (e) {
    throw new Error("calibredb returned invalid machine JSON: " + e.message);
  }
}

export function shortError(error) {
  return String(error?.message || error || "")
    .replace(/\s+/g, " ")
    .slice(0, 1000);
}
