/**
 * 智能定价命令 - 根据各平台竞争情况智能定价
 * 支持竞争性定价、激进定价、保守定价策略
 */

const chalk = require('chalk');
const ora = require('ora');
const { PricingEngine } = require('../src/pricing');
const { FeishuSync } = require('../src/feishu');

async function execute(options) {
  const spinner = ora('准备智能定价分析...').start();
  
  try {
    console.log(chalk.bold.cyan('\n💰 智能定价系统\n'));
    
    const pricingEngine = new PricingEngine();
    
    // 分析竞争价格
    if (options.analyze) {
      spinner.text = '分析各平台竞争价格...';
      
      const analysis = await pricingEngine.analyzeCompetition({
        platform: options.platform,
        strategy: options.strategy || 'competitive'
      });
      
      spinner.succeed(chalk.green('✓ 竞争分析完成'));
      
      console.log(chalk.bold('\n📊 竞争价格分析:\n'));
      
      // 显示平台价格对比
      console.log(chalk.bold('各平台价格分布:'));
      analysis.platformPrices.forEach(p => {
        console.log(`  ${chalk.cyan(p.platform)}: $${p.min} - $${p.max} (平均: $${p.average.toFixed(2)})`);
      });
      
      console.log(chalk.bold('\n建议定价:'));
      console.log(`  当前成本：${chalk.gray('$' + analysis.cost.toFixed(2))}`);
      console.log(`  建议售价：${chalk.green('$' + analysis.suggestedPrice.toFixed(2))}`);
      console.log(`  预期利润率：${chalk.cyan(analysis.margin + '%')}`);
      console.log(`  竞争力指数：${chalk.yellow(analysis.competitiveness + '/100')}\n`);
      
      return analysis;
    }
    
    // 生成定价建议
    if (options.suggest) {
      spinner.text = '生成定价建议...';
      
      const suggestions = await pricingEngine.generateSuggestions({
        margin: options.margin || 30,
        strategy: options.strategy || 'competitive'
      });
      
      spinner.succeed(chalk.green('✓ 生成定价建议'));
      
      console.log(chalk.bold('\n💡 定价建议:\n'));
      
      suggestions.forEach((item, index) => {
        console.log(`${index + 1}. ${chalk.white(item.productName)}`);
        console.log(`   当前价格：${chalk.gray('$' + item.currentPrice)}`);
        console.log(`   建议价格：${chalk.green('$' + item.suggestedPrice)}`);
        console.log(`   调整幅度：${item.change > 0 ? chalk.green('+') : chalk.red('')}${item.change.toFixed(1)}%`);
        console.log(`   预期利润：${chalk.cyan('$' + item.expectedProfit)}\n`);
      });
      
      // 飞书同步
      if (options.feishu) {
        spinner.text = '同步定价建议到飞书...';
        const feishu = new FeishuSync();
        await feishu.syncPricingSuggestions(suggestions);
        spinner.succeed(chalk.green('✓ 飞书多维表格已更新'));
      }
      
      return { suggestions };
    }
    
    // 应用定价策略
    if (options.apply) {
      spinner.text = '应用定价策略...';
      
      const result = await pricingEngine.applyPricing({
        strategy: options.strategy || 'competitive',
        margin: options.margin || 30,
        platform: options.platform
      });
      
      spinner.succeed(chalk.green('✓ 定价策略已应用'));
      
      console.log(chalk.bold('\n✅ 应用结果:\n'));
      console.log(`  更新商品数：${chalk.green(result.updated)}`);
      console.log(`  失败商品数：${chalk.red(result.failed)}`);
      console.log(`  平均调价幅度：${chalk.cyan(result.averageChange + '%')}\n`);
      
      return result;
    }
    
    // 默认显示帮助
    console.log(chalk.yellow('请指定操作:\n'));
    console.log('  --analyze    分析竞争价格');
    console.log('  --suggest    生成定价建议');
    console.log('  --apply      应用定价策略');
    console.log(chalk.gray('\n可选参数:'));
    console.log('  --strategy <type>   定价策略 (competitive|aggressive|conservative)');
    console.log('  --margin <number>   目标利润率 (%)');
    console.log('  --platform <name>   目标平台\n');
    
  } catch (error) {
    spinner.fail(chalk.red('✗ 定价分析失败'));
    console.error(chalk.red(error.message));
    if (options.debug) {
      console.error(error.stack);
    }
    throw error;
  }
}

module.exports = { execute };
