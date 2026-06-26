/**
 * 订单管理命令 - 统一订单管理
 * 聚合多平台订单，提供统一视图和管理功能
 */

const chalk = require('chalk');
const ora = require('ora');
const dayjs = require('dayjs');
const { OrderManager } = require('../src/orders');
const { FeishuSync } = require('../src/feishu');

async function execute(options) {
  const spinner = ora('准备订单管理...').start();
  
  try {
    console.log(chalk.bold.cyan('\n🛒 统一订单管理\n'));
    
    const orderManager = new OrderManager();
    
    // 列出订单
    if (options.list) {
      spinner.text = '获取订单列表...';
      
      const filters = {
        platform: options.platform,
        status: options.status,
        dateFrom: options.dateFrom,
        dateTo: options.dateTo
      };
      
      const orders = await orderManager.getOrders(filters);
      
      spinner.succeed(chalk.green(`✓ 获取到 ${orders.length} 个订单`));
      
      // 显示订单摘要
      console.log(chalk.bold('\n📋 订单列表:\n'));
      
      if (orders.length === 0) {
        console.log(chalk.gray('  暂无订单'));
        return;
      }
      
      // 分组统计
      const byPlatform = {};
      const byStatus = {};
      let totalAmount = 0;
      
      orders.forEach(order => {
        byPlatform[order.platform] = (byPlatform[order.platform] || 0) + 1;
        byStatus[order.status] = (byStatus[order.status] || 0) + 1;
        totalAmount += order.amount || 0;
      });
      
      console.log(chalk.bold('按平台统计:'));
      Object.entries(byPlatform).forEach(([platform, count]) => {
        console.log(`  ${chalk.cyan(platform)}: ${count} 单`);
      });
      
      console.log(chalk.bold('\n按状态统计:'));
      Object.entries(byStatus).forEach(([status, count]) => {
        console.log(`  ${chalk.yellow(status)}: ${count} 单`);
      });
      
      console.log(chalk.bold('\n销售总额:'), chalk.green(`$${totalAmount.toFixed(2)}`));
      
      // 显示最近 10 个订单
      console.log(chalk.bold('\n最近订单:'));
      orders.slice(0, 10).forEach(order => {
        console.log(`  ${chalk.gray(order.id)} | ${chalk.cyan(order.platform)} | ${chalk.yellow(order.status)} | $${order.amount} | ${dayjs(order.createdAt).format('YYYY-MM-DD HH:mm')}`);
      });
      
      // 飞书同步
      if (options.feishu) {
        spinner.text = '同步订单到飞书多维表格...';
        const feishu = new FeishuSync();
        await feishu.syncOrders(orders);
        spinner.succeed(chalk.green('✓ 飞书多维表格已更新'));
      }
      
      // 导出订单
      if (options.export) {
        spinner.text = '导出订单数据...';
        const exportPath = await orderManager.exportOrders(orders, options.export);
        spinner.succeed(chalk.green(`✓ 订单已导出：${exportPath}`));
      }
      
      return {
        success: true,
        orders: orders.length,
        totalAmount,
        byPlatform,
        byStatus
      };
    }
    
    // 其他订单操作...
    console.log(chalk.yellow('请使用 --list 参数查看订单列表'));
    console.log(chalk.gray('\n可用选项:'));
    console.log('  --list              列出订单');
    console.log('  --status <status>   按状态过滤');
    console.log('  --platform <name>   按平台过滤');
    console.log('  --date-from <date>  开始日期');
    console.log('  --date-to <date>    结束日期');
    console.log('  --export            导出订单\n');
    
  } catch (error) {
    spinner.fail(chalk.red('✗ 订单管理失败'));
    console.error(chalk.red(error.message));
    if (options.debug) {
      console.error(error.stack);
    }
    throw error;
  }
}

module.exports = { execute };
