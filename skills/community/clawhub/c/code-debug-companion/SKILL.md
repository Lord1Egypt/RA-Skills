---
name: code-debug-companion
description: AI 驱动的智能代码调试助手，自动诊断错误、搜索解决方案、修复代码并验证。
category: 开发
triggers: 调试, debug, 报错, 修复, 错误分析, 代码诊断
---

# Code Debug Companion - AI 智能代码调试助手

## 概述

这是一个完整的代码调试工作流，将错误捕获、解决方案研究、代码修复和测试验证串联起来，帮助开发者快速定位并解决 Bug。

## 工作流程

```
[错误信息/截图]
       ↓
[Code Review 分析错误原因]
       ↓
[Web Search 搜索类似问题/解决方案]
       ↓
[生成修复方案 + 单元测试]
       ↓
[写入修复代码 + 测试报告]
```

## 核心 Skill 编排

| Skill | 职责 |
|-------|------|
| code-review | 分析错误类型、定位根因、识别代码问题 |
| brave-search | 搜索 StackOverflow/GitHub/文档中的类似问题 |
| setup-unit-test | 生成修复验证的单元测试用例 |
| github-issues | 有用的解决方案创建 Issue 跟踪 |

## 使用方法

### 场景 1：粘贴错误信息调试

```
调试以下错误：
TypeError: Cannot read property 'map' of undefined
  at Array.reduce (src/utils.ts:42:18)
  at processData (src/handlers.ts:15:7)
```

### 场景 2：截图调试

直接发送错误截图或终端输出，助手自动解析并开始调试流程。

### 场景 3：批量调试

粘贴整个错误堆栈，助手按优先级排序后逐个修复。

## 输出格式

修复完成后输出：

```
🐛 问题诊断：[错误类型 + 根因分析]
🔍 类似问题：搜索到 N 条相关讨论
✅ 修复方案：[具体修改内容]
🧪 测试用例：已生成 N 个测试覆盖此场景
📁 修改文件：列出所有变更文件
```

## 支持语言

JavaScript / TypeScript / Python / Go / Rust / Java / C++

## 示例对话

**用户**: 调试这个错误：`AssertionError: expected function to throw Error`

**助手**: 分析 → 搜索 → 修复 → 测试，一站式完成。