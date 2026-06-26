# meta.json 字段规范（schema_version 1.2）

## 完整示例

    {
      "$schema_version": "1.2",
      "slug": "how-we-build-agent-skills",
      "title": "我们是如何构建 Agent Skill 的",
      "description": "从零到一设计一套可复用的 Agent Skill 架构",
      "author": "黎东",
      "route": "BLOG",
      "category": "技术探索",
      "categoryId": 5,
      "subCategory": "",
      "tags": ["Agent", "LangChain4j"],
      "coverImage": "./images/cover.webp",
      "coverImageUrl": "https://cdn.fenxianglife.com/xxx.webp",
      "publishTime": "2026-04-10T10:30:00+08:00",
      "readTime": "8 分钟",
      "tint": "bg-tint-blue",
      "sortOrder": 100,
      "components_used": ["Callout", "Timeline", "CodeTabs"],
      "render": {
        "last_rendered_at": "2026-04-10T10:31:05+08:00",
        "snapshot_version": "1.0",
        "feima_lab_commit": "abc1234"
      },
      "source": {
        "original_input": "plain_text",
        "source_md_exists": true
      },
      "publish": {
        "status": "draft",
        "remote_id": null,
        "last_saved_at": null,
        "last_saved_tag_ids": null,
        "published_at": null,
        "published_slug": null,
        "api_response": null
      }
    }

## 必填字段（save-article 前必须填好）

| 字段 | 类型 | 约束 |
|---|---|---|
| `slug` | string | kebab-case（小写字母/数字/单连字符，**不加日期前缀**），全局唯一，max 200 字 |
| `title` | string | 非空，max 300 字 |
| `description` | string | 非空，max 1000 字，建议 20-80 字 |
| `author` | string | 非空，从 MEMORY.md 默认 |
| `category` **或** `categoryId` | string / number | `categoryId` 优先；为空时按 `category` 名字 + `route` 自动查找 |

## 重要：`route` 字段（v1.2 新增）

`route` 决定文章属于哪个路由：

| 值 | 含义 | 前端路径 | 典型场景 |
|---|---|---|---|
| `BLOG` | 博客 | `/blog` | 技术文章、实践分享、产品思考 |
| `NEWS` | 动态 | `/news` | 产品更新、公司动态、行业观察 |

**默认是 `BLOG`**。Claude 看到"写博客"/"技术文章"类意图用 BLOG；"发公告"/"动态"/"新闻"类用 NEWS。

`category` 和 `categoryId` 的查找会按 `route` 过滤——所以同一个分类名在不同 route 下可能解析到不同 id，必须配对使用。

## 可选字段

| 字段 | 默认 | 说明 |
|---|---|---|
| `categoryId` | `null` | 后端分类 id（数字）。留空会自动按 `route` + `category` 名字查 |
| `subCategory` | `""` | 本 skill 保留字段，API 无对应字段，不上传 |
| `coverImage` | `""` | **本地路径**（如 `./images/cover.webp`），save 时自动上传 |
| `coverImageUrl` | `""` | **远程 URL**。save 前若为空会自动上传 `coverImage` 并回写本字段 |
| `tint` | `"bg-tint-blue"` | 列表卡片背景色块——**必须带 `bg-` 前缀** |
| `sortOrder` | `0` | 排序权重（数字，越大越靠前）。相同时按 updateTime 倒序 |
| `tags` | `[]` | 字符串数组。save-article 会闭环处理：查已有→缺失的自动建→上传 tagIds |
| `components_used` | `[]` | 由 Claude 根据 article.mdx 统计 |

## tint 合法值（后端字典）

必须带 `bg-` 前缀，否则后端会拒绝：

| 值 | 说明 |
|---|---|
| `bg-tint-yellow` | 米黄 |
| `bg-tint-blue`   | 淡蓝 |
| `bg-tint-rose`   | 淡粉 |
| `bg-tint-green`  | 淡绿 |

（v1.1 默认值 `tint-blue` 是 bug，v1.2 已修复为 `bg-tint-blue`）

## 受控字段（脚本自动写回，不要手工改）

| 字段 | 何时写入 |
|---|---|
| `categoryId` | save-article 成功后（自动查到的值） |
| `coverImageUrl` | save-article 触发自动上传后 |
| `publish.remote_id` | save-article 成功，后端返回 articleId |
| `publish.last_saved_at` | save-article 成功的时间 |
| `publish.last_saved_tag_ids` | v1.2 新增：save 闭环生成的 tagIds |
| `publish.status` | publish-article 成功后变 `"published"`；unpublish 成功后变 `"draft"` |
| `publish.published_at` | publish-article 成功的时间 |
| `publish.published_slug` | publish-article 成功的 slug |
| `render.last_rendered_at` | render.mjs 成功后 |

## tags 处理说明（v1.2 起闭环）

meta.tags 中的每个字符串：
1. skill 调 `GET /content/api/tag/list` 查后端已有标签
2. 名字大小写无关匹配——命中则复用 id
3. 未命中则调 `POST /content/api/tag/save` 自动创建（tagName ≤64 字符）
4. 最终 tagIds 写入 `publish.last_saved_tag_ids`，方便下次编辑

重复名字在同一次 save 内去重。

## 字段长度硬上限（后端约束）

| 字段 | 最大 |
|---|---|
| `slug` | 200 |
| `title` | 300 |
| `description` | 1000 |
| `tags[*]`（每个标签名） | 64 |

超出会在 save 前被 skill 校验拦截 / 后端拒绝。

## 校验清单（save-article 前自检）

- [ ] slug 格式为 kebab-case（不加日期前缀），长度 ≤ 200
- [ ] title ≤ 300，description ≤ 1000
- [ ] route 是 `BLOG` 或 `NEWS`
- [ ] `category`（名字）或 `categoryId`（数字）二选一已填
- [ ] tint 带 `bg-` 前缀
- [ ] 如果有封面图：`coverImage` 本地路径存在 **或** `coverImageUrl` 已填远程 URL
- [ ] article.mdx 存在且 render.mjs 可以成功渲染
- [ ] tags 每个名字 ≤ 64 字符

## 版本迁移

- **1.0 → 1.1**：加 categoryId / coverImageUrl / publish.remote_id / publish.last_saved_at
- **1.1 → 1.2**：加 route / sortOrder / publish.last_saved_tag_ids；修 tint 默认值为 `bg-tint-blue`；tags 字段不再被忽略

旧 meta.json 打开仍然可用——新增字段都有默认值。第一次跑 save-article 会自动写入所有受控字段。
