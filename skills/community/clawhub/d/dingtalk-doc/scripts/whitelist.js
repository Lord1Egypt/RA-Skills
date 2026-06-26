#!/usr/bin/env node

/**
 * 白名单权限校验工具
 * 
 * 功能：
 * - 加载白名单配置
 * - 校验路径是否在白名单内
 * - 支持前缀匹配
 */

const fs = require('fs');
const path = require('path');

/**
 * 获取技能目录路径
 */
function getSkillDir() {
  return path.resolve(__dirname, '..');
}

/**
 * 加载白名单配置
 * 
 * @returns {Object} 配置对象
 */
function loadConfig() {
  const configPath = path.join(getSkillDir(), 'config', 'whitelist.json');
  
  if (!fs.existsSync(configPath)) {
    return {
      workspaces: [],
      _missingConfig: true,
      _configPath: configPath
    };
  }
  
  const configContent = fs.readFileSync(configPath, 'utf8');
  const config = JSON.parse(configContent);
  
  return {
    ...config,
    _missingConfig: false,
    _configPath: configPath
  };
}

/**
 * 规范化路径
 */
function normalizePath(p) {
  if (!p) return '/';
  if (!p.startsWith('/')) p = '/' + p;
  if (p.endsWith('/') && p.length > 1) p = p.slice(0, -1);
  return p;
}

/**
 * 检查路径是否在白名单内
 */
function checkPath(targetPath, whitelist) {
  const normalizedTarget = normalizePath(targetPath);
  
  if (!whitelist || whitelist.length === 0) {
    return {
      allowed: false,
      reason: '白名单为空，不允许写入操作'
    };
  }
  
  for (const rule of whitelist) {
    const normalizedRule = normalizePath(rule);
    
    // 特殊规则 "/" 匹配所有路径
    if (normalizedRule === '/') {
      return {
        allowed: true,
        matchedRule: rule
      };
    }
    
    // 精确匹配或前缀匹配（子目录）
    if (normalizedTarget === normalizedRule || normalizedTarget.startsWith(normalizedRule + '/')) {
      return {
        allowed: true,
        matchedRule: rule
      };
    }
  }
  
  return {
    allowed: false,
    reason: `路径 "${targetPath}" 不在白名单内`
  };
}

/**
 * 校验写入权限
 */
function checkWritePermission(targetPath, whitelist, allowRootWrite = false) {
  const normalizedTarget = normalizePath(targetPath);
  
  if (!whitelist || whitelist.length === 0) {
    return {
      allowed: false,
      reason: '白名单为空，不允许写入操作'
    };
  }
  
  if (normalizedTarget === '/' && allowRootWrite) {
    return {
      allowed: true,
      matchedRule: 'root (allowRootWrite=true)'
    };
  }
  
  return checkPath(targetPath, whitelist);
}

/**
 * 构建完整路径
 */
function buildFullPath(parentNodePath, nodeName) {
  const normalizedParent = normalizePath(parentNodePath);
  
  if (normalizedParent === '/') {
    return '/' + nodeName;
  }
  
  return normalizedParent + '/' + nodeName;
}

/**
 * 查找指定知识库的白名单配置
 */
function findWorkspaceConfig(workspaceId, config) {
  if (!config || !config.workspaces) {
    return null;
  }
  
  for (const ws of config.workspaces) {
    if (ws.workspaceId === workspaceId) {
      return ws;
    }
  }
  
  return null;
}

/**
 * 主函数 - 命令行入口
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log('白名单权限校验工具');
    console.log('');
    console.log('用法:');
    console.log('  node whitelist.js <command> [options]');
    console.log('');
    console.log('命令:');
    console.log('  check <path>              检查路径是否在白名单内');
    console.log('  show                      显示当前配置');
    console.log('  build-path <parent> <name>  构建完整路径');
    console.log('');
    process.exit(0);
  }
  
  try {
    let result;
    
    switch (command) {
      case 'check':
        const targetPath = args[1];
        if (!targetPath) {
          throw new Error('缺少参数：目标路径');
        }
        
        const config = loadConfig();
        const wsConfig = config.workspaces && config.workspaces[0];
        if (!wsConfig) {
          throw new Error('配置中未找到 workspaces');
        }
        
        result = checkWritePermission(targetPath, wsConfig.whitelist, wsConfig.allowRootWrite);
        result.path = targetPath;
        break;
        
      case 'show':
        result = loadConfig();
        break;
        
      case 'build-path':
        const parentPath = args[1];
        const nodeName = args[2];
        if (!parentPath || !nodeName) {
          throw new Error('缺少参数：parentPath 和 nodeName');
        }
        result = {
          fullPath: buildFullPath(parentPath, nodeName)
        };
        break;
        
      default:
        console.error(`未知命令：${command}`);
        process.exit(1);
    }
    
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: error.message
    }, null, 2));
    process.exit(1);
  }
}

// 导出函数供其他模块使用
module.exports = {
  loadConfig,
  checkPath,
  checkWritePermission,
  buildFullPath,
  normalizePath,
  getSkillDir,
  findWorkspaceConfig
};

// 命令行执行
if (require.main === module) {
  main();
}
