# 🐛 Debug Companion 调试伴侣

## 📖 简介

**调试伴侣**（Debug Companion）是一款 OpenClaw 技能，专门帮助开发者快速分析代码错误和 traceback，自动定位问题根因并提供修复建议，让调试不再是噩梦，让开发更高效、更愉快！✨

---

## 🚀 快速开始

### 安装

确保已安装 OpenClaw 环境，然后将调试伴侣技能放入技能目录：

```bash
# 方式一：使用技能市场安装
openclaw skill install debug-companion

# 方式二：手动安装
cp -r debug-companion ~/.openclaw/skills/
```

### 使用方式

在对话中直接提交错误信息即可：

```
帮我看看这个错误：
[粘贴你的错误信息/traceback]
```

技能会自动分析并返回：
- 🎯 **问题根因** - 一句话点明问题所在
- 📋 **错误类型** - 语法错误？类型错误？逻辑错误？
- 💡 **修复建议** - 具体的代码修复方案
- 📚 **相关知识** - 避免同类错误的最佳实践

---

## 📌 示例

### 示例一：Python 错误

**输入：**
```
TypeError: 'str' object is not callable
Traceback (most recent call last):
  File "test.py", line 5, in <module>
    result = foo()(10)
TypeError: 'str' object is not callable
```

**输出：**
| 项目 | 内容 |
|------|------|
| 🔍 问题根因 | `foo` 是一个字符串，而不是函数，你试图调用它 |
| 📋 错误类型 | 类型错误（TypeError） |
| 💡 修复建议 | 检查 `foo` 的定义，确保它是一个可调用对象（函数/类），而不是字符串 |
| 📚 最佳实践 | 变量命名避免与内置函数冲突，添加类型检查 |

---

### 示例二：JavaScript 错误

**输入：**
```
ReferenceError: Cannot access 'count' before initialization
    at countUp (index.js:3)
    at <anonymous> (index.js:10)
```

**输出：**
| 项目 | 内容 |
|------|------|
| 🔍 问题根因 | 存在Temporal Dead Zone（TDZ），`count` 在声明前被访问 |
| 📋 错误类型 | 引用错误（ReferenceError） |
| 💡 修复建议 | 将 `const count = ...` 的声明移到 `countUp()` 函数调用之前 |
| 📚 最佳实践 | 使用 `let`/`const` 时注意变量提升规则，建议启用 ESLint 规则 |

---

## ⚠️ 注意事项

1. **提供完整 traceback** - 错误信息越完整，分析越准确，建议粘贴完整的错误堆栈
2. **注明编程语言** - 虽然技能会自动识别，但明确标注语言（如 Python/JavaScript）会更精确
3. **包含相关代码片段** - 如果可能，附上出错代码的上下文，有助于精确定位
4. **多次错误分别处理** - 如果有多个错误，建议逐个提交分析

---

## ❓ 常见问题 FAQ

### Q1: 支持哪些编程语言？
> A: 目前支持主流语言，包括 Python、JavaScript/TypeScript、Java、C++、Go、Rust 等，持续更新中。

### Q2: 分析结果一定准确吗？
> A: 技能基于大量调试经验训练，对常见错误能给出准确分析。但复杂业务逻辑可能需要结合具体情况判断。

### Q3: 如何获得更好的分析结果？
> A: 建议提供：完整的错误堆栈、相关代码片段、期望行为与实际行为的对比。

### Q4: 可以分析框架特定的错误吗？
> A: 可以！技能内置了常见框架（如 React、Vue、Django、Spring）的错误模式识别。

### Q5: 如何反馈分析结果不准确？
> A: 可以直接回复「分析有误」或提供更多上下文，技能会尝试重新分析。

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2024-XX-XX | 🎉 初始版本发布，支持常见编程语言错误分析 |
| v1.1.0 | 2024-XX-XX | ✨ 新增框架特定错误识别（React、Django等） |
| v1.2.0 | 2024-XX-xx | 🛠️ 优化分析逻辑，提升准确率和响应速度 |

---

<div align="center">

**让调试变得更简单** 🚀

有问题？尽管问！ Debug Companion 随时待命～ 🐛✨

</div>
