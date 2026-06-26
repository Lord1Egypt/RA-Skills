#!/usr/bin/env node

/**
 * 飞书消息表情回复工具 - 使用飞书官方 SDK
 * 用法: node add_reaction_sdk.js <message_id> <emoji_type>
 */

const MESSAGE_ID = process.argv[2];
const EMOJI_TYPE = process.argv[3];

if (!MESSAGE_ID || !EMOJI_TYPE) {
  console.error('用法: node add_reaction_sdk.js <message_id> <emoji_type>');
  console.error('示例: node add_reaction_sdk.js om_xxx THUMBSUP');
  process.exit(1);
}

(async () => {
  try {
    const Lark = await import('@larksuiteoapi/node-sdk');
    
    const APP_ID = process.env.FEISHU_APP_ID_INSTANCE2;
    const APP_SECRET = process.env.FEISHU_APP_SECRET_INSTANCE2;
    
    if (!APP_ID || !APP_SECRET) {
      throw new Error('未设置环境变量: FEISHU_APP_ID_INSTANCE2 或 FEISHU_APP_SECRET_INSTANCE2');
    }

    console.log('正在初始化飞书客户端...');
    const client = new Lark.default.Client({
      appId: APP_ID,
      appSecret: APP_SECRET,
      domain: Lark.default.Domain.Feishu,
    });

    console.log(`正在添加表情回复: ${EMOJI_TYPE} 到消息 ${MESSAGE_ID} ...`);
    const response = await client.im.messageReaction.create({
      path: { message_id: MESSAGE_ID },
      data: {
        reaction_type: {
          emoji_type: EMOJI_TYPE,
        },
      },
    });

    if (response.code !== 0) {
      throw new Error(`API 返回错误: code=${response.code}, msg=${response.msg}`);
    }

    console.log('✅ 成功添加表情回复!');
    console.log('Reaction ID:', response.data?.reaction_id);
  } catch (error) {
    console.error('❌ 添加表情回复失败:', error.message);
    if (error.response) {
      console.error('详细信息:', JSON.stringify(error.response.data, null, 2));
    }
    process.exit(1);
  }
})();
