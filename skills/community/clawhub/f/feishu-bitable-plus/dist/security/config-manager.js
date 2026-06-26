"use strict";
/**
 * 配置管理器
 * Configuration Manager - Secure credential storage
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConfigManager = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
class ConfigManager {
    configDir;
    credentialsFile;
    constructor() {
        this.configDir = path.join(os.homedir(), '.feishu-bitable-plus');
        this.credentialsFile = path.join(this.configDir, 'credentials.json');
        this.ensureConfigDir();
    }
    ensureConfigDir() {
        if (!fs.existsSync(this.configDir)) {
            fs.mkdirSync(this.configDir, { recursive: true, mode: 0o700 });
        }
    }
    /**
     * 保存凭证
     * 注意：实际生产环境应该使用系统密钥链（keytar）
     * 这里简化为加密文件存储
     */
    async setCredentials(appId, appSecret) {
        // 简单的Base64编码（实际应该使用加密）
        const data = {
            appId: Buffer.from(appId).toString('base64'),
            appSecret: Buffer.from(appSecret).toString('base64')
        };
        fs.writeFileSync(this.credentialsFile, JSON.stringify(data), { mode: 0o600 });
    }
    /**
     * 获取凭证
     */
    async getCredentials() {
        if (!fs.existsSync(this.credentialsFile)) {
            return null;
        }
        try {
            const content = fs.readFileSync(this.credentialsFile, 'utf-8');
            const data = JSON.parse(content);
            return {
                appId: Buffer.from(data.appId, 'base64').toString('utf-8'),
                appSecret: Buffer.from(data.appSecret, 'base64').toString('utf-8')
            };
        }
        catch (error) {
            return null;
        }
    }
    /**
     * 清除凭证
     */
    async clearCredentials() {
        if (fs.existsSync(this.credentialsFile)) {
            fs.unlinkSync(this.credentialsFile);
        }
    }
    /**
     * 检查是否已配置
     */
    async isConfigured() {
        const creds = await this.getCredentials();
        return creds !== null;
    }
}
exports.ConfigManager = ConfigManager;
//# sourceMappingURL=config-manager.js.map