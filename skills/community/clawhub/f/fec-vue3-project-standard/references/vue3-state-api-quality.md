# Vue 3 state, API, and quality patterns

## Status Management (Pinia)

| Status type | Recommended solution |
| ------------------ | ----------------------------- |
| Temporary UI state within the component | `ref` / `reactive` |
| Sharing business status across components | Pinia store |
| Server-side data cache | VueQuery / Custom composable |
| URL driver status | Route parameters / `useRoute().query` |
| Form Status | VeeValidate / FormKit |

### Pinia Store Specifications

Using Composition API style (`setup store`):

```typescript
// stores/authStore.ts
export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem("token"));

  const isLoggedIn = computed(() => !!token.value);

  async function login(credentials: LoginParams) {
    const res = await authApi.login(credentials);
    user.value = res.user;
    token.value = res.token;
    localStorage.setItem("token", res.token);
  }

  function logout() {
    user.value = null;
    token.value = null;
    localStorage.removeItem("token");
  }

  return { user: readonly(user), isLoggedIn, login, logout };
});
```

### Store Principles

- Each store has a single responsibility and is split by area.
- Expose the status of `readonly` to the outside world and modify it through action
- Do not store UI temporary states (modal switches, form inputs, etc.) in the store
- Server-side data is first managed by the request library rather than manually stored in the store

## API layer specification

### Request instance

```typescript
// services/request.ts
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

request.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

request.interceptors.response.use(
  (res) => res.data,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      router.push({ name: "Login" });
    }
    return Promise.reject(normalizeError(error));
  },
);
```

### API functions

```typescript
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

- API functions are organized by feature instead of all being piled in one file
- Request parameters and responses have type constraints
- The interceptor handles authentication and error formatting uniformly

## Error handling

### Global error capture

```typescript
// main.ts
app.config.errorHandler = (err, instance, info) => {
  reportError(err, { component: instance?.$options.name, info });
};
```

### Component level errors

- Use `onErrorCaptured` to capture child component errors in the parent component
- Failed data requests must have user-visible prompts and retry mechanisms
- Don't swallow errors (empty catch block)

## Custom directive

```typescript
// directives/vPermission.ts
export const vPermission: Directive<HTMLElement, string> = {
  mounted(el, binding) {
    const authStore = useAuthStore();
    if (!authStore.hasPermission(binding.value)) {
      el.parentNode?.removeChild(el);
    }
  },
};
```

- The directive only handles operations at the DOM level
- Do not put business logic in instructions
- Implement the `updated` hook when responsive updates are required

## Style specification

- Use `<style scoped>` to isolate styles
- Depth selector uses `:deep()` instead of the deprecated `::v-deep`
- Be consistent with the existing style system of the project
- Dynamic styles preferentially use `:class` / `:style` binding
- Complex theme switching using CSS variables
- Theme/global variables are managed through CSS variables or Token

## Test specifications

### Must be tested

- Core interaction behaviors (click, input, submit)
- Conditional rendering (loading/error/empty/data)
- Emits trigger and payload
- Return value of key composables
- Pinia store actions and getters

### Test style

```typescript
describe("UserForm", () => {
  it("should emit submit with valid data", async () => {
    const wrapper = mount(UserForm);

    await wrapper.find('[data-testid="username"]').setValue("test");
    await wrapper.find("form").trigger("submit");

    expect(wrapper.emitted("submit")?.[0]).toEqual([{ username: "test" }]);
  });

  it("should show validation error on empty submit", async () => {
    const wrapper = mount(UserForm);
    await wrapper.find("form").trigger("submit");
    expect(wrapper.text()).toContain("Username cannot be empty");
  });
});
```

### Store Test

```typescript
describe("authStore", () => {
  beforeEach(() => setActivePinia(createPinia()));

  it("should login and set user", async () => {
    const store = useAuthStore();
    await store.login({ username: "admin", password: "pass" });
    expect(store.isLoggedIn).toBe(true);
  });
});
```


## Anti-pattern

- Inline large sections of business logic in template-driven components
- Used wide range watcher instead of computed
- The event payload is unclear
- Mix raw API calls directly into pure presentation components
- ref and props have no type constraints
- Use `watch` + manual assignment to simulate computed
- Mixing unrelated responsibilities into a component
- Use large-scale global style coverage to solve local UI problems
- Push all status to Pinia store instead of managing it nearby
- Put business coupling components in `components/`
- Import directly from the deep path inside the feature, bypassing `index.ts`

## Output checklist

- [ ] The file structure is consistent with the project convention (pages/features/components are separated)
- [ ] Use `<script setup lang="ts">`
- [ ] Props / Emits type complete
- [ ] Whether explanatory comments should be given priority in Chinese and to the point
- [ ] Reusable logic has been extracted to composable
- [ ] Loading / Error / Empty status have been processed
- [ ] Routing components are loaded using dynamic import
- [ ] Reasonable status management plan (proximity principle)
- [ ] API calls have type constraints and unified error handling
- [ ] styles use scoped isolation
- [ ] Key behaviors are covered by tests
