# CMS Project Governance 中文治理协议

版本：2.2.1

本 Skill 是 AI 软件交付的控制层。它把模糊意图、变化中的目标和大量旧 CMS 记录收敛成一个当前授权，让执行 Agent 在边界内主动推进，并确保完成声明不超过证据强度。

使用用户语言，先用普通语言，再用技术术语。

## 语言与兼容

- 中文任务使用本文件，只加载 `{baseDir}/references/zh-CN/` 中当前需要的文件。
- 英文任务使用 `{baseDir}/SKILL.md` 和 `references/en/`。
- 机器字段与枚举值保持英文。
- Active Packet 保持 `contract_version: "2.0"`，通过 2.1 策略字段兼容升级。

## 核心原则

1. 用户拥有目的、优先级和重大决定权。
2. 普通、可逆的实现选择由 AI 自主解决，不转嫁给不熟悉编程的用户。
3. 治理用于降低不确定性、偏移、Token 与返工，不用于增加文书。
4. 一个当前事实只有一个权威位置。
5. Milestone 是完整、用户可观察的能力，不是短任务、测试失败或计时阶段。
6. `Developer Complete`、`Stage Verified`、`Runtime Verified`、`Accepted` 是不同声明。
7. 类型、接口或文档契约通过，不等于运行功能可用。
8. 证据高于状态文字；证据冲突时采用较弱结论。
9. 局部合规不能掩盖整体目标偏移。
10. 使用足以控制真实风险的最轻治理档位。
11. 治理产出按「消除了多少不确定性」计价，不按「产出了多少文档」计价。当文档持续增长而已验证行为不变时，治理本身已经成为风险。
12. 目标变更必须新建基线记录，绝不在旧文件上标注作废。历史通过移动来归档，不通过叠加覆盖说明来处理。

## 与执行 Skill 的关系

- 本 Skill 负责发现、规模、旧状态迁移、授权、对齐和最终验收。
- `agent-loop-engineering` 负责 Bounded Autopilot 执行。
- 两者通过一份 `Docs/ACTIVE_PACKET.md` 交接。
- 本 Skill 拥有目标和最终 QA 权限；执行 Skill 拥有实现与阶段证据。
- 单 Agent 提示词中的 `QC` 代表 Stage Reviewer，Standard / Full 终验仍须独立。
- 若用户只要一次性的只读结论（继续 / 收窄 / 转向 / 归档 / 停止），且不需要持续治理状态，改用 `project-lifecycle-navigator`。
- **独立安装。** 本 Skill 不依赖 `agent-loop-engineering` 也能运行。文档中出现的 `{baseDir}/../agent-loop-engineering/...` 路径或 `node <agent-loop-engineering>/scripts/...` 命令，只是「两者同时安装」时的快捷写法。若未安装该同级 Skill，用一行说明情况，并改用等价的内置动作：跳过 Active Packet 引导脚本，直接用本包模板写 `Docs/ACTIVE_PACKET.md`；用手工阶段证据检查替代校验脚本；用上文「最多三个 worker」规则替代 `isolated-delegation.md`。不得仅因缺少同级 Skill 就中断流程。

创建或审核 Packet 前读取 `{baseDir}/references/zh-CN/execution-contract.md`。

## 跨插件文件契约（CDH）

当 Personal Supervisor 与 Governance 同时挂在同一 Cordis 上下文时，文件所有权
遵循 CDH 握手，而不是共享可变目录。在写入 `.agent-state/<task-id>/`、盖戳
`governance/supervisor-binding`、或跨插件缝引用 Active Packet / 工单之前，先读
`{baseDir}/references/zh-CN/cross-plugin-file-contracts.md`。

插件只实现该契约；本 Skill 拥有契约正文。冲突时以该参考文件为准。

## 单次模式

每次只选择一个权限模式：

| 需求 | 模式 | 参考 |
| --- | --- | --- |
| 只有概念或问题 | Goal Discovery | `goal-discovery.md` |
| 把目标转成有界工作 | Planning and Sizing | `planning-and-sizing.md` |
| 有旧 CMS 文件但没有可靠当前态 | Legacy Bootstrap | `legacy-bootstrap.md` |
| 授权 Milestone、Program、Work Order | Dispatch | `governance-profiles.md`、`controller-qa.md` |
| 审查最新阶段或交付 | Stage Review / Delivery QA | `controller-qa.md` |
| 检查是否仍符合初衷 | Direction Alignment | `alignment-and-rebaseline.md` |
| 新需求可能改变目标 | Target Rebaseline | `alignment-and-rebaseline.md` |
| 全项目审计或完成线 | Audit / Roadmap | `alignment-and-rebaseline.md` |

全项目审计、最新交付 QA、目标重基线不能混在同一个权限动作内。

## Legacy Bootstrap

没有有效 Active Packet 时：

1. 大小写不敏感地定位 `Docs` 或 `docs`；
2. 只索引文件名、大小、时间，不读取全部正文；
3. 只读当前权威文件和其中明确链接的文件；
4. 找出当前目标、验收、活跃 Work Order、最新有效状态和唯一下一步；
5. 检查路线冲突、重复 Current Assignment、被后续推翻的 QA、权限缺失和交付类别错报；
6. 计算 authority fingerprint；
7. 无冲突时草拟一份精简 Packet；
8. 只有显式 `--write` 且路径位于真实项目根目录内时才写入。

命令：

```text
node {baseDir}/../agent-loop-engineering/scripts/bootstrap-active-packet.mjs --workspace <项目路径> --language zh-CN --json
```

两个 Skill 分开安装时，从已安装的 `agent-loop-engineering` 找到同名脚本。有冲突时零写入，只返回一个合并后的 Owner 决策请求。

保留旧历史。迁移后停止继续扩张重复的 STATUS、NEXT_ACTIONS、PENDING、COMPLETED、逐阶段 Dispatch 和逐阶段 Handoff；只有受监管流程明确要求时例外。

详见 `{baseDir}/references/zh-CN/legacy-bootstrap.md`。

## 通用流程

```text
想法、需求或旧状态
  -> 发现或迁移出一个目标结果
  -> 定义最小有效范围与 Non-Goals
  -> 分类交付声明和证据
  -> Small / Medium / Large
  -> Lite / Standard / Full
  -> 创建或刷新 Active Packet
  -> Bounded Autopilot
  -> 阶段检查和必要返修
  -> 方向对齐
  -> 需要时独立终验
  -> 接受、返修、拆分、重基线或停止
```

可逆的不确定项可以用明确假设继续。只有可能改变核心目标、产生重大风险、跨越保护边界或浪费大量工作时才停止。

## 状态与声明维度

必须分开记录：

| 维度 | 取值 |
| --- | --- |
| Goal readiness | `Concept`、`Direction`、`Ready for Planning`、`Ready for Execution`、`Owner Decision Required` |
| Execution | `Ready`、`In Progress`、`Ready for Independent Acceptance`、`Needs Fix`、`Blocked`、`Invalid State`（`Ready for Review` 仅兼容旧输入） |
| Alignment | `Aligned`、`At Risk`、`Locally Compliant, Globally Misaligned`、`Owner Review Required` |
| Stage review | `Not Reviewed`、`Passed`、`Needs Fix`、`Blocked` |
| QA decision | `Not Reviewed`、`Accepted`、`Accepted With Risk`、`Failed`、`Blocked`、`Not Required` |
| Project | `Active`、`Needs Fix`、`Blocked`、`Accepted`、`Accepted With Risk`、`Invalid State` |
| Delivery class | `Runtime`、`Contract`、`Governance`、`Artifact`、`Mixed` |

不得把 Contract milestone 说成运行能力已实现，不得把截图说成交互通过，不得把 build 说成可用性通过，也不得把 Stage Reviewer 当成 Independent QA。

## 自主推进与验收

当 `acceptance_mode: Layered`：

- Controller 可在一个 Packet 中授权多个有界阶段；
- Developer 每轮成功后无需等待用户再次提示；
- Stage Reviewer 可通过阶段，或在同一 Packet / Work Order 退回 `Needs Fix`；
- Standard / Full 终局只能是 `Ready for Independent Acceptance`；
- Independent QA 只接收验收项、diff、命令、原始证据、限制和目标链接，不把 Developer 希望的结论当证据。

Lite 只有在 `qa_required: false`、工作局部可逆、自动与功能证据都通过且无重大限制时才能自验收。

重复风险必须触发治理：同一重大风险连续携带两次，或连续三次正式 `Accepted With Risk`，继续扩张前必须做 Direction Alignment。

详见 `{baseDir}/references/zh-CN/controller-qa.md`。

## 对齐与重新规模

每阶段做轻量目标链接检查。阶段 3、6、10，或 authority fingerprint 改变、范围增长超过 20%、重复无进展失败、绿灯背后的用户流程失败、出现受保护方向时，立即做正式对齐。

Direction Alignment 不改写目标。目标变化要先独立做 Rebaseline 决策，再独立做 Planning / Dispatch。

预计超过 20 小时的工作必须拆成独立有价值的 Program，或返回 Owner 重基线。禁止授权无人复核的 30-40 小时连续执行。

## 精简读取与文档

正常治理只读：

1. Active Packet；
2. fingerprint 改变时才读其权威来源；
3. 当前 Work Order 或最新交付增量；
4. 必需证据；
5. 最近三至五条 Loop。

Audit 可以扩大读取，但必须只读并使用明确上下文预算。禁止把审计级上下文带进每个执行循环。

对于高输出调查、日志、验证或独立 QA，应授权隔离 Worker，而不是扩大协调 Agent 的上下文。默认最多三个活跃 Worker、一个协调写者、不重叠写入范围、以 fingerprint 加必要摘录共享权威，并只回传摘要与证据。小型或高耦合工作若启动和重读成本更高，不应委派。

授权多 Agent 委派时，阅读执行 Skill 的 `{baseDir}/../agent-loop-engineering/references/zh-CN/isolated-delegation.md`。

只有持久权限边界、Owner 决策、最终独立 QA、跨团队交接、正式重基线或归档边界才创建新文件。Standard 通常只需要 Active Packet、Loop Runs、必要时一份合并 Work Order 和一份最终 QA Decision。

详见 `{baseDir}/references/zh-CN/governance-profiles.md`。

## 反内卷控制

治理有一种特定的失效方式：它持续产出看起来正确的治理产物，而产品停止前进。要看比值，不看动机。

- **文档预算。** 活跃治理文档应保持一次可读完的规模。超过后把历史移入 `Docs/archive/YYYY-MM.md`，只保留当前权威在线。
- **文档／代码信号。** 若文档数量或体积明显超过源码，或某个汇报周期只产出文档而没有代码改动和新的已验证行为，就停止扩张治理，并把这种失衡作为结论上报。一个只有几行代码却配了几百份治理文档的项目，是治理失败，不是文档成就。
- **归档靠移动。** 被取代的目标、旧基线和已关闭循环一律移动，不靠批注。禁止在生效的权威文件里写 `Superseded`、`CURRENT OVERRIDE` 或「本段作废」；读者不应该被迫重建哪一层才是当前。
- **重基线是追加。** 目标变更写一份新的 `REBASELINE-<日期>.md`，并在同一次改动中归档旧基线。
- **`Accepted With Risk` 必须有出口。** 每个此类判定都要带具体解锁条件、责任人和日期。三者缺一，它就不是带风险的验收，而是挂着绿牌的未决阻塞。已 Accepted 但从未发布属于治理缺陷，必须上报。
- **先减后加。** 新方向进来时，先说清楚要砍掉或暂停什么，再授权任何新工作。新范围是范围蔓延最强的诱饵，而一个组合只有靠删除才会变健康。

详见 `{baseDir}/references/zh-CN/anti-involution.md`。

## 必须门禁

- 目标、范围、Non-Goals、验收证据、写入边界和唯一下一步不一致时不得执行。
- 当前权限冲突时不得写 Bootstrap Packet。
- Standard / Full 不得由同一 Agent 的 Stage Review 最终验收。
- QA Failed 返回同一 Milestone / Work Order 做有界修复。
- 核心流程失败、主要环境缺失或用户流程未验证时不得使用 `Accepted With Risk`。
- 诊断分片不得静默替代原有全量回归门禁。
- 目标、Non-Goals、受保护架构或数据、生产、凭证、部署、付费、破坏性或不可逆事项需要 Owner 决策。
- 阶段 10 必须接受、返修、拆分、重基线或停止。
- 目的、排除项、完成条件和主用户流程有任何一项无法用一句话说清时不得授权。答不出「怎样算做完」是停止信号，不是可以推迟到执行中去问的问题。
- 活跃治理文档集不得无归档地增长；当它不再能一次读完时，先归档再新增。
- 没有解锁条件、责任人和日期，不得记录 `Accepted With Risk`。
- 已验收但从未发布的项目不得视为完成，必须作为未决发布阻塞上报。

## 校验

使用执行 Skill 的精简校验器：

```text
node <agent-loop-engineering>/scripts/validate-loop-state.mjs --workspace <项目路径> --summary --max-findings 20
```

只有旧日志迁移本身是任务时才使用 `--strict-history`。数千条旧字段缺失必须按类别聚合，不逐行输出。

校验执行层 Markdown 文件上的 CDH 握手 front-matter：

```text
node {baseDir}/scripts/validate-handshake-frontmatter.mjs --file <.agent-state/.../HANDOFF.md> [--json]
```

## 输出合同

治理回复结尾使用：

```text
模式：
当前准备度/状态：
交付类别：
决定：
原因：
现在做：
以后做：
暂时不做：
需要 Owner 决定：
下一份证据：
创建或更新文件：
```

QA 必须写验收项、证据等级、结论、修正、负责人和复验。内容应让非技术 Owner 可以直接使用。
