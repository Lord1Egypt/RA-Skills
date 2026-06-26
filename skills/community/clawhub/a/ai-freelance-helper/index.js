#!/usr/bin/env node
/**
 * AI 接单助手 - 主入口
 * 
 * 功能：
 * - 项目分析
 * - 智能报价
 * - 项目管理
 * - 客户管理
 */

const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'config', 'freelance-config.yaml');
const PROJECTS_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'data', 'freelance-projects.json');
const CLIENTS_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'data', 'freelance-clients.json');

// 默认配置
const DEFAULT_CONFIG = {
  name: '接单达人',
  email: 'your@email.com',
  hourly_rate: 200,
  market_rates: {
    frontend: { min: 150, max: 300 },
    backend: { min: 200, max: 400 },
    mobile: { min: 200, max: 350 },
    design: { min: 100, max: 200 },
    fullstack: { min: 250, max: 500 }
  }
};

// 加载配置
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('加载配置失败:', e.message);
  }
  return DEFAULT_CONFIG;
}

// 保存配置
function saveConfig(config) {
  const dir = path.dirname(CONFIG_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

// 加载项目数据
function loadProjects() {
  try {
    if (fs.existsSync(PROJECTS_FILE)) {
      return JSON.parse(fs.readFileSync(PROJECTS_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('加载项目数据失败:', e.message);
  }
  return [];
}

// 保存项目数据
function saveProjects(projects) {
  const dir = path.dirname(PROJECTS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(PROJECTS_FILE, JSON.stringify(projects, null, 2));
}

// 加载客户数据
function loadClients() {
  try {
    if (fs.existsSync(CLIENTS_FILE)) {
      return JSON.parse(fs.readFileSync(CLIENTS_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('加载客户数据失败:', e.message);
  }
  return [];
}

// 保存客户数据
function saveClients(clients) {
  const dir = path.dirname(CLIENTS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(CLIENTS_FILE, JSON.stringify(clients, null, 2));
}

// 分析项目
function analyzeProject(requirements) {
  const config = loadConfig();
  
  // 识别项目类型
  const projectType = identifyProjectType(requirements);
  
  // 评估复杂度 (1-5)
  const complexity = assessComplexity(requirements);
  
  // 计算预估工时
  const estimatedHours = estimateHours(requirements, complexity);
  
  // 生成报价
  const quote = generateQuote(estimatedHours, config.hourly_rate, projectType, complexity);
  
  return {
    projectType,
    complexity,
    estimatedHours,
    quote,
    recommendations: generateRecommendations(requirements, complexity)
  };
}

// 识别项目类型
function identifyProjectType(requirements) {
  const text = requirements.toLowerCase();
  
  if (text.includes('小程序') || text.includes('app') || text.includes('ios') || text.includes('android')) {
    return 'mobile';
  } else if (text.includes('网站') || text.includes('web') || text.includes('h5')) {
    return 'frontend';
  } else if (text.includes('后台') || text.includes('api') || text.includes('服务端')) {
    return 'backend';
  } else if (text.includes('设计') || text.includes('ui') || text.includes('ux')) {
    return 'design';
  } else if (text.includes('全栈') || text.includes('fullstack')) {
    return 'fullstack';
  }
  
  return 'frontend'; // 默认
}

// 评估复杂度 (1-5)
function assessComplexity(requirements) {
  const text = requirements.toLowerCase();
  let score = 3; // 基础分数
  
  // 增加复杂度的因素
  if (text.includes('支付')) score += 1;
  if (text.includes('实时')) score += 1;
  if (text.includes('聊天')) score += 1;
  if (text.includes('推荐')) score += 1;
  if (text.includes('数据分析')) score += 1;
  if (text.includes('机器学习') || text.includes('ai')) score += 2;
  if (text.includes('区块链')) score += 2;
  if (text.includes('高并发')) score += 2;
  
  // 减少复杂度的因素
  if (text.includes('简单')) score -= 1;
  if (text.includes('基础')) score -= 1;
  if (text.includes('静态')) score -= 1;
  
  return Math.max(1, Math.min(5, score));
}

// 估算工时
function estimateHours(requirements, complexity) {
  const baseHours = {
    1: 8,
    2: 16,
    3: 32,
    4: 48,
    5: 80
  };
  
  return baseHours[complexity] || 32;
}

// 生成报价
function generateQuote(hours, hourlyRate, projectType, complexity) {
  const config = loadConfig();
  const marketRate = config.market_rates[projectType] || { min: 200, max: 400 };
  
  // 基础价格
  let basePrice = hours * hourlyRate;
  
  // 复杂度溢价
  const complexityMultiplier = 1 + (complexity - 3) * 0.2;
  basePrice *= complexityMultiplier;
  
  // 市场价校准
  const marketAdjustedPrice = Math.max(marketRate.min * hours, Math.min(marketRate.max * hours, basePrice));
  
  // 税费 (6%)
  const tax = marketAdjustedPrice * 0.06;
  
  // 总价
  const totalPrice = Math.round(marketAdjustedPrice + tax);
  
  return {
    basePrice: Math.round(basePrice),
    marketAdjustedPrice: Math.round(marketAdjustedPrice),
    tax: Math.round(tax),
    totalPrice,
    priceRange: {
      min: Math.round(marketRate.min * hours),
      max: Math.round(marketRate.max * hours)
    }
  };
}

// 生成建议
function generateRecommendations(requirements, complexity) {
  const recommendations = [];
  
  if (complexity >= 4) {
    recommendations.push('建议分阶段交付，降低风险');
    recommendations.push('考虑使用敏捷开发方法');
  }
  
  if (complexity <= 2) {
    recommendations.push('可以一次性交付');
    recommendations.push('适合快速迭代');
  }
  
  if (requirements.includes('支付')) {
    recommendations.push('需要特别注意支付安全');
  }
  
  if (requirements.includes('实时')) {
    recommendations.push('考虑使用 WebSocket 或类似技术');
  }
  
  recommendations.push('建议预留 20% 的缓冲时间');
  
  return recommendations;
}

// CLI 命令处理
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'analyze':
    const requirements = args.slice(1).join(' ');
    if (!requirements) {
      console.log('用法: ai-freelance-helper analyze "项目需求描述"');
      process.exit(1);
    }
    const result = analyzeProject(requirements);
    console.log(JSON.stringify(result, null, 2));
    break;
    
  case 'projects':
    const projects = loadProjects();
    console.log(JSON.stringify(projects, null, 2));
    break;
    
  case 'config':
    const config = loadConfig();
    console.log(JSON.stringify(config, null, 2));
    break;
    
  default:
    console.log(`
AI 接单助手

用法:
  ai-freelance-helper analyze "项目需求"  - 分析项目并生成报价
  ai-freelance-helper projects               - 显示所有项目
  ai-freelance-helper config                - 显示当前配置
    `);
}
