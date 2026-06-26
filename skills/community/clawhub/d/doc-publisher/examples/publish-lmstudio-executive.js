// 发布 LM Studio 领导决策版文章
const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  const docPath = 'D:\\DocsAutoWrter\\LMStudio\\executive-brief\\LM Studio 快速了解 - 领导决策版.md';
  
  console.log('📄 读取文档:', docPath);
  const content = fs.readFileSync(docPath, 'utf8');
  console.log('   原始长度:', content.length, '字符');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  const title = 'LM Studio 快速了解：企业本地化 AI 部署方案（领导决策版）';
  const digest = '面向企业决策者，8 分钟快速了解 LM Studio 的核心价值、成本优势、应用场景及部署建议';
  
  console.log('📤 发布到微信公众号...');
  console.log('   标题:', title);
  console.log('   摘要:', digest);
  
  const result = await wechatApi.addDraft({
    title: title,
    author: 'AI 技术团队',
    digest: digest,
    content: html,
    thumb_media_id: process.env.WECHAT_THUMB_MEDIA_ID || 'bEleejFU9wv67FJfDm4w_sMvySqwlvOnfetM_NzcuIcfkYc4hqJ_t3L5f8uFLeCP'
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
