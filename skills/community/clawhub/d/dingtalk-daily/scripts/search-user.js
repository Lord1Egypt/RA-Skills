#!/usr/bin/env node

/**
 * 钉钉用户搜索脚本
 * 用途：根据姓名搜索用户工号
 */

const axios = require('axios');
const { getAccessToken } = require('./auth');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    const value = args[i + 1];
    params[key] = value;
  }
  
  return params;
}

/**
 * 根据姓名搜索用户工号
 * @param {string} queryWord 用户姓名
 * @param {number} offset 分页偏移量（可选，默认 0）
 * @param {number} size 每页数量（可选，默认 10）
 * @param {number} fullMatchField 是否完全匹配（可选，1=完全匹配，0=模糊匹配，默认 1）
 * @returns {Promise<Array>} 工号列表
 */
async function searchUser(queryWord, offset = 0, size = 10, fullMatchField = 1) {
  // 验证参数
  if (!queryWord) {
    throw new Error('缺少必要参数：queryWord（用户姓名）');
  }
  
  // 获取 access_token
  const accessToken = await getAccessToken();
  
  // 构造请求体
  const requestBody = {
    queryWord: queryWord,
    offset: offset,
    size: size,
    fullMatchField: fullMatchField
  };
  
  try {
    const response = await axios.post(
      'https://api.dingtalk.com/v1.0/contact/users/search',
      requestBody,
      {
        headers: {
          'Content-Type': 'application/json',
          'x-acs-dingtalk-access-token': accessToken
        },
        timeout: 10000
      }
    );
    
    const data = response.data;
    
    if (!data.success && data.code) {
      throw new Error(`搜索用户失败：${data.message || data.code} (错误码：${data.code})`);
    }
    
    return {
      list: data.list || [],
      hasMore: data.hasMore || false,
      totalCount: data.totalCount || 0
    };
  } catch (error) {
    if (error.response) {
      throw new Error(`HTTP 请求失败：${error.response.status} ${error.response.statusText}`);
    }
    throw error;
  }
}

// 主函数
async function main() {
  const params = parseArgs();
  
  try {
    const result = await searchUser(
      params['query-word'] || params.queryword || params.queryWord,
      parseInt(params.offset) || 0,
      parseInt(params.size) || 10,
      parseInt(params['full-match']) || 1
    );
    
    console.log(JSON.stringify({ success: true, data: result }, null, 2));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { searchUser };
