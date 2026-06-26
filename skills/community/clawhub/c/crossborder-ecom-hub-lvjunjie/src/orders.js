/**
 * 订单管理器 - 统一订单管理
 * 聚合多平台订单，提供统一视图
 */

const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

class OrderManager {
  constructor() {
    this.platforms = {};
  }
  
  /**
   * 获取订单列表
   */
  async getOrders(filters = {}) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const allOrders = [];
    const platforms = filters.platform ? [filters.platform] : await adapter.listPlatforms();
    
    for (const platform of platforms) {
      try {
        const orders = await adapter.getOrders(platform, filters);
        
        // 应用过滤器
        let filtered = orders;
        
        if (filters.status) {
          filtered = filtered.filter(o => o.status === filters.status);
        }
        
        if (filters.dateFrom) {
          filtered = filtered.filter(o => new Date(o.createdAt) >= new Date(filters.dateFrom));
        }
        
        if (filters.dateTo) {
          filtered = filtered.filter(o => new Date(o.createdAt) <= new Date(filters.dateTo));
        }
        
        allOrders.push(...filtered);
      } catch (error) {
        console.error(chalk.red(`Failed to get orders from ${platform}:`), error.message);
      }
    }
    
    // 按创建时间排序
    return allOrders.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  }
  
  /**
   * 获取订单详情
   */
  async getOrder(orderId, platform) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    const orders = await adapter.getOrders(platform, { orderId });
    return orders.find(o => o.id === orderId);
  }
  
  /**
   * 更新订单状态
   */
  async updateOrderStatus(orderId, platform, status) {
    const { PlatformAdapter } = require('./platforms');
    const adapter = new PlatformAdapter();
    
    // TODO: 调用平台 API 更新订单状态
    console.log(`Updating order ${orderId} status to ${status} on ${platform}`);
    
    return {
      success: true,
      orderId,
      platform,
      status
    };
  }
  
  /**
   * 导出订单
   */
  async exportOrders(orders, format = 'csv', outputPath = null) {
    if (!outputPath) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      outputPath = path.join(process.cwd(), `orders_export_${timestamp}.${format}`);
    }
    
    if (format === 'csv') {
      return this._exportCSV(orders, outputPath);
    } else if (format === 'json') {
      return this._exportJSON(orders, outputPath);
    } else {
      throw new Error(`不支持的导出格式：${format}`);
    }
  }
  
  /**
   * 导出为 CSV
   */
  _exportCSV(orders, outputPath) {
    const headers = ['Order ID', 'Platform', 'Status', 'Amount', 'Currency', 'Customer', 'Created At'];
    
    const rows = orders.map(order => [
      order.id,
      order.platform,
      order.status,
      order.amount,
      order.currency || 'USD',
      order.customer?.name || '',
      new Date(order.createdAt).toLocaleString()
    ]);
    
    const csv = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');
    
    fs.writeFileSync(outputPath, csv, 'utf-8');
    return outputPath;
  }
  
  /**
   * 导出为 JSON
   */
  _exportJSON(orders, outputPath) {
    fs.writeFileSync(outputPath, JSON.stringify(orders, null, 2), 'utf-8');
    return outputPath;
  }
  
  /**
   * 统计订单
   */
  async getStatistics(filters = {}) {
    const orders = await this.getOrders(filters);
    
    const stats = {
      totalOrders: orders.length,
      totalAmount: 0,
      byPlatform: {},
      byStatus: {},
      averageOrderValue: 0
    };
    
    orders.forEach(order => {
      stats.totalAmount += parseFloat(order.amount || 0);
      
      stats.byPlatform[order.platform] = (stats.byPlatform[order.platform] || 0) + 1;
      stats.byStatus[order.status] = (stats.byStatus[order.status] || 0) + 1;
    });
    
    stats.averageOrderValue = stats.totalOrders > 0 
      ? stats.totalAmount / stats.totalOrders 
      : 0;
    
    return stats;
  }
}

module.exports = { OrderManager };
