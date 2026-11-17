---
name: readme-generator
description: README 文档生成：项目分析、ARCHITECTURE.md、API 文档、数据库 Schema 文档
source:
  type: derived
  repo: skills-repo/docs-writer
  path: skills/readme-generator/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/jezweb/claude-skills/project-docs
metadata:
  category: 文档
  platform: 通用
  difficulty: 入门
---

# README 生成器

> 从代码库分析生成项目文档：README、ARCHITECTURE.md、API_ENDPOINTS.md、DATABASE_SCHEMA.md。

## 能力

- **项目类型检测**：自动识别 Cloudflare Worker、React SPA、Next.js、Hono API、Python、Rust 等项目类型
- **ARCHITECTURE.md**：系统概览、技术栈、目录结构、关键流程
- **API_ENDPOINTS.md**：路由、HTTP 方法、参数、响应类型、鉴权方式
- **DATABASE_SCHEMA.md**：表结构、关系、迁移、索引
- **文档自选**：根据项目实际内容只生成有意义的文档类型

## 使用方式

```text
/readme-generator 为这个项目生成完整文档
/readme-generator 只生成 API 端点文档
/readme-generator 更新数据库 Schema 文档
```

## 项目类型检测表

| 标识文件 | 项目类型 |
|----------|----------|
| `wrangler.jsonc/toml` | Cloudflare Worker |
| `vite.config.ts` + `src/App.tsx` | React SPA |
| `next.config.js` | Next.js |
| `package.json` with `hono` | Hono API |
| `drizzle.config.ts` | 含数据库层 |
| `pyproject.toml` | Python 项目 |
| `Cargo.toml` | Rust 项目 |

## 适用场景

- 新项目文档初始化
- 文档缺失或过时更新
- 新开发者入门文档
- 重构后文档刷新

## 限制

- 模板化输出，特殊项目需手动调整
- 仅生成文档内容，不涉及发布
- 不会自动推断未写明的设计意图

## 相关参考（Playbook）

- [references/doc-lifecycle-and-pipeline.md](../../references/doc-lifecycle-and-pipeline.md) — 文档入口与生成顺序（第 1 步）、受众分层主文档写法
- [references/diagram-selection-guide.md](../../references/diagram-selection-guide.md) — 第 15 节：本技能产出的架构图占位如何按真实技术栈补全
- 产出后核查：[scripts/check_code_blocks.py](../../scripts/check_code_blocks.py)、[scripts/check_md_links.py](../../scripts/check_md_links.py)（文档门禁，防死链/未标注）
- 模板范本：[assets/readme-template.md](../../assets/readme-template.md)