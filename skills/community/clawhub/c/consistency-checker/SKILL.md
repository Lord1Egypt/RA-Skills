---
name: consistency-checker
description: 一致性检查器 - 检测小说章节中的一致性问题。当需要检查角色名称、特征、时间线、地点描述是否前后一致时使用。
---

# Consistency Checker - 一致性检查器

## Overview

读取角色档案和章节正文，自动检测一致性问题，包括角色名称不一致、特征矛盾、时间线混乱、地点描述矛盾等。

**使用场景**：
- 需要检查章节与角色档案的一致性
- 需要发现前后矛盾的描述
- 需要确保时间线连贯
- 需要在发布前进行一致性审核

## 检测项目

| 检测项 | 说明 |
|--------|------|
| **角色名称** | 检测同一角色的不同称呼/译名 |
| **特征矛盾** | 检测与角色档案矛盾的描述（如眼睛颜色、年龄等） |
| **时间线** | 检测时间描述是否连贯（如"第二天"vs"三天后"） |
| **地点矛盾** | 检测地点描述是否前后一致 |
| **关系矛盾** | 检测角色关系是否与档案一致 |

## CLI 使用

```bash
# 基本用法
python3 scripts/check_consistency.py --book-dir projects/my-novel --chapter chapters/chapter-01.md

# 输出报告到文件
python3 scripts/check_consistency.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md \
  --output reports/chapter-01-consistency.md

# 简写
python3 scripts/check_consistency.py -d ./project -c chapter.md -o report.md
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--book-dir` / `-d` | ✅ | 小说项目目录路径 |
| `--chapter` / `-c` | ✅ | 章节文件路径（相对于 book-dir） |
| `--output` / `-o` | ❌ | 输出报告文件路径 |

## 项目目录结构

```
projects/my-novel/
├── characters/         # 角色档案（必需）
│   ├── 主角.yml
│   └── 配角.yml
├── chapters/           # 章节正文
│   └── chapter-01.md
└── reports/            # 检查报告输出
    └── chapter-01-consistency.md
```

## 角色档案格式 (characters/*.yml)

```yaml
name: 林风
aliases:
  - 林侦探
  - 风哥
gender: 男
age: 35
features:
  - 黑色短发
  - 灰色眼睛
  - 左眉疤痕
occupation: 私家侦探
relationships:
  苏雨：咖啡馆老板娘，朋友
background: 前刑警
```

## 输出报告格式

```markdown
# 一致性检测报告

**章节**: chapters/chapter-01.md
**检测时间**: 2026-04-04 23:55:00
**问题数量**: 3

## 检测结果

| 检测项 | 状态 | 问题数 |
|--------|------|--------|
| 角色名称 | ⚠️ 警告 | 1 |
| 特征矛盾 | ✅ 通过 | 0 |
| 时间线 | ⚠️ 警告 | 1 |
| 地点矛盾 | ✅ 通过 | 0 |
| 关系矛盾 | ✅ 通过 | 0 |

## 问题详情

### 角色名称不一致
- "林峰" → 应为 "林风"（出现 2 次）

### 时间线混乱
- 第 5 段："第二天清晨"
- 第 12 段："三天后的夜晚"
- 建议：检查时间跨度是否合理

## 建议

1. 统一使用 "林风" 作为角色名称
2. 核实时间线是否连贯
```

## 依赖

- Python 3.8+
- rich (终端渲染)
- PyYAML (配置文件解析)

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 与其他技能集成

### 与 novel-writer 集成

```bash
# 1. 生成章节正文
python3 ../novel-writer/scripts/write_chapter.py \
  --book-dir projects/my-novel \
  --chapter 1 \
  --output chapters/chapter-01.md

# 2. 检查一致性
python3 scripts/check_consistency.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md \
  --output reports/chapter-01-consistency.md
```

### 与 quality-checker 集成

```bash
# 1. 质量检测
python3 ../quality-checker/scripts/check_quality.py \
  --input chapters/chapter-01.md \
  --output reports/chapter-01-quality.md

# 2. 一致性检查
python3 scripts/check_consistency.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md \
  --output reports/chapter-01-consistency.md
```

## 注意事项

- 角色档案目录（characters/）为必需
- 支持 UTF-8 和 GBK 编码
- 时间线检测基于关键词识别，可能不完全准确
- 建议每章完成后立即进行一致性检查
