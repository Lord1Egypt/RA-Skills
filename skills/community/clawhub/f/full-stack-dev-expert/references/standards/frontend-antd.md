# Ant Design（antd 5）管理后台规范（管理后台前端工程师实现必读）

适用：React 18+ / antd 5.x。定位：中后台/管理端默认 UI 方案（组件密度高、表单表格开箱即用）；
C 端高定制场景不适用（走 frontend-tailwind-shadcn.md）。

## 1. 主题与令牌

- 主题统一经 `ConfigProvider`（`theme.token`：主色/圆角/字号；`theme.components` 细调），
  禁止逐组件传 style 硬编码色值。
- 品牌色对齐 ui-spec 色板；语义色用 token（`colorError` 等）不写死。
- 中文字体栈显式配置；`dayjs` 为唯一日期库（antd5 内置），禁混用 moment。

## 2. 列表页范式（管理端 70% 页面形态）

- 查询表单 + 表格 + 服务端分页固定三段式；优先 `ProTable`（procomponents）承接：
  列定义（`columns`）集中声明：格式化（金额/时间/字典 tag）、宽度、操作列权限过滤。
- **服务端分页/筛选/排序**：`request` 接契约列表端点，参数映射契约字段名，
  不发明契约外筛选；`manual: false` + 查询防抖。
- 竞态防护：快速切筛选/翻页取消过期请求（AbortController/`request` 自身取消）。
- 批量操作：`rowSelection` + 批量按钮；执行后展示逐条结果（成功 n/失败 m+原因），
  并刷新列表保留当前页码策略（删空当前页回退一页）。

## 3. 表单范式

- `Form` 非受控优先：`Form.useForm()` + `onFinish` 提交，不逐 keystroke setState 同步。
- 校验规则与后端契约一致（`rules` 声明式），错误文案走 ui-spec 表单规范（说人话）。
- 编辑态 `form.setFieldsValue(initial)` 一次赋值；禁止 `preserve=false` 与受控混搭踩坑。
- 新建/编辑复用同一表单组件；提交 loading 防重复提交（按钮 disabled + 防抖）。
- 复杂分步/动态字段用 `Form.List`，仍保持一个 Form 实例，不拆多实例手同步。

## 4. 反馈与状态

- 命令式 API（message/notification/Modal.confirm）统一经 `App` 上下文
  （`App.useApp()`）调用，禁止静态方法直调（ConfigProvider 主题不生效）。
- 异步五态齐备：空（Empty/Table locale）/载（Table loading + 查询按钮 loading）/
  错（错误页+重试）/禁（无权限 disabled+tooltip）。
- 路由级 loading 与数据级 loading 分开（页面骨架 ≠ 表格 loading）。

## 5. 权限落地

- 按钮/操作列权限统一权限组件包裹（`<Auth code="order:delete">`），
  禁止散落 `hasPermission('xxx') &&` 三元链。
- 菜单与路由守卫走 admin-frontend-dev 角色定义的权限码机制；
  无权限页面直敲 URL 渲染 403，不白屏。

## 6. 样式共存纪律

- antd 与 Tailwind 并存时（仅限工具类布局）：关闭 Tailwind preflight 或用
  `@layer` 隔离，避免 reset 冲突按钮/输入框样式——是否并存由 ADR 决定，默认不并存。
- 覆盖 antd 样式用 token/`className` + CSS 变量，禁用 `:global` 深选择器硬怼。

## 7. 质量命令

```bash
npm run lint && npm run build
```

React 共性纪律见 `standards/frontend-react.md`；管理端页面形态与权限机制见
`agents/admin-frontend-dev.md`。
