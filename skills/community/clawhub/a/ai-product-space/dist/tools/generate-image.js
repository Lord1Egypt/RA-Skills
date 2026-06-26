"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
exports.manifest = {
    name: 'generate_single_image',
    description: '根据自定义 Prompt 生成单张商品图。Generate a single product image from a custom prompt.',
    parameters: {
        type: 'object',
        properties: {
            space_id: {
                type: 'string',
                description: '工作空间 ID。The workspace ID.',
            },
            prompt: {
                type: 'string',
                description: '图片生成 Prompt，描述你想要的商品图效果。Image generation prompt.',
            },
            count: {
                type: 'number',
                description: '生成图片数量（1-4，默认 1）。Number of images to generate.',
            },
        },
        required: ['space_id', 'prompt'],
    },
};
async function handler(client, params) {
    const result = await client.generateImage(params.space_id, params.prompt, { n: params.count });
    if (!result.success || !result.images?.length) {
        return '❌ 图片生成失败，请检查 Prompt 或稍后重试。';
    }
    const lines = [`✅ 已生成 ${result.images.length} 张图片：`];
    result.images.forEach((url, i) => {
        lines.push(`${i + 1}. ${url}`);
    });
    if (result.revisedPrompt) {
        lines.push(`\n优化后的 Prompt: ${result.revisedPrompt}`);
    }
    return lines.join('\n');
}
