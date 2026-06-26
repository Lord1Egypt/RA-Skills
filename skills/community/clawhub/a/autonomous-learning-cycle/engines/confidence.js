#!/usr/bin/env node

/**
 * 自信度评估引擎 - 计算模式的可靠性评分
 * 
 * 功能：
 * 1. 计算单个模式的自信度
 * 2. 批量更新所有模式的自信度
 * 3. 标记高自信模式（可自动应用）
 * 4. 标记低自信模式（需人工验证）
 * 
 * 评分公式：
 * confidence = baseScore * successRate * usageBonus * timeDecay * qualityBonus
 * 
 * 用法：
 *   node confidence.js [command]
 *   
 * 命令：
 *   update      - 批量更新所有模式自信度（默认）
 *   show        - 显示所有模式及自信度
 *   pattern <id> - 显示单个模式详情
 */

const fs = require('fs');
const path = require('path');

// 工作空间根目录
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.jvs/.openclaw/workspace');
const PATTERNS_PATH = path.join(WORKSPACE, 'instincts/patterns.jsonl');
const CONFIDENCE_PATH = path.join(WORKSPACE, 'instincts/confidence.json');

/**
 * 加载所有模式
 */
function loadPatterns() {
  if (!fs.existsSync(PATTERNS_PATH)) {
    console.log('⚠️  模式文件不存在，创建空文件');
    fs.writeFileSync(PATTERNS_PATH, '');
    return [];
  }
  
  const content = fs.readFileSync(PATTERNS_PATH, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.trim());
  
  return lines.map(line => {
    try {
      return JSON.parse(line);
    } catch (error) {
      console.error('⚠️  解析模式失败:', error.message);
      return null;
    }
  }).filter(p => p !== null);
}

/**
 * 保存模式
 */
function savePatterns(patterns) {
  const content = patterns.map(p => JSON.stringify(p) + '\n').join('');
  fs.writeFileSync(PATTERNS_PATH, content);
}

/**
 * 加载自信度配置
 */
function loadConfidenceConfig() {
  const defaultConfig = {
    weights: {
      baseScore: 0.5,          // 基础分
      successRate: 0.3,        // 成功率权重
      usageBonus: 0.15,        // 使用次数权重
      timeDecay: 0.05,         // 时间衰减权重
      qualityBonus: 0.1        // 质量加成权重
    },
    thresholds: {
      high: 0.7,               // 高自信（自动应用）
      medium: 0.4,             // 中自信（手动应用）
      low: 0.0                 // 低自信（待验证）
    },
    decay: {
      daysToHalf: 30,          // 半衰期（天）
      minDecay: 0.5            // 最小衰减系数
    },
    lastUpdated: null
  };
  
  try {
    if (fs.existsSync(CONFIDENCE_PATH)) {
      const config = JSON.parse(fs.readFileSync(CONFIDENCE_PATH, 'utf-8'));
      return { ...defaultConfig, ...config };
    }
  } catch (error) {
    console.error('⚠️  加载自信度配置失败，使用默认配置');
  }
  
  return defaultConfig;
}

/**
 * 保存自信度配置
 */
function saveConfidenceConfig(config) {
  config.lastUpdated = new Date().toISOString();
  fs.writeFileSync(CONFIDENCE_PATH, JSON.stringify(config, null, 2));
}

/**
 * 计算自信度
 * 
 * 公式：
 * confidence = baseScore * successRate * usageBonus * timeDecay * qualityBonus
 */
function calculateConfidence(pattern, config) {
  const { weights, decay } = config;
  
  // 1. 基础分（0.5）
  const baseScore = weights.baseScore;
  
  // 2. 成功率（成功次数 / 总使用次数）
  const totalUses = (pattern.successCount || 0) + (pattern.failCount || 0);
  const successRate = totalUses > 0 
    ? (pattern.successCount || 0) / totalUses 
    : 0.5; // 未使用时默认 0.5
  
  // 3. 使用次数加成（越多越可靠，上限 1.5）
  const usageBonus = 1 + Math.min(0.5, (pattern.usedCount || 0) / 20);
  
  // 4. 时间衰减（越近越可靠，半衰期 30 天）
  const createdAt = new Date(pattern.createdAt);
  const daysSinceCreation = (Date.now() - createdAt.getTime()) / (1000 * 60 * 60 * 24);
  const timeDecay = Math.max(
    decay.minDecay,
    Math.pow(0.5, daysSinceCreation / decay.daysToHalf)
  );
  
  // 5. 质量加成（步骤详细、有洞察、有标签）
  let qualityBonus = 1.0;
  if (pattern.steps && pattern.steps.length > 3) qualityBonus += 0.1;
  if (pattern.keyInsights && pattern.keyInsights.length > 0) qualityBonus += 0.1;
  if (pattern.tags && pattern.tags.length > 2) qualityBonus += 0.05;
  
  // 计算最终自信度
  const confidence = baseScore * 
                    (0.5 + successRate * 0.5) *  // 成功率贡献
                    usageBonus * 
                    timeDecay * 
                    qualityBonus;
  
  // 限制在 0-1 范围
  return Math.min(1.0, Math.max(0.0, confidence));
}

/**
 * 获取自信度等级
 */
function getConfidenceLevel(confidence, config) {
  if (confidence >= config.thresholds.high) {
    return {
      level: 'high',
      label: '高自信',
      color: '🟢',
      autoApply: true,
      description: '可自动应用到新任务'
    };
  } else if (confidence >= config.thresholds.medium) {
    return {
      level: 'medium',
      label: '中自信',
      color: '🟡',
      autoApply: false,
      description: '可手动应用，建议人工确认'
    };
  } else {
    return {
      level: 'low',
      label: '低自信',
      color: '🔴',
      autoApply: false,
      description: '待验证，不建议应用'
    };
  }
}

/**
 * 批量更新自信度
 */
function updateAllConfidence() {
  console.log('\n🧠 开始批量更新自信度...\n');
  
  const config = loadConfidenceConfig();
  const patterns = loadPatterns();
  
  if (patterns.length === 0) {
    console.log('⚠️  暂无模式需要更新');
    return;
  }
  
  console.log(`📊 共 ${patterns.length} 个模式\n`);
  
  let highCount = 0;
  let mediumCount = 0;
  let lowCount = 0;
  
  patterns.forEach(pattern => {
    const oldConfidence = pattern.confidence || 0.5;
    const newConfidence = calculateConfidence(pattern, config);
    const level = getConfidenceLevel(newConfidence, config);
    
    pattern.confidence = parseFloat(newConfidence.toFixed(3));
    pattern.confidenceLevel = level.level;
    pattern.lastCalculatedAt = new Date().toISOString();
    
    // 统计
    if (level.level === 'high') highCount++;
    else if (level.level === 'medium') mediumCount++;
    else lowCount++;
    
    // 显示变化
    const change = newConfidence - oldConfidence;
    const changeStr = change >= 0 ? `+${change.toFixed(3)}` : change.toFixed(3);
    
    console.log(`${level.color} ${pattern.id}`);
    console.log(`   标题：${pattern.title}`);
    console.log(`   自信度：${oldConfidence.toFixed(3)} → ${newConfidence.toFixed(3)} (${changeStr})`);
    console.log(`   等级：${level.label} - ${level.description}`);
    console.log(`   成功率：${(pattern.successCount || 0)}/${(pattern.successCount || 0) + (pattern.failCount || 0)}`);
    console.log(`   使用次数：${pattern.usedCount || 0}`);
    console.log('');
  });
  
  // 保存更新
  savePatterns(patterns);
  saveConfidenceConfig(config);
  
  // 汇总
  console.log('═'.repeat(60));
  console.log('📊 自信度分布:');
  console.log(`   🟢 高自信：${highCount} 个（可自动应用）`);
  console.log(`   🟡 中自信：${mediumCount} 个（手动应用）`);
  console.log(`   🔴 低自信：${lowCount} 个（待验证）`);
  console.log('═'.repeat(60));
  console.log('\n✅ 自信度更新完成\n');
}

/**
 * 显示所有模式
 */
function showAllPatterns() {
  const patterns = loadPatterns();
  const config = loadConfidenceConfig();
  
  if (patterns.length === 0) {
    console.log('\n⚠️  暂无模式\n');
    return;
  }
  
  console.log('\n📊 所有模式列表:\n');
  console.log('═'.repeat(100));
  
  patterns.sort((a, b) => b.confidence - a.confidence);
  
  patterns.forEach((pattern, index) => {
    const level = getConfidenceLevel(pattern.confidence, config);
    console.log(`${index + 1}. ${level.color} [${pattern.id}]`);
    console.log(`   ${pattern.title}`);
    console.log(`   自信度：${pattern.confidence.toFixed(3)} (${level.label})`);
    console.log(`   类型：${pattern.type} | 分类：${pattern.category} | 使用：${pattern.usedCount || 0}次`);
    console.log('');
  });
  
  console.log('═'.repeat(100));
  console.log(`总计：${patterns.length} 个模式\n`);
}

/**
 * 显示单个模式详情
 */
function showPatternDetail(patternId) {
  const patterns = loadPatterns();
  const config = loadConfidenceConfig();
  
  const pattern = patterns.find(p => p.id === patternId);
  
  if (!pattern) {
    console.error(`❌ 模式不存在：${patternId}`);
    return;
  }
  
  const level = getConfidenceLevel(pattern.confidence, config);
  
  console.log('\n📊 模式详情:\n');
  console.log('═'.repeat(80));
  console.log(`ID: ${pattern.id}`);
  console.log(`标题：${pattern.title}`);
  console.log(`描述：${pattern.description}`);
  console.log('');
  console.log(`自信度：${pattern.confidence.toFixed(3)} (${level.color} ${level.label})`);
  console.log(`等级：${level.description}`);
  console.log('');
  console.log(`类型：${pattern.type}`);
  console.log(`分类：${pattern.category}`);
  console.log(`标签：${(pattern.tags || []).join(', ') || '无'}`);
  console.log('');
  console.log(`成功率：${(pattern.successCount || 0)}/${(pattern.successCount || 0) + (pattern.failCount || 0)}`);
  console.log(`使用次数：${pattern.usedCount || 0}`);
  console.log(`创建时间：${pattern.createdAt}`);
  console.log(`最后计算：${pattern.lastCalculatedAt || '从未'}`);
  console.log('');
  
  if (pattern.steps && pattern.steps.length > 0) {
    console.log('步骤:');
    pattern.steps.forEach((step, i) => {
      console.log(`  ${i + 1}. ${step}`);
    });
    console.log('');
  }
  
  if (pattern.keyInsights && pattern.keyInsights.length > 0) {
    console.log('关键洞察:');
    pattern.keyInsights.forEach(insight => {
      console.log(`  • ${insight}`);
    });
    console.log('');
  }
  
  console.log('═'.repeat(80));
  console.log('');
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'update';
  
  switch (command) {
    case 'update':
      updateAllConfidence();
      break;
    case 'show':
      showAllPatterns();
      break;
    case 'pattern':
      if (!args[1]) {
        console.error('❌ 请提供模式 ID');
        console.log('用法：node confidence.js pattern <pattern-id>');
        process.exit(1);
      }
      showPatternDetail(args[1]);
      break;
    default:
      console.log('用法：node confidence.js [command]');
      console.log('\n命令:');
      console.log('  update           - 批量更新所有模式自信度（默认）');
      console.log('  show             - 显示所有模式及自信度');
      console.log('  pattern <id>     - 显示单个模式详情');
  }
}

// 运行主函数
main().catch(error => {
  console.error('❌ 自信度引擎错误:', error.message);
  console.error(error.stack);
  process.exit(1);
});
