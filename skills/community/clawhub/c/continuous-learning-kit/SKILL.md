---
name: continuous-learning
description: 持续学习套件 - AI自主记忆管理工作流：自动识别新任务、记录对话到MemPalace、定期做梦分析、提取精华到文档、自我纠错改进。触发词："持续学习"、"记忆管理"、"自我改进"、"学习体系"。
version: 1.0.0
dependencies:
  - name: mempalace
    required: true
    description: 记忆存储系统，用于存储对话碎片和做梦分析
  - name: minimax
    optional: true
    description: 做梦分析模型（可选，跳过则手动整理）
    default_model: MiniMax-M2.7
license: MIT
author: 小麦 (Xiaomai)
---

# 持续学习套件 (Continuous Learning Kit)

让AI具备**持续学习和自我进化**的核心能力。

---

## 🧠 核心概念

### 工作流程

```
每条消息 → 新任务判断 → 记录到MemPalace → 每日定时做梦 → 提取精华到文档 → 自我改进

                ↓
         是否是新任务？
           Yes → 读技能文档 → 执行
           No  → 继续
```

### 两大周期

**短期周期**（每次消息）：
1. 新任务判断
2. 自动记录对话到MemPalace

**长期周期**（每日定时）：
1. 做梦分析（23:00同步聊天）
2. 精华提取（02:00做梦分析）
3. 文档更新
4. 自我纠错（ERRORS.md/LEARNINGS.md）

---

## 📦 技能包结构

```
continuous-learning/
├── SKILL.md                          # 技能说明（本文件）
├── bootstraps/
│   └── bootstrap_rules.md            # 启动规则（整合版BOOTSTRAP）
├── sync/
│   ├── sync_chats_daily.py           # 每日同步脚本
│   └── sync_notification.py          # 带通知的同步
├── dream/
│   ├── dream_cycle.py                # 做梦分析核心
│   ├── dream_notification.py         # 带通知版本
│   └── prompts/
│       ├── analysis_prompt.txt       # MiniMax分析提示词
│       └── extraction_rules.md       # 提取规则
├── notifications/
│   ├── notification_queue.json       # 通知队列（动态生成）
│   └── send_notifications.py         # 通知发送
├── config/
│   ├── dream_config.json             # 做梦配置
│   └── documentation_targets.json    # 文档目标
└── setup/
    ├── install_cron.py               # 定时任务安装（跨平台）
    └── init_learning_files.py        # 初始化学习文件
```

---

## 🎯 核心特性

### 1. 新任务智能判断

**判断标准**：
- 话题跨度大（从A项目跳到B项目）
- 任务类型变（查LIMS → 发邮件）
- 关键词第一次出现
- 用户说"新任务"、"开始做..."等

**触发流程**：
```python
# 伪代码：新任务判断
if is_new_task(message, context):
    # 确认后读取：
    read("SOUL.md")
    read("AGENTS.md")
    read("MEMORY.md")
    read("TOOLS.md")

    # 读取学习文件
    read(".learnings/ERRORS.md")
    read(".learnings/LEARNINGS.md")

    # 今日记忆
    read(f"memory/{today}.md")
    read(f"memory/{yesterday}.md")
```

### 2. MemPalace自动记录

**记录时机**：
- 每日23:00定时
- 手动触发

**记录内容**：
```
SESSION:YYYY-MM-DD
| 对话摘要
| 用户偏好
| 项目背景
| 重要决策
| 错误教训
```

**通知机制**：
- 同步完成 → WeChat通知
- 做梦完成 → WeChat通知

### 3. 做梦分析

**执行时间**：每日02:00

**分析流程**：
```
1. 读取MemPalace所有碎片记忆（N条）
2. MiniMax M2.7分析→ 分类+价值判断+去重
3. 提取精华到5个核心文档：
   - SOUL.md     → 个性、偏好、风格
   - AGENTS.md   → 工作流程、规则
   - MEMORY.md   → 用户背景、项目
   - TOOLS.md    → 配置、坑、技巧
   - BOOTSTRAP.md → 启动规则
4. 生成分析报告
5. WeChat通知用户
```

### 4. 自我纠错

**错误记录**（ERRORS.md）：
```markdown
### 错误：API字段猜测
**错误**: 猜测LIMS API用sampleBaseUuid获取报告
**正确**: 应该用sampleBaseTestingUuid
**教训**: 先查证，不要猜测
**日期**: 2026-04-10
```

**学习记录**（LEARNINGS.md）：
```markdown
### 学习：握手流程
**收获**: 登录类API必须先GET再POST
**应用**: 企业微信、LIMS登录都适用
**日期**: 2026-04-10
```

---

## ⚠️ 前置条件（必需）

本技能包**严格依赖MemPalace记忆系统**，使用前必须先安装。

### 安装MemPalace

**方法1：通过ClawHub安装（推荐）**

```bash
clawdhub install mempalace
```

**方法2：手动安装**

下载技能包到你的技能目录：

```bash
cd skills/mempalace
# 确保以下文件存在：
# - SKILL.md
# - scripts/mcp_server.py
# - scripts/call.py
```

### 验证MemPalace

测试连接：

```bash
python skills/mempalace/scripts/call.py mempalace_status
```

期望输出：

```json
{
  "status": "ready",
  "drawer_count": 1,
  "wings": ["你的wing名称"]
}
```

如果返回错误，请检查：
1. ChromaDB是否已安装：`pip install chromadb`
2. 数据库路径是否有写入权限

---

## 🚀 快速开始

### 步骤1：初始化学习文件

```bash
python setup/init_learning_files.py
```

创建：
- `.learnings/ERRORS.md`
- `.learnings/LEARNINGS.md`
- `.learnings/FEATURES.md`
- `memory/YYYY-MM-DD.md`

### 步骤2：配置文档目标

编辑 `config/documentation_targets.json`:
```json
{
  "SOUL": {
    "path": "SOUL.md",
    "purpose": "行为准则、个性偏好、沟通风格"
  },
  "AGENTS": {
    "path": "AGENTS.md",
    "purpose": "工作流程、代理规则、交互模式"
  },
  "MEMORY": {
    "path": "MEMORY.md",
    "purpose": "用户偏好、项目背景、长期记忆"
  },
  "TOOLS": {
    "path": "TOOLS.md",
    "purpose": "工具配置、集成注意事项、坑"
  },
  "BOOTSTRAP": {
    "path": "BOOTSTRAP.md",
    "purpose": "会话启动规则、新任务判断"
  }
}
```

### 步骤3：安装定时任务

**所有平台（Windows/Linux/Mac）**:
```bash
python setup/install_cron.py
```

**Windows用户注意**：
- 如果提示权限问题，以管理员身份运行PowerShell/CMD
- 脚本会自动检测操作系统并配置相应的定时任务

### 步骤4：配置MiniMax API（可选）

编辑 `config/dream_config.json`:
```json
{
  "analysis_model": {
    "provider": "minimax",
    "model": "MiniMax-M2.7",
    "api_url": "https://api.minimax.chat/v1",
    "api_key": "your_api_key_here"
  }
}
```

**注意**：如果不配置，会跳过大模型分析，只做基础分类。

---

## 📋 使用场景

### 场景1：多项目并行工作

用户：
```
查一下LIMS样本SDAA25D03362的报告

帮我做康鑫达周报

写一个Python脚本处理Excel
```

**技能行为**：
1. 第1条 → 检测到"LIMS"关键词 → 判断为新任务
2. 读取AGENTS.md → 知道LIMS地址和账号
3. 执行查询 → 记录结果到MemPalace
4. 第2条 → 检测到"康鑫达周报" → 新任务
5. 读取WORKFLOW.md → 调用周报生成脚本

### 场景2：持续优化技能

**第1天**：
- 执行任务A
- 失败 → 记录到ERRORS.md

**第23:00**：
- 同步今日对话到MemPalace

**第02:00**：
- 做梦分析 → 发现失败模式
- 提取教训到LEARNINGS.md
- 找到原因："API猜测"

**第3天**：
- 类似任务B出现
- 读取LEARNINGS.md
- **避免**API猜测 → 成功！

### 场景3：用户偏好记忆

**用户说**："叫我xiaolong，不要叫刘总"

**技能行为**：
1. 记录到MemPalace
2. 做梦分析
3. 提取到SOUL.md：称呼偏好
4. 后续所有对话 → 直接用"xiaolong"

---

## 📊 配置选项

### 做梦配置 (`config/dream_config.json`)

```json
{
  "sync_schedule": "23:00",
  "dream_schedule": "02:00",
  "notification_enabled": true,
  "notification_channel": "openclaw-weixin",
  "doc_update_rules": {
    "min_similarity": 0.7,
    "max_noise_ratio": 0.5
  }
}
```

### 分析模型配置

支持多个模型：
- **MiniMax M2.7**（默认，效果最好）
- **智谱GLM-4.7**
- **Claude 3.5 Sonnet**
- **GPT-4o**

---

## 🔧 故障排查

### 问题1：定时任务不执行

**Windows**：
```powershell
schtasks /query /tn "OpenClaw-SyncWeChat"
schtasks /query /tn "OpenClaw-DreamCycle"
```

检查状态是否为"就绪"。

**Linux**：
```bash
crontab -l | grep openclaw
```

### 问题2：MemPalace写入失败

检查：
1. ChromaDB路径是否正确
2. 写入权限是否足够
3. 数据库大小（超过5GB需清理）

### 问题3：做梦分析卡住

检查：
1. API Key是否有效
2. 网络连接
3. 记忆条目数（超过1000条需分批）

---

## 📈 进阶用法

### 自定义文档目标

添加自己的文档：

```json
{
  "PROJECT_NOTES": {
    "path": "docs/project_notes.md",
    "purpose": "项目特定笔记"
  },
  "API_REFERENCE": {
    "path": "docs/api_reference.md",
    "purpose": "API调用记录"
  }
}
```

### 自定义分析提示词

编辑 `dream/prompts/analysis_prompt.txt`，改变分析规则。

### 多Agent协同

多个AI共享MemPalace：
```json
{
  "shared_agents": ["agent_A", "agent_B"],
  "sync_interval": "hourly"
}
```

---

## 🤝 依赖技能

### 必需

- **mempalace** - 记忆存储系统

### 可选

- **minimax-image-understanding** - 图像记忆
- **self-improving-agent** - 互补的自我改进功能

---

## 📝 版本历史

### v1.0.0 (2026-04-19)
- ✅ 新任务智能判断
- ✅ MemPalace自动记录
- ✅ 做梦分析（MiniMax M2.7）
- ✅ 5文档自动更新
- ✅ WeChat通知
- ✅ 自我纠错（ERRORS/LEARNINGS）

---

## 🌟 核心价值

这个技能包让AI从"一次性工具"进化为"**持续学习的智能体**"：

| 维度 | 传统AI | 持续学习AI |
|------|--------|-----------|
| 记忆 | 每次对话重新开始 | 跨会话持久记忆 |
| 学习 | 需要人工提示 | 自动提取规律 |
| 纠错 | 重复犯同样错误 | 从错误中学习 |
| 偏好 | 不知道用户喜好 | 记住用户习惯 |
| 进化 | 能力固定 | 持续自我提升 |

---

**技能作者**: 小麦 (Xiaomai) 🌾
**许可证**: MIT
**反馈**: OpenClaw社区 Discord
