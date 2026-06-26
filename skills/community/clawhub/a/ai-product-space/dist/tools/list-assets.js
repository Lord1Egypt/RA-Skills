"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.handler = handler;
exports.manifest = {
    name: 'list_assets',
    description: '浏览已生成的素材资源。Browse generated assets.',
    parameters: {
        type: 'object',
        properties: {
            folder_id: {
                type: 'string',
                description: '素材文件夹 ID（可选，不填返回全部）。Asset folder ID.',
            },
        },
    },
};
async function handler(client, params) {
    const result = await client.listAssets(params.folder_id);
    if (!result.assets.length) {
        return '📂 暂无素材。请先运行 run_ecommerce_pipeline 生成素材。';
    }
    const lines = [`📂 共 ${result.assets.length} 个素材：`];
    const byType = {};
    for (const asset of result.assets) {
        byType[asset.type] = (byType[asset.type] || 0) + 1;
    }
    for (const [type, count] of Object.entries(byType)) {
        lines.push(`- ${type}: ${count} 个`);
    }
    lines.push('');
    const preview = result.assets.slice(0, 5);
    for (const asset of preview) {
        lines.push(`• [${asset.type}] ${asset.name || '未命名'} — ${asset.url}`);
    }
    if (result.assets.length > 5) {
        lines.push(`\n... 还有 ${result.assets.length - 5} 个素材`);
    }
    return lines.join('\n');
}
