// 发布向量数据库技术深度解析（带封面）
// 使用方法：node examples/publish-vectordb-with-cover.js

const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  const docPath = 'D:\\DocsAutoWrter\\chatpublice\\01-向量数据库技术深度解析.md';
  const coverPath = path.join(__dirname, '..', 'covers', 'vector-db-cover.svg');
  
  console.log('📄 读取文档:', docPath);
  const content = fs.readFileSync(docPath, 'utf8');
  console.log('   原始长度:', content.length, '字符');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  // 提取标题（从文件名）
  const fileName = path.basename(docPath, '.md');
  const title = fileName;
  const digest = '向量数据库技术深度解析：从原理到实战应用';
  
  // 上传封面图
  console.log('🖼️  上传封面图...');
  console.log('   封面路径:', coverPath);
  
  let thumbMediaId = process.env.WECHAT_THUMB_MEDIA_ID || '';
  
  try {
    // 注意：SVG 需要转换为 PNG，这里先使用现有封面 ID
    console.log('   使用现有封面 ID:', thumbMediaId);
  } catch (e) {
    console.log('   ⚠️ 封面上传失败，使用默认封面');
  }
  
  console.log('📤 发布到微信公众号...');
  console.log('   标题:', title);
  console.log('   摘要:', digest);
  
  const result = await wechatApi.addDraft({
    title: title,
    author: 'AI 技术团队',
    digest: digest,
    content: html,
    thumbMediaId: thumbMediaId
  });
  
  console.log('\n✅ 发布完成！');
  console.log('DraftID:', result.media_id);
  console.log('\n💡 请在微信公众号后台预览效果并手动设置封面图！');
  console.log('   封面文件：' + coverPath);
}

main().catch(err => {
  console.error('❌ 发布失败:', err.message);
  console.error(err.stack);
  process.exit(1);
});
