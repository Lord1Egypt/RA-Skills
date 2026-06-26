---
name: cross-border-intel
description: 面向跨境卖家的选品与竞品情报助手，自动监控 Amazon ASIN 动态并追踪 TikTok 爆品趋势
metadata:
    openclaw:
        emoji: '🔍 '
        requires:
            bins: ['python3', 'curl', 'jq']
---

# 跨境选品情报助手

面向跨境卖家的本地化情报工作台，持续追踪 Amazon 竞品价格、BSR 与评价变化，并捕捉 TikTok 爆品信号，帮助你更快发现机会、验证选品和跟进竞品动作。

## 命令

### /intel_add <type> <value>
添加需要长期追踪的 Amazon ASIN 或 TikTok 关键词。

- `/intel_add asin B0XXXXXXXXX` — 添加 Amazon ASIN
- `/intel_add keyword "kitchen gadgets"` — 添加 TikTok 品类关键词

### /intel_list
查看当前监控清单与追踪范围。

### /intel_remove <type> <value>
从监控清单中移除目标。

### /intel_report [daily|weekly]
手动生成日报或周报，快速复盘市场变化。

### /intel_scan
立即执行一次全量扫描并刷新最新情报。

## 自动化
- 每天 08:00 自动扫描 Amazon 竞品数据
- 每天 20:00 自动扫描 TikTok 趋势数据
- 当价格变动 >5%、BSR 变动 >30% 或 TikTok 视频播放 >100 万时自动触发告警
- 每周一 09:00 自动生成周报，沉淀关键趋势与机会点