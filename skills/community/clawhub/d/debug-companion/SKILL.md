---
slug: debug-companion
name: 调试伴侣
description: 根据错误信息/traceback 自动分析根因并给出修复建议
author: workflow-coordinator
version: 1.0.0
tags:
  - debug
  - error
  - troubleshooting
  - developer-tools
---

# 调试伴侣 SKILL.md

> 你的专属调试助手 —— 粘贴错误信息，立即得到根因分析和修复方案

## 技能简介

**调试伴侣**（Debug Companion）是一个 OpenClaw 技能，专门帮助开发者快速定位和修复代码错误。

### 核心能力

- 🔍 **智能解析**：自动识别错误类型、文件位置、行号
- 🎯 **根因分析**：用大白话解释"为什么会出错"
- ✅ **修复建议**：给出具体操作步骤，甚至直接生成补丁
- 📚 **参考资料**：附赠类似问题的解决方案链接

### 支持语言

| 语言 | 状态 |
|------|------|
| Python | ✅ |
| JavaScript / Node.js | ✅ |
| TypeScript | ✅ |
| Go | ✅ |
| Java | ✅ |
| C++ | ✅ |
| Rust | ✅ |
| PHP | ✅ |
| Ruby | ✅ |

---

## 工作流程

```
用户发送错误信息/traceback
         ↓
   错误信息解析
（提取错误类型、文件、行号）
         ↓
   智能搜索
（Tavily + Code Search）
         ↓
   根因分析 + 修复建议
         ↓
   结构化输出
```

---

## 使用方式

### 触发词

用户发送以下内容时会激活技能：

- `调试 + 错误信息`
- `报错 + traceback`
- `出了个bug`
- `这个错误怎么修`
- 直接粘贴错误信息/traceback

### 输入格式

**推荐格式**：
```
[错误类型]: [错误描述]
  File "[文件]", line [行号], in [函数名]
    [代码]
  [更多堆栈信息]
```

**示例**：
```
TypeError: Cannot read property 'map' of undefined
  at processData (/app/utils.js:15:20)
  at handleRequest (/app/server.js:42:10)
```

### 可选上下文

| 上下文 | 说明 | 示例 |
|--------|------|------|
| 语言 | 指定编程语言 | `Python`、`JavaScript` |
| 代码片段 | 相关代码 | 粘贴出错的代码 |
| 环境信息 | OS、版本等 | `Node.js v18`、`Python 3.11` |

---

## 输出格式

```markdown
## 🔍 错误解析
**错误类型**：TypeError
**问题文件**：/app/utils.js:15
**问题描述**：在 `processData` 函数中尝试调用 `.map()`，但数据是 `undefined`

## 🎯 根因分析
你正在对 `data` 变量调用 `.map()` 方法，但这个变量是 `undefined`。这通常是因为：
1. API 返回的数据结构不符合预期
2. 异步操作尚未完成就开始处理
3. 数据获取函数出错返回了空值

## ✅ 修复建议
1. **添加防御性检查**：在使用 `.map()` 前检查 `data` 是否存在
   ```javascript
   if (!data) {
     console.error('数据不存在:', data);
     return [];
   }
   ```
2. **确保数据加载完成**：使用 `await` 或检查 Promise 状态
3. **添加默认值**：使用 `data ?? []` 防止 undefined

## 📚 参考资料
- [MDN: undefined 处理](https://developer.mozilla.org/...)
- [Stack Overflow: Cannot read property of undefined](https://stackoverflow.com/...)
```

---

## 错误类型速查表

| 错误类型 | 常见原因 |
|----------|----------|
| `TypeError: Cannot read property 'X' of undefined` | 访问了 undefined/null 的属性 |
| `ReferenceError: X is not defined` | 变量未定义或拼写错误 |
| `SyntaxError` | 语法错误，缺少括号/引号等 |
| `IndexError: list index out of range` | 数组索引越界 |
| `KeyError: 'X'` | 字典/对象没有这个键 |
| `NullPointerException` | 空指针调用 |
| `ENOENT: No such file or directory` | 文件路径错误 |
| `Permission denied` | 权限不足 |

---

## 工具调用

技能内部使用以下工具：

| 工具 | 用途 |
|------|------|
| `tavily_search` | 搜索类似问题的解决方案 |
| `code_search` | 搜索官方文档和权威教程 |
| `web_fetch` | 抓取详细修复方案页面 |

---

## 注意事项

1. **隐私安全**：如果错误信息包含敏感路径或密钥，会自动脱敏处理
2. **上下文重要**：提供更多代码上下文能获得更准确的建议
3. **版本相关**：某些错误在不同版本语言中处理方式不同，请提供版本信息
4. **二次确认**：涉及代码修改时，建议先在测试环境验证

---

## 示例对话

**用户**：
```
js报错：TypeError: Cannot read property 'map' of undefined
  at processData (utils.js:15:20)
  at handleRequest (server.js:42:10)
```

**调试伴侣**：
（按上方输出格式返回完整分析）

---

## 更新日志

- 2026-03-27：v1.0.0 初始版本
  - 支持8种主流语言
  - 错误解析+根因分析+修复建议
  - Tavily搜索+代码搜索双保险
