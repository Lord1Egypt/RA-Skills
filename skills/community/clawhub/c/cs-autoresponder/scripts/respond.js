#!/usr/bin/env node
/**
 * respond.js - FAQ 매칭 & 자동 응답
 * 단일 메시지 처리 (테스트 및 수동 실행용)
 */

const fs = require('fs');
const path = require('path');
const FAQMatcher = require('../lib/matcher');
const ChannelAdapter = require('../lib/channels');
const CSLogger = require('../lib/logger');

function loadConfig(configPath) {
  const fullPath = path.resolve(configPath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`❌ Config file not found: ${fullPath}`);
    process.exit(1);
  }

  return JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
}

async function respond(config, channel, user, message) {
  console.log(`\n🎧 CS Auto-Responder - ${config.name}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📨 Message from: ${user} (${channel})`);
  console.log(`💬 Content: "${message}"\n`);

  // FAQ 매칭
  const matcher = new FAQMatcher(path.resolve(config.faqPath));
  const matchResult = matcher.match(message);

  // 에스컬레이션 조건 확인
  const shouldEscalate = (
    !matchResult ||
    matchResult.score < config.escalationRules.lowScoreThreshold ||
    matcher.detectNegative(message, config.escalationRules.negativeKeywords) ||
    matcher.detectHumanRequest(message, config.escalationRules.requestHumanKeywords)
  );

  let response = null;
  let faqId = null;
  let score = 0;
  let category = null;
  let escalationReason = null;

  if (shouldEscalate) {
    // 에스컬레이션 사유 결정
    if (matcher.detectNegative(message, config.escalationRules.negativeKeywords)) {
      escalationReason = '부정 키워드 감지';
    } else if (matcher.detectHumanRequest(message, config.escalationRules.requestHumanKeywords)) {
      escalationReason = '담당자 요청';
    } else if (!matchResult) {
      escalationReason = 'FAQ 매칭 실패';
    } else if (matchResult.score < config.escalationRules.lowScoreThreshold) {
      escalationReason = '낮은 매칭 점수';
    } else {
      escalationReason = '기타';
    }

    console.log(`⚠️  Escalation required`);
    console.log(`   Reason: ${escalationReason}`);
    
    // 에스컬레이션 알림은 escalate.js에서 처리
  } else {
    response = matcher.generateResponse(matchResult.faq, config);
    faqId = matchResult.faq.id;
    score = matchResult.score;
    category = matchResult.faq.category;

    console.log(`✅ FAQ Matched`);
    console.log(`   FAQ ID: ${faqId}`);
    console.log(`   Category: ${category}`);
    console.log(`   Score: ${(score * 100).toFixed(1)}%`);
    console.log(`\n📤 Response:\n${response}\n`);

    // 자동 응답 전송
    const channelAdapter = new ChannelAdapter(config);
    await channelAdapter.sendMessage(channel, user, response);
  }

  // 로그 기록
  const logger = new CSLogger(config);
  logger.log({
    channel,
    user,
    message,
    response,
    faqId,
    score,
    category,
    escalated: shouldEscalate,
    reason: escalationReason
  });

  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: node respond.js --config <path> --channel <name> --user <id> --message <text>

Options:
  --config    고객사 설정 파일 경로 (필수)
  --channel   채널 이름 (instagram, kakao, email)
  --user      사용자 ID
  --message   고객 문의 메시지

Example:
  node respond.js \\
    --config config/example.json \\
    --channel instagram \\
    --user "iam.dawn.kim" \\
    --message "영업시간 알려주세요"
    `);
    process.exit(0);
  }

  const configPath = args[args.indexOf('--config') + 1];
  const channel = args[args.indexOf('--channel') + 1];
  const user = args[args.indexOf('--user') + 1];
  const messageIndex = args.indexOf('--message') + 1;
  const message = args.slice(messageIndex).join(' ');

  if (!configPath || !channel || !user || !message) {
    console.error('❌ Missing required arguments. Use --help for usage.');
    process.exit(1);
  }

  const config = loadConfig(configPath);
  respond(config, channel, user, message).catch(err => {
    console.error('❌ Error:', err);
    process.exit(1);
  });
}

module.exports = respond;
