const fs = require('fs');
const path = require('path');
// 已移除 child_process 引用以修复安全审计告警

// 获取目标路径
const rawTargetDir = process.argv[2];
if (!rawTargetDir) {
    console.error('Error: Please provide a directory path.');
    process.exit(1);
}

// 路径规范化，防止路径遍历攻击
const targetDir = path.resolve(rawTargetDir);

/**
 * 安全增强：HTML 实体转义函数
 * 防止恶意文件名触发 XSS 攻击
 */
function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, function(m) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[m];
    });
}

function getFileStructure(dir, depth = 0) {
    
    let items;
    try {
        items = fs.readdirSync(dir);
    } catch (e) {
        return []; // 无法访问的目录返回空
    }

    const structure = [];
    for (const item of items) {
        const itemPath = path.join(dir, item);
        try {
            const stats = fs.statSync(itemPath);
            const modified = stats.mtime.toISOString().split('T')[0];

            if (stats.isDirectory()) {
                const children = getFileStructure(itemPath, depth + 1);
                const dirNode = {
                    name: item, // 存储原始名称，渲染时再转义
                    type: 'folder',
                    modified: modified,
                    childCount: children ? children.length : 0,
                    children: children
                };
                structure.push(dirNode);
            } else {
                structure.push({
                    name: item,
                    type: 'file',
                    size: stats.size,
                    modified: modified
                });
            }
        } catch (e) {
            // 忽略无权限访问的文件
        }
    }
    return structure;
}

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function createHtmlList(structure) {
    if (!structure) return '';
    let html = '';
    for (const item of structure) {
        // 渲染时进行 HTML 转义
        const safeName = escapeHTML(item.name);
        
        if (item.type === 'folder') {
            html += `<details>`;
            html += `<summary>📁 <strong>${safeName}</strong> [${item.childCount} items, ${item.modified}]</summary>`;
            html += `<blockquote>`;
            if (item.children) {
                html += createHtmlList(item.children);
            }
            html += `</blockquote>`;
            html += `</details>`;
        } else {
            html += `<p>📄 ${safeName} [${formatBytes(item.size)}, ${item.modified}]</p>`;
        }
    }
    return html;
}

try {
    const rootStats = fs.statSync(targetDir);
    const rootModified = rootStats.mtime.toISOString().split('T')[0];

    const structure = getFileStructure(targetDir);
    const listHtml = createHtmlList(structure);

    let totalItems = 0;
    if (structure) {
        totalItems = structure.length;
    }

    // 构建最终 HTML 模板，保持原有的 style 风格
    const finalHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Folder Visualizer - ${escapeHTML(path.basename(targetDir))}</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.4; color: #333; }
        blockquote { border-left: 2px solid #ddd; margin-left: 15px; padding-left: 10px; }
        summary { cursor: pointer; padding: 4px; border-radius: 4px; }
        summary:hover { background: #f0f0f0; }
        p { margin: 4px 0; }
        hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
    </style>
</head>
<body>
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
      <tr>
        <td><h2>📁 Folder Visualizer</h2></td>
        <td align="right"><p style="color: #888;">made by sdsds222</p></td>
      </tr>
    </table>
    <p><b>Path:</b> <code>${escapeHTML(targetDir)}</code></p>
    <p><b>Last Modified:</b> ${rootModified} &nbsp;&nbsp;&nbsp; <b>Root Items:</b> ${totalItems}</p>
    <hr>
    ${listHtml}
</body>
</html>`;

    const folderName = path.basename(targetDir) || 'Root';
    const outputFileName = `FileList_${folderName}_${Date.now()}.html`; // 增加时间戳防止重名冲突
    const outputFilePath = path.resolve(outputFileName);

    fs.writeFileSync(outputFilePath, finalHtml);

    // 关键：只输出最终文件路径，方便 OpenClaw 捕获并传递给下一环节
    process.stdout.write(outputFilePath);

} catch (error) {
    console.error(`An error occurred: ${error.message}`);
    process.exit(1);
}