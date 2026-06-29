# weekly-industry-scan.md — 周级别行业投资分析（定时任务执行手册）

> 五个定时任务（周一~周五 11:00）共用本执行手册。每个任务只在 prompt 里指定【本周行业】，其余执行标准全在这里。
> 引用：research-core.md（9红线+5步法+反证+质量门控）、content-reading-protocol.md（全文阅读硬门控）、source-registry.md（8行业一手源）。

## 任务目标（一句话）
对【指定行业】做一份**周级别**投资分析：了解过去一周的行业动态，从中寻找**预期差投资机会**（不是复述新闻，是找"市场认知 vs 真实情况"的差）。覆盖**内地A股 + 港股 + 美股**三地标的。纯研究，不下交易指令。

## 五条硬要求（用户明确·逐条满足）
1. **数据有效期 = 最近一周**：只用过去 7 天内发布/发生的数据、公告、政策、价格、资金面。更早的只作背景，不作"本周动态"。每条动态标日期。
2. **目的 = 找预期差**：不是行业新闻汇编。每个值得说的动态都要过一遍"市场怎么看 vs 真实情况如何 vs 是否已price in"。没有预期差的动态简述带过，把篇幅给有预期差的。
3. **三地覆盖**：A股 + 港股 + 美股都要扫，列各自的关键标的与本周变化。哪个市场本周该行业是主线要点明。
4. **prompt最佳实践 / 榨干模型**：自顶向下、由表及里——先扫全行业本周发生了什么（表），再下钻到驱动因子、关键公司、数据细节（里），不停留在标题层。
5. **研究深度（红线3硬门控）**：禁止只读标题/摘要就下结论。每个进入结论的判断，必须基于 web_fetch/pdf 读到的正文段落 / 已解读的具体数值。搜索只用来找线索。

## 执行流程

### Step 0 — 读方法论（开工先读）
- {baseDir}/methodology/research-core.md
- {baseDir}/methodology/content-reading-protocol.md
- {baseDir}/methodology/source-registry.md（找到本行业那一节的一手源）
- 看 ${RESEARCH_OUTPUT_DIR:-~/research-output}/<本行业目录>/ 最近 2-3 篇研究作背景（注意时效，只作线索不作事实）

### Step 1 — 一手数据采集（最近一周）
SK={baseDir}/scripts
- 行情/资金/估值：exec + yfinance（A/H/美三地关键标的，取近一周价格、成交、估值）
- 港股：python3 $SK/southbound_top10.py（南向）、$SK/short_interest.py（沽空）、$SK/hkex_announcements.py（港股公告）
- 美股：$SK/edgar_filings.py（8-K/财报/13F）、$SK/earnings_surprise.py、$SK/analyst_revision.py（预期修正）
- 政策：$SK/policy_gov_fetcher.py、$SK/ministry_scanner.py（如本行业本周有政策）
- 行业一手源见 source-registry（如半导体看SIA/台积电月营收/BIS；AI看大厂capex；机器人看厂商发布/IFR；商业航天看FAA/FCC/发射；黄金看WGC/COMEX/GLD持仓/实际利率/地缘）
搜索默认 Serper（加 --type news 取本周新闻）：
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "查询" --provider serper --max-results 6 --type news
Tavily 备用：node ~/.openclaw/skills/tavily-search/scripts/search.mjs "查询" --topic news --deep（未安装搜索 skill 时降级用内置 web_search 工具）

### Step 2 — 全文读取（红线3）
对本周关键动态（财报/政策/重大事件/数据），用 web_fetch / pdf 读正文，提取：关键原文/具体数值/措辞信号变化。读不到全文的标信息盲区，不脑补。

### Step 3 — 自顶向下分析（先研究设计，再七棱镜扫描）
先做研究设计（见 research-core 一半章）：本周该行业最关键的矛盾/变量是什么→决定哪个棱镜是本周主战场（不千篇一律，有的周主线是政策、有的周是业绩、有的周是地缘）。
然后按三层展开，【七棱镜】逐个扫一遍（相关取数深挖、不相关一句话跳过）：
- 【七棱镜】①宏观(利率/汇率/景气周期) ②政策/监管 ③地缘政治 ④产业链上下游 ⑤资金面(南向/机构/沽空/预期修正) ⑥新闻/事件/情绪 ⑦行业/公司自身
- 表层：本周该行业三地发生了什么（按重要性排序，标日期+来源）
- 中层：驱动因子层面发生了什么变化（景气/政策/技术/资金/地缘）——用七棱镜交叉看
- 里层：下钻到 2-4 个最有预期差的点，做 A→B→C→D（事实→推断→定价检查→含义），写清"市场共识 vs 我的看法"
预期差常在棱镜交叉处（如基本面平但地缘催化被低估、景气升但政策风险被忽视）。

### Step 4 — 推送前过质量门控（research-core 第四节逐条）
有立场/有依据(具体数字)/有定价检查/有反方/有量化/有前瞻/有确信度与盲区/客观/充分调研/反共识/紧扣目标。

## 输出模板（最终回复＝成品，以第一个实义字符开始，无任何过程旁白/投递说明）

```
📊 【行业】周报 | <日期区间> | 一句话本周定调

## 本周三地动态速览（最近一周，标日期）
- A股：关键动态 + 标的 + 数据
- 港股：关键动态 + 标的 + 数据
- 美股：关键动态 + 标的 + 数据

## 预期差扫描（核心，2-4个）
每个：动态事实 → 市场共识 → 我的看法（哪里不同/为何没被price in）→ 含义与确信度
写不出预期差的周 → 老实说"本周无明显预期差，行业按既有逻辑演进"，并说明检查了什么。

## 关键数据/资金面
南向、沽空、预期修正、capex、行业景气指标等具体数值 + 环比/同比/vs共识。

## 风险与跟踪信号
本周新增的下行风险 + 下周要盯的催化剂/数据。

## 信息盲区
没查到/查不准/付费墙的，诚实标注。
```

## 入库
报告写入 ${RESEARCH_OUTPUT_DIR:-~/research-output}/<行业目录>/YYYY-MM-DD-周报-<行业>.md（mkdir -p 先建目录）。
行业目录：semiconductor / ai-fullchain / embodied-ai-robotics / commercial-space / gold（黄金+地缘放 gold/，地缘横向部分也可标注 macro-policy）。

## 红线提醒
- 效果优先于速度，不为省时间减量（用户明确）。
- 数据真实不杜撰，查不到标盲区。一手优先于二手。
- 搜索只找线索，结论靠全文。
- 最终回复只放成品，不调用 message 工具主动发送（投递由系统 announce 完成）。
