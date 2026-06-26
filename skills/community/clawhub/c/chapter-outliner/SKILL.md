---
name: chapter-outliner
description: 章节大纲生成器 - 基于 15 节拍系统生成小说章节大纲。当需要根据故事大纲和章节号创建详细写作大纲时使用，支持字数分配、角色参考、风格注入。
---

# Chapter Outliner - 章节大纲生成器

## Overview

根据小说项目文件（outline.md, style.yml, characters/）和章节号，自动生成结构化的 15 节拍章节大纲，包含字数分配、角色参考和风格备注。

**使用场景**：
- 需要为具体章节创建详细写作大纲
- 需要确保章节符合 15 节拍结构
- 需要分配字数到各个节拍
- 需要整合角色档案和风格配置

## 15 节拍系统

| 阶段 | 节拍 | 名称 | 用途 |
|------|------|------|------|
| **铺垫** | 1 | 钩子 | 吸引读者注意 |
| | 2 | 设定 | 建立场景背景 |
| | 3 | context | 提供上下文 |
| **转折** | 4 | inciting | 引入冲突 |
| | 5 | 发展 | 情节推进 |
| | 6 | turning | 转折点 |
| | 7 | 转折 | 方向变化 |
| **高潮** | 8 | 对抗 | 矛盾激化 |
| | 9 | 发展 | 高潮铺垫 |
| | 10 | 高潮 | 冲突顶点 |
| | 11 | 转折 | 高潮转折 |
| **结局** | 12 | 解决 | 问题解决 |
| | 13 | 收尾 | 情节收尾 |
| | 14 | 余韵 | 情感延续 |
| | 15 | 结局 | 章节结束 |

## CLI 使用

```bash
# 基本用法
python3 scripts/generate_outline.py --book-dir projects/my-novel --chapter 1

# 指定字数
python3 scripts/generate_outline.py \
  --book-dir projects/my-novel \
  --chapter 5 \
  --word-count 5000

# 输出到文件
python3 scripts/generate_outline.py \
  --book-dir projects/my-novel \
  --chapter 10 \
  --output outlines/chapter-10.md

# 简写
python3 scripts/generate_outline.py -d ./project -c 5 -w 3000 -o output.md
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--book-dir` / `-d` | ✅ | 小说项目目录路径 |
| `--chapter` / `-c` | ✅ | 章节编号 |
| `--word-count` / `-w` | ❌ | 目标字数（默认 3000） |
| `--output` / `-o` | ❌ | 输出文件路径（缺省则只显示） |

## 项目目录结构

```
projects/my-novel/
├── outline.md          # 故事大纲（可选）
├── style.yml           # 风格配置（可选）
├── characters/         # 角色档案（可选）
│   ├── 主角.yml
│   └── 配角.yml
└── chapters/
    └── outlines/       # 章节大纲输出
```

## 输出大纲格式

```markdown
# 第 1 章 大纲

**字数目标**: 3000 字
**生成时间**: 2026-04-04 23:30:00

## 章节概述
[来自 outline.md 的章节摘要]

## 15 节拍大纲

### 1. 钩子 (铺垫)
**目标字数**: 135 字
**目的**: 建立场景和基础信息

第 1 节拍 - 待填充

### 2. 设定 (铺垫)
**目标字数**: 157 字
**目的**: 建立场景和基础信息

第 2 节拍 - 待填充

...

## 角色参考

### 林风
私家侦探，35 岁，冷静敏锐...
```

## 字数分配规则

| 阶段 | 总占比 | 说明 |
|------|--------|------|
| 铺垫 | 15% | 场景建立 |
| 转折 | 20% | 冲突引入 |
| 高潮 | 45% | 核心内容 |
| 结局 | 20% | 收尾解决 |

## 依赖

- Python 3.8+
- rich (终端渲染)
- PyYAML (配置文件解析)

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 与其他技能集成

### 与 style-analyzer 集成

```bash
# 1. 分析参考文本风格
python3 ../style-analyzer/scripts/analyze_style.py \
  --input reference.txt \
  --output style.yml

# 2. 生成章节大纲（自动读取 style.yml）
python3 scripts/generate_outline.py \
  --book-dir projects/my-novel \
  --chapter 1
```

### 与 novel-writer 集成

```bash
# 1. 生成章节大纲
python3 scripts/generate_outline.py \
  --book-dir projects/my-novel \
  --chapter 5 \
  --output chapters/outlines/chapter-5.md

# 2. novel-writer 根据大纲生成正文
```

## 注意事项

- 项目文件（outline.md, style.yml, characters/）均为可选
- 缺少文件时会自动使用默认值
- 输出 Markdown 可直接用于 novel-writer 输入
- 15 节拍名称和阶段可自定义修改
