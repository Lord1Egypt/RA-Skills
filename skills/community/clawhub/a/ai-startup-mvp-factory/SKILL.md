---
name: ai-startup-mvp-factory
description: AI创业MVP快造工厂——从需求文档到容器化部署的全流程自动化工作流
category: 开发|自动化
triggers: 创建MVP, 创业项目, 快速上线, 新产品开发, 从零开始写项目
---

# AI Startup MVP Factory — 从想法到生产级应用的完整流水线

## 概述

本 Skill Combo 将 PRD 生成、代码构建、CI/CD 流水线、容器化部署全链路打通，实现**从一句话创业想法到生产级可运行应用**的端到端自动化。

适用于：独立开发者、创业团队技术负责人、快速验证想法的 MVP 场景。

---

## 技能编排图谱

```
用户输入创业想法
       │
       ▼
┌─────────────────┐
│  PRD Generator   │  ← 生成结构化产品需求文档 + 技术选型建议
│ (clawhub:prd)    │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ AI Startup MVP  │  ← 基于 PRD 自动生成完整项目代码（Scaffold）
│ Launcher        │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ GitHub PR        │  ← 代码质量检查 + AI Code Review + PR 知识同步
│ Knowledge Wiki   │
│ Sync             │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ Docker CI/CD    │  ← 容器构建 + 镜像推送 + 环境一致性验证
│ Release Pipeline│
└────────┬─────────┘
         │
         ▼
   可部署上线的 MVP 应用
```

---

## 协作说明

### 1. PRD Generator（入口）
- **输入**: 用户的一句话产品想法 / 业务需求
- **输出**: 结构化 PRD 文档（功能列表、技术栈建议、API 设计、数据模型）
- **负责 Skill**: `prd-generator` (clawhub) / `ai-prd-generator` (本地)

### 2. AI Startup MVP Launcher（构建引擎）
- **输入**: PRD 文档内容
- **输出**: 完整可运行的项目代码（前端 + 后端 + 配置）
- **负责 Skill**: `ai-startup-mvp-launcher` (本地)

### 3. GitHub PR Knowledge Wiki Sync（质量门禁）
- **输入**: 生成的代码
- **输出**: PR 知识库同步 + AI Code Review 报告
- **负责 Skill**: `github-pr-knowledge-wiki-sync` (本地)

### 4. Docker CI/CD Release Pipeline（部署出口）
- **输入**: 审查通过的代码
- **输出**: 容器镜像 + 部署配置 + 生产环境就绪状态
- **负责 Skill**: `docker-ci-release-pipeline` (本地)

---

## 使用方法

### 第一步：输入你的创业想法
```markdown
我想做一个 AI 简历优化器：
1. 用户上传简历 PDF
2. AI 分析简历并给出优化建议
3. 支持一键重写
4. 导出优化后的 PDF
```

### 第二步：交给 PRD Generator 生成产品规范
激活 `prd-generator` Skill，输入上述想法，获取完整 PRD。

### 第三步：将 PRD 投入 MVP Launcher
将 PRD 内容传给 `ai-startup-mvp-launcher`，它会：
- 选择技术栈（FastAPI + React + PostgreSQL）
- 生成项目结构
- 编写核心业务逻辑
- 配置 Docker 环境

### 第四步：质量门禁
传给 `github-pr-knowledge-wiki-sync`，自动：
- 创建 PR 并进行 AI Code Review
- 同步知识到 Wiki
- 修复代码质量问题

### 第五步：容器化部署
最后交给 `docker-ci-release-pipeline`：
- 多阶段 Dockerfile 构建
- 镜像安全扫描
- 推送到镜像仓库
- 生成 docker-compose 部署文件

---

## 适用场景

| 场景 | 价值 |
|------|------|
| 独立开发者快速验证想法 | 1 小时内完成从想法到可演示的应用 |
| 创业比赛 / 路演 Demo | 生成可运行的技术原型 |
| MVP 技术选型参考 | PRD 阶段已明确技术栈，无需重复踩坑 |
| 团队交接文档 | 自动生成 Wiki，降低沟通成本 |

---

## 技术栈覆盖

- **后端**: Python FastAPI / Node.js Express / Go Gin
- **前端**: React / Vue / Next.js
- **数据库**: PostgreSQL / MongoDB / Redis
- **AI 集成**: OpenAI API / LangChain / 向量数据库
- **容器**: Docker + Docker Compose
- **CI/CD**: GitHub Actions + 容器镜像仓库

---

## 注意事项

1. **PRD 是入口**，不要跳过。清晰的 PRD 能大幅提升 MVP 代码质量。
2. **代码审查**是可选的，但建议开启，特别是涉及第三方 API Key 时。
3. **容器化**在 MVP 阶段可跳过，直接用 `mvp-launcher` 生成的代码本地运行即可。
4. 所有生成的代码默认使用 MIT License，需确认后再部署。