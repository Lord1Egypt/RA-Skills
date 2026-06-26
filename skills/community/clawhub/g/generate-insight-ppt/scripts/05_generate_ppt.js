/**
 * 05_generate_ppt.js - 生成最终 PPT
 * 
 * 配色：
 * - 标题：深红色 #C00000
 * - 正文：黑色 #000000
 * - 辅助色：灰色 #666666
 * - 页面背景：白色 #FFFFFF（所有页面统一白色背景）
 * - 内容块背景：淡灰色 #F5F5F5
 * - 原理图背景：极淡灰 #F8F8F8
 * - 效果块背景：淡蓝色 #96DCDF
 */
const fs = require('fs');
const path = require('path');
const Logger = require('../lib/logger');
const fileUtils = require('../lib/file_utils');

let PptxGenJS;
try { PptxGenJS = require('pptxgenjs'); } catch (e) { console.warn('pptxgenjs not installed'); }

const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].substring(2);
    params[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
  }
}

const SESSION_ID = params['session-id'];
const OUTPUT_FILE = params.output || 'report.pptx';
if (!SESSION_ID) { console.error('Need --session-id'); process.exit(1); }

const dirs = fileUtils.createSessionDirs(SESSION_ID);
const log = new Logger(SESSION_ID);

// 配色
const C = {
  primary: 'C00000',
  text: '000000',
  muted: '666666',
  white: 'FFFFFF',
  lightGray: 'F5F5F5',
  diagramBg: 'F8F8F8',
  effectBg: '96DCDF',
  gold: 'D4AF37',
  yellow: 'FFEEB9'
};

// 布局
const L = { margin: 0.5, slideW: 10, slideH: 5.625 };

// 字体
const F = { title: 'Microsoft YaHei', body: 'Microsoft YaHei' };

// 创建幻灯片（白色背景）
const mkSlide = (pres) => {
  const s = pres.addSlide();
  s.background = { color: C.white };
  return s;
};

// 绘制标题（居左、深红色、无背景框）
const drawTitle = (slide, title, y = 0.3) => {
  slide.addText(title, {
    x: L.margin, y: y, w: L.slideW - L.margin * 2, h: 0.6,
    fontSize: 28, color: C.primary, bold: true, fontFace: F.title, align: 'left', margin: 0
  });
  return y + 0.65;
};

// ========== 封面页 ==========
function genCover(pres, d) {
  const s = mkSlide(pres);
  s.background = { color: C.primary };
  s.addShape('rect', { x: 0, y: 0, w: L.slideW, h: 0.12, fill: { color: C.gold } });
  s.addText(d.title || '技术洞察报告', {
    x: L.margin, y: L.slideH / 2 - 1.2, w: L.slideW - L.margin * 2, h: 1,
    fontSize: 48, color: C.white, bold: true, align: 'center', fontFace: F.title
  });
  if (d.subtitle) {
    s.addText(d.subtitle, {
      x: L.margin, y: L.slideH / 2 - 0.1, w: L.slideW - L.margin * 2, h: 0.6,
      fontSize: 24, color: C.gold, align: 'center', fontFace: F.body
    });
  }
  s.addText(new Date().toLocaleDateString('zh-CN'), {
    x: L.margin, y: L.slideH - 0.5, w: L.slideW - L.margin * 2, h: 0.3,
    fontSize: 12, color: 'FFCCCC', align: 'center', fontFace: F.body
  });
  console.log('[封面] OK');
}

// ========== 目录页 ==========
function genToc(pres, d) {
  const s = mkSlide(pres);
  drawTitle(s, '目 录', 0.3);
  const items = d.pages || [];
  items.forEach((item, i) => {
    const y = 1.2 + i * 0.55;
    s.addShape('rect', { x: L.margin, y: y, w: 0.4, h: 0.4, fill: { color: C.primary } });
    s.addText(String(i + 1).padStart(2, '0'), {
      x: L.margin, y: y, w: 0.4, h: 0.4,
      fontSize: 14, color: C.white, bold: true, align: 'center', valign: 'middle'
    });
    s.addText(item.title || '页面', { x: L.margin + 0.5, y: y, w: 4, h: 0.4, fontSize: 16, color: C.text, bold: true });
  });
  console.log('[目录] OK');
}

// ========== 执行摘要页 ==========
function genExecSummary(pres, d) {
  const s = mkSlide(pres);
  let y = drawTitle(s, '执行摘要', 0.3);
  const cardW = 2.1, cardGap = 0.2;
  (d.stats || []).slice(0, 4).forEach((stat, i) => {
    const x = L.margin + i * (cardW + cardGap);
    s.addShape('rect', { x: x, y: y, w: cardW, h: 1.0, fill: { color: C.lightGray } });
    s.addText(stat.value || '', { x: x, y: y + 0.15, w: cardW, h: 0.5, fontSize: 28, color: C.primary, bold: true, align: 'center' });
    s.addText(stat.label || '', { x: x, y: y + 0.65, w: cardW, h: 0.3, fontSize: 11, color: C.muted, align: 'center' });
  });
  y += 1.2;
  s.addShape('rect', { x: L.margin, y: y, w: 1.5, h: 0.35, fill: { color: C.primary } });
  s.addText('核心发现', { x: L.margin, y: y, w: 1.5, h: 0.35, fontSize: 14, color: C.white, bold: true, align: 'center', valign: 'middle' });
  y += 0.5;
  (d.insights || []).slice(0, 5).forEach(insight => {
    const text = typeof insight === 'string' ? insight : (insight.text || '');
    s.addShape('rect', { x: L.margin, y: y, w: 0.05, h: 0.4, fill: { color: C.primary } });
    s.addText(text, { x: L.margin + 0.15, y: y, w: L.slideW - L.margin * 2 - 0.15, h: 0.4, fontSize: 13, color: C.text });
    y += 0.5;
  });
  console.log('[执行摘要] OK');
}

// ========== 技术点展开页 ==========
function genTechPoint(pres, d) {
  const s = mkSlide(pres);
  drawTitle(s, d.title || '技术点', 0.3);
  let y = 1.0;
  
  // 背景说明（淡黄色）
  if (d.background) {
    s.addShape('rect', { x: L.margin, y: y, w: L.slideW - L.margin * 2, h: 0.45, fill: { color: C.yellow } });
    s.addText(d.background, { x: L.margin + 0.15, y: y + 0.08, w: L.slideW - L.margin * 2 - 0.3, h: 0.35, fontSize: 12, color: C.text });
    y += 0.55;
  }
  
  // 左侧原理图区域（40%）
  const diagX = L.margin;
  const diagW = 3.6;
  const diagH = 3.4;
  
 