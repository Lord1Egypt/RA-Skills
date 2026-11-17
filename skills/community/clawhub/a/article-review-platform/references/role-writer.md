# 写稿角色指引（小博）

## 职责
创建文章记录，管理写作状态，审稿后更新状态。

## 创建文章
```bash
curl -s -X POST "http://localhost:3100/api/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "文章标题",
    "slug": "article-slug",
    "status": "draft",
    "project_path": "/path/to/project",
    "target_platforms": ["github", "wechat"],
    "complexity": "medium"
  }'
```

## 更新状态
```bash
# 审稿完成，标记为 in_review
curl -s -X PUT "http://localhost:3100/api/articles/{id}" \
  -H "Content-Type: application/json" \
  -d '{"status":"in_review"}'
```

## 读取文章内容
```bash
curl -s "http://localhost:3100/api/articles/{id}/content"
```
