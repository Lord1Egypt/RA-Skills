# 订阅回调处理（MoviePilot）

脚本：
- `scripts/card_callback_router.py`（统一入口）
- `scripts/subscribe_callback_handler.py`（订阅处理器）

## 输入

- `--channel`：渠道（默认 feishu）
- `--user-id`：用户ID（用于读取用户凭证）
- `--payload`：卡片回调 JSON

回调 payload 约定：

```json
{"action":"subscribe","media_type":"movie|tv","tmdb_id":"1419406","title":"..."}
```

## 行为

1. 校验 payload 必要字段。
2. 幂等去重（30 秒窗口，按 `media_type+tmdb_id`）。
3. 查询是否已订阅：`/api/v1/subscribe/media/tmdb:<id>`。
4. 未订阅时调用 `POST /api/v1/subscribe/` 新增订阅。
5. 输出标准结果 JSON：created / exists / deduped / error。

## 示例

```bash
python3 scripts/subscribe_callback_handler.py \
  --channel feishu \
  --user-id ou_xxx \
  --payload '{"action":"subscribe","media_type":"movie","tmdb_id":"1419406","title":"捕风追影"}'
```
