/**
 * 库存管理器 - 实时库存同步
 * 确保多平台库存一致性
 */

const chalk = require('chalk');

class InventoryManager {
  constructor() {
    this.syncQueue = [];
    this.lastSync = null;
  }
  
  /**
   * 同步多平台库存
   */
  async syncInventory(options = {}) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const platform = options.platform || 'all';
    const platforms = platform === 'all' ? await adapter.listPlatforms() : [platform];
    
    let synced = 0;
    let updated = 0;
    let failed = 0;
    
    // 获取主平台库存（通常是最先上架的平台）
    const masterPlatform = platforms[0];
    const masterInventory = await this._getPlatformInventory(adapter, masterPlatform);
    
    console.log(chalk.cyan(`主平台：${masterPlatform}, SKU 数量：${masterInventory.length}`));
    
    // 同步到其他平台
    for (const targetPlatform of platforms.slice(1)) {
      console.log(chalk.gray(`同步到 ${targetPlatform}...`));
      
      const targetInventory = await this._getPlatformInventory(adapter, targetPlatform);
      
      for (const masterItem of masterInventory) {
        try {
          const targetItem = targetInventory.find(i => i.sku === masterItem.sku);
          
          if (targetItem) {
            // 更新现有商品库存
            if (targetItem.quantity !== masterItem.quantity) {
              await adapter.platforms[targetPlatform].updateInventory(
                masterItem.sku,
                masterItem.quantity
              );
              updated++;
            }
          } else {
            // TODO: 处理新商品
          }
          
          synced++;
        } catch (error) {
          failed++;
          console.error(chalk.red(`同步失败 ${masterItem.sku}:`), error.message);
        }
      }
    }
    
    this.lastSync = new Date().toISOString();
    
    return {
      synced,
      updated,
      failed,
      lastSync: this.lastSync
    };
  }
  
  /**
   * 获取平台库存
   */
  async _getPlatformInventory(adapter, platform) {
    const products = await adapter.getProducts(platform, { limit: 1000 });
    
    return products.map(p => ({
      sku: p.sku,
      productId: p.id,
      platform,
      quantity: p.quantity || 0,
      reserved: p.reserved || 0,
      available: (p.quantity || 0) - (p.reserved || 0)
    }));
  }
  
  /**
   * 获取库存状态
   */
  async getInventoryStatus() {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const platforms = await adapter.listPlatforms();
    const inventory = [];
    
    for (const platform of platforms) {
      const products = await adapter.getProducts(platform, { limit: 1000 });
      
      products.forEach(p => {
        inventory.push({
          sku: p.sku,
          productId: p.id,
          platform,
          title: p.title,
          quantity: p.quantity || 0,
          reserved: p.reserved || 0,
          available: (p.quantity || 0) - (p.reserved || 0),
          status: this._getStockStatus(p.quantity)
        });
      });
    }
    
    return inventory;
  }
  
  /**
   * 获取库存状态标签
   */
  _getStockStatus(quantity) {
    if (quantity <= 0) return 'out_of_stock';
    if (quantity <= 5) return 'low_stock';
    if (quantity <= 20) return 'medium_stock';
    return 'in_stock';
  }
  
  /**
   * 检查低库存
   */
  async checkLowStock(threshold = 10) {
    const inventory = await this.getInventoryStatus();
    
    return inventory.filter(item => item.quantity <= threshold);
  }
  
  /**
   * 更新库存
   */
  async updateInventory(sku, quantity, platform = 'all') {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const platforms = platform === 'all' ? await adapter.listPlatforms() : [platform];
    const results = [];
    
    for (const p of platforms) {
      try {
        await adapter.platforms[p].updateInventory(sku, quantity);
        results.push({
          platform: p,
          success: true,
          sku,
          quantity
        });
      } catch (error) {
        results.push({
          platform: p,
          success: false,
          sku,
          quantity,
          error: error.message
        });
      }
    }
    
    return results;
  }
  
  /**
   * 批量更新库存
   */
  async bulkUpdateInventory(updates) {
    const results = {
      success: 0,
      failed: 0,
      details: []
    };
    
    for (const update of updates) {
      const result = await this.updateInventory(
        update.sku,
        update.quantity,
        update.platform
      );
      
      if (result.every(r => r.success)) {
        results.success++;
      } else {
        results.failed++;
      }
      
      results.details.push(...result);
    }
    
    return results;
  }
  
  /**
   * 设置库存预警
   */
  async setAlert(sku, threshold) {
    // TODO: 实现库存预警配置
    console.log(`Setting alert for ${sku}: threshold = ${threshold}`);
    return { success: true, sku, threshold };
  }
}

module.exports = { InventoryManager };
