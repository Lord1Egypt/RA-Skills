/**
 * ============================================
 * 类型: 核心框架
 * 模块: permissions.models
 * 说明: 权限模型定义
 * 修改建议: 如需扩展，添加新的权限规则
 * ============================================

class PermissionManager {
  constructor(config = {}) {
    this.mode = config.mode || 'ask';
    this.rules = (config.rules || []).map(rule => ({
      pattern: rule.pattern,
      action: rule.action,
      level: rule.level || 'read'
    }));
  }
  
  checkPermission(toolName, toolInput) {
    for (const rule of this.rules) {
      const regex = new RegExp(rule.pattern.replace('*', '.*'));
      if (regex.test(toolName)) {
        if (rule.action === 'deny') {
          return false;
        } else if (rule.action === 'ask') {
          throw new Error(`Permission required for: ${toolName}`);
        }
      }
    }
    return true;
  }
  
  addRule(pattern, action, level = 'read') {
    this.rules.push({ pattern, action, level });
  }
}

module.exports = { PermissionManager };
