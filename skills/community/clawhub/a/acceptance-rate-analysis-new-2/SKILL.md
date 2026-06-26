---
name: acceptance-rate-analysis
description: 对承接率下降做阶段式归因分析。适用于“今天/本周承接率为什么下降”“分析承接率下降原因”“看一下承接率环比是否下降及原因”等场景。先定位异常切片，再逐层判断是一级切片结构迁移、资方总量明显减少或分布左移、资产维度异常，还是进一步闭环到敏感资方侧收缩。
---

# 承接率下降归因
在用户询问承接率下降原因、承接率环比变化、今天/本周承接率为什么变差时，使用这个 skill。

这个 skill 采用阶段式执行。每个阶段只做当前层级需要的取数和判断，命中终点后立即停止，不继续下钻。

## 规则优先级
- 本 `SKILL.md` 是该技能的唯一主契约，决定阶段执行顺序、判定口径、展示字段和下钻规则。
- `agents/openai.yaml` 只负责运行时默认提示，不应额外定义与本文件冲突的新口径。

## 默认规则
- 用户未指定粒度时，默认按周环比分析。
- 只支持 `day` 和 `week` 两档粒度。
- 周粒度默认以周一为一周起点。
- 用户说“本周和上周”时，默认解释为“最近一个已落定周 vs 再前一个已落定周”，不再默认按同进度单日对比。
- 用户明确说“本周截至目前 / 截至今天 / 周内累计 / 与上周同期”时，才切回同进度周累计口径。
- 周粒度对话展示优先使用实际分析周段，也就是自然周闭区间 `周一~周日`。
- 用户直接说 `4.13周`、`4.6周` 这类“周标签”时，默认按“该日期作为周一标签，对应上一完整自然周”解释。
- 例如 `4.13周 -> 2026-04-06~2026-04-12`，`4.6周 -> 2026-03-30~2026-04-05`。
- 只有用户明确说“4月13日所在周”“4月6日所在周”时，才按该日期所在自然周解释。
- 已确定粒度后，不要静默改成其他粒度；若当前粒度下时间窗或数据桶不成立，应先说明原因。

## 快速使用
先从用户问题中明确这 3 个信息：
- `granularity`
- `current_period`
- `baseline_period`

脚本不负责解析自然语言时间，运行前要先把时间窗补齐。

时间参数可以传：
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:MM:SS`

如果只传日期，脚本会自动补成开始时间 `00:00:00` 和结束时间 `23:59:59`。

命令示例只是模板，不要求逐字照抄。路径写法优先跟随当前工作目录；如果当前目录就是仓库根目录，优先使用相对路径。只有在当前工作目录不确定、跨目录调用、或已经出现找不到脚本的问题时，再退回绝对路径。

## 执行顺序
默认严格按阶段执行：
1. 先运行 `primary`
2. 读取 `primary.analysis_sequence` 与 `primary_display`
3. 对每个异常切片顺序运行 `capital`
4. 若第二阶段结果显示还需要继续看资产维度，再运行 `asset`
5. 若第三阶段结果显示还需要继续看敏感资方侧，再对 `qualified_combos` 逐个运行 `funding`

执行约束：
- 每执行完一个阶段，都必须先输出这一阶段的分析，再决定是否继续下一阶段。
- 每个阶段都要尽量覆盖“在看什么、看到了什么、所以怎么判断、下一步怎么办”，但允许自然合并成 1 到 2 段业务表达，不必机械照着内部步骤标题逐条回显。
- 后续阶段必须直接复用上游返回的 `slice_key`、`combo_key` 和分析顺序，不要手动改写或重排。
- 每个切片都要按 `capital -> asset -> funding` 固定顺序单独展开。
- `primary` 结束后，要先拿第一个异常切片，把这个切片完整分析到 `stop` 或 `funding` 结束，再开始下一个切片。
- `next_action` 只决定当前切片的下一步，不表示全部切片统一进入下一阶段；这是内部路由字段，不要对用户原样输出。
- 禁止先把所有切片批量跑完 `capital` 再统一进入 `asset` 或 `funding`。
- 禁止在还有切片未完成时，提前输出“第二阶段汇总”“第三阶段汇总”这类跨切片中间汇总。

## 统一输出原则
- `terminal_reason`、`next_action`、`run_asset`、`run_funding`、JSON 字段名都属于内部路由信息；对用户必须翻译成业务话术。
- 每个阶段优先覆盖“分析、证据、结论、下一步”四类信息，但可以合并成顺滑的业务表达，不要求机械加四个固定小标题。
- 如果某个判断没有命中，也要用一句话交代“为什么没命中，所以接下来继续看什么 / 停在哪里”，不要直接跳到下一张表或下一阶段。
- 若结果里有 `root_cause`，优先翻译成便于排查的表达，不要只说“证据不足”。
- 最终回答面向业务方，不直接暴露命令、路径、JSON 字段名、内部终点码或调试信息。

## 第一阶段：一级诊断
向 `primary` 传入粒度、当前期和对比期即可。
- `week` 传实际分析周段的闭区间，例如 `2026-04-20~2026-04-26`
- `day` 传单日闭区间，例如 `2026-04-26~2026-04-26`
- 每个时间窗都必须落在单个粒度桶内；如果时间窗跨了两个桶，先修正时间窗，再继续运行
- 如果用户给的是 `4.13周` 这类周标签，要先翻译成该周标签对应的上一完整自然周再传脚本，例如 `4.13周 -> 2026-04-06~2026-04-12`

模板：

```bash
python nanobot/skills/acceptance-rate-analysis/scripts/acceptance_rate_analysis.py primary --granularity <week|day> --current-start <当前周期开始> --current-end <当前周期结束> --baseline-start <对比周期开始> --baseline-end <对比周期结束>
```

示例 1：`2026-04-28` 这一天按默认周口径分析“本周 vs 上周”

```bash
python nanobot/skills/acceptance-rate-analysis/scripts/acceptance_rate_analysis.py primary --granularity week --current-start 2026-04-20 --current-end 2026-04-26 --baseline-start 2026-04-13 --baseline-end 2026-04-19
```

示例 2：用户说“分析 4.13周 相较于 4.6周 的承接率”

```bash
python nanobot/skills/acceptance-rate-analysis/scripts/acceptance_rate_analysis.py primary --granularity week --current-start 2026-04-06 --current-end 2026-04-12 --baseline-start 2026-03-30 --baseline-end 2026-04-05
```

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `next_action`
- `analysis_sequence`
- `drill_down_rule`

一级判定与停止：
- 若 `terminal_reason` 为 `R1`、`R2`、`R8`，第一阶段直接停止。
- 只要存在异常切片，就必须先展示异常切片表，再继续第二阶段。
- 第一阶段表格展示的是全部承接率下降切片；`analysis_sequence` 只保留后续真正继续下钻的切片。

第一阶段给模型展示时：
- 只能直接展示 `primary_display.markdown_table`，不要自己重拼，也不要改列、删列、换顺序。
- 在表格之外，必须额外展示 `primary_display.render_summary.drill_down_scope_text`；若没有该字段，再展示 `primary_display.overall_summary.drill_down_rule_text`。
- 不要把 `terminal_reason`、`next_action`、JSON 字段名原样抄给用户。

一级下钻规则必须按固定口径解释：
- 只有拖累路由金额达到 `max(20万, 全部异常切片总拖累路由金额 × 5%)` 的切片，才进入后续归因。
- 如果达到门槛的切片超过 5 个，只继续拖累路由金额最高的前 5 个。
- 如果一个都没达到门槛，保底继续分析拖累路由金额最高的 1 个切片。
- 只有当 `drill_down_rule.cap_applied = true` 时，才允许说“前 5 个”。

一级解释与排序要求：
- 表格默认按 `drag_amount` 从高到低排序，这表示“少承接金额估算”从高到低，不等于“承接率降幅”从高到低。
- 如果需要补业务解释，可以引用脚本已经给出的 `当前/对比路由占比`、`路由占比变化`、`impact_type` 等字段做推理，但不要把这些字段扩成默认展示表格。

## 第二阶段：资方分布诊断

```bash
python nanobot/skills/acceptance-rate-analysis/scripts/acceptance_rate_analysis.py capital --granularity <week|day> --current-start <沿用 primary> --current-end <沿用 primary> --baseline-start <沿用 primary> --baseline-end <沿用 primary> --slice-key "<if_qd>|<irr24_new>"
```

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `next_action`

第二阶段判断顺序固定为：
1. 先看总准入资方个数是否明显下降。
2. 如果总量没有明显下降，再看资方桶分布是否左移。
3. 如果总量没明显下降、分布也没左移，则当前先停在第二阶段，更像规则变化或授用信通过率变化，但当前脚本缺少对应指标继续验证。

第二阶段的明确口径：
- “总准入资方个数明显下降”的阈值是：当前期相对对比期下降超过 `30%`，也就是 `(对比期准入资方个数 - 当前期准入资方个数) / 对比期准入资方个数 > 30%`。
- “分布左移”不能只看均值或中位数，要一起看：
  - `<=2`、`<=3` 桶的路由金额占比是否明显上升
  - `>=4`、`>=5` 桶的路由金额占比是否明显下降
  - 加权均值 / 加权中位数是否同步下行
- 只有出现“低桶抬升 + 高桶回落”的结构变化，才算左移，才继续进入第三阶段。

面向用户展示第二阶段结果时：
- 至少交代两个判断点：先看总准入资方个数是否明显下降，再看资方桶分布是否左移。
- 即使第一个判断没有命中，也要用一句话明确说明“总量没到阈值，因此继续看分布”，不要一上来只贴分布表。
- 第二阶段讲总量判断时，必须明确带出：当前期准入资方个数、对比期准入资方个数、减少量、下降比例、判断阈值；优先直接复用代码返回的 `capital_total_judgement`。
- 下一步只用业务表达，例如“继续看资产维度”或“当前先停在资方侧”，不要输出 `next_action: run_asset` 这类内部判定行。

## 第三阶段：资产维度诊断

```bash
python nanobot/skills/acceptance-rate-analysis/scripts/acceptance_rate_analysis.py asset --granularity <week|day> --current-start <沿用 primary> --current-end <沿用 primary> --baseline-start <沿用 primary> --baseline-end <沿用 primary> --slice-key "<if_qd>|<irr24_new>"
```

内部路由重点看（不对用户直出）：
- `terminal_reason`
- `next_action`
- `qualified_combos`
- `asset_display`

第三阶段判断口径：
- 单桶识别门槛 = `max(10万, 当前切片少承接金额估算 × 5%)`
- 进入第四阶段的组合门槛 = `max(100万, 当前切片少承接金额估算 × 15%)`
- 对外表达不要说“订单特征”“画像”“异常因子”；优先说“资产维度”“异常桶”“维度组合”
- 第三阶段展示以 `asset_display.summary_markdown`、`asset_display.factor_detail_markdown`、`asset_display.combo_detail_markdown` 为唯一主来源；LLM 不再自己根据原始字段拼表
- 若需要引用维度、桶、组合名称，直接复用 trace 里的 `factor_label`、`bucket_label`、`combo_display`；不要自己根据 `factor_key` 翻译；尤其不要把 `edu_rand` 解释成“学历”，它在本技能里代表“高额区间 / 金额区间”
- 若 `qualified_combos` 为空，不要根据 `factor_results`、`abnormal_factors` 或其他字段自行臆造“高龄 + 新疆”这类组合直接进入第四阶段

面向用户展示第三阶段结果时：
- 固定按这个顺序呈现：
  1. 原样展示 `asset_display.summary_markdown`
  2. 原样展示 `asset_display.factor_detail_markdown`
  3. 原样展示 `asset_display.combo_detail_markdown`
  4. 最后再补 1 段自然语言，只总结：
     - 哪些组合进入下一阶段
     - 为什么进入
     - 没进入的典型原因是什么
- 第三阶段必须让用户看见：
  - 每个因子的具体分析过程
  - 每个桶的证据数值、影响路由金额、是否命中与结论
  - 每一种候选组合的情况
  - 哪些组合进入下一阶段、哪些没进入以及原因
- 如果继续下钻，只说“继续看敏感资方侧”；如果停住，要说明停在资产维度的原因，不要输出 `next_action: run_funding`。
- 如果第三阶段已经发现“占比上升、承接更差”的疑似异常桶，但影响路由金额没有达到单桶门槛，应直接表述为“资产维度有信号，但影响金额不足，当前停在第三阶段”；不要再外推成“更像规则变化或授用信通过率变化”。
- LLM 不再自行翻译 `factor_key`，也不再自行从 `factor_results` / `combo_results` 重新拼第三阶段表格。

## 第四阶段：敏感资方闭环
第四阶段仍通过资金项目映射数据做敏感资方侧闭环。只允许直接复用 `asset.qualified_combos[*].combo_key`；`combo_id` 只用于阅读顺序，不要把它当成跨阶段稳定主键。

```bash
python nanobot/skills/acceptance-rate-analysis/scripts/acceptance_rate_analysis.py funding --granularity <week|day> --current-start <沿用 primary> --current-end <沿用 primary> --baseline-start <沿用 primary> --baseline-end <沿用 primary> --slice-key "<if_qd>|<irr24_new>" --combo-key "<qualified_combos[i].combo_key>"
```

内部路由重点看（不对用户直出）：
- `terminal_reason`

第四阶段结果解释：
- `R7`：敏感资方收缩
- `R6`：资产维度组合异常成立，但未闭环到敏感资方
- `R8`：字段不足、映射失败或证据不足

面向用户展示第四阶段结果时：
- 重点说明“是否已经闭环到敏感资方侧”“证据是什么”“因此这一个切片最终停在哪一层”。
- 要明确说是否观察到“敏感资方相关项目数量或放款金额下降”。
- 若未闭环，也要明确说明是“资产维度组合成立，但敏感资方侧没有观察到同步收缩”，不要只说“未命中”。
- 不要对用户输出任何 `run_funding`、`terminal_reason` 或其他内部路由词。

## 内部终点码速查
- `R1`：大盘未下降
- `R2`：一级切片结构迁移
- `R3`：资方总量明显减少
- `R4`：第二阶段停住时更像规则 / 授用信通过率变化；若第三阶段停住且资产维度已有弱信号，优先按“资产维度有信号但影响金额不足”解释，不要直接复用这句口径
- `R5`：资产维度有异常，但没形成达到第四阶段门槛的高影响组合
- `R6`：资产维度组合未闭环到敏感资方
- `R7`：敏感资方收缩
- `R8`：证据不足 / 字段不足 / 口径异常
