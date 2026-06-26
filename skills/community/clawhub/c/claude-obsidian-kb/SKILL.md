---
name: claude-obsidian-kb
description: >
  Claude-Obsidian 风格个人知识库构建与自动整理。当用户提到以下任何场景时激活：
  知识库、笔记整理、自动双向链接、Obsidian、第二大脑、卡片笔记、原子化笔记、
  个人知识管理、PKM、Zettelkasten、卢曼笔记法、笔记原子化、笔记链接、
  知识图谱笔记、raw/wiki/output三层、知识引擎、笔记自动归类、
  建立个人知识库、整理旧笔记、AI自动织网、知识复利、note-taking knowledge engine
author: 一休（赵铭远团队）
version: 1.0.0
---

# Claude-Obsidian 知识引擎

> 灵感来源：AgriciDaniel/claude-obsidian + Andrej Karpathy LLM Wiki 模式
> 核心理念：你只管写，AI负责整理、链接和维护——知识随时间复利增长

---

## 核心原则

**传统 AI 插件** = 问答机器人（Session级，无持久记忆）
**Claude-Obsidian 知识引擎** = AI员工（持久化 Vault，知识自动织网）

每次对话都是对知识库的写操作。AI 不只是回答问题，而是主动更新、维护、链接笔记。

---

## 三层架构

```
raw/         原始素材层：文章/论文/网页剪藏/会议记录，只增不改
wiki/        结构化知识层：AI编译后的 concepts · entities · topics
output/      产出层：基于 wiki 生成的报告/分析/回答
```

---

## 必选文件（Vault 根目录）

### 1. CLAUDE.md — AI 员工手册

Vault 根目录创建 `CLAUDE.md`，AI 启动时自动读取。结构：

```markdown
# AI 助手角色定义

## 身份
你是一个专业的知识管理员，负责维护[用户]的个人知识库。

## 关注领域
- [列出专业领域]

## 目录结构规范
- `raw/` — 原始素材，只增不改
- `wiki/` — 结构化知识
  - `wiki/concepts/` — 概念页
  - `wiki/entities/` — 实体页（人/组织/产品）
  - `wiki/topics/` — 主题页
- `output/` — 产出物

## frontmatter 模板
每个 wiki 页面必须包含：
title: 标题
type: concept | entity | topic
tags: [领域, 子领域]
sources: [来源链接或空数组]
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: 一句话描述（≤50字）

## 链接规则
- 首次提到概念 → `[[笔记名]]` 双向链接
- 同一笔记内同一概念只链接第一次
- 提到不存在实体 → 询问是否创建

## 行为准则
- 整理用户输入时，主动提取实体和概念
- 发现矛盾信息 → 添加 `[!contradiction]` 标记
- 定期检查孤儿笔记和死链
```

### 2. SCHEMA.md — 规范定义（≤50行）

```markdown
# 知识库规范

## 命名规范
- 概念页：全小写，英文优先，用 `-` 连接。如 `neural-network`
- 实体页：人名英文全名（姓在前）。如 `turing-alan`

## 标签体系
顶级标签（预设，禁止自创）：
[领域列表]

## frontmatter 必填字段
- title, type, tags, sources, created, updated, summary

## 目录结构
- 超过10篇笔记 → 建立子目录
- index.md 放在每个主要目录（3-5行导航）
```

---

## 核心工作流

### 工作流 A：输入素材 → wiki 化

```
用户输入素材（URL/文本/文件）
        ↓
[提取实体和概念]
        ↓
检查 vault 中是否存在对应笔记
  有 → 更新现有笔记 + 添加链接
  无 → 创建新笔记 + 链接
        ↓
写入 raw/（原始素材）+ wiki/（结构化页面）
更新相关笔记的双向链接
```

### 工作流 B：双向链接自动织网

```
扫描日记/笔记中的所有提及（人名/地名/书名/概念）
        ↓
对每个提及在 vault 中搜索
  存在 → 替换为 [[笔记名]] 双向链接
  不存在 → 创建对应实体页 → 链接
        ↓
生成孤儿笔记报告
```

### 工作流 C：知识整理（批量）

```
用户: "整理我所有的 [项目/领域] 笔记"
        ↓
扫描相关目录
        ↓
统一添加 frontmatter
建立双向链接
生成/更新 index.md
```

---

## 卡片笔记原子化标准

每张笔记只包含**一个**原子思想：

| 类型 | 内容 | 长度 |
|------|------|------|
| concept | 一个概念的定义+解释+例子 | 100-300字 |
| entity | 一个实体的关键事实 | 100-500字 |
| topic | 一个主题的现状+关键问题 | 300-800字 |

---

## 矛盾检测

发现两篇笔记对同一事实描述矛盾时：

1. 在矛盾处添加 `[!contradiction]` Obsidian callout
2. 记录矛盾双方
3. 在相关笔记的 summary 中标注"存在争议"
4. 提示用户核实

---

## 定期维护任务

| 任务 | 频率 | 操作 |
|------|------|------|
| 死链检测 | 每次对话末尾 | 检查 `[[链接]]` 是否存在 |
| 孤儿笔记报告 | 按需 | 无任何笔记链接的笔记 |
| 批量添加frontmatter | 按需 | 对缺少字段的笔记统一补全 |
| index.md 更新 | 按需 | 新增笔记后更新目录索引 |

---

## 脚本工具

运行方式：`python3 /workspace/skills/claude-obsidian-kb/scripts/<script>`

| 脚本 | 用途 |
|------|------|
| `auto_link.py` | 扫描笔记，检测死链，生成孤儿笔记报告 |
| `hot_cache.py` | 管理热缓存，维持跨session记忆 |
| `extract_entities.py` | 从文本中提取实体并建档 |

详细用法见 [references/scripts.md](references/scripts.md)

---

## 与 iBrain 项目的整合

当用户说 `iBrain` 或提到"个人第二大脑"时，将此 skill 的方法论带入：

- iBrain 的"卡片库" = Claude-Obsidian 的 wiki层
- iBrain 的"来源管理" = raw层
- CLAUDE.md 模式 → iBrain 的 AI行为定义文件
- 双向链接 → iBrain 的实体关系图谱

详见 [references/ibrain-integration.md](references/ibrain-integration.md)
