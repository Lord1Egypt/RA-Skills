---
name: china-stock-main-force
description: "主力候选池（纯 OpenClaw 公开源版）：基于东财公开实时主力净流入做候选池筛选。"
version: 2.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
---

# A 股主力选股（公开源）

## 工具

- `exec`：运行 `{baseDir}/scripts/a_share_main_force_public.py`
- `web_search`、`web_fetch`：补充资讯

## 调用

```bash
python3 "{baseDir}/scripts/a_share_main_force_public.py" 3m 100 50 5000 30 10
```

参数顺序：`period_type max_rows min_market_cap max_market_cap max_range_change top_n`

返回 JSON 字段：`ok`、`period_type`、`reference_final_n`、`rows`、`params`。

## 说明

- 本技能不依赖 `WENCAI_COOKIE`、不依赖 python-tools。
- 主力口径为公开源实时近似，不等价问财历史区间口径。
- 输出仅供参考，不构成投资建议。
