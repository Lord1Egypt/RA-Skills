#!/usr/bin/env node
/**
 * 接口盒子 API Skill - 交互式调用助手
 * ApiHz Interactive Caller
 * 
 * @version 1.0.5
 * @changelog 支持加密的 KEY 和 DMSG
 * 
 * 两步选择：先选分类，再选 API，然后调用
 */

const path = require('path');
const { ApiHzAuth } = require('../src/auth.js');
const { ApiHzClient } = require('../src/client-enhanced.js');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function printMenu(items, title) {
  console.log(`\n${title}`);
  console.log('='.repeat(50));
  items.forEach((item, index) => {
    const num = (index + 1).toString().padStart(2, ' ');
    const name = typeof item === 'string' ? item : item.name;
    console.log(`  ${num}. ${name}`);
  });
  console.log('  0. 返回上级');
  console.log('');
}

async function selectCategory(categories) {
  while (true) {
    printMenu(categories.map(c => c.name), '📦 选择 API 分类');
    const choice = await ask('请输入分类编号: ');
    
    if (choice === '0') return null;
    
    const index = parseInt(choice) - 1;
    if (index >= 0 && index < categories.length) {
      return categories[index];
    }
    console.log('❌ 无效选择，请重试');
  }
}

async function selectApi(apis) {
  while (true) {
    printMenu(apis.map(api => {
      const free = api.mengdian === '0' ? '[免费]' : '[会员]';
      return `${api.name} ${free}`;
    }), '🔌 选择 API 接口');
    
    const choice = await ask('请输入 API 编号: ');
    
    if (choice === '0') return null;
    
    const index = parseInt(choice) - 1;
    if (index >= 0 && index < apis.length) {
      return apis[index];
    }
    console.log('❌ 无效选择，请重试');
  }
}

async function getApiParams(api) {
  const params = {};
  
  // 解析 API 说明中的参数
  const explain = api.explain || '';
  
  // 常见参数提取
  if (api.type === '天气预报' || api.name.includes('天气')) {
    params.province = await ask('省份 (默认：安徽): ') || '安徽';
    params.place = await ask('城市 (默认：芜湖): ') || '芜湖';
  } else if (api.name.includes('IP') && api.name.includes('归属')) {
    params.ip = await ask('IP 地址 (默认：114.114.114.114): ') || '114.114.114.114';
  } else if (api.name.includes('手机')) {
    params.phone = await ask('手机号: ');
  } else if (api.name.includes('ICP') || api.name.includes('备案')) {
    params.domain = await ask('域名 (例：baidu.com): ');
  } else if (api.name.includes('WHOIS')) {
    params.domain = await ask('域名 (例：baidu.com): ');
  } else if (api.name.includes('翻译')) {
    params.text = await ask('要翻译的文本: ');
    params.from = await ask('源语言 (默认：en): ') || 'en';
    params.to = await ask('目标语言 (默认：zh): ') || 'zh';
  } else if (api.name.includes('拼音')) {
    params.text = await ask('要转换的中文: ');
  } else if (api.name.includes('成语')) {
    params.idiom = await ask('成语: ');
  } else if (api.name.includes('解梦')) {
    params.keyword = await ask('关键词 (例：飞): ');
  } else if (api.name.includes('彩票')) {
    params.type = await ask('彩票类型 (默认：ssq): ') || 'ssq';
  } else if (api.name.includes('邮箱')) {
    // 临时邮箱不需要额外参数
  } else if (api.name.includes('地震')) {
    // 地震数据不需要额外参数
  } else if (api.name.includes('时间戳') || api.name.includes('时间')) {
    // 时间戳不需要额外参数
  } else if (api.name.includes('热榜') || api.name.includes('新闻')) {
    // 新闻热榜不需要额外参数
  } else if (api.name.includes('汇率') || api.name.includes('货币')) {
    // 汇率不需要额外参数
  } else if (api.name.includes('壁纸')) {
    // 壁纸不需要额外参数
  } else if (api.name.includes('历史上的今天')) {
    // 历史上的今天不需要额外参数
  } else {
    console.log('\n⚠️  该 API 需要特定参数，请参考官方文档');
  }
  
  return params;
}

async function callApi(client, api, params) {
  // 根据 API URL 映射到客户端方法
  const urlMap = {
    'tianqi/tqyb.php': 'weather',
    'tianqi/tqybip.php': 'weatherIp',
    'tianqi/dizhen.php': 'earthquake',
    'time/getapi.php': 'time',
    'ajax/ajax.php': 'ajax',
  };
  
  // 查找匹配的方法
  let methodName = null;
  for (const [urlKey, method] of Object.entries(urlMap)) {
    if (api.apiurl && api.apiurl.includes(urlKey)) {
      methodName = method;
      break;
    }
  }
  
  // 特殊处理 ajax 接口
  if (api.apiurl && api.apiurl.includes('ajax/ajax.php')) {
    const typeMap = {
      '11': 'phone',
      '12': 'ip',
      '4': 'icp',
      '7': 'whois',
      '66': 'news',
      '35': 'email',
      '41': 'translate',
      '37': 'pinyin',
      '43': 'idiom',
      '42': 'history',
      '82': 'exchange',
      '30': 'lottery',
      '71': 'dream',
      '27': 'wallpaper'
    };
    params.type = Object.keys(typeMap).find(key => typeMap[key] === methodName) || '0';
  }
  
  if (methodName && client[methodName]) {
    return await client[methodName](params);
  }
  
  // 通用调用
  const endpoint = api.apiurl;
  return await client.request(endpoint, params);
}

async function main() {
  console.log('=========================================');
  console.log('接口盒子 API - 交互式调用');
  console.log('=========================================\n');

  // 读取配置 - 使用动态路径
  const auth = new ApiHzAuth({
    workspace: process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || '', '.openclaw', 'workspace')
  });

  if (!auth.isConfigured()) {
    console.log('❌ 未检测到配置，请先运行初始化向导:');
    console.log('   node skills/apihz/scripts/init-wizard.js\n');
    rl.close();
    return;
  }

  const config = auth.readConfig();
  console.log(`✅ 已加载配置：开发者 ID ${config.id}`);

  // 获取 API 分类列表
  console.log('\n正在获取 API 分类列表...');
  const listResult = await auth.getApiList(config.id, config.key);
  
  if (!listResult.success) {
    console.log(`❌ 获取失败：${listResult.message}`);
    rl.close();
    return;
  }

  console.log(`✅ 获取到 ${listResult.categories.length} 个分类\n`);

  const client = new ApiHzClient({
    id: config.id,
    key: config.key,
    baseUrl: 'https://cn.apihz.cn'
  });

  // 主循环
  while (true) {
    // 选择分类
    const category = await selectCategory(listResult.categories);
    if (!category) {
      console.log('\n👋 退出');
      rl.close();
      return;
    }

    console.log(`\n📂 已选择分类：${category.name}`);
    console.log('正在获取 API 列表...');

    // 获取该分类下的 API 列表
    const apiListResult = await auth.getApiListByCategory(config.id, config.key, category.name);
    
    if (!apiListResult.success) {
      console.log(`❌ 获取失败：${apiListResult.message}`);
      continue;
    }

    console.log(`✅ 获取到 ${apiListResult.apis.length} 个 API\n`);

    // 选择 API
    const api = await selectApi(apiListResult.apis);
    if (!api) {
      continue;
    }

    console.log(`\n🔌 已选择 API: ${api.name}`);
    console.log(`📝 说明：${api.desc}`);
    console.log(`💰 费用：${api.mengdiantext || '免费'}`);

    // 获取参数
    console.log('\n请输入 API 参数:');
    const params = await getApiParams(api);

    // 调用 API
    console.log('\n正在调用 API...');
    try {
      const result = await callApi(client, api, params);
      console.log('\n✅ 调用成功!\n');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.log('\n❌ 调用失败:', error.message);
    }

    // 询问是否继续
    const cont = await ask('\n是否继续调用其他 API? (y/n): ');
    if (cont.toLowerCase() !== 'y') {
      console.log('\n👋 退出');
      rl.close();
      return;
    }
  }
}

main().catch(console.error);
