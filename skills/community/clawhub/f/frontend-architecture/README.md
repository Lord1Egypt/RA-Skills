# Frontend Architecture（前端架构设计）

为大型前端应用设计长期可维护的架构——不是"用什么框架"，而是如何组织代码、划分模块、管理依赖，让项目在 2 年后还能维护。

## What It Does

- 按团队规模（小/中/大型）给出对应的项目结构方案
- 设计 Feature-Sliced 分层架构，用 ESLint 强制模块边界
- 制定代码分割策略（路由级、大型依赖、低频功能）
- 技术选型决策矩阵（框架、状态管理、样式方案）
- 用 ADR 记录架构决策，管理技术债
- 渐进式重构与绞杀者模式（Strangler Fig）

## How to Use

当用户说「新项目技术选型」「项目结构怎么组织」「模块耦合严重」「技术债怎么管」「微前端迁移」时触发。先问清楚团队规模、生命周期、性能要求，再给出匹配当前规模的方案。

## Requirements

- 框架无关（React/Vue/Svelte 均适用）
- Monorepo 方案基于 pnpm + Turborepo
- 依赖规则强制基于 ESLint no-restricted-imports
