# 博客页面 API（2 端点）

路径前缀：`{base_url}` · 无认证 · 返回 HTML 页面

> 这两个端点返回完整 HTML 页面（博客前端），非 JSON API。
> 子命令返回 HTML 文本，适合预览或检查页面渲染。

## 1. GET / — 博客首页

**子命令**：`blog-home`

| 参数 | 位置 | 类型 | 默认 | 说明 |
|------|------|------|------|------|
| page | query | int | 1 | 页码 |
| lid | query | int | 0 | 标签 ID 筛选 |
| keyword | query | string | "" | 标题关键词搜索 |

```bash
curl -s --max-time 30 "{base_url}/?page=1"
```

响应：`text/html` — 文章列表页（含侧边栏热门文章 + 标签云 + 分页）

## 2. GET /article/{article_id} — 文章详情页

**子命令**：`blog-article`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| article_id | path | int | 是 | 文章 ID |

```bash
curl -s --max-time 30 "{base_url}/article/1"
```

响应：`text/html` — 文章详情页（含正文渲染 + 评论区） · 404 文章不存在

> 调用后文章热度 +1。
