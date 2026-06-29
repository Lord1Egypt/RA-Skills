---
name: deep-investment-research
description: "系统化投研能力中枢。覆盖宏观/行业/政策/个股/投资可行性/风险/投资规划七类研究，内置9条研究红线、深度研究5步法、7专题框架（每类型含专属独门分析方法）、6研究模板（分析引导器结构：独门分析方法层+材料分析示范）、8重点行业一手源清单，以及多源数据采集脚本（SEC EDGAR/HKEX/AKShare/FRED/政策门户等）。Use for: 任何投资研究、行业分析、公司研究、个股深度研究、政策解读、可行性评估、风险分析、投资规划，以及研究所需的真实一手数据采集。纯研究，不做盯盘/交易信号/交易执行。"
license: MIT
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins:
        - python3
---

# deep-investment-research — 系统化投研能力中枢

> 一套可复用的投研方法论 + 多源一手数据采集工具。OpenClaw 提供运行时（gateway/cron/工具），本 skill 提供投研方法论+数据采集能力。
> 本 skill 只承载「研究能力」；调用方的身份/人格/记忆由各自 workspace 提供，不在本 skill 内。

## 环境约定（可选，均带默认值）
- `RESEARCH_OUTPUT_DIR`：研究报告归档目录，默认 `~/research-output`
- `RESEARCH_DATA_ROOT`：数据采集落盘目录，默认 `~/research-data`
- `SEARCH_SKILL_PATH`：联网搜索脚本路径，默认指向 web-search-plus（未安装则降级用内置 web_search 工具）
- 脚本内 API key 一律读环境变量（如 `FINNHUB_API_KEY`/`FRED_API_KEY`），未设置则跳过该数据源。

## 数据与隐私披露（安装前知情）
本 skill 是研究工具，会进行以下外部交互与本地写入——安装/使用即视为知情同意：
- **第三方数据传输**：研究主题/查询词会发送给外部搜索与数据 API（Serper/Tavily/Finnhub/FRED/SEC EDGAR/HKEX/政府门户等）以获取一手资料。**不要在涉及保密持仓、未公开自营研究主题时使用，除非可接受向这些第三方披露查询内容。**
- **读取环境变量**：仅读取数据源 API key（`FINNHUB_API_KEY`/`FRED_API_KEY` 等）用于调用对应数据源，不外传 key 本身、不读取其它环境变量。
- **本地落盘**：研究报告写入 `RESEARCH_OUTPUT_DIR`（默认 `~/research-output`），采集数据写入 `RESEARCH_DATA_ROOT`（默认 `~/research-data`）。文件写入预测路径，使用前确认目录无敏感数据冲突。
- **网络抓取**：方法论会对搜索发现的 URL 做全文抓取（web_fetch）。少数官方站点（国资委/人民网/openinsider）仅支持明文 http（其 https 不可达），已在代码注释标明；其余已统一走 https。
- **最小权限**：脚本以列表参数调用子进程（无 shell=True、无 eval/exec/动态 import），不执行任意命令。

## 何时触发
- 任何投资研究请求：宏观/行业/政策/个股/可行性/风险/规划
- 需要真实一手数据（财报/公告/政策原文/宏观/机构动向/一致性预期）
- 用户点题某行业/标的/主题/政策

## 九条研究红线（地基，贯穿全部）
1 深度·价值·前瞻 ｜ 2 数据真实不杜撰 ｜ 3 全文阅读不停留表面 ｜ 4 结论质量门控不说空话 ｜ 5 第一性原理广收集深研究 ｜ 6 紧扣目标不偏离 ｜ 7 prompt最佳实践榨干模型 ｜ 8 客观准确不主观 ｜ 9 未充分调研不下结论

## 怎么用（任何研究先走这里）

### Step 1 — 读内核（所有研究通用）+ 看近期产物
先读 `${RESEARCH_OUTPUT_DIR:-~/research-output}/<行业>/` 最近 2-3 篇同领域研究作背景（有则读，注意时效；无则跳过），再读：
- `methodology/research-core.md` — 9红线 + **研究设计+七棱镜多维扫描（强制前置：反千篇一律+反单维度）** + 深度研究5步法(A→B→C→D) + 反证5问 + 结论质量门控
  > 任何研究动笔前先做：①诊断对象核心矛盾、设计本次研究重心（贴合实际不套模板）②过七棱镜（宏观/政策/地缘/产业链/资金面/新闻情绪/标的自身），相关维度深挖、不相关明说为何忽略
- `methodology/source-registry.md` — 8行业权威一手源清单 + 搜索工具优先级
- `methodology/content-reading-protocol.md` — 全文阅读硬门控 + 读取量 + 来源回溯

### Step 2 — 按课题类型读对应框架+模板
| 课题 | 框架 | 模板 |
|------|------|------|
| 行业深度研究 | methodology/industry-research.md | templates/01 |
| 公司研究（看懂生意本身） | methodology/company-research.md | templates/06 |
| 个股深度研究（投资判断） | methodology/stock-deep-dive.md | templates/02 |
| 投资可行性分析 | methodology/feasibility-analysis.md | templates/03 |
| 政策研究与追踪 | methodology/policy-research.md | templates/04 |
| 风险分析 | methodology/risk-analysis.md | templates/05 |
| 投资规划 | methodology/investment-planning.md | — |
| 宏观研究 | methodology/{china-macro,us-macro}.md | — |

### Step 3 — 取真实一手数据（红线2/5）
**优先级：一手原文/官方数据/API > 定向爬虫 > 搜索引擎兜底。** 各行业权威源见 source-registry.md。

```bash
SK={baseDir}/scripts
python3 $SK/policy_gov_fetcher.py        # 政策原文
python3 $SK/ministry_scanner.py          # 部委政策扫描
python3 $SK/edgar_filings.py             # 美股财报/8-K/13F
python3 $SK/hkex_announcements.py        # 港股公告
python3 $SK/china_macro.py               # 中国宏观(AKShare)
python3 $SK/macro_snapshot.py            # 市场宏观快照
python3 $SK/analyst_consensus.py         # 一致性预期
python3 $SK/analyst_revision.py          # 预期修正
python3 $SK/earnings_surprise.py         # 业绩beat/miss
python3 $SK/superinvestor_moves.py       # 机构大师持仓
python3 $SK/sec_13f.py / insider_transactions.py / short_interest.py / southbound_top10.py / transcripts.py
python3 $SK/data_daily.py --tags morning # 批量采集
```
数据落盘 `${RESEARCH_DATA_ROOT:-~/research-data}/data/daily/{date}/`（由 RESEARCH_DATA_ROOT 环境变量控制）。

### 搜索（找线索，不出结论）
**优先用专用搜索 skill（Serper/Tavily，覆盖好、可控）；未安装时降级用内置 `web_search` 工具兜底。** 结论靠 web_fetch/pdf 读全文，搜索只找线索。
```bash
# 若已安装 web-search-plus（路径可用 SEARCH_SKILL_PATH 覆盖）：
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "查询" --provider serper --max-results 5
# 若已安装 tavily-search：
node ~/.openclaw/skills/tavily-search/scripts/search.mjs "查询" --topic news
# 均未安装：直接用 OpenClaw 内置 web_search 工具
```

## 认知连续性（用研究产物，不用静态档案）
不预存任何静态行业档案——静态认知必然过时且锚定共识，违背找预期差的本质。认知连续性靠研究产物库实现（见上）。
连续性靠**研究产物库**实现：做某行业/标的研究前，先看 `${RESEARCH_OUTPUT_DIR:-~/research-output}/<行业>/` 最近 2-3 篇研究（带日期、带一手数据、带来源），站在上次真实研究的肩上，而非模型存量记忆。
注意时效：产物只作背景与线索，"当前景气/估值/最新动态"一律用本次一手数据现取覆盖；过时结论只当"曾经的判断"参考，不当事实。

## 研究产物入库
报告写入 `${RESEARCH_OUTPUT_DIR:-~/research-output}/<行业>/YYYY-MM-DD-课题.md`。如需远程备份，由调用方的备份任务自行处理。

## 红线·边界
纯研究助理：不盯盘、不发买卖/止损信号、不做交易执行、不维护持仓。提供判断+依据+风险+可选路径，用户是最终决策者。
