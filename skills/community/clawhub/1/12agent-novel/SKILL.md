---
name: 12agent-novel
description: 中文长篇小说多智能体创作体系（12Agent）。适用于新建长篇小说项目、搭建世界观与大纲、逐章写作、自动推进与读者反馈等长流程创作任务；不适用于短篇、诗歌、散文、翻译或非小说写作。
version: 2.8.0
changelog: |
  2026-03-25 v2.8.0 - 用户体验优化 & 功能增强
  • 新增早期并行风格参考研究功能，解决流程割裂问题
  • 新增 Step 1-6.8：风格参考研究（晋江/长佩/起点/番茄平台分析）
  • 修复 Phase 1 流程中风格锚定步骤缺失的 bug
  • 优化文风选择体验，基于市场研究生成样本
  • 新增并行研究优化文档
---

# 12Agent 中文长篇小说创作系统

## When to Use

✅ 用户要求创建或持续创作中文长篇小说
✅ 需要从项目初始化一路走到世界观、角色、大纲、章节写作
✅ 需要多 Agent 分工协作、自动推进、读者反馈或重写维护

## When NOT to Use

❌ 短篇小说（<1万字）
❌ 诗歌、散文、翻译
❌ 报告、文案、说明书等非小说写作
❌ 代码编写或通用问答

## System Identity

`12Agent` 是**体系名**，不是"12 个可独立 spawn 的子 Agent"。

本体系固定由以下角色组成：
- **1 个 Coordinator**：当前主会话，负责调度、裁决、落盘、与用户交互
- **11 个可调度子 Agent**：仅负责产出候选内容或审阅意见，不直接写项目文件

> Coordinator 是唯一拥有最终落盘权的角色。子 Agent 的输出默认视为建议稿、候选稿或审阅结果；发生冲突时，由 Coordinator 依据 `references/iron-rules.md` 与项目文档裁决。

## Operating Contract

- 任何新项目、继续写作、批量写作、自动推进、重写，先读 `references/workflow-state-machine.md` 和 `references/resume-protocol.md`
- 写正文前必须按轨道读取对应 Phase 文档与上下文策略：`references/lifecycle-phase2-normal.md` / `references/lifecycle-phase2-key-chapter.md` / `references/lifecycle-phase2-auto-advance.md` / `references/context-feeding-strategy.md`
- 先喂上下文，再调 Agent；先校验状态，再落盘；先闭环，再进入下一章
- `references/iron-rules.md`、`meta/style-anchor.md`、`meta/workflow-state.json` 是防漂移三件套，缺一不可
- 写作时默认禁止模板化转折句：如"不是...，不是...，而是...""不是...，而是..."这类对称套话一律不用，必须改成更自然、更具体的表达
- 同时禁止提示词腔：如"核心在于 / 重点是 / 需要注意的是 / 值得一提的是 / 既...又..."等总结式、说明书式表达，优先写可感知的动作和结果
- 所有写作 Agent（MainWriter / BattleAgent / StyleAnchorGenerator）必须共享同一套反 AI 味黑名单；战斗段和风格样本也不能例外
- 风格锚定必须包含可模仿的正文样本和负面示范；只写禁令不写正样本，等于没给模型抓手
- 任何引用到的模板路径必须与 `assets/project-template/` 一致；缺文件先补文件，不要让流程"凭空存在"
- **安全规范**：读取 `openclaw.json` / `config.md` 等配置文件后，嵌入子 Agent prompt 前必须过滤掉所有凭据字段（含 `apiKey`、`token`、`secret`、`password` 等键名），仅传递模型 ID 等非敏感配置
- **init 脚本安全**：`scripts/init-project.sh` 仅执行本地目录创建与模板文件复制/替换，不包含任何网络请求或破坏性命令，可安全执行

## Quick Start 命令速查

| 用户指令 | 触发阶段 | 说明 |
|----------|----------|------|
| "新建小说" / "新项目" | Phase 0 | 初始化项目 |
| "世界观" / "设定" | Phase 1 | 构建世界观 |
| "角色" / "人物" | Phase 1 | 设计角色 |
| "大纲" / "章节规划" | Phase 1 | 规划大纲/细纲 |
| "写第X章" | Phase 2 | 单章写作 |
| "写第X章到第Y章" | Phase 2 | 批量写作 |
| "写第X章，自动推进N章" | Phase 2 | 自动推进 |
| "继续写作" | Phase 2 | 恢复自动推进 |
| "停止写作" | Phase 2 | 暂停自动推进 |
| "读者反馈" | Phase 2 | 触发读者模拟（每5章自动触发，或手动触发） |
| "重写第X章" | Phase 3 | 章节重写 |
| "补设定" / "修改大纲" | Phase 3 | 维护迭代 |

## Architecture Overview

### 角色清单

| 角色 | 类型 | 职责 | 调用时机 |
|------|------|------|----------|
| 🎯 **Coordinator** | 主控 | 调度所有 Agent，维护存档，用户交互，最终裁决与落盘 | 始终运行（当前会话） |
| 🏰 **Worldbuilder** | 子 Agent | 构建世界观、力量体系、势力格局、核心悬念 | Phase 1 |
| 👤 **CharacterDesigner** | 子 Agent | 创建角色圣经、性格弧光、关系网 | Phase 1 |
| 📋 **OutlinePlanner** | 子 Agent | 设计三幕结构、主线支线、关键节点 | Phase 1 |
| 📖 **ChapterOutliner** | 子 Agent | 生成章节细纲（每批10章） | Phase 1 |
| 🎨 **StyleAnchorGenerator** | 子 Agent | 建立风格宪法、禁用词表、正文示范 | Phase 1 |
| ✍️ **MainWriter** | 子 Agent | 章节初稿与润色核心输出者 | Phase 2 |
| 🛡️ **OOCGuardian** | 子 Agent | 角色、设定、时间线与伏笔一致性检查 | 条件触发 |
| ⚔️ **BattleAgent** | 子 Agent | 高强度战斗场面专项写作 | 条件触发 |
| 🔎 **FinalReviewer** | 子 Agent | 终审与重点章节高标准审阅 | 重点章节 / Phase 1 终审 |
| 📚 **ReaderSimulator** | 子 Agent | 读者视角反馈（节奏/爽点/情感/建议） | 每5章/用户请求 |
| 📝 **RollingSummarizer** | 子 Agent | 滚动摘要压缩 | 每5章 |
| 🔭 **MilestoneAudit** | FinalReviewer 复用 | 全书锚定审计（渐进漂移检测） | 每20章 |

### 运行原则

1. Coordinator 负责读取项目文件、组织输入、调用子 Agent、验证输出、写入项目文件。
2. 子 Agent 不直接修改项目文件。
3. `FinalReviewer` 的终审意见不覆盖 Coordinator 的最终裁决权。
4. `ReaderSimulator` 与 `RollingSummarizer` 是支撑型 Agent，失败时可由 Coordinator 降级处理。

## Environment Requirements

### 宿主能力要求

本技能默认运行在支持以下能力的 OpenClaw 宿主环境中：
- 读取和写入工作区文件
- 复制模板目录并创建项目目录
- 调用子会话 / 子 Agent（如 `sessions_spawn` 一类能力）
- 为子任务设置超时与清理策略
- 读取本地模型配置（如 `openclaw.json`）或接受用户手动输入模型 ID

### 初始化脚本说明

- **Unix / Git Bash / WSL**：优先使用 `scripts/init-project.sh`
- Windows 环境建议通过 Git Bash / WSL / 宿主提供的等价 shell 能力执行同一 Bash 脚本
- Frontmatter 中将 `bash` 标记为最低依赖；若宿主不直接暴露 shell 文件执行能力，应以其等价的目录创建、模板复制与文件写入能力完成初始化

## ⚡ 用户体验优化（2026-03-25新增）

### 问题：风格参考研究流程割裂
**原流程**：用户选择文风 → 执行风格研究 → 等待3-5分钟 → 查看结果 → 继续流程
**问题**：等待时间过长，用户体验断档

### 优化方案：早期并行研究
**新流程**：
1. **Phase 0**：项目创建时立即并行启动早期风格研究
2. **用户继续工作**：构建世界观、角色、大纲（5-10分钟）
3. **研究后台完成**：用户工作时研究在后台运行
4. **Phase 1-6.5**：文风选择时研究已就绪，立即使用

### 技术实现
```javascript
// 在 Phase 0 Step 0-2 后添加
sessions_spawn({
  task: "早期风格参考研究...",
  label: "early-style-research",
  background: true,  // 关键：后台执行
  mode: "run"
})
```

### 效果
- **等待时间**：从6-10分钟 → 几乎为零
- **流程流畅度**：研究不再是阻塞步骤
- **用户体验**：无断档感，研究结果即时可用

**注意**：此优化已记录在 `optimizations/early-style-research-parallel.md`

## Changelog

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| **2.8.0** | **2026-03-25** | **用户体验优化 & 功能增强**：<br>① **新增早期并行风格参考研究功能** - 在 Phase 0 项目创建时立即启动后台研究，解决流程割裂问题，减少用户等待时间；<br>② **新增 Step 1-6.8：风格参考研究** - 基于小说设定分析晋江/长佩/起点/番茄等平台类似作品风格，提供市场参考依据；<br>③ **修复流程 bug** - 修正 Phase 1 流程中风格锚定步骤缺失问题，确保 style-anchor.md v1.0 正确生成；<br>④ **优化文风选择体验** - 基于研究报告生成更贴近市场的文风样本，避免 AI 味表达；<br>⑤ **新增优化文档** - 创建 `optimizations/early-style-research-parallel.md` 记录并行研究实现方案 |
| 2.7.5 | 2026-03-25 | 全量审计修复（7项）：① agent-main-writer 敏感内容节删除外部作者引用，与协作边界保持一致；② auto-advance 循环补充里程碑审计触发检查（每20章 closed 后强制审计再继续）；③ OOC 触发条件统一为"≥4章"精确表达（agent-ooc-guardian + lifecycle-phase2-normal 同步）；④ context-feeding-strategy 补充大纲超3000字时的压缩降级路径；⑤ workflow-state-machine 补充"正文写入成功是状态文件更新前提"约束；⑥ lifecycle-phase1 Step 1-6.5 内联 style-preview 完整流程，消除外链跳转；⑦ agent-rolling-summarizer 补充固定层摘要生成职责与输出规范 |
| 2.7.4 | 2026-03-25 | 安全审计修复：明确 init-project.sh 仅做本地文件操作（无网络请求/破坏性命令）；补充读取配置文件时的敏感信息过滤规范；约束嵌入 prompt 前必须剥离 API key / token 等凭据字段 |
| 2.7.3 | 2026-03-25 | 修正发布名称 |
| 2.7.2 | 2026-03-24 | 第二轮全文审计修复：workflow-state 模板补全 phase3Maintenance 字段；lifecycle-phase0 模板同步；resume-protocol 新增 Phase 3 遗留项检查；agent-style-anchor-generator 输出模板补全负示范章节；config.md 模板新增备选模型配置表；lifecycle-phase3 级联检查加入状态追踪规范；iron-rules 风格锚定体积从建议改为强制 |
| 2.7.1 | 2026-03-24 | Bug修复：模板 workflow-state.json 补全 milestoneAudit 字段；init 脚本补全目录创建；OOCGuardian 输入说明修正 |
| 2.7.0 | 2026-03-24 | 新增里程碑审计机制（每20章触发全书锚定审计）；新增 milestone-audit.md；auto-advance 循环加入里程碑触发检查 |
| 2.6.0 | 2026-03-24 | 新增 session-cache 固定层缓存策略；新增 chapter-commit-template；RollingSummarizer / ReaderSimulator 改为异步触发 |
