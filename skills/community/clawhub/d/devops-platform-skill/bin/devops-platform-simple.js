#!/usr/bin/env node

const { program } = require('commander');
const axios = require('axios');
const inquirer = require('inquirer');
const fs = require('fs');
const path = require('path');

// 简单的颜色输出（避免chalk的ESM问题）
const colors = {
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  red: (text) => `\x1b[31m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
  gray: (text) => `\x1b[90m${text}\x1b[0m`
};

const CONFIG_FILE = path.join(process.env.HOME, '.devops-platform-config.json');

// 简单的配置管理
class SimpleConfig {
  constructor() {
    this.config = {};
    this.load();
  }

  load() {
    try {
      if (fs.existsSync(CONFIG_FILE)) {
        const data = fs.readFileSync(CONFIG_FILE, 'utf8');
        this.config = JSON.parse(data);
      }
    } catch (error) {
      console.log(colors.yellow('⚠️  配置文件读取失败，将使用空配置'));
    }
  }

  save() {
    try {
      fs.writeFileSync(CONFIG_FILE, JSON.stringify(this.config, null, 2));
      return true;
    } catch (error) {
      console.log(colors.red('❌ 配置文件保存失败:'), error.message);
      return false;
    }
  }

  get(key) {
    return this.config[key];
  }

  set(key, value) {
    this.config[key] = value;
    return this.save();
  }
}

const config = new SimpleConfig();
const pkg = require('../package.json');

program
  .name('devops-platform')
  .description('DevOps效能平台CLI工具')
  .version(pkg.version);

// 配置命令
program
  .command('config')
  .description('配置API地址和Token')
  .option('-u, --base-url <url>', '后端接口地址')
  .option('-t, --token <token>', '用户Open Token')
  .action(async (options) => {
    if (options.baseUrl) {
      config.set('baseUrl', options.baseUrl);
      console.log(colors.green('✓ 后端地址已保存'));
    }
    
    if (options.token) {
      config.set('token', options.token);
      console.log(colors.green('✓ Token已保存'));
    }
    
    if (!options.baseUrl && !options.token) {
      const answers = await inquirer.prompt([
        {
          type: 'input',
          name: 'baseUrl',
          message: '请输入后端接口地址:',
          default: config.get('baseUrl') || ''
        },
        {
          type: 'input',
          name: 'token',
          message: '请输入用户Open Token:',
          default: config.get('token') || ''
        }
      ]);
      
      if (answers.baseUrl) {
        config.set('baseUrl', answers.baseUrl);
        console.log(colors.green('✓ 后端地址已保存'));
      }
      
      if (answers.token) {
        config.set('token', answers.token);
        console.log(colors.green('✓ Token已保存'));
      }
    }
    
    console.log(colors.blue('\n当前配置:'));
    console.log(`后端地址: ${config.get('baseUrl') || '未设置'}`);
    console.log(`Token: ${config.get('token') ? '***' + config.get('token').slice(-4) : '未设置'}`);
    console.log(`配置文件: ${CONFIG_FILE}`);
  });

// 获取研发迭代列表
program
  .command('iterations')
  .description('获取研发迭代列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .option('--search <value>', '搜索条件', 'pub_stage < 8')
  .action(async (options) => {
    const baseUrl = config.get('baseUrl');
    const token = config.get('token');
    
    if (!baseUrl || !token) {
      console.log(colors.red('错误: 请先使用 devops-platform config 命令配置API地址和Token'));
      console.log(colors.yellow('提示: 运行 devops-platform config 进行配置'));
      return;
    }
    
    try {
      const url = `${baseUrl}/proxy/devopsmng/publish/publishplan/list`;
      const params = {
        interTypeList: '',
        searchValue: options.search,
        status: '',
        appIds: '',
        pageNum: options.page,
        pageSize: options.size
      };
      
      console.log(colors.blue('正在获取研发迭代列表...'));
      console.log(colors.gray(`请求URL: ${url}`));
      console.log(colors.gray(`参数: ${JSON.stringify(params)}`));
      
      const response = await axios.get(url, {
        params,
        headers: {
          'authorization': `Bearer ${token}`,
          'from': 'openapi',
          'content-type': 'application/json'
        },
        timeout: 10000
      });
      
      if (response.data && response.data.success) {
        const data = response.data.data;
        console.log(colors.green(`✓ 获取成功 (共 ${data.total} 条)`));
        console.log(colors.blue('\n迭代列表:'));
        
        if (data.list && data.list.length > 0) {
          data.list.forEach((item, index) => {
            console.log(colors.yellow(`\n${index + 1}. ${item.publishPlanName || '未命名'}`));
            console.log(`   ID: ${item.id}`);
            console.log(`   状态: ${item.status || '未知'}`);
            console.log(`   应用ID: ${item.appId || '未设置'}`);
            console.log(`   发布时间: ${item.publishTime || '未设置'}`);
            console.log(`   创建时间: ${item.createTime || '未设置'}`);
          });
        } else {
          console.log(colors.yellow('暂无迭代数据'));
        }
      } else {
        console.log(colors.red('获取失败:'), response.data?.message || '未知错误');
      }
    } catch (error) {
      console.log(colors.red('请求失败:'), error.message);
      if (error.response) {
        console.log(colors.red('状态码:'), error.response.status);
        console.log(colors.red('响应数据:'), JSON.stringify(error.response.data, null, 2));
      } else if (error.request) {
        console.log(colors.red('无响应:'), '请求已发送但未收到响应');
      }
    }
  });

// 获取应用列表
program
  .command('apps')
  .description('获取应用列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '10')
  .option('--status <status>', '应用状态', 'ONLINE_RUN,OFFLINE_RUN,APPLYING,CODING')
  .action(async (options) => {
    const baseUrl = config.get('baseUrl');
    const token = config.get('token');
    
    if (!baseUrl || !token) {
      console.log(colors.red('错误: 请先使用 devops-platform config 命令配置API地址和Token'));
      console.log(colors.yellow('提示: 运行 devops-platform config 进行配置'));
      return;
    }
    
    try {
      const url = `${baseUrl}/proxy/devopsmng/application/app/list`;
      const params = {
        pageNum: options.page,
        pageSize: options.size,
        appStatus: options.status,
        'interTypeList[0]': 'base'
      };
      
      console.log(colors.blue('正在获取应用列表...'));
      console.log(colors.gray(`请求URL: ${url}`));
      console.log(colors.gray(`参数: ${JSON.stringify(params)}`));
      
      const response = await axios.get(url, {
        params,
        headers: {
          'authorization': `Bearer ${token}`,
          'from': 'openapi',
          'content-type': 'application/json'
        },
        timeout: 10000
      });
      
      // 调试信息
      // console.log('完整响应:', JSON.stringify(response.data, null, 2));
      
      if (response.data && response.data.code === 200) {
        const total = response.data.total || 0;
        const rows = response.data.rows || [];
        
        console.log(colors.green(`✓ 获取成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
        console.log(colors.blue('\n应用列表:'));
        
        if (rows.length > 0) {
          rows.forEach((item, index) => {
            console.log(colors.yellow(`\n${index + 1}. ${item.appName || '未命名'}`));
            console.log(`   ID: ${item.id}`);
            console.log(`   状态: ${item.appStatus || '未知'}`);
            console.log(`   应用编码: ${item.serviceName || item.appName || '未设置'}`);
            console.log(`   负责人: ${item.devOwner || item.ownerName || '未设置'}`);
            console.log(`   创建时间: ${item.createdTime || item.createTime || '未设置'}`);
            console.log(`   中文名: ${item.appCnName || '未设置'}`);
            console.log(`   项目类型: ${item.projectType || '未知'}`);
            console.log(`   部署类型: ${item.deployType || '未知'}`);
          });
        } else {
          console.log(colors.yellow('暂无应用数据'));
        }
      } else {
        console.log(colors.red('获取失败:'), response.data?.msg || response.data?.message || '未知错误');
        console.log('响应状态码:', response.status);
        console.log('响应code:', response.data?.code);
      }
    } catch (error) {
      console.log(colors.red('请求失败:'), error.message);
      if (error.response) {
        console.log(colors.red('状态码:'), error.response.status);
        console.log(colors.red('响应数据:'), JSON.stringify(error.response.data, null, 2));
      } else if (error.request) {
        console.log(colors.red('无响应:'), '请求已发送但未收到响应');
      }
    }
  });

// 查看配置
program
  .command('status')
  .description('查看当前配置状态')
  .action(() => {
    const baseUrl = config.get('baseUrl');
    const token = config.get('token');
    
    console.log(colors.blue('DevOps平台配置状态:'));
    console.log(`后端地址: ${baseUrl ? colors.green(baseUrl) : colors.red('未设置')}`);
    console.log(`Token: ${token ? colors.green('已设置 (***' + token.slice(-4) + ')') : colors.red('未设置')}`);
    console.log(`配置文件: ${CONFIG_FILE}`);
    
    if (!baseUrl || !token) {
      console.log(colors.yellow('\n提示: 使用 devops-platform config 命令进行配置'));
    }
  });

// 清除配置
program
  .command('clear')
  .description('清除所有配置')
  .action(() => {
    try {
      if (fs.existsSync(CONFIG_FILE)) {
        fs.unlinkSync(CONFIG_FILE);
        console.log(colors.green('✓ 配置已清除'));
      } else {
        console.log(colors.yellow('⚠️  配置文件不存在'));
      }
    } catch (error) {
      console.log(colors.red('❌ 清除配置失败:'), error.message);
    }
  });

program.parse(process.argv);