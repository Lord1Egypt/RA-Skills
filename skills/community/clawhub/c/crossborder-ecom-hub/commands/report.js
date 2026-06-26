/**
 * 数据报表命令 - 数据分析报表生成
 * 销售、库存、利润、平台对比等多维度分析
 */

const chalk = require('chalk');
const ora = require('ora');
const dayjs = require('dayjs');
const { ReportGenerator } = require('../src/reports');
const { FeishuSync } = require('../src/feishu');

async function execute(options) {
  const spinner = ora('准备数据报表...').start();
  
  try {
    console.log(chalk.bold.cyan('\n📈 数据分析报表\n'));
    
    const reportGenerator = new ReportGenerator();
    const period = options.period || 'weekly';
    
    // 销售报表
    if (options.sales) {
      spinner.text = '生成销售报表...';
      
      const report = await reportGenerator.generateSalesReport({ period });
      
      spinner.succeed(chalk.green('✓ 销售报表生成完成'));
      
      console.log(chalk.bold(`\n📊 销售报表 (${period})\n`));
      
      console.log(chalk.bold('销售概览:'));
      console.log(`  总销售额：${chalk.green('$' + report.totalSales.toFixed(2))}`);
      console.log(`  总订单数：${chalk.cyan(report.totalOrders)}`);
      console.log(`  平均客单价：${chalk.yellow('$' + report.averageOrderValue.toFixed(2))}`);
      console.log(`  同比增长：${report.growth > 0 ? chalk.green('+') : chalk.red('')}${report.growth.toFixed(1)}%\n`);
      
      console.log(chalk.bold('按平台销售:'));
      report.byPlatform.forEach(p => {
        const percentage = ((p.sales / report.totalSales) * 100).toFixed(1);
        console.log(`  ${chalk.cyan(p.platform)}: $${p.sales.toFixed(2)} (${percentage}%)`);
      });
      
      console.log(chalk.bold('\n销售趋势:'));
      report.trend.forEach(point => {
        const bar = '█'.repeat(Math.round(point.sales / 100));
        console.log(`  ${point.date}: ${bar} $${point.sales.toFixed(2)}`);
      });
      
      // 飞书同步
      if (options.feishu) {
        spinner.text = '同步报表到飞书多维表格...';
        const feishu = new FeishuSync();
        await feishu.syncReport('sales', report);
        spinner.succeed(chalk.green('✓ 飞书多维表格已更新'));
      }
      
      // 导出
      if (options.export) {
        const path = await reportGenerator.exportReport(report, options.export);
        console.log(chalk.green(`\n✓ 报表已导出：${path}\n`));
      }
      
      return report;
    }
    
    // 库存报表
    if (options.inventory) {
      spinner.text = '生成库存报表...';
      
      const report = await reportGenerator.generateInventoryReport({ period });
      
      spinner.succeed(chalk.green('✓ 库存报表生成完成'));
      
      console.log(chalk.bold(`\n📦 库存报表 (${period})\n`));
      
      console.log(chalk.bold('库存概览:'));
      console.log(`  总 SKU 数：${chalk.cyan(report.totalSkus)}`);
      console.log(`  总库存量：${chalk.yellow(report.totalQuantity)}`);
      console.log(`  库存周转率：${chalk.green(report.turnoverRate.toFixed(2))}`);
      console.log(`  滞销商品：${chalk.red(report.slowMoving)}\n`);
      
      console.log(chalk.bold('库存预警:'));
      console.log(`  低库存商品：${chalk.red(report.lowStockCount)}`);
      console.log(`  零库存商品：${chalk.red(report.outOfStockCount)}`);
      console.log(`  超储商品：${chalk.yellow(report.overstockCount)}\n`);
      
      return report;
    }
    
    // 利润分析
    if (options.profit) {
      spinner.text = '生成利润分析...';
      
      const report = await reportGenerator.generateProfitReport({ period });
      
      spinner.succeed(chalk.green('✓ 利润分析完成'));
      
      console.log(chalk.bold(`\n💰 利润分析 (${period})\n`));
      
      console.log(chalk.bold('利润概览:'));
      console.log(`  总收入：${chalk.green('$' + report.revenue.toFixed(2))}`);
      console.log(`  总成本：${chalk.red('$' + report.cost.toFixed(2))}`);
      console.log(`  毛利润：${chalk.cyan('$' + report.grossProfit.toFixed(2))}`);
      console.log(`  利润率：${chalk.yellow(report.margin.toFixed(1) + '%')}\n`);
      
      console.log(chalk.bold('按平台利润:'));
      report.byPlatform.forEach(p => {
        console.log(`  ${chalk.cyan(p.platform)}: $${p.profit.toFixed(2)} (${p.margin.toFixed(1)}%)`);
      });
      
      return report;
    }
    
    // 平台对比
    if (options.platform) {
      spinner.text = '生成平台对比报表...';
      
      const report = await reportGenerator.generatePlatformComparison({ period });
      
      spinner.succeed(chalk.green('✓ 平台对比完成'));
      
      console.log(chalk.bold(`\n🔍 平台对比 (${period})\n`));
      
      console.table(report.platforms.map(p => ({
        平台：chalk.cyan(p.name),
        销售额：'$' + p.sales.toFixed(2),
        订单数：p.orders,
        利润率：p.margin.toFixed(1) + '%',
        评分：p.rating + '/5'
      })));
      
      console.log(chalk.bold('\n最佳表现:'));
      console.log(`  销售额最高：${chalk.green(report.bestBySales.platform)}`);
      console.log(`  利润率最高：${chalk.green(report.bestByMargin.platform)}`);
      console.log(`  订单量最高：${chalk.green(report.bestByOrders.platform)}\n`);
      
      return report;
    }
    
    // 默认显示帮助
    console.log(chalk.yellow('请指定报表类型:\n'));
    console.log('  --sales            销售报表');
    console.log('  --inventory        库存报表');
    console.log('  --profit           利润分析');
    console.log('  --platform         平台对比');
    console.log(chalk.gray('\n可选参数:'));
    console.log('  --period <type>    报表周期 (daily|weekly|monthly)');
    console.log('  --export <path>    导出路径');
    console.log('  --feishu           同步到飞书多维表格\n');
    
  } catch (error) {
    spinner.fail(chalk.red('✗ 报表生成失败'));
    console.error(chalk.red(error.message));
    if (options.debug) {
      console.error(error.stack);
    }
    throw error;
  }
}

module.exports = { execute };
