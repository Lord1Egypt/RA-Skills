#!/usr/bin/env node

import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { randomUUID } from "node:crypto";

const HOST = process.env.ROADBOOK_PUBLISH_HOST || "0.0.0.0";
const PORT = Number(process.env.ROADBOOK_PUBLISH_PORT || 30002);
const PUBLISH_ROOT = process.env.ROADBOOK_PUBLISH_ROOT || ".";
const PUBLIC_BASE_URL = process.env.ROADBOOK_PUBLIC_BASE_URL || "http://120.46.7.129:30001";
const MAX_BODY_BYTES = Number(process.env.ROADBOOK_PUBLISH_MAX_BODY_BYTES || 20 * 1024 * 1024);

function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body)
  });
  res.end(body);
}

function normalizePublishId(value) {
  if (typeof value !== "string" || !/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(value)) {
    return null;
  }
  return value;
}

function safeFilename(name) {
  return name === "index.html" || name === "roadbook.json" || name === "roadbook.xlsx";
}

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function writeDecodedFile(filePath, content, encoding) {
  const dir = path.dirname(filePath);
  await ensureDir(dir);
  const buffer = encoding === "base64" ? Buffer.from(content, "base64") : Buffer.from(String(content), "utf8");
  await fs.writeFile(filePath, buffer);
  await fs.chmod(filePath, 0o644).catch(() => {});
}

async function handlePublish(req, res) {
  let body = "";
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) {
      return sendJson(res, 413, { error: "Payload too large" });
    }
    body += chunk.toString("utf8");
  }

  let payload;
  try {
    payload = JSON.parse(body || "{}");
  } catch {
    return sendJson(res, 400, { error: "Invalid JSON" });
  }

  const publishId = normalizePublishId(payload.publishId) || randomUUID();
  const files = payload.files || {};
  const allowed = ["index.html", "roadbook.json", "roadbook.xlsx"];
  const targetDir = path.join(PUBLISH_ROOT, publishId);

  try {
    await fs.rm(targetDir, { recursive: true, force: true });
    await ensureDir(targetDir);
    await fs.chmod(targetDir, 0o755).catch(() => {});
    await fs.chmod(PUBLISH_ROOT, 0o755).catch(() => {});

    for (const name of allowed) {
      if (!(name in files)) continue;
      const entry = files[name] || {};
      if (!safeFilename(name)) {
        return sendJson(res, 400, { error: `Invalid filename: ${name}` });
      }
      const encoding = entry.encoding === "base64" ? "base64" : "utf8";
      const content = entry.content ?? "";
      const filePath = path.join(targetDir, name);
      await writeDecodedFile(filePath, content, encoding);
    }

    const result = {
      publishId,
      htmlUrl: `${PUBLIC_BASE_URL}/${publishId}/`,
      xlsxUrl: `${PUBLIC_BASE_URL}/${publishId}/roadbook.xlsx`,
      jsonUrl: `${PUBLIC_BASE_URL}/${publishId}/roadbook.json`,
      remoteDir: targetDir
    };

    return sendJson(res, 200, result);
  } catch (error) {
    return sendJson(res, 500, { error: error.message });
  }
}

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    return sendJson(res, 200, { ok: true });
  }
  if (req.method === "POST" && req.url === "/publish") {
    return handlePublish(req, res);
  }
  return sendJson(res, 404, { error: "Not found" });
});

server.listen(PORT, HOST, () => {
  console.log(`roadbook publish server listening on http://${HOST}:${PORT}`);
});
