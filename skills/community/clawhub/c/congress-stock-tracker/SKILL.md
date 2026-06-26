---
name: congress-stock-tracker
description: 国会山股神线索追踪工具。追踪美国国会议员最新股票交易动态，识别被多位议员集中买入的重仓标的，结合议员所在委员会和近期立法/监管动态，分析交易背后可能的政策事件催化剂，并检测大额交易、密集交易、跨党派共识等异常信号。当用户询问以下问题时使用本技能：(1) 国会议员最近买了什么股票 (2) 哪些股票被议员重仓买入 (3) 议员交易背后有什么政策线索 (4) 国会山股神/佩洛西等议员的持仓动态 (5) 分析国会交易异常信号
---

# 🏛️ 国会山股神线索追踪

追踪美国国会议员股票交易，挖掘重仓标的，分析政策线索。

## 工作流程

```
用户提问 → 判断查询类型 → 获取交易数据 → 分析处理 → 生成报告
```

1. **判断查询类型**：
   - **全景扫描**（"最近议员们买了什么"）→ 获取全量数据 + 重仓分析
   - **定向追踪**（"佩洛西最近的交易"）→ 按议员/标的筛选
   - **异常猎手**（"有什么异常交易"）→ 异常检测模式
   - **深度分析**（"为什么这么多人买 NVDA"）→ 事件关联分析

2. **获取数据**：运行 `scripts/fetch_trades.py`
3. **分析数据**：结合 `references/` 中的知识进行深度解读
4. **生成报告**：按模板输出结构化表格 + 分析解读

## 数据获取

运行数据抓取脚本获取最新交易记录：

```bash
# 基础用法：获取最近30天数据并执行分析
python scripts/fetch_trades.py --days 30 --analyze

# 筛选特定议员
python scripts/fetch_trades.py --politician "Pelosi" --analyze

# 筛选特定股票
python scripts/fetch_trades.py --ticker NVDA --analyze

# 筛选大额交易（>$100K）
python scripts/fetch_trades.py --min-amount 100000 --analyze

# 仅看参议院
python scripts/fetch_trades.py --chamber senate --analyze

# 保存结果到文件
python scripts/fetch_trades.py --analyze --output trades.json
python scripts/fetch_trades.py --output trades.csv
```

脚本输出 JSON 格式，包含：
- `trades`：筛选后的交易记录列表
- `concentration`：重仓标的排行（`--analyze` 模式）
- `anomalies`：异常交易信号（`--analyze` 模式）
- `meta`：查询元数据

**数据源优先级**：Capitol Trades → Quiver Quantitative API → 参议院官方披露

## 分析流程

### 重仓标的分析

拿到数据后，对被多位议员买入的标的进行深度分析：

1. 读取 `references/committee_industry_map.md`，查找买入议员所在委员会
2. 判断标的行业是否在委员会管辖范围内（高关联 = 更强信号）
3. 搜索近期相关立法、听证会、监管动态（使用联网搜索）
4. 按 `references/analysis_framework.md` 中的信号强度评估体系打分
5. 生成事件假设和展望

### 异常交易检测

脚本自动检测三类异常：
- 🔴 **大额交易**：单笔 ≥ $500K
- 🟡 **密集交易**：同一议员短期内对同一标的交易 ≥ 3 次
- 🔴 **跨党派共识**：两党 ≥ 3 位议员同时买入同一标的

### 事件关联分析

读取 `references/committee_industry_map.md` 获取委员会-行业映射，结合以下信息源进行关联：
- 议员委员会任职信息
- 近期国会立法日程
- 监管机构（FDA/FCC/EPA/SEC）近期动态
- 地缘政治事件

详细分析模板和评估框架见 `references/analysis_framework.md`。

## 输出要求

每次输出必须包含：

1. **交易总览表格**：议员、标的、买/卖、金额、日期、党派
2. **重仓排行**：被最多议员买入的标的排名
3. **深度分析**：Top 3-5 标的的事件关联解读
4. **异常警报**：检测到的异常交易信号
5. **⚖️ 免责声明**：必须提醒用户数据存在披露延迟（最长45天），分析仅供参考不构成投资建议

完整报告模板见 `references/analysis_framework.md` 的"输出报告结构"章节。

## 注意事项

- 国会议员交易披露存在 **最长 45 天延迟**，数据并非实时
- Capitol Trades 网站结构可能变化，如抓取失败会自动切换备用数据源
- 交易金额以范围形式披露（如 $1,001-$15,000），非精确数字
- 分析结论是基于公开数据的推测，不代表确定性事件
