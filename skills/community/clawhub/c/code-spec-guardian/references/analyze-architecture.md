# 架构规范分析指引 | Architecture Analyzer

> 指导 AI 分析项目架构，提取 `architecture.md` 规范。

## 分析流程

1. **先读 `references/architecture.md`** 了解条目编号
2. **读 `project_context.json`** 获取语言和框架信息；用 `exec` 列出项目目录结构（depth=2），用 `read` 读入口文件/路由/store 配置
3. **读关键文件**：入口文件（main.ts/main.py/App.vue 等）、路由配置、状态管理 store
4. **写入 `.code-spec/architecture.md`**

## 各条目分析要点

### 目录结构 [ARCH-01 ~ ARCH-02]

#### [ARCH-01] 项目目录布局
- 用 `exec` 列出项目根目录和 src 目录结构（depth=2）：`Get-ChildItem -Path . -Depth 2 | Select-Object FullName` 或 `find . -maxdepth 2 -type d`
- 项目根目录关键配置文件 + src/ 下的一级/二级目录
- 描述每个目录的职责

#### [ARCH-02] 模块划分原则
- 从目录结构判断：按功能模块还是按技术层分目录
- 用 `exec` 检测 monorepo 标志文件：`package.json` workspaces / `pnpm-workspace.yaml` / `lerna.json`

### 分层架构 [ARCH-03 ~ ARCH-04]

#### [ARCH-03] 分层结构
- 用 `exec` 搜索 controller/service/repository/model/view 相关目录：`Get-ChildItem -Path src -Directory -Recurse` 或 `find src -type d`
- 前端：components / pages / stores / api / utils 分层
- 后端：router → controller → service → dao 分层

#### [ARCH-04] 层间依赖规则
- 从 import 关系推断：service 只能被 controller 调？utils 可以被任意层用？
- 循环依赖检测

### 依赖管理 [ARCH-05 ~ ARCH-06]

#### [ARCH-05] 依赖注入
- 前端：provide/inject、Context.Provider
- 后端：nestjs DI、Spring IoC
- 来源：抽样 import 模式

#### [ARCH-06] 包管理器
- lock 文件（package-lock.json / pnpm-lock.yaml / yarn.lock）
- project_context.json 中 scripts 是否用了 pnpm/yarn

### 状态与路由 [ARCH-07 ~ ARCH-10]

#### [ARCH-07] 状态管理方案
- 从 `project_context.json` → `frameworks` 检查是否有 Pinia/Vuex/Redux/Zustand 等
- Pinia：store 命名、模块拆分方式
- Vuex：module 划分、命名空间
- Redux：slice 拆分、middleware
- Zustand/Jotai：store 文件位置

#### [ARCH-08] 全局 vs 局部状态
- 状态持久化方案（pinia-plugin-persistedstate / redux-persist）
- URL 参数作为状态（Vue Router query/params）

#### [ARCH-09] 路由方案
- 从 `project_context.json` → `frameworks` 检查是否有 vue-router/react-router 等
- 用 `exec` 搜索路由配置文件（如 `src/router/`）
- 路由配置文件位置、路由懒加载

#### [ARCH-10] 路由组织
- 嵌套路由 / 动态路由 / 路由守卫
- 路由 meta 信息定义
- 权限路由分离

### 工程化 [ARCH-11 ~ ARCH-19]

#### [ARCH-11] 构建工具
- 从 `project_context.json` → `configs` 中读 Vite/webpack 配置片段；如截断则用 `read` 读完整文件
- Vite：plugins 配置、proxy 配置
- Webpack：loaders、aliases

#### [ARCH-12] TypeScript 严格模式
- 从 `project_context.json` → `configs` 中读 `tsconfig.json` 片段；如截断则用 `read` 读完整文件
- 提取 strict / strictNullChecks / noImplicitAny
- paths / baseUrl 别名配置

#### [ARCH-13] 代码格式化
- 从 `project_context.json` → `configs` 中读 ESLint 和 Prettier 配置片段
- ESLint：parser、extends、rules 关键项
- Prettier：关键配置项
- 是否有自动修复（lint-staged）

#### [ARCH-14] 测试框架
- 从 `project_context.json` → `frameworks` 检查是否有 vitest/jest/playwright
- 用 `exec` 搜索 `package.json` 的 devDependencies 中的测试库
- 用 `exec` 搜索测试目录和文件：`Get-ChildItem -Path . -Recurse -Include *.test.ts,*.spec.ts` 或 `find . -name '*.test.ts'`
- 单元测试目录（__tests__ / src/**/*.test.ts）
- E2E 测试目录（cypress / e2e）

#### [ARCH-15] 环境变量
- 用 `read` 读 `.env` / `.env.development` / `.env.production` 等文件（只列变量名，不取值）
- 区分：构建时 vs 运行时

#### [ARCH-16] Monorepo
- 用 `exec` 检查 `pnpm-workspace.yaml` / `lerna.json` / `nx.json` / `turbo.json` 是否存在
- 子包目录结构

#### [ARCH-17] CI/CD
- 用 `exec` 检查 `.github/workflows/` / `.gitlab-ci.yml` / `Jenkinsfile` 是否存在
- 用 `read` 读 CI 配置文件
- 构建步骤、部署目标

#### [ARCH-18] Docker
- 用 `read` 读 `Dockerfile` / `docker-compose.yml`（如存在）
- Dockerfile 内容摘要
- docker-compose 服务列表

#### [ARCH-19] 国际化方案
- 从 `project_context.json` → `frameworks` 检查是否有 vue-i18n / react-i18next
- 用 `exec` 搜索 `src/locales/` 或 `src/i18n/` 目录
- 语言包位置、切换机制

### 错误与日志 [ARCH-20 ~ ARCH-22]

#### [ARCH-20] 全局错误处理
- 前端：Vue errorHandler / React ErrorBoundary
- 搜索 errorHandler / onError 钩子

#### [ARCH-21] 业务错误处理
- API 层错误处理封装
- 错误上报（Sentry / Aegis）

#### [ARCH-22] 日志方案
- 搜索 console.log 使用频率
- 统一的 logger 封装
- 后端日志框架
