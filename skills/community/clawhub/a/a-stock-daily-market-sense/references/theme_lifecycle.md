# 主线生命周期台账（theme lifecycle）

跨日跟踪每日报告《3.x 主线判定》中的上涨主线，把"主线确认 → 高位分歧 → 退潮 → 修复 → 再聚焦"这类演变沉淀为可查询、可可视化的序列。数据存 PG（`theme_registry` / `theme_daily_state` / `theme_market_day`，见 `scripts/_shared/init_alpha_data.sql` §13）；Markdown 报告仍是叙事真相源，台账只存运行时序列数据；HTML 报告会在主线判定小节下方自动注入泳道图区块（红 = 强势在场，绿 = 退潮，闪电 = 低位启动）。

## 状态机（八态）

| 状态 | 判定基准（与日常报告口径一致） |
|---|---|
| 低位启动 | 新上榜且位置判断为低位启动 |
| 在场候选 | ★★ 且位置为高位趋势，或启动后的延续 |
| 主线确认 | 当日 ★★★ |
| 高位分歧 | 位置判断含"分歧/分化"，或催化逻辑记录内部撕裂、核心换锚 |
| 退潮 | 从判定表消失且成员命中当日 M4 爆量下跌池，或正文明确"退潮" |
| 修复 | 退潮/分歧后重新上榜，证据为缩量或温和修复 |
| 再聚焦 | 修复后成交厚度回升、确认度维持或上调 |
| 沉寂 | 连续约 5 个交易日未上榜（隐式终态，可重新低位启动） |

合法转移由 `record` 强校验（非法转移报错并列出合法去向）：

- 低位启动 → 低位启动 / 在场候选 / 主线确认 / 高位分歧 / 退潮 / 沉寂
- 在场候选 → 在场候选 / 主线确认 / 高位分歧 / 退潮 / 沉寂
- 主线确认 → 主线确认 / 在场候选 / 高位分歧 / 退潮
- 高位分歧 → 高位分歧 / 主线确认 / 在场候选 / 再聚焦 / 修复 / 退潮
- 退潮 → 退潮 / 修复 / 沉寂 / 低位启动
- 修复 → 修复 / 再聚焦 / 主线确认 / 在场候选 / 高位分歧 / 退潮
- 再聚焦 → 再聚焦 / 主线确认 / 高位分歧 / 在场候选 / 修复 / 退潮
- 沉寂 → 沉寂 / 低位启动 / 在场候选 / 修复

主线首次入库的状态只能是：低位启动 / 在场候选 / 主线确认 / 高位分歧。

## 分工

- **脚本**（`scripts/theme_lifecycle.py`，确定性、无 LLM）：提供上下文、校验枚举与状态机转移、落库、导出窗口、向 HTML 注入区块。
- **模型**：别名归一（当日临时主题名 → canonical `theme_id`，新主线起名注册）；生命周期状态判定（退潮/修复/再聚焦需要读正文语境）；每条记录摘 evidence（来自当日催化逻辑列或正文），保证可回溯。

## 当日落库流程

1. 取上下文：

   ```bash
   python3 scripts/theme_lifecycle.py context --asof YYYYMMDD
   ```

   输出注册表（含 aliases）、各主线近期状态、watchlist（近期在场但当日尚无记录、需要判退潮还是继续在场的主线）和状态机规则。

2. 模型完成归一与状态判定，写 `reports/lifecycle_YYYYMMDD.json`：

   ```json
   {
     "asof": "2026-06-09",
     "source_report": "wiki/07-趋势复盘/2026-06-09趋势复盘.md",
     "market_state": "正常",
     "records": [
       {
         "theme_id": "TH-光通信算力连接",
         "raw_theme_name": "光通信 / 通信线缆 / 算力连接链",
         "stars": 2,
         "position": "高位趋势",
         "crowding": "高",
         "state": "再聚焦",
         "evidence": "新易盛、中天科技、亨通光电同步放量修复……仍是强分歧后的再聚焦",
         "members_sample": ["新易盛", "中天科技", "亨通光电"]
       },
       {
         "new_theme": {"theme_id": "TH-电力电子电源", "name": "电力电子 / 电源设备", "overlay": null},
         "raw_theme_name": "电力电子 / 电源设备 / 能源材料分支",
         "stars": 2,
         "position": "低位启动",
         "crowding": "中",
         "state": "低位启动",
         "evidence": "麦格米特、顺络电子等进入赚钱效应池，资金向能源和电源环节扩散",
         "members_sample": ["麦格米特", "顺络电子"]
       }
     ]
   }
   ```

   字段约定：

   - `theme_id`：已注册主线直接引用；新主线改用 `new_theme` 块注册，`theme_id` 必须 `TH-` 前缀。
   - `stars`：主线确认度 ★ 数（1/2/3）；未上榜的退潮/沉寂记录写 `null`。
   - `state`：八态之一。watchlist 中当日缺席的主线，结合 M4 爆量下跌池与正文判断写 `退潮` 或 `沉寂`，并给出依据。
   - `force`: true 时跳过状态机校验，仅用于人工确认过的特例。
   - `market_state`：全面退潮日（当日报告没有主线判定表）必写 `"全面退潮"` 并可附 `market_note`；正常日可省略。

3. 写入：

   ```bash
   python3 scripts/theme_lifecycle.py record --input reports/lifecycle_YYYYMMDD.json
   ```

   校验失败会逐条列出错误与合法去向，修正后重跑（幂等 upsert，可重复执行）。成功后 `lifecycle_YYYYMMDD.json` 属于中间产物，`run_daily_panel.py --cleanup` 会一并删除。

## 其他命令

```bash
# 窗口导出（HTML 区块 payload，调试用）
python3 scripts/theme_lifecycle.py window --asof YYYYMMDD --days 22

# 向既有报告 HTML 幂等注入区块（marker 注释包裹，可重复执行；
# 对已带原生 ChartHook 区块的新版页面自动跳过，并清除历史重复 marker 块）
python3 scripts/theme_lifecycle.py inject --html <file.html> [--asof YYYY-MM-DD] [--days 22]

# 解析历史复盘的主线判定表，生成回填草稿（归一与状态标注由模型完成后再 record）
python3 scripts/theme_lifecycle.py backfill-draft --reviews <复盘目录> [--out draft.json]
```
