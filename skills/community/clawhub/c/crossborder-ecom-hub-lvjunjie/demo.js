#!/usr/bin/env node

/**
 * CrossBorder Ecom Hub - 演示脚本
 * 展示技能核心功能
 */

const chalk = require('chalk');
const ora = require('ora');

async function demo() {
  console.log(chalk.bold.cyan('\n🌏 CrossBorder Ecom Hub - 功能演示\n'));
  console.log(chalk.gray('='.repeat(60)));
  
  // 演示 1: 平台连接
  console.log(chalk.bold('\n1️⃣ 平台连接演示\n'));
  
  const spinner = ora('连接 TikTok Shop...').start();
  await sleep(1000);
  spinner.succeed(chalk.green('✓ TikTok Shop 已连接'));
  
  spinner.start('连接 Amazon Seller Central...');
  await sleep(1000);
  spinner.succeed(chalk.green('✓ Amazon Seller Central 已连接'));
  
  spinner.start('连接 Shopee...');
  await sleep(1000);
  spinner.succeed(chalk.green('✓ Shopee 已连接'));
  
  spinner.start('连接 Lazada...');
  await sleep(1000);
  spinner.succeed(chalk.green('✓ Lazada 已连接'));
  
  console.log(chalk.green('\n✓ 所有平台已连接\n'));
  
  // 演示 2: 商品同步
  console.log(chalk.bold('2️⃣ 商品同步演示\n'));
  
  spinner.start('从 TikTok 获取商品列表...');
  await sleep(1000);
  const products = generateMockProducts(10);
  spinner.succeed(chalk.green(`✓ 获取到 ${products.length} 个商品`));
  
  console.log(chalk.gray('\n商品列表:'));
  products.forEach((p, i) => {
    console.log(`  ${i + 1}. ${chalk.white(p.title)} - $${p.price} (${p.quantity} 件)`);
  });
  
  spinner.start('\n同步商品到 Amazon...');
  await sleep(1500);
  spinner.succeed(chalk.green('✓ 已同步 10 个商品到 Amazon'));
  
  spinner.start('同步商品到 Shopee...');
  await sleep(1500);
  spinner.succeed(chalk.green('✓ 已同步 10 个商品到 Shopee'));
  
  spinner.start('同步商品到 Lazada...');
  await sleep(1500);
  spinner.succeed(chalk.green('✓ 已同步 10 个商品到 Lazada'));
  
  console.log(chalk.green('\n✓ 商品同步完成\n'));
  
  // 演示 3: 订单管理
  console.log(chalk.bold('3️⃣ 订单管理演示\n'));
  
  spinner.start('获取各平台订单...');
  await sleep(1000);
  const orders = generateMockOrders(20);
  spinner.succeed(chalk.green(`✓ 获取到 ${orders.length} 个订单`));
  
  const byPlatform = {};
  orders.forEach(o => {
    byPlatform[o.platform] = (byPlatform[o.platform] || 0) + 1;
  });
  
  console.log(chalk.gray('\n订单分布:'));
  Object.entries(byPlatform).forEach(([platform, count]) => {
    console.log(`  ${chalk.cyan(platform)}: ${count} 单`);
  });
  
  const totalAmount = orders.reduce((sum, o) => sum + o.amount, 0);
  console.log(chalk.bold('\n销售总额:'), chalk.green(`$${totalAmount.toFixed(2)}`));
  
  // 演示 4: 智能定价
  console.log(chalk.bold('\n4️⃣ 智能定价演示\n'));
  
  spinner.start('分析各平台竞争价格...');
  await sleep(1000);
  
  console.log(chalk.gray('\n市场价格分析:'));
  console.log(`  TikTok 平均价：${chalk.cyan('$45.99')}`);
  console.log(`  Amazon 平均价：${chalk.cyan('$52.99')}`);
  console.log(`  Shopee 平均价：${chalk.cyan('$38.99')}`);
  console.log(`  Lazada 平均价：${chalk.cyan('$41.99')}`);
  
  spinner.start('\n生成定价建议...');
  await sleep(1000);
  
  console.log(chalk.green('\n定价建议:'));
  console.log(`  建议售价：${chalk.green('$49.99')}`);
  console.log(`  预期利润率：${chalk.yellow('35%')}`);
  console.log(`  竞争力指数：${chalk.cyan('85/100')}`);
  
  // 演示 5: 库存同步
  console.log(chalk.bold('\n5️⃣ 库存同步演示\n'));
  
  spinner.start('检查各平台库存...');
  await sleep(1000);
  
  const lowStock = [
    { sku: 'SKU-001', platform: 'TikTok', quantity: 5 },
    { sku: 'SKU-003', platform: 'Amazon', quantity: 3 },
    { sku: 'SKU-007', platform: 'Shopee', quantity: 8 }
  ];
  
  console.log(chalk.red(`\n⚠️ 发现 ${lowStock.length} 个低库存商品:\n`));
  lowStock.forEach(item => {
    console.log(`  ${chalk.yellow(item.sku)} (${item.platform}): ${chalk.red(item.quantity)} 件`);
  });
  
  spinner.start('\n同步库存到所有平台...');
  await sleep(1500);
  spinner.succeed(chalk.green('✓ 库存同步完成'));
  
  // 演示 6: 数据报表
  console.log(chalk.bold('\n6️⃣ 数据报表演示\n'));
  
  spinner.start('生成销售报表...');
  await sleep(1000);
  
  console.log(chalk.green('\n📊 本周销售报表:\n'));
  console.log(`  总销售额：${chalk.green('$12,450.00')}`);
  console.log(`  总订单数：${chalk.cyan('287')}`);
  console.log(`  平均客单价：${chalk.yellow('$43.38')}`);
  console.log(`  同比增长：${chalk.green('+15.3%')}`);
  
  console.log(chalk.bold('\n按平台销售:'));
  console.log(`  TikTok:  $4,230.00 (34%)`);
  console.log(`  Amazon:  $4,890.00 (39%)`);
  console.log(`  Shopee:  $2,150.00 (17%)`);
  console.log(`  Lazada:  $1,180.00 (10%)`);
  
  // 演示 7: 飞书集成
  console.log(chalk.bold('\n7️⃣ 飞书多维表格集成演示\n'));
  
  spinner.start('同步数据到飞书多维表格...');
  await sleep(1500);
  
  console.log(chalk.green('\n✓ 飞书多维表格已更新:\n'));
  console.log(`  📦 商品管理：${chalk.cyan('40')} 条记录`);
  console.log(`  🛒 订单管理：${chalk.cyan('287')} 条记录`);
  console.log(`  📊 库存管理：${chalk.cyan('40')} 条记录`);
  console.log(`  💰 定价建议：${chalk.cyan('10')} 条记录`);
  console.log(`  📈 数据报表：${chalk.cyan('4')} 条记录`);
  
  // 完成
  console.log(chalk.gray('\n' + '='.repeat(60)));
  console.log(chalk.bold.green('\n✅ 演示完成！\n'));
  
  console.log(chalk.cyan('下一步:\n'));
  console.log('  1. 运行 ' + chalk.white('crossborder-ecom init') + ' 初始化配置');
  console.log('  2. 配置各平台 API 密钥');
  console.log('  3. 运行 ' + chalk.white('crossborder-ecom sync --all') + ' 开始同步\n');
  
  console.log(chalk.gray('📖 详细文档：https://clawhub.com/skills/crossborder-ecom-hub/docs\n'));
}

// 生成模拟商品
function generateMockProducts(count) {
  const products = [];
  for (let i = 1; i <= count; i++) {
    products.push({
      id: `prod_${i}`,
      sku: `SKU-${String(i).padStart(3, '0')}`,
      title: `Product ${i}`,
      price: (Math.random() * 50 + 20).toFixed(2),
      cost: (Math.random() * 30 + 10).toFixed(2),
      quantity: Math.floor(Math.random() * 100),
      platform: 'tiktok'
    });
  }
  return products;
}

// 生成模拟订单
function generateMockOrders(count) {
  const platforms = ['tiktok', 'amazon', 'shopee', 'lazada'];
  const statuses = ['pending', 'processing', 'shipped', 'delivered'];
  const orders = [];
  
  for (let i = 1; i <= count; i++) {
    orders.push({
      id: `order_${i}`,
      platform: platforms[Math.floor(Math.random() * platforms.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      amount: (Math.random() * 100 + 20).toFixed(2),
      createdAt: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString()
    });
  }
  
  return orders;
}

// 延迟函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 运行演示
demo().catch(console.error);
