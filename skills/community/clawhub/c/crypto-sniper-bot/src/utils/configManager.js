const fs = require('fs');
const path = require('path');

class ConfigManager {
  constructor() {
    this.configPath = path.join(__dirname, '../../data/config.json');
    this.ensureDataDir();
    this.config = this.loadConfig();
  }

  ensureDataDir() {
    const dataDir = path.join(__dirname, '../../data');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
  }

  loadConfig() {
    if (fs.existsSync(this.configPath)) {
      return JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
    }
    return {
      walletPrivateKey: process.env.WALLET_PRIVATE_KEY || '',
      buyAmount: parseFloat(process.env.BUY_AMOUNT) || 0.1,
      takeProfitPercent: parseFloat(process.env.TAKE_PROFIT_PERCENT) || 50,
      stopLossPercent: parseFloat(process.env.STOP_LOSS_PERCENT) || 30,
      maxPositions: parseInt(process.env.MAX_POSITIONS) || 10,
      minLiquidity: parseFloat(process.env.MIN_LIQUIDITY) || 1000,
      minHolders: parseInt(process.env.MIN_HOLDERS) || 10,
      maxHolderConcentration: parseFloat(process.env.MAX_HOLDER_CONCENTRATION) || 50,
      botActive: false,
      notifications: {
        telegram: {
          enabled: !!process.env.TELEGRAM_BOT_TOKEN,
          botToken: process.env.TELEGRAM_BOT_TOKEN || '',
          chatId: process.env.TELEGRAM_CHAT_ID || ''
        },
        discord: {
          enabled: !!process.env.DISCORD_WEBHOOK_URL,
          webhookUrl: process.env.DISCORD_WEBHOOK_URL || ''
        },
        email: {
          enabled: !!process.env.EMAIL_USER,
          host: process.env.EMAIL_HOST || 'smtp.gmail.com',
          user: process.env.EMAIL_USER || '',
          pass: process.env.EMAIL_PASS || '',
          to: process.env.EMAIL_TO || ''
        }
      }
    };
  }

  saveConfig() {
    fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
  }

  updateConfig(updates) {
    this.config = { ...this.config, ...updates };
    this.saveConfig();
  }

  getConfig() {
    return this.config;
  }

  setBotActive(active) {
    this.config.botActive = active;
    this.saveConfig();
  }

  isBotActive() {
    return this.config.botActive;
  }
}

module.exports = new ConfigManager();
