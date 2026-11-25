/**
 * 把一段文本（这里是微信支付的 code_url）变成能用手机扫的二维码：终端里画一份，同时落一份 HTML 备用。（来自 wharf-deploy 技能）
 *
 * 终端那份用半块字符（▀）：一个字符格放上下两个模块，字符格本身是竖长方形，
 * 这样画出来的模块才接近正方形 —— 用整块字符画会被拉成长条，很多手机扫不出来。
 * 颜色写死成黑白真彩色，不跟随终端主题：深色主题下如果把模块画成亮色，
 * 扫码器看到的是一张反相的码，认不出来。
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import zlib from 'node:zlib';
import qrcode from './vendor/qrcode.mjs';
import { stringToBytes as utf8StringToBytes } from './vendor/qrcode_UTF8.mjs';

qrcode.stringToBytes = utf8StringToBytes;

const RESET = '\x1b[0m';
const WHITE_BG = '\x1b[48;2;255;255;255m';
const BLACK_FG = '\x1b[38;2;0;0;0m';


export function buildMatrix(text, { ecl = 'M' } = {}) {
  const qr = qrcode(0, ecl); // 0 = 按内容自动选版本
  qr.addData(text, 'Byte');
  qr.make();
  const n = qr.getModuleCount();
  const rows = [];
  for (let r = 0; r < n; r += 1) {
    const row = [];
    for (let c = 0; c < n; c += 1) row.push(qr.isDark(r, c));
    rows.push(row);
  }
  return rows;
}

/**
 * 半块渲染。true = 深色模块。
 * 每个字符格：前景色画上面那行，背景色画下面那行。
 */
export function renderTerminal(matrix, { quiet = 2 } = {}) {
  const n = matrix.length;
  const size = n + quiet * 2;
  const at = (r, c) => {
    const rr = r - quiet;
    const cc = c - quiet;
    if (rr < 0 || cc < 0 || rr >= n || cc >= n) return false;
    return matrix[rr][cc];
  };

  const lines = [];
  for (let r = 0; r < size; r += 2) {
    // 整行只设一次颜色：白底黑字，浅色模块就是留白
    let line = `${WHITE_BG}${BLACK_FG}`;
    for (let c = 0; c < size; c += 1) {
      const top = at(r, c);
      const bottom = r + 1 < size ? at(r + 1, c) : false;
      if (top && bottom) line += '█';
      else if (!top && !bottom) line += ' ';
      else if (top) line += '▀';
      else line += '▄';
    }
    lines.push(line + RESET);
  }
  return lines.join('\n');
}

/** 不支持 ANSI 时的退路：用 ██ / 两个空格画，宽一倍但纯文本 */
export function renderAscii(matrix, { quiet = 2 } = {}) {
  const n = matrix.length;
  const size = n + quiet * 2;
  const at = (r, c) => {
    const rr = r - quiet;
    const cc = c - quiet;
    if (rr < 0 || cc < 0 || rr >= n || cc >= n) return false;
    return matrix[rr][cc];
  };
  const lines = [];
  for (let r = 0; r < size; r += 1) {
    let line = '';
    for (let c = 0; c < size; c += 1) line += at(r, c) ? '██' : '  ';
    lines.push(line);
  }
  return lines.join('\n');
}

export function renderSvg(matrix, { quiet = 4, cell = 8 } = {}) {
  const n = matrix.length;
  const size = (n + quiet * 2) * cell;
  let rects = '';
  for (let r = 0; r < n; r += 1) {
    for (let c = 0; c < n; c += 1) {
      if (!matrix[r][c]) continue;
      const x = (c + quiet) * cell;
      const y = (r + quiet) * cell;
      rects += `<rect x="${x}" y="${y}" width="${cell}" height="${cell}"/>`;
    }
  }
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" shape-rendering="crispEdges">` +
    `<rect width="${size}" height="${size}" fill="#ffffff"/><g fill="#000000">${rects}</g></svg>`
  );
}

/**
 * PNG 版本：上传成 https 图片后，Agent 在回复里贴一行 Markdown 图片就能直接渲染出来，
 * 不用用户再去开文件。有些客户端会过滤 SVG 图片，所以单独出一份 PNG（灰度、无依赖，zlib 压缩）。
 */
export function renderPng(matrix, { quiet = 4, cell = 8 } = {}) {
  const n = matrix.length;
  const size = (n + quiet * 2) * cell;
  const raw = Buffer.alloc((size + 1) * size, 255);
  for (let y = 0; y < size; y += 1) {
    raw[y * (size + 1)] = 0; // 每行开头的过滤类型：None
    const r = Math.floor(y / cell) - quiet;
    if (r < 0 || r >= n) continue;
    for (let x = 0; x < size; x += 1) {
      const c = Math.floor(x / cell) - quiet;
      if (c >= 0 && c < n && matrix[r][c]) raw[y * (size + 1) + 1 + x] = 0;
    }
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8; // 位深
  ihdr[9] = 0; // 灰度
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    pngChunk('IHDR', ihdr),
    pngChunk('IDAT', zlib.deflateSync(raw)),
    pngChunk('IEND', Buffer.alloc(0)),
  ]);
}

const CRC_TABLE = Array.from({ length: 256 }, (_, i) => {
  let c = i;
  for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});

function pngChunk(type, data) {
  const head = Buffer.alloc(8);
  head.writeUInt32BE(data.length, 0);
  head.write(type, 4, 'ascii');
  let crc = 0xffffffff;
  for (const b of Buffer.concat([head.subarray(4), data])) crc = CRC_TABLE[(crc ^ b) & 0xff] ^ (crc >>> 8);
  const tail = Buffer.alloc(4);
  tail.writeUInt32BE((crc ^ 0xffffffff) >>> 0, 0);
  return Buffer.concat([head, data, tail]);
}

/**
 * 终端那份可能被日志、窗口宽度或者字体毁掉，AI 工具也常把命令输出折叠起来，
 * 所以另外落一个 HTML 文件，用系统默认浏览器打开 —— 那一份一定扫得出来。
 */
export function writeHtml(matrix, { title = '微信扫码支付', subtitle = '', lines = [], file } = {}) {
  const target = file || path.join(os.tmpdir(), `studio-pay-qr-${process.pid}.html`);
  const svg = renderSvg(matrix);
  const extra = lines.map((l) => `<p style="margin:6px 0 0;color:#475569;font-size:14px">${escapeHtml(l)}</p>`).join('');
  const html = `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title>
<body style="font-family:system-ui,-apple-system,'PingFang SC',sans-serif;background:#f8fafc;color:#0f172a;display:flex;min-height:100vh;margin:0;align-items:center;justify-content:center">
<div style="background:#fff;padding:32px 40px;border-radius:16px;box-shadow:0 10px 40px rgba(15,23,42,.12);text-align:center;max-width:420px">
<h1 style="font-size:20px;margin:0 0 4px">${escapeHtml(title)}</h1>
<p style="margin:0 0 20px;color:#64748b;font-size:13px">${escapeHtml(subtitle || '用微信扫描下面的二维码完成支付，付完回到 Agent 即可')}</p>
${svg}
${extra}
</div></body>`;
  fs.writeFileSync(target, html, 'utf8');
  return target;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

/** 打开文件/链接；打不开就算了，终端里那份还在 */
export function openExternal(target) {
  const cmd = process.platform === 'darwin' ? 'open'
    : process.platform === 'win32' ? 'cmd'
      : 'xdg-open';
  const args = process.platform === 'win32' ? ['/c', 'start', '', target] : [target];
  try {
    const child = spawn(cmd, args, { stdio: 'ignore', detached: true });
    child.on('error', () => {});
    child.unref();
    return true;
  } catch {
    return false;
  }
}
