#!/usr/bin/env node

/**
 * 速查表生成器 - 主入口
 * 
 * 使用示例：
 *   node index.js "npm 发布"
 *   node index.js "Git 速查表"
 */

const renderer = require('./renderer');

// 获取命令行参数
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  // 显示帮助
  showHelp();
} else if (args.includes('--list') || args.includes('-l')) {
  // 列出所有模板
  listAllTemplates();
} else if (args.includes('--search') || args.includes('-s')) {
  // 搜索模板
  const keyword = args.find(a => !a.startsWith('-')) || '';
  searchTemplates(keyword);
} else {
  // 生成速查表
  const topic = args.join(' ');
  generateCheatSheet(topic);
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
📋 速查表生成器 - 使用帮助

【基本用法】
  node index.js <主题>           # 生成速查表
  node index.js npm 发布          # 示例：npm 发布速查表
  node index.js Git 命令          # 示例：Git 速查表

【搜索功能】
  node index.js --search <关键词>  # 搜索模板
  node index.js -s npm             # 示例：搜索 npm 相关
  node index.js -s 发布             # 示例：搜索发布相关

【列出模板】
  node index.js --list           # 列出所有可用模板
  node index.js -l               # 简写

【内置模板】
  - npm 发布（npm-publish）
  - OpenClaw 技能开发（openclaw-skill-dev）
  - Git 常用命令（git-common）

【示例】
  node index.js "生成 npm 发布速查表"
  node index.js "Git 速查"
  node index.js "OpenClaw 技能开发指南"
  node index.js --search npm
  node index.js -s 发布
`);
}

/**
 * 列出所有模板
 */
function listAllTemplates() {
  const templates = renderer.listTemplates();
  
  console.log('\n📋 可用模板列表：\n');
  templates.forEach((t, index) => {
    console.log(`${index + 1}. ${t.title}`);
    console.log(`   ID: ${t.id}`);
    console.log(`   关键词：${t.keywords.join(', ')}`);
    console.log('');
  });
}

/**
 * 搜索模板
 */
function searchTemplates(keyword) {
  if (!keyword) {
    console.log('❌ 请提供搜索关键词');
    console.log('示例：node index.js --search npm');
    return;
  }
  
  console.log(`\n🔍 搜索 "${keyword}"\n`);
  
  const results = renderer.searchTemplates(keyword);
  
  if (results.exact.length > 0) {
    console.log('🎯 精确匹配：\n');
    results.exact.forEach((r, index) => {
      console.log(`${index + 1}. ${r.template.title}`);
      console.log(`   匹配度：${r.score}%`);
      console.log(`   关键词：${r.template.keywords.join(', ')}`);
      console.log(`   使用：node index.js "${r.template.id}"`);
      console.log('');
    });
  }
  
  if (results.partial.length > 0) {
    console.log('📖 内容匹配：\n');
    results.partial.forEach((r, index) => {
      console.log(`${index + 1}. ${r.template.title}`);
      console.log(`   匹配度：${r.score}%`);
      console.log(`   匹配内容：${r.matches.join(', ')}`);
      console.log(`   使用：node index.js "${r.template.id}"`);
      console.log('');
    });
  }
  
  if (results.exact.length === 0 && results.partial.length === 0) {
    console.log('❌ 未找到匹配的模板');
    console.log('\n💡 建议：');
    console.log('   - 尝试其他关键词');
    console.log('   - 使用 --list 查看所有可用模板');
    console.log('   - 说"添加新模板，主题是 XXX"创建新模板');
  }
  
  console.log('\n---\n');
  console.log('💡 提示：找到想要的模板后，说"生成 XXX 速查表"获取完整内容');
}

/**
 * 生成速查表
 */
function generateCheatSheet(topic) {
  console.log('\n📋 正在生成速查表...\n');
  
  const markdown = renderer.renderCheatSheet(topic);
  console.log(markdown);
  
  console.log('\n\n---\n');
  console.log('💡 提示：需要保存为 Markdown 文件吗？');
  console.log('   保存：node index.js "<主题>" > ~/Documents/cheatsheets/<主题>-速查表.md');
}
