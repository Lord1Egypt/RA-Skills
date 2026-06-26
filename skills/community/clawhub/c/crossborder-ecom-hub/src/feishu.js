/**
 * 飞书多维表格同步模块
 * 实现与飞书 Bitable 的数据同步
 */

const chalk = require('chalk');

class FeishuSync {
  constructor() {
    this.appId = process.env.FEISHU_APP_ID;
    this.appSecret = process.env.FEISHU_APP_SECRET;
    this.bitableToken = process.env.FEISHU_BITABLE_TOKEN;
    this.accessToken = null;
    this.tokenExpire = null;
  }
  
  /**
   * 获取访问令牌
   */
  async getAccessToken() {
    if (this.accessToken && this.tokenExpire && new Date() < this.tokenExpire) {
      return this.accessToken;
    }
    
    const fetch = require('node-fetch');
    
    try {
      const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          app_id: this.appId,
          app_secret: this.appSecret
        })
      });
      
      const data = await response.json();
      
      if (data.code !== 0) {
        throw new Error(`飞书认证失败：${data.msg}`);
      }
      
      this.accessToken = data.tenant_access_token;
      this.tokenExpire = new Date(Date.now() + (data.expire - 300) * 1000);
      
      console.log(chalk.green('✓ 飞书认证成功'));
      return this.accessToken;
      
    } catch (error) {
      console.error(chalk.red('✗ 飞书认证失败:'), error.message);
      throw error;
    }
  }
  
  /**
   * 同步商品到飞书多维表格
   */
  async syncProducts(products) {
    if (!this.bitableToken) {
      console.log(chalk.yellow('⚠ 未配置飞书多维表格 Token，跳过同步'));
      return { success: false, reason: 'no_token' };
    }
    
    try {
      await this.getAccessToken();
      
      // 获取表格 ID
      const tableId = await this._getTableId('商品管理');
      
      // 批量创建记录
      const records = products.map(p => ({
        fields: {
          '商品 ID': p.id,
          'SKU': p.sku,
          '标题': p.title,
          '价格': parseFloat(p.price),
          '成本': parseFloat(p.cost),
          '库存': p.quantity,
          '平台': p.platform,
          '状态': p.status,
          '更新时间': p.updatedAt
        }
      }));
      
      // 分批创建（每批 500 条）
      const batchSize = 500;
      let created = 0;
      
      for (let i = 0; i < records.length; i += batchSize) {
        const batch = records.slice(i, i + batchSize);
        await this._batchCreateRecords(tableId, batch);
        created += batch.length;
      }
      
      console.log(chalk.green(`✓ 同步 ${created} 个商品到飞书多维表格`));
      return { success: true, created };
      
    } catch (error) {
      console.error(chalk.red('✗ 飞书商品同步失败:'), error.message);
      return { success: false, error: error.message };
    }
  }
  
  /**
   * 同步订单到飞书多维表格
   */
  async syncOrders(orders) {
    if (!this.bitableToken) {
      console.log(chalk.yellow('⚠ 未配置飞书多维表格 Token，跳过同步'));
      return { success: false, reason: 'no_token' };
    }
    
    try {
      await this.getAccessToken();
      
      const tableId = await this._getTableId('订单管理');
      
      const records = orders.map(o => ({
        fields: {
          '订单 ID': o.id,
          '订单号': o.orderNo,
          '平台': o.platform,
          '状态': o.status,
          '金额': parseFloat(o.amount),
          '客户': o.customer?.name,
          '创建时间': o.createdAt
        }
      }));
      
      const batchSize = 500;
      let created = 0;
      
      for (let i = 0; i < records.length; i += batchSize) {
        const batch = records.slice(i, i + batchSize);
        await this._batchCreateRecords(tableId, batch);
        created += batch.length;
      }
      
      console.log(chalk.green(`✓ 同步 ${created} 个订单到飞书多维表格`));
      return { success: true, created };
      
    } catch (error) {
      console.error(chalk.red('✗ 飞书订单同步失败:'), error.message);
      return { success: false, error: error.message };
    }
  }
  
  /**
   * 同步库存到飞书多维表格
   */
  async syncInventory(inventory) {
    if (!this.bitableToken) {
      console.log(chalk.yellow('⚠ 未配置飞书多维表格 Token，跳过同步'));
      return { success: false, reason: 'no_token' };
    }
    
    try {
      await this.getAccessToken();
      
      const tableId = await this._getTableId('库存管理');
      
      const records = inventory.map(i => ({
        fields: {
          'SKU': i.sku,
          '商品 ID': i.productId,
          '平台': i.platform,
          '库存数量': i.quantity,
          '可用库存': i.available,
          '状态': i.status,
          '更新时间': new Date().toISOString()
        }
      }));
      
      const batchSize = 500;
      let updated = 0;
      
      for (let i = 0; i < records.length; i += batchSize) {
        const batch = records.slice(i, i + batchSize);
        await this._batchCreateRecords(tableId, batch);
        updated += batch.length;
      }
      
      console.log(chalk.green(`✓ 同步 ${updated} 个库存记录到飞书多维表格`));
      return { success: true, updated };
      
    } catch (error) {
      console.error(chalk.red('✗ 飞书库存同步失败:'), error.message);
      return { success: false, error: error.message };
    }
  }
  
  /**
   * 同步定价建议到飞书多维表格
   */
  async syncPricingSuggestions(suggestions) {
    if (!this.bitableToken) {
      console.log(chalk.yellow('⚠ 未配置飞书多维表格 Token，跳过同步'));
      return { success: false, reason: 'no_token' };
    }
    
    try {
      await this.getAccessToken();
      
      const tableId = await this._getTableId('定价建议');
      
      const records = suggestions.map(s => ({
        fields: {
          '商品 ID': s.productId,
          'SKU': s.sku,
          '商品名称': s.productName,
          '当前价格': s.currentPrice,
          '建议价格': s.suggestedPrice,
          '调整幅度': s.change + '%',
          '建议': s.recommendation,
          '预期利润': s.expectedProfit,
          '利润率': s.margin + '%'
        }
      }));
      
      const batchSize = 500;
      let created = 0;
      
      for (let i = 0; i < records.length; i += batchSize) {
        const batch = records.slice(i, i + batchSize);
        await this._batchCreateRecords(tableId, batch);
        created += batch.length;
      }
      
      console.log(chalk.green(`✓ 同步 ${created} 条定价建议到飞书多维表格`));
      return { success: true, created };
      
    } catch (error) {
      console.error(chalk.red('✗ 飞书定价同步失败:'), error.message);
      return { success: false, error: error.message };
    }
  }
  
  /**
   * 同步报表到飞书多维表格
   */
  async syncReport(type, report) {
    if (!this.bitableToken) {
      console.log(chalk.yellow('⚠ 未配置飞书多维表格 Token，跳过同步'));
      return { success: false, reason: 'no_token' };
    }
    
    try {
      await this.getAccessToken();
      
      const tableId = await this._getTableId('数据报表');
      
      const record = {
        fields: {
          '报表类型': type,
          '周期': report.period,
          '生成时间': report.generatedAt,
          '数据': JSON.stringify(report)
        }
      };
      
      if (type === 'sales') {
        record.fields['总销售额'] = report.totalSales;
        record.fields['总订单数'] = report.totalOrders;
        record.fields['同比增长'] = report.growth + '%';
      } else if (type === 'inventory') {
        record.fields['总 SKU 数'] = report.totalSkus;
        record.fields['总库存量'] = report.totalQuantity;
        record.fields['低库存商品'] = report.lowStockCount;
      } else if (type === 'profit') {
        record.fields['总收入'] = report.revenue;
        record.fields['毛利润'] = report.grossProfit;
        record.fields['利润率'] = report.margin + '%';
      }
      
      await this._createRecord(tableId, record);
      
      console.log(chalk.green(`✓ 同步 ${type} 报表到飞书多维表格`));
      return { success: true };
      
    } catch (error) {
      console.error(chalk.red('✗ 飞书报表同步失败:'), error.message);
      return { success: false, error: error.message };
    }
  }
  
  /**
   * 获取表格 ID
   */
  async _getTableId(tableName) {
    const fetch = require('node-fetch');
    
    const response = await fetch(`https://open.feishu.cn/open-apis/bitable/v1/apps/${this.bitableToken}/tables`, {
      headers: { 'Authorization': `Bearer ${this.accessToken}` }
    });
    
    const data = await response.json();
    
    if (data.code !== 0) {
      throw new Error(`获取表格列表失败：${data.msg}`);
    }
    
    const table = data.data.items.find(t => t.name === tableName);
    
    if (!table) {
      // 创建新表格
      return await this._createTable(tableName);
    }
    
    return table.table_id;
  }
  
  /**
   * 创建表格
   */
  async _createTable(tableName) {
    const fetch = require('node-fetch');
    
    const response = await fetch(`https://open.feishu.cn/open-apis/bitable/v1/apps/${this.bitableToken}/tables`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        table: {
          name: tableName
        }
      })
    });
    
    const data = await response.json();
    
    if (data.code !== 0) {
      throw new Error(`创建表格失败：${data.msg}`);
    }
    
    return data.data.table_id;
  }
  
  /**
   * 批量创建记录
   */
  async _batchCreateRecords(tableId, records) {
    const fetch = require('node-fetch');
    
    const response = await fetch(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${this.bitableToken}/tables/${tableId}/records/batch_create`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ records })
      }
    );
    
    const data = await response.json();
    
    if (data.code !== 0) {
      throw new Error(`批量创建记录失败：${data.msg}`);
    }
    
    return data.data;
  }
  
  /**
   * 创建单条记录
   */
  async _createRecord(tableId, record) {
    const fetch = require('node-fetch');
    
    const response = await fetch(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${this.bitableToken}/tables/${tableId}/records`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fields: record.fields })
      }
    );
    
    const data = await response.json();
    
    if (data.code !== 0) {
      throw new Error(`创建记录失败：${data.msg}`);
    }
    
    return data.data;
  }
}

module.exports = { FeishuSync };
