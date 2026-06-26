# Skill 命名与分类规范

> 本文件定义 skill 的**外部规范**（命名、分类、标签、版本、边界划分）。
> SKILL.md 内部结构规范见 `skillmd-structure.md`。
> 整理时间：2026-04-23

## 文档分工

| 文件 | 覆盖内容 |
|------|---------|
| naming-conventions.md | 命名、分类、标签、版本、边界划分 |
| skillmd-structure.md | SKILL.md 章节层级、代码块、表格、避坑指南格式 |

## Skill 命名规范

### 命名格式

**格式：** 小写字母 + 连字符
**长度：** 最多 64 字符
**字符集：** a-z、0-9、连字符（-）

```yaml
# ✅ 正确
name: swift-language
name: apple-design
name: distill-skill-builder
name: musk-eeg
name: wikipedia-eeg-crawler

# ❌ 错误
name: Swift Language        # 有空格
name: SWIFT_LANGUAGE       # 有下划线
name: swift.language        # 有点号
name: swift language skill  # 有空格
name: swiftLanguage         # 驼峰命名
```

### 命名约定

#### 按平台命名

```yaml
# iOS 相关
name: ios-dev
name: ios-development
name: apple-design

# Android 相关
name: android-dev
name: android-development

# Flutter
name: flutter-dev
name: flutter-development

# 跨平台
name: react-native-dev
name: kotlin-multiplatform
```

#### 按技术领域命名

```yaml
# 编程语言
name: swift-language
name: python-expert
name: typescript-advanced
name: rust-core

# 框架
name: nextjs-guide
name: vue3-composition-api
name: react-hooks

# 数据库
name: postgresql-internals
name: sqlite-best-practices
name: redis-performance
```

#### 按功能命名

```yaml
# 开发工具
name: git-advanced
name: docker-mastery
name: kubernetes-operations

# AI/ML
name: llm-prompt-engineering
name: ml-pytorch-fundamentals
name: transformers-deep-dive

# 特定技能
name: code-review-expert
name: system-design-101
name: api-design-principles
```

### 命名优先级

1. **核心功能** — 技术栈、框架、语言优先
2. **平台** — 特定平台的 skill 用平台名开头
3. **简洁性** — 越短越好，但要明确
4. **一致性** — 与现有 skill 命名风格保持一致

### 常见错误

```yaml
# ❌ 命名过长
name: a-very-long-skill-name-that-is-hard-to-read

# ❌ 使用缩写（不通用）
name: swift-lang  # OK，但 swift-language 更明确
name: js-expert   # JS 不如 JavaScript 明确

# ❌ 与已有 skill 冲突
name: apple-design  # 已存在

# ❌ 过于宽泛
name: programming    # 太宽泛
name: development   # 太宽泛
```

---

## Skill 分类体系

### 按领域分类

| 类别 | 说明 | 示例 |
|------|------|------|
| `platform` | 特定平台开发 | ios-dev, android-dev, flutter-dev |
| `language` | 编程语言 | swift-language, python-expert |
| `framework` | 框架/库 | react-hooks, vue3-composition |
| `tool` | 开发工具 | git-advanced, docker-mastery |
| `ai-ml` | AI/机器学习 | llm-prompt-engineering, ml-pytorch |
| `database` | 数据库 | postgresql-internals, redis-perf |
| `infrastructure` | 基础设施 | kubernetes-ops, aws-architecture |
| `design` | 设计规范 | apple-design, material-design |
| `productivity` | 效率工具 | obsidian-knowledge, notion-workflow |
| `personality` | 人物蒸馏 | musk, naval, jobs, graham |

### 按层级分类

#### Level 1: 平台级
- 覆盖整个平台的完整知识
- 示例：`ios-dev`, `android-dev`, `flutter-dev`

#### Level 2: 技术栈级
- 覆盖特定技术栈的深度知识
- 示例：`swift-language`, `react-advanced`

#### Level 3: 专题级
- 覆盖特定主题的深度知识
- 示例：`widget-development`, `localization-guide`

### 按用途分类

| 类型 | 说明 | 触发场景 |
|------|------|---------|
| `knowledge` | 知识参考型 | "解释 X"、"X 是什么" |
| `action` | 行动执行型 | "帮我做 X"、"实现 X" |
| `analysis` | 分析评估型 | "分析 X"、"评估 X" |
| `creative` | 创意生成型 | "生成 X"、"创作 X" |

---

## 标签体系

### 标签格式

```yaml
tags:
  - <primary-tag>    # 主要标签
  - <secondary-tag>  # 次要标签
  - <platform>       # 平台
  - <language>       # 语言
  - <framework>      # 框架
```

### 推荐标签

#### 平台标签
```yaml
- ios
- android
- flutter
- harmonyos
- windows
- macos
- linux
- web
```

#### 语言标签
```yaml
- swift
- python
- javascript
- typescript
- kotlin
- dart
- go
- rust
```

#### 技术标签
```yaml
- swiftui
- uikit
- react
- vue
- nextjs
- django
- flask
```

#### 概念标签
```yaml
- concurrency
- async-await
- protocols
- generics
- dependency-injection
- testing
- performance
- security
```

### 标签使用规范

```yaml
# ✅ 正确：标签清晰、有层次
tags:
  - swift
  - swift-language
  - swift6
  - ios
  - apple
  - programming-language

# ❌ 错误：标签重复、混乱
tags:
  - ios-dev
  - iOS
  - swift development
  - swift
```

---

## Skill 边界划分

### 边界冲突检测

创建新 skill 前，检查是否与现有 skill 冲突：

```bash
# 检查同名或相似 skill
ls <skill_dir>/ | grep -i <keyword>

# 检查标签重叠
grep -r "tags:" <skill_dir>/*/SKILL.md | grep -i <keyword>
```

### 边界划分原则

#### 原则 1：单一职责

每个 skill 专注于一个领域：

```yaml
# ✅ 好：一个 skill 一个职责
name: swift-language      # Swift 语言
name: ios-dev            # iOS 开发
name: apple-design       # Apple 设计规范

# ❌ 差：一个 skill 多个职责
name: swift-ios-apple    # 混合了多个领域
```

#### 原则 2：层次清晰

不同层次的 skill 不重叠：

```
apple-design (Level 1: Apple 设计规范)
  └── 不包含 iOS 开发细节
ios-dev (Level 1: iOS 开发)
  └── 不包含 Apple 设计规范细节
swift-language (Level 2: Swift 语言)
  └── 独立于平台，可被多个平台使用
```

#### 原则 3：触发词不冲突

触发词可以有重叠，但主触发词不应完全相同：

```yaml
# ios-dev 的主触发词
trigger: iOS 开发|iOS app|SwiftUI|UIKit

# swift-language 的主触发词
trigger: Swift 语法|Swift 类型|Swift 闭包

# 触发词有重叠但不冲突
# 用户问 "SwiftUI" → ios-dev
# 用户问 "Swift 闭包" → swift-language
```

### 常见边界冲突及解决方案

| 冲突 | 原因 | 解决方案 |
|------|------|---------|
| swift-language vs ios-dev | Swift 既是语言又是 iOS 开发语言 | ios-dev 侧重 SwiftUI/UIKit，swift-language 侧重纯 Swift 语法 |
| apple-design vs ios-dev | Apple 设计规范和 iOS 开发有重叠 | apple-design 侧重 HIG 设计原则，ios-dev 侧重代码实现 |
| flutter-dev vs dart | Flutter 和 Dart 强关联 | flutter-dev 侧重 Flutter 框架，dart-expert 侧重 Dart 语言 |

---

## Skill 版本管理

### 版本号格式

```yaml
hermes:
  version: "1.0"  # 语义版本：MAJOR.MINOR
```

### 版本规则

| 版本 | 说明 | 何时升级 |
|------|------|---------|
| MAJOR | 不兼容的 API 变更 | 重写核心内容 |
| MINOR | 向后兼容的功能增加 | 新增章节、参考文档 |
| PATCH | 向后兼容的问题修复 | 修复错误、补充内容 |

### 更新频率

```yaml
hermes:
  last_updated: "2026-04-23"
```

**更新触发条件：**
- 新增重要 API 或特性
- 官方文档有重大更新
- 发现错误或过时内容
- 评估分数下降需要修复

---

## Skill 描述规范

### description 字段

**长度：** 30-100 字
**格式：** 一句话描述

```yaml
# ✅ 正确：描述清晰、触发条件明确
description: Swift 语言权威参考。覆盖 Swift 6.3 完整语法、类型系统、集合类型、函数、闭包、协议、泛型、并发、安全特性。当用户询问 Swift 语法、类型、关键字、标准库 API、SwiftUI 基础语法，或要求解释 Swift 代码时触发。

# ✅ 正确：简洁明了
description: Apple Human Interface Guidelines 权威参考。覆盖 Apple 平台设计原则、组件规范、交互模式。当用户询问 Apple 设计规范、iOS 界面设计原则，或需要 UI 设计参考时触发。

# ❌ 错误：太泛
description: iOS 开发相关技能

# ❌ 错误：太长
description: Swift 语言权威参考...（超过 100 字）
```

### 描述结构

```
<技能名称>。<核心覆盖内容>。<触发场景>。
```

---

## Skill 目录结构规范

### 标准目录结构

```
<skill-name>/
├── SKILL.md                    # 主技能文件（必须）
├── references/                 # 参考文档目录（必须）
│   ├── topic-1.md            # 深度参考文档
│   ├── topic-2.md
│   └── ...
├── templates/                  # 模板目录（可选）
│   ├── template-1.md
│   └── ...
└── assets/                     # 资源目录（可选）
    ├── diagram-1.svg
    └── ...
```

### 目录命名规范

```bash
# ✅ 正确
references/
templates/

# ❌ 错误
Reference/    # 大写
ref_docs/      # 缩写
raw-data/      # 中划线
Script/        # 大写
```

---

## Skill 发布检查清单

### 发布前检查

```bash
# 1. 评估分数达到 A 级（90+）
python ../../distill-skill-builder/scripts/skill_evaluator_v2.py \
   <skill_dir>/<skill-name>

# 2. 检查触发词不与现有 skill 冲突
grep "trigger:" SKILL.md

# 3. 检查目录结构完整
ls -la <skill_dir>/<skill-name>/

# 4. 检查参考文档数量和行数
wc -l references/*.md

# 5. 检查同步到 Hermes
ls <hermes_dir>/<skill-name>/

# 6. 测试 skill 可用性
# 使用 skill_view 加载并测试
```

### 必需文件

- [ ] SKILL.md
- [ ] references/ 目录（非空）
- [ ] 至少 1 个参考文档

### 推荐文件

（当前推荐目录结构无推荐文件）

---

## 来源

> apple-design SKILL.md
> ios-dev SKILL.md
> swift-language SKILL.md
> harmonyos-dev SKILL.md
> musk SKILL.md
