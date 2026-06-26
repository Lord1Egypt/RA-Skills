# Skill 元数据字段规范

> 来源：基于 apple-design、ios-dev、swift-language 三个 A 级 skill 的 frontmatter 分析
> 整理时间：2026-04-23

## 标准 Frontmatter 模板

```yaml
---
name: <skill-name>
description: <30-100 字，一句话描述技能用途>
trigger: <触发词1|触发词2|触发词3|...>
tags:
  - <tag1>
  - <tag2>
  - <tag3>
hermes:
  platform: hermes
  version: "<X.Y>"
  last_updated: "<YYYY-MM-DD>"
  source: |
    <官方文档 URL>
    <多行字符串>
---

# <Skill 标题>
```

## 字段详解

### name 字段

**格式：** 小写字母 + 连字符
**长度：** 最多 64 字符
**用途：** 技能的唯一标识符

```yaml
# ✅ 正确
name: swift-language
name: apple-design
name: distill-skill-builder

# ❌ 错误
name: Swift Language  # 有空格
name: SWIFT_LANGUAGE  # 下划线
name: swift.language  # 点号
```

### description 字段

**格式：** 一句话描述
**长度：** 30-100 字
**用途：** 在 skills_list 时显示给用户

```yaml
# ✅ 正确（具体说明何时触发）
description: Swift 语言权威参考。覆盖 Swift 6.3 完整语法、类型系统、集合类型、函数、闭包、协议、泛型、并发、安全特性。当用户询问 Swift 语法、类型、关键字、标准库 API、SwiftUI 基础语法，或要求解释 Swift 代码时触发。

# ❌ 错误（太泛）
description: iOS 开发技能

# ❌ 错误（太长）
description: Swift 语言权威参考。覆盖 Swift 6.3 完整语法...
```

### trigger 字段

**格式：** 单行，竖线 `|` 分隔
**触发条件：** 用户消息中包含任意一个触发词
**数量：** 越多越好（影响得分）

```yaml
# ✅ 正确（数量多，覆盖全面）
trigger: Swift 语法|Swift 类型|Swift 闭包|Swift 泛型|Swift async|Swift await|Swift actor|Swift @State|Swift 代码解释|Swift optional|Swift protocol|Swift struct|Swift class|Swift enum|Swift guard|Swift if let|Swift ??|Swift @escaping|Swift @autoclosure|Swift 错误处理|Swift throws|Swift do-catch|Swift 泛型|Swift where 子句|Swift 访问控制|Swift private|Swift public|Swift extension|Swift protocol extension|Swift 类型转换|Swift as|Swift is|Swift subscript|Swift 下标|Swift init|Swift deinit|Swift 继承|Swift override|Swift final|Swift delegate|Swift Sendable|Swift actor isolation|Swift @propertyWrapper

# ❌ 错误（多行格式）
trigger: |
  - Swift 语法
  - Swift 类型
  - Swift 闭包

# ❌ 错误（列表格式）
trigger:
  - Swift 语法
  - Swift 类型
```

### tags 字段

**格式：** YAML 列表
**用途：** 分类和搜索

```yaml
# ✅ 正确
tags:
  - swift
  - swift-language
  - swift6
  - ios
  - apple
  - programming-language

# ❌ 错误（字符串格式）
tags: swift, ios, apple
```

### hermes 字段（嵌套）

```yaml
hermes:
  platform: hermes        # 固定值
  version: "1.0"          # 语义版本
  last_updated: "2026-04-23"  # 更新日期
  source: |               # 官方文档 URL（多行字符串）
    https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
    https://developer.apple.com/documentation/swift
```

**注意：**
- `source` 放在 `hermes:` 里时，评估器默认**不会**计入官方 URL
- 需要 patch 评估器或同时在 body 中添加 URL
- `last_updated` 也需要 patch 评估器才能识别

### hermes.source 格式

```yaml
# ✅ 单行 URL
hermes:
  source: https://docs.swift.org/swift-book/documentation/the-swift-programming-language/

# ✅ 多行 URL
hermes:
  source: |
    https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
    https://developer.apple.com/design/human-interface-guidelines/

# ❌ 错误（嵌套结构）
hermes:
  source:
    primary: https://...
    secondary: https://...
```

---

## 评估器对 frontmatter 的处理

### YAML 解析

```python
import yaml

# frontmatter 必须是标准 YAML
fm = yaml.safe_load(frontmatter_text)
```

### frontmatter 解析位置

```python
if content.startswith('---'):
    parts = content[3:].split('---', 1)
    if len(parts) == 2:
        fm = yaml.safe_load(parts[0])
        body = parts[1].strip()
```

### frontmatter 字段传递

```python
# _parse_frontmatter 返回 dict
self._evaluate_metadata(fm)
self._evaluate_trigger(fm)
self._evaluate_core_content(body, fm)
self._evaluate_sources(body, fm)  # fm 作为第二个参数传入
```

---

## 各字段对评分的影响

| 字段 | 影响维度 | 权重 |
|------|----------|------|
| name | 元数据完整性 | 2/10 |
| description | 元数据完整性 | 2/10 |
| trigger | 触发词覆盖 | 15/15 |
| tags | 元数据完整性 | 1/10 |
| hermes.platform | 元数据完整性 | 1/10 |
| hermes.version | 元数据完整性 | 1/10 |
| hermes.last_updated | 来源标注 | 3/10 |
| hermes.source | 来源标注 | 3-4/10 |

---

## 最佳实践

### 1. 触发词覆盖策略

触发词应覆盖：
- **核心概念**（如"Swift 闭包"、"Swift 泛型"）
- **常见场景**（如"Swift 代码解释"、"这段代码"）
- **具体 API**（如"Swift @escaping"、"Swift async/await"）
- **对比场景**（如"Swift vs Objective-C"）
- **常见问题**（如"Swift optional 解包"）

### 2. 触发词格式陷阱

```yaml
# ❌ 触发词中有引号
trigger: "Swift 语法"|"Swift 类型"

# ❌ 触发词中有括号
trigger: Swift (@State)|Swift (@escaping)

# ✅ 纯触发词，无引号无特殊字符
trigger: Swift 语法|Swift 类型|Swift @State|Swift @escaping
```

### 3. description 写法

```yaml
# ✅ 结构：平台 + 内容 + 触发场景
description: Swift 语言权威参考。覆盖 Swift 6.3 完整语法、类型系统、集合类型、函数、闭包、协议、泛型、并发、安全特性。当用户询问 Swift 语法、类型、关键字、标准库 API、SwiftUI 基础语法，或要求解释 Swift 代码时触发。

# ❌ 太泛
description: iOS 开发相关技能

# ❌ 太窄
description: Swift async/await 语法糖
```

---

## 来源

> apple-design SKILL.md frontmatter
> ios-dev SKILL.md frontmatter
> swift-language SKILL.md frontmatter
> skill_evaluator_v2.py frontmatter 解析逻辑
