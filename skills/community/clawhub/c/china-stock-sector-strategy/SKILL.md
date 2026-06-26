---
name: china-stock-sector-strategy
description: "板块策略分析（纯 OpenClaw 公开源版）：基于东财公开行业/概念板块快照。"
version: 2.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
---

# A 股板块策略（公开源）

## 工具

- `exec`：运行 `{baseDir}/scripts/sector_strategy_public.py`
- `web_search`、`web_fetch`：补充资讯

## 调用

```bash
python3 "{baseDir}/scripts/sector_strategy_public.py" 1D
```

返回 JSON 字段：`ok`、`payload`、`sectors_count`、`concepts_count`。

## 说明

- 本技能不依赖 `WENCAI_COOKIE`、不依赖 python-tools。
- 北向资金在公开接口里不稳定，脚本会返回限制说明。
- 输出仅供参考，不构成投资建议。
