"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateCredential = validateCredential;
exports.normalizePageParams = normalizePageParams;
exports.estimateCredits = estimateCredits;
exports.validate = validate;
const types_1 = require("./types");
const i18n_1 = require("./i18n");
function validationError(locale, zh, en) {
    return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_1.localize)(locale, zh, en) };
}
function getFileExtension(filename) {
    const lastDot = filename.lastIndexOf(".");
    if (lastDot === -1)
        return "";
    return filename.slice(lastDot).toLowerCase();
}
function validateCredential(userNo, apiKey, locale) {
    if (typeof userNo !== "string" || userNo.trim().length === 0) {
        return validationError(locale, "userNo 不能为空", "userNo is required");
    }
    if (userNo.trim().length > types_1.MAX_CREDENTIAL_LENGTH) {
        return validationError(locale, `userNo 长度不能超过 ${types_1.MAX_CREDENTIAL_LENGTH} 个字符`, `userNo must not exceed ${types_1.MAX_CREDENTIAL_LENGTH} characters`);
    }
    if (typeof apiKey !== "string" || apiKey.trim().length === 0) {
        return validationError(locale, "apiKey 不能为空", "apiKey is required");
    }
    if (apiKey.trim().length > types_1.MAX_CREDENTIAL_LENGTH) {
        return validationError(locale, `apiKey 长度不能超过 ${types_1.MAX_CREDENTIAL_LENGTH} 个字符`, `apiKey must not exceed ${types_1.MAX_CREDENTIAL_LENGTH} characters`);
    }
    return null;
}
function validateFile(file, locale) {
    if (!file)
        return validationError(locale, "文件不能为空", "A video file is required");
    if (typeof file.name !== "string" || file.name.trim().length === 0)
        return validationError(locale, "文件名不能为空", "The video filename is required");
    const size = Number(file.size ?? file.data?.length);
    if (Number.isFinite(size) && size > types_1.MAX_FILE_SIZE) {
        return validationError(locale, `文件大小超限，最大支持 1GB，当前文件大小为 ${size} 字节`, `The video exceeds the 1 GB limit (${size} bytes)`);
    }
    const ext = getFileExtension(file.name);
    if (!types_1.SUPPORTED_VIDEO_EXTENSIONS.includes(ext)) {
        return validationError(locale, `不支持的视频格式 "${ext}"，仅支持 mp4、mov 格式`, `Unsupported video format "${ext}"; use MP4 or MOV`);
    }
    return null;
}
function validateImageFile(file, locale) {
    if (!file)
        return validationError(locale, "图片文件不能为空", "An image file is required");
    if (typeof file.name !== "string" || file.name.trim().length === 0)
        return validationError(locale, "图片文件名不能为空", "The image filename is required");
    const size = Number(file.size ?? file.data?.length);
    if (Number.isFinite(size) && size > types_1.MAX_IMAGE_FILE_SIZE)
        return validationError(locale, "图片大小不能超过 50MB", "The image must not exceed 50 MB");
    const ext = getFileExtension(file.name);
    if (!types_1.SUPPORTED_IMAGE_EXTENSIONS.includes(ext)) {
        return validationError(locale, `不支持的图片格式 "${ext}"，支持 JPG、PNG、BMP、WebP、AVIF、TIFF、SVG`, `Unsupported image format "${ext}"; use JPG, PNG, BMP, WebP, AVIF, TIFF, or SVG`);
    }
    return null;
}
function validateUrl(url, locale) {
    if (typeof url !== "string" || url.trim().length === 0)
        return validationError(locale, "videoUrl 不能为空", "videoUrl is required");
    url = url.trim();
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return validationError(locale, "videoUrl 必须以 http:// 或 https:// 开头", "videoUrl must start with http:// or https://");
    }
    if (url.length > types_1.MAX_URL_LENGTH) {
        return validationError(locale, `videoUrl 长度不能超过 ${types_1.MAX_URL_LENGTH} 个字符`, `videoUrl must not exceed ${types_1.MAX_URL_LENGTH} characters`);
    }
    return null;
}
function validateResolution(width, height, locale) {
    if (Math.max(width, height) > 1920 || Math.min(width, height) > 1080) {
        return validationError(locale, `视频分辨率超限，要求最大边不超过 1920 且最小边不超过 1080（当前 ${width}×${height}）`, `Video resolution exceeds the limit: longest side 1920 and shortest side 1080 (received ${width}×${height})`);
    }
    return null;
}
function validateDuration(duration, locale) {
    if (duration == null || typeof duration !== "number" || !Number.isFinite(duration)) {
        return validationError(locale, "duration 必须为有效数字", "duration must be a valid number");
    }
    if (duration < 1 || duration > types_1.MAX_DURATION) {
        return validationError(locale, `视频时长超限，有效范围为 1~${types_1.MAX_DURATION} 秒（当前 ${duration} 秒）`, `Video duration must be between 1 and ${types_1.MAX_DURATION} seconds (received ${duration})`);
    }
    return null;
}
function validateDimension(value, fieldName, locale) {
    if (value == null || typeof value !== "number" || !Number.isFinite(value)) {
        return validationError(locale, `${fieldName} 必须为有效数字`, `${fieldName} must be a valid number`);
    }
    if (!Number.isInteger(value))
        return validationError(locale, `${fieldName} 必须为整数`, `${fieldName} must be an integer`);
    if (value < 1 || value > types_1.MAX_DIMENSION) {
        return validationError(locale, `${fieldName} 超出有效范围，有效范围为 1~${types_1.MAX_DIMENSION}（当前 ${value}）`, `${fieldName} must be between 1 and ${types_1.MAX_DIMENSION} (received ${value})`);
    }
    return null;
}
function validateTaskId(taskId, locale) {
    if (typeof taskId !== "string" || taskId.trim().length === 0) {
        return validationError(locale, "taskId 不能为空", "taskId is required");
    }
    if (taskId.trim().length > types_1.MAX_TASK_ID_LENGTH) {
        return validationError(locale, `taskId 长度不能超过 ${types_1.MAX_TASK_ID_LENGTH} 个字符`, `taskId must not exceed ${types_1.MAX_TASK_ID_LENGTH} characters`);
    }
    return null;
}
function validateOperationId(operationId, locale) {
    if (operationId == null || operationId === "")
        return null;
    if (typeof operationId !== "string" || !/^[A-Za-z0-9._:-]{8,64}$/.test(operationId.trim())) {
        return validationError(locale, "operationId 必须为 8–64 位，且只能包含字母、数字、点、下划线、冒号和连字符", "operationId must be 8–64 characters using only letters, numbers, periods, underscores, colons, and hyphens");
    }
    return null;
}
function validateIdempotencyKey(value, locale) {
    if (value == null || value === "")
        return null;
    if (typeof value !== "string" || !/^[A-Za-z0-9._:-]{8,128}$/.test(value.trim())) {
        return validationError(locale, "idempotencyKey 必须为 8–128 位，且只能包含字母、数字、点、下划线、冒号和连字符", "idempotencyKey must be 8–128 characters using only letters, numbers, periods, underscores, colons, and hyphens");
    }
    return null;
}
function validateSubUserId(value, locale) {
    if (value == null || value === "")
        return null;
    if (typeof value !== "string" || value.trim().length > 128) {
        return validationError(locale, "subUserId 长度不能超过 128 个字符", "subUserId must not exceed 128 characters");
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
    return validateFile(params.file, params.locale);
}
function validateSubmitTask(params) {
    const urlError = validateUrl(params.videoUrl, params.locale);
    if (urlError)
        return urlError;
    const widthError = validateDimension(params.width, "width", params.locale);
    if (widthError)
        return widthError;
    const heightError = validateDimension(params.height, "height", params.locale);
    if (heightError)
        return heightError;
    const durationError = validateDuration(params.duration, params.locale);
    if (durationError)
        return durationError;
    const resolutionError = validateResolution(params.width, params.height, params.locale);
    if (resolutionError)
        return resolutionError;
    if (params.removeAudio != null && typeof params.removeAudio !== "boolean") {
        return validationError(params.locale, "removeAudio 必须为 boolean", "removeAudio must be a boolean");
    }
    return validateIdempotencyKey(params.idempotencyKey, params.locale) || validateSubUserId(params.subUserId, params.locale);
}
function validateEstimateCredits(params) {
    const widthError = validateDimension(params.width, "width", params.locale);
    if (widthError)
        return widthError;
    const heightError = validateDimension(params.height, "height", params.locale);
    if (heightError)
        return heightError;
    const durationError = validateDuration(params.duration, params.locale);
    if (durationError)
        return durationError;
    return null;
}
function validate(action, params) {
    switch (action) {
        case "uploadVideo": return validateUploadVideo(params);
        case "submitTask": return validateSubmitTask(params);
        case "taskDetail": return validateTaskId(params.taskId, params.locale) || validateSubUserId(params.subUserId, params.locale);
        case "taskList": return validateSubUserId(params.subUserId, params.locale);
        case "deleteTask": {
            const taskError = validateTaskId(params.taskId, params.locale);
            if (taskError)
                return taskError;
            return validateSubUserId(params.subUserId, params.locale);
        }
        case "queryCredits": return null;
        case "removeVideoWatermark": {
            const urlError = validateUrl(params.videoUrl, params.locale);
            return urlError || validateOperationId(params.operationId, params.locale);
        }
        case "removeImageWatermark": {
            const fileError = validateImageFile(params.file, params.locale);
            if (fileError)
                return fileError;
            if (params.sync != null && typeof params.sync !== "boolean")
                return validationError(params.locale, "sync 必须为 boolean", "sync must be a boolean");
            return null;
        }
        case "imageWatermarkTaskDetail": return validateTaskId(params.taskId, params.locale);
        case "estimateCredits": return validateEstimateCredits(params);
        case "workflow": {
            if (params.file && params.videoUrl)
                return validationError(params.locale, "file 和 videoUrl 只能提供一个", "Provide either filePath or videoUrl, not both");
            if (params.file)
                return validateFile(params.file, params.locale);
            if (params.videoUrl) {
                const urlError = validateUrl(params.videoUrl, params.locale);
                if (urlError)
                    return urlError;
                if (params.removeAudio != null && typeof params.removeAudio !== "boolean") {
                    return validationError(params.locale, "removeAudio 必须为 boolean", "removeAudio must be a boolean");
                }
                const suppliedMetadata = [params.width, params.height, params.duration].filter((value) => value != null).length;
                if (suppliedMetadata !== 0 && suppliedMetadata !== 3) {
                    return validationError(params.locale, "width、height、duration 必须全部提供或全部省略", "Provide width, height, and duration together, or omit all three");
                }
                if (suppliedMetadata === 3) {
                    const metadataError = validateEstimateCredits(params);
                    if (metadataError)
                        return metadataError;
                    const resolutionError = validateResolution(params.width, params.height, params.locale);
                    if (resolutionError)
                        return resolutionError;
                }
                return validateIdempotencyKey(params.idempotencyKey, params.locale) || validateSubUserId(params.subUserId, params.locale);
            }
            return validationError(params.locale, "需要提供 file 或 videoUrl 参数", "Provide either filePath or videoUrl");
        }
        default: return validationError(params.locale, `不支持的 action：${action}`, `Unsupported action: ${action}`);
    }
}
//# sourceMappingURL=validator.js.map