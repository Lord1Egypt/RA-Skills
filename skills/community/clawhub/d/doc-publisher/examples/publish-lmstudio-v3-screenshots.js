// 发布 LM Studio V3.0 实战指南（带截图版）
const fs = require('fs');
const path = require('path');
const wechatApi = require('../src/wechat-api.js');
const markdownToWechat = require('../src/markdown-to-wechat.js');

async function main() {
  const docPath = 'D:\\DocsAutoWrter\\LMStudioV2\\LM Studio 实战指南 V3.md';
  
  console.log('📄 读取文档:', docPath);
  let content = fs.readFileSync(docPath, 'utf8');
  
  // 在第六节开头添加截图说明
  const screenshotNote = `## 六、快速开始指南（带截图演示）

> **📸 截图说明：** 本文配有 14 张操作截图，帮助用户直观学习。实际发布时需将截图上传到微信素材库并替换链接。
>
> **截图清单：** LM Studio 官网、下载按钮、安装界面、主界面、搜索图标、搜索模型、量化选择、下载进度、推理界面、模型选择、加载提示、API 启动、API 验证、代码测试

`;
  
  content = content.replace('## 六、快速开始指南', screenshotNote);
  
  console.log('   原始长度:', content.length, '字符');
  
  console.log('🔄 转换 Markdown 到 HTML...');
  const html = markdownToWechat.markdownToWechatHtml(content);
  console.log('   HTML 长度:', html.length, '字符');
  
  const title = 'LM Studio 实战指南：企业本地化 AI 部署完整方案（V3.0 带截图版）';
  const digest = '能力边界、部署条件、实战案例、模型推荐、14 张截图演示，一站式落地指南';
  
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
  
  console.log('\\n✅ 发布完成！');
  console.log('DraftID:', result.media_id);
  console.log('\\n💡 请在微信公众号后台预览效果！');
  console.log('\\n📸 截图清单：需要在以下位置补充截图：');
  console.log('   1. LM Studio 官网首页');
  console.log('   2. 下载按钮位置');
  console.log('   3. 安装界面');
  console.log('   4. 主界面');
  console.log('   5. 搜索图标位置');
  console.log('   6. 搜索模型界面');
  console.log('   7. 量化版本选择');
  console.log('   8. 下载进度显示');
  console.log('   9. 推理界面');
  console.log('   10. 模型选择下拉菜单');
  console.log('   11. 模型加载成功提示');
  console.log('   12. API 服务启动界面');
  console.log('   13. API 验证结果');
  console.log('   14. API 调用测试结果');
  console.log('\\n⚠️ 截图后上传到微信素材库，替换文中占位说明！\\n');
}

main().catch(err => {
  console.error('❌ 发布失败:', err.message);
  console.error(err.stack);
  process.exit(1);
});
