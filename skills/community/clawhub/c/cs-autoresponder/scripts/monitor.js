#!/usr/bin/env node
/**
 * monitor.js - 멀티채널 모니터링 메인 루프
 * 설정된 채널들을 주기적으로 폴링하여 새 메시지 감지 & 자동 응답
 */

const fs = require('fs');
const path = require('path');
const ChannelAdapter = require('../lib/channels');
const FAQMatcher = require('../lib/matcher');
const CSLogger = require('../lib/logger');

function loadConfig(configPath) {
  const fullPath = path.resolve(configPath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`❌ Config file not found: ${fullPath}`);
    process.exit(1);
  }

  return JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
}

class CSMonitor {
  constructor(config) {
    this.config = config;
    this.channelAdapter = new ChannelAdapter(config);
    this.matcher = new FAQMatcher(path.resolve(config.faqPath));
    this.logger = new CSLogger(config);
    this.processedMessages = new Set(); // 중복 처리 방지
    this.userInquiryCount = {}; // 사용자별 연속 문의 카운트
  }

  /**
   * 모니터링 시작
   */
  async start() {
    console.log(`\n🎧 CS Auto-Responder Monitor - ${this.config.name}`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    console.log(`🟢 Monitoring started at ${new Date().toISOString()}`);
    console.log(`📡 Active channels:`);
    
    Object.entries(this.config.channels).forEach(([name, config]) => {
      if (config.enabled) {
        const interval = config.checkIntervalSeconds || 60;
        console.log(`   • ${name} (check every ${interval}s)`);
      }
    });
    
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

    // 각 채널 폴링 시작
    Object.entries(this.config.channels).forEach(([channelName, channelConfig]) => {
      if (channelConfig.enabled) {
        const interval = (channelConfig.checkIntervalSeconds || 60) * 1000;
        this.pollChannel(channelName, interval);
      }
    });

    // 로그 정리 (매일 00:00)
    setInterval(() => {
      this.logger.cleanOldLogs();
    }, 24 * 60 * 60 * 1000);
  }

  /**
   * 채널 폴링
   */
  async pollChannel(channelName, interval) {
    const poll = async () => {
      try {
        const messages = await this.channelAdapter.fetchMessages(channelName);
        
        for (const msg of messages) {
          await this.processMessage(channelName, msg);
        }
      } catch (error) {
        console.error(`❌ Error polling ${channelName}:`, error.message);
      }
    };

    // 첫 폴링
    await poll();
    
    // 주기적 폴링
    setInterval(poll, interval);
  }

  /**
   * 메시지 처리
   */
  async processMessage(channelName, msg) {
    const messageId = `${channelName}:${msg.user}:${msg.timestamp}`;
    
    // 중복 처리 방지
    if (this.processedMessages.has(messageId)) {
      return;
    }
    this.processedMessages.add(messageId);

    console.log(`\n📨 New message from ${msg.user} (${channelName})`);
    console.log(`   "${msg.message}"`);

    // 사용자별 연속 문의 카운트
    const userKey = `${channelName}:${msg.user}`;
    this.userInquiryCount[userKey] = (this.userInquiryCount[userKey] || 0) + 1;

    // FAQ 매칭
    const matchResult = this.matcher.match(msg.message);

    // 에스컬레이션 조건 확인
    const shouldEscalate = this.checkEscalation(msg, matchResult, userKey);

    if (shouldEscalate) {
      await this.handleEscalation(channelName, msg, matchResult);
    } else {
      await this.handleAutoResponse(channelName, msg, matchResult);
    }
  }

  /**
   * 에스컬레이션 필요 여부 확인
   */
  checkEscalation(msg, matchResult, userKey) {
    const rules = this.config.escalationRules;

    // FAQ 매칭 실패 또는 점수 낮음
    if (!matchResult || matchResult.score < rules.lowScoreThreshold) {
      return true;
    }

    // 부정 키워드 감지
    if (this.matcher.detectNegative(msg.message, rules.negativeKeywords)) {
      return true;
    }

    // 담당자 요청
    if (this.matcher.detectHumanRequest(msg.message, rules.requestHumanKeywords)) {
      return true;
    }

    // 연속 문의 제한 초과
    if (this.userInquiryCount[userKey] >= rules.consecutiveInquiryLimit) {
      return true;
    }

    return false;
  }

  /**
   * 자동 응답 처리
   */
  async handleAutoResponse(channelName, msg, matchResult) {
    const response = this.matcher.generateResponse(matchResult.faq, this.config);
    
    console.log(`   ✅ Auto-response (FAQ: ${matchResult.faq.id}, Score: ${(matchResult.score * 100).toFixed(1)}%)`);
    
    await this.channelAdapter.sendMessage(channelName, msg.user, response);

    // 로그 기록
    this.logger.log({
      channel: channelName,
      user: msg.user,
      message: msg.message,
      response,
      faqId: matchResult.faq.id,
      score: matchResult.score,
      category: matchResult.faq.category,
      escalated: false
    });
  }

  /**
   * 에스컬레이션 처리
   */
  async handleEscalation(channelName, msg, matchResult) {
    const reason = this.getEscalationReason(msg, matchResult);
    
    console.log(`   ⚠️  Escalated (Reason: ${reason})`);

    // 에스컬레이션 알림
    const escalate = require('./escalate');
    await escalate(this.config, channelName, msg.user, msg.message, reason);

    // 로그 기록
    this.logger.log({
      channel: channelName,
      user: msg.user,
      message: msg.message,
      response: null,
      faqId: matchResult ? matchResult.faq.id : null,
      score: matchResult ? matchResult.score : 0,
      category: matchResult ? matchResult.faq.category : null,
      escalated: true,
      reason
    });
  }

  /**
   * 에스컬레이션 사유 반환
   */
  getEscalationReason(msg, matchResult) {
    const rules = this.config.escalationRules;

    if (!matchResult || matchResult.score < rules.lowScoreThreshold) {
      return 'FAQ 매칭 실패 또는 낮은 점수';
    }

    if (this.matcher.detectNegative(msg.message, rules.negativeKeywords)) {
      return '부정 키워드 감지';
    }

    if (this.matcher.detectHumanRequest(msg.message, rules.requestHumanKeywords)) {
      return '담당자 요청';
    }

    return '연속 문의 제한 초과';
  }
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: node monitor.js --config <path>

Options:
  --config    고객사 설정 파일 경로 (필수)

Example:
  node monitor.js --config config/example.json

Background execution (pm2):
  pm2 start monitor.js --name cs-mufi -- --config config/example.json
  pm2 logs cs-mufi
  pm2 stop cs-mufi
    `);
    process.exit(0);
  }

  const configPath = args[args.indexOf('--config') + 1];

  if (!configPath) {
    console.error('❌ Missing --config argument. Use --help for usage.');
    process.exit(1);
  }

  const config = loadConfig(configPath);
  const monitor = new CSMonitor(config);
  
  monitor.start().catch(err => {
    console.error('❌ Monitor error:', err);
    process.exit(1);
  });
}

module.exports = CSMonitor;
