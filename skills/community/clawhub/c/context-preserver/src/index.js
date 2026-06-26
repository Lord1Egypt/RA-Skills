#!/usr/bin/env node

/**
 * Context Preserver - 上下文保持器
 * 自动快照、按需恢复、版本管理和上下文导出
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 配置
const CONFIG = {
  dataDir: path.join(os.homedir(), '.context-preserver'),
  snapshotsDir: path.join(os.homedir(), '.context-preserver', 'snapshots'),
  configFile: path.join(os.homedir(), '.context-preserver', 'config.json'),
  maxSnapshots: 50, // 最大快照数量
  autoSnapshotInterval: 30 * 60 * 1000 // 30分钟自动快照
};

// 初始化目录
function init() {
  if (!fs.existsSync(CONFIG.dataDir)) {
    fs.mkdirSync(CONFIG.dataDir, { recursive: true });
  }
  if (!fs.existsSync(CONFIG.snapshotsDir)) {
    fs.mkdirSync(CONFIG.snapshotsDir, { recursive: true });
  }
  if (!fs.existsSync(CONFIG.configFile)) {
    fs.writeFileSync(CONFIG.configFile, JSON.stringify({
      autoSnapshot: true,
      maxSnapshots: 50,
      autoSnapshotInterval: 30 * 60 * 1000,
      lastSnapshot: null
    }, null, 2));
  }
}

// 获取配置
function getConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG.configFile, 'utf8'));
  } catch (e) {
    return { autoSnapshot: true, maxSnapshots: 50 };
  }
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG.configFile, JSON.stringify(config, null, 2));
}

// 生成快照ID
function generateSnapshotId() {
  const now = new Date();
  return `snapshot_${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}${String(now.getSeconds()).padStart(2, '0')}_${Date.now()}`;
}

// 创建快照
function createSnapshot(name, tags = []) {
  init();
  
  const snapshotId = generateSnapshotId();
  const timestamp = new Date().toISOString();
  
  // 收集当前上下文信息
  const context = {
    id: snapshotId,
    name: name || `Snapshot ${timestamp}`,
    timestamp: timestamp,
    tags: tags,
    cwd: process.cwd(),
    env: {
      PATH: process.env.PATH,
      HOME: process.env.HOME,
      USER: process.env.USER,
      SHELL: process.env.SHELL
    },
    node: {
      version: process.version,
      platform: process.platform,
      arch: process.arch
    },
    session: {
      pid: process.pid,
      ppid: process.ppid
    }
  };
  
  // 保存快照
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  fs.writeFileSync(snapshotPath, JSON.stringify(context, null, 2));
  
  // 更新配置
  const config = getConfig();
  config.lastSnapshot = snapshotId;
  saveConfig(config);
  
  // 清理旧快照
  cleanupOldSnapshots();
  
  console.log(`✅ 快照已创建: ${snapshotId}`);
  console.log(`   名称: ${context.name}`);
  console.log(`   时间: ${timestamp}`);
  console.log(`   标签: ${tags.join(', ') || '无'}`);
  
  return snapshotId;
}

// 列出所有快照
function listSnapshots() {
  init();
  
  const files = fs.readdirSync(CONFIG.snapshotsDir)
    .filter(f => f.endsWith('.json'))
    .map(f => {
      const filepath = path.join(CONFIG.snapshotsDir, f);
      const stat = fs.statSync(filepath);
      const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      return {
        id: data.id,
        name: data.name,
        timestamp: data.timestamp,
        tags: data.tags,
        size: stat.size
      };
    })
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
  if (files.length === 0) {
    console.log('📭 暂无快照');
    return [];
  }
  
  console.log(`📸 共有 ${files.length} 个快照:\n`);
  files.forEach((snapshot, index) => {
    const date = new Date(snapshot.timestamp);
    const dateStr = date.toLocaleString('zh-CN');
    const tagsStr = snapshot.tags.length > 0 ? ` [${snapshot.tags.join(', ')}]` : '';
    console.log(`  ${index + 1}. ${snapshot.id}`);
    console.log(`     名称: ${snapshot.name}${tagsStr}`);
    console.log(`     时间: ${dateStr}`);
    console.log(`     大小: ${(snapshot.size / 1024).toFixed(2)} KB`);
    console.log('');
  });
  
  return files;
}

// 恢复快照
function restoreSnapshot(snapshotId) {
  init();
  
  // 支持通过序号恢复
  if (/^\d+$/.test(snapshotId)) {
    const snapshots = fs.readdirSync(CONFIG.snapshotsDir)
      .filter(f => f.endsWith('.json'))
      .sort((a, b) => {
        const statA = fs.statSync(path.join(CONFIG.snapshotsDir, a));
        const statB = fs.statSync(path.join(CONFIG.snapshotsDir, b));
        return statB.mtime - statA.mtime;
      });
    
    const index = parseInt(snapshotId) - 1;
    if (index < 0 || index >= snapshots.length) {
      console.error(`❌ 无效的快照序号: ${snapshotId}`);
      return false;
    }
    snapshotId = snapshots[index].replace('.json', '');
  }
  
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  
  if (!fs.existsSync(snapshotPath)) {
    console.error(`❌ 快照不存在: ${snapshotId}`);
    return false;
  }
  
  const context = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  
  console.log('✅ 快照恢复成功:\n');
  console.log(`  ID: ${context.id}`);
  console.log(`  名称: ${context.name}`);
  console.log(`  时间: ${context.timestamp}`);
  console.log(`  工作目录: ${context.cwd}`);
  console.log(`  标签: ${context.tags.join(', ') || '无'}`);
  console.log(`  Node版本: ${context.node.version}`);
  console.log(`  平台: ${context.node.platform} ${context.node.arch}`);
  
  return context;
}

// 删除快照
function deleteSnapshot(snapshotId) {
  init();
  
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  
  if (!fs.existsSync(snapshotPath)) {
    console.error(`❌ 快照不存在: ${snapshotId}`);
    return false;
  }
  
  fs.unlinkSync(snapshotPath);
  console.log(`✅ 快照已删除: ${snapshotId}`);
  return true;
}

// 清理旧快照
function cleanupOldSnapshots() {
  const config = getConfig();
  const files = fs.readdirSync(CONFIG.snapshotsDir)
    .filter(f => f.endsWith('.json'))
    .map(f => ({
      name: f,
      path: path.join(CONFIG.snapshotsDir, f),
      mtime: fs.statSync(path.join(CONFIG.snapshotsDir, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime);
  
  if (files.length > config.maxSnapshots) {
    const toDelete = files.slice(config.maxSnapshots);
    toDelete.forEach(f => {
      fs.unlinkSync(f.path);
      console.log(`🗑️  已清理旧快照: ${f.name}`);
    });
  }
}

// 导出快照
function exportSnapshot(snapshotId, exportPath) {
  init();
  
  // 支持导出所有快照
  if (snapshotId === 'all') {
    const exportDir = exportPath || `context-preserver-export-${Date.now()}`;
    const fullExportPath = path.resolve(exportDir);
    
    if (!fs.existsSync(fullExportPath)) {
      fs.mkdirSync(fullExportPath, { recursive: true });
    }
    
    const files = fs.readdirSync(CONFIG.snapshotsDir).filter(f => f.endsWith('.json'));
    files.forEach(f => {
      const src = path.join(CONFIG.snapshotsDir, f);
      const dest = path.join(fullExportPath, f);
      fs.copyFileSync(src, dest);
    });
    
    // 导出配置
    fs.copyFileSync(CONFIG.configFile, path.join(fullExportPath, 'config.json'));
    
    console.log(`✅ 所有快照已导出到: ${fullExportPath}`);
    console.log(`   共导出 ${files.length} 个快照`);
    return fullExportPath;
  }
  
  // 支持通过序号导出
  if (/^\d+$/.test(snapshotId)) {
    const snapshots = fs.readdirSync(CONFIG.snapshotsDir)
      .filter(f => f.endsWith('.json'))
      .sort((a, b) => {
        const statA = fs.statSync(path.join(CONFIG.snapshotsDir, a));
        const statB = fs.statSync(path.join(CONFIG.snapshotsDir, b));
        return statB.mtime - statA.mtime;
      });
    
    const index = parseInt(snapshotId) - 1;
    if (index < 0 || index >= snapshots.length) {
      console.error(`❌ 无效的快照序号: ${snapshotId}`);
      return false;
    }
    snapshotId = snapshots[index].replace('.json', '');
  }
  
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  
  if (!fs.existsSync(snapshotPath)) {
    console.error(`❌ 快照不存在: ${snapshotId}`);
    return false;
  }
  
  const finalExportPath = exportPath || `${snapshotId}.json`;
  fs.copyFileSync(snapshotPath, path.resolve(finalExportPath));
  
  console.log(`✅ 快照已导出: ${finalExportPath}`);
  return finalExportPath;
}

// 导入快照
function importSnapshot(importPath) {
  init();
  
  const fullPath = path.resolve(importPath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`❌ 文件不存在: ${importPath}`);
    return false;
  }
  
  // 如果是目录，导入所有快照
  const stat = fs.statSync(fullPath);
  if (stat.isDirectory()) {
    const files = fs.readdirSync(fullPath).filter(f => f.endsWith('.json') && f !== 'config.json');
    let imported = 0;
    
    files.forEach(f => {
      const src = path.join(fullPath, f);
      const dest = path.join(CONFIG.snapshotsDir, f);
      if (!fs.existsSync(dest)) {
        fs.copyFileSync(src, dest);
        imported++;
      }
    });
    
    console.log(`✅ 已导入 ${imported} 个快照`);
    return true;
  }
  
  // 导入单个快照
  let filename = path.basename(fullPath);
  
  // 尝试读取文件获取正确的快照ID
  try {
    const data = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
    if (data.id) {
      filename = `${data.id}.json`;
    }
  } catch (e) {
    // 如果解析失败，使用原文件名
  }
  
  const dest = path.join(CONFIG.snapshotsDir, filename);
  
  if (fs.existsSync(dest)) {
    console.error(`❌ 快照已存在: ${filename}`);
    return false;
  }
  
  fs.copyFileSync(fullPath, dest);
  console.log(`✅ 快照已导入: ${filename}`);
  return true;
}

// 显示快照详情
function showSnapshot(snapshotId) {
  init();
  
  // 支持通过序号查看
  if (/^\d+$/.test(snapshotId)) {
    const snapshots = fs.readdirSync(CONFIG.snapshotsDir)
      .filter(f => f.endsWith('.json'))
      .sort((a, b) => {
        const statA = fs.statSync(path.join(CONFIG.snapshotsDir, a));
        const statB = fs.statSync(path.join(CONFIG.snapshotsDir, b));
        return statB.mtime - statA.mtime;
      });
    
    const index = parseInt(snapshotId) - 1;
    if (index < 0 || index >= snapshots.length) {
      console.error(`❌ 无效的快照序号: ${snapshotId}`);
      return false;
    }
    snapshotId = snapshots[index].replace('.json', '');
  }
  
  const snapshotPath = path.join(CONFIG.snapshotsDir, `${snapshotId}.json`);
  
  if (!fs.existsSync(snapshotPath)) {
    console.error(`❌ 快照不存在: ${snapshotId}`);
    return false;
  }
  
  const context = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  
  console.log('📸 快照详情:\n');
  console.log(JSON.stringify(context, null, 2));
  
  return context;
}

// 显示帮助
function showHelp() {
  console.log(`
Context Preserver - 上下文保持器

用法: context-preserver <command> [options]

命令:
  snapshot [name] [--tags tag1,tag2]  创建新快照
  list                                列出所有快照
  restore <id|number>                 恢复快照
  delete <id|number>                  删除快照
  show <id|number>                    显示快照详情
  export <id|number|all> [path]       导出快照
  import <path>                       导入快照
  config                              显示配置
  auto [on|off]                       开启/关闭自动快照
  clean                               清理旧快照
  help                                显示帮助

示例:
  context-preserver snapshot "项目初始化" --tags project,init
  context-preserver list
  context-preserver restore 1
  context-preserver export all ./backups
  context-preserver import ./backups

快捷命令:
  ctxp s "名称"     创建快照
  ctxp ls           列出快照
  ctxp r 1          恢复快照 #1
`);
}

// 显示配置
function showConfig() {
  init();
  const config = getConfig();
  
  console.log('⚙️  当前配置:\n');
  console.log(`  数据目录: ${CONFIG.dataDir}`);
  console.log(`  快照目录: ${CONFIG.snapshotsDir}`);
  console.log(`  自动快照: ${config.autoSnapshot ? '开启' : '关闭'}`);
  console.log(`  最大快照数: ${config.maxSnapshots}`);
  console.log(`  自动快照间隔: ${config.autoSnapshotInterval / 60000} 分钟`);
  console.log(`  上次快照: ${config.lastSnapshot || '无'}`);
}

// 设置自动快照
function setAutoSnapshot(enabled) {
  init();
  const config = getConfig();
  config.autoSnapshot = enabled;
  saveConfig(config);
  console.log(`✅ 自动快照已${enabled ? '开启' : '关闭'}`);
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'snapshot':
    case 's':
      const name = args[1] || '';
      const tagsIndex = args.indexOf('--tags');
      const tags = tagsIndex > -1 ? args[tagsIndex + 1].split(',') : [];
      createSnapshot(name, tags);
      break;
      
    case 'list':
    case 'ls':
      listSnapshots();
      break;
      
    case 'restore':
    case 'r':
      if (!args[1]) {
        console.error('❌ 请指定快照ID或序号');
        process.exit(1);
      }
      restoreSnapshot(args[1]);
      break;
      
    case 'delete':
    case 'rm':
      if (!args[1]) {
        console.error('❌ 请指定快照ID或序号');
        process.exit(1);
      }
      deleteSnapshot(args[1]);
      break;
      
    case 'show':
      if (!args[1]) {
        console.error('❌ 请指定快照ID或序号');
        process.exit(1);
      }
      showSnapshot(args[1]);
      break;
      
    case 'export':
    case 'e':
      if (!args[1]) {
        console.error('❌ 请指定快照ID、序号或 "all"');
        process.exit(1);
      }
      exportSnapshot(args[1], args[2]);
      break;
      
    case 'import':
    case 'i':
      if (!args[1]) {
        console.error('❌ 请指定导入路径');
        process.exit(1);
      }
      importSnapshot(args[1]);
      break;
      
    case 'config':
    case 'c':
      showConfig();
      break;
      
    case 'auto':
      if (args[1] === 'on') {
        setAutoSnapshot(true);
      } else if (args[1] === 'off') {
        setAutoSnapshot(false);
      } else {
        const config = getConfig();
        console.log(`自动快照当前状态: ${config.autoSnapshot ? '开启' : '关闭'}`);
        console.log('用法: context-preserver auto [on|off]');
      }
      break;
      
    case 'clean':
      cleanupOldSnapshots();
      console.log('✅ 旧快照清理完成');
      break;
      
    case 'help':
    case '-h':
    case '--help':
      showHelp();
      break;
      
    default:
      showHelp();
      break;
  }
}

// 主入口
if (require.main === module) {
  init();
  parseArgs();
}

// 导出API
module.exports = {
  init,
  createSnapshot,
  listSnapshots,
  restoreSnapshot,
  deleteSnapshot,
  exportSnapshot,
  importSnapshot,
  showSnapshot,
  cleanupOldSnapshots,
  getConfig,
  saveConfig,
  CONFIG
};
