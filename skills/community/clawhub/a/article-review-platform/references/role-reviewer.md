# 审稿角色指引（文风分析师）

## 职责
获取待审文章，审稿打分，更新审稿轮次。

## 获取待审文章
```bash
# 草稿状态，审稿轮次 < 3
curl -s "http://localhost:3100/api/articles?status=draft" | \
  jq '[.articles[] | select(.review_round < 3)]'
```

## 阅读文章内容
```bash
curl -s "http://localhost:3100/api/articles/{id}/content"
# 或读本地文件
cat "{project_path}/draft.md"
```

## 更新审稿轮次
```bash
curl -s -X PUT "http://localhost:3100/api/articles/{id}" \
  -H "Content-Type: application/json" \
  -d '{"review_round": 2}'
```

## 审稿完成（3轮后）
```bash
curl -s -X PUT "http://localhost:3100/api/articles/{id}" \
  -H "Content-Type: application/json" \
  -d '{"status":"in_review","review_round":3}'
```
