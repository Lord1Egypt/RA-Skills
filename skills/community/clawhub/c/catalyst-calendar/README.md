# Catalyst Calendar — 催化事件日历 Skill

未来14天催化事件前瞻，覆盖宏观政策、财报、行业事件、市场技术四大维度。

## 功能

- 🔴🟡⚪ 三级影响标注：高/中/低影响事件分类
- 📅 多维度事件采集：
  - 宏观政策：美联储议息、央行操作、经济数据发布
  - 财报：关注标的及行业龙头财报季
  - 行业政策：监管新规、重大展会论坛
  - 市场技术：期权到期日、ETF调仓窗口
- ⏰ 提前提醒：高影响事件提前1天 IMA 笔记提醒

## 触发方式

- 说 "催化日历" / "事件日历" / "未来大事" / "catalyst calendar"
- 说 "下周有什么大事" / "本月重要事件"

## 依赖

- `web_search` tool
- `neodata-financial-search` skill（财报日期查询）

## 输出

Markdown 催化事件日历，保存至 `catalyst-calendar/reports/YYYY-MM-DD-catalyst-calendar.md`

## 版本

v1.0.0 — 初始版本
