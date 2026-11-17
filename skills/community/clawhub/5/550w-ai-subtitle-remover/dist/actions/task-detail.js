"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.taskDetail = taskDetail;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const i18n_1 = require("../i18n");
async function taskDetail(params, client) {
    const validationError = (0, validator_1.validate)("taskDetail", params);
    if (validationError)
        return validationError;
    const requestParams = { taskId: params.taskId };
    if (params.subUserId != null && String(params.subUserId).trim() !== "")
        requestParams.subUserId = String(params.subUserId).trim();
    const apiResponse = await client.post("/open/taskDetail", requestParams, types_1.TIMEOUT_CONFIG.query);
    if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
    }
    const { taskId, status, width, height, duration, cost, createTime, updateTime, resultUrl, failReason, failCode, refundStatus } = apiResponse;
    const response = {
        code: types_1.ErrorCode.SUCCESS,
        message: (0, i18n_1.localize)(params.locale, "查询成功", "Task retrieved"),
        taskId, status, width, height, duration, cost, createTime, updateTime,
        ...(failCode != null && { failCode }),
        ...(refundStatus != null && { refundStatus }),
    };
    switch (status) {
        case "success":
            response.resultUrl = resultUrl;
            break;
        case "failed":
            response.message = (0, i18n_1.localize)(params.locale, `任务处理失败：${failReason || "未知原因"}`, "Task processing failed");
            if ((0, i18n_1.resolveLocale)(params.locale) === "zh" && failReason)
                response.failReason = failReason;
            break;
        case "waiting":
        case "processing":
            response.message = (0, i18n_1.localize)(params.locale, `任务${status === "waiting" ? "等待中" : "处理中"}，建议 30 秒后再次查询`, `Task is ${status}; check again in about 30 seconds`);
            break;
    }
    return response;
}
//# sourceMappingURL=task-detail.js.map