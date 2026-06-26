name: web3-weekly-report
description: 自动抓取数据并生成 Web3 行业资本运作周报，涵盖融资事件、监管动态、上市公司 DAT 动态、并购交易与 RWA 项目追踪。当用户提到"写周报"、"生成周报"、"整理本周融资"、"Web3 周报"、"资本运作周报"、"采编周报"，或请求整理加密行业本周动态时，立即激活此 skill。即使用户只说"帮我写本周的"，只要上下文涉及 Web3、加密、融资、RWA、DAT，也应激活。
version: 2.1.0
tags:
  - web3
  - crypto
  - finance
  - newsletter
  - rwa
  - weekly-report
  - data-fetching
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins:
        - curl
        - python3
    files:
      - run_all.py
      - scripts/part3_fetch.py
      - scripts/part4_fetch.py
      - scripts/part5_fetch.py
      - scripts/part7_fetch.py
---

# Web3 行业资本运作周报采编 Skill（自动抓取版）

根据当前日期自动抓取各数据源，按固定栏目格式生成完整周报。对无法自动获取的数据，明确提示用户手动补充。

---

## 第一步：确定周报时间范围

运行前先确定本期周报的日期区间（通常为上周一至上周日）：

```python
from datetime import datetime, timedelta
today = datetime.today()
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday = last_monday + timedelta(days=6)
start_date = last_monday.strftime("%Y-%m-%d")
end_date = last_sunday.strftime("%Y-%m-%d")
print(f"本期周报覆盖：{start_date} 至 {end_date}")
```

若用户指定了日期区间，以用户指定为准。

---

## 数据源与可抓取性总览

| 模块 | 数据源 | 抓取方式 | 需要 Key |
|------|--------|----------|---------|
| Part.3 监管/行业 | 深潮 TechFlow RSS | curl + Python XML | 否 |
| Part.4 融资事件 | Rootdata（SSR HTML） | curl + HTMLParser | 否 |
| Part.5 DAT 动态 | CoinGecko 公开 API | curl + JSON | 否 |
| Part.6 并购 | 来自 Part.4（M&A 过滤） | 同 Part.4 | 否 |
| Part.7 RWA | PANews RWA 周刊 | 专栏页 + curl | 否 |
| Part.2 汇总 | 自动统计 Part.4 结果 | Python 计算 | — |
| Part.1 概览 | Part.3–6 内容 | AI 汇总生成 | — |

---

## 采编顺序

```
Part.3 → Part.4 → Part.5 → Part.6 → Part.7 → Part.2（汇总）→ Part.1（最后）
```

---

## Part.3 近期监管/行业事件

### 数据源

**主要来源：深潮 TechFlow 7x24h 快讯**
- RSS 接口：`https://www.techflowpost.com/api/client/common/rss.xml?page=N`
- 支持翻页（`page=1`、`page=2` 等），每页约 50 条
- 覆盖中英文加密媒体，包含中国大陆/香港监管动态，无需 API Key

### 筛选与排序规则

按以下顺序排列（每期 10–12 条，不超过 15 条）：

1. 中国大陆监管
2. 香港监管
3. 美国监管
4. 欧洲监管
5. 其他地区监管（日韩等发达国家优先）
6. 行业新闻（RWA 相关优先）

**进一步筛选原则：**
- 优先收录：监管动向、立法进展、执法行动、RWA 相关政策
- 一般不收录：虚拟货币犯罪案件、DAO 日常治理、普通技术升级
- 内容相近的多条新闻合并为一条呈现

---

## Part.4 主要融资事件

### 数据源

**主要来源：Rootdata Fundraising 页面**
- 地址：`https://www.rootdata.com/Fundraising`
- 标准 HTML 表格，7 列：`Project | Round | Amount | Valuation | Date | Source | Investors`
- 每页约 30 条，无需登录，无需 API Key
- 投资方中带 `*` 标记的为领投方

### 每个项目最终输出格式

```
[项目名称]
定位：一句话概括
轮次与金额：X 美元 X 轮融资
投资方：XX 领投；XX、XX 参投
点评：
  ① 项目背景与解决的问题
  ② 技术或产品特色
  ③ 本次融资目的与市场意义
```

---

## Part.5 上市公司 DAT 动态

### 数据源

**CoinGecko 公开免费 API（无需 Key）**
- BTC 持仓：`https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin`
- ETH 持仓：`https://api.coingecko.com/api/v3/companies/public_treasury/ethereum`
- **局限**：仅返回当前持仓快照，变动部分由脚本自动抓取 CoinGecko 详情页补充

### 每个条目最终输出格式

```
[公司名称]（国家）
股票代号：X（交易所）
动作：以约 X 美元购入/出售 X 枚 BTC/ETH
总持仓：X 枚（当前市值约 X 美元）
点评：（结合公司特征分析此次持仓变动意义）
```

---

## Part.6 并购交易情况

并购数据直接从 Part.4 的 Rootdata 解析结果中提取，筛选条件：`round == 'M&A'`。

### 每个条目输出格式

```
[收购方] 收购 [标的]
收购方：X（一句话概括）
标的：Y（一句话概括）
分析：
  ① 被收购方做什么，解决什么问题
  ② 收购方战略布局
  ③ 这笔并购的市场意义
```

---

## Part.7 RWA 项目动态

### 数据源

**PANews RWA 周刊**（每周约周四发布）
- 文章 URL 格式：`https://www.panewslab.com/en/articles/{uuid}`
- 通过专栏页自动获取最新期 URL，无需搜索引擎
- 只收录「Institutional & Project Activity」或「项目进展」部分
- 排除稳定币相关内容

### 每个条目最终输出格式

```
[项目名]
详情：
  ① 项目是什么，解决什么问题
  ② 近期具体动态与数据
```

---

## Part.2 关键数据速览（汇总）

Part.3–Part.7 完成后自动统计并填入：

```
融资项目数     X 件
总融资额       约 X 美元
DAT 变动       X 家机构有变动 / 本周暂无检测到变动
并购交易       X 起
```

---

## Part.1 近期概览（最后撰写）

所有模块完成后生成，150-200字，依次覆盖：融资亮点 → 并购动态 → DAT 趋势 → 监管要点。

---

## 快速开始

### 一键生成（推荐）

```bash
# 自动计算上周日期区间，生成完整周报骨架
python3 run_all.py

# 指定周起始日期
python3 run_all.py --week 2026-03-17

# 指定 PANews RWA 周刊文章 URL（跳过专栏页自动查找）
python3 run_all.py --rwa-url https://www.panewslab.com/en/articles/xxx

# 指定输出文件路径
python3 run_all.py --output weekly_20260325.md
```

脚本完成后，**立即使用以下固定 prompt 对骨架报告进行 AI 补全**，无需用户手动触发，群聊和私聊均适用：

---

```
你是资深 Web3 行业分析师。以下是本周资本运作周报的数据骨架，请补全所有标注 ⚠️ 的字段。

规则：
- Part.1：150-200字整体概述，依次点出本周最大融资、并购亮点、DAT 动态、监管趋势
- Part.3：每条新闻在标题后补充 1-2 句背景解读（不改动原标题）
- Part.4 定位：一句话说明赛道和核心产品
- Part.4 点评：三层结构，每层一句：①项目背景 ②技术/产品特色 ③本次融资意义
- Part.5 动作：根据变动摘要生成；若无变动写「本周维持持仓，暂无新增操作」
- Part.5 点评：结合公司特征和动作分析持仓变动意义
- Part.6 分析：三层结构，每层一句：①收购标的价值 ②收购方战略意图 ③市场意义
- Part.7 详情：补充项目背景和近期具体数据

不要修改任何已有的数据字段（金额、日期、投资方等），只填写 ⚠️ 标注的位置。
不要编造数据或估值。
```

---

### 单独运行各模块

```bash
python3 scripts/part3_fetch.py          # 监管/行业新闻
python3 scripts/part4_fetch.py          # 融资 + 并购
python3 scripts/part5_fetch.py          # DAT 持仓快照
python3 scripts/part7_fetch.py          # RWA 项目动态
python3 scripts/part7_fetch.py <URL>    # 指定文章 URL
```

---

## 执行流程

```
1. 确定日期区间（自动计算或用户指定）
2. 运行 python3 run_all.py，并行抓取所有模块
3. 输出各模块数据骨架，⚠️ 字段标注待补全位置
4. 用户补充缺失数据（如有）
5. 【必须执行】将完整骨架报告连同上方固定补全 prompt 一起传给 AI，
   完成所有 ⚠️ 字段补全后输出最终报告
```

> ⚠️ 第 5 步是必须步骤，不可省略。群聊和私聊均需执行，否则输出的是未补全的骨架，不是完整周报。

所有点评基于公开可查证信息生成，不编造数据或估值。
