---
doc-type: HANDOFF
layer: process
doc-class: history
task-id: FS-yyyymmdd-nnn     # FS-<日期>-<当日序号>，一经分配不复用
stage: 需求                  # 需求 | 设计 | 实现 | 测试 | 交付 | 文档
role:                        # 本次委派的目标角色
status: dispatched           # dispatched（已派发待产出） | delivered（角色已产出并回填交接字段）
owner:                       # 本次委派的责任角色（默认总指挥）
created: YYYY-MM-DD
---

# HANDOFF：〈FS-yyyymmdd-nnn〉〈stage〉阶段委派单

> **产出者**：总指挥（元技能）——每次委派构造一份新单，是跨角色任务派发的唯一载体
> **受众**：本次委派的目标角色 + 任务全程的审计者（人类 + AI 编程智能体）
> **归档**：`docs/process/handoffs/FS-yyyymmdd-nnn.md`（本文件即该次委派的唯一权威记录；delivered 后不可变）
> **真值源**：委派内容与交接摘要以本文件为准；产出物内容以其自身文件为准——本文件只存指向与摘要，不复制内容
> **质量门禁**：① 每次委派一份新单，task-id 当日递增、不复用 ② user_brief 逐字保留用户原话，任何角色不得改写 ③ 正文为单个 yaml 块，字段完整、可被机器解析 ④ 角色产出后须回填 blocked_on 与交接字段，且不改动派发时的既有字段

## 阶段与角色对照

| stage | 典型目标角色（role 取值参考） |
|---|---|
| 需求 | 需求分析师 |
| 设计 | 架构师 / UI-UX 设计师 / 数据库工程师 |
| 实现 | 后端工程师 / 前端工程师 |
| 测试 | 测试工程师 / 安全工程师 |
| 交付 | DevOps 工程师 |
| 文档 | 技术文档工程师 |

## 1. 委派单正文

〈填写指引：以下 yaml 块由总指挥在派发时构造，占位符一律〈尖括号〉，示例值只示范格式不照抄内容。目标角色产出时在文末追加/回填 blocked_on 与交接字段，其余字段不改写。〉

```yaml
task_id: FS-20261113-001            # FS-<yyyymmdd>-<当日序号>
stage: 设计                          # 需求|设计|实现|测试|交付|文档
role: architect                      # 本次委派的目标角色

user_brief: |                        # 用户原话，逐字保留，不转述、不删减、不改写
  〈用户原话〉

stack:                               # 已锁定的技术栈；未定项写"待选型"
  backend: 〈如 Java17/SpringBoot3，或 待选型〉
  frontend: 〈如 React18，或 待选型〉
  database: 〈如 MySQL8，或 待选型〉
  cache: 〈如 Redis7，或 待选型〉

artifacts:                           # 已有产出物，docs/ 相对路径，无则保留空列表
  - docs/project/req-spec.md

handoff_notes: |                     # 上一角色的关键决策与关注点摘要
  〈上一角色交接说明；重大决策引 ADR-NNNN + 相对路径，只指向不复制结论〉

scope: |                             # 本次委派范围
  做什么：〈...〉
  不做什么：〈明确排除项——防止角色越界产出，与"做什么"同等重要〉

constraints: |                       # 约束：deadline、环境、兼容性、红线
  〈约束〉

blocked_on: []                       # 所需他人信息（角色产出时追加）：每项 = ID + 相对路径 + 需要什么
                                     # 示例：- docs/process/handoffs/FS-20261113-002.md（需要 DBA 的容量评估数据）

dissent: |                           # 技术异议留痕（可选）：仅方案经终审后仍存异议时填写
  〈异议与论据；终审记录出处〉
```

## 2. 字段填写规则

〈填写指引：本节是硬规则，非建议；违反任一条即委派单不合格，目标角色有权拒收。〉

| 规则 | 说明 |
|---|---|
| user_brief 透传 | 用户原话全流程原样透传，任何角色不得改写、转述或删减——后续角色须能还原用户最初意图 |
| 产出回填 | 角色产出时仅在文末追加 blocked_on（所需他人信息，每项 ID + 相对路径 + 需要什么）与交接字段；派发时的既有字段一字不动 |
| dissent 时机 | 仅在技术方案经终审后仍存异议时填写（仲裁留痕）；终审前的异议走评审流程，不落本字段，终审后仍保留 |
| 单号不复用 | task-id 一经分配不复用；同日多次委派序号递增，作废单保留不删 |
| 交接摘要去重 | handoff_notes 只存指向与要点，产出物内容不复制——同一信息只维护一处 |

## 红线自查（一票否决，派发前逐条勾选）

- [ ] 本次委派为一份新单，未复用、改写或覆盖任何既有 HANDOFF
- [ ] user_brief 为用户原话逐字拷贝，未转述
- [ ] scope 同时写明"做什么"与"不做什么"
- [ ] 正文为单个 yaml 块，task_id / stage / role / user_brief / stack / artifacts / handoff_notes / scope / constraints 字段完整
- [ ] 未定技术栈项已标"待选型"，未留空、未猜测
- [ ] 产出回填未改动派发时的既有字段，仅追加 blocked_on 与交接字段
- [ ] 所有〈占位符〉已替换为实际内容，task-id 与 frontmatter、文件名三者一致

## 追踪链

| 方向 | 对象 | 说明 |
|---|---|---|
| 上游（本文消费） | 〈上一阶段 HANDOFF FS-yyyymmdd-nnn / PRD FR-xxx / ADR-NNNN〉 | 委派依据与上游产出 |
| 下游（消费本文） | 〈目标角色的产出物（docs/ 相对路径）〉 | 本单 scope 约定的产出指向 |
| 下游（消费本文） | 〈下一阶段 HANDOFF（`docs/process/handoffs/`）〉 | handoff_notes 与交接字段被后续委派引用 |
| 下游（消费本文） | PR-SUMMARY（`docs/process/pr-summaries/FS-yyyymmdd-nnn.md`） | 任务收尾时汇总本单交付状态与 dissent |
