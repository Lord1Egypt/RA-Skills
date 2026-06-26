/**
 * 通用 API 代理 — 一次 exec 完成任意 API 调用
 * 
 * 用法:
 *   node scripts/proxy/api-call.js <METHOD> <PATH> [BODY_JSON]
 * 
 * 示例:
 *   node scripts/proxy/api-call.js GET /api/products/list '{"page":1}'
 *   node scripts/proxy/api-call.js POST /api/products/create '{"title":"test"}'
 *   node scripts/proxy/api-call.js PUT /api/products/123 '{"title":"updated"}'
 *   node scripts/proxy/api-call.js DELETE /api/products/123
 */

const api = require('../base/api-client');

const method = (process.argv[2] || '').toUpperCase();
const path   = process.argv[3] || '';
let   body   = null;

if (process.argv[4]) {
    try {
        body = JSON.parse(process.argv[4]);
    } catch (e) {
        console.error(JSON.stringify({ code: -1, message: `body 参数 JSON 解析失败: ${e.message}` }));
        process.exit(1);
    }
}

if (!method || !path) {
    console.error(JSON.stringify({ code: -1, message: '用法: node api-call.js <METHOD> <PATH> [BODY_JSON]' }));
    process.exit(1);
}

(async () => {
    try {
        let result;
        switch (method) {
            case 'GET':    result = await api.get(path); break;
            case 'POST':   result = await api.post(path, body); break;
            case 'PUT':    result = await api.put(path, body); break;
            case 'DELETE': result = await api.del(path); break;
            default:
                console.error(JSON.stringify({ code: -1, message: `不支持的 HTTP 方法: ${method}` }));
                process.exit(1);
        }
        console.log(JSON.stringify(result));
    } catch (err) {
        console.error(JSON.stringify({ code: -1, message: err.message }));
        process.exit(1);
    }
})();
