const configManager = require('../utils/configManager');

class NotificationManager {
  constructor() {
    this.telegram = null;
    this.discord = null;
    this.email = null;
  }

  async initialize() {
    const config = configManager.getConfig();

    if (config.notifications.telegram.enabled) {
      const TelegramNotifier = require('./telegram');
      this.telegram = new TelegramNotifier(
        config.notifications.telegram.botToken,
        config.notifications.telegram.chatId
      );
    }

    if (config.notifications.discord.enabled) {
      const DiscordNotifier = require('./discord');
      this.discord = new DiscordNotifier(config.notifications.discord.webhookUrl);
    }

    if (config.notifications.email.enabled) {
      const EmailNotifier = require('./email');
      this.email = new EmailNotifier(config.notifications.email);
    }
  }

  async sendBuyAlert(token, price, amount, txHash, platform) {
    const message = `
🟢 **BUY EXECUTED**

Platform: ${platform}
Token: ${token.symbol}
Address: ${token.address}
Price: $${price.toFixed(6)}
Amount: ${amount} SOL
TX: ${txHash}

Time: ${new Date().toISOString()}
    `.trim();

    await this.sendToAll(message);
  }

  async sendSellAlert(token, buyPrice, sellPrice, profitLoss, reason, txHash) {
    const emoji = profitLoss > 0 ? '🟢' : '🔴';
    const message = `
${emoji} **SELL EXECUTED**

Token: ${token.symbol}
Reason: ${reason}
Buy Price: $${buyPrice.toFixed(6)}
Sell Price: $${sellPrice.toFixed(6)}
P&L: ${profitLoss.toFixed(2)}%
TX: ${txHash}

Time: ${new Date().toISOString()}
    `.trim();

    await this.sendToAll(message);
  }

  async sendErrorAlert(error, context) {
    const message = `
⚠️ **ERROR ALERT**

Context: ${context}
Error: ${error.message}

Time: ${new Date().toISOString()}
    `.trim();

    await this.sendToAll(message);
  }

  async sendStatusUpdate(status) {
    const message = `
📊 **BOT STATUS UPDATE**

Status: ${status.active ? 'Active' : 'Stopped'}
Open Positions: ${status.openPositions}
Total P&L: $${status.totalPnL.toFixed(2)}
Win Rate: ${status.winRate.toFixed(1)}%

Time: ${new Date().toISOString()}
    `.trim();

    await this.sendToAll(message);
  }

  async sendToAll(message) {
    const promises = [];

    if (this.telegram) {
      promises.push(this.telegram.send(message).catch(err =>
        console.error('Telegram notification failed:', err.message)
      ));
    }

    if (this.discord) {
      promises.push(this.discord.send(message).catch(err =>
        console.error('Discord notification failed:', err.message)
      ));
    }

    if (this.email) {
      promises.push(this.email.send('Crypto Sniper Alert', message).catch(err =>
        console.error('Email notification failed:', err.message)
      ));
    }

    await Promise.allSettled(promises);
  }
}

module.exports = new NotificationManager();
