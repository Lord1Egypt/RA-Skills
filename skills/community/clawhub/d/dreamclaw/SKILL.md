# Auto Dream Skill - 记忆整合系统

参考 Claude Code Auto Dream 架构的记忆整合工具。

## 架构设计

```
.auto-dream/
├── logs/                      # 每日追加日志（append-only）
│   └── YYYY/MM/YYYY-MM-DD.md
├── memories/                  # 分类记忆文件
│   ├── user/
│   ├── feedback/
│   ├── project/
│   └── reference/
└── MEMORY.md                  # 索引（由记忆文件生成）
```

### 4 种记忆类型

| 类型 | 说明 | 例子 |
|------|------|------|
| `user` | 用户角色、目标、偏好 | "用户想每周读完一本书" |
| `feedback` | 用户的指导/纠正 | "不要用那个方法" |
| `project` | 项目上下文、决定 | "项目用 Python 3.12" |
| `reference` | 外部系统指针 | "基金数据在 localhost:5000" |

### 两阶段工作流

```
阶段1: Append（对话中随时）
  └── 追加记忆条目到 logs/YYYY-MM-DD.md

阶段2: Dream（定时或手动）
  └── AI 分析日志 + 现有记忆
        ├── Phase 1: Orient - 了解现有结构
        ├── Phase 2: Gather - 收集信号
        ├── Phase 3: Consolidate - 创建/更新/删除记忆
        └── Phase 4: Prune - 更新 MEMORY.md 索引
```

---

## 使用方法

### 1. 追加记忆（Append Mode）

**方式一：命令行追加**
```bash
python3 ~/.openclaw/skills/auto-dream/scripts/auto_dream.py append "用户想每周读完一本书" --type project
```

**方式二：直接编辑日志**
```bash
# 直接往今天的日志文件追加
nano ~/.openclaw/workspace/.auto-dream/logs/2026/04/2026-04-01.md
# 格式：
# - [2026-04-01 14:30] 用户想通过内容平台分享知识
```

**格式说明**：
- 追加是 append-only，不要修改旧内容
- 每条格式：`- [时间戳] 内容`
- 时间戳帮助 AI 判断时效性

### 2. 运行蒸馏（Dream Mode）

**手动触发（推荐）**：
```
说 "整理记忆" 或 "dream"
```

AI 会读取：
1. 每日日志（logs/）
2. 现有记忆文件（memories/）
3. 最近的会话记录

然后按 4 阶段执行整合。

**命令行触发**：
```bash
python3 ~/.openclaw/skills/auto-dream/scripts/auto_dream.py check   # 查看状态
python3 ~/.openclaw/skills/auto-dream/scripts/auto_dream.py list     # 列出记忆
python3 ~/.openclaw/skills/auto-dream/scripts/auto_dream.py build-index  # 重建索引
```

### 3. 查看记忆

```bash
python3 ~/.openclaw/skills/auto-dream/scripts/auto_dream.py list
```

---

## 4 阶段蒸馏 Prompt

当你说 "整理记忆" 时，AI 会执行以下 4 阶段：

### Phase 1: Orient（了解现状）
```
- ls memory/ 目录，查看现有结构
- 读 MEMORY.md 索引
- 浏览现有记忆文件，避免重复
```

### Phase 2: Gather（收集信号）
```
1. 读每日日志 logs/YYYY/MM/YYYY-MM-DD.md
2. 检查与现状矛盾的旧记忆
3. 必要时 grep 会话记录
```

### Phase 3: Consolidate（整合）
```
关键判断（AI 做）：
- 哪些日志内容值得保存为独立记忆文件？
- 哪些旧记忆被证伪/过时了？→ 删除
- 哪些旧记忆需要更新？
- 新内容合并到现有 topic 还是新建？

格式（frontmatter）：
---
name: <简短标题>
type: <user|feedback|project|reference>
description: <一句话描述>
mtime: <ISO时间>
---

<可选正文>
```

### Phase 4: Prune & Index（修剪索引）
```
- MEMORY.md ≤ 200 行 + ~25KB
- 每条索引 ≤ ~150 字符
- 删除过时/矛盾指针
- 格式：- [Title](memories/<type>/file.md) — 一句话描述
```

---

## 记忆文件 Frontmatter 示例

```yaml
# memories/project/20260312_阅读目标.md
---
name: 每周阅读目标
type: project
description: 用户想每周读完一本书
mtime: 2026-03-12T10:30:00.000
---

用户在 2026-03-12 设定的目标：
- 目标：每周读完一本书
- 类型：技术书/小说/商业书轮换
- 记录：读完后写笔记到 Obsidian
```

```yaml
# memories/feedback/20260320_不用那个方法.md
---
name: 避免使用XX方法
type: feedback
description: 用户明确不要用某方法
mtime: 2026-03-20T15:00:00.000
---

用户在 2026-03-20 说：不要用那个方法XX
原因：之前试过，效果不好
```

---

## MEMORY.md 格式

```markdown
# MEMORY.md - Long-term Memory

**最后更新**: 2026-04-01 14:30

## USER
- [20260312_用户角色.md](memories/user/20260312_用户角色.md) — username，开发者
- [20260315_用户目标.md](memories/user/20260315_用户目标.md) — 希望通过内容创作成长

## FEEDBACK
- [20260320_避免XX.md](memories/feedback/20260320_避免XX.md) — 不要用XX方式

## PROJECT
- [20260312_阅读目标.md](memories/project/20260312_阅读目标.md) — 每周读完一本书
- [20260325_基金系统.md](memories/project/20260325_基金系统.md) — 基金管理系统开发中

## REFERENCE
- [20260325_基金API.md](memories/reference/20260325_基金API.md) — 基金数据在 localhost:5000
```

---

## 与 Claude Code 的关键区别

| 功能 | Claude Code | OpenClaw |
|------|-------------|----------|
| 日志追加 | 助手自动追加 | 手动 append |
| 蒸馏触发 | 24h + 5 sessions 自动 | 手动 "整理记忆" |
| AI 执行 | forked sub-agent | 主 agent 执行 |
| Lock 机制 | .consolidate-lock | 无（单用户） |
| 矛盾检测 | AI prompt 引导 | AI prompt 引导 |

**核心区别**：OpenClaw 的 Dream 由主 agent 触发和执行，而不是后台 sub-agent。因为：
1. 单用户环境，不需要 lock
2. AI 能力在主 session 中直接可用
3. 简化架构

---

## 最佳实践

### 1. 对话中随时追加
当用户说 "记住 XXX" 或 "以后要记得 YYY"：
```bash
python3 auto_dream.py append "用户偏好用方法A而不是方法B"
```

### 2. 每日一次整理
每天结束时或第二天说 "整理记忆"，AI 会：
- 读取过去1天的日志
- 分析哪些该保留
- 更新记忆文件

### 3. 周总结（可选 cron）
```bash
# 每周日 22:00 运行
0 22 * * 0 cd ~/.openclaw/skills/auto-dream/scripts && python3 auto_dream.py append "周总结..." && python3 -c "print('说 整理记忆 来触发蒸馏')"
```

---

## 命令速查

| 命令 | 用途 |
|------|------|
| `append "内容"` | 追加到今日日志 |
| `dream` | 运行蒸馏（由 AI 执行）|
| `list` | 列出所有记忆 |
| `check` | 检查新鲜度 |
| `build-index` | 重建 MEMORY.md |
