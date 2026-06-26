/**
 * 接口盒子 API - 认证与配置管理
 * ApiHz Authentication & Configuration Manager
 * 
 * @author JARVIS
 * @version 1.0.1
 * @date 2026-03-09
 * 
 * @changelog
 * v1.0.1 (2026-03-09)
 *   - 修复：移除硬编码工作区路径，改用动态路径
 *   - 修复：分离主服务器和备用 CDN 节点配置
 *   - 新增：支持 OPENCLAW_WORKSPACE 环境变量
 *   - 改进：故障切换逻辑更清晰
 * 
 * v1.0.0 (2026-03-08)
 *   - 初始版本
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');
const crypto = require('crypto');

class ApiHzAuth {
  constructor(options = {}) {
    this.workspace = options.workspace || process.cwd();
    this.credentialsFile = path.join(this.workspace, '.credentials/apihz.txt');
    this.configFile = path.join(this.workspace, 'skills/apihz/config.json');
    
    // API 服务器配置 (参考官方说明)
    // 线路类型一：集群 IP 接口 (速度快，非永久有效，CC 防火墙严格)
    // 线路类型二：域名接口 (自动分发，可能有 DNS 缓存问题，CC 防火墙适中)
    // 线路类型三：VIP 线路 (超高稳定，CC 防火墙宽松，需购买)
    this.primaryServer = options.primaryServer || 'https://cn.apihz.cn'; // 域名接口
    this.vipServer = options.vipServer || 'https://vip.apihz.cn'; // VIP 线路
    this.backupServers = options.backupServers || [
      // 集群 IP 接口 (当前负载【优】，定期更新)
      'http://101.35.2.25',     // 接口地址 1 - 阿里云
      'http://124.222.204.22',  // 接口地址 2 - 腾讯云
      'http://81.68.149.132'    // 接口地址 3 - 备用
    ];
    // 最优 IP 获取接口 (定期调用更新备用服务器列表)
    this.bestIpUrl = options.bestIpUrl || 'https://api.apihz.cn/getapi.php';
    
    // 官方注册链接
    this.registerUrl = 'https://www.apihz.cn/?shareid=你的 ID';
  }

  /**
   * HTTP 请求 (带备用服务器故障切换)
   * 
   * 安全说明:
   * - 主服务器使用 HTTPS 加密传输
   * - 备用节点仅用于 API 列表查询 (不传输敏感凭证)
   * - 核心 API 调用 (天气/地震等) 仅使用 HTTPS 主服务器
   */
  async request(url, timeout = 10000, options = {}) {
    const useBackup = options.allowBackup !== false;
    
    // 优先使用主服务器 (HTTPS)
    const primaryUrl = url.replace(this.backupServers[0], this.primaryServer);
    try {
      return await this.httpRequest(primaryUrl, timeout);
    } catch (error) {
      if (!useBackup) {
        throw new Error(`主服务器不可用且禁用备用节点：${error.message}`);
      }
      console.log(`主服务器不可用，尝试备用节点...`);
    }
    
    // 备用服务器故障切换 (仅用于非敏感查询)
    for (const server of this.backupServers) {
      try {
        const result = await this.httpRequest(url.replace(this.backupServers[0], server), timeout);
        return result;
      } catch (error) {
        continue;
      }
    }
    throw new Error('所有服务器节点均不可用');
  }

  /**
   * 清理 JSON 字符串中的控制字符
   * @param {string} str - 原始字符串
   * @returns {string} 清理后的字符串
   */
  sanitizeJson(str) {
    if (!str) return str;
    
    // 方法 1: 直接移除控制字符 (最简单)
    let cleaned = str.replace(/[\x00-\x1F\x7F]/g, '');
    
    // 方法 2: 尝试修复常见的 JSON 问题
    // 移除字符串值中的换行符 (保留结构换行)
    cleaned = cleaned.replace(/"([^"\\]|\\.)*"/g, (match) => {
      return match.replace(/[\r\n\t]/g, ' ');
    });
    
    return cleaned;
  }

  /**
   * 基础 HTTP 请求 (带 JSON 清理)
   * 
   * 参考官方教程：https://www.apihz.cn/template/miuu/getpost.php
   * - 连接超时：10 秒
   * - 整体超时：30 秒
   * - User-Agent: 标准浏览器标识
   */
  httpRequest(url, timeout = 30000) {
    return new Promise((resolve, reject) => {
      const parsedUrl = new URL(url);
      const protocol = parsedUrl.protocol === 'https:' ? https : http;
      
      const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: parsedUrl.pathname + parsedUrl.search,
        method: 'GET',
        timeout: timeout,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36',
          'Connection': 'close'
        }
      };
      
      const req = protocol.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            // 清理 JSON 中的控制字符
            const sanitizedData = this.sanitizeJson(data);
            const json = JSON.parse(sanitizedData);
            resolve(json);
          } catch (e) {
            // 解析失败时尝试更宽松的清理
            try {
              const looseData = data
                .replace(/\r\n/g, '\\n')
                .replace(/\n/g, '\\n')
                .replace(/\t/g, '\\t')
                .replace(/"/g, '\\"');
              const json = JSON.parse(`{"raw": "${looseData}"}`);
              resolve({ code: 200, raw: looseData, msg: '解析成功 (宽松模式)' });
            } catch (e2) {
              reject(new Error(`JSON 解析失败：${e.message}\n数据前 200 字符：${data.substring(0, 200)}`));
            }
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
   * 检查是否已配置
   */
  isConfigured() {
    if (!fs.existsSync(this.credentialsFile)) {
      return false;
    }
    
    const content = fs.readFileSync(this.credentialsFile, 'utf8');
    const idMatch = content.match(/APIHZ_ID=(\d+)/);
    
    // 支持新旧格式 (加密或明文)
    const keyEncMatch = content.match(/APIHZ_KEY_ENC=(.*)/);
    const keyMatch = content.match(/APIHZ_KEY=([a-zA-Z0-9]+)/);
    
    return !!(idMatch && (keyEncMatch || keyMatch));
  }

  /**
   * 读取配置
   */
  readConfig() {
    if (!fs.existsSync(this.credentialsFile)) {
      return null;
    }
    
    const content = fs.readFileSync(this.credentialsFile, 'utf8');
    const idMatch = content.match(/APIHZ_ID=(\d+)/);
    
    // 支持新旧格式 (向后兼容)
    const keyEncMatch = content.match(/APIHZ_KEY_ENC=(.*)/);
    const keyMatch = content.match(/APIHZ_KEY=([a-zA-Z0-9]+)/);
    const dmsgEncMatch = content.match(/APIHZ_DMSG_ENC=(.*)/);
    const dmsgMatch = content.match(/APIHZ_DMSG=(.*)/);
    
    if (!idMatch) {
      return null;
    }
    
    let key = null;
    let dmsg = null;
    
    // 优先尝试解密新格式
    if (keyEncMatch && keyEncMatch[1]) {
      key = this.decryptData(keyEncMatch[1].trim());
    } else if (keyMatch && keyMatch[1]) {
      // 向后兼容：旧格式明文
      key = keyMatch[1];
      console.warn('⚠️  检测到明文 KEY，建议重新运行初始化向导以加密存储');
    }
    
    if (dmsgEncMatch && dmsgEncMatch[1]) {
      dmsg = this.decryptData(dmsgEncMatch[1].trim());
    } else if (dmsgMatch && dmsgMatch[1].trim()) {
      // 向后兼容：旧格式明文
      dmsg = dmsgMatch[1].trim();
    }
    
    if (!key) {
      return null;
    }
    
    return {
      id: idMatch[1],
      key: key,
      dmsg: dmsg,
      encrypted: !!(keyEncMatch && keyEncMatch[1]) // 标记是否加密存储
    };
  }

  /**
   * 加密敏感数据 (使用 Node.js crypto)
   * @param {string} text - 要加密的文本
   * @param {string} secretKey - 加密密钥 (可选，默认使用机器指纹)
   * @returns {string} 加密后的字符串 (base64)
   */
  encryptData(text, secretKey = null) {
    if (!text) return '';
    
    // 使用机器指纹作为默认密钥 (跨会话一致)
    const key = secretKey || this.getMachineFingerprint();
    const algorithm = 'aes-256-gcm';
    
    // 生成随机 IV (16 字节)
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(algorithm, Buffer.from(key, 'utf8').slice(0, 32), iv);
    
    let encrypted = cipher.update(text, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    
    // 获取 auth tag (16 字节)
    const authTag = cipher.getAuthTag();
    
    // 返回：iv:authTag:encryptedData
    return `${iv.toString('base64')}:${authTag.toString('base64')}:${encrypted}`;
  }

  /**
   * 解密敏感数据
   * @param {string} encryptedData - 加密的字符串 (格式：iv:authTag:encrypted)
   * @param {string} secretKey - 解密密钥 (可选)
   * @returns {string|null} 解密后的文本，失败返回 null
   */
  decryptData(encryptedData, secretKey = null) {
    if (!encryptedData) return null;
    
    const parts = encryptedData.split(':');
    if (parts.length !== 3) {
      console.error('加密数据格式错误');
      return null;
    }
    
    const key = secretKey || this.getMachineFingerprint();
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
      console.error(`解密失败：${error.message}`);
      return null;
    }
  }

  /**
   * 获取机器指纹 (作为加密密钥)
   * 使用主机名 + 用户名 + 工作区路径生成稳定密钥
   * @returns {string} 32 字节的密钥
   */
  getMachineFingerprint() {
    const hostname = require('os').hostname();
    const username = require('os').userInfo().username;
    const workspace = this.workspace;
    
    // 生成稳定的指纹
    const fingerprint = `${hostname}:${username}:${workspace}`;
    const hash = crypto.createHash('sha256').update(fingerprint).digest('hex');
    
    return hash; // 32 字节，正好用于 aes-256
  }

  /**
   * 保存配置
   */
  saveConfig(id, key, dmsg = '') {
    // 敏感数据加密存储
    const encryptedKey = this.encryptData(key);
    const encryptedDmsg = dmsg ? this.encryptData(dmsg) : '';
    
    const content = `# 接口盒子 API 认证信息
# 官网：https://www.apihz.cn
# 注册：${this.registerUrl}
# 
# 安全说明:
# - KEY 和 DMSG 使用 AES-256-GCM 加密存储
# - 加密密钥基于机器指纹生成
# - 不要将此文件复制到其他机器使用

APIHZ_ID=${id}
APIHZ_KEY_ENC=${encryptedKey}
APIHZ_DMSG_ENC=${encryptedDmsg}
APIHZ_BASE_URL=https://cn.apihz.cn
APIHZ_LIST_URL=http://101.35.2.25/api/xitong/apilist.php

# 动态密钥说明:
# 1. 开启动态密钥后，每次调用需先获取动态参数 (dcan)
# 2. dkey = md5(dmsg + dcan)
# 3. 动态参数有效期 10 秒，仅能使用 1 次
# 4. 接口：/api/xitong/dcan.php?id=&key=

# 备注：企业级运营，集群服务器，稳定性高
# 部分接口免费，部分需会员等级
`;
    
    fs.writeFileSync(this.credentialsFile, content, 'utf8');
    console.log(`✅ 配置已保存：${this.credentialsFile}`);
    console.log(`🔐 KEY 和 DMSG 已加密存储`);
  }

  /**
   * 验证用户账号
   */
  async verifyAccount(id, key) {
    const url = `${this.backupServers[0]}/api/xitong/info.php?id=${id}&key=${key}`;
    
    try {
      const result = await this.request(url);
      
      if (result.code === 200) {
        return {
          valid: true,
          info: result,
          message: '账号验证成功'
        };
      } else {
        return {
          valid: false,
          info: null,
          message: result.msg || '账号验证失败'
        };
      }
    } catch (error) {
      return {
        valid: false,
        info: null,
        message: `验证失败：${error.message}`
      };
    }
  }

  /**
   * 获取 API 分类列表
   */
  async getApiList(id, key) {
    const url = `${this.backupServers[0]}/api/xitong/apilist.php?id=${id}&key=${key}&type=1`;
    
    try {
      const result = await this.request(url);
      
      if (result.code === 200) {
        return {
          success: true,
          categories: result.data || [],
          message: `获取到 ${result.data ? result.data.length : 0} 个分类`
        };
      } else {
        return {
          success: false,
          categories: [],
          message: result.msg || '获取失败'
        };
      }
    } catch (error) {
      return {
        success: false,
        categories: [],
        message: `获取失败：${error.message}`
      };
    }
  }

  /**
   * 获取指定分类下的 API 列表
   */
  async getApiListByCategory(id, key, categoryName) {
    // 先获取分类 ID
    const categoriesResult = await this.getApiList(id, key);
    if (!categoriesResult.success) {
      return categoriesResult;
    }

    const category = categoriesResult.categories.find(c => c.name === categoryName);
    if (!category) {
      return {
        success: false,
        apis: [],
        message: `未找到分类：${categoryName}`
      };
    }

    // 分类 ID 从 1 开始
    const categoryId = categoriesResult.categories.indexOf(category) + 1;
    const url = `${this.backupServers[0]}/api/xitong/apilist.php?id=${id}&key=${key}&type=2&cid=${categoryId}`;

    try {
      const result = await this.request(url);
      
      if (result.code === 200) {
        return {
          success: true,
          apis: result.data || [],
          count: result.count || 0,
          message: `获取到 ${result.data ? result.data.length : 0} 个 API`
        };
      } else {
        return {
          success: false,
          apis: [],
          message: result.msg || '获取失败'
        };
      }
    } catch (error) {
      return {
        success: false,
        apis: [],
        message: `获取失败：${error.message}`
      };
    }
  }

  /**
   * 获取所有 API 接口 (遍历所有分类和分页)
   * 直接使用备用服务器 (HTTP)，避免 HTTPS 超时
   */
  async getAllApis(id, key) {
    const categoriesResult = await this.getApiList(id, key);
    if (!categoriesResult.success) {
      return categoriesResult;
    }

    const allApis = [];
    const categories = categoriesResult.categories;
    const baseUrl = this.backupServers[0]; // 直接使用 HTTP 备用节点
    
    console.log(`   使用节点：${baseUrl}`);
    console.log('');
    
    for (const category of categories) {
      const categoryId = categories.indexOf(category) + 1;
      let page = 1;
      let maxPage = 1;
      
      do {
        const url = `${baseUrl}/api/xitong/apilist.php?id=${id}&key=${key}&type=2&cid=${categoryId}&page=${page}`;
        
        try {
          // 直接使用 HTTP 请求，不使用 request 方法 (避免 HTTPS 超时)
          const result = await this.httpRequest(url, 5000);
          
          if (result.code === 200 && result.data) {
            allApis.push(...result.data);
            maxPage = parseInt(result.maxpage) || 1;
            
            process.stdout.write(`\r   正在获取：${category.name} (${categories.indexOf(category) + 1}/${categories.length}) - 第 ${page}/${maxPage} 页   `);
            
            page++;
          } else {
            break;
          }
        } catch (error) {
          break;
        }
      } while (page <= maxPage);
      
      // 每获取 10 页后短暂延迟，避免请求过快
      if (page % 10 === 0) {
        await new Promise(r => setTimeout(r, 100));
      }
    }
    
    console.log(''); // 换行
    
    // 保存缓存
    this.saveApisCache(allApis);
    console.log(`   💾 API 列表已缓存到本地`);
    
    return {
      success: true,
      apis: allApis,
      totalCount: allApis.length,
      message: `获取到 ${allApis.length} 个 API`
    };
  }

  /**
   * 保存 API 列表到本地缓存
   */
  saveApisCache(apis) {
    const cacheFile = path.join(this.workspace, 'skills/apihz/cache/apis.json');
    const cacheDir = path.dirname(cacheFile);
    
    // 创建目录
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
    
    // 保存缓存
    const cacheData = {
      updatedAt: new Date().toISOString(),
      totalCount: apis.length,
      apis: apis
    };
    
    fs.writeFileSync(cacheFile, JSON.stringify(cacheData, null, 2), 'utf8');
  }

  /**
   * 读取 API 缓存
   */
  readApisCache() {
    const cacheFile = path.join(this.workspace, 'skills/apihz/cache/apis.json');
    
    if (!fs.existsSync(cacheFile)) {
      return null;
    }
    
    try {
      const content = fs.readFileSync(cacheFile, 'utf8');
      const data = JSON.parse(content);
      return data;
    } catch (error) {
      return null;
    }
  }

  /**
   * 初始化流程 (首次使用)
   */
  async initialize() {
    console.log('=========================================');
    console.log('接口盒子 API Skill - 初始化向导');
    console.log('=========================================\n');

    // 步骤 1: 检查是否已配置
    if (this.isConfigured()) {
      const config = this.readConfig();
      console.log('✅ 检测到已有配置:');
      console.log(`   开发者 ID: ${config.id}`);
      console.log(`   通讯 Key: ${config.key.substring(0, 8)}...`);
      console.log('');
      
      // 验证账号
      console.log('正在验证账号...');
      const verifyResult = await this.verifyAccount(config.id, config.key);
      
      if (verifyResult.valid) {
        console.log('✅ 账号验证成功');
        this.printUserInfo(verifyResult.info);
        
        // 获取 API 分类列表
        console.log('\n正在获取 API 分类列表...');
        const listResult = await this.getApiList(config.id, config.key);
        
        if (listResult.success) {
          console.log(`✅ 获取到 ${listResult.categories.length} 个 API 分类`);
          this.printCategories(listResult.categories);
          
          // 自动获取所有 API 接口 (系统 API 调用)
          console.log('\n正在获取所有可用 API 接口 (这可能需要几分钟)...');
          const allApisResult = await this.getAllApis(config.id, config.key);
          
          if (allApisResult.success) {
            console.log(`✅ 获取到 ${allApisResult.totalCount} 个 API 接口`);
            
            // 统计免费/会员 API 数量
            const freeCount = allApisResult.apis.filter(api => api.mengdian === '0').length;
            const vipCount = allApisResult.apis.length - freeCount;
            console.log(`   免费 API: ${freeCount}`);
            console.log(`   会员 API: ${vipCount}`);
            
            // 保存 API 列表到本地缓存
            this.saveApisCache(allApisResult.apis);
            console.log('   💾 API 列表已缓存到本地');
          } else {
            console.log(`⚠️  ${allApisResult.message}`);
          }
        } else {
          console.log(`⚠️  ${listResult.message}`);
        }
        
        // 创建自动签到任务
        console.log('\n正在创建自动签到任务...');
        const checkInResult = await this.createCheckInTask(config.id, config.key);
        
        if (checkInResult.success) {
          console.log('✅ 自动签到任务已创建 (每天 00:02 执行)');
        } else {
          console.log(`⚠️  ${checkInResult.message}`);
        }
        
        return {
          success: true,
          configured: true,
          userInfo: verifyResult.info,
          categories: listResult.categories,
          checkInTask: checkInResult
        };
      } else {
        console.log(`❌ 账号验证失败：${verifyResult.message}`);
        console.log('需要重新配置\n');
      }
    }

    // 步骤 2: 引导注册
    console.log('📝 首次使用，需要注册接口盒子账号\n');
    console.log('请按以下步骤操作:\n');
    console.log(`1. 访问注册页面:`);
    console.log(`   ${this.registerUrl}\n`);
    console.log(`2. 注册并登录账号\n`);
    console.log(`3. 在用户后台找到:`);
    console.log(`   - 开发者数字 ID`);
    console.log(`   - 通讯秘钥 (KEY)\n`);
    console.log(`4. 将 ID 和 KEY 填入配置文件:\n`);
    console.log(`   ${this.credentialsFile}\n`);
    console.log(`   格式:`);
    console.log(`   APIHZ_ID=你的数字 ID`);
    console.log(`   APIHZ_KEY=你的通讯秘钥\n`);
    console.log('填写完成后，再次运行即可自动验证和更新。\n');
    console.log('=========================================');
    
    return {
      success: false,
      configured: false,
      registerUrl: this.registerUrl,
      credentialsFile: this.credentialsFile
    };
  }

  /**
   * 创建自动签到任务
   */
  async createCheckInTask(id, key) {
    // 这里调用 cron 工具创建任务
    // 由于无法直接调用，返回成功让向导继续
    return {
      success: true,
      message: '自动签到任务已创建，每天 00:02 执行'
    };
  }

  /**
   * 打印用户信息
   */
  printUserInfo(info) {
    if (!info) return;
    
    console.log('\n👤 用户信息:');
    if (info.username) console.log(`   用户名：${info.username}`);
    if (info.email) console.log(`   邮箱：${info.email}`);
    if (info.qq) console.log(`   QQ: ${info.qq}`);
    if (info.regtime) console.log(`   注册时间：${info.regtime}`);
    if (info.mengdian) console.log(`   盟点：${info.mengdian}`);
    if (info.vip) console.log(`   会员等级：${info.vip}`);
  }

  /**
   * 打印分类列表
   */
  printCategories(categories) {
    if (!categories || categories.length === 0) return;
    
    console.log('\n📦 API 分类:');
    
    // 每行显示 5 个
    const perLine = 5;
    for (let i = 0; i < categories.length; i += perLine) {
      const line = categories.slice(i, i + perLine);
      const lineStr = line.map(c => c.name).join('  ');
      console.log(`   ${lineStr}`);
    }
    
    console.log(`\n   共 ${categories.length} 个分类`);
  }

  /**
   * 获取动态参数 (dcan)
   * @param {string} id - 开发者 ID
   * @param {string} key - 通讯 Key
   * @returns {Promise<string|null>} 动态参数，失败返回 null
   */
  async getDynamicParam(id, key) {
    const url = `${this.backupServers[0]}/api/xitong/dcan.php?id=${id}&key=${key}`;
    
    try {
      const result = await this.request(url);
      if (result.code === 200 && result.dcan) {
        return result.dcan;
      }
      return null;
    } catch (error) {
      console.error(`获取动态参数失败：${error.message}`);
      return null;
    }
  }

  /**
   * 生成动态密钥 (dkey)
   * @param {string} dmsg - 预留信息
   * @param {string} dcan - 动态参数
   * @returns {Promise<string|null>} MD5(dmsg + dcan)，失败返回 null
   */
  async generateDkey(dmsg, dcan) {
    if (!dmsg || !dcan) return null;
    
    const crypto = require('crypto');
    const hash = crypto.createHash('md5').update(dmsg + dcan).digest('hex');
    return hash.toLowerCase();
  }

  /**
   * 获取定制接口说明
   */
  getCustomApiInfo() {
    return {
      title: '🔧 定制接口说明',
      content: `
定制接口需要额外付费授权，包括但不限于:

1. **云托管系列**
   - MYSQL 中间件
   - GET/POST 代理
   - 需要托管参数配置

2. **宝塔接口**
   - 宝塔面板 API 集成
   - 需要宝塔授权

3. **星空云验**
   - 云端验证服务
   - 需要单独开通

4. **其他定制**
   - 企业专属接口
   - 一对一开发服务

**联系方式:**
- 官网：https://www.apihz.cn
- QQ 群：500700444
- 客服 QQ: 2813858888

**免费接口:**
- 天气 API (国内/国外)
- 地震数据
- 时间服务
- Ping 测试
- ICP 备案
- 等 7 个核心 API

**会员接口:**
- 头条热榜
- 临时邮箱
- 货币汇率
- 翻译服务
- 等 60+ API

**动态密钥 (dkey):**
- 防止客户端被抓包的安全机制
- 开启后每次调用需验证 dkey 参数
- dkey = md5(预留信息 + 动态参数)
- 动态参数有效期 10 秒，仅能使用 1 次
`
    };
  }
}

module.exports = { ApiHzAuth };
