// 清空草稿箱并发布向量数据库文章（带封面）
// 使用方法：node scripts/clear-and-publish.js

const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  console.log('🗑️  第一步：清空草稿箱...\n');
  
  // 获取并删除所有草稿
  const drafts = await wechatApi.getAllDrafts();
  console.log(`📝 找到 ${drafts.length} 篇草稿\n`);
  
  let deleted = 0;
  for (const draft of drafts) {
    try {
      await wechatApi.deleteDraft(draft.media_id);
      deleted++;
    } catch (e) {
      console.log(`❌ 删除失败：${draft.title || draft.media_id}`);
    }
  }
  console.log(`✅ 已删除 ${deleted} 篇草稿\n`);
  
  // 等待一下
  await new Promise(r => setTimeout(r, 2000));
  
  console.log('🖼️  第二步：上传封面图...\n');
  
  // 创建封面图（PNG 格式）
  const coverDir = path.join(__dirname, '..', 'covers');
  if (!fs.existsSync(coverDir)) fs.mkdirSync(coverDir, { recursive: true });
  
  // 使用一个简单的 PNG 生成（这里用 base64 编码的占位图）
  // 实际应该用 canvas 或 sharp 库生成
  const coverPath = path.join(coverDir, 'vector-db-cover.png');
  
  // 创建一个简单的蓝色渐变 PNG（使用预生成的 base64）
  // 由于 Node 原生不支持图片生成，我们使用微信已有的封面
  console.log('📌 使用微信素材库中的封面图');
  const thumbMediaId = process.env.WECHAT_THUMB_MEDIA_ID || 'bEleejFU9wv67FJfDm4w_sMvySqwlvOnfetM_NzcuIcfkYc4hqJ_t3L5f8uFLeCP';
  console.log('   封面 ID:', thumbMediaId);
  
  console.log('\n📖 第三步：发布文章...\n');
  
  const docPath = 'D:\\DocsAutoWrter\\chatpublice\\01-向量数据库技术深度解析.md';
  console.log('📄 读取文档:', docPath);
  const content = fs.readFileSync(docPath, 'utf8');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  const title = '01-向量数据库技术深度解析';
  const digest = '向量数据库技术深度解析：从原理到实战应用';
  
  console.log('\n📤 发布到微信公众号...');
  console.log('   标题:', title);
  console.log('   摘要:', digest);
  console.log('   封面:', thumbMediaId);
  
  const result = await wechatApi.addDraft({
    title: title,
    author: 'AI 技术团队',
    digest: digest,
    content: html,
    thumb_media_id: thumbMediaId
  });
  
  console.log('\n✅ 发布完成！');
  console.log('DraftID:', result.media_id);
  console.log('\n💡 请在微信公众号后台预览效果！');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  console.error(err.stack);
  process.exit(1);
});
