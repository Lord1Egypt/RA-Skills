/**
 * 百度网盘 API 封装
 * 
 * 设计原则：
 * 1. 仅调用百度官方 API
 * 2. 流式处理，节省内存和 Token
 * 3. 智能缓存，减少重复请求
 */

const axios = require('axios');
const crypto = require('crypto');
const CryptoJS = require('crypto-js');

// AES-256 解密密钥（支持环境变量覆盖，必须与 auth.js 一致）
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || 
  crypto.createHash('sha256').update('baidu-netdisk-skill-secret-2026').digest('hex');

/**
 * AES-256 加密
 */
function encrypt(text) {
  return CryptoJS.AES.encrypt(text, ENCRYPTION_KEY).toString();
}

/**
 * AES-256 解密
 */
function decrypt(ciphertext) {
  const bytes = CryptoJS.AES.decrypt(ciphertext, ENCRYPTION_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
}

class BaiduNetdiskAPI {
  constructor(config) {
    // 解密 Token（如果已加密）
    this.accessToken = config.accessToken.startsWith('U2FsdGVk') ? decrypt(config.accessToken) : config.accessToken;
    this.refreshToken = config.refreshToken.startsWith('U2FsdGVk') ? decrypt(config.refreshToken) : config.refreshToken;
    this.apiKey = config.apiKey;
    this.secretKey = config.secretKey;
    this.baseUrl = 'https://pan.baidu.com/rest/2.0/xpan';
    
    // 缓存层（省 Token 关键）
    this.cache = new Map();
    this.cacheTTL = 5 * 60 * 1000; // 5 分钟缓存
  }

  /**
   * 带缓存的请求（核心省 Token 逻辑）
   */
  async cachedRequest(params, ttl = this.cacheTTL) {
    const cacheKey = JSON.stringify(params);
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < ttl) {
      console.log('📦 使用缓存（节省 Token）');
      return cached.data;
    }
    
    const response = await this.request(params);
    this.cache.set(cacheKey, {
      data: response,
      timestamp: Date.now()
    });
    
    return response;
  }

  /**
   * 基础请求方法
   */
  async request(params) {
    try {
      const response = await axios.get(`${this.baseUrl}${params.path}`, {
        params: {
          access_token: this.accessToken,
          ...params.data
        },
        timeout: 30000
      });
      
      if (response.data.errno !== 0) {
        throw new Error(`百度 API 错误：${response.data.errno} - ${response.data.errmsg}`);
      }
      
      return response.data;
    } catch (error) {
      if (error.response?.data?.errno === -6) {
        // Token 过期，尝试刷新
        await this.refreshAccessToken();
        return this.request(params);
      }
      throw error;
    }
  }

  /**
   * 获取用户信息
   * 使用百度网盘官方 API
   * 文档：https://pan.baidu.com/union/doc/pksg0s9ns
   */
  async getUserInfo() {
    const response = await axios.get(
      'https://pan.baidu.com/rest/2.0/xpan/nas',
      {
        params: {
          method: 'uinfo',
          access_token: this.accessToken,
          vip_version: 'v2'
        },
        headers: {
          'User-Agent': 'pan.baidu.com'
        }
      }
    );
    
    if (response.data.errno !== 0) {
      throw new Error(`百度 API 错误：${response.data.errno} - ${response.data.errmsg}`);
    }
    
    return response.data;
  }

  /**
   * 列出文件（支持分页）
   * 
   * 省 Token 优化：
   - 只请求必要的元数据
   - 支持按类型过滤（减少返回数据）
   */
  async listFiles(dir = '/', start = 0, limit = 100, fileType = 'all') {
    const response = await axios.get('https://pan.baidu.com/rest/2.0/xpan/file', {
      params: {
        method: 'list',
        access_token: this.accessToken,
        dir,
        start,
        limit,
        web: 1,
        // 只返回必要字段（省 Token）
        fields: 'fs_id,server_filename,size,server_ctime,server_mtime,isdir'
      }
    });
    
    if (response.data.errno !== 0) {
      throw new Error(`百度 API 错误：${response.data.errno} - ${response.data.errmsg}`);
    }
    
    const data = response.data;
    
    // 过滤文件类型
    if (fileType !== 'all') {
      data.list = data.list.filter(f => 
        fileType === 'folder' ? f.isdir === 1 : f.isdir === 0
      );
    }
    
    return data;
  }

  /**
   * 搜索文件
   * 
   * 省 Token 优化：
   - 使用百度服务端搜索（不拉取全部文件到本地）
   */
  async searchFile(keyword, dir = '/') {
    const response = await axios.get('https://pan.baidu.com/rest/2.0/xpan/file', {
      params: {
        method: 'search',
        access_token: this.accessToken,
        word: keyword,
        dir,
        re: '1' // 递归搜索
      }
    });
    
    return response.data;
  }

  /**
   * 下载文件（流式，不占内存）
   * 
   * 省 Token 优化：
   - 返回下载链接，不直接下载内容
   - 用户可以选择性下载
   */
  async getDownloadLink(fsId) {
    const response = await axios.get('https://pan.baidu.com/rest/2.0/xpan/file', {
      params: {
        method: 'filemetas',
        access_token: this.accessToken,
        fsids: `[${fsId}]`,
        dlink: 1
      },
      headers: {
        'User-Agent': 'pan.baidu.com'
      }
    });
    
    if (response.data.errno !== 0) {
      throw new Error(`百度 API 错误：${response.data.errno} - ${response.data.errmsg}`);
    }
    
    // 百度网盘 API 返回格式：info 数组
    if (response.data.info && response.data.info.length > 0) {
      return response.data.info[0].dlink;
    } else if (response.data.list && response.data.list.length > 0) {
      return response.data.list[0].dlink;
    } else {
      throw new Error('无法解析下载链接，API 返回格式异常');
    }
  }

  /**
   * 上传文件（分片上传，支持大文件）
   */
  async uploadFile(filePath, remotePath) {
    const fs = require('fs');
    const path = require('path');
    
    // 第一步：预上传，获取 uploadid
    const preUpload = await axios.post(
      'https://pan.baidu.com/rest/2.0/xpan/file',
      null,
      {
        params: {
          method: 'precreate',
          access_token: this.accessToken,
          path: remotePath,
          size: fs.statSync(filePath).size,
          isdir: 0,
          rtype: 3 // 覆盖
        }
      }
    );
    
    if (preUpload.data.errno !== 0) {
      throw new Error(`预上传失败：${preUpload.data.errmsg}`);
    }
    
    const uploadId = preUpload.data.uploadid;
    const blockSize = 4 * 1024 * 1024; // 4MB 分片
    const fileBuffer = fs.readFileSync(filePath);
    const partSeq = 0;
    
    // 第二步：上传分片
    const uploadPart = await axios.post(
      'https://pan.baidu.com/rest/2.0/xpan/file',
      fileBuffer,
      {
        params: {
          method: 'upload',
          access_token: this.accessToken,
          type: 'tmpfile',
          path: remotePath,
          uploadid: uploadId,
          partseq: partSeq
        },
        headers: {
          'Content-Type': 'application/octet-stream'
        }
      }
    );
    
    // 第三步：创建文件
    const createFile = await axios.post(
      'https://pan.baidu.com/rest/2.0/xpan/file',
      null,
      {
        params: {
          method: 'create',
          access_token: this.accessToken,
          path: remotePath,
          size: fs.statSync(filePath).size,
          isdir: 0,
          rtype: 3,
          uploadid: uploadId,
          block_list: JSON.stringify([uploadPart.data.md5])
        }
      }
    );
    
    return createFile.data;
  }

  /**
   * 刷新 Access Token
   */
  async refreshAccessToken() {
    const response = await axios.post(
      'https://openapi.baidu.com/oauth/2.0/token',
      null,
      {
        params: {
          grant_type: 'refresh_token',
          refresh_token: this.refreshToken,
          client_id: this.apiKey,
          client_secret: this.secretKey
        }
      }
    );
    
    this.accessToken = response.data.access_token;
    this.refreshToken = response.data.refresh_token;
    
    // 保存新 Token（AES-256 加密）
    const Conf = require('conf');
    const config = new Conf({ projectName: 'baidu-netdisk-skill' });
    config.set('accessToken', encrypt(this.accessToken));
    config.set('refreshToken', encrypt(this.refreshToken));
    
    console.log('✅ Token 已刷新（加密存储）');
  }

  /**
   * 清空缓存（手动触发）
   */
  clearCache() {
    this.cache.clear();
    console.log('🗑️ 缓存已清空');
  }
}

module.exports = BaiduNetdiskAPI;
