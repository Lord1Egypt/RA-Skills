---
subdomain: react-admin
version: 9
updated: 2026-11-17
---
# react-admin

## 定位与心智模型

react-admin（当前 **5.15.7**，npm 锚定 2026-11-15）是基于 React + react-router + TanStack Query + react-hook-form + MUI 的**前端管理后台框架**（非组件库）。三层契约架构：**DataProvider**（数据访问，9 方法）→ **authProvider**（认证授权，≥4 方法）→ **UI 组件**（List/Edit/Show/Create 组合）。

核心设计哲学："never blocks you"——任何组件都可被自有实现替换 [官方文档](https://marmelab.com/react-admin/)。组合模型：`<List>`/`<Edit>` 负责**取数与上下文**，渲染委托给子组件。

## 法则

[RA-1] **MUST**: 生成表格代码前确认 react-admin 版本与表格线：v5.8+ 新代码用 `<DataTable>`，存量 `<Datagrid>` 合法但勿混写。
- 违反后果: 新项目用 Datagrid 走向弃用轨道；混写两条线维护困难。
- 溯源: [官方文档](https://marmelab.com/react-admin/Datagrid.html) + npm 5.15.7 锚定

[RA-2] **MUST**: getList 必须返回 `{ data, total }`。
- 违反后果: 分页控件异常/崩溃。
- 溯源: [官方文档](https://marmelab.com/react-admin/Tutorial.html)

[RA-3] **MUST**: 自定义 Field/组件消费 `useRecordContext()` 前必须判空。
- 违反后果: 加载期 record undefined，组件白屏。

[RA-4] **MUST**: authProvider 四方法必须是 async 且用 reject 表达失败；checkError 对 401 必须 reject。
- 违反后果: return false 语义无效；401 死循环不登出。
- 溯源: [官方文档](https://marmelab.com/react-admin/Tutorial.html)

[RA-5] **MUST**: DataProvider 错误必须 throw（非 2xx + status），驱动通知与 checkError（全局宪法 LAW-8）。
- 违反后果: 接口失败 UI 无反馈像卡死。

[RA-6] **MUST**: Field 用于展示（List/Show）、Input 用于编辑（Edit/Create），不得混用。
- 违反后果: 列表里 Input 无表单上下文报错；表单里 Field 只读不提交。

[RA-7] **MUST**: 开源核心与 EE 分界先查清再引用：`<CanAccess>`/`useCanAccess`/`useCanAccessResources`/`authProvider.canAccess` 为**开源核心**（`import { CanAccess } from 'react-admin'`）；EE 为 `@react-admin/ra-*` 包（ra-rbac/ra-realtime/ra-navigation 等）与 react-admin-ee 站模块——EE 能力用前查 react-admin-ee.marmelab.com 确认模块与版本要求。
- 违反后果: 引用不存在的 EE 能力 import 报错；误判核心能力为 EE 导致方案降级。
- 溯源: [官方文档](https://marmelab.com/react-admin/CanAccess.html)（import 自 react-admin 铁证）+ [官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-realtime)

[RA-12] **MUST**: 表单校验四选一且不混写：Form 级 `validate` 与 Input 级 `validate` **互斥**（react-hook-form 限制）；schema 校验用 `resolver`；服务端校验仅 pessimistic 模式生效。
- 违反后果: 双轨 validate 静默失效；undoable/optimistic 下服务端字段错误不回显。
- 溯源: [官方文档](https://marmelab.com/react-admin/Validation.html)

[RA-8] **MUST**: `optimized` Datagrid 的 children 必须静态。
- 违反后果: 动态列（权限分支渲染）break。
- 溯源: [官方文档](https://marmelab.com/react-admin/Datagrid.html)

[RA-9] **MUST**: 完全自定义 layout 时必须保留 `<Notification>`（及 Confirm 类全局容器）。
- 违反后果: 全局通知不弹，保存成功无提示。

[RA-10] **MUST**: 对接自定义后端先写 DataProvider 映射层（10~30 行），不改后端凑 simple-rest 约定。
- 违反后果: 后端为前端框架改契约，维护倒挂。
- 溯源: [官方文档](https://marmelab.com/react-admin/Tutorial.html)

[RA-11] **MUST**: 用户文案必须走 i18nProvider（`useTranslate`/`ra.*` 覆写），不得硬编码。
- 违反后果: 内建文案无法本地化；多语言项目返工。

[RA-13] **MUST**: ReferenceInput 族的通用 Input props（label/validate/format/parse/optionText/onCreate）必须传给**子组件**，不得传给 ReferenceInput 本体。
- 违反后果: props 静默无效——校验丢失、label 不显、format/parse 不生效
- 溯源: [官方文档](https://marmelab.com/react-admin/ReferenceInput.html)

[RA-14] **MUST**: 过滤 Input 不得同时设 `defaultValue` 与 `alwaysOn`（技术限制互斥）——alwaysOn 过滤器的默认值改经 `<List filterDefaultValues>` 提供。
- 违反后果: 过滤器不显示或默认值丢失
- 溯源: [官方文档](https://marmelab.com/react-admin/FilteringTutorial.html)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| Resource | `<Resource name="posts" list={PostList} .../>`，一个后端实体类型 |
| DataProvider | 数据访问契约：getList/getOne/getMany/getManyReference/create/update/updateMany/delete/deleteMany |
| authProvider | 认证契约：login/logout/checkError/checkAuth（+扩展 getIdentity/getPermissions） |
| RecordContext | 当前记录上下文，`useRecordContext()` 消费 |
| source 机制 | Field/Input 的字段路径 prop（支持点路径），从 record 读取 |
| 乐观更新 + Undo | 保存后 UI 立即更新，约 5 秒后才真正发请求，可撤销 [官方文档](https://marmelab.com/react-admin/Tutorial.html) |
| i18nProvider | `translate/changeLocale/getLocale` 三契约，内置 polyglot |
| layout | `<Admin layout={...}>` 可整体替换；`<CustomRoutes>` 挂非资源页 |
| canAccess | `authProvider.canAccess({ resource, action, record? }) → Promise<boolean>`——授权推荐轨；未实现则**视为全放行** |
| mutationMode | 三模式：pessimistic（等响应）/ optimistic（本地先改失败回滚）/ undoable（延迟发请求+Undo）；Edit 默认 undoable，hooks 默认 pessimistic，Create 恒 pessimistic |
| format / parse | Input 值双向转换：format（record→input，默认 null→''）；parse（input→record，默认 ''→null） |
| queryKey 结构 | `[resource, method, params]`（如 `['orders', 'getList']`）——invalidateQueries 精确失效 |

## 最佳实践

### 场景：起步与代码生成

推荐路径：`npm create react-admin@latest my-admin -- --interactive` → Guesser（ListGuesser/EditGuesser）把猜测代码**打印到控制台**，复制出来再定制。坑：Guesser 代码只作起点，别直接提交。
- 来源：[官方文档](https://marmelab.com/react-admin/Tutorial.html)

### 场景：对接自定义 REST 后端（[RA-10]）

推荐路径：写映射层（10~30 行），DataProvider 契约内消化差异；httpClient 包一层注入 Authorization（fetchJson 工具，勿手改 Content-Type boundary）。

```tsx
// don't：改后端凑 simple-rest 约定
// do：映射层消化差异（[RA-10]）
const dataProvider: DataProvider = {
  getList: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const res = await httpClient(`/api/${resource}?page=${page}&size=${perPage}`);
    if (res.status < 200 || res.status >= 300) throw new HttpError(...);  // [RA-5]
    return { data: res.json.items, total: res.json.count };               // [RA-2]
  },
};
```

边界条件：page 从 1 起；order 'ASC'/'DESC'；后端不支持 updateMany/deleteMany 时逐条退化。

**DataProvider 增强工具链**（[官方文档](https://marmelab.com/react-admin/DataProviders.html)，2026-11-15 深度补强）：

- **缓存调优**：react-admin 内部自建 QueryClient（React Query 默认：stale 即后台重取/inactive 5min GC/失败静默重试 3 次）；覆盖传 `<Admin queryClient>`（常改 staleTime/retry/refetchOnWindowFocus）；组件级 `<List queryOptions={{ staleTime: 60000 }}>`，hook 第三参 `useUpdate(resource, params, { retry: false })`
- **生命周期拦截**：`withLifecycleCallbacks(baseProvider, [{ resource, beforeDelete, beforeSave, ... }])`——级联删除等前置逻辑放这里（优先放服务端）
- **多 API 组合**：`combineDataProviders((resource) => switch...)` 按 resource 分发；更复杂用 Proxy + 资源名前缀
- **查询取消**：`dataProvider.supportAbortSignal = true` → dataProvider 调用收 `params.signal` 传给 fetch（组件卸载取消在途请求）
- **关联预取**：响应带 `meta.prefetched` 填充 queryClient 缓存，`<ReferenceField>` 免二次请求；embed（响应内嵌）是双刃剑需测量
- **离线支持**：`addOfflineSupportToQueryClient` + `<PersistQueryClientProvider>` + `resumePausedMutations`；自定义 mutation 需 `mutationKey` + `setMutationDefaults`
- 异步初始化 dataProvider：`useState`/`useEffect` + `setDataProvider(() => provider)`（**函数式 setState**——legacy provider 可能是函数，防立即调用）

### 场景：表格选型（[RA-1]/[RA-8]）

推荐路径：v5.8+ 新代码 `<DataTable>` + `<DataTable.Col>`（官方推荐继任者，存量 Datagrid 合法 + codemod）；大数据页 `optimized`（children 必须静态 [RA-8]）或 `<DatagridConfigurable>` 减渲染列；移动端 `<SimpleList>`；超大导出走后端异步任务。

```tsx
// 新代码（推荐）：DataTable
<DataTable rowClick="edit">
  <DataTable.Col source="id" />
  <DataTable.Col source="email"><EmailField source="email" /></DataTable.Col>
</DataTable>
```

**Datagrid 细节（文档锚定）**：`rowClick` 取值 `edit|show|expand|toggleSelection|false` 或自定义函数；`bulkActionButtons` 定制批量操作；`expand`/`expandSingle` 行展开（`isRowExpandable` 控制哪些行可展开）；`isRowSelectable` 函数控制哪些行可选；列排序控制 `sortable={false}`/`sortBy`/`sortByOrder="DESC"`；`<DatagridConfigurable>` 用户配置列显隐（`<SelectColumnsButton>` 入口、`omit` 排除、`<WrapperField>` 包非 Field 子元素）；**无障碍：rowClick 行点击键盘不可达——MUST 加 `<EditButton>`/`<ShowButton>` 列**；脱离 `<List>` 独立使用：传 `resource/data/total/isPending/sort` props，交互需 `useList` + `<ListContextProvider>`；EE 有 EditableDatagrid 与 DatagridAG（[RA-7]）。

### 场景：认证与权限（[RA-4]）

推荐路径：authProvider 四契约 async + reject 语义——checkError 对 401 reject（触发登出）；403 按业务决定；checkAuth 只查本地凭证，API 失效靠 checkError 兜底。自定义登录页：`<Admin loginPage>` 组件替换（`<LoginForm>` children 定制字段；`<Login>` 换 backgroundImage）；完全从零建用 `useLogin()`（提交凭据调 authProvider.login）。

**授权推荐轨（Access Control，2026-11-16 深度补强）**：`authProvider.canAccess({ resource, action, record? }) → Promise<boolean>`——授权逻辑收在 authProvider 内（RBAC/ABAC/ACL 任选）：

- **页面组件内置访问控制**：`<List>/<Create>/<Edit>/<Show>` 渲染前自动调 canAccess（action: list/create/edit/show）；拒绝 → Access Denied 页（/accessDenied 可定制）；**authProvider 未实现 canAccess 视为全放行**
- **操作按钮内置访问控制**：EditButton/CreateButton/DeleteButton/ShowButton/ListButton 无权限自动隐藏
- 细粒度用核心 `<CanAccess>`/`useCanAccess`（开源，[RA-7]）——props：action（必填）/resource/record/loading/accessDenied/error；多资源批量 `useCanAccessResources`
- **性能**：canAccess 在页面渲染前调用——慢则导航延迟；**登录时取权限存本地**保持快
- Permissions 旧轨（getPermissions + usePermissions）仍支持——自由格式（string/数组/对象）；`<Admin>` 函数子元素收 permissions 条件注册 Resource（仅一个此类子元素）
- 细粒度 RBAC（角色/组/通配符/显式 deny/record-level + RBAC 感知 List/Edit/Datagrid/SimpleForm）= **EE @react-admin/ra-rbac**（[RA-7]）

**认证开关矩阵**：自定义页默认无保护（`useAuthenticated`/`<Authenticated>` 包裹）；单页放行匿名 `disableAuthentication`（List/Create/Edit/Show 系）；全站强制 `<Admin requireAuth>`（UI 隐藏防信息泄漏；不影响 `<CustomRoutes noLayout>` 公共页）；OAuth 回调走内置 `/auth-callback` 路由 → `authProvider.handleCallback`；Refresh Token 用官方装饰器 `addRefreshAuthToAuthProvider` + `addRefreshAuthToDataProvider`。
- 来源：[官方文档](https://marmelab.com/react-admin/Authentication.html)、[官方文档](https://marmelab.com/react-admin/Permissions.html)

### 场景：输入组件与校验（[RA-12]）

**Input 通用语义（2026-11-16 深度补强）**：

- **readOnly vs disabled**：readOnly 可聚焦且**参与提交**；disabled 不可聚焦、**不进表单值**（且可能误触发 `warnWhenUnsavedChanges`）——想让值进提交用 readOnly
- **format/parse**：format（record→input）默认 `null→''`；parse（input→record）默认 `''→null`——单位换算/日期对象转换成对用（口诀：parse 进 record，format 出 input）
- **defaultValue 层级**：Form 级 `defaultValues` > Input 级；**defaultValue 不接受函数**（运行时计算用 Form 级函数）；`''`/`0`/`null`/`[]` 均为合法值（非 undefined 即非空，defaultValue 不生效）
- **联动 Input**：react-hook-form `useWatch` 或 `<FormDataConsumer>`（render props；ArrayInput 行内联动用 `scopedFormData`）
- **按条件隐藏 Input**：FormDataConsumer + `shouldUnregister`（卸载不提交）；**shouldUnregister 避免与 ArrayInput 同用**（useFieldArray 重排时序问题）——改用 Edit `transform` 清理

**校验四轨（[RA-12]）**：

1. Form 级 `validate`（函数收 values 返回 errors 按 source 索引；可 async）——与 2 互斥
2. Input 级 `validate`：内建工厂 required/minValue/maxValue/minLength/maxLength/number/email/regex/choices/unique()（useUnique 异步唯一）或自定义（undefined=通过）；**校验器数组定义在组件外**（JSX 内联数组每次渲染新建引用 → 无限重渲染）
3. schema `resolver`（@hookform/resolvers：yup/zod/valibot/ArkType 等全支持）
4. 服务端校验：**仅 pessimistic 生效**——dataProvider throw 的 body.errors 按 source 回显；`root.serverError` 全局错误位

校验器返回翻译 key 或 `{ message, args }` 自动过 translate。校验模式默认 onSubmit + reValidateMode onChange（`<SimpleForm mode="onBlur">` 可改）。
- 来源：[官方文档](https://marmelab.com/react-admin/Inputs.html)、[官方文档](https://marmelab.com/react-admin/Validation.html)

### 场景：参考关联输入（ReferenceInput 族，[RA-13]）

- **职责边界（核心心智模型）**：ReferenceInput 管"取数 + 提供 ChoicesContext"；子组件管"渲染选择 + 通用 props"（label/validate/format/parse/optionText/onCreate 传子组件，传 ReferenceInput 无效 [RA-13]）；自定义子组件用 `useChoicesContext` 取 choices
- **双查询**：挂载即 `getList(reference, { filter, sort, pagination })`（默认 page 1/perPage 25）+ `getMany(reference, { ids: [当前值] })` 解引用；**同资源多引用自动聚合为单次 getMany**（性能设计，勿改 getOne）；数组外键用 `<ReferenceArrayInput>`（默认 `<AutocompleteArrayInput>`，getMany 传 ids 数组）
- **默认子组件与谱系**：ReferenceInput 默认 `<AutocompleteInput>`；换子组件直接嵌套（不传 source）：SelectInput / RadioButtonGroupInput / SelectArrayInput / DualListInput / CheckboxGroupInput / DataTableInput（`multiple` 多列对比，@react-admin/ra-form-layout，普通 ReferenceInput 也可用）
- **搜索过滤链路**：输入词进 `filter: { q: [...] }`（q 是**数组**）；子组件 `filterToQuery={searchText => ({ name_ilike: `%${searchText}%` })}` 改写匹配 API；`filter` prop 是**永久过滤**，与搜索词互不影响（叠加）
- **懒加载**：`enableGetChoices={({ q }) => q && q.length >= 2}` 达条件才调 getList——大数据量资源必备；`perPage` 调大只对 Select/CheckboxGroup 型子组件有意义（Autocomplete 可搜索过滤，默认 25 够用）；`queryOptions` 传 getList 查询参数
- **显示名**：reference 资源的 `recordRepresentation`（Resource 定义处）；子组件 `optionText` 覆盖
- **现场创建**：子组件 `onCreate`（简单场景直接建）或 `create`（弹自定义 UI 收集更多字段）；`useCreate` + `{ returnPromise: true }` 返回新记录自动选中
- **离线兜底**：`offline` prop（字符串或元素）——仅当"引用记录缺失**且**无网络"时渲染
- **Filter 表单特例**：ReferenceInput 的 label 在 Filter 中用作过滤标签（Edit/Create 中设 label 无效果），子组件 label 仍须自设；树形引用用 `@react-admin/ra-tree` 的 `<ReferenceNodeInput>` 替代
- 来源：[官方文档](https://marmelab.com/react-admin/ReferenceInput.html)、[官方文档](https://marmelab.com/react-admin/ReferenceArrayInput.html)

### 场景：List 架构与过滤深水（useListController / FilteringTutorial）

- **List 架构链**：`useGetList` → `ListContextProvider` → `useListController` → `ListBase` → `List`——`<List>` 是配置器：把 `filters`/`sort`/`perPage`/`filter` 等 props 喂给 controller，渲染结果入 ListContext，再渲染子组件（Datagrid 等）
- **controller 内建行为**：取数（页/排序/过滤变化自动重查）、URL 持久化（刷新不丢）、过滤 debounce、状态记忆（返回 List 保留页码/过滤）、aggregate 查询、数据转 UI；`emptyWhileLoading`（默认 true）：子组件挂载时若有上一次查询数据先用旧数据渲染（避免闪烁）
- **自定义复用**：不想要 `<List>` 默认 UI 用 `<ListBase>` + `useListController()`（或 `useListContext` 消费）；`<WithListContext render={...}>` 拿 context 免自定义组件
- **预排序/预过滤进 List 的链接**：须传**全部** query 参数（page/perPage/sort/order/filter），漏了会被 controller 默认值重置
- **四种过滤 UI**：`<List filters={[...]}>`（默认，FilterForm+FilterButton）/ `<FilterList>` aside 侧栏 / SavedQueriesList（保存查询组合）/ `<Search>`（EE）；**StackedFilters 也是 EE**
- **filters 数组渲染两次 [RA-14]**：元素同时渲染进 FilterForm（表单区）与 FilterButton（按钮 label 区）——同一 source 的 Quick Filter 只能一个、自定义组件须兼容两处
- **alwaysOn 与 defaultValue 互斥 [RA-14]**：alwaysOn 过滤器默认值用 `<List filterDefaultValues={{ ... }}>`（Link 进 List 页同理）
- **FilterList 侧栏**：`<FilterList label icon>` + `<FilterListItem label value={{...}}>`（value 对象字面量）；侧栏内搜索必须 `<FilterLiveSearch>`（普通 SearchInput 无效）；可配 SavedQueriesList
- **filter 存 URL**：JSON 序列化进 query string——自定义 filter 值须可 JSON 序列化；Date 类对象直接存会出问题（转 ISO 字符串）
- **filter 操作符**：**无官方后缀约定**（`_gte` 等是 demo 约定）——后端不认须在 DataProvider 转换
- **自定义过滤表单**：`<FilterLiveForm>` 挂 controller（自动 debounce+URL 持久化）；绕过它自建表单 = 每击键发一次请求
- **SavedQueriesList**：用户保存 filter+sort 组合持久跨会话；默认 UI（Button+Form 组合）自带，FilterList 侧栏需手动加 `<SavedQueriesList />`
- 来源：[官方文档](https://marmelab.com/react-admin/ListTutorial.html)、[官方文档](https://marmelab.com/react-admin/FilteringTutorial.html)

### 场景：数据 hooks 与副作用（Actions）

- Query hooks（挂载执行）：useGetList/useGetOne/useGetMany/useGetManyReference → `{ data, isPending, error }`；第三参 React Query options + onSuccess/onError/onSettled；组件级 `queryOptions` prop 覆写
- Mutation hooks（调用执行）：useCreate/useUpdate/useUpdateMany/useDelete/useDeleteMany → `[mutate, { data, isPending, error }]`；组件级 `mutationOptions` prop（UpdateButton + useNotify/useRedirect 标准范式）
- **loading 判断一律 isPending**（isFetching 含后台 refetch；isLoading=pending+fetching）——重访页面有 stale 数据不显示 loading
- **mutationMode**（[核心概念]）：Edit 默认 undoable / hooks 默认 pessimistic / Create 恒 pessimistic（须等响应拿 id 重定向）；undoable 下副作用立即执行（onSuccess 不能依赖响应数据），notify 传 `{ undoable: true }` 显示 Undo
- queryKey 结构 `[resource, method, params]`：`queryClient.invalidateQueries({ queryKey: ['orders', 'getList'] })` 部分刷新；列表/详情 shape 不同时 onSuccess 里 resetQueries 防缓存误填
- `meta` 参数透传 DataProvider 自行解释（如 `{ _embed: 'authors' }`）；自定义 RPC 方法：useDataProvider + @tanstack/react-query useMutation
- 来源：[官方文档](https://marmelab.com/react-admin/Actions.html)

### 场景：主题与布局定制

推荐路径：单组件 `sx` → 全局 `<Admin theme>`（展开 defaultTheme；palette/typography/components）→ 布局整体替换。

- **5 内建主题**：Default / B&W / Nano / Radiant / House
- **3 内建布局**：`<Layout>`（默认侧边栏）/ `<SolarLayout>`（核心）/ `<ContainerLayout>`（顶栏——**@react-admin/ra-navigation EE 包**，[RA-7]）
- 页面元素定制 prop：`<Layout appBar/menu/sidebar/error>`、`<AppBar userMenu>`、`<Admin loginPage/notification>`
- 布局配套 MUI 三件套：Box（通用容器）/ Stack（堆叠）/ Grid（栅格）
- 来源：[官方文档](https://marmelab.com/react-admin/Theming.html)

### 场景：自定义页面 / 布局 / 菜单（[RA-9]）

推荐路径：非资源页 `<CustomRoutes>`（react-router 基座，不需布局加 `noLayout` 防双 AppBar）→ 首页 `<Admin dashboard={...}>` → 菜单替换 `<Menu>` 子元素（MenuItemLink）。完全自定义 layout **必须保留 `<Notification>`**。

### 场景：i18n（[RA-11]）

推荐路径：内置 polyglot——`<Admin i18nProvider>` 三契约 `translate(key, options)` / `changeLocale(locale)` / `getLocale()`；`useTranslate()` 消费；框架内建文案全部可覆写（`ra.*` key 约定，如 `ra.navigation.no_results`）；多语言字段用 `<TranslatableInputs/Fields>`。
坑：自定义组件裸字符串不走 translate；浏览器语言检测要有 fallback locale；后端错误消息 key 与前端共享翻译集；日期/货币本地化需另配 adapter。

### 场景：实时更新（realtime，[RA-7]）

推荐路径：开源版 DIY——WebSocket/SSE 订阅（按 resource 维度）→ 消息到达 `queryClient.invalidateQueries`（精确更新用 setQueryData）；与 NestJS Gateway 推送配合（见 `kb/nestjs.md`）。
坑：WS 事件直接 setState 绕过 queryClient（切页回旧数据）；乐观更新与远端推送冲突覆盖。

EE 对应物（文档锚定，2026-11-15）：**ra-realtime 5.4.0**，要求 **react-admin ≥ 5.9.0**——DataProvider 扩展 `subscribe/unsubscribe/publish` + 锁协作（lock/unlock）；hooks `usePublish/useSubscribe/useSubscribeToRecord/useSubscribeToRecordList`；UI `<ListLiveUpdate>/<EditLive>/<ShowLive>`；topic 格式 `resource/[name]`，事件 `{ type, payload }`（created/updated/deleted）；后端适配 Supabase/API Platform/Mercure [官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-realtime)。

### 场景：EE 模块深挖（ra-ai / ra-datagrid-ag，[RA-7]）

**ra-ai 5.5.0**——AI 能力统一入口是 **DataProvider 扩展 2 个 AI 方法**（自行实现对接 LLM 提供商）：`generateContent(messages) → Promise<string>`（驱动 `<SmartRichTextInput>` 富文本内 AI 生成与 `<FormFillerButton>` 从图像/摄像头/文本提示填表）+ `suggestCompletion(...) → Promise<string>`（输入框内联补全建议）。版本要求以 changelog 为准：v5.5.0 要求 react-admin ≥ 5.14.1（文档头 ≥5.0.2 为旧值）。

**ra-datagrid-ag 7.2.0**（react-admin ≥ 5.3.0）——基于 ag-grid 的企业表格，**双组件分工**：

- `<DatagridAG>`：**服务端模式**——经 ListContext 拿部分数据集，排序/过滤/分页变化自动调 dataProvider；**代价：失去 grouping/pivoting/aggregating/高级过滤（含 multi-filters）/multi-sorting/auto page size**
- `<DatagridAGClient>`：**客户端模式**——`<List perPage={10000} pagination={false}>` 一次拉全量（官方测 10000 条无性能问题），排序/过滤/分页全客户端，解锁 grouping 等客户端特性；**不兼容 `<InfiniteList>`**；默认模块 `ClientSideRowModelModule`+`AllCommunityModule`+`CsvExportModule`（自定义 `modules` 至少保留 `ClientSideRowModelModule`）
- **包级限制：不支持 ag-grid server-side row model**；v7.x 支持 AG Grid v35/v36（v36 改 DOM 结构与部分 CSS 类名——自定义样式可能受影响）+ MUI v9
- v6.0.0 BREAKING 线索（升级必读）：ag-grid v33+ 新包名（`ag-grid-react`/`ag-grid-community`/`ag-grid-enterprise`，有 codemod）；v33 Theming API——**移除旧 CSS imports（ag-grid.css/ag-theme-*.css），改 theme 对象**（`themeBalham.withParams({...})`）；**`darkTheme` prop 已移除**（主题内建明暗，跟随 `<Admin>` 主题）；**selection 复选框列自动添加，除非 `bulkActionButtons={false}`**
- 就地编辑：双击单元格 → `dataProvider.update`（`editType="fullRow"` 整行编辑；`mutationOptions` 传 mutationMode/meta/onSuccess）；`preferenceKey`（默认 `${resource}.ag-grid.params`）持久化列宽/排序/过滤到 Store
- 来源：[官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-ai)、[官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-datagrid-ag)

### 场景：性能

推荐路径：`perPage` 默认 25，调大后配套优化；TanStack Query 基座调优 staleTime/gcTime 减少列表闪烁（DevTools 排网络瀑布）；ReferenceField 自动请求去重合并（N 个外键引用同资源自动合并）[官方文档](https://marmelab.com/react-admin/Tutorial.html)。

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | 列表页分页控件异常/报错 | getList 忘返回 total | [RA-2] |
| 2 | 列空白但不报错；自定义 Field 白屏 | source 拼写错 / useRecordContext 加载期 undefined | [RA-3] 判空 |
| 3 | 401 后不登出死循环 | authProvider return false 当失败用 | [RA-4] reject 语义 |
| 4 | 引用 `@react-admin/ra-*` 包组件报错（如 ContainerLayout） | EE 组件（CanAccess 已核心化，[RA-7] 修正） | 核心 CanAccess/useCanAccess；EE 能力查 react-admin-ee |
| 5 | 列表里 Input 报错；表单里 Field 不提交 | Field/Input 混用 | [RA-6] |
| 6 | 接口失败页面像卡死，无通知 | DataProvider 吞错 | [RA-5] throw + status |
| 7 | `optimized` 后动态列异常 | children 必须静态 | [RA-8] |
| 8 | 保存成功无任何提示 | 自定义 layout 丢了 `<Notification>` | [RA-9] |
| 9 | disabled 的 Input 值提交时消失（或误报未保存变更） | disabled 不进表单值；readOnly 才进 | 想保留值用 readOnly |
| 10 | Form 级 + Input 级校验只有一套生效 | 双轨 validate 互斥（RHF 限制） | 四轨选一 [RA-12] |
| 11 | 页面无限重渲染/卡死 | 校验器数组 JSX 内联（每次渲染新引用） | 数组定义在组件外 |
| 12 | 服务端字段校验错误不回显表单 | 仅 pessimistic 模式生效；或 errors key 与 source 不对应 | mutationMode 改 pessimistic；key 对齐 source |
| 13 | shouldUnregister + ArrayInput 行为异常 | useFieldArray 重排后 unregister 时序问题 | 用 Edit `transform` 清理提交值 |
| 14 | canAccess 配了但页面全放行/全拦 | authProvider 未实现 canAccess 视为全放行；实现了则 List/Create/Edit/Show 全走它 | 确认方法名与签名 |
| 15 | 页面导航莫名延迟 | canAccess 在页面渲染前调用且慢 | 登录时取权限存本地 |
| 16 | useCanAccess 结果用于 defaultValue 无效 | canAccess 异步解析，非响应式 props 读不到 | `!isPending` 后再渲染该 Input |
| 17 | ReferenceInput 上的 validate/label/format/parse 不生效 | 通用 props 归子组件，传本体无效 | 传给内嵌子组件 [RA-13] |
| 18 | AutocompleteInput 输入搜索词不触发请求 | enableGetChoices 设了门槛未达标 | 输入达阈值再查；未设门槛则挂载即拉 |
| 19 | Select 型子组件选项只显示 25 条 | 默认 perPage 25 | 调大 perPage 或改用可搜索的 Autocomplete |
| 20 | Filter 表单里 ReferenceInput 的 label 缺一份 | Filter 用本体 label 作过滤标签，子组件 label 独立 | 本体与子组件两处都设 |
| 21 | alwaysOn 过滤器配 defaultValue 不生效/不显示 | 两者技术限制互斥 | `<List filterDefaultValues>` [RA-14] |
| 22 | 自定义过滤表单每击键发一次请求 | 绕过 FilterForm/FilterLiveForm 失去 debounce | 用 `<FilterLiveForm>`（自动 debounce+URL 持久化） |
| 23 | 预排序链接进 List 排序丢了 | 只传了 sort/order，漏其余 query 参数 | 全参数（page/perPage/sort/order/filter）都传 |
| 24 | 同一 source 挂两个 Quick Filter 只出一个 | filters 元素渲染两处（表单+按钮），同 source Quick Filter 唯一 | 合并或拆 source [RA-14] |

**Top 展开：坑点 2（useRecordContext 判空）**

```tsx
const FullNameField = () => {
  const record = useRecordContext();
  if (!record) return null;  // 判空不可省（[RA-3]）：加载期间 record 为 undefined
  return <span>{record.first_name} {record.last_name}</span>;
};
```

**Top 展开：坑点 6（DataProvider 错误链路，[RA-5]/LAW-8）**

react-admin 靠 Promise rejection 驱动错误通知与 checkError：非 2xx 必须 throw（携带 status）→ notification 弹出 + checkError({ status }) 收到 → 401 触发登出。吞错 = 整条链失明。

## API 速查表

| API | 签名要点 | 易错点 |
|---|---|---|
| DataProvider.getList | `(resource, { pagination, sort, filter }) => { data, total }` | page 从 1 起；order 'ASC'/'DESC'；忘 total [RA-2] |
| getManyReference | `(resource, { target, id, ... })` | target 是外键字段名，id 是父记录 id |
| updateMany / deleteMany | `ids: any[]` | 后端不支持时逐条退化 |
| authProvider.checkError | `({ status }) => Promise<void>` | 401/403 忘 reject [RA-4] |
| useRecordContext | `() => record \| undefined` | 忘判空 [RA-3] |
| `<List>` | 取数/分页/排序/过滤上下文 | `filters={[...]}` 数组；alwaysOn |
| `<DataTable>` | `rowClick` + `<DataTable.Col>`（v5.8+ 推荐） | 新代码首选 [RA-1] |
| `<Datagrid>` | `rowClick/optimized/bulkActionButtons/expand` | optimized 禁动态 children [RA-8] |
| `<ReferenceField>` | `source` 外键 + `reference` 目标资源 | 请求自动去重合并 |
| `<ReferenceInput>` | source/reference/filter/sort/pagination/queryOptions/enableGetChoices/offline | 默认渲染 `<AutocompleteInput>`；通用 input props 传子组件 [RA-13] |
| `<ReferenceArrayInput>` | 同 ReferenceInput；数组外键（getMany 传 ids 数组） | 默认 `<AutocompleteArrayInput>` |
| enableGetChoices | `(filter) => boolean` 达标才 getList | 懒加载大数据量必备 |
| filterToQuery（子组件） | `searchText => filter`，默认 `{ q }`（q 为数组） | 改写搜索匹配 API |
| i18nProvider | translate/changeLocale/getLocale | 自定义文案不走 translate [RA-11] |
| `<CustomRoutes>` | `<Admin>` 内挂非资源路由 | `noLayout` 防双 AppBar |
| recordRepresentation | `<Resource recordRepresentation={...}>` | 定制记录引用显示 |
| DataProvider httpClient | 包一层注入 Authorization | fetchJson 工具；勿手改 Content-Type boundary |
| `<CanAccess>` / useCanAccess | action（必填）/resource/record + loading/accessDenied/error | **开源核心**（旧认知 EE 已修正）[RA-7]；canAccess 异步 [坑点 16] |
| mutationMode | pessimistic/optimistic/undoable | Edit 默认 undoable；Create 恒 pessimistic；服务端校验仅 pessimistic [RA-12] |
| format / parse | Input 值双向转换 | parse 进 record，format 出 input |
| useUpdate 等 mutation hooks | `[mutate, { data, isPending, error }]` + mutationOptions | loading 用 isPending（非 isFetching） |
| `<Admin requireAuth>` / disableAuthentication | 全站强制认证 / 单页放行匿名 | requireAuth 不影响 noLayout 公共页 |
| addRefreshAuthToAuthProvider/DataProvider | Refresh Token 官方装饰器 | accessToken 过期自动刷新 |
| useListController / ListBase | controller 逻辑收拢进 ListContext | URL 持久化/过滤 debounce/状态记忆内建；`emptyWhileLoading` 默认 true |
| `<FilterList>` / `<FilterListItem>` | aside 侧栏：label/icon + value 对象字面量 | 侧栏搜索必须 `<FilterLiveSearch>`；SavedQueriesList 须手动加 |
| FilterForm / FilterButton | `<List filters>` 默认过滤 UI | filters 元素渲染两处；alwaysOn 与 defaultValue 互斥 [RA-14] |
| `<List filterDefaultValues>` | alwaysOn 过滤器默认值 | alwaysOn+defaultValue 互斥时用它 [RA-14] |
| SavedQueriesList | 保存 filter+sort 组合，跨会话持久 | 默认 UI 自带；侧栏模式手动挂 |

## 版本注意

- **版本锚定：5.15.7**（npm `react-admin` 页，2026-11-15 抓取）；v5 系列
- **v5.8.0 引入 `<DataTable>`** 作为 `<Datagrid>` 继任者：新代码推荐 DataTable；Datagrid 向后兼容保留 + 官方 codemod [官方文档](https://marmelab.com/react-admin/Datagrid.html)
- 教程锚定的现行 API（硬事实）：`<DataTable>`/`<DataTable.Col>`、create-react-admin 脚手架、DataProvider 9 方法、authProvider 4 方法、乐观更新+Undo、MUI `sx` [官方文档](https://marmelab.com/react-admin/Tutorial.html)
- 技术栈基座（官方明示）：React、react-router、TanStack Query、react-hook-form、TypeScript；框架无关（默认 Vite SPA，可跑 Next.js/Remix）[官方文档](https://marmelab.com/react-admin/)
- **依赖矩阵（npm registry 验证 5.15.7，2026-11-15）**：`@mui/material`/`@mui/icons-material` `^5.16.12 || ^6 || ^7 || ^9`（MUI 四线支持）；react-router `^6.28.1 || ^7.1.1`（6/7 双线）；react-hook-form `^7.72.0`；@tanstack/react-query `^5.83.0`；peer react/react-dom `^18 || ^19`
- 生态：50+ DataProvider 适配器、10+ authProvider 适配器；开源版 170+ hooks/components；RBAC 细粒度权限、可编辑表格、realtime、审计日志属企业版（EE）[官方文档](https://marmelab.com/react-admin/)
- **EE 模块全景（18 个，react-admin-ee.marmelab.com 锚定 2026-11-15）**：ra-form-layout / ra-relationships / ra-navigation / ra-datagrid-ag / ra-soft-delete（New）/ ra-ai（New）/ ra-rbac / ra-audit-log / ra-history / **ra-realtime** / ra-markdown / ra-tree / ra-search / ra-calendar / ra-scheduler（New）/ ra-json-schema-form / ra-editable-datagrid / ra-tour
- **ra-realtime 5.4.0**：要求 react-admin ≥ 5.9.0；订阅/发布/锁协作全功能模块（开源版 DIY 方案的 EE 对应物）[官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-realtime)
- **ra-ai 5.5.0**（2026-11-17 锚定）：DataProvider 扩展 `generateContent`/`suggestCompletion` 两个 AI 方法 + `<SmartRichTextInput>`/`<FormFillerButton>`；changelog v5.5.0 要求 react-admin ≥ 5.14.1 [官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-ai)
- **ra-datagrid-ag 7.2.0**（2026-11-17 锚定，react-admin ≥ 5.3.0）：`<DatagridAG>`（服务端分页）vs `<DatagridAGClient>`（客户端全量）双组件；AG Grid v35/v36；MUI v9；不支持 ag-grid server-side row model [官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-datagrid-ag)

## 与其他子领域的集成要点

- **NestJS**：Nest 做 react-admin 后端 = 实现 9 个 REST 语义 + 分页/排序/filter 映射（`page` 从 1 起）+ 统一错误格式（非 2xx + JSON body）；自己写 controller 映射——`@nestjsx/crud` **已停更 4 年以上**（最后发布 2022-04，stable 4.6.2 停在 2020-05，npm registry 核实 2026-11），Nest 12 下无兼容承诺，不应采用 → 见 `kb/nestjs.md`
- **Next.js**：react-admin 框架无关可挂 Next.js，但 `<Admin>` 所在文件必须 `'use client'`，且不用 App Router 数据获取（react-admin 自带 TanStack Query 层）→ 见 `kb/nextjs.md`
- **TanStack Query**：开源版 realtime DIY、staleTime 调优直接操作底层 queryClient → 见 `kb/tanstack-query.md`
- **react-core**：大量消费 React context（RecordContext/ListContext）——context 级联渲染坑、自定义 hook 判空模式直接适用 → 见 `kb/react-core.md`

## 来源索引

- react-admin 官方首页（技术栈/生态/EE 边界）：https://marmelab.com/react-admin/ [官方文档]
- 官方 Tutorial（现行 API 锚点）：https://marmelab.com/react-admin/Tutorial.html [官方文档]
- Datagrid 参考（v5.8 DataTable 继任 + optimized/rowClick 等细节）：https://marmelab.com/react-admin/Datagrid.html [官方文档]
- npm react-admin（版本号 5.15.7 锚定）：https://www.npmjs.com/package/react-admin [官方文档]
- 文档索引：https://marmelab.com/react-admin/documentation.html [官方文档]
- DataProviders 指南（QueryClient 覆盖/withLifecycleCallbacks/查询取消/离线）：https://marmelab.com/react-admin/DataProviders.html [官方文档]
- EE 官网（模块全景，18 模块清单）：https://react-admin-ee.marmelab.com/ [官方文档]
- ra-realtime EE 文档（5.4.0 / react-admin ≥ 5.9.0 / hooks/UI/锁协作）：https://react-admin-ee.marmelab.com/documentation/ra-realtime [官方文档]
- Inputs 参考（通用 props/readOnly vs disabled/format-parse/联动/自定义 Input）：https://marmelab.com/react-admin/Inputs.html [官方文档]
- Validation 参考（四轨校验/内建校验器/服务端校验）：https://marmelab.com/react-admin/Validation.html [官方文档]
- Authentication（requireAuth/disableAuthentication/OAuth handleCallback/Refresh Token 装饰器）：https://marmelab.com/react-admin/Authentication.html [官方文档]
- Authorization（canAccess 推荐轨/内置访问控制/useCanAccess/Permissions 旧轨）：https://marmelab.com/react-admin/Permissions.html [官方文档]
- CanAccess 组件参考（开源核心铁证）：https://marmelab.com/react-admin/CanAccess.html [官方文档]
- Actions（Query/Mutation hooks/isPending 语义/三 mutation 模式/queryKey）：https://marmelab.com/react-admin/Actions.html [官方文档]
- Theming（sx/theme/5 主题/3 布局/定制 prop 表）：https://marmelab.com/react-admin/Theming.html [官方文档]
- ra-ai EE 文档（5.5.0 / DataProvider AI 方法 generateContent+suggestCompletion / SmartRichTextInput / FormFillerButton）：https://react-admin-ee.marmelab.com/documentation/ra-ai [官方文档]
- ra-datagrid-ag EE 文档（7.2.0 / DatagridAG vs DatagridAGClient / ag-grid v33+ 迁移 / v6 BREAKING / Enterprise 特性）：https://react-admin-ee.marmelab.com/documentation/ra-datagrid-ag [官方文档]
- ReferenceInput 参考（getList+getMany 双查询/ChoicesContext/通用 props 归子组件/enableGetChoices 懒加载/filterToQuery/onCreate 现场创建/offline/Filter label 特例/recordRepresentation）：https://marmelab.com/react-admin/ReferenceInput.html [官方文档]
- ReferenceArrayInput 参考（默认 AutocompleteArrayInput/子组件谱系 SelectArray·DualList·CheckboxGroup·DataTableInput 多列对比/useCreate returnPromise 自动选中）：https://marmelab.com/react-admin/ReferenceArrayInput.html [官方文档]
- ListTutorial（List 架构链 useGetList→ListContext→useListController→ListBase→List/controller 内建行为/emptyWhileLoading/WithListContext/预排序链接全参数/自定义分页 hasPreviousPage·hasNextPage）：https://marmelab.com/react-admin/ListTutorial.html [官方文档]
- FilteringTutorial（四种过滤 UI/filters 渲染两处/alwaysOn 与 defaultValue 互斥/FilterList 侧栏/FilterLiveSearch/filter 存 URL JSON/操作符无官方约定/SavedQueriesList/FilterLiveForm debounce/StackedFilters·Search 属 EE）：https://marmelab.com/react-admin/FilteringTutorial.html [官方文档]
- [模型经验]：坑点 1/2/3/5/6 的故障模式、开源版权限分层模式、映射层策略、i18n/布局/realtime 要点——适用 react-admin 4.x/5.x
- 法则条款来源：corpus/react/react-admin/elicited/10-laws.md（法则化萃取）

## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| 表格组件为 `<Datagrid>` + `<TextField>` 列，或（第一轮）教程 DataTable 是否取代 Datagrid 存疑 | v5.8.0 引入 `<DataTable>` 为**推荐继任者**；`<Datagrid>` 向后兼容保留 + codemod（Datagrid.html + npm 5.15.7 双重锚定） | **双轨并存**：新代码 DataTable，存量 Datagrid 合法不强改；`optimized`/`bulkActionButtons` 等 Datagrid 细节继续有效 |
| authProvider 需 5+ 方法（含 getPermissions） | 最少 4 方法（login/logout/checkError/checkAuth），其余为扩展 | 采用文档：4 方法为必需底线 |
| 乐观更新需手动实现 | core 内建乐观更新 + 约 5s Undo | 采用文档 |
| realtime 可能为开源内置 | ra-realtime 属 EE（EE 功能清单） | 开源版方案改为 DIY：WS/SSE + queryClient 失效 |
| EE 具体模块与版本未锚定（缺口登记） | EE 18 模块全景 + ra-realtime 5.4.0（要求 react-admin ≥5.9.0）[官方 EE 文档](https://react-admin-ee.marmelab.com/documentation/ra-realtime) | 锚定：模块清单与 realtime 关键 API 入库；EE 细节用前查 EE 文档 |
| 版本号未锚定（第一轮） | 5.15.7（npm，2026-11-15） | 锚定 5.15.7，v5 系列 |
| **`<CanAccess>`/`useCanAccess` 属 EE，开源不可用**（v5 kb RA-7 原判定） | **开源核心**——`import { CanAccess } from 'react-admin'`（CanAccess.html + Permissions.html 双页铁证，2026-11-16）；EE 对应物是 @react-admin/ra-rbac（角色/组/通配符/显式 deny/record-level） | **修正 RA-7**：核心能力用 canAccess/useCanAccess/CanAccess；EE 分界改为 @react-admin/ra-* 包与 react-admin-ee 模块 |
| 校验可 Form 级与 Input 级同时配置 | 双轨 validate 互斥（react-hook-form 限制） | 新增 [RA-12]：四轨选一 |
| 服务端校验任何 mutation 模式下都回显 | 仅 pessimistic 模式生效 | 采用文档：需服务端字段校验的表单改 pessimistic [RA-12] |
| 速查表旧结论"嵌套结构别多包 SelectInput"（本 kb 此前误写） | 嵌套子组件正是官方定制方式（SelectInput 等均可作子组件），通用 props 传子组件 | 已修正速查表行；新增 [RA-13]（2026-11-17 ReferenceInput.html 锚定） |
| Filter 表单中 ReferenceInput 的 label 与 Edit/Create 同判无效 | Filter 特例：本体 label 用作过滤标签，子组件 label 独立 | 两处都设（坑点 20） |
| 过滤器 alwaysOn 与 defaultValue 可同用 | 技术限制互斥；默认值走 `<List filterDefaultValues>` | 新增 [RA-14]（2026-11-17 FilteringTutorial.html 锚定） |
| filter 操作符 `_gte`/`_lte` 等是官方约定 | 无官方后缀约定，demo 约定；后端不认须 DataProvider 转换 | 采用文档：后缀约定 + DataProvider 转换 |
