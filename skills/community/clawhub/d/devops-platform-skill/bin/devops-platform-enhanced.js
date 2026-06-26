#!/usr/bin/env node

const { program } = require('commander');
const axios = require('axios');
const inquirer = require('inquirer');
const fs = require('fs');
const path = require('path');

// 简单的颜色输出
const colors = {
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  red: (text) => `\x1b[31m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
  cyan: (text) => `\x1b[36m${text}\x1b[0m`,
  magenta: (text) => `\x1b[35m${text}\x1b[0m`,
  gray: (text) => `\x1b[90m${text}\x1b[0m`,
  white: (text) => `\x1b[37m${text}\x1b[0m`
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

  delete(key) {
    delete this.config[key];
    return this.save();
  }

  clear() {
    this.config = {};
    return this.save();
  }
}

const config = new SimpleConfig();
const pkg = require('../package.json');

// API基础URL
const getBaseUrl = () => {
  const baseUrl = config.get('baseUrl');
  if (!baseUrl) {
    console.log(colors.red('错误: 请先配置API地址'));
    console.log(colors.yellow('提示: 运行 devops-platform config 进行配置'));
    return null;
  }
  return baseUrl;
};

// 获取Token
const getToken = () => {
  const token = config.get('token');
  if (!token) {
    console.log(colors.red('错误: 请先配置Token'));
    console.log(colors.yellow('提示: 运行 devops-platform config 进行配置'));
    return null;
  }
  return token;
};

// 通用API请求函数
const makeRequest = async (endpoint, params = {}, method = 'GET') => {
  const baseUrl = getBaseUrl();
  const token = getToken();
  
  if (!baseUrl || !token) {
    return null;
  }

  try {
    // 添加代理前缀
    const proxyPrefix = '/proxy/devopsmng';
    const url = `${baseUrl}${proxyPrefix}${endpoint}`;
    
    console.log(colors.gray(`请求URL: ${url}`));
    if (Object.keys(params).length > 0) {
      console.log(colors.gray(`参数: ${JSON.stringify(params)}`));
    }
    
    const config = {
      headers: {
        'authorization': `Bearer ${token}`,
        'from': 'openapi',
        'content-type': 'application/json'
      },
      timeout: 15000
    };

    let response;
    if (method === 'GET') {
      response = await axios.get(url, { ...config, params });
    } else if (method === 'POST') {
      response = await axios.post(url, params, config);
    } else if (method === 'PUT') {
      response = await axios.put(url, params, config);
    } else if (method === 'DELETE') {
      response = await axios.delete(url, { ...config, params });
    }

    return response.data;
  } catch (error) {
    console.log(colors.red('请求失败:'), error.message);
    if (error.response) {
      console.log(colors.red('状态码:'), error.response.status);
      console.log(colors.red('响应数据:'), JSON.stringify(error.response.data, null, 2));
    } else if (error.request) {
      console.log(colors.red('无响应:'), '请求已发送但未收到响应');
    }
    return null;
  }
};

// 显示表格数据
const displayTable = (title, data, fields) => {
  console.log(colors.blue(`\n${title}:`));
  
  if (!data || data.length === 0) {
    console.log(colors.yellow('暂无数据'));
    return;
  }

  data.forEach((item, index) => {
    console.log(colors.yellow(`\n${index + 1}. ${item.name || item.title || item.appName || '未命名'}`));
    
    fields.forEach(field => {
      if (item[field.key] !== undefined && item[field.key] !== null) {
        const label = field.label || field.key;
        const value = item[field.key];
        console.log(`   ${label}: ${value}`);
      }
    });
  });
};

program
  .name('devops-platform')
  .description('DevOps效能平台CLI工具 - 增强版')
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
      }
      if (answers.token) {
        config.set('token', answers.token);
      }
      
      console.log(colors.green('✓ 配置已保存'));
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

// 1. 查询发布窗口列表
program
  .command('pub-windows')
  .description('查询发布窗口列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .option('--status <status>', '窗口状态')
  .option('--window-date <date>', '发布窗口日期')
  .option('--ops <name>', '运维值班人')
  .action(async (options) => {
    console.log(colors.blue('正在查询发布窗口列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size
    };
    
    if (options.status) params.status = options.status;
    if (options.windowDate) params.windowDate = options.windowDate;
    if (options.ops) params.ops = options.ops;
    
    const result = await makeRequest('/publish/pubwindow/list', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('发布窗口列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'windowDate', label: '窗口日期' },
        { key: 'status', label: '状态' },
        { key: 'ops', label: '运维值班人' },
        { key: 'createTime', label: '创建时间' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 2. 查询研发迭代列表
program
  .command('iterations')
  .description('查询研发迭代列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .option('--search <value>', '搜索条件')
  .option('--status <status>', '状态筛选')
  .option('--app-ids <ids>', '应用ID筛选（逗号分隔）')
  .action(async (options) => {
    console.log(colors.blue('正在查询研发迭代列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size,
      searchValue: options.search || 'pub_stage < 8',
      status: options.status || '',
      appIds: options.appIds || '',
      interTypeList: ''
    };
    
    const result = await makeRequest('/publish/publishplan/list', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('研发迭代列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'planName', label: '迭代名称' },
        { key: 'planType', label: '迭代类型' },
        { key: 'pubStage', label: '发布阶段' },
        { key: 'status', label: '状态' },
        { key: 'createTime', label: '创建时间' },
        { key: 'ownerName', label: '负责人' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 3. 查询我的研发迭代列表
program
  .command('my-iterations')
  .description('查询我的研发迭代列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .action(async (options) => {
    console.log(colors.blue('正在查询我的研发迭代列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size
    };
    
    const result = await makeRequest('/publish/publishplan/myplanlist', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('我的研发迭代列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'planName', label: '迭代名称' },
        { key: 'planType', label: '迭代类型' },
        { key: 'pubStage', label: '发布阶段' },
        { key: 'status', label: '状态' },
        { key: 'createTime', label: '创建时间' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 4. 查询应用列表
program
  .command('apps')
  .description('查询应用列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '10')
  .option('--status <status>', '应用状态', 'ONLINE_RUN,OFFLINE_RUN,APPLYING,CODING')
  .action(async (options) => {
    console.log(colors.blue('正在查询应用列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size,
      appStatus: options.status,
      'interTypeList[0]': 'base'
    };
    
    const result = await makeRequest('/application/app/list', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('应用列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'appName', label: '应用名称' },
        { key: 'appStatus', label: '状态' },
        { key: 'serviceName', label: '服务名称' },
        { key: 'devOwner', label: '负责人' },
        { key: 'projectType', label: '项目类型' },
        { key: 'deployType', label: '部署类型' },
        { key: 'createdTime', label: '创建时间' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 5. 查询发布任务列表
program
  .command('pub-tasks')
  .description('查询发布任务列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .option('--plan-id <id>', '迭代ID')
  .option('--status <status>', '任务状态')
  .action(async (options) => {
    console.log(colors.blue('正在查询发布任务列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size
    };
    
    if (options.planId) params.planId = options.planId;
    if (options.status) params.status = options.status;
    
    const result = await makeRequest('/publish/pubtask/list', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('发布任务列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'taskName', label: '任务名称' },
        { key: 'planName', label: '所属迭代' },
        { key: 'appName', label: '应用名称' },
        { key: 'status', label: '状态' },
        { key: 'createTime', label: '创建时间' },
        { key: 'ownerName', label: '负责人' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 6. 查询发布记录列表
program
  .command('pub-records')
  .description('查询发布记录列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .option('--task-id <id>', '任务ID')
  .option('--status <status>', '发布状态')
  .action(async (options) => {
    console.log(colors.blue('正在查询发布记录列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size
    };
    
    if (options.taskId) params.taskId = options.taskId;
    if (options.status) params.status = options.status;
    
    const result = await makeRequest('/publish/pubrecord/list', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('发布记录列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'recordName', label: '记录名称' },
        { key: 'taskName', label: '所属任务' },
        { key: 'appName', label: '应用名称' },
        { key: 'status', label: '状态' },
        { key: 'createTime', label: '创建时间' },
        { key: 'publishTime', label: '发布时间' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 7. 查询染色环境涉及的应用列表
program
  .command('staging-apps')
  .description('查询染色环境涉及的应用列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .action(async (options) => {
    console.log(colors.blue('正在查询染色环境应用列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size
    };
    
    const result = await makeRequest('/publish/publishplan/stagingapplist', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('染色环境应用列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'appName', label: '应用名称' },
        { key: 'serviceName', label: '服务名称' },
        { key: 'appStatus', label: '状态' },
        { key: 'devOwner', label: '负责人' },
        { key: 'projectType', label: '项目类型' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 8. 获取应用详细信息
program
  .command('app-detail')
  .description('获取应用详细信息')
  .requiredOption('--id <id>', '应用ID')
  .action(async (options) => {
    console.log(colors.blue(`正在查询应用 ${options.id} 的详细信息...`));
    
    const result = await makeRequest(`/application/app/${options.id}`);
    
    if (result && result.code === 200) {
      const data = result.data || {};
      
      console.log(colors.green(`✓ 查询成功`));
      console.log(colors.blue('\n应用详细信息:'));
      
      const fields = [
        { key: 'id', label: 'ID' },
        { key: 'appName', label: '应用名称' },
        { key: 'appCnName', label: '中文名' },
        { key: 'serviceName', label: '服务名称' },
        { key: 'appStatus', label: '状态' },
        { key: 'devOwner', label: '开发负责人' },
        { key: 'testOwner', label: '测试负责人' },
        { key: 'productOwner', label: '产品负责人' },
        { key: 'projectType', label: '项目类型' },
        { key: 'deployType', label: '部署类型' },
        { key: 'gitlabUrl', label: 'GitLab地址' },
        { key: 'createdTime', label: '创建时间' },
        { key: 'updatedTime', label: '更新时间' }
      ];
      
      fields.forEach(field => {
        if (data[field.key] !== undefined && data[field.key] !== null) {
          console.log(`${field.label}: ${colors.cyan(data[field.key])}`);
        }
      });
      
      // 显示额外信息
      if (data.description) {
        console.log(`\n${colors.blue('描述:')} ${data.description}`);
      }
      
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 9. 查询研发迭代下应用列表
program
  .command('iteration-apps')
  .description('查询研发迭代下应用列表')
  .requiredOption('--plan-id <id>', '迭代ID')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .action(async (options) => {
    console.log(colors.blue(`正在查询迭代 ${options.planId} 下的应用列表...`));
    
    const params = {
      planId: options.planId,
      pageNum: options.page,
      pageSize: options.size
    };
    
    const result = await makeRequest('/publish/publishplan/applist', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('迭代应用列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'appName', label: '应用名称' },
        { key: 'appStatus', label: '状态' },
        { key: 'serviceName', label: '服务名称' },
        { key: 'devOwner', label: '负责人' },
        { key: 'projectType', label: '项目类型' },
        { key: 'deployType', label: '部署类型' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 10. 收藏/取消收藏研发迭代
program
  .command('favorite-iteration')
  .description('收藏或取消收藏研发迭代')
  .requiredOption('--plan-id <id>', '迭代ID')
  .option('--remove', '取消收藏（默认是收藏）')
  .action(async (options) => {
    const action = options.remove ? '取消收藏' : '收藏';
    console.log(colors.blue(`正在${action}迭代 ${options.planId}...`));
    
    const endpoint = options.remove 
      ? '/publish/publishplan/unfavorite' 
      : '/publish/publishplan/favorite';
    
    const result = await makeRequest(endpoint, { planId: options.planId }, 'POST');
    
    if (result && result.code === 200) {
      console.log(colors.green(`✓ ${action}成功`));
      console.log(colors.cyan(`消息: ${result.msg || '操作成功'}`));
    } else {
      console.log(colors.red(`${action}失败:`), result?.msg || '未知错误');
    }
  });

// 11. 查询我收藏的研发迭代列表
program
  .command('favorites')
  .description('查询我收藏的研发迭代列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '20')
  .action(async (options) => {
    console.log(colors.blue('正在查询我收藏的研发迭代列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size
    };
    
    const result = await makeRequest('/publish/publishplan/myfavoritelist', params);
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (共 ${total} 条，本页显示 ${rows.length} 条)`));
      
      displayTable('收藏的迭代列表', rows, [
        { key: 'id', label: 'ID' },
        { key: 'planName', label: '迭代名称' },
        { key: 'planType', label: '迭代类型' },
        { key: 'pubStage', label: '发布阶段' },
        { key: 'status', label: '状态' },
        { key: 'createTime', label: '创建时间' },
        { key: 'ownerName', label: '负责人' }
      ]);
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 12. 统计信息
program
  .command('stats')
  .description('获取平台统计信息')
  .action(async () => {
    console.log(colors.blue('正在获取平台统计信息...'));
    
    // 获取应用统计
    const appsResult = await makeRequest('/application/app/list', {
      pageNum: 1,
      pageSize: 1,
      appStatus: 'ONLINE_RUN,OFFLINE_RUN,APPLYING,CODING',
      'interTypeList[0]': 'base'
    });
    
    // 获取迭代统计
    const iterationsResult = await makeRequest('/publish/publishplan/list', {
      pageNum: 1,
      pageSize: 1,
      searchValue: 'pub_stage < 8',
      status: '',
      appIds: '',
      interTypeList: ''
    });
    
    console.log(colors.green('✓ 统计信息获取成功'));
    console.log(colors.blue('\n📊 DevOps平台统计信息:'));
    console.log('='.repeat(40));
    
    if (appsResult && appsResult.code === 200) {
      console.log(`📱 应用总数: ${colors.cyan(appsResult.total || 0)}`);
    }
    
    if (iterationsResult && iterationsResult.code === 200) {
      console.log(`🔄 迭代总数: ${colors.cyan(iterationsResult.total || 0)}`);
    }
    
    // 获取发布窗口统计
    const windowsResult = await makeRequest('/publish/pubwindow/list', {
      pageNum: 1,
      pageSize: 1
    });
    
    if (windowsResult && windowsResult.code === 200) {
      console.log(`📅 发布窗口数: ${colors.cyan(windowsResult.total || 0)}`);
    }
    
    console.log('='.repeat(40));
    console.log(colors.gray('\n提示: 使用具体命令查看详细信息'));
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
      console.log(colors.red('清除失败:'), error.message);
    }
  });

// 帮助信息
program
  .command('help-all')
  .description('显示所有命令的详细帮助')
  .action(() => {
    console.log(colors.blue('📚 DevOps平台CLI工具 - 所有命令'));
    console.log('='.repeat(60));
    
    const commands = [
      { cmd: 'config', desc: '配置API地址和Token' },
      { cmd: 'status', desc: '查看当前配置状态' },
      { cmd: 'stats', desc: '获取平台统计信息' },
      { cmd: 'apps', desc: '查询应用列表' },
      { cmd: 'app-detail --id <ID>', desc: '获取应用详细信息' },
      { cmd: 'iterations', desc: '查询研发迭代列表' },
      { cmd: 'my-iterations', desc: '查询我的研发迭代列表' },
      { cmd: 'iteration-apps --plan-id <ID>', desc: '查询迭代下应用列表' },
      { cmd: 'favorites', desc: '查询收藏的迭代列表' },
      { cmd: 'favorite-iteration --plan-id <ID>', desc: '收藏迭代' },
      { cmd: 'favorite-iteration --plan-id <ID> --remove', desc: '取消收藏迭代' },
      { cmd: 'pub-windows', desc: '查询发布窗口列表' },
      { cmd: 'pub-tasks', desc: '查询发布任务列表' },
      { cmd: 'pub-records', desc: '查询发布记录列表' },
      { cmd: 'staging-apps', desc: '查询染色环境应用列表' },
      { cmd: 'clear', desc: '清除所有配置' }
    ];
    
    commands.forEach(cmd => {
      console.log(`${colors.yellow(cmd.cmd.padEnd(40))} ${cmd.desc}`);
    });
    
    console.log('='.repeat(60));
    console.log(colors.gray('\n示例:'));
    console.log('  devops-platform apps --size 20');
    console.log('  devops-platform iterations --search "test"');
    console.log('  devops-platform app-detail --id 10907');
  });

// 如果没有命令，显示帮助
if (process.argv.length <= 2) {
  program.help();
}

program.parse(process.argv);