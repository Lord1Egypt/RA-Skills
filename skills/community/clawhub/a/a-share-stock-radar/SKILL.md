---
name: a-share-stock-radar
description: A股短线选股「股票雷达」——先判市场情绪环境 → 锁定主线板块 → 挑低位/启动位置 → 看形态与资金 → 输出带止损的候选名单，并附仓位、卖点与次日复核。适用于：A股短线选股（1–5 个交易日）、"今天买什么/明天买什么"、强势股与龙头筛选、市场情绪与连板梯队、主力资金流与实时大单、龙虎榜席位、涨停板质量、板块资金接力、竞价雷达（9:15–9:25）、公告/减持/解禁排雷、按风险自动算仓位、持仓到价/止损提醒、交易日志与复盘统计。触发词：选股、短线标的、强势股、龙头、涨停、连板、市场情绪、情绪周期、资金流、主力净额、大单、龙虎榜、席位、板块接力、竞价、打板、止损、仓位、买点、卖点、次日复核、复盘、胜率。
---

# 股票雷达（A股短线选股）

给 A 股短线交易者的一套「数据驱动选股」工作流 + 免费数据脚本（纯标准库，无需 API Key，数据源为公开免费接口）。

## 铁律

- 仅提供**分析与参考，不构成投资建议**；不保证盈利，短线风险高，盈亏自负。
- **每条候选必须给止损位**，没止损不出单；**绝不追高、绝不补仓摊平**。
- 数据必须**脚本实时抓取**；取不到就如实说明，**不得编造价格**。

## 核心顺序（务必按此顺序）

**先判环境 → 再锁主线 → 再挑位置 → 最后看形态/资金。**

0. **定环境**：`python3 scripts/emotion.py` → 涨停/跌停/炸板家数、最高板、封板率、昨日涨停今日溢价+晋级率 → 定阶段（冰点/启动/发酵/高潮/退潮）+ 建议仓位。溢价为负或晋级率低 → **当天防守，不追强势股**。
1. **扫候选**：`python3 scripts/ashare_screen.py scan 20` → 全市场扫（涨幅 3–9.5% + 换手 4–25% + 主力净额>0）。
2. **位置前置**：剔除「当日涨幅>4% 且量能环比>1.5倍」的兑现位；优先「平台/缩量整理后首次温和放量」的启动位。
3. **风险前置**：`python3 scripts/risk_flags.py <code...>` → 炸板/长上影/天量/换手过热/5日透支 → 一律**降级**。
4. **资金看趋势不看单日**：`python3 scripts/money_flow.py trend <code> 5` → 近3日连续流入优先，单日脉冲降级。盘中用 `scripts/realtime_flow.py` 取**实时**主力/大单。
5. **公告排雷**：`python3 scripts/announce.py <code...>` → 减持/解禁/监管/预亏 → 命中直接剔除。
6. **输出 3–5 只**：每只给 `代码 名称 | 现价 | 买点 | 止损 | 目标 | 星级 | 理由(环境+主线+位置+资金+形态)`。资金流需标注口径与时点（**盘中用实时；历史趋势注明日期**，不当前瞻信号）。
7. **仓位**：`python3 scripts/position_size.py --capital <总额> --entry <买点> --stop <止损> --targets <目标>` → 按单笔风险 ≤2%、单票 10–20% 自动算手数。
8. **盯盘**：`python3 scripts/price_alert.py add/check` 挂止损/止盈提醒。

## 主要脚本

```bash
# 市场情绪温度计（先判环境）
python3 scripts/emotion.py [YYYYMMDD]
# 全市场短线扫描（首选）/ 各类榜
python3 scripts/ashare_screen.py scan 20     # 也可 gainers|inflow|turnover|amount
# 资金流
python3 scripts/money_flow.py trend <code> 8   # 近N日主力/超大/大/中/小净额 + 趋势
python3 scripts/money_flow.py intraday <code>  # 当日分时主力
python3 scripts/realtime_flow.py               # 全市场/板块实时资金（分钟级）
python3 scripts/realtime_flow.py --codes <code...>  # 个股实时大单
# 形态风险 / 位置
python3 scripts/risk_flags.py <code...>
python3 scripts/kline.py <code> 30             # 日K + MA5/10/20
python3 scripts/intraday_structure.py <code...># 30分钟结构 + 量价背离
# 板块
python3 scripts/sector_flow.py industry 15 [flow]
python3 scripts/sector_relay.py industry 15    # 板块资金接力（今/5/10日）
# 盘后
python3 scripts/lhb.py day|api|ngw|stock|seat  # 龙虎榜/席位
python3 scripts/limitup_quality.py [YYYYMMDD]  # 涨停封单/首封/连板
# 竞价（9:15–9:25）
python3 scripts/auction.py snapshot <code...>
# 排雷 / 仓位 / 盯盘
python3 scripts/announce.py <code...>
python3 scripts/position_size.py --capital 100000 --entry 10.0 --stop 9.5 --targets 11,12
python3 scripts/price_alert.py add --code <code> --name <名> --entry 10 --stop 9.5 --target 11.5
python3 scripts/price_alert.py check
# 交易日志 + 复盘统计
python3 scripts/trade_log.py add|close|list|stats ...
python3 scripts/review.py [--import-csv <券商csv>]
# 历史回测（4 形态）
python3 scripts/backtest.py --days 180
# 一键跑全套
bash scripts/radar_run.sh [候选代码...]
```

## 输出格式（固定）

```
【环境】阶段 / 建议仓位
【主线】板块 + 资金
【候选】代码 名称 | 现价 | 买点 | 止损 | 目标 | 星 | 理由(环境+主线+位置+资金+形态)
【校验】多源比价 + 分时量能
【盯盘】止损/止盈监控位
```

必附风险声明。硬规则：**当日涨幅>4% 且量能环比>1.5倍 = 兑现位，只观察**；炸板/长上影/天量/高位/5日透支 → 降级；**早盘 ≤09:40 不追高，最佳买入窗口 09:40–11:30 与 13:00–14:00**。

## 参考文件

- `references/stock-radar.md` — 完整 SOP（执行顺序 + 数据维度）。
- `references/playbook.md` — 形态定义、仓位/止损纪律、位置三分法。
- `references/emotion-cycle.md` — 情绪周期 / 主线梯队 / 复盘 8 要素。

## 关于 & 完整版

- 本技能为**免费开源版**（ClawHub · MIT-0），可自由使用、修改、分发。
- **完整版 / 商业授权 / 一对一答疑 / 数据源持续维护** → **https://gupiaoleida.surge.sh**

## 兜底

东财 `push2` 直连易被限流 → 脚本已内置「带 Referer + 镜像轮换 + 退避重试」，失败自动落 **腾讯 `qt.gtimg.cn` / 新浪 `hq.sinajs.cn`** 双源兜底；两源一致即可采信，并在输出标注数据源。数据源冲突以交易所/东财盘口为准。

> ⚠️ 仅为分析与参考，不构成投资建议；A股短线风险高，盈亏自负，务必带止损、控仓。
