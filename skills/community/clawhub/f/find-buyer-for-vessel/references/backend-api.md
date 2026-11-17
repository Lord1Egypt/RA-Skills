# 卖家找买家需求同步

后台接口提供后设置：

- `API_BASE_URL`
- `SELLER_BUYER_DEMAND_API_PATH`
- 可选的 `ADMIN_API_KEY` 或 `ADMIN_TOKEN`

技能以 `POST application/json` 提交：

```json
{
  "user_id": "卖家用户ID",
  "vessel_type": "油船",
  "capacity": "5000DWT",
  "age": "8年",
  "flag": "中国旗",
  "trade_scope": "内贸",
  "queried_at": "ISO-8601时间"
}
```

接口未配置或提交失败时写入缓存目录的 `demand_outbox.jsonl`。测试阶段用户ID为空时跳过同步。
