const publisher = require('../../wechat-publisher/src/publisher.js');
const fs = require('fs');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function publishArticle(part, filename, title, digest) {
  const content = fs.readFileSync('C:\\Users\\LIYONG\\.openclaw\\workspace\\skills\\wechat-publisher\\' + filename, 'utf8');
  
  // 使用 doc-publisher 的 markdown-to-wechat 模板
  const html = markdownToWechat.markdownToWechatHtml(content);
  
  console.log(part + ' HTML 长度:', html.length);
  
  const result = await publisher.publish({
    title: title,
    author: '小蛋蛋',
    digest: digest,
    content: html
  });
  
  console.log('✅ ' + part + '发布成功！DraftID:', result.media_id);
  return result.media_id;
}

async function main() {
  try {
    console.log('📝 开始发布上篇（使用 doc-publisher 模板）...');
    const draftId1 = await publishArticle(
      '上篇',
      'articles/claude-routines-part1.md',
      'Claude Code Routines 实战指南（上）：配置你的 24 小时 AI 员工',
      '三种触发方式详解 + 5 分钟快速入门 + 国内访问方案'
    );
    
    console.log('\n📝 开始发布下篇...');
    const draftId2 = await publishArticle(
      '下篇',
      'articles/claude-routines-part2.md',
      'Claude Code Routines 实战指南（下）：高级用法与风险防范',
      '早期用户真实场景 + 提示词优化技巧 + 限额成本分析 + 三大风险防范'
    );
    
    console.log('\n✅ 两篇都已发布完成！');
    console.log('上篇 DraftID:', draftId1);
    console.log('下篇 DraftID:', draftId2);
    
  } catch (error) {
    console.error('❌ 发布失败:', error.message);
    throw error;
  }
}

main().catch(console.error);
