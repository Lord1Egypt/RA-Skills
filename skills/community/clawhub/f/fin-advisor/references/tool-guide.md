# 工具使用参考

本文档列出你可以使用的所有 MCP 工具。根据用户问题的实际需要，自主选择调用哪些工具。不需要的工具不调，简单问题可能只需调用一个工具。

## 调用方式

通过 `mcporter call` 命令调用 MCP 工具，使用 `key:value` 格式传参，添加 `--output json` 获取 JSON 格式输出：

```bash
mcporter call <服务名>.<工具名> <参数名>:"<参数值>" --output json
```

### 调用示例

```bash
# 查询基金基本信息（支持基金代码、简称或全称）
mcporter call fund-diagnosis.fundIntro fundObject:"富国新兴产业" --output json

# 查询基金阶段业绩
mcporter call fund-diagnosis.fundStagePerformance fundObject:"001048" --output json

# 条件筛选基金
mcporter call fund-investments.conditionSelectFund condition:"医药板块近一年收益率前10" --output json

# 搜索财经新闻
mcporter call public-opinion-explanation.queryPublicOpinionNews keyWords:"降息" --output json

# 兜底搜索
mcporter call ai-search-all.all_search query:"富国新兴产业基金最新情况" --output json
```

### 注意事项
- 大多数工具通过 `fundObject` 参数接收基金标识，支持基金代码、简称或全称
- `buyerInvestmentAdvisor` 的参数名为 `scene`（基金全称），不是 `fundObject`
- 如果对话中存在指代（"这只基金"、"上面那个"），先消解为具体的基金名称再传入
- 参数值包含空格或特殊字符时用双引号包裹

---

## 基金诊断工具（fund-diagnosis）

| 工具名 | 能力说明 | 使用建议 |
|--------|---------|---------|
| `fundIntro` | 基金基本信息：类型、规模、成立时间、基金经理、风险等级 | 几乎所有场景的基础工具，优先考虑调用 |
| `fundPlate` | 基金板块标签（申万行业、概念等） | 需要了解基金所属板块/行业时 |
| `fundRateReport` | 完整费率报告：申购费、赎回费、管理费等费率阶梯 | 用户问费率、费用、手续费时 |
| `fundComment` | 一句话评价（盈利能力、抗跌能力、投资性价比） | 需要快速概括性评价时 |
| `fundscore` | 综合评分（0-100），含盈利、风控、选股、择时等维度 | 评估基金整体质量、做交易决策参考时 |
| `fundRiskEvaluation` | 风险评估指标（贝塔、阿尔法、夏普比率、最大回撤及同类排名） | 分析基金风险特征时 |
| `fundStagePerformance` | 阶段业绩（近 1 月/3 月/6 月/1 年/3 年等收益率） | 分析基金历史收益表现时 |
| `fundnettrendreport` | 净值走势数据（指定时间区间的逐日净值和收益率） | 分析基金历史净值变化趋势时 |
| `fundShareHoldingAna` | 持股风格分析（大盘/中盘/小盘，市盈率、市净率、持股集中度） | 分析基金投资风格、持仓偏好时 |
| `fundAssetAllocation` | 资产配置比例（股票/债券/基金/现金占比） | 分析基金资产结构时 |
| `fundIndustryAllocation` | 行业配置分布（申万一级行业持仓占比） | 分析行业集中度、板块暴露时 |
| `fundCompare` | 两只基金横向对比（基本信息、收益、回撤等） | 用户要求对比两只基金时 |
| `fundKeyShareHoldingDetail` | 前10大重仓股明细（股票代码、名称、持仓比例） | 分析基金具体持仓时 |
| `fundTopTenHolderDetail` | 前10大持有人明细（持有份额、持有比例） | 了解基金持有人结构时 |
| `fundReturnWithFrame` | 基金收益归因解读（近一月涨跌及关联板块分析） | 分析基金近期表现原因时 |
| `getCurTime` | 获取当前日期时间 | 需要知道当前日期时（模型自身不知道实时日期） |

## 基金投资工具（fund-investments）

| 工具名 | 能力说明 | 使用建议 |
|--------|---------|---------|
| `buyerInvestmentAdvisor` | 专业投顾建议：包含操作建议、市场分析、推荐理由。参数为 `scene`（基金全称） | 用户问"该不该买/卖"、无明确条件的基金推荐、交易决策场景 |
| `conditionSelectFund` | 条件筛选：根据板块、风险等级、投资风格等条件筛选基金 | 用户有明确筛选条件的推荐场景（如"推荐半导体板块的基金"、"有没有低风险的债基"） |

**使用规则：** `buyerInvestmentAdvisor` 和 `conditionSelectFund` 在同一次回答中只选其一：
- 有具体条件（板块、风格、风险等级等）→ 用 `conditionSelectFund`
- 无具体条件、泛泛地问推荐 → 用 `buyerInvestmentAdvisor`

## 舆情分析工具（public-opinion-explanation）

| 工具名 | 能力说明 | 使用建议 |
|--------|---------|---------|
| `queryPublicOpinionNews` | 金融新闻搜索：按关键字查询新闻资讯，返回标题、内容、来源 | 需要了解市场动态、行业新闻、基金相关舆情时 |
| `queryEventAnalysis` | 热点事件分析：查询事件解读，含影响板块、情绪方向 | 用户问到某个事件对基金的影响、需要分析市场热点时 |
| `top_daily_events` | 每日大事复盘（综合所有类型的重点焦点大事） | 用户问"今天市场有什么大事"时 |
| `top_macro_events` | 每日宏观要闻复盘 | 用户关注宏观经济动态时 |
| `top_industry_events` | 每日行业要闻复盘 | 用户关注特定行业动态时 |
| `top_company_events` | 每日公司大事复盘 | 用户关注公司层面事件时 |
| `top_global_events` | 每日海外大事复盘 | 用户关注海外市场动态时 |

## 通用搜索工具（ai-search-all）

| 工具名 | 能力说明 | 使用建议 |
|--------|---------|---------|
| `all_search` | 全网搜索（融合百度、Google 等），支持通识百科、新闻资讯、行业数据 | **兜底工具**：仅在上述专业工具无法满足需求、或多个工具调用失败时使用 |
