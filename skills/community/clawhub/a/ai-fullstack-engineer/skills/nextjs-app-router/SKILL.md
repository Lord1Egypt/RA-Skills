---
name: nextjs-app-router
description: Next.js App Router 范式专精：布局/路由处理器、服务端组件与客户端组件、数据获取缓存、RSC、流式渲染、中间件、Metadata API
source:
  type: original
  repo: skills-repo/ai-fullstack-engineer
  path: skills/nextjs-app-router/SKILL.md
  version: 1.0.0
  updated: 2026-08-12
metadata:
  category: 前端框架
  platform: Next.js
  difficulty: 进阶
---

# Next.js App Router 专精

> 面向 Next.js（App Router 架构，`app/` 目录）的落地指南：把「服务端组件、路由处理器、数据缓存、流式渲染」这些 App Router 独有的范式讲清楚，避免用 Pages Router 的旧习惯踩坑。

## 何时使用

- 新建或维护基于 `app/` 目录的 Next.js 项目（而非旧版 `pages/`）
- 需要决定「某个组件应该是 Server Component 还是 Client Component」
- 需要写路由处理器（Route Handler）、Server Action、Middleware
- 需要理解 `fetch` 缓存、`revalidate`、`unstable_cache`、静态/动态渲染边界
- 需要嵌套布局、路由组（route group）、并行路由（parallel）、拦截路由（intercepting）
- 需要处理 `params` / `searchParams`、Metadata API、loading/error/not-found

## 能力边界

- 覆盖 App Router 的**范式决策与常见坑**（决策树见 [references/nextjs-app-router-playbook.md](../../references/nextjs-app-router-playbook.md)）
- 不替代 `component-builder`（通用 Web 组件）、`css-master`（样式）、`web-performance`（性能指标）——它们仍是基础层能力
- 不涉及后端服务实现（走 `fastapi-python` / `backend-patterns`）、不涉及部署（走 `devops-engineer`）

## 使用方式

```
/nextjs-app-router 这个组件应该标 'use client' 吗？
/nextjs-app-router 怎么在 App Router 里做带缓存的数据获取？
/nextjs-app-router 路由处理器和 Server Action 该怎么选？
```

## 工作流

1. 先判断任务落在哪一类：**渲染单元（layout/page）、交互单元（client）、数据接口（route handler / server action）、横切（middleware / metadata）**
2. 按 [references/nextjs-app-router-playbook.md](../../references/nextjs-app-router-playbook.md) 的决策树选对范式
3. 落地时优先用原生 App Router API，避免引入与范式冲突的第三方抽象
4. 对照 playbook 的「上线前检查清单」逐项核验（'use client' 边界、缓存语义、异步 `params`）

## 适用场景

- 从零搭建 Next.js 全栈应用的前端骨架
- 把 Pages Router 项目迁移到 App Router
- AI-native 全栈工作流里「前端框架层」的 Next.js 专项落地

## 限制

- Next.js 版本演进快（`params`/`searchParams` 异步化、默认缓存策略变更等），落地前先确认目标项目版本，必要时用 `npx next --version` 核对
- 不覆盖 Next.js 以外的框架（Remix、Astro、纯 Vite SPA 等）
- 搜索结果/官方文档需人工判断适用性
