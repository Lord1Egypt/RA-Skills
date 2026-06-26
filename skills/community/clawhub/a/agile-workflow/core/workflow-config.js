// 工作流配置文件 v7.11
// 完全串行模式（质量优先）

const WORKFLOW_CONFIG = {
  // 项目配置
  project: {
    workspace: '/home/ubutu/.openclaw/workspace',
    novelArchitect: '/home/ubutu/.openclaw/workspace-novel_architect'
  },
  
  // 章节细纲配置 - 完全串行（质量优先）
  outlineParallelism: {
    mode: 'serial',  // 'serial' 完全串行
    enableStateLock: false,  // 串行不需要锁
    chapterByChapter: true,  // 逐章创作
    syncEveryChapter: true   // 每章同步状态
  },
  
  // 正文创作配置
  writingConfig: {
    chapterWordCount: 6500,  // 每章字数
    qualityThreshold: 80,    // 质量阈值
    enableReview: true       // 启用审查
  },
  
  // 状态管理配置
  stateManagement: {
    enableCentralLibrary: true,    // 启用中央状态库
    enableForeshadowingTrack: true, // 启用伏笔追踪
    autoSync: true                 // 自动同步
  }
};

module.exports = WORKFLOW_CONFIG;
