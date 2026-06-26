// 通用文档发布脚本
// 使用方法：node examples/publish-any.js "D:\你的文档目录"

const path = require('path');
const fs = require('fs');
const docPublisher = require('../src/doc-publisher.js');

// ============================================
// 🔒 配置检查（保护机制）
// ============================================
function checkConfig() {
  const envPath = path.join(__dirname, '..', '.env');
  
  // 检查 1: .env 文件是否存在
  if (!fs.existsSync(envPath)) {
    console.log('\n❌ 未找到 .env 配置文件\n');
    console.log('📋 请按以下步骤配置公众号信息：\n');
    console.log('   1. 进入技能目录：cd skills/doc-publisher');
    console.log('   2. 复制配置模板：copy .env.example .env');
    console.log('   3. 编辑 .env 填入你的 APPID 和 SECRET');
    console.log('   4. 重新运行此命令\n');
    console.log('📖 详细说明请查看：skill.md 或 README.md\n');
    process.exit(1);
  }
  
  // 检查 2: 配置是否填写
  const envContent = fs.readFileSync(envPath, 'utf8');
  const missingConfigs = [];
  
  if (envContent.includes('你的公众号 APPID') || !envContent.match(/WECHAT_APPID=wx[a-f0-9]+/i)) {
    missingConfigs.push('WECHAT_APPID');
  }
  if (envContent.includes('你的公众号 SECRET') || !envContent.match(/WECHAT_SECRET=[a-f0-9]+/i)) {
    missingConfigs.push('WECHAT_SECRET');
  }
  
  if (missingConfigs.length > 0) {
    console.log('\n❌ 公众号配置未填写完整\n');
    console.log('📋 请编辑 .env 文件，填写以下配置项：');
    missingConfigs.forEach(key => console.log('   - ' + key));
    console.log('');
    console.log('📖 获取方式请查看：.env.example 中的注释\n');
    process.exit(1);
  }
  
  console.log('✅ 公众号配置检查通过\n');
}

// 运行配置检查
checkConfig();

// ============================================
// 🚀 主程序
// ============================================
async function main() {
  const targetDir = process.argv[2];
  
  if (!targetDir) {
    console.log('❌ 请指定文档目录路径');
    console.log('');
    console.log('使用方法：');
    console.log('  node publish-any.js "D:\\你的文档目录"');
    console.log('');
    console.log('示例：');
    console.log('  node publish-any.js "D:\\SGLang"');
    console.log('  node publish-any.js "D:\\Python 教程"');
    process.exit(1);
  }
  
  // 检查目录是否存在
  if (!fs.existsSync(targetDir)) {
    console.log('');
    console.log('❌ 目录不存在：' + targetDir);
    console.log('');
    console.log('📋 请检查路径是否正确\n');
    process.exit(1);
  }
  
  // 检查是否有.md 文件
  const mdFiles = getAllMdFiles(targetDir);
  if (mdFiles.length === 0) {
    console.log('');
    console.log('❌ 目录中没有找到 .md 文件：' + targetDir);
    console.log('');
    console.log('📋 请确保目录下有 Markdown 文档\n');
    process.exit(1);
  }
  
  // 从目录名提取系列名称
  const seriesName = path.basename(targetDir).replace(/_/g, ' ');
  
  const config = {
    rootDir: targetDir,
    chaptersDir: 'chapters',
    appendixDir: 'appendix',
    outputDir: targetDir + '\\published',
    seriesName: seriesName,
    
    publish: {
      author: '技术团队',
      prefix: '',
      addSeriesInfo: true,
      seriesName: seriesName
    }
  };
  
  console.log('📂 文档目录:', config.rootDir);
  console.log('📚 章节目录:', config.chaptersDir);
  console.log('📎 附录目录:', config.appendixDir);
  console.log('📄 找到文档:', mdFiles.length, '个');
  console.log('');
  
  try {
    const results = await docPublisher.publishSeries(config);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 发布完成！');
    console.log('='.repeat(60));
    console.log('📊 统计：发布', results.length, '篇文章');
    console.log('');
    console.log('📁 草稿箱：');
    results.forEach((r, i) => {
      console.log('   ' + (i+1) + '. ' + r.title);
    });
    console.log('');
    console.log('💡 提示：请在微信公众号后台预览效果！');
    console.log('='.repeat(60) + '\n');
  } catch (err) {
    console.log('\n❌ 发布失败：' + err.message);
    console.log('');
    console.log('📋 可能的原因：');
    console.log('   1. 公众号配置错误（检查 .env 中的 APPID 和 SECRET）');
    console.log('   2. 网络连接问题');
    console.log('   3. 文档格式问题\n');
    process.exit(1);
  }
}

// 辅助函数：获取所有.md 文件
function getAllMdFiles(dir) {
  const files = [];
  function walk(currentDir) {
    if (!fs.existsSync(currentDir)) return;
    const items = fs.readdirSync(currentDir);
    for (const item of items) {
      if (item.startsWith('.')) continue;
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        if (item === 'assets' || item === 'node_modules') continue;
        walk(fullPath);
      } else if (item.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  }
  walk(dir);
  return files;
}

main().catch(err => {
  console.log('\n❌ 程序异常：' + err.message);
  process.exit(1);
});
