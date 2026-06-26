"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.taskList = taskList;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
async function taskList(params, client) {
    const { page, size } = (0, validator_1.normalizePageParams)(params);
    const apiResponse = await client.post("/open/taskList", { page: String(page), size: String(size) }, types_1.TIMEOUT_CONFIG.query);
    if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse);
    }
    return {
        code: types_1.ErrorCode.SUCCESS,
        message: apiResponse.message || "success",
        total: apiResponse.total,
        page,
        size,
        list: apiResponse.list || [],
    };
}
//# sourceMappingURL=task-list.js.map