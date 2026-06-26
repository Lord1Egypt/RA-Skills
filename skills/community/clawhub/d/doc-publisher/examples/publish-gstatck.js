const publisher = require('../../wechat-publisher/src/publisher.js');
const fs = require('fs');
const path = require('path');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function publish() {
  const rootDir = 'D:\\DocsAutoWrter\\gstatck';
  
  // 查找所有 md 文件
  const files = fs.readdirSync(rootDir).filter(f => f.endsWith('.md'));
  console.log('找到文件:', files);
  
  for (const file of files) {
    const filePath = path.join(rootDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // 提取标题
    const titleMatch = content.match(/^#\s+(.+)/);
    const title = titleMatch ? titleMatch[1] : file.replace('.md', '');
    
    // 使用 doc-publisher 模板
    const html = markdownToWechat.markdownToWechatHtml(content);
    
    console.log('\n📝 发布:', title);
    console.log('HTML 长度:', html.length);
    
    const result = await publisher.publish({
      title: title,
      author: '小蛋蛋',
      digest: 'GStack 官方规范 + 实战项目 WenRead 阅读系统，从 0 到 1 实现细节',
      content: html
    });
    
    console.log('✅ 发布成功！DraftID:', result.media_id);
  }
  
  console.log('\n✅ 所有文章已发布完成！');
}

publish().catch(console.error);
