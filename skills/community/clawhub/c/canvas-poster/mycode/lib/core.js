/**
 * canvas-poster 核心绘制工具
 * 基于 @napi-rs/canvas 的通用图形绘制函数
 */
const { createCanvas, GlobalFonts } = require('@napi-rs/canvas');
const fs = require('fs');
const path = require('path');

// ===== 字体注册 =====
const FONT_FAMILY = 'CanvasPoster';

const FONT_PATHS = [
  path.join(__dirname, 'fonts', 'SmileySans-Oblique.ttf'),
  'C:/Windows/Fonts/msyh.ttc',
  'C:/Windows/Fonts/simhei.ttf',
  '/System/Library/Fonts/PingFang.ttc',
  '/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc',
  '/home/node/.local/share/fonts/wqy-zenhei.ttc',
];

let FONT = 'sans-serif';
for (const fp of FONT_PATHS) {
  if (fs.existsSync(fp)) {
    GlobalFonts.registerFromPath(fp, FONT_FAMILY);
    FONT = FONT_FAMILY;
    break;
  }
}

if (FONT === 'sans-serif') {
  console.warn('[canvas-poster] No CJK font found. Chinese characters may render as boxes. See README for font setup.');
}

// Emoji font (registered as fallback alongside the main font)
const EMOJI_FONT_PATHS = [
  'C:/Windows/Fonts/seguiemj.ttf',
  '/System/Library/Fonts/Apple Color Emoji.ttc',
  '/usr/share/fonts/noto-color-emoji/NotoColorEmoji.ttf',
  '/usr/share/fonts/google-noto-color-emoji-fonts/NotoColorEmoji.ttf',
  '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
  '/usr/local/share/fonts/NotoColorEmoji.ttf',
];

let emojiRegistered = false;
for (const fp of EMOJI_FONT_PATHS) {
  if (fs.existsSync(fp)) {
    GlobalFonts.registerFromPath(fp, 'EmojiFont');
    emojiRegistered = true;
    break;
  }
}

if (emojiRegistered && FONT !== 'sans-serif') {
  FONT = `${FONT_FAMILY}", "EmojiFont`;
} else if (emojiRegistered) {
  FONT = 'EmojiFont';
}

if (!emojiRegistered) {
  console.warn('[canvas-poster] No emoji font found. Emoji characters will be stripped. See README for font setup.');
}

const EMOJI_RE = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{FE00}-\u{FE0F}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]+/gu;

function sanitizeText(text) {
  if (emojiRegistered) return text;
  return text.replace(EMOJI_RE, '').replace(/^\s+/, '');
}

// ===== 颜色方案 =====
const DARK_THEME = {
  bg: '#0f172a',
  cardBg: '#1e293b',
  cardBorder: '#334155',
  headerGrad1: '#1e40af',
  headerGrad2: '#3b82f6',
  white: '#ffffff',
  text: '#e2e8f0',
  subtle: '#94a3b8',
  accent: '#3b82f6',
  green: '#22c55e',
  red: '#ef4444',
  orange: '#f59e0b',
  purple: '#a855f7',
  cyan: '#06b6d4',
  barColors: ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#a855f7', '#06b6d4', '#ec4899', '#f97316'],
};

// ===== 基础绘制函数 =====

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

function formatMoney(n) {
  if (typeof n !== 'number') return String(n);
  if (n >= 10000) return `¥${(n / 10000).toFixed(1)}万`;
  return `¥${n.toLocaleString()}`;
}

function drawPieChart(ctx, cx, cy, radius, data, opts = {}) {
  const total = data.reduce((s, d) => s + d.value, 0);
  if (total === 0) return;
  let angle = -Math.PI / 2;
  const colors = DARK_THEME.barColors;
  const innerRatio = opts.donut ? (typeof opts.donut === 'number' ? opts.donut : 0.55) : 0;
  const innerR = radius * innerRatio;

  for (let i = 0; i < data.length; i++) {
    const sliceAngle = (data[i].value / total) * Math.PI * 2;
    ctx.beginPath();
    if (innerR > 0) {
      ctx.arc(cx, cy, radius, angle, angle + sliceAngle);
      ctx.arc(cx, cy, innerR, angle + sliceAngle, angle, true);
    } else {
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, radius, angle, angle + sliceAngle);
    }
    ctx.closePath();
    ctx.fillStyle = data[i].color || colors[i % colors.length];
    ctx.fill();
    angle += sliceAngle;
  }

  if (innerR > 0 && opts.center) {
    ctx.fillStyle = opts.centerColor || DARK_THEME.white;
    ctx.font = opts.centerFont || `bold 16px "${FONT}"`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(sanitizeText(opts.center), cx, cy);
    ctx.textBaseline = 'alphabetic';
    ctx.textAlign = 'left';
  }
}

function drawBarH(ctx, x, y, w, h, pct, color, maxPct = 100) {
  const barW = (pct / maxPct) * w;
  roundRect(ctx, x, y, barW, h, 3);
  ctx.fillStyle = color;
  ctx.fill();
}

// 文本截断（超宽加省略号）
function truncateText(ctx, text, maxWidth) {
  if (ctx.measureText(text).width <= maxWidth) return text;
  let t = text;
  while (ctx.measureText(t + '…').width > maxWidth && t.length > 0) {
    t = t.slice(0, -1);
  }
  return t + '…';
}

// 分隔线
function drawDivider(ctx, P, y, W, color = '#334155') {
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(P, y);
  ctx.lineTo(W - P, y);
  ctx.stroke();
}

// 坐标轴绘制（折线图/面积图/散点图共用）
function drawAxes(ctx, opts) {
  const { x, y, w, h, xLabels, yMin, yMax, yTicks = 4 } = opts;
  const leftPad = 45;
  const bottomPad = 24;
  const plotX = x + leftPad;
  const plotY = y;
  const plotW = w - leftPad - 10;
  const plotH = h - bottomPad;

  // grid lines
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= yTicks; i++) {
    const gy = plotY + plotH - (i / yTicks) * plotH;
    ctx.beginPath();
    ctx.moveTo(plotX, gy);
    ctx.lineTo(plotX + plotW, gy);
    ctx.stroke();
  }

  // Y axis labels
  ctx.font = `11px "${FONT}"`;
  ctx.fillStyle = DARK_THEME.subtle;
  ctx.textAlign = 'right';
  for (let i = 0; i <= yTicks; i++) {
    const val = yMin + (i / yTicks) * (yMax - yMin);
    const gy = plotY + plotH - (i / yTicks) * plotH;
    ctx.fillText(formatAxisVal(val), plotX - 6, gy + 4);
  }

  // X axis labels
  ctx.textAlign = 'center';
  if (xLabels && xLabels.length > 0) {
    const step = xLabels.length > 1 ? plotW / (xLabels.length - 1) : 0;
    for (let i = 0; i < xLabels.length; i++) {
      const lx = plotX + i * step;
      ctx.fillText(String(xLabels[i]), lx, plotY + plotH + 16);
    }
  }
  ctx.textAlign = 'left';

  // axis lines
  ctx.strokeStyle = DARK_THEME.subtle;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(plotX, plotY);
  ctx.lineTo(plotX, plotY + plotH);
  ctx.lineTo(plotX + plotW, plotY + plotH);
  ctx.stroke();

  const scaleX = (dataIdx, total) => plotX + (total > 1 ? (dataIdx / (total - 1)) * plotW : plotW / 2);
  const scaleY = (val) => plotY + plotH - ((val - yMin) / (yMax - yMin || 1)) * plotH;

  return { plotX, plotY, plotW, plotH, scaleX, scaleY };
}

function formatAxisVal(n) {
  if (Math.abs(n) >= 10000) return (n / 10000).toFixed(1) + 'w';
  if (Math.abs(n) >= 1000) return (n / 1000).toFixed(1) + 'k';
  if (Number.isInteger(n)) return String(n);
  return n.toFixed(1);
}

module.exports = {
  FONT,
  DARK_THEME,
  createCanvas,
  roundRect,
  formatMoney,
  drawPieChart,
  drawBarH,
  truncateText,
  drawDivider,
  drawAxes,
  sanitizeText,
};
