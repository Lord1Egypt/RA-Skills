# Vue 3 composables and routing patterns

## Composables 规范

### 设计原则

- 以 `use` 前缀命名
- 返回值使用对象，明确标注类型
- 内部处理 loading / error / data 三态
- 支持参数响应式（接受 `Ref` 或 getter）
- 库级 composable 要明确参数是否支持普通值、`Ref`、`computed` 或 getter，并在副作用内部解析最新值

```typescript
export function useUserList(params: MaybeRef<QueryParams>) {
  const data = ref<User[]>([]);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  async function fetch() {
    loading.value = true;
    error.value = null;
    try {
      const res = await getUserList(toValue(params));
      data.value = res.list;
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  watchEffect(() => {
    fetch();
  });

  return {
    data: readonly(data),
    loading: readonly(loading),
    error: readonly(error),
    refetch: fetch,
  };
}
```

### Composable 使用原则

- 返回 `readonly` 引用防止外部意外修改
- 数据请求场景优先使用 VueQuery / VueUse 等库（如项目已引入）
- `onUnmounted` 中清理定时器、事件监听等副作用
- 避免在 composable 中直接操作 DOM
- 只读输入可接受普通值、ref、computed 或 getter；需要双向写入的输入只接受可写 ref 或明确的 setter。
- 如果参数本身是回调、比较器或 predicate，不要把它设计成 getter 型输入，否则解析时可能误调用业务函数。

### Vue Router / Pinia / 测试常见边界

- 路由参数变化不会重新创建同一个路由组件；依赖 `route.params` 的数据要 watch 明确字段，并处理取消和竞态。
- 导航守卫中避免旧式 `next()` 多分支重复调用；优先返回 `false`、重定向对象或抛出可处理错误。
- Pinia store 解构会丢失响应性时使用 `storeToRefs`；setup store 必须返回需要被外部追踪的 state、getter 和 action。
- UI 临时状态、表单输入、弹窗开关不进入全局 store；URL 查询、服务端缓存和本地组件状态先各归其位。
- Vue Test Utils 测试优先断言用户可见行为，不把快照作为唯一证明；异步更新使用 `await`、`flushPromises` 或框架推荐的等待方式。
- 测试使用 Pinia、Router、Teleport、Suspense、async setup 或 `defineAsyncComponent` 时，在测试夹具中显式安装插件、挂载目标容器并等待异步稳定。

## Slots 与 Provide/Inject

### Slots

- 用 `<slot>` 实现组件组合，而非过多 props
- 具名 slot 用于明确的布局区域
- 作用域 slot 传递数据给父组件自定义渲染

```vue
<template>
  <div class="card">
    <div class="card-header">
      <slot name="header">{{ title }}</slot>
    </div>
    <div class="card-body">
      <slot :data="processedData" :loading="loading" />
    </div>
  </div>
</template>
```

### Provide/Inject

- 用于跨多层级的上下文共享（主题、配置、权限）
- 提供 InjectionKey 保证类型安全
- 不要用 provide/inject 替代 props 传递直接父子数据

```typescript
// keys.ts
export const ThemeKey: InjectionKey<Ref<Theme>> = Symbol("theme");

// Provider.vue
provide(ThemeKey, theme);

// Consumer.vue
const theme = inject(ThemeKey);
```

## 路由规范

### 路由组织

```typescript
// app/router.ts
const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "Dashboard",
        component: () => import("@/pages/Dashboard/DashboardPage.vue"),
      },
      {
        path: "users",
        name: "UserList",
        component: () => import("@/pages/UserList/UserListPage.vue"),
      },
      {
        path: "users/:id",
        name: "UserDetail",
        component: () => import("@/pages/UserDetail/UserDetailPage.vue"),
      },
      {
        path: "settings",
        name: "Settings",
        component: () => import("@/pages/Settings/SettingsPage.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/pages/Login/LoginPage.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/pages/NotFound.vue"),
  },
];
```

### 路由原则

- 路由配置集中管理，每个路由必须有 `name`
- 页面组件使用动态 `import()` 按需加载
- 权限控制使用路由守卫（`beforeEach`），而非在每个页面内判断
- URL 参数（分页、筛选、排序）与路由状态同步

```typescript
// 导航守卫
router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return { name: "Login", query: { redirect: to.fullPath } };
  }
});
```

