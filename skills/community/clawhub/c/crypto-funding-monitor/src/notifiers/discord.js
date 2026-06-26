const axios = require('axios');

/**
 * Discord 通知推送器
 */
class DiscordNotifier {
  constructor(webhookUrl) {
    this.webhookUrl = webhookUrl;
  }

  /**
   * 发送简报到Discord
   * @param {string} message - 消息内容
   */
  async sendReport(message) {
    if (!this.webhookUrl) {
      console.warn('Discord webhook not configured');
      return false;
    }

    try {
      await axios.post(this.webhookUrl, {
        content: message,
        username: 'Crypto Funding Monitor',
        avatar_url: 'https://example.com/avatar.png'
      });
      return true;
    } catch (error) {
      console.error('Discord send failed:', error.message);
      return false;
    }
  }

  /**
   * 发送富文本嵌入消息
   */
  async sendEmbedReport(fundingData, tegData) {
    if (!this.webhookUrl) {
      console.warn('Discord webhook not configured');
      return false;
    }

    const embeds = this.createEmbeds(fundingData, tegData);

    try {
      await axios.post(this.webhookUrl, {
        username: 'Crypto Funding Monitor',
        embeds
      });
      return true;
    } catch (error) {
      console.error('Discord embed send failed:', error.message);
      return false;
    }
  }

  /**
   * 创建Discord嵌入消息
   */
  createEmbeds(fundingData, tegData) {
    const embeds = [];

    // 主标题
    embeds.push({
      title: '🚀 加密项目融资简报',
      description: `📅 ${new Date().toLocaleDateString('zh-CN')}`,
      color: 0x00ff00,
      timestamp: new Date().toISOString()
    });

    // 融资项目
    if (fundingData && fundingData.length > 0) {
      const fundingFields = fundingData.slice(0, 5).map(project => ({
        name: `💰 ${project.projectName}`,
        value: `**金额**: ${project.amount}\n**轮次**: ${project.round}\n**投资方**: ${project.investors}\n[查看详情](${project.url})`,
        inline: false
      }));

      embeds.push({
        title: '最新融资项目',
        fields: fundingFields,
        color: 0x0099ff
      });
    }

    // TEG项目
    if (tegData && tegData.length > 0) {
      const tegFields = tegData.slice(0, 5).map(project => ({
        name: `🎯 ${project.projectName} (${project.tokenSymbol})`,
        value: `**TEG日期**: ${project.tgeDate}\n**初始价格**: ${project.initialPrice}\n[查看详情](${project.url})`,
        inline: false
      }));

      embeds.push({
        title: '即将TEG的项目',
        fields: tegFields,
        color: 0xff9900
      });
    }

    // 底部提示
    embeds.push({
      description: '💡 **提示**: 早期参与项目建设，获取更多机会！\n⚠️ **风险提示**: 投资有风险，请谨慎决策。',
      color: 0xff0000
    });

    return embeds;
  }
}

module.exports = DiscordNotifier;
