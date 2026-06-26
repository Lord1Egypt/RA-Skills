/**
 * 平台管理命令 - 平台配置管理
 * 添加、移除、检查各电商平台连接状态
 */

const chalk = require('chalk');
const ora = require('ora');
const { PlatformManager } = require('../src/platforms');

async function execute(options) {
  const spinner = ora('准备平台管理...').start();
  
  try {
    console.log(chalk.bold.cyan('\n🔧 平台配置管理\n'));
    
    const platformManager = new PlatformManager();
    
    // 列出已配置平台
    if (options.list) {
      spinner.text = '获取平台配置...';
      
      const platforms = await platformManager.listPlatforms();
      
      spinner.succeed(chalk.green('✓ 获取平台配置完成'));
      
      console.log(chalk.bold('\n📋 已配置平台:\n'));
      
      if (platforms.length === 0) {
        console.log(chalk.gray('  暂无配置平台'));
        console.log(chalk.yellow('\n使用 crossborder-ecom platform --add <platform> 添加平台\n'));
        return;
      }
      
      platforms.forEach((p, index) => {
        const statusIcon = p.connected ? chalk.green('✓') : chalk.red('✗');
        console.log(`${index + 1}. ${chalk.cyan(p.name)} ${statusIcon}`);
        console.log(`   API Key: ${p.apiKey ? chalk.gray('已配置') : chalk.red('未配置')}`);
        console.log(`   状态：${p.connected ? chalk.green('已连接') : chalk.red('未连接')}`);
        console.log(`   最后同步：${p.lastSync ? chalk.gray(p.lastSync) : chalk.gray('从未')}\n`);
      });
      
      return platforms;
    }
    
    // 添加平台
    if (options.add) {
      const platform = options.add.toLowerCase();
      const supportedPlatforms = ['tiktok', 'amazon', 'shopee', 'lazada'];
      
      if (!supportedPlatforms.includes(platform)) {
        console.log(chalk.red(`✗ 不支持的平台：${platform}`));
        console.log(chalk.gray(`支持的平台：${supportedPlatforms.join(', ')}\n`));
        return;
      }
      
      spinner.text = `添加 ${platform} 平台...`;
      
      // 提示用户输入 API 密钥
      console.log(chalk.yellow(`\n请配置 ${platform.toUpperCase()} API 密钥:\n`));
      console.log('  方式 1: 在配置文件中添加');
      console.log('  方式 2: 使用环境变量');
      console.log('  方式 3: 通过交互式配置\n');
      
      const config = {
        name: platform,
        apiKey: options.apiKey || '',
        connected: false,
        createdAt: new Date().toISOString()
      };
      
      await platformManager.addPlatform(config);
      
      spinner.succeed(chalk.green(`✓ ${platform} 平台已添加`));
      
      console.log(chalk.cyan('\n下一步:'));
      console.log(`  1. 配置 ${platform.toUpperCase()} API 密钥`);
      console.log(`  2. 运行 crossborder-ecom platform --status 检查连接\n`);
      
      return config;
    }
    
    // 移除平台
    if (options.remove) {
      const platform = options.remove.toLowerCase();
      
      spinner.text = `移除 ${platform} 平台...`;
      
      await platformManager.removePlatform(platform);
      
      spinner.succeed(chalk.green(`✓ ${platform} 平台已移除`));
      
      return { success: true, platform };
    }
    
    // 检查平台状态
    if (options.status) {
      spinner.text = '检查平台连接状态...';
      
      const status = await platformManager.checkStatus();
      
      spinner.succeed(chalk.green('✓ 平台状态检查完成'));
      
      console.log(chalk.bold('\n📊 平台连接状态:\n'));
      
      let connectedCount = 0;
      status.forEach(p => {
        const icon = p.connected ? chalk.green('✓') : chalk.red('✗');
        console.log(`  ${icon} ${chalk.cyan(p.name)}: ${p.connected ? chalk.green('已连接') : chalk.red('未连接')}`);
        if (p.connected) connectedCount++;
      });
      
      console.log(chalk.bold(`\n总计：${connectedCount}/${status.length} 平台已连接\n`));
      
      return status;
    }
    
    // 默认显示帮助
    console.log(chalk.yellow('请指定操作:\n'));
    console.log('  --list             列出已配置平台');
    console.log('  --add <platform>   添加平台 (tiktok|amazon|shopee|lazada)');
    console.log('  --remove <name>    移除平台');
    console.log('  --status           检查平台状态');
    console.log(chalk.gray('\n可选参数:'));
    console.log('  --api-key <key>    API 密钥\n');
    
  } catch (error) {
    spinner.fail(chalk.red('✗ 平台管理失败'));
    console.error(chalk.red(error.message));
    if (options.debug) {
      console.error(error.stack);
    }
    throw error;
  }
}

module.exports = { execute };
