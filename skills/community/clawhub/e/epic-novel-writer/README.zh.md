# epic-novel-writer — 史诗级长篇写作工作流

一个面向长篇连载小说的 AI 驱动创作 SKILL，从世界观设定、人物塑造、章纲规划，到正文写作、版本存档、HTML 导引页生成，覆盖一部小说从零到出版的全生命周期。

**适配篇幅：中篇（10-25 万字）→ 长篇（25-60 万字）→ 超长篇（60-150 万字）**
> 💡 **实测标杆**：已用于生成 **420,000 字**（300 章，10 卷），验证了全局连续编号、防崩设定体系、HTML 导引页生成在超长篇场景下的可靠性。

## 🚀 为什么需要这个 SKILL？

写小说最难的不是"开始"，而是**持续 300 章不崩**。这个 SKILL 解决的是长篇写作中最痛苦的几个问题：

### 1. 文件编号 = 章编号，永远不迷路
```
chapter-001.md → 第 1 章
chapter-150.md → 第 150 章（不管它在哪一卷）
chapter-300.md → 第 300 章
```
**每卷内从 1 重新开始**是每个长篇写作者的噩梦。我们采用**全局连续编号**——文件名即章节号，打开文件夹就知道写到哪了。

### 2. 一键生成专业级存档
从 `references/archive-template.md` 出发，8 步流程自动生成：
- ✅ **全文合并版**（md + txt 双格式）
- ✅ **人物画像 JSON**（char_data.json，含角色名、定位、成长线、首次出场）
- ✅ **HTML 导引页**（暗色主题、响应式布局、人物卡网格、连续编号章节目录）
- ✅ **纯文本目录**（章节号 + 超链接）

### 3. 防崩设定体系
- **世界观模板**（`world-setting-template.md`）— 地理、历史、力量体系、核心矛盾
- **角色卡片模板**（`character-card-template.md`）— 性格、背景、能力成长弧线、登场退出追踪
- **章纲模板**（`chapter-blueprint-template.md`）— 每章场景设定、情节大纲、伏笔/线索追踪、技能调用记录

### 4. 只读存档，编辑自由
所有编辑在 `在编辑稿/` 下完成，存档版本（v1/v2/v3…）**只读**，随时可以对比、回溯、反向合并。

## 📋 包含什么

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 核心规则、工作流、命名规范、存档流程指引 |
| `references/archive-template.md` | 版本存档 8 步完整流程（目录结构 + 命令示例 + 检查清单） |
| `references/world-setting-template.md` | 世界观设定模板（地理/历史/力量体系/节奏规划） |
| `references/character-card-template.md` | 角色卡片模板（性格/背景/能力成长/登场追踪） |
| `references/chapter-blueprint-template.md` | 章纲模板（场景/情节/伏笔/技能调用） |

## 🔧 快速开始

### 1. 初始化项目

```bash
mkdir -p "我的小说/在编辑稿/{01-story-premise,02-world-setting,03-outline,04-chapters,05-references}"
```

### 2. 填写核心设定

从 `references/` 复制模板：
```bash
cp references/world-setting-template.md 在编辑稿/02-world-setting.md
cp references/character-card-template.md 在编辑稿/references/characters/主角.md
```

### 3. 开始写第一章

```bash
cp references/chapter-blueprint-template.md 在编辑稿/03-outline/chapter-001-blueprint.md
# 填写章纲后，在 04-chapters/ 创建 chapter-001.md
```

### 4. 存档

用户说"存成 v1"时：
```bash
# 阅读 references/archive-template.md，按 8 步流程执行
```

## 📐 项目结构

```
我的小说/
├── 在编辑稿/              ← 所有编辑在此
│   ├── 01-story-premise.md     # 故事设定
│   ├── 02-world-setting.md     # 世界观
│   ├── 03-chapters-written.md  # 章节状态
│   ├── 03-outline/             # 大纲
│   ├── 04-chapters/            # 正文（chapter-001.md ~ chapter-XXX.md）
│   ├── 05-reports/             # 过程报告
│   └── references/             # 参考文档
├── 我的小说_v1/               ← 存档（只读）
├── 我的小说_v2/               ← 存档（只读）
└── ……
```

## ⚠️ 核心规则

1. **所有编辑在 `在编辑稿/` 下完成**，不碰存档目录
2. **存档版本只读**，用于对比、回溯
3. **全局连续编号**：`chapter-001.md` = 第 1 章，不随卷重置
4. **存档时需生成人物画像 JSON + HTML 导引页**

## 📏 适用篇幅

| 篇幅 | 章节数 | 字数范围 | 推荐程度 |
|------|--------|---------|---------|
| 中篇 | 30-80 章 | 10-25 万字 | ✅ 完全覆盖 |
| 长篇 | 80-200 章 | 25-60 万字 | ✅ 完美匹配 |
| 超长篇 | 200-500 章 | 60-150 万字 | ✅ 完全胜任 |

> 💡 **实测标杆**：本项目已用于生成 **420,000 字**（300 章，10 卷），验证了全局连续编号、防崩设定体系、HTML 导引页生成等核心功能在超长篇场景下的可靠性。

## 🏷️ 适用场景

- 长篇连载小说（100 章+）
- 网络文学/轻小说/奇幻/科幻
- AI 辅助写作（大模型生成 + 人工润色）
- 多人协作（每人在 `在编辑稿/` 下工作，定期存档）
- 世界观复杂、角色众多的作品

## 📦 安装

```bash
clawhub install epic-novel-writer
```

## 🔄 更新

```bash
clawhub update epic-novel-writer
```

## 📄 协议

BSD 3-Clause License

Copyright (c) 2026, sunshinejnjn@github

---

> 用结构化流程对抗长篇写作的混沌。从第 1 章到第 300 章，每一步都有据可查。
