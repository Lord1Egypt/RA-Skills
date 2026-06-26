#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: <base-url>/agent/auth/me, <base-url>/posts*, <base-url>/profiles*, <base-url>/uploads/presign, PUT <presigned-url>
//   Local files read: required session file, optional local avatar file for upload-avatar
//   Local files written: none

import { readFileSync, statSync } from "node:fs";
import path from "node:path";

const DEFAULT_ALLOWED_API_HOSTS = ["www.first-principle.com.cn", "first-principle.com.cn"];
const DEFAULT_ALLOWED_UPLOAD_HOST_RULES = ["*.aliyuncs.com", ".first-principle.com.cn"];

function usage() {
  console.log(`OpenClaw First-Principle social ops helper

Usage:
  node scripts/agent_social_ops.mjs whoami --base-url <api> --session-file <file>
  node scripts/agent_social_ops.mjs feed-updates --base-url <api> --session-file <file> [--limit <1-200>]
  node scripts/agent_social_ops.mjs create-post --base-url <api> --session-file <file> --content <text> [--media-json <json-array>]
  node scripts/agent_social_ops.mjs like-post --base-url <api> --session-file <file> --post-id <id>
  node scripts/agent_social_ops.mjs unlike-post --base-url <api> --session-file <file> --post-id <id>
  node scripts/agent_social_ops.mjs comment-post --base-url <api> --session-file <file> --post-id <id> [--content <text>] [--parent-comment-id <id>] [--media-json <json-array>]
  node scripts/agent_social_ops.mjs delete-comment --base-url <api> --session-file <file> --post-id <id> --comment-id <id>
  node scripts/agent_social_ops.mjs remove-post --base-url <api> --session-file <file> --post-id <id>
  node scripts/agent_social_ops.mjs update-profile --base-url <api> --session-file <file> [--display-name <text>] [--avatar-object-path <path>] [--clear-avatar]
  node scripts/agent_social_ops.mjs upload-avatar --base-url <api> --session-file <file> --file <local_path> [--filename <name>] [--content-type <mime>] [--display-name <text>] [--allowed-upload-hosts <csv>]
  node scripts/agent_social_ops.mjs smoke-social --base-url <api> --session-file <file> [--post-content <text>] [--comment-content <text>]
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

function normalizeBaseUrl(raw) {
  const baseUrl = String(raw || "").trim().replace(/\/$/, "");
  if (!/^https?:\/\//.test(baseUrl)) {
    throw new Error("Invalid --base-url (must start with http:// or https://)");
  }
  assertAllowedApiHost(baseUrl);
  return baseUrl;
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

function parseMediaJson(raw, fieldName) {
  if (!raw) {
    return undefined;
  }
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new Error(`Invalid ${fieldName}: not valid JSON`);
  }
  if (!Array.isArray(parsed)) {
    throw new Error(`Invalid ${fieldName}: expected JSON array`);
  }
  return parsed;
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

function ensureAllowedUploadHost(baseUrl, putUrl, args) {
  const apiHost = new URL(baseUrl).hostname.toLowerCase();
  const uploadHost = new URL(putUrl).hostname.toLowerCase();
  if (uploadHost === apiHost) {
    return {
      uploadHost,
      allowedBy: "base-url-host",
    };
  }

  const allowRules = parseAllowedUploadHosts(args);
  for (const rule of allowRules) {
    if (matchAllowedHostRule(uploadHost, rule)) {
      return {
        uploadHost,
        allowedBy: rule,
      };
    }
  }

  const configured = allowRules.length ? allowRules.join(",") : "<none>";
  throw new Error(
    `Upload host is not allowed: ${uploadHost} (api host: ${apiHost}, allowed rules: ${configured}). ` +
      "Pass --allowed-upload-hosts to extend the default upload allowlist.",
  );
}

async function requestJson(url, method, token, body) {
  const headers = {
    Authorization: `Bearer ${token}`,
  };
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
    const message = json?.error ? String(json.error) : `HTTP ${res.status}`;
    const error = new Error(`${method} ${url} -> ${message}`);
    error.cause = { status: res.status, body: json };
    throw error;
  }
  return json;
}

async function requestUploadPut(url, contentType, body) {
  const res = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": contentType,
    },
    body,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`PUT ${url} -> HTTP ${res.status}${text ? ` (${text.slice(0, 200)})` : ""}`);
  }
}

function withApi(baseUrl, path) {
  return `${baseUrl}${path}`;
}

function tokenPreview(token) {
  return token.length > 12 ? `${token.slice(0, 12)}...` : "***";
}

function inferContentType(fileName) {
  const ext = path.extname(String(fileName || "")).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") {
    return "image/jpeg";
  }
  if (ext === ".png") {
    return "image/png";
  }
  if (ext === ".webp") {
    return "image/webp";
  }
  if (ext === ".gif") {
    return "image/gif";
  }
  if (ext === ".svg") {
    return "image/svg+xml";
  }
  if (ext === ".bmp") {
    return "image/bmp";
  }
  return "application/octet-stream";
}

async function doWhoAmI(baseUrl, token) {
  const data = await requestJson(withApi(baseUrl, "/agent/auth/me"), "GET", token);
  return {
    command: "whoami",
    user: data.user || null,
    profile: data.profile || null,
    identity: data.identity || null,
  };
}

async function doFeedUpdates(baseUrl, token, args) {
  const limitRaw = args.limit ? Number(args.limit) : 20;
  const limit = Number.isFinite(limitRaw) ? Math.max(1, Math.min(200, Math.floor(limitRaw))) : 20;
  const data = await requestJson(withApi(baseUrl, `/posts/updates?limit=${limit}`), "POST", token);
  return {
    command: "feed-updates",
    window: data.window || null,
    item_count: Array.isArray(data.items) ? data.items.length : 0,
    items: data.items || [],
  };
}

async function doCreatePost(baseUrl, token, args) {
  const content = requireArg(args, "content");
  const media = parseMediaJson(args["media-json"], "--media-json");
  const payload = { content_text: content };
  if (media) {
    payload.media = media;
  }
  const data = await requestJson(withApi(baseUrl, "/posts"), "POST", token, payload);
  return {
    command: "create-post",
    post_id: data.id || null,
    raw: data,
  };
}

async function doLike(baseUrl, token, args, methodName) {
  const postId = requireArg(args, "post-id");
  const method = methodName === "like-post" ? "POST" : "DELETE";
  const data = await requestJson(withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/likes`), method, token);
  return {
    command: methodName,
    post_id: postId,
    liked: Boolean(data.liked),
  };
}

async function doComment(baseUrl, token, args) {
  const postId = requireArg(args, "post-id");
  const content = args.content ? String(args.content) : "";
  const media = parseMediaJson(args["media-json"], "--media-json");
  const parentCommentId = args["parent-comment-id"] ? String(args["parent-comment-id"]) : undefined;

  if (!content && (!media || media.length === 0)) {
    throw new Error("At least one of --content or --media-json is required");
  }

  const payload = {};
  if (content) {
    payload.content_text = content;
  }
  if (parentCommentId) {
    payload.parent_comment_id = parentCommentId;
  }
  if (media) {
    payload.media = media;
  }

  const data = await requestJson(
    withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/comments`),
    "POST",
    token,
    payload,
  );
  return {
    command: "comment-post",
    post_id: postId,
    comment_id: data.id || null,
    raw: data,
  };
}

async function doDeleteComment(baseUrl, token, args) {
  const postId = requireArg(args, "post-id");
  const commentId = requireArg(args, "comment-id");
  const data = await requestJson(
    withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/comments/${encodeURIComponent(commentId)}`),
    "DELETE",
    token,
  );
  return {
    command: "delete-comment",
    post_id: postId,
    comment_id: commentId,
    ok: Boolean(data.ok),
  };
}

async function doRemovePost(baseUrl, token, args) {
  const postId = requireArg(args, "post-id");
  const data = await requestJson(
    withApi(baseUrl, `/posts/${encodeURIComponent(postId)}/status`),
    "PATCH",
    token,
    { status: "removed" },
  );
  return {
    command: "remove-post",
    post_id: postId,
    ok: Boolean(data.ok),
  };
}

async function doUpdateProfile(baseUrl, token, args) {
  const payload = {};
  if (Object.prototype.hasOwnProperty.call(args, "display-name")) {
    payload.display_name = String(args["display-name"]);
  }
  if (Object.prototype.hasOwnProperty.call(args, "avatar-object-path")) {
    payload.avatar_object_path = String(args["avatar-object-path"]);
  }
  if (String(args["clear-avatar"] || "").toLowerCase() === "true") {
    payload.avatar_object_path = null;
  }
  if (!Object.keys(payload).length) {
    throw new Error("update-profile requires at least one of --display-name, --avatar-object-path, --clear-avatar");
  }

  const data = await requestJson(withApi(baseUrl, "/profiles/me"), "PATCH", token, payload);
  return {
    command: "update-profile",
    profile: data,
  };
}

async function doUploadAvatar(baseUrl, token, args) {
  const filePath = requireArg(args, "file");
  const fileStat = statSync(filePath);
  if (!fileStat.isFile()) {
    throw new Error(`Avatar file is not a regular file: ${filePath}`);
  }
  const fileBuffer = readFileSync(filePath);
  if (!fileBuffer.length) {
    throw new Error("Avatar file is empty");
  }

  const filename = args.filename ? String(args.filename).trim() : path.basename(filePath);
  if (!filename) {
    throw new Error("Unable to determine upload filename");
  }
  const contentType = args["content-type"]
    ? String(args["content-type"]).trim()
    : inferContentType(filename);

  const presign = await requestJson(withApi(baseUrl, "/uploads/presign"), "POST", token, {
    filename,
    contentType,
  });
  const putUrl = presign?.putUrl ? String(presign.putUrl) : "";
  const objectPath = presign?.object_path ? String(presign.object_path) : "";
  if (!putUrl || !objectPath) {
    throw new Error("Invalid presign response: missing putUrl or object_path");
  }
  const uploadHostDecision = ensureAllowedUploadHost(baseUrl, putUrl, args);

  await requestUploadPut(putUrl, contentType || "application/octet-stream", fileBuffer);

  const profilePayload = {
    avatar_object_path: objectPath,
  };
  if (Object.prototype.hasOwnProperty.call(args, "display-name")) {
    profilePayload.display_name = String(args["display-name"]);
  }

  const profile = await requestJson(withApi(baseUrl, "/profiles/me"), "PATCH", token, profilePayload);
  return {
    command: "upload-avatar",
    file: filePath,
    object_path: objectPath,
    upload_host: uploadHostDecision.uploadHost,
    upload_host_allowed_by: uploadHostDecision.allowedBy,
    get_url: presign?.getUrl || null,
    media_type: presign?.media_type || null,
    profile,
  };
}

async function doSmokeSocial(baseUrl, token, args) {
  const postContent = args["post-content"] || `OpenClaw smoke post ${new Date().toISOString()}`;
  const commentContent = args["comment-content"] || "OpenClaw smoke comment";

  const create = await doCreatePost(baseUrl, token, { content: postContent });
  if (!create.post_id) {
    throw new Error("Smoke failed: create-post did not return post_id");
  }

  const like = await doLike(baseUrl, token, { "post-id": create.post_id }, "like-post");
  const comment = await doComment(baseUrl, token, {
    "post-id": create.post_id,
    content: commentContent,
  });

  const unlike = await doLike(baseUrl, token, { "post-id": create.post_id }, "unlike-post");
  let deleteComment = null;
  if (comment.comment_id) {
    deleteComment = await doDeleteComment(baseUrl, token, {
      "post-id": create.post_id,
      "comment-id": comment.comment_id,
    });
  }
  const removePost = await doRemovePost(baseUrl, token, { "post-id": create.post_id });

  return {
    command: "smoke-social",
    ok: true,
    post_id: create.post_id,
    comment_id: comment.comment_id || null,
    steps: {
      create_post: create,
      like_post: like,
      comment_post: comment,
      unlike_post: unlike,
      delete_comment: deleteComment,
      remove_post: removePost,
    },
  };
}

function pickHint(errorMessage, cause) {
  const errorCode =
    cause &&
    typeof cause === "object" &&
    cause.body &&
    typeof cause.body === "object" &&
    typeof cause.body.code === "string"
      ? cause.body.code
      : "";

  if (
    errorCode === "HUMAN_EMAIL_NOT_VERIFIED" ||
    errorCode === "AGENT_DID_IDENTITY_INACTIVE" ||
    errorMessage.includes("Verified identity required")
  ) {
    return "Confirm this DID account has active agent identity mapping on backend.";
  }
  if (errorMessage.includes("Missing authorization") || errorMessage.includes("Session file has no access token")) {
    return "Run DID login again and save a fresh session file.";
  }
  if (errorMessage.includes("401") || errorMessage.includes("jwt")) {
    return "Token may be expired. Re-run DID login to refresh the session.";
  }
  if (errorMessage.includes("403")) {
    return "Check permission scope for this agent and endpoint.";
  }
  if (errorMessage.includes("avatar_object_path")) {
    return "Use /uploads/presign first, then PATCH /profiles/me with returned object_path.";
  }
  if (errorMessage.includes("Upload host is not allowed")) {
    return "Allow the presigned upload host via --allowed-upload-hosts.";
  }
  return "Check request parameters and API reachability.";
}

async function main() {
  const [, , command = "", ...rest] = process.argv;
  if (!command || command === "--help" || command === "-h") {
    usage();
    process.exit(0);
  }
  const args = parseArgs(rest);
  const baseUrl = normalizeBaseUrl(requireArg(args, "base-url"));
  const sessionFile = requireArg(args, "session-file");
  const token = readSessionToken(sessionFile);

  let result;
  if (command === "whoami") {
    result = await doWhoAmI(baseUrl, token);
  } else if (command === "feed-updates") {
    result = await doFeedUpdates(baseUrl, token, args);
  } else if (command === "create-post") {
    result = await doCreatePost(baseUrl, token, args);
  } else if (command === "like-post") {
    result = await doLike(baseUrl, token, args, "like-post");
  } else if (command === "unlike-post") {
    result = await doLike(baseUrl, token, args, "unlike-post");
  } else if (command === "comment-post") {
    result = await doComment(baseUrl, token, args);
  } else if (command === "delete-comment") {
    result = await doDeleteComment(baseUrl, token, args);
  } else if (command === "remove-post") {
    result = await doRemovePost(baseUrl, token, args);
  } else if (command === "update-profile") {
    result = await doUpdateProfile(baseUrl, token, args);
  } else if (command === "upload-avatar") {
    result = await doUploadAvatar(baseUrl, token, args);
  } else if (command === "smoke-social") {
    result = await doSmokeSocial(baseUrl, token, args);
  } else {
    usage();
    process.exit(1);
  }

  console.log(JSON.stringify({
    ok: true,
    token_preview: tokenPreview(token),
    ...result,
  }, null, 2));
}

try {
  await main();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  const rawCause = error && typeof error === "object" && "cause" in error ? error.cause : null;
  let cause = null;
  if (rawCause && typeof rawCause === "object") {
    const c = rawCause;
    cause = {
      code: typeof c.code === "string" ? c.code : null,
      errno: typeof c.errno === "number" ? c.errno : null,
      syscall: typeof c.syscall === "string" ? c.syscall : null,
      hostname: typeof c.hostname === "string" ? c.hostname : null,
      address: typeof c.address === "string" ? c.address : null,
      port: typeof c.port === "number" ? c.port : null,
      status: typeof c.status === "number" ? c.status : null,
      body: c.body !== undefined ? c.body : null,
    };
  } else if (rawCause !== null && rawCause !== undefined) {
    cause = String(rawCause);
  }
  console.error(JSON.stringify({
    ok: false,
    error: message,
    hint: pickHint(message, cause),
    cause,
  }, null, 2));
  process.exit(1);
}
