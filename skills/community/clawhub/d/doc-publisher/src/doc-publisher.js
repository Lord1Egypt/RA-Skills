/**
 * 文档系列发布工具
 * 功能：将本地 Markdown 文档系列发布到微信公众号
 */

const fs = require('fs');
const path = require('path');
const wechatApi = require(path.join(__dirname, 'wechat-api.js'));
const imagePicker = require(path.join(__dirname, 'image-picker.js'));
const markdownToWechat = require(path.join(__dirname, 'markdown-to-wechat.js'));

/**
 * 从文件名提取标题（保留序号）
 */
function extractTitleFromFileName(filePath) {
  if (!filePath) return '无标题';
  const fileName = path.basename(filePath, '.md');
  let title = fileName.replace(/_/g, ' ');
  title = title.trim();
  return title || '无标题';
}

/**
 * 清理 Markdown 格式符号（智能过滤）
 */
function cleanMarkdownSymbols(text) {
  let cleaned = text;
  cleaned = cleaned.replace(/\*\*([^*]+)\*\*/g, '$1');
  cleaned = cleaned.replace(/\*([^*]+)\*/g, '$1');
  cleaned = cleaned.replace(/^---$/gm, '');
  cleaned = cleaned.replace(/^\*\*\*$/gm, '');
  cleaned = cleaned.replace(/\t/g, ' ');
  cleaned = cleaned.replace(/  +/g, ' ');
  cleaned = cleaned.replace(/^>\s*/gm, '');
  return cleaned.trim();
}

/**
 * Markdown 转微信公众号 HTML（使用新模块）
 */
function markdownToWechatHtml(markdown, options = {}) {
  return markdownToWechat.markdownToWechatHtml(markdown);
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return text.replace(/[&<>"']/g, m => map[m]);
}

function generateSeriesNav(seriesInfo, currentIndex, total, seriesName = 'OpenClaw 安装手册') {
  const prev = currentIndex > 0 ? seriesInfo[currentIndex - 1] : null;
  const next = currentIndex < total - 1 ? seriesInfo[currentIndex + 1] : null;
  
  return `\n<div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:16px;border-radius:8px;margin:16px 0;">\n  <p style="color:white;font-size:15px;margin:0 0 12px;font-weight:600;text-align:center;">📚 ${seriesName}</p>\n  <div style="display:flex;justify-content:space-between;align-items:center;color:white;font-size:14px;">\n    <span style="flex:1;text-align:left;">\n      ${prev ? `← ${prev.title}` : '← 第一篇'}\n    </span>\n    <span style="color:rgba(255,255,255,0.7);font-size:13px;padding:0 12px;white-space:nowrap;">\n      ${currentIndex + 1}/${total}\n    </span>\n    <span style="flex:1;text-align:right;">\n      ${next ? `${next.title} →` : '完结 →'}\n    </span>\n  </div>\n</div>\n  `.trim();
}

function generateSeriesFooter(seriesInfo, currentIndex, seriesName = 'OpenClaw 安装手册') {
  const next = currentIndex < seriesInfo.length - 1 ? seriesInfo[currentIndex + 1] : null;
  
  return `\n<div style="background:#f8f9fa;padding:16px;border-radius:8px;margin:16px 0;border-top:2px solid #667eea;">\n  <p style="font-size:15px;color:#667eea;margin:0 0 12px;font-weight:600;">📖 系列导航</p>\n  ${next ? `\n  <p style="font-size:14px;color:#333;margin:8px 0;">\n    👉 下一篇：${next.title}\n  </p>\n` : ''}\n  <p style="font-size:13px;color:#999;margin:12px 0 0;">\n    📚 ${seriesName} · 共${seriesInfo.length}篇\n  </p>\n</div>\n  `.trim();
}

function scanDirectory(rootDir, chaptersDir, appendixDir) {
  const series = [];
  
  const chaptersPath = path.join(rootDir, chaptersDir);
  if (fs.existsSync(chaptersPath)) {
    const files = fs.readdirSync(chaptersPath).filter(f => f.endsWith('.md')).sort();
    files.forEach((file, index) => {
      const filePath = path.join(chaptersPath, file);
      const content = readMarkdown(filePath);
      if (content) {
        const title = extractTitleFromFileName(filePath);
        const orderMatch = file.match(/^(\d+)-/);
        const order = orderMatch ? parseInt(orderMatch[1]) : index + 1;
        series.push({ title, filePath, fileName: file, type: 'chapter', order });
      }
    });
  }
  
  if (!fs.existsSync(chaptersPath)) {
    const files = fs.readdirSync(rootDir).filter(f => {
      if (!f.endsWith('.md')) return false;
      if (f.includes('规划') || f.includes('collect')) return false;
      return true;
    }).sort();
    
    files.forEach((file, index) => {
      const filePath = path.join(rootDir, file);
      const content = readMarkdown(filePath);
      if (content) {
        const title = extractTitleFromFileName(filePath);
        const orderMatch = file.match(/^(\d+|[A-E])-/);
        const order = orderMatch ? (isNaN(parseInt(orderMatch[1])) ? orderMatch[1].charCodeAt(0) - 'A'.charCodeAt(0) + 100 : parseInt(orderMatch[1])) : index + 1;
        series.push({ title, filePath, fileName: file, type: 'chapter', order });
      }
    });
  }
  
  const appendixPath = path.join(rootDir, appendixDir);
  if (fs.existsSync(appendixPath)) {
    const files = fs.readdirSync(appendixPath).filter(f => f.endsWith('.md')).sort();
    files.forEach((file, index) => {
      const filePath = path.join(appendixPath, file);
      const content = readMarkdown(filePath);
      if (content) {
        const title = extractTitleFromFileName(filePath);
        const orderMatch = file.match(/^([A-E])-/);
        const order = orderMatch ? orderMatch[1].charCodeAt(0) - 'A'.charCodeAt(0) + 100 : 100 + index;
        series.push({ title, filePath, fileName: file, type: 'appendix', order });
      }
    });
  }
  
  return series;
}

function readMarkdown(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const invalidChars = (content.match(/[\uFFFD]/g) || []).length;
    if (invalidChars > 10) {
      console.log(`  ⚠️ 检测到乱码，尝试 GBK 编码：${filePath}`);
      try {
        const iconv = require('iconv-lite');
        const buffer = fs.readFileSync(filePath);
        content = iconv.decode(buffer, 'gbk');
      } catch (e) {
        console.log(`  ⚠️ 无法转换 GBK，使用 UTF-8`);
      }
    }
    return content;
  } catch (e) {
    console.log(`❌ 读取失败：${filePath}`);
    return null;
  }
}

async function publishDocument(doc, seriesInfo, index, options) {
  console.log(`\n📝 发布第 ${index + 1}/${seriesInfo.length} 篇：${doc.title}`);
  
  const content = readMarkdown(doc.filePath);
  if (!content) {
    console.log('❌ 读取失败，跳过');
    return null;
  }
  
  let html = markdownToWechatHtml(content, options);
  const seriesName = options.seriesName || 'OpenClaw 安装手册';
  const navHtml = generateSeriesNav(seriesInfo, index, seriesInfo.length, seriesName);
  
  let imageUsed = null;
  if (options.randomImage && options.imageDir) {
    const images = imagePicker.scanImages(options.imageDir);
    if (images.length > 0) {
      const image = imagePicker.pickRandomImage(images);
      const imageNote = `\n\n<div style="text-align:center;margin:20px 0;padding:20px;background:#f0f7ff;border-radius:8px;">\n        <p style="color:#667eea;font-size:14px;">🖼️ 本文配图：${image.filename}</p>\n        <p style="color:#999;font-size:12px;margin:8px 0 0;">（请在公众号后台手动添加图片）</p>\n      </div>\n\n`;
      html = navHtml + imageNote + html;
      imageUsed = image.filename;
      console.log(`  🖼️  配图：${image.filename}`);
    } else {
      html = navHtml + html;
    }
  } else {
    html = navHtml + html;
  }
  
  if (options.addSeriesInfo !== false) {
    const footerHtml = generateSeriesFooter(seriesInfo, index, seriesName);
    html = html + footerHtml;
  }
  
  const publishTitle = doc.title;
  
  try {
    const result = await wechatApi.addDraft({
      title: publishTitle,
      author: options.author || '小蛋蛋',
      digest: `${seriesName}第 ${index + 1} 篇`,
      content: html
    });
    
    console.log(`✅ 发布成功！DraftID: ${result.media_id}`);
    return { ...result, imageUsed };
  } catch (e) {
    console.log(`❌ 发布失败：${e.message}`);
    return null;
  }
}

async function publishSeries(config) {
  console.log('🚀 开始发布文档系列...\n');
  console.log('📂 文档根目录:', config.rootDir);
  console.log('📚 章节目录:', config.chaptersDir);
  console.log('📎 附录目录:', config.appendixDir);
  
  console.log('\n🔍 扫描文档结构...');
  const seriesInfo = scanDirectory(config.rootDir, config.chaptersDir, config.appendixDir);
  seriesInfo.sort((a, b) => a.order - b.order);
  
  console.log(`✅ 找到 ${seriesInfo.length} 篇文档`);
  console.log('\n文档列表:');
  seriesInfo.forEach((doc, i) => {
    console.log(`  ${i + 1}. [${doc.type}] ${doc.fileName} → ${doc.title.substring(0, 40)}...`);
  });
  
  if (seriesInfo.length === 0) {
    console.log('❌ 没有找到文档，请检查目录配置');
    return [];
  }
  
  const results = [];
  for (let i = 0; i < seriesInfo.length; i++) {
    const result = await publishDocument(seriesInfo[i], seriesInfo, i, config.publish || {});
    if (result) {
      results.push({
        ...seriesInfo[i],
        draftId: result.media_id,
        publishedAt: new Date().toISOString()
      });
    }
    
    if (i < seriesInfo.length - 1) {
      await new Promise(r => setTimeout(r, 1000));
    }
  }
  
  const outputDir = config.outputDir || config.rootDir;
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  const recordFile = path.join(outputDir, 'publish-record.json');
  fs.writeFileSync(recordFile, JSON.stringify({
    publishedAt: new Date().toISOString(),
    total: results.length,
    articles: results
  }, null, 2), 'utf8');
  console.log(`\n📄 发布记录已保存到：${recordFile}`);
  
  return results;
}

module.exports = {
  publishSeries,
  publishDocument,
  scanDirectory,
  markdownToWechatHtml,
  generateSeriesNav,
  generateSeriesFooter,
  extractTitleFromFileName,
  cleanMarkdownSymbols,
  readMarkdown
};
