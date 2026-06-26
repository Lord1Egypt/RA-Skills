# App Builder - 全栈应用开发技能

**功能**: 自动完成从页面设计、数据库构建到代码生成与部署的全流程，支持可视化调试

**版本**: 1.0.0  
**作者**: OpenClaw Workspace  
**创建日期**: 2026-03-16

---

## 🎯 核心能力

| 阶段 | 功能 | 输出 |
|------|------|------|
| 1. 需求分析 | 理解用户需求，生成 PRD | 需求文档、用户故事 |
| 2. 页面设计 | UI/UX 设计，原型生成 | Figma 链接、组件树 |
| 3. 数据库设计 | Schema 设计，ER 图 | SQL/NoSQL Schema、ER 图 |
| 4. 代码生成 | 前后端代码自动生成 | 完整项目代码 |
| 5. 可视化调试 | 实时预览，断点调试 | 预览链接、调试报告 |
| 6. 部署发布 | 一键部署到云平台 | 生产环境 URL |

---

## 🤖 多模型配置

### 模型优先级

1. **Claude Code** (首选) - 代码生成质量最佳
2. **通义千问** - 中文理解好，适合国内部署
3. **Gemini** - 多模态能力强
4. **智谱 GLM** - 代码生成能力优秀

### 配置文件

创建 `~/.config/app-maker/models.json`:

```json
{
  "default": "claude-code",
  "models": {
    "claude-code": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "apiKey": "sk-ant-...",
      "priority": 1,
      "capabilities": ["code", "design", "debug"]
    },
    "qwen": {
      "provider": "aliyun",
      "model": "qwen-max",
      "apiKey": "sk-...",
      "priority": 2,
      "capabilities": ["code", "design"]
    },
    "gemini": {
      "provider": "google",
      "model": "gemini-2.0-pro",
      "apiKey": "AIza...",
      "priority": 3,
      "capabilities": ["code", "multimodal"]
    },
    "glm": {
      "provider": "zhipu",
      "model": "glm-4-plus",
      "apiKey": "sk-...",
      "priority": 4,
      "capabilities": ["code"]
    }
  },
  "fallback": true,
  "maxRetries": 3
}
```

---

## 📋 工作流程

### 阶段 1: 需求分析

```yaml
输入：用户自然语言描述
输出:
  - prd.md: 产品需求文档
  - user_stories.md: 用户故事地图
  - features.json: 功能列表 (优先级排序)

步骤:
  1. 提取核心功能需求
  2. 识别目标用户群体
  3. 定义 MVP 范围
  4. 生成验收标准
```

### 阶段 2: 页面设计

```yaml
输入：PRD 文档
输出:
  - wireframes/: 线框图
  - components.json: 组件树
  - design_system.json: 设计规范

步骤:
  1. 生成用户流程图
  2. 创建页面线框图
  3. 设计组件层次结构
  4. 定义设计规范 (颜色、字体、间距)
```

### 阶段 3: 数据库设计

```yaml
输入：功能列表、数据需求
输出:
  - schema.sql / schema.prisma: 数据库 Schema
  - er_diagram.png: ER 图
  - migrations/: 迁移文件

步骤:
  1. 识别实体和关系
  2. 设计表结构
  3. 定义索引和约束
  4. 生成迁移脚本
```

### 阶段 4: 代码生成

```yaml
输入：设计文档、Schema
输出:
  - src/frontend/: 前端代码 (React/Vue/Flutter)
  - src/backend/: 后端代码 (Node.js/Python/Go)
  - src/api/: API 定义 (OpenAPI/GraphQL)
  - tests/: 测试文件

步骤:
  1. 初始化项目结构
  2. 生成数据模型层
  3. 生成 API 层
  4. 生成 UI 组件
  5. 生成业务逻辑
  6. 生成单元测试
```

### 阶段 5: 可视化调试

```yaml
输入：生成的代码
输出:
  - preview_url: 实时预览链接
  - debug_report.md: 调试报告
  - hot_reload: 热重载支持

步骤:
  1. 启动开发服务器
  2. 生成预览环境
  3. 运行自动化测试
  4. 捕获并修复错误
  5. 生成调试报告
```

### 阶段 6: 部署发布

```yaml
输入：通过测试的代码
输出:
  - production_url: 生产环境 URL
  - deploy_log.md: 部署日志
  - monitoring_dashboard: 监控面板

步骤:
  1. 构建生产版本
  2. 配置 CI/CD 流水线
  3. 部署到云平台
  4. 配置域名和 SSL
  5. 设置监控和告警
```

---

## 🛠️ 技术栈选择

### 前端框架

| 场景 | 推荐 | 备选 |
|------|------|------|
| Web 应用 | React + TypeScript | Vue 3 / Next.js |
| 移动应用 | Flutter | React Native |
| 桌面应用 | Electron | Tauri |
| 小程序 | 原生 | Uni-app |

### 后端框架

| 场景 | 推荐 | 备选 |
|------|------|------|
| API 服务 | Node.js (Express/Nest) | Python (FastAPI) |
| 实时应用 | Go + WebSocket | Node.js + Socket.io |
| 数据密集 | Python + Django | Java + Spring |
| 高并发 | Go | Rust |

### 数据库

| 场景 | 推荐 | 备选 |
|------|------|------|
| 关系型 | PostgreSQL | MySQL |
| 文档型 | MongoDB | Firestore |
| 缓存 | Redis | Memcached |
| 搜索 | Elasticsearch | Meilisearch |

### 部署平台

| 场景 | 推荐 | 备选 |
|------|------|------|
| Web 托管 | Vercel / Netlify | Cloudflare Pages |
| 容器部署 | Docker + K8s | ECS / Fargate |
| Serverless | AWS Lambda | Cloud Functions |
| 国内部署 | 阿里云 / 腾讯云 | 华为云 |

---

## 📁 项目结构模板

```
my-app/
├── .clawhub/
│   └── app-config.json      # 应用配置
├── docs/
│   ├── prd.md               # 产品需求文档
│   ├── user_stories.md      # 用户故事
│   ├── api_docs.md          # API 文档
│   └── deploy_guide.md      # 部署指南
├── design/
│   ├── wireframes/          # 线框图
│   ├── components.json      # 组件树
│   └── design_system.json   # 设计规范
├── database/
│   ├── schema.prisma        # 数据库 Schema
│   ├── er_diagram.png       # ER 图
│   └── migrations/          # 迁移文件
├── src/
│   ├── frontend/            # 前端代码
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── styles/
│   ├── backend/             # 后端代码
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   └── middleware/
│   └── shared/              # 共享代码
│       ├── types/
│       └── utils/
├── tests/
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── e2e/                 # 端到端测试
├── infra/
│   ├── docker/              # Docker 配置
│   ├── k8s/                 # K8s 配置
│   └── terraform/           # IaC 配置
├── .env.example             # 环境变量示例
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🚀 快速开始

### 1. 初始化新项目

```bash
# 创建新项目
npx app-builder init my-app

# 或使用交互式向导
npx app-builder create
```

### 2. 配置模型

```bash
# 设置首选模型
npx app-builder config set model claude-code

# 配置 API Key
npx app-builder config set claude-api-key sk-ant-...
```

### 3. 生成应用

```bash
# 从自然语言描述生成
npx app-builder generate "创建一个任务管理应用，支持团队协作、看板视图、截止日期提醒"

# 或从 PRD 文件生成
npx app-builder generate --from docs/prd.md
```

### 4. 预览和调试

```bash
# 启动预览服务器
npx app-builder preview

# 运行测试
npx app-builder test

# 可视化调试
npx app-builder debug --visual
```

### 5. 部署

```bash
# 部署到 Vercel
npx app-builder deploy vercel

# 部署到阿里云
npx app-builder deploy aliyun

# 自定义部署
npx app-builder deploy --config infra/deploy.json
```

---

## 🔧 命令行参考

### 核心命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `init` | 初始化新项目 | `app-builder init my-app` |
| `generate` | 生成应用代码 | `app-builder generate "描述"` |
| `preview` | 启动预览服务器 | `app-builder preview --port 3000` |
| `debug` | 可视化调试 | `app-builder debug --visual` |
| `deploy` | 部署应用 | `app-builder deploy vercel` |
| `config` | 配置管理 | `app-builder config set model claude-code` |

### 生成选项

```bash
app-builder generate <description> [options]

选项:
  --framework <name>     指定框架 (react/vue/flutter)
  --backend <name>       指定后端 (node/python/go)
  --database <name>      指定数据库 (postgres/mongo)
  --template <name>      使用模板 (saas/ecommerce/social)
  --from <file>          从文件生成 (PRD/设计稿)
  --output <dir>         输出目录
  --dry-run              预览生成内容，不写入文件
```

### 调试选项

```bash
app-builder debug [options]

选项:
  --visual               启用可视化调试界面
  --hot-reload           启用热重载
  --breakpoints <file>   设置断点文件
  --logs                 实时日志输出
  --performance          性能分析
```

---

## 📊 可视化调试界面

### 功能特性

1. **实时预览**: 查看应用运行效果
2. **组件树**: 可视化组件层次结构
3. **状态检查**: 检查应用状态和数据流
4. **网络监控**: 查看 API 请求和响应
5. **性能分析**: 识别性能瓶颈
6. **错误追踪**: 捕获和定位错误

### 界面布局

```
┌─────────────────────────────────────────────────────────┐
│  🔍 App Builder Debug Console                           │
├─────────────┬─────────────────────┬─────────────────────┤
│             │                     │                     │
│  组件树     │    实时预览         │   属性面板          │
│             │                     │                     │
│  - App      │   ┌───────────┐     │  选中组件：        │
│  - Layout   │   │           │     │  - 名称            │
│  - Header   │   │  Preview  │     │  - Props           │
│  - Main     │   │           │     │  - State           │
│  - Footer   │   │           │     │  - Events          │
│             │   └───────────┘     │                     │
│  数据流     │                     │                     │
│  - Store    ├─────────────────────┴─────────────────────┤
│  - API      │  📊 性能  │  🌐 网络  │  ⚠️ 错误  │  📝 日志 │
│             │                                             │
└─────────────┴─────────────────────────────────────────────┘
```

---

## 🔐 安全最佳实践

### 代码安全

- [ ] 使用参数化查询防止 SQL 注入
- [ ] 实现输入验证和清理
- [ ] 使用 HTTPS 加密通信
- [ ] 实现适当的认证和授权
- [ ] 存储敏感信息使用环境变量

### 数据安全

- [ ] 加密存储敏感数据
- [ ] 实现数据备份策略
- [ ] 遵守数据保护法规 (GDPR 等)
- [ ] 实施访问控制和审计日志

### 部署安全

- [ ] 使用最小权限原则
- [ ] 定期更新依赖
- [ ] 启用安全扫描
- [ ] 配置 WAF 和 DDoS 防护

---

## 📈 性能优化

### 前端优化

```json
{
  "codeSplitting": true,
  "lazyLoading": true,
  "imageOptimization": true,
  "caching": {
    "strategy": "stale-while-revalidate",
    "maxAge": 3600
  },
  "bundleAnalysis": true
}
```

### 后端优化

```json
{
  "databaseIndexing": true,
  "queryOptimization": true,
  "caching": {
    "redis": true,
    "ttl": 300
  },
  "connectionPooling": true,
  "rateLimiting": {
    "enabled": true,
    "requests": 100,
    "window": 60
  }
}
```

---

## 🧩 插件系统

### 内置插件

| 插件 | 功能 | 状态 |
|------|------|------|
| `@app-builder/react` | React 代码生成 | ✅ |
| `@app-builder/vue` | Vue 代码生成 | ✅ |
| `@app-builder/flutter` | Flutter 代码生成 | ✅ |
| `@app-builder/prisma` | Prisma ORM 支持 | ✅ |
| `@app-builder/vercel` | Vercel 部署 | ✅ |
| `@app-builder/aliyun` | 阿里云部署 | ✅ |

### 开发自定义插件

```bash
# 创建插件模板
npx app-builder plugin create my-plugin

# 插件结构
my-plugin/
├── src/
│   ├── generator.ts    # 代码生成器
│   ├── templates/      # 模板文件
│   └── index.ts        # 插件入口
├── package.json
└── plugin.json         # 插件配置
```

---

## 📝 示例项目

### 示例 1: 任务管理应用

```bash
npx app-builder generate "创建一个任务管理应用，包含以下功能：
- 用户认证 (登录/注册)
- 项目管理 (创建、编辑、删除)
- 任务看板 (待办、进行中、已完成)
- 团队协作 (邀请成员、分配任务)
- 截止日期提醒
- 文件附件
- 活动日志

技术栈：React + Node.js + PostgreSQL
部署目标：Vercel + Supabase"
```

### 示例 2: 电商应用

```bash
npx app-builder generate "创建一个电商应用：
- 商品展示和搜索
- 购物车和结算
- 用户评价
- 订单管理
- 支付集成 (支付宝/微信)
- 物流追踪
- 后台管理

技术栈：Next.js + Python + MongoDB
部署目标：阿里云"
```

---

## 🆘 常见问题

### Q: 如何切换模型？

```bash
# 查看可用模型
npx app-builder config list

# 切换默认模型
npx app-builder config set default-model qwen

# 临时使用其他模型
npx app-builder generate "..." --model gemini
```

### Q: 如何自定义生成的代码风格？

创建 `.apprc` 配置文件：

```json
{
  "codeStyle": {
    "language": "typescript",
    "semi": true,
    "singleQuote": true,
    "trailingComma": "es5"
  },
  "architecture": {
    "pattern": "mvvm",
    "stateManagement": "zustand"
  }
}
```

### Q: 如何集成现有项目？

```bash
# 导入现有项目
npx app-builder import ./existing-project

# 增强现有代码
npx app-builder enhance --target ./src
```

---

## 📚 资源链接

- **文档**: https://docs.app-builder.skill
- **模板库**: https://templates.app-builder.skill
- **插件市场**: https://plugins.app-builder.skill
- **社区**: https://discord.gg/app-builder
- **GitHub**: https://github.com/app-builder/skill

---

*最后更新：2026-03-16*
