"use strict";
// ============================================================
// ai-subtitle-remover Skill - 核心类型与接口定义
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.SUPPORTED_IMAGE_EXTENSIONS = exports.SUPPORTED_VIDEO_EXTENSIONS = exports.CREDENTIAL_APPLY_URL = exports.CREDENTIAL_APPLY_URL_EN = exports.CREDENTIAL_APPLY_URL_ZH = exports.BASE_URL = exports.RATE_ABOVE_720P = exports.RATE_720P_OR_BELOW = exports.RESOLUTION_720P_THRESHOLD = exports.MAX_CONSECUTIVE_FAILURES = exports.MAX_POLL_COUNT = exports.POLL_INTERVAL = exports.MAX_IMAGE_FILE_SIZE = exports.MAX_CREDENTIAL_LENGTH = exports.MAX_TASK_ID_LENGTH = exports.MAX_DIMENSION = exports.MAX_DURATION = exports.MAX_URL_LENGTH = exports.MAX_FILE_SIZE = exports.TIMEOUT_CONFIG = exports.ErrorCode = void 0;
// ======================== 错误码 ========================
var ErrorCode;
(function (ErrorCode) {
    ErrorCode[ErrorCode["SUCCESS"] = 200] = "SUCCESS";
    ErrorCode[ErrorCode["AUTH_FAILED"] = -100] = "AUTH_FAILED";
    ErrorCode[ErrorCode["INVALID_PARAMS"] = -200] = "INVALID_PARAMS";
    ErrorCode[ErrorCode["BUSINESS_REJECTED"] = -300] = "BUSINESS_REJECTED";
    ErrorCode[ErrorCode["ACCOUNT_TEMPORARILY_BLOCKED"] = -401] = "ACCOUNT_TEMPORARILY_BLOCKED";
    ErrorCode[ErrorCode["ACCOUNT_PERMANENTLY_BLOCKED"] = -402] = "ACCOUNT_PERMANENTLY_BLOCKED";
    ErrorCode[ErrorCode["SERVER_ERROR"] = -500] = "SERVER_ERROR";
    ErrorCode[ErrorCode["UNSUPPORTED_VIDEO"] = -600] = "UNSUPPORTED_VIDEO";
})(ErrorCode || (exports.ErrorCode = ErrorCode = {}));
// ======================== 常量配置 ========================
exports.TIMEOUT_CONFIG = {
    upload: 180000,
    submit: 150000,
    query: 10000,
    videoWatermark: 45000,
    imageWatermark: 180000,
};
exports.MAX_FILE_SIZE = 1073741824;
exports.MAX_URL_LENGTH = 2048;
exports.MAX_DURATION = 600;
exports.MAX_DIMENSION = 10000;
exports.MAX_TASK_ID_LENGTH = 64;
exports.MAX_CREDENTIAL_LENGTH = 128;
exports.MAX_IMAGE_FILE_SIZE = 52428800;
exports.POLL_INTERVAL = 30000;
exports.MAX_POLL_COUNT = 20;
exports.MAX_CONSECUTIVE_FAILURES = 3;
exports.RESOLUTION_720P_THRESHOLD = 921600;
exports.RATE_720P_OR_BELOW = 1.3;
exports.RATE_ABOVE_720P = 1.6;
exports.BASE_URL = "https://www.550wai.cn";
exports.CREDENTIAL_APPLY_URL_ZH = "https://qzm.550wai.cn/api-keys";
exports.CREDENTIAL_APPLY_URL_EN = "https://eraser.550wai.com/api/";
// Backward-compatible alias for callers that expect the original constant.
exports.CREDENTIAL_APPLY_URL = exports.CREDENTIAL_APPLY_URL_ZH;
exports.SUPPORTED_VIDEO_EXTENSIONS = [".mp4", ".mov"];
exports.SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".avif", ".tif", ".tiff", ".svg"];
//# sourceMappingURL=types.js.map