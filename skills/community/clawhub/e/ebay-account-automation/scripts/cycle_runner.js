/**
 * 主循环控制器
 */

const adsApi = require('./ads_api');
const CdpEbayBot = require('./cdp_ebay_bot');
const CycleState = require('./cycle_state');
const config = require('./config');
const { randomDelay } = require('./behavior_engine');
const logger = require('./run_logger');

class CycleRunner {
  constructor() {
    this.state = new CycleState(config.CYCLE_STATE_FILE);
    this.accounts = [];
    this.currentAccount = null;
  }

  async init() {
    console.log('正在从 ADS Power 获取账号列表...');
    logger.log('INFO', '开始读取 ADS Power 账号列表');
    try {
      this.accounts = await adsApi.getAllUsersFull();
      if (this.accounts.length === 0) throw new Error('ADS Power 中没有找到任何账号');
      console.log(`共找到 ${this.accounts.length} 个账号`);
      logger.log('INFO', `账号列表读取完成，共 ${this.accounts.length} 个账号`);
      this.state.load();
    } catch (e) {
      logger.log('ERROR', `初始化失败: ${e.message}`);
      throw e;
    }
  }

  async runAccount(account, accountNum) {
    const userId = account.user_id;
    const accountName = account.name || account.user_id;
    const startTime = Date.now();

    logger.logRunStart(accountName, accountNum, this.accounts.length);

    let bot = null;
    try {
      console.log('  关闭旧浏览器...');
      await adsApi.stopBrowser(userId);
      await randomDelay(1000, 2000);

      bot = new CdpEbayBot(userId);
      await bot.connect();

      const result = await bot.runActiveSession(config.ACCOUNT_RUNTIME_MS);
      const durationSec = Math.round((Date.now() - startTime) / 1000);
      result.durationSec = durationSec;

      console.log(`  账号 [${accountName}] 任务完成:`);
      console.log(`    ${result.searchesDone} 轮搜索`);
      console.log(`    ${result.totalFavorited} 个商品收藏`);
      console.log(`    ${result.totalAddedToCart} 个商品加入购物车`);

      logger.logRunEnd(accountName, result);
      this.state.markCompleted(userId);

    } catch (e) {
      if (e instanceof adsApi.ExceedingDailyLimit) {
        console.warn(`  ⚠️  账号 [${accountName}] ADS Power 配额耗尽（${e.waitSeconds/3600}h 后恢复），跳过执行下一个账号`);
        logger.log('WARN', `账号 [${accountName}] 配额耗尽跳过: ${e.message}`);
        return { skipped: true, reason: '配额耗尽' };
      }
      console.error(`  账号 [${accountName}] 执行出错:`, e.message);
      logger.logError(accountName, e.message);
    } finally {
      if (bot) await bot.close().catch(() => {});
      console.log('  关闭浏览器');
      await adsApi.stopBrowser(userId).catch(() => {});
    }
  }

  async runOnce() {
    await this.init();
    const idx = this.state.nextIndex(this.accounts.length);
    const account = this.accounts[idx];
    await this.runAccount(account, idx + 1);
    console.log('\n本轮完成，等待下一次触发...');
    logger.log('INFO', '本轮完成，等待下一次触发');
  }

  async runAllOnce() {
    await this.init();
    const total = this.accounts.length;
    for (let i = 0; i < total; i++) {
      const account = this.accounts[i];
      await this.runAccount(account, i + 1);
      if (i < total - 1) {
        console.log(`\n  切换账号，休息 10 秒...`);
        logger.log('INFO', `切换账号，休息 10 秒`);
        await randomDelay(10000, 20000);
      }
    }
    console.log('\n========== 所有账号全量覆盖完成 ==========');
    logger.log('INFO', '所有账号全量覆盖完成');
  }
}

module.exports = CycleRunner;
