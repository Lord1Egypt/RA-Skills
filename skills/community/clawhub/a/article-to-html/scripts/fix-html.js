#!/usr/bin/env node
/**
 * 信息图 HTML 后处理脚本
 * 修复模型生成时常见的 CSS 问题：大边距、坐标可见、字号太小、overflow 截断
 *
 * 用法：node fix-html.js <html文件路径>
 * 或：  node fix-html.js <目录>  （批量修复目录下所有 .html）
 */

const fs = require('fs');
const path = require('path');

function fixHTML(filePath) {
  let html = fs.readFileSync(filePath, 'utf-8');
  let fixes = [];

  // 1. 强制 body 无边距
  if (html.includes('<body')) {
    // 移除 body 上的 padding/margin 样式
    html = html.replace(
      /body\s*\{([^}]*)\}/g,
      (match, content) => {
        let fixed = content
          .replace(/padding\s*:\s*[^;]+;?/g, 'padding:0;')
          .replace(/margin\s*:\s*[^;]+;?/g, 'margin:0;')
          .replace(/display\s*:\s*flex\s*;?/g, '')
          .replace(/justify-content\s*:\s*center\s*;?/g, '')
          .replace(/align-items\s*:\s*[^;]+;?/g, '')
          .replace(/min-height\s*:\s*100vh\s*;?/g, '');
        fixes.push('body: 清除 padding/margin/flex');
        return `body{${fixed}background:transparent;margin:0;padding:0;}`;
      }
    );
  }

  // 2. 强制 .coord 隐藏
  if (!html.includes('.coord') || !html.includes('display: none') && !html.includes('display:none')) {
    html = html.replace(
      '</style>',
      '.coord{display:none!important;}\n</style>'
    );
    fixes.push('.coord: 强制 display:none');
  }
  // 确保已有的 .coord 规则是 display:none
  html = html.replace(
    /\.coord\s*\{([^}]*)\}/g,
    '.coord{display:none!important;}'
  );

  // 3. container: 强制 width:1080px, 移除 max-width, 移除 overflow:hidden, 修复 margin/padding
  html = html.replace(
    /\.container\s*\{([^}]*)\}/g,
    (match, content) => {
      let fixed = content
        .replace(/overflow\s*:\s*hidden\s*;?/g, '')
        .replace(/(?<!\-)height\s*:\s*1440px\s*;?/g, 'min-height:1440px;')
        .replace(/margin\s*:\s*0\s+auto\s*;?/g, 'margin:0;')
        .replace(/margin\s*:\s*auto\s*;?/g, 'margin:0;')
        // 关键修复：max-width 替换为 width:1080px
        .replace(/max-width\s*:\s*\d+px\s*;?/g, 'width:1080px;')
        // 如果没有 width 声明，加上
        .replace(/width\s*:\s*(?!1080)\d+px\s*;?/g, 'width:1080px;');

      // 确保有 width:1080px
      if (!fixed.includes('width:1080px') && !fixed.includes('width: 1080px')) {
        fixed = 'width:1080px;' + fixed;
        fixes.push('container: 强制添加 width:1080px');
      }

      // 检查 padding 是否过大（>60px）
      const paddingMatch = fixed.match(/padding\s*:\s*(\d+)px/);
      if (paddingMatch && parseInt(paddingMatch[1]) > 60) {
        fixed = fixed.replace(/padding\s*:\s*\d+px/, 'padding:48px');
        fixes.push(`container: padding ${paddingMatch[1]}px → 48px`);
      }

      fixes.push('container: 修复 width/overflow/margin');
      return `.container{${fixed}}`;
    }
  );

  // 4. 移除 body 上的 padding 内联样式
  html = html.replace(
    /(<body[^>]*style="[^"]*)(padding\s*:\s*[^;"]+;?)/g,
    '$1padding:0;'
  );

  fs.writeFileSync(filePath, html, 'utf-8');
  console.log(`✅ ${path.basename(filePath)}: ${fixes.length} fixes`);
  fixes.forEach(f => console.log(`   - ${f}`));
}

// 入口
const target = process.argv[2];
if (!target) {
  console.log('用法: node fix-html.js <html文件或目录>');
  process.exit(1);
}

const stat = fs.statSync(target);
if (stat.isDirectory()) {
  const files = fs.readdirSync(target).filter(f => f.endsWith('.html') && f !== 'gallery.html');
  files.forEach(f => fixHTML(path.join(target, f)));
  console.log(`\n共修复 ${files.length} 个文件`);
} else {
  fixHTML(target);
}
