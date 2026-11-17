# 网站分析脚本模板（v3.4.0）

> 场景 1 交付物模板（v3.4.0 新增，源自 TRAE 社区爬虫教程）
> 配套方法论：M22 SPA 动态 API 识别 + M23 动态 API Key 模拟
> 用途：用户在抓取网页数据前，AI 引导用户完成 6 步标准化网站分析

## 使用说明

**AI 行为**：
- 用户进入场景 1 且识别到 SPA 信号 → 主动展示本模板引导用户完成 6 步分析
- 用户完成分析后 → 基于结果生成爬虫代码

**用户行为**：
- 按步骤在浏览器 DevTools 中操作
- 把每步结果（cURL / HTML / JSON）粘贴给 AI
- AI 基于真实数据生成代码

---

## Step 1：识别网站类型（5 分钟）

### 操作
1. 打开目标网页
2. 按 Ctrl+U 查看页面源码
3. 在源码中搜索目标数据关键词（如帖子标题）

### 判断

| 搜索结果 | 网站类型 | 后续步骤 |
|---------|---------|---------|
| 搜到关键词 | 静态网站 | 直接用 requests.get + BeautifulSoup 解析 |
| 搜不到关键词 | 动态网站（SPA） | 继续步骤 2-6 |

### 记录

```
网站类型：[静态 / 动态]
判断依据：[源码中是否搜到目标数据]
```

---

## Step 2：Network 面板分析（10 分钟）

### 操作
1. 按 F12 打开开发者工具
2. 切换到 Network 面板
3. 筛选 XHR/Fetch
4. 刷新页面
5. 在搜索框输入目标数据关键词
6. 找到返回该数据的请求

### 记录

```
数据 API URL：[如 https://xxx.algolia.net/query]
请求方法：[GET / POST]
请求头：
  - User-Agent：[复制]
  - Authorization：[如有]
  - X-API-Key：[如有]
  - Content-Type：[如 application/json]
请求体（POST）：[复制 JSON]
响应类型：[JSON / HTML / XML]
响应数据路径：[如 hits[].title / results.items]
```

---

## Step 3：分析请求参数（5 分钟）

### 操作
1. 在 Network 面板查看请求 URL
2. 分析查询参数

### 记录

```
分页参数：[如 page / offset / cursor]
排序参数：[如 sort_by / order]
过滤参数：[如 filters / q]
时间戳参数：[如 since / until]
```

---

## Step 4：分析响应结构（10 分钟）

### 操作
1. 在 Network 面板查看响应
2. 打印原始 JSON（或复制到 JSON 格式化工具）
3. 识别字段路径

### 记录（字段映射表）

| 业务字段 | API 字段路径 | 数据类型 | 示例值 | 是否必填 |
|---------|------------|---------|--------|---------|
| 标题 | hits[].title | str | "如何用 AI 写爬虫" | ✅ |
| 作者 | hits[].author | str | "张三" | ✅ |
| 时间 | hits[].created_at | int (Unix 秒) | 1785042594 | ✅ |
| 点赞 | hits[].like_count | int | 42 | ✅ |
| 链接 | hits[].url | str (URL) | "https://..." | ✅ |
| 分类 | hits[].category.name | str | "技术分享" | ❌ |

---

## Step 5：识别动态参数（5 分钟）

### 操作
1. 查看请求头中的认证字段
2. 判断 Key 来源

### 判断

| Key 状态 | 处理方式 |
|---------|---------|
| 无 Key（公开 API） | 直接用，继续步骤 6 |
| 静态 Key（在请求头） | 复制即可，注意可能过期 |
| 动态 Key（每次不同） | 需用 M23 模拟获取流程 |

### 记录

```
Key 类型：[无 / 静态 / 动态]
Key 字段名：[如 X-API-Key / Authorization]
Key 来源：[如 HTML 内嵌 / 另一个 API 端点 / Cookie]
Key 获取链：[如 访问页面 → 请求 /api/auth → 返回 Key]
```

---

## Step 6：设计抓取流程（10 分钟）

### 操作
基于前 5 步分析结果，设计完整抓取流程

### 记录

```
基础流程：
  1. 构造请求（URL + Method + Headers + Payload）
  2. 发送请求
  3. 解析响应 JSON
  4. 提取字段（按字段映射表）
  5. 存储数据（CSV / 飞书多维表格）

异常处理：
  - 超时：[10 秒]
  - 403：[切换 User-Agent 或添加 Referer]
  - 429：[指数退避，1s/2s/4s/8s]
  - 字段缺失：[填 None 或跳过]

限速策略：
  - 每次请求间隔：[1-2 秒]
  - 单次抓取量：[如 100 条]
  - 总抓取上限：[如 1000 条]

增量策略（如适用）：
  - 唯一 ID：[如 tid 从 URL 解析]
  - 缓存方式：[JSON 文件 / SQLite / 飞书多维表格]
  - 增量逻辑：[抓新数据 → 对比已缓存 → 过滤 → 写入 → 更新缓存]
```

---

## 完成标志

✅ 6 步分析全部完成 → AI 基于结果生成完整爬虫代码
❌ 任一步骤卡住 → 主动反问用户对应步骤的问题

## 与其他模板的关系

- 完成本模板后 → 进入 [scenario-1-prompt-template.md](scenario-1-prompt-template.md) 生成最终 Prompt
- 如需飞书存储 → 进入 [feishu-base-storage-template.md](feishu-base-storage-template.md) 设计字段映射
- 如遇调试问题 → 参考 [crawler-debug-experience.md](crawler-debug-experience.md)

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
