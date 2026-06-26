/**
 * htmlUtils.js — HTML 解析共享工具
 * 供 validate_page.js 和 verify/index.js 共用
 */

/**
 * 从 const XXX = {...}; 中提取 JSON（字符流 brace 追踪，处理密文含 } 的情况）
 * @param {string} html - HTML 内容
 * @param {string} varName - 变量名（如 'ENCRYPTED_SQL'）
 * @returns {{ data?: object, error?: string }}
 */
function extractJsonFromAssignment(html, varName) {
    const startMarker = `const ${varName} = `;
    const startIdx = html.indexOf(startMarker);
    if (startIdx === -1) return { error: `找不到 ${startMarker}` };
    const jsonStart = startIdx + startMarker.length;
    if (jsonStart >= html.length || html[jsonStart] !== '{') {
        return { error: `${startMarker} 后面不是 {` };
    }

    let depth = 0, inString = false, stringChar = null, i = jsonStart;
    while (i < html.length) {
        const ch = html[i];
        if (inString) {
            if (ch === '\\' && i + 1 < html.length) { i += 2; continue; }
            if (ch === stringChar) { inString = false; i++; continue; }
            i++; continue;
        }
        if (ch === '"' || ch === "'") { inString = true; stringChar = ch; i++; continue; }
        if (ch === '{') { depth++; i++; continue; }
        if (ch === '}') {
            depth--;
            if (depth === 0) {
                const jsonEnd = i + 1;
                const jsonStr = html.slice(jsonStart, jsonEnd);
                try {
                    return { data: JSON.parse(jsonStr) };
                } catch (e) {
                    return { error: `JSON parse error: ${e.message}` };
                }
            }
            i++; continue;
        }
        i++;
    }
    return { error: `找不到 ${varName} 的结束 brace` };
}

/**
 * 从 HTML 中提取所有 key 名（ENCRYPTED_SQL 用，正则提取，不解析 JSON）
 * 用于密文含 } 字符导致 JSON.parse 失败的场景
 * @param {string} html
 * @param {string} varName
 * @returns {Set<string>}
 */
function extractJsonKeys(html, varName) {
    const startMarker = `const ${varName} = `;
    const startIdx = html.indexOf(startMarker);
    if (startIdx === -1) return new Set();
    const jsonStart = startIdx + startMarker.length;

    let depth = 0, inString = false, stringChar = null, i = jsonStart;
    while (i < html.length) {
        const ch = html[i];
        if (inString) {
            if (ch === '\\' && i + 1 < html.length) { i += 2; continue; }
            if (ch === stringChar) { inString = false; i++; continue; }
            i++; continue;
        }
        if (ch === '"' || ch === "'") { inString = true; stringChar = ch; i++; continue; }
        if (ch === '{') { depth++; i++; continue; }
        if (ch === '}') {
            depth--;
            if (depth === 0) {
                const block = html.slice(jsonStart, i + 1);
                const keys = new Set();
                const re = /"([^"]+)":\s*\{/g;
                let m;
                while ((m = re.exec(block)) !== null) keys.add(m[1]);
                return keys;
            }
            i++; continue;
        }
        i++;
    }
    return new Set();
}

module.exports = { extractJsonFromAssignment, extractJsonKeys };
