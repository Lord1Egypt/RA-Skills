#!/usr/bin/env node

/**
 * 百度网盘 Skill for OpenClaw
 * 
 * 主入口文件
 * 
 * 使用方式：
 * npx baidu-netdisk-skill <command> [options]
 */

const { Command } = require('commander');
const ora = require('ora');
const chalk = require('chalk');
const Conf = require('conf');
const BaiduNetdiskAPI = require('./baidu-api');
const path = require('path');
const fs = require('fs');

const program = new Command();
const config = new Conf({ projectName: 'baidu-netdisk-skill' });

program
  .name('baidu-netdisk-skill')
  .description('百度网盘 Skill - 安全、省 Token、云端友好')
  .version('0.1.0');

// 配置命令
program
  .command('config')
  .description('配置百度 API 密钥')
  .option('-k, --apikey <key>', 'API Key')
  .option('-s, --secret <secret>', 'Secret Key')
  .option('-t, --token <token>', 'Access Token')
  .option('-r, --refresh <refresh>', 'Refresh Token')
  .action(async (options) => {
    console.log(chalk.blue('🔧 配置百度 API 密钥\n'));
    
    if (options.apikey) config.set('apiKey', options.apikey);
    if (options.secret) config.set('secretKey', options.secret);
    if (options.token) config.set('accessToken', options.token);
    if (options.refresh) config.set('refreshToken', options.refresh);
    
    // 检查配置是否完整
    const apiKey = config.get('apiKey');
    const secretKey = config.get('secretKey');
    const accessToken = config.get('accessToken');
    const refreshToken = config.get('refreshToken');
    
    if (apiKey && secretKey && accessToken) {
      console.log(chalk.green('✅ 配置完成！'));
      console.log(`API Key: ${apiKey.slice(0, 8)}...`);
      console.log(`Access Token: ${accessToken.slice(0, 8)}...`);
    } else {
      console.log(chalk.yellow('⚠️  配置不完整，请运行：'));
      console.log('npx baidu-netdisk-skill config -k <apikey> -s <secret> -t <token> -r <refresh>');
    }
  });

// 列出文件
program
  .command('list [dir]')
  .description('列出指定目录的文件')
  .option('-l, --limit <number>', '返回数量', '100')
  .option('-t, --type <type>', '文件类型：all|folder|file', 'all')
  .action(async (dir = '/', options) => {
    const spinner = ora('正在获取文件列表...').start();
    
    try {
      const api = getAPI();
      const result = await api.listFiles(dir, 0, parseInt(options.limit), options.type);
      
      spinner.succeed('获取成功！');
      console.log(`\n📁 目录：${dir}`);
      console.log(`📊 共 ${result.list.length} 个文件\n`);
      
      result.list.forEach(file => {
        const icon = file.isdir ? '📁' : '📄';
        const size = file.isdir ? '-' : formatSize(file.size);
        const time = new Date(file.server_mtime * 1000).toLocaleString('zh-CN');
        const fsId = file.fs_id || '-';
        
        console.log(`${icon} ${file.server_filename.padEnd(40)} ${size.padStart(10)}  ${time}`);
        console.log(`   fs_id: ${fsId}`);
      });
    } catch (error) {
      spinner.fail('获取失败');
      console.error(chalk.red(error.message));
    }
  });

// 搜索文件
program
  .command('search <keyword>')
  .description('搜索文件')
  .option('-d, --dir <dir>', '搜索目录', '/')
  .action(async (keyword, options) => {
    const spinner = ora(`正在搜索 "${keyword}"...`).start();
    
    try {
      const api = getAPI();
      const result = await api.searchFile(keyword, options.dir);
      
      spinner.succeed('搜索完成！');
      console.log(`\n🔍 关键词：${keyword}`);
      console.log(`📊 找到 ${result.list?.length || 0} 个文件\n`);
      
      if (result.list && result.list.length > 0) {
        result.list.forEach(file => {
          const icon = file.isdir ? '📁' : '📄';
          const size = file.isdir ? '-' : formatSize(file.size);
          console.log(`${icon} ${file.path}`);
          console.log(`   ${size}  ${new Date(file.server_mtime * 1000).toLocaleString('zh-CN')}`);
        });
      } else {
        console.log(chalk.yellow('未找到相关文件'));
      }
    } catch (error) {
      spinner.fail('搜索失败');
      console.error(chalk.red(error.message));
    }
  });

// 获取下载链接
program
  .command('download <fsId>')
  .description('获取文件下载链接（不直接下载）')
  .action(async (fsId) => {
    const spinner = ora('正在获取下载链接...').start();
    
    try {
      const api = getAPI();
      const link = await api.getDownloadLink(fsId);
      
      spinner.succeed('获取成功！');
      console.log(`\n📥 下载链接：${link}`);
      console.log(chalk.yellow('\n提示：使用下载工具下载此链接'));
    } catch (error) {
      spinner.fail('获取失败');
      console.error(chalk.red(error.message));
    }
  });

// 上传文件
program
  .command('upload <localPath> <remotePath>')
  .description('上传文件到百度网盘')
  .action(async (localPath, remotePath) => {
    const spinner = ora('正在上传文件...').start();
    
    try {
      // 检查本地文件是否存在
      if (!fs.existsSync(localPath)) {
        throw new Error(`本地文件不存在：${localPath}`);
      }
      
      const api = getAPI();
      const result = await api.uploadFile(localPath, remotePath);
      
      spinner.succeed('上传成功！');
      console.log(`\n📤 本地：${localPath}`);
      console.log(`☁️  云端：${remotePath}`);
      console.log(`📊 大小：${formatSize(fs.statSync(localPath).size)}`);
    } catch (error) {
      spinner.fail('上传失败');
      console.error(chalk.red(error.message));
    }
  });

// 清空缓存
program
  .command('clear-cache')
  .description('清空缓存')
  .action(() => {
    const api = getAPI();
    api.clearCache();
  });

// 显示用户信息
program
  .command('whoami')
  .description('显示当前用户信息')
  .action(async () => {
    const spinner = ora('正在获取用户信息...').start();
    
    try {
      const api = getAPI();
      const user = await api.getUserInfo();
      
      spinner.succeed('获取成功！');
      console.log(`\n👤 百度账号：${user.baidu_name || user.netdisk_name}`);
      console.log(`🆔 用户 ID：${user.uk}`);
      console.log(`💎 会员类型：${user.vip_type === 0 ? '普通用户' : user.vip_type === 1 ? 'VIP' : 'SVIP'}`);
      console.log(`🔗 头像：${user.avatar_url}`);
    } catch (error) {
      spinner.fail('获取失败');
      console.error(chalk.red(error.message));
    }
  });

// 帮助信息
program.on('command:*', () => {
  console.error('未知命令：%s', program.args.join(' '));
  console.error('运行 baidu-netdisk-skill --help 查看可用命令');
  process.exit(1);
});

program.parse(process.argv);

// 辅助函数

function getAPI() {
  const apiKey = config.get('apiKey');
  const secretKey = config.get('secretKey');
  const accessToken = config.get('accessToken');
  const refreshToken = config.get('refreshToken');
  
  if (!apiKey || !secretKey || !accessToken) {
    throw new Error('请先配置 API 密钥：npx baidu-netdisk-skill config');
  }
  
  return new BaiduNetdiskAPI({
    apiKey,
    secretKey,
    accessToken,
    refreshToken
  });
}

function formatSize(bytes) {
  if (!bytes || bytes === 0) return '-';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let i = 0;
  while (bytes >= 1024 && i < units.length - 1) {
    bytes /= 1024;
    i++;
  }
  return `${bytes.toFixed(2)} ${units[i]}`;
}
