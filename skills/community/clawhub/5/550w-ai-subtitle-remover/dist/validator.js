"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateCredential = validateCredential;
exports.normalizePageParams = normalizePageParams;
exports.estimateCredits = estimateCredits;
exports.validate = validate;
const types_1 = require("./types");
function validationError(message) {
    return { code: types_1.ErrorCode.INVALID_PARAMS, message };
}
function getFileExtension(filename) {
    const lastDot = filename.lastIndexOf(".");
    if (lastDot === -1)
        return "";
    return filename.slice(lastDot).toLowerCase();
}
function validateCredential(userNo, apiKey) {
    if (userNo == null || userNo.trim().length === 0) {
        return validationError("userNo 不能为空");
    }
    if (userNo.trim().length > types_1.MAX_CREDENTIAL_LENGTH) {
        return validationError(`userNo 长度不能超过 ${types_1.MAX_CREDENTIAL_LENGTH} 个字符`);
    }
    if (apiKey == null || apiKey.trim().length === 0) {
        return validationError("apiKey 不能为空");
    }
    if (apiKey.trim().length > types_1.MAX_CREDENTIAL_LENGTH) {
        return validationError(`apiKey 长度不能超过 ${types_1.MAX_CREDENTIAL_LENGTH} 个字符`);
    }
    return null;
}
function validateFile(file) {
    if (!file)
        return validationError("文件不能为空");
    if (!file.name || file.name.trim().length === 0)
        return validationError("文件名不能为空");
    if (file.size > types_1.MAX_FILE_SIZE) {
        return validationError(`文件大小超限，最大支持 1GB，当前文件大小为 ${file.size} 字节`);
    }
    const ext = getFileExtension(file.name);
    if (!types_1.SUPPORTED_VIDEO_EXTENSIONS.includes(ext)) {
        return validationError(`不支持的视频格式 "${ext}"，仅支持 mp4、mov 格式`);
    }
    return null;
}
function validateUrl(url) {
    if (url == null || url.trim().length === 0)
        return validationError("videoUrl 不能为空");
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return validationError("videoUrl 必须以 http:// 或 https:// 开头");
    }
    if (url.length > types_1.MAX_URL_LENGTH) {
        return validationError(`videoUrl 长度不能超过 ${types_1.MAX_URL_LENGTH} 个字符`);
    }
    return null;
}
function validateResolution(width, height) {
    if (width * height > types_1.MAX_RESOLUTION) {
        return validationError(`视频分辨率超限，最大支持 ${types_1.MAX_RESOLUTION} 像素（当前 ${width}×${height}=${width * height} 像素）`);
    }
    return null;
}
function validateDuration(duration) {
    if (duration == null || typeof duration !== "number" || !Number.isFinite(duration)) {
        return validationError("duration 必须为有效数字");
    }
    if (duration < 1 || duration > types_1.MAX_DURATION) {
        return validationError(`视频时长超限，有效范围为 1~${types_1.MAX_DURATION} 秒（当前 ${duration} 秒）`);
    }
    return null;
}
function validateDimension(value, fieldName) {
    if (value == null || typeof value !== "number" || !Number.isFinite(value)) {
        return validationError(`${fieldName} 必须为有效数字`);
    }
    if (!Number.isInteger(value))
        return validationError(`${fieldName} 必须为整数`);
    if (value < 1 || value > types_1.MAX_DIMENSION) {
        return validationError(`${fieldName} 超出有效范围，有效范围为 1~${types_1.MAX_DIMENSION}（当前 ${value}）`);
    }
    return null;
}
function validateCoordinates(x1, y1, x2, y2, width, height) {
    if (x1 === 0 && y1 === 0 && x2 === 0 && y2 === 0)
        return null;
    if (x2 <= x1)
        return validationError(`坐标范围错误：x2(${x2}) 必须大于 x1(${x1})`);
    if (y2 <= y1)
        return validationError(`坐标范围错误：y2(${y2}) 必须大于 y1(${y1})`);
    if (x2 > width)
        return validationError(`坐标范围错误：x2(${x2}) 不能超过视频宽度(${width})`);
    if (y2 > height)
        return validationError(`坐标范围错误：y2(${y2}) 不能超过视频高度(${height})`);
    return null;
}
function validateTaskId(taskId) {
    if (taskId == null || typeof taskId !== "string" || taskId.length === 0) {
        return validationError("taskId 不能为空");
    }
    if (taskId.length > types_1.MAX_TASK_ID_LENGTH) {
        return validationError(`taskId 长度不能超过 ${types_1.MAX_TASK_ID_LENGTH} 个字符`);
    }
    return null;
}
function normalizePageParams(params) {
    const page = params.page != null ? Math.max(0, Math.floor(params.page)) : 0;
    const size = params.size != null ? Math.min(100, Math.max(1, Math.floor(params.size))) : 20;
    return { page, size };
}
function estimateCredits(width, height, duration) {
    const pixels = width * height;
    const isAbove720p = pixels > types_1.RESOLUTION_720P_THRESHOLD;
    const rate = isAbove720p ? types_1.RATE_ABOVE_720P : types_1.RATE_720P_OR_BELOW;
    const estimatedCost = Math.ceil(duration * rate);
    return { estimatedCost, resolution: isAbove720p ? "above_720p" : "720p_or_below" };
}
function validateUploadVideo(params) {
    return validateFile(params.file);
}
function validateSubmitTask(params) {
    const urlError = validateUrl(params.videoUrl);
    if (urlError)
        return urlError;
    const widthError = validateDimension(params.width, "width");
    if (widthError)
        return widthError;
    const heightError = validateDimension(params.height, "height");
    if (heightError)
        return heightError;
    const durationError = validateDuration(params.duration);
    if (durationError)
        return durationError;
    const resolutionError = validateResolution(params.width, params.height);
    if (resolutionError)
        return resolutionError;
    const coordError = validateCoordinates(params.x1, params.y1, params.x2, params.y2, params.width, params.height);
    if (coordError)
        return coordError;
    return null;
}
function validateEstimateCredits(params) {
    const widthError = validateDimension(params.width, "width");
    if (widthError)
        return widthError;
    const heightError = validateDimension(params.height, "height");
    if (heightError)
        return heightError;
    const durationError = validateDuration(params.duration);
    if (durationError)
        return durationError;
    return null;
}
function validate(action, params) {
    switch (action) {
        case "uploadVideo": return validateUploadVideo(params);
        case "submitTask": return validateSubmitTask(params);
        case "taskDetail": return validateTaskId(params.taskId);
        case "taskList": return null;
        case "queryCredits": return null;
        case "estimateCredits": return validateEstimateCredits(params);
        case "workflow": {
            if (params.file)
                return validateFile(params.file);
            if (params.videoUrl)
                return validateSubmitTask(params);
            return validationError("workflow 模式需要提供 file 或 videoUrl 参数");
        }
        default: return validationError(`不支持的 action: ${action}`);
    }
}
//# sourceMappingURL=validator.js.map