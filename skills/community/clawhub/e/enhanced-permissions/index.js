/**
 * Enhanced Permissions Skill for OpenClaw
 * 
 * 自动注册所有工具和功能，安装即可使用
 */

const {
  MemoryManager,
  PermissionChecker,
  PermissionLevel,
  KnowledgeGraph,
  EntityType,
  RelationType,
  EntityExtractor,
  defaultAuditLogger
} = require('./dist/index.js');

// 全局实例（单例模式）
let memoryManagerInstance = null;
let permissionCheckerInstance = null;

/**
 * 初始化 Skill
 */
function initialize(config = {}) {
  console.log('🔧 Enhanced Permissions Skill 初始化...');
  
  const {
    enableVersionControl = true,
    enableAutoOrganize = true,
    enableSuggestions = true,
    userLevel = 'moderate'
  } = config;
  
  // 创建记忆管理器
  memoryManagerInstance = new MemoryManager(
    enableVersionControl,
    enableAutoOrganize,
    enableSuggestions
  );
  
  // 创建权限检查器
  permissionCheckerInstance = new PermissionChecker({
    userLevel: PermissionLevel[userLevel.toUpperCase()] || PermissionLevel.MODERATE,
    requireConfirm: PermissionLevel.MODERATE,
    trustedSessions: ['main-session']
  });
  
  console.log('✅ Enhanced Permissions Skill 初始化完成');
  console.log(`   版本控制：${enableVersionControl ? '✅' : '❌'}`);
  console.log(`   自动整理：${enableAutoOrganize ? '✅' : '❌'}`);
  console.log(`   智能建议：${enableSuggestions ? '✅' : '❌'}`);
  
  return {
    memoryManager: memoryManagerInstance,
    permissionChecker: permissionCheckerInstance
  };
}

/**
 * 获取记忆管理器实例
 */
function getMemoryManager() {
  if (!memoryManagerInstance) {
    initialize();
  }
  return memoryManagerInstance;
}

/**
 * 获取权限检查器实例
 */
function getPermissionChecker() {
  if (!permissionCheckerInstance) {
    initialize();
  }
  return permissionCheckerInstance;
}

/**
 * 注册到 OpenClaw 工具系统
 */
function registerTools(openclaw) {
  console.log('🔧 注册 Enhanced Permissions 工具...');
  
  const mm = getMemoryManager();
  const pc = getPermissionChecker();
  
  // 注册记忆工具
  openclaw.registerTool('memory_store', {
    description: 'Store a memory with tags',
    handler: async (params) => {
      const { content, tags = [] } = params;
      const id = await mm.store(content, tags);
      return { success: true, id };
    }
  });
  
  openclaw.registerTool('memory_recall', {
    description: 'Recall memories by query',
    handler: async (params) => {
      const { query, limit = 5 } = params;
      const memories = await mm.recall(query, { limit });
      return { success: true, memories };
    }
  });
  
  openclaw.registerTool('memory_update', {
    description: 'Update memory content (creates new version)',
    handler: async (params) => {
      const { id, newContent, reason } = params;
      const memory = await mm.updateMemory(id, newContent, 'user', reason);
      return { success: !!memory, memory };
    }
  });
  
  openclaw.registerTool('memory_version_history', {
    description: 'Get version history of a memory',
    handler: async (params) => {
      const { id, limit = 10 } = params;
      const history = await mm.getVersionHistory(id, { limit });
      return { success: true, history };
    }
  });
  
  openclaw.registerTool('memory_auto_organize', {
    description: 'Auto-organize memories (merge duplicates, auto-tag, etc)',
    handler: async (params) => {
      const { dryRun = true } = params;
      const result = await mm.autoOrganize({ dryRun });
      return { success: true, result };
    }
  });
  
  openclaw.registerTool('permission_check', {
    description: 'Check if an operation is allowed',
    handler: async (params) => {
      const { operation, sessionId, operationParams } = params;
      const result = await pc.check(operation, {
        sessionId: sessionId || 'main',
        operation,
        params: operationParams || {},
        timestamp: Date.now()
      });
      return { success: true, result };
    }
  });
  
  console.log('✅ 注册 6 个工具完成');
  console.log('   - memory_store');
  console.log('   - memory_recall');
  console.log('   - memory_update');
  console.log('   - memory_version_history');
  console.log('   - memory_auto_organize');
  console.log('   - permission_check');
}

// 导出
module.exports = {
  initialize,
  getMemoryManager,
  getPermissionChecker,
  registerTools,
  
  // 直接导出类（高级用法）
  MemoryManager,
  PermissionChecker,
  PermissionLevel,
  KnowledgeGraph,
  EntityType,
  RelationType,
  EntityExtractor,
  defaultAuditLogger
};

// 自动初始化（如果在全局环境）
if (typeof window !== 'undefined' || typeof global !== 'undefined') {
  console.log('🎉 Enhanced Permissions Skill 已加载');
  console.log('💡 使用：const { memoryManager } = require("enhanced-permissions")');
}
