// 微信公众号格式校验工具
// 使用方法：node examples/check-wechat-format.js "D:\你的文档.md"

const fs = require('fs');
const path = require('path');

// 引入转换函数
const docPublisher = require('../src/doc-publisher.js');

async function main() {
  const filePath = process.argv[2];
  
  if (!filePath) {
    console.log('❌ 请指定文档路径');
    console.log('');
    console.log('使用方法：');
    console.log('  node check-wechat-format.js "D:\\你的文档.md"');
    process.exit(1);
  }
  
  if (!fs.existsSync(filePath)) {
    console.log(`❌ 文件不存在：${filePath}`);
    process.exit(1);
  }
  
  console.log('📄 读取文档:', filePath);
  const content = fs.readFileSync(filePath, 'utf8');
  
  console.log('\n🔄 转换为微信公众号 HTML...');
  const html = docPublisher.markdownToWechatHtml(content);
  
  // 输出统计
  console.log('\n📊 格式统计:');
  console.log(`  原始字符数：${content.length}`);
  console.log(`  HTML 字符数：${html.length}`);
  console.log(`  放大倍数：${(html.length / content.length).toFixed(2)}x`);
  
  // 检查常见问题
  console.log('\n🔍 格式检查:');
  
  const checks = [
    { name: '代码块格式', pattern: /<div.*<pre.*<code/s, should: true, desc: '代码块应包含 div>pre>code 结构' },
    { name: '标题格式', pattern: /<h[123].*style=/s, should: true, desc: '标题应包含 style 属性' },
    { name: '段落格式', pattern: /<p.*style=/s, should: true, desc: '段落应包含 style 属性' },
    { name: '特殊字符转义', test: (html) => {
        const codeBlocks = html.match(/<code[^>]*>([\s\S]*?)<\/code>/g) || [];
        for (const block of codeBlocks) {
          if (block.includes('<h1') || block.includes('<p>') || block.includes('<div')) {
            return false;
          }
        }
        return true;
      }, should: true, desc: '代码块内的 HTML 标签应被转义' }
  ];
  
  let allPassed = true;
  for (const check of checks) {
    let passed;
    if (check.test) {
      passed = check.test(html);
    } else {
      passed = check.pattern.test(html);
    }
    
    if (check.should) {
      passed = passed;
    } else {
      passed = !passed;
    }
    
    const status = passed ? '✅' : '❌';
    console.log(`  ${status} ${check.name}: ${check.desc}`);
    if (!passed) allPassed = false;
  }
  
  // 保存 HTML 到文件
  const outputPath = filePath.replace('.md', '-wechat.html');
  fs.writeFileSync(outputPath, html, 'utf8');
  console.log(`\n💾 HTML 已保存到：${outputPath}`);
  
  // 保存预览文件（带简单样式）
  const previewPath = filePath.replace('.md', '-preview.html');
  const previewHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>微信公众号预览</title>
  <style>
    body { background: #f5f5f5; padding: 20px; }
    .container { max-width: 677px; margin: 0 auto; background: white; padding: 20px; }
    .info { background: #e3f2fd; padding: 15px; margin-bottom: 20px; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="info">
      <h3>📱 微信公众号预览</h3>
      <p>请在手机模式下查看效果（按 F12 切换设备模拟器）</p>
      <p>文档：${path.basename(filePath)}</p>
    </div>
    ${html}
  </div>
</body>
</html>`;
  fs.writeFileSync(previewPath, previewHtml, 'utf8');
  console.log(`📱 预览文件已保存到：${previewPath}`);
  
  console.log('\n' + '='.repeat(60));
  if (allPassed) {
    console.log('✅ 格式检查通过！');
  } else {
    console.log('⚠️  格式检查发现问题，请检查上方标记项');
  }
  console.log('='.repeat(60));
  
  console.log('\n💡 下一步:');
  console.log(`  1. 在浏览器打开：${previewPath}`);
  console.log('  2. 按 F12 打开开发者工具');
  console.log('  3. 切换设备模拟器（手机模式）');
  console.log('  4. 检查显示效果');
}

main();
