require('dotenv').config();
const express = require('express');
const sniperBot = require('./utils/sniperBot');
const configManager = require('./utils/configManager');
const positionManager = require('./utils/positionManager');
const notificationManager = require('./notifiers/notificationManager');
const SkillPayment = require('./payment');
const payment = new SkillPayment(process.env.SKILLPAY_API_KEY);

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

// Middleware to verify SkillPay payment
app.use(async (req, res, next) => {
  if (req.path === '/health') return next();

  // For testing, allow requests with test signature
  const paymentHeader = req.headers['x-skillpay-signature'];
  if (!paymentHeader) {
    return res.status(402).json({
      error: 'Payment required',
      message: 'Please include SkillPay payment signature'
    });
  }

  // In production, verify with SkillPay API
  // For now, accept test signatures
  if (paymentHeader === 'test_signature') {
    return next();
  }

  return res.status(402).json({
    error: 'Invalid payment',
    message: 'Payment verification failed'
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'crypto-sniper-bot' });
});

// Configure bot
app.post('/configure', async (req, res) => {
  try {
    const {
      walletPrivateKey,
      buyAmount,
      takeProfitPercent,
      stopLossPercent,
      maxPositions,
      minLiquidity,
      minHolders
    } = req.body;

    const updates = {};
    if (walletPrivateKey) updates.walletPrivateKey = walletPrivateKey;
    if (buyAmount) updates.buyAmount = parseFloat(buyAmount);
    if (takeProfitPercent) updates.takeProfitPercent = parseFloat(takeProfitPercent);
    if (stopLossPercent) updates.stopLossPercent = parseFloat(stopLossPercent);
    if (maxPositions) updates.maxPositions = parseInt(maxPositions);
    if (minLiquidity) updates.minLiquidity = parseFloat(minLiquidity);
    if (minHolders) updates.minHolders = parseInt(minHolders);

    configManager.updateConfig(updates);

    res.json({
      success: true,
      message: 'Configuration updated',
      config: configManager.getConfig()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Start bot
app.post('/start', async (req, res) => {
  try {
    const result = await sniperBot.start();
    res.json(result);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Stop bot
app.post('/stop', async (req, res) => {
  try {
    const result = await sniperBot.stop();
    res.json(result);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get status
app.get('/status', (req, res) => {
  try {
    const status = sniperBot.getStatus();
    res.json(status);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get trading history
app.get('/history', (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const history = positionManager.getHistory(limit);
    const stats = {
      totalTrades: history.length,
      totalPnL: positionManager.getTotalPnL(),
      winRate: positionManager.getWinRate()
    };

    res.json({
      success: true,
      history,
      stats
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Configure notifications
app.post('/notifications', async (req, res) => {
  try {
    const { telegram, discord, email } = req.body;

    const updates = { notifications: configManager.getConfig().notifications };

    if (telegram) {
      updates.notifications.telegram = {
        enabled: telegram.enabled || false,
        botToken: telegram.botToken || '',
        chatId: telegram.chatId || ''
      };
    }

    if (discord) {
      updates.notifications.discord = {
        enabled: discord.enabled || false,
        webhookUrl: discord.webhookUrl || ''
      };
    }

    if (email) {
      updates.notifications.email = {
        enabled: email.enabled || false,
        host: email.host || 'smtp.gmail.com',
        user: email.user || '',
        pass: email.pass || '',
        to: email.to || ''
      };
    }

    configManager.updateConfig(updates);
    await notificationManager.initialize();

    res.json({
      success: true,
      message: 'Notification settings updated'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`Crypto Sniper Bot running on port ${PORT}`);
  console.log(`
⚠️  IMPORTANT WARNINGS:
- HIGH RISK: Cryptocurrency trading involves substantial risk
- Keep your private keys secure
- Start with small amounts to test
- Monitor bot activity regularly
  `);
});
