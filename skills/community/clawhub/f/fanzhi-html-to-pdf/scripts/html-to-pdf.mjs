#!/usr/bin/env node
// ================================
// fanzhi-provenance: fz:skill:bef3c5f1:wsl_lobster:mpc2j3a6
// project: html-to-pdf v1.0.4
// content-hash: bef3c5f1
// license: MIT-0 (ClawHub)
// copyright: 泛智生态 / Ronie & 泛智小龙虾
// fanzhi-signature: (Phase 3)
// ================================

import puppeteer from 'puppeteer-core';
import { writeFileSync, existsSync } from 'fs';
import { join, resolve } from 'path';
import { PDFDocument } from 'pdf-lib';

// ====== 配置 ======
const CHROME_PATH = process.env.CHROME_PATH ||
  (process.platform === 'darwin'
    ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    : '/opt/chrome-linux/chrome');
const CHROME_ARGS = [
  '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
  '--font-render-hinting=none', '--enable-font-antialiasing'
];
const VIEWPORT = { width: 1400, height: 900 };
const TIMEOUTS = {
  pageLoad: 30000,
  canvasWait: 15000,
  postRender: 2000,
  postExpand: 500
};

// 安全路径白名单：仅允许写入这些目录的父级
const SAFE_PARENTS = [
  process.env.HOME,
  '/tmp',
  process.cwd()
].filter(Boolean);

function isSafePath(p) {
  return SAFE_PARENTS.some(dir => resolve(p).startsWith(dir));
}

// ====== 参数校验 ======
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('用法: node scripts/html-to-pdf.mjs <输入.html> [输出.pdf]');
  process.exit(1);
}

// 禁止控制字符 + shell 特殊字符
const inputPath = args[0].trim();
if (/[\x00-\x1f<>"|?*]/.test(inputPath)) {
  console.error('❌ 输入路径包含非法字符');
  process.exit(1);
}

const absPath = resolve(inputPath.startsWith('/') ? inputPath : join(process.cwd(), inputPath));
if (!existsSync(absPath)) {
  console.error('❌ 文件不存在:', absPath);
  process.exit(1);
}
if (!absPath.endsWith('.html') && !absPath.endsWith('.htm')) {
  console.error('❌ 仅支持 .html / .htm 文件');
  process.exit(1);
}

// 输出路径校验：只在用户主动指定时做安全拦截
// 不指定时默认输出到输入文件同目录（安全，用户已授权该目录）
let pdfPath;
if (args[1]) {
  const outRaw = args[1].trim();
  if (/[\x00-\x1f<>"|?*]/.test(outRaw)) {
    console.error('❌ 输出路径包含非法字符');
    process.exit(1);
  }
  pdfPath = resolve(outRaw);
  if (!isSafePath(pdfPath)) {
    console.error('❌ 输出路径不在安全白名单内');
    console.error('   安全路径: HOME(' + process.env.HOME + '), /tmp, 当前目录(' + process.cwd() + ')');
    console.error('   建议: 将 PDF 输出到上述路径，或使用不指定输出参数（默认输出到输入文件同目录）');
    process.exit(1);
  }
} else {
  // 默认输出：输入文件同目录，同名 .pdf
  pdfPath = absPath.replace(/\.html?$/i, '.pdf');
  console.log(`   (未指定输出，沿用输入目录: ${pdfPath})`);
}

console.log(`📄 ${absPath} → ${pdfPath}`);

// ====== 主流程 ======
let browser;
try {
  browser = await puppeteer.launch({
    executablePath: CHROME_PATH, headless: true, args: CHROME_ARGS
  });

  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  await page.goto(`file://${absPath}`, {
    waitUntil: 'networkidle0', timeout: TIMEOUTS.pageLoad
  });

  // 等 canvas 图表完成
  const hasCanvas = await page.evaluate(() =>
    document.querySelectorAll('canvas').length);
  if (hasCanvas > 0) {
    await page.waitForFunction(() =>
      Array.from(document.querySelectorAll('canvas')).every(c => c.width > 0),
      { timeout: TIMEOUTS.canvasWait });
  }
  await new Promise(r => setTimeout(r, TIMEOUTS.postRender));

  // 展开隐藏内容 + 检测背景色
  const bgColor = await page.evaluate(() => {
    const cssVar = getComputedStyle(document.documentElement)
      .getPropertyValue('--bg').trim();
    return cssVar || getComputedStyle(document.body || document.documentElement)
      .backgroundColor || '#ffffff';
  });
  console.log(`   底色: ${bgColor}`);

  await page.evaluate(() => {
    document.querySelectorAll('.tc').forEach(t => t.classList.add('act'));
    const sugGrid = document.getElementById('sugGrid');
    if (sugGrid) sugGrid.style.display = '';
    document.querySelectorAll('.fi').forEach(el => el.classList.add('sho'));
  });
  await new Promise(r => setTimeout(r, TIMEOUTS.postExpand));

  // 测量内容高度
  let contentHeight = await page.evaluate(() => Math.max(
    document.documentElement.scrollHeight, document.body.scrollHeight));
  console.log(`   展开后高度: ${contentHeight}px`);

  // 底部 filler（消除 PDF 白色画布缝隙）
  await page.evaluate(bg => {
    const filler = document.createElement('div');
    filler.style.cssText =
      `height:2px;width:${VIEWPORT.width}px;background:${bg};`;
    document.body.appendChild(filler);
  }, bgColor);

  contentHeight = await page.evaluate(() => Math.max(
    document.documentElement.scrollHeight, document.body.scrollHeight));
  console.log(`   含 filler: ${contentHeight}px`);

  // 防分页 + PDF 生成
  await page.addStyleTag({
    content: 'body, html { overflow: hidden !important; }'
  });
  await new Promise(r => setTimeout(r, 200));

  const pdf = await page.pdf({
    width: `${VIEWPORT.width}px`, height: `${contentHeight}px`,
    printBackground: true
  });

  writeFileSync(pdfPath, pdf);
  console.log(`✅ ${pdfPath} (${(pdf.length / 1024).toFixed(1)} KB)`);

  // 验证 PDF 页数
  const doc = await PDFDocument.load(pdf);
  const pageCount = doc.getPageCount();
  console.log(`   PDF 页数: ${pageCount}`);
  for (let i = 0; i < pageCount; i++) {
    const { width, height } = doc.getPage(i).getSize();
    console.log(`   页${i + 1}: ${width.toFixed(0)} x ${height.toFixed(0)} pt`);
  }
  if (pageCount > 1) {
    console.warn('⚠️ 多页 PDF（预期 1 页），可能有内容未展开或分页策略需调整');
  }

  await page.close();
} catch (e) {
  console.error('❌ 错误:', e.message);
  process.exit(1);
} finally {
  if (browser) await browser.close();
}
