---
name: agent-stock-pro
description: "股市 AI 量化交易 Pro 版，支持选股、交易决策、持仓分析、量化评分、PDF 报告生成、策略跟踪模拟交易等。基于 agent-stock 优化：修复 PDF 中文字体、精简工作流、支持定时任务。"
author: Tom (forked from AnoyiX/agent-stock)
version: "0.4.0"
tags:
  - Stock
  - 股票数据
  - 选股
  - 持仓分析
  - 交易决策
  - 量化交易决策
  - PDF报告
  - 定时任务
  - 策略跟踪
---

# Agent Stock Pro

> 📌 **Fork 自** [AnoyiX/agent-stock](https://clawhub.ai/anoyix/agent-stock) v0.2.8
> 原版许可：MIT-0。本 fork 在保留核心功能的基础上做了 **13 项核心优化**：
>
> **选股条件层（screen.md）：**
> 1. 条件选股增加市值/板块过滤，候选池控制在 10-15 只，减少无效工作量
> 2. 新增"昨日情绪延续"因子（强势股惯性、龙头首阴扫描）
> 3. 区分"趋势跟随"与"拐点博弈"两条策略路线，避免逻辑矛盾
> 4. 大盘状态自适应：根据综合评分动态调整选股条件、仓位上限、止损要求
>
> **深度分析层：**
> 5. 选股流程直接对候选股跑 `stock quant`（五维量化评分），替代人工分析 `stock quote`
> 6. 新增连板/龙头识别：连板数统计、同板块涨幅排名、龙虎榜辨识度
> 7. 风险排查扩展：北向资金流出、融资余额异常、限售股解禁、股权质押率等一票否决项
>
> **评分体系层（quant.md）：**
> 8. 快讯加分限制为风险排查维度内子项评分（≤5分），禁止直接加到总分
> 9. 维度冲突修正从 6 种扩展至 10 种（含板块强+大盘弱、RSI背离无量、尾盘偷袭等）
> 10. 决策矩阵增加波动率修正：高波动题材股与低波动蓝筹差异化操作
>
> **执行层：**
> 11. 新增黑名单规则：放量滞涨、长上影线密集、尾盘偷袭等坚决不碰的形态
> 12. 买入价精确到 2-3 档挂单（基于集合竞价+EMA10+BOLL中轨），止损精确到分
> 13. 全局仓位约束：总仓位上限、同板块上限、评分加权分配
>
> **工程优化：**
> - 修复 weasyprint 生成 PDF 时中文乱码问题（显式 @font-face 加载中文字体）
> - 精简 screen.md 工作流描述，适配 isolated cron job 自动执行选股+PDF发送

帮助用户查询实时股市数据，分析数据，为用户提供交易决策。

## Workflows

当用户有如下需求时，可以查看对应的文档，帮用户完成相关任务：

- 短线交易选股：参考文档 [references/screen.md](references/screen.md)，为用户完成选股；
- 短线交易决策：参考文档 [references/trade.md](references/trade.md)，为用户完成个股交易决策；
- 短线量化交易决策：参考文档 [references/quant.md](references/quant.md)，为用户完成个股量化交易决策；
- 用户持仓分析：参考文档 [references/holdings.md](references/holdings.md)，为用户完成持仓分析；
- 策略跟踪（模拟交易）：参考文档 [references/strategy-track.md](references/strategy-track.md)，基于选股建议模拟执行买卖，跟踪策略有效性；

## Prerequisites

检查 `stock` 命令是否已安装：

```bash
stock -v
```

如果没有安装，需要先安装 `stock` 命令行工具：

**uv:**
```bash
uv tool install agent-stock
```

**pip:**
```bash
pip3 install agent-stock
```

如果用户没有 `uv` 或者 `pip`，需要先帮用户安装好 python 环境，然后使用 `pip` 安装 `agent-stock` 包。

同时需要 `weasyprint` 用于生成 PDF 报告：

```bash
pip3 install weasyprint
```

## PDF 中文字体

生成 PDF 报告时，必须使用 `@font-face` 显式加载系统已安装的 `Noto Sans CJK SC` 中文字体，否则中文会显示为方块/乱码。

screen.md 中的 PDF 转换脚本模板已包含正确的字体配置，直接使用即可。
