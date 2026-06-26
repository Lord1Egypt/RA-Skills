#!/usr/bin/env node
/**
 * Convert Agentic Payment Daily Report MD to styled PDF via HTML.
 * Usage: node convert-ap-report.mjs <input.md> <output.pdf>
 */
import { readFileSync, writeFileSync, renameSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { resolve } from 'path';

const [, , inputMd, outputPdf] = process.argv;
if (!inputMd || !outputPdf) {
  console.error('Usage: node convert-ap-report.mjs <input.md> <output.pdf>');
  process.exit(1);
}

const src = readFileSync(resolve(inputMd), 'utf-8');

// Parse YAML frontmatter
const lines = src.split('\n');
let bodyStart = 0;
for (let i = 0; i < lines.length; i++) {
  if (lines[i] === '---' && i > 0) { bodyStart = i + 1; break; }
}
const body = lines.slice(bodyStart).join('\n');

// Parse title from first h1
const titleMatch = body.match(/^#\s+(.+)/m);
const title = titleMatch ? titleMatch[1].replace(/[🪶]/g, '').trim() : 'Agentic Payment Daily Report';

// Parse date from title or use today
const dateMatch = body.match(/(\d{4}\.\d{2}\.\d{2})/);
const dateStr = dateMatch ? dateMatch[1] : new Date().toISOString().split('T')[0].replace(/-/g, '.');

// Split into sections
const sections = body.split(/^##\s+/m).filter(s => s.trim());
const sectionLines = sections[0].split('\n'); // title section
const dateLine = sectionLines.find(l => l.trim().match(/^\d{4}/));
const dateDisplay = dateLine ? dateLine.trim() : dateStr;

function buildSectionHTML(section) {
  const sLines = section.trim().split('\n');
  const header = sLines[0].trim();
  
  // Determine tag
  let tagClass = 'tag-green', tagLabel = 'BACKGROUND';
  if (header.includes('重点必读')) { tagClass = 'tag-red'; tagLabel = 'MUST READ'; }
  else if (header.includes('值得关注')) { tagClass = 'tag-yellow'; tagLabel = 'WATCH'; }
  
  const cleanTitle = header.replace(/[🔴🟡🟢🪶|]/g, '').replace(/\s+/g, ' ').trim().replace(/^[\d.]+\s*/, '');
  const num = header.match(/^(\d+)/)?.[1] || '';
  
  let content = '';
  let i = 1;
  let currentEnP = '';
  
  while (i < sLines.length) {
    const line = sLines[i].trim();
    if (!line) {
      if (currentEnP) { content += `<p class="en">${currentEnP}</p>`; currentEnP = ''; }
      i++; continue;
    }
    
    if (line.startsWith('- 💡') || line.match(/^-\s*💡/)) {
      const c = line.replace(/^-\s*💡\s*\*\*(?:So What[^：:]*[：:])\*\*\s*/, '').replace(/\*$/g, '').trim();
      content += `<blockquote class="so-what"><strong>So What:</strong> ${c}</blockquote>`;
    } else if (line.startsWith('- 🎯') || line.match(/^-\s*🎯/)) {
      const c = line.replace(/^-\s*🎯\s*\*\*(?:Action Item[^：:]*[：:])\*\*\s*/, '').replace(/\*$/g, '').trim();
      content += `<blockquote class="action"><strong>Action Item:</strong> ${c}</blockquote>`;
    } else if (line.startsWith('🔗')) {
      // Extract URLs from this line
      const urls = line.match(/https?:\/\/[^\s)]+/g) || [];
      const linksHTML = urls.map(u => {
        // Shorten URL for display
        let display = u;
        try { display = new URL(u).hostname + (u.length > 60 ? '...' : ''); } catch(e) {}
        return `<a href="${u}">${display}</a>`;
      }).join(' &nbsp; ');
      content += `<p class="link">Source: ${linksHTML}</p>`;
    } else if (!line.startsWith('- ') && !line.startsWith('#') && !line.startsWith('---') && !line.startsWith('&lt;')) {
      // Detect English vs Chinese paragraph
      if (/^[A-Z]/.test(line)) {
        currentEnP += (currentEnP ? ' ' : '') + line;
      } else {
        if (currentEnP) { content += `<p class="en">${currentEnP}</p>`; currentEnP = ''; }
        content += `<p class="cn">${line}</p>`;
      }
    } else if (line.startsWith('- ') && !line.startsWith('- 💡') && !line.startsWith('- 🎯')) {
      // bullet point
      content += `<p class="cn" style="margin-left:12px;">• ${line.slice(2).replace(/^\*\*|!\[.*?\]\(.*?\)/g, '').trim()}</p>`;
    }
    
    i++;
  }
  if (currentEnP) content += `<p class="en">${currentEnP}</p>`;
  
  return `<div class="section"><h2 class="${tagClass}">${num}. [${tagLabel}] ${cleanTitle}</h2>${content}</div>`;
}

const sectionsHTML = sections.slice(1).map(buildSectionHTML).join('\n<hr/>\n');

const fullHTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8">
<style>
body { font-family: "PingFang SC", "Noto Sans SC", "Microsoft YaHei", "Helvetica Neue", sans-serif; color: #1F2937; font-size: 13px; line-height: 1.75; max-width: 750px; margin: 0 auto; padding: 30px 20px; }
h1 { text-align: center; font-size: 22px; color: #111827; margin-bottom: 2px; letter-spacing: 1px; }
.subtitle { text-align: center; color: #9CA3AF; font-size: 14px; margin-bottom: 32px; }
.section { margin-bottom: 20px; }
h2 { font-size: 13.5px; padding: 8px 14px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid; }
.tag-red { background: #FEF2F2; color: #B91C1C; border-left-color: #DC2626; }
.tag-yellow { background: #FFFBEB; color: #92400E; border-left-color: #D97706; }
.tag-green { background: #F0FDF4; color: #065F46; border-left-color: #059669; }
p { margin: 5px 0; }
p.en { color: #6B7280; font-size: 12px; line-height: 1.6; margin-bottom: 2px; }
p.cn { color: #374151; font-size: 13px; line-height: 1.7; }
blockquote { padding: 8px 14px; margin: 8px 0; font-size: 12px; border-radius: 0 4px 4px 0; line-height: 1.65; }
blockquote.so-what { border-left: 3px solid #3B82F6; background: #EFF6FF; color: #1E40AF; }
blockquote.action { border-left: 3px solid #EA580C; background: #FFF7ED; color: #9A3412; }
p.link { margin-top: 8px; font-size: 10.5px; }
p.link a { color: #2563EB; text-decoration: none; }
hr { border: none; border-top: 1px solid #F3F4F6; margin: 20px 0; }
</style>
</head><body>
<h1>Agentic Payment Daily Report</h1>
<p class="subtitle">${dateDisplay}</p>
${sectionsHTML}
</body></html>`;

const tmpHtml = outputPdf.replace(/\.pdf$/, '.html');
writeFileSync(tmpHtml, fullHTML);

// Convert via md-to-pdf (uses puppeteer under the hood)
const tmpMd = outputPdf.replace(/\.pdf$/, '.tmp.md');
writeFileSync(tmpMd, `---
pdf_options:
  format: A4
  margin: 18mm
stylesheet: ""
---

<iframe src="file://${tmpHtml}" style="width:100%;height:100vh;border:none;"></iframe>`);

// Actually just use puppeteer directly through md-to-pdf's launch option
// md-to-pdf can render any HTML if we structure it right
// Simplest: use md-to-pdf to render our HTML file
try {
  execSync(`md-to-pdf "${tmpHtml}" --pdf-options '{"format":"A4","margin":"18mm","printBackground":true}' 2>&1 || true`, { stdio: 'pipe', timeout: 30000 });
  const generated = tmpHtml.replace(/\.html$/, '.pdf');
  if (existsSync(generated)) {
    renameSync(generated, resolve(outputPdf));
    console.log('OK');
  } else {
    // Fallback: try node with puppeteer directly
    console.log('Fallback: trying direct puppeteer render...');
    execSync(`node -e "
      const puppeteer = require('puppeteer');
      (async () => {
        const browser = await puppeteer.launch({headless:'new'});
        const page = await browser.newPage();
        await page.goto('file://${tmpHtml}', {waitUntil:'networkidle0'});
        await page.pdf({path:'${resolve(outputPdf)}', format:'A4', margin:{top:'18mm',bottom:'18mm',left:'18mm',right:'18mm'}, printBackground:true});
        await browser.close();
        console.log('OK');
      })();
    "`, { stdio: 'inherit', timeout: 30000 });
  }
} catch (e) {
  console.error('Failed:', e.message);
  process.exit(1);
}
