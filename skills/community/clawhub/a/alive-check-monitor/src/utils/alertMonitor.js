/**
 * 告警监测器
 * 检查用户签到状态并发送告警
 */
class AlertMonitor {
  constructor(userManager, notifiers) {
    this.userManager = userManager;
    this.telegram = notifiers.telegram;
    this.discord = notifiers.discord;
    this.email = notifiers.email;

    this.alertThreshold = parseInt(process.env.ALERT_THRESHOLD_HOURS) || 24;
    this.highRiskThreshold = 48;
  }

  /**
   * 检查所有用户状态
   */
  async checkAllUsers() {
    console.log('[告警监测] 开始检查所有用户状态...');

    const users = this.userManager.getAllUsers();
    const alerts = [];

    for (const user of users) {
      const status = this.userManager.getUserStatus(user.userId);

      if (status.hoursSinceLastCheckin >= this.alertThreshold) {
        const alert = await this.handleAlert(status);
        if (alert) {
          alerts.push(alert);
        }
      }
    }

    console.log(`[告警监测] 完成，共发送 ${alerts.length} 条告警`);
    return alerts;
  }

  /**
   * 处理告警
   */
  async handleAlert(userStatus) {
    const { userId, name, hoursSinceLastCheckin, emergencyContacts } = userStatus;

    let alertLevel = '警告';
    let message = '';

    if (hoursSinceLastCheckin >= this.highRiskThreshold) {
      alertLevel = '高危';
      message = this.createHighRiskMessage(userStatus);
      // 通知所有紧急联系人
      await this.notifyAllContacts(userStatus, message);
    } else if (hoursSinceLastCheckin >= this.alertThreshold) {
      alertLevel = '警告';
      message = this.createWarningMessage(userStatus);
      // 通知第一紧急联系人
      await this.notifyPrimaryContact(userStatus, message);
    }

    return {
      userId,
      name,
      alertLevel,
      hoursSinceLastCheckin,
      message,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 创建警告消息
   */
  createWarningMessage(userStatus) {
    const { name, hoursSinceLastCheckin, lastCheckin } = userStatus;

    return `⚠️ 【签到提醒】\n\n` +
      `用户：${name}\n` +
      `状态：已经 ${hoursSinceLastCheckin} 小时未签到\n` +
      `上次签到：${new Date(lastCheckin).toLocaleString('zh-CN')}\n\n` +
      `请确认 TA 的安全状况。\n` +
      `如果一切正常，请提醒 TA 及时签到。`;
  }

  /**
   * 创建高危消息
   */
  createHighRiskMessage(userStatus) {
    const { name, hoursSinceLastCheckin, lastCheckin } = userStatus;

    return `🆘 【紧急告警】\n\n` +
      `用户：${name}\n` +
      `状态：已经 ${hoursSinceLastCheckin} 小时未签到！\n` +
      `上次签到：${new Date(lastCheckin).toLocaleString('zh-CN')}\n\n` +
      `⚠️ 这是高危状态！\n` +
      `建议立即联系本人或上门查看！\n` +
      `如有紧急情况，请拨打110或120。`;
  }

  /**
   * 通知第一紧急联系人
   */
  async notifyPrimaryContact(userStatus, message) {
    const contacts = userStatus.emergencyContacts;
    if (!contacts || contacts.length === 0) {
      console.warn(`用户 ${userStatus.name} 没有设置紧急联系人`);
      return;
    }

    // 按优先级排序
    const sortedContacts = contacts.sort((a, b) => (a.priority || 99) - (b.priority || 99));
    const primaryContact = sortedContacts[0];

    await this.sendNotification(primaryContact, message);
  }

  /**
   * 通知所有紧急联系人
   */
  async notifyAllContacts(userStatus, message) {
    const contacts = userStatus.emergencyContacts;
    if (!contacts || contacts.length === 0) {
      console.warn(`用户 ${userStatus.name} 没有设置紧急联系人`);
      return;
    }

    for (const contact of contacts) {
      await this.sendNotification(contact, message);
    }
  }

  /**
   * 发送通知
   */
  async sendNotification(contact, message) {
    const results = {};

    // Telegram
    if (contact.telegram && this.telegram) {
      try {
        results.telegram = await this.telegram.sendTrendingReport(
          contact.telegram,
          [],
          { title: message }
        );
      } catch (error) {
        console.error('Telegram通知失败:', error.message);
      }
    }

    // Discord
    if (contact.discord && this.discord) {
      try {
        results.discord = await this.discord.sendTrendingReport([], {
          title: message
        });
      } catch (error) {
        console.error('Discord通知失败:', error.message);
      }
    }

    // Email
    if (contact.email && this.email) {
      try {
        results.email = await this.email.sendTrendingReport(
          contact.email,
          [],
          { title: message }
        );
      } catch (error) {
        console.error('Email通知失败:', error.message);
      }
    }

    console.log(`已通知 ${contact.name} (${contact.relation})`);
    return results;
  }

  /**
   * 发送签到提醒
   */
  async sendCheckinReminder(userId) {
    const status = this.userManager.getUserStatus(userId);
    if (!status) return;

    const message = `👋 【签到提醒】\n\n` +
      `${status.name}，你好！\n` +
      `今天还没有签到哦，记得签到让大家放心～\n\n` +
      `连续签到天数：${status.consecutiveDays} 天\n` +
      `继续保持！💪`;

    // 这里可以发送给用户本人
    console.log(`发送签到提醒给 ${status.name}`);
  }
}

module.exports = AlertMonitor;
