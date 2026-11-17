---
name: tailwind-audit
description: Tailwind CSS 审计：未用类/purge 正确性、v3→v4 迁移体检、配置漂移、冲突/重复类名、@apply 滥用与动态类名断 purge 排查
source:
  type: original
  repo: skills-repo/ai-fullstack-engineer
  path: skills/tailwind-audit/SKILL.md
  version: 1.0.0
  updated: 2026-08-12
metadata:
  category: 前端样式
  platform: Tailwind CSS
  difficulty: 进阶
---

# Tailwind CSS 审计（Tailwind Audit）

> 面向「已存在、但说不清健康度」的 Tailwind CSS 项目的体检指南：把 `purge` 是否真生效、v3→v4 迁移是否漏改、配置是否漂移、类名是否冲突重复、`@apply` 是否滥用、动态拼接类名是否断了 purge 这些**诊断性问题**讲清楚。这是与 `css-master`（教你怎么写布局）正交的**审计能力**。

## 何时使用

- 想确认生产 CSS 里**有没有大量没用到的类**在白白撑体积（purge / content 路径是否配错）
- 正在做或刚做完 **Tailwind v3 → v4 迁移**，需要系统性核对漏改项
- 怀疑 `tailwind.config` 的主题扩展与实际使用**漂移**（定义了却没人用 / 用了却没定义）
- 看到**冲突或重复类名**（如同时写 `px-2 px-4`、`text-red-500 text-blue-500`），需要统一与去重
- 代码里大量用 **`@apply`** 或**动态拼接类名**（`class={`text-${color}`}`），担心破坏构建或性能
- 接手别人留下的 Tailwind 项目，想先出一份**样式健康度报告**再动手

## 能力边界

- 覆盖 Tailwind 的**诊断与体检**（决策树与清单见 [references/tailwind-audit-playbook.md](../../references/tailwind-audit-playbook.md)）
- **不替代** `css-master`（教你怎么写 Grid/Flexbox 布局）、`web-performance`（CWV/打包体积通用优化）——它们是基础层
- 审计产出是**报告与整改建议**，不在未经确认时直接大改生产样式
- 不涉及原生 CSS / CSS-in-JS 方案的审计（超出 Tailwind 范畴）

## 使用方式

```
/tailwind-audit 帮我看看这个项目的 Tailwind 生产 CSS 有没有大量没用到的类
/tailwind-audit 我们刚从 v3 升到 v4，帮我列一份迁移漏改清单
/tailwind-audit 这些 @apply 用得有问题吗？会拖慢构建吗？
/tailwind-audit 有没有冲突或重复的类名可以合并？
```

## 工作流

1. 先判断审计目标类型：**体积（purge）/ 迁移（v3→v4）/ 配置漂移 / 类名冲突 / @apply 与动态类**
2. 按 [references/tailwind-audit-playbook.md](../../references/tailwind-audit-playbook.md) 的决策树定位问题类别
3. 用对应命令/脚本采集事实（构建产物体积、lint 结果、配置比对），**先核对 Tailwind 版本再跑命令**
4. 汇总成「问题 → 根因 → 整改建议」清单，重大改动先给报告、不擅自拍板

## 适用场景

- 上线前的样式健康度门禁
- v3→v4 升级后的回归核对
- 接手存量 Tailwind 项目的快速评估
- 配合 `web-performance` 做 CSS 体积专项优化前的定位

## 限制

- Tailwind 版本演进快（v4 默认把 `@tailwind` 指令改为 `@import "tailwindcss"`、配置从 JS 迁到 CSS-first、`dark:` 默认策略变化等），落地前先用 `npx tailwindcss --help` 与目标项目 `package.json` 核对版本，必要时对照官方迁移指南
- 第三方审计工具（lint / 插件）的可用性随版本与生态变化，**命令以目标环境实际安装为准**，不要凭记忆硬跑
- 搜索结果 / 官方文档需人工判断适用性
