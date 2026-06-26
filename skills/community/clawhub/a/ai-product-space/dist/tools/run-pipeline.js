"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
const pipeline_formatter_1 = require("./pipeline-formatter");
exports.manifest = {
    name: 'run_ecommerce_pipeline',
    description: '运行电商素材全套生成流水线（商品图、场景图、卖点图、海报、文案）。Run the full ecommerce asset pipeline.',
    parameters: {
        type: 'object',
        properties: {
            space_id: {
                type: 'string',
                description: '工作空间 ID。The workspace ID.',
            },
            language: {
                type: 'string',
                description: '输出语言代码：zh（中文）、en（英语）等。Output language code.',
                enum: ['zh', 'en', 'ja', 'ko', 'fr', 'de', 'es', 'pt', 'ar', 'ru'],
            },
            wait: {
                type: 'boolean',
                description: '是否等待流水线完成（默认 true）。Whether to wait for completion.',
            },
        },
        required: ['space_id'],
    },
};
async function handler(client, params) {
    const result = await client.runPipeline(params.space_id, params.language);
    if (!result.success) {
        return `❌ 流水线启动失败: ${result.message || '未知错误'}`;
    }
    if (params.wait === false) {
        return `✅ 流水线已启动，正在后台生成中...\n使用 get_space_status 查看进度。`;
    }
    const status = await client.waitForPipeline(params.space_id);
    if (status.status === 'failed') {
        return '❌ 流水线生成失败，部分任务可能出错。请使用 get_space_status 查看详情。';
    }
    const outputs = (status.pipelineOutputs || {});
    const formatted = (0, pipeline_formatter_1.formatPipelineOutputs)(outputs);
    if (!formatted) {
        const label = status.status === 'partial' ? '⚠️ 部分完成' : '✅ 完成';
        return `${label}\n使用 get_space_status 查看详细结果。`;
    }
    return formatted;
}
