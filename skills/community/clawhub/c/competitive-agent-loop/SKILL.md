# Competitive Agent Loop — SKILL.md (v2.0.1)
> 自动加载，不需要手动触发
>
> **v2.0.1 修订（2026-08-06）：** 二次全流程时序与一致性校验——修正 2.3 VRAM 约束中编码模型归属错误（原误标 35B-A3B 为"编码代理独占"，实际编码模型为 27B-MTP-CODER / UD-coder，并补充 35B-A3B 为 MoE 稀疏激活的说明）；澄清 2.6 失活检测"无响应"定义（含 heartbeat 刷新语义）；规范化 3.3 复杂度公式（明确输入变量与分级阈值）；4.2 门禁凭证表加注"核验步骤本身不产出凭证"；4.6/4.8/4.9 统一 PASS/RETRY 决策语义与迭代上限术语；5.2 补齐 workboard_read / workboard_release API 定义；6.5/6.6 区分 Worker/Planner 侧动作与角色职责；6.9 审查决策代码按 5.4 状态流转重写；9.3 人工介入条件与 0-10 分制对齐。
>
> **v2.0.0 修订（2026-08-06）：** 全流程时序一致性校验与结构优化——补齐阶段D 详细步骤、门禁凭证表与详细流程严格一一对应、统一状态流转表与打分尺度、修正卡片归属/领取规则（派发制）、澄清 sessions_send 超时语义。

## 1. 技能概述

### 1.1 核心架构（分离式多 Agent 体系）

**Planner（规划）/ Coder（编码）/ Checker（审查）/ Memowriter（记录）四角色分离：**

- 每个角色是**独立的 configured agent**，有自己的 QQ 主会话
- 调度时用 `sessions_send` 直接发消息到该 agent 的 QQ 主会话（如 `agent:coder:qqbot:direct:3512d704...`），让它在自己会话里执行，QQ 聊天全程可见
- **⚠️ 禁止用 `sessions_spawn`：** 它创建的永远是 subagent 会话（`agent:xxx:subagent:...`），只借用模型配置在后台跑，QQ 里看不到任何记录，且容易丢失执行上下文（2026-08-05 实测：subagent 跑 31 分钟 0 输出失败）
- **串行执行：** RTX 4090 (24GB) VRAM 限制要求编码代理和审查代理不能并行
- **Workboard 集成：** 任务持久化追踪，卡片归属在建卡时锁定（派发制，无主动认领/竞争）

### 1.2 调度与执行原则

| 原则 | 说明 |
|------|------|
| 派发制 | 卡片归属在建卡时由 `agentId` 锁定，Planner 用 sessions_send 派发到对应 agent，Worker 只领取**派发给自己名下**的卡，不存在主动认领/竞争 |
| QQ 全程可见 | 所有执行经各 agent 的 QQ 主会话，sessions_send 派发，禁止 sessions_spawn |
| 串行执行 | 编码代理 + 审查代理互斥（VRAM 约束），通过 Workboard 状态机控制 |
| 状态留痕 | 跨代理信息交换必须走 workboard 评论，禁止文件系统/内存直接共享状态 |

## 2. 配置概览

### 2.1 Agent 模型分配

| 角色 | 主模型 | 兜底模型 |
|------|--------|----------|
| main / planner（主/规划） | ollama/Qwen3.6-35B-A3B-MTP | ollama/Qwen3.6-27B-MTP -> ollama/Qwen3.6-27B-UD:latest -> deepseek/deepseek-v4-flash |
| coder / generator（编码/生成） | ollama/Qwen3.6-27B-MTP-CODER | ollama/Qwen3.6-27B-UD-coder:latest -> qwen3.6:27b -> ctyun/glm-5 |
| checker / evaluator（审查/评估） | Qwythos（首选） | 主模型可用时优先 |
| memowriter（记录） | ollama/qwen3.5:9b | ollama/qwen3.6:4b |

**模型参数说明：**
- 通用模型（MTP/UD）：temperature=0.6, presence_penalty=0, repeat_penalty=1.1, num_predict=16384
- 编码模型（CODER/UD-coder）：temperature=0.4, presence_penalty=0, repeat_penalty=1.1, num_predict=16384
- 统一 num_ctx=131072（128k），全部显式设置采样参数，避免默认值导致工具调用故障

### 2.2 兜底链策略

- **链 A（主/规划）：** Qwen3.6-35B-A3B-MTP -> Qwen3.6-27B-MTP -> Qwen3.6-27B-UD:latest -> deepseek/deepseek-v4-flash
- **链 B（编码/生成）：** Qwen3.6-27B-MTP-CODER -> Qwen3.6-27B-UD-coder:latest -> qwen3.6:27b -> ctyun/glm-5
- **链 C（审查/评估）：** Qwythos -> 主模型兜底（main 主模型 Qwen3.6-35B-A3B-MTP）
- **链 D（记录）：** qwen3.5:9b -> qwen3.6:4b

### 2.3 VRAM 约束（RTX 4090 24GB）

| 模型 | 显存占用 | 归属 |
|------|---------|------|
| Qwen3.6-27B-MTP-CODER / UD-coder | 约 ~20GB | 编码代理独占（大模型串行） |
| Qwythos | 约 ~6GB | 审查代理独占 |
| qwen3.5:9b | 约 ~7GB | 记录代理 |
| Qwen3.6-35B-A3B-MTP（planner 主模型） | MoE 稀疏激活（3B active），占用小 | 规划/调度，串行加载不冲突 |

- **串行规则：** 编码代理和审查代理不能并行（~20GB + ~6GB = ~26GB > 24GB 显存上限），通过 Workboard 状态机互斥
- **宿主模型亲和规则：** 父会话使用本地 Ollama 时，派生的代理必须使用相同模型

### 2.4 兜底触发条件

1. VRAM 溢出 — nvidia-smi 检测到显存不足
2. Provider 超时 — Ollama/云端 API 超时或不可达
3. 压缩失败 — 上下文溢出自动压缩失败，降级模型
4. 质量门 — 审查代理反复失败且当前模型无法改进

### 2.5 不应作为兜底目标的模型（太慢）

- qwen2.* 系列（推理慢，质量不稳定）
- llama3.* 8B（编码能力不足）
- mistral.* 7B（代码生成质量差）

### 2.6 超时与熔断策略

| 对象 | 策略 |
|------|------|
| 编码/审查代理 | **无固定执行超时** — 复杂模块迭代可能耗时数小时/数天；由质量门控制进度，而非时间限制 |
| 记录代理 | 600 秒（10 分钟）— 文档生成通常较快 |
| 平台熔断 | 派生会话挂起 > 30 分钟无输出，网关可能终止（平台默认） |
| 技能侧失活检测 | 无响应 > 30 分钟的会话标记供人工审查（**不自动终止**，与平台熔断相互独立） |

> **⚠️ sessions_send 超时语义（重要澄清）：** `timeoutSeconds` 是等待 Worker **首次确认回复**的时间（建议 300s），**不是任务执行时限**。长任务 Worker 收到派发消息后应尽快回复"已收到，开始执行"，实际产出通过 workboard 回填；Planner 用 workboard_list 跟踪完成状态，不依赖 sessions_send 等待结果。
>
> **⚠️ "无响应"定义：** 失活检测与平台熔断中的"无响应"指该会话在阈值时间内**既未输出任何消息、也未调用 workboard_heartbeat 刷新**。长任务每 10-15 分钟 heartbeat 即视为活跃，不受 30 分钟限制；"无固定执行超时"指不限制任务总时长，而非允许长期静默。

### 2.7 通知策略

- **心跳：** 不主动推送进度更新（避免噪音）。仅在失败或完成时推送
- **完成时：** 推送结果到今日任务面板（today-task）
- **失败时：** 立即通知并附带错误原因

## 3. 触发条件与任务分类

### 3.1 触发条件

接收满足以下条件的任务时自动应用：
1. **编程/开发任务** — 涉及代码生成、审查或调试
2. **复杂度 >= 中等** — 多文件修改或需要测试验证
3. **目标明确** — 有可衡量的验收标准

### 3.2 任务分类规则

| 复杂度 | 条件 | 处理方式 |
|--------|------|----------|
| 低 | 单文件编辑，< 50 行 | 直接执行（不进入循环） |
| 中 | 多文件或需要测试 | **双方案质量门评估**（阶段B 生成 2 个方案） |
| 高 | 架构设计或大型重构 | **三方案深度质量评估 + 人工审查门**（阶段B 生成 3 个方案，阶段C 触发人工审查） |

### 3.3 复杂度评估公式

输入变量（任务进入循环前由 Planner 评估）：

| 变量 | 含义 | 取值 |
|------|------|------|
| fileCount | 改动文件数 | 整数 |
| testRequired | 是否需要测试验证 | true / false |
| architectureChange | 是否涉及架构变更 | true / false |
| unknownDependencies | 是否存在未知依赖 | true / false |

```text
score = fileCount × 2
      + (testRequired ? 3 : 0)
      + (architectureChange ? 5 : 0)
      + (unknownDependencies ? 4 : 0)

分级：score ≤ 5      -> 低复杂度（直接执行，不进入循环）
      6 ≤ score ≤ 12 -> 中复杂度（阶段B 双方案）
      score > 12     -> 高复杂度（阶段B 三方案 + 阶段C 人工审查门）
```

## 4. 执行流程（阶段门禁 · 强制分步）

### 4.1 阶段门禁机制

> **🔒 阶段门禁机制（防跳步核心）：** 每个阶段结束必须产出**可验证的完成凭证**，Planner 逐项核验通过后才能进入下一阶段。**凭证不齐 = 阶段未完成 = 禁止进入下一阶段，也禁止提前开展下一阶段的工作。** 任何 Agent 都无权自我宣称"差不多了，先干起来再说"。

**冲刺定义：** 一个冲刺 = 阶段 A→D 一轮完整循环。跨冲刺总迭代上限 5 轮（见 4.8）。

### 4.2 阶段门禁凭证表（与详细流程步骤一一对应）

**核验时逐项对照「详细流程」中标注的步骤编号（[A1]~[A6] / [B1]~[B5] / [C1]~[C3] / [D1]~[D3]）核对产出物，严格按详细流程处理。任一凭证缺失即视为阶段未完成，禁止进入下一阶段。**

| 阶段 | 对应步骤 | 完成凭证（缺一不可，逐项核验） | 核验人 |
|------|---------|------------------------------|--------|
| 阶段A | [A1]~[A6] | ① 契约 draft 文件（标注 [DRAFT v1.0]，含目标/架构草图/技术方案/交付标准/依赖项/技术风险）[A1] ② sessions_send 送审调用记录 + 主卡评论"契约 draft v1.0 待审查" [A2] ③ Coder 实质性质疑清单 **或** 明确认可回复（QQ 消息，二选一必产，禁止默认跳过）[A3] ④ 修订版契约文件（v1.1、v1.2...，每轮含 sessions_send 重审 + 主卡评论留痕）[A4] ⑤ 契约终稿文件（去 DRAFT 标记，标注最终版本号 + 双方确认记录）[A5] ⑥ Coder 最终**明确认可回复**（QQ 消息，禁止"应该没问题"替代）[A5] ⑦ 阶段A 全部评论留痕齐全（A2 送审 + A4 每轮修订）[A2][A4] | Planner |
| 阶段B | [B1]~[B5] | ① sessions_send 派发记录（附契约终稿全文或摘要 + "严格按契约实现，禁止引入契约外需求、禁止自行变更方案"指令）[B1] ② 按复杂度要求的实现方案（中=2 个 / 高=3 个，每个方案：代码 + 单测 repo/tests/ + 简要说明）[B2] ③ 方案产物 workboard 评论留痕 [B2] ④ Checker 评分 JSON（单测/集成/回归**分别验证分别打分** 0-10 + 正确性/性能/健壮性/可读性 0-10 + verdict）+ 完整审计报告（repo/doc/reviews/）[B3] ⑤ 最高分方案选择记录 + workboard 评论 [B4] | Planner |
| 阶段C | [C1]~[C3] | ① 质量验证与对比结论（基于契约交付标准对选定方案最终验证）[C1] ② 决策记录（PASS 通过 / RETRY 重试 / BLOCKED 阻塞 + 理由）[C2] ③ 契约更新文件（PASS，进入下一冲刺时产出）**或** 返工指令（RETRY 时产出）[C2] ④ 决策 workboard 评论留痕 [C3] | Planner |
| 阶段D | [D1]~[D3] | ① 文档产物落盘路径（repo/doc/ 下项目/接口/用户文档）[D1] ② today-task 推送记录 [D2] ③ 主卡归档记录（全部子卡 done）[D3] | Planner |

> **注：** 门禁核验步骤（A6 / B5 / C3 / D3）本身不产出新凭证，其职责是逐项核验本表列出的凭证；核验通过以当轮 workboard 评论留痕为据。

### 4.3 每轮动作前自检（防偏离第一步）

开始任何动作前，先回答三个问题，回答不齐禁止动手：
1. **我现在处于哪个阶段？**（A/B/C/D）
2. **上一阶段的门禁凭证齐备吗？**（对照 4.2 门禁凭证表逐项核验）
3. **我即将做的动作，属于当前阶段吗？**（不属于 → 停止，回到当前阶段该做的事）

自检结果必须写进当轮回复/评论，让执行链路可审计。

---

### 4.4 阶段 A：冲刺契约（契约驱动开发）— 强制分步

**核心原则：契约是双方谈判的产物，不是 Planner 单方定稿。**
Planner 只产出**初稿草案**，由 Coder 审查质疑、多轮协商，双方在目标、架构、方案、交付标准上达成共识后，才形成**最终契约**并锁定范围。**本阶段未完成，阶段B 不允许启动，Coder 不允许写任何实现代码。**

**步骤 A1 — 产出初稿草案（Planner）**
- 输入：任务需求（已完成复杂度评估）
- 动作：分析需求，产出**冲刺契约初稿（draft）**，文件明确标注 [DRAFT v1.0]，说明这是待协商提案而非定稿
- 输出：契约 draft 文件（包含目标/架构草图/技术方案/交付标准/依赖项/技术风险）

**步骤 A2 — 送审（Planner → Coder）【关键防跳步点】**
- 动作：必须用 sessions_send 把契约 draft 发送到 **coder 的 QQ 主会话**（agent:coder:qqbot:direct:3512d704...），同时在主卡 workboard_comment 留痕"契约 draft v1.0 待审查"
- **禁止：** 不送审就直接进入下一步；把送审省略为"我觉得 Coder 会同意"
- 输出：sessions_send 调用记录 + 主卡评论

**步骤 A3 — Coder 审查质疑（Coder）**
- 动作：Coder 收到 draft 后，逐项审查并提出**实质性质疑与修改意见**（技术方案合理性、验收标准是否可量化、架构漏洞、依赖风险），通过主卡评论回复
- 若 Coder 无异议，也必须回复**明确认可**（如"契约 v1.0 认可，无异议"），不得默认跳过
- 输出：Coder 的 QQ 回复（质疑清单 或 明确认可）+ 主卡评论留痕

**步骤 A4 — 多轮谈判（Planner ↔ Coder）**
- 每轮：Coder 反馈 → Planner 修订 → 重新送审（sessions_send + 主卡评论留痕）
- 谈判聚焦：目标边界、技术架构、实现方案、交付标准
- 循环直到双方达成共识，或触发人工介入
- 输出：修订版契约（v1.1、v1.2...）+ 每轮评论留痕

**步骤 A5 — 范围锁定（双方确认）**
- 动作：双方共同认可后，Planner 产出**契约终稿**（去掉 DRAFT 标记，标注版本号和双方确认记录）
- **必须有 Coder 的最终明确认可回复**（QQ 消息）作为凭证，禁止用"应该没问题"替代
- 输出：契约终稿文件 + Coder 认可回复记录

**步骤 A6 — 阶段A 门禁核验（Planner）**
- 逐项核对 4.2 门禁凭证表：终稿文件 ✅ / Coder 明确认可 ✅ / workboard 留痕 ✅
- 全部通过 → 阶段A 完成，才能创建阶段B 子卡并派发
- 任一缺失 → 回到对应步骤补齐，**不得带病进入阶段B**

> **⚠️ 禁止（阶段A 防跳步红线）：**
> - 禁止 Planner 独自写完全部内容后直接交给 Coder"盖章确认"——必须真实送审、真实谈判
> - 禁止跳过 A2 直接开始编码——**Coder 在收到阶段B 派发任务前，不得编写任何实现代码**
> - 禁止把"时间紧"作为跳过谈判的理由——跳步造成的返工成本远高于谈判成本

**冲刺契约必须包含：**
- **目标**（要解决什么问题、边界在哪）
- **架构草图**（简要架构图/数据结构）
- **技术方案**（技术路径及选型理由）
- **交付标准**（可验证的验收条件，可量化）
- **依赖项**（所需外部依赖/API）
- **技术风险**（已知风险及缓解措施）

---

### 4.5 阶段 B：多方案竞争 — 强制分步

**阶段B 启动前提：阶段A 门禁已通过（契约终稿 + Coder 认可凭证齐备）。**

**步骤 B1 — 派发实现任务（Planner）**
- 按复杂度级别决定方案数（中=双方案 2 个，高=三方案 3 个）
- 用 sessions_send 派发到 coder QQ 主会话，消息中**必须附上契约终稿全文或摘要 + 明确指令"严格按契约实现，禁止引入契约外需求、禁止自行变更方案"**（模板见 6.6）
- 输出：sessions_send 派发记录

**步骤 B2 — Coder 生成方案（Coder）**
- 严格按已锁定契约，生成 2-3 个不同技术路径的实现方案
- 每个方案交付：代码 + 单测（repo/tests/）+ 简要说明
- 完成后 workboard_complete 回填实现子卡（进入 review），并在主卡评论留痕
- 输出：方案产物 + workboard 评论留痕

**步骤 B3 — Checker 量化打分（Checker）**
- Planner 派发审查卡（agentId=checker）后，Checker 领取并**对每个方案分别打分**（0-10）
- 打分维度：单测/集成/回归**分别验证分别打分**（0-10）+ 正确性/性能/健壮性/可读性（0-10）
- 输出：评分 JSON（标准模板见 8.3）+ 完整审计报告（repo/doc/reviews/）

**步骤 B4 — 方案决策（Planner）**
- 读取分数，选定最高分方案作为**主实现**，进入阶段C 质量门验证与迭代
- 输出：选择记录 + workboard 评论

**步骤 B5 — 阶段B 门禁核验（Planner）**
- 核对 4.2 门禁凭证表：2-3 方案 ✅ / Checker 评分 JSON ✅ / 最高分选择记录 ✅
- 通过 → 进入阶段C；缺失 → 补齐

> 评分与迭代决策（≥7 晋级 / <7 返工 / 迭代上限）统一见 4.8 质量门迭代规则。

---

### 4.6 阶段 C：质量门与迭代控制 — 强制分步

**步骤 C1 — 质量验证与对比结论（Checker）**
- 基于契约交付标准，对阶段B 选定的最高分方案做**最终质量验证**（单测/集成/回归 + 四维度复测），输出质量对比与验收结论
- 高复杂度任务：同时触发**人工审查门**（结论提交老板确认）
- 输出：质量验证与对比结论

**步骤 C2 — 决策（Planner）**
- **PASS（通过）** — 采纳最高分方案作为本冲刺交付；**先更新契约**（产出契约更新文件：记录本冲刺交付结论与下一冲刺目标，作为下一轮阶段A 新 draft 的输入基线），再进入下一冲刺（返回阶段A）
- **RETRY（重试）** — 返回编码代理改进选定方案（每冲刺最多 3 次）：Planner 通过 sessions_send 向 Coder 派发改进任务（附返工指令：BUG 清单 + 修改要求），实现卡 review -> running；Coder 改进后 complete 回填，回到 C1 复测
- **BLOCKED（阻塞）** — 需要人工介入
- 输出：决策记录（PASS/RETRY/BLOCKED + 理由）+ 契约更新文件或返工指令

**步骤 C3 — 阶段C 门禁核验（Planner）**
- 核对 4.2 门禁凭证表：质量对比结论 ✅ / 决策记录 ✅ / 契约更新文件或返工指令 ✅
- 通过/重试都必须在 workboard 评论留痕后才算完成

### 4.7 阶段 D：归档 — 强制分步

**阶段D 启动前提：阶段C 决策为 PASS（本冲刺交付已锁定）。**

**步骤 D1 — 文档产出（Memowriter）**
- 项目主体完成后，产出/完善文档交付物：项目文档、接口文档、用户文档
- 项目变更、修改调整时，及时更新对应文档
- 输出：文档落盘 repo/doc/（项目/接口/用户文档）

**步骤 D2 — 完成推送（Memowriter）**
- 通过 today-task 推送完成通知到今日任务面板
- 输出：today-task 推送记录

**步骤 D3 — 阶段D 门禁核验与归档（Planner）**
- 核对 4.2 门禁凭证表：文档落盘路径 ✅ / today-task 推送记录 ✅
- 全部子卡 done → 归档主卡，本轮冲刺结束
- 缺失 → 补齐后再归档

### 4.8 质量门迭代规则（统一）

| 判定 | 条件 | 动作 |
|------|------|------|
| PASS | 审查评分 >= 7（且通过 C1 质量验证） | 采纳方案，更新契约，进入下一冲刺 |
| RETRY | 审查评分 < 7 | 返回编码代理改进选定方案（每冲刺最多重试 3 次），改进后重新打分 |
| BLOCKED | 不可恢复错误 / 需人工决策 | 标记阻塞，通知老板 |

- **总最大迭代：** 跨所有冲刺最多 5 轮（即最多 5 个冲刺），防止死循环
- **卡住判定：** 同一方案连续 3 轮重试无进展（评分无改善）时需人工介入
- **无固定超时：** 迭代持续到质量阈值达标或达到最大重试次数，由质量门控制进度

### 4.9 执行框架速览

```
0. 阶段定位：明确当前阶段 + 核验上一阶段门禁凭证（缺失 -> 先补齐，禁止前进）
1. 接收任务 -> 复杂度评估 -> 任务分类：
   - 低复杂度 -> 直接执行，不进入循环
   - 中/高复杂度 -> 进入冲刺循环（步骤 2-5）
2. 阶段A（冲刺契约）：产出初稿 [A1] -> sessions_send 送审 Coder + 主卡评论 [A2]
   -> Coder 审查质疑 [A3] -> 多轮谈判修订 [A4] -> 范围锁定（终稿 + Coder 明确认可）[A5]
   -> 门禁核验 [A6]
3. 阶段B（多方案竞争）：派发（附契约 + 指令）[B1] -> Coder 生成 2-3 个方案 [B2]
   -> Checker 分方案打分 + 审计报告 [B3] -> 选定最高分方案 [B4] -> 门禁核验 [B5]
4. 阶段C（质量门与迭代）：Checker 质量验证与对比结论 [C1]
   -> Planner 决策 PASS/RETRY/BLOCKED [C2] -> 门禁核验 [C3]
5. 阶段D（归档）：Memowriter 产出文档 [D1] -> today-task 推送 [D2]
   -> Planner 核验并归档主卡 [D3]
6. 决策回路：
   - PASS -> 本冲刺完成，更新契约进入下一冲刺（返回步骤 2，计入总迭代）
   - RETRY -> 返回阶段C 重试循环（Planner 派发改进任务给 Coder -> Checker 复测，每冲刺最多 3 次）
   - BLOCKED -> 人工介入
7. 总迭代上限：跨所有冲刺最多 5 轮；同一方案连续 3 轮重试无进展 -> 人工介入
```

## 5. Workboard 集成 - Agent间任务分派与通信规范

### 5.1 看板管理

**创建/更新看板：**
```javascript
await _workboard.workboard_board_create({
  id: "my-project",              // 唯一看板标识
  name: "My Project",            // 显示名称
  description: "项目描述",
  icon: "board",
  color: "blue",
  defaultWorkspace: {
    kind: "dir",                  // scratch | dir | worktree
    path: "/绝对/路径/工作区"
  },
  orchestration: {
    autoDecompose: true,          // 自动拆解就绪卡片
    autoDecomposePerDispatch: 10, // 每次分派最大拆解数
    defaultAssignee: "main"       // 默认分派人
  }
});
```

**列出所有看板：**
```javascript
await _workboard.workboard_boards({});
// -> { boards: [{ id, name, icon, status, activeCards, totalCards }] }
```

### 5.2 卡片生命周期 - 完整 API

#### 1. workboard_create - 创建任务卡片
**用途：** 规划代理创建主任务/编排卡，或拆解时创建子任务

```javascript
const card = await _workboard.workboard_create({
  title: "搭建愤怒小鸟 H5 游戏",    // 必填
  notes: "验收标准...\n技术风险...",
  status: "ready",                  // ready | running | review | done | blocked
  priority: "high",                 // low | normal | high | urgent
  labels: ["game", "h5"],           // 标签数组
  agentId: "main",                  // 分派的代理（归属在建卡时锁定）
  boardId: "my-project",            // 目标看板
  tenant: "personal",               // 命名空间
  skills: ["competitive-agent-loop"] // 推荐技能
});
// -> { id, token, ... }  // token 为建卡时返回的操作令牌
```

#### 2. workboard_claim - 领取被派发的卡（获取操作令牌）
**用途：** 卡片归属在建卡时已由 `agentId` 锁定（**派发制，无主动认领/竞争**）。Worker 收到 Planner 的 sessions_send 派发后，调用 claim 领取**自己名下**的卡并获取操作令牌，将卡置为 running。**若卡不在自己名下，claim 应被拒绝。**

```javascript
const claim = await _workboard.workboard_claim({ id: cardId });
// -> { tokenId, cardId, status }  // tokenId 用于后续持卡操作（传 token 字段）
```

#### 3. workboard_decompose - 拆解卡片为子任务
**用途：** 规划代理将大任务拆分为子卡，每个子卡指定 agentId（归属锁定）

```javascript
await _workboard.workboard_decompose({
  id: cardId,
  token: tokenId,                   // 父卡令牌（建卡时获取）
  summary: "分解为4个子阶段",
  completeParent: true,             // 自动标记父卡完成（编排）
  children: [
    { title: "阶段A: 冲刺契约", agentId: "main" },
    { title: "阶段B: 多方案实现", agentId: "coder" },
    { title: "阶段C: 质量门审查", agentId: "checker" },
    { title: "阶段D: 归档", agentId: "memowriter" }
  ]
});
```

#### 4. workboard_comment - 添加评论（跨代理通信）
**用途：** 代理在卡片上留下沟通记录，实现跨代理同步（**跨代理信息交换必须走评论**）

```javascript
await _workboard.workboard_comment({
  id: cardId,
  body: "规划代理: 冲刺契约 v1.0 草稿待审查",
  token: tokenId
});
// 编码代理回复:
await _workboard.workboard_comment({
  id: cardId,
  body: "编码代理: 建议 Matter.js CDN + Canvas2D 兜底。标准 3 需量化。",
  token: tokenId
});
```

#### 5. workboard_heartbeat - 心跳保活
**用途：** 长时间任务中刷新存活状态，防止被诊断系统标记为失效

```javascript
await _workboard.workboard_heartbeat({
  id: cardId,
  token: tokenId,
  note: "阶段B进行中 - 编码代理生成两个方案"
});
// 建议：长时间任务每 10-15 分钟调用一次
```

#### 6. workboard_complete - 完成卡片
**用途：** 代理完成任务，提交结构化成果（摘要 + 证明 + 产物）

```javascript
await _workboard.workboard_complete({
  id: cardId,
  token: tokenId,
  summary: "阶段A完成: 冲刺契约 v2.0 已确认",
  proof: {
    status: "passed",               // passed | failed | skipped | unknown
    note: "验收标准与技术方案已审查"
  },
  artifacts: [
    { label: "sprint-contract-v2.md", path: "/路径/文件.md" }
  ]
});
```

#### 7. workboard_block - 阻塞卡片
**用途：** 代理遇到不可恢复的问题时标记卡片并释放领取（归还给 Planner 重新派发）

```javascript
await _workboard.workboard_block({
  id: cardId,
  token: tokenId,
  reason: "显存溢出 - 编码模型加载失败，所有兜底已耗尽"
});
```

#### 8. workboard_list - 列出卡片
**用途：** 查看当前看板/代理的卡片状态，用于路由决策

```javascript
await _workboard.workboard_list({ limit: 50 });               // 所有卡片
await _workboard.workboard_list({ agentId: "coder" });        // 按代理
await _workboard.workboard_list({ status: "running" });       // 按状态
await _workboard.workboard_list({ boardId: "my-project" });   // 按看板
```

#### 9. workboard_read - 读取卡片详情
**用途：** 读取卡片完整上下文（评论、状态、产物），执行/审查前获取任务详情

```javascript
const card = await _workboard.workboard_read({ id: cardId, token: tokenId });
// -> { id, title, status, agentId, comments: [...], artifacts: [...] }
```

#### 10. workboard_release - 释放卡片
**用途：** 主动释放已领取的卡（归还给 Planner 重新派发），如 Worker 判断自己无法继续

```javascript
await _workboard.workboard_release({ id: cardId, token: tokenId, status: "ready", reason: "..." });
```

### 5.3 卡片归属与领取规则（派发制，无主动认领）

- **建卡时必须在 workboard_create / decompose 里写清 agentId** —— 卡片归属在建卡时锁定，Planner 用 sessions_send 派发到对应 agent 的 QQ 主会话，Worker 领取**派发给自己的卡**。**不存在主动认领/竞争。**
- **阶段A 特例：** 阶段A 子卡归属 main（Planner 自己），Coder 不单独建卡/不领卡——Coder 收到 sessions_send 送审的 draft 后，在**主卡评论**回复质疑/认可即可，评论即凭证（见 4.4 A3）
- worker 通过 `workboard_list(agentId=自己)` 只看到派发给自己的卡，天然隔离
- `workboard_claim` 是原子的（实测确认），只接受领取**自己名下**的卡；若卡不在自己名下，claim 应被拒绝

### 5.4 卡片状态流转

**双卡模型说明：** 阶段B 存在两张独立卡片，状态独立流转，通过评论/评分联动：
- **实现卡**（agentId=coder）：B2 完成后 complete → review，等待审查结果
- **审查卡**（agentId=checker）：Planner 派发后 Checker 领取打分，评分反馈实现卡状态决策；**审查卡打分完成后使命即结束**，后续 PASS/RETRY/BLOCKED 决策均作用于实现卡

| 转换 | 触发方式 | 说明 |
|------|----------|------|
| ready -> running | `workboard_claim()` | Worker 领取被派发的卡并开始工作（agentId 归属已锁定，无竞争） |
| running -> review | `workboard_complete({proof})` | 提交完成待审查 |
| review -> done | 审查通过（PASS，分数 >= 7） | 批准晋级 |
| review -> running | 重试（RETRY，分数 < 7） | 拒绝，返回编码代理改进（最多 3 次/冲刺） |
| running -> blocked | `workboard_block(reason)` | 不可恢复错误 |
| running -> ready | `workboard_release({status:"ready"})` | 释放卡，由 Planner 重新派发 |

### 5.5 代理间通信规范

**核心原则：跨代理信息交换必须经过 Workboard 评论留下痕迹。**

- 规划代理创建卡 -> 写评论 -> 携带契约草稿派发（sessions_send）编码代理
- 编码代理审查契约（阶段A）-> 评论反馈 -> 协商
- 规划代理修订契约 -> 写评论（达成共识）-> 阶段A 完成
- 审查代理打分方案 -> 评论结果

**禁止行为：**
- 不允许跳过评论直接用文件系统或内存共享代理间状态
- 不允许直接操作其他代理负责的卡片（审查场景除外）
- 不允许在长任务中不做心跳

### 5.6 错误处理与恢复

| 场景 | 解决方式 |
|----------|------------|
| 领取令牌过期 | 重新调用 `workboard_claim({id})` 续期 |
| 找不到卡 / ID 错误 | 调用 `workboard_list()` 刷新状态 |
| 代理会话断开 | 网关自动释放过期领取（30分钟），dispatcher 回收后由 Planner 重新派发 |
| 阻塞超时 | 自动触发阻塞状态，通知用户 |
| 派发归属冲突 | 不存在争抢：卡片归属由 agentId 锁定，`workboard_claim` 只接受归属自己的卡 |

### 5.7 循环阶段 × Workboard 集成映射

| 循环阶段 | 规划/协调代理动作 | 执行代理动作 | Workboard 状态机 |
|------------|---------------------------|--------------------|-------------------------|
| 阶段A: 冲刺契约 | 建主卡（agentId=main）-> 产出契约 draft -> sessions_send 送审编码代理 + 主卡评论 | Coder 收到送审后**在主卡评论**回复质疑/认可（不单独领卡） | ready->running(Planner claim) -> running(协商) -> review(提交终稿) |
| 阶段B: 多方案竞争 | 拆实现子卡（agentId=coder）-> 派发编码代理；完成后派发审查卡（agentId=checker） | Coder 领取实现卡 -> 生成方案 -> complete；Checker 领取审查卡 -> 分方案打分 -> 评论结果 | 实现卡: ready->running(实现) -> review(打分)；审查卡: ready->running(审查) -> review(评分完成) |
| 阶段C: 质量门与迭代 | 读取评分 -> 决策 PASS/RETRY/BLOCKED -> 评论留痕 | Checker 对选定方案做质量验证与对比结论（C1） | 实现卡: review -> done(PASS) / running(RETRY) / blocked(BLOCKED) |
| 阶段D: 归档 | 核验文档落盘 + today-task 推送记录 -> 归档主卡 | Memowriter 产出文档 -> today-task 推送 | 全部子卡 done -> 父卡 done(completeParent) |

## 6. Agent 调度编排流程（task + Workboard 打通）

> 能力说明：task 调度（llm-task 插件 / Gateway task-tracked run）与 Workboard 插件均为 OpenClaw 自带且已启用。Agent 调度通过「建卡（锁定 agentId）-> 派发 -> 领取执行 -> 完成回填」驱动，task 后台自动追踪每次运行。**卡片归属在建卡时锁定，不存在主动认领/竞争。**

### 6.1 调度总览

```
任务进入 -> Planner 建主卡 -> 拆子卡（agentId 锁定归属）-> sessions_send 派发到 Worker 的 QQ 主会话 -> Worker 领取执行
                -> heartbeat 保活 -> complete 回填 -> Planner 派发审查卡 -> Checker 领取审查
                -> PASS(晋级) / RETRY(返工) / BLOCKED(阻塞) -> 全部 done 归档
```

### 6.2 建看板（初始化）

```javascript
await _workboard.workboard_board_create({
  id: "loop-board",
  name: "竞争式 Agent 循环",
  icon: "loop",
  orchestration: { autoDecompose: true, autoDecomposePerDispatch: 10 }
});
```

### 6.3 建主卡（Planner）

收到任务后，Planner 创建主任务卡，status: ready：

```javascript
const card = await _workboard.workboard_create({
  title: "任务标题",
  notes: "需求描述 + 验收标准 + 技术风险",
  status: "ready",
  priority: "high",
  agentId: "main",                 // 分派给主/规划代理
  boardId: "loop-board",
  skills: ["competitive-agent-loop"]
});
// card.token 为主卡操作令牌（建卡时获取，非认领）
```

### 6.4 拆子卡（阶段划分）

Planner 将主卡拆为子阶段，每个子卡绑定对应 worker agent（归属在建卡时锁定）：

```javascript
await _workboard.workboard_decompose({
  id: card.id,                     // 主卡 id
  token: card.token,               // 主卡 token（建卡时获取，非认领）
  summary: "拆解为 4 个子阶段",
  completeParent: true,            // 子卡全完成时自动标记父卡完成
  children: [
    { title: "阶段A: 冲刺契约", agentId: "main" },
    { title: "阶段B: 多方案实现", agentId: "coder" },
    { title: "阶段C: 质量门审查", agentId: "checker" },
    { title: "阶段D: 归档", agentId: "memowriter" }
  ]
});
```

### 6.5 派发任务 + Worker 领取（QQ 主会话）

Planner 在拆卡时已指定子卡 agentId（归属锁定）。拆卡后用 sessions_send 把任务派发到该 agent 的 QQ 主会话，Worker 领取**自己名下**的子卡并开始工作：

```javascript
// ---- Worker 侧：领取被派发到自己名下的卡（agentId 归属已锁定，不存在竞争） ----
const claim = await _workboard.workboard_claim({ id: childCardId, ttlSeconds: 3600 });

// ---- Planner 侧：发任务到 coder 的 QQ 主会话 ----
sessions_send({
  sessionKey: "agent:coder:qqbot:direct:3512d7045667f4df660228b731965c2", // coder 的 QQ 主会话
  message: "执行阶段B: 实现方案，完成后调用 _workboard.workboard_complete 回填",
  timeoutSeconds: 300   // 等待 Worker 首次确认回复的时间，非执行时限（见 2.6）
});
```

**各 agent 的 QQ 主会话 sessionKey（固定）：**
- coder: `agent:coder:qqbot:direct:3512d7045667f4df660228b731965c2`
- checker: `agent:checker:qqbot:direct:3c2515212bbbed28731e70ef0dd5af4f`
- memowriter: `agent:memowriter:qqbot:direct:fa5ee4a0bb61c7da1cf68a3cc87fc801`

**要点：**
- coder 在自己会话里执行，老板在 coder 的 QQ 聊天窗口全程可见执行记录
- sessions_send 同步等待回复，Worker 收到后应**先回复确认**（"已收到，开始执行"），任务完成通过 workboard_complete 回填
- 任务内容要包含：子卡 ID、任务步骤、完成后如何回填（workboard_complete）

### 6.6 派发消息模板（前置门禁检查 + 防链断裂）

**⚠️ 任务消息必须要求 worker 按 loop 技能执行（防链断裂）：**

> 模板适用于阶段B/C/D 的执行派发（Planner → Coder/Checker/Memowriter）。**阶段A 的 sessions_send 仅用于向 Coder 送审契约 draft（见 4.4 A2），不适用本模板。**

Planner 发出的任务消息必须包含明确指令，要求 worker 严格按 competitive-agent-loop 技能执行对应阶段步骤，禁止 worker 自己另起逻辑、跳步或自由发挥：

```
【任务：阶段X - <角色名> <动作>】

按 competitive-agent-loop 技能执行，不要自行处理其他逻辑或跳步。

## 你的子卡
- 卡片ID: <childCardId>
- 标题: <阶段X标题>
- 归属: <agentId>

## 前置门禁检查（先做，不通过禁止开工）
- 确认上一阶段（<上一阶段名>）的门禁凭证齐备（对照 SKILL.md 门禁凭证表逐项核验）
- 凭证不齐 -> 回复 Planner 缺失项，拒绝开工，禁止自己补做或跳过上一阶段
- 凭证齐备 -> 在回复中声明"门禁通过"，再继续

## 执行步骤（严格按 loop 技能，按序执行）
0. 先回复：当前所处阶段 + 上阶段门禁凭证核验结果
1. workboard_claim 领取子卡 <childCardId>（卡片归属已锁定给本 agent，只领取派发给自己的卡）
2. workboard_list 读取主卡/子卡上下文（boardId: <boardId>）
3. 按 loop 技能对应阶段执行（只做本阶段该做的事，禁止越阶段）：
   - 阶段A（Coder）：审查契约初稿 -> 提出实质性质疑（技术方案/验收标准/架构/依赖风险）-> 参与谈判 -> 明确认可或要求修订。禁止直接盖章确认，禁止在本阶段写任何实现代码
   - 阶段B（Coder）：严格按已锁定契约实现（禁止引入契约外需求、禁止自行变更技术方案）
   - 阶段B（Checker）：对每个实现方案分别打分（0-10）+ 完整审计报告
   - 阶段C（Checker）：对选定的最高分方案做最终质量验证与对比结论
   - 阶段D（Memowriter）：产出文档并归档
4. workboard_comment 在主卡上留痕（跨代理通信必须走评论，写明你的明确结论）
5. workboard_complete 回填子卡（summary + proof + artifacts）

## 契约内容摘要
<关键上下文：契约/验收标准/任务说明>

完成后回复结果，并注明：你完成了哪个步骤、产出了什么凭证。
```

**loop 链断裂的典型表现（禁止）：**
- worker 收到任务后自己另起炉灶，不领取子卡、不回填 → 子卡永远 todo，主卡 blocked
- worker 跳步直接产出，不在 workboard 留痕 → 跨代理状态丢失
- worker 用 sessions_spawn 再派生别的会话 → 执行脱离 QQ 主会话，链路不可见

**正确行为：** worker 只执行自己阶段对应的 loop 步骤，完成后回填，把控制权交回 Planner（主会话）继续下一阶段。

### 6.7 执行中保活

长时间执行时刷新心跳，防止被标记 stale：

```javascript
await _workboard.workboard_heartbeat({
  id: childCardId,
  token: claim.tokenId,   // 领取时返回的令牌，用于持卡操作
  note: "阶段B进行中 - 已生成方案1，正生成方案2"
});
// 建议：长任务每 10-15 分钟调用一次
```

### 6.8 完成回填

Worker 完成子卡，提交结构化成果：

```javascript
await _workboard.workboard_complete({
  id: childCardId,
  token: claim.tokenId,
  summary: "阶段B完成: 生成 2 个实现方案",
  proof: { status: "passed", note: "实现已完成" },
  artifacts: [{ label: "solution1.md", path: "/路径/solution1.md" }]
});
```

### 6.9 审查决策

**阶段B：** Planner 派发审查卡（agentId=checker）后，Checker 领取并分方案打分：

```javascript
// ---- Checker 侧：领取审查卡，读取卡片上下文，完成打分后回填 ----
const c = await _workboard.workboard_claim({ id: reviewCardId, ttlSeconds: 3600 });
const card = await _workboard.workboard_read({ id: reviewCardId, token: c.tokenId });  // 读卡片上下文
// 打分结果写入 repo/doc/reviews/，并在审查卡评论留痕
await _workboard.workboard_comment({
  id: reviewCardId, token: c.tokenId,
  body: "Checker: 评分 JSON + 审计报告已产出（repo/doc/reviews/），实现卡可进入阶段C"
});
await _workboard.workboard_complete({
  id: reviewCardId, token: c.tokenId,
  summary: "审查完成: 分方案评分 + 审计报告",
  proof: { status: "passed", note: "评分与审计报告已提交" },
  artifacts: [{ label: "review-json", path: "repo/doc/reviews/review.json" }]
});
```

**阶段C：** Planner 依据评分决策，决策作用于**实现卡**的状态流转（见 5.4）：

```javascript
// ---- Planner 侧：读取评分，按 4.8 规则决策（作用于实现卡） ----
if (score >= 7) {
  // PASS -> 实现卡 review -> done（批准晋级），进入 C1 质量验证后归档
} else if (score < 7 && retryCount < 3) {
  // RETRY -> 实现卡 review -> running（返回 coder 改进，每冲刺最多 3 次）
  // 通过 sessions_send 向 coder 派发改进任务（附返工指令），改进后回到 C1 复测
} else {
  // BLOCKED -> 实现卡 -> blocked（不可恢复错误 / 重试耗尽），通知老板
  await _workboard.workboard_block({ id: implCardId, token: plannerToken, reason: "..." });
}
```

### 6.10 任务追踪说明

- 每次 autonomous 启动（Card -> Run）都会挂到 Gateway task 台账，workboard 卡自动链接 task/run/session
- Planner 可通过 workboard_list 轮询查看各卡状态，不必单独查 task
- 未完成的卡保持 running，完成/失败/超时自动移向 review 或 blocked

### 6.11 协议约束

- Worker 停机前必须调用 workboard_complete 或 workboard_block，否则 worker_log / protocol_violation 会标记违规
- 跨 Agent 信息交换必须走 workboard_comment 留痕，禁止用文件系统/内存直接共享状态
- 长时间任务不做 heartbeat 会被 stale 检测标记

## 7. 调度与执行架构（CPU 调度 / GPU 执行分离）

### 7.1 双 Ollama 节点架构（核心设计）

| 层级 | 节点 | 用途 | 模型 |
|------|------|------|------|
| **调度层** | 192.168.50.10:11434（本机 NAS，纯 CPU） | Planner 事件驱动派生、workboard 查卡/派发/dispatch、dispatcher 兜底 | ollama_nas/qwen3.5:4b |
| **执行层** | 192.168.50.5:11434（GPU Ollama） | 真实编码、审查、文档产出 | MTP / UD / CODER / Qwythos / qwen3.5:9b |

**设计原则：调度与执行物理隔离，零竞争。**
- 调度动作（查卡、claim 领取、dispatch、读事件）走 **CPU 4b**，不占 GPU
- 真实任务走 **GPU 模型**，专注推理质量
- 避免两个模型在同一 GPU 上争抢显存/加载，杜绝"调度挤掉执行"

> **模型分工澄清：** Planner 的规划/决策推理走主模型（Qwen3.6-35B-A3B-MTP，见 2.1）；查卡、派发、dispatch 等**调度动作**走 CPU 4b，不占用 GPU。两者不冲突。
>
> 注：192.168.50.10 既是 OpenClaw 运行主机（本机），也是 CPU 调度 Ollama 节点。Ollama 需保持服务常驻，qwen3.5:4b 建议 keep_alive=1h 常驻内存（16G 充足，保证轮询即点即用）。

### 7.2 keep_alive 策略

| 模型 | 节点 | keep_alive | 理由 |
|------|------|-----------|------|
| ollama_nas/qwen3.5:4b | CPU 192.168.50.10 | 1h | 高频轮询，常驻避免重复加载 |
| GPU 各执行模型 | GPU 192.168.50.5 | 1h | 任务执行时常驻，避免频繁换载 |

### 7.3 调度触发机制（事件驱动派生 + dispatcher 兜底）

**核心：loop 执行调度由 Planner 事件驱动派生，不依赖独立 cron 轮询。cron 仅保留一个 dispatcher 做状态机兜底。**

**背景（2026-08-04 修正）：** cron agentTurn 每次会新建完整 isolated agent 会话（加载模型+工具+上下文），在资源受限（CPU 4b / GPU 换载）环境下 attempt-dispatch 阶段易超时；且 main 在处理任务时模型会卸载，systemEvent 也不可靠。故放弃"每 agent 定时轮询"，改为事件驱动派生。

| Cron Job | 周期 | 挂载 | 动作 |
|----------|------|------|------|
| loop-dispatcher-main | 每 10min | main (systemEvent) | workboard_dispatch 兜底状态机（promote 未阻塞卡/回收过期 claim/block 超时） |

**主调度链条（事件驱动，无 cron 参与）：**
```
Planner 接收任务
  -> 复杂度评估 -> 生成冲刺契约初稿草案
  -> workboard_create 建主卡（注明各子阶段的 agentId）
  -> workboard_decompose 拆子卡
  -> 用 sessions_send 直接发任务到各 agent 的 QQ 主会话执行
       （agent:coder:qqbot:direct:3512d704... 等，QQ 全程可见；禁止 sessions_spawn）
  -> 各 worker 执行完 workboard_complete / block 回填
  -> Planner 检查所有子卡 done -> 归档
```

**dispatcher 职责（兜底，非主调度）：**
- 回收过期 claim：worker 崩溃/中断后释放卡片占用，让 Planner 可重新派发
- block 超时任务：长时间无心跳的卡标记阻塞并通知
- promote 未阻塞卡：将满足条件的卡推进到 ready
- 不做 spawn 派生，只维护状态机，保证轻量

**可选手动触发：**
```javascript
await _workboard.workboard_dispatch({});
```

**异常恢复：**
- worker 中断：dispatcher 回收其 claim，Planner 重新派生或人工介入
- 卡死在 running：dispatcher 检测超时 -> block -> 通知
- 模型加载失败：fallback 链自动降级

### 7.4 归属与领取判定规则

- **建卡时必须在 workboard_create/decompose 里写清 agentId**（卡片归属在建卡时锁定，**派发制，不存在主动认领/竞争**）
- worker 通过 `workboard_list(agentId=自己)` 只看到派发给自己的卡，天然隔离
- `workboard_claim` 是原子的（实测确认），用于领取**自己名下**的卡并获取操作令牌；若卡不在自己名下，claim 应被拒绝

### 7.5 心跳保活与异常恢复兜底

- 任务执行中（GPU 模型跑长任务），每 10-15min `workboard_heartbeat` 刷新领取状态
- 防止被诊断系统标记 stale、被 dispatcher 误回收
- **worker cron 异常中断**：dispatcher 回收过期 claim 释放卡，Planner 重新派发（或人工介入）
- **卡死在 running**：dispatcher 检测超时 → block 该卡 → 通知
- **模型加载失败**：fallback 链自动降级

## 8. Agent 职责与数据流转

### 8.1 Planner / Main（规划/调度）— Qwen3.6-35B-A3B-MTP

**职责：**
- 接收任务 → 复杂度评估 → 生成冲刺契约初稿草案
- 建主卡 + 拆子卡（注明每个子卡的 agentId，归属锁定）
- 全局 dispatcher 兜底（cron 跑 workboard_dispatch）
- 协调 PASS/RETRY/BLOCKED 决策
- 逐阶段核验门禁凭证，控制进度

### 8.2 Coder（生成/编码）— Qwen3.6-27B-MTP-CODER / UD-coder

**职责：**
- 领取派发给自己的阶段B 实现卡，按契约生成代码
- **编写单元测试**（放 `repo/tests/`）：单测代码由 Coder 写，Checker 运行验证
- 完成后 `workboard_complete` 提交 artifacts（代码产物路径 + git commit/PR 链接）
- 收到 Checker 的 BUG/返工反馈 → 领取对应修复卡 → 修改推回

**交付物：**
- 代码 → GitHub 仓库（git 管理，如 `repo/src/`）
- 单测案例 → `repo/tests/`
- 短期交互/BUG 简述 → workboard comment
- 详细设计/说明 → `repo/doc/` 对应文件

### 8.3 Checker（审查/测试/评估）— Qwythos

**职责（不止打分，是完整测试人）：**
1. 运行验证：Coder 已写的单测直接跑；缺失的测试案例由 Checker 补充到 `repo/tests/`
2. 全流程测试：单测 / 集成测试 / 回归测试 **分别验证分别打分**（0-10）
3. BUG 排查：查找 BUG、待优化功能点，记录并反馈 Coder
4. 打分离散：0-10，维度正确性/性能/健壮性/可读性 + 单测/集成/回归测试通过率
5. 阶段C：对选定方案做质量验证与对比结论（C1）

**测试环境：**
- 本地 workfiles 目录建立运行环境，走全流程部署、测试，进行集成验证
- 测试代码在 `repo/tests/`

**评分输出（标准 JSON + 完整审计报告）：**
```json
{
  "taskId": "...",
  "solutionId": "...",
  "scores": {
    "unitTest": 8,      // 单测通过率/覆盖（0-10）
    "integrationTest": 7, // 集成测试（0-10）
    "regressionTest": 8,  // 回归测试（0-10）
    "correctness": 8, "performance": 7, "robustness": 8, "readability": 9
  },
  "verdict": "PASS|RETRY|BLOCKED",
  "bugs": [{ "id": "BUG-1", "severity": "high", "desc": "...", "repro": "..." }],
  "optimizations": ["..."],
  "recommendations": "..."
}
```

**交付物：**
- 评分 JSON + 完整审计报告 → `repo/doc/reviews/`
- BUG 简述 → workboard comment
- BUG 详情 → `repo/doc/reviews/` 下 BUG 报告文件（含复现步骤）
- **反馈闭环**：Checker 反馈 BUG → Planner 建 BUG 修复卡（agentId=coder）→ Coder 领取修复 → Checker 复测

### 8.4 Memowriter（文档/记录）— qwen3.5:9b

**职责：**
- 在项目主体完成后（阶段C PASS 后），产出/完善文档交付物：项目文档、接口文档、用户文档
- 项目变更、修改调整时，及时更新对应文档
- 通过 today-task 推送完成通知

**交付物：**
- `repo/doc/` 下：项目文档、接口文档、用户文档

### 8.5 数据流转分工总则

| 数据类别 | 存放位置 | 载体 |
|----------|---------|------|
| 项目代码 | GitHub 仓库 | git 管理（`repo/src/`） |
| 测试代码 | GitHub 仓库 | `repo/tests/` |
| 短期交互 / BUG 简述 | workboard | card comment |
| BUG 详情 / 审计报告 / 评分 | GitHub 仓库 | `repo/doc/reviews/` |
| 项目/接口/用户文档 | GitHub 仓库 | `repo/doc/` |
| 任务编排状态 | workboard | 卡片状态机（ready/running/review/done/blocked） |

## 9. 安全与隔离

### 9.1 显存安全规则

1. **串行锁定：** 编码代理 + 审查代理互斥，通过 Workboard 状态机控制
2. **模型亲和：** 父会话使用 Ollama 时，派生代理复用相同模型
3. **失活会话检测：** 若派生会话无响应 > 30 分钟，标记供人工审查（不自动终止；"无响应"定义见 2.6）
4. **兜底降级：** 显存不足时自动切换到轻量模型

### 9.2 执行上下文隔离

- 每个派生会话维护自己的上下文窗口（128k）
- 不共享对话历史 — 仅通过文件系统和 Workboard 交换状态
- 完成/失败自动推送通知；无需轮询

### 9.3 人工介入条件

出现以下情况时暂停并请求老板确认：
- 同一方案连续 3 轮重试后评分仍 < 7 分（RETRY 循环内无改善，达到每冲刺重试上限）
- 编码代理连续失败 3 次且无兜底恢复
- 架构变更影响超出预期（> 5 个文件）
- VRAM 溢出持续存在且兜底链已耗尽
- 阶段C 决策为 BLOCKED
- 高复杂度任务的人工审查门（C1）

### 9.4 sessions_send 用法（推荐，2026-08-05 修订）

```javascript
sessions_send({
  sessionKey: "agent:coder:qqbot:direct:3512d7045667f4df660228b731965c2",
  message: "任务内容...",
  timeoutSeconds: 300   // 等待首次确认回复，非执行时限
})
```

**注意：**
- 调度已有 agent 用 `sessions_send` 发到其 QQ 主会话，QQ 全程可见执行记录
- `sessions_spawn` 只用于纯后台子代理任务（不需要用户可见的场合），它创建的 `agent:xxx:subagent:...` 会话与 QQ 主会话无关；**loop 流程内禁止使用**
- 串行约束依旧生效：编码代理和审查代理不能并行（VRAM 限制）
- 不要给派生会话传递过多上下文 — 保持隔离的上下文窗口干净
