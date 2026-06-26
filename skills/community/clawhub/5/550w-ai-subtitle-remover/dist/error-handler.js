"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createErrorResponse = createErrorResponse;
exports.mapApiError = mapApiError;
exports.createTimeoutErrorResponse = createTimeoutErrorResponse;
const types_1 = require("./types");
function createErrorResponse(code, message) {
    return { code, message };
}
function mapApiError(apiResponse) {
    const { code, message } = apiResponse;
    if (code === types_1.ErrorCode.SUCCESS) {
        return { ...apiResponse };
    }
    switch (code) {
        case types_1.ErrorCode.AUTH_FAILED:
            return createErrorResponse(code, `鉴权失败: ${message}。请检查 userNo 和 apiKey 是否正确配置，如需重新获取凭证请访问 ${types_1.CREDENTIAL_APPLY_URL}`);
        case types_1.ErrorCode.INVALID_PARAMS:
            return createErrorResponse(code, `参数错误: ${message}`);
        case types_1.ErrorCode.BUSINESS_REJECTED:
            if (message.includes("积分不足")) {
                return createErrorResponse(code, `业务拒绝: ${message}。请前往平台充值积分后重试`);
            }
            return createErrorResponse(code, `业务拒绝: ${message}`);
        case types_1.ErrorCode.SERVER_ERROR:
            return createErrorResponse(code, `服务异常: ${message}。建议等待 30 秒后重试`);
        default:
            return createErrorResponse(code, `未知错误 (code=${code}): ${message}。建议联系服务方排查`);
    }
}
function createTimeoutErrorResponse(timeoutMs) {
    return createErrorResponse(types_1.ErrorCode.SERVER_ERROR, `网络超时: 请求在 ${timeoutMs / 1000} 秒内未收到响应。请检查网络连接后重试`);
}
//# sourceMappingURL=error-handler.js.map