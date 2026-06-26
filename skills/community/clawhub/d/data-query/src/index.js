/**
 * index.js — 技能主入口
 *
 * 导出所有核心模块，供主 agent 或外部调用方使用
 */

// 核心模块
const config = require('./core/config.js');
const errors = require('./core/errors.js');
const validator = require('./core/validator.js');
const dialect = require('./core/dialect.js');

// 安全模块
const encryptSql = require('./security/encryptSql.js');

// 验证模块
const { verify, batchVerifyHtml } = require('./verify/index.js');

// 生成模块
const generatePage = require('./generate/page.js');
const chartSpecSchema = require('./generate/chartSpecSchema.js');

// 模板模块
const templateManager = require('./templates/index.js');

// 导出所有模块
module.exports = {
  // 核心模块
  config,
  errors,
  validator,
  dialect,
  
  // 安全模块
  encryptSql,
  
  // 验证模块
  verify,
  batchVerifyHtml,
  
  // 生成模块
  generatePage,
  chartSpecSchema,
  
  // 模板模块
  templateManager
};