# eframe 前端开发范式

> 本文档为 SKILL.md 的前端代码参考，提取自框架现有前端工程（eframe-vue-frontend）真实代码。

## 一、技术栈与目录结构

**技术栈**：Vue3 + Vite2 + Element Plus + Ant Design Vue + Pinia + Vuex + Vue Router4 + Axios + ECharts + dayjs + file-saver。

```
src/
├── api/                  # 接口层，按域分目录
│   ├── login.js / menu.js / req.js / user.js
│   ├── admin/  dept.js info.js menu.js notice.js post.js role.js user.js
│   ├── monitor/ cache.js commlog.js job.js jobLog.js loginlog.js online.js server.js
│   ├── system/  configwhole.js dictionary.js dictype.js
│   └── tool/    gen.js
├── views/                # 页面层，按域分目录
│   ├── admin/  dept/ info/ menu/ notice/ post/ role/ user/
│   ├── monitor/ cache/ commlog/ druid/ job/ loginlog/ online/ server/
│   ├── system/  tool/
│   ├── login/ my/ profile/ workbench/ error/
├── utils/                # request.js axios封装、auth、errorCode、common、LocalIcon、LocalUtil
├── router/  store/  components/  directive/  plugins/  assets/
└── main.js  App.vue
```

## 二、请求封装（src/utils/request.js，勿重写）

axios 实例统一配置，新接口一律走 `@/utils/request`：

```javascript
const service = axios.create({
    baseURL: import.meta.env.VITE_API_DOMAIN,  // 环境变量配置后端地址
    timeout: 10000,
});

// 请求拦截：注入 token，格式 'Linlan ' + token
service.interceptors.request.use((config) => {
    if (getToken() && !isToken) {
        config.headers['Authorization'] = 'Linlan ' + getToken();
    }
    return config;
});

// 响应拦截：code === 200 或 '0' 视为成功；401 弹登录过期；500 弹失败通知
service.interceptors.response.use((res) => {
    const code = res.data.code || 200;
    if (code === 200 || code === '0') return res.data;
    if (code === 401) { /* 登录过期，登出跳转 */ }
    if (code === 500) { /* 请求后端服务失败 */ }
    // 其余弹错误通知，reject
});
```

**通用下载**：`download(url, params, filename)` 已封装（blob + file-saver），导出场景直接调用。

## 三、api 层范式（src/api/{域}/{实体}.js）

以 `system/dictionary.js` 为模板，命名约定 listData/getData/addData/updateData/delData：

```javascript
import request from '@/utils/request'

// 查询列表
export function listData(query) {
    return request({ url: '/api/system/dictionary/list', method: 'get', params: query })
}
// 查询详情
export function getData(dictId) {
    return request({ url: '/api/system/dictionary/' + dictId, method: 'get' })
}
// 新增
export function addData(data) {
    return request({ url: '/api/system/dictionary', method: 'post', data: data })
}
// 修改
export function updateData(data) {
    return request({ url: '/api/system/dictionary', method: 'put', data: data })
}
// 删除
export function delData(dictId) {
    return request({ url: '/api/system/dictionary/' + dictId, method: 'delete' })
}
```

## 四、views 层范式（src/views/{域}/{实体}/index.vue）

页面结构要点：

1. **列表页**：表格 + 查询条件 + 分页 + 新增/编辑弹窗 + 删除确认。
2. **UI 库**：Element Plus（el-table/el-form/el-dialog）+ Ant Design Vue（a-modal/a-notification）混用，框架两套都已装，按需选择。
3. **状态管理**：Pinia（新页面优先）与 Vuex 并存；登录态、用户信息走 store。
4. **路由**：`src/router/` 配置，菜单由后端 `sys_menu` 表驱动（前端只做路由映射）。
5. **字典渲染**：下拉/标签取值走 `/api/system/dictionary/type/{dictType}` 接口（`getDicts`）。

典型列表页数据流：`listData(query)` -> el-table 渲染 -> 编辑弹窗 `addData/updateData` -> 成功后刷新列表。

## 五、环境与启动

```
.env.dev / .env.test / .env.prod   环境变量（VITE_API_DOMAIN 等）
npm run dev       开发（vite --mode dev）
npm run build     构建（vite build --mode prod）
```

## 六、前后端联调检查清单

- [ ] 前端 api URL 与后端 `@RequestMapping` + `@GetMapping` 拼接一致（`/api/{域}/{实体}/{动作}`）
- [ ] 后端返回 `code=200` 或 `'0'`，前端 response 拦截器能正确取值
- [ ] token 注入格式 `'Linlan ' + token` 与后端 Security 解析一致
- [ ] 分页字段对应：后端 `Pagination` -> 前端 el-pagination
- [ ] 导出用 `download()` 或后端 `ExcelUtil.exportExcel` 流式返回
