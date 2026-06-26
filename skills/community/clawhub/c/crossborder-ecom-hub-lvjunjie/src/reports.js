/**
 * 报表生成器 - 数据分析报表
 * 销售、库存、利润、平台对比等多维度分析
 */

const chalk = require('chalk');
const dayjs = require('dayjs');

class ReportGenerator {
  constructor() {
    this.cache = new Map();
  }
  
  /**
   * 生成销售报表
   */
  async generateSalesReport(options = {}) {
    const { OrderManager } = require('./orders');
    const orderManager = new OrderManager();
    
    const period = options.period || 'weekly';
    const dateRange = this._getDateRange(period);
    
    const orders = await orderManager.getOrders({
      dateFrom: dateRange.from,
      dateTo: dateRange.to
    });
    
    // 计算销售统计
    const totalSales = orders.reduce((sum, o) => sum + parseFloat(o.amount || 0), 0);
    const totalOrders = orders.length;
    const averageOrderValue = totalOrders > 0 ? totalSales / totalOrders : 0;
    
    // 按平台分组
    const byPlatform = {};
    orders.forEach(order => {
      if (!byPlatform[order.platform]) {
        byPlatform[order.platform] = { sales: 0, orders: 0 };
      }
      byPlatform[order.platform].sales += parseFloat(order.amount || 0);
      byPlatform[order.platform].orders += 1;
    });
    
    // 销售趋势
    const trend = this._calculateTrend(orders, period);
    
    // 同比增长（模拟）
    const growth = (Math.random() * 20 - 5).toFixed(1);
    
    return {
      period,
      dateRange,
      totalSales,
      totalOrders,
      averageOrderValue,
      growth: parseFloat(growth),
      byPlatform: Object.entries(byPlatform).map(([platform, data]) => ({
        platform,
        sales: data.sales,
        orders: data.orders
      })),
      trend,
      generatedAt: new Date().toISOString()
    };
  }
  
  /**
   * 生成库存报表
   */
  async generateInventoryReport(options = {}) {
    const { InventoryManager } = require('./inventory');
    const inventoryManager = new InventoryManager();
    
    const inventory = await inventoryManager.getInventoryStatus();
    
    const totalSkus = inventory.length;
    const totalQuantity = inventory.reduce((sum, i) => sum + i.quantity, 0);
    
    // 库存状态统计
    const lowStockCount = inventory.filter(i => i.quantity <= 10).length;
    const outOfStockCount = inventory.filter(i => i.quantity <= 0).length;
    const overstockCount = inventory.filter(i => i.quantity > 100).length;
    const slowMoving = inventory.filter(i => i.quantity > 50 && i.status === 'in_stock').length;
    
    // 库存周转率（模拟）
    const turnoverRate = (Math.random() * 5 + 3).toFixed(2);
    
    return {
      period: options.period || 'current',
      totalSkus,
      totalQuantity,
      turnoverRate: parseFloat(turnoverRate),
      slowMoving,
      lowStockCount,
      outOfStockCount,
      overstockCount,
      byPlatform: this._groupByPlatform(inventory),
      generatedAt: new Date().toISOString()
    };
  }
  
  /**
   * 生成利润分析报表
   */
  async generateProfitReport(options = {}) {
    const { OrderManager } = require('./orders');
    const orderManager = new OrderManager();
    
    const period = options.period || 'weekly';
    const dateRange = this._getDateRange(period);
    
    const orders = await orderManager.getOrders({
      dateFrom: dateRange.from,
      dateTo: dateRange.to
    });
    
    // 计算收入和成本
    const revenue = orders.reduce((sum, o) => sum + parseFloat(o.amount || 0), 0);
    const cost = revenue * 0.6; // 假设成本占 60%
    const grossProfit = revenue - cost;
    const margin = (grossProfit / revenue * 100);
    
    // 按平台分组
    const byPlatform = {};
    orders.forEach(order => {
      if (!byPlatform[order.platform]) {
        byPlatform[order.platform] = { revenue: 0, cost: 0, orders: 0 };
      }
      byPlatform[order.platform].revenue += parseFloat(order.amount || 0);
      byPlatform[order.platform].orders += 1;
    });
    
    Object.keys(byPlatform).forEach(platform => {
      byPlatform[platform].cost = byPlatform[platform].revenue * 0.6;
      byPlatform[platform].profit = byPlatform[platform].revenue - byPlatform[platform].cost;
      byPlatform[platform].margin = (byPlatform[platform].profit / byPlatform[platform].revenue * 100);
    });
    
    return {
      period,
      dateRange,
      revenue,
      cost,
      grossProfit,
      margin: parseFloat(margin.toFixed(1)),
      byPlatform: Object.entries(byPlatform).map(([platform, data]) => ({
        platform,
        revenue: data.revenue,
        cost: data.cost,
        profit: data.profit,
        margin: parseFloat(data.margin.toFixed(1)),
        orders: data.orders
      })),
      generatedAt: new Date().toISOString()
    };
  }
  
  /**
   * 生成平台对比报表
   */
  async generatePlatformComparison(options = {}) {
    const { OrderManager } = require('./orders');
    const orderManager = new OrderManager();
    
    const period = options.period || 'weekly';
    const dateRange = this._getDateRange(period);
    
    const orders = await orderManager.getOrders({
      dateFrom: dateRange.from,
      dateTo: dateRange.to
    });
    
    // 按平台统计
    const platformStats = {};
    orders.forEach(order => {
      if (!platformStats[order.platform]) {
        platformStats[order.platform] = {
          sales: 0,
          orders: 0,
          profit: 0,
          ratings: []
        };
      }
      platformStats[order.platform].sales += parseFloat(order.amount || 0);
      platformStats[order.platform].orders += 1;
      platformStats[order.platform].profit += parseFloat(order.amount || 0) * 0.4; // 40% 利润率
      platformStats[order.platform].ratings.push(4 + Math.random()); // 模拟评分
    });
    
    const platforms = Object.entries(platformStats).map(([name, data]) => ({
      name,
      sales: data.sales,
      orders: data.orders,
      profit: data.profit,
      margin: parseFloat((data.profit / data.sales * 100).toFixed(1)),
      rating: parseFloat((data.ratings.reduce((a, b) => a + b, 0) / data.ratings.length).toFixed(1))
    }));
    
    // 找出最佳表现
    const bestBySales = platforms.reduce((best, p) => p.sales > best.sales ? p : best, platforms[0]);
    const bestByMargin = platforms.reduce((best, p) => p.margin > best.margin ? p : best, platforms[0]);
    const bestByOrders = platforms.reduce((best, p) => p.orders > best.orders ? p : best, platforms[0]);
    
    return {
      period,
      dateRange,
      platforms,
      bestBySales,
      bestByMargin,
      bestByOrders,
      generatedAt: new Date().toISOString()
    };
  }
  
  /**
   * 导出报表
   */
  async exportReport(report, format = 'json', outputPath = null) {
    const fs = require('fs');
    const path = require('path');
    
    if (!outputPath) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      outputPath = path.join(process.cwd(), `report_${timestamp}.${format}`);
    }
    
    if (format === 'json') {
      fs.writeFileSync(outputPath, JSON.stringify(report, null, 2), 'utf-8');
    } else if (format === 'csv') {
      // TODO: 实现 CSV 导出
      fs.writeFileSync(outputPath, JSON.stringify(report), 'utf-8');
    }
    
    return outputPath;
  }
  
  /**
   * 获取日期范围
   */
  _getDateRange(period) {
    const now = dayjs();
    
    switch (period) {
      case 'daily':
        return {
          from: now.startOf('day').toISOString(),
          to: now.endOf('day').toISOString()
        };
      case 'weekly':
        return {
          from: now.startOf('week').toISOString(),
          to: now.endOf('week').toISOString()
        };
      case 'monthly':
        return {
          from: now.startOf('month').toISOString(),
          to: now.endOf('month').toISOString()
        };
      default:
        return {
          from: now.subtract(7, 'day').toISOString(),
          to: now.toISOString()
        };
    }
  }
  
  /**
   * 计算销售趋势
   */
  _calculateTrend(orders, period) {
    const trend = [];
    const grouped = {};
    
    orders.forEach(order => {
      const date = dayjs(order.createdAt).format('YYYY-MM-DD');
      if (!grouped[date]) {
        grouped[date] = 0;
      }
      grouped[date] += parseFloat(order.amount || 0);
    });
    
    Object.entries(grouped)
      .sort(([a], [b]) => a.localeCompare(b))
      .forEach(([date, sales]) => {
        trend.push({ date, sales });
      });
    
    return trend;
  }
  
  /**
   * 按平台分组
   */
  _groupByPlatform(items) {
    const grouped = {};
    items.forEach(item => {
      if (!grouped[item.platform]) {
        grouped[item.platform] = { quantity: 0, skus: 0 };
      }
      grouped[item.platform].quantity += item.quantity;
      grouped[item.platform].skus += 1;
    });
    return Object.entries(grouped).map(([platform, data]) => ({
      platform,
      quantity: data.quantity,
      skus: data.skus
    }));
  }
}

module.exports = { ReportGenerator };
