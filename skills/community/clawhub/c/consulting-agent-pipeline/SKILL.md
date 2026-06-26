---
name: multi-agent-pipeline
description: 多Agent协作研究管线 — 将"调研→框架→执行→审核→迭代→交付"的咨询项目工作流抽象为可复制的标准化协议。触发场景：(1) 新项目需要多Agent协作且横跨多个平台（Claude/Codex/Gemini/Minimax），(2) 咨询类交付物需要多轮结构化审核迭代，(3) 需要建立项目状态追踪机制替代散落的进度文档，(4) 需要防止内部代号/敏感信息泄漏到交付物，(5) 需要明确Human决策节点避免Agent过度自主。核心解决的问题：审核意见靠聊天中转导致失真、内部代号泄漏到v4才发现、Human决策点散落在对话中无法追溯。
---

# Multi-Agent Pipeline — 多Agent协作研究管线

> 首钢吉泰安项目（2026-04-09 ~ 04-14）的实战协作经验抽象为可复制工作流。

## 技能定位

**不是什么**：本技能不是通用任务管理工具（task-management），不是单Agent TODO列表，不是LangGraph/CrewAI框架替代品，不是项目管理软件（Gantt/Jira）的替代品。

**是什么**：一套跨平台、多Agent协作的**文件系统协议**——定义如何通过共享文件夹 + 结构化文档实现协作，而不依赖任何特定Agent平台或聊天通道。

**适用项目类型**：
- ✅ 咨询类交付物（PPT/报告/方案文档）
- ✅ 多专题并行调研 → 单一线性产出的项目
- ✅ 需要多轮审核迭代（≥2轮）的对外交付
- ✅ 跨平台Agent协作（Agent不同属一个公司/平台）

**不适用**：
- ❌ 纯软件开发迭代（代码频繁merge/branch，适合用Git工作流而非本技能）
- ❌ 实时通信/客服类项目（需要毫秒级响应，不适合文件交接协议）
- ❌ 单Agent独立完成任务（不需要多Agent协作协议）
- ❌ 高度机密项目（不建议在共享文件系统存储任何项目信息）

## 核心设计原则

1. **Agent-Agnostic**：基于文件系统协议，任何能读/写本地文件的Agent都能参与
2. **Shared State**：PROJECT_STATE.yaml 是唯一的项目状态数据源，消除分散在多个文档中的状态不一致
3. **Structured Handoff**：交接文档使用 YAML frontmatter（机器可解析）+ Markdown 正文八节（人类可读）
4. **Calibrated Autonomy**：Human 决策矩阵决定干预层级，P0/P1/P2 优先级决定自动化程度
5. **Every Handoff Auditable**：每次交接都有文档记录，替代聊天传递，审计可追溯

## 工作流五阶段

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 0: INIT                                               │
│ → Orion: 初始化项目结构 + 填写 PROJECT_STATE               │
│ → 人类审批: 框架方向 + Agent分配 + 禁用词清单               │
└──────────────────────────────┬──────────────────────────────┘
                               │ 人类Gate ✅
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 1: RESEARCH（可并行 Fan-Out）                         │
│ → N个 Research Agent 并行执行专题调研                       │
│ → Orion: 汇总 → research-synthesis.md                       │
│ → 人类审批: 调研质量 + 数据可用性                           │
└──────────────────────────────┬──────────────────────────────┘
                               │ 人类Gate ✅
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 2: FRAMEWORK                                         │
│ → Reviewer Agent: 构建交付物内容框架                        │
│ → 输出: framework-to-execution.handoff.md                  │
│ → 人类审批: 框架方向（如"冒总定调：先出框架去谈"）          │
└──────────────────────────────┬──────────────────────────────┘
                               │ 人类Gate ✅
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 3: EXECUTION                                          │
│ → Execution Agent: 生成 v1 交付物                           │
│ → forbidden-terms-scan.sh: 自动扫描                         │
│ ⚡ Auto Gate: 扫描通过 → 进入审核；不通过 → 退回修复        │
└──────────────────────────────┬──────────────────────────────┘
                               │ Auto Gate ✅
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 4: AUDIT（Generator / Critic 循环，3轮上限）          │
│ Round 1: 方向 + 语气 + 视觉层级                             │
│ Round 2: 完整度 + 合规性 + 数据一致性                        │
│ Round 3: 风险边界 + 禁用词清除                               │
│                                                            │
│ 📊 Calibrated Gate:                                        │
│   全部P2 → Agent自动迭代进入下一轮                          │
│   有P1无P0 → Agent迭代后人类复核                            │
│   有P0 → 人类必须审批修复方案                               │
│   审核通过 → 进入 Phase 5                                  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Human Gate ✅
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 5: DELIVERY                                          │
│ → validate-deliverable.sh: 结构验证                        │
│ → forbidden-terms-scan.sh: 最终扫描                         │
│ → snapshot-dir.sh: 版本快照归档                            │
│ → 人类审批: 最终交付物确认                                  │
└─────────────────────────────────────────────────────────────┘
```

### Human Gate 与 Calibrated Autonomy 速查

| 阶段 | 门控类型 | 触发条件 | 谁操作 |
|------|---------|---------|--------|
| Phase 0→1 | 🔴 Human审批 | 框架+Agent+禁用词确认 | 人类 |
| Phase 1→2 | 🔴 Human审批 | 调研质量通过 | 人类 |
| Phase 2→3 | 🔴 Human审批 | 框架方向确认 | 人类 |
| Phase 3→4 | ⚡ Auto | 禁用词扫描无P0违规 | 脚本 |
| Phase 4 每轮 | 📊 Calibrated | 见上方矩阵 | Agent+人类 |
| Phase 4→5 | 🔴 Human审批 | 审核通过 | 人类 |

## 核心文件速查

| 文件 | 用途 | 谁写/读 |
|------|------|---------|
| `00_pipeline/PROJECT_STATE.yaml` | 项目状态数据库（单一真相源） | Orion写，人类必读 |
| `00_pipeline/FORBIDDEN_TERMS.yaml` | 禁用词清单 | 人类初始化，所有Agent必读 |
| `00_pipeline/AGENT_REGISTRY.yaml` | Agent能力注册表 | Orion维护，分发任务时用 |
| `00_pipeline/DECISION_LOG.md` | 人类决策记录 | 人类写，追溯用 |
| `00_pipeline/handoffs/*.md` | 交接文档 | 发送Agent写，接收Agent读 |

## 模板选择指南

| 场景 | 使用的模板 | 说明 |
|------|-----------|------|
| 启动新项目 | `init-project.sh` | 一键生成项目结构 |
| 新增专题调研 | `research-topic-template.md` | 每个专题一份 |
| 并行启动多个调研 | `parallel-research-launcher.md` | 一次性分发N个 |
| 汇总所有调研成果 | `research-synthesis.md` | Orion汇总后给Framework |
| Phase间交接 | `generic-handoff.md` | 通用交接文档 |
| 执行→审核交接 | `audit-round{1,2,3}.md` | 三轮审核专用 |
| 版本归档 | `version-snapshot-template.md` | 每次Phase完成时 |
| 验证产物结构 | `validate-deliverable.sh`（脚本）| 每轮交付后必跑 |

## 关键协议速览

| 协议 | 核心内容 | 详细说明 |
|------|---------|---------|
| **handoff-spec** | YAML frontmatter + 八节正文 | `references/handoff-spec.md` |
| **state-lifecycle** | 六种状态 + 状态转换规则 | `references/state-lifecycle.md` |
| **forbidden-terms** | 三类禁用词 + 扫描机制 | `references/forbidden-terms-spec.md` |
| **agent-card** | Agent注册表格式 + Role定义 | `references/agent-card-spec.md` |
| **version-control** | 版本快照 + 验证规则 | `references/version-control-spec.md` |

## 脚本工具

| 脚本 | 用途 | 必跑时机 |
|------|------|---------|
| `scripts/init-project.sh` | 项目初始化 | Phase 0 |
| `scripts/forbidden-terms-scan.sh` | 禁用词扫描（依赖yq可选） | 每轮交付前（all-rounds） |
| `scripts/validate-handoff.sh` | 交接文档格式校验 | 每次交接文档创建后 |
| `scripts/validate-deliverable.sh` | 交付物结构校验 | 每次交付物完成时 |
| `scripts/snapshot-dir.sh` | 版本目录快照 | 每次Phase完成时 |

## 局限性（必须了解）

| 局限性 | 影响 | 缓解方案 |
|--------|------|---------|
| **依赖共享文件系统** | 所有Agent必须能访问同一项目目录 | 初始化时确认路径可访问 |
| **YAML解析可选** | `forbidden-terms-scan.sh` 无yq时使用硬编码 | 建议 `brew install yq`，见脚本内警告 |
| **无自动任务调度** | Phase推进依赖人类或编排者触发 | Orion维护 PROJECT_STATE 状态 |
| **Obsidian可选** | 技能模板存在Obsidian，但项目文件在任意目录均可 | 项目文件可在任意路径，Obsidian仅用于个人知识库同步 |
| **脚本为bash** | 需要macOS/Linux环境 | Windows需WSL |

## 首钢吉泰安项目教训

| 教训 | 触发事件 | 本技能中的解决方案 |
|------|---------|------------------|
| G1/G2/G3/G4 代号泄漏到v4才发现 | 禁用词final-only扫描 | enforcement: all-rounds，每轮必扫 |
| 审核意见靠聊天中转失真 | `00_使用说明_如何把Claude的输出给到Codex.md` workaround | 交接文档YAML frontmatter，Codex直接读 |
| Human决策点散落无法追溯 | 重要决策在对话中未记录 | DECISION_LOG.md 集中记录 |
| v4/v5版本混乱 | 版本未做快照覆盖交付 | snapshot-dir.sh + 版本快照模板 |
| Figma-desktop MCP鉴权失败阻塞 | 工具阻塞未及时上报 | state-lifecycle: input-required + Orion立即通知人类 |

## 复盘机制

本技能内置两层复盘：

**1. 阶段级复盘（每Phase结束时）**
- Orion 对照 PROJECT_STATE 的 `decisions` 节，审查本阶段是否有未记录决策
- 检查 milestone 是否全部 `completed`
- 更新 `PHASE_README.md` 的阶段总结节

**2. 项目级复盘（Phase 5 完成后）**
- Orion 填写 `DECISION_LOG.md` 最终汇总
- 对照首钢吉泰安教训清单，检查本项目是否有新教训
- 将新教训追加到 MEMORY.md 的"协作反思"节

复盘结果不修改本技能的 SKILL.md，而是追加到 `~/.openclaw/workspace/memory/YYYY-MM-DD.md`。

## 敏感信息处理

| 信息类型 | 存储位置 | 风险 | 处理方式 |
|---------|---------|------|---------|
| 真实Agent ID/名称 | AGENT_REGISTRY.yaml | 低（仅平台角色） | 使用平台角色名而非个人名称 |
| API Key / Token | **不存于此技能** | — | 使用各平台Keychain/Gateway凭据管理 |
| 客户机密数据 | 项目目录（非技能目录）| 高 | 技能模板不包含任何真实项目数据 |
| 内部代号（G1/G2/G3/G4）| FORBIDDEN_TERMS.yaml | 中 | 仅在项目初始化时注入，交付物扫描清除 |
| 政策金额/资本市场表述 | FORBIDDEN_TERMS.yaml | 中 | risk_expressions类管控，须条件使用 |

**警告**：所有模板中的示例数据（如 `YYYY-MM-DD` / `PROJECT_NAME` / `项目ID`）均为占位符，不得包含真实项目数据。
