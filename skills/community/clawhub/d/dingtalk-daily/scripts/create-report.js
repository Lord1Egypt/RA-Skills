#!/usr/bin/env node

/**
 * 钉钉日志创建脚本
 * 用途：创建并发送日报/周报
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
 * 创建日志
 * @param {string} userid 创建者工号
 * @param {string} templateId 模板ID
 * @param {array} contents 日志内容数组
 * @param {array} toUserids 接收人工号列表（可选）
 * @param {boolean} toChat 是否发送消息通知（可选）
 * @param {string} toCids 群ID（可选）
 */
async function createReport(userid, templateId, contents, toUserids = [], toChat = false, toCids = '') {
  // 验证参数
  if (!userid) {
    throw new Error('缺少必要参数: userid');
  }
  if (!templateId) {
    throw new Error('缺少必要参数: template-id');
  }
  if (!contents || !Array.isArray(contents)) {
    throw new Error('缺少必要参数: contents（JSON数组格式）');
  }
  
  // 验证内容格式
  for (const item of contents) {
    if (typeof item.sort === 'undefined' || !item.key || !item.content) {
      throw new Error('内容项格式错误，每项需包含 sort、key、content 字段');
    }
    if (item.content.length > 1000) {
      throw new Error(`字段"${item.key}"内容超过1000字符限制`);
    }
  }
  
  // 获取access_token
  const accessToken = await getAccessToken();
  
  // 构造请求体
  const requestBody = {
    create_report_param: {
      contents: contents.map((item, index) => ({
        content_type: 'markdown',
        sort: String(item.sort),
        type: '1',
        content: item.content,
        key: item.key
      })),
      template_id: templateId,
      userid: userid,
      to_chat: toChat
    }
  };
  
  // 添加可选参数
  if (toUserids && toUserids.length > 0) {
    requestBody.create_report_param.to_userids = toUserids;
  }
  if (toCids) {
    requestBody.create_report_param.to_cids = toCids;
  }
  
  try {
    const response = await axios.post(
      'https://oapi.dingtalk.com/topapi/report/create',
      requestBody,
      {
        params: { access_token: accessToken },
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      }
    );
    
    const data = response.data;
    
    if (data.errcode !== 0) {
      throw new Error(`创建日志失败: ${data.errmsg} (错误码: ${data.errcode})`);
    }
    
    return {
      report_id: data.result,
      request_id: data.request_id
    };
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
    // 解析contents参数（JSON字符串）
    let contents;
    try {
      contents = JSON.parse(params.contents);
    } catch (e) {
      throw new Error('contents参数格式错误，应为JSON数组');
    }
    
    // 解析可选参数
    const toUserids = params['to-userids'] ? params['to-userids'].split(',') : [];
    const toChat = params['to-chat'] === 'true';
    const toCids = params['to-cids'] || '';
    
    const result = await createReport(
      params.userid,
      params['template-id'],
      contents,
      toUserids,
      toChat,
      toCids
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

module.exports = { createReport };
