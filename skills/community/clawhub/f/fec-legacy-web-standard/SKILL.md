---
name: fec-legacy-web-standard
description: Use when maintaining or safely modifying existing non-framework frontend code: vanilla JavaScript, jQuery, HTML/CSS, MPA pages, server-rendered templates, legacy plugins, or long-lived code that should stay in its current stack. Use migration skill when planning a move to React/Vue/TypeScript; Chinese triggers include 传统前端, 原生 JS, jQuery.
---

# 传统前端项目规范（JS + jQuery + HTML）

## Purpose

在不重写技术栈的前提下安全维护 vanilla JS、jQuery、HTML/CSS 和服务端模板项目。

## Procedure

1. 先确认本次改动是维护旧栈还是迁移；迁移到 React/Vue/TypeScript 时切换到现代化迁移 workflow。
2. 沿用现有架构和代码风格，优先修复问题，不在一次改动中引入多项现代化。
3. JavaScript 用 IIFE/命名空间减少全局污染，事件绑定优先委托到合理容器。
4. DOM 更新缓存选择器、批量操作、转义用户输入；Ajax 必须处理 loading、error、空状态和防重复提交。
5. HTML/CSS 保持语义、label、alt、BEM/既有命名和低选择器深度。
6. 安全重点检查 `.html()`、`innerHTML`、URL 参数渲染、CSRF token 和文件上传。

## Detailed References

涉及 jQuery 命名空间、事件绑定、Ajax、XSS 转义、文件组织和维护清单示例时，加载 [references/legacy-patterns.md](references/legacy-patterns.md)。

## Constraints

- 在现有架构内改进，不要引入与项目格格不入的现代框架。
- 渐进增强优于推倒重来。
- 禁止用 `innerHTML` / `.html()` 直接插入用户输入。
- 避免全局变量污染。
- 每次聚焦一个维护点，避免顺手重构整个模块。

## Expected Output

改动与旧项目风格一致，无全局变量泄漏，事件和 DOM 操作可维护，Ajax 状态完整，用户输入已转义，渐进改进不破坏现有功能。
