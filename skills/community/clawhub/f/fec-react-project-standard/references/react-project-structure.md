# React project structure and component boundaries

## 项目结构（推荐参考）

以下为中大型 React 项目的业界最佳实践结构，按项目实际情况裁剪：

```text
src/
├── app/                        # 应用入口与全局配置
│   ├── App.tsx                 # 根组件（Provider 组合）
│   ├── routes.tsx              # 路由配置
│   └── providers.tsx           # 全局 Provider 组装
│
├── pages/                      # 页面组件（与路由一一对应）
│   ├── Dashboard/
│   │   ├── DashboardPage.tsx
│   │   ├── components/         # 页面私有组件
│   │   └── hooks/              # 页面私有 hooks
│   ├── UserList/
│   └── Settings/
│
├── layouts/                    # 布局组件
│   ├── MainLayout.tsx          # 主布局（侧边栏 + 顶栏 + 内容区）
│   ├── AuthLayout.tsx          # 登录/注册页布局
│   └── BlankLayout.tsx         # 空白布局（错误页等）
│
├── features/                   # 功能模块（按业务领域划分）
│   ├── auth/
│   │   ├── components/         # 模块组件
│   │   ├── hooks/              # 模块 hooks
│   │   ├── api.ts              # 模块 API 调用
│   │   ├── types.ts            # 模块类型定义
│   │   ├── constants.ts        # 模块常量
│   │   └── index.ts            # 模块公开导出
│   └── order/
│
├── components/                 # 全局共享 UI 组件
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.styles.css
│   │   └── __tests__/
│   ├── Modal/
│   ├── Form/
│   └── ErrorBoundary/          # 对 react-error-boundary 等的薄封装（函数组件）
│
├── hooks/                      # 全局共享 hooks
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useMediaQuery.ts
│
├── services/                   # API 基础层
│   ├── request.ts              # Axios/fetch 实例与拦截器
│   └── endpoints/              # API 端点定义（如按领域拆分）
│
├── stores/                     # 全局状态管理
│   ├── authStore.ts
│   └── uiStore.ts
│
├── locales/                    # 国际化语言包
│   ├── zh-CN.json              # 中文
│   ├── en-US.json              # 英文
│   └── index.ts                # i18n 实例初始化（i18next / react-intl）
│
├── assets/                     # 静态资源
│   ├── images/                 # 图片（PNG、JPG、WebP）
│   ├── icons/                  # SVG 图标
│   └── fonts/                  # 自定义字体
│
├── config/                     # 应用配置
│   ├── env.ts                  # 环境变量类型化封装
│   └── features.ts             # Feature Flags 管理
│
├── types/                      # 全局共享类型
│   ├── api.ts                  # API 响应/请求通用类型
│   ├── models.ts               # 业务实体类型
│   └── global.d.ts             # 全局类型扩展（图片模块声明等）
│
├── utils/                      # 纯工具函数
│   ├── format.ts               # 日期、数字、货币格式化
│   ├── validators.ts           # 表单校验规则
│   └── storage.ts              # LocalStorage / SessionStorage 封装
│
├── styles/                     # 全局样式与主题
│   ├── global.css              # 全局基础样式（reset / normalize）
│   ├── variables.css           # CSS 变量（颜色、间距、字号）
│   ├── breakpoints.ts          # 响应式断点常量
│   └── themes/                 # 主题定义
│       ├── light.css           # 亮色主题变量
│       ├── dark.css            # 暗色主题变量
│       └── index.ts            # 主题切换逻辑
│
└── constants/                  # 全局常量
    ├── routes.ts               # 路由路径常量
    └── config.ts               # 业务常量（分页大小、超时时间等）
```

### 关键原则

- `pages/` 做路由映射和页面编排，不承载大块可复用业务逻辑
- `layouts/` 负责页面骨架和布局容器，由路由配置引用
- `features/` 按业务领域划分，模块内尽量自包含
- `components/` 仅放跨页面、跨模块复用的通用组件
- `hooks/` 仅放全局通用 hooks；业务 hooks 优先放回对应 feature 或 page
- `locales/` 存放语言包 JSON 文件，组件中使用 `t('key')` 而非硬编码文案
- `assets/` 存放静态资源，图标优先使用 SVG，图片优先使用 WebP/AVIF
- `services/` 负责请求基础设施，不堆叠业务细节
- `config/` 统一封装环境变量和特性开关，禁止组件中直接读取 `import.meta.env`
- `styles/` 和主题变量统一管理，避免颜色和尺寸散落在业务代码中
- 每个模块通过 `index.ts` 管控对外公开 API，避免深层路径导入

---

## 组件与模块分层

推荐分层：

```text
页面组件 (Pages)        → 路由映射、布局组合、页面编排
  └── 容器/编排层        → 数据获取、状态组织、事件编排
       └── 业务组件      → 领域逻辑展示
            └── 通用组件 → 无业务耦合、可跨模块复用
```

### 什么时候放到 `pages/`

适合放：

- 路由入口组件
- 页面级布局组合
- 页面私有的轻量编排逻辑

不适合放：

- 大量领域逻辑
- 可复用于多个页面的复杂业务块
- 与某个业务域强绑定的 API / hooks / types

### 什么时候放到 `features/`

适合放：

- 某个业务域的组件、hooks、api、types
- 可被多个页面共享但带业务语义的逻辑
- 一个完整业务单元的自包含实现

### 什么时候放到 `components/`

适合放：

- 按钮、弹窗、表单项、表格壳子、空态、错误态等通用 UI
- 与具体业务无关、可跨模块复用的组件

---

## 组件设计规范

- 使用**函数组件**、Hooks 与 TypeScript；**不要**新增类组件（Error Boundary 用 `react-error-boundary` 等库，见下文）
- **单文件规模**与拆分原则见 `templates/shared/rules/fec-react.md`「**组件文件规模**」（约 300 行内为佳，逾 500 行或复杂度过高拆子组件、Hooks、utils、类型）
- 保持组件职责单一、可组合
- 将可复用逻辑提取到 hooks
- 在合适场景优先使用受控组件 API
- props 定义清晰且类型明确
- 优先复用现有设计系统组件
- 保持可访问性与键盘交互
- 避免过深的 JSX 嵌套和重复分支
- 对可推导的值不要额外存 state

---


## 组件目录建议

当组件复杂度较低时，可只保留一个文件。  
当组件包含样式、子组件、hooks、测试时，推荐使用如下结构：

```text
ComponentName/
├── ComponentName.tsx
├── ComponentName.types.ts
├── ComponentName.styles.css
├── hooks/
│   └── useComponentLogic.ts
├── components/
│   └── SubComponent.tsx
└── __tests__/
    └── ComponentName.spec.tsx
```

说明：

- 类型复杂时再拆 `ComponentName.types.ts`
- 存在局部逻辑复用时再拆 `hooks/`
- 子组件仅在当前组件内部使用时，放到当前目录 `components/`
- 测试是否就近放置，应遵循仓库现有约定

---

