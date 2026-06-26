const api = require('../src/wechat-api.js');
const md = require('../src/markdown-to-wechat.js');

async function test() {
  // 测试带 emoji 的内容
  const md1 = '# 测试\n\n## 功能\n\n| 功能 | 说明 |\n|------|------|\n| 📚 数据 | 测试数据 |\n| 🔍 搜索 | 搜索功能 |';
  const html1 = md.markdownToWechatHtml(md1);
  console.log('测试 1 - Emoji 表格:', html1.length, '字符');
  console.log('HTML:', html1.substring(0, 300));
  try {
    const r1 = await api.addDraft({ title: 'Emoji 测试', author: '测试', digest: '测试', content: html1 });
    console.log('✅ 成功，DraftID:', r1.media_id);
  } catch (e) {
    console.log('❌ 失败:', e.message);
  }
  
  // 测试带链接的内容
  const md2 = '# 目录\n\n1. [什么是测试](#test-1)\n2. [快速开始](#test-2)\n3. [核心概念](#test-3)';
  const html2 = md.markdownToWechatHtml(md2);
  console.log('\n测试 2 - 目录链接:', html2.length, '字符');
  console.log('HTML:', html2);
  try {
    const r2 = await api.addDraft({ title: '链接测试', author: '测试', digest: '测试', content: html2 });
    console.log('✅ 成功，DraftID:', r2.media_id);
  } catch (e) {
    console.log('❌ 失败:', e.message);
  }
}

test().catch(e => console.error('Error:', e));
