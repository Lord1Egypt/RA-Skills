#!/usr/bin/env node
/**
 * escalate.js - 에스컬레이션 알림
 * 복잡한 문의를 사장님에게 Discord/카톡으로 전달
 */

const fs = require('fs');
const path = require('path');

function loadConfig(configPath) {
  const fullPath = path.resolve(configPath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`❌ Config file not found: ${fullPath}`);
    process.exit(1);
  }

  return JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
}

async function escalate(config, channel, user, message, reason) {
  console.log(`\n🚨 Escalation Alert - ${config.name}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📨 From: ${user} (${channel})`);
  console.log(`💬 Message: "${message}"`);
  console.log(`⚠️  Reason: ${reason}\n`);

  const escalationTarget = config.escalationTarget;
  
  // 알림 메시지 생성
  const alertMessage = `
🚨 **CS 에스컬레이션** - ${config.name}

**채널**: ${channel}
**고객**: ${user}
**메시지**: ${message}

**사유**: ${reason}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 고객에게 답변 후 로그를 확인하세요.
  `.trim();

  if (escalationTarget.type === 'discord') {
    // Discord 알림 (OpenClaw message tool 사용)
    console.log(`📤 [MOCK] Sending Discord alert to channel ${escalationTarget.channelId}`);
    console.log(`   Mention: ${escalationTarget.mention || 'none'}`);
    console.log(`\n${alertMessage}\n`);

    // Production:
    // const { exec } = require('child_process');
    // const mention = escalationTarget.mention ? `<@${escalationTarget.mention}>` : '';
    // const fullMessage = `${mention}\n${alertMessage}`;
    // 
    // await exec(`openclaw message send --channel ${escalationTarget.channelId} --message "${fullMessage}"`);
    
  } else if (escalationTarget.type === 'kakao') {
    console.log(`📤 [MOCK] Sending Kakao alert to ${escalationTarget.phoneNumber}`);
    console.log(`\n${alertMessage}\n`);

    // Production: Kakao 알림톡 전송
  } else {
    console.error(`❌ Unknown escalation type: ${escalationTarget.type}`);
  }

  console.log(`✅ Escalation notification sent`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: node escalate.js --config <path> --channel <name> --user <id> --message <text> --reason <reason>

Options:
  --config    고객사 설정 파일 경로 (필수)
  --channel   채널 이름 (instagram, kakao, email)
  --user      사용자 ID
  --message   고객 문의 메시지
  --reason    에스컬레이션 사유

Example:
  node escalate.js \\
    --config config/example.json \\
    --channel instagram \\
    --user "angry_customer" \\
    --message "환불 요청합니다" \\
    --reason "환불 키워드"
    `);
    process.exit(0);
  }

  const configPath = args[args.indexOf('--config') + 1];
  const channel = args[args.indexOf('--channel') + 1];
  const user = args[args.indexOf('--user') + 1];
  const messageIndex = args.indexOf('--message') + 1;
  const reasonIndex = args.indexOf('--reason');
  const message = args.slice(messageIndex, reasonIndex).join(' ');
  const reason = args.slice(reasonIndex + 1).join(' ');

  if (!configPath || !channel || !user || !message || !reason) {
    console.error('❌ Missing required arguments. Use --help for usage.');
    process.exit(1);
  }

  const config = loadConfig(configPath);
  escalate(config, channel, user, message, reason).catch(err => {
    console.error('❌ Error:', err);
    process.exit(1);
  });
}

module.exports = escalate;
