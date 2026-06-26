// 发布 LlamaIndex 完全指南
// 使用方法：node examples/publish-llamaindex.js

const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  const docPath = 'C:\\Users\\LIYONG\\.openclaw\\workspace\\documents-site\\AI_Infrastructure\\02-部署指南\\03-LlamaIndex-完全指南.md';
  
  console.log('📄 读取文档:', docPath);
  const content = fs.readFileSync(docPath, 'utf8');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  console.log('📤 发布到微信公众号...');
  const result = await wechatApi.addDraft({
    title: '01-向量数据库技术深度解析',
    author: 'AI 技术团队',
    digest: 'LlamaIndex 完全指南：RAG 数据索引框架深度解析',
    content: html
  });
  
  console.log('\n✅ 发布完成！');
  console.log('DraftID:', result.media_id);
  console.log('\n💡 请在微信公众号后台预览效果！');
}

main().catch(err => {
  console.error('❌ 发布失败:', err.message);
  console.error(err.stack);
  process.exit(1);
});
