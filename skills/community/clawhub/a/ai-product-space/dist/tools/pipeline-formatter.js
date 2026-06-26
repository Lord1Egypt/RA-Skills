"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.formatPipelineOutputs = formatPipelineOutputs;
// Display order and labels for each pipeline stage
const STAGE_META = [
    { id: 'layer3-product', label: '产品展示图', icon: '📦', type: 'image' },
    { id: 'layer3-scene', label: '场景图', icon: '🏠', type: 'image' },
    { id: 'layer3-feature', label: '卖点图', icon: '⭐', type: 'image' },
    { id: 'layer3-model', label: '模特图', icon: '👤', type: 'image' },
    { id: 'layer5-poster', label: '营销海报', icon: '🎨', type: 'image' },
    { id: 'layer5-model', label: '模特合成', icon: '👗', type: 'image' },
    { id: 'layer2', label: '文案策划', icon: '✍️', type: 'text' },
    { id: 'layer-translate', label: '多语言文案', icon: '🌐', type: 'text' },
];
/**
 * Formats pipelineOutputs into grouped markdown sections — one per stage.
 * Image stages use markdown image syntax so chat clients render them inline.
 * Returns empty string if there are no outputs to display.
 */
function formatPipelineOutputs(outputs) {
    const sections = [];
    let totalImages = 0;
    let totalTexts = 0;
    for (const meta of STAGE_META) {
        const stageData = outputs[meta.id];
        if (!stageData || Object.keys(stageData).length === 0)
            continue;
        const lines = [`${meta.icon} **${meta.label}**`];
        if (meta.type === 'image') {
            const imageLines = [];
            for (const [taskId, value] of Object.entries(stageData)) {
                const urls = Array.isArray(value) ? value : (value ? [value] : []);
                const altText = taskId.replace(/^img-/, '').replace(/-/g, ' ');
                for (const url of urls) {
                    if (url) {
                        imageLines.push(`![${altText}](${url})`);
                        totalImages++;
                    }
                }
            }
            if (imageLines.length > 0)
                lines.push(imageLines.join('\n'));
        }
        else {
            for (const [, value] of Object.entries(stageData)) {
                const text = Array.isArray(value) ? value.join('\n') : value;
                if (text) {
                    lines.push(text);
                    totalTexts++;
                }
            }
        }
        sections.push(lines.join('\n'));
    }
    if (sections.length === 0)
        return '';
    const header = `✅ 电商素材生成完成！共 ${totalImages} 张图片、${totalTexts} 段文案\n`;
    const footer = '\n---\n💡 使用 `generate_video` 可基于以上图片生成 8 秒展示视频。';
    return header + '\n---\n' + sections.join('\n\n---\n\n') + footer;
}
