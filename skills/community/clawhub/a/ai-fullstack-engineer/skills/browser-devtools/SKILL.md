---
name: browser-devtools
description: Chrome DevTools 自动化：页面导航、快照、点击、表单、JS 执行、性能审计
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/browser-devtools/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/kunchenguid/chrome-devtools-axi/chrome-devtools-axi
metadata:
  category: 工具
  platform: Web
  difficulty: 入门
---

# Chrome DevTools 浏览器自动化

> 通过 chrome-devtools-axi CLI 控制 Chrome 浏览器：导航、快照、交互、脚本执行、调试、性能审计。

## 能力

- **页面操作**：open 导航、snapshot 快照、screenshot 截图、多页面管理
- **元素交互**：click/fill/fillform/hover/drag/upload 基于无障碍快照 ref
- **脚本执行**：eval 运行任意 JS、console 查看输出、network 分析请求
- **性能审计**：lighthouse 审计、perf-start/perf-stop 性能录制
- **设备模拟**：resize 视口、emulate 设备模式

## 使用方式

```
/browser-devtools 打开 https://example.com 并截图
/browser-devtools 自动化测试这个登录流程
/browser-devtools 审计这个页面的性能
```

## 工作流

1. `npx -y chrome-devtools-axi open <url>` 导航到页面
2. 基于快照中的 `uid=` ref 进行交互（click @ref、fill @ref text）
3. 状态变更后用 snapshot 确认结果
4. 调试用 console/network，审计用 lighthouse
5. 完成用 stop 关闭浏览器会话

## 适用场景

- 网页自动化测试
- 页面内容提取和截图
- 性能审计
- 浏览器行为调试

## 限制

- 需要 Chrome 浏览器
- 不替代完整的 E2E 测试框架（Playwright/Cypress）
- 复杂交互流程建议用专业工具

## 相关参考（Playbook）

本子技能落地"浏览器自动化调试"，前端方法论见下列 `references/`（按需读取）：

- 前端深度 playbook（组件 / CSS / 调试 / 性能 / 水合踩坑）：[references/frontend-playbook.md](../../references/frontend-playbook.md)