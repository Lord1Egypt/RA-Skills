#!/usr/bin/env node
/**
 * 接口盒子 - 自动签到脚本
 * 每天 00:02 自动执行
 * 
 * @version 1.0.5
 * @changelog 
 *   v1.0.5 - 支持加密的 KEY 和 DMSG
 *   v1.0.2 - 修复硬编码路径，使用 OPENCLAW_WORKSPACE 环境变量
 *   v1.0.1 - 改进服务器故障切换逻辑
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 认证信息路径 - 支持环境变量覆盖
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || '', '.openclaw', 'workspace');
const CREDENTIALS_FILE = path.join(WORKSPACE, '.credentials/apihz.txt');

// API 服务器配置
// 主服务器：官方域名
// 备用服务器：官方 CDN 节点 (阿里云/腾讯云)
const PRIMARY_SERVER = 'https://cn.apihz.cn';
const BACKUP_SERVERS = [
  'http://101.35.2.25',    // 阿里云 CDN 节点 1
  'http://124.222.204.22'   // 腾讯云 CDN 节点 2
];

/**
 * 获取机器指纹 (与 auth.js 保持一致)
 */
function getMachineFingerprint() {
  const os = require('os');
  const hostname = os.hostname();
  const username = os.userInfo().username;
  const workspace = WORKSPACE;
  
  const fingerprint = `${hostname}:${username}:${workspace}`;
  const hash = crypto.createHash('sha256').update(fingerprint).digest('hex');
  
  return hash;
}

/**
 * 解密敏感数据
 */
function decryptData(encryptedData, secretKey = null) {
  if (!encryptedData) return null;
  
  const parts = encryptedData.split(':');
  if (parts.length !== 3) return null;
  
  const key = secretKey || getMachineFingerprint();
  const algorithm = 'aes-256-gcm';
  
  const iv = Buffer.from(parts[0], 'base64');
  const authTag = Buffer.from(parts[1], 'base64');
  const encryptedText = parts[2];
  
  try {
    const decipher = crypto.createDecipheriv(algorithm, Buffer.from(key, 'utf8').slice(0, 32), iv);
    decipher.setAuthTag(authTag);
    
    let decrypted = decipher.update(encryptedText, 'base64', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  } catch (error) {
    return null;
  }
}

/**
 * 读取认证信息 (支持加密格式)
 */
function readCredentials() {
  if (!fs.existsSync(CREDENTIALS_FILE)) {
    console.log('❌ 认证文件不存在，请先运行初始化向导');
    return null;
  }
  
  const content = fs.readFileSync(CREDENTIALS_FILE, 'utf8');
  const idMatch = content.match(/APIHZ_ID=(\d+)/);
  
  // 支持新旧格式
  const keyEncMatch = content.match(/APIHZ_KEY_ENC=(.*)/);
  const keyMatch = content.match(/APIHZ_KEY=([a-zA-Z0-9]+)/);
  const dmsgEncMatch = content.match(/APIHZ_DMSG_ENC=(.*)/);
  const dmsgMatch = content.match(/APIHZ_DMSG=(.*)/);
  
  if (!idMatch) {
    console.log('❌ 认证信息格式错误');
    return null;
  }
  
  let key = null;
  let dmsg = null;
  
  // 优先解密新格式
  if (keyEncMatch && keyEncMatch[1]) {
    key = decryptData(keyEncMatch[1].trim());
  } else if (keyMatch && keyMatch[1]) {
    key = keyMatch[1];
  }
  
  if (dmsgEncMatch && dmsgEncMatch[1]) {
    dmsg = decryptData(dmsgEncMatch[1].trim());
  } else if (dmsgMatch && dmsgMatch[1].trim()) {
    dmsg = dmsgMatch[1].trim();
  }
  
  if (!key) {
    console.log('❌ 无法读取 KEY，请检查配置文件');
    return null;
  }
  
  return {
    id: idMatch[1],
    key: key,
    dmsg: dmsg,
    encrypted: !!(keyEncMatch && keyEncMatch[1])
  };
}

/**
 * HTTP 请求 (带备用服务器故障切换)
 */
async function request(url, timeout = 10000) {
  // 优先使用主服务器
  const primaryUrl = url.replace(BACKUP_SERVERS[0], PRIMARY_SERVER);
  try {
    return await httpRequest(primaryUrl, timeout);
  } catch (error) {
    console.log(`主服务器不可用，尝试备用节点...`);
  }
  
  // 备用服务器故障切换
  for (const server of BACKUP_SERVERS) {
    try {
      return await httpRequest(url.replace(BACKUP_SERVERS[0], server), timeout);
    } catch (error) {
      continue;
    }
  }
  throw new Error('所有服务器节点均不可用');
}

/**
 * 基础 HTTP 请求
 */
function httpRequest(url, timeout) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      timeout: timeout
    };
    
    const req = protocol.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(new Error(`JSON 解析失败：${e.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('请求超时'));
    });
    
    req.end();
  });
}

/**
 * 执行签到
 */
async function checkIn(id, key) {
  const url = `${BACKUP_SERVERS[0]}/api/xitong/function.php?id=${id}&key=${key}&type=1`;
  
  try {
    const result = await request(url);
    
    if (result.code === 200) {
      console.log('✅ 签到成功');
      console.log(`   ${result.msg}`);
      return { success: true, message: result.msg };
    } else if (result.code === 400) {
      console.log('ℹ️  今天已签到');
      console.log(`   ${result.msg}`);
      return { success: true, message: result.msg };
    } else {
      console.log('❌ 签到失败');
      console.log(`   ${result.msg}`);
      return { success: false, message: result.msg };
    }
  } catch (error) {
    console.log('❌ 请求失败');
    console.log(`   ${error.message}`);
    return { success: false, message: error.message };
  }
}

/**
 * 查询账号信息
 */
async function getAccountInfo(id, key) {
  const url = `${BACKUP_SERVERS[0]}/api/xitong/info.php?id=${id}&key=${key}`;
  
  try {
    const result = await request(url);
    
    if (result.code === 200) {
      return {
        success: true,
        info: {
          username: result.username,
          liquan: result.liquan,      // 礼券
          zuan1: result.zuan1,        // 1 天钻石会员
          zuan2: result.zuan2,        // 7 天钻石会员
          zuan3: result.zuan3,        // 30 天钻石会员
          zuan4: result.zuan4,        // 永久扩展频次
          dayapi: result.dayapi,      // 今日 API 调用
          leve: result.leve           // 用户等级
        }
      };
    } else {
      return { success: false, message: result.msg };
    }
  } catch (error) {
    return { success: false, message: error.message };
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('=========================================');
  console.log('接口盒子 - 自动签到');
  console.log('=========================================\n');
  
  // 读取认证信息
  const creds = readCredentials();
  if (!creds) {
    process.exit(1);
  }
  
  console.log(`👤 用户：${creds.id}`);
  console.log('');
  
  // 执行签到
  const checkInResult = await checkIn(creds.id, creds.key);
  console.log('');
  
  // 查询账号信息
  console.log('📊 账号信息:');
  const accountInfo = await getAccountInfo(creds.id, creds.key);
  
  if (accountInfo.success) {
    const info = accountInfo.info;
    console.log(`   用户名：${info.username}`);
    console.log(`   礼券：${info.liquan}`);
    console.log(`   1 天会员：${info.zuan1} 天`);
    console.log(`   7 天会员：${info.zuan2} 天`);
    console.log(`   30 天会员：${info.zuan3} 天`);
    console.log(`   永久扩展：${info.zuan4}`);
    console.log(`   今日 API: ${info.dayapi} 次`);
    console.log(`   等级：${info.leve}`);
  } else {
    console.log(`   ${accountInfo.message}`);
  }
  
  console.log('');
  console.log('=========================================');
  
  return checkInResult;
}

// 运行
main().catch(console.error);
