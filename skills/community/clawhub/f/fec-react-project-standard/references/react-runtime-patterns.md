# React runtime patterns

## 常用 UI 与状态模式

以下模式可与本 skill 其他章节（Hooks、状态管理、性能优化、错误处理）对照使用；**按业务复杂度与团队熟悉度选用**，避免为模式而模式。思路参考业界常见的 React 前端模式实践（如组件组合、复合组件、性能与无障碍等）。

### 组合优于继承

- 用**小颗粒子组件** + `children` / 显式 props 拼装界面，而不是在 React 中搭建类继承层次。
- 示例：`Card` + `CardHeader` + `CardBody`，由使用方组合，而不是一个巨型 `Card` 用大量布尔 props 分支。

### 复合组件（Compound Components）

- 根组件通过 **Context** 向子组件提供内部状态（如当前 Tab、打开/关闭）。
- 子组件在 `useContext` 为空时**抛错或断言**，明确「必须在 Provider 树内使用」。
- API 表面保持可读：`<Tabs><TabList><Tab /></TabList></Tabs>`。

### Render Props / 函数子

- 适用：封装**数据获取与三态**（loading / error / data），把**渲染决策**交给父级。
- 与 **自定义 Hook** 二选一即可：多数场景 `useXxx()` + 普通组件更直观；仅在需要强约束「同层渲染逻辑」时保留 Render Props。

### Context + useReducer

- 适合**中等复杂度、多子树共享**的客户端状态，且更新可归约为明确 `action`。
- 避免把高频变化的大对象塞进顶层 Context；服务端数据仍优先 **React Query / SWR**。
- 大型全局业务状态继续用仓库已选的 **Zustand / Redux Toolkit / Jotai**。

### 表单

- 受控字段 + 校验错误对象是一类可行实现；中大型表单优先 **React Hook Form**（或 Formik）+ **Zod**，复杂表单值、DTO 和校验类型契约分流到 `fec-typescript-project-standard`。
- 避免单组件内巨型 `useState` 表单对象与重复校验逻辑，可拆字段子组件或抽 `useFormSchema`。

### Error Boundary

- **不要**在业务代码中手写 React **类组件**形式的 Error Boundary；统一使用 **`react-error-boundary`**（或团队认可的同类库）在**模块边界**兜底渲染失败（与本章「错误处理」、`error-handling.md` 一致）。
- 用 `FallbackComponent` 与 `resetErrorBoundary` 提供「重试」；**日志上报**放在库的 **`onError`**（等回调）中，生产代码避免长期依赖 `console.log`（见 TypeScript 规则）。


### 动画与过渡

- 列表进出场可用 **Framer Motion** 的 `AnimatePresence` + `key`，或 CSS `transition`；注意减少布局抖动与 `prefers-reduced-motion`（与无障碍策略一致时）。

### 无障碍与焦点

- 自定义下拉、标签页等：**`role` / `aria-*`**、**方向键 / Enter / Escape** 行为与焦点环可见。
- 弹窗：打开时将焦点移入对话框，关闭时**恢复**触发元素焦点；可用 **`focus-trap-react`** 或类似方案，与 `fec-accessibility-check` skill 互补。

### Next.js 与服务端组件

- **App Router、Server Components、服务端数据获取与缓存**见 **`fec-nextjs-project-standard`**；客户端交互模式仍以本章与 Hooks 规范为准。

---


## Hooks 设计模式

### 适合抽为自定义 Hook 的场景

- 数据获取与三态管理
- 表单状态逻辑
- 分页、筛选、排序编排
- 事件监听与副作用清理
- 可在多个组件复用的交互逻辑

### 推荐原则

- 统一使用 `use` 前缀命名
- 返回对象而非数组，方便按需解构，增强可读性和扩展性
- 状态和行为封装在一起
- Hook 内部处理 `loading / error / data`
- 对外暴露清晰的最小接口，不泄漏无关内部细节

### 示例

```tsx
function useUserList(params: QueryParams) {
  const [data, setData] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getUserList(params);
      setData(res.list);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { data, loading, error, refetch: fetch };
}
```

### Hook 使用原则

- `useEffect` 必须有正确依赖和清理逻辑
- `useMemo` / `useCallback` 不要滥用，只有在稳定引用确实重要时再加
- 不在条件分支或循环中调用 hooks
- 已引入 React Query / SWR 时，数据请求优先走这些库，而不是自己重复造一套缓存层

---

## 路由组织

### 推荐方式

- 路由配置集中管理
- 路径常量化
- 页面组件按需懒加载
- 权限控制放在 guard 层，而不是散落在页面组件内
- 分页、筛选、排序等 URL 驱动状态优先与地址栏同步

### 示例

```tsx
const routes: RouteObject[] = [
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "users", element: <UserListPage /> },
      { path: "users/:id", element: <UserDetailPage /> },
      { path: "settings", element: <SettingsPage /> },
    ],
  },
  { path: "/login", element: <LoginPage /> },
  { path: "*", element: <NotFoundPage /> },
];
```

```tsx
const UserListPage = lazy(() => import("@/pages/UserList/UserListPage"));

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}
```

---

## 状态管理选型

| 状态类型           | 推荐方案                                          |
| ------------------ | ------------------------------------------------- |
| 组件内临时 UI 状态 | `useState` / `useReducer`                         |
| 跨组件共享业务状态 | Zustand / Redux Toolkit / Jotai（按仓库实际选择） |
| 服务端数据缓存     | React Query / SWR                                 |
| URL 驱动状态       | 路由参数 / `useSearchParams`                      |
| 表单状态           | React Hook Form / Formik                          |

### 核心原则

- 就近管理：状态尽量放在最近的公共祖先
- 单一数据源：同一份数据不要维护多份
- 派生优于同步：可计算值优先在渲染期计算
- 服务端数据优先交给请求库管理，不手动塞进全局 store
- 不要因为“以后可能会用到”就把局部状态提前升级为全局状态

---

## API 层规范

### 设计原则

- 请求基础设施集中在 `services/`
- 业务 API 按 feature 拆分，而不是全部堆在一个文件
- 请求参数和响应结果都应有明确类型
- 认证、错误格式化、通用拦截放在请求层统一处理
- 页面和组件不要直接散落拼接请求细节

### 示例

```ts
// services/request.ts
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

request.interceptors.response.use(
  (res) => res.data,
  (error) => {
    if (error.response?.status === 401) {
      redirectToLogin();
    }
    return Promise.reject(normalizeError(error));
  },
);
```

```ts
// features/user/api.ts
export function getUserList(
  params: UserQueryParams,
): Promise<PageResult<User>> {
  return request.get("/users", { params });
}

export function updateUser(id: string, data: UpdateUserDTO): Promise<User> {
  return request.put(`/users/${id}`, data);
}
```

---

## 错误处理

### 必须覆盖的状态

- Loading
- Error
- Empty
- Data

### 推荐做法

- 关键功能模块使用 Error Boundary 包裹，避免局部异常导致全页白屏
- 异步请求失败时必须给用户可见反馈
- 重要操作提供重试能力
- 不要吞错，不写空 `catch`

### 示例（`react-error-boundary`，函数式 Fallback）

```tsx
import { ErrorBoundary } from "react-error-boundary";

function ModuleErrorFallback({
  resetErrorBoundary,
}: {
  resetErrorBoundary: () => void;
}) {
  return (
    <div>
      模块加载失败
      <button type="button" onClick={resetErrorBoundary}>
        重试
      </button>
    </div>
  );
}

export function UserDashboardSection() {
  return (
    <ErrorBoundary FallbackComponent={ModuleErrorFallback}>
      <UserDashboard />
    </ErrorBoundary>
  );
}
```

---

## Suspense 与懒加载

适用场景：

- 路由级页面
- 图表、富文本编辑器、地图、重型表格等大体积组件
- 初始化成本较高的模块

示例：

```tsx
const HeavyChart = lazy(() => import("./components/HeavyChart"));

function Dashboard() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart data={chartData} />
    </Suspense>
  );
}
```

建议：

- 路由级优先 `lazy + Suspense`
- `fallback` 优先使用 Skeleton 或更贴近内容的占位态，而不是纯 spinner

---

