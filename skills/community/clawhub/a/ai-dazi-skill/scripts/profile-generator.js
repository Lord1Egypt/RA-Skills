/**
 * 用户画像生成器 - AI搭子匹配平台
 *
 * 基于 token-collector 存储的数据，纯本地生成多维用户画像。
 * 不访问 session 日志、不访问 home 目录、不联网。
 *
 * 用法：
 *   node scripts/profile-generator.js generate   # 生成/更新用户画像
 *   node scripts/profile-generator.js view        # 查看当前画像
 */

const fs = require('fs');
const path = require('path');
const { loadAllDailyData, ensureDataDirs, DATA_DIR, DAILY_DIR, PROFILES_DIR } = require('./token-collector');

// ── 玩家等级定义 ──────────────────────────────────────────────

const PLAYER_LEVELS = {
  PIONEER: { name: 'Pioneer', label: '先锋玩家', description: '深度使用AI，探索前沿功能', minScore: 80 },
  BUILDER: { name: 'Builder', label: '建造者', description: '善于用AI构建实际项目', minScore: 50 },
  EXPLORER: { name: 'Explorer', label: '探索者', description: '广泛尝试各种AI工具', minScore: 25 },
  OBSERVER: { name: 'Observer', label: '观察者', description: '正在了解和学习AI', minScore: 0 }
};

// ── 活跃度评分算法（满分100）──────────────────────────────

function calculateActivityScore(allData) {
  if (allData.length === 0) return 1;
  let score = 0;

  // 维度1: 总 Token 量 (最多25分)
  const totalTokens = allData.reduce((sum, d) => sum + (d.tokenUsage?.total || 0), 0);
  if (totalTokens >= 5000000) score += 25;
  else if (totalTokens >= 1000000) score += 20;
  else if (totalTokens >= 500000) score += 15;
  else if (totalTokens >= 100000) score += 10;
  else if (totalTokens >= 10000) score += 5;
  else score += 2;

  // 维度2: 活跃天数占比 (最多20分)
  const activeDays = allData.length;
  const firstDate = new Date(allData[0].date);
  const lastDate = new Date(allData[allData.length - 1].date);
  const spanDays = Math.max(1, Math.round((lastDate - firstDate) / 86400000) + 1);
  score += Math.round((activeDays / spanDays) * 20);

  // 维度3: 日均消息量 (最多20分)
  const totalMessages = allData.reduce((sum, d) => sum + (d.messageCount || 0), 0);
  const avgDaily = totalMessages / activeDays;
  if (avgDaily >= 50) score += 20;
  else if (avgDaily >= 20) score += 15;
  else if (avgDaily >= 10) score += 10;
  else if (avgDaily >= 5) score += 5;
  else score += 2;

  // 维度4: 模型多样性 (最多15分)
  const allModels = new Set();
  for (const d of allData) Object.keys(d.modelFrequency || {}).forEach(m => allModels.add(m));
  score += Math.min(allModels.size * 3, 15);

  // 维度5: 工具调用多样性 (最多10分)
  const allTools = new Set();
  for (const d of allData) Object.keys(d.toolCallFrequency || {}).forEach(t => allTools.add(t));
  score += Math.min(allTools.size, 10);

  // 维度6: 技能安装数量 (最多10分)
  const latestData = allData[allData.length - 1];
  const skillCount = latestData.installedSkills?.length || 0;
  if (skillCount >= 50) score += 10;
  else if (skillCount >= 20) score += 8;
  else if (skillCount >= 10) score += 6;
  else if (skillCount >= 5) score += 4;
  else score += 2;

  return Math.max(1, Math.min(100, score));
}

function determinePlayerLevel(score) {
  for (const level of Object.values(PLAYER_LEVELS)) {
    if (score >= level.minScore) return level;
  }
  return PLAYER_LEVELS.OBSERVER;
}

// ── 技能标签推断 ──────────────────────────────────────────────

function inferSkillTags(allData) {
  const tags = new Set();

  const toolTotals = {};
  for (const d of allData) {
    for (const [tool, count] of Object.entries(d.toolCallFrequency || {})) {
      toolTotals[tool] = (toolTotals[tool] || 0) + count;
    }
  }

  const toolTagMap = {
    'coding': ['exec', 'write', 'read', 'edit'],
    'writing': ['draft', 'blog', 'article', 'document'],
    'data-analysis': ['data', 'csv', 'sql', 'chart'],
    'research': ['search', 'web_search', 'web_fetch'],
    'communication': ['message', 'feishu_doc', 'feishu_chat'],
    'memory': ['memory_search', 'memory_get'],
    'automation': ['exec', 'process', 'sessions_spawn']
  };

  const toolNames = Object.keys(toolTotals).map(t => t.toLowerCase());
  for (const [tag, keywords] of Object.entries(toolTagMap)) {
    if (keywords.some(k => toolNames.some(t => t.includes(k)))) tags.add(tag);
  }

  // 基于 installedSkills
  const latestData = allData[allData.length - 1] || {};
  const skills = (latestData.installedSkills || []).map(s => s.toLowerCase());
  const skillTagMap = {
    'coding': ['coding', 'code', 'dev', 'github'],
    'writing': ['write', 'writing', 'blog', 'summarize', 'prd'],
    'data-analysis': ['data', 'excel', 'analytics'],
    'communication': ['slack', 'discord', 'himalaya', 'feishu'],
    'media': ['music', 'video', 'tts'],
    'research': ['oracle', 'blogwatcher']
  };

  for (const [tag, keywords] of Object.entries(skillTagMap)) {
    if (keywords.some(k => skills.some(s => s.includes(k)))) tags.add(tag);
  }

  if (tags.size === 0) tags.add('general');
  return Array.from(tags);
}

// ── AI 使用风格推断 ──────────────────────────────────────────────

function inferAIStyle(allData) {
  const toolTotals = {};
  let totalToolCalls = 0;
  for (const d of allData) {
    for (const [tool, count] of Object.entries(d.toolCallFrequency || {})) {
      toolTotals[tool] = (toolTotals[tool] || 0) + count;
      totalToolCalls += count;
    }
  }
  const toolVariety = Object.keys(toolTotals).length;

  const allModels = new Set();
  for (const d of allData) Object.keys(d.modelFrequency || {}).forEach(m => allModels.add(m));

  const allProviders = new Set();
  for (const d of allData) Object.keys(d.providerFrequency || {}).forEach(p => allProviders.add(p));

  const totalMessages = allData.reduce((sum, d) => sum + (d.messageCount || 0), 0);
  const avgDaily = totalMessages / Math.max(1, allData.length);

  if (totalToolCalls >= 50 && toolVariety >= 8) return 'power-tools';
  if (allModels.size >= 4 || allProviders.size >= 3) return 'explorer';
  if (avgDaily >= 20 && toolVariety < 5) return 'conversational';
  return 'efficiency';
}

// ── 匹配标签生成 ──────────────────────────────────────────────

function generateMatchTags(allData, playerLevel, skillTags, aiStyle) {
  const tags = [playerLevel.name, ...skillTags, aiStyle];

  // 活跃时段
  const hourTotals = {};
  for (const d of allData) {
    for (const [h, count] of Object.entries(d.activeHours || {})) {
      hourTotals[h] = (hourTotals[h] || 0) + count;
    }
  }
  const peakHour = Object.entries(hourTotals).sort((a, b) => b[1] - a[1])[0];
  if (peakHour) {
    const h = parseInt(peakHour[0]);
    if (h >= 0 && h < 6) tags.push('night-owl');
    else if (h >= 6 && h < 12) tags.push('early-bird');
    else if (h >= 12 && h < 18) tags.push('afternoon');
    else tags.push('evening');
  }

  return [...new Set(tags)];
}

// ── 用户总结 ──────────────────────────────────────────────

function generateSummary(profile, stats) {
  const { playerLevel, skillTags, aiStyle, activityScore } = profile;
  const scoreDesc = activityScore >= 80 ? 'very high' : activityScore >= 50 ? 'high' : activityScore >= 25 ? 'moderate' : 'beginner';

  return `${playerLevel.label} (${playerLevel.name}) player. ` +
    `${stats.activeDays} active days, ${stats.totalTokens.toLocaleString()} tokens consumed. ` +
    `Skills: ${skillTags.join(', ')}. Style: ${aiStyle}. ` +
    `Activity: ${scoreDesc} (${activityScore}/100), ` +
    `using ${stats.modelCount} models and ${stats.skillCount} skills.`;
}

// ── 主流程 ──────────────────────────────────────────────

function generate() {
  ensureDataDirs();
  console.log('Generating user profile...\n');

  const allData = loadAllDailyData();
  if (allData.length === 0) {
    console.log('No data found. Ask your AI assistant to collect usage data first.');
    return;
  }

  const activityScore = calculateActivityScore(allData);
  const playerLevel = determinePlayerLevel(activityScore);
  const skillTags = inferSkillTags(allData);
  const aiStyle = inferAIStyle(allData);

  const totalTokens = allData.reduce((s, d) => s + (d.tokenUsage?.total || 0), 0);
  const totalMessages = allData.reduce((s, d) => s + (d.messageCount || 0), 0);
  const totalSessions = allData.reduce((s, d) => s + (d.sessionCount || 0), 0);
  const modelFreqAgg = {};
  const toolFreqAgg = {};
  const providerFreqAgg = {};

  for (const d of allData) {
    for (const [m, c] of Object.entries(d.modelFrequency || {})) modelFreqAgg[m] = (modelFreqAgg[m] || 0) + c;
    for (const [t, c] of Object.entries(d.toolCallFrequency || {})) toolFreqAgg[t] = (toolFreqAgg[t] || 0) + c;
    for (const [p, c] of Object.entries(d.providerFrequency || {})) providerFreqAgg[p] = (providerFreqAgg[p] || 0) + c;
  }

  const latestData = allData[allData.length - 1];
  const stats = {
    totalTokens, totalMessages,
    activeDays: allData.length,
    modelCount: Object.keys(modelFreqAgg).length,
    skillCount: latestData.installedSkills?.length || 0
  };

  const profile = { playerLevel, skillTags, aiStyle, activityScore, matchTags: [], summary: '' };
  profile.matchTags = generateMatchTags(allData, playerLevel, skillTags, aiStyle);
  profile.summary = generateSummary(profile, stats);

  const output = {
    version: '2.0.0',
    generatedAt: new Date().toISOString(),
    dataRange: { from: allData[0].date, to: allData[allData.length - 1].date, days: allData.length },
    playerLevel: playerLevel.name,
    playerLevelLabel: playerLevel.label,
    playerLevelDescription: playerLevel.description,
    activityScore,
    skillTags,
    aiStyle,
    matchTags: profile.matchTags,
    summary: profile.summary,
    rawMetrics: {
      totalTokens, totalMessages, totalSessions,
      installedSkills: latestData.installedSkills || [],
      modelFrequency: modelFreqAgg,
      providerFrequency: providerFreqAgg,
      toolFrequency: toolFreqAgg
    }
  };

  const outputPath = path.join(PROFILES_DIR, 'latest.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');

  const historyPath = path.join(PROFILES_DIR, `profile-${new Date().toISOString().slice(0, 10)}.json`);
  fs.writeFileSync(historyPath, JSON.stringify(output, null, 2), 'utf-8');

  console.log(JSON.stringify(output, null, 2));
  console.log(`\nProfile saved to: ${outputPath}`);
  return output;
}

function view() {
  ensureDataDirs();
  const profilePath = path.join(PROFILES_DIR, 'latest.json');
  if (!fs.existsSync(profilePath)) {
    console.log('No profile found. Run generate first.');
    return;
  }
  const profile = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));
  console.log(JSON.stringify(profile, null, 2));
}

// ── CLI ──────────────────────────────────────────────

if (require.main === module) {
  const command = process.argv[2];
  switch (command) {
    case 'generate': generate(); break;
    case 'view': view(); break;
    default:
      console.log('Usage:');
      console.log('  node scripts/profile-generator.js generate');
      console.log('  node scripts/profile-generator.js view');
  }
}

module.exports = { generate, view };
