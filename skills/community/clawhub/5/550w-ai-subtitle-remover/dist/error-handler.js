"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createErrorResponse = createErrorResponse;
exports.mapApiError = mapApiError;
exports.createTimeoutErrorResponse = createTimeoutErrorResponse;
const types_1 = require("./types");
const i18n_1 = require("./i18n");
function createErrorResponse(code, message) {
    return { code, message };
}
function mapApiError(apiResponse, locale, region) {
    const { code, message } = apiResponse;
    if (code === types_1.ErrorCode.SUCCESS) {
        return { ...apiResponse };
    }
    switch (code) {
        case types_1.ErrorCode.AUTH_FAILED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `请求未通过：${message}。请检查凭证或积分余额，并访问 ${(0, i18n_1.credentialApplyUrl)(locale, region)} 管理凭证。`, `Authentication or credit check failed. Check your credentials or balance, and manage your API key at ${(0, i18n_1.credentialApplyUrl)(locale, region)}.`));
        case types_1.ErrorCode.INVALID_PARAMS:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `参数错误：${message}`, `The service rejected one or more request parameters.`));
        case types_1.ErrorCode.BUSINESS_REJECTED:
            if (message.includes("积分不足")) {
                return createErrorResponse(code, (0, i18n_1.localize)(locale, `业务拒绝：${message}。请充值积分后重试。`, `Request rejected: insufficient credits. Add credits and try again.`));
            }
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `业务拒绝：${message}`, `The service rejected the request. Check the input and account status before trying again.`));
        case types_1.ErrorCode.ACCOUNT_TEMPORARILY_BLOCKED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `账号暂时受限：${message}`, "The account is temporarily restricted. Stop submitting requests until the restriction expires."));
        case types_1.ErrorCode.ACCOUNT_PERMANENTLY_BLOCKED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `账号已被永久限制：${message}`, "The account is permanently restricted. Stop submitting requests and contact support if you believe this is an error."));
        case types_1.ErrorCode.SERVER_ERROR:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `服务异常：${message}。请稍后重试。`, `The service is temporarily unavailable. Try again later; do not resubmit a billed task if its outcome is uncertain.`));
        case types_1.ErrorCode.UNSUPPORTED_VIDEO:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, "视频格式不受支持。请重新导出为兼容的 MP4 或 MOV（建议 8-bit SDR），然后重试。", "The video format is unsupported. Export a compatible MP4 or MOV file (8-bit SDR recommended) and try again."));
        default:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `未知错误（code=${code}）：${message}。请联系服务方。`, `Unexpected service error (code=${code}). Contact support.`));
    }
}
function createTimeoutErrorResponse(timeoutMs, locale) {
    return createErrorResponse(types_1.ErrorCode.SERVER_ERROR, (0, i18n_1.localize)(locale, `网络超时：请求在 ${timeoutMs / 1000} 秒内未收到响应。请检查网络连接后重试。`, `Network timeout: no response within ${timeoutMs / 1000} seconds. Check your connection and try again.`));
}
//# sourceMappingURL=error-handler.js.map