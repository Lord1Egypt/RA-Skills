#!/usr/bin/env node

const { program } = require('commander');
const axios = require('axios');
const inquirer = require('inquirer');
const fs = require('fs');
const path = require('path');

// 颜色输出
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

// 配置管理
class Config {
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

const config = new Config();
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
const makeRequest = async (endpoint, params = {}, method = 'GET', options = {}) => {
  const baseUrl = getBaseUrl();
  const token = getToken();
  
  if (!baseUrl || !token) {
    return null;
  }

  try {
    // 判断是否需要添加代理前缀
    const useProxy = endpoint.startsWith('/proxy/') ? false : !endpoint.startsWith('/getInfo');
    const url = useProxy ? `${baseUrl}/proxy/devopsmng${endpoint}` : `${baseUrl}${endpoint}`;
    
    if (options.debug) {
      console.log(colors.gray(`请求URL: ${url}`));
      if (Object.keys(params).length > 0) {
        console.log(colors.gray(`参数: ${JSON.stringify(params)}`));
      }
    }
    
    const requestConfig = {
      headers: {
        'authorization': `Bearer ${token}`,
        'from': 'openapi',
        'content-type': 'application/json'
      },
      timeout: options.timeout || 15000
    };

    let response;
    if (method === 'GET') {
      response = await axios.get(url, { ...requestConfig, params });
    } else if (method === 'POST') {
      response = await axios.post(url, params, requestConfig);
    } else if (method === 'PUT') {
      response = await axios.put(url, params, requestConfig);
    } else if (method === 'DELETE') {
      response = await axios.delete(url, { ...requestConfig, params });
    }

    return response.data;
  } catch (error) {
    if (options.silent) return null;
    
    console.log(colors.red('请求失败:'), error.message);
    if (error.response) {
      console.log(colors.red('状态码:'), error.response.status);
      if (error.response.data) {
        console.log(colors.red('响应数据:'), JSON.stringify(error.response.data, null, 2));
      }
    } else if (error.request) {
      console.log(colors.red('无响应:'), '请求已发送但未收到响应');
    }
    return null;
  }
};

// 显示表格数据
const displayTable = (title, data, fields, options = {}) => {
  console.log(colors.blue(`\n${title}:`));
  
  if (!data || data.length === 0) {
    console.log(colors.yellow('暂无数据'));
    return;
  }

  data.forEach((item, index) => {
    const prefix = options.numbered !== false ? `${index + 1}. ` : '';
    console.log(colors.yellow(`\n${prefix}${item.name || item.title || item.appName || item.dictLabel || '未命名'}`));
    
    fields.forEach(field => {
      if (item[field.key] !== undefined && item[field.key] !== null) {
        const label = field.label || field.key;
        const value = item[field.key];
        const formattedValue = field.formatter ? field.formatter(value) : value;
        console.log(`   ${label}: ${formattedValue}`);
      }
    });
  });
};

// 字典类型映射
const DICT_TYPES = {
  'app-status': 'sg_app_status', // 应用状态
  'project-language': 'sg_project_language', // 编程语言
  'release-type': 'sg_release_type', // 发布类型
  'publish-status': 'sg_publish_status', // 发布状态
  'deploy-mode': 'sg_deploy_mode', // 部署方式
  'app-type': 'sg_app_type', // 应用类型
  'host-type': 'sg_host_type', // 部署类型
  'env-type': 'sg_env_type', // 环境类型
  'pipeline-stage': 'sg_pipeline_stage', // 流水线阶段
  'window-status': 'sg_window_status', // 发布窗口状态
  'apply-status': 'sg_apply_status', // 工单状态
  'inter-type': 'sg_inter_type', // 国际化标识
  'gitlab-type': 'sg_gitlab_type', // gitlab仓库类型
  'apply-type': 'sg_apply_type', // 工单类型
  'user-sex': 'sys_user_sex', // 用户性别
  'normal-disable': 'sys_normal_disable', // 系统开关
  'common-status': 'sys_common_status', // 系统状态
  'yes-no': 'sys_yes_no' // 系统是否
};

program
  .name('devops-platform')
  .description('DevOps效能平台CLI工具 - 完整版')
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
  .action(async () => {
    const baseUrl = config.get('baseUrl');
    const token = config.get('token');
    
    console.log(colors.blue('DevOps平台配置状态:'));
    console.log(`后端地址: ${baseUrl ? colors.green(baseUrl) : colors.red('未设置')}`);
    console.log(`Token: ${token ? colors.green('已设置 (***' + token.slice(-4) + ')') : colors.red('未设置')}`);
    console.log(`配置文件: ${CONFIG_FILE}`);
    
    if (!baseUrl || !token) {
      console.log(colors.yellow('\n提示: 使用 devops-platform config 命令进行配置'));
      return;
    }
    
    // 测试连接并获取用户信息
    console.log(colors.blue('\n正在测试连接并获取用户信息...'));
    const userInfo = await makeRequest('/getInfo', {}, 'GET', { debug: true, silent: true });
    
    if (userInfo && userInfo.code === 200) {
      const user = userInfo.user || userInfo.data;
      console.log(colors.green('✓ 连接成功'));
      console.log(`用户: ${colors.cyan(user.nickName || user.userName || '未知')}`);
      console.log(`部门: ${colors.cyan(user.dept?.deptName || '未知')}`);
      console.log(`角色: ${colors.cyan((user.roles || []).map(r => r.roleName).join(', ') || '未知')}`);
    } else {
      console.log(colors.red('✗ 连接失败或认证无效'));
    }
  });

// 1. 获取用户信息
program
  .command('user')
  .description('获取当前用户信息')
  .action(async () => {
    console.log(colors.blue('正在获取用户信息...'));
    
    const result = await makeRequest('/getInfo', {}, 'GET', { debug: true });
    
    if (result && result.code === 200) {
      const user = result.user || result.data;
      console.log(colors.green('✓ 获取成功'));
      
      console.log(colors.blue('\n👤 用户信息:'));
      console.log('='.repeat(40));
      console.log(`用户ID: ${colors.cyan(user.userId || '未知')}`);
      console.log(`用户名: ${colors.cyan(user.userName || '未知')}`);
      console.log(`昵称: ${colors.cyan(user.nickName || '未知')}`);
      console.log(`邮箱: ${colors.cyan(user.email || '未知')}`);
      console.log(`手机: ${colors.cyan(user.phonenumber || '未知')}`);
      console.log(`性别: ${colors.cyan(user.sex === '0' ? '男' : user.sex === '1' ? '女' : '未知')}`);
      
      if (user.dept) {
        console.log(`部门: ${colors.cyan(user.dept.deptName || '未知')}`);
        console.log(`部门ID: ${colors.cyan(user.dept.deptId || '未知')}`);
      }
      
      if (user.roles && user.roles.length > 0) {
        console.log(`角色: ${colors.cyan(user.roles.map(r => r.roleName).join(', '))}`);
      }
      
      console.log(`创建时间: ${colors.cyan(user.createTime || '未知')}`);
      console.log('='.repeat(40));
    } else {
      console.log(colors.red('获取失败:'), result?.msg || '未知错误');
    }
  });

// 2. 查询字典数据
program
  .command('dict')
  .description('查询字典数据')
  .argument('[type]', '字典类型 (app-status, project-language, release-type等)', 'app-status')
  .action(async (type) => {
    const dictType = DICT_TYPES[type] || type;
    console.log(colors.blue(`正在查询字典: ${type} (${dictType})...`));
    
    const result = await makeRequest(`/system/dict/data/type/${dictType}`, {}, 'GET', { debug: true });
    
    if (result && result.code === 200) {
      const data = result.data || [];
      console.log(colors.green(`✓ 查询成功 (共 ${data.length} 条)`));
      
      displayTable('字典数据', data, [
        { key: 'dictCode', label: '编码' },
        { key: 'dictValue', label: '值' },
        { key: 'dictLabel', label: '标签' },
        { key: 'dictSort', label: '排序' },
        { key: 'status', label: '状态', formatter: (v) => v === '0' ? colors.green('正常') : colors.red('停用') }
      ], { numbered: false });
      
      // 显示字典类型说明
      const typeNames = {
        'sg_app_status': '应用状态',
        'sg_project_language': '编程语言',
        'sg_release_type': '发布类型',
        'sg_publish_status': '发布状态',
        'sg_deploy_mode': '部署方式',
        'sg_app_type': '应用类型',
        'sg_host_type': '部署类型',
        'sg_env_type': '环境类型',
        'sg_pipeline_stage': '流水线阶段',
        'sg_window_status': '发布窗口状态',
        'sg_apply_status': '工单状态',
        'sg_inter_type': '国际化标识',
        'sg_gitlab_type': 'GitLab仓库类型',
        'sg_apply_type': '工单类型',
        'sys_user_sex': '用户性别',
        'sys_normal_disable': '系统开关',
        'sys_common_status': '系统状态',
        'sys_yes_no': '系统是否'
      };
      
      console.log(colors.gray(`\n字典类型: ${typeNames[dictType] || dictType}`));
    } else {
      console.log(colors.red('查询失败:'), result?.msg || '未知错误');
    }
  });

// 3. 列出所有字典类型
program
  .command('dict-types')
  .description('列出所有可用的字典类型')
  .action(() => {
    console.log(colors.blue('📚 可用字典类型:'));
    console.log('='.repeat(60));
    
    Object.entries(DICT_TYPES).forEach(([key, value]) => {
      const typeNames = {
        'sg_app_status': '应用状态',
        'sg_project_language': '编程语言',
        'sg_release_type': '发布类型',
        'sg_publish_status': '发布状态',
        'sg_deploy_mode': '部署方式',
        'sg_app_type': '应用类型',
        'sg_host_type': '部署类型',
        'sg_env_type': '环境类型',
        'sg_pipeline_stage': '流水线阶段',
        'sg_window_status': '发布窗口状态',
        'sg_apply_status': '工单状态',
        'sg_inter_type': '国际化标识',
        'sg_gitlab_type': 'GitLab仓库类型',
        'sg_apply_type': '工单类型',
        'sys_user_sex': '用户性别',
        'sys_normal_disable': '系统开关',
        'sys_common_status': '系统状态',
        'sys_yes_no': '系统是否'
      };
      
      console.log(`${colors.yellow(key.padEnd(20))} ${colors.cyan(value.padEnd(30))} ${typeNames[value] || ''}`);
    });
    
    console.log('='.repeat(60));
    console.log(colors.gray('\n使用示例:'));
    console.log('  devops-platform dict app-status');
    console.log('  devops-platform dict project-language');
    console.log('  devops-platform dict sg_app_status');
  });

// 4. 查询应用列表
program
  .command('apps')
  .description('查询应用列表')
  .option('-p, --page <number>', '页码', '1')
  .option('-s, --size <number>', '每页大小', '10')
  .option('--status <status>', '应用状态 (多个用逗号分隔)', 'ONLINE_RUN,OFFLINE_RUN,APPLYING,CODING')
  .option('--search <keyword>', '搜索关键词')
  .action(async (options) => {
    console.log(colors.blue('正在查询应用列表...'));
    
    const params = {
      pageNum: options.page,
      pageSize: options.size,
      appStatus: options.status,
      'interTypeList[0]': 'base'
    };
    
    if (options.search) {
      params.searchValue = options.search;
    }
    
    const result = await makeRequest('/application/app/list', params, 'GET', { debug: true });
    
    if (result && result.code === 200) {
      const total = result.total || 0;
      const rows = result.rows || [];
      
      console.log(colors.green(`✓ 查询成功 (