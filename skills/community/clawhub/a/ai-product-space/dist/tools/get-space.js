"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
const pipeline_formatter_1 = require("./pipeline-formatter");
exports.manifest = {
    name: 'get_space_status',
    description: '查看工作空间的状态和流水线进度。Get workspace status and pipeline progress.',
    parameters: {
        type: 'object',
        properties: {
            space_id: {
                type: 'string',
                description: '工作空间 ID。The workspace ID.',
            },
        },
        required: ['space_id'],
    },
};
async function handler(client, params) {
    const [space, pipeline] = await Promise.all([
        client.getSpace(params.space_id),
        client.pollPipeline(params.space_id).catch(() => null),
    ]);
    // If pipeline is done and has outputs, show grouped results
    if (pipeline &&
        (pipeline.status === 'completed' || pipeline.status === 'partial') &&
        pipeline.pipelineOutputs &&
        Object.keys(pipeline.pipelineOutputs).length > 0) {
        const outputs = pipeline.pipelineOutputs;
        const formatted = (0, pipeline_formatter_1.formatPipelineOutputs)(outputs);
        if (formatted) {
            const header = `📋 **${space.name}** · ${pipeline.status === 'partial' ? '⚠️ 部分完成' : '✅ 已完成'}\n\n`;
            return header + formatted;
        }
    }
    // Otherwise show progress summary
    const lines = [`📋 工作空间: ${space.name}`, `- ID: ${space.id}`, `- 状态: ${space.status}`];
    if (space.inputImageUrls && Array.isArray(space.inputImageUrls)) {
        lines.push(`- 已上传 ${space.inputImageUrls.length} 张产品图`);
    }
    if (pipeline) {
        lines.push(`\n🔄 流水线状态: ${pipeline.status}`);
        if (pipeline.runningStageId) {
            lines.push(`- 正在执行: ${pipeline.runningStageId}`);
        }
        if (pipeline.failedTasks && Array.isArray(pipeline.failedTasks) && pipeline.failedTasks.length > 0) {
            lines.push(`- 失败任务数: ${pipeline.failedTasks.length}`);
        }
    }
    return lines.join('\n');
}
