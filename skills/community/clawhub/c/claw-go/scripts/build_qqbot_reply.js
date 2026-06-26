#!/usr/bin/env node

/**
 * Build a QQ-ready reply block for 虾游记.
 *
 * Usage:
 *   node scripts/build_qqbot_reply.js "港口篇" "打卡虾" "Lisbon" "coastal sunset walk" \
 *     "旅伴，我发来一张新明信片。虾游记今天翻到港口篇了。"
 *   node scripts/build_qqbot_reply.js "港口篇" "打卡虾" "Lisbon" "coastal sunset walk" \
 *     "旅伴，我发来一张新明信片。虾游记今天翻到港口篇了。" "postcard" "zh" \
 *     '{"name":"Miso","species":"duck","rarity":"rare","hat":"wizard","eye":"✦","shiny":false}'
 */

const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");

const scriptPath = path.join(__dirname, "generate_media_bundle.js");
const args = process.argv.slice(2);

function normalizeQqMediaRef(value) {
  if (!value) {
    return null;
  }
  const trimmed = String(value).trim();
  if (!trimmed) {
    return null;
  }
  if (trimmed.startsWith("file:///")) {
    return decodeURIComponent(trimmed.replace(/^file:\/\//, ""));
  }
  return trimmed;
}

function extensionFromContentType(contentType) {
  const normalized = String(contentType || "").toLowerCase().split(";")[0].trim();
  if (normalized === "image/png") return ".png";
  if (normalized === "image/jpeg") return ".jpg";
  if (normalized === "image/webp") return ".webp";
  if (normalized === "image/gif") return ".gif";
  return "";
}

function extensionFromUrl(value) {
  try {
    const parsed = new URL(value);
    const ext = path.extname(parsed.pathname || "");
    return ext && ext.length <= 8 ? ext : "";
  } catch {
    return "";
  }
}

async function materializeImageRef(imageRef, requestType) {
  if (!imageRef) {
    return null;
  }
  if (!/^https?:\/\//i.test(imageRef)) {
    return imageRef;
  }

  const response = await fetch(imageRef);
  if (!response.ok) {
    throw new Error(`image_download_failed:${response.status}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  const ext =
    extensionFromContentType(response.headers.get("content-type")) || extensionFromUrl(imageRef) || ".png";
  const filename = `clawgo-${requestType || "image"}-${Date.now()}${ext}`;
  const filePath = path.join(os.tmpdir(), filename);
  fs.writeFileSync(filePath, Buffer.from(arrayBuffer));
  fs.writeFileSync(
    `${filePath}.meta.json`,
    JSON.stringify(
      {
        source_url: imageRef,
        downloaded_at: new Date().toISOString()
      },
      null,
      2
    ) + "\n"
  );
  return filePath;
}

(async () => {
  const raw = execFileSync(process.execPath, [scriptPath, ...args], {
    encoding: "utf8",
    maxBuffer: 10 * 1024 * 1024
  });

  const bundle = JSON.parse(raw);
  const lines = [];
  const isSelfie = bundle.request_type === "selfie";

  if (isSelfie && !bundle.image_url) {
    throw new Error("selfie request produced no image_url");
  }

  const imageRef = await materializeImageRef(normalizeQqMediaRef(bundle.image_url), bundle.request_type);
  const audioRef = normalizeQqMediaRef(bundle.audio_path);
  const companion = bundle.companion && typeof bundle.companion === "object" ? bundle.companion : null;

  lines.push(isSelfie ? "旅伴，这张是本虾刚给你拍的自拍。" : "旅伴，收虾导的现场播报。");
  lines.push(
    isSelfie
      ? `虾游记翻到${bundle.chapter}了，我正在 ${bundle.destination} 给你举钳比镜头。`
      : `虾游记翻到${bundle.chapter}了，这次落脚在 ${bundle.destination}。`
  );
  if (companion?.name) {
    lines.push(
      isSelfie
        ? `Buddy 旅伴兽 ${companion.name} 也挤进了镜头里。`
        : `Buddy 旅伴兽 ${companion.name} 正在旁边蹭镜头。`
    );
  }
  lines.push(bundle.voice_script);

  if (imageRef) {
    lines.push(`<qqimg>${imageRef}</qqimg>`);
  }

  if (audioRef) {
    lines.push(`<qqvoice>${audioRef}</qqvoice>`);
  }

  process.stdout.write(lines.join("\n") + "\n");
})().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
