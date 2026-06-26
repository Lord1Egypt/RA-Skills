/**
 * 定时任务入口
 *
 * 使用方式:
 *   node scheduler.js              - 执行一轮（单个账号）
 *   node scheduler.js --full       - 一次性跑完所有账号（不等待定时）
 */

const CycleRunner = require('./cycle_runner');

async function main() {
  const args = process.argv.slice(2);
  const isFullRun = args.includes('--full');

  console.log('========================================');
  console.log(`eBay 账号活跃任务启动 | ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
  console.log(`模式: ${isFullRun ? '全量覆盖（一次性跑完）' : '单账号轮换'}`);
  console.log('========================================');

  const runner = new CycleRunner();

  try {
    if (isFullRun) {
      await runner.runAllOnce();
    } else {
      await runner.runOnce();
    }
  } catch (e) {
    console.error('任务执行出错:', e.message);
    process.exit(1);
  }

  console.log('\n任务结束');
}

main().catch(console.error);
