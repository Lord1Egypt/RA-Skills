"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
exports.manifest = {
    name: 'create_space',
    description: '创建一个新的电商素材工作空间。Create a new ecommerce asset workspace.',
    parameters: {
        type: 'object',
        properties: {
            name: {
                type: 'string',
                description: '工作空间名称，例如产品名。Workspace name, e.g. product name.',
            },
        },
    },
};
async function handler(client, params) {
    const space = await client.createSpace(params.name);
    return `✅ 工作空间已创建\n- ID: ${space.id}\n- 名称: ${space.name}\n- 状态: ${space.status}\n\n下一步：上传产品白底图 (upload_product_image)`;
}
