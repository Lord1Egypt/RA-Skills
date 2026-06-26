/**
 * Book-PDF 构建脚本模板
 * 将 fragments/ 目录下的 HTML 片段合并成完整的单页 HTML
 *
 * 使用前：修改 FRAGMENT_ORDER 和 <title> 为你的项目
 * 用法：node build.js
 */

const fs = require('fs');
const path = require('path');

const FRAGMENTS_DIR = path.join(__dirname, 'fragments');
const OUTPUT_DIR = path.join(__dirname, 'output');
const CSS_FILE = path.join(__dirname, 'styles.css');
const VERSION_FILE = path.join(__dirname, 'version.json');
const versionData = JSON.parse(fs.readFileSync(VERSION_FILE, 'utf-8'));
const OUTPUT_FILE = path.join(OUTPUT_DIR, `${versionData.title}-v${versionData.version}.html`);

// ★ 修改这里：按你的片段文件名排序
const FRAGMENT_ORDER = [
  '00-cover.html',
  '01-toc.html',
  // 'part1-xxx.html',
  // 'part2-xxx.html',
  // ...
  // 'appendix.html',
  '99-backpage.html',
];

/**
 * 注入作者信息到HTML内容
 * 支持 Mustache 风格的占位符
 */
function injectAuthorInfo(content, name) {
  const author = versionData.author || {};

  // 通用替换函数
  const replace = (template, data) => {
    let result = template;

    // 处理条件块 {{#KEY}}...{{/KEY}}
    result = result.replace(/\{\{#(\w+)\}\}([\s\S]*?)\{\{\/\1\}\}/g, (match, key, inner) => {
      const value = data[key];
      if (!value) return '';
      // 替换内部的 {{KEY}}
      return inner.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), value);
    });

    // 处理简单占位符 {{KEY}}
    Object.keys(data).forEach(key => {
      result = result.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), data[key] || '');
    });

    return result;
  };

  // 封面替换数据
  const coverData = {
    AUTHOR_NAME: author.name || '',
    AUTHOR_TITLE: author.title || '',
    AUTHOR_EXCLUSIVE: author.exclusive || ''
  };

  // 尾页替换数据
  const backpageData = {
    BOOK_TITLE: versionData.title || '',
    BOOK_SUBTITLE: author.subtitle || '',
    AUTHOR_NAME: author.name || '',
    AUTHOR_BIO: author.bio || '',
    AUTHOR_QR_IMAGE: author.qrImage || '',
    AUTHOR_LINK_URL: author.linkUrl || '',
    AUTHOR_LINK_TEXT: author.linkText || '',
    AUTHOR_SOCIAL: author.social || '',
    VERSION: versionData.version || '1.0.0',
    YEAR: new Date().getFullYear()
  };

  // 根据文件名选择替换数据
  if (name === '00-cover.html') {
    content = replace(content, coverData);
  } else if (name === '99-backpage.html') {
    content = replace(content, backpageData);
  }

  return content;
}

function build() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const buildTime = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  console.log(`📦 Version: v${versionData.version} (build #${versionData.build})`);

  const css = fs.readFileSync(CSS_FILE, 'utf-8');

  const fragments = [];
  const missing = [];

  for (const name of FRAGMENT_ORDER) {
    const filePath = path.join(FRAGMENTS_DIR, name);
    if (fs.existsSync(filePath)) {
      let content = fs.readFileSync(filePath, 'utf-8').trim();

      // 注入版本信息到封面
      if (name === '00-cover.html') {
        content = content.replace(/文档版本：<\/strong>v[\d.]+/g,
          `文档版本：</strong>v${versionData.version}`);
        content = content.replace(/发布时间：<\/strong>[^<]+/g,
          `发布时间：</strong>${versionData.lastUpdate} (build #${versionData.build})`);
      }

      // 注入作者信息
      content = injectAuthorInfo(content, name);

      fragments.push(`<!-- ===== ${name} ===== -->\n${content}`);
      console.log(`  ✅ ${name}`);
    } else {
      missing.push(name);
      console.log(`  ⬜ ${name} (missing, skipped)`);
    }
  }

  if (missing.length > 0) {
    console.log(`\n⚠️  ${missing.length} fragments missing, building partial HTML\n`);
  }

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${versionData.title}</title>
<style>
${css}
</style>
</head>
<body>

${fragments.join('\n\n')}

</body>
</html>`;

  fs.writeFileSync(OUTPUT_FILE, html, 'utf-8');

  const sizeKB = (Buffer.byteLength(html, 'utf-8') / 1024).toFixed(1);
  console.log(`\n✅ Built: ${OUTPUT_FILE}`);
  console.log(`   Size: ${sizeKB} KB`);
  console.log(`   Fragments: ${fragments.length}/${FRAGMENT_ORDER.length}`);
}

build();
