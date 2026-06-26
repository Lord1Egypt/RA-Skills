#!/usr/bin/env node

/**
 * HTML 转 Markdown 转换脚本
 * 读取抓取的 HTML 文件，转换为结构化 Markdown
 * 
 * 用法:
 *   node convert-markdown.js <HTML_PATH>
 *   或
 *   bun run convert-markdown.js <HTML_PATH>
 */

const fs = require('fs');
const path = require('path');

/**
 * 提取代码块内容（CodeMirror 或 pre 标签）
 * 返回替换后的 HTML 和代码块数组
 */
function extractCodeBlocks(html) {
  const codeBlocks = [];
  let counter = 0;
  let result = html;
  
  // 处理 ChatGPT 代码块（带 overflow-visible 类的 pre）
  const chatGptPreRegex = /<pre[^>]*class="[^"]*overflow-visible[^"]*"[^>]*>([\s\S]*?)<\/pre>/gi;
  result = result.replace(chatGptPreRegex, (match, preContent) => {
    // 提取语言标识符（在包含图标和文本的 div 中）
    let lang = '';
    const langMatch = preContent.match(/<svg[^>]*>[\s\S]*?<\/svg>\s*(\w+)\s*<\/div>/i);
    if (langMatch) {
      lang = langMatch[1].trim();
    }
    
    // 提取 CodeMirror 内容
    const cmMatch = preContent.match(/<div[^>]*class="[^"]*cm-content[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
    if (cmMatch) {
      let code = cmMatch[1];
      // 移除 span 标签，保留内容
      code = code.replace(/<span[^>]*>/gi, '');
      code = code.replace(/<\/span>/gi, '');
      // 处理 <br> 为换行
      code = code.replace(/<br[^>]*\/?>/gi, '\n');
      // 清理 HTML 实体
      code = code.replace(/&nbsp;/g, ' ');
      code = code.replace(/&lt;/g, '<');
      code = code.replace(/&gt;/g, '>');
      code = code.replace(/&amp;/g, '&');
      code = code.trim();
      
      // 过滤掉太短或包含"复制"的内容
      if (code && code.length > 5 && !code.includes('复制')) {
        const placeholder = `__CODE_BLOCK_${counter}__`;
        codeBlocks.push({ code, lang });
        counter++;
        return `<pre>${placeholder}</pre>`;
      }
    }
    return '';
  });
  
  // 处理其他 <pre> 标签
  const preRegex = /<pre[^>]*>([\s\S]*?)<\/pre>/gi;
  result = result.replace(preRegex, (match, content) => {
    // 如果已经是占位符，跳过
    if (content.includes('__CODE_BLOCK_')) {
      return match;
    }
    
    let code = content;
    // 移除所有 HTML 标签
    code = code.replace(/<[^>]+>/g, '');
    // 清理 HTML 实体
    code = code.replace(/&nbsp;/g, ' ');
    code = code.replace(/&lt;/g, '<');
    code = code.replace(/&gt;/g, '>');
    code = code.replace(/&amp;/g, '&');
    code = code.trim();
    
    if (code && code.length > 5) {
      const placeholder = `__CODE_BLOCK_${counter}__`;
      codeBlocks.push({ code, lang: '' });
      counter++;
      return `<pre>${placeholder}</pre>`;
    }
    return '';
  });
  
  return { html: result, codeBlocks };
}

/**
 * 提取匹配的列表内容（处理嵌套）
 * @param {string} html - HTML 内容
 * @param {string} tag - 标签名称 ('ul' 或 'ol')
 * @returns {Array} - { fullMatch, content } 数组
 */
function extractTopLevelLists(html, tag) {
  const results = [];
  const openTag = `<${tag}`;
  const closeTag = `</${tag}>`;
  let i = 0;
  
  while (i < html.length) {
    // 找到下一个开始标签
    const openIdx = html.indexOf(openTag, i);
    if (openIdx === -1) break;
    
    // 找到开始标签的结束位置
    const openEnd = html.indexOf('>', openIdx);
    if (openEnd === -1) break;
    
    // 计算嵌套层级
    let depth = 1;
    let j = openEnd + 1;
    
    while (j < html.length && depth > 0) {
      const nextOpen = html.indexOf(openTag, j);
      const nextClose = html.indexOf(closeTag, j);
      
      if (nextClose === -1) break;
      
      if (nextOpen !== -1 && nextOpen < nextClose) {
        // 找到下一个开始标签
        // 检查是否是完整的开始标签（不是其他标签的一部分）
        const tagEnd = html.indexOf('>', nextOpen);
        if (tagEnd !== -1 && /^<\w+[^>]*>$/.test(html.substring(nextOpen, tagEnd + 1))) {
          depth++;
        }
        j = tagEnd + 1;
      } else {
        // 找到结束标签
        depth--;
        if (depth === 0) {
          // 找到匹配的结束标签
          const content = html.substring(openEnd + 1, nextClose);
          const fullMatch = html.substring(openIdx, nextClose + closeTag.length);
          results.push({ fullMatch, content });
          i = nextClose + closeTag.length;
          break;
        }
        j = nextClose + closeTag.length;
      }
    }
    
    if (depth > 0) {
      // 没有找到匹配的结束标签
      i = openEnd + 1;
    }
  }
  
  return results;
}

/**
 * 提取指定层级的 li 内容（处理嵌套）
 * @param {string} html - HTML 内容
 * @returns {Array} - li 内容数组
 */
function extractLItems(html) {
  const items = [];
  let depth = 0;
  let start = -1;
  
  for (let i = 0; i < html.length; i++) {
    // 检查 <li 开始
    if (html.substring(i, i + 3) === '<li') {
      const tagEnd = html.indexOf('>', i);
      if (tagEnd !== -1) {
        const tagPart = html.substring(i, tagEnd + 1);
        if (/^<li[^>]*>$/.test(tagPart)) {
          if (depth === 0) {
            start = tagEnd + 1;
          }
          depth++;
          i = tagEnd;
          continue;
        }
      }
    }
    
    // 检查 </li>
    if (html.substring(i, i + 5) === '</li>') {
      depth--;
      if (depth === 0 && start !== -1) {
        items.push(html.substring(start, i));
        start = -1;
      }
      i += 4;
    }
  }
  
  return items;
}

/**
 * 递归处理嵌套列表
 * @param {string} html - HTML 内容
 * @param {number} level - 当前嵌套层级
 * @param {string} listType - 列表类型 ('ul' 或 'ol')
 * @returns {string} - Markdown 格式的列表
 */
function processNestedList(html, level = 0, listType = 'ul') {
  const indent = '  '.repeat(level);
  const marker = listType === 'ol' ? '1.' : '-';
  
  // 提取所有直接子 li 元素
  const liItems = extractLItems(html);
  let result = '';
  
  for (const liContent of liItems) {
    // 检查是否有嵌套列表
    const nestedUlMatch = liContent.match(/<ul[^>]*>([\s\S]*?)<\/ul>/i);
    const nestedOlMatch = liContent.match(/<ol[^>]*>([\s\S]*?)<\/ol>/i);
    
    // 提取文本内容（移除嵌套列表后）
    let text = liContent;
    if (nestedUlMatch) {
      text = text.replace(nestedUlMatch[0], '');
    }
    if (nestedOlMatch) {
      text = text.replace(nestedOlMatch[0], '');
    }
    
    // 清理文本
    text = text.replace(/<p\b[^>]*>([\s\S]*?)<\/p>/gi, '$1');
    text = text.replace(/<[^>]+>/g, '');
    text = text.trim();
    
    if (text) {
      result += `${indent}${marker} ${text}\n`;
    }
    
    // 递归处理嵌套列表
    if (nestedUlMatch) {
      result += processNestedList(nestedUlMatch[1], level + 1, 'ul');
    }
    if (nestedOlMatch) {
      result += processNestedList(nestedOlMatch[1], level + 1, 'ol');
    }
  }
  
  return result;
}

/**
 * 将 HTML 转换为 Markdown 格式
 */
function htmlToMarkdown(html) {
  let content = html;
  
  // 处理标题 (h1-h6)
  content = content.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n');
  content = content.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n');
  content = content.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n');
  content = content.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n');
  content = content.replace(/<h5[^>]*>([\s\S]*?)<\/h5>/gi, '\n##### $1\n');
  content = content.replace(/<h6[^>]*>([\s\S]*?)<\/h6>/gi, '\n###### $1\n');
  
  // 处理表格（必须在其他标签处理之前）
  content = content.replace(/<table[^>]*>([\s\S]*?)<\/table>/gi, (match, tableContent) => {
    let result = '\n';
    
    // 提取表头
    const theadMatch = tableContent.match(/<thead[^>]*>([\s\S]*?)<\/thead>/i);
    let headers = [];
    if (theadMatch) {
      const thMatches = theadMatch[1].matchAll(/<th[^>]*>([\s\S]*?)<\/th>/gi);
      for (const th of thMatches) {
        headers.push(th[1].trim());
      }
    }
    
    // 提取表体
    const tbodyMatch = tableContent.match(/<tbody[^>]*>([\s\S]*?)<\/tbody>/i);
    const tbodyContent = tbodyMatch ? tbodyMatch[1] : tableContent;
    
    // 提取所有行
    const rows = [];
    const trMatches = tbodyContent.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi);
    for (const tr of trMatches) {
      const cells = [];
      const tdMatches = tr[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi);
      for (const td of tdMatches) {
        cells.push(td[1].trim());
      }
      if (cells.length > 0) {
        rows.push(cells);
      }
    }
    
    // 生成 Markdown 表格
    if (headers.length > 0) {
      result += '| ' + headers.join(' | ') + ' |\n';
      result += '| ' + headers.map(() => '---').join(' | ') + ' |\n';
    } else if (rows.length > 0) {
      result += '| ' + rows[0].join(' | ') + ' |\n';
      result += '| ' + rows[0].map(() => '---').join(' | ') + ' |\n';
      rows.shift();
    }
    
    for (const row of rows) {
      result += '| ' + row.join(' | ') + ' |\n';
    }
    
    return result + '\n';
  });
  
  // 处理加粗
  content = content.replace(/<(strong|b)[^>]*>([\s\S]*?)<\/\1>/gi, '**$2**');
  
  // 处理斜体
  content = content.replace(/<(em|i)[^>]*>([\s\S]*?)<\/\1>/gi, '*$2*');
  
  // 处理行内代码
  content = content.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`');
  
  // 处理链接
  content = content.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)');
  
  // 处理嵌套列表（使用自定义函数处理嵌套结构）
  // 先处理 <ul> 列表
  let lists = extractTopLevelLists(content, 'ul');
  for (const { fullMatch, content: listContent } of lists) {
    content = content.replace(fullMatch, '\n' + processNestedList(listContent, 0, 'ul'));
  }
  
  // 再处理 <ol> 列表
  lists = extractTopLevelLists(content, 'ol');
  for (const { fullMatch, content: listContent } of lists) {
    content = content.replace(fullMatch, '\n' + processNestedList(listContent, 0, 'ol'));
  }
  
  // 处理段落（确保只匹配 <p> 标签，不匹配 <pre> 等）
  content = content.replace(/<p\b[^>]*>([\s\S]*?)<\/p>/gi, '\n$1\n');
  
  // 处理换行
  content = content.replace(/<br\s*\/?>/gi, '\n');
  
  // 处理水平线
  content = content.replace(/<hr[^>]*>/gi, '\n---\n');
  
  return content;
}

/**
 * 清理 HTML 标签，提取纯文本
 */
function cleanHtml(html) {
  let content = html;

  // 提取 main 区域
  const mainMatch = content.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  if (mainMatch) {
    content = mainMatch[1];
  }

  // 先提取代码块
  const { html: htmlWithPlaceholders, codeBlocks } = extractCodeBlocks(content);
  content = htmlWithPlaceholders;

  // 移除脚本、样式、SVG
  content = content
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<svg[^>]*>[\s\S]*?<\/svg>/gi, '')
    .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[^>]*>[\s\S]*?<\/header>/gi, '');

  // 转换 HTML 格式为 Markdown
  content = htmlToMarkdown(content);

  // 移除所有剩余的 HTML 标签（但保留 <pre> 标签内的占位符）
  content = content.replace(/<pre>(__CODE_BLOCK_\d+__)<\/pre>/gi, (match, placeholder) => {
    const idx = parseInt(placeholder.match(/\d+/)[0]);
    const block = codeBlocks[idx];
    if (block) {
      const lang = block.lang || '';
      return `\n\`\`\`${lang}\n${block.code}\n\`\`\`\n`;
    }
    return '';
  });
  content = content.replace(/<[^>]+>/g, '');

  // 转换 HTML 实体
  content = content
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&quot;/g, '"');

  // 清理多余空白（但保留代码块内的格式）
  content = content.replace(/\n\s*\n\s*\n/g, '\n\n').trim();

  return content;
}

/**
 * 生成 Markdown 文件
 */
function generateMarkdown(metadata, html) {
  const content = cleanHtml(html);
  const now = new Date().toISOString();
  const isClaude = metadata.source.includes('claude.ai');
  
  const markdown = `---
title: "${metadata.title}"
source: "${metadata.source}"
source_type: "${isClaude ? 'claude' : 'chatgpt'}"
date: ${now}
captured_at: ${metadata.timestamp}
---

# ${metadata.title}

${metadata.description || ''}

---

## 对话内容

${content}
`;

  return markdown;
}

/**
 * 主函数
 */
async function main() {
  const htmlPath = process.argv[2] || process.argv[3];
  
  if (!htmlPath) {
    console.error('用法: node convert-markdown.js <HTML_PATH>');
    console.error('或: bun run convert-markdown.js <HTML_PATH>');
    console.error('\n从元数据文件读取: node convert-markdown.js --metadata <METADATA_JSON>');
    process.exit(1);
  }

  // 检查是否是元数据模式
  if (htmlPath === '--metadata' || htmlPath === '-m') {
    const metaPath = process.argv[3];
    if (!metaPath) {
      console.error('错误: 需要提供元数据文件路径');
      process.exit(1);
    }
    
    const metaStr = fs.readFileSync(metaPath, 'utf8');
    const metadata = JSON.parse(metaStr);
    const html = fs.readFileSync(metadata.htmlPath, 'utf8');
    
    const markdown = generateMarkdown(metadata, html);
    const mdPath = metadata.htmlPath.replace('-captured.html', '.md');
    fs.writeFileSync(mdPath, markdown);
    
    console.log(`✅ Markdown 已保存: ${mdPath}`);
    return;
  }

  // 普通模式：直接处理 HTML 文件
  if (!fs.existsSync(htmlPath)) {
    console.error(`错误: 文件不存在: ${htmlPath}`);
    process.exit(1);
  }

  const html = fs.readFileSync(htmlPath, 'utf8');
  
  // 尝试从同目录读取元数据
  const dir = path.dirname(htmlPath);
  const metaPath = path.join(dir, '.metadata.json');
  
  let metadata;
  if (fs.existsSync(metaPath)) {
    metadata = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  } else {
    // 从 HTML 中提取基本信息
    const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
    const ogTitleMatch = html.match(/<meta property="og:title" content="([^"]+)"/);
    
    metadata = {
      title: ogTitleMatch ? ogTitleMatch[1] : (titleMatch ? titleMatch[1] : 'Untitled'),
      source: '',
      timestamp: new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5)
    };
  }

  const markdown = generateMarkdown(metadata, html);
  const mdPath = htmlPath.replace('.html', '.md').replace('-captured', '');
  
  fs.writeFileSync(mdPath, markdown);
  
  console.log(`✅ Markdown 已保存: ${mdPath}`);
  
  // 输出文件大小
  const htmlSize = (fs.statSync(htmlPath).size / 1024).toFixed(1);
  const mdSize = (fs.statSync(mdPath).size / 1024).toFixed(1);
  console.log(`📊 大小: ${mdSize}KB (Markdown) + ${htmlSize}KB (HTML)`);
}

main().catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});