---
name: auto-memory
version: 3.0.0
description: LLM 增强记忆系统 — 语义理解、智能摘要、敏感信息保护。三层架构自动管理 agent 记忆。
author: dtldhjh
license: MIT
category: productivity
platforms:
  - openclaw
---

# Auto Memory - LLM 增强记忆系统 v3.0.0

LLM 驱动的智能记忆系统，让 agent 拥有完整的持久记忆能力。

## v3.0.0 核心特性

| 特性 | 说明 |
|------|------|
| 🤖 LLM 分析 | 语义理解对话内容，智能分类 |
| 🔒 敏感信息保护 | 自动检测并脱敏 API Key、Token、密码等 |
| 📊 结构化提取 | 偏好/决策/待办/问题/学习 五维分类 |
| 📝 智能摘要 | 自动生成对话摘要 |
| 🔄 智能去重 | 跨次运行去重，不再重复累积 |

---

## 三层记忆架构

```
用户对话
    ↓ (extract-memory.sh v3 + LLM)
┌─────────────────────────┐
│  memory/YYYY-MM-DD.md   │  日常日志
│  - LLM 智能分析         │
│  - 五维分类提取         │
│  - 敏感信息脱敏         │
└───────────┬─────────────┘
            ↓ (update-long-memory.sh)
┌─────────────────────────┐
│      MEMORY.md          │  长期记忆
│  - 用户偏好             │
│  - 重要决策             │
│  - 项目进展             │
└───────────┬─────────────┘
            ↓ (openclaw memory index)
┌─────────────────────────┐
│     向量数据库          │  可检索
│  - openclaw memory search │
└─────────────────────────┘
```

---

## 安装

```bash
# 创建目录
mkdir -p ~/.openclaw/scripts
mkdir -p ~/.openclaw/workspace/memory/archive
mkdir -p ~/.openclaw/workspace/.learnings/shared

# 下载脚本
# extract-memory.sh (v3.0 LLM 增强版)
# update-long-memory.sh

# 设置权限
chmod +x ~/.openclaw/scripts/extract-memory.sh
chmod +x ~/.openclaw/scripts/update-long-memory.sh
```

---

## 配置 HEARTBEAT.md

```markdown
## 1. 自动记忆更新
\`\`\`bash
~/.openclaw/scripts/extract-memory.sh main
\`\`\`

## 2. 长期记忆同步
\`\`\`bash
~/.openclaw/scripts/update-long-memory.sh main
\`\`\`
```

---

## LLM 分析输出

```markdown
## LLM 分析 (10:34)

**摘要**: 本次对话完成了记忆系统的三层架构改造

### 🎯 偏好
- OpenCode 模型偏好设置
- 服务开发配置：端口 10001-10100

### 📋 决策
- 采用三层互补架构管理记忆

### 📌 待办
- ✅ 优化脚本
- ✅ 创建更新脚本

### ❌ 问题
- MEMORY.md 未及时更新

### 💡 学习
- 去重机制需要跨次检查
```

---

## 敏感信息保护

| 类型 | 模式 | 替换为 |
|------|------|--------|
| API Key | `api_key=xxx` | `[REDACTED_KEY]` |
| Token | `token=xxx` | `[REDACTED_TOKEN]` |
| 密码 | `password=xxx` | `[REDACTED_PASSWORD]` |
| 手机号 | `13812345678` | `[REDACTED_PHONE]` |
| 邮箱 | `user@example.com` | `[REDACTED_EMAIL]` |
| 内网 IP | `192.168.x.x` | `[REDACTED_IP]` |

**脱敏流程：**
1. 检测敏感模式
2. 发送给 LLM 前脱敏
3. LLM 返回结果再次检查

---

## 示例输出

```
🧹 检查过期文件...
📚 加载学习经验...
📄 分析 session: e0262284-xxx.jsonl
   🤖 使用 LLM 分析对话...
✅ LLM 分析完成
   📝 摘要: 本次对话完成了记忆系统的三层架构改造...
🔄 更新向量索引...
✅ 索引已更新
```

---

## 更新日志

### v3.0.0 (2026-03-22)
- 🤖 LLM 语义分析（使用当前模型）
- 🔒 敏感信息自动脱敏
- 📊 五维分类提取
- 📝 智能摘要生成
- 🔄 智能去重

### v2.0.0 (2026-03-22)
- 三层记忆架构
- 自动同步到 MEMORY.md

### v1.0.0 (2026-03-12)
- 初始版本