#!/usr/bin/env node
import { program } from 'commander';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import https from 'https';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config({ path: path.join(__dirname, '..', '.env') });

const API_ENDPOINT = 'https://qianfan.baidubce.com/v2/ai_search/web_search';

program
  .name('baidu-qianfan-search')
  .description('百度千帆搜索API调用工具')
  .version('1.0.0')
  .argument('<query>', '搜索关键词')
  .option('-n, --count <number>', '返回结果数量，默认20，最大50', '20')
  .option('--edition <edition>', '搜索版本：standard（完整）或 lite（轻量）', 'standard')
  .option('--time <time>', '快速时效过滤：week/month/semiyear/year')
  .option('--from <from>', '起始时间：YYYY-MM-DD或相对时间（如now-2d/d）')
  .option('--to <to>', '结束时间：YYYY-MM-DD或相对时间（如now/d）')
  .option('--site <site...>', '指定搜索站点（可重复使用）')
  .option('--block <block...>', '屏蔽搜索站点（可重复使用）')
  .option('--types <types>', '资源类型：web,image,video,aladdin，可带数量如web:10,image:5')
  .option('--safe', '开启安全搜索（过滤敏感内容）')
  .option('--config <config>', 'query干预配置ID（高级）')
  .option('--raw', '输出原始JSON响应')
  .parse(process.argv);

const options = program.opts();
const query = program.args[0];

// Get API Key
const apiKey = process.env.BAIDU_QIANFAN_API_KEY;
if (!apiKey) {
  console.error('错误：未找到BAIDU_QIANFAN_API_KEY环境变量');
  console.error('请通过以下方式之一配置：');
  console.error('  1. 环境变量：export BAIDU_QIANFAN_API_KEY="你的百度千帆API Key"');
  console.error('  2. 配置文件：在技能目录创建.env文件，内容为BAIDU_QIANFAN_API_KEY=你的API Key');
  console.error('');
  console.error('如何获取API Key：访问 https://cloud.baidu.com/ 登录后进入千帆平台，创建应用并获取AppBuilder API Key');
  process.exit(1);
}

// Build resource_type_filter
let resourceTypeFilter = [{ type: 'web', top_k: parseInt(options.count) }];
if (options.types) {
  resourceTypeFilter = options.types.split(',').map(type => {
    const [t, k] = type.split(':');
    const typeName = t.trim();
    let defaultTopK;
    switch (typeName) {
      case 'web': defaultTopK = 20; break;
      case 'image': defaultTopK = 30; break;
      case 'video': defaultTopK = 10; break;
      case 'aladdin': defaultTopK = 5; break;
      default: defaultTopK = 20;
    }
    return { type: typeName, top_k: k ? parseInt(k) : defaultTopK };
  });
}

// Build search_filter
const searchFilter = {};
if (options.site) {
  searchFilter.match = { site: options.site };
}
if (options.from && options.to) {
  searchFilter.range = { page_time: { gte: options.from, lt: options.to } };
}
if (options.block) {
  searchFilter.block_websites = options.block;
}

// Build request body
const requestBody = {
  messages: [{ content: query, role: 'user' }],
  edition: options.edition,
  search_source: 'baidu_search_v2',
  resource_type_filter: resourceTypeFilter,
};

if (Object.keys(searchFilter).length > 0) {
  requestBody.search_filter = searchFilter;
}
if (options.time) {
  requestBody.search_recency_filter = options.time;
}
if (options.safe) {
  requestBody.safe_search = true;
}
if (options.config) {
  requestBody.config_id = options.config;
}

// Make request
const postData = JSON.stringify(requestBody);
const requestOptions = {
  hostname: 'qianfan.baidubce.com',
  port: 443,
  path: '/v2/ai_search/web_search',
  method: 'POST',
  headers: {
    'X-Appbuilder-Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData),
  },
};

const req = https.request(requestOptions, (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    try {
      const result = JSON.parse(data);
      if (options.raw) {
        console.log(JSON.stringify(result, null, 2));
        return;
      }
      if (result.code) {
        console.error(`错误：${result.code} - ${result.message}`);
        process.exit(1);
      }
      if (!result.references || result.references.length === 0) {
        console.log('未找到搜索结果');
        return;
      }
      result.references.forEach((ref, index) => {
        console.log(`#${index + 1} ${ref.title}`);
        if (ref.website) console.log(`站点: ${ref.website}`);
        console.log(`链接: ${ref.url}`);
        if (ref.date) console.log(`时间: ${ref.date}`);
        if (ref.snippet) console.log(`摘要: ${ref.snippet}`);
        if (index < result.references.length - 1) console.log('---');
      });
    } catch (e) {
      console.error('解析响应失败:', e);
      console.log('原始响应:', data);
    }
  });
});

req.on('error', (e) => {
  console.error('请求失败:', e);
  process.exit(1);
});

req.write(postData);
req.end();
