"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.taskList = taskList;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const i18n_1 = require("../i18n");
async function taskList(params, client) {
    const { page, size } = (0, validator_1.normalizePageParams)(params);
    const requestParams = { page: String(page), size: String(size) };
    if (params.subUserId != null && String(params.subUserId).trim() !== "")
        requestParams.subUserId = String(params.subUserId).trim();
    const apiResponse = await client.post("/open/taskList", requestParams, types_1.TIMEOUT_CONFIG.query);
    if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
    }
    return {
        code: types_1.ErrorCode.SUCCESS,
        message: (0, i18n_1.localize)(params.locale, "查询成功", "Tasks retrieved"),
        total: apiResponse.total,
        page,
        size,
        list: (apiResponse.list || []).map((item) => {
            const publicItem = { ...item };
            delete publicItem.x1;
            delete publicItem.y1;
            delete publicItem.x2;
            delete publicItem.y2;
            delete publicItem.mode;
            if (params.locale && !String(params.locale).toLowerCase().startsWith("zh"))
                delete publicItem.failReason;
            return publicItem;
        }),
    };
}
//# sourceMappingURL=task-list.js.map