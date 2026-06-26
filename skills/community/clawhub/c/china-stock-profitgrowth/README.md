# china-stock-profitgrowth

公开源净利增长近似策略（纯 OpenClaw 版本）。

## 依赖

- OpenClaw 内置工具：`exec`、`web_search`、`web_fetch`
- Python 3（`python` 或 `python3`）

## 使用

```bash
python3 "{baseDir}/scripts/a_share_public_selector.py" profitgrowth 10
```

参数：
- `strategy_type`：固定 `profitgrowth`
- `top_n`：可选，默认 10

## 返回

JSON 字段：`ok`、`strategy_type`、`stocks`、`message`。

## 说明

- 公开接口不提供完整问财净利同比字段，本策略为公开源近似版本。
- 仅供参考，不构成投资建议。
