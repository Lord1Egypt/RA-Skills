---
name: china-stock-lowpricebull
description: "低价擒牛选股（纯 OpenClaw 公开源版）：基于东财公开行情做低价+资金强度近似筛选。"
version: 2.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
---

# A 股低价擒牛选股（公开源）

## 工具

- `exec`：运行 `{baseDir}/scripts/a_share_public_selector.py`
- `web_search`、`web_fetch`：补充资讯

## 调用

```bash
python3 "{baseDir}/scripts/a_share_public_selector.py" lowpricebull 10
```

返回 JSON 字段：`ok`、`strategy_type`、`stocks`、`message`。

## 说明

- 本技能不依赖 `WENCAI_COOKIE`、不依赖 python-tools。
- 该策略是公开源近似版本，不等价问财公式。
- 输出仅供参考，不构成投资建议。
