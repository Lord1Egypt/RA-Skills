#!/usr/bin/env node

/**
 * 权限配置生成器 - 检测系统并生成权限配置选项
 */

const os = require('os');
const fs = require('fs');
const path = require('path');

/**
 * 检测当前系统类型
 */
function detectSystem() {
  const platform = os.platform();
  const homedir = os.homedir();
  
  if (platform === 'win32') {
    return { type: 'windows', homedir };
  } else if (platform === 'darwin') {
    return { type: 'macos', homedir };
  } else {
    return { type: 'linux', homedir };
  }
}

/**
 * 生成权限配置选项
 */
function generateOptions(system) {
  const options = [
    {
      id: 1,
      name: '限制级',
      desc: '只读写常用用户目录',
      config: {
        security: 'allowlist',
        allowedPaths: getRestrictedPaths(system)
      }
    },
    {
      id: 2,
      name: '中等',
      desc: '读写用户目录和部分系统目录',
      config: {
        security: 'allowlist',
        allowedPaths: getMediumPaths(system)
      }
    },
    {
      id: 3,
      name: '宽松',
      desc: '读写整个系统（谨慎使用）',
      config: {
        security: 'allowlist',
        allowedPaths: getLoosePaths(system)
      }
    }
  ];
  
  return options;
}

/**
 * 获取限制级路径
 */
function getRestrictedPaths(system) {
  const home = system.homedir;
  
  if (system.type === 'windows') {
    return [
      `${home}/**`,
      `${home.replace(/\\/g, '/')}/**`,
      'C:/Users/**',
      'C:/Temp/**',
      'D:/**'
    ];
  } else if (system.type === 'macos') {
    return [
      `${home}/**`,
      '/tmp/**',
      '/private/**'
    ];
  } else {
    // Linux
    return [
      `${home}/**`,
      '/tmp/**',
      '/home/**'
    ];
  }
}

/**
 * 获取中等权限路径
 */
function getMediumPaths(system) {
  const home = system.homedir;
  
  if (system.type === 'windows') {
    return [
      'C:/Users/**',
      'C:/Temp/**',
      'D:/**',
      'E:/**'
    ];
  } else if (system.type === 'macos') {
    return [
      '/Users/**',
      '/tmp/**',
      '/private/**',
      '/opt/**'
    ];
  } else {
    // Linux
    return [
      '/home/**',
      '/tmp/**',
      '/opt/**',
      '/var/**',
      '/srv/**'
    ];
  }
}

/**
 * 获取宽松权限路径
 */
function getLoosePaths(system) {
  if (system.type === 'windows') {
    return ['/**'];
  } else {
    return ['/**'];
  }
}

/**
 * 获取当前配置
 */
function getCurrentConfig() {
  const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
  
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config;
    } catch (e) {
      return null;
    }
  }
  return null;
}

/**
 * 显示选项
 */
function showOptions() {
  const system = detectSystem();
  const options = generateOptions(system);
  
  console.log('\n=== 权限配置选项 ===\n');
  console.log(`检测到系统: ${system.type.toUpperCase()} (${system.homedir})`);
  console.log('\n请选择权限级别:\n');
  
  options.forEach(opt => {
    console.log(`  ${opt.id}. ${opt.name}`);
    console.log(`     ${opt.desc}`);
    console.log(`     路径: ${opt.config.allowedPaths.join(', ')}`);
    console.log('');
  });
  
  return options;
}

/**
 * 应用配置
 */
function applyConfig(optionId) {
  const system = detectSystem();
  const options = generateOptions(system);
  const selected = options.find(o => o.id === optionId);
  
  if (!selected) {
    return { success: false, error: '无效的选项' };
  }
  
  const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
  let config = { skills: { entries: {} } };
  
  // 读取现有配置
  if (fs.existsSync(configPath)) {
    try {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    } catch (e) {
      // 使用默认配置
    }
  }
  
  // 确保结构存在
  if (!config.skills) config.skills = {};
  if (!config.skills.entries) config.skills.entries = {};
  
  // 添加技能权限配置
  config.skills.entries['feishu-temp-file'] = {
    security: selected.config.security,
    allowedPaths: selected.config.allowedPaths
  };
  
  // 写入配置
  const dir = path.dirname(configPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  return {
    success: true,
    message: `已配置 "${selected.name}" 权限`,
    config: selected.config
  };
}

module.exports = {
  detectSystem,
  generateOptions,
  getCurrentConfig,
  showOptions,
  applyConfig
};

// 如果直接运行
if (require.main === module) {
  const options = showOptions();
  
  const args = process.argv.slice(2);
  if (args.length > 0) {
    const optionId = parseInt(args[0]);
    const result = applyConfig(optionId);
    console.log('\n=== 配置结果 ===\n');
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log('\n用法:');
    console.log('  node perm-config.js          # 显示选项');
    console.log('  node perm-config.js <选项>  # 应用配置');
    console.log('  例如: node perm-config.js 2  # 应用中等权限\n');
  }
}
