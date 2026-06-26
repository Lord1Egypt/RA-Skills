#!/usr/bin/env node

const { program } = require('commander');
const Configstore = require('configstore');
const axios = require('axios');
const chalk = require('chalk');
const inquirer = require('inquirer');

const config = new Configstore('devops-platform');
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
      console.log(chalk.green('✓ 后端地址已保存'));
    }
    
    if (options.token) {
      config.set('token', options.token);
      console.log(chalk.green('✓ Token已保存'));
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
        console.log(chalk.green('✓ 后端地址已保存'));
      }
      
      if (answers.token) {
        config.set('token', answers.token);
        console.log(chalk.green('✓ Token已保存'));
      }
    }
    
    console.log(chalk.blue('\n当前配置:'));
    console.log(`后端地址: ${config.get('baseUrl') || '未设置'}`);
    console.log(`Token: ${config.get('token') ? '***' + config.get('token').slice(-4) : '未设置'}`);
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
      console.log(chalk.red('错误: 请先使用 devops-platform config 命令配置API地址和Token'));
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
      
      console.log(chalk.blue('正在获取研发迭代列表...'));
      
      const response = await axios.get(url, {
        params,
        headers: {
          'authorization': `Bearer ${token}`,
          'from': 'openapi',
          'content-type': 'application/json'
        }
      });
      
      if (response.data && response.data.success) {
        const data = response.data.data;
        console.log(chalk.green(`✓ 获取成功 (共 ${data.total} 条)`));
        console.log(chalk.blue('\n迭代列表:'));
        
        if (data.list && data.list.length > 0) {
          data.list.forEach((item, index) => {
            console.log(chalk.yellow(`\n${index + 1}. ${item.publishPlanName || '未命名'}`));
            console.log(`   ID: ${item.id}`);
            console.log(`   状态: ${item.status || '未知'}`);
            console.log(`   应用ID: ${item.appId || '未设置'}`);
            console.log(`   发布时间: ${item.publishTime || '未设置'}`);
            console.log(`   创建时间: ${item.createTime || '未设置'}`);
          });
        } else {
          console.log(chalk.yellow('暂无迭代数据'));
        }
      } else {
        console.log(chalk.red('获取失败:'), response.data?.message || '未知错误');
      }
    } catch (error) {
      console.log(chalk.red('请求失败:'), error.message);
      if (error.response) {
        console.log(chalk.red('状态码:'), error.response.status);
        console.log(chalk.red('响应数据:'), JSON.stringify(error.response.data, null, 2));
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
      console.log(chalk.red('错误: 请先使用 devops-platform config 命令配置API地址和Token'));
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
      
      console.log(chalk.blue('正在获取应用列表...'));
      
      const response = await axios.get(url, {
        params,
        headers: {
          'authorization': `Bearer ${token}`,
          'from': 'openapi',
          'content-type': 'application/json'
        }
      });
      
      if (response.data && response.data.success) {
        const data = response.data.data;
        console.log(chalk.green(`✓ 获取成功 (共 ${data.total} 条)`));
        console.log(chalk.blue('\n应用列表:'));
        
        if (data.list && data.list.length > 0) {
          data.list.forEach((item, index) => {
            console.log(chalk.yellow(`\n${index + 1}. ${item.appName || '未命名'}`));
            console.log(`   ID: ${item.id}`);
            console.log(`   状态: ${item.appStatus || '未知'}`);
            console.log(`   应用编码: ${item.appCode || '未设置'}`);
            console.log(`   负责人: ${item.ownerName || '未设置'}`);
            console.log(`   创建时间: ${item.createTime || '未设置'}`);
          });
        } else {
          console.log(chalk.yellow('暂无应用数据'));
        }
      } else {
        console.log(chalk.red('获取失败:'), response.data?.message || '未知错误');
      }
    } catch (error) {
      console.log(chalk.red('请求失败:'), error.message);
      if (error.response) {
        console.log(chalk.red('状态码:'), error.response.status);
        console.log(chalk.red('响应数据:'), JSON.stringify(error.response.data, null, 2));
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
    
    console.log(chalk.blue('DevOps平台配置状态:'));
    console.log(`后端地址: ${baseUrl ? chalk.green(baseUrl) : chalk.red('未设置')}`);
    console.log(`Token: ${token ? chalk.green('已设置 (***' + token.slice(-4) + ')') : chalk.red('未设置')}`);
    
    if (!baseUrl || !token) {
      console.log(chalk.yellow('\n提示: 使用 devops-platform config 命令进行配置'));
    }
  });

program.parse(process.argv);