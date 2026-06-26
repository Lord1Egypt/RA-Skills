#!/usr/bin/env node

/**
 * 钉钉日志模板查询脚本
 * 用途：获取日志模板信息（模板ID、字段列表等）
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
 * 获取模板信息
 * @param {string} userid 用户工号
 * @param {string} templateName 模板名称（日报或周报）
 * @returns {Promise<object>} 模板信息
 */
async function getTemplate(userid, templateName) {
  // 验证参数
  if (!userid) {
    throw new Error('缺少必要参数: userid');
  }
  if (!templateName) {
    throw new Error('缺少必要参数: template-name');
  }
  
  // 验证模板名称
  const validNames = ['日报', '周报'];
  if (!validNames.includes(templateName)) {
    throw new Error(`模板名称错误，仅支持: ${validNames.join('、')}`);
  }
  
  // 获取access_token
  const accessToken = await getAccessToken();
  
  try {
    const response = await axios.post(
      'https://oapi.dingtalk.com/topapi/report/template/getbyname',
      {
        userid: userid,
        template_name: templateName
      },
      {
        params: { access_token: accessToken },
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      }
    );
    
    const data = response.data;
    
    if (data.errcode !== 0) {
      throw new Error(`获取模板失败: ${data.errmsg} (错误码: ${data.errcode})`);
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
    const result = await getTemplate(params.userid, params['template-name']);
    console.log(JSON.stringify({ success: true, data: result }, null, 2));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { getTemplate };
