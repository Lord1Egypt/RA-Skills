/**
 * CrossBorder Ecom Hub - 主入口
 * 跨境电商多平台管理技能核心模块
 * 
 * @version 1.0.0
 * @author OpenClaw Skills
 */

// 导出核心模块
const { PlatformAdapter, PlatformManager } = require('./platforms');
const { OrderManager } = require('./orders');
const { PricingEngine } = require('./pricing');
const { InventoryManager } = require('./inventory');
const { ReportGenerator } = require('./reports');
const { FeishuSync } = require('./feishu');

module.exports = {
  // 平台管理
  PlatformAdapter,
  PlatformManager,
  
  // 订单管理
  OrderManager,
  
  // 智能定价
  PricingEngine,
  
  // 库存管理
  InventoryManager,
  
  // 数据报表
  ReportGenerator,
  
  // 飞书集成
  FeishuSync,
  
  // 版本号
  version: '1.0.0'
};
