const { Telegraf } = require('telegraf');

/**
 * Telegram 通知推送器
 */
class TelegramNotifier {
  constructor(botToken) {
    this.botToken = botToken;
    this.bot = botToken ? new Telegraf(botToken) : null;
  }

  /**
   * 发送简报到Telegram
   * @param {string} chatId - 聊天ID
   * @param {string} message - 消息内容
   */
  async sendReport(chatId, message) {
    if (!this.bot) {
      console.warn('Telegram bot not configured');
      return false;
    }

    try {
      await this.bot.telegram.sendMessage(chatId, message, {
        parse_mode: 'Markdown',
        disable_web_page_preview: true
      });
      return true;
    } catch (error) {
      console.error('Telegram send failed:', error.message);
      return false;
    }
  }

  /**
   * 发送格式化的融资简报
   */
  async sendFundingReport(chatId, fundingData, tegData) {
    const message = this.formatReport(fundingData, tegData);
    return await this.sendReport(chatId, message);
  }

  /**
   * 格式化简报消息
   */
  formatReport(fundingData, tegData) {
    let message = '🚀 *加密项目融资简报*\n\n';
    message += `📅 ${new Date().toLocaleDateString('zh-CN')}\n\n`;

    // 融资信息
    if (fundingData && fundingData.length > 0) {
      message += '💰 *最新融资项目*\n\n';
      fundingData.slice(0, 5).forEach((project, index) => {
        message += `${index + 1}. *${project.projectName}*\n`;
        message += `   💵 金额: ${project.amount}\n`;
        message += `   🔄 轮次: ${project.round}\n`;
        message += `   👥 投资方: ${project.investors}\n`;
        message += `   🔗 [查看详情](${project.url})\n\n`;
      });
    }

    // TEG项目
    if (tegData && tegData.length > 0) {
      message += '🎯 *即将TEG的项目*\n\n';
      tegData.slice(0, 5).forEach((project, index) => {
        message += `${index + 1}. *${project.projectName}* (${project.tokenSymbol})\n`;
        message += `   📆 TEG日期: ${project.tgeDate}\n`;
        message += `   💎 初始价格: ${project.initialPrice}\n`;
        message += `   🔗 [查看详情](${project.url})\n\n`;
      });
    }

    message += '\n---\n';
    message += '💡 *提示*: 早期参与项目建设，获取更多机会！\n';
    message += '⚠️ *风险提示*: 投资有风险，请谨慎决策。';

    return message;
  }

  /**
   * 启动bot监听
   */
  launch() {
    if (!this.bot) {
      console.warn('Telegram bot not configured');
      return;
    }

    this.bot.start((ctx) => {
      ctx.reply('欢迎使用加密项目融资监测服务！\n\n使用 /subscribe 订阅定时推送');
    });

    this.bot.command('subscribe', (ctx) => {
      ctx.reply('订阅成功！您将收到每日融资简报。');
    });

    this.bot.command('unsubscribe', (ctx) => {
      ctx.reply('已取消订阅。');
    });

    this.bot.launch();
    console.log('Telegram bot started');
  }
}

module.exports = TelegramNotifier;
