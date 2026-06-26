// 清空所有草稿
// 使用方法：node scripts/clear-all-drafts.js

const wechatApi = require('../src/wechat-api.js');

async function main() {
  console.log('🗑️  开始清空草稿箱...\n');
  
  // 获取所有草稿
  const token = await wechatApi.getAccessToken();
  
  console.log('📋 获取草稿列表...');
  const drafts = await wechatApi.getAllDrafts();
  
  if (!drafts || drafts.length === 0) {
    console.log('✅ 草稿箱已经是空的！');
    return;
  }
  
  console.log(`📝 找到 ${drafts.length} 篇草稿\n`);
  
  let deleted = 0;
  let failed = 0;
  
  for (const draft of drafts) {
    try {
      await wechatApi.deleteDraft(draft.media_id);
      console.log(`✅ 删除：${draft.title || draft.media_id}`);
      deleted++;
    } catch (e) {
      console.log(`❌ 失败：${draft.title || draft.media_id} - ${e.message}`);
      failed++;
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('✅ 清空完成！');
  console.log('='.repeat(60));
  console.log(`📊 总计：${drafts.length} 篇`);
  console.log(`✅ 成功：${deleted} 篇`);
  console.log(`❌ 失败：${failed} 篇`);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  console.error(err.stack);
  process.exit(1);
});
