"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.imageWatermarkTaskDetail = imageWatermarkTaskDetail;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
const image_task_result_1 = require("../image-task-result");
async function imageWatermarkTaskDetail(params, client) {
    const validationError = (0, validator_1.validate)("imageWatermarkTaskDetail", params);
    if (validationError)
        return validationError;
    const response = await client.post("/open/imageWatermarkTaskDetail", { taskId: params.taskId }, types_1.TIMEOUT_CONFIG.query);
    if (response.code !== types_1.ErrorCode.SUCCESS)
        return (0, error_handler_1.mapApiError)(response, params.locale, params.region);
    return (0, image_task_result_1.imageTaskResult)(response, params.locale);
}
//# sourceMappingURL=image-watermark-task-detail.js.map