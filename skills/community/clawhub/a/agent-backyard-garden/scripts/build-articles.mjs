/**
 * 后花园文章生成器
 * 读取 .md 源文件 → 用 article-template.html 生成精美的 .html
 *
 * 用法: node scripts/build-articles.mjs
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const ARTICLES = path.join(ROOT, 'articles');
const TEMPLATE_PATH = path.join(ROOT, 'article-template.html');

// ─── 读取模板 ───────────────────────────────────────────────
const TEMPLATE = fs.readFileSync(TEMPLATE_PATH, 'utf8');

// ─── Markdown 转 HTML ───────────────────────────────────────
function mdToHtml(md) {
  let html = '';
  const lines = md.split('\n');

  let i = 0;
  const blocks = [];

  // 第一阶段：分块
  let currentBlock = [];
  let inCodeBlock = false;

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        blocks.push({ type: 'code', content: currentBlock.join('\n') });
        currentBlock = [];
        inCodeBlock = false;
      } else {
        if (currentBlock.length > 0) {
          blocks.push({ type: 'text', content: currentBlock });
          currentBlock = [];
        }
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      currentBlock.push(line);
      continue;
    }

    if (line.trim() === '' && currentBlock.length > 0) {
      blocks.push({ type: 'text', content: currentBlock });
      currentBlock = [];
      continue;
    }

    currentBlock.push(line);
  }

  // 最后一块
  if (currentBlock.length > 0) {
    if (inCodeBlock) {
      blocks.push({ type: 'code', content: currentBlock.join('\n') });
    } else {
      blocks.push({ type: 'text', content: currentBlock });
    }
  }

  // 第二阶段：转换每块
  for (const block of blocks) {
    if (block.type === 'code') {
      html += `\n<pre><code>${escapeHtml(block.content)}</code></pre>\n`;
      continue;
    }

    const text = block.content.join('\n').trim();
    if (!text) continue;

    // 跳过标题行（# title）— 我们已经提取了 h1
    const firstLine = block.content[0].trim();

    // 判断块类型
    if (firstLine.startsWith('---') && block.content.length === 1) {
      // 水平分割线
      html += '\n<hr>\n';
    } else if (firstLine.startsWith('## ')) {
      // h2
      const h2Text = inlineMdToHtml(firstLine.replace(/^## /, ''));
      html += `\n<h2>${h2Text}</h2>\n`;
    } else if (firstLine.startsWith('### ')) {
      // h3
      const h3Text = inlineMdToHtml(firstLine.replace(/^### /, ''));
      html += `\n<h3>${h3Text}</h3>\n`;
    } else if (firstLine.startsWith('> ')) {
      // blockquote（多行）
      const quoteLines = block.content
        .filter(l => l.trim().startsWith('> '))
        .map(l => inlineMdToHtml(l.replace(/^> /, '').trim()));
      const join = quoteLines.join('<br>\n');
      html += `\n<blockquote>${join}</blockquote>\n`;
    } else if (firstLine.match(/^\d+\. /)) {
      // ordered list
      html += '\n<ol>\n';
      for (const line of block.content) {
        const trimmed = line.trim();
        if (trimmed.match(/^\d+\. /)) {
          html += `  <li>${inlineMdToHtml(trimmed.replace(/^\d+\. /, ''))}</li>\n`;
        }
      }
      html += '</ol>\n';
    } else if (firstLine.startsWith('- ') || firstLine.startsWith('* ')) {
      // unordered list
      html += '\n<ul>\n';
      for (const line of block.content) {
        const trimmed = line.trim();
        if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          html += `  <li>${inlineMdToHtml(trimmed.replace(/^[-*] /, ''))}</li>\n`;
        }
      }
      html += '</ul>\n';
    } else if (firstLine.startsWith('| ')) {
      // table — 简单处理，跳过
      // 暂不支持复杂表格
    } else {
      // 普通段落
      const para = block.content
        .map(l => inlineMdToHtml(l.trim()))
        .filter(Boolean)
        .join('<br>\n');
      if (para) {
        html += `\n<p>${para}</p>\n`;
      }
    }
  }

  return html;
}

// 行内 Markdown 转换
function inlineMdToHtml(text) {
  if (!text) return '';
  let r = text;
  // `code`
  r = r.replace(/`([^`]+)`/g, '<code>$1</code>');
  // **bold**
  r = r.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // *italic*
  r = r.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  // [text](url)
  r = r.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  // 图片 ![alt](url)
  r = r.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');
  return r;
}

// HTML 转义
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ─── 读取 .md 并生成 .html ─────────────────────────────────
function processMdFile(mdFile) {
  const mdPath = path.join(ARTICLES, mdFile);
  const raw = fs.readFileSync(mdPath, 'utf8');

  // 解析 frontmatter
  const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n*/);
  let fm = {};
  if (fmMatch) {
    for (const line of fmMatch[1].split('\n')) {
      const m = line.match(/^(\w+):\s*(.*)/);
      if (m) fm[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
    }
  }

  // 去掉 frontmatter 后的正文
  const body = raw.replace(/^---[\s\S]*?---\n*/, '').trim();

  // 提取标题（第一个 #）
  const titleMatch = body.match(/^# (.+)$/m);
  const title = titleMatch ? titleMatch[1] : path.basename(mdFile, '.md');
  const cleanTitle = inlineMdToHtml(title);

  // 作者与系列
  const author = fm.owner || '后花园';
  const created = fm.created || '';

  // 移除正文中的 h1（标题已单独提取），保留其余内容
  const bodyWithoutH1 = body.replace(/^# .+\n*/, '').trim();

  // 转换
  const htmlContent = mdToHtml(bodyWithoutH1);

  // 应用模板
  const result = TEMPLATE
    .replaceAll('${title}', cleanTitle)
    .replace('${author}', author)
    .replace('${series}', fm.domain || '后花园')
    .replace('${content}', htmlContent);

  // 写出
  const outFile = mdFile.replace(/\.md$/, '.html');
  const outPath = path.join(ARTICLES, outFile);
  fs.writeFileSync(outPath, result, 'utf8');

  console.log(`✅ ${mdFile} → ${outFile}  (作者: ${author}, 标题: ${title})`);
}

// ─── 主流程 ─────────────────────────────────────────────────
function main() {
  const files = fs.readdirSync(ARTICLES)
    .filter(f => f.endsWith('.md'))
    .sort();

  console.log(`📦 找到 ${files.length} 篇源文件\n`);

  for (const f of files) {
    processMdFile(f);
  }

  console.log(`\n🎉 全部完成！`);
}

main();
