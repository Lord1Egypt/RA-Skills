import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

/**
 * Encryption Service (Node.js/Backend Edition - Multi-User + Channel Isolated)
 * 
 * 修正版：移除 TS 类型注解，确保在原生 Node.js 环境下通过
 */
export class EncryptionService {
  // 静态属性（使用标准 JS 语法）
  static masterKeys = new Map();
  static keks = new Map();
  static deks = new Map();
  
  static storagePath = path.join(process.cwd(), '.anydef-vault.json');
  static vaultBaseDir = path.join(process.cwd(), '.anydef-vault');

  static getCtx(userId, channelId) {
    return `${userId}:${channelId}`;
  }

  static async storageGet(key) {
    try {
      if (!fs.existsSync(this.storagePath)) return null;
      const data = JSON.parse(fs.readFileSync(this.storagePath, 'utf8'));
      return data[key] || null;
    } catch (e) {
      console.error("[Vault] Storage Read Error:", e);
      return null;
    }
  }

  static async storageSet(key, value) {
    try {
      const data = fs.existsSync(this.storagePath) 
        ? JSON.parse(fs.readFileSync(this.storagePath, 'utf8')) 
        : {};
      data[key] = value;
      fs.writeFileSync(this.storagePath, JSON.stringify(data, null, 2));
    } catch (e) {
      console.error("[Vault] Storage Write Error:", e);
    }
  }

  /**
   * 解锁特定上下文
   */
  static async unlock(userId, channelId, passphrase) {
    const ctx = this.getCtx(userId, channelId);
    
    const saltKey = `${ctx}:enc-vault-salt`;
    let saltBase64 = await this.storageGet(saltKey);
    let salt;
    if (!saltBase64) {
      salt = crypto.randomBytes(16);
      await this.storageSet(saltKey, salt.toString('base64'));
    } else {
      salt = Buffer.from(saltBase64, 'base64');
    }

    this.masterKeys.set(ctx, crypto.pbkdf2Sync(passphrase, salt, 100000, 32, 'sha256'));
    await this.initKek(userId, channelId);
    console.log(`[Vault] Context ${ctx} unlocked successfully.`);
  }

  static async initKek(userId, channelId) {
    const ctx = this.getCtx(userId, channelId);
    const mk = this.masterKeys.get(ctx);
    if (!mk) throw new Error("Context not unlocked");
    
    const storageKey = `${ctx}:enc-kek-wrapped`;
    const wrappedKek = await this.storageGet(storageKey);
    
    if (wrappedKek) {
      this.keks.set(ctx, await this.decryptRaw(wrappedKek, mk));
    } else {
      const kek = crypto.randomBytes(32);
      const wrapped = await this.encryptRaw(kek, mk);
      await this.storageSet(storageKey, wrapped);
      this.keks.set(ctx, kek);
    }
  }

  /**
   * 保存数据（带隔离）
   */
  static async save(userId, channelId, scope, key, data) {
    try {
      const encrypted = await this.encrypt(userId, channelId, scope, data);
      const ctx = this.getCtx(userId, channelId);
      
      if (scope === 'assets') {
        const userDir = path.join(this.vaultBaseDir, userId, channelId);
        if (!fs.existsSync(userDir)) {
          fs.mkdirSync(userDir, { recursive: true });
        }
        const filePath = path.join(userDir, `${key}.enc`);
        fs.writeFileSync(filePath, encrypted);
        console.log(`[Vault] Asset saved to: ${filePath}`);
        return filePath;
      } else {
        const storageKey = `vault:${ctx}:${scope}:${key}`;
        await this.storageSet(storageKey, encrypted);
        return storageKey;
      }
    } catch (e) {
      console.error("[Vault] Save Error:", e);
      throw e;
    }
  }

  static async load(userId, channelId, scope, key) {
    const ctx = this.getCtx(userId, channelId);
    let encrypted = null;

    if (scope === 'assets') {
      const filePath = path.join(this.vaultBaseDir, userId, channelId, `${key}.enc`);
      if (fs.existsSync(filePath)) {
        encrypted = fs.readFileSync(filePath, 'utf8');
      }
    } else {
      encrypted = await this.storageGet(`vault:${ctx}:${scope}:${key}`);
    }

    if (!encrypted) return null;
    return await this.decrypt(userId, channelId, scope, encrypted);
  }

  static async encrypt(userId, channelId, scope, data) {
    const dek = await this.getOrCreateDek(userId, channelId, scope);
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', dek, iv);
    
    let encrypted = cipher.update(data, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    const authTag = cipher.getAuthTag().toString('base64');

    return `${iv.toString('base64')}:${encrypted}:${authTag}`;
  }

  static async decrypt(userId, channelId, scope, encryptedData) {
    const dek = await this.getOrCreateDek(userId, channelId, scope);
    const [ivBase64, cipherBase64, authTagBase64] = encryptedData.split(':');
    
    const iv = Buffer.from(ivBase64, 'base64');
    const authTag = Buffer.from(authTagBase64, 'base64');
    const decipher = crypto.createDecipheriv('aes-256-gcm', dek, iv);
    
    decipher.setAuthTag(authTag);
    let decrypted = decipher.update(cipherBase64, 'base64', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }

  static async getOrCreateDek(userId, channelId, scope) {
    const ctx = this.getCtx(userId, channelId);
    const kek = this.keks.get(ctx);
    if (!kek) throw new Error(`Vault locked for context ${ctx}`);

    if (!this.deks.has(ctx)) this.deks.set(ctx, new Map());
    const ctxDeks = this.deks.get(ctx);

    if (ctxDeks.has(scope)) return ctxDeks.get(scope);

    const storageKey = `${ctx}:enc-dek-${scope}`;
    const wrappedDek = await this.storageGet(storageKey);
    
    let dek;
    if (wrappedDek) {
      dek = await this.decryptRaw(wrappedDek, kek);
    } else {
      dek = crypto.randomBytes(32);
      const wrapped = await this.encryptRaw(dek, kek);
      await this.storageSet(storageKey, wrapped);
    }
    
    ctxDeks.set(scope, dek);
    return dek;
  }

  static async encryptRaw(data, key) {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    let encrypted = cipher.update(data);
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    return `${iv.toString('base64')}:${encrypted.toString('base64')}:${cipher.getAuthTag().toString('base64')}`;
  }

  static async decryptRaw(wrappedStr, key) {
    const [ivBase64, cipherBase64, authTagBase64] = wrappedStr.split(':');
    const iv = Buffer.from(ivBase64, 'base64');
    const authTag = Buffer.from(authTagBase64, 'base64');
    const cipher = Buffer.from(cipherBase64, 'base64');
    
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);
    let decrypted = decipher.update(cipher);
    decrypted = Buffer.concat([decrypted, decipher.final()]);
    return decrypted;
  }
}
