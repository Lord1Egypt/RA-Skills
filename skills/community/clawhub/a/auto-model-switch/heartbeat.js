#!/usr/bin/env node
/**
 * 心跳触发脚本 - 供 HEARTBEAT.md 调用
 * 
 * 用法: node heartbeat.js
 * 
 * 返回:
 * - OK: 一切正常
 * - WARN: Token即将用完
 * - SWITCH: 已切换模型
 * - ERROR: 所有模型不可用
 */

const AutoModelSwitch = require('./auto_model_switch.js');

async function main() {
  const ams = new AutoModelSwitch();
  
  try {
    const result = await ams.heartbeat();
    
    switch (result.action) {
      case 'ok':
        console.log('OK');
        break;
        
      case 'warn':
        console.log(`WARN: Token使用 ${result.percentage}%`);
        break;
        
      case 'switch':
        if (result.switched) {
          console.log(`SWITCH: ${result.from} → ${result.to}`);
        } else {
          console.log(`ERROR: 无法切换 - ${result.reason}`);
        }
        break;
    }
  } catch (e) {
    console.log('ERROR:', e.message);
  }
}

main();
