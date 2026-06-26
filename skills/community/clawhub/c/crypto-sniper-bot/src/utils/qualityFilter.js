const configManager = require('../utils/configManager');

class QualityFilter {
  constructor() {
    this.config = configManager.getConfig();
  }

  evaluateToken(token) {
    const scores = {
      liquidity: this.scoreLiquidity(token.liquidity),
      holders: this.scoreHolders(token.holders),
      age: this.scoreAge(token.createdAt),
      marketCap: this.scoreMarketCap(token.marketCap)
    };

    const totalScore = Object.values(scores).reduce((a, b) => a + b, 0) / Object.keys(scores).length;

    return {
      passed: totalScore >= 60,
      score: totalScore,
      scores,
      reasons: this.getReasons(scores, token)
    };
  }

  scoreLiquidity(liquidity) {
    if (liquidity >= this.config.minLiquidity * 10) return 100;
    if (liquidity >= this.config.minLiquidity * 5) return 80;
    if (liquidity >= this.config.minLiquidity) return 60;
    if (liquidity >= this.config.minLiquidity * 0.5) return 40;
    return 20;
  }

  scoreHolders(holders) {
    if (holders >= this.config.minHolders * 10) return 100;
    if (holders >= this.config.minHolders * 5) return 80;
    if (holders >= this.config.minHolders) return 60;
    if (holders >= this.config.minHolders * 0.5) return 40;
    return 20;
  }

  scoreAge(createdAt) {
    const ageMinutes = (Date.now() - createdAt) / 1000 / 60;

    // Prefer very new tokens (0-5 minutes)
    if (ageMinutes <= 5) return 100;
    if (ageMinutes <= 15) return 80;
    if (ageMinutes <= 30) return 60;
    if (ageMinutes <= 60) return 40;
    return 20;
  }

  scoreMarketCap(marketCap) {
    if (marketCap >= 100000) return 100;
    if (marketCap >= 50000) return 80;
    if (marketCap >= 10000) return 60;
    if (marketCap >= 5000) return 40;
    return 20;
  }

  getReasons(scores, token) {
    const reasons = [];

    if (scores.liquidity < 60) {
      reasons.push(`Low liquidity: $${token.liquidity}`);
    }
    if (scores.holders < 60) {
      reasons.push(`Low holders: ${token.holders}`);
    }
    if (scores.age < 60) {
      const ageMinutes = Math.floor((Date.now() - token.createdAt) / 1000 / 60);
      reasons.push(`Token age: ${ageMinutes} minutes`);
    }
    if (scores.marketCap < 60) {
      reasons.push(`Low market cap: $${token.marketCap}`);
    }

    return reasons;
  }
}

module.exports = new QualityFilter();
