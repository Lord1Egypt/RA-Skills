---
name: bytetech
description: 获取 ByteTech 技术文章的元信息、目录结构和正文内容。通过 Chrome DevTools MCP 直连用户本地 Chrome，复用登录态，抓包分析 API，提取文章数据。触发词：bytetech、字节技术、技术文章、bytetech article、获取 bytetech 文章、整理 bytetech。
allowed-tools: Bash(mcporter:*), Bash(npx -y chrome-devtools-mcp@latest:*)
---

# ByteTech 文章获取

通过 Chrome DevTools MCP 连接用户本地 Chrome，复用登录态，抓取 ByteTech 技术文章。

## 前置条件

1. Chrome 已开启远程调试：`chrome://inspect/#remote-debugging`
2. mcporter 已配置 chrome-devtools server

## 验证连接

```bash
mcporter call chrome-devtools.list_pages
```

应返回 Chrome 中打开的页面列表。

## 获取文章详情（核心 API）

```bash
# 1. 导航到 bytetech 文章页（在 Chrome 新 tab 中打开）
mcporter call chrome-devtools.new_page url="https://bytetech.info/articles/<ARTICLE_ID>" timeout=30000

# 2. 刷新并抓包
mcporter call chrome-devtools.navigate_page type=reload

# 3. 过滤 XHR/Fetch 请求，找到文章详情 API
mcporter call chrome-devtools.list_network_requests resourceTypes='["xhr","fetch"]'
# 找 reqid 对应 /proxy_tech_api/v1/article/detail

# 4. 获取文章详情响应
mcporter call chrome-devtools.get_network_request reqid=<ID>
```

**文章详情 API** 返回完整元信息：
- `data.article_info.title` — 标题
- `data.article_info.en_title` — 英文标题
- `data.article_info.summary` — 摘要
- `data.article_info.lark_doc_token` — 飞书文档 token
- `data.article_info.lark_doc_url` — 飞书文档 URL
- `data.article_info.view_cnt` — 浏览量
- `data.article_info.dig_cnt` — 点赞数
- `data.article_info.collect_cnt` — 收藏数
- `data.article_info.coin_cnt` — 投币数
- `data.article_info.labels` — 标签列表 `[{name, en_name, ...}]`
- `data.auther` — 作者信息 `[{name, full_name, email, department_name, ...}]`

**Request Body:**
```json
{"article_id":"<ARTICLE_ID>","id_type":8}
```

## 直接调用 bytetech API（无需浏览器刷新）

用 `evaluate_script` 在 bytetech 页面上下文中直接 fetch：

```bash
# 获取文章详情
mcporter call chrome-devtools.evaluate_script function='
async () => {
  const resp = await fetch("/proxy_tech_api/v1/article/detail", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({article_id: "7619471842051620907", id_type: 8})
  });
  return await resp.json();
}'
```

```bash
# 获取推荐文章
mcporter call chrome-devtools.evaluate_script function='
async () => {
  const resp = await fetch("/proxy_tech_api/v1/article/recommend", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({article_id: "7619471842051620907", id_type: 8, limit: 10})
  });
  return await resp.json();
}'
```

```bash
# 获取团队目录和关联文章
mcporter call chrome-devtools.evaluate_script function='
async () => {
  const resp = await fetch("/proxy_tech_api/v2/content/team_account/item_include_info", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({item_id: "7619471842051620907", id_type: 8})
  });
  return await resp.json();
}'
```

```bash
# 获取团队热门文章
mcporter call chrome-devtools.evaluate_script function='
async () => {
  const resp = await fetch("/proxy_tech_api/v1/content/team_account/rank/item", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({team_id: "<TEAM_ID>", limit: 10})
  });
  return await resp.json();
}'
```

## 获取文章正文

bytetech 文章正文存储在飞书文档中。

### 方式 A：lark-cli（推荐）

```bash
# 从 bytetech API 获取 lark_doc_token
# 然后用 lark-cli 获取飞书文档内容
lark-cli docs +fetch --as user --doc "<LARK_DOC_TOKEN>"
```

### 方式 B：Chrome DevTools MCP 导航到飞书文档

```bash
# 选择 bytetech 页面所在的 browser context（共享 cookies）
# 导航到飞书文档
mcporter call chrome-devtools.navigate_page type=url url="https://bytetech.info/articles/<ID>"
# 等待加载
mcporter call chrome-devtools.wait_for text='["文章"]' timeout=15000
# 提取页面文本
mcporter call chrome-devtools.take_snapshot
```

### 方式 C：evaluate_script 提取（从 SSR meta）

```bash
mcporter call chrome-devtools.evaluate_script function='
() => {
  const title = document.title.replace(/ - 文章 - ByteTech$/, "");
  const og = {};
  document.querySelectorAll("meta[property^=\"og:\"],meta[name]").forEach(m => {
    const k = m.getAttribute("property") || m.getAttribute("name");
    og[k] = m.content || "";
  });
  return JSON.stringify({title, description: og["og:description"] || og["description"]});
}'
```

## 搜索文章

```bash
# 在 bytetech 页面中搜索
mcporter call chrome-devtools.navigate_page type=url url="https://bytetech.info"
mcporter call chrome-devtools.wait_for text='["ByteTech"]' timeout=15000
mcporter call chrome-devtools.take_snapshot
# 找到搜索框 uid 后 fill
mcporter call chrome-devtools.fill uid="<SEARCH_UID>" value="AI Coding"
mcporter call chrome-devtools.press_key key=Enter
mcporter call chrome-devtools.wait_for text='["搜索结果"]' timeout=10000
mcporter call chrome-devtools.take_snapshot
```

## 抓包模式（接口探索）

```bash
# 导航到目标页面
mcporter call chrome-devtools.navigate_page type=reload

# 列出所有 API 请求
mcporter call chrome-devtools.list_network_requests resourceTypes='["xhr","fetch"]'

# 查看具体请求详情（含完整 headers 和 body）
mcporter call chrome-devtools.get_network_request reqid=<ID>

# 保存响应到文件（大响应）
mcporter call chrome-devtools.get_network_request reqid=<ID> responseFilePath=/tmp/response.json
```

## API 速查表

| API | Method | 用途 | Request Body |
|-----|--------|------|-------------|
| `/proxy_tech_api/v1/article/detail` | POST | 文章详情（标题、摘要、标签、作者、飞书token） | `{article_id, id_type:8}` |
| `/proxy_tech_api/v1/article/recommend` | POST | 推荐文章列表 | `{article_id, id_type:8, limit}` |
| `/proxy_tech_api/v2/content/team_account/item_include_info` | POST | 团队目录和关联文章 | `{item_id, id_type:8}` |
| `/proxy_tech_api/v1/content/team_account/rank/item` | POST | 团队热门文章排行 | `{team_id, limit}` |
| `/proxy_tech_api/v1/content/item_detail_inclusion` | POST | 文章详细关联信息 | `{item_id, id_type:8}` |
| `/proxy_tech_api/v2/label/tree` | POST | 标签树 | `{}` |
| `/proxy_tech_api/v2/search/hotwords` | GET | 热搜词 | - |
| `/proxy_tech_api/v1/login` | POST | 登录检查 | `{}` |
| `/api/v1/lark/component_auth` | POST | 飞书组件鉴权 | `{url}` |

## Cookie 说明

bytetech 使用以下 Cookie 进行鉴权：
- `gateway_sid` — 网关 session
- `bytetech=bytetech-user` — 用户标识
- `csrf_session_id` — CSRF 防护

通过 Chrome DevTools MCP 的 `--autoConnect` 直连用户 Chrome，自动继承所有 Cookie，无需额外处理。

## 批量获取文章并总结

### Step 1: 获取文章列表

先通过推荐 API 或团队排行 API 获取一批文章 ID：

```bash
# 推荐文章（基于某篇文章）
mcporter call chrome-devtools.evaluate_script function='
async () => {
  const resp = await fetch("/proxy_tech_api/v1/article/recommend", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({limit: 10})
  });
  const data = await resp.json();
  return JSON.stringify(data.data.map(i => ({
    article_id: i.article_info.article_id,
    title: i.article_info.title,
    author: i.auther.name,
    summary: (i.article_info.generated_summary || i.article_info.summary || "").substring(0, 200),
    lark_doc_token: i.article_info.lark_doc_token,
    views: i.article_info.view_cnt,
    likes: i.article_info.dig_cnt,
    collects: i.article_info.collect_cnt
  })));
}'
```

```bash
# 团队热门文章
mcporter call chrome-devtools.evaluate_script function='
async () => {
  const resp = await fetch("/proxy_tech_api/v1/content/team_account/rank/item", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({team_id: "<TEAM_ID>", limit: 10})
  });
  return await resp.json();
}'
```

### Step 2: 批量获取文章详情

拿到 article_id 列表后，逐个调用 article/detail 获取完整元信息（标题、摘要、标签、作者、数据）。

### Step 3: 按需获取正文

如果需要正文内容（不仅仅是摘要），逐个用 lark-cli 获取飞书文档：

```bash
lark-cli docs +fetch --as user --doc "<LARK_DOC_TOKEN>" 2>&1
```

**注意**：
- 每篇正文可能 10000-50000+ 字符，10 篇全文可能超过上下文窗口
- **建议策略**：先只取摘要和 generated_summary 做初步筛选，再对感兴趣的 3-5 篇取全文
- 正文返回格式为 JSON，`data.markdown` 字段包含 markdown 格式的完整正文
- 长文的 markdown 中包含飞书自定义标签（如 `<lark-td>` 等），需要清洗

### Step 4: 清洗正文（Markdown 清洗）

lark-cli 返回的飞书文档 markdown 包含大量飞书自定义标签，需要清洗：

```bash
lark-cli docs +fetch --as user --doc "<TOKEN>" 2>&1 | node -e "
let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{
  const r=JSON.parse(d);
  let md = r.data.markdown;
  // 清洗飞书自定义标签
  md = md.replace(/<\/?lark-[a-zA-Z0-9_-]+>/g, '');
  md = md.replace(/<\/?grid[^>]*>/g, '');
  md = md.replace(/<\/?column[^>]*>/g, '');
  md = md.replace(/<mention-doc[^>]*>.*?<\/mention-doc>/g, '');
  md = md.replace(/<quote-container>.*?<\/quote-container>/gs, '');
  md = md.replace(/<image[^>]*\/>/g, '');
  // 保留标准 markdown 格式
  console.log(md);
})"
```

### Step 5: 生成总结

根据获取到的数据，生成结构化总结，包括：
- 文章标题和链接：`https://bytetech.info/articles/<article_id>`
- 作者和部门
- 核心要点（从 summary 或正文中提取）
- 数据指标（阅读量、点赞、收藏）
- 趋势观察（多篇之间共同的话题方向）

### 链接格式

- ByteTech 文章：`https://bytetech.info/articles/<article_id>`
- 飞书文档：`https://bytetech.info/articles/<article_id>#<lark_doc_token>`

**注意**：ByteTech 文章需要飞书 OAuth 登录后才能查看，未登录会跳转登录页。

## id_type 说明

- `8` — 文章
- `24` — 其他类型（视频等）
