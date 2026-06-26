# AI 全栈项目脚手架工厂

> 描述你的项目需求 → AI 自动生成完整的项目结构、代码框架、Makefile 和 Docker 配置

## 🎯 业务场景

**适用人群：** 全栈工程师、后端开发者、创业团队、技术管理者

**场景：** 当你需要快速初始化一个新项目时——无论是 Node.js REST API、Python 爬虫服务、Go 微服务，只需要描述需求，脚手架自动生成，包含代码框架、标准化构建脚本和生产级 Docker 配置。

---

## 😣 痛点分析

| 痛点 | 传统方式 | 本技能 |
|------|---------|--------|
| 项目初始化慢 | 手动创建目录、复制模板、配置环境，每次耗时 2-4 小时 | 一键生成，5 分钟完成 |
| 技术决策纠结 | 反复查文档选技术栈，容易选错重做 | AI 自动推荐最优技术栈组合 |
| 规范不统一 | 每个项目 Makefile/Docker 配置风格各异 | 标准化模板，统一规范 |
| Docker 配置难 | 每次都要查文档调优，生产镜像体积大 | AI 生成多阶段构建，自动安全加固 |
| 任务无追踪 | 项目做着做着不知道进度到哪了 | 自动生成任务清单，版本化管理 |

---

## 🧩 Skill 编排图谱

```
用户输入：项目需求描述
    │
    ▼
┌─────────────────────────────┐
│  dev-task                   │  需求解析 + 版本规划 + 任务清单
│  技能：版本化开发流程         │
└────────────┬────────────────┘
             │ VERSION.md + TODO.md
             ▼
┌─────────────────────────────┐
│  kimi-cli                    │  生成完整项目代码框架
│  技能：大模型代码生成 CLI      │  前端+后端+数据库，自动技术选型
└────────────┬────────────────┘
             │ 完整项目结构
             ▼
┌─────────────────────────────┐
│  makefile-generator          │  生成标准化 Makefile
│  技能：多语言 Makefile 生成    │  dev/test/build/run/deploy 命令规范
└────────────┬────────────────┘
             │ Makefile
             ▼
┌─────────────────────────────┐
│  docker-expert               │  生产级 Docker 配置
│  技能：容器化专家              │  多阶段构建、安全加固、docker-compose
└─────────────────────────────┘
   输出：可运行、可部署的完整项目
```

---

## 📦 依赖的 Skills

| Skill | 作用 | 关键能力 |
|-------|------|---------|
| **dev-task** | 需求解析 & 任务规划 | 版本化开发、任务清单生成 |
| **kimi-cli** | 大模型代码生成 | 多语言支持、大型项目脚手架生成 |
| **makefile-generator** | 标准化构建脚本 | Node.js/Python/Go/Java 多语言支持 |
| **docker-expert** | 容器化配置 | 多阶段构建、安全加固、最佳实践 |

---

## 🚀 使用示例

### 场景 1：创建一个社区电商后端 API

**需求：** "社区团购电商后端，支持商品管理、订单系统、优惠券、微信支付"

**执行：**
```bash
openclaw skill run ai-fullstack-project-scaffold \
  --name "shop-api" \
  --stack "nodejs+postgres" \
  --desc "社区团购电商后端，支持商品管理、订单系统、优惠券、微信支付"
```

**输出项目结构：**
```
shop-api/
├── Makefile               ✅ make dev / make test / make build / make run
├── Dockerfile            ✅ node:22-alpine 多阶段构建
├── docker-compose.yml    ✅ api + postgres + redis
├── .dockerignore
├── package.json
├── prisma/schema.prisma   ✅ 数据模型
├── README.md
└── src/
    ├── index.ts           ✅ 入口 + 路由注册
    ├── config/index.ts    ✅ 环境变量配置
    └── modules/
        ├── goods/          ✅ 商品模块骨架
        ├── order/          ✅ 订单模块骨架
        └── coupon/         ✅ 优惠券模块骨架
```

### 场景 2：创建数据采集服务

**需求：** "定时任务爬虫，抓取行业资讯并存入 PostgreSQL，支持关键词过滤"

**执行：**
```bash
openclaw skill run ai-fullstack-project-scaffold \
  --name "crawler-service" \
  --stack "python+postgres" \
  --desc "定时任务爬虫，抓取行业资讯并存入 PostgreSQL，支持关键词过滤"
```

**输出项目结构：**
```
crawler-service/
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── src/
    ├── main.py
    ├── config.py
    ├── spiders/
    └── models/
```

### 场景 3：创建文件上传服务（Go）

**需求：** "大文件分片上传，支持断点续传"

**执行：**
```bash
openclaw skill run ai-fullstack-project-scaffold \
  --name "file-upload-service" \
  --stack "go+minio" \
  --desc "大文件分片上传，支持断点续传和 S3 协议兼容存储"
```

---

## 🔧 技术栈速查

| 命令示例 | 语言 | 数据库 | 适用场景 |
|---------|------|--------|---------|
| `--stack nodejs+postgres` | Node.js/TypeScript | PostgreSQL | REST API、电商后端 |
| `--stack nodejs+mysql` | Node.js/TypeScript | MySQL | 传统业务系统 |
| `--stack python+postgres` | Python/FastAPI | PostgreSQL | 数据采集、AI 服务 |
| `--stack python+redis` | Python/FastAPI | Redis | 缓存优先、异步任务 |
| `--stack go+postgres` | Go/Gin | PostgreSQL | 高性能 API |
| `--stack go+minio` | Go/Gin | MinIO | 对象存储服务 |
| `--stack java+postgres` | Java/Spring | PostgreSQL | 企业级系统 |

---

## ⚠️ 使用前提

1. **kimi-cli** 需安装并配置 Kimi Code CLI API Key
2. **Docker** 环境可用（本地或远程）
3. 首次使用建议在空目录运行，生成后 review 代码再提交 git