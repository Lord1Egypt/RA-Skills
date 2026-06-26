// 批量发布 LM Studio chapters 目录下的文档
const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

const docs = [
  {
    file: '01-LM Studio 深度解读概述.md',
    title: 'LM Studio 深度解读：企业本地化 AI 部署方案',
    digest: '一文了解 LM Studio 的核心价值、技术架构和应用场景'
  },
  {
    file: '02-LM Studio 结合 llama.cpp 和 GGUF 模型转换.md',
    title: 'LM Studio 实战：llama.cpp 与 GGUF 模型转换详解',
    digest: '手把手教你转换和优化大语言模型'
  },
  {
    file: '03-LM Studio 本地部署与 API 实战.md',
    title: 'LM Studio 本地部署与 API 调用完整指南',
    digest: '从安装到 API 对接，一站式部署教程'
  },
  {
    file: '04-LM Studio 性能优化与 API 高级用法.md',
    title: 'LM Studio 性能优化与 API 高级用法',
    digest: '响应速度提升 5 倍的优化技巧'
  },
  {
    file: '05-LM Studio 本地部署与企业应用.md',
    title: 'LM Studio 企业级应用：从部署到生产',
    digest: '企业本地化 AI 部署的最佳实践'
  }
];

async function publishDoc(doc, index) {
  const docPath = path.join('D:\\DocsAutoWrter\\LMStudio\\chapters', doc.file);
  
  console.log(`\n📄 发布第 ${index + 1}/${docs.length} 篇：${doc.file}`);
  
  if (!fs.existsSync(docPath)) {
    console.log('❌ 文件不存在');
    return null;
  }
  
  const content = fs.readFileSync(docPath, 'utf8');
  console.log('   原始长度:', content.length, '字符');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  console.log('📤 发布到微信公众号...');
  const result = await wechatApi.addDraft({
    title: doc.title,
    author: 'AI 技术团队',
    digest: doc.digest,
    content: html,
    thumb_media_id: process.env.WECHAT_THUMB_MEDIA_ID || 'bEleejFU9wv67FJfDm4w_sMvySqwlvOnfetM_NzcuIcfkYc4hqJ_t3L5f8uFLeCP'
  });
  
  console.log('✅ 发布成功！DraftID:', result.media_id);
  return { title: doc.title, draftId: result.media_id };
}

async function main() {
  console.log('🚀 开始批量发布 LM Studio 系列文档...\n');
  console.log('📁 文档目录：D:\\DocsAutoWrter\\LMStudio\\chapters');
  console.log('📊 文档数量:', docs.length, '篇\n');
  
  const results = [];
  
  for (let i = 0; i < docs.length; i++) {
    try {
      const result = await publishDoc(docs[i], i);
      if (result) {
        results.push(result);
      }
      // 避免 API 限流，等待 2 秒
      if (i < docs.length - 1) {
        console.log('⏳ 等待 2 秒...');
        await new Promise(r => setTimeout(r, 2000));
      }
    } catch (e) {
      console.error('❌ 发布失败:', e.message);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('✅ 批量发布完成！');
  console.log('='.repeat(60));
  console.log(`📊 总计：${docs.length} 篇`);
  console.log(`✅ 成功：${results.length} 篇\n`);
  
  console.log('发布列表:');
  results.forEach((r, i) => {
    console.log(`  ${i + 1}. ${r.title}`);
    console.log(`     DraftID: ${r.draftId}`);
  });
  
  console.log('\n💡 请在微信公众号后台预览效果！\n');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  console.error(err.stack);
  process.exit(1);
});
