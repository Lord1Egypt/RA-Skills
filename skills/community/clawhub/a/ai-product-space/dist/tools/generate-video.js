"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
exports.manifest = {
    name: 'generate_video',
    description: '根据商品图生成 8 秒展示视频。Generate an 8-second product showcase video from images.',
    parameters: {
        type: 'object',
        properties: {
            space_id: {
                type: 'string',
                description: '工作空间 ID。The workspace ID.',
            },
            image_urls: {
                type: 'array',
                items: { type: 'string' },
                description: '1-2 张商品图 URL 作为视频关键帧。1-2 image URLs as video keyframes.',
            },
            prompt: {
                type: 'string',
                description: '视频运镜/风格描述（可选）。Video motion/style prompt.',
            },
            wait: {
                type: 'boolean',
                description: '是否等待视频生成完成（默认 true）。Wait for completion.',
            },
        },
        required: ['space_id', 'image_urls'],
    },
};
async function handler(client, params) {
    const submitResult = await client.submitVideo(params.space_id, params.image_urls, params.prompt);
    if (!submitResult.success || !submitResult.videoId) {
        return `❌ 视频生成提交失败: ${submitResult.message || '未知错误'}`;
    }
    const shouldWait = params.wait !== false;
    if (!shouldWait) {
        return `✅ 视频生成已提交\n- Video ID: ${submitResult.videoId}\n\n使用 get_space_status 轮询进度。`;
    }
    const status = await client.waitForVideo(params.space_id, submitResult.videoId);
    if (status.status === 'failed') {
        return '❌ 视频生成失败，请稍后重试。';
    }
    return `✅ 视频已生成完成！\n- 视频地址: ${status.videoUrl}\n- 时长: 8 秒`;
}
