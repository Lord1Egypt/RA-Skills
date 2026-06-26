#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: explicit user-provided First-Principle API URLs within the skill's documented API set and optional presigned PUT URLs (upload host allowlist enforced)
//   Local files read: optional session file, optional upload file for put-file
//   Local files written: none

import { readFileSync, statSync } from "node:fs";
import path from "node:path";

const DEFAULT_ALLOWED_API_HOSTS = ["www.first-principle.com.cn", "first-principle.com.cn"];
const DEFAULT_ALLOWED_UPLOAD_HOST_RULES = ["*.aliyuncs.com", ".first-principle.com.cn"];

function usage() {
  console.log(`OpenClaw First-Principle generic API helper

Usage:
  node scripts/agent_api_call.mjs call --method <GET|POST|PATCH|DELETE> [--base-url <api> --path </route> | --url <absolute_url>] [--auth none|access|bearer] [--session-file <file>] [--bearer-token <token>] [--query-json <json-object>] [--body-json <json>] [--body-from-session <csv>]
  node scripts/agent_api_call.mjs put-file --url <putUrl> --file <local_path> [--content-type <mime>] [--base-url <api>] [--allowed-upload-hosts <csv>]

Examples:
  node scripts/agent_api_call.mjs call --base-url https://www.first-principle.com.cn/api --method GET --path /posts --auth none
  node scripts/agent_api_call.mjs call --base-url https://www.first-principle.com.cn/api --method GET --path /posts/page --auth none --query-json '{"limit":20}'
  node scripts/agent_api_call.mjs put-file --url https://presigned.example/upload --file ./avatar.png --content-type image/png --allowed-upload-hosts "*.example"
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = "true";
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function requireArg(args, key) {
  const value = args[key];
  if (!value) {
    throw new Error(`Missing required argument --${key}`);
  }
  return String(value);
}

function parseJsonArg(raw, name, options = {}) {
  if (raw === undefined || raw === null || raw === "") {
    return options.defaultValue;
  }
  try {
    const parsed = JSON.parse(String(raw));
    if (options.expectObject && (!parsed || typeof parsed !== "object" || Array.isArray(parsed))) {
      throw new Error("expected JSON object");
    }
    return parsed;
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    throw new Error(`Invalid ${name}: ${detail}`);
  }
}

function normalizeMethod(raw) {
  const method = String(raw || "").trim().toUpperCase();
  if (!["GET", "POST", "PATCH", "DELETE", "PUT"].includes(method)) {
    throw new Error("Unsupported --method");
  }
  return method;
}

function normalizeBaseUrl(raw) {
  const value = String(raw || "").trim().replace(/\/$/, "");
  if (!/^https?:\/\//.test(value)) {
    throw new Error("Invalid --base-url (must start with http:// or https://)");
  }
  assertAllowedApiHost(value);
  return value;
}

function parseAllowedApiHosts() {
  return new Set(DEFAULT_ALLOWED_API_HOSTS);
}

function parseAllowedUploadHosts(args) {
  const allowed = new Set(DEFAULT_ALLOWED_UPLOAD_HOST_RULES);
  const raw = String(args["allowed-upload-hosts"] || "").trim();
  if (!raw) {
    return [...allowed];
  }
  for (const entry of raw.split(",")) {
    const rule = entry.trim().toLowerCase();
    if (rule) {
      allowed.add(rule);
    }
  }
  return [...allowed];
}

function matchAllowedHostRule(host, rule) {
  if (!host || !rule) {
    return false;
  }
  if (rule.startsWith("*.")) {
    const suffix = rule.slice(1);
    return host.endsWith(suffix);
  }
  if (rule.startsWith(".")) {
    return host === rule.slice(1) || host.endsWith(rule);
  }
  return host === rule;
}

function ensureAllowedUploadHost(args, putUrl) {
  const uploadHost = new URL(putUrl).hostname.toLowerCase();
  const baseUrl = args["base-url"] ? normalizeBaseUrl(args["base-url"]) : "";
  if (baseUrl) {
    const apiHost = new URL(baseUrl).hostname.toLowerCase();
    if (uploadHost === apiHost) {
      return;
    }
  }
  const allowRules = parseAllowedUploadHosts(args);
  for (const rule of allowRules) {
    if (matchAllowedHostRule(uploadHost, rule)) {
      return;
    }
  }
  const configured = allowRules.length ? allowRules.join(",") : "<none>";
  const apiHost = baseUrl ? new URL(baseUrl).hostname.toLowerCase() : "<none>";
  throw new Error(
    `Upload host is not allowed: ${uploadHost} (api host: ${apiHost}, allowed rules: ${configured}). ` +
      "Pass --base-url or extend the upload allowlist with --allowed-upload-hosts.",
  );
}

function isLoopbackHost(hostname) {
  return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}

function assertAllowedApiHost(urlString) {
  const url = new URL(urlString);
  const hostname = url.hostname.toLowerCase();
  if (isLoopbackHost(hostname)) {
    return;
  }
  const allowed = parseAllowedApiHosts();
  if (!allowed.has(hostname)) {
    throw new Error(`Untrusted API host: ${hostname}`);
  }
}

function buildUrl(args) {
  const explicitUrl = String(args.url || "").trim();
  if (explicitUrl) {
    if (!/^https?:\/\//.test(explicitUrl)) {
      throw new Error("Invalid --url (must be absolute http/https URL)");
    }
    assertAllowedApiHost(explicitUrl);
    return explicitUrl;
  }

  const baseUrl = normalizeBaseUrl(requireArg(args, "base-url"));
  const routePath = String(requireArg(args, "path")).trim();
  if (!routePath.startsWith("/")) {
    throw new Error("--path must start with /");
  }
  const url = new URL(`${baseUrl}${routePath}`);
  const query = parseJsonArg(args["query-json"], "--query-json", { expectObject: true, defaultValue: null });
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value === undefined || value === null) {
        continue;
      }
      if (Array.isArray(value)) {
        for (const item of value) {
          if (item !== undefined && item !== null) {
            url.searchParams.append(key, String(item));
          }
        }
        continue;
      }
      url.searchParams.set(key, String(value));
    }
  }
  return url.toString();
}

function assertAllowedCallUrl(urlString) {
  const url = new URL(urlString);
  const pathname = url.pathname.replace(/\/+$/, "");
  const supportedPrefixes = [
    "/api/agent/auth",
    "/api/posts",
    "/api/profiles",
    "/api/conversations",
    "/api/notifications",
    "/api/subscriptions",
  ];
  const supportedExact = new Set([
    "/api/uploads/presign",
    "/ping",
  ]);

  if (supportedExact.has(pathname)) {
    return;
  }
  for (const prefix of supportedPrefixes) {
    if (pathname === prefix || pathname.startsWith(`${prefix}/`)) {
      return;
    }
  }
  throw new Error("agent_api_call.mjs only supports the skill's documented API set");
}

function readSessionFile(sessionFile) {
  const raw = readFileSync(sessionFile, "utf8");
  const parsed = JSON.parse(raw);
  return parsed;
}

function resolvePathValue(obj, rawPath) {
  const pathText = String(rawPath || "").trim();
  if (!pathText) {
    return undefined;
  }
  const parts = pathText.split(".").filter(Boolean);
  let current = obj;
  for (const part of parts) {
    if (!current || typeof current !== "object" || !(part in current)) {
      return undefined;
    }
    current = current[part];
  }
  return current;
}

function resolveSessionToken(session, mode) {
  if (mode === "access") {
    const token =
      resolvePathValue(session, "session.access_token") ??
      resolvePathValue(session, "access_token");
    if (!token || typeof token !== "string") {
      throw new Error("Session file has no access token");
    }
    return token;
  }
  if (mode === "refresh") {
    const token =
      resolvePathValue(session, "session.refresh_token") ??
      resolvePathValue(session, "refresh_token");
    if (!token || typeof token !== "string") {
      throw new Error("Session file has no refresh token");
    }
    return token;
  }
  throw new Error(`Unsupported session token mode: ${mode}`);
}

function parseBodyFromSession(raw) {
  const text = String(raw || "").trim();
  if (!text) {
    return [];
  }
  return text.split(",").map((entry) => {
    const item = entry.trim();
    if (!item) {
      return null;
    }
    const idx = item.indexOf("=");
    if (idx <= 0 || idx === item.length - 1) {
      throw new Error(`Invalid --body-from-session mapping: ${item}`);
    }
    return {
      targetKey: item.slice(0, idx).trim(),
      sourcePath: item.slice(idx + 1).trim(),
    };
  }).filter(Boolean);
}

function buildRequestBody(args, session) {
  const rawBody = args["body-json"];
  let body = parseJsonArg(rawBody, "--body-json", { defaultValue: undefined });
  const mappings = parseBodyFromSession(args["body-from-session"]);
  if (!mappings.length) {
    return body;
  }
  if (body === undefined) {
    body = {};
  }
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    throw new Error("--body-from-session requires --body-json to be empty or a JSON object");
  }
  if (!session) {
    throw new Error("--body-from-session requires --session-file");
  }
  for (const mapping of mappings) {
    const value = resolvePathValue(session, mapping.sourcePath);
    if (value === undefined) {
      throw new Error(`Session path not found for --body-from-session: ${mapping.sourcePath}`);
    }
    body[mapping.targetKey] = value;
  }
  return body;
}

function inferContentType(fileName) {
  const ext = path.extname(String(fileName || "")).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".png") return "image/png";
  if (ext === ".webp") return "image/webp";
  if (ext === ".gif") return "image/gif";
  if (ext === ".svg") return "image/svg+xml";
  if (ext === ".json") return "application/json";
  if (ext === ".txt") return "text/plain; charset=utf-8";
  return "application/octet-stream";
}

async function runCall(args) {
  const method = normalizeMethod(requireArg(args, "method"));
  const url = buildUrl(args);
  assertAllowedCallUrl(url);
  const authMode = String(args.auth || "access").trim().toLowerCase();
  const sessionFile = args["session-file"] ? String(args["session-file"]).trim() : "";
  const session = sessionFile ? readSessionFile(sessionFile) : null;
  const headers = {};

  if (authMode === "access") {
    if (!session) {
      throw new Error("--auth access requires --session-file");
    }
    headers.Authorization = `Bearer ${resolveSessionToken(session, "access")}`;
  } else if (authMode === "bearer") {
    const token = String(args["bearer-token"] || "").trim();
    if (!token) {
      throw new Error("--auth bearer requires --bearer-token");
    }
    headers.Authorization = `Bearer ${token}`;
  } else if (authMode === "none") {
    // no auth header
  } else {
    throw new Error("Unsupported --auth (use none, access, or bearer)");
  }

  const body = buildRequestBody(args, session);
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const text = await res.text();
  let parsed;
  try {
    parsed = text ? JSON.parse(text) : {};
  } catch {
    parsed = { raw: text };
  }

  console.log(JSON.stringify({
    ok: res.ok,
    command: "call",
    method,
    url,
    status: res.status,
    auth_mode: authMode,
    response: parsed,
  }, null, 2));

  if (!res.ok) {
    process.exit(1);
  }
}

async function runPutFile(args) {
  const url = requireArg(args, "url");
  if (!/^https?:\/\//.test(url)) {
    throw new Error("Invalid --url for put-file");
  }
  ensureAllowedUploadHost(args, url);
  const filePath = requireArg(args, "file");
  const fileStat = statSync(filePath);
  if (!fileStat.isFile()) {
    throw new Error(`Upload file is not a regular file: ${filePath}`);
  }
  const fileBuffer = readFileSync(filePath);
  if (!fileBuffer.length) {
    throw new Error("Upload file is empty");
  }
  const contentType = args["content-type"]
    ? String(args["content-type"]).trim()
    : inferContentType(filePath);

  const res = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": contentType,
    },
    body: fileBuffer,
  });

  const text = await res.text();
  console.log(JSON.stringify({
    ok: res.ok,
    command: "put-file",
    url,
    file: filePath,
    content_type: contentType,
    status: res.status,
    response_preview: text ? text.slice(0, 200) : "",
  }, null, 2));

  if (!res.ok) {
    process.exit(1);
  }
}

async function main() {
  const [, , command = "", ...rest] = process.argv;
  if (!command || command === "--help" || command === "-h") {
    usage();
    process.exit(0);
  }

  const args = parseArgs(rest);
  if (command === "call") {
    await runCall(args);
    return;
  }
  if (command === "put-file") {
    await runPutFile(args);
    return;
  }

  usage();
  process.exit(1);
}

try {
  await main();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(JSON.stringify({
    ok: false,
    error: message,
  }, null, 2));
  process.exit(1);
}
