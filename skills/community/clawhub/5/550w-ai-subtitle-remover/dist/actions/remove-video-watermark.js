"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.removeVideoWatermark = removeVideoWatermark;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const i18n_1 = require("../i18n");
async function removeVideoWatermark(params, client) {
    const rawInput = typeof params.videoUrl === "string" ? params.videoUrl.trim() : "";
    const extractedUrl = rawInput.match(/https?:\/\/[^\s]+/i)?.[0]?.replace(/[，。；;！!）)】\]]+$/, "") || rawInput;
    const normalizedParams = { ...params, videoUrl: extractedUrl };
    const validationError = (0, validator_1.validate)("removeVideoWatermark", normalizedParams);
    if (validationError)
        return validationError;
    const response = await client.post("/open/removeVideoWatermark", { videoUrl: extractedUrl, ...(params.operationId ? { operationId: params.operationId.trim() } : {}) }, types_1.TIMEOUT_CONFIG.videoWatermark);
    return response.code === types_1.ErrorCode.SUCCESS
        ? { ...response, message: (0, i18n_1.localize)(params.locale, "视频去水印完成", "Video watermark removal completed") }
        : (0, error_handler_1.mapApiError)(response, params.locale, params.region);
}
//# sourceMappingURL=remove-video-watermark.js.map