"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.imageTaskResult = imageTaskResult;
const types_1 = require("./types");
const i18n_1 = require("./i18n");
function imageTaskResult(response, locale) {
    const task = response.task && typeof response.task === "object" ? { ...response.task } : null;
    const status = task?.status;
    if (task && status !== "success")
        delete task.resultUrl;
    if (task && (0, i18n_1.resolveLocale)(locale) === "en")
        delete task.failReason;
    const taskId = task?.taskNo || task?.taskId;
    const base = { ...response, task, ...(taskId ? { taskId } : {}) };
    if (status === "success" && task?.resultUrl) {
        return { ...base, code: types_1.ErrorCode.SUCCESS, message: (0, i18n_1.localize)(locale, "图片去水印完成", "Image watermark removal completed") };
    }
    if (status === "success") {
        return { ...base, code: types_1.ErrorCode.SERVER_ERROR,
            message: (0, i18n_1.localize)(locale, "图片任务显示成功，但结果尚不可用；请稍后按任务编号重新查询。", "The image task reports success, but its result is unavailable. Check this task ID again later.") };
    }
    if (status === "failed") {
        return { ...base, code: types_1.ErrorCode.BUSINESS_REJECTED,
            message: (0, i18n_1.localize)(locale, `图片处理失败${task?.failReason ? `：${task.failReason}` : ""}；请检查图片后再决定是否重新提交。`, "Image processing failed. Check the image and failure code before deciding whether to submit again.") };
    }
    if (status === "expired") {
        return { ...base, code: types_1.ErrorCode.BUSINESS_REJECTED,
            message: (0, i18n_1.localize)(locale, "图片任务已过期，结果不可再获取；如需处理请重新提交。", "The image task has expired and its result is no longer available. Submit a new task if needed.") };
    }
    if (taskId) {
        return { ...base, code: types_1.ErrorCode.SUCCESS,
            message: (0, i18n_1.localize)(locale, "图片任务仍在处理中，请保存任务编号并稍后查询。", "Image processing is still in progress. Keep the task ID and check again later.") };
    }
    return { ...base, code: types_1.ErrorCode.SERVER_ERROR,
        message: (0, i18n_1.localize)(locale, "图片接口未返回可确认的任务状态；请先核查已有任务，不要直接重复提交。", "The image API returned no verifiable task status. Check for an existing task before submitting again.") };
}
//# sourceMappingURL=image-task-result.js.map