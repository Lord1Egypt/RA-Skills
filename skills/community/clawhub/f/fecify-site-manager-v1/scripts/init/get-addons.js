/**
 * 获取站点已安装的插件列表
 * GET /api/skill/base/init
 * 
 * 用法: node scripts/init/get-addons.js
 * 输出: JSON { code, data: { addons: [...] }, message }
 */

const api = require('../base/api-client');

api.get('/api/skill/base/init').then(res => {
    console.log(JSON.stringify(res));
}).catch(err => {
    console.error(JSON.stringify({ code: -1, message: err.message }));
    process.exit(1);
});
