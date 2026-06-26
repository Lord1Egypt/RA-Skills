#!/usr/bin/env node

/**
 * Autonomous Learning Cycle - 初始化脚本
 * 
 * 功能：
 * 1. 创建必要目录
 * 2. 初始化配置文件
 * 3. 初始化任务队列
 * 4. 初始化状态文件
 */

const fs = require('fs');
const path = require('path');

// 工作空间根目录
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.jvs/.openclaw/workspace');

// 需要创建的目录
const DIRS = [
  'tasks',
  'instincts',
  'memory/reflections',
  'auto-skills',
  'progress'
];

// 配置文件
const CONFIGS = {
  'tasks/queue.json': {
    version: '1.0.0',
    createdAt: new Date().toISOString(),
    currentCycle: 0,
    totalCyclesCompleted: 0,
    tasks: [],
    config: {
      cycleMinutes: 17,
      maxTasksPerCycle: 1,
      autoSpawnSubagents: true,
      logLevel: 'info'
    },
    stats: {
      totalTasks: 0,
      pendingTasks: 0,
      completedTasks: 0,
      blockedTasks: 0,
      averageCompletionTime: null
    }
  },
  'instincts/patterns.jsonl': '',
  'instincts/lessons.jsonl': '',
  'instincts/confidence.json': {
    weights: {
      baseScore: 0.5,
      successRate: 0.3,
      usageBonus: 0.15,
      timeDecay: 0.05,
      qualityBonus: 0.1
    },
    thresholds: {
      high: 0.7,
      medium: 0.4,
      low: 0.0
    },
    decay: {
      daysToHalf: 30,
      minDecay: 0.5
    },
    lastUpdated: null
  },
  'instincts/skill-evolution.jsonl': '',
  'autonomous/state.json': {
    currentCycle: 0,
    lastRunAt: null,
    currentTask: null,
    totalCyclesCompleted: 0
  }
};

/**
 * 创建目录
 */
function createDirectories() {
  console.log('\n📁 创建目录...\n');
  
  DIRS.forEach(dir => {
    const dirPath = path.join(WORKSPACE, dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
      console.log(`✅ 创建：${dir}`);
    } else {
      console.log(`⏭️  已存在：${dir}`);
    }
  });
}

/**
 * 初始化配置文件
 */
function initializeConfigs() {
  console.log('\n📝 初始化配置文件...\n');
  
  Object.entries(CONFIGS).forEach(([filePath, content]) => {
    const fullPath = path.join(WORKSPACE, filePath);
    const dir = path.dirname(fullPath);
    
    // 确保目录存在
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // 创建文件
    if (!fs.existsSync(fullPath)) {
      if (typeof content === 'object') {
        fs.writeFileSync(fullPath, JSON.stringify(content, null, 2));
      } else {
        fs.writeFileSync(fullPath, content);
      }
      console.log(`✅ 创建：${filePath}`);
    } else {
      console.log(`⏭️  已存在：${filePath}`);
    }
  });
}

/**
 * 主函数
 */
async function main() {
  console.log('\n🚀 Autonomous Learning Cycle - 初始化\n');
  console.log('═'.repeat(60));
  
  createDirectories();
  initializeConfigs();
  
  console.log('\n═'.repeat(60));
  console.log('\n✅ 初始化完成！\n');
  console.log('下一步:\n');
  console.log('1. 设置定时任务：node setup-cron.js');
  console.log('2. 启动系统：node start.js');
  console.log('3. 或手动执行：node engines/evolution-engine.js run\n');
}

// 运行主函数
main().catch(error => {
  console.error('❌ 初始化失败:', error.message);
  console.error(error.stack);
  process.exit(1);
});
