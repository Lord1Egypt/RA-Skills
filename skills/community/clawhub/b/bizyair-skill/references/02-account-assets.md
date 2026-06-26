# 02 账号与资产

用于 API Key 管理、钱包余额、调用记录查询。

## API Key

### 检查

```bash
python3 scripts/cli.py check
python3 scripts/cli.py check --api-key <KEY>
```

返回 `status`：`ok` / `no_key` / `invalid_key` / `no_balance`

### 配置优先级

1. CLI `--api-key`
2. 环境变量 `BIZYAIR_API_KEY`
3. `config.json` → `credentials.api_key`（单 key）或 `credentials.api_keys[]`（多 key）

多 Key 时自动轮换：遇到余额不足 / 限流 / 排队满等可重试错误自动换下一个 key。

### 余额查询

```bash
python3 scripts/cli.py wallet
```

对应接口：`GET /y/v1/wallet`

返回：`charge_balance_amount` + `gift_balance_amount` + `total_balance_amount`

## 调用记录

AI 应用和 modelzoo 的调用记录统一走 `POST /x/v1/modelzoo/mycalls`：

- AI 应用：`call_type=comfy_task`
- ModelZoo：`call_type=trd_api_record`

不传时间时默认查最近 2 天。

单条详情：
- `GET /x/v1/modelzoo/mycalls/comfy_task/:request_id`
- `GET /x/v1/modelzoo/mycalls/trd_api_record/:request_id`

trd_api_record 单条额外含 `request_payload`（原始参数）和 `usage.charge_amount`（精确金币消耗）。
