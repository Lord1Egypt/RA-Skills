"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TIMEOUT_CONFIG = exports.ApiClient = void 0;
const axios_1 = __importDefault(require("axios"));
const form_data_1 = __importDefault(require("form-data"));
const types_1 = require("./types");
Object.defineProperty(exports, "TIMEOUT_CONFIG", { enumerable: true, get: function () { return types_1.TIMEOUT_CONFIG; } });
class ApiClient {
    constructor(credential) {
        this.credential = credential;
        this.baseUrl = types_1.BASE_URL;
    }
    async post(endpoint, params, timeout) {
        try {
            const body = new URLSearchParams({
                userNo: this.credential.userNo,
                apiKey: this.credential.apiKey,
                ...params,
            });
            const response = await axios_1.default.post(`${this.baseUrl}${endpoint}`, body.toString(), {
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                timeout,
            });
            return this.parseResponse(response.data);
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    async upload(endpoint, params, file, timeout) {
        try {
            const form = new form_data_1.default();
            form.append("userNo", this.credential.userNo);
            form.append("apiKey", this.credential.apiKey);
            for (const [key, value] of Object.entries(params)) {
                form.append(key, value);
            }
            form.append("file", file.data, { filename: file.name });
            const response = await axios_1.default.post(`${this.baseUrl}${endpoint}`, form, {
                headers: form.getHeaders(),
                timeout,
            });
            return this.parseResponse(response.data);
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    parseResponse(data) {
        if (data == null || typeof data.code === "undefined") {
            return { code: -500, message: "响应格式异常" };
        }
        return data;
    }
    handleError(error) {
        if (error?.code === "ECONNABORTED" || error?.code === "ETIMEDOUT") {
            return { code: -500, message: "请求超时，请检查网络连接后重试" };
        }
        const msg = error?.message || "未知错误";
        return { code: -500, message: `网络请求失败: ${msg}` };
    }
}
exports.ApiClient = ApiClient;
//# sourceMappingURL=api-client.js.map