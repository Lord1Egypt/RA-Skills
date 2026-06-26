"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.submitTask = submitTask;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
async function submitTask(params, client) {
    const validationError = (0, validator_1.validate)("submitTask", params);
    if (validationError)
        return validationError;
    const requestParams = {
        videoUrl: params.videoUrl,
        width: String(params.width),
        height: String(params.height),
        duration: String(params.duration),
        x1: String(params.x1),
        y1: String(params.y1),
        x2: String(params.x2),
        y2: String(params.y2),
    };
    if (params.mode != null && params.mode !== "")
        requestParams.mode = String(params.mode);
    if (params.fileName != null && params.fileName !== "")
        requestParams.fileName = String(params.fileName);
    if (params.coverUrl != null && params.coverUrl !== "")
        requestParams.coverUrl = String(params.coverUrl);
    const apiResponse = await client.post("/open/submitTask", requestParams, types_1.TIMEOUT_CONFIG.submit);
    if (apiResponse.code === types_1.ErrorCode.SUCCESS) {
        return {
            code: types_1.ErrorCode.SUCCESS,
            message: "任务提交成功",
            taskId: apiResponse.taskId,
            status: "waiting",
            notice: "注意：相同 videoUrl 重复提交会被视为独立任务并独立计费",
        };
    }
    return (0, error_handler_1.mapApiError)(apiResponse);
}
//# sourceMappingURL=submit-task.js.map