"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
exports.manifest = {
    name: 'upload_product_image',
    description: '上传产品白底图到工作空间。Upload a product image (white background) to a workspace.',
    parameters: {
        type: 'object',
        properties: {
            space_id: {
                type: 'string',
                description: '工作空间 ID。The workspace ID.',
            },
            image_path: {
                type: 'string',
                description: '本地图片文件路径。Local image file path.',
            },
            image_url: {
                type: 'string',
                description: '图片 URL（与 image_path 二选一）。Image URL (alternative to image_path).',
            },
        },
        required: ['space_id'],
    },
};
async function handler(client, params) {
    if (!params.image_path && !params.image_url) {
        return '❌ 请提供 image_path 或 image_url 之一。';
    }
    const result = params.image_url
        ? await client.uploadImageFromUrl(params.space_id, params.image_url)
        : await client.uploadImage(params.space_id, params.image_path);
    if (!result.success) {
        return '❌ 图片上传失败，请检查文件路径或 URL 是否正确。';
    }
    return `✅ 图片已上传\n- URL: ${result.url}\n\n下一步：运行电商素材生成流水线 (run_ecommerce_pipeline)`;
}
