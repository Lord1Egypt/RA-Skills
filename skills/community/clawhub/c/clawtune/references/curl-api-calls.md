# ClawTune curl templates: core API calls

```bash
export CLAWTUNE_BASE_URL="https://clawtune.aqifun.com/api/v1"
export CLAWTUNE_ACCESS_TOKEN="<access_token>"
```

## 1. 获取内容维度

```bash
curl "$CLAWTUNE_BASE_URL/content/facets" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 2. 生成歌单（主路径）

```bash
curl -X POST "$CLAWTUNE_BASE_URL/playlists/generate" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: playlist-gen-demo-001" \
  -d '{
    "title": "Late Night City Walk",
    "summary": "A moody but not too dark original playlist for walking home after overtime.",
    "query": "late-night walking, slightly emo but not too dark, atmospheric original playlist",
    "target_count": 3,
    "limit": 5,
    "is_public": false,
    "user_ref": "demo-user-001",
    "skill_session_id": "sess-demo-001",
    "idempotency_key": "playlist-gen-demo-001",
    "style_tags": [],
    "mood_tags": [],
    "scene_tags": []
  }'
```

## 3. 创建创作草案

```bash
curl -X POST "$CLAWTUNE_BASE_URL/creation-drafts" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "proposal_summary": "A warm cinematic anniversary song based on a late-night city-walk feeling.",
    "theme": "anniversary",
    "style": "mandopop",
    "language": "zh-CN",
    "mood": "warm",
    "scene": "gift",
    "lyrics_input": "We walked home together after long days and still felt close.",
    "user_ref": "demo-user-001",
    "skill_session_id": "sess-demo-001",
    "source_context_playlist_id": "<playlist_id>"
  }'
```

## 4. 更新草案

```bash
curl -X PATCH "$CLAWTUNE_BASE_URL/creation-drafts/<draft_id>" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "bright"
  }'
```

## 5. 草案推荐

```bash
curl -X POST "$CLAWTUNE_BASE_URL/creation-drafts/<draft_id>/recommendations" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 6. 创建订单

```bash
curl -X POST "$CLAWTUNE_BASE_URL/orders" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: order-demo-001" \
  -d '{
    "draft_id": "<draft_id>",
    "proposal_summary": "A warm cinematic anniversary song with gentle late-night imagery.",
    "currency": "CNY",
    "user_ref": "demo-user-001",
    "skill_session_id": "sess-demo-001",
    "source_context_playlist_id": "<playlist_id>",
    "idempotency_key": "order-demo-001"
  }'
```

## 7. 订单创建后的正确承接

```text
skill 对用户只应返回线上正式订单入口链接。
后续步骤都应由 ClawTune 网页承接，而不是继续由对话 agent 调 API 完成。
```

## 8. 推荐配合脚本

```bash
bash scripts/auth-bootstrap.sh ensure
bash scripts/api-request.sh GET /content/facets
bash scripts/generate-playlist.sh "Late Night City Walk" "A moody but not too dark original playlist for walking home after overtime." "late-night walking after overtime"
bash scripts/main-flow-smoke.sh
```
