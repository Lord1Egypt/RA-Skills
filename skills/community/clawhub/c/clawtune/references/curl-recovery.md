# ClawTune curl templates: recovery and tracing

```bash
export CLAWTUNE_BASE_URL="https://clawtune.aqifun.com/api/v1"
export CLAWTUNE_ACCESS_TOKEN="<access_token>"
```

## 1. 已知 order_id：查聚合状态

```bash
curl "$CLAWTUNE_BASE_URL/orders/<order_id>/status" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 2. 已知 order_id：查交付结果

```bash
curl "$CLAWTUNE_BASE_URL/orders/<order_id>/delivery" \
  -H "Authorization: Bearer $CLAWTUNE_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 3. 公开结果页查询

```bash
curl "$CLAWTUNE_BASE_URL/public/orders/<order_id>/result"
curl "$CLAWTUNE_BASE_URL/public/playlists/<playlist_id>"
```

## 4. 推荐恢复优先级
1. `order_id`
2. `GET /orders/<order_id>/delivery` 返回的 `playlist_id`
3. 仅有旧听歌 `playlist_id` 时，不要假装能直接恢复已完成的创作链

## 5. 推荐配合恢复脚本

```bash
# 直接从本地 session 中恢复
bash scripts/recover-order.sh

# 指定 order_id 恢复
bash scripts/recover-order.sh ord_xxx

# 若已经拿到结果歌单，再继续查公开歌单页
bash scripts/check-public-result.sh playlist pl_xxx
```

## 6. 当前 smoke 结果如何理解

本轮线上 smoke 已验证到：
- order status / delivery / public result / recover-order 可用
- 真实网页完成与页面承接由网页负责

所以如果还没有真实完成，就不要期待结果歌单已经可见；这时应继续围绕 `order_id` 查状态，而不是跳到其他对象。
