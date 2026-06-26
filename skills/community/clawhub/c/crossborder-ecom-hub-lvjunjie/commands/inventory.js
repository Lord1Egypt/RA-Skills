/**
 * 库存同步命令 - 实时库存同步管理
 * 确保多平台库存一致性，防止超卖
 */

const chalk = require('chalk');
const ora = require('ora');
const { InventoryManager } = require('../src/inventory');
const { FeishuSync } = require('../src/feishu');

async function execute(options) {
  const spinner = ora('准备库存管理...').start();
  
  try {
    console.log(chalk.bold.cyan('\n📊 库存同步管理\n'));
    
    const inventoryManager = new InventoryManager();
    
    // 同步库存
    if (options.sync) {
      spinner.text = '同步多平台库存...';
      
      const result = await inventoryManager.syncInventory({
        platform: options.platform,
        realTime: true
      });
      
      spinner.succeed(chalk.green('✓ 库存同步完成'));
      
      console.log(chalk.bold('\n📦 同步结果:\n'));
      console.log(`  同步商品数：${chalk.green(result.synced)}`);
      console.log(`  更新库存数：${chalk.cyan(result.updated)}`);
      console.log(`  同步失败数：${chalk.red(result.failed)}\n`);
      
      return result;
    }
    
    // 检查库存状态
    if (options.check) {
      spinner.text = '检查库存状态...';
      
      const inventory = await inventoryManager.getInventoryStatus();
      
      spinner.succeed(chalk.green('✓ 库存检查完成'));
      
      console.log(chalk.bold('\n📋 库存状态:\n'));
      
      // 低库存预警
      const lowStockItems = inventory.filter(item => item.quantity <= (options.alert || 10));
      
      if (lowStockItems.length > 0) {
        console.log(chalk.bold.red(`⚠️ 低库存预警 (${lowStockItems.length} 个商品):\n`));
        lowStockItems.forEach(item => {
          console.log(`  ${chalk.yellow(item.sku)}: ${chalk.red(item.quantity)} 件 (平台：${item.platform})`);
        });
        console.log();
      } else {
        console.log(chalk.green('✓ 所有商品库存充足\n'));
      }
      
      // 库存汇总
      const totalItems = inventory.length;
      const totalQuantity = inventory.reduce((sum, item) => sum + item.quantity, 0);
      const avgQuantity = totalQuantity / totalItems;
      
      console.log(chalk.bold('库存汇总:'));
      console.log(`  总商品数：${totalItems}`);
      console.log(`  总库存量：${totalQuantity}`);
      console.log(`  平均库存：${avgQuantity.toFixed(1)} 件\n`);
      
      // 飞书同步
      if (options.feishu) {
        spinner.text = '同步库存到飞书多维表格...';
        const feishu = new FeishuSync();
        await feishu.syncInventory(inventory);
        spinner.succeed(chalk.green('✓ 飞书多维表格已更新'));
      }
      
      return { inventory, lowStockItems };
    }
    
    // 更新库存
    if (options.update) {
      spinner.text = '更新库存...';
      
      // 这里可以从标准输入或文件读取库存更新
      console.log(chalk.yellow('请提供库存更新数据:\n'));
      console.log('  方式 1: 使用 --sync 从平台同步');
      console.log('  方式 2: 提供 CSV 文件路径');
      console.log('  方式 3: 通过 API 直接更新\n');
      
      return;
    }
    
    // 默认显示帮助
    console.log(chalk.yellow('请指定操作:\n'));
    console.log('  --sync             同步多平台库存');
    console.log('  --check            检查库存状态');
    console.log('  --update           更新库存');
    console.log(chalk.gray('\n可选参数:'));
    console.log('  --alert <number>    低库存预警阈值 (默认：10)');
    console.log('  --platform <name>   目标平台');
    console.log('  --feishu            同步到飞书多维表格\n');
    
  } catch (error) {
    spinner.fail(chalk.red('✗ 库存管理失败'));
    console.error(chalk.red(error.message));
    if (options.debug) {
      console.error(error.stack);
    }
    throw error;
  }
}

module.exports = { execute };
