/**
 * Notification Service
 * Sends notifications via Telegram, Email, OpenClaw
 */

const axios = require('axios');
const logger = require('../utils/logger');
const config = require('../config/config');

class NotificationService {
  /**
   * Send payment notification
   */
  async sendPaymentNotification(data) {
    const { type, provider, amount, currency, customer, error } = data;

    let message;
    let emoji;

    switch (type) {
      case 'success':
        emoji = '💰';
        message = `${emoji} 새로운 결제 성공!\n\n`;
        message += `제공자: ${provider}\n`;
        message += `금액: ${currency} ${amount.toLocaleString()}\n`;
        message += `고객: ${customer || 'N/A'}\n`;
        message += `시간: ${new Date().toLocaleString('ko-KR')}`;
        break;

      case 'failed':
        emoji = '❌';
        message = `${emoji} 결제 실패\n\n`;
        message += `제공자: ${provider}\n`;
        message += `금액: ${currency} ${amount.toLocaleString()}\n`;
        message += `고객: ${customer || 'N/A'}\n`;
        message += `오류: ${error || 'Unknown error'}\n`;
        message += `시간: ${new Date().toLocaleString('ko-KR')}`;
        break;

      default:
        message = 'Unknown payment event';
    }

    await this.sendTelegram(message);
    logger.info('Payment notification sent', { type, amount });
  }

  /**
   * Send subscription notification
   */
  async sendSubscriptionNotification(data) {
    const { type, provider, customer, plan } = data;

    let message;
    let emoji;

    switch (type) {
      case 'created':
        emoji = '🎉';
        message = `${emoji} 새로운 구독 생성!\n\n`;
        message += `제공자: ${provider}\n`;
        message += `플랜: ${plan}\n`;
        message += `고객: ${customer}\n`;
        message += `시간: ${new Date().toLocaleString('ko-KR')}`;
        break;

      case 'cancelled':
        emoji = '😢';
        message = `${emoji} 구독 취소\n\n`;
        message += `제공자: ${provider}\n`;
        message += `고객: ${customer}\n`;
        message += `시간: ${new Date().toLocaleString('ko-KR')}`;
        break;

      default:
        message = 'Unknown subscription event';
    }

    await this.sendTelegram(message);
    logger.info('Subscription notification sent', { type, customer });
  }

  /**
   * Send daily revenue summary
   */
  async sendDailySummary(data) {
    const {
      date,
      totalRevenue,
      totalPayments,
      successfulPayments,
      failedPayments,
      newSubscriptions,
      cancelledSubscriptions
    } = data;

    const message = `
📊 일일 재무 요약 (${date})

【매출】
💰 총 매출: ${totalRevenue.toLocaleString()}원
✅ 성공한 결제: ${successfulPayments}건
❌ 실패한 결제: ${failedPayments}건
📦 총 거래: ${totalPayments}건

【구독】
🎉 신규 구독: ${newSubscriptions}건
😢 취소된 구독: ${cancelledSubscriptions}건

시간: ${new Date().toLocaleString('ko-KR')}
    `.trim();

    await this.sendTelegram(message);
    logger.info('Daily summary sent', { date, totalRevenue });
  }

  /**
   * Send Telegram message
   */
  async sendTelegram(text) {
    if (!config.telegram.botToken || !config.telegram.chatId) {
      logger.warn('Telegram not configured, skipping notification');
      return;
    }

    try {
      await axios.post(
        `https://api.telegram.org/bot${config.telegram.botToken}/sendMessage`,
        {
          chat_id: config.telegram.chatId,
          text,
          parse_mode: 'HTML'
        }
      );
      logger.debug('Telegram message sent');
    } catch (error) {
      logger.error('Failed to send Telegram message', {
        error: error.message
      });
    }
  }

  /**
   * Send via OpenClaw
   */
  async sendOpenClaw(message) {
    if (!config.openclaw.apiUrl || !config.openclaw.token) {
      logger.warn('OpenClaw not configured, skipping notification');
      return;
    }

    try {
      await axios.post(
        `${config.openclaw.apiUrl}/api/message`,
        {
          action: 'send',
          message
        },
        {
          headers: {
            Authorization: `Bearer ${config.openclaw.token}`
          }
        }
      );
      logger.debug('OpenClaw message sent');
    } catch (error) {
      logger.error('Failed to send OpenClaw message', {
        error: error.message
      });
    }
  }
}

module.exports = new NotificationService();
