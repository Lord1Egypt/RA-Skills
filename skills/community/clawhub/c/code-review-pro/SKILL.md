---
name: Code Review Pro
version: 1.0.0
slug: code-review-pro
description: "专业代码审查 | 4Agent并行审查+ 置信度评分 | 覆盖逻辑/安全/性能/风格"
author: Softboypatrick
license: MIT-0
tags: [code-review, security, analysis]
---

# Code Review Pro

4Agent 并行代码审查。置信度≥70% 才输出。

## Agent 1: 逻辑
检查：逻辑错误、边界条件、竞态条件、死循环

## Agent 2: 安全
检查：注入漏洞、XSS、CSRF、权限泄露、密钥硬编码

## Agent 3: 性能
检查：时间复杂度、内存泄漏、不必要重复、过大循环

## Agent 4: 风格
检查：命名规范、代码整洁度、语言惯用法

## 输出格式
### [严重] 问题描述 (置信度: 92%)
- 位置：文件:行号 | 风险：高危 | 建议：...
### [建议] 优化点 (置信度: 78%)
- ...
