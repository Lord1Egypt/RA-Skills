const cron = require('node-cron');
const PumpFunMonitor = require('../monitors/pumpFunMonitor');
const FourMemeMonitor = require('../monitors/fourMemeMonitor');
const qualityFilter = require('../utils/qualityFilter');
const strategyManager = require('../strategies/strategyManager');
const tradingEngine = require('../trading/tradingEngine');
const positionManager = require('../utils/positionManager');
const configManager = require('../utils/configManager');
const notificationManager = require('../notifiers/notificationManager');

class SniperBot {
  constructor() {
    this.pumpFunMonitor = new PumpFunMonitor();
    this.fourMemeMonitor = new FourMemeMonitor();
    this.monitorJob = null;
    this.strategyJob = null;
    this.isRunning = false;
  }

  async start() {
    if (this.isRunning) {
      console.log('Bot is already running');
      return { success: false, message: 'Bot is already running' };
    }

    const config = configManager.getConfig();

    if (!config.walletPrivateKey) {
      return { success: false, message: 'Wallet private key not configured' };
    }

    // Initialize wallet
    const walletInitialized = tradingEngine.initializeWallet(config.walletPrivateKey);
    if (!walletInitialized) {
      return { success: false, message: 'Failed to initialize wallet' };
    }

    // Initialize notifications
    await notificationManager.initialize();

    // Start monitoring for new tokens (every 30 seconds)
    this.monitorJob = cron.schedule('*/30 * * * * *', async () => {
      await this.scanForNewTokens();
    });

    // Start checking positions (every minute)
    this.strategyJob = cron.schedule('*/60 * * * * *', async () => {
      await strategyManager.checkPositions();
    });

    this.isRunning = true;
    configManager.setBotActive(true);

    console.log('Sniper bot started successfully');
    await notificationManager.sendStatusUpdate({
      active: true,
      openPositions: positionManager.getPositionCount(),
      totalPnL: positionManager.getTotalPnL(),
      winRate: positionManager.getWinRate()
    });

    return { success: true, message: 'Bot started successfully' };
  }

  async stop() {
    if (!this.isRunning) {
      return { success: false, message: 'Bot is not running' };
    }

    if (this.monitorJob) {
      this.monitorJob.stop();
      this.monitorJob = null;
    }

    if (this.strategyJob) {
      this.strategyJob.stop();
      this.strategyJob = null;
    }

    this.isRunning = false;
    configManager.setBotActive(false);

    console.log('Sniper bot stopped');
    await notificationManager.sendStatusUpdate({
      active: false,
      openPositions: positionManager.getPositionCount(),
      totalPnL: positionManager.getTotalPnL(),
      winRate: positionManager.getWinRate()
    });

    return { success: true, message: 'Bot stopped successfully' };
  }

  async scanForNewTokens() {
    try {
      // Get new tokens from both platforms
      const [pumpTokens, fourTokens] = await Promise.all([
        this.pumpFunMonitor.getNewTokens(),
        this.fourMemeMonitor.getNewTokens()
      ]);

      const allTokens = [...pumpTokens, ...fourTokens];

      for (const token of allTokens) {
        await this.evaluateAndBuy(token);
      }
    } catch (error) {
      console.error('Error scanning for new tokens:', error.message);
    }
  }

  async evaluateAndBuy(token) {
    try {
      // Check if we can open new position
      if (!strategyManager.canOpenNewPosition()) {
        console.log('Max positions reached, skipping token:', token.symbol);
        return;
      }

      // Evaluate token quality
      const evaluation = qualityFilter.evaluateToken(token);

      if (!strategyManager.shouldBuyToken(evaluation)) {
        console.log(`Token ${token.symbol} failed quality check. Score: ${evaluation.score}`);
        return;
      }

      console.log(`Token ${token.symbol} passed quality check. Score: ${evaluation.score}`);

      // Execute buy
      const config = configManager.getConfig();
      const chain = token.chain || 'solana'; // Default to Solana
      const buyResult = await tradingEngine.buyToken(token.address, config.buyAmount, chain);

      if (buyResult.success) {
        // Record position
        const position = positionManager.addPosition(
          token.address,
          token.symbol,
          token.platform,
          buyResult.price,
          buyResult.amount,
          buyResult.txHash
        );

        // Send notification
        await notificationManager.sendBuyAlert(
          token,
          buyResult.price,
          buyResult.amount,
          buyResult.txHash,
          token.platform
        );

        console.log(`Successfully bought ${token.symbol}. Position ID: ${position.id}`);
      } else {
        console.error(`Failed to buy ${token.symbol}:`, buyResult.error);
      }
    } catch (error) {
      console.error('Error in evaluateAndBuy:', error.message);
      await notificationManager.sendErrorAlert(error, 'evaluateAndBuy');
    }
  }

  getStatus() {
    return {
      isRunning: this.isRunning,
      openPositions: positionManager.getPositionCount(),
      positions: positionManager.getOpenPositions(),
      totalPnL: positionManager.getTotalPnL(),
      winRate: positionManager.getWinRate(),
      config: configManager.getConfig()
    };
  }
}

module.exports = new SniperBot();
