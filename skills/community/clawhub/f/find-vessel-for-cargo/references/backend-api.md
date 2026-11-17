# 货找船需求同步接口

后台接口提供后设置：

- `API_BASE_URL`：后台基础地址。
- `VESSEL_DEMAND_API_PATH`：货找船需求提交路径。
- `ADMIN_API_KEY` 或 `ADMIN_TOKEN`：可选鉴权信息。

技能以 `POST application/json` 提交：

```json
{
  "user_id": "货主用户ID",
  "load_port": "装货港名称或UN/LOCODE",
  "discharge_port": "卸货港名称或UN/LOCODE",
  "cargo_name": "货名",
  "cargo_tons": 10000,
  "loading_date": "2026-07-25",
  "trade_type": "domestic",
  "queried_at": "ISO-8601时间"
}
```

接口未配置或请求失败时，需求写入技能缓存目录下的
`demand_outbox.jsonl`。测试阶段用户ID为空时跳过同步，不写待同步队列。
