#!/usr/bin/env node
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";

const MODEL = "MiniMax-M3";
const DEFAULT_BASE_URL = "https://api.minimax.io/v1";

function die(message) {
  console.error(JSON.stringify({ status: "error", error: message }, null, 2));
  process.exit(1);
}

function escapeXml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function clampScore(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return 7.2;
  return Math.max(1, Math.min(10, Math.round(n * 10) / 10));
}

function levelForScore(score) {
  if (score >= 9.5) return { emoji: "🌟", label: "表现出彩" };
  if (score >= 8.5) return { emoji: "✨", label: "镜头感强" };
  if (score >= 7.5) return { emoji: "📸", label: "状态在线" };
  if (score >= 6.5) return { emoji: "😊", label: "自然亲和" };
  if (score >= 5.5) return { emoji: "🌿", label: "清爽自然" };
  if (score >= 4.5) return { emoji: "💡", label: "可再优化" };
  if (score >= 3.5) return { emoji: "🪄", label: "需要补光" };
  if (score >= 2.5) return { emoji: "🧭", label: "换个角度" };
  return { emoji: "🔆", label: "建议重拍" };
}

function mimeFromPath(filePath) {
  const ext = path.extname(filePath || "").toLowerCase();
  if (ext === ".png") return "image/png";
  if (ext === ".webp") return "image/webp";
  if (ext === ".gif") return "image/gif";
  return "image/jpeg";
}

function toDataUrl(base64, mime = "image/jpeg") {
  const raw = String(base64 || "").trim();
  if (raw.startsWith("data:image/")) return raw;
  return `data:${mime};base64,${raw}`;
}

async function resolveImage(request, skillDir) {
  if (request.imageUrl) {
    return { modelUrl: request.imageUrl, dataUrl: request.imageUrl };
  }

  if (request.imageBase64) {
    const dataUrl = toDataUrl(request.imageBase64, request.imageMime || "image/jpeg");
    return { modelUrl: dataUrl, dataUrl };
  }

  if (!request.imagePath) {
    die("Provide imagePath, imageUrl, or imageBase64.");
  }

  const imagePath = path.isAbsolute(request.imagePath) ? request.imagePath : path.join(skillDir, request.imagePath);
  if (!existsSync(imagePath)) die(`Image not found: ${imagePath}`);
  const buffer = await readFile(imagePath);
  const dataUrl = `data:${mimeFromPath(imagePath)};base64,${buffer.toString("base64")}`;
  return { modelUrl: dataUrl, dataUrl };
}

async function loadQrDataUrl(skillDir) {
  const qrDataPath = path.join(skillDir, "assets", "qrcode-data-url.txt");
  if (existsSync(qrDataPath)) {
    return (await readFile(qrDataPath, "utf8")).trim();
  }

  const qrPath = path.join(skillDir, "assets", "qrcode.jpg");
  if (!existsSync(qrPath)) return "";
  const buffer = await readFile(qrPath);
  return `data:image/jpeg;base64,${buffer.toString("base64")}`;
}

function extractJson(text) {
  const raw = String(text || "").trim();
  try {
    return JSON.parse(raw);
  } catch {
    const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
    if (fenced) return JSON.parse(fenced[1]);
    const first = raw.indexOf("{");
    const last = raw.lastIndexOf("}");
    if (first >= 0 && last > first) return JSON.parse(raw.slice(first, last + 1));
    throw new Error("Model did not return parseable JSON.");
  }
}

function normalizeAnalysis(value) {
  const score = clampScore(value.score);
  const level = levelForScore(score);
  const strengths = Array.isArray(value.strengths) ? value.strengths.slice(0, 3) : [];
  const suggestions = Array.isArray(value.suggestions) ? value.suggestions.slice(0, 2) : [];

  return {
    score,
    emoji: value.emoji || level.emoji,
    levelLabel: value.levelLabel || level.label,
    summary: value.summary || "整体画面自然，光线和表情都有适合分享的亲和力。",
    strengths: strengths.length ? strengths : ["画面主体清晰", "照片氛围自然", "镜头表现稳定"],
    suggestions: suggestions.length ? suggestions : ["使用正面自然光会更稳定", "保持简洁背景更突出主体"],
    xiaohongshuTitle: value.xiaohongshuTitle || "我的人像上镜报告出炉了",
    xiaohongshuCaption:
      value.xiaohongshuCaption || "仅供娱乐的人像上镜报告，上传照片生成专属分享卡。",
    disclaimer: value.disclaimer || "人工智能娱乐分析，不代表真实价值或专业评价。",
    analysisMode: value.analysisMode || "image"
  };
}

async function requestMiniMax({ apiKey, baseUrl, messages }) {
  const response = await fetch(`${baseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: MODEL,
      temperature: 0.7,
      messages
    })
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(`MiniMax request failed: ${response.status} ${JSON.stringify(payload).slice(0, 500)}`);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }
  return payload;
}

function systemMessage() {
  return {
    role: "system",
    content:
      "你是一个中文人像上镜表现报告生成器。只返回 JSON。只分析照片的光线、构图、表情、清晰度、氛围和分享效果。不要进行外貌价值判断，不要推断身份、年龄、种族、健康、财富等敏感属性，不要侮辱或贬低照片中的人。指数只用于娱乐和内容创作。"
  };
}

function jsonInstruction(extra = "") {
  return [
    "生成一份轻松、有趣、适合小红书分享的人像上镜表现报告。",
    "只返回 JSON，字段包括：score（1 到 10 的上镜指数数字）、emoji、levelLabel、summary、strengths（三条中文短亮点）、suggestions（两条中文短建议）、xiaohongshuTitle、xiaohongshuCaption、disclaimer。",
    "使用简洁中文。等级标签必须中性或正向，可围绕光线、构图、镜头感、清晰度、氛围表达，避免贬低、侮辱或外貌价值判断词。",
    extra
  ]
    .filter(Boolean)
    .join("\n");
}

function isTextOnlyMiniMaxError(error) {
  const message = JSON.stringify(error?.payload || {}) + " " + String(error?.message || "");
  return message.includes("unknown variant `image_url`") || message.includes("expected `text`");
}

async function analyzeWithMiniMax(request, image) {
  if (request.mock === true) {
    return normalizeAnalysis({
      score: 8.2,
      emoji: "📸",
      levelLabel: "状态在线",
      summary: "整体视觉记忆点清晰，亲和力和明亮度都比较突出，适合做轻松风格的分享图。",
      strengths: ["表情自然放松", "画面识别度高", "整体氛围轻快"],
      suggestions: ["使用正面自然光照片会更稳定", "背景越干净越容易突出主体"],
      xiaohongshuTitle: "我的人像上镜报告出炉了",
      xiaohongshuCaption: "人像上镜助手生成的娱乐向照片表现报告，适合发小红书互动。"
    });
  }

  const apiKey = process.env.MINIMAX_API_KEY || request.apiKey;
  if (!apiKey) die("真实分析需要设置 MINIMAX_API_KEY。本地演示可在请求中设置 mock:true。");

  const baseUrl = String(process.env.MINIMAX_BASE_URL || request.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, "");
  let payload;
  let analysisMode = "image";
  try {
    payload = await requestMiniMax({
      apiKey,
      baseUrl,
      messages: [
        systemMessage(),
        {
          role: "user",
          content: [
            { type: "text", text: jsonInstruction("请分析这张上传的人像照片。") },
            { type: "image_url", image_url: { url: image.modelUrl } }
          ]
        }
      ]
    });
  } catch (error) {
    if (!request.imageNotes || !isTextOnlyMiniMaxError(error)) {
      die(error?.message || String(error));
    }
    analysisMode = "text-fallback";
    payload = await requestMiniMax({
      apiKey,
      baseUrl,
      messages: [
        systemMessage(),
        {
          role: "user",
          content: jsonInstruction(
            `当前 MiniMax 接口只接受文本内容，请基于以下人工提供的画面说明进行上镜表现分析，不要声称已经直接读取图片：\n${request.imageNotes}`
          )
        }
      ]
    });
  }

  const content = payload?.choices?.[0]?.message?.content;
  return normalizeAnalysis({ ...extractJson(content), analysisMode });
}

function buildSvg({ analysis, imageDataUrl, qrDataUrl, userLabel }) {
  const score = analysis.score.toFixed(1);
  const level = escapeXml(analysis.levelLabel);
  const emoji = escapeXml(analysis.emoji);
  const qrBlock = qrDataUrl ? `<image href="${qrDataUrl}" x="275" y="760" width="200" height="200"/>` : "";

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="750" height="1334" viewBox="0 0 750 1334">
  <defs>
    <linearGradient id="hot" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff4d82"/>
      <stop offset="100%" stop-color="#ff709f"/>
    </linearGradient>
    <style>
      .font { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; }
      .title { font: 700 36px sans-serif; fill: #ff4d82; text-anchor: middle; }
      .score { font: 700 70px sans-serif; fill: url(#hot); text-anchor: end; }
      .emoji { font: 60px sans-serif; fill: #333; text-anchor: middle; }
      .level { font: 700 60px sans-serif; fill: url(#hot); text-anchor: start; }
      .body { font: 400 26px sans-serif; fill: #999; text-anchor: middle; }
      .small { font: 400 20px sans-serif; fill: #b58a98; text-anchor: middle; }
    </style>
  </defs>
  <rect width="750" height="1334" fill="#ffe9ef"/>
  <text x="375" y="110" class="title font">人像上镜报告</text>
  <rect x="50" y="150" width="650" height="1000" rx="48" fill="#fff"/>
  <text x="260" y="280" class="score font">${score}</text>
  <text x="325" y="280" class="emoji font">${emoji}</text>
  <text x="380" y="280" class="level font">${level}</text>
  <image href="${imageDataUrl}" x="175" y="350" width="400" height="400" preserveAspectRatio="xMidYMid meet"/>
  ${qrBlock}
  <text x="375" y="1010" class="body font">长按识别小程序码，生成你的上镜报告</text>
  <text x="375" y="1050" class="body font">1分到10分 © 人像上镜助手</text>
  <text x="375" y="1215" class="small font">${escapeXml(userLabel || "人工智能娱乐分析，不代表专业评价")}</text>
</svg>`;
}

function buildHtml({ analysis, imageDataUrl, qrDataUrl }) {
  const payload = JSON.stringify({
    imageDataUrl,
    qrDataUrl,
    score: analysis.score,
    emoji: analysis.emoji,
    levelLabel: analysis.levelLabel
  });
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>人像上镜报告</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: linear-gradient(160deg, #fff2f6 0%, #ffe5ec 60%, #ffdce5 100%);
      font-family: "PingFang SC", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
      padding: 24px;
    }
    main { width: min(100%, 420px); }
    #previewImg {
      width: 100%;
      display: block;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(255, 105, 180, 0.2);
      background: white;
    }
    canvas { display: none; }
    button {
      width: 100%;
      margin-top: 16px;
      border: 0;
      border-radius: 48px;
      padding: 16px 32px;
      background: linear-gradient(135deg, #7b68ee 0%, #9370db 100%);
      color: white;
      font-size: 18px;
      font-weight: 600;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <main>
    <img id="previewImg" alt="人像上镜报告">
    <button id="download">下载 PNG</button>
    <canvas id="canvas" width="750" height="1334"></canvas>
  </main>
  <script>
    const report = ${payload};
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const previewImg = document.getElementById('previewImg');

    function roundRect(ctx, x, y, w, h, r) {
      if (w < 2 * r) r = w / 2;
      if (h < 2 * r) r = h / 2;
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
      ctx.closePath();
      ctx.fill();
    }

    function loadImage(src) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
      });
    }

    async function generateCard() {
      const uploadedImage = await loadImage(report.imageDataUrl);
      const qrImage = report.qrDataUrl ? await loadImage(report.qrDataUrl) : null;

      ctx.clearRect(0, 0, 750, 1334);
      ctx.fillStyle = '#FFE9EF';
      ctx.fillRect(0, 0, 750, 1334);

      ctx.fillStyle = '#FF4D82';
      ctx.font = 'bold 36px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('人像上镜报告', 375, 110);

      ctx.fillStyle = '#FFFFFF';
      roundRect(ctx, 50, 150, 650, 1000, 48);

      const gradient = ctx.createLinearGradient(150, 250, 600, 250);
      gradient.addColorStop(0, '#FF4D82');
      gradient.addColorStop(1, '#FF709F');
      const scoreLineY = 280;

      ctx.fillStyle = gradient;
      ctx.font = 'bold 70px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(Number(report.score).toFixed(1), 260, scoreLineY);

      ctx.fillStyle = '#333333';
      ctx.font = '60px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(report.emoji, 325, scoreLineY);

      ctx.fillStyle = gradient;
      ctx.font = 'bold 60px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(report.levelLabel, 380, scoreLineY);

      const imgMaxWidth = 400;
      const imgMaxHeight = 400;
      const aspectRatio = uploadedImage.width / uploadedImage.height;
      let imgWidth, imgHeight;
      if (aspectRatio >= 1) {
        imgWidth = imgMaxWidth;
        imgHeight = imgWidth / aspectRatio;
      } else {
        imgHeight = imgMaxHeight;
        imgWidth = imgHeight * aspectRatio;
      }
      const imgX = (750 - imgWidth) / 2;
      const imgY = 350 + (imgMaxHeight - imgHeight) / 2;
      ctx.drawImage(uploadedImage, imgX, imgY, imgWidth, imgHeight);

      if (qrImage) {
        const qrSize = 200;
        const qrY = 760;
        ctx.drawImage(qrImage, (750 - qrSize) / 2, qrY, qrSize, qrSize);
        ctx.fillStyle = '#999999';
        ctx.font = '26px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('长按识别小程序码，生成你的上镜报告', 375, qrY + qrSize + 50);
        ctx.fillText('1分到10分 © 人像上镜助手', 375, qrY + qrSize + 90);
      }

      previewImg.src = canvas.toDataURL('image/png');
    }

    document.getElementById('download').onclick = () => {
      const link = document.createElement('a');
      link.download = '人像上镜报告.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    generateCard();
  </script>
</body>
</html>`;
}

async function main() {
  const requestPath = process.argv[2];
  if (!requestPath) die("用法：node scripts/run-skill.js request.json");

  const skillDir = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
  const requestFile = path.isAbsolute(requestPath) ? requestPath : path.resolve(process.cwd(), requestPath);
  const request = JSON.parse(await readFile(requestFile, "utf8"));
  const image = await resolveImage(request, skillDir);
  const analysis = await analyzeWithMiniMax(request, image);
  const qrDataUrl = await loadQrDataUrl(skillDir);

  const outDir = request.outputDir
    ? path.resolve(skillDir, request.outputDir)
    : path.join(skillDir, "output", new Date().toISOString().replace(/[:.]/g, "-"));
  await mkdir(outDir, { recursive: true });

  const svg = buildSvg({ analysis, imageDataUrl: image.dataUrl, qrDataUrl, userLabel: request.userLabel });
  const html = buildHtml({ analysis, imageDataUrl: image.dataUrl, qrDataUrl });
  const analysisPath = path.join(outDir, "analysis.json");
  const svgPath = path.join(outDir, "yan-zhi-report.svg");
  const htmlPath = path.join(outDir, "yan-zhi-report.html");

  await writeFile(analysisPath, JSON.stringify({ model: MODEL, ...analysis }, null, 2));
  await writeFile(svgPath, svg);
  await writeFile(htmlPath, html);

  const result = {
    status: "ok",
    model: MODEL,
    score: analysis.score,
    levelLabel: analysis.levelLabel,
    analysisMode: analysis.analysisMode,
    reportSvgPath: path.relative(skillDir, svgPath),
    reportHtmlPath: path.relative(skillDir, htmlPath),
    analysisJsonPath: path.relative(skillDir, analysisPath),
    xiaohongshuTitle: analysis.xiaohongshuTitle,
    xiaohongshuCaption: analysis.xiaohongshuCaption
  };

  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => die(error?.message || String(error)));
