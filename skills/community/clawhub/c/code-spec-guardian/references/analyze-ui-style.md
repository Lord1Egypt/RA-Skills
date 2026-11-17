# UI 风格分析指引 | UI Style Analyzer

> 指导 AI 分析项目 UI 风格，提取 `ui-style.md` 规范。

## 分析流程

1. **读 `references/ui-style.md`** 了解 38 个条目编号
2. **读 `project_context.json`** 获取框架信息；用 `exec` 搜索样式文件（`Get-ChildItem -Path src -Recurse -Include *.css,*.scss` 或 `find src -name '*.scss'`），用 `read` 读取
3. **抽样源文件**：用 `exec` 列 `src/components` 和 `src/views` 目录，`read` 抽读 5-10 个
4. **写入 `.code-spec/ui-style.md`**

## 各条目分析要点

### 配色 [UI-01~05]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-01 | 主题色 | 读配置中 Tailwind/UnoCSS/Element Plus/Ant Design 的 primary 色值；`exec` 搜 `color-primary`；抽样组件中 `type="primary"` 用法 |
| UI-02 | CSS 变量体系 | `read` 全局样式入口，提取所有 `--xxx` 按语义分组（颜色/间距/圆角/阴影/字号/字重/动画） |
| UI-03 | 功能色 | 搜 `success`/`warning`/`danger`/`info` 对应色值 |
| UI-04 | 中性色 | 搜 `text-color`/`bg-color`/`border-color` 层级 |
| UI-05 | 暗色模式 | `exec` 搜 `dark`/`prefers-color-scheme`；检查 `html.dark`/`[data-theme]`/VueUse `useDark()` |

### 字体 [UI-06~09]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-06 | 字体族 | 读全局样式中 `font-family`；检查 webfont 引入 |
| UI-07 | 字号体系 | 提取 `font-size` 值/Tailwind `text-*` 体系 |
| UI-08 | 字重 | 提取 `font-weight` 分布及语义命名 |
| UI-09 | 行高 | 提取 `line-height`/`leading-*` 模式 |

### 间距与形状 [UI-10~12]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-10 | 间距体系 | Tailwind spacing 自定义值或 `--spacing-*` 变量；观察 padding/margin/gap 实际值 |
| UI-11 | 圆角体系 | 提取 `border-radius` 值及语义（按钮/卡片/弹窗/输入框） |
| UI-12 | 阴影体系 | 提取 `box-shadow` 值，推断层级（small/card hover → medium/dropdown → large/modal） |

### 布局 [UI-13~15]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-13 | 布局方案 | 抽样页面统计 flex/grid/absolute 比例；识别代表性布局模式 |
| UI-14 | 响应式断点 | 读 Tailwind `screens` 或搜索 `@media` 断点；判断移动优先 vs 桌面优先 |
| UI-15 | 容器/栅格 | 搜 `max-width` 容器；检查 el-row/el-col、v-container 或 Tailwind container 配置 |

### 全局样式 [UI-16~18]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-16 | 全局 CSS 类规范 ⭐ | `read` 全局样式文件，提取自定义工具类（flex-center/text-ellipsis/cursor-pointer 等），分析命名约定 |
| UI-17 | 样式方案 | 判断 Tailwind 优先 / CSS Modules / styled-components / SCSS / Scoped style 及混合比例 |
| UI-18 | 全局样式入口 | 检查 main.ts/App.vue 中 import；CSS Reset/Normalize；body/html 基础样式；`:root` 变量范围 |

### 组件 [UI-19~24]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-19 | 组件库及版本 | 从 `project_context.json` → `frameworks` + `read` package.json 确认版本；判断按需 vs 全量引入 |
| UI-20 | 全局组件注册 ⭐ | 搜 `app.component(`/`app.use(`/`createApp`；检查 plugins 注册文件；检查 unplugin-vue-components/auto-import |
| UI-21 | 高频全局组件 ⭐ | 抽样 5-10 个页面，统计组件库组件 + 自定义业务组件使用频率，输出 Top 10 |
| UI-22 | 高频组件 Props 约定 ⭐ | 对 Top 10 组件抽样多个实例，提取常用 props 取值模式（size/type/width/rules 等） |
| UI-23 | 组件命名约定 | 文件命名（PascalCase/kebab-case）；Template 引用方式；页面 vs 通用组件区分 |
| UI-24 | 组件目录组织 | `exec` 列 `src/components`、`src/views` 结构（depth=2）；识别 common/business/layout 分层 |

### 全局函数 [UI-25~26] ⭐

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-25 | Composables/Hooks | 搜 `src/composables/`/`src/hooks/`；`read` 列出所有 hooks，说明用途和参数/返回值约定 |
| UI-26 | 全局工具函数 | 搜 `src/utils/`/`src/helpers/`；`read` 关键文件；识别日期/文件/验证等高频函数及导出方式 |

### 表单与交互 [UI-27~30]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-27 | 表单校验方案 | 从 frameworks 推断组件库校验；`exec` 搜 zod/yup/vee-validate/async-validator；检查规则定义位置和错误展示 |
| UI-28 | Toast/Message/Modal | 搜统一封装（如 `src/utils/message.ts`）；常用类型和参数；Modal/Confirm 使用约定 |
| UI-29 | 加载状态 | Skeleton 骨架屏使用；v-loading/n-spin/Spin 指令；首屏加载方案 |
| UI-30 | 空/错误状态 | Empty 组件使用约定；统一错误页 vs 内联提示；无数据时隐藏 vs 占位 |

### 动画与图标 [UI-31~33]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-31 | 过渡动画时长 | 提取 transition duration 值；组件库默认动画 |
| UI-32 | 缓动函数 | 提取 timing-function 值 |
| UI-33 | 图标库 | 从 frameworks 检查图标库依赖；判断使用方式（组件/CSS类/SVG）；命名风格 |

### 其他 [UI-34~35]

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-34 | 国际化 | 从 frameworks 检查 i18n 库；搜 `src/locales/`；语言文件位置和切换方式；`$t()`/`useI18n()` 用法 |
| UI-35 | z-index 层级 | 搜 `z-index` 值，推断层级体系（dropdown→sticky→modal→toast→loading） |

### 新建组件规范 [UI-36~38] ⭐

| 编号 | 条目 | 分析方法 |
|------|------|----------|
| UI-36 | 新组件全局样式 ⭐ | 汇总：root 元素应用什么 class、哪些全局 class 默认该用、文字层级和间距选择指南 |
| UI-37 | 新组件全局组件 ⭐ | 基于 UI-21 高频清单：优先使用的组件、布局骨架组件、通用基础设施组件 |
| UI-38 | 新组件必传入参 ⭐ | Vue：必填 props/emit 约定；React：props 类型/回调命名（onXxx）；是否要求类型定义和 JSDoc |
