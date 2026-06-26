#!/usr/bin/env node

/**
 * 钉钉日志查询脚本
 * 用途：查询用户发送的日报/周报列表
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
 * 查询日志列表
 * @param {string} userid 查询用户的工号
 * @param {string} templateName 模板名称（日报或周报）
 * @param {number} startTime 查询开始时间（毫秒时间戳）
 * @param {number} endTime 查询结束时间（毫秒时间戳）
 * @param {number} cursor 分页游标（可选）
 * @param {number} size 每页数量（可选）
 */
async function queryReport(userid, templateName, startTime, endTime, cursor = 0, size = 10) {
  // 验证参数
  if (!userid) {
    throw new Error('缺少必要参数: userid');
  }
  if (!templateName) {
    throw new Error('缺少必要参数: template-name');
  }
  if (!startTime || !endTime) {
    throw new Error('缺少必要参数: start-time 和 end-time');
  }
  
  // 验证模板名称
  const validNames = ['日报', '周报'];
  if (!validNames.includes(templateName)) {
    throw new Error(`模板名称错误，仅支持: ${validNames.join('、')}`);
  }
  
  // 验证时间范围
  const start = parseInt(startTime);
  const end = parseInt(endTime);
  
  if (isNaN(start) || isNaN(end)) {
    throw new Error('时间参数格式错误，应为Unix时间戳（毫秒）');
  }
  
  if (start >= end) {
    throw new Error('开始时间必须小于结束时间');
  }
  
  // 检查时间跨度（不超过180天）
  const maxSpan = 180 * 24 * 60 * 60 * 1000; // 180天的毫秒数
  if (end - start > maxSpan) {
    throw new Error('查询时间跨度不能超过180天');
  }
  
  // 获取access_token
  const accessToken = await getAccessToken();
  
  try {
    const response = await axios.post(
      'https://oapi.dingtalk.com/topapi/report/list',
      {
        userid: userid,
        template_name: templateName,
        start_time: start,
        end_time: end,
        cursor: parseInt(cursor) || 0,
        size: parseInt(size) || 10
      },
      {
        params: { access_token: accessToken },
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      }
    );
    
    const data = response.data;
    
    if (data.errcode !== 0) {
      throw new Error(`查询日志失败: ${data.errmsg} (错误码: ${data.errcode})`);
    }
    
    return data.result;
  } catch (error) {
    if (error.response) {
      throw new Error(`HTTP请求失败: ${error.response.status} ${error.response.statusText}`);
    }
    throw error;
  }
}

// 主函数
async function main() {
  const params = parseArgs();
  
  try {
    const result = await queryReport(
      params.userid,
      params['template-name'],
      params['start-time'],
      params['end-time'],
      params.cursor,
      params.size
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

module.exports = { queryReport };
