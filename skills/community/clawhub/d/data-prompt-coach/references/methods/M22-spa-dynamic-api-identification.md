# M22 — SPA 动态 API 识别

> 来源：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》教程蒸馏
> 挂载版本：v3.4.0（2026-07-26）
> 触发咒语："动态加载""JavaScript 渲染""XHR""Fetch""SPA""单页应用"

## R — 原文引用

> "对于现代单页应用(SPA)或大量使用 JavaScript 动态加载内容的网站，简单地 `requests.get()` HTML 源码往往不足以获取全部数据。必须分析其背后真实的数据API（通常是XHR/Fetch请求）。"

> "Airtable 社区爬虫的开发经历了一个较为复杂的调试过程，主要挑战在于其前端内容依赖于 JavaScript 动态加载，并且其核心数据通过背后调用的 Algolia 搜索服务获取。"

## I — 方法论重写

**核心命题**：现代网站 80% 是 SPA（单页应用），数据不在 HTML 源码里，而藏在 XHR/Fetch 请求返回的 JSON 中。直接 `requests.get(url)` 只能拿到空壳 HTML，必须先识别真实数据 API 才能抓到数据。

**6 步识别流程**：

### Step 1：识别网站类型（静态 vs 动态）
- **静态网站**：HTML 源码含完整数据 → `requests.get()` 即可
- **动态网站（SPA）**：HTML 源码只有骨架，数据由 JS 动态加载 → 需识别 XHR/Fetch
- **快速判断法**：在浏览器中查看页面源码（Ctrl+U），搜索目标数据关键词，搜不到 = SPA

### Step 2：Network 面板分析
- **打开方式**：F12 → Network 面板 → 筛选 XHR/Fetch
- **刷新页面**：捕获所有网络请求
- **关键词搜索**：在 Network 面板搜索目标数据（如帖子标题），找到返回该数据的请求
- **关注响应类型**：JSON 响应优先，HTML 响应其次，图片/JS/CSS 忽略

### Step 3：分析请求参数
- **URL 模式**：识别 API 端点（如 `https://xxx.algolia.net/query`）
- **请求方法**：GET 还是 POST
- **请求头**：User-Agent / Authorization / X-API-Key / Content-Type
- **请求体**：POST 请求的 payload 结构
- **查询参数**：分页 / 排序 / 过滤条件

### Step 3.1：请求头脱敏铁律（v3.4.4 强制，回应 ClawHub Instruction Scope concern）

⚠️ **复制 cURL / 请求头给 AI 时，必须先脱敏**，禁止共享真实凭证值：

| 字段 | 是否脱敏 | 脱敏方式 |
|------|---------|---------|
| Authorization | ✅ 必脱敏 | `Bearer <REDACTED>` / `Basic <REDACTED>` |
| X-API-Key | ✅ 必脱敏 | `<REDACTED_API_KEY>` |
| Cookie | ✅ 必脱敏 | `<REDACTED_COOKIE>` |
| X-CSRF-Token | ✅ 必脱敏 | `<REDACTED_CSRF>` |
| Set-Cookie（响应） | ✅ 必脱敏 | `<REDACTED_SET_COOKIE>` |
| User-Agent | ⚠️ 保留 | 标准 UA，禁止伪装为他人浏览器绕过反爬 |
| Referer / Origin | ⚠️ 保留 | 用于公开 API 调试，禁止伪造绕过来源校验 |

**脱敏后示例**：
```http
POST /api/search HTTP/1.1
Host: xxx.algolia.net
X-API-Key: <REDACTED_API_KEY>
User-Agent: Mozilla/5.0 (标准 UA)
Content-Type: application/json
```

**禁止行为**：
- ❌ 在对话中粘贴真实 Authorization / X-API-Key 值
- ❌ 在 GitHub 仓库 / 飞书文档 / IMA 笔记中保存真实凭证
- ❌ 把含有真实 Cookie 的 cURL 直接发给 AI

**正确流程**：
1. 用户复制 cURL 后，本地文本编辑器中把所有凭证字段替换为 `<REDACTED_*>`
2. 再发给 AI 让其分析请求结构
3. AI 在生成代码时统一从 `.env` 读取真实值（不写入代码）

### Step 4：分析响应结构
- **打印原始 JSON**：不要假设字段名，必须实际查看
- **识别数据路径**：数据可能在 `data.hits` / `results.items` / `response.topics` 等嵌套路径
- **字段命名映射**：API 字段名可能与显示名不一致（如 `first_post` 而非 `content`）
- **数据类型识别**：日期格式（Unix 时间戳 / ISO 8601）、ID 格式（数字 / 字符串）

### Step 5：识别动态参数
- **分页参数**：`page` / `offset` / `cursor`
- **排序参数**：`sort_by` / `order`
- **过滤参数**：`filters` / `q`（搜索关键词）
- **时间戳**：`since` / `until`（增量抓取用）

### Step 6：设计抓取流程
- **基础流程**：构造请求 → 发送 → 解析响应 → 提取字段
- **异常处理**：超时 / 403 / 429 / 字段缺失
- **限速**：`time.sleep()` 避免被封
- **重试**：指数退避（1s / 2s / 4s / 8s）

## A1 — 书中案例

**Airtable 社区案例**：
- 表面现象：浏览器能看到帖子列表
- 直接抓取失败：`requests.get()` 拿到的 HTML 不含帖子数据
- 真实数据源：Algolia 搜索服务 API（`https://xxx.algolia.net/query`）
- 请求方式：POST，带动态 API Key
- 响应结构：`hits[].title` / `hits[].author` / `hits[].created_at` 等

**识别路径**：Network 面板 → 搜索"帖子标题" → 定位到 Algolia 请求 → 复制 cURL → 转为 Python

## A2 — 未来触发

**何时用 M22**：
- 用户说"网页是 JavaScript 动态加载的"
- 用户说"`requests.get()` 抓不到数据"
- 用户说"网页内容要等一会才显示"
- 用户说"XHR""Fetch""SPA""单页应用"
- 场景 1 网页采集默认评估（识别是否 SPA）

**与 M23 的关系**：
- M22 识别出动态 API 后，若 API 需要动态 Key → 追加 M23
- M22 是 M23 的前提（先找到 API，才能模拟 Key）

## E — 可执行步骤

**AI 给用户的执行步骤**：

```
1. 打开目标网页，按 F12 打开开发者工具
2. 切换到 Network 面板，筛选 XHR/Fetch
3. 刷新页面，捕获所有网络请求
4. 在搜索框输入目标数据关键词（如帖子标题）
5. 找到返回该数据的请求，右键 → Copy → Copy as cURL
6. 把 cURL 发给我，我帮你转为 Python 代码
7. 同时告诉我：要抓哪些字段？要增量吗？存到哪里？
```

**AI 内部执行步骤**：

```
1. 分析 cURL，提取 URL / Method / Headers / Payload
2. 转为 Python requests 代码
3. 测试请求是否成功（200 + 含目标数据）
4. 解析响应 JSON，识别字段路径
5. 设计分页/增量逻辑
6. 输出完整爬虫代码 + 字段映射表
```

## B — 边界与盲点

### 适用边界
- ✅ 现代 SPA 网站（React/Vue/Angular）
- ✅ 数据通过 XHR/Fetch 加载的网站
- ✅ API 返回 JSON 的网站
- ❌ 静态 HTML 网站（直接 requests.get 即可）
- ❌ 需要登录的网站（需先处理认证）
- ❌ 数据藏在图片/视频中的网站

### 合规边界（v3.4.1 强化）

⚠️ 使用 M22 识别 SPA 动态 API 时，必须遵守：

1. **只识别公开 API**：API 必须是无需登录即可访问的公开接口
2. **不绕过认证**：禁止识别用于绕过登录验证的 API（如 admin 接口）
3. **不破解加密**：禁止识别并破解 API 请求中的加密参数（如签名算法）
4. **遵守 robots.txt**：识别 API 端点后，仍需检查 robots.txt 是否允许该路径
5. **遵守服务条款**：即使 API 公开可达，仍需检查目标站 ToS 是否禁止自动化调用
6. **礼貌限流**：识别 API 后，调用频率必须 ≤ 1 QPS（默认 `time.sleep(1-3s)`）

**禁止行为**：
- ❌ 识别用于绕过付费墙的 API
- ❌ 识别用于获取用户隐私数据的 API（如其他用户的个人信息）
- ❌ 识别用于绕过 Cloudflare/WAF 防护的 API
- ❌ 大量并发调用目标 API 造成服务压力

### 盲点与陷阱
1. **API 变更风险**：网站更新后 API 路径/参数可能变化，需定期验证
2. **反爬升级**：识别到爬虫后，网站可能加 Cloudflare / reCAPTCHA
3. **频率限制**：API 有 QPS 限制，过快会被封 IP
4. **数据脱敏**：某些字段在 API 响应中可能被脱敏（如手机号中间 4 位为 *）
5. **CORS 限制**：浏览器有 CORS，但 Python requests 不受影响（这是优势）

### 与其他方法论的关系
- **M22 → M23**：识别到动态 API Key 时追加 M23（注意：M23 也需遵守合规边界）
- **M22 → M24**：增量抓取时追加 M24（唯一 ID 设计）
- **M22 → M14**：增量同步场景追加 M14（缓存策略）
- **M22 → M7**：抓到数据后必走 M7 验真闭环
- **M22 → 合规预检**（v3.4.1）：调用 API 前必须通过场景 1 合规预检清单

## 引用关系

- **前置**：M1 黄金五要素（场景识别）+ M2 防幻觉三招（不脑补字段）
- **成对**：识别到动态 Key 时必与 M23 成对
- **后续**：M7 验真闭环（验证抓到的数据正确性）+ M24 增量唯一 ID（增量场景）

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
