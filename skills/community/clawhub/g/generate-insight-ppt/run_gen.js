const fs = require('fs');
const path = require('path');
const PptxGenJS = require('pptxgenjs');

const C = { primary: 'C00000', text: '000000', muted: '666666', white: 'FFFFFF', lightGray: 'F5F5F5', diagramBg: 'F8F8F8', effectBg: '96DCDF', gold: 'D4AF37', yellow: 'FFEEB9' };
const L = { margin: 0.5, slideW: 10, slideH: 5.625 };

async function main() {
  const SESSION_ID = 'claude_code_1775296043840';
  const OUTPUT = 'Claude_Code_技术洞察_v3.pptx';
  const baseDir = 'D:/techinsight/reports/' + SESSION_ID;
  const outline = JSON.parse(fs.readFileSync(baseDir + '/content/outline.json', 'utf-8'));
  
  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = 'Claude Code 技术洞察报告';
  
  // 封面
  const s1 = pres.addSlide();
  s1.background = { color: C.primary };
  s1.addShape('rect', { x: 0, y: 0, w: L.slideW, h: 0.12, fill: { color: C.gold } });
  s1.addText(outline.cover?.title || '技术洞察报告', { x: L.margin, y: L.slideH / 2 - 1.2, w: L.slideW - L.margin * 2, h: 1, fontSize: 48, color: C.white, bold: true, align: 'center' });
  if (outline.cover?.subtitle) s1.addText(outline.cover.subtitle, { x: L.margin, y: L.slideH / 2 - 0.1, w: L.slideW - L.margin * 2, h: 0.6, fontSize: 24, color: C.gold, align: 'center' });
  console.log('[封面] OK');
  
  // 目录
  const s2 = pres.addSlide();
  s2.background = { color: C.white };
  s2.addText('目 录', { x: L.margin, y: 0.3, w: L.slideW - L.margin * 2, h: 0.6, fontSize: 28, color: C.primary, bold: true, fontFace: 'Microsoft YaHei', align: 'left' });
  outline.pages.forEach((item, i) => {
    const y = 1.2 + i * 0.55;
    s2.addShape('rect', { x: L.margin, y: y, w: 0.4, h: 0.4, fill: { color: C.primary } });
    s2.addText(String(i + 1).padStart(2, '0'), { x: L.margin, y: y, w: 0.4, h: 0.4, fontSize: 14, color: C.white, bold: true, align: 'center', valign: 'middle' });
    s2.addText(item.title || '页面', { x: L.margin + 0.5, y: y, w: 4, h: 0.4, fontSize: 16, color: C.text, bold: true });
  });
  console.log('[目录] OK');
  
  // 各页面
  outline.pages.forEach((page) => {
    if (page.type === 'executive_summary') {
      const s = pres.addSlide();
      s.background = { color: C.white };
      s.addText('执行摘要', { x: L.margin, y: 0.3, w: L.slideW - L.margin * 2, h: 0.6, fontSize: 28, color: C.primary, bold: true, fontFace: 'Microsoft YaHei', align: 'left' });
      let y = 1.0;
      (page.stats || []).slice(0, 4).forEach((stat, i) => {
        const x = L.margin + i * 2.3;
        s.addShape('rect', { x: x, y: y, w: 2.1, h: 1.0, fill: { color: C.lightGray } });
        s.addText(stat.value || '', { x: x, y: y + 0.15, w: 2.1, h: 0.5, fontSize: 28, color: C.primary, bold: true, align: 'center' });
        s.addText(stat.label || '', { x: x, y: y + 0.65, w: 2.1, h: 0.3, fontSize: 11, color: C.muted, align: 'center' });
      });
      y = 2.3;
      s.addShape('rect', { x: L.margin, y: y, w: 1.5, h: 0.35, fill: { color: C.primary } });
      s.addText('核心发现', { x: L.margin, y: y, w: 1.5, h: 0.35, fontSize: 14, color: C.white, bold: true, align: 'center', valign: 'middle' });
      y += 0.5;
      (page.insights || []).slice(0, 5).forEach(insight => {
        const text = typeof insight === 'string' ? insight : (insight.text || '');
        s.addShape('rect', { x: L.margin, y: y, w: 0.05, h: 0.4, fill: { color: C.primary } });
        s.addText(text, { x: L.margin + 0.15, y: y, w: L.slideW - L.margin * 2 - 0.15, h: 0.4, fontSize: 13, color: C.text });
        y += 0.5;
      });
      console.log('[执行摘要] OK');
    }
    
    if (page.type === 'tech_point') {
      const s = pres.addSlide();
      s.background = { color: C.white };
      s.addText(page.title || '技术点', { x: L.margin, y: 0.3, w: L.slideW - L.margin * 2, h: 0.6, fontSize: 28, color: C.primary, bold: true, fontFace: 'Microsoft YaHei', align: 'left' });
      let y = 1.0;
      
      if (page.background) {
        s.addShape('rect', { x: L.margin, y: y, w: L.slideW - L.margin * 2, h: 0.45, fill: { color: C.yellow } });
        s.addText(page.background, { x: L.margin + 0.15, y: y + 0.08, w: L.slideW - L.margin * 2 - 0.3, h: 0.35, fontSize: 12, color: C.text });
        y += 0.55;
      }
      
      const diagX = L.margin, diagW = 3.6, diagH = 3.4;
      s.addShape('rect', { x: diagX, y: y, w: diagW, h: diagH, fill: { color: C.diagramBg }, line: { color: 'E0E0E0', width: 1 } });
      const steps = page.steps || ['Step1', 'Step2', 'Step3', 'Step4'];
      const boxW = 0.85;
      steps.forEach((step, i) => {
        const boxX = diagX + 0.15 + i * (boxW + 0.25);
        s.addShape('rect', { x: boxX, y: y + 0.5, w: boxW, h: 0.5, fill: { color: C.primary } });
        s.addText(step, { x: boxX, y: y + 0.5, w: boxW, h: 0.5, fontSize: 11, color: C.white, bold: true, align: 'center', valign: 'middle' });
      });
      s.addText(page.diagramLabel || '原理图', { x: diagX, y: y + diagH - 0.5, w: diagW, h: 0.4, fontSize: 11, color: C.muted, align: 'center' });
      
      const detailX = L.margin + diagW + 0.2, detailW = L.slideW - detailX - L.margin;
      let detailY = y;
      
      if (page.principles && page.