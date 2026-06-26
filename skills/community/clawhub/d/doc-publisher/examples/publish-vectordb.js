// 发布向量数据库技术深度解析
// 使用方法：node examples/publish-vectordb.js

const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  const docPath = 'D:\\DocsAutoWrter\\chatpublice\\01-向量数据库技术深度解析.md';
  
  console.log('📄 读取文档:', docPath);
  const content = fs.readFileSync(docPath, 'utf8');
  console.log('   原始长度:', content.length, '字符');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  // 提取标题（从文件名）
  const fileName = path.basename(docPath, '.md');
  const title = fileName;
  
  // 提取摘要
  const digest = '向量数据库技术深度解析：从原理到实战应用';
  
  console.log('📤 发布到微信公众号...');
  console.log('   标题:', title);
  console.log('   摘要:', digest);
  
  const result = await wechatApi.addDraft({
    title: title,
    author: 'AI 技术团队',
    digest: digest,
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
