const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Cookie 加密存储模块
 * 
 * 使用 AES-256-GCM 加密存储 115 Cookie
 * 支持自动密钥派生和安全存储
 */
class CookieStore {
  constructor() {
    this.storagePath = path.join(
      process.env.HOME || process.env.USERPROFILE,
      '.openclaw/115-cookie.json'
    );
    this.algorithm = 'aes-256-gcm';
    this.keyLength = 32;
    this.ivLength = 16;
    this.authTagLength = 16;
  }

  /**
   * 从密码派生加密密钥
   * @param {string} password - 密码（使用机器标识作为密码）
   * @param {Buffer} salt - 盐值
   * @returns {Buffer} 派生的密钥
   */
  deriveKey(password, salt) {
    return crypto.pbkdf2Sync(password, salt, 100000, this.keyLength, 'sha256');
  }

  /**
   * 生成随机盐值
   * @returns {Buffer} 盐值
   */
  generateSalt() {
    return crypto.randomBytes(this.ivLength);
  }

  /**
   * 获取机器标识作为加密密码
   * @returns {string} 机器标识
   */
  getMachineId() {
    const os = require('os');
    const crypto = require('crypto');
    const machineInfo = `${os.hostname()}-${os.platform()}-${os.arch()}`;
    return crypto.createHash('sha256').update(machineInfo).digest('hex');
  }

  /**
   * 加密 Cookie 数据
   * @param {Object} cookie - Cookie 对象
   * @returns {string} 加密后的 JSON 字符串
   */
  encrypt(cookie) {
    const password = this.getMachineId();
    const salt = this.generateSalt();
    const key = this.deriveKey(password, salt);
    const iv = crypto.randomBytes(this.ivLength);

    const cipher = crypto.createCipheriv(this.algorithm, key, iv);
    
    let encrypted = cipher.update(JSON.stringify(cookie), 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();

    // 组装加密数据
    const encryptedData = {
      salt: salt.toString('hex'),
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex'),
      encryptedData: encrypted,
      timestamp: Date.now()
    };

    return JSON.stringify(encryptedData);
  }

  /**
   * 解密 Cookie 数据
   * @param {string} encryptedJson - 加密的 JSON 字符串
   * @returns {Object} 解密后的 Cookie 对象
   */
  decrypt(encryptedJson) {
    const data = JSON.parse(encryptedJson);
    const password = this.getMachineId();
    
    const salt = Buffer.from(data.salt, 'hex');
    const iv = Buffer.from(data.iv, 'hex');
    const authTag = Buffer.from(data.authTag, 'hex');
    const key = this.deriveKey(password, salt);

    const decipher = crypto.createDecipheriv(this.algorithm, key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(data.encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return JSON.parse(decrypted);
  }

  /**
   * 保存 Cookie
   * @param {Object} cookie - Cookie 对象 {uid, cid, se, ...}
   * @returns {Promise<Object>} 保存结果
   */
  async save(cookie) {
    try {
      // 确保目录存在
      const dir = path.dirname(this.storagePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      // 加密并保存
      const encrypted = this.encrypt({
        uid: cookie.uid,
        cid: cookie.cid,
        se: cookie.se,
        loginTime: cookie.loginTime || Date.now(),
        expireAt: cookie.expireAt || null,
        vip: cookie.vip || false,
        vipType: cookie.vipType || null,
        vipExpire: cookie.vipExpire || null
      });

      fs.writeFileSync(this.storagePath, encrypted, {
        mode: 0o600, // 仅所有者可读写
        encoding: 'utf8'
      });

      return {
        success: true,
        path: this.storagePath,
        timestamp: Date.now()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 加载 Cookie
   * @returns {Promise<Object|null>} Cookie 对象或 null
   */
  async load() {
    try {
      if (!fs.existsSync(this.storagePath)) {
        return null;
      }

      const encrypted = fs.readFileSync(this.storagePath, 'utf8');
      const cookie = this.decrypt(encrypted);

      // 检查是否过期
      if (cookie.expireAt && Date.now() > cookie.expireAt) {
        await this.clear();
        return null;
      }

      return cookie;
    } catch (error) {
      // 解密失败可能是密钥变化或文件损坏
      await this.clear();
      return null;
    }
  }

  /**
   * 清除 Cookie
   * @returns {Promise<Object>} 清除结果
   */
  async clear() {
    try {
      if (fs.existsSync(this.storagePath)) {
        fs.unlinkSync(this.storagePath);
      }
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * 检查 Cookie 是否存在
   * @returns {boolean} 是否存在
   */
  exists() {
    return fs.existsSync(this.storagePath);
  }

  /**
   * 获取存储文件信息
   * @returns {Object|null} 文件信息
   */
  getStorageInfo() {
    if (!fs.existsSync(this.storagePath)) {
      return null;
    }

    const stats = fs.statSync(this.storagePath);
    return {
      path: this.storagePath,
      size: stats.size,
      createdAt: stats.birthtime,
      modifiedAt: stats.mtime,
      permissions: stats.mode.toString(8).slice(-3)
    };
  }
}

module.exports = CookieStore;
