"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.taskDetail = taskDetail;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
async function taskDetail(params, client) {
    const validationError = (0, validator_1.validate)("taskDetail", params);
    if (validationError)
        return validationError;
    const apiResponse = await client.post("/open/taskDetail", { taskId: params.taskId }, types_1.TIMEOUT_CONFIG.query);
    if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse);
    }
    const { taskId, status, width, height, duration, x1, y1, x2, y2, mode, cost, createTime, updateTime, resultUrl, failReason } = apiResponse;
    const response = {
        code: types_1.ErrorCode.SUCCESS,
        message: "查询成功",
        taskId, status, width, height, duration, x1, y1, x2, y2, mode, cost, createTime, updateTime,
    };
    switch (status) {
        case "success":
            response.resultUrl = resultUrl;
            break;
        case "failed":
            response.failReason = failReason;
            break;
        case "waiting":
        case "processing":
            response.message = `任务${status === "waiting" ? "等待中" : "处理中"}，建议 30 秒后再次查询`;
            break;
    }
    return response;
}
//# sourceMappingURL=task-detail.js.map