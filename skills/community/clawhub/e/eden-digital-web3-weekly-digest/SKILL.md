---
name: web3-weekly-report
description: 自动抓取数据并生成 Web3 行业资本运作周报，涵盖融资事件、监管动态、上市公司 DAT 动态、并购交易与 RWA 项目追踪。当用户提到"写周报"、"生成周报"、"整理本周融资"、"Web3 周报"、"资本运作周报"、"采编周报"，或请求整理加密行业本周动态时，立即激活此 skill。即使用户只说"帮我写本周的"，只要上下文涉及 Web3、加密、融资、RWA、DAT，也应激活。
version: 2.0.0
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
    files: []
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

| 模块 | 数据源 | 抓取方式 | 是否需要 API Key |
|------|--------|----------|----------------|
| Part.3 监管/行业 | CoinDesk | web 搜索 + 抓取 | 否 |
| Part.4 融资事件 | Cryptorank 网页 | web 搜索 + 抓取 | 否（网页版） |
| Part.4 融资事件 | Rootdata | web 搜索 + 抓取 | 否 |
| Part.5 DAT 动态 | CoinGecko 公开 API | curl | 否（免费端点） |
| Part.6 并购 | Cryptorank / 搜索 | web 搜索 | 否 |
| Part.7 RWA | PANews RWA周刊 | 抓取网页 | 否 |

---

## 采编顺序

```
Part.3 → Part.4 → Part.5 → Part.6 → Part.7 → Part.2（汇总）→ Part.1（最后）
```

---

## Part.3 近期监管/行业事件

### 抓取方法

用 web 搜索抓取本周 CoinDesk 新闻，关键词组合：

```
site:coindesk.com regulation crypto [start_date]..[end_date]
Web3 crypto regulation news this week China Hong Kong US Europe [year]
site:coindesk.com RWA tokenization [start_date]..[end_date]
```

抓取后按以下顺序排列（每期 10–12 条，不超过 15 条）：

1. 中国大陆监管
2. 香港监管
3. 美国监管
4. 欧洲监管
5. 其他地区监管（日韩等优先）
6. 中国大陆/香港行业新闻（RWA 相关优先）
7. 其他地区行业新闻（RWA 相关优先）

筛选原则：优先监管动向、行业趋势、RWA；排除虚拟货币犯罪、DAO 日常活动、普通技术发布（除非重大事件）；内容相近的合并为一条。

### ⚠️ 需要手动补充
抓取完成后提示用户：
> 「Part.3 已从 CoinDesk 自动整理 X 条。如有来自世链大宗等国内公众号的新闻，请粘贴给我，我将按优先级插入。」

---

## Part.4 主要融资事件

### 抓取方法

**Step 1：web 搜索抓取 Cryptorank 和 Rootdata 融资数据**

```
crypto funding rounds week of [start_date] site:cryptorank.io
Web3 startup raised funding [start_date] [end_date] million
rootdata crypto investment [start_date]..[end_date]
```

**Step 2：补充抓取各重点项目详情**

对每个入选项目，搜索其官网或介绍页面，生成"定位"和"点评"。

### 统计与筛选

收集完成后统计：
- 融资项目总数 → 用于 Part.1 和 Part.2
- 总融资额 → 用于 Part.1 和 Part.2

筛选重点展示项目：

| 当周总数 | 展示数量 |
|---------|---------|
| ~10 余个 | 5 个 |
| 20 个以上 | 10 个 |

优先级：融资金额 > 机构知名度（a16z、Paradigm、Coinbase、阿里巴巴等头部机构参投即使金额小也纳入）

### 每个项目输出格式

```
[项目名称]
定位：（一句话）
轮次与金额：X 美元 X 轮融资
投资方：XX 领投，XX、XX 参投（中资机构使用中文名）
点评：
  ① 项目做什么，解决什么问题
  ② 技术亮点或产品特色
  ③ 本次融资目的或市场意义
```

### ⚠️ 需要手动补充
若 Cryptorank 搜索结果不完整，提示用户：
> 「已从搜索结果整理到 X 个融资项目，可能有遗漏。建议访问 https://cryptorank.io/funding-rounds 筛选本周数据后粘贴给我补全。」

---

## Part.5 上市公司 DAT 动态

### 抓取方法（CoinGecko 免费 API）

```bash
# 抓取 BTC 持仓上市公司列表（免费端点，无需 API Key）
curl -s "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin" \
  -H "Accept: application/json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('companies', [])[:20]:
    print(f\"{c['name']} | {c['symbol']} | {c['total_holdings']} BTC\")
"

# 抓取 ETH 持仓上市公司列表
curl -s "https://api.coingecko.com/api/v3/companies/public_treasury/ethereum" \
  -H "Accept: application/json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('companies', [])[:20]:
    print(f\"{c['name']} | {c['symbol']} | {c['total_holdings']} ETH\")
"
```

CoinGecko 免费 API 返回**当前持仓快照**，无法获取本周增减变化量。

### ⚠️ 需要手动补充
自动获取总持仓后，提示用户：
> 「已从 CoinGecko 获取以下公司当前持仓快照：[公司清单]。由于免费 API 不含周度变化数据，请补充本周各公司具体买入/卖出操作（可从各公司公告或 Coingecko 公司详情页获取），我来生成格式和点评。」

### 每个条目输出格式

```
[公司名称]
股票代号：X（交易所）
动作：以约 X 美元购入/出售 X 枚 BTC/ETH
总持仓：增加/减少至 X 枚 BTC/ETH
点评：（结合公司特征分析此次持仓变动意义）
```

---

## Part.6 并购交易情况

### 抓取方法

```
crypto M&A acquisition merger [start_date] [end_date]
Web3 blockchain company acquired this week [year]
site:theblock.co OR site:coindesk.com acquisition [start_date]
```

### 每个条目输出格式

```
[收购方] 收购 [标的]
收购方：X（一句话概括）
标的：Y（一句话概括）
分析：
  ① 被收购方做什么，解决什么问题
  ② 收购方做什么，战略布局
  ③ 这笔并购对收购方意味着什么
```

### ⚠️ 需要手动补充
> 「已找到 X 笔并购交易，如有遗漏请补充。」

---

## Part.7 RWA 项目动态

### 抓取方法

```
# 搜索 PANews 本周 RWA 周刊最新一期
site:panewslab.com RWA周刊 [year]
```

抓取最新一期文章，提取「项目进展」部分，筛选规则：
- 只收录实际落地或正在推进中的项目
- 排除稳定币相关项目

### 每个条目输出格式

```
[项目名]
详情：
  ① 项目是什么，解决什么问题
  ② 近期具体动态与数据
```

### ⚠️ 需要手动补充
> 「PANews RWA周刊本期链接无法访问，请提供本期链接或将「项目进展」部分粘贴给我。」

---

## Part.2 关键数据速览（汇总）

Part.3–Part.7 完成后自动统计：

```
融资项目数     X 件          ← Part.4 统计
总融资额       约 X 美元      ← Part.4 统计
DAT 变动       增持/减持约 X  ← Part.5（依赖手动数据）
并购交易       X 起          ← Part.6 统计
新设立基金     X 美元         ← Part.4（如有）
```

---

## Part.1 近期概览（最后撰写）

所有模块完成后生成：

```
X年X月X日至X月X日期间，共录得 Web3 行业 X 个项目完成融资，总融资金额超 X 美元。
其中，[从最大单笔开始，依次提及项目名及融资额，简述市场意义]。

在 DAT 方面，[一句话概括当周上市公司增减持趋势]。其中，[列出各公司具体动作]。

并购方面，[一句话概括趋势]。其中，[列出交易及意义]。

期间，其他值得关注的全球监管与行业新闻有：
[按 Part.3 顺序合并总结]
```

---

## 执行流程

```
1. 确定日期区间（自动计算或用户指定）
2. 并行抓取所有模块
3. 输出各模块内容，每模块末尾注明「⚠️ 需手动补充」项
4. 用户补充缺失数据
5. 汇总 Part.2 和 Part.1
```

所有点评基于公开可查证信息生成，不编造数据或估值。
