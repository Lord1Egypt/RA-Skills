"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.executeWorkflow = executeWorkflow;
const upload_video_1 = require("./actions/upload-video");
const submit_task_1 = require("./actions/submit-task");
const task_detail_1 = require("./actions/task-detail");
const video_probe_1 = require("./video-probe");
const types_1 = require("./types");
const validator_1 = require("./validator");
const i18n_1 = require("./i18n");
function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
async function executeWorkflow(params, client) {
    const inputError = (0, validator_1.validate)("workflow", params);
    if (inputError)
        return inputError;
    let submitParams;
    if (params.file) {
        const uploadResult = await (0, upload_video_1.uploadVideo)({ file: params.file, locale: params.locale }, client);
        if (uploadResult.code !== types_1.ErrorCode.SUCCESS)
            return uploadResult;
        submitParams = {
            videoUrl: uploadResult.videoUrl,
            coverUrl: uploadResult.coverUrl,
            width: uploadResult.width,
            height: uploadResult.height,
            duration: uploadResult.duration,
            ...(params.fileName != null && { fileName: params.fileName }),
            ...(params.callbackUrl != null && { callbackUrl: params.callbackUrl }),
            ...(params.removeAudio != null && { removeAudio: params.removeAudio }),
            ...(params.idempotencyKey != null && { idempotencyKey: params.idempotencyKey }),
            ...(params.subUserId != null && { subUserId: params.subUserId }),
            locale: params.locale,
        };
    }
    else {
        submitParams = { ...params };
        delete submitParams.file;
        delete submitParams.x1;
        delete submitParams.y1;
        delete submitParams.x2;
        delete submitParams.y2;
        delete submitParams.mode;
        try {
            if (params.width != null && params.height != null && params.duration != null) {
                submitParams.width = params.width;
                submitParams.height = params.height;
                submitParams.duration = params.duration;
            }
            else {
                const metadata = await (0, video_probe_1.probeVideoUrl)(submitParams.videoUrl);
                submitParams.width = metadata.width;
                submitParams.height = metadata.height;
                submitParams.duration = metadata.duration;
            }
        }
        catch (error) {
            return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_1.localize)(params.locale, "无法读取远程视频信息。请确认链接可直接访问且视频格式受支持。", "Could not inspect the remote video. Make sure the URL is directly accessible and the video format is supported.") };
        }
    }
    const submitResult = await (0, submit_task_1.submitTask)(submitParams, client);
    if (submitResult.code !== types_1.ErrorCode.SUCCESS)
        return submitResult;
    const taskId = submitResult.taskId;
    let consecutiveFailures = 0;
    for (let pollCount = 0; pollCount < types_1.MAX_POLL_COUNT; pollCount++) {
        await delay(types_1.POLL_INTERVAL);
        const detailResult = await (0, task_detail_1.taskDetail)({ taskId, subUserId: params.subUserId, locale: params.locale, region: params.region }, client);
        if (detailResult.code !== types_1.ErrorCode.SUCCESS) {
            consecutiveFailures++;
            if (consecutiveFailures >= types_1.MAX_CONSECUTIVE_FAILURES) {
                return { code: types_1.ErrorCode.SERVER_ERROR, message: (0, i18n_1.localize)(params.locale, `连续 ${types_1.MAX_CONSECUTIVE_FAILURES} 次查询任务状态失败。请稍后使用任务编号查询最终状态。`, `Task status checks failed ${types_1.MAX_CONSECUTIVE_FAILURES} times. Use the task ID to check the final status later.`), taskId };
            }
            continue;
        }
        consecutiveFailures = 0;
        const status = detailResult.status;
        if (status === "success") {
            return { code: types_1.ErrorCode.SUCCESS, message: (0, i18n_1.localize)(params.locale, "去字幕任务处理完成", "Subtitle removal completed"), taskId, resultUrl: detailResult.resultUrl };
        }
        if (status === "failed") {
            return {
                code: types_1.ErrorCode.BUSINESS_REJECTED,
                message: (0, i18n_1.localize)(params.locale, `任务处理失败：${detailResult.failReason || "未知原因"}${detailResult.refundStatus === 1 ? "。已退款" : ""}。`, `Task processing failed${detailResult.refundStatus === 1 ? "; deducted credits were refunded" : ""}.`),
                taskId,
                ...(detailResult.failCode != null && { failCode: detailResult.failCode }),
                ...(detailResult.refundStatus != null && { refundStatus: detailResult.refundStatus }),
                ...((0, i18n_1.resolveLocale)(params.locale) === "zh" && detailResult.failReason ? { failReason: detailResult.failReason } : {}),
            };
        }
    }
    return { code: types_1.ErrorCode.SERVER_ERROR, message: (0, i18n_1.localize)(params.locale, `任务在 ${types_1.MAX_POLL_COUNT * types_1.POLL_INTERVAL / 1000 / 60} 分钟内未完成。请稍后使用任务编号查询最终状态。`, `The task did not finish within ${types_1.MAX_POLL_COUNT * types_1.POLL_INTERVAL / 1000 / 60} minutes. Use the task ID to check the final status later.`), taskId, timedOut: true };
}
//# sourceMappingURL=workflow-engine.js.map