/**
 * Markdown 转微信公众号 HTML - 优化版
 * 修复：锚点链接、代码块样式、列表样式
 * 版本：v3.0
 */

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function parseInline(text) {
  if (!text) return '';
  // 粗体
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // 行内代码
  text = text.replace(/`([^`]+)`/g, '<code style="background:#f6f8fa;padding:2px 6px;border-radius:3px;font-size:14px;font-family:Consolas,monospace;color:#e83e8c;">$1</code>');
  // 链接：只保留 http/https，移除锚点链接
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, linkText, url) => {
    if (url.startsWith('http://') || url.startsWith('https://')) {
      return '<a href="' + url + '" style="color:#07c160;text-decoration:underline;">' + linkText + '</a>';
    }
    return linkText; // 锚点链接只保留文字
  });
  return text;
}

function parseTable(rows) {
  if (rows.length < 2) return '';
  const headers = rows[0].split('|').filter(h => h.trim()).map(h => h.trim());
  const bodyRows = rows.slice(2).map(row => row.split('|').filter(c => c.trim()).map(c => c.trim()));
  
  let h = '<table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.6;">';
  h += '<thead><tr style="background:#f2f2f2;">';
  headers.forEach(hdr => {
    h += '<th style="border:1px solid #ddd;padding:10px 8px;text-align:left;font-weight:600;color:#333;">' + parseInline(hdr) + '</th>';
  });
  h += '</tr></thead><tbody>';
  
  bodyRows.forEach((row, idx) => {
    const bg = idx % 2 === 0 ? '#fff' : '#f9f9f9';
    h += '<tr style="background:' + bg + '">';
    row.forEach(cell => {
      cell = cell.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      cell = cell.replace(/`(.+?)`/g, '<code style="background:#f6f8fa;padding:2px 4px;border-radius:2px;font-size:13px;font-family:Consolas,monospace;">$1</code>');
      h += '<td style="border:1px solid #ddd;padding:8px;color:#333;">' + parseInline(cell) + '</td>';
    });
    h += '</tr>';
  });
  
  return h + '</tbody></table>';
}

function markdownToWechatHtml(markdown) {
  if (!markdown) return '';
  const lines = markdown.split('\n');
  let html = '';
  let inCode = false, codeLang = '', codeBuf = [];
  let inList = false, listBuf = [];
  let paraBuf = [];
  
  const flushPara = () => {
    if (paraBuf.length > 0) {
      const t = paraBuf.join(' ').trim();
      if (t) html += '<p style="margin:12px 0;line-height:1.8;color:#333;font-size:15px;">' + parseInline(t) + '</p>';
      paraBuf = [];
    }
  };
  
  const flushList = () => {
    if (listBuf.length > 0) {
      // 列表项合到一个卡片容器中，统一样式
      html += '<section style="margin:20px 0;padding:20px;background:linear-gradient(135deg,#f8f9fa,#e9ecef);border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);">';
      listBuf.forEach((item, idx) => {
        html += '<section style="display:flex;align-items:flex-start;margin:' + (idx === 0 ? '0' : '12px') + ' 0;padding:12px 0;' + (idx < listBuf.length - 1 ? 'border-bottom:1px solid rgba(0,0,0,0.06);' : '') + '">';
        html += '<span style="width:8px;height:8px;background:#07c160;border-radius:50%;margin:8px 12px 0 0;flex-shrink:0;"></span>';
        html += '<span style="flex:1;color:#333;line-height:1.8;font-size:15px;">' + parseInline(item) + '</span>';
        html += '</section>';
      });
      html += '</section>';
      listBuf = [];
    }
    inList = false;
  };
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const t = line.trim();
    
    if (t.startsWith('> **')) continue;
    
    // 代码块 - 优化样式（支持 ``` 和 \\\ 两种格式）
    if (t.startsWith('```') || t.startsWith('\\\\\\')) {
      flushPara();
      if (!inCode) {
        inCode = true;
        codeLang = t.replace(/[`\\]/g, '').trim();
        codeBuf = [];
      } else {
        inCode = false;
        const code = codeBuf.map(l => escapeHtml(l)).join('\n');
        html += '<section style="margin:20px 0;border:1px solid #e1e4e8;border-radius:6px;overflow:hidden;">';
        if (codeLang) {
          html += '<div style="background:#f6f8fa;padding:10px 15px;font-size:13px;color:#666;font-family:Consolas,monospace;border-bottom:1px solid #e1e4e8;">' + escapeHtml(codeLang) + '</div>';
        }
        html += '<pre style="margin:0;padding:16px;overflow-x:auto;font-size:14px;line-height:1.7;font-family:Consolas,Monaco,monospace;white-space:pre;background:#f8f9fa;"><code style="color:#24292e;display:block;min-width:100%;white-space:pre;">' + code + '</code></pre>';
        html += '</section>';
      }
      continue;
    }
    if (inCode) { codeBuf.push(line); continue; }
    
    // 表格
    if (t.startsWith('|') && t.endsWith('|')) {
      flushPara();
      if (inList) flushList();
      const tableRows = [];
      let j = i;
      while (j < lines.length && lines[j].trim().startsWith('|') && lines[j].trim().endsWith('|')) {
        if (!lines[j].trim().match(/^\|[\s\-:|]+\|$/)) tableRows.push(lines[j]);
        j++;
      }
      if (tableRows.length > 0) {
        html += '<section style="margin:20px 0;overflow-x:auto;">' + parseTable(tableRows) + '</section>';
        i = j - 1;
      }
      continue;
    }
    
    // ASCII 图
    if (line.includes('┌') || line.includes('──') || line.includes('│')) {
      flushPara();
      if (inList) flushList();
      const asciiLines = [];
      let j = i;
      while (j < lines.length && (lines[j].includes('┌') || lines[j].includes('──') || lines[j].includes('│') || lines[j].includes('├'))) {
        asciiLines.push(lines[j]);
        j++;
      }
      html += '<section style="margin:20px 0;padding:15px;background:#f8f9fa;border-radius:6px;overflow-x:auto;"><pre style="margin:0;font-family:Consolas,monospace;font-size:12px;line-height:1.5;white-space:pre;color:#333;">' + escapeHtml(asciiLines.join('\n')) + '</pre></section>';
      i = j - 1;
      continue;
    }
    
    // 标题
    if (t.startsWith('### ')) {
      flushPara();
      if (inList) flushList();
      html += '<h3 style="font-size:17px;color:#1a1a1a;margin:18px 0 10px;font-weight:600;border-left:4px solid #07c160;padding-left:12px;">' + parseInline(t.slice(4)) + '</h3>';
      continue;
    }
    if (t.startsWith('## ')) {
      flushPara();
      if (inList) flushList();
      html += '<h2 style="font-size:18px;color:#1a1a1a;margin:20px 0 12px;font-weight:600;border-left:4px solid #07c160;padding-left:12px;">' + parseInline(t.slice(3)) + '</h2>';
      continue;
    }
    if (t.startsWith('# ')) {
      flushPara();
      if (inList) flushList();
      html += '<h1 style="font-size:20px;color:#1a1a1a;margin:20px 0 16px;font-weight:bold;text-align:center;">' + parseInline(t.slice(2)) + '</h1>';
      continue;
    }
    
    // 列表
    const lm = t.match(/^[-*]\s+(.+)$/);
    if (lm) {
      flushPara();
      const item = lm[1].trim();
      if (item.length > 1 && item !== '--' && !item.match(/^[-*_]{2,}$/)) {
        if (!inList) inList = true;
        listBuf.push(item);
      } else if (inList) {
        flushList();
      }
      continue;
    }
    
    if (inList) flushList();
    
    // 引用
    if (t.startsWith('> ')) {
      flushPara();
      html += '<section style="margin:15px 0;padding:15px;background:#f0f9ff;border-left:4px solid #0066cc;border-radius:4px;"><p style="margin:0;color:#333;line-height:1.8;">' + parseInline(t.slice(2)) + '</p></section>';
      continue;
    }
    
    // 水平线
    if (t.startsWith('---')) {
      flushPara();
      html += '<hr style="border:none;border-top:1px solid #eaecef;margin:25px 0;">';
      continue;
    }
    
    // 空行
    if (t === '') {
      flushPara();
      continue;
    }
    
    // 符号行
    if (t.match(/^[-*_]{2,}$/)) continue;
    
    paraBuf.push(line);
  }
  
  if (inList) flushList();
  flushPara();
  
  return '<section style="max-width:677px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,sans-serif;font-size:15px;line-height:1.8;color:#333;">' + html + '</section>';
}

module.exports = { markdownToWechatHtml, escapeHtml, parseInline, parseTable };
