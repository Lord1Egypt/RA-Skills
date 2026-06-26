#!/usr/bin/env node
/**
 * channels.js - 채널 어댑터 (Mock API)
 * Production에서는 실제 API로 교체
 */

class ChannelAdapter {
  constructor(config) {
    this.config = config;
  }

  /**
   * 특정 채널에서 새 메시지 가져오기
   * @param {string} channelName - instagram, kakao, email
   * @returns {Promise<Array>} 메시지 배열
   */
  async fetchMessages(channelName) {
    const channelConfig = this.config.channels[channelName];
    
    if (!channelConfig || !channelConfig.enabled) {
      return [];
    }

    // Mock 데이터 생성
    return this.generateMockMessages(channelName);
  }

  /**
   * 메시지 전송
   * @param {string} channelName 
   * @param {string} recipient 
   * @param {string} message 
   * @returns {Promise<boolean>}
   */
  async sendMessage(channelName, recipient, message) {
    const channelConfig = this.config.channels[channelName];
    
    if (!channelConfig || !channelConfig.enabled) {
      console.error(`❌ Channel ${channelName} is not enabled`);
      return false;
    }

    console.log(`📤 [MOCK] Sending to ${channelName} (${recipient}): ${message}`);
    
    // Production: 실제 API 호출
    // - Instagram: tools/insta-cli/v2.js
    // - Kakao: Kakao Alimtalk API
    // - Email: himalaya 또는 nodemailer
    
    return true;
  }

  /**
   * Mock 메시지 생성 (테스트용)
   */
  generateMockMessages(channelName) {
    const mockMessages = {
      instagram: [
        { user: 'iam.dawn.kim', message: '영업시간 알려주세요', timestamp: new Date().toISOString() },
        { user: 'test_user_123', message: '가격이 얼마예요?', timestamp: new Date().toISOString() }
      ],
      kakao: [
        { user: '010-1234-5678', message: '예약 가능한가요?', timestamp: new Date().toISOString() }
      ],
      email: [
        { user: 'customer@example.com', message: '위치가 어디인가요?', timestamp: new Date().toISOString() }
      ]
    };

    // 실제로는 빈 배열 반환 (주기적으로 폴링)
    // 여기서는 테스트를 위해 mock 데이터 반환
    return mockMessages[channelName] || [];
  }

  /**
   * Instagram DM 조회 (실제 연동 예시)
   */
  async fetchInstagramDMs() {
    // Production 연동 예시:
    // const { exec } = require('child_process');
    // const { promisify } = require('util');
    // const execAsync = promisify(exec);
    // 
    // const CLI = '/Users/mupeng/.openclaw/workspace/tools/insta-cli/v2.js';
    // const result = await execAsync(`node ${CLI} unread`);
    // const dms = JSON.parse(result.stdout);
    // 
    // return dms.map(dm => ({
    //   user: dm.username,
    //   message: dm.lastMessage,
    //   timestamp: dm.timestamp
    // }));

    return [];
  }

  /**
   * 카카오톡 알림톡 전송 (실제 연동 예시)
   */
  async sendKakaoAlimtalk(recipient, message) {
    // Production 연동 예시:
    // const axios = require('axios');
    // const response = await axios.post('https://kapi.kakao.com/v1/api/talk/...', {
    //   receiver: recipient,
    //   message: message
    // }, {
    //   headers: {
    //     'Authorization': `KakaoAK ${this.config.channels.kakao.apiKey}`
    //   }
    // });
    // 
    // return response.status === 200;

    return true;
  }

  /**
   * 이메일 전송 (실제 연동 예시)
   */
  async sendEmail(recipient, subject, body) {
    // Production 연동 예시:
    // const nodemailer = require('nodemailer');
    // const transporter = nodemailer.createTransport({
    //   host: this.config.channels.email.imapHost,
    //   port: 587,
    //   secure: false,
    //   auth: {
    //     user: this.config.channels.email.address,
    //     pass: process.env.EMAIL_PASSWORD
    //   }
    // });
    // 
    // await transporter.sendMail({
    //   from: this.config.channels.email.address,
    //   to: recipient,
    //   subject: subject,
    //   text: body
    // });

    return true;
  }
}

module.exports = ChannelAdapter;
