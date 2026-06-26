"use strict";

/**
 * Financial Analyst Skill — 入口文件
 *
 * 金融分析师技能包：综合趋势判断、周期定位与风险控制的投资分析。
 * 适用于市场方向判断、行业/公司分析、基金/ETF分析、理财产品分析、
 * 资产配置、交易策略评估、持仓复盘、杠杆与仓位管理。
 *
 * 框架：周期定位 → 本质与驱动 → 条件与约束 → 得失与风险 → 先后与节奏 → 博弈与对手
 *
 * @module financial-analyst-skill
 */

const router = require("./router");

/**
 * 分析给定的投资问题
 * @param {string} message - 用户输入
 * @returns {object} 路由分析结果
 */
function analyze(message) {
  return router.route(message);
}

/**
 * 获取所有支持的分析子领域
 * @returns {object} SUB_DOMAINS 映射
 */
function getDomains() {
  return { ...router.SUB_DOMAINS };
}

/**
 * 获取所有子领域的关键词库
 * @returns {object} SUB_DOMAIN_KEYWORDS 映射
 */
function getDomainKeywords() {
  return Object.fromEntries(
    Object.entries(router.SUB_DOMAIN_KEYWORDS).map(([key, val]) => [key, [...val]])
  );
}

module.exports = {
  analyze,
  getDomains,
  getDomainKeywords,
  route: router.route,
  SUB_DOMAINS: router.SUB_DOMAINS,
  SUB_DOMAIN_KEYWORDS: router.SUB_DOMAIN_KEYWORDS,
};
