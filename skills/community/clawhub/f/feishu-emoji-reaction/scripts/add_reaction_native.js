#!/usr/bin/env node

/**
 * 飞书消息表情回复工具 - 使用 OpenClaw 内部 API
 * 用法: node add_reaction_native.js <message_id> <emoji_type>
 */

const MESSAGE_ID = process.argv[2];
const EMOJI_TYPE = process.argv[3];

if (!MESSAGE_ID || !EMOJI_TYPE) {
  console.error('用法: node add_reaction_native.js <message_id> <emoji_type>');
  console.error('示例: node add_reaction_native.js om_xxx THUMBSUP');
  process.exit(1);
}

// 动态导入 OpenClaw 的飞书 reactions 模块
(async () => {
  try {
    const { addReactionFeishu } = await import(
      '/Users/jyxc-dz-0100132/.npm-global/lib/node_modules/openclaw/extensions/feishu/src/reactions.js'
    );
    
    const { loadConfig } = await import(
      '/Users/jyxc-dz-0100132/.npm-global/lib/node_modules/openclaw/dist/index.js'
    );

    console.log('正在加载配置...');
    const cfg = await loadConfig();

    console.log(`正在添加表情回复: ${EMOJI_TYPE} 到消息 ${MESSAGE_ID} ...`);
    const result = await addReactionFeishu({
      cfg,
      messageId: MESSAGE_ID,
      emojiType: EMOJI_TYPE,
      accountId: 'instance2', // 使用 instance2 账号
    });

    console.log('✅ 成功添加表情回复!');
    console.log('Reaction ID:', result.reactionId);
  } catch (error) {
    console.error('❌ 添加表情回复失败:', error.message);
    process.exit(1);
  }
})();
