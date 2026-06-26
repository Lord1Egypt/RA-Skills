# china-stock-main-force

公开源主力候选池策略（纯 OpenClaw 版本）。

## 依赖

- OpenClaw 内置工具：`exec`、`web_search`、`web_fetch`
- Python 3（`python` 或 `python3`）

## 使用

```bash
python3 "{baseDir}/scripts/a_share_main_force_public.py" 3m 100 50 5000 30 10
```

参数顺序：
1. `period_type`：`3m` / `6m` / `1y`
2. `max_rows`
3. `min_market_cap`（亿）
4. `max_market_cap`（亿）
5. `max_range_change`（%）
6. `top_n`

## 返回

JSON 字段：`ok`、`period_type`、`reference_final_n`、`rows`、`params`。

## 说明

- 主力口径来自公开接口实时数据，和问财历史区间不完全一致。
- 仅供参考，不构成投资建议。
