# Financial Data Analyzer - 脚本使用指南

本指南说明 financial-data-analyzer 技能中各 Python 脚本的用法。所有路径中的 `{skillDir}` 会在加载技能时自动替换为实际路径。

---

## 执行流程（必须先采集再分析）

**⚠️ 正确顺序**：
1. **先获取准确时间**（date 或 python -c "from datetime import datetime; print(datetime.now())"）
2. 下载数据保存为 CSV（优先腾讯财经 API，参考 niuniu_dev/demo.py）
3. 基于 CSV 做指标计算
4. ⭐ 执行宏观经济数据采集与分析
5. ⭐ 采集全网时政热点（`fetch_trending.py`，13平台直采 + 按行业扩展 + 时效性检查）
6. （可选）执行专业估值分析（DCF/Comps/三表）
7. 生成内容丰富的 HTML 报告

1. **数据采集**：`fetch_stock_data.py` 将数据保存为 CSV
2. **指标计算**：`calculate_indicators.py`、`calculate_risk_metrics.py` 读取 CSV 进行计算
3. **时政热点采集**：通过 `fetch_trending.py` 脚本直接从 13 个平台公开接口采集热榜（基础7个 + 按行业扩展），保存为 `trending.json`，覆盖地缘政治/国家政策/央行活动/银行金融等广泛领域
4. **宏观分析**（必须）：`macro_analysis.py` 获取宏观经济数据和经济周期判断，可合并时政热点
5. **估值分析**（可选）：`calculate_valuation.py` 执行 DCF/Comps/三表分析
6. **报告生成**：`generate_html_report.py` 读取所有数据文件生成 HTML 报告

---

## 1. fetch_stock_data.py - 数据采集

将股票数据下载并保存为 CSV，供后续分析使用。

```bash
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol <股票代码> \
  --type <数据类型> \
  --output-dir <输出目录> \
  --format csv
```

**常用示例**：

```bash
# 实时行情
python {skillDir}/scripts/fetch_stock_data.py --symbol 600519.SH --type realtime --output-dir {OUTPUT_DIR}/financial_data/600519_SH --format csv

# 历史 K 线（3 年）
python {skillDir}/scripts/fetch_stock_data.py --symbol 600519.SH --type history --period 3y --output-dir {OUTPUT_DIR}/financial_data/600519_SH --format csv

# 港股（必须 5 位代码）
python {skillDir}/scripts/fetch_stock_data.py --symbol 00700.HK --type realtime --output-dir {OUTPUT_DIR}/financial_data/00700_HK --format csv
```

**数据类型**：`realtime` | `history` | `fundamental` | `financial` | `dividends` | `valuation`

**数据源**：realtime/history 必须参考 niuniu_dev/demo.py，使用腾讯财经 API 确保数据可靠性；fundamental/financial 等使用 yfinance

---

## 2. calculate_indicators.py - 技术指标

基于历史 CSV 计算 MA、MACD、RSI、BOLL、KDJ 等。

```bash
python {skillDir}/scripts/calculate_indicators.py \
  --input <历史数据CSV路径> \
  --output <输出CSV路径> \
  --indicator all
```

**示例**：

```bash
python {skillDir}/scripts/calculate_indicators.py \
  --input {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_history.csv \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_indicators.csv \
  --indicator all
```

---

## 3. calculate_risk_metrics.py - 风险指标

基于历史 CSV 计算波动率、最大回撤、夏普比率、VaR 等。

```bash
python {skillDir}/scripts/calculate_risk_metrics.py \
  --input <历史数据CSV路径> \
  --output <输出JSON路径> \
  --risk-free-rate 0.03
```

**示例**：

```bash
python {skillDir}/scripts/calculate_risk_metrics.py \
  --input {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_history.csv \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_risk_metrics.json \
  --risk-free-rate 0.03
```

**输出**：JSON 文件，包含累计收益率、年化波动率、最大回撤、夏普比率、VaR 等。

---

## 4. generate_html_report.py - HTML 报告

读取数据目录下的 CSV/JSON，生成带 ECharts 图表的可交互 HTML 报告。支持 4 种模板。

```bash
python {skillDir}/scripts/generate_html_report.py \
  --title '报告标题' \
  --template {stock|market|comprehensive|compare} \
  --data-dir <数据目录> \
  --output <输出HTML路径> \
  [--market-json <大盘数据JSON路径>] \
  [--stocks <逗号分隔的多股数据目录>] \
  [--valuation-json <估值分析JSON路径>] \
  [--comps-json <可比公司分析JSON路径>] \
  [--macro-json <宏观分析JSON路径>] \
  [--ai-analysis-json <AI综合分析JSON路径>] \
  [--ai-deep-analysis-json <AI深度分析JSON路径>]
```

**必填参数**：`--output`。`--title` 默认「投资分析报告」；`--template` 默认 `stock`；`--data-dir` 未指定时使用 `--output` 所在目录。

**模板参数**：
- `--template stock`：个股分析（默认）
- `--template market`：大盘总览（**需 --market-json**）
- `--template comprehensive`：综合研报（**需 --market-json**，可选 --data-dir）
- `--template compare`：多股对比（**需 --stocks**）

**新增参数**：
- `--market-json`：大盘数据 JSON（由 `market_review.py --format json --region all` 生成），`market`/`comprehensive` 模板必须传入
- `--stocks`：多股数据目录（逗号分隔，如 `dir1,dir2,dir3`），`compare` 模板使用

**可选参数**：
- `--valuation-json`：DCF 估值 / 三表分析 JSON（由 `calculate_valuation.py` 生成）
- `--comps-json`：可比公司分析 JSON（由 `calculate_valuation.py --mode comps` 生成）
- `--macro-json`：宏观经济分析 JSON（由 `macro_analysis.py --dashboard` 生成）
- `--ai-analysis-json`：AI 综合分析研判 JSON（核心结论、事件影响评估、新闻情报）
- `--ai-deep-analysis-json`：AI 深度分析 JSON（推理链路、多维分析）

**示例**：

```bash
# 个股分析（stock 模板）
python {skillDir}/scripts/generate_html_report.py \
  --title '贵州茅台(600519)投资分析报告' \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/贵州茅台投资分析报告.html \
  --macro-json {OUTPUT_DIR}/financial_data/macro_dashboard.json \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/ai_deep_analysis.json

# 大盘总览（market 模板）—— ⚠️ 必须先执行 market_review.py 生成 JSON
python {skillDir}/scripts/generate_html_report.py \
  --title '全球市场大盘总览' \
  --template market \
  --output {OUTPUT_DIR}/market_overview.html \
  --market-json {OUTPUT_DIR}/financial_data/market_review.json \
  --macro-json {OUTPUT_DIR}/financial_data/macro_dashboard.json \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/ai_deep_analysis.json

# 综合研报（comprehensive 模板）
python {skillDir}/scripts/generate_html_report.py \
  --title '全球市场综合研报' \
  --template comprehensive \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/comprehensive_report.html \
  --market-json {OUTPUT_DIR}/financial_data/market_review.json \
  --macro-json {OUTPUT_DIR}/financial_data/macro_dashboard.json \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/ai_deep_analysis.json

# 深度报告（专业分析模式使用，替换上面的基础命令，二选一）
python {skillDir}/scripts/generate_html_report.py \
  --title '贵州茅台(600519)深度投资分析报告' \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/贵州茅台深度分析报告.html \
  --valuation-json {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_valuation.json \
  --comps-json {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_comps.json \
  --macro-json {OUTPUT_DIR}/financial_data/macro_dashboard.json \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/ai_deep_analysis.json
```

**⚠️ 注意**：每次分析只执行其中一个命令，专业模式用深度报告命令**替换**基础报告命令，不要两个都执行。

**功能**：
- 自动从数据文件识别数据来源（腾讯财经 API / yfinance）
- 内置 ECharts K 线图（可缩放、悬停查看）
- 可选 `--valuation-json` / `--comps-json` 展示 DCF 估值、可比公司分析、三表财务分析
- 可选 `--macro-json` 展示宏观经济环境（经济周期、利率、通胀、PMI、资金流向）
- 可选 `--ai-analysis-json` 展示 AI 综合分析研判（核心结论、事件影响评估、新闻情报）
- 可选 `--ai-deep-analysis-json` 展示 AI 深度分析（推理链路、多维分析）；若不指定则从 `--ai-analysis-json` 中读取

**报告修改**：如果对生成的报告不满意，用 `read_file` 读取 HTML 后用 `replace_in_file` 直接修改，不要重新生成。

---

## 5. calculate_valuation.py - 专业估值分析

基于 yfinance 数据进行 DCF 估值、可比公司分析、三表财务分析。

```bash
python {skillDir}/scripts/calculate_valuation.py \
  --symbol <股票代码> \
  --data-dir <数据目录> \
  --output <输出JSON路径> \
  --mode <分析模式>
```

**分析模式**：
- `dcf`：DCF 估值（三场景 Bear/Base/Bull + WACC + 敏感性矩阵）
- `comps`：可比公司分析（peer 对比 + 统计基准 + 隐含估值）
- `statements`：三表财务分析（利润表/资产负债表/现金流 + 联动验证）
- `all`：执行全部模式（默认）

**可选参数**：
- `--risk-free-rate`：无风险利率（默认 0.03）
- `--projection-years`：预测期年数（默认 5）
- `--terminal-growth`：终值增长率（默认 0.03）
- `--erp`：股权风险溢价（默认 0.05）
- `--peers`：可比公司代码列表，逗号分隔（Comps 模式必须）

**示例**：

```bash
# DCF 估值
python {skillDir}/scripts/calculate_valuation.py \
  --symbol 600519.SH \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_valuation.json \
  --mode dcf

# 可比公司分析
python {skillDir}/scripts/calculate_valuation.py \
  --symbol 600519.SH \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_comps.json \
  --mode comps \
  --peers "000858.SZ,000568.SZ,603369.SH"

# 全部分析
python {skillDir}/scripts/calculate_valuation.py \
  --symbol 600519.SH \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_valuation.json \
  --mode all \
  --peers "000858.SZ,000568.SZ"
```

**输出**：JSON 文件，包含 dcf / comps / statements 三个顶级键。

---

## 6. macro_analysis.py - 宏观经济分析

获取中国宏观经济数据（LPR/CPI/PPI/PMI/社融/M2/GDP/社零/FAI/工业增加值/进出口/房地产/国债收益率），自动判断经济周期阶段（含过热/滞胀期），支持合并全球局势与政策新闻，支持整合 `fetch_trending.py` 采集的全网时政热点并自动分类为 13 个类别（不局限于金融相关），含时效性检查机制。

```bash
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  [--global-context-json <全球局势新闻JSON路径>] \
  [--trending-json <时政热点JSON路径>] \
  [--stock-name <股票名称>] \
  [--industry <行业>] \
  --output <输出JSON路径>
```

**分析模式**：
- `--dashboard`：完整宏观仪表盘（全部指标 + 经济周期判断 + 全球局势新闻 + 时政热点，**推荐**）
- `--rates`：利率数据（LPR 1Y/5Y、Shibor、10Y国债收益率、期限利差）
- `--inflation`：通胀数据（CPI、PPI 同比）
- `--pmi`：PMI 数据（制造业 / 非制造业）
- `--social-financing`：社融规模与 M2 增速
- `--growth`：经济增长数据（GDP/社零/FAI/工业增加值/进出口）
- `--real-estate`：房地产数据（开发投资/销售面积同比）
- `--cycle`：经济周期评估（综合多指标判断阶段，含过热/滞胀）
- `--global-queries`：生成国际事件 web_search 搜索指令

**可选参数**：
- `--global-context-json`：全球局势与政策新闻 JSON 路径（AI 通过 web_search 整理的地缘政治/国内政策/银行金融机构行为等新闻，合并到宏观仪表盘）
- `--trending-json`：`fetch_trending.py` 采集的时政热点 JSON 路径（由 `fetch_trending.py` 脚本采集后保存，自动分类为 13 个类别并检查时效性，**不局限于金融相关，覆盖地缘政治/国家政策/央行/银行金融/全球时事等**）
- `--stock-name`：关联的股票名称（用于定制国际化搜索和时政热点筛选）
- `--industry`：关联的行业（用于定制行业政策搜索和时政热点筛选）
- `--output`：输出 JSON 文件路径

**示例**：

```bash
# 完整宏观仪表盘（不含新闻和热点）
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  --output {OUTPUT_DIR}/financial_data/macro_dashboard.json

# 完整宏观仪表盘 + 全球局势新闻（推荐）
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  --global-context-json {OUTPUT_DIR}/financial_data/global_context.json \
  --output {OUTPUT_DIR}/financial_data/macro_dashboard.json

# 完整宏观仪表盘 + 全球局势新闻 + 时政热点（推荐，报告最丰富）
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  --global-context-json {OUTPUT_DIR}/financial_data/global_context.json \
  --trending-json {OUTPUT_DIR}/financial_data/trending.json \
  --stock-name "贵州茅台" \
  --industry "白酒" \
  --output {OUTPUT_DIR}/financial_data/macro_dashboard.json

# 仅经济周期评估
python {skillDir}/scripts/macro_analysis.py \
  --cycle \
  --output {OUTPUT_DIR}/financial_data/business_cycle.json

# 生成国际事件搜索指令（含行业定制）
python {skillDir}/scripts/macro_analysis.py \
  --global-queries \
  --stock-name "贵州茅台" \
  --industry "白酒"
```

**输出**：JSON 文件，包含 rates / inflation / pmi / social_financing / growth / real_estate / business_cycle / global_context / trending_classified 等顶级键。

**全球局势 JSON 格式**（`--global-context-json`）：
```json
{
  "geopolitical": "地缘政治事件摘要...",
  "us_china": "中美关系进展...",
  "fed": "美联储与全球央行政策...",
  "banking_institutions": "银行与金融机构动态（央行操作/商业银行/社保/险资/公募/外资）...",
  "domestic_policy": "国内政策（产业/监管/地方/财政）...",
  "tech_sanctions": "科技制裁与出口管制...",
  "global_markets": "全球市场走势...",
  "commodities": "大宗商品价格...",
  "forex": "汇率与资金流向..."
}
```

**时政热点 JSON 格式**（`--trending-json`）：
```json
{
  "sources": [
    {
      "source": "xueqiu",
      "source_name": "雪球财经",
      "items": [
        {"title": "央行宣布定向降准0.5个百分点", "hot": 1234567, "url": "https://..."},
        {"title": "贵州茅台发布2025年报", "hot": 987654, "url": "https://..."}
      ]
    },
    {
      "source": "toutiao",
      "source_name": "今日头条",
      "items": [
        {"title": "国务院常务会议：部署扩大内需措施", "hot": 876543, "url": "https://..."},
        {"title": "中东局势升级：以色列与伊朗互射导弹", "hot": 765432, "url": "https://..."}
      ]
    }
  ],
  "fetch_time": "2026-03-02T10:00:00"
}
```

> **说明**：`--trending-json` 传入后，脚本会调用 `classify_trending()` 对**所有热点**进行广覆盖分类（不再仅筛选金融相关），自动分为 13 个类别：company_related / industry_related / geopolitical / us_china / national_policy / central_bank / banking_finance / macro_economy / stock_market / commodities_forex / industry_tech / global_events / general，结果写入输出 JSON 的 `trending_classified` 字段。同时检查数据时效性（超过 48 小时标记警告）。

**依赖**：需要安装 `akshare`（`pip install akshare`），无需 API Key。`fetch_trending.py` 仅需 `requests` 库。

---

## 7. setup_dependencies.py - 依赖安装

首次使用前运行，安装 pandas、numpy、yfinance、requests、Jinja2 等依赖。

```bash
python {skillDir}/scripts/setup_dependencies.py
```

---

## 路径说明

- `{skillDir}`：技能目录，由系统自动替换
- `{OUTPUT_DIR}`：从 `<user_info>` 的 Output Directory 获取，用于保存数据和报告

---

## 常见问题

**Q: 计算风险指标报 KeyError: 0？**
A: 已修复。确保使用最新版 `calculate_risk_metrics.py`，且输入 CSV 包含 Date、Open、High、Low、Close、Volume 列。

**Q: 腾讯/港股数据获取失败？**
A: 先执行 `use_skill("financial-data-analyzer")` 加载技能，再执行 fetch 脚本。数据会保存为 CSV，后续分析均基于 CSV。

**Q: 报告没有图表？**
A: 确保数据目录中有 `*_history.csv`，报告脚本会自动生成 ECharts K 线图。
