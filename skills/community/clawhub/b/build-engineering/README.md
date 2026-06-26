# Build Engineering（构建与工程化）

优化构建速度、搭建 Monorepo、配置模块联邦、提速 CI/CD，让团队把时间花在业务上而不是工具上。

## What It Does

- 诊断构建慢的根因（Vite 预构建、Webpack 缓存、loader 范围）
- 设计 pnpm workspace + Turborepo Monorepo 结构与 pipeline
- 配置模块联邦（Module Federation）实现微前端运行时共享
- 优化 GitHub Actions CI：缓存策略、并行化、增量构建
- 搭建代码生成工具链（OpenAPI → 类型 + React Query hooks、plop 脚手架）

## How to Use

当用户说「构建太慢」「CI 跑太久」「多项目共享组件」「模块联邦怎么配」「代码生成」时触发。先诊断问题类型，再给出针对性方案和可直接使用的配置代码。

## Requirements

- 适用于 Vite / Webpack 5 项目
- Monorepo 方案基于 pnpm + Turborepo
- CI 示例基于 GitHub Actions
