#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const dispatcher_1 = require("./dispatcher");
const i18n_1 = require("./i18n");
const local_media_1 = require("./local-media");
function withLocalFile(action, params) {
    const filePath = typeof params.filePath === "string" ? params.filePath : null;
    if (!filePath)
        return params;
    const kind = action === "removeImageWatermark" ? "image" : "video";
    const next = { ...params, file: (0, local_media_1.openSelectedLocalMedia)(filePath, kind) };
    delete next.filePath;
    return next;
}
function toolResult(result) {
    return {
        content: [{ type: "text", text: JSON.stringify(result) }],
        structuredContent: result,
        isError: result.code !== 200,
    };
}
async function call(action, params) {
    try {
        if (action === "workflow") {
            const hasFile = typeof params.filePath === "string" && params.filePath.trim() !== "";
            const hasUrl = typeof params.videoUrl === "string" && params.videoUrl.trim() !== "";
            if (hasFile === hasUrl) {
                return toolResult({ code: -200, message: (0, i18n_1.localize)(params.locale, "filePath 和 videoUrl 必须且只能提供一个", "Provide exactly one of filePath or videoUrl") });
            }
        }
        return toolResult(await (0, dispatcher_1.invoke)({ action, params: withLocalFile(action, params) }));
    }
    catch {
        return toolResult({ code: -200, message: (0, i18n_1.localize)(params.locale, "无法读取本地文件。请确认路径存在且文件可访问。", "Could not read the local file. Make sure the path exists and is accessible.") });
    }
}
const locale = zod_1.z.string().min(2).optional().describe("Optional BCP 47 language tag for localized messages. The domestic package always responds in Chinese; the global package defaults to English.");
const domestic = (0, i18n_1.resolveServiceRegion)() === "domestic";
const description = (zh, en) => domestic ? zh : en;
const localeField = domestic ? {} : { locale };
const server = new mcp_js_1.McpServer({ name: "ai-subtitle-remover", version: require("../package.json").version });
server.registerTool("remove_video_subtitles", {
    description: description("去除用户指定 MP4/MOV 视频或公开视频文件直链中的硬字幕。所选文件或链接会发送至 550W Open API；这是计费操作，结果未确认时不要重复提交。", "Remove subtitles from a user-selected local MP4/MOV file or a public direct video URL. The selected file or URL is sent to the 550W Open API. This is a billed operation; do not retry an uncertain submission."),
    inputSchema: {
        filePath: zod_1.z.string().optional().describe(description("本地 MP4 或 MOV 文件的绝对路径。", "Absolute path to a local MP4 or MOV file.")),
        videoUrl: zod_1.z.string().url().optional().describe(description("MP4 或 MOV 文件的 HTTP(S) 直链。", "Direct HTTP(S) URL to an MP4 or MOV file.")),
        width: zod_1.z.number().int().positive().optional().describe(description("视频真实像素宽度；与高度、时长一起提供可跳过本地检测。", "Actual pixel width; supply with height and duration to skip local ffprobe.")),
        height: zod_1.z.number().int().positive().optional().describe(description("视频真实像素高度；与宽度、时长一起提供。", "Actual pixel height; supply with width and duration.")),
        duration: zod_1.z.number().min(1).max(600).optional().describe(description("视频真实时长（秒）；与宽度、高度一起提供。", "Actual duration in seconds; supply with width and height.")),
        removeAudio: zod_1.z.boolean().optional().describe(description("仅在用户明确要求去除音轨时设为 true。", "Set true only when the user explicitly asks to remove the audio track.")),
        idempotencyKey: zod_1.z.string().min(8).max(128).regex(/^[A-Za-z0-9._:-]+$/).optional().describe(description("稳定的幂等键；仅对完全相同的提交参数复用。", "Stable idempotency key; reuse only with identical submission parameters.")),
        subUserId: zod_1.z.string().max(128).optional().describe(description("可选子用户标识；提交与后续查询保持一致。", "Optional child or tenant user scope; reuse it for status and list queries.")),
        ...localeField,
    },
    annotations: { destructiveHint: false, idempotentHint: false, openWorldHint: true },
}, (params) => call("workflow", params));
server.registerTool("remove_video_watermark", {
    description: description("将从抖音、快手、Bilibili、微博、小红书等 App 内复制的公开视频分享链接解析为无水印视频；实际以服务端支持的平台为准。成功扣 1 积分。", "Resolve a TikTok or other supported short-video share link copied from its app to a watermark-free video. Costs one credit only on success."),
    inputSchema: {
        videoUrl: zod_1.z.string().describe(description("从短视频 App 内复制的公开视频分享链接，或包含单个链接的分享文本。", "Public short-video share URL copied from the platform app, or share text containing one URL.")),
        operationId: zod_1.z.string().min(8).max(64).regex(/^[A-Za-z0-9._:-]+$/).optional().describe(description("建议传入稳定操作标识，以支持安全重试。", "Recommended stable operation ID for safe retries.")),
        ...localeField,
    },
    annotations: { destructiveHint: false, idempotentHint: false, openWorldHint: true },
}, (params) => call("removeVideoWatermark", params));
server.registerTool("remove_image_watermark", {
    description: description("去除用户选中的一张图片中的水印或多余文字。文件会发送至 550W Open API；成功扣 10 积分，多张图片逐张处理。", "Remove a watermark or unwanted text from one user-selected local image. The selected file is sent to the 550W Open API. Costs 10 credits only on success. Call serially for multiple images."),
    inputSchema: {
        filePath: zod_1.z.string().describe(description("本地 JPG、PNG、BMP、WebP、AVIF、TIFF 或 SVG 图片的绝对路径。", "Absolute path to a JPG, PNG, BMP, WebP, AVIF, TIFF, or SVG image.")),
        sync: zod_1.z.boolean().optional().default(true).describe(description("为 true 时等待处理结果。", "Wait for the result when true.")),
        operationId: zod_1.z.string().min(8).max(64).regex(/^[A-Za-z0-9._:-]+$/).optional().describe(description("可选请求追踪标识。", "Optional request tracking key.")),
        ...localeField,
    },
    annotations: { destructiveHint: false, idempotentHint: false, openWorldHint: true },
}, (params) => call("removeImageWatermark", params));
server.registerTool("get_subtitle_task", {
    description: description("查询去字幕任务状态与结果。", "Get the current status and result of a subtitle-removal task."),
    inputSchema: { taskId: zod_1.z.string(), subUserId: zod_1.z.string().max(128).optional(), ...localeField },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
}, (params) => call("taskDetail", params));
server.registerTool("get_image_task", {
    description: description("查询异步图片去水印任务状态与结果。", "Get the current status and result of an asynchronous image-watermark task."),
    inputSchema: { taskId: zod_1.z.string(), ...localeField },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
}, (params) => call("imageWatermarkTaskDetail", params));
server.registerTool("list_subtitle_tasks", {
    description: description("分页列出历史去字幕任务。", "List previous subtitle-removal tasks."),
    inputSchema: { page: zod_1.z.number().int().nonnegative().optional().describe(description("从零开始的页码。", "Zero-based page index.")), size: zod_1.z.number().int().min(1).max(100).optional(), subUserId: zod_1.z.string().max(128).optional(), ...localeField },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
}, (params) => call("taskList", params));
server.registerTool("delete_subtitle_task", {
    description: description("删除本人一项去字幕任务，并安排清理上传及结果媒体；已扣积分不退还。", "Permanently hide one owned subtitle-removal task and schedule its uploaded and result media for cleanup. Charged credits are not refunded."),
    inputSchema: {
        taskId: zod_1.z.string().min(1).max(64).describe(description("去字幕任务 ID。", "Task ID returned by subtitle removal.")),
        subUserId: zod_1.z.string().max(128).optional().describe(description("提交时使用的可选子用户标识。", "Optional sub-user scope when the task was submitted for one.")),
        ...localeField,
    },
    annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true, openWorldHint: true },
}, (params) => call("deleteTask", params));
server.registerTool("query_credits", {
    description: description("查询 550W 账号当前积分余额。", "Return the current 550W account credit balance."),
    inputSchema: { ...localeField },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
}, (params) => call("queryCredits", params));
async function main() {
    await server.connect(new stdio_js_1.StdioServerTransport());
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
});
//# sourceMappingURL=mcp-server.js.map