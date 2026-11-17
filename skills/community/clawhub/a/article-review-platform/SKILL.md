---
name: article-review-platform
description: |
  文章审阅平台（Article Review Platform）的完整使用指南。
  覆盖：文章列表查看、内容阅读、创建新文章、更新状态、发布状态同步、审稿流程。
  适用角色：小博（写稿）→ 文风分析师（审稿）→ 文章发布管家（发布）
  触发词：审阅平台、article review platform、平台API、审稿、review、发布文章
---

# 文章审阅平台使用指南

## 平台信息
- **API**: http://localhost:3100
- **前端看板**: http://localhost:5174
- **项目目录**: ~/workspace/project/article-review-platform/
- **数据流**: 小博写稿 → 平台创建记录 → 文风分析师审稿 → 用户确认 → 文章发布管家发布

## 文章状态完整流转
```
draft → in_review → approved → publishing → published
  ↑        ↑           ↑          ↑           ↑
  写稿    审稿中     审稿通过    发布中     全部发完
```

每篇文章有 `platform_status`（JSON对象），记录各平台的发布进度：`pending` → `publishing` → `published` / `failed`

## API 速查

### 健康检查
```bash
curl -s http://localhost:3100/api/health
```

### 获取文章列表
```bash
# 按状态筛选
curl -s "http://localhost:3100/api/articles?status=draft"
curl -s "http://localhost:3100/api/articles?status=in_review"
curl -s "http://localhost:3100/api/articles?status=approved"
curl -s "http://localhost:3100/api/articles?status=publishing"
curl -s "http://localhost:3100/api/articles?status=published"

# 按标题搜索
curl -s "http://localhost:3100/api/articles?q={title}"

# 获取特定文章
curl -s "http://localhost:3100/api/articles/{id}"
```

**返回字段**：`id`, `title`, `slug`, `project_path`, `feishu_url`, `review_round`, `status`, `priority`, `complexity`, `target_platforms`, `platform_status`, `created_at`, `updated_at`

### 阅读文章内容
```bash
curl -s "http://localhost:3100/api/articles/{id}/content"
# 或直接读本地文件
cat "{project_path}/draft.md"
```

### 创建新文章
```bash
curl -s -X POST "http://localhost:3100/api/articles" \
  -H "Content-Type: application/json" \
  -d '{"title":"标题","slug":"slug","status":"draft","project_path":"/path/to/project","target_platforms":["github","wechat"],"complexity":"medium"}'
```

### 更新文章状态
```bash
curl -s -X PUT "http://localhost:3100/api/articles/{id}" \
  -H "Content-Type: application/json" \
  -d '{"status":"publishing"}'
```
状态值：`draft` / `in_review` / `approved` / `publishing` / `published`

### 更新平台发布状态
```bash
curl -s -X PUT "http://localhost:3100/api/articles/{id}" \
  -H "Content-Type: application/json" \
  -d '{"platform_status":{"zhihu":"published","csdn":"failed"}}'
```

### 发布日志
```bash
# 记录
curl -s -X POST "http://localhost:3100/api/articles/{id}/publish-logs" \
  -H "Content-Type: application/json" \
  -d '{"platform":"zhihu","stage":"completed","status":"success","message":"发布成功"}'

# 查看
curl -s "http://localhost:3100/api/articles/{id}/publish-logs"
```

### 删除文章
```bash
curl -s -X DELETE "http://localhost:3100/api/articles/{id}"
```

## 角色分工

### 小博（blog-agent）— 写稿
- 创建文章记录（POST）→ status=draft
- 审稿后更新 → PUT status=in_review
- 详见 `references/role-writer.md`

### 文风分析师 — 审稿
- 获取待审文章（status=draft/in_review）
- 阅读内容审稿，更新 review_round
- 3轮审稿完成 → 标记
- 详见 `references/role-reviewer.md`

### 文章发布管家（article-publisher-agent）— 发布
- 查询 status=approved / status=publishing 的文章
- 检查 platform_status，找出还有 pending/failed 的
- 发布到各平台，更新 platform_status
- 每步记录 publish-logs
- 全部完成 → PUT status=published
- 详见 `references/role-publisher.md`

## 完整链路
```
小博: POST → status=draft
  ↓ 文风分析师审稿(1-3轮)
小博: PUT → status=in_review
  ↓ 用户在飞书确认
用户/小博: PUT → status=approved
  ↓ 文章发布管家开始发布
发布管家: PUT → status=publishing + 更新 platform_status
  ↓ 所有平台完成
发布管家: PUT → status=published
```

## 本地文件结构
```
{project_path}/
├── README.md        # 项目概览、状态、飞书链接
├── draft.md         # 草稿
├── archive/         # 旧版本存档
└── published/       # 发布版本
```

## 注意事项
- 使用前确保平台运行（`curl http://localhost:3100/api/health`）
- 启动：`cd ~/workspace/project/article-review-platform && npm run dev`
- platform_status 字段是 JSON，API 返回时已解析
- 每个平台状态值：`pending` / `publishing` / `published` / `failed`
