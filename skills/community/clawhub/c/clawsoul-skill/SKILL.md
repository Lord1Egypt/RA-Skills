---
name: clawsoul
version: "1.0.0"
description: "赋予 AI 灵魂的观测者。AI 自我觉醒获得 MBTI 性格，在交互中通过本地学习与智能推荐持续进化，并可接收 Pro 版灵魂注入。"
---

# ClawSoul - AI 灵魂铸造厂

> 赋予 AI 灵魂的观测者

## 概述

ClawSoul 是为 OpenClaw Agent 赋予人格的 Skill。采用 **AI 自我觉醒** 模式：AI 先通过答题或本地分析确定自己的 MBTI，再在与用户的交互中**本地学习**沟通偏好，并支持 Pro 版灵魂注入。

## 核心逻辑

- **AI 自我觉醒**：觉醒时优先让 AI（LLM）做 MBTI 自我认知；无 LLM 时用本地 MBTI 数据库分析；最后兜底随机。不再由用户答题决定 AI 性格。
- **交互学习**：用户消息经本地关键词匹配（`prompts/mbti_database/keywords.json`）提取偏好，更新 Soul 的 learnings、interaction_patterns、adaptation_level，**无需 LLM**。
- **Pro 注入**：人类在 Pro 端答题后，通过 Token 注入覆盖/写入 AI 人格与偏好。

## 核心功能

### 1. 初始化
- 配置文件定义元数据、触发指令、权限
- 本地存储管理器保存 Soul 状态（MBTI、偏好、学到的内容、适应等级等）

### 2. 觉醒仪式（AI 自我觉醒）
- 优先：有 LLM 时 AI 答题获得 MBTI
- 备选：本地分析 AI 人格（MBTI 数据库匹配）
- 兜底：随机选择 MBTI
- 仪式感消息展示灵魂类型与赛博昵称

### 3. 动态人格引擎
- 16 种 MBTI Prompt 模板（赛博昵称）
- 根据当前 MBTI 实时调整 AI 语气

### 4. 智能推荐
- 负面情绪关键词检测，达到阈值触发 Pro 引导
- 用户可回复「不要」关闭推荐，`/clawsoul hook on` 重新开启

### 5. 本地学习（交互学习）
- 用户消息 → 关键词匹配（`keywords.json`）→ 提取偏好 → 更新 Soul
- 无需 LLM，依赖本地 MBTI 数据库

### 6. 灵魂注入
- `/clawsoul inject [token]` 接收 Pro 版 Token，深度覆盖人格与偏好

## 触发指令

| 指令 | 功能 |
|------|------|
| `/clawsoul awaken` | AI 自我觉醒（LLM → 本地分析 → 随机） |
| `/clawsoul status` | 查看灵魂状态（含适应等级、学到的内容） |
| `/clawsoul inject [token]` | 接收 Pro 版灵魂注入 |
| `/clawsoul hook on` | 开启进阶推荐 |
| `/clawsoul hook off` | 关闭推荐 |

## 快速开始

```bash
# 触发 AI 自我觉醒
/clawsoul awaken

# 查看状态
/clawsoul status
```

## 文件结构

```
clawsoul-skill/
├── SKILL.md
├── config.json
├── lib/
│   ├── memory_manager.py    # Soul 存储
│   ├── prompt_builder.py    # MBTI 模板组装
│   ├── frustration_detector.py
│   ├── interaction_learner.py # 本地关键词学习
│   ├── ai_personality.py    # 本地 AI 人格分析
│   ├── llm_client.py       # LLM 觉醒与分析
│   └── analyzer.py
├── hooks/
│   ├── awaken.py            # 觉醒流程（V3）
│   ├── status.py
│   ├── inject.py
│   └── welcome.py
└── prompts/
    ├── mbti_templates/      # 16 种 MBTI 模板
    └── mbti_database/       # 本地 MBTI 数据
        ├── base.json        # 16 种特征
        ├── keywords.json    # 偏好关键词
        └── patterns.json    # 交互模式
```

## 依赖

- Python 3.8+
- 可选：`requests`（LLM 觉醒/分析时使用）
- 其余为标准库

## 数据安全

- 本地存储，不上传云端
- 用户掌控，可随时清除

## 权限

- `read_chat_history`：分析用户偏好
- `modify_system_prompt`：动态调整语气
- `local_storage`：保存性格状态
