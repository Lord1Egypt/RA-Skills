"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteTask = deleteTask;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const i18n_1 = require("../i18n");
async function deleteTask(params, client) {
    const validationError = (0, validator_1.validate)("deleteTask", params);
    if (validationError)
        return validationError;
    const requestParams = { taskId: params.taskId.trim() };
    if (params.subUserId != null && String(params.subUserId).trim() !== "") {
        requestParams.subUserId = String(params.subUserId).trim();
    }
    const response = await client.post("/open/deleteTask", requestParams, types_1.TIMEOUT_CONFIG.query);
    return response.code === types_1.ErrorCode.SUCCESS
        ? { ...response, message: (0, i18n_1.localize)(params.locale, "任务已删除，相关媒体将异步清理；已扣积分不会退还", "Task deleted. Related media will be cleaned up asynchronously; charged credits are not refunded.") }
        : (0, error_handler_1.mapApiError)(response, params.locale, params.region);
}
//# sourceMappingURL=delete-task.js.map