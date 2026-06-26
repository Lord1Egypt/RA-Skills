#!/bin/bash
# Dreaming Guard Pro - Cron Runner
# 每分钟执行一次guard循环检查
# 安装: crontab -e 添加 * * * * * /path/to/dreaming-guard-pro.sh >> /tmp/dreaming-guard-pro.log 2>&1

set -e

# 项目路径
PROJECT_DIR="/root/.openclaw/workspace/projects/dreaming-guard-pro"
NODE_PATH="$(which node)"

# 进入项目目录
cd "$PROJECT_DIR"

# 执行单次循环
# 使用Node.js直接调用Guard模块的runOnce方法
$NODE_PATH -e "
const Guard = require('./src/guard');

async function main() {
  const guard = new Guard({
    loopInterval: 60000,     // cron每分钟调用，不需要内部定时
    reportInterval: 0,       // 禁用内部报告定时
    enableProtector: true,
    enableHealer: true,
    enableReporter: false,   // cron模式下禁用自动报告
    logLevel: 'info'
  });

  try {
    // 启动监控器和保护器（但不启动内部定时循环）
    await guard.monitor.start();
    if (guard.protector) await guard.protector.start();
    if (guard.healer) await guard.healer.start();
    
    // 执行一次循环
    const result = await guard.runOnce();
    
    // 输出结果
    if (result.error) {
      console.error('[ERROR]', result.error);
      process.exit(1);
    }
    
    // 简要日志
    const ts = new Date().toISOString();
    const monitor = result.steps.monitor || {};
    const decision = result.steps.decision || {};
    console.log(\`[\${ts}] Loop #\${result.loopCount}: size=\${monitor.currentSize || 0}B, files=\${monitor.currentFiles || 0}, risk=\${decision.riskLevel || 'unknown'}, action=\${decision.action || 'none'}\`);
    
    // 停止
    await guard.monitor.stop();
    if (guard.protector) await guard.protector.stop();
    if (guard.healer) await guard.healer.stop();
    
    process.exit(0);
  } catch (err) {
    console.error('[FATAL]', err.message);
    process.exit(1);
  }
}

main();
"