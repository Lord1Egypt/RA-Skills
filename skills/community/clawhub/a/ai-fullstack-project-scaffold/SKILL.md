---
name: ai-fullstack-project-scaffold
description: AI 全栈项目脚手架工厂 — 从需求描述到可运行项目，一键生成代码框架、Makefile、任务追踪和 Docker 部署配置
category: AI
triggers: 创建项目, 初始化项目, 项目脚手架, 代码生成, 新项目, 全栈开发, 快速开发, 项目模板
version: 1.0.0
author: OpenClaw Agent
tags:
  - project-scaffold
  - fullstack
  - kimi-cli
  - makefile
  - docker
  - dev-task
  - code-generation
dependencies:
  - kimi-cli
  - makefile-generator
  - dev-task
  - docker-expert
---

# AI 全栈项目脚手架工厂 (ai-fullstack-project-scaffold)

> 描述你的项目需求 → AI 自动生成完整的项目结构、代码框架、Makefile 和 Docker 配置

## 🎯 解决痛点

- ❌ 从零开始搭项目，光配置就要花半天
- ❌ 每次新建项目都要复制旧项目，改来改去容易出错
- ❌ 团队项目规范不统一，Makefile/配置文件五花八门
- ❌ Docker 配置每次都要查文档，调试耗时
- ❌ 没有任务追踪，项目做到一半不知道进度到哪了

## 💡 解决方案

```
输入：项目需求描述（一句话或详细需求文档）
   ↓
┌──────────────────────────┐
│  dev-task                │ → 解析需求，生成版本规划与任务清单
│  (需求拆解 & 任务规划)    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│  kimi-cli                │ → 生成完整项目代码框架（全栈：前端+后端+数据库）
│  (代码自动生成)          │   自动选择技术栈、目录结构、核心模块
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│  makefile-generator      │ → 生成标准化 Makefile（开发/测试/构建/部署）
│  (标准化构建脚本)        │   支持多语言：Node.js / Python / Go / Java
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│  docker-expert            │ → 生成生产级 Dockerfile 和 docker-compose.yml
│  (容器化部署)            │   多阶段构建、安全加固、最佳实践
└──────────────────────────┘
```

## 🚀 快速开始

```bash
# 启动全栈项目脚手架
openclaw skill run ai-fullstack-project-scaffold --name "社区电商 API" --stack "nodejs+postgres" --desc "支持商品管理、订单系统、用户鉴权的电商后端服务"

# Python 项目示例
openclaw skill run ai-fullstack-project-scaffold --name "数据采集服务" --stack "python+redis" --desc "定时抓取网站数据并存储到 PostgreSQL"

# Go 项目示例
openclaw skill run ai-fullstack-project-scaffold --name "文件上传服务" --stack "go+minio" --desc "大文件分片上传，支持断点续传"
```

## 📋 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 项目名称（英文，无空格） |
| stack | string | 是 | 技术栈，如 `nodejs+postgres`、`python+redis`、`go+minio` |
| desc | string | 是 | 项目一句话描述（中文即可，AI 自动解析） |
| port | number | 否 | 服务端口，默认 3000 |

## 技术栈支持

| 技术栈 | 语言 | 数据库 | 特征 |
|--------|------|--------|------|
| nodejs+postgres | Node.js/TypeScript | PostgreSQL | REST API / Express / Prisma |
| nodejs+mysql | Node.js/TypeScript | MySQL | REST API / Express / Sequelize |
| python+postgres | Python/FastAPI | PostgreSQL | OpenAPI / SQLAlchemy / Pydantic |
| python+redis | Python/FastAPI | Redis | 缓存优先 / 异步任务 |
| go+postgres | Go/Gin | PostgreSQL | 高性能 API / GORM |
| go+minio | Go/Gin | MinIO | 对象存储 / S3 协议 |
| java+postgres | Java/Spring | PostgreSQL | 企业级 / MyBatis |

## 输出产物

```
{project-name}/
├── Makefile              ✅ 标准 Makefile（dev/test/build/run/deploy）
├── Dockerfile            ✅ 多阶段构建生产镜像
├── docker-compose.yml    ✅ 开发 + 生产环境编排
├── .dockerignore         ✅ 构建优化
├── README.md             ✅ 项目说明 + 快速启动
├── package.json          ✅ 或 requirements.txt / go.mod（按语言）
└── src/                  ✅ 核心业务代码框架
    ├── main.{ext}         ✅ 入口文件（已包含基础路由）
    ├── config.{ext}       ✅ 配置文件
    └── modules/          ✅ 分模块代码骨架
```

## Skill 协作说明

### 1. dev-task（需求解析层）
接收用户需求描述，用 AI 拆解为版本规划：
- 解析项目类型和技术栈选择
- 生成 `VERSION.md` 版本规划文档
- 生成 `TODO.md` 初始任务清单
- 为后续代码生成提供技术决策

### 2. kimi-cli（代码生成层）
基于 dev-task 的技术决策，生成完整项目代码：
- 调用 Kimi Code CLI 生成完整目录结构
- 自动注入项目配置文件（.env, config.*）
- 生成模块化代码骨架，支持直接运行
- 适合大项目（>10 个文件），支持增量修改

### 3. makefile-generator（构建标准化层）
生成跨平台标准化 Makefile：
- 统一命令规范：`make dev` / `make test` / `make build` / `make run`
- 自动检测语言类型，生成对应的构建规则
- 包含 health-check、lint、format 等开发命令
- 支持多环境变量切换（dev/staging/prod）

### 4. docker-expert（容器化层）
生成生产级 Docker 配置：
- 多阶段构建，最小化镜像体积
- 非 root 用户运行，安全加固
- 健康检查 / 日志轮转 / 信号处理
- docker-compose 开发环境一键启动

## 使用示例

### 示例 1：创建一个电商后端 API

```bash
openclaw skill run ai-fullstack-project-scaffold \
  --name "shop-api" \
  --stack "nodejs+postgres" \
  --desc "社区团购电商后端，支持商品管理、订单系统、优惠券、微信支付"
```

输出：
```
shop-api/
├── Makefile               ✅ make dev / make test / make build / make run
├── Dockerfile             ✅ node:22-alpine 多阶段构建
├── docker-compose.yml     ✅ api + postgres + redis
├── .dockerignore
├── package.json
├── prisma/schema.prisma   ✅ 数据模型（商品/订单/用户/优惠券）
├── README.md
└── src/
    ├── index.ts           ✅ 入口 + 路由注册
    ├── config/index.ts    ✅ 环境变量配置
    └── modules/
        ├── goods/         ✅ 商品模块骨架
        ├── order/        ✅ 订单模块骨架
        └── coupon/       ✅ 优惠券模块骨架
```

### 示例 2：创建数据采集服务

```bash
openclaw skill run ai-fullstack-project-scaffold \
  --name "crawler-service" \
  --stack "python+redis" \
  --desc "定时任务爬虫，抓取行业资讯并存入 PostgreSQL，支持关键词过滤"
```

输出：
```
crawler-service/
├── Makefile               ✅ make crawl / make schedule / make test
├── Dockerfile
├── docker-compose.yml     ✅ crawler + postgres + redis + scheduler
├── requirements.txt
├── README.md
└── src/
    ├── main.py            ✅ FastAPI 入口
    ├── config.py          ✅ 配置管理
    ├── spiders/           ✅ 爬虫模块（可扩展）
    ├── tasks/             ✅ 定时任务
    └── models/           ✅ 数据模型
```

## 高级用法

### 指定端口
```bash
--port 8080
```

### 增量开发（已有项目）
```bash
# 在已有项目目录下运行，自动生成缺失的文件
cd existing-project && openclaw skill run ai-fullstack-project-scaffold --name "existing" --stack "nodejs+postgres" --desc "补充缺失模块"
```

### 只生成 Docker 配置
```bash
openclaw skill run ai-fullstack-project-scaffold --name "my-api" --stack "go+postgres" --desc "仅生成 Docker 配置" --docker-only
```

## 注意事项

1. **kimi-cli** 需要本地安装 Kimi Code CLI 并配置 API Key
2. **代码生成质量**取决于需求描述的详细程度，建议描述越详细越好
3. 生成后请 review 代码，确保业务逻辑符合预期再提交到 git
4. Docker 配置默认为开发模式，生产部署需根据实际情况调整