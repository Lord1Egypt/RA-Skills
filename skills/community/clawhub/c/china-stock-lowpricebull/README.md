# china-stock-lowpricebull

公开源低价擒牛策略（纯 OpenClaw 版本）。

## 依赖

- OpenClaw 内置工具：`exec`、`web_search`、`web_fetch`
- Python 3（`python` 或 `python3`）

## 使用

```bash
python3 "{baseDir}/scripts/a_share_public_selector.py" lowpricebull 10
```

参数：
- `strategy_type`：固定 `lowpricebull`
- `top_n`：可选，默认 10

## 返回

JSON 字段：`ok`、`strategy_type`、`stocks`、`message`。

## 说明

- 数据来自公开接口，结果为近似筛选，不等价问财。
- 仅供参考，不构成投资建议。
