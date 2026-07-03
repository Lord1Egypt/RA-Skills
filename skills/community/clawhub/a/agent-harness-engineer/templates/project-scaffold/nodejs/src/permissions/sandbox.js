/**
 * ============================================
 * 类型: 核心框架
 * 模块: permissions.sandbox
 * 说明: 沙箱管理实现
 * 修改建议: 如需扩展，继承SandboxManager类
 * ============================================

const fs = require('fs');
const path = require('path');

class SandboxManager {
  constructor(config = {}) {
    this.enabled = config.enabled !== false;
    this.allowedDirectories = config.allowedDirectories || ['workspace/'];
    this.deniedPatterns = config.deniedPatterns || [];
  }
  
  validatePath(filePath) {
    if (!this.enabled) return true;
    
    const resolvedPath = path.resolve(filePath);
    const allowed = this.allowedDirectories.some(dir => {
      const resolvedDir = path.resolve(dir);
      return resolvedPath.startsWith(resolvedDir);
    });
    
    if (!allowed) {
      console.warn(`Path outside allowed directories: ${filePath}`);
      return false;
    }
    
    for (const pattern of this.deniedPatterns) {
      if (resolvedPath.includes(pattern)) {
        console.warn(`Path matches denied pattern: ${pattern}`);
        return false;
      }
    }
    
    return true;
  }
  
  validateCommand(command) {
    if (!this.enabled) return true;
    
    const dangerousPatterns = ['rm -rf', 'sudo', 'dd if=', '> /dev', 'mkfs'];
    for (const pattern of dangerousPatterns) {
      if (command.includes(pattern)) {
        console.warn(`Dangerous command detected: ${command}`);
        return false;
      }
    }
    
    return true;
  }
}

module.exports = { SandboxManager };
