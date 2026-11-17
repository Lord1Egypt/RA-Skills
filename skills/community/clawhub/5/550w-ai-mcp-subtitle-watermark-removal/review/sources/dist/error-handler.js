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
function mapApiError(apiResponse, locale, region, sideEffect = false) {
    const { code, message } = apiResponse;
    if (code === types_1.ErrorCode.SUCCESS) {
        return { ...apiResponse };
    }
    const insufficientCredits = (code === types_1.ErrorCode.AUTH_FAILED || code === types_1.ErrorCode.BUSINESS_REJECTED)
        && (/积分不足|点数不足|余额不足|insufficient\s+(?:subtitle-removal\s+)?credits/i.test(String(message || ""))
            || String(apiResponse.errorCode || "").toUpperCase() === "INSUFFICIENT_CREDITS");
    if (insufficientCredits) {
        const purchaseUrl = (0, i18n_1.creditPurchaseUrl)(locale, region);
        return {
            code,
            message: (0, i18n_1.localize)(locale, `积分不足。请前往 ${purchaseUrl} 购买积分，到账后再提交任务。`, `Insufficient credits. Buy credits at ${purchaseUrl}, then submit the task after your balance updates.`),
            purchaseUrl,
        };
    }
    const errorCode = String(apiResponse.errorCode || "").toUpperCase();
    const reason = String(message || "");
    if (errorCode === "IMAGE_TOO_LARGE") {
        return createErrorResponse(code, (0, i18n_1.localize)(locale, "图片超过 50 MB，请缩小后重新选择。", "The image exceeds 50 MB. Choose a smaller image."));
    }
    if (errorCode === "INVALID_OR_UNSUPPORTED_IMAGE") {
        return createErrorResponse(code, (0, i18n_1.localize)(locale, "图片无法解析或格式不受支持，请换用有效的 JPG、PNG、WebP 等支持格式。", "The image could not be read or its format is unsupported. Choose a valid JPG, PNG, WebP, or other supported image."));
    }
    if (code === types_1.ErrorCode.INVALID_PARAMS && /idempotencyKey.*(不同|different)/i.test(reason)) {
        return createErrorResponse(code, (0, i18n_1.localize)(locale, "这个幂等键已用于其他提交参数；请核对原任务，新的输入需使用新键。", "This idempotency key was used with different inputs. Check the original task; use a new key for a new submission."));
    }
    if (code === types_1.ErrorCode.INVALID_PARAMS && /operationId.*(不一致|different|mismatch)/i.test(reason)) {
        return createErrorResponse(code, (0, i18n_1.localize)(locale, "这个操作 ID 已用于其他视频链接；相同链接才可复用，新的链接请使用新 ID。", "This operation ID belongs to another video link. Reuse it only for the same link, or use a new ID."));
    }
    if (code === types_1.ErrorCode.BUSINESS_REJECTED && (/task.*(not exist|not accessible)/i.test(reason) || /任务不存在|无权访问/.test(reason))) {
        return createErrorResponse(code, (0, i18n_1.localize)(locale, "任务不存在或无权访问；请核对任务 ID、账号及子用户范围。", "Task not found or inaccessible. Check the task ID, account, and sub-user scope."));
    }
    switch (code) {
        case types_1.ErrorCode.AUTH_FAILED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `鉴权失败。请检查同一账号的用户 ID 和 API Key，并到 ${(0, i18n_1.credentialApplyUrl)(locale, region)} 管理凭据。`, `Authentication failed. Check the user ID and API key from the same account at ${(0, i18n_1.credentialApplyUrl)(locale, region)}.`));
        case types_1.ErrorCode.INVALID_PARAMS:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `参数错误：${message}。请核对输入后再试。`, `The service rejected the input. Check the URL, file, and required fields before trying again.`));
        case types_1.ErrorCode.BUSINESS_REJECTED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `请求未完成：${message}。请核对链接或任务状态后再决定是否重试。`, `The service could not complete the request. Check the link or task status before deciding whether to retry.`));
        case types_1.ErrorCode.ACCOUNT_TEMPORARILY_BLOCKED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `账号暂时受限：${message}`, "The account is temporarily restricted. Stop submitting requests until the restriction expires."));
        case types_1.ErrorCode.ACCOUNT_PERMANENTLY_BLOCKED:
            return createErrorResponse(code, (0, i18n_1.localize)(locale, `账号已被永久限制：${message}`, "The account is permanently restricted. Stop submitting requests and contact support if you believe this is an error."));
        case types_1.ErrorCode.SERVER_ERROR:
            return createErrorResponse(code, sideEffect
                ? (0, i18n_1.localize)(locale, "服务或网络异常，提交结果可能尚未确定。先核查已有任务或原操作结果，不要直接重复提交计费请求。", "A service or network error left the submission outcome uncertain. Check the existing task or operation result before another billed submission.")
                : (0, i18n_1.localize)(locale, "服务或网络暂时不可用，请稍后重新查询。", "The service or network is temporarily unavailable. Try the read-only request again later."));
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