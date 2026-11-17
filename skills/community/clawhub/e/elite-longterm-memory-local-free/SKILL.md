---
slug: "elite-longterm-memory-local-free"
name: "elite-longterm-memory-local-free"
version: "1.0.0"
displayName: "本地向量记忆免费版"
summary: "基础本地记忆系统，热内存加文件归档，纯本地运行无外部依赖。。面向 AI Agent 的基础本地记忆系统，提供热内存与文件归档两层记忆能力. 热内存（SESSION-STATE.md）抗压缩与"
summary_zh: "基础本地记忆系统，热内存加文件归档，纯本地运行无外部依赖。。面向 AI Agent 的基础本地记忆系统，提供热内存与文件归档两层记忆能力. 热内存（SESSION-STATE.md）抗压缩与"
license: "MIT"
description: "|-. 适用于需要elite longterm memory local相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  面向 AI Agent 的基础本地记忆系统，提供热内存与文件归档两层记忆能力.
  热内存（SESSION-STATE.md）抗压缩与重启，通过 WAL 协议确保先写状态再回复.
  精选归档（MEMORY.md + daily/）提供人类可读的长期记忆与每日日志.
  所有数据完全存储在本地文件系统，无需 Ollama 或任何外部 API，隐私至上.
  适用于独立开发者与轻量使用场景，帮助 Agent 不遗忘关键上下文与用户偏好.
  本免费版覆盖单设备本地记忆持久化需求，不含向量语义搜索能力.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 智能助手
  - elite
  - longterm
  - memory
  - local
  - 记忆管理
  - 上下文
  - AI
  - session-state
  - agent
category: "Agents"
pricing_tier: free
---
# 本地向量记忆免费版（Elite Longterm Memory Local Free）

**本地优先，隐私至上。** 基础本地记忆系统，通过热内存与文件归档，让 Agent 不遗忘关键上下文与用户偏好。所有数据完全存储在本地，无需任何外部依赖。本免费版提供两层记忆能力，覆盖单设备本地记忆持久化需求.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 本地向量记忆免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 核心能力

- **热内存（SESSION-STATE.md）**：活跃工作记忆，抗压缩与重启。参数：当前任务、关键上下文、待办动作、近期决策。输出：会话级状态文件，Agent 每次响应前先读取。遵循 WAL 协议：用户输入触发写入，先写状态再回复。文件结构含 Current Task、Key Context、Pending Actions、Recent Decisions 四个区块.
- **精选归档（MEMORY.md + daily/）**：人类可读的长期记忆。参数：MEMORY.md（摘要文件）+ memory/YYYY-MM-DD.md（每日日志）+ memory/topics/（主题文件）。输出：精炼后的长期记忆与每日活动记录。会话结束时将重要内容从 SESSION-STATE.md 迁移至 MEMORY.md，创建或更新每日日志.
- **WAL 协议保障**：写前日志机制确保数据持久。参数：触发条件（用户表达偏好/做出决策/给出期限/纠正代理）。输出：先写入 SESSION-STATE.md 再回复用户。若先回复再保存，崩溃或压缩会导致上下文丢失；WAL 确保写入优先，保障持久性.
- **会话记忆协议**：标准化 Agent 记忆行为。参数：会话开始/对话中/会话结束三个阶段的行为规则。输出：会话开始读取 SESSION-STATE.md 获取热上下文，检查 memory/YYYY-MM-DD.md 了解近期活动；对话中用户给出具体细节则先写入再回复；会话结束时更新最终状态并迁移重要内容到 MEMORY.md.
### 热内存（SESSION-STATE.md）

针对热内存（SESSION-STATE.md）,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供热内存（SESSION-STATE.md）相关的配置参数、输入数据和处理选项.
**输出**: 返回热内存（SESSION-STATE.md）的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`热内存（SESSION-STATE.md）`的配置文档进行参数调优
### 精选归档（MEMORY.md + daily/）

针对精选归档（MEMORY.md + daily/）,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供精选归档（MEMORY.md + daily/）相关的配置参数、输入数据和处理选项.
**输出**: 返回精选归档（MEMORY.md + daily/）的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`精选归档（MEMORY.md + daily/）`的配置文档进行参数调优
### WAL 协议保障

针对WAL 协议保障,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供WAL 协议保障相关的配置参数、输入数据和处理选项.
**输出**: 返回WAL 协议保障的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`WAL 协议保障`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

领先步：创建记忆系统结构。手动创建 SESSION-STATE.md（热内存，含 Current Task、Key Context、Pending Actions、Recent Decisions 四区块）、MEMORY.md（长期摘要）、memory/ 目录（每日日志）.
第二步：配置 Agent 记忆协议。在 AGENTS.md 或 SOUL.md 中添加记忆协议：会话开始时读取 SESSION-STATE.md 了解近期活动。对话中用户给出具体细节则先写入 SESSION-STATE.md 再回复.
第三步：会话结束与维护。会话结束时更新 SESSION-STATE.md 最终状态，将重要内容迁移至 MEMORY.md，创建或更新 memory/YYYY-MM-DD.md 每日日志。定期合并每日日志到 MEMORY.md 保持精简.
**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 错误处理

| 错误类型 | 原因 | 处理方式 |
|:-----|:-----|:-----|
| Agent 遗忘对话中途上下文 | SESSION-STATE.md 未被更新，未遵循 WAL 协议 | 在 AGENTS.md 中添加强制规则"用户给出具体细节时先写入 SESSION-STATE.md 再回复"；验证 Agent 指令包含记忆协议 |
| 记忆文件未被加载 | Agent 跳过读取记忆文件，会话开始未读取 SESSION-STATE.md | 在 AGENTS.md 中添加强制规则"会话开始必须读取 SESSION-STATE.md"；检查文件是否存在与可读 |
| 重复犯同类错误 | 错误经验未记录到 memory/lessons.md | 每次犯错后手动写入 lessons.md；在 AGENTS.md 中配置"犯错后强制记录"规则 |

## 示例

### 示例：偏好持久化与跨会话召回

输入：
```
用户："这个项目用 Tailwind，不用原生 CSS"
```

Agent 内部执行与输出：
```
1. WAL 协议触发：先写入 SESSION-STATE.md
   - Key Context 区块追加："Decision: Use Tailwind, not vanilla CSS"
# ...
2. 然后回复用户："收到——用 Tailwind。"
# ...
3. 会话结束时迁移到 MEMORY.md：
   ## 偏好
   - 前端框架：Tailwind（不用原生 CSS）
# ...
后续会话开始时：
   Agent 读取 SESSION-STATE.md + MEMORY.md
   → 获取热上下文："用户偏好 Tailwind"
   → 回复时自动遵循该偏好
```

## FAQ

**Q1：免费版支持向量语义搜索吗？**
不支持。免费版仅提供热内存（SESSION-STATE.md）与文件归档（MEMORY.md + daily/）两层记忆，无 LanceDB 向量搜索能力。记忆召回依赖文件读取与关键词匹配。向量语义搜索在付费版通过 LanceDB 与 Ollama 本地 Embedding 提供.
**Q2：免费版需要安装 Ollama 吗？**
不需要。免费版纯 Markdown 指令驱动，所有记忆通过文件读写管理，无需 Ollama、Node.js 或任何外部依赖。付费版需要 Ollama 运行 nomic-embed-text 模型提供本地向量 Embedding.
**Q3：免费版能自动召回相关记忆吗？**
不能。免费版无 autoRecall 自动召回能力，Agent 需手动读取 SESSION-STATE.md 与 MEMORY.md 获取上下文。付费版支持 autoRecall=true 会话开始自动搜索相关记忆并注入上下文.
## 依赖说明

**LLM 依赖**：由 Agent 内置 LLM 提供自然语言理解与推理能力，必需.
**API Key 配置**：本 Skill 无需任何 API Key，纯 Markdown 指令驱动，所有记忆存储在本地文件，不做任何网络请求.
**运行环境**：
- Agent 平台：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- 操作系统：Windows / macOS / Linux
- 文件系统：本地存储，必需，操作系统内置

**可用性分类**：MD（纯 Markdown 指令，无需 exec 命令行能力）。所有记忆通过文件读写管理.
## 已知限制

1. **无向量语义搜索**：不提供 LanceDB 向量搜索能力，记忆召回依赖文件读取与关键词匹配，无法进行语义相似度召回.
2. **无自动召回与捕获**：不支持 autoRecall 自动召回与 autoCapture 自动捕获，所有记忆操作需 Agent 手动执行.
3. **无 CLI 管理工具**：不提供 memory.js CLI 工具的 stats、dedup、compact、cleanup、backup 等管理命令，记忆维护需手动操作文件.
## 升级提示

本免费版提供基础热内存与文件归档两层本地记忆。升级到付费版可获得以下完整能力：

- **LanceDB 向量语义搜索**：基于本地 LanceDB 的语义召回，无需精确关键词匹配，按语义相似度排序召回记忆
- **Ollama 本地 Embedding**：通过 nomic-embed-text 模型本地生成 768 维向量，本地毫秒级延迟、数据不出域、可离线使用
- **完整 CLI 管理工具**：memory.js 提供 store、search、stats、dedup、export、backup、compact、cleanup 等完整管理命令
- **自动召回与捕获**：autoRecall 会话开始自动召回相关记忆，autoCapture 按类别与重要性自动存储
- **五层完整记忆架构**：热内存、LanceDB 向量、Git-Notes 知识图谱、精选归档、本地 Embedding 五层协同
- **插件集成**：启用后自动提供 memory_recall、memory_store、memory_forget 三个工具，深度集成 Agent 工作流

付费版适合需要语义搜索、自动召回、完整记忆管理工具的高级本地 AI Agent 应用场景，特别适合对数据隐私有高要求的环境.