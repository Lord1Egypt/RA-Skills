# 引擎口径与配置说明（chan.py 内核）

## 选型定案（2026-08-24 调研，四维横评）

| 引擎 | 理论覆盖(16项) | 集成 | 判决 |
|---|---|---|---|
| **chan.py (Vespa314)** | ≈11/16：笔/线段(特征序列)/中枢/6类买卖点/12种背驰算法/多级别联立 | MIT、纯Python≥3.11、核心零第三方依赖、单股1500根22ms | ✅ 主引擎，vendor 钉 commit `429d6ed` |
| czsc 1.0.x | ≈5/16：分型/笔/笔中枢+信号函数，**无线段对象**(作者立场) | pip即装但核心在Rust二进制不可读 | 备选/对拍用，不进主流水线 |
| chanlun-pro | 全但核心 cl.py 需付费授权文件 | GitHub 的 Apache-2.0 名不副实 | ❌ 排除 |
| 自写 | 对拍成本极高(中枢对齐率实证0.0-0.42) | — | ❌ 排除 |

chan.py 注意：README 按作者2.2万行私有完整版写的，开源版约5300行，**以 quick_guide.md 为准**；
上游 2026-06-25 后静默，vendor+钉commit，遇 bug 自行 patch（MIT 允许）。

## 配置陷阱（README 默认值不可信，已在 chan_engine.py 全部显式钉死）

| 参数 | README说 | 代码实际 | 本引擎钉死值 |
|---|---|---|---|
| `divergence_rate` | 0.9 | **inf = 根本不判背驰** | 0.9 |
| `gap_as_kl` | True | False | False |
| `max_bs2_rate` | — | 0.9999 | 0.618 |
| `min_zs_cnt` | — | — | 1 |
| `macd_algo` | — | peak | peak（24课"辅助判断"本义） |

配置指纹：输出 JSON 的 `meta.config_hash` 是配置的 md5 前8位，对拍/回归时先核对它。

## chanlun_structure_v1 字段明细

```
meta:    symbol / asof / bars_day / engine(chan.py@commit) / config_hash / stance=structure_proxy
day,week:
  bi[]:  i(序号) dir(UP/DOWN) sure b/e(起止日) bv/ev(起止价)
  seg[]: i dir sure b/e zs_n(段内中枢数)
  zs[]:  b/e sure zg/zd(中枢上下沿) gg/dd(峰值) bi_n
  bsp[]: d(日期) bs(B/S) type(1,1p,2,2s,3a,3b可组合) px sure
  pos_vs_last_zs: above_zs / in_zs / below_zs
ma:      values(ma5/10/20/60) state{long:多头排列, entangled:缠绕(5-20乖离<2%, 11-14课"吻"近似)}
signals: fresh_bsp(最近tail_days根K的bsp=选股信号) / week_day_confluence(周日同向bsp时间窗≤40天)
         / actionable_date(防前视声明)
invalidations[]: 每个fresh_bsp的失效规则+价位数值（3买→跌回ZG失效；1买→跌破当日低点；2买→跌破dd）
caveats: 口径声明四条（报告必须保留要点）
```

## 数据要求

- 前复权日K（复权在数据侧完成，引擎 autype=NONE 不再复权）；除权除息后历史结构会整体漂移，复盘对比要意识到
- ≥120 根拒绝计算（结构不可靠）；建议 ≥500 根（2年）
- 周K由日K按 ISO 周合成（引擎内部完成，无需另备周K）

## 性能基准（实测）

单股 600 根日K 双级别全量 ≈10ms；1500 根 22ms；全市场 5000 股单进程 ≈2 分钟，
`scan_market.py --workers N` 可并行。扫描哲学：**结构扫描便宜到不需要预筛**，全市场直接扫。

## 贡献指南（欢迎 PR 的方向）

- 新笔(台风帖口径)支持：`bi_algo` 配置暴露与对拍报告
- 线段口径对拍：chan vs 1+1 vs break 三算法在真实A股数据上的差异统计
- 中枢延伸/扩展(20课)的显式标注
- czsc 对拍脚本（validation/：理论不变量破坏=硬错误；数量差异=口径差异不算bug）
- 均线系统完整版：面积力度(15课)、三类吻(11-14课)的显式检测
