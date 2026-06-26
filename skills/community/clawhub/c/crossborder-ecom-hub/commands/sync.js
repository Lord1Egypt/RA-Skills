/**
 * 商品同步命令 - 多平台商品同步
 * 支持 TikTok、Amazon、Shopee、Lazada 之间的商品同步
 */

const chalk = require('chalk');
const ora = require('ora');
const { PlatformAdapter } = require('../src/platforms');
const { FeishuSync } = require('../src/feishu');

async function execute(options) {
  const spinner = ora('准备商品同步...').start();
  
  try {
    console.log(chalk.bold.cyan('\n📦 商品同步管理\n'));
    
    // 1. 初始化平台适配器
    spinner.text = '初始化平台连接...';
    const platforms = new PlatformAdapter();
    
    const availablePlatforms = await platforms.listPlatforms();
    console.log(chalk.gray('可用平台:'), availablePlatforms.join(', '));
    
    // 2. 获取商品列表
    spinner.text = '获取商品列表...';
    const sourcePlatform = options.from || 'tiktok';
    let products = [];
    
    if (options.all) {
      products = await platforms.getProducts(sourcePlatform);
    } else if (options.productIds) {
      const ids = options.productIds.split(',');
      products = await platforms.getProductsByIds(sourcePlatform, ids);
    } else {
      // 默认获取最近 100 个商品
      products = await platforms.getProducts(sourcePlatform, { limit: 100 });
    }
    
    console.log(chalk.green(`✓ 获取到 ${products.length} 个商品`));
    
    // 3. 确定目标平台
    const targetPlatforms = options.to 
      ? options.to.split(',') 
      : availablePlatforms.filter(p => p !== sourcePlatform);
    
    console.log(chalk.gray('目标平台:'), targetPlatforms.join(', '));
    
    // 4. 执行同步
    spinner.text = '同步商品到目标平台...';
    const syncResults = [];
    
    for (const target of targetPlatforms) {
      const result = await platforms.syncProducts(products, sourcePlatform, target);
      syncResults.push({
        platform: target,
        success: result.success,
        synced: result.synced?.length || 0,
        failed: result.failed?.length || 0,
        errors: result.errors
      });
    }
    
    spinner.succeed(chalk.green('✓ 商品同步完成'));
    
    // 5. 显示结果
    console.log(chalk.bold('\n📊 同步结果:\n'));
    console.table(syncResults.map(r => ({
      平台：r.platform,
      成功：chalk.green(r.synced),
      失败：r.failed > 0 ? chalk.red(r.failed) : r.failed,
      状态：r.success ? chalk.green('✓ 完成') : chalk.red('✗ 失败')
    })));
    
    // 6. 飞书多维表格同步 (如果启用)
    if (options.feishu) {
      spinner.text = '同步到飞书多维表格...';
      const feishu = new FeishuSync();
      await feishu.syncProducts(products);
      spinner.succeed(chalk.green('✓ 飞书多维表格已更新'));
    }
    
    // 7. 显示统计
    console.log(chalk.bold.cyan('\n📈 同步统计:\n'));
    const totalSynced = syncResults.reduce((sum, r) => sum + r.synced, 0);
    const totalFailed = syncResults.reduce((sum, r) => sum + r.failed, 0);
    
    console.log(`  总商品数：${chalk.white(products.length)}`);
    console.log(`  同步成功：${chalk.green(totalSynced)}`);
    console.log(`  同步失败：${chalk.red(totalFailed)}`);
    console.log(`  成功率：${chalk.cyan(((totalSynced / (totalSynced + totalFailed)) * 100).toFixed(1) + '%')}\n`);
    
    return {
      success: true,
      products: products.length,
      synced: totalSynced,
      failed: totalFailed,
      results: syncResults
    };
    
  } catch (error) {
    spinner.fail(chalk.red('✗ 同步失败'));
    console.error(chalk.red(error.message));
    if (options.debug) {
      console.error(error.stack);
    }
    throw error;
  }
}

module.exports = { execute };
