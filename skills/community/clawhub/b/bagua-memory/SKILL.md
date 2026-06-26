---
name: bagua-memory
description: >
  八卦记忆系统 (Bagua Memory) - AI Agent 记忆管理框架。
  将记忆按八个维度（规则/知识/热记忆/决策/事件/关联/归档/偏好）分类存储，
  通过生命周期自动衰减和卦变关联联想检索。
  
  使用场景：
  (1) 为 AI Agent 建立结构化的长期记忆系统
  (2) 管理 workspace 中的记忆文件（memory/ 目录）
  (3) 记忆的写入、归档、压缩、检索
  (4) 用户提到"记忆系统"、"bagua"、"八卦"、"长期记忆"、"归档记忆"
  (5) 需要从对话中提取关键信息并持久化存储
  (6) 定期维护和整理记忆文件
---

# 八卦记忆系统

基于文件的记忆管理框架，零依赖，适用于任何能读写本地文件的 AI Agent。

详细架构见 [references/architecture.md](references/architecture.md)（权威来源：`memory/bagua/README.md`）。

## ⚡ 自激活（首次触发必做）

**检测条件**：如果 `AGENTS.md` 或 `SOUL.md` 中不存在 `## 记忆规则` 章节，说明尚未激活。

**激活步骤**：
1. 运行 `bash scripts/init_bagua.sh .`（在 workspace 根目录，自动创建 memory/ 和 MEMORY.md）
2. 读取 `references/soul-inject.md`，将其内容追加到 `AGENTS.md`（或 `SOUL.md`）末尾
3. 如果 `HEARTBEAT.md` 存在，将 `references/heartbeat-inject.md` 追加进去
4. 告知用户："八卦记忆系统已激活 ✅"

## 核心流程

### 写入记忆

1. 新信息按归类指南判断所属卦位
2. 写入对应 `memory/bagua/<卦位>/` 下的 Markdown 文件
3. 文件命名：`YYYY-MM-DD.md`（时间线类）或按主题命名

### 检索记忆（渐进式）

1. **L0**：读 `MEMORY.md`（索引+归类指南）
2. **L1**：根据话题读 1-2 个相关卦位
3. **L2**：复杂检索时读 `memory/bagua/README.md`（卦变关联表）

### 记忆维护

1. **归档**：离卦超过 7 天 → 移入艮卦
2. **压缩**：艮卦超过 30 天 → 摘要化
3. **恢复**：归档记忆再次被引用 → 升回原卦位

## 八卦速查

| 卦 | 目录 | 存什么 | 边界 |
|---|------|--------|------|
| ☰ 乾 | `qian/` | 系统规则、行为准则 | - |
| ☷ 坤 | `kun/` | 知识库、事实 | 相对稳定的信息 |
| ☲ 离 | `li/` | 近期新发现 | 只放"新东西"，不放对话总结 |
| ☵ 坎 | `kan/` | 决策推理 | 只记"为什么"（reason） |
| ☳ 震 | `zhen/` | 事件时间线 | 只记"发生了什么"（fact） |
| ☴ 巽 | `xun/` | 关联网络 | 人/项目/概念关系 |
| ☶ 艮 | `gen/` | 归档记忆 | 冷却中的旧记忆 |
| ☱ 兑 | `dui/` | 用户偏好 | 风格、习惯、情感 |

## 与 MEMORY.md 的关系

`MEMORY.md` 是入口（L0），记忆本体在 `memory/bagua/` 各卦位下。
