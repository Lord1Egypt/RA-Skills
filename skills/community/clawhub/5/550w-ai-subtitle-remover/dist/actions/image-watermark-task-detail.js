"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.imageWatermarkTaskDetail = imageWatermarkTaskDetail;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const i18n_1 = require("../i18n");
async function imageWatermarkTaskDetail(params, client) {
    const validationError = (0, validator_1.validate)("imageWatermarkTaskDetail", params);
    if (validationError)
        return validationError;
    const response = await client.post("/open/imageWatermarkTaskDetail", { taskId: params.taskId }, types_1.TIMEOUT_CONFIG.query);
    if (response.code !== types_1.ErrorCode.SUCCESS)
        return (0, error_handler_1.mapApiError)(response, params.locale, params.region);
    const localized = { ...response, task: response.task ? { ...response.task } : response.task };
    localized.message = (0, i18n_1.localize)(params.locale, "图片任务查询成功", "Image task retrieved");
    if ((0, i18n_1.resolveLocale)(params.locale) === "en" && localized.task)
        delete localized.task.failReason;
    return localized;
}
//# sourceMappingURL=image-watermark-task-detail.js.map