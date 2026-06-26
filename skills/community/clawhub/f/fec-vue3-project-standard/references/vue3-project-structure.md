# Vue 3 project structure and component standards

## 项目结构

以下为中大型 Vue 3 项目的业界最佳实践结构，按项目实际情况裁剪：

```
src/
├── app/                        # 应用入口与全局配置
│   ├── App.vue                 # 根组件
│   ├── main.ts                 # 应用启动入口
│   └── router.ts               # 路由实例与配置
│
├── pages/                      # 页面组件（与路由一一对应）
│   ├── Dashboard/
│   │   ├── DashboardPage.vue
│   │   ├── components/         # 页面私有组件
│   │   └── composables/        # 页面私有 composables
│   ├── UserList/
│   └── Settings/
│
├── layouts/                    # 布局组件
│   ├── MainLayout.vue          # 主布局（侧边栏 + 顶栏 + 内容区）
│   ├── AuthLayout.vue          # 登录/注册页布局
│   └── BlankLayout.vue         # 空白布局（错误页等）
│
├── features/                   # 功能模块（按业务领域划分）
│   ├── auth/
│   │   ├── components/         # 模块组件
│   │   ├── composables/        # 模块 composables
│   │   ├── api.ts              # 模块 API 调用
│   │   ├── types.ts            # 模块类型定义
│   │   ├── constants.ts        # 模块常量
│   │   └── index.ts            # 模块公开导出
│   └── order/
│
├── components/                 # 全局共享 UI 组件
│   ├── AppButton/
│   │   ├── AppButton.vue
│   │   └── __tests__/
│   ├── AppModal/
│   ├── AppForm/
│   └── AppErrorBoundary/
│
├── composables/                # 全局共享 composables
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useMediaQuery.ts
│
├── services/                   # API 基础层
│   ├── request.ts              # Axios/fetch 实例与拦截器
│   └── endpoints/              # API 端点定义（如按领域拆分）
│
├── stores/                     # Pinia 状态管理
│   ├── authStore.ts
│   └── uiStore.ts
│
├── locales/                    # 国际化语言包
│   ├── zh-CN.json              # 中文
│   ├── en-US.json              # 英文
│   └── index.ts                # i18n 实例初始化（vue-i18n）
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
│   └── global.d.ts             # 全局类型扩展（组件类型、模块声明等）
│
├── utils/                      # 纯工具函数
│   ├── format.ts               # 日期、数字、货币格式化
│   ├── validators.ts           # 表单校验规则
│   └── storage.ts              # LocalStorage / SessionStorage 封装
│
├── directives/                 # 自定义指令
│   ├── vPermission.ts          # 权限指令
│   └── vClickOutside.ts        # 点击外部关闭
│
├── plugins/                    # Vue 插件注册
│   ├── i18n.ts                 # vue-i18n 插件配置
│   └── index.ts                # 插件统一注册入口
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

- `pages/` 做路由映射和布局组合，不放业务逻辑
- `layouts/` 定义页面骨架（侧边栏、顶栏、面包屑），由路由配置的 `component` 引用
- `features/` 按业务领域划分，模块内自包含（components + composables + api + types）
- `components/` 仅放无业务耦合的通用组件，可跨项目复用
- `composables/` 仅放通用逻辑（防抖、媒体查询等），业务 composables 放到对应 feature 中
- `locales/` 存放语言包 JSON 文件，模板中使用 `$t('key')` 而非硬编码文案
- `assets/` 存放静态资源，图标优先使用 SVG，图片优先使用 WebP/AVIF
- `config/` 封装环境变量和 Feature Flags，禁止组件中直接读取 `import.meta.env`
- `styles/themes/` 通过 CSS 变量实现主题切换，组件中引用变量而非硬编码颜色
- 每个模块通过 `index.ts` 管控公开 API，避免深层路径导入

## 组件设计规范

- 使用 `<script setup lang="ts">`
- 明确使用 `defineProps` / `defineEmits` 并附带类型
- 可复用逻辑优先提取到 composables
- 保持 template 可读，避免过深条件嵌套
- 优先使用计算属性，而不是重复维护状态
- 避免构建大型单体组件；**单文件规模**见 `templates/shared/rules/fec-vue.md`「**组件文件规模**」（约 300 行内为佳，逾 500 行或复杂度过高拆子组件与 Composables）
- 优先使用强类型的 props、emits 和暴露方法
- 遵循仓库的文件与目录命名规范
- 优先复用现有 UI 组件和 Token

### 组件分层

```
页面组件 (Pages)          → 路由映射、布局组合
  └── 容器组件 (Containers)  → 数据获取、状态编排
       └── 业务组件 (Features) → 领域逻辑展示
            └── 通用组件 (UI)   → 纯展示，无业务耦合
```

## 注释规范

- **优先使用中文**：解释「为什么这样做」、业务约束、边界情况、非显而易见的权衡时，优先用中文撰写注释，便于团队与业务方阅读。
- **与代码语言一致时的例外**：对接第三方协议字段名、HTTP 头、规范中的英文术语时，注释里可保留英文专有名词，必要时中英文并列说明。
- **少而精**：能通过清晰命名与类型表达清楚的逻辑不写废话注释；复杂分支、临时兼容、性能取舍必须写清意图。
- **公开 API**：composable 或模块的对外契约可用 JSDoc（`@param` / `@returns` / `@example`），说明用中文即可，除非仓库统一要求英文。

## TypeScript 规范

通用 TypeScript 工程规则由 `fec-typescript-project-standard` 负责，包括 `tsconfig`、strictness、DTO / view model 边界、`unknown` 收窄、public API 类型、声明产物和类型测试。

Vue 规范只补充 SFC、Props / Emits、暴露方法、Provide / Inject 和 composable 响应性类型；复杂类型建模或跨框架类型契约先分流到 `fec-typescript-project-standard`。

### Vue 3 项目补充约定

```vue
<script setup lang="ts">
interface Props {
  title: string;
  items: Item[];
  loading?: boolean;
}

interface Emits {
  (e: "select", item: Item): void;
  (e: "delete", id: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
});

const emit = defineEmits<Emits>();
</script>
```

- Props 和 Emits 使用 TypeScript interface 定义
- 使用 `withDefaults` 设置默认值
- `defineExpose` 暴露的方法需有类型约束

