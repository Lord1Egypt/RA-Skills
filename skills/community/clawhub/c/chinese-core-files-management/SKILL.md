---
name: core-files-management
description: "OpenClaw 工作区核心文件管理。使用时机：(1) 管理或更新核心 Markdown 文件（identity.md、soul.md、agents.md、user.md、memory.md、tools.md、bootstrap.md），(2) 检查文件组织，(3) 确保核心文件之间无重复，(4) 应用语言规则，(5) 用户或集群询问文件结构或管理。本技能管理 OpenClaw 工作区中的 6 个核心文件 + bootstrap.md。语言规则：用户通信 → 代理母语，代理之间 → 中文，代码/技术 → English。"
---

# 📁 核心文件管理

> OpenClaw 工作区核心文件的通用管理

| 信息 | 值 |
|------|-----|
| **版本** | 1.1.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 目的和范围

### 目标

管理 OpenClaw 工作区中的 6 个核心文件 + bootstrap.md，避免重复。

### 通用设计

本技能适用于任何 OpenClaw 代理。根据用户偏好调整语言规则。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| 修改核心文件 | 检查分发规则 |
| 验证组织 | 读取所有核心文件 |
| 避免重复 | 使用修改清单 |
| 用户询问结构 | 阅读本技能并给出总结 |

---

## 2. 6 个核心文件

| # | 文件 | 定义 | 关键内容 |
|---|------|------|---------|
| 1 | **identity.md** | 代理的"第一印象" | 名称、头像、签名、功能、语言架构 |
| 2 | **soul.md** | 代理的"心脏" — 个性与价值观 | 本质、价值观、L7/L8 记忆集成 |
| 3 | **agents.md** | 逻辑与程序手册 | 规格、工作区规则、心跳、红线 |
| 4 | **user.md** | 用户上下文 | 用户信息、偏好、基础设施 |
| 5 | **memory.md** | 长期记忆 | 重要事件、关键配置、工作流程 |
| 6 | **tools.md** | 技术配置 | 端点、主机、命令、服务 |

### 加：bootstrap.md

| 文件 | 定义 | 用途 |
|------|------|------|
| **bootstrap.md** | 机器启动序列 | 不是灵魂 — 仅机器启动顺序 |

---

## 3. 分发规则

| 内容类型 | 目标文件 |
|----------|----------|
| 身份 | `identity.md` |
| 个性/价值观 | `soul.md` |
| 操作规则 | `agents.md` |
| 用户上下文 | `user.md` |
| 持久事实 | `memory.md` |
| 技术配置 | `tools.md` |
| 启动序列 | `bootstrap.md` |

**规则：** 每个文件只有一个目的。不要混合内容类型。

### 集群集成

| 组件 | 用途 | 位置 |
|------|------|------|
| identity.md | 代理第一印象 | 工作区根目录 |
| soul.md | 代理心脏 | 工作区根目录 |
| agents.md | 操作规则 | 工作区根目录 |
| 集群配置 | 代理连接 | workspace/cluster/ |
| 技能存储 | 发布的技能 | workspace/skills/ |

---

## 4. 语言规则

适应您的代理上下文：

| 上下文 | 语言 | 示例 |
|--------|------|------|
| **用户通信** | 代理母语 | "你好！" / "Bonjour!" / "Hello!" |
| **代理之间** | 中文 | "你好！很高兴与你交流" |
| **代码/技术** | English | `python3 script.py` |

**规则：** 每个 identity.md 必须声明用户通信语言。

---

## 5. 工具

### 必需的 OpenClaw 工具

| 工具 | 用途 | 模式 |
|------|------|------|
| `read` | 读取核心文件 | 必需 |
| `write` | 修改核心文件 | 必需 |
| `edit` | 修复特定部分 | 可选 |
| `exec` | 验证文件状态、备份 | 可选 |

### 验证命令

```bash
# 列出核心文件
ls -la ~/.openclaw/workspace/*.md

# 检查文件内容
head -20 ~/.openclaw/workspace/identity.md

# 修改前备份
cp ~/.openclaw/workspace/<file>.md ~/.openclaw/workspace/<file>.md.bak

# 统计所有文件行数
wc -l ~/.openclaw/workspace/*.md

# 验证文件存在
test -f ~/.openclaw/workspace/identity.md && echo "exists"

# 统计文件数量
ls ~/.openclaw/workspace/*.md | wc -l

# 完整文件列表
find ~/.openclaw/workspace -maxdepth 1 -name "*.md" -type f
```

### 所需权限

| 权限 | 用途 |
|------|------|
| 读取工作区 | 访问核心文件 |
| 写入工作区 | 修改核心文件 |
| 执行（可选） | 文件操作、备份 |

### 备份与恢复

```bash
# 创建备份
cp ~/.openclaw/workspace/identity.md ~/.openclaw/workspace/identity.md.backup

# 从备份恢复
cp ~/.openclaw/workspace/identity.md.backup ~/.openclaw/workspace/identity.md

# 列出备份
ls ~/.openclaw/workspace/*.backup
```

---

## 6. 修改清单

修改任何核心文件之前：

```
1. 此内容属于哪个文件？
   → 身份 → identity.md
   → 个性/价值观 → soul.md
   → 操作规则 → agents.md
   → 用户 → user.md
   → 持久事实 → memory.md
   → 技术配置 → tools.md

2. 它是否已在其他地方？
   → 检查所有 6 个核心文件

3. 语言规则清楚吗？
   → 用户 → 他们的母语
   → 代理 → 中文
   → 代码 → English

4. 需要备份吗？
   → 是 → 先备份！
```

---

## 7. 文件路径

| 文件 | 默认路径 |
|------|----------|
| identity.md | `~/.openclaw/workspace/identity.md` |
| soul.md | `~/.openclaw/workspace/soul.md` |
| agents.md | `~/.openclaw/workspace/agents.md` |
| user.md | `~/.openclaw/workspace/user.md` |
| memory.md | `~/.openclaw/workspace/memory.md` |
| tools.md | `~/.openclaw/workspace/tools.md` |
| bootstrap.md | `~/.openclaw/workspace/bootstrap.md` |

---

## 8. 约束

| 约束 | 描述 |
|------|------|
| **无重复** | 工作区规则仅在 agents.md，不在 soul.md 或 identity.md |
| **无混合** | tools.md 仅限技术 — 不含个性内容 |
| **无膨胀** | memory.md 不包含完整会话日志 |
| **先备份** | 更改核心文件前始终备份 |
| **每文件一目的** | 不要混合内容类型 |

---

## 9. 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 内容在错误位置 | 未检查分发规则 | 重新阅读清单，重新分配 |
| 重复 | 相同内容在多个地方 | 合并，只保留一个 |
| 缺少语言 | 未检查语言规则 | 添加用户母语 |
| 数据丢失 | 修改前未备份 | 从备份恢复 |

### 安全问题

| 问题 | 严重性 | 行动 |
|------|--------|------|
| 未备份就覆盖 | 高 | 始终先备份 |
| 修改了错误文件 | 中 | 写入前验证 |
| 缺少语言规则 | 低 | 添加到 identity.md |

---

## 10. 边缘情况

| 情况 | 处理方式 |
|------|----------|
| **文件缺失** | 从头创建正确格式 |
| **文件损坏** | 从备份恢复或重新创建 |
| **大量重复** | 读取所有文件，按类型重新组织 |
| **新代理设置** | 创建所有 6 个核心文件 + bootstrap.md |
| **路径不清楚** | 使用默认 `~/.openclaw/workspace/` |

---

## 11. 使用命令

```bash
# 列出所有核心文件
ls -la ~/.openclaw/workspace/*.md

# 检查特定文件
head -20 ~/.openclaw/workspace/identity.md

# 修改前备份
cp ~/.openclaw/workspace/<file>.md ~/.openclaw/workspace/<file>.md.bak

# 统计所有文件行数
wc -l ~/.openclaw/workspace/*.md
```

---

## 12. 模板 — 空核心文件

### identity.md

```markdown
# IDENTITY.md — [代理名称]

> 身份 = 第一印象

| 属性 | 值 |
|------|-----|
| **名称** | [你的名字] |
| **签名** | [你的签名表情] |
| **角色** | [你的角色] |

## 语言规则

- 用户通信：[母语]
- 代理之间：中文
- 代码/技术：English

_In Altum Per [你的原则]。_
[你的名字]
```

---

_In Altum Per CoreFiles._
📁 核心文件管理 v1.1