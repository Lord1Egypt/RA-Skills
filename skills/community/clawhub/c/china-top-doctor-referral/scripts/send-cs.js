#!/usr/bin/env node
'use strict';

// Send a message to customer service via OceanBus P2P.
// Usage: node scripts/send-cs.js <message>

const { createOceanBus } = require('oceanbus');
const config = require('../config/api');

async function main() {
  const message = process.argv.slice(2).join(' ');
  if (!message) {
    console.log('Usage: node scripts/send-cs.js <message>');
    process.exit(1);
  }

  if (!config.csOpenid || config.csOpenid.startsWith('请在')) {
    console.error('客服 Agent OpenID 未配置。请设置环境变量 OCEANBUS_CS_OPENID。');
    process.exit(1);
  }

  const ob = await createOceanBus({ keyStore: { type: 'memory' } });

  try {
    await ob.send(config.csOpenid, message);
    console.log('消息已发送给客服。');
  } catch (e) {
    console.error('发送失败:', e.message);
    process.exit(1);
  } finally {
    await ob.destroy();
  }
}

main();
