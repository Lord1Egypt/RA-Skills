/**
 * 通过 Gateway HTTP API 发送飞书消息
 */
const GATEWAY_URL = 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = '30176f5d9e3d3372a70cefc8c1cf34248e5abc5888ec5519';
const ACCOUNT_ID = 'erbai';
const DEFAULT_TARGET = 'ou_56cdb528c6356bf5e344d2da35e98dad';

async function sendMessage(message, target = DEFAULT_TARGET) {
  const response = await fetch(`${GATEWAY_URL}/tools/invoke`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GATEWAY_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      tool: 'message',
      args: {
        action: 'send',
        channel: 'feishu',
        accountId: ACCOUNT_ID,
        target: target,
        message: message
      }
    })
  });
  
  const result = await response.json();
  
  if (!result.ok) {
    throw new Error(result.error?.message || JSON.stringify(result.error));
  }
  
  return result.result;
}

// 如果直接运行此脚本
if (require.main === module) {
  const message = process.argv[2] || '测试消息';
  const target = process.argv[3] || DEFAULT_TARGET;
  
  sendMessage(message, target)
    .then((result) => {
      console.log('消息发送成功');
      process.exit(0);
    })
    .catch((error) => {
      console.error('消息发送失败:', error.message);
      process.exit(1);
    });
}

module.exports = { sendMessage };