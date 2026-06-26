const publisher = require('../../wechat-publisher/src/publisher.js');
const fs = require('fs');
const path = require('path');
const markdownToWechat = require('../src/markdown-to-wechat.js');

// 优化后的模板：列表项合并到卡片，标题带左边框，代码块优化
function generateOptimizedHTML(content, title, digest) {
  const html = markdownToWechat.markdownToWechatHtml(content);
  
  let headerHtml = '';
  
  // 添加头部
  headerHtml += '<section style="padding:0;margin:0;">';
  headerHtml += '<section style="text-align:center;margin-bottom:24px;">';
  headerHtml += '<h1 style="font-size:20px;font-weight:bold;color:#000;margin:16px 0;line-height:1.4;">' + title + '</h1>';
  headerHtml += '<section style="font-size:13px;color:#888;margin-top:12px;">';
  headerHtml += '<span>📅 ' + new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' }) + '</span>';
  headerHtml += '<span style="margin:0 8px;">·</span>';
  headerHtml += '<span>✍️ 小蛋蛋</span>';
  headerHtml += '</section></section>';
  headerHtml += '<section style="height:1px;background:#f0f0f0;margin:20px 0;"></section>';
  
  // 添加摘要
  if (digest) {
    headerHtml += '<section style="background:linear-gradient(135deg,#667eea,#764ba2);padding:20px;border-radius:12px;margin-bottom:24px;">';
    headerHtml += '<section style="font-size:15px;color:white;line-height:1.8;">💡 ' + digest + '</section>';
    headerHtml += '</section>';
  }
  
  let footerHtml = '';
  footerHtml += '<section style="height:1px;background:#f0f0f0;margin:32px 0 20px;"></section>';
  footerHtml += '<section style="text-align:center;color:#888;font-size:13px;margin-bottom:20px;">';
  footerHtml += '<section style="margin:8px 0;">— 感谢阅读 —</section>';
  footerHtml += '</section></section>';
  
  return headerHtml + html + footerHtml;
}

async function publishSeries() {
  const rootDir = 'D:\\DocsAutoWrter\\gstatck';
  
  // 读取所有文件
  const files = fs.readdirSync(rootDir).filter(f => f.endsWith('.md'));
  console.log('找到文件:', files);
  
  // 按顺序发布
  const series = [
    {
      file: '用 GStack 从零开发生产级系统：WenRead 项目全流程实战（公众号版）.md',
      title: 'GStack 实战：从需求到工程的完整落地（上）',
      digest: '需求分析 + 技术选型 + 架构设计，从 0 到 1 构建生产级系统'
    },
    {
      file: 'WenRead.md',
      title: 'WenRead 阅读系统需求文档（中）',
      digest: '完整需求说明：文件登记、借阅、归还、用户管理全流程'
    },
    {
      file: 'addfuc.md',
      title: 'WenRead 系统功能增强需求（下）',
      digest: '扫码、用户、归还三大功能增强，提升用户体验'
    }
  ];
  
  for (const item of series) {
    const filePath = path.join(rootDir, item.file);
    if (!fs.existsSync(filePath)) {
      console.log('⚠️ 文件不存在:', filePath);
      continue;
    }
    
    const content = fs.readFileSync(filePath, 'utf8');
    const html = generateOptimizedHTML(content, item.title, item.digest);
    
    console.log('\n📝 发布:', item.title);
    console.log('HTML 长度:', html.length);
    
    const result = await publisher.publish({
      title: item.title,
      author: '小蛋蛋',
      digest: item.digest,
      content: html
    });
    
    console.log('✅ 发布成功！DraftID:', result.media_id);
  }
  
  console.log('\n✅ 系列文章已全部发布完成！');
}

publishSeries().catch(console.error);
