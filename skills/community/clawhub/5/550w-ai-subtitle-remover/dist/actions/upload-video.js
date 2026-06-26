"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.uploadVideo = uploadVideo;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
async function uploadVideo(params, client) {
    const validationError = (0, validator_1.validate)("uploadVideo", params);
    if (validationError)
        return validationError;
    const file = params.file;
    const apiResponse = await client.upload("/open/uploadVideo", {}, { name: file.name, data: file.data ?? file }, types_1.TIMEOUT_CONFIG.upload);
    if (apiResponse.code === types_1.ErrorCode.SUCCESS) {
        return {
            code: types_1.ErrorCode.SUCCESS,
            message: "上传成功",
            videoUrl: apiResponse.videoUrl,
            coverUrl: apiResponse.coverUrl,
            width: apiResponse.width,
            height: apiResponse.height,
            duration: apiResponse.duration,
        };
    }
    return (0, error_handler_1.mapApiError)(apiResponse);
}
//# sourceMappingURL=upload-video.js.map