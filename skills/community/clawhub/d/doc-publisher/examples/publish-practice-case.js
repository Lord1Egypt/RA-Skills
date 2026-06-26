// Publish practice case article
const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  const docPath = 'D:\\DocsAutoWrter\\chatpublice\\02-向量数据库实战案例与测试.md';
  
  console.log('Reading document:', docPath);
  const content = fs.readFileSync(docPath, 'utf8');
  console.log('Original length:', content.length, 'chars');
  
  console.log('Converting Markdown to HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('HTML length:', html.length, 'chars');
  
  const title = '02-向量数据库实战案例与代码测试';
  const digest = '完整实战代码 + 测试输出结果，所有代码均经验证可直接运行';
  
  console.log('Publishing to WeChat...');
  console.log('Title:', title);
  console.log('Digest:', digest);
  
  const result = await wechatApi.addDraft({
    title: title,
    author: 'AI 技术团队',
    digest: digest,
    content: html,
    thumb_media_id: process.env.WECHAT_THUMB_MEDIA_ID || 'bEleejFU9wv67FJfDm4w_sMvySqwlvOnfetM_NzcuIcfkYc4hqJ_t3L5f8uFLeCP'
  });
  
  console.log('\n✅ Published!');
  console.log('DraftID:', result.media_id);
  console.log('\n💡 Please preview in WeChat backend!');
}

main().catch(err => {
  console.error('Error:', err.message);
  console.error(err.stack);
  process.exit(1);
});
