---
name: fe-cli
version: "3.1.1"
homepage: https://github.com/z-Zihan/awesome-skills
description: >
  前端项目脚手架 CLI。支持 React/Vue/Next.js/Nuxt.js/Astro/React Native + shadcn/Ant Design/MUI/Tailwind
  + Zustand/Redux + i18n，初始化标准化前端项目。支持 9 种项目类型：Web SPA、后台管理、移动 H5、
  Electron 桌面端、Tauri 桌面端、SSR (Next.js/Nuxt)、小程序 (微信/Taro)、React Native 移动端、
  静态建站 (Astro/Gatsby/VitePress)。
  触发：用户要求创建新前端项目、初始化项目、搭建脚手架，
  或提到"新建前端项目"、"初始化项目"、"脚手架"、"创建 React/Vue 项目"。
  也可用于检查/审查已有前端项目的规范性。
---

# fe-cli — 前端项目脚手架

## 语言规则

**检测用户使用的语言，全程使用同一语言输出。** 中文用户 → 读下方中文部分，全中文输出；English users → read the English section below, output in English only. 技术术语（React、Vite、pnpm 等）保留原文即可。子技能文件为英文，AI 执行时根据用户语言输出对应语言的交互文本。

---

# 中文版

所有前端项目类型的统一入口。路由到类型专属子技能，并生成共享公共层（请求工具、全局样式、多环境配置等）。

## 快速开始

### 一句话启动（跳过所有问题）

```
用户: "初始化一个 React + Tailwind + Zustand 后台项目，叫 my-admin"
→ 识别类型=admin → 委派给 fe-cli-admin 快速模式
```

### 交互模式

```
用户: "新建前端项目"
→ 询问: "什么类型？" → 路由到子技能 → 子技能询问详细问题
```

## 项目类型检测

从用户请求中识别类型：

| 关键词 | 类型 | 子技能 |
|---|---|---|
| 后台/管理/Admin/Dashboard/CRUD | admin | fe-cli-admin |
| 移动/H5/手机/微信H5/Mobile | h5 | fe-cli-h5 |
| 桌面/Electron/客户端/Desktop | electron | fe-cli-electron |
| Tauri/轻量桌面/Rust桌面 | tauri | fe-cli-tauri |
| SSR/Next.js/Nuxt/服务端渲染/SEO | ssr | fe-cli-ssr |
| 小程序/微信小程序/MiniApp/WeChat | miniapp | fe-cli-miniapp |
| React Native/RN/原生移动/App | rn | fe-cli-rn |
| Astro/Gatsby/建站/博客/文档站/VitePress | astro | fe-cli-astro |
| (默认/官网/Web/SPA/网页) | web | fe-cli-web |

如果不确定，询问："这是什么类型的项目？Web SPA / 后台管理 / 移动H5 / Electron桌面 / Tauri桌面 / SSR / 小程序 / React Native / 静态建站"

### 输入澄清

当用户请求模糊时，**必须先澄清再执行**：
- **模糊输入**（如"帮我搞一下"、"新建项目"）→ 询问项目名称 + 类型 + 技术栈偏好
- **矛盾请求**（如"用 React 和 Vue"）→ 指出矛盾，请求确认使用哪一个
- **越界请求**（如"帮我部署到服务器"）→ 拒绝并说明："fe-cli 只负责本地项目初始化，部署请使用其他工具"
- **非前端请求**（如"写一个 Python 后端"）→ 拒绝并重定向："fe-cli 仅支持前端项目脚手架"

### 降级策略

- `bun create vite` / `pnpm create vite` 失败 → 提示用户手动创建，或检查网络/Node/Bun 版本
- 依赖安装失败 → 提示检查网络代理、npm registry 配置，提供淘宝镜像命令
- 目标目录已存在 → 询问："目录已存在，覆盖 / 合并 / 取消？"
- 模板中引用的包版本不存在 → 提示用户手动指定版本，不阻塞流程

## 路由到子技能

类型识别后，读取对应子技能的 SKILL.md：

```
Read: ./<type>/SKILL.md (relative to fe-cli/)
```

每个子技能负责：
1. 类型专属问题（框架、UI 库、状态管理、i18n、pre-commit）
2. 类型专属文件生成（布局、页面、路由）
3. 安装和后续配置

## 共享公共层

子技能生成类型专属文件后，在项目中生成以下共享文件。
Read `references/shared-base.md` and `references/shared-config.md` for code templates.

### 要生成的目录结构

```
project-name/
├── src/
│   ├── components/
│   │   ├── AppProvider.tsx      # 根级 Context Provider 包裹层
│   │   ├── AuthGuard.tsx        # 路由鉴权守卫（角色控制）
│   │   ├── ErrorBoundary.tsx    # React 错误边界
│   │   ├── GlobalLoading.tsx    # 全屏 Loading 遮罩
│   │   ├── PageLoading.tsx      # 页面级 Loading
│   │   ├── EmptyState.tsx       # 空状态占位
│   │   └── ErrorState.tsx       # 错误状态（含重试）
│   ├── config/
│   │   ├── index.ts             # 应用常量 + 环境配置
│   │   └── routes.tsx           # 集中式路由定义
│   ├── hooks/
│   │   ├── index.ts             # Re-export all hooks
│   │   ├── useRequest.ts        # 数据请求
│   │   ├── useDebounce.ts       # 防抖
│   │   ├── useLocalStorage.ts   # 类型安全的 localStorage
│   │   ├── useMediaQuery.ts     # CSS 媒体查询响应式
│   │   ├── useClickAway.ts      # 点击外部检测
│   │   ├── useToggle.ts         # 布尔切换
│   │   ├── usePrevious.ts       # 上一次值追踪
│   │   └── useUpdateEffect.ts   # 跳过首次渲染的 effect
│   ├── layouts/
│   │   ├── AppLayout.tsx        # 主布局（侧边栏 + 头部 + 内容）
│   │   ├── Header.tsx           # 顶栏（主题切换、用户菜单）
│   │   └── Sidebar.tsx          # 侧边导航
│   ├── locales/                 # （仅 i18n 选中时生成）
│   │   ├── index.ts             # i18n 初始化
│   │   ├── zh-CN.json           # 中文翻译
│   │   ├── en-US.json           # 英文翻译
│   │   └── useLanguage.ts       # 语言切换 hook
│   ├── store/                   # （仅状态管理选中时生成）
│   │   ├── index.ts             # Re-export stores
│   │   ├── useUserStore.ts      # 用户认证 & 信息
│   │   ├── useAppStore.ts       # 应用级状态（主题、语言、侧边栏）
│   │   └── middleware.ts        # 自定义中间件（logger、persist）
│   ├── theme/
│   │   ├── index.ts             # ThemeProvider + 主题逻辑
│   │   ├── tokens.ts            # 亮色 + 暗色设计令牌
│   │   └── useTheme.ts          # 主题 hook（读取/切换/主题感知类名）
│   ├── services/
│   │   ├── request.ts           # fetch 请求封装（含拦截器）
│   │   ├── logger.ts            # 结构化日志（分级、轮转、持久化）
│   │   ├── log-export.ts        # 日志导出（下载 .log/.json）+ 上报（待定）
│   │   └── api/
│   │       └── index.ts         # API 接口定义
│   ├── styles/
│   │   ├── global.scss          # CSS 变量 + 全局样式
│   │   ├── reset.scss           # CSS reset
│   │   └── variables.scss       # 设计令牌（颜色、间距、断点）
│   ├── utils/
│   │   ├── index.ts             # 通用工具函数（防抖、深拷贝等）
│   │   ├── storage.ts           # localStorage/sessionStorage 封装
│   │   ├── format.ts            # 日期/数字格式化
│   │   └── validate.ts          # 表单校验工具
│   └── types/
│       └── global.d.ts          # 全局类型声明
├── .env                       # 公共环境变量
├── .env.development           # 开发环境
├── .env.test                  # 测试环境
├── .env.production            # 生产环境
└── package.json               # Scripts 配置
```

### Package.json scripts

```json
{
  "scripts": {
    "dev": "vite --mode development",
    "dev:test": "vite --mode test",
    "build:test": "vite build --mode test",
    "build:prod": "vite build --mode production",
    "preview": "vite preview",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "typecheck": "tsc --noEmit"
  }
}
```

### 共享代码模板

基础层模板见 `references/shared-base.md`（含 logger.ts 和 log-export.ts）。
构建配置模板见 `references/shared-config.md`。
基础设施层模板见 `references/shared-infrastructure.md`（状态管理、主题系统、i18n、通用 Hooks、全局组件、布局、路由守卫、常量配置）。

**条件生成**：
- 用户选了 Zustand/Redux Toolkit/Pinia → 生成 `src/store/`
- 用户选了 i18n → 生成 `src/locales/`
- **无论选什么都生成**：`src/hooks/`（通用 hooks）、`src/components/AppProvider.tsx`、`src/components/AuthGuard.tsx`、`src/components/GlobalLoading.tsx`、`src/config/`、`src/theme/`

## AI 可读项目文档

生成所有项目文件后，在项目根目录生成 `.ai/PROJECT.md`。
This file is for AI agents to quickly understand the project.

### .ai/PROJECT.md 目标

- **完整目录树**，每个文件列出并有一行说明
- **技术栈摘要**（框架、UI 库、状态管理、CSS 等）
- **架构约定**（路径别名、导入顺序、命名规则）
- **命令**（dev、build、test、lint、typecheck）
- **关键模式**（路由、API 调用、状态管理）

### 模板

完整模板见 `references/ai-project-md.md`，根据具体项目类型调整目录树。

### 规则

- 目录使用 `tree` 命令格式（├── 和 └──），文件用一行说明
- 每个文件必须有说明其用途的注释
- 按目录分组，与实际文件系统顺序一致
- 项目结构变化时更新
- 保持简洁——每个文件一行，不是段落

## 关键规则

- **包管理器**：默认使用 **bun**（更快），备选 pnpm。检测方式：`bun --version` 存在则用 bun，否则用 pnpm
- **运行时**：默认 Node.js，bun 也可作为运行时（`bun run` 替代 `node`）
- **CSS 预处理器**：默认 Sass（SCSS 语法）
- **路径别名**：在 tsconfig 和 vite config 中配置 `@/` → `src/`
- **响应式断点**：Mobile < 768px < Tablet < 1024px < Desktop
- **网络库**：原生 fetch 封装（不用 axios），见 references/shared-base.md
- **环境文件**：始终生成 `.env`、`.env.development`、`.env.test`、`.env.production`
- **日志**：始终生成 `services/logger.ts` + `services/log-export.ts`。使用 `Logger.child("Module")` 模式。最大存储 5MB 自动清理。仅开发模式控制台输出。上报端点为占位符（待定）。
- **Node 版本**：目标 Node 18+
- **部署**：默认推荐 Vercel 部署（零配置），在项目生成后提供 `vercel` 初始化命令
- **图表库**：轻量场景推荐 Recharts，重场景用 ECharts
- **pnpm 构建脚本**：在 package.json 中使用 `pnpm.onlyBuiltDependencies` 自动批准原生构建（如 `@parcel/watcher`）。Vite 渲染层构建命令（`build:prod`、`build:test`）不应包含 `tsc -b`——Vite 处理 TS 转译；类型检查是独立的 `typecheck` 脚本。**Electron/Tauri 主进程例外**：主进程代码在 Node 环境运行，需要 `tsc -p tsconfig.electron.json` 编译。

## 模板占位符参数化

生成项目时，AI 应主动将模板中的占位值替换为用户提供的实际值，包括但不限于：
- `com.example.app` → 用户指定的应用 ID
- `https://api.example.com` → 用户指定的 API 地址
- `My App` / `Your App` → 用户指定的应用名称
- `https://update.example.com` → 用户指定的更新服务地址

完成后提示用户确认："项目已生成，请确认以下占位值是否正确：[列出替换后的值]"

## 已有项目审查

当用户要求检查已有项目时："检查这个前端项目"、"审查项目规范性"：

### 审查步骤

1. 读取 `package.json` → 检查必要依赖和脚本
2. 检查 vite.config / tsconfig / eslint / prettier 配置
3. 对照上述标准检查 src 目录结构
4. 输出审查报告

### 审查报告格式

```markdown
## 项目审查报告

### ✅ 符合项
- [列出符合标准的条目]

### ❌ 缺失项
- [缺失项]：描述 + 建议修复方案
- ...

### ⚠️ 建议项
- [可选改进]：描述
```

### 审查检查项

| 检查项 | 标准 |
|---|---|
| 包管理器 | 使用 bun（优先）或 pnpm |
| 路径别名 | tsconfig + vite.config 中 `@/` → `src/` |
| CSS 预处理器 | 配置 Sass (SCSS) |
| 环境文件 | 存在 `.env` / `.env.development` / `.env.test` / `.env.production` |
| 请求封装 | `services/request.ts` 使用 fetch wrapper（非 axios） |
| 日志 | `services/logger.ts` 存在，使用 `Logger.child("Module")` 模式 |
| 全局样式 | `styles/global.scss` + `reset.scss` + `variables.scss` |
| 主题系统 | `theme/` 目录存在，支持亮/暗模式切换 |
| 状态管理 | 若选了状态管理 → `store/` 目录存在，含 userStore + appStore |
| 多语言 | 若选了 i18n → `locales/` 目录存在，含 zh-CN + en-US |
| 通用 Hooks | `hooks/` 目录存在，含 useDebounce、useLocalStorage、useMediaQuery 等 |
| 全局组件 | `components/AppProvider.tsx` + `AuthGuard.tsx` + `GlobalLoading.tsx` |
| 布局组件 | `layouts/` 目录存在，含 AppLayout + Header + Sidebar |
| 路由配置 | `config/routes.tsx` 集中定义，非分散在各页面 |
| 常量配置 | `config/index.ts` 含路由路径、HTTP 状态码、分页默认值等 |
| 工具函数 | `utils/index.ts` + `storage.ts` + `format.ts` + `validate.ts` |
| 类型声明 | `types/global.d.ts` 含 ImportMetaEnv |
| Scripts | 含 dev / build:prod / build:test / lint / typecheck |
| .ai/PROJECT.md | 存在且与实际项目结构一致 |

---
---

# English Version

**fe-cli** is a unified entry point for scaffolding frontend projects. It detects the project type from user input and routes to one of 9 sub-skills: **web** (SPA), **admin** (dashboard/CRUD), **h5** (mobile), **electron** (desktop), **tauri** (lightweight desktop), **ssr** (Next.js/Nuxt), **miniapp** (WeChat Mini Program), **rn** (React Native), or **astro** (Astro/Gatsby/VitePress static site). Each sub-skill handles type-specific questions, file generation, and setup.

**Key rules:** Default package manager is **bun** (fallback: pnpm); default CSS preprocessor is **Sass (SCSS)**; path alias `@/` → `src/`; native **fetch** wrapper (no axios); always generate `.env` / `.env.development` / `.env.test` / `.env.production`; always generate `services/logger.ts` + `services/log-export.ts`; target Node 18+; Vite handles TS transpilation (separate `typecheck` script), except Electron/Tauri main process needs `tsc -p tsconfig.electron.json`; default deployment: **Vercel**; chart libs: **Recharts** (lightweight) / **ECharts** (heavy); new UI libs: **shadcn/ui + Lucide** (React), **shadcn-vue + Vue Bits** (Vue), **Chakra UI**, **React Bits**.

After type-specific files, generate the **shared common layer** (request utils, global styles, multi-env config, utilities, type declarations). Finally, generate `.ai/PROJECT.md` for AI-readability. Supports **existing project audit** against the same standards.

**Template placeholder rule:** When generating projects, AI should replace placeholders (`com.example.app`, `https://api.example.com`, etc.) with actual user-provided values and prompt the user to confirm.

Sub-skill files are in English; AI should output interaction text in the user's language during execution.
