---
doc-type: RETRO
layer: process
doc-class: history
status: open                 # open | closed（关闭条件见 §5；行动项未全部外发前不得 closed）
iteration: YYYY-iterN        # 一迭代一文件，与 PROGRESS 同号对应
owner:                       # 复盘执笔人（角色或人）
created: YYYY-MM-DD
closed:                      # 关闭日期，仅 status: closed 时填写
---

# RETRO：〈YYYY-iterN〉迭代复盘

> **产出者**：迭代全体参与者（人类 + AI 编程智能体）共同提炼，一人执笔；迭代收尾时进行
> **受众**：团队、下一迭代执行者、ROADMAP 维护者
> **归档**：`docs/process/retro/YYYY-iterN.md`（本文件即该迭代复盘的唯一权威记录；closed 后不可变）
> **真值源**：判断与结论以本文件为准；过程事实以 PROGRESS（`docs/process/progress/YYYY-iterN.md`）为准——本文件只做提炼，不重述细节
> **质量门禁**：① 行动项全部外发到具体去处（新 ADR / ROADMAP BK-xxx / 新 TECH / 新或更新 RUNBOOK）并回链后方可 status: closed ② 无处可落的行动项视为未完成，复盘不得关闭 ③ 事实留在 PROGRESS，本文件只含提炼后的判断 ④ 每个 Problem 含一句机制层面的根因，不追责个人

## 状态说明

| 状态 | 何时使用 | 关键义务 |
|---|---|---|
| open | 复盘已开始，行动项未全部外发 | 持续追踪 §4 外发进度；本文件可继续更新 |
| closed | §5 关闭检查全部通过 | 填写 closed 日期，本文件转不可变；新问题登记 BK-xxx 或开新 RETRO |

迁移路径：open → closed（单向）；关闭的唯一条件是 §5 逐项勾选完成，与时间无关——到期未外发只能保持 open，不能"到期自动关闭"。

## 1. 目标回顾

〈填写指引：对照 PROGRESS §1 迭代目标与 ROADMAP（`docs/project/ROADMAP.md` §1）当前迭代的承诺，逐条写"达成了什么、偏差是什么"；可引用关键数据（完成率、缺陷数、周期），数据口径与 PROGRESS §3 迭代收尾一致，不另立口径。事实结论引 PROGRESS 链接即可，不复制过程细节；偏差只描述差距本身，原因分析放 §3。表格保留示例行示范。〉

| 条目 | 达成情况 | 证据与偏差 |
|---|---|---|
| CUR-001（示例行） | 达成 | 导出接口 P95 287ms，证据 `docs/process/progress/2026-iter4.md` §3；偏差：压测环境与生产规格不一致，数据代表性有限 |
| CUR-002（示例行） | 未达成 | 完成 60%；未完成部分已回 Backlog BK-021（`docs/project/ROADMAP.md` §2） |

## 2. 做得好的（Keep）

〈填写指引：列出本迭代值得保持的实践，每条 = 实践 + 为什么有效（一句话），让未经历现场的读者或 AI 也能照做。只收有证据的：能在 PROGRESS §2 找到对应事实的才写；"团队氛围好"类不可操作的表述禁止。Keep 项默认延续为下一迭代的默认实践。〉

- 〈示例行：每日记录阻塞并当场指定 blocked_on 对象——阻塞平均滞留 < 1 天，见 PROGRESS §2 各日"阻塞 / 待办移交"段〉
- 〈示例行：接口变更先改契约文档再改代码——联调零返工，见 PROGRESS §2 中 `docs/project/api-contract.md` 的相关提交〉
- 〈示例行：危险操作先在预发环境演练一次再上生产——本迭代零生产事故，见 `docs/project/runbooks/` 相关操作记录〉

## 3. 做得不好的（Problem）

〈填写指引：每个问题一行 = 现象 + 一句根因。根因指向机制（流程缺失 / 信息断层 / 标准缺位），不指向个人——"某人忘了"不是根因，"缺提醒机制"才是。无根因的条目不合格；现象须能在 PROGRESS §2 找到对应事实，不凭印象罗列。不求全：一次复盘聚焦当期影响最大的 3-5 个问题。〉

- 〈示例行：两个模块对同一枚举各自定义取值，联调返工 1 天；根因：DESIGN 横切概念一节未登记枚举的真值源位置〉
- 〈示例行：压测启动两次被打断，累计等待 3 天；根因：影子库申请无标准流程与责任角色〉

## 4. 改进行动项（Action）

〈填写指引：针对 §3 每个问题给出行动，优先级高者排前。每个行动必须指定唯一去处：ROADMAP 待办（登记为 BK-xxx）/ 新 ADR（决策类问题）/ 新 TECH（满足成文门槛——同一问题第二次出现或排查成本 > 30 分钟，`templates/knowledge/TECH.md`）/ 新或更新 RUNBOOK（操作类问题）。责任人写角色不写人名（人可变动，角色常在）。状态只有两值：未外发 / 已外发；已外发必须回链目标 ID + 相对路径，"已安排"不算外发。行动项不求多：每个 Problem 至少一条、至多两条；一次改不动的问题拆到后续迭代，不堆清单。〉

| # | 行动 | 去处 | 责任人 | 状态 |
|---|---|---|---|---|
| 1（示例行） | 〈在 DESIGN §8 横切概念登记枚举真值源位置〉 | BK-022（`docs/project/ROADMAP.md` §2） | 〈架构师〉 | 已外发 |
| 2（示例行） | 〈为影子库申请建立标准操作流程〉 | RUNBOOK（`docs/project/runbooks/`，新建） | 〈DevOps〉 | 未外发 |

## 5. 关闭检查

〈填写指引：逐项勾选；全部满足后将 frontmatter 改为 status: closed 并填写 closed 日期，本文件随之转不可变。任何一项不满足，复盘保持 open——"差一项也算差不多"不成立；长期 open 的 RETRO 本身就是一个待解决问题，应在下一期复盘中首先追因。〉

- [ ] §4 全部行动项已外发并回链（每行状态为"已外发"且含目标 ID + 相对路径）
- [ ] 未完成事项去向已在 PROGRESS（`docs/process/progress/YYYY-iterN.md` §3 迭代收尾）记录
- [ ] frontmatter 的 status 已改为 closed、closed 日期已填写
- [ ] 本 RETRO 已归档至 `docs/process/retro/YYYY-iterN.md`

## 红线自查（一票否决，关闭前逐条勾选）

- [ ] 行动项全部外发到新 ADR / ROADMAP BK-xxx / 新 TECH / 新或更新 RUNBOOK 之一并回链
- [ ] 无处可落的行动项已视为未完成，本复盘保持 status: open
- [ ] frontmatter 的 status 与 §5 勾选进度一致——未全部勾选前保持 open，未虚标 closed
- [ ] 未重述过程事实——本文件只含提炼后的判断，过程细节均在 PROGRESS
- [ ] 每个 Problem 含一句机制层面的根因，无指向个人的追责
- [ ] 每条 Keep 可在 PROGRESS §2 找到对应事实
- [ ] 目标回顾的数据口径与 PROGRESS §3 一致
- [ ] frontmatter 的 iteration 与文件名、同号 PROGRESS 一致
- [ ] status: closed 后未再修改正文（发现新问题开新 RETRO 或登记 BK-xxx，不改本文件）

## 追踪链

| 方向 | 对象 | 说明 |
|---|---|---|
| 上游（本文消费） | PROGRESS（`docs/process/progress/YYYY-iterN.md`）§2 §3 | 全部过程事实的来源 |
| 上游（本文消费） | ROADMAP CUR-xxx（`docs/project/ROADMAP.md` §1） | 迭代承诺的对照基准 |
| 下游（消费本文） | 〈ROADMAP BK-xxx / ADR-NNNN / TECH / RUNBOOK〉 | 行动项的全部外发去处 |
| 下游（消费本文） | 下一迭代 PROGRESS（`docs/process/progress/YYYY-iterN+1.md`） | Keep 项延续为新迭代实践；未外发行动项的追因对象 |
