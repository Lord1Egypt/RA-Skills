# china-stock-sector-strategy

公开源板块策略分析（纯 OpenClaw 版本）。

## 依赖

- OpenClaw 内置工具：`exec`、`web_search`、`web_fetch`
- Python 3（`python` 或 `python3`）

## 使用

```bash
python3 "{baseDir}/scripts/sector_strategy_public.py" 1D
```

参数：
- `period_type`：当前固定 `1D`

## 返回

JSON 字段：`ok`、`payload`、`sectors_count`、`concepts_count`。

## 说明

- 北向资金在公开接口可得性不稳定，脚本会返回限制说明。
- 仅供参考，不构成投资建议。
