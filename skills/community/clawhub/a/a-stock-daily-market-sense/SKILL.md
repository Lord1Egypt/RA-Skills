---
name: a-stock-daily-market-sense
description: 基于 Tushare Pro A 股日线与 Baostock 风格指数生成盘后市场研报。当用户要求分析每日或历史盘面、指数与市场风格、情绪和成交额集中度、赚钱效应与上涨主线、即时及短中期催化、主线细分线路、爆量下跌，或容量上涨、全市场月线平台突破、10:30 前涨停、折扣启动等特征分组时使用；也用于特征分组量化回溯与相对收益因子挖掘。本 skill 先生成确定性证据包，再由模型按模块判断与写作；脚本不调用 LLM，外部消息不得改变量价确定的主线星级，不套用现成行业/概念分类，不提供买卖建议。
---

# Tushare Daily Market Sense

## 目标

基于 Tushare 日线、指数、成交额与本地情绪历史，为 A 股盘后复盘生成结构化研报：盘面趋势、成交额集中度、赚钱效应与上涨主线、爆量下跌风险、特征分组分析。

不做单股基本面深度研究、港股/美股/基金/期货/加密分析、超短线交易决策、自动下单、组合优化或买卖建议。脚本只负责取数、计算、筛选、切分 JSON；主题归纳、风险措辞和研报写作由模型完成。

## 核心理念

成交额优先。所有强弱判断都要有成交额证据：上涨主线按成交额厚度确认，爆量下跌按放量异常与跌幅强度识别，特征分组按命中规则与成交额证据分开呈现。

主题主线由模型基于业务事实临时归纳，不套现成行业或概念标签。共同性不足时明确写“暂不构成主线”或“资金轮动”。

## 工作流程

1. 确定交易日：解析“今天/最近”或具体日期，默认只使用 `D` 及以前数据；只有用户明确要求后验时才允许 `--allow-future`。
2. 生成证据包：运行 `scripts/run_daily_panel.py`。脚本会直接调用数据管线，写出完整 evidence、个股 K 线展示数据（`kline_YYYYMMDD.json`）和模块级 JSON。
3. 生成首轮模块产物：模块 1、2、4、5 继续各自只读自己的 JSON、方法论与模板。模块 3 首轮只根据 `module3_money_effect.json` 归纳临时主题、父主题成员与候选细分成员，先写 `stars: null` 的 `module3_theme_map.json`；不要搜索，也不要在统计前凭手算锁星。有 subagent 时分发最小上下文，没有时按相同边界顺序执行。
4. 统计并锁定模块 3 星级：运行 `theme_group_stats.py` 生成 `module3_theme_stats.json`，再由模型严格按 Market Evidence Pack 与统计结果写回 `stars: 1/2/3`。星级锁定后，只对当日 ★★/★★★ 主线强制尝试搜索，并按宿主能力选读知识库或产业链资料；★ 级方向不搜索、不做产业推演、不进入 3.2。主 agent 将 Web 结果、可选的宿主知识证据与查询错误压缩成 `module3_enrichment_pack.json`。外部资料只用于解释催化、推演产业变量与挖掘细分线路，绝不回写或上调 3.1 星级。详细搜索、证据和评级纪律见 `references/methodology/catalyst_subline_mining.md`。
5. 聚合成稿：模块 3 第二阶段只读取 theme map、统计结果、enrichment pack、方法论与模板，完成 3.1 主线判定、3.2 催化与细分线路推演、3.3 领导股与弹性股。主 agent 再读取模块 1-5 输出、`assembled_checks.json` 与 `references/methodology/output_discipline.md`，补一句话盘面判断、风险传导提示和最终语气校准。搜索或知识查询失败不阻断日报，但要披露证据缺口并降低产业推演确定性。
6. 主线生命周期落库：报告定稿后，把当日 3.1 主线判定沉淀进 PG 生命周期台账。先运行 `python3 scripts/theme_lifecycle.py context --asof YYYYMMDD` 取注册表、各主线近期状态与 watchlist；模型完成别名归一（当日临时主题名 → canonical theme_id）和生命周期状态判定（低位启动/在场候选/主线确认/高位分歧/退潮/修复/再聚焦/沉寂），写出 `reports/lifecycle_YYYYMMDD.json` 后运行 `python3 scripts/theme_lifecycle.py record --input reports/lifecycle_YYYYMMDD.json` 落库。脚本只做确定性校验（枚举、状态机转移合法性、theme_id 存在性），判断留给模型；输入格式、状态机与判定基准见 `references/theme_lifecycle.md`。
7. 按需生成 HTML：当用户要求 HTML、网页、可视化报告或截图风格输出时，先完成并核对 `reports/report_YYYYMMDD.md`，再运行 `scripts/render_report_html.py` 生成同日期 HTML。HTML 是展示层产物，不新增研报判断、不删减 Markdown 正文；若同目录存在 `evidence_YYYYMMDD_utf8.json` 与 `kline_YYYYMMDD.json`，HTML 会自动读取指数 120 日 K 线与个股 K 线并插入对应正文附近；其中 5.2 全市场月线平台突破组改画**月线 K 线图**（多年底部箱体阴影 + 箱体上沿 pivot 水平线 + 突破月标记，数据来自 `kline_YYYYMMDD.json` 的 `monthly` 段），其余分组仍为 120 日日线。若 `theme_daily_state` 已有该日数据，HTML 还会在主线判定小节下方自动注入主线生命周期泳道图区块（近 22 个交易日，红 = 强势在场、绿 = 退潮、闪电 = 低位启动；`--lifecycle-days` 调窗口、`--no-lifecycle` 关闭）；区块只展示台账已落库数据，不新增判断。若 evidence 含风格序列，HTML 会在「市场风格」小节表格下方自动注入两张 60 日归一化对比图（规模轴五线 / 成长价值红利三线，起点=100），区块只展示 evidence 已有数据、不新增判断。
8. 证据包边界：`reports/evidence_YYYYMMDD_utf8.json` 是本 skill 的 Market Evidence Pack，只属于 skill 输出目录。即使宿主把最终趋势复盘写入其他知识系统，也不要把该证据包复制或登记成宿主原始来源；宿主知识查询只以可选 evidence pack 输入，不成为 core skill 的路径依赖。生命周期台账同理：它是 skill 域运行时数据，归 PG 管。
9. 清理临时产物：确认 `reports/report_YYYYMMDD.md`（及按需生成的 HTML）已写入并可读后，运行一条确定性清理命令，不要手工逐个删文件：

   ```bash
   python3 scripts/run_daily_panel.py --cleanup YYYYMMDD
   ```

   该命令删除同日期的 evidence、kline、stderr 日志、lifecycle 输入、report_context 与 module_context 目录，永远不会碰 `report_YYYYMMDD.md` / `report_YYYYMMDD.html`（生命周期数据已持久化在 PG，不受清理影响）。不要跨日期批量清理，除非用户明确要求。

## 特征因子挖掘（量化回溯 · 按需研究流程）

这是独立于每日日报的一条研究线：**你提一个特征分组，skill 在分组之上做额外因子挖掘，给出分组内的"叠加条件最优解"**。不进日报，想挖时才跑。完整方法论、基准表、spec 格式、最优解选择 rubric 见 `references/methodology/factor_mining.md`。

脑/手边界照旧：脚本 `scripts/factor_backtest.py` 只铺确定性证据（历史回放命中、6 格前向相对收益、因子分层、单/配对候选叠加条件 + 过拟合护栏标记），**不挑"最优解"、不下结论**；读证据、选叠加条件、写归因与 caveat 是模型的活。

流程（两处人工，其余自动）：

1. **你提分组**：内置组直接点名（如折扣启动）；新组用大白话给硬条件，模型译成 filter spec 给你确认。
2. **脚本回放 + 回测 + 铺网格**：
   ```bash
   # 内置折扣启动（多日序列组，复用生产函数，语义同线上）
   python3 scripts/factor_backtest.py --group discount_relaunch --min-n 15
   # 自定义单日特征阈值组（含容量上涨式），用 spec
   python3 scripts/factor_backtest.py --group custom --spec my_group.json
   ```
   产物：`reports/factor_mining_<group>_<asof>.json`（证据包，gitignore，跑完即临时）。
3. **模型选最优叠加解**：读 JSON，按 reference §四 rubric（稳健优先于大 Δ、看 `oos_balance` 与中位数胜率、深度≤2、经济逻辑）选定叠加条件，写 `reports/factor_mining_<group>_<asof>.md`。
4. **你决定要不要用**：把结果作为研究参考，或手动把叠加条件提级成分组生产阈值；脚本不替你改生产。

口径要点：进场 T+1 开盘/尾盘 × 持有 T+3/T+5/T+10，后复权；相对收益挂**板块/市值匹配基准**（科创→科创50、创业→创业板指、主板按市值→沪深300/中证500/中证1000），沪深300 作宽基对照。脚本默认会把信号窗口缺失的 `daily_basic` 从 Tushare 回补入库（需 `TUSHARE_TOKEN`）。折扣启动要完整 200 日历史，信号只落在数据最近端、样本偏小——所以护栏与诚实 caveat 是骨架，结论按"单一环境证据扫描、非统计定论"来写。挖矿证据分**决策包**（≤150KB，模型读：结论 + 每条过闸条件 ≤3 例证）与 `_detail.json`（整列 signals，按需读）；每次挖矿自动登记进 PG `factor_experiment_log`（可查、可判分，见下）。

需要回看已跑过的实验或补人工判定时，使用 `factor_lab.py experiments` 查询 PG `factor_experiment_log`。实验台账只记录挖矿参数、样本数、过闸数量、证据路径与人工 verdict，不进入每日日报。

## 数据获取

环境变量：

```bash
TUSHARE_TOKEN=your_token
ALPHA_DB_BACKEND=postgresql
ALPHA_PG_URL=postgresql://alpha_user:alpha_pass@/alpha_data?host=/tmp
TAVILY_API_KEY=your_token  # 催化搜索主路径；缺失时可由宿主 Web Search 降级
```

数据库连接统一走 `scripts/_shared/db_core.py`（开发仓库中为 `shared/data/db_core.py`）。首次进入任意 Agent 环境时先运行 `python3 scripts/_shared/db_ping.py --alpha-schema`；源仓库开发态用 `python3 ../../shared/data/db_ping.py --alpha-schema`。如果不能使用 Unix socket，再把 `ALPHA_PG_URL` 改为 `postgresql://alpha_user:alpha_pass@localhost:5432/alpha_data`。

运行脚本会先更新 `references/market_data.csv`，并同步维护派生文件 `references/market_data.json`，再生成情绪趋势：盘面情绪计数默认由 Tushare `daily` 直接计算，其中涨跌停数按**板制规则精确判定**——未复权前收盘 ×(1±板块限幅) 四舍五入到分后与收盘价比对（主板 10%、主板 ST 5%、创业/科创 20%、北交所 30%），口径为收盘封板、不含盘中炸板，`limit_detection` 字段标注判定方式；搜狐涨跌停历史页仅在主路径不可用时作为 fallback；Tushare `margin` 汇总 T-1 交易日融资净买入，Tushare `daily` 与 `daily_basic.circ_mv` 计算流通市值加权的全市场换手率。市场风格代理指数使用 Baostock `query_history_k_data_plus`，默认覆盖超大盘、沪深300、中证500、中证1000、国证2000、中证红利、300成长、300价值；历史数据缓存在 PG 的 `stock_index_daily` 表（以 bs_code 为 ts_code），每次运行只向 Baostock 增量取缺口，Baostock 不可用时直接用缓存窗口出摘要。个股日线、复权因子（`stock_adj_factor`）、daily_basic、交易日历同样全部缓存在 PG。因此环境中还需安装 `baostock`（`akshare` 为历史遗留可选依赖）。

基础命令（在 skill 根目录下执行）：

```bash
python3 scripts/run_daily_panel.py --asof 20260429 --lookback 120 --market-trend-days 90 --index 000300.SH
```

模块 3 首轮完成临时主题映射后，先用下列原子命令补充确定性统计；模型据此锁星后才运行搜索：

```bash
python3 scripts/theme_group_stats.py \
  --context reports/module_context_YYYYMMDD/module3_money_effect.json \
  --mapping reports/module_context_YYYYMMDD/module3_theme_map.json \
  --output reports/module_context_YYYYMMDD/module3_theme_stats.json
python3 scripts/web_search.py "主题 事件 YYYY-MM-DD" --topic news \
  --start-date YYYY-MM-DD --end-date YYYY-MM-DD --max-results 6
```

`theme_group_stats.py` 只统计模型已分组的成员；`web_search.py` 只返回结构化搜索结果。两者都不做主题、催化或产业强弱判断。

主要输出：

- `reports/evidence_YYYYMMDD_utf8.json`：完整证据包（紧凑 JSON，metadata 含 `stage_timings_seconds` 各阶段耗时与 `fetch_gaps` 各端点缺失交易日清单；任一端点缺日非空时必须在报告中显式说明）。
- `reports/kline_YYYYMMDD.json`：个股 K 线展示层数据，只供 HTML 渲染使用，模型撰写不读取。
- `reports/module_context_YYYYMMDD/`：供 subagent 分工的模块级 JSON。
- `references/market_data.json`：`market_data.csv` 的全量派生 JSON，按交易日升序保留所有列、清洗数值并提供 `series` 给 HTML 趋势图使用。

这些文件中，evidence、kline、lifecycle 输入和 module_context 是研报撰写过程中的临时产物。最终报告生成并核对后，按工作流程第 9 步用 `--cleanup` 一键删除，只保留 `reports/report_YYYYMMDD.md`、按需生成的 `reports/report_YYYYMMDD.html`，以及长期维护的 `references/market_data.csv` / `references/market_data.json`。

HTML 输出命令：

```bash
python3 scripts/render_report_html.py --input reports/report_20260429.md [--theme default|claude|print]
```

默认输出 `reports/report_20260429.html`，并将 `references/market_data.json` 内嵌到 HTML 中。本地浏览器可直接打开，图表不依赖外部 CDN。`--theme` 默认 `default`（AlphaVault 站点 / Google Material）；`--theme claude` 为 Claude.ai 暖色风格；`--theme print` 为黑白衬线、A4 友好，适合导出 PDF 或邮件附件。样式模板由仓库通用 `shared/html_report`（同步到 `scripts/_shared/html_report/`）提供，与 `a-stock-analyzer` 共用。

常用参数（赚钱效应/爆量/容量/折扣阈值、`--fetch-workers`、`--cleanup` 等）与
`factor_backtest.py` / `factor_lab.py` / `render_report_html.py` 的参数集中在 `references/cli_reference.md`。

## Subagent 编排契约

主 agent 先生成模块级 JSON，然后按下列最小上下文分发。每个 subagent 只看自己的模块数据，不读取其他模块数据。

| 模块 | JSON | 方法论 | 模板 |
|---|---|---|---|
| 1 盘面趋势 | `module1_market_trend.json` | `references/methodology/module1_trend.md` | `references/template/section1.md` |
| 2 集中度 | `module2_concentration.json` | `references/methodology/module2_concentration.md` | `references/template/section2.md` |
| 3 赚钱效应（首轮） | `module3_money_effect.json` | `references/methodology/module3_money_effect.md` | 先输出临时主题短名单与 `stars: null` 的 `module3_theme_map.json` |
| 4 爆量下跌 | `module4_decline.json` | `references/methodology/module4_decline.md` | `references/template/section4.md` |
| 5 特征分组 | `module5_feature_groups.json` | `references/methodology/module5_feature_groups.md` | `references/template/section5.md` |

模块 1、2、4、5 互不读取。模块 3 使用两阶段契约：首轮只做临时主题与成员映射；统计脚本完成后，由模型按量价 rubric 写回并锁定星级；第二阶段只读取已锁星的 `module3_theme_map.json`、`module3_theme_stats.json`、`module3_enrichment_pack.json`、模块 3 方法论和 `references/template/section3.md`，不回读其他模块的完整 JSON。Skill 只规定最小上下文边界，不规定 subagent 数量、并发槽位或模型。

聚合 agent 额外读取：

- `assembled_checks.json`：M3 赚钱效应池与 M4 爆量下跌池的确定性交叉检查。
- `references/methodology/output_discipline.md`：最终成稿纪律。

Python 不调用 Anthropic API、不调用任何 LLM、不硬编码模型名。Codex、Claude Code 或其他通用 agent 的 subagent 编排能力负责撰写；知识 evidence pack 是宿主可选输入，不在 core skill 中硬编码知识库路径或图谱实现。

## 输出规范

完整研报按五个模块输出。每个判断段先给自然语言结论，再选择少量关键证据支撑；表格承载细项数据，段落解释这些数据意味着进攻、分歧、退潮、修复、拥挤还是扩散。所有强弱判断都要能回到成交额、放量倍数、涨跌幅、相对收益或回撤证据，但不要把所有可用指标塞进同一段。模块 3 的主题分组只作为内部推理步骤，不输出单独的主题分组陈列表，赚钱效应总览后直接进入主线判定。

**文风默认（项目级硬性要求）：**

- **文风讲人话，减少机械与僵硬。** 像跟懂行的人当面把一件事讲清楚那样写，句子通顺、有逻辑衔接，该解释因果和给判断时把话说透。避免模板腔、翻译腔和套话——别成段堆砌"综上所述""值得注意的是""总体来看"，别把每条都写成生硬的"主语+动词+宾语"公式句，也别为了凑结构把话说断、只丢关键词。
- **同项罗列优先用 list，但每条要说人话。** 同一维度的多个条目（多个信号、多只个股观察点、多项风险传导）拆成 bullet 或编号，一条一项，别塞进一个长段落；但每条用完整通顺的话写，不要退化成"字段A - 字段B - 字段C"式的横杠拼接。结构化对照（指标 × 数值、分组 × 判定）才用表格。

文风目标：僵硬度约 5/10。报告应像一位有经验的盘后研究员在做复盘：先给人能立刻理解的盘面状态，再用少量关键数字支撑，最后给出下一交易日需要验证的条件。避免把所有可用指标都塞进段落；同一自然段最多放 2-3 个核心数字，其余数字放表格。

每个一级大章节（1-5）里已有的总结/定性段落必须使用 Markdown 高亮样式 `==...==` 包裹，例如“指数趋势判断”“市场风格判断”“盘面定性”“拥挤度判断”“主线 vs 资金轮动结论”“风险传导提示”“特征分组一句话判断”。不要为了高亮额外新增“本节总结”段落；高亮的是原本就承担总结作用的段落。

禁止输出买卖建议。可以写“风险传导”“持续性待验证”“主线确认度”，不要写“买入/卖出/止损/目标价”。

HTML 输出只改变呈现方式：必须保留 Markdown 研报中的所有文字、表格、引用和免责声明。`==...==` 高亮段落在 HTML 中渲染为浅蓝提示块；正文前可以增加 `market_data.json` 驱动的趋势图区域。若可读取同日期 evidence，HTML 可以在“指数趋势”正文附近插入上证指数、创业板指数、科创50 的 120 日 K 线图，并在图中展示成交金额柱；也可以在 3.3、5.2、5.3、5.4 股票明细表下方插入表内股票的 120 日 K 线图；若 evidence 含风格序列，还可以在“市场风格”表格下方插入两张 60 日归一化对比图（规模轴五线 / 成长价值红利三线，起点=100）。这些图表只展示 evidence 中已有的 OHLC、成交金额与风格指数收盘序列数据，不得新增与 Markdown 不一致的分析结论。

## 示例

用户：`复盘 2026-04-29 的 A 股盘面，重点看赚钱效应和容量上涨。`

执行：

```bash
python3 scripts/run_daily_panel.py --asof 20260429
```

然后按 subagent 契约加载 `reports/module_context_20260429/` 下的模块 JSON。若没有 subagent，就顺序加载每个模块的 JSON + 方法论 + 模板段，最后聚合为完整研报。
