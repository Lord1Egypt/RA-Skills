#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import { LogisticsAggregator } from './core/aggregator.js';
import { Platform } from './types/index.js';
import os from 'os';
import path from 'path';

const program = new Command();

program
  .name('ecommerce-logistics')
  .description('Query logistics from Taobao, JD, PDD, Douyin')
  .version('1.0.0');

program
  .option('-p, --platform <platform>', 'Platform to query (taobao|jd|pdd|douyin|all)', 'all')
  .option('-d, --data-dir <dir>', 'Data directory for cookies', path.join(os.homedir(), '.ecommerce-logistics'))
  .option('--headless', 'Run in headless mode', false)
  .option('--login', 'Perform QR login for specified platform')
  .action(async (options) => {
    const aggregator = new LogisticsAggregator({
      platform: options.platform as Platform | 'all',
      dataDir: options.dataDir,
      headless: options.headless
    });

    try {
      await aggregator.initialize();

      if (options.login) {
        // QR Login mode
        if (options.platform === 'all') {
          console.log(chalk.red('Error: --login requires --platform <platform>'));
          process.exit(1);
        }
        const success = await aggregator.loginPlatform(options.platform as Platform);
        process.exit(success ? 0 : 1);
      }

      // Query mode
      if (options.platform === 'all') {
        console.log(chalk.bold('\n📦 电商物流聚合查询\n'));
        const results = await aggregator.queryAll();
        
        let totalOrders = 0;
        for (const [platform, orders] of results) {
          totalOrders += orders.length;
          
          if (orders.length > 0) {
            console.log(chalk.bold(`\n━━━ ${getPlatformName(platform)} ━━━`));
            for (const order of orders) {
              printOrder(order);
            }
          }
        }

        console.log(chalk.bold(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`));
        console.log(chalk.green(`总计: ${totalOrders} 个订单`));
        console.log(chalk.gray(`数据目录: ${options.dataDir}\n`));
      } else {
        const orders = await aggregator.queryPlatform(options.platform as Platform);
        
        console.log(chalk.bold(`\n━━━ ${getPlatformName(options.platform)} ━━━`));
        for (const order of orders) {
          printOrder(order);
        }
        console.log(chalk.gray(`\n数据目录: ${options.dataDir}\n`));
      }
    } catch (error: any) {
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    } finally {
      await aggregator.close();
    }
  });

function getPlatformName(platform: string): string {
  const names: Record<string, string> = {
    taobao: '淘宝',
    jd: '京东',
    pdd: '拼多多',
    douyin: '抖音'
  };
  return names[platform] || platform;
}

function printOrder(order: any): void {
  const statusEmoji: Record<string, string> = {
    pending: '⏳',
    shipped: '📦',
    in_transit: '🚚',
    out_for_delivery: '🏃',
    delivered: '✅',
    exception: '⚠️',
    cancelled: '❌'
  };

  console.log(chalk.cyan(`\n  订单号: ${order.orderId}`));
  if (order.orderTitle) {
    console.log(chalk.gray(`  商品: ${order.orderTitle.substring(0, 40)}${order.orderTitle.length > 40 ? '...' : ''}`));
  }
  console.log(chalk.gray(`  快递: ${order.carrier}${order.trackingNumber ? ' | 单号: ' + order.trackingNumber : ''}`));
  console.log(`  状态: ${statusEmoji[order.status] || '❓'} ${order.status}`);
  
  if (order.timeline && order.timeline.length > 0) {
    const latest = order.timeline[0];
    console.log(chalk.gray(`  最新: [${latest.time}] ${latest.description.substring(0, 50)}...`));
  }
}

program.parse();