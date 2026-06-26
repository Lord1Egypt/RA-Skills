---
name: memory-system
description: 完整记忆系统 - 文件系统记忆 + 向量搜索 + 四类记忆分类 + AutoDream 自动整合
---

# Memory System 🧠

> 完整记忆系统 - 文件系统记忆 + 向量搜索 + 四类记忆分类 + AutoDream 自动整合 + Feedback 双向记录

## 特性

- 📁 **文件系统存储** - 基于 Markdown 文件，无数据库依赖
- 🔍 **语义搜索** - 支持 Ollama 向量搜索
- ⚡ **自动加载** - 会话启动时自动加载相关记忆
- 💾 **Memory Flush** - 上下文接近阈值时自动持久化
- 📝 **四类记忆分类** - User / Feedback / Project / Reference
- 🔄 **Feedback 双向记录** - 同时记录纠正和确认
- 🌙 **AutoDream** - 定时自动整合记忆，保持记忆新鲜

---

## 安装

```bash
clawhub install memory-system
```

---

## 核心概念

### 1. 四类记忆

| 类型 | 作用域 | 用途 | 保存时机 |
|------|--------|------|---------|
| **User** | 私密 | 用户角色、偏好、知识 | 了解用户任何细节 |
| **Feedback** | 私密/团队 | 用户的纠正和确认 | 用户纠正或确认时 |
| **Project** | 团队 | 项目进展、目标、决策 | 了解项目动态时 |
| **Reference** | 团队 | 外部系统指针 | 发现外部资源时 |

### 2. Feedback 双向记录

**为什么重要？**

只记录"不要做什么" → AI 会变得保守，不敢做决定

双向记录 → AI 既能避免错误，也能复用成功经验

```markdown
### 不要mock数据库
**Type:** negative
**Why:** 上一季度mock测试通过了但生产迁移失败
**How to apply:** 集成测试必须用真实数据库

### 接受单PR而非多个小PR
**Type:** positive
**Why:** 拆分反而造成不必要的开销
**How to apply:** 重构类需求优先合并为大PR
```

### 3. AutoDream 🌙

自动记忆整合系统，在空闲时整理记忆。

**触发条件：**
- 距离上次整合 >= 24 小时
- 新增 >= 3 个会话

**整合任务：**
1. 扫描现有记忆文件
2. 识别过时信息并删除
3. 更新 MEMORY.md 索引
4. 合并重复记忆

---

## 工具

### memory_search

语义搜索记忆文件。

```json
{
  "query": "用户偏好",
  "type": "user",
  "topK": 5
}
```

### memory_write

写入或追加记忆。

```json
{
  "file": "feedback/dev-rules.md",
  "content": "### 不要mock数据库\n**Type:** negative\n**Why:** ...\n**How to apply:** ...",
  "type": "feedback",
  "mode": "append"
}
```

### memory_flush

手动触发记忆持久化。

```json
{ "force": true }
```

### memory_dream ⭐

执行 AutoDream 记忆整合。

```json
{ "force": false }
```

- 默认检查触发条件（时间 + 会话数）
- `force: true` 强制执行

### memory_dream_status

查看 AutoDream 状态。

```json
{}
```

返回：
- 上次整合时间
- 距下次触发还需多久
- 当前记忆文件数

---

## 配置

```json
{
  "skills": {
    "memory-system": {
      "memoryDir": "~/.openclaw/workspace/memory",
      "flushMode": "safeguard",
      "softThresholdTokens": 300000,
      "vectorEnabled": true,
      "embeddingModel": "nomic-embed-text",
      "autoDream": {
        "enabled": true,
        "minHours": 24,
        "minSessions": 3
      }
    }
  }
}
```

### AutoDream 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | true | 是否启用 |
| `minHours` | 24 | 最小触发间隔（小时） |
| `minSessions` | 3 | 最小新增会话数 |

---

## 目录结构

```
memory/
├── MEMORY.md              # 索引文件
├── .auto-dream-state.json # AutoDream 状态
├── user/                  # 用户记忆
├── feedback/              # 反馈记忆
│   ├── positive/         # 正面确认
│   └── negative/         # 纠正指导
├── project/              # 项目记忆
├── reference/            # 引用记忆
└── sessions/             # 会话历史
```

---

## 最佳实践

### 保存记忆

```
了解用户 → 保存到 user/
收到反馈 → 保存到 feedback/
了解项目 → 保存到 project/
发现资源 → 保存到 reference/
```

### 格式规范

```markdown
### [标题]
**Type:** negative | positive
**Why:** [原因]
**How to apply:** [何时应用]
**Date:** YYYY-MM-DD
```

### 索引规范

- 每条索引 <= 150 字符
- 绝对日期代替相对日期
- 定期清理过时记忆

---

## 版本

**1.3.0** - AutoDream 支持 MiniMax LLM 整合  
**1.2.0** - AutoDream 自动整合系统  
**1.1.0** - 引入四类记忆分类 + Feedback 双向记录

---

**作者**：团宝 (openclaw)
