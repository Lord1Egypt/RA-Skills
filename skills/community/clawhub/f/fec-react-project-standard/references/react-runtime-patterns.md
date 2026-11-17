# React runtime patterns

## Common UI and status mode

The following patterns can be used in comparison with other chapters of this skill (Hooks, state management, performance optimization, error handling); **Select based on business complexity and team familiarity** to avoid patterns for pattern's sake. The ideas refer to common React front-end pattern practices in the industry (such as component combination, composite components, performance and accessibility, etc.).

### Composition is better than inheritance

- Use **small subcomponents** + `children` / explicit props to assemble the interface instead of building a class inheritance hierarchy in React.
- Example: `Card` + `CardHeader` + `CardBody`, composed by the consumer, rather than one giant `Card` branched with a lot of boolean props.

### Compound Components

- The root component provides internal state (such as current Tab, open/closed) to child components through **Context**.
- The subcomponent **throws an error or asserts** when `useContext` is empty, making it clear that it "must be used within the Provider tree".
- API surfaces remain readable: `<Tabs><TabList><Tab /></TabList></Tabs>`.

### Render Props/Functionator

- Applicable: Encapsulate **data acquisition and three-state** (loading / error / data), and hand over **rendering decision** to the parent.
- Choose one of the two with **Custom Hook**: `useXxx()` + ordinary components are more intuitive in most scenarios; only keep Render Props when strong constraints on "same-layer rendering logic" are required.

### Context + useReducer

- Suitable for **moderate complexity, multi-subtree sharing** client state, and updates can be reduced to explicit `action`.
- Avoid stuffing large objects that change frequently into the top-level Context; server-side data still takes priority **React Query / SWR**.
- Large global business status continues to use the **Zusand / Redux Toolkit / Jotai** selected by the warehouse.

### Form

- Controlled fields + validation error objects are a feasible implementation; medium and large forms are given priority **React Hook Form** (or Formik) + **Zod**, and complex form values, DTO and validation type contracts are offloaded to `fec-typescript-project-standard`.
- Avoid huge `useState` form objects and repeated validation logic in a single component, detachable field subcomponents or extract `useFormSchema`.

### Error Boundary

- **Don't** handwrite Error Boundary in the form of React **class component** in business code; uniformly use **`react-error-boundary`** (or a similar library recognized by the team) to render failure at the **module boundary** (consistent with "Error Handling" and `error-handling.md` in this chapter).
- Use `FallbackComponent` and `resetErrorBoundary` to provide "retry"; **log reporting** is placed in the library's **`onError`** (waiting for callbacks), and production code avoids long-term dependence on `console.log` (see TypeScript rules).


### Animation and Transition

- List entry and exit can be done using **Framer Motion**'s `AnimatePresence` + `key`, or CSS `transition`; note that reduced layout jitter and `prefers-reduced-motion` (when consistent with accessibility policies).

### Accessibility and Focus

- Customized drop-downs, tabs, etc.: **`role` / `aria-*`**, **Direction keys / Enter / Escape** Behavior and focus rings are visible.
- Pop-up window: Move the focus into the dialog box when it is opened, and **restore** when it is closed to trigger the element focus; **`focus-trap-react`** or similar solutions can be used to complement the `fec-accessibility-check` skill.

### Next.js and server-side components

- **App Router, Server Components, server-side data acquisition and caching** see **`fec-nextjs-project-standard`**; the client interaction mode is still subject to this chapter and the Hooks specification.

---


## Hooks design pattern

### Suitable for scenarios where custom Hooks are drawn

- Data acquisition and three-state management
- Form status logic
- Paging, filtering, sorting and arrangement
- Event monitoring and side effect cleanup
- Interaction logic that can be reused in multiple components

### Recommended principles

- Uniformly use `use` prefix naming
- Return objects instead of arrays to facilitate on-demand destructuring and enhance readability and scalability
- State and behavior are encapsulated together
- Hook internal processing `loading/error/data`
- Expose a clear minimal interface to the outside world without leaking irrelevant internal details

### Example

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

### Hook usage principles

- `useEffect` must have correct dependencies and cleanup logic
- `useMemo` / `useCallback` Don’t overuse it, add it only when stable references are really important
- Don't call hooks in conditional branches or loops
- When React Query / SWR has been introduced, data requests go through these libraries first instead of recreating a cache layer yourself.

---

## Routing organization

### Recommended method

- Centralized management of routing configuration
- Path constantization
- Lazy loading of page components on demand
- Permission control is placed in the guard layer instead of scattered within the page components
- Paging, filtering, sorting, etc. URL driver status is synchronized with the address bar first

### Example

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

## Status management selection

| Status type | Recommended solution |
| ------------------ | ------------------------------------------------- |
| Temporary UI state within the component | `useState` / `useReducer` |
| Sharing business status across components | Zustand / Redux Toolkit / Jotai (actual selection by warehouse) |
| Server-side data caching | React Query / SWR |
| URL driver status | Route parameters / `useSearchParams` |
| Form State | React Hook Form / Formik |

### Core Principles

- Proximity management: try to place the state on the nearest common ancestor
-Single data source: Do not maintain multiple copies of the same data
- Derived over synchronized: computable values are calculated first at render time
- The server-side data is given priority to the request library management and is not manually inserted into the global store.
- Don’t upgrade local state to global state in advance just because it “may be used in the future”

---

## API layer specification

### Design principles

- Request infrastructure is centralized in `services/`
-Business APIs are split by feature instead of stacking them all in one file
- Both request parameters and response results should have clear types
- Authentication, error formatting, and universal interception are handled uniformly at the request layer
- Do not directly scatter splicing request details on pages and components

### Example

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

## Error handling

### Status that must be overridden

- Loading
- Error
- Empty
- Data

### Recommended practices

- Use Error Boundary to wrap key functional modules to avoid local exceptions causing a full-page white screen
- Visible feedback must be given to the user when an asynchronous request fails
- Provide retry capability for important operations
- Don’t catch mistakes, don’t write empty `catch`

### Example (`react-error-boundary`, functional Fallback)

```tsx
import { ErrorBoundary } from "react-error-boundary";

function ModuleErrorFallback({
  resetErrorBoundary,
}: {
  resetErrorBoundary: () => void;
}) {
  return (
    <div>
      Module loading failed
      <button type="button" onClick={resetErrorBoundary}>
        Try again
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

## Suspense and lazy loading

Applicable scenarios:

- Routing level page
- Large components such as charts, rich text editors, maps, heavy tables, etc.
- Modules with higher initialization costs

Example:

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

Suggestions:

- Route level priority `lazy + Suspense`
- `fallback` gives priority to using Skeleton or a placeholder state closer to the content instead of a pure spinner

---

