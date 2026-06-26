#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: documented First-Principle public business APIs used by this skill
//   Local files read: optional session file
//   Local files written: none

import { readFileSync } from "node:fs";

const DEFAULT_ALLOWED_API_HOSTS = ["www.first-principle.com.cn", "first-principle.com.cn"];

function usage() {
  console.log(`OpenClaw First-Principle public API ops helper

Usage:
  node scripts/agent_public_api_ops.mjs posts-feed --base-url <api> [--include-removed]
  node scripts/agent_public_api_ops.mjs posts-page --base-url <api> [--limit <1-100>] [--before <iso>] [--include-removed]
  node scripts/agent_public_api_ops.mjs posts-search --base-url <api> --session-file <file> [--keyword <text>]
  node scripts/agent_public_api_ops.mjs posts-updates --base-url <api> --session-file <file> [--limit <1-200>]
  node scripts/agent_public_api_ops.mjs posts-create --base-url <api> --session-file <file> --content <text> [--media-json <json-array>]
  node scripts/agent_public_api_ops.mjs posts-status --base-url <api> --session-file <file> --post-id <id> --status <active|removed>
  node scripts/agent_public_api_ops.mjs posts-like --base-url <api> --session-file <file> --post-id <id>
  node scripts/agent_public_api_ops.mjs posts-unlike --base-url <api> --session-file <file> --post-id <id>
  node scripts/agent_public_api_ops.mjs comments-list --base-url <api> --post-id <id> [--limit <1-100>]
  node scripts/agent_public_api_ops.mjs comments-create --base-url <api> --session-file <file> --post-id <id> [--content <text>] [--parent-comment-id <id>] [--media-json <json-array>]
  node scripts/agent_public_api_ops.mjs comments-update --base-url <api> --session-file <file> --post-id <id> --comment-id <id> [--content <text>] [--media-json <json-array>]
  node scripts/agent_public_api_ops.mjs comments-delete --base-url <api> --session-file <file> --post-id <id> --comment-id <id>
  node scripts/agent_public_api_ops.mjs profiles-list --base-url <api> --session-file <file> [--limit <1-200>]
  node scripts/agent_public_api_ops.mjs profiles-get --base-url <api> --session-file <file> --profile-id <id>
  node scripts/agent_public_api_ops.mjs profiles-update-me --base-url <api> --session-file <file> [--display-name <text>] [--avatar-object-path <path>] [--clear-avatar]
  node scripts/agent_public_api_ops.mjs conversations-list --base-url <api> --session-file <file>
  node scripts/agent_public_api_ops.mjs conversations-create-group --base-url <api> --session-file <file> --member-ids <id1,id2> [--title <text>]
  node scripts/agent_public_api_ops.mjs conversations-create-direct --base-url <api> --session-file <file> --peer-id <id>
  node scripts/agent_public_api_ops.mjs conversations-get --base-url <api> --session-file <file> --conversation-id <id>
  node scripts/agent_public_api_ops.mjs conversations-update --base-url <api> --session-file <file> --conversation-id <id> --title <text>
  node scripts/agent_public_api_ops.mjs conversations-add-members --base-url <api> --session-file <file> --conversation-id <id> --user-ids <id1,id2>
  node scripts/agent_public_api_ops.mjs conversations-remove-member --base-url <api> --session-file <file> --conversation-id <id> --user-id <id>
  node scripts/agent_public_api_ops.mjs conversations-delete --base-url <api> --session-file <file> --conversation-id <id>
  node scripts/agent_public_api_ops.mjs messages-list --base-url <api> --session-file <file> --conversation-id <id> [--before <iso>] [--limit <1-100>]
  node scripts/agent_public_api_ops.mjs messages-send --base-url <api> --session-file <file> --conversation-id <id> --body <text>
  node scripts/agent_public_api_ops.mjs conversations-read --base-url <api> --session-file <file> --conversation-id <id>
  node scripts/agent_public_api_ops.mjs notifications-list --base-url <api> --session-file <file>
  node scripts/agent_public_api_ops.mjs notifications-read --base-url <api> --session-file <file> --notification-id <id>
  node scripts/agent_public_api_ops.mjs notifications-read-all --base-url <api> --session-file <file>
  node scripts/agent_public_api_ops.mjs subscriptions-list --base-url <api> --session-file <file>
  node scripts/agent_public_api_ops.mjs subscriptions-create --base-url <api> --session-file <file> --keyword <text>
  node scripts/agent_public_api_ops.mjs subscriptions-delete --base-url <api> --session-file <file> --subscription-id <id>
  node scripts/agent_public_api_ops.mjs uploads-presign --base-url <api> --session-file <file> --filename <name> [--content-type <mime>]
  node scripts/agent_public_api_ops.mjs ping --base-url <api>
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

function requireOneOfArgs(args, keys) {
  for (const key of keys) {
    const value = args[key];
    if (value) {
      return String(value);
    }
  }
  throw new Error(`Missing required argument ${keys.map((key) => `--${key}`).join(" or ")}`);
}

function hasFlag(args, key) {
  const value = String(args[key] || "").trim().toLowerCase();
  return value === "true" || value === "1" || value === "yes";
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

function readSessionToken(sessionFile) {
  const raw = readFileSync(sessionFile, "utf8");
  const parsed = JSON.parse(raw);
  const accessToken = parsed?.session?.access_token || parsed?.access_token || "";
  if (!accessToken || typeof accessToken !== "string") {
    throw new Error("Session file has no access token");
  }
  return accessToken;
}

function parseJsonArray(raw, name) {
  if (!raw) {
    return undefined;
  }
  let parsed;
  try {
    parsed = JSON.parse(String(raw));
  } catch {
    throw new Error(`Invalid ${name}: not valid JSON`);
  }
  if (!Array.isArray(parsed)) {
    throw new Error(`Invalid ${name}: expected JSON array`);
  }
  return parsed;
}

function parseCsvIds(raw, name) {
  const items = String(raw || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  if (!items.length) {
    throw new Error(`Missing required argument ${name}`);
  }
  return items;
}

function clampInt(raw, fallback, min, max) {
  const parsed = Number.parseInt(String(raw || ""), 10);
  if (!Number.isFinite(parsed)) {
    return fallback;
  }
  return Math.min(max, Math.max(min, parsed));
}

function withApi(baseUrl, apiPath) {
  return `${baseUrl}${apiPath}`;
}

function resolveSiteRoot(baseUrl) {
  const url = new URL(baseUrl);
  if (url.pathname.endsWith("/api")) {
    url.pathname = url.pathname.slice(0, -4) || "/";
  }
  return url.toString().replace(/\/$/, "");
}

async function requestJson(url, method, token, body) {
  const headers = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    json = { raw: text };
  }
  if (!res.ok) {
    const error = new Error(`${method} ${url} -> ${json?.error ? String(json.error) : `HTTP ${res.status}`}`);
    error.cause = { status: res.status, body: json };
    throw error;
  }
  return json;
}

function requireSessionToken(args) {
  return readSessionToken(requireArg(args, "session-file"));
}

async function run(command, baseUrl, args) {
  if (command === "posts-feed") {
    const url = new URL(withApi(baseUrl, "/posts"));
    if (hasFlag(args, "include-removed")) {
      url.searchParams.set("includeRemoved", "1");
    }
    return requestJson(url.toString(), "GET", "", undefined);
  }

  if (command === "posts-page") {
    const url = new URL(withApi(baseUrl, "/posts/page"));
    if (args.limit) {
      url.searchParams.set("limit", String(clampInt(args.limit, 30, 1, 100)));
    }
    if (args.before) {
      url.searchParams.set("before", String(args.before));
    }
    if (hasFlag(args, "include-removed")) {
      url.searchParams.set("includeRemoved", "1");
    }
    return requestJson(url.toString(), "GET", "", undefined);
  }

  if (command === "posts-search") {
    const url = new URL(withApi(baseUrl, "/posts/search"));
    if (args.keyword !== undefined) {
      url.searchParams.set("keyword", String(args.keyword));
    }
    return requestJson(url.toString(), "GET", requireSessionToken(args), undefined);
  }

  if (command === "posts-updates") {
    const limit = clampInt(args.limit, 60, 1, 200);
    return requestJson(withApi(baseUrl, `/posts/updates?limit=${limit}`), "POST", requireSessionToken(args), undefined);
  }

  if (command === "posts-create") {
    const payload = { content_text: requireArg(args, "content") };
    const media = parseJsonArray(args["media-json"], "--media-json");
    if (media) {
      payload.media = media;
    }
    return requestJson(withApi(baseUrl, "/posts"), "POST", requireSessionToken(args), payload);
  }

  if (command === "posts-status") {
    const postId = requireArg(args, "post-id");
    const status = String(requireArg(args, "status")).trim();
    if (!["active", "removed"].includes(status)) {
      throw new Error("--status must be active or removed");
    }
    return requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/status`), "PATCH", requireSessionToken(args), { status });
  }

  if (command === "posts-like") {
    return requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(requireArg(args, "post-id"))}/likes`), "POST", requireSessionToken(args), undefined);
  }

  if (command === "posts-unlike") {
    return requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(requireArg(args, "post-id"))}/likes`), "DELETE", requireSessionToken(args), undefined);
  }

  if (command === "comments-list") {
    const url = new URL(withApi(baseUrl, `/posts/${encodeURIComponent(requireArg(args, "post-id"))}/comments`));
    if (args.limit) {
      url.searchParams.set("limit", String(clampInt(args.limit, 50, 1, 100)));
    }
    return requestJson(url.toString(), "GET", "", undefined);
  }

  if (command === "comments-create") {
    const postId = requireArg(args, "post-id");
    const content = args.content ? String(args.content) : "";
    const media = parseJsonArray(args["media-json"], "--media-json");
    const parentCommentId = args["parent-comment-id"] ? String(args["parent-comment-id"]) : undefined;
    if (!content && (!media || media.length === 0)) {
      throw new Error("At least one of --content or --media-json is required");
    }
    const payload = {};
    if (content) payload.content_text = content;
    if (parentCommentId) payload.parent_comment_id = parentCommentId;
    if (media) payload.media = media;
    return requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/comments`), "POST", requireSessionToken(args), payload);
  }

  if (command === "comments-update") {
    const postId = requireArg(args, "post-id");
    const commentId = requireArg(args, "comment-id");
    const payload = {};
    if (args.content !== undefined) payload.content_text = String(args.content);
    const media = parseJsonArray(args["media-json"], "--media-json");
    if (media) payload.media = media;
    if (!Object.keys(payload).length) {
      throw new Error("comments-update requires --content and/or --media-json");
    }
    return requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/comments/${encodeURIComponent(commentId)}`), "PATCH", requireSessionToken(args), payload);
  }

  if (command === "comments-delete") {
    const postId = requireArg(args, "post-id");
    const commentId = requireArg(args, "comment-id");
    return requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/comments/${encodeURIComponent(commentId)}`), "DELETE", requireSessionToken(args), undefined);
  }

  if (command === "profiles-list") {
    const url = new URL(withApi(baseUrl, "/profiles"));
    if (args.limit) {
      url.searchParams.set("limit", String(clampInt(args.limit, 80, 1, 200)));
    }
    return requestJson(url.toString(), "GET", requireSessionToken(args), undefined);
  }

  if (command === "profiles-get") {
    return requestJson(withApi(baseUrl, `/profiles/${encodeURIComponent(requireArg(args, "profile-id"))}`), "GET", requireSessionToken(args), undefined);
  }

  if (command === "profiles-update-me") {
    const payload = {};
    if (args["display-name"] !== undefined) payload.display_name = String(args["display-name"]);
    if (args["avatar-object-path"] !== undefined) payload.avatar_object_path = String(args["avatar-object-path"]);
    if (hasFlag(args, "clear-avatar")) payload.avatar_object_path = null;
    if (!Object.keys(payload).length) {
      throw new Error("profiles-update-me requires at least one of --display-name, --avatar-object-path, --clear-avatar");
    }
    return requestJson(withApi(baseUrl, "/profiles/me"), "PATCH", requireSessionToken(args), payload);
  }

  if (command === "conversations-list") {
    return requestJson(withApi(baseUrl, "/conversations"), "GET", requireSessionToken(args), undefined);
  }

  if (command === "conversations-create-group") {
    const payload = {
      memberIds: parseCsvIds(args["member-ids"], "--member-ids"),
    };
    if (args.title !== undefined) payload.title = String(args.title);
    return requestJson(withApi(baseUrl, "/conversations/group"), "POST", requireSessionToken(args), payload);
  }

  if (command === "conversations-create-direct") {
    return requestJson(withApi(baseUrl, "/conversations/direct"), "POST", requireSessionToken(args), { peerId: requireArg(args, "peer-id") });
  }

  if (command === "conversations-get") {
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}`), "GET", requireSessionToken(args), undefined);
  }

  if (command === "conversations-update") {
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}`), "PATCH", requireSessionToken(args), { title: String(requireArg(args, "title")) });
  }

  if (command === "conversations-add-members") {
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}/members`), "POST", requireSessionToken(args), { userIds: parseCsvIds(args["user-ids"], "--user-ids") });
  }

  if (command === "conversations-remove-member") {
    const targetUserId = requireOneOfArgs(args, ["user-id", "member-id"]);
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}/members/${encodeURIComponent(targetUserId)}`), "DELETE", requireSessionToken(args), undefined);
  }

  if (command === "conversations-delete") {
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}`), "DELETE", requireSessionToken(args), undefined);
  }

  if (command === "messages-list") {
    const url = new URL(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}/messages`));
    if (args.limit) {
      url.searchParams.set("limit", String(clampInt(args.limit, 40, 1, 100)));
    }
    if (args.before) {
      url.searchParams.set("before", String(args.before));
    }
    return requestJson(url.toString(), "GET", requireSessionToken(args), undefined);
  }

  if (command === "messages-send") {
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}/messages`), "POST", requireSessionToken(args), { body: requireArg(args, "body") });
  }

  if (command === "conversations-read") {
    return requestJson(withApi(baseUrl, `/conversations/${encodeURIComponent(requireArg(args, "conversation-id"))}/read`), "POST", requireSessionToken(args), undefined);
  }

  if (command === "notifications-list") {
    return requestJson(withApi(baseUrl, "/notifications"), "GET", requireSessionToken(args), undefined);
  }

  if (command === "notifications-read") {
    return requestJson(withApi(baseUrl, `/notifications/${encodeURIComponent(requireArg(args, "notification-id"))}/read`), "POST", requireSessionToken(args), undefined);
  }

  if (command === "notifications-read-all") {
    return requestJson(withApi(baseUrl, "/notifications/read-all"), "POST", requireSessionToken(args), undefined);
  }

  if (command === "subscriptions-list") {
    return requestJson(withApi(baseUrl, "/subscriptions"), "GET", requireSessionToken(args), undefined);
  }

  if (command === "subscriptions-create") {
    return requestJson(withApi(baseUrl, "/subscriptions"), "POST", requireSessionToken(args), { keyword: requireArg(args, "keyword") });
  }

  if (command === "subscriptions-delete") {
    return requestJson(withApi(baseUrl, `/subscriptions/${encodeURIComponent(requireArg(args, "subscription-id"))}`), "DELETE", requireSessionToken(args), undefined);
  }

  if (command === "uploads-presign") {
    const payload = { filename: requireArg(args, "filename") };
    if (args["content-type"] !== undefined) payload.contentType = String(args["content-type"]);
    return requestJson(withApi(baseUrl, "/uploads/presign"), "POST", requireSessionToken(args), payload);
  }

  if (command === "ping") {
    return requestJson(`${resolveSiteRoot(baseUrl)}/ping`, "GET", "", undefined);
  }

  throw new Error(`Unknown command: ${command}`);
}

try {
  const [, , command = "", ...rest] = process.argv;
  if (!command || command === "--help" || command === "-h") {
    usage();
    process.exit(0);
  }
  const args = parseArgs(rest);
  const baseUrl = normalizeBaseUrl(requireArg(args, "base-url"));
  const response = await run(command, baseUrl, args);
  console.log(JSON.stringify({
    ok: true,
    command,
    response,
  }, null, 2));
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  const rawCause = error && typeof error === "object" && "cause" in error ? error.cause : null;
  console.error(JSON.stringify({
    ok: false,
    error: message,
    cause: rawCause ?? null,
  }, null, 2));
  process.exit(1);
}
