#!/usr/bin/env node

/**
 * 钉钉认证脚本 - 获取access_token
 * 
 * 授权方式：ApiKey
 * 凭证Key：COZE_DINGTALK_API_<skill_id>
 */

const axios = require('axios');

// Skill ID（在构建时已确定）
const SKILL_ID = '7623630174566891562';

/**
 * 获取钉钉access_token
 * @returns {Promise<string>} access_token
 */
async function getAccessToken() {
  // 从环境变量获取凭证
  const credentialKey = `COZE_DINGTALK_API_${SKILL_ID}`;
  const credentialValue = process.env[credentialKey];
  
  if (!credentialValue) {
    throw new Error(`缺少钉钉API凭证，请检查环境变量 ${credentialKey}`);
  }
  
  // 凭证格式：APP_KEY:APP_SECRET
  const [appKey, appSecret] = credentialValue.split(':');
  
  if (!appKey || !appSecret) {
    throw new Error('凭证格式错误，应为 APP_KEY:APP_SECRET');
  }
  
  try {
    const response = await axios.get('https://oapi.dingtalk.com/gettoken', {
      params: {
        appkey: appKey,
        appsecret: appSecret
      },
      timeout: 10000
    });
    
    const data = response.data;
    
    if (data.errcode !== 0) {
      throw new Error(`获取access_token失败: ${data.errmsg} (错误码: ${data.errcode})`);
    }
    
    return data.access_token;
  } catch (error) {
    if (error.response) {
      throw new Error(`HTTP请求失败: ${error.response.status} ${error.response.statusText}`);
    }
    throw error;
  }
}

// 如果作为独立脚本运行
if (require.main === module) {
  getAccessToken()
    .then(token => {
      console.log(JSON.stringify({ success: true, access_token: token }));
    })
    .catch(error => {
      console.log(JSON.stringify({ success: false, error: error.message }));
      process.exit(1);
    });
}

module.exports = { getAccessToken };
