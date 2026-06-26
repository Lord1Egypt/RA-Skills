#!/usr/bin/env node

/**
 * CrossBorder Ecom Hub - CLI Entry Point
 * 跨境电商多平台管理技能命令行入口
 * 
 * @version 1.0.0
 * @author OpenClaw Skills
 */

const { program } = require('commander');
const chalk = require('chalk');
const ora = require('ora');
const path = require('path');
const fs = require('fs');

// 加载命令
const syncCommand = require('../commands/sync');
const orderCommand = require('../commands/order');
const pricingCommand = require('../commands/pricing');
const inventoryCommand = require('../commands/inventory');
const reportCommand = require('../commands/report');
const platformCommand = require('../commands/platform');

const pkg = require('../package.json');

// 设置 CLI 信息
program
  .name('crossborder-ecom')
  .description(chalk.bold('🌏 跨境电商多平台管理技能 - TikTok+Amazon+Shopee+Lazada 统一管理'))
  .version(pkg.version);

// 全局选项
program
  .option('-k, --api-key <key>', 'API 密钥')
  .option('-p, --platform <platform>', '目标平台 (tiktok|amazon|shopee|lazada|all)')
  .option('-o, --output <format>', '输出格式 (json|table|csv)', 'table')
  .option('--feishu', '启用飞书多维表格同步')
  .option('--debug', '调试模式');

// 商品同步命令
program
  .command('sync')
  .description('📦 多平台商品同步')
  .option('--from <platform>', '源平台')
  .option('--to <platforms>', '目标平台 (逗号分隔)')
  .option('--product-ids <ids>', '商品 ID 列表 (逗号分隔)')
  .option('--all', '同步所有商品')
  .action(async (options, cmd) => {
    const globalOpts = cmd.parent.opts();
    await syncCommand.execute({ ...options, ...globalOpts });
  });

// 订单管理命令
program
  .command('order')
  .description('🛒 统一订单管理')
  .option('--list', '列出订单')
  .option('--status <status>', '订单状态')
  .option('--platform <platform>', '平台过滤')
  .option('--date-from <date>', '开始日期')
  .option('--date-to <date>', '结束日期')
  .option('--export', '导出订单')
  .action(async (options, cmd) => {
    const globalOpts = cmd.parent.opts();
    await orderCommand.execute({ ...options, ...globalOpts });
  });

// 智能定价命令
program
  .command('pricing')
  .description('💰 智能定价系统')
  .option('--analyze', '分析竞争价格')
  .option('--suggest', '生成定价建议')
  .option('--apply', '应用定价策略')
  .option('--strategy <strategy>', '定价策略 (competitive|aggressive|conservative)')
  .option('--margin <number>', '目标利润率 (%)', 30)
  .action(async (options, cmd) => {
    const globalOpts = cmd.parent.opts();
    await pricingCommand.execute({ ...options, ...globalOpts });
  });

// 库存同步命令
program
  .command('inventory')
  .description('📊 库存同步管理')
  .option('--sync', '同步库存')
  .option('--check', '检查库存状态')
  .option('--alert <threshold>', '低库存预警阈值', 10)
  .option('--update', '更新库存')
  .action(async (options, cmd) => {
    const globalOpts = cmd.parent.opts();
    await inventoryCommand.execute({ ...options, ...globalOpts });
  });

// 数据报表命令
program
  .command('report')
  .description('📈 数据分析报表')
  .option('--sales', '销售报表')
  .option('--inventory', '库存报表')
  .option('--profit', '利润分析')
  .option('--platform', '平台对比')
  .option('--period <period>', '报表周期 (daily|weekly|monthly)', 'weekly')
  .option('--export <path>', '导出路径')
  .action(async (options, cmd) => {
    const globalOpts = cmd.parent.opts();
    await reportCommand.execute({ ...options, ...globalOpts });
  });

// 平台管理命令
program
  .command('platform')
  .description('🔧 平台配置管理')
  .option('--list', '列出已配置平台')
  .option('--add <platform>', '添加平台')
  .option('--remove <platform>', '移除平台')
  .option('--status', '检查平台状态')
  .action(async (options, cmd) => {
    const globalOpts = cmd.parent.opts();
    await platformCommand.execute({ ...options, ...globalOpts });
  });

// 快速启动向导
program
  .command('init')
  .description('🚀 初始化配置向导')
  .action(async () => {
    const spinner = ora('初始化配置...').start();
    
    try {
      const configDir = path.join(process.env.HOME || process.env.USERPROFILE, '.crossborder-ecom');
      
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }
      
      const configPath = path.join(configDir, 'config.json');
      const defaultConfig = {
        platforms: {},
        feishu: {
          enabled: false,
          appId: '',
          appSecret: '',
          bitableToken: ''
        },
        pricing: {
          defaultMargin: 30,
          strategy: 'competitive'
        },
        inventory: {
          lowStockThreshold: 10,
          syncInterval: 300
        }
      };
      
      fs.writeFileSync(configPath, JSON.stringify(defaultConfig, null, 2));
      
      spinner.succeed(chalk.green('✓ 初始化完成！'));
      console.log(chalk.cyan('\n配置文件已创建：'), configPath);
      console.log(chalk.yellow('\n下一步:'));
      console.log('  1. 编辑配置文件，添加各平台 API 密钥');
      console.log('  2. 运行 crossborder-ecom platform --list 查看配置');
      console.log('  3. 运行 crossborder-ecom sync --all 开始同步商品\n');
      
    } catch (error) {
      spinner.fail(chalk.red('✗ 初始化失败'));
      console.error(chalk.red(error.message));
      process.exit(1);
    }
  });

// 处理命令执行
async function main() {
  try {
    await program.parseAsync(process.argv);
    
    // 如果没有提供命令，显示帮助
    if (!process.argv.slice(2).length) {
      program.outputHelp();
      showQuickStart();
    }
  } catch (error) {
    console.error(chalk.red('\n❌ 错误:'), error.message);
    if (program.opts().debug) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// 显示快速入门提示
function showQuickStart() {
  console.log(chalk.bold.cyan('\n⚡ 快速入门:\n'));
  console.log('  ' + chalk.white('crossborder-ecom init') + '          - 初始化配置');
  console.log('  ' + chalk.white('crossborder-ecom sync --all') + '      - 同步所有商品');
  console.log('  ' + chalk.white('crossborder-ecom order --list') + '    - 查看订单');
  console.log('  ' + chalk.white('crossborder-ecom pricing --analyze') + ' - 分析定价');
  console.log('  ' + chalk.white('crossborder-ecom report --sales') + '  - 销售报表\n');
  console.log(chalk.gray('  使用 crossborder-ecom <command> --help 查看命令详情\n'));
}

main();
