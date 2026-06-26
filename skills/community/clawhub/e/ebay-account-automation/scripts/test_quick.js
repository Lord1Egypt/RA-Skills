/**
 * 5分钟快速验证脚本
 * 用于测试环境是否正确，不需要等30分钟
 */

const CycleRunner = require('./cycle_runner');
const config = require('./config');

// Override runtime to 5 minutes for quick test
const originalRuntime = config.ACCOUNT_RUNTIME_MS;
config.ACCOUNT_RUNTIME_MS = 5 * 60 * 1000;

async function main() {
  console.log('========================================');
  console.log(`eBay 快速验证 (5分钟) | ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
  console.log('========================================');

  const runner = new CycleRunner();

  try {
    await runner.runOnce();
  } catch (e) {
    console.error('验证失败:', e.message);
    process.exit(1);
  }

  console.log('\n验证结束');
  config.ACCOUNT_RUNTIME_MS = originalRuntime;
}

main().catch(console.error);
