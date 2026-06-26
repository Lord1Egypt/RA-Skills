#!/usr/bin/env node

/**
 * OAuth 授权配置工具
 * 
 * 交互式引导用户完成百度网盘授权
 */

const { Command } = require('commander');
const ora = require('ora');
const chalk = require('chalk');
const Conf = require('conf');
const axios = require('axios');
const readline = require('readline');
const CryptoJS = require('crypto-js');
const crypto = require('crypto');

const config = new Conf({ projectName: 'baidu-netdisk-skill' });

// AES-256 加密密钥（支持环境变量覆盖）
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || 
  crypto.createHash('sha256').update('baidu-netdisk-skill-secret-2026').digest('hex');

/**
 * AES-256 加密
 */
function encrypt(text) {
  return CryptoJS.AES.encrypt(text, ENCRYPTION_KEY).toString();
}

/**
 * AES-256 解密
 */
function decrypt(ciphertext) {
  const bytes = CryptoJS.AES.decrypt(ciphertext, ENCRYPTION_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
}
const program = new Command();

// 百度 API 配置（用我们的企业应用）
const BAIDU_CONFIG = {
  apiKey: config.get('apiKey') || process.env.BAIDU_API_KEY,
  secretKey: config.get('secretKey') || process.env.BAIDU_SECRET_KEY,
  redirectUri: 'oob' // 离线授权
};

program
  .name('baidu-netdisk-skill auth')
  .description('百度网盘 OAuth 授权配置')
  .action(async () => {
    console.log(chalk.blue('\n🔐 百度网盘 OAuth 授权\n'));
    
    // 第 1 步：生成授权 URL
    const authUrl = `https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=${BAIDU_CONFIG.apiKey}&redirect_uri=${BAIDU_CONFIG.redirectUri}&scope=basic,netdisk`;
    
    console.log('请按以下步骤完成授权：\n');
    console.log('1. 在浏览器打开以下 URL：');
    console.log(chalk.green(authUrl));
    console.log('\n2. 登录你的百度网盘账号并同意授权');
    console.log('3. 复制页面显示的 Authorization Code');
    console.log('\n---\n');
    
    // 第 2 步：等待用户输入 Code
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    const code = await new Promise((resolve) => {
      rl.question('请输入 Authorization Code: ', resolve);
    });
    
    rl.close();
    
    // 第 3 步：用 Code 换 Token
    const spinner = ora('正在获取 Token...').start();
    
    try {
      const response = await axios.post(
        'https://openapi.baidu.com/oauth/2.0/token',
        null,
        {
          params: {
            grant_type: 'authorization_code',
            code: code.trim(),
            client_id: BAIDU_CONFIG.apiKey,
            client_secret: BAIDU_CONFIG.secretKey,
            redirect_uri: BAIDU_CONFIG.redirectUri
          }
        }
      );
      
      if (response.data.error) {
        throw new Error(`${response.data.error}: ${response.data.error_description}`);
      }
      
      const { access_token, refresh_token, expires_in } = response.data;
      
      // 第 4 步：AES-256 加密保存 Token
      config.set('accessToken', encrypt(access_token));
      config.set('refreshToken', encrypt(refresh_token));
      config.set('tokenExpires', Date.now() + (expires_in * 1000));
      
      spinner.succeed('授权成功！');
      
      console.log(chalk.green('\n✅ 百度网盘授权完成！\n'));
      console.log('Token 已加密保存在本地配置文件');
      console.log(`Access Token 有效期：${Math.floor(expires_in / 86400)} 天`);
      console.log('\n你现在可以开始使用百度网盘 Skill 了！\n');
      console.log('常用命令：');
      console.log('  npx baidu-netdisk-skill whoami     # 查看用户信息');
      console.log('  npx baidu-netdisk-skill list /     # 列出根目录文件');
      console.log('  npx baidu-netdisk-skill search "关键词"  # 搜索文件\n');
      
    } catch (error) {
      spinner.fail('获取 Token 失败');
      console.error(chalk.red(`\n错误：${error.message}\n`));
      console.log('请检查 Code 是否正确，或重新运行授权命令。\n');
      process.exit(1);
    }
  });

program.parse(process.argv);
