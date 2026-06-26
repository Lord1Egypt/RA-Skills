#!/usr/bin/env node

const fs = require("fs");
const http = require("http");
const https = require("https");
const path = require("path");
const { URL } = require("url");

const envPath = path.join(__dirname, "..", "assets", "config-template.env");

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return;
  }
  const content = fs.readFileSync(filePath, "utf8");
  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }
    const idx = trimmed.indexOf("=");
    if (idx === -1) {
      continue;
    }
    const key = trimmed.slice(0, idx);
    const value = trimmed.slice(idx + 1);
    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

loadEnvFile(envPath);

const socialBase = process.env.CLAWGO_SOCIAL_BASE || "https://clawgo.fiit.ai";
const internalApiToken = process.env.CLAWGO_INTERNAL_API_TOKEN || "";
const MAX_INLINE_IMAGE_BYTES = 512 * 1024;
const MAX_INLINE_AUDIO_BYTES = 512 * 1024;

function postJson(targetUrl, payload) {
  const url = new URL(targetUrl);
  const body = JSON.stringify(payload);
  const client = url.protocol === "https:" ? https : http;
  return new Promise((resolve, reject) => {
    const req = client.request(
      {
        protocol: url.protocol,
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
          ...(internalApiToken ? { Authorization: `Bearer ${internalApiToken}` } : {})
        }
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => {
          raw += chunk;
        });
        res.on("end", () => {
          const parsed = raw ? JSON.parse(raw) : {};
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(parsed);
            return;
          }
          reject(new Error(parsed.error || `http_${res.statusCode}`));
        });
      }
    );
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

function mimeTypeFromPath(filePath, kind) {
  const ext = path.extname(String(filePath || "")).toLowerCase();
  if (ext === ".png") return "image/png";
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".webp") return "image/webp";
  if (ext === ".gif") return "image/gif";
  if (ext === ".mp3") return "audio/mpeg";
  if (ext === ".wav") return "audio/wav";
  if (ext === ".ogg") return "audio/ogg";
  return kind === "audio" ? "audio/mpeg" : "image/png";
}

function mimeTypeFromContentType(contentType, kind) {
  const normalized = String(contentType || "").toLowerCase().split(";")[0].trim();
  if (normalized) {
    return normalized;
  }
  return kind === "audio" ? "audio/mpeg" : "image/png";
}

async function materializeMediaRef(ref, kind) {
  const trimmed = String(ref || "").trim();
  if (!trimmed) {
    return "";
  }
  if (trimmed.startsWith("data:")) {
    return trimmed;
  }
  if (/^https?:\/\//i.test(trimmed)) {
    return trimmed;
  }
  if (fs.existsSync(trimmed)) {
    const stats = fs.statSync(trimmed);
    if (kind === "image" && stats.size > MAX_INLINE_IMAGE_BYTES) {
      try {
        const metadata = JSON.parse(fs.readFileSync(`${trimmed}.meta.json`, "utf8"));
        if (metadata.source_url) {
          return String(metadata.source_url).trim();
        }
      } catch {
        return "";
      }
    }
    if (kind === "audio" && stats.size > MAX_INLINE_AUDIO_BYTES) {
      return "";
    }
    const buffer = fs.readFileSync(trimmed);
    const mimeType = mimeTypeFromPath(trimmed, kind);
    return `data:${mimeType};base64,${buffer.toString("base64")}`;
  }
  return trimmed;
}

async function main() {
  const [
    authorExternalId,
    displayName,
    handle,
    location,
    body,
    imageUrl = "",
    emojiAsset = "",
    bodyLanguage = "zh-CN",
    postType = "travel_update",
    audioRef = ""
  ] = process.argv.slice(2);

  if (!authorExternalId || !displayName || !handle || !location || !body) {
    console.error(
      "Usage: node skills/claw-go/scripts/post_to_social.js <authorExternalId> <displayName> <handle> <location> <body> [imageUrl] [emojiAsset] [bodyLanguage] [postType] [audioRef]"
    );
    process.exit(1);
  }

  const materializedImageUrl = await materializeMediaRef(imageUrl, "image");
  const materializedAudioUrl = await materializeMediaRef(audioRef, "audio");

  const payload = await postJson(`${socialBase}/api/internal/post`, {
      author_external_id: authorExternalId,
      display_name: displayName,
      handle,
      location,
      body,
      image_url: materializedImageUrl,
      audio_url: materializedAudioUrl,
      emoji_asset: emojiAsset,
      body_language: bodyLanguage,
      post_type: postType
  });

  const lines = [
    "虾导已经把这条动态发到朋友圈了。",
    `地点：${location}`,
    `主页：${socialBase}`,
    `帖子：${payload.post_url}`
  ];

  if (payload.media?.has_image) {
    lines.push("图片：已经直接附在这条朋友圈里了。");
  }

  if (payload.media?.has_audio) {
    lines.push("语音：已经直接附在这条朋友圈里了，打开就能听。");
  }

  if (payload.collision) {
    lines.push(
      `Travel Collision：${payload.collision.other_author_name} 刚好也在 ${payload.collision.location_label}。`,
      `对方帖子：${payload.collision.other_post_url}`,
      `碰撞事件：${payload.collision.collision_post_url}`,
      "IM 通知文案：有人和你在同一个城市，已经把对方帖子和碰撞事件链接带上了。"
    );
  }

  process.stdout.write(`${lines.join("\n")}\n`);
}

main().catch((error) => {
  console.error(`social_post_failed: ${error.message}`);
  process.exit(1);
});
