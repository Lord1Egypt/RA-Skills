const fs = require('fs');
const path = require('path');
const moment = require('moment');

class PositionManager {
  constructor() {
    this.positionsPath = path.join(__dirname, '../../data/positions.json');
    this.historyPath = path.join(__dirname, '../../data/history.json');
    this.ensureDataDir();
    this.positions = this.loadPositions();
    this.history = this.loadHistory();
  }

  ensureDataDir() {
    const dataDir = path.join(__dirname, '../../data');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
  }

  loadPositions() {
    if (fs.existsSync(this.positionsPath)) {
      return JSON.parse(fs.readFileSync(this.positionsPath, 'utf8'));
    }
    return [];
  }

  loadHistory() {
    if (fs.existsSync(this.historyPath)) {
      return JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
    }
    return [];
  }

  savePositions() {
    fs.writeFileSync(this.positionsPath, JSON.stringify(this.positions, null, 2));
  }

  saveHistory() {
    fs.writeFileSync(this.historyPath, JSON.stringify(this.history, null, 2));
  }

  addPosition(tokenAddress, tokenSymbol, platform, buyPrice, amount, txHash) {
    const position = {
      id: Date.now().toString(),
      tokenAddress,
      tokenSymbol,
      platform,
      buyPrice,
      amount,
      buyTxHash: txHash,
      buyTime: moment().toISOString(),
      status: 'open'
    };
    this.positions.push(position);
    this.savePositions();
    return position;
  }

  closePosition(positionId, sellPrice, txHash, reason) {
    const position = this.positions.find(p => p.id === positionId);
    if (!position) return null;

    position.sellPrice = sellPrice;
    position.sellTxHash = txHash;
    position.sellTime = moment().toISOString();
    position.status = 'closed';
    position.closeReason = reason;
    position.profitLoss = ((sellPrice - position.buyPrice) / position.buyPrice) * 100;
    position.profitLossAmount = (sellPrice - position.buyPrice) * position.amount;

    // Move to history
    this.history.push(position);
    this.positions = this.positions.filter(p => p.id !== positionId);

    this.savePositions();
    this.saveHistory();

    return position;
  }

  getOpenPositions() {
    return this.positions;
  }

  getPositionCount() {
    return this.positions.length;
  }

  getHistory(limit = 50) {
    return this.history.slice(-limit).reverse();
  }

  getTotalPnL() {
    return this.history.reduce((total, trade) => {
      return total + (trade.profitLossAmount || 0);
    }, 0);
  }

  getWinRate() {
    if (this.history.length === 0) return 0;
    const wins = this.history.filter(t => t.profitLoss > 0).length;
    return (wins / this.history.length) * 100;
  }
}

module.exports = new PositionManager();
