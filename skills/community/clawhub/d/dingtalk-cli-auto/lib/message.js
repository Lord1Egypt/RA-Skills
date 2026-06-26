/**
 * 消息发送模块
 * 支持文本、Markdown 消息发送给用户或群聊
 */

const { DWSClient, formatISO } = require('./dws');
const axios = require('axios');

class MessageClient {
  constructor(options = {}) {
    this.dws = new DWSClient(options);
  }

  /**
   * 发送文本消息
   * @param {string} userId - 用户ID (与 chatId 二选一)
   * @param {string} chatId - 群聊ID (与 userId 二选一)
   * @param {string} content - 消息内容
   * @returns {Object} 发送结果
   */
  async sendText(userId, chatId, content) {
    if (!userId && !chatId) {
      throw new Error('必须指定 userId 或 chatId');
    }
    if (!content) {
      throw new Error('消息内容不能为空');
    }

    // 使用 dws 发送消息
    const args = [];
    if (userId) args.push('--user-id', userId);
    if (chatId) args.push('--chat-id', chatId);
    args.push('--content', content);

    const result = this.dws.exec('message', ['send-text', ...args]);
    return result;
  }

  /**
   * 发送 Markdown 消息
   * @param {string} userId - 用户ID
   * @param {string} chatId - 群聊ID
   * @param {string} title - 标题
   * @param {string} content - Markdown 内容
   * @returns {Object} 发送结果
   */
  async sendMarkdown(userId, chatId, title, content) {
    if (!userId && !chatId) {
      throw new Error('必须指定 userId 或 chatId');
    }
    if (!content) {
      throw new Error('消息内容不能为空');
    }

    const args = [];
    if (userId) args.push('--user-id', userId);
    if (chatId) args.push('--chat-id', chatId);
    if (title) args.push('--title', title);
    args.push('--content', content);

    const result = this.dws.exec('message', ['send-markdown', ...args]);
    return result;
  }

  /**
   * 使用 Webhook 发送机器人消息
   * @param {string} webhook - Webhook 地址
   * @param {string} secret - 加签密钥 (可选)
   * @param {string} content - 消息内容
   * @param {string} msgType - 消息类型 (text/markdown)
   * @returns {Object} 发送结果
   */
  async sendRobot(webhook, secret, content, msgType = 'text') {
    if (!webhook || !content) {
      throw new Error('webhook 和 content 不能为空');
    }

    // 如果有密钥，需要签名
    let url = webhook;
    if (secret) {
      const timestamp = Date.now();
      const sign = this.sign(secret, timestamp);
      const connector = webhook.includes('?') ? '&' : '?';
      url = `${webhook}${connector}timestamp=${timestamp}&sign=${sign}`;
    }

    // 构建消息体
    const body = {
      msgtype: msgType
    };
    
    if (msgType === 'text') {
      body.text = { content };
    } else if (msgType === 'markdown') {
      body.markdown = { title: '通知', text: content };
    }

    try {
      const response = await axios.post(url, body, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      });
      
      if (response.data && response.data.errcode === 0) {
        return { success: true, messageId: response.data.msgid };
      }
      throw new Error(response.data?.errmsg || '发送失败');
    } catch (error) {
      throw new Error(`机器人消息发送失败: ${error.message}`);
    }
  }

  /**
   * 生成签名
   * @param {string} secret - 密钥
   * @param {number} timestamp - 时间戳
   * @returns {string} 签名
   */
  sign(secret, timestamp) {
    const crypto = require('crypto');
    const str = `${timestamp}\n${secret}`;
    const hmac = crypto.createHmac('sha256', secret);
    hmac.update(str);
    return encodeURIComponent(hmac.digest('base64'));
  }
}

module.exports = MessageClient;