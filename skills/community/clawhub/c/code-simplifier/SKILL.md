---
name: code-simplifier
description: 当用户要求简化代码、重构代码、优化代码、改进代码质量时使用此技能。提供代码简化原则和最佳实践指导，确保代码符合质量标准。
---

# Code Simplifier

提供代码简化、重构和优化的原则指导。

## 核心原则

### 函数设计

- **单一职责**: 每个函数只做一件事
- **长度控制**: 目标 < 50 行，理想 10-30 行
- **参数控制**: ≤ 4 个参数；超过时使用数据类或配置对象
- **早期返回**: 用 guard clauses 避免深层嵌套

### 代码组织

- **DRY**: 提取重复逻辑为公共函数
- **命名清晰**: 变量名反映意图，避免单字母（循环变量除外）
- **无魔法数字**: 提取为命名常量
- **嵌套控制**: 嵌套层级 ≤ 3 层

### 错误处理

- 捕获具体异常，不使用裸 `except:`
- 保留原始异常链 (`raise ... from e`)
- 使用 context manager 管理资源

## 语言特定规范

### Python

```python
# ✅ 类型注解
def process(user_id: int, data: dict) -> dict | None:
    ...

# ✅ list/dict comprehension（避免嵌套）
result = [x for x in items if x.condition]

# ✅ 命名
snake_case（变量/函数）, PascalCase（类）, UPPER_SNAKE_CASE（常量）

# ❌ 避免
# - 嵌套 comprehension
# - 过度使用 lambda
# - 裸 except:
```

### JavaScript / TypeScript

```javascript
// ✅ const/let，无 var
// ✅ 箭头函数
const process = (data) => data.filter(x => x.valid);

// ✅ 解构
const { name, email } = user;

// ✅ 命名
camelCase（变量/函数）, PascalCase（类/接口）, UPPER_SNAKE_CASE（常量）
```

## 自动化工具

### 命令行分析工具

```bash
python scripts/code_simplifier.py <file.py> --analyze        # 分析复杂度
python scripts/code_simplifier.py <file.py> --suggest       # 生成重构建议
python scripts/code_simplifier.py <file.py> --simplify      # 自动简化代码
python scripts/code_simplifier.py <file.py> --output=out.py # 指定输出文件
```

输出格式支持 `text`（默认）和 `json`。

## 质量检查清单

### 函数级别
- [ ] 函数长度 < 50 行
- [ ] 嵌套层级 < 3 层
- [ ] 单一职责
- [ ] 命名有意义

### 代码级别
- [ ] 无重复代码
- [ ] 无魔法数字
- [ ] 无未使用变量/导入
- [ ] 错误处理具体

### 整体质量
- [ ] 符合语言规范
- [ ] 类型注解/标注完整
- [ ] 可读性良好
- [ ] 易于维护

## 前端编码规范（网页项目必须遵守）

1. **HTML 安全**：所有动态内容用 `textContent` 赋值，禁止 `innerHTML`；必须用 `escapeHTML()` 转义 `< > & ' "`
2. **移动端兼容**：按钮 `touch-action: manipulation`，点击目标 ≥44px
3. **CSS 布局**：用 Flexbox/Grid，不用 float
4. **响应式**：相对单位（rem/em/%），viewport meta tag
5. **性能**：LCP < 2.5s、INP < 200ms、CLS < 0.1

> 修复阶段加载 `web-fixing` 技能诊断；编码阶段遵守以上 5 条即可预防大部分问题。

## 参考文档

- **重构模式**: [refactoring_patterns.md](references/refactoring_patterns.md) — Early Return、Extract Method、Guard Clauses、Async/Await 等 20+ 模式
- **最佳实践**: [best-practices.md](references/best-practices.md) — 函数设计、代码组织、错误处理、性能优化、测试友好设计
- **故障排除**: [troubleshooting.md](references/troubleshooting.md) — 代码异味诊断、复杂度分析、自动化工具、重构工作流
