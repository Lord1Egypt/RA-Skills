#!/usr/bin/env node

/**
 * Build a QQ-ready selfie reply block for 虾游记.
 *
 * Usage:
 *   node scripts/build_qqbot_selfie_reply.js "Lisbon" "港口篇" "zh"
 *   node scripts/build_qqbot_selfie_reply.js "Kyoto" "夜市篇" "en" "street snack alley"
 *   node scripts/build_qqbot_selfie_reply.js "Kyoto" "夜市篇" "zh" "旅行地标前自拍" \
 *     '{"name":"Miso","species":"duck","rarity":"rare","hat":"wizard","eye":"✦","shiny":false}'
 */

const path = require("path");
const { execFileSync } = require("child_process");

const destination = process.argv[2] || "Lisbon";
const chapter = process.argv[3] || "港口篇";
const language = process.argv[4] || "zh";
const topicAngle =
  process.argv[5] || (language === "en" ? "travel selfie at golden hour" : "旅行地标前自拍");
const companionJson = process.argv[6];

const expression = "打卡虾";
const voiceScript =
  language === "en"
    ? `Travel partner, I just took a selfie for you in ${destination}. Xia Travel Log is now on ${chapter}, and I made sure the view stayed in frame with me.`
    : `旅伴，本虾刚在${destination}给你拍了一张自拍。虾游记现在翻到${chapter}了，我特地把风景和本虾一起塞进镜头里。`;

const scriptPath = path.join(__dirname, "build_qqbot_reply.js");
const replyArgs = [chapter, expression, destination, topicAngle, voiceScript, "selfie", language];
if (companionJson) {
  replyArgs.push(companionJson);
}

const raw = execFileSync(process.execPath, [scriptPath, ...replyArgs], {
  encoding: "utf8",
  maxBuffer: 10 * 1024 * 1024
});

process.stdout.write(raw);
