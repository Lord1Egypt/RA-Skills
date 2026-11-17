# 股票雷达 · A股选股 SOP（2026-09-24 正式命名 + 写死）

> 用户要求：**选股必须 10 个交易技能全部参与，各司其职、多源交叉验证，不能只靠一个技能。**
> 与「期货雷达」（`futures-sop.md`）并列：选股 = **股票雷达**。
> 🔒 **本规则已写死（2026-09-24 用户确认「写死，名字是股票雷达」）：**
> 1. **正式名称 =「股票雷达」**（不再叫「选股雷达」）。
> 2. 以后每次选股都要按本 SOP 跑全套 10 技能；逐项执行并汇报状态（跑了/取不到→已换源兜底/本次不适用及原因）；**不得为省事跳过任一技能。** trading-coach 只在用户提供券商交割单时进入（否则标注「待交割单」）。
> 3. **数据维度一并写死**：实时（全市场/板块主力资金 · 个股逐笔大单 · 竞价 · 行情）+ 盘后（龙虎榜席位 · 涨停质量 · 板块接力 · 公告排雷）+ 历史（资金趋势 · 30min结构 · 形态回测）+ 闭环（仓位 · 止损/卖点 · 交割单复盘）。

## 🚀 一键执行（推荐）

```bash
# 阶段1-6（无需候选）：环境 + 全市场扫描 + 第二引擎 + 第二名单 + 多源复核
bash skills/trading-desk/scripts/radar_run.sh

# 全链（带候选代码）：再加 形态风险 / 资金趋势 / 分时量能 / 深研快照
bash skills/trading-desk/scripts/radar_run.sh 002487 603667 601218

# 复跑（跳过基础扫描，只跑需候选的 7~9）
RADAR_SKIP_BASE=1 bash skills/trading-desk/scripts/radar_run.sh <code...>
```
- 原始输出：`/tmp/openclaw/radar/<时间戳>/`；终端打印**参与状态汇总表**（✅跑了/🟡换源兜底/⬜待输入/❌失败）。
- 逐项清单与命令速查：**`references/stock-radar-checklist.md`**（所选/回报用）。

## 十个技能的角色分工（缺一不可，取不到数据要如实说）

| # | 技能 | 角色 | 具体动作 |
|---|---|---|---|
| 0 | **trading-sop** | 总编排 | 意图路由 + 串联全链 + 汇总输出 |
| 1 | **trading-desk** | ①主引擎 | `emotion.py`（环境）+ `ashare_screen.py scan`（全市场）+ `money_flow.py`（资金）+ `risk_flags.py`（形态）|
| 2 | **a-share-short-decision** | ②第二引擎 | `main.py short_term_signal_engine --date <D>` 独立评分 → 与主引擎**取交集/并列** |
| 3 | **market-price** | ③实时价校验 | 对最终候选逐只拉实时价，与东财/新浪**三方比价** |
| 4 | **futures-panda** | ④关联背景 | 拉对应期货/成本端（如商品股看对应品种、大盘看股指期货）|
| 5 | **a-stock-analysis** | ⑤盘中量能 | `analyze.py <code> --minute`：分时放量、主力动向、封单 |
| 6 | **a-stock-trading-assistant** | ⑥多源复核 | `fetch_stock.py`（东财→新浪→同花顺→雪球）+ `--index` 大盘 |
| 7 | **a-share-stock-dossier** | ⑦候选深研 | `a_share_snapshot.py` + web 证据；对 Top1-2 做「产业逻辑+交易逻辑」深挖 |
| 8 | **a-stock-portfolio-monitor** | ⑧出单后盯盘 | `portfolio.py add/analyze` + `selector.py` 多因子；止损止盈提醒 |
| 9 | **trading-coach** | ⑨盘后复盘 | 券商 CSV FIFO 配对 + 8 维评分（事后迭代）|

## 执行顺序（6 阶段）

**阶段1 · 定环境（串行）**
1. `trading-desk/emotion.py` → 阶段/仓位
2. `a-share-short-decision` signal engine → 独立情绪/信号分（交叉验证）

**阶段2 · 扫候选（并行）**
3. `trading-desk/ashare_screen.py scan` → 全市场命中
4. `a-stock-portfolio-monitor/selector.py` → 多因子评分（第二名单）

**阶段3 · 风险/资金过滤**
5. `trading-desk/risk_flags.py` → 炸板/长上影/天量/高位/透支 → 降级
6. `trading-desk/realtime_flow.py` → **实时**全市场/板块主力资金 + 个股逐笔大单（取代 T-1 滞后）
7. `trading-desk/money_flow.py trend` → 近3日资金趋势（历史背景）
8. `a-stock-analysis analyze.py --minute` → 分时量能/主力动向复核
9. `trading-desk/announce.py` → **公告/事件排雷**（减持/解禁/监管/预亏/退市…）→ 命中🔴直接剔除

**阶段4 · 多源交叉（防幻觉）**
8. `market-price` 实时价三源比价
9. `a-stock-trading-assistant fetch_stock.py` + `--index` 大盘复核
10. `futures-panda` 拉关联期货/成本端背景

**阶段5 · 深研 + 出单**
11. `a-share-stock-dossier` 对 Top1-2 做证据深研
12. `trading-desk/position_size.py` → 按 2% 风险 + 单票 10–20% 自动算**手数/占用/最大亏损**
13. `trading-sop` 汇总 → 输出 3~5 只（格式见下）

**阶段5.5 · 竞价确认（次日 9:15–9:25）**
14. `trading-desk/auction.py snapshot <codes>` → 虚拟开盘/高开%/竞价强度/撤回单
15. 纪律：高开>5% 开盘即减；**≤09:40 不追高**，等 9:40 后确认再上

**阶段6 · 盯盘 + 复盘**
13. `a-stock-portfolio-monitor` 挂止损止盈监控
14. `trading-coach` 盘后复盘，写 `references/lessons.md`

## 输出格式（固定）

```
【环境】阶段/仓位（emotion + short-decision 双引擎）
【主线】板块 + 资金
【候选】代码 名称 | 现价 | 买点 | 止损 | 目标 | 星 | 理由(环境+主线+位置+资金口径+形态)
【校验】market-price / a-stock-analysis / trading-assistant 的复核结论
【深研】dossier 摘要（Top1-2）
【盯盘】portfolio-monitor 监控位
```
- 必附：风险声明；每条必带止损；资金流口径：**盘中用实时（realtime_flow）**，历史趋势标注日期。
- 硬规则：当日涨幅>4% 且 量能环比>1.5 倍 = 兑现位，只观察；炸板/长上影/天量/高位/5日透支 → 降级。
- 硬规则（2026-09-24 实盘复盘新增）：**早盘 ≤09:40 的追高单胜率低**（用户实盘 3 笔 -206 元、67%）→ **竞价/早盘高开不追**，等 09:40 后确认再上；**最佳买入窗口 = 09:40–11:30 与 13:00–14:00**（用户实盘各 6 笔、胜率 83%）。

## 兜底
- 任一数据源挂（RemoteDisconnected/空回复）→ 换镜像域名/降速重试；仍取不到就**如实标注"取不到"**，不硬编。
- 数据源冲突 → 以「交易所/东财盘口」为准并标注。
- **东财 push2 直连被限流/重置**（2026-09-24 定位，常态易发）→ 已固化两级兜底：
  1. `a-share-stock-dossier/scripts/a_share_snapshot.py` 已改为 **东财主用（带 Referer + 镜像轮换 + 3 次退避重试）→ 失败自动落腾讯 `qt.gtimg.cn`（quotes/indices 均有 fallback，实测可用）**。
  2. `a-share-short-decision/tools/market_data.py` 同样已固化「带 Referer 直连 + 行业优先 + junk 过滤」兜底。
  - 且本机有 `em_delay_patch.py`（sitecustomize）把 `push2` 自动改写为 `push2delay` 镜像。
  - 若东财整体不可达：改用 **腾讯(qt.gtimg.cn) + 新浪(hq.sinajs.cn)** 双源，两源一致即可采信，并在输出里标注数据源。
