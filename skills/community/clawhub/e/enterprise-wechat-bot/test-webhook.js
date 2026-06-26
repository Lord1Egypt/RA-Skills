#!/usr/bin/env node

/**
 * WeChat Automation 测试脚本
 * 
 * 用法:
 *   node test-webhook.js YOUR_WEBHOOK_KEY
 */

const { sendMessage } = require('./index');

async function test() {
  const webhookKey = process.argv[2];

  if (!webhookKey) {
    console.log('用法：node test-webhook.js YOUR_WEBHOOK_KEY');
    console.log('');
    console.log('获取 Webhook Key:');
    console.log('1. 打开企业微信管理后台');
    console.log('2. 进入「工作台」→「群机器人」');
    console.log('3. 添加机器人，复制 Webhook Key');
    process.exit(1);
  }

  console.log('🧪 开始测试企业微信自动化...\n');

  try {
    // 测试 1: 发送文本消息
    console.log('📤 测试 1: 发送文本消息...');
    const result1 = await sendMessage({
      webhookKey,
      text: '🎉 WeChat Automation 测试消息！\n\n技能运行正常，可以开始使用了。',
      markdown: false
    });
    console.log('✅ 文本消息发送成功，ID:', result1.msgid);

    // 等待 1 秒
    await new Promise(r => setTimeout(r, 1000));

    // 测试 2: 发送 Markdown 消息
    console.log('\n📤 测试 2: 发送 Markdown 消息...');
    const result2 = await sendMessage({
      webhookKey,
      text: `## 🎯 WeChat Automation 测试

### 功能列表
- ✅ 文本消息
- ✅ Markdown 格式
- ✅ 群聊推送
- ✅ @提醒

### 状态
所有功能运行正常！
`,
      markdown: true
    });
    console.log('✅ Markdown 消息发送成功，ID:', result2.msgid);

    console.log('\n🎉 所有测试通过！技能可以正常使用了。');
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    process.exit(1);
  }
}

test();
