/**
 * Agent-SBTI: 配置应用器
 * 
 * 负责将 Agent 配置应用到 SOUL.md
 * 包含备份、回滚、变更提醒功能
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const BACKUP_DIR = path.join(WORKSPACE, 'backup', 'agent-sbti');
const SOUL_PATH = path.join(WORKSPACE, 'SOUL.md');

// 确保备份目录存在
function ensureBackupDir() {
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }
}

// 获取当前时间戳
function getTimestamp() {
  const now = new Date();
  return now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
}

// 备份 SOUL.md
function backupSoul() {
  ensureBackupDir();
  
  if (!fs.existsSync(SOUL_PATH)) {
    console.log('SOUL.md 不存在，跳过备份');
    return null;
  }
  
  const timestamp = getTimestamp();
  const backupPath = path.join(BACKUP_DIR, `${timestamp}`);
  
  fs.mkdirSync(backupPath, { recursive: true });
  fs.copyFileSync(SOUL_PATH, path.join(backupPath, 'SOUL.md'));
  
  console.log(`✅ 已备份到: ${backupPath}`);
  return backupPath;
}

// 读取当前 SOUL.md
function readSoul() {
  if (!fs.existsSync(SOUL_PATH)) {
    return null;
  }
  return fs.readFileSync(SOUL_PATH, 'utf8');
}

// 写入 SOUL.md
function writeSoul(content) {
  fs.writeFileSync(SOUL_PATH, content, 'utf8');
  console.log(`✅ 已更新: ${SOUL_PATH}`);
}

// 应用配置到 SOUL.md
function applyConfig(soulConfig, dryRun = false) {
  const currentSoul = readSoul();
  
  if (!currentSoul) {
    console.error('SOUL.md 不存在，无法应用配置');
    return { success: false, error: 'SOUL.md not found' };
  }
  
  // 检查是否已有 Agent 性格配置区块
  const SBTI_START = '<!-- SBTI-AGENT-START -->';
  const SBTI_END = '<!-- SBTI-AGENT-END -->';
  
  let newSoul;
  
  if (currentSoul.includes(SBTI_START) && currentSoul.includes(SBTI_END)) {
    // 替换现有区块
    const regex = new RegExp(`${SBTI_START}[\\s\\S]*?${SBTI_END}`, 'm');
    newSoul = currentSoul.replace(regex, soulConfig.trim());
  } else {
    // 追加到文件末尾
    newSoul = currentSoul.trim() + '\n\n' + soulConfig.trim();
  }
  
  if (dryRun) {
    console.log('\n📋 预览变更:\n');
    console.log(soulConfig);
    return { success: true, dryRun: true };
  }
  
  // 先备份
  const backupPath = backupSoul();
  
  // 写入
  writeSoul(newSoul);
  
  // 返回变更摘要
  return {
    success: true,
    backupPath,
    changes: extractChanges(currentSoul, newSoul)
  };
}

// 提取变更内容
function extractChanges(oldSoul, newSoul) {
  const changes = [];
  
  // 简单提取变更的配置项
  const configRegex = /\*\*(\S+)\*\*:?\s*(.+)/g;
  let match;
  
  while ((match = configRegex.exec(newSoul)) !== null) {
    const key = match[1];
    const newValue = match[2].trim();
    
    // 尝试在旧版本中查找对应值
    const oldRegex = new RegExp(`\\*\\*${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\*\\*:?\\s*(.+)`);
    const oldMatch = oldRegex.exec(oldSoul);
    const oldValue = oldMatch ? oldMatch[1].trim() : '(无)';
    
    if (oldValue !== newValue) {
      changes.push({
        field: key,
        before: oldValue,
        after: newValue
      });
    }
  }
  
  return changes;
}

// 列出可用备份
function listBackups() {
  ensureBackupDir();
  
  const dirs = fs.readdirSync(BACKUP_DIR)
    .filter(f => fs.statSync(path.join(BACKUP_DIR, f)).isDirectory())
    .sort()
    .reverse();
  
  if (dirs.length === 0) {
    console.log('暂无备份');
    return [];
  }
  
  console.log('\n📁 可用备份:\n');
  dirs.slice(0, 5).forEach((dir, i) => {
    console.log(`  ${i + 1}. ${dir}`);
  });
  
  return dirs.slice(0, 5).map(dir => path.join(BACKUP_DIR, dir));
}

// 回滚到指定备份
function rollback(backupIndex = 0) {
  const backups = listBackups();
  
  if (backups.length === 0) {
    return { success: false, error: 'No backups found' };
  }
  
  const backupPath = backups[backupIndex];
  const backupSoulPath = path.join(backupPath, 'SOUL.md');
  
  if (!fs.existsSync(backupSoulPath)) {
    return { success: false, error: 'Backup file not found' };
  }
  
  // 先备份当前版本
  backupSoul();
  
  // 恢复备份
  const backupContent = fs.readFileSync(backupSoulPath, 'utf8');
  writeSoul(backupContent);
  
  return {
    success: true,
    restoredFrom: backupPath
  };
}

// 生成变更摘要文本
function formatChanges(changes) {
  if (!changes || changes.length === 0) {
    return '  (无变更)';
  }
  
  return changes.map(c => `  - ${c.field}: ${c.before} → ${c.after}`).join('\n');
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === 'list') {
    listBackups();
  } else if (args[0] === 'rollback' && args[1]) {
    const idx = parseInt(args[1]) - 1;
    const result = rollback(idx);
    console.log(result);
  } else if (args[0] === 'preview') {
    const { generateSoulConfig } = require('./agent_config');
    const config = JSON.parse(args[1] || '{}');
    console.log(generateSoulConfig(config, 'SAME'));
  } else {
    console.log('用法:');
    console.log('  node apply.js list              # 列出备份');
    console.log('  node apply.js rollback <n>    # 回滚到第 n 个备份');
    console.log('  node apply.js preview <json>  # 预览配置');
  }
}

module.exports = {
  backupSoul,
  applyConfig,
  listBackups,
  rollback,
  formatChanges,
  readSoul,
  writeSoul,
  SOUL_PATH,
  BACKUP_DIR
};
