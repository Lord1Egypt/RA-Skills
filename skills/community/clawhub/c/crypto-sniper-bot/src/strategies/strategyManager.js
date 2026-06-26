const configManager = require('../utils/configManager');
const positionManager = require('../utils/positionManager');
const tradingEngine = require('../trading/tradingEngine');
const notificationManager = require('../notifiers/notificationManager');

class StrategyManager {
  constructor() {
    this.config = configManager.getConfig();
  }

  async checkPositions() {
    const positions = positionManager.getOpenPositions();

    for (const position of positions) {
      await this.evaluatePosition(position);
    }
  }

  async evaluatePosition(position) {
    try {
      const currentPrice = await tradingEngine.getTokenPrice(position.tokenAddress);
      if (!currentPrice) return;

      const priceChange = ((currentPrice - position.buyPrice) / position.buyPrice) * 100;

      // Check take profit
      if (priceChange >= this.config.takeProfitPercent) {
        await this.closePosition(position, currentPrice, 'Take Profit');
        return;
      }

      // Check stop loss
      if (priceChange <= -this.config.stopLossPercent) {
        await this.closePosition(position, currentPrice, 'Stop Loss');
        return;
      }

      // Additional strategy: trailing stop loss
      if (priceChange > 30) {
        const trailingStopPercent = 15;
        if (priceChange < (position.highestPrice || priceChange) - trailingStopPercent) {
          await this.closePosition(position, currentPrice, 'Trailing Stop');
          return;
        }
        position.highestPrice = Math.max(position.highestPrice || priceChange, priceChange);
      }

    } catch (error) {
      console.error('Error evaluating position:', error.message);
    }
  }

  async closePosition(position, currentPrice, reason) {
    try {
      console.log(`Closing position ${position.id}: ${reason}`);

      const sellResult = await tradingEngine.sellToken(
        position.tokenAddress,
        position.amount
      );

      if (sellResult.success) {
        const closedPosition = positionManager.closePosition(
          position.id,
          currentPrice,
          sellResult.txHash,
          reason
        );

        await notificationManager.sendSellAlert(
          { symbol: position.tokenSymbol, address: position.tokenAddress },
          position.buyPrice,
          currentPrice,
          closedPosition.profitLoss,
          reason,
          sellResult.txHash
        );

        console.log(`Position closed successfully. P&L: ${closedPosition.profitLoss.toFixed(2)}%`);
      } else {
        console.error('Failed to sell token:', sellResult.error);
        await notificationManager.sendErrorAlert(
          new Error(sellResult.error),
          `Failed to close position ${position.id}`
        );
      }
    } catch (error) {
      console.error('Error closing position:', error.message);
      await notificationManager.sendErrorAlert(error, 'closePosition');
    }
  }

  shouldBuyToken(evaluation) {
    return evaluation.passed && evaluation.score >= 60;
  }

  canOpenNewPosition() {
    const currentPositions = positionManager.getPositionCount();
    return currentPositions < this.config.maxPositions;
  }
}

module.exports = new StrategyManager();
