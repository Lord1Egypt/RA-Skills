---
name: "Bolt.new"
version: "1.0.0"
description: "Bolt.new AI 全栈开发助手，精通浏览器内开发、WebContainer、一键部署"
tags: ["ai-coding", "fullstack", "bolt", "webcontainer"]
author: "ClawSkills Team"
category: "developer-tools"
---

# Bolt.new AI 全栈开发技能指南

## 概述

Bolt.new 是 StackBlitz 推出的 AI 全栈开发平台，完全运行在浏览器中。基于 WebContainer 技术，无需本地安装任何工具，输入一句话描述即可生成、预览、部署一个完整的 Web 应用。

## 核心功能

### 浏览器内全栈开发（WebContainer）

WebContainer 是 StackBlitz 的核心技术，让 Node.js 直接在浏览器中运行：

- **零配置**：不需要安装 Node.js、npm 或任何开发工具
- **完整运行时**：支持 npm install、文件系统操作、HTTP 服务器
- **实时预览**：代码修改后即时在右侧预览窗口看到效果
- **隔离环境**：每个项目独立运行，互不干扰

### AI 项目生成与一键部署

- 用自然语言描述应用，AI 自动生成完整项目结构
- 支持多轮对话迭代，生成后可继续修改、添加功能
- 点击 Deploy 按钮直接部署到 Netlify，获得公网 URL，无需配置 CI/CD

## 支持的技术栈

| 类别 | 支持的技术 |
|------|-----------|
| 前端框架 | React、Vue 3、Svelte、Solid、Astro、Next.js、Nuxt |
| 样式方案 | Tailwind CSS、CSS Modules、Styled Components、UnoCSS |
| 构建工具 | Vite（默认）、Webpack |
| 后端框架 | Express、Fastify、Hono |
| 数据库 | SQLite（better-sqlite3）、内存数据库、localStorage |
| 包管理 | npm、pnpm |
| 语言 | TypeScript 完全支持 |

## 提示词技巧

### 推荐的 prompt 结构

```
创建一个 [应用类型]，使用 [技术栈]。

功能需求：
1. [核心功能1]
2. [核心功能2]

UI 要求：
- [设计风格]
- [配色方案]
- [响应式要求]
```

### 实战示例

```
创建一个个人记账应用，使用 React + TypeScript + Tailwind CSS。

功能：
1. 添加收入/支出记录（金额、分类、备注、日期）
2. 按月查看收支统计图表（用 recharts）
3. 数据存储在 localStorage

UI：现代简洁风格，蓝色系主色调，移动端优先
```

### 关键技巧

1. **明确技术栈**：不指定的话 AI 会自己选，可能不是你想要的
2. **分步迭代**：先生成基础版本，再逐步添加功能
3. **指定存储方案**：浏览器环境限制多，提前说明用 localStorage 还是 SQLite
4. **描述 UI 风格**：给出具体设计偏好，否则生成的界面可能很朴素
5. **遇到报错直接粘贴**：把错误信息发给 AI，它通常能自动修复

## 限制和注意事项

- **不支持原生二进制**：C/C++ 扩展、Python、Go 等无法运行
- **数据库受限**：不能用 MySQL/PostgreSQL，只能用 SQLite 或内存方案
- **无 Docker 支持**：WebContainer 不是虚拟机，不能运行容器
- **文件大小限制**：不适合处理大文件或大量静态资源
- **网络请求**：浏览器 CORS 策略仍然生效
- **持久化**：项目数据存在 StackBlitz 云端，免费账户有存储限制
- **性能**：复杂项目在浏览器中运行可能比本地慢

## 与其他工具对比

| 维度 | Bolt.new | Cursor/Windsurf | v0 (Vercel) |
|------|----------|----------------|-------------|
| 运行环境 | 浏览器 | 本地 IDE | 浏览器 |
| 全栈能力 | 前后端都支持 | 前后端都支持 | 仅前端组件 |
| 配置成本 | 零配置 | 需安装 IDE | 零配置 |
| 部署 | 一键 Netlify | 需自行配置 | 一键 Vercel |
| 适合场景 | 快速原型、演示 | 正式项目开发 | UI 组件生成 |
| 代码可控性 | 中等 | 高 | 低 |
| 离线使用 | 不支持 | 支持 | 不支持 |
| 项目复杂度 | 中小型 | 不限 | 小型组件 |

Bolt.new 适合"5 分钟出一个能跑的 demo"，Cursor/Windsurf 适合"认真写要上线的项目"。

## 使用场景和最佳实践

**适合场景**：快速原型验证、技术演示、学习新框架、黑客松、临时开发

**最佳实践：**
1. 先用简单 prompt 生成骨架，再分步迭代添加功能
2. 生成后检查 package.json，确认依赖版本合理
3. 重要项目及时导出代码到本地 Git 仓库备份
4. 利用 Bolt 生成原型后，迁移到本地 IDE 做正式开发
5. 复杂状态管理建议在 prompt 中指定方案（Zustand、Jotai 等）
6. 部署前检查环境变量和 API 密钥，避免泄露到前端代码中
