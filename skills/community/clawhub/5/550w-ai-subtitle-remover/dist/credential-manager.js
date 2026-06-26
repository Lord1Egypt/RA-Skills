"use strict";
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
exports.CredentialManager = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const types_1 = require("./types");
class CredentialManager {
    constructor(storagePath) {
        this.storagePath = storagePath ?? path.resolve(__dirname, "../.credentials.json");
    }
    get() {
        // 优先从环境变量读取
        const envUserNo = process.env.SUBTITLE_REMOVER_USER_NO?.trim();
        const envApiKey = process.env.SUBTITLE_REMOVER_API_KEY?.trim();
        if (envUserNo &&
            envApiKey &&
            envUserNo.length >= 1 &&
            envUserNo.length <= types_1.MAX_CREDENTIAL_LENGTH &&
            envApiKey.length >= 1 &&
            envApiKey.length <= types_1.MAX_CREDENTIAL_LENGTH) {
            return { userNo: envUserNo, apiKey: envApiKey };
        }
        // 其次从 JSON 文件读取
        try {
            const content = fs.readFileSync(this.storagePath, "utf-8");
            const data = JSON.parse(content);
            if (typeof data.userNo === "string" &&
                typeof data.apiKey === "string" &&
                data.userNo.trim().length >= 1 &&
                data.userNo.trim().length <= types_1.MAX_CREDENTIAL_LENGTH &&
                data.apiKey.trim().length >= 1 &&
                data.apiKey.trim().length <= types_1.MAX_CREDENTIAL_LENGTH) {
                return { userNo: data.userNo.trim(), apiKey: data.apiKey.trim() };
            }
            return null;
        }
        catch {
            return null;
        }
    }
    set(credential) {
        const userNo = credential.userNo?.trim() ?? "";
        const apiKey = credential.apiKey?.trim() ?? "";
        if (userNo.length < 1 || userNo.length > types_1.MAX_CREDENTIAL_LENGTH) {
            throw new Error(`userNo 长度必须在 1-${types_1.MAX_CREDENTIAL_LENGTH} 之间，当前长度: ${userNo.length}`);
        }
        if (apiKey.length < 1 || apiKey.length > types_1.MAX_CREDENTIAL_LENGTH) {
            throw new Error(`apiKey 长度必须在 1-${types_1.MAX_CREDENTIAL_LENGTH} 之间，当前长度: ${apiKey.length}`);
        }
        const stored = { userNo, apiKey, updatedAt: Date.now() };
        fs.writeFileSync(this.storagePath, JSON.stringify(stored, null, 2), "utf-8");
    }
    isConfigured() {
        return this.get() !== null;
    }
    getGuideMessage() {
        return {
            code: types_1.ErrorCode.AUTH_FAILED,
            message: `凭证未配置。请先获取 userNo 和 apiKey，申请地址: ${types_1.CREDENTIAL_APPLY_URL}。` +
                `获取后请通过 set 方法配置凭证。`,
        };
    }
}
exports.CredentialManager = CredentialManager;
//# sourceMappingURL=credential-manager.js.map