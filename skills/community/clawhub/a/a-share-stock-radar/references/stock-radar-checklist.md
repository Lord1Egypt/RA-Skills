# 股票雷达 · 执行清单（10 技能逐项勾选，2026-09-24 写死）

> 每次选股**必须**按本清单逐项执行并回报状态。可一键跑：`bash skills/trading-desk/scripts/radar_run.sh [候选代码...]`
> 状态图例：✅ 跑了 ｜ 🟡 换源兜底 ｜ ⬜ 待输入/不适用 ｜ ❌ 失败(需修复后重跑)

## 一键执行

```bash
# 阶段1-2（无需候选）：环境 + 全市场扫描 + 第二名单
bash skills/trading-desk/scripts/radar_run.sh

# 全链（带候选代码）：再加 风险/资金/分时/深研
bash skills/trading-desk/scripts/radar_run.sh 002487 603667 601218
```

原始输出落到 `/tmp/openclaw/radar/<时间戳>/`，终端打印「参与状态汇总」表。

## 逐项清单（手工模式 / 核对用）

| # | 技能 | 命令 | 期望产出 | 状态 |
|---|---|---|---|---|
| 1 | **trading-desk** | `scripts/emotion.py` → `scripts/ashare_screen.py scan 20` → `scripts/sector_flow.py industry 15` | 环境阶段+仓位 / 候选池 / 主线板块 | ☐ |
| 2 | **a-share-short-decision** | `cd skills/a-share-short-decision && python3 main.py short_term_signal_engine --date <D>` | candidates + 因子分（交叉验证） | ☐ |
| 3 | **market-price** | juglans ticker（不可达则）新浪+腾讯双源 | 候选实时价三源一致 | ☐ |
| 4 | **futures-panda** | `scripts/futures_quote.py 沪深300 中证500 <关联品种>` | 股指/成本端背景 | ☐ |
| 5 | **a-stock-analysis** | `scripts/analyze.py <codes> --minute` | 分时量能/主力动向/封单 | ☐ |
| 6 | **a-stock-trading-assistant** | `fetch_stock.py --index` `--hot-sectors` | 大盘 + 热点板块复核 | ☐ |
| 7 | **a-share-stock-dossier** | `a_share_snapshot.py --codes ... --with-indices --with-kline` | 候选快照+K线+证据深研 | ☐ |
| 8 | **a-stock-portfolio-monitor** | `scripts/selector.py` → 出单后 `portfolio.py add` 挂止损 | 第二名单 / 盯盘位 | ☐ |
| 9 | **trading-sop** | 本清单即其编排；汇总输出 3~5 只 | 定稿「候选」段 | ☐ |
| 10 | **trading-coach** | 用户给券商交割单 CSV → FIFO 配对 + 8 维评分 | 复盘 → `references/lessons.md` | ☐ |

## 硬规则（不满足即剔除/降级）

- 当日涨幅 **>4% 且** 量能环比 **>1.5 倍** = 兑现位 → **只观察不推荐**
- 炸板 / 长上影 / 天量 / 高位 / 换手过热 / 5日透支 → **降级**
- 剔除：连板一字、纯题材无资金、ST、新股首日
- 每条必带**止损**；资金流标注「**昨日(滞后)**」；总仓 ≤2-3 成（大盘弱时）

## 数据源兜底（2026-09-24 固化）

- 东财 push2 被限流 → 自动落**腾讯 `qt.gtimg.cn`**（dossier 已固化双 fallback）
- 东财整体不可达 → **新浪 + 腾讯** 双源，两源一致即采信并标注
- 仍取不到 → **如实标注「取不到」**，绝不编造

## 扩展维度（雷达+，2026-09-24 为提升胜率新增）

| 工具 | 命令 | 补的缺口 |
|---|---|---|
| 龙虎榜/游资 | `lhb.py day` / `lhb.py stock <code>` | 谁在买（机构/游资/成功率） |
| 涨停板质量 | `limitup_quality.py [YYYYMMDD] [--early]` | 封单强度 / 首封时间 / 连板梯队 |
| 板块资金接力 | `sector_relay.py industry 15` | 今日/5日/10日主力净额 → 接力 vs 脉冲 |
| 30min结构 | `intraday_structure.py <codes>` | 量价背离 / 比日线更早的拐点 |
| 4形态回测 | `backtest.py --days 180` | 把形态胜率从「感觉」变「数据」 |
| 持仓监控 | `price_alert.py add/check` | 盘中破止损自动提醒 |
| 交易日志+复盘 | `trade_log.py` / `review.py` | **复盘闭环**：按形态统计胜率/期望 |

> 以上均已接入 `radar_run.sh`：基础阶段自动跑 涨停质量/板块接力/龙虎榜；带候选时再跑 30min 结构。

## 2026-09-24 三件套（补最后三个缺口）
| 工具 | 命令 | 作用 |
|---|---|---|
| 竞价雷达 | `auction.py snapshot <codes>` | 9:15–9:25 虚拟开盘/高开%/竞价强度/撤单 |
| 公告排雷 | `announce.py <codes>` | 减持/解禁/监管/预亏 → 🔴直接剔除 |
| 自动仓位 | `position_size.py --capital ... --entry ... --stop ...` | 按 2%风险+单票20% 算手数 |
| 盘中卖点 | `price_alert.py check --fade 3` | 冲高走弱（距今高≥3%）提醒减仓 |

> `announce.py` 已接入 `radar_run.sh` 候选段（`↳ 公告排雷`）。

## 实时资金（2026-09-24，解决 T-1 滞后）
| 工具 | 命令 | 作用 |
|---|---|---|
| 全市场/板块/个股榜 实时 | `realtime_flow.py` | 牛股王 API，分钟级主力净额（实时） |
| 个股实时大单 | `realtime_flow.py --codes <code...>` | 东财逐笔，超大单/大单净额（近1000笔） |
> 已接入 radar_run.sh：基础段跑「↳ 实时资金(全市场)」，候选段跑「↳ 实时大单(个股)」。

## 龙虎榜 / 席位（2026-09-24 装技能，盘后 17:30）
| 来源 | 命令 | 特点 |
|---|---|---|
| 东财 | `lhb.py day [date]` | 净买入榜 + 游资标签 |
| lhb-api | `lhb.py api [date]` / `seat <code>` | **买5卖5营业部席位明细**（今天默认源） |
| 牛股王 | `lhb.py ngw [date] --type N` | 按**资金性质**筛（1机构/2游资/3外资/4顶级游资/5一线游资） |
> `lhb.py` 自动处理盘后规则：<17:30 自动回退到上一交易日并提示。
