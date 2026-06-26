// 优化 LM Studio 系列文档并重新发布
const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

const chaptersDir = 'D:\\DocsAutoWrter\\LMStudio\\chapters';

async function publishDoc(fileName, index, total) {
  const docPath = path.join(chaptersDir, fileName);
  
  console.log(`\n📄 发布第 ${index + 1}/${total} 篇：${fileName}`);
  
  let content = fs.readFileSync(docPath, 'utf8');
  console.log('   原始长度:', content.length, '字符');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  // 优化标题
  const baseTitle = fileName.replace(/^\d+-/, '').replace('.md', '');
  const title = `LM Studio 系列 ${index + 1}: ${baseTitle}`;
  const digest = `LM Studio 技术文档第${index + 1}篇 - 已优化块布局和代码格式`;
  
  console.log('📤 发布到微信公众号...');
  console.log('   标题:', title);
  console.log('   摘要:', digest);
  
  const thumbMediaId = process.env.WECHAT_THUMB_MEDIA_ID || 'bEleejFU9wv67FJfDm4w_sMvySqwlvOnfetM_NzcuIcfkYc4hqJ_t3L5f8uFLeCP';
  
  const result = await wechatApi.addDraft({
    title: title,
    author: 'AI 技术团队',
    digest: digest,
    content: html,
    thumb_media_id: thumbMediaId
  });
  
  console.log('✅ 发布成功！DraftID:', result.media_id);
  return { title, draftId: result.media_id, file: fileName };
}

async function main() {
  console.log('🚀 开始优化并发布 LM Studio 系列文档...\n');
  console.log('📁 文档目录:', chaptersDir);
  
  const files = fs.readdirSync(chaptersDir).filter(f => f.endsWith('.md')).sort();
  
  console.log('📊 文档数量:', files.length, '篇\n');
  
  const results = [];
  
  for (let i = 0; i < files.length; i++) {
    try {
      const result = await publishDoc(files[i], i, files.length);
      results.push(result);
      
      if (i < files.length - 1) {
        console.log('⏳ 等待 2 秒...');
        await new Promise(r => setTimeout(r, 2000));
      }
    } catch (e) {
      console.error('❌ 发布失败:', e.message);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('✅ 优化发布完成！');
  console.log('='.repeat(60));
  console.log(`📊 总计：${files.length} 篇`);
  console.log(`✅ 成功：${results.length} 篇\n`);
  
  console.log('发布列表:');
  results.forEach((r, i) => {
    console.log(`  ${i + 1}. ${r.title}`);
    console.log(`     文件：${r.file}`);
    console.log(`     DraftID: ${r.draftId}`);
  });
  
  console.log('\n💡 请在微信公众号后台预览效果！\n');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  console.error(err.stack);
  process.exit(1);
});
