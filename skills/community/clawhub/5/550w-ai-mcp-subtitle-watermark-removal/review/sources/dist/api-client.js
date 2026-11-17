"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TIMEOUT_CONFIG = exports.ApiClient = void 0;
const node_https_1 = __importDefault(require("node:https"));
const node_crypto_1 = require("node:crypto");
const node_stream_1 = require("node:stream");
const types_1 = require("./types");
Object.defineProperty(exports, "TIMEOUT_CONFIG", { enumerable: true, get: function () { return types_1.TIMEOUT_CONFIG; } });
const i18n_1 = require("./i18n");
class ApiClient {
    constructor(credential, locale) {
        this.credential = credential;
        this.baseUrl = types_1.BASE_URL;
        this.locale = locale;
    }
    async post(endpoint, params, timeout) {
        try {
            const body = new URLSearchParams({
                userNo: this.credential.userNo,
                apiKey: this.credential.apiKey,
                ...params,
            });
            return this.parseResponse(await this.request(endpoint, body.toString(), {
                "Content-Type": "application/x-www-form-urlencoded",
            }, timeout));
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    async upload(endpoint, params, file, timeout, fieldName = "file") {
        try {
            const boundary = `550w-${(0, node_crypto_1.randomBytes)(16).toString("hex")}`;
            const fields = { userNo: this.credential.userNo, apiKey: this.credential.apiKey, ...params };
            const part = (name, value) => `--${boundary}\r\nContent-Disposition: form-data; name="${this.safeHeader(name)}"\r\n\r\n${value}\r\n`;
            const chunks = Object.entries(fields).map(([name, value]) => part(name, value));
            chunks.push(`--${boundary}\r\nContent-Disposition: form-data; name="${this.safeHeader(fieldName)}"; filename="${this.safeHeader(file.name)}"\r\nContent-Type: application/octet-stream\r\n\r\n`);
            const body = node_stream_1.Readable.from((async function* () {
                for (const chunk of chunks)
                    yield chunk;
                if (Buffer.isBuffer(file.data))
                    yield file.data;
                else
                    for await (const chunk of file.data)
                        yield chunk;
                yield `\r\n--${boundary}--\r\n`;
            })());
            return this.parseResponse(await this.request(endpoint, body, {
                "Content-Type": `multipart/form-data; boundary=${boundary}`,
            }, timeout));
        }
        catch (error) {
            return this.handleError(error);
        }
    }
    safeHeader(value) {
        return value.replace(/[\r\n"\\]/g, "_");
    }
    request(endpoint, body, headers, timeout) {
        return new Promise((resolve, reject) => {
            const url = new URL(endpoint, this.baseUrl);
            if (url.origin !== new URL(this.baseUrl).origin) {
                reject(new Error("Invalid API endpoint"));
                return;
            }
            const request = node_https_1.default.request(url, { method: "POST", headers }, (response) => {
                const chunks = [];
                let size = 0;
                response.on("data", (chunk) => {
                    size += chunk.length;
                    if (size > 2 * 1024 * 1024) {
                        request.destroy(new Error("API response too large"));
                        return;
                    }
                    chunks.push(chunk);
                });
                response.on("end", () => {
                    clearTimeout(timer);
                    if ((response.statusCode ?? 0) >= 300 && (response.statusCode ?? 0) < 400) {
                        reject(new Error("API redirects are not allowed"));
                        return;
                    }
                    try {
                        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8")));
                    }
                    catch (error) {
                        reject(error);
                    }
                });
                response.on("error", reject);
            });
            const timer = setTimeout(() => {
                const error = Object.assign(new Error("Request timed out"), { code: "ETIMEDOUT" });
                request.destroy(error);
            }, timeout);
            request.on("error", (error) => {
                clearTimeout(timer);
                if (body instanceof node_stream_1.Readable)
                    body.destroy();
                reject(error);
            });
            if (body instanceof node_stream_1.Readable) {
                body.on("error", (error) => request.destroy(error));
                body.pipe(request);
            }
            else
                request.end(body);
        });
    }
    parseResponse(data) {
        if (data == null || typeof data.code === "undefined") {
            return { code: -500, message: (0, i18n_1.localize)(this.locale, "响应格式异常", "The service returned an invalid response") };
        }
        return data;
    }
    handleError(error) {
        const responseData = error?.response?.data;
        if (responseData != null && typeof responseData.code !== "undefined") {
            return this.parseResponse(responseData);
        }
        if (error?.code === "ECONNABORTED" || error?.code === "ETIMEDOUT") {
            return { code: -500, message: (0, i18n_1.localize)(this.locale, "请求超时，请检查网络连接后重试", "The request timed out; check your connection and try again") };
        }
        return { code: -500, message: (0, i18n_1.localize)(this.locale, "网络请求失败，请检查网络连接后重试", "Network request failed; check your connection and try again") };
    }
}
exports.ApiClient = ApiClient;
//# sourceMappingURL=api-client.js.map