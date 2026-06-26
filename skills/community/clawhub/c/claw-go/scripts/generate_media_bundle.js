#!/usr/bin/env node

/**
 * Generate one 虾游记 media bundle using configured SiliconFlow endpoints.
 *
 * Usage:
 *   node scripts/generate_media_bundle.js "港口篇" "打卡虾" "Lisbon" "coastal sunset walk" \
 *     "旅伴，我发来一张新明信片。虾游记今天翻到港口篇了。" "selfie" "zh"
 *   node scripts/generate_media_bundle.js "港口篇" "打卡虾" "Lisbon" "coastal sunset walk" \
 *     "旅伴，我发来一张新明信片。虾游记今天翻到港口篇了。" "selfie" "zh" \
 *     '{"name":"Miso","species":"duck","rarity":"rare","hat":"wizard","eye":"✦","shiny":false}'
 */

const fs = require("fs");
const path = require("path");
const emojiManifest = require(path.join(__dirname, "..", "assets", "emoji-manifest.json"));

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

function parseCompanion(raw) {
  if (!raw) {
    return null;
  }
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

loadEnvFile(envPath);

const chapter = process.argv[2] || "港口篇";
const expression = process.argv[3] || "打卡虾";
const destination = process.argv[4] || "Lisbon";
const topicAngle = process.argv[5] || "coastal sunset walk";
const voiceScript =
  process.argv[6] ||
  "旅伴，我发来一张新明信片。虾游记今天翻到港口篇了。海风有点咸，我先把这张虾拍寄给你。";
const requestType = process.argv[7] || "postcard";
const language = process.argv[8] || "zh";
const companion = parseCompanion(process.argv[9]);

// 宠物形象风格配置 (可根据参考图片调整)
const companionStyle = "detailed illustration style, painterly rendering, soft edges, vibrant colors";

const outfitByChapter = {
  "夜市篇": "camera strap, snack bag, lantern glow",
  "雪国篇": "scarf, wool cap, frosty breath",
  "港口篇": "sailor stripe, sea wind, harbor light",
  "山野篇": "windbreaker, hiking satchel, mountain air",
  "古城篇": "guide badge, old-street postcard satchel",
  "海岛篇": "floral shirt, beach tote, seaside sun",
  "节庆篇": "confetti, ribbon, festival wristband",
  "秘境篇": "trench coat, lantern, hidden alley light"
};

const poseByExpression = {
  "得意虾": "one claw raised, eyebrow lifted, smug smile",
  "震惊虾": "eyes wide, antennae up, mouth open",
  "馋嘴虾": "sparkling eyes, focused on food, eager pose",
  "社牛虾": "waving claw, leaning forward, talkative posture",
  "委屈虾": "hunched pose, watery eyes, tiny frown",
  "开摆虾": "slouched body, half-lidded eyes, tired travel mood",
  "打卡虾": "selfie pose, tilted body, postcard grin",
  "神秘虾": "side-eye, composed pose, knowing grin"
};

function selectEmojiAsset() {
  const loweredTopic = String(topicAngle || "").toLowerCase();
  for (const [keyword, filename] of Object.entries(emojiManifest.by_topic || {})) {
    if (loweredTopic.includes(keyword)) {
      return filename;
    }
  }
  return (
    emojiManifest.by_request_type?.[requestType] ||
    emojiManifest.by_expression?.[expression] ||
    emojiManifest.default
  );
}

function buildCompanionPrompt() {
  if (!companion) {
    return null;
  }
  const parts = [];
  const rarity = companion.rarity ? `${companion.rarity} ` : "";
  if (companion.species) {
    parts.push(`secondary ${rarity}${companion.species} buddy companion in frame`);
  } else {
    parts.push("secondary buddy companion in frame");
  }
  if (companion.name) {
    parts.push(`companion name vibe: ${companion.name}`);
  }
  if (companion.hat && companion.hat !== "none") {
    parts.push(`wearing a ${companion.hat}`);
  }
  if (companion.eye) {
    parts.push(`eye style inspired by ${companion.eye}`);
  }
  if (companion.shiny) {
    parts.push("slightly shiny, special sparkle treatment");
  }
  parts.push("supporting role beside the mascot, not replacing the mascot");
  parts.push(companionStyle);
  return parts.join(", ");
}

function buildBrief() {
  const emojiAsset = `assets/emojis/${selectEmojiAsset()}`;
  const companionPrompt = buildCompanionPrompt();
  return {
    media_mode: "image_gen",
    request_type: requestType,
    language,
    chapter,
    expression,
    destination,
    topic_angle: topicAngle,
    emoji_asset: emojiAsset,
    image_prompt: [
      "same mascot identity as 虾游记 icon",
      `use skills/claw-go/${emojiAsset} as facial-expression reference`,
      "bright red cartoon crayfish",
      "bold black outline",
      poseByExpression[expression] || poseByExpression["打卡虾"],
      outfitByChapter[chapter] || outfitByChapter["港口篇"],
      `travel scene in ${destination}`,
      `topic angle: ${topicAngle}`,
      requestType === "selfie"
        ? "mascot selfie composition, mascot in foreground, destination clearly visible"
        : "travel postcard composition",
      companionPrompt,
      "clean composition, sticker-ready silhouette, vibrant travel postcard style",
      "preserve the same grin, eye shape, claw proportion, and mascot silhouette as the reference emoji asset"
    ]
      .filter(Boolean)
      .join(", "),
    voice_script: voiceScript,
    voice_style: "warm-smug-travel-companion",
    companion
  };
}

async function postJson(url, token, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return { type: "json", data: await res.json() };
  }

  return { type: "binary", data: Buffer.from(await res.arrayBuffer()), contentType };
}

async function main() {
  const brief = buildBrief();

  const imageResp = await postJson(process.env.CLAWGO_IMAGE_API_BASE, process.env.CLAWGO_IMAGE_API_KEY, {
    model: process.env.CLAWGO_IMAGE_MODEL,
    prompt: brief.image_prompt
  });

  const ttsResp = await postJson(process.env.CLAWGO_TTS_API_BASE, process.env.CLAWGO_TTS_API_KEY, {
    model: process.env.CLAWGO_TTS_MODEL,
    input: brief.voice_script,
    voice: process.env.CLAWGO_TTS_VOICE,
    response_format: "mp3",
    stream: false
  });

  let audioPath = null;
  let audioBytes = 0;
  if (ttsResp.type === "binary") {
    const safeName = `${Date.now()}-${chapter}-${expression}`.replace(/[^\w\u4e00-\u9fff-]+/g, "_");
    audioPath = path.join("/tmp", `${safeName}.mp3`);
    fs.writeFileSync(audioPath, ttsResp.data);
    audioBytes = ttsResp.data.length;
  }

  const imageUrl =
    imageResp.data?.images?.[0]?.url ||
    imageResp.data?.data?.[0]?.url ||
    imageResp.data?.image_url ||
    null;

  const bundle = {
    ...brief,
    image_url: imageUrl,
    audio_path: audioPath,
    audio_bytes: audioBytes,
    provider: {
      image_model: process.env.CLAWGO_IMAGE_MODEL,
      tts_model: process.env.CLAWGO_TTS_MODEL,
      tts_voice: process.env.CLAWGO_TTS_VOICE
    }
  };

  process.stdout.write(`${JSON.stringify(bundle, null, 2)}\n`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
