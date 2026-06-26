---
name: ashare-analyzer
description: 生成A股综合分析报告（深交所/上交所/北交所），包含K线技术指标图表、同行业对比、基本面分析、主营业务构成、技术面评分、催化剂与风险、短线/中线买卖建议。当用户提供A股名称（如康盛股份）或代码（如002418、002418.SZ、sz002418）并要求分析、出报告、看技术面，或简单输入"002418"、"看看康盛股份"时触发。仅对A股触发，不对美股、港股、加密货币或无具体标的的大盘评论触发。
---

# A股综合分析器

根据A股名称或代码，生成包含两张图表的综合分析报告，严格遵循 `references/report_template.md` 中的锁定模板。

## 触发条件

- 股票名称：`康盛股份`、`贵州茅台`、`宁德时代`
- 任意格式代码：`002418`、`600519`、`002418.SZ`、`sz002418`、`SH600519`
- 口语化表达：`分析一下 002418`、`看看康盛股份`、`002418 怎么样`、`贵州茅台技术面`

如果名称有歧义，先询问用户确认后再继续。

## 数据架构

本 skill 使用多个专业数据源，每个领域选择最可靠的来源：

| 领域 | 主要来源 | 说明 |
|---|---|---|
| 价量K线（股票 + 沪深300 + 对比股） | 腾讯财经 | `web.ifzq.gtimg.cn` + `qt.gtimg.cn` — 无需认证，实时 |
| 同行业/同概念/题材 | 东方财富F10 `ssbk` + 板块成员 | 直连 `push2delay` API，规避 akshare 限流 |
| 基本面 | Fallback链：tushare → akshare → baostock → eastmoney | 来源透明，永不做静默回退 |
| 主营业务构成 | 东方财富 `RPT_F10_FN_MAINOP` | 按产品/行业/地区拆分 |

## 前置条件

- Python 依赖：`tushare`、`akshare`、`baostock`、`pandas`、`numpy`、`matplotlib`。安装：
  ```bash
  pip install tushare akshare baostock pandas numpy matplotlib -q
  ```
- **可选：** `TUSHARE_TOKEN` 环境变量 — 启用 tushare pro 作为基本面第一优先来源。未配置时自动降级到 akshare/baostock/eastmoney。
- 中文字体：Windows 自带 SimHei 和 Microsoft YaHei，图表脚本会自动注册可用的中文字体。

## 工作流（单路径，无分支）

### 第1步 — 解析输入

```bash
python scripts/resolve_code.py "康盛股份"   # 名称
python scripts/resolve_code.py 002418       # 代码
python scripts/resolve_code.py 002418.SZ    # 带后缀代码
python scripts/resolve_code.py sz002418     # 带前缀代码
```

返回 JSON，包含 `code6`、`ts_code`、`tencent_code`、`name`、`industry`。如果匹配到多个结果：`{"matches": [...]}` — 停下来让用户选择。

### 第2步 — 运行数据管线

```bash
python scripts/fetch_and_analyze.py "康盛股份" --outdir ./output
# （接受名称或代码 — 与 resolve_code.py 参数相同）
```

这一条命令完成全部数据采集：
1. 解析输入
2. 通过腾讯财经获取252天K线（股票 + 沪深300 + 4只对比股）
3. 获取实时行情（价格 / PE_TTM / PB / 总市值 / 换手率）
4. 从东方财富F10 `ssbk` 分类中选取3-4只对比股：
   - 1-2只来自行业板块（以Ⅰ/Ⅱ/Ⅲ结尾的）
   - 1-2只来自概念板块（液冷/算力/储能/新能源等或以"概念"结尾）
   - 补充自题材板块
5. 运行基本面 fallback 链（tushare → akshare → baostock → eastmoney）
6. 获取主营业务构成
7. 渲染K线图 → `kline_<code>.png`
8. 渲染对比图 → `compare_<code>.png`
9. 写入数据包 → `data_<code>.json`

**如果 `fundamental_used` 为 null 且 `needs_websearch` 为 true**，说明4层 fallback 全部失败；Claude 必须 `web_search` 补充缺失的基本面数据（ROE、利润率、最新财报），再填写报告。

### 第3步 — 生成叙述性分析 JSON

**⚠️ 执行前必读规则（不可跳过）：**
1. **先读模板理解字段含义** — 在生成 narrative JSON 之前，先 `Read` `references/report_template.md`，确认每个字段的名称和含义。
2. **逐字段对照** — 下方 JSON structure 是严格契约，字段名不得自创、不得遗漏、不得改名。输出时逐字段核对，确保与 JSON schema 完全一致。
3. **不跳步** — 严格按 workflow 顺序执行，不得省略任何步骤（特别是下方的 `web_search` 要求）。

读取 `data_<code>.json`，基于 Claude 判断生成叙述性分析 JSON 文件（`narrative_<code>.json`）。**不得编造数字** — 所有数字来自数据包，Claude 只负责叙述和判断类字段。**不得编造催化剂/风险** — 催化剂和风险必须基于 `web_search` 结果，不得凭通用行业知识编造。

**写 narrative 前必须 `web_search`（不可省略）：**
- 搜索 `<名称> 公告`、`<名称> 澄清`、`<名称> 减持`、`<名称> 利好`，覆盖最近30天
- 包含3-5条催化剂和3-5条风险，每条标注 高/中高/中/低 影响级别
- 技术面评分标准：参见 `references/technical_scoring.md`

**narrative JSON 结构**（保存为 `narrative_<code>.json`，放在 output 目录）：
```json
{
  "concepts": "3-5个最相关概念板块",
  "company_comment": "1-2句公司定性描述",
  "price_position": "当前价格位置描述",
  "business_comment": "业务结构评价",
  "region_summary": "按地区一句话概述",
  "tech_score": 3,
  "tech_verdict": "中性偏多",
  "tech_brief": "简评",
  "ma_verdict": "均线排列判断",
  "rsi_verdict": "RSI判断",
  "macd_verdict": "MACD判断",
  "bb_verdict": "布林带判断",
  "kdj_verdict": "KDJ判断",
  "vol_verdict": "成交量判断",
  "market_comment": "vs沪深300一句话点评",
  "peer_findings": ["发现1", "发现2", "发现3", "发现4"],
  "catalysts": [{"title":"标题", "impact":"高/中高/中/低", "desc":"描述"}],
  "risks": [{"title":"标题", "impact":"高/中高/中/低", "desc":"描述"}],
  "overall_judgment": "一句话整体判断",
  "short_term": {"tech":"...", "support":"支撑位", "resist":"阻力位", "advice":"操作建议", "stop_loss":"止损价"},
  "mid_term": {"drivers":"驱动力", "valuation":"估值判断", "support":"中期支撑", "advice":"建议", "target":"目标价", "scenarios":"乐观X/中性X/悲观X"},
  "stars": {"fundamental": 1-5, "concept": 1-5, "tech": 1-5, "timing": 1-5},
  "stars_comment": {"fundamental":"评价", "concept":"评价", "tech":"评价", "timing":"评价"},
  "one_liner": "一句话投资结论"
}
```

### 第4步 — 生成 HTML 报告

```bash
python scripts/generate_report.py --data ./output/data_<code>.json --narrative ./output/narrative_<code>.json --outdir ./output
```

生成独立的 `report_<code>.html`，包含：
- K线图和对比图以 Base64 内嵌
- 所有数据驱动的板块自动格式化（表格、KPI、数字）
- 内联 CSS 暗色主题，与图表风格一致
- 无外部依赖

### 第5步 — 呈现给用户

告知用户 HTML 报告已生成，路径为 `./output/report_<code>.html`，并询问是否在浏览器中打开。

## 边界范围

- **仅支持A股。** 港股/美股代码 → 拒绝并说明。
- **如果基本面 fallback 链返回 `needs_websearch: true`**，必须先 `web_search` 获取该股票最近财报数据，再填写财务板块。不得留空或使用占位文字。
- **如果股票停牌**（实时行情无近期数据）：报告停牌状态，跳过技术面评分，仅输出基本面报告。
- **如果对比股不足3只**，使用已有数据继续，并在对比板块标注"同行业数据有限"。

## 参考文件

- `references/report_template.md` — 报告模板（叙述内容的填写指南）
- `references/technical_scoring.md` — 10分制技术面评分标准
- `references/peer_selection_rules.md` — 对比股板块分类规则

## 脚本文件

```
scripts/
├── resolve_code.py           — 名称/代码 → ts_code / tencent_code（东方财富搜索 + 快照）
├── fetch_and_analyze.py      — 主管线（一条命令完成全部采集）
├── generate_report.py        — 数据JSON + 叙述JSON → 独立HTML报告
├── peer_selector.py          — 行业/概念/题材分类 + 代表性选股
├── fundamental_chain.py      — tushare → akshare → baostock → eastmoney fallback
├── plot_kline.py             — K线渲染（MA / BB / 成交量 / MACD / RSI）
├── plot_compare.py           — 归一化1年对比图
└── sources/
    ├── tencent.py            — K线 + 实时行情（无需认证）
    ├── eastmoney.py          — F10 ssbk、主营业务、板块成员、数据中心指标
    ├── akshare_src.py        — 个股信息、行业/概念查询、基本面
    ├── tushare_src.py        — tushare pro 基本面（优先级1）
    └── baostock_src.py       — 免费季报基本面（优先级3）
```
