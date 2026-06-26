const publisher = require('../../wechat-publisher/src/publisher.js');
const fs = require('fs');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function publish() {
  const content = fs.readFileSync('temp/gstatck-deep-dive.md', 'utf8');
  const html = markdownToWechat.markdownToWechatHtml(content);
  
  console.log('HTML 长度:', html.length);
  
  const result = await publisher.publish({
    title: 'GStack 实战深度解析：从需求到工程的完整落地（上）',
    author: '小蛋蛋',
    digest: '架构设计 + 技术选型对比 + 自动化实现 + 关键技术解析，10 倍提升开发效率',
    content: html
  });
  
  console.log('✅ 发布成功！DraftID:', result.media_id);
  return result.media_id;
}

publish().catch(console.error);
