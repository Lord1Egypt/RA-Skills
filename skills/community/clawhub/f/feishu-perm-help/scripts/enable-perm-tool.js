#!/usr/bin/env node

/**
 * 启用飞书权限管理工具
 * 
 * 功能：
 * 1. 读取 openclaw.json 配置文件
 * 2. 为所有飞书账号启用 perm 工具
 * 3. 重启 Gateway 使配置生效
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_PATH = path.join(require('os').homedir(), '.openclaw/openclaw.json');

console.log('🦞 OpenClaw 飞书权限工具启用脚本\n');

// 读取配置文件
console.log('📖 读取配置文件...');
let config;
try {
  const configContent = fs.readFileSync(CONFIG_PATH, 'utf8');
  config = JSON.parse(configContent);
  console.log('✅ 配置文件读取成功');
} catch (error) {
  console.error('❌ 读取配置文件失败:', error.message);
  console.error('文件路径:', CONFIG_PATH);
  process.exit(1);
}

// 检查是否有 feishu 配置
if (!config.channels || !config.channels.feishu) {
  console.error('❌ 未找到飞书配置，请先配置飞书插件');
  process.exit(1);
}

console.log('✅ 飞书配置已找到');

// 启用顶层 tools.perm
if (!config.channels.feishu.tools) {
  config.channels.feishu.tools = {};
}
config.channels.feishu.tools.perm = true;
console.log('✅ 已启用 channels.feishu.tools.perm');

// 为所有账号启用 perm 工具
const accounts = config.channels.feishu.accounts || {};
const accountNames = Object.keys(accounts);

if (accountNames.length === 0) {
  console.log('⚠️  未配置飞书账号');
} else {
  console.log(`📋 找到 ${accountNames.length} 个飞书账号：${accountNames.join(', ')}`);
  
  for (const accountName of accountNames) {
    const account = accounts[accountName];
    if (!account.tools) {
      account.tools = {};
    }
    account.tools.perm = true;
    console.log(`✅ 已为 ${accountName} 账号启用 perm 工具`);
  }
}

// 保存配置文件
console.log('\n💾 保存配置文件...');
try {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + '\n', 'utf8');
  console.log('✅ 配置文件保存成功');
} catch (error) {
  console.error('❌ 保存配置文件失败:', error.message);
  process.exit(1);
}

// 重启 Gateway
console.log('\n🔄 重启 Gateway...');
try {
  execSync('openclaw gateway restart', { stdio: 'inherit' });
  console.log('✅ Gateway 重启成功');
} catch (error) {
  console.error('❌ Gateway 重启失败:', error.message);
  console.log('\n⚠️  请手动执行：openclaw gateway restart');
}

// 验证
console.log('\n🔍 验证配置...');
setTimeout(() => {
  try {
    const status = execSync('openclaw gateway status', { encoding: 'utf8' });
    if (status.includes('feishu_perm: Registered feishu_perm tool')) {
      console.log('✅ feishu_perm 工具已成功注册');
      console.log('\n🎉 配置完成！现在可以在飞书里使用权限管理功能了！');
      console.log('\n📝 使用示例：');
      console.log('  - "给这个表格添加编辑权限 https://xxx.feishu.cn/base/XXX"');
      console.log('  - "查看这个表格的协作者 https://xxx.feishu.cn/base/XXX"');
      console.log('  - "移除 XX 的编辑权限 https://xxx.feishu.cn/base/XXX"');
    } else {
      console.log('⚠️  未检测到 feishu_perm 工具，可能需要等待几秒后重试');
    }
  } catch (error) {
    console.log('⚠️  验证失败，请手动执行：openclaw gateway status');
  }
}, 3000);
