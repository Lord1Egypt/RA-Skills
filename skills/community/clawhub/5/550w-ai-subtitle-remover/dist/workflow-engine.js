"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.executeWorkflow = executeWorkflow;
const upload_video_1 = require("./actions/upload-video");
const submit_task_1 = require("./actions/submit-task");
const task_detail_1 = require("./actions/task-detail");
const video_probe_1 = require("./video-probe");
const types_1 = require("./types");
function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
async function executeWorkflow(params, client) {
    let submitParams;
    if (params.file) {
        const uploadResult = await (0, upload_video_1.uploadVideo)({ file: params.file }, client);
        if (uploadResult.code !== types_1.ErrorCode.SUCCESS)
            return uploadResult;
        submitParams = {
            videoUrl: uploadResult.videoUrl,
            coverUrl: uploadResult.coverUrl,
            width: uploadResult.width,
            height: uploadResult.height,
            duration: uploadResult.duration,
            x1: params.x1 ?? 0,
            y1: params.y1 ?? 0,
            x2: params.x2 ?? 0,
            y2: params.y2 ?? 0,
            ...(params.mode != null && { mode: params.mode }),
            ...(params.fileName != null && { fileName: params.fileName }),
        };
    }
    else {
        submitParams = { ...params };
        delete submitParams.file;
        if (submitParams.x1 == null)
            submitParams.x1 = 0;
        if (submitParams.y1 == null)
            submitParams.y1 = 0;
        if (submitParams.x2 == null)
            submitParams.x2 = 0;
        if (submitParams.y2 == null)
            submitParams.y2 = 0;
        const needsProbe = submitParams.width == null || submitParams.height == null || submitParams.duration == null;
        if (needsProbe) {
            const metadata = await (0, video_probe_1.probeVideoUrl)(submitParams.videoUrl, client);
            if (metadata) {
                if (submitParams.width == null)
                    submitParams.width = metadata.width;
                if (submitParams.height == null)
                    submitParams.height = metadata.height;
                if (submitParams.duration == null)
                    submitParams.duration = metadata.duration;
            }
        }
    }
    const submitResult = await (0, submit_task_1.submitTask)(submitParams, client);
    if (submitResult.code !== types_1.ErrorCode.SUCCESS)
        return submitResult;
    const taskId = submitResult.taskId;
    let consecutiveFailures = 0;
    for (let pollCount = 0; pollCount < types_1.MAX_POLL_COUNT; pollCount++) {
        await delay(types_1.POLL_INTERVAL);
        const detailResult = await (0, task_detail_1.taskDetail)({ taskId }, client);
        if (detailResult.code !== types_1.ErrorCode.SUCCESS) {
            consecutiveFailures++;
            if (consecutiveFailures >= types_1.MAX_CONSECUTIVE_FAILURES) {
                return { code: types_1.ErrorCode.SERVER_ERROR, message: `轮询任务状态连续 ${types_1.MAX_CONSECUTIVE_FAILURES} 次失败，工作流终止。您可以稍后使用 taskDetail 查询任务 ${taskId} 的最终状态`, taskId };
            }
            continue;
        }
        consecutiveFailures = 0;
        const status = detailResult.status;
        if (status === "success") {
            return { code: types_1.ErrorCode.SUCCESS, message: "去字幕任务处理完成", taskId, resultUrl: detailResult.resultUrl };
        }
        if (status === "failed") {
            return { code: types_1.ErrorCode.BUSINESS_REJECTED, message: `任务处理失败：${detailResult.failReason || "未知原因"}。积分已自动退还到您的账户`, taskId, failReason: detailResult.failReason };
        }
    }
    return { code: types_1.ErrorCode.SERVER_ERROR, message: `轮询超时：任务在 ${types_1.MAX_POLL_COUNT * types_1.POLL_INTERVAL / 1000 / 60} 分钟内未完成处理。您可以稍后使用 taskDetail 查询任务 ${taskId} 的最终状态`, taskId, timedOut: true };
}
//# sourceMappingURL=workflow-engine.js.map