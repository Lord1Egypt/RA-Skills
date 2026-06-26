/**
 * Cognitive Brain - Main Entry Point
 * 类脑认知系统主入口
 */

const path = require('path');

// 导出核心模块
module.exports = {
  // 脚本路径
  scripts: {
    encode: path.join(__dirname, 'scripts', 'encode.cjs'),
    recall: path.join(__dirname, 'scripts', 'recall.cjs'),
    brain: path.join(__dirname, 'scripts', 'brain.cjs'),
    associate: path.join(__dirname, 'scripts', 'associate.cjs'),
    reflect: path.join(__dirname, 'scripts', 'reflect.cjs'),
    forget: path.join(__dirname, 'scripts', 'forget.cjs'),
    visualize: path.join(__dirname, 'scripts', 'visualize.cjs'),
    timeline: path.join(__dirname, 'scripts', 'timeline.cjs'),
    sharedMemory: path.join(__dirname, 'scripts', 'shared_memory.cjs'),
    prediction: path.join(__dirname, 'scripts', 'prediction_client.cjs'),
    heartbeatReflect: path.join(__dirname, 'scripts', 'heartbeat_reflect.cjs'),
    freeThink: path.join(__dirname, 'scripts', 'free_think.cjs'),
    sessionStartLoader: path.join(__dirname, 'scripts', 'session_start_loader.cjs')
  },

  // Hook 路径
  hooks: {
    cognitiveRecall: path.join(__dirname, 'hooks', 'cognitive-recall')
  },

  // 版本信息
  version: require('./package.json').version,

  // 健康检查
  healthCheck: () => {
    const { execSync } = require('child_process');
    try {
      execSync('node scripts/brain.cjs health_check', {
        cwd: __dirname,
        stdio: 'inherit'
      });
      return true;
    } catch (e) {
      return false;
    }
  }
};

// CLI 支持
if (require.main === module) {
  console.log('🧠 Cognitive Brain v' + require('./package.json').version);
  console.log('\n可用脚本:');
  const mod = module.exports;
  Object.entries(mod.scripts).forEach(([name, path]) => {
    console.log(`  - ${name}: ${path}`);
  });
  console.log('\n使用示例:');
  console.log('  node scripts/brain.cjs health_check');
  console.log('  node scripts/encode.cjs --content "记忆内容"');
  console.log('  node scripts/recall.cjs --query "关键词"');
}
