#!/usr/bin/env node

/**
 * Auto-Heal Skill Installer
 * 一键安装和配置
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_PATH = path.join(process.env.HOME, '.openclaw', 'openclaw.json');

console.log('🦞 Auto-Heal Skill Installer');
console.log('============================\n');

// 检查 OpenClaw 是否安装
try {
  execSync('which openclaw', { stdio: 'ignore' });
} catch {
  console.error('❌ OpenClaw CLI not found. Please install OpenClaw first.');
  process.exit(1);
}

console.log('✅ OpenClaw CLI found');

// 读取现有配置
let config = {};
try {
  const configContent = fs.readFileSync(CONFIG_PATH, 'utf8');
  config = JSON.parse(configContent);
  console.log('✅ Config file loaded');
} catch {
  console.log('⚠️  Creating new config file');
  config = {};
}

// 添加技能配置
config.skills = config.skills || {};
config.skills['auto-heal'] = {
  enabled: true,
  checkInterval: 60,
  autoFix: true,
  memoryThreshold: 80,
  zombieSessionAge: 30,
  notifyChannel: '',
  logRetentionDays: 7
};

// 保存配置
try {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  console.log('✅ Config updated');
} catch (error) {
  console.error('❌ Failed to write config:', error.message);
  process.exit(1);
}

// 创建日志目录
const logDir = path.join(__dirname, 'logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
  console.log('✅ Log directory created');
}

console.log('\n🎉 Installation complete!');
console.log('\nUsage:');
console.log('  npm start          # Start continuous monitoring');
console.log('  npm run check      # Run single health check');
console.log('  npm run monitor    # Alias for start');
console.log('\nTo add to cron (recommended):');
console.log('  crontab -e');
console.log('  */5 * * * * cd ' + __dirname + ' && npm run check');
console.log('\nFor more info: cat SKILL.md');
