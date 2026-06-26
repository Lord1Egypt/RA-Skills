/**
 * 智能定价引擎 - 根据竞争情况智能定价
 * 支持多种定价策略
 */

const chalk = require('chalk');

class PricingEngine {
  constructor() {
    this.strategies = {
      competitive: this._competitivePricing.bind(this),
      aggressive: this._aggressivePricing.bind(this),
      conservative: this._conservativePricing.bind(this)
    };
  }
  
  /**
   * 分析竞争价格
   */
  async analyzeCompetition(options = {}) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const platform = options.platform || 'all';
    const platforms = platform === 'all' ? await adapter.listPlatforms() : [platform];
    
    const platformPrices = [];
    const allPrices = [];
    
    for (const p of platforms) {
      const products = await adapter.getProducts(p, { limit: 100 });
      const prices = products.map(prod => parseFloat(prod.price));
      
      const min = Math.min(...prices);
      const max = Math.max(...prices);
      const average = prices.reduce((a, b) => a + b, 0) / prices.length;
      
      platformPrices.push({
        platform: p,
        min,
        max,
        average,
        count: prices.length
      });
      
      allPrices.push(...prices);
    }
    
    // 计算整体市场均价
    const marketAverage = allPrices.reduce((a, b) => a + b, 0) / allPrices.length;
    
    // 模拟成本
    const cost = marketAverage * 0.6; // 假设成本占 60%
    
    // 根据策略计算建议价格
    const strategy = options.strategy || 'competitive';
    const suggestedPrice = this.strategies[strategy](marketAverage, cost);
    
    // 计算利润率
    const margin = ((suggestedPrice - cost) / suggestedPrice * 100).toFixed(1);
    
    // 竞争力指数
    const competitiveness = this._calculateCompetitiveness(suggestedPrice, platformPrices);
    
    return {
      platformPrices,
      marketAverage,
      cost,
      suggestedPrice: parseFloat(suggestedPrice.toFixed(2)),
      margin: parseFloat(margin),
      competitiveness,
      strategy
    };
  }
  
  /**
   * 生成定价建议
   */
  async generateSuggestions(options = {}) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const margin = options.margin || 30;
    const strategy = options.strategy || 'competitive';
    
    const products = await adapter.getProducts('all', { limit: 100 });
    const suggestions = [];
    
    for (const product of products) {
      const cost = parseFloat(product.cost) || parseFloat(product.price) * 0.6;
      const currentPrice = parseFloat(product.price);
      
      // 计算建议价格
      let suggestedPrice;
      if (strategy === 'competitive') {
        suggestedPrice = cost / (1 - margin / 100);
      } else if (strategy === 'aggressive') {
        suggestedPrice = currentPrice * 0.95; // 降价 5% 提高竞争力
      } else {
        suggestedPrice = currentPrice * 1.1; // 涨价 10% 提高利润
      }
      
      const expectedProfit = suggestedPrice - cost;
      const change = ((suggestedPrice - currentPrice) / currentPrice * 100);
      
      suggestions.push({
        productId: product.id,
        productName: product.title,
        sku: product.sku,
        platform: product.platform,
        cost,
        currentPrice,
        suggestedPrice: parseFloat(suggestedPrice.toFixed(2)),
        expectedProfit: parseFloat(expectedProfit.toFixed(2)),
        margin: ((expectedProfit / suggestedPrice) * 100).toFixed(1),
        change: parseFloat(change.toFixed(1)),
        recommendation: change > 5 ? '涨价' : change < -5 ? '降价' : '维持'
      });
    }
    
    return suggestions;
  }
  
  /**
   * 应用定价策略
   */
  async applyPricing(options = {}) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const strategy = options.strategy || 'competitive';
    const margin = options.margin || 30;
    const platform = options.platform || 'all';
    
    const platforms = platform === 'all' ? await adapter.listPlatforms() : [platform];
    
    let updated = 0;
    let failed = 0;
    let totalChange = 0;
    
    for (const p of platforms) {
      const products = await adapter.getProducts(p, { limit: 100 });
      
      for (const product of products) {
        try {
          const cost = parseFloat(product.cost) || parseFloat(product.price) * 0.6;
          const currentPrice = parseFloat(product.price);
          
          // 计算新价格
          let newPrice;
          if (strategy === 'competitive') {
            newPrice = cost / (1 - margin / 100);
          } else if (strategy === 'aggressive') {
            newPrice = currentPrice * 0.95;
          } else {
            newPrice = currentPrice * 1.1;
          }
          
          // 更新价格
          await adapter.platforms[p].updateProduct(product.id, {
            ...product,
            price: newPrice.toFixed(2)
          });
          
          updated++;
          totalChange += ((newPrice - currentPrice) / currentPrice * 100);
          
        } catch (error) {
          failed++;
          console.error(chalk.red(`Failed to update ${product.id}:`), error.message);
        }
      }
    }
    
    return {
      updated,
      failed,
      averageChange: updated > 0 ? (totalChange / updated).toFixed(1) : 0,
      strategy,
      margin
    };
  }
  
  /**
   * 竞争性定价策略 - 跟随市场均价
   */
  _competitivePricing(marketAverage, cost) {
    // 略低于市场均价，提高竞争力
    return marketAverage * 0.95;
  }
  
  /**
   * 激进定价策略 - 低价抢占市场
   */
  _aggressivePricing(marketAverage, cost) {
    // 明显低于市场均价
    return marketAverage * 0.85;
  }
  
  /**
   * 保守定价策略 - 保证高利润
   */
  _conservativePricing(marketAverage, cost) {
    // 保证 40% 以上利润率
    return Math.max(marketAverage, cost / 0.6);
  }
  
  /**
   * 计算竞争力指数
   */
  _calculateCompetitiveness(price, platformPrices) {
    // 计算价格在各平台中的排名
    let score = 100;
    
    platformPrices.forEach(p => {
      if (price < p.average) {
        score += 5; // 低于均价加分
      } else if (price > p.average) {
        score -= 5; // 高于均价减分
      }
    });
    
    return Math.min(100, Math.max(0, score));
  }
}

module.exports = { PricingEngine };
