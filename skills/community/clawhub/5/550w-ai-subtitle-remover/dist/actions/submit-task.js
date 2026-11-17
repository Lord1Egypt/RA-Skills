"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.submitTask = submitTask;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const i18n_1 = require("../i18n");
async function submitTask(params, client) {
    const validationError = (0, validator_1.validate)("submitTask", params);
    if (validationError)
        return validationError;
    const requestParams = {
        videoUrl: params.videoUrl,
        width: String(params.width),
        height: String(params.height),
        duration: String(params.duration),
        // Agent 场景固定全屏擦除，不接受或透传用户坐标。
        x1: "0",
        y1: "0",
        x2: "0",
        y2: "0",
    };
    if (params.fileName != null && params.fileName !== "")
        requestParams.fileName = String(params.fileName);
    if (params.coverUrl != null && params.coverUrl !== "")
        requestParams.coverUrl = String(params.coverUrl);
    if (params.callbackUrl != null && params.callbackUrl !== "")
        requestParams.callbackUrl = String(params.callbackUrl);
    if (params.removeAudio != null)
        requestParams.removeAudio = String(params.removeAudio);
    if (params.idempotencyKey != null && String(params.idempotencyKey).trim() !== "")
        requestParams.idempotencyKey = String(params.idempotencyKey).trim();
    if (params.subUserId != null && String(params.subUserId).trim() !== "")
        requestParams.subUserId = String(params.subUserId).trim();
    const apiResponse = await client.post("/open/submitTask", requestParams, types_1.TIMEOUT_CONFIG.submit);
    if (apiResponse.code === types_1.ErrorCode.SUCCESS) {
        return {
            code: types_1.ErrorCode.SUCCESS,
            message: (0, i18n_1.localize)(params.locale, "任务提交成功", "Task submitted"),
            taskId: apiResponse.taskId,
            status: "waiting",
            notice: params.idempotencyKey
                ? (0, i18n_1.localize)(params.locale, "相同幂等键和提交参数可安全重放并返回原任务", "The same idempotency key and submission parameters can be replayed safely to return the original task")
                : (0, i18n_1.localize)(params.locale, "注意：未提供幂等键时，相同 videoUrl 重复提交会被视为独立任务并独立计费", "Without an idempotency key, submitting the same videoUrl again creates a separate task and may be billed separately"),
        };
    }
    return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
}
//# sourceMappingURL=submit-task.js.map