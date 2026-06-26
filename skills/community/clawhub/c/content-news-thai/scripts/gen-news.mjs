/**
 * gen-news.mjs — News Image Generator with Thai Text Overlay
 * 
 * Usage:
 *   node gen-news.mjs '<json_params>'
 * 
 * Params:
 *   headline    — Main headline text (Thai/English)
 *   sub         — Sub-headline text
 *   badge       — Badge text (default: "AI NEWS")
 *   badgeColor  — Badge color (default: "#CC0000")
 *   bgImage     — Path to background image (optional)
 *   bgColor     — Fallback bg color if no bgImage (default: "#0a0a1a")
 *   source      — Source text at bottom
 *   output      — Output file path (default: auto-generated)
 *   brandName   — Brand name watermark (default: none)
 *   accentColor — Accent color (default: "#CC0000")
 * 
 * Example:
 *   node gen-news.mjs '{"headline":"AI กำลังเปลี่ยนวงการค้าปลีก","sub":"ยอดขายพุ่ง 40% ใน 6 เดือน","badge":"BREAKING NEWS","bgImage":"/tmp/bg.jpg","output":"/tmp/news.jpg"}'
 */

import { createCanvas, registerFont, loadImage } from "canvas";
import { writeFileSync, existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const FONTS_DIR = resolve(__dirname, "../assets/fonts");
const WS = process.env.OPENCLAW_WORKSPACE || resolve(__dirname, "../../..");

// Register fonts
const fonts = [
  { file: "Kanit-Bold.ttf", family: "Kanit", weight: "bold" },
  { file: "Kanit-Light.ttf", family: "KanitLight", weight: "normal" },
  { file: "Sarabun-SemiBold.ttf", family: "Sarabun", weight: "bold" },
  { file: "Prompt-Bold.ttf", family: "Prompt", weight: "bold" },
];

for (const f of fonts) {
  const p = resolve(FONTS_DIR, f.file);
  if (existsSync(p)) {
    registerFont(p, { family: f.family, weight: f.weight });
  } else {
    // Try workspace root
    const p2 = resolve(WS, f.file);
    if (existsSync(p2)) registerFont(p2, { family: f.family, weight: f.weight });
  }
}

const W = 1080, H = 1350;

// ===== Helpers =====
function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function wrapText(ctx, text, maxWidth) {
  const words = text.split("");
  const lines = [];
  let currentLine = "";

  for (const char of words) {
    const testLine = currentLine + char;
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && currentLine) {
      lines.push(currentLine);
      currentLine = char;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);
  return lines;
}

function coverImage(ctx, img, W, H) {
  const s = Math.max(W / img.width, H / img.height);
  const sw = W / s, sh = H / s;
  const sx = (img.width - sw) / 2, sy = Math.max(0, (img.height - sh) / 2 - 40);
  ctx.drawImage(img, sx, sy, sw, sh, 0, 0, W, H);
}

// ===== Main Generator =====
async function generate(params) {
  const p = {
    headline: "Headline ข่าว AI",
    sub: "",
    badge: "AI NEWS",
    badgeColor: "#CC0000",
    bgImage: null,
    bgColor: "#0a0a1a",
    source: "",
    output: null,
    brandName: "",
    accentColor: "#CC0000",
    ...params,
  };

  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext("2d");

  // === Background ===
  if (p.bgImage && existsSync(p.bgImage)) {
    const img = await loadImage(p.bgImage);
    coverImage(ctx, img, W, H);
  } else if (p.bgImage && p.bgImage.startsWith("http")) {
    try {
      const img = await loadImage(p.bgImage);
      coverImage(ctx, img, W, H);
    } catch {
      ctx.fillStyle = p.bgColor;
      ctx.fillRect(0, 0, W, H);
    }
  } else {
    // Gradient background
    const grad = ctx.createLinearGradient(0, 0, W, H);
    grad.addColorStop(0, p.bgColor);
    grad.addColorStop(0.5, "#0f0f2e");
    grad.addColorStop(1, "#1a0a2e");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Add subtle grid pattern
    ctx.strokeStyle = "rgba(255,255,255,0.03)";
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 60) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += 60) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
  }

  // === Dark overlay for text readability ===
  const grd = ctx.createLinearGradient(0, 0, 0, H);
  grd.addColorStop(0, "rgba(0,0,0,0.4)");
  grd.addColorStop(0.25, "rgba(0,0,0,0.15)");
  grd.addColorStop(0.45, "rgba(0,0,0,0.35)");
  grd.addColorStop(0.6, "rgba(0,0,0,0.7)");
  grd.addColorStop(0.8, "rgba(0,0,0,0.88)");
  grd.addColorStop(1, "rgba(0,0,0,0.95)");
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, W, H);

  // === Frame — white corners ===
  ctx.strokeStyle = "rgba(255,255,255,0.35)";
  ctx.lineWidth = 2.5;
  const cL = 65;
  const m = 35;
  [[m, m + cL, m, m, m + cL, m],
   [W - m - cL, m, W - m, m, W - m, m + cL],
   [m, H - m - cL, m, H - m, m + cL, H - m],
   [W - m - cL, H - m, W - m, H - m, W - m, H - m - cL]].forEach(([x1, y1, x2, y2, x3, y3]) => {
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.lineTo(x3, y3); ctx.stroke();
  });

  // === Badge ===
  if (p.badge) {
    ctx.fillStyle = p.badgeColor;
    const badgeW = ctx.measureText(p.badge).width || 200;
    ctx.font = "bold 24px Kanit";
    const tw = ctx.measureText(p.badge).width + 50;
    roundRect(ctx, 65, 78, tw, 48, 4);
    ctx.fill();
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 24px Kanit";
    ctx.textAlign = "left";
    ctx.fillText(p.badge, 90, 111);
  }

  // === Divider line ===
  const divY = H * 0.58;
  const lineGrad = ctx.createLinearGradient(80, divY, W - 80, divY);
  lineGrad.addColorStop(0, "rgba(255,255,255,0)");
  lineGrad.addColorStop(0.15, `rgba(255,255,255,0.25)`);
  lineGrad.addColorStop(0.85, `rgba(255,255,255,0.25)`);
  lineGrad.addColorStop(1, "rgba(255,255,255,0)");
  ctx.strokeStyle = lineGrad;
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(80, divY); ctx.lineTo(W - 80, divY); ctx.stroke();

  // === Headline — auto-wrap ===
  ctx.textAlign = "center";
  ctx.shadowColor = "rgba(0,0,0,0.9)";
  ctx.shadowBlur = 25;
  ctx.shadowOffsetY = 4;

  // Try different font sizes for headline
  let fontSize = 72;
  let headlineLines;
  const maxHeadlineWidth = W - 140;

  while (fontSize >= 42) {
    ctx.font = `bold ${fontSize}px Kanit`;
    headlineLines = wrapText(ctx, p.headline, maxHeadlineWidth);
    if (headlineLines.length <= 4) break;
    fontSize -= 4;
  }

  const lineHeight = fontSize * 1.3;
  const totalHeadlineHeight = headlineLines.length * lineHeight;
  let startY = H * 0.68;

  // If we have sub, adjust positioning
  if (p.sub) {
    startY = H * 0.62;
  }

  ctx.fillStyle = "#FFFFFF";
  ctx.font = `bold ${fontSize}px Kanit`;
  for (let i = 0; i < headlineLines.length; i++) {
    ctx.fillText(headlineLines[i], W / 2, startY + i * lineHeight);
  }

  // === Sub headline ===
  if (p.sub) {
    const subY = startY + headlineLines.length * lineHeight + 20;
    let subFontSize = Math.min(fontSize * 0.65, 46);

    ctx.font = `bold ${subFontSize}px Kanit`;
    const subLines = wrapText(ctx, p.sub, maxHeadlineWidth);
    ctx.fillStyle = "rgba(255,255,255,0.8)";

    for (let i = 0; i < subLines.length; i++) {
      ctx.fillText(subLines[i], W / 2, subY + i * (subFontSize * 1.3));
    }
  }

  // === Source ===
  if (p.source) {
    ctx.shadowBlur = 0;
    ctx.shadowOffsetY = 0;
    ctx.fillStyle = "rgba(255,255,255,0.3)";
    ctx.font = "bold 21px Sarabun";
    ctx.textAlign = "center";
    ctx.fillText(p.source, W / 2, H - 90);
  }

  // === Bottom accent bar ===
  ctx.fillStyle = p.accentColor;
  ctx.fillRect(0, H - 5, W, 5);

  // === Brand watermark ===
  if (p.brandName) {
    ctx.fillStyle = "rgba(255,255,255,0.2)";
    ctx.font = "bold 20px Kanit";
    ctx.textAlign = "right";
    ctx.fillText(p.brandName.toUpperCase(), W - 60, H - 35);
  }

  // === Save ===
  const outputPath = p.output || resolve(WS, `news_${Date.now()}.jpg`);
  writeFileSync(outputPath, canvas.toBuffer("image/jpeg", { quality: 0.93 }));
  console.log(JSON.stringify({
    status: "done",
    output: outputPath,
    size: `${W}x${H}`,
    type: "image"
  }));
}

// ===== CLI =====
const jsonStr = process.argv[2];
if (!jsonStr) {
  console.log("Usage: node gen-news.mjs '<json_params>'");
  console.log("");
  console.log("Params: headline, sub, badge, badgeColor, bgImage, bgColor, source, output, brandName, accentColor");
  console.log("");
  console.log(`Example: node gen-news.mjs '{"headline":"AI เปลี่ยนโลก","sub":"ยอดขายพุ่ง 40%","badge":"BREAKING NEWS","output":"/tmp/test.jpg"}'`);
  process.exit(1);
}

generate(JSON.parse(jsonStr)).catch(e => {
  console.error(JSON.stringify({ status: "fail", error: e.message }));
  process.exit(1);
});
