# Vue 3 composables and routing patterns

## Composables specification

### Design principles

- Named with `use` prefix
- Use objects as return values and clearly mark the type
- Internal processing loading / error / data tri-state
-Support parameter responsiveness (accepts `Ref` or getter)
- Library level composable to clarify whether the parameter supports normal values, `Ref`, `computed` or getter, and parse the latest value inside the side effect

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

### Composable usage principles

- Return a `readonly` reference to prevent accidental modification by outsiders
- In data request scenarios, libraries such as VueQuery / VueUse are preferred (if the project has been introduced)
- Clean up timers, event listeners and other side effects in `onUnmounted`
- Avoid directly manipulating DOM in composable
- Read-only inputs accept normal values, refs, computed or getters; inputs that require bidirectional writing only accept writable refs or explicit setters.
- If the parameter itself is a callback, comparator or predicate, do not design it as a getter type input, otherwise the business function may be mistakenly called during parsing.

### Vue Router / Pinia / Test common boundaries

- Changes in routing parameters will not recreate the same routing component; data that relies on `route.params` must watch clear fields and handle cancellation and race conditions.
- Avoid old-style `next()` multi-branch repeated calls in navigation guards; give priority to returning `false`, redirecting objects or throwing handleable errors.
- Use `storeToRefs` when destructuring the Pinia store will lose responsiveness; the setup store must return state, getters and actions that need to be tracked externally.
- UI temporary status, form input, and pop-up window switches do not enter the global store; URL query, server-side cache, and local component status are returned to their respective places first.
- Vue Test Utils tests prioritize user-visible behavior and do not use snapshots as the only proof; asynchronous updates use `await`, `flushPromises` or the waiting method recommended by the framework.
- When testing using Pinia, Router, Teleport, Suspense, async setup or `defineAsyncComponent`, explicitly install the plugin in the test fixture, mount the target container and wait for async to stabilize.

## Slots and Provide/Inject

### Slots

- Use `<slot>` to achieve component composition instead of too many props
- Named slots are used for explicit layout areas
- Scope slot passes data to parent component for custom rendering

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

- For context sharing across multiple levels (topics, configurations, permissions)
- Provide InjectionKey to ensure type safety
- Do not use provide/inject instead of props to pass direct parent-child data

```typescript
// keys.ts
export const ThemeKey: InjectionKey<Ref<Theme>> = Symbol("theme");

// Provider.vue
provide(ThemeKey, theme);

// Consumer.vue
const theme = inject(ThemeKey);
```

## Routing specifications

### Routing organization

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

### Routing principles

- Centralized management of routing configuration, each route must have a `name`
- Page components are loaded on demand using dynamic `import()`
- Permission control uses route guard (`beforeEach`) instead of judging within each page
- URL parameters (pagination, filtering, sorting) and routing status are synchronized

```typescript
// Navigation guard
router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return { name: "Login", query: { redirect: to.fullPath } };
  }
});
```

