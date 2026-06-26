# Vue 3 state, API, and quality patterns

## 状态管理（Pinia）

| 状态类型           | 推荐方案                      |
| ------------------ | ----------------------------- |
| 组件内临时 UI 状态 | `ref` / `reactive`            |
| 跨组件共享业务状态 | Pinia store                   |
| 服务端数据缓存     | VueQuery / 自定义 composable  |
| URL 驱动状态       | 路由参数 / `useRoute().query` |
| 表单状态           | VeeValidate / FormKit         |

### Pinia Store 规范

使用 Composition API 风格（`setup store`）：

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

### Store 原则

- 每个 store 职责单一，按领域拆分
- 对外暴露 `readonly` 的状态，通过 action 修改
- 不要在 store 中存放 UI 临时状态（modal 开关、表单输入等）
- 服务端数据优先用请求库管理，而非手动存入 store

## API 层规范

### 请求实例

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

### API 函数

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

- API 函数按 feature 组织，而非全部堆在一个文件
- 请求参数和响应都有类型约束
- 拦截器统一处理认证、错误格式化

## 错误处理

### 全局错误捕获

```typescript
// main.ts
app.config.errorHandler = (err, instance, info) => {
  reportError(err, { component: instance?.$options.name, info });
};
```

### 组件级错误

- 使用 `onErrorCaptured` 在父组件中捕获子组件错误
- 数据请求失败需有用户可见的提示和重试机制
- 不要吞掉错误（空 catch 块）

## 自定义指令

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

- 指令只处理 DOM 层面的操作
- 业务逻辑不要放在指令中
- 需要响应式更新时实现 `updated` 钩子

## 样式规范

- 使用 `<style scoped>` 隔离样式
- 深度选择器使用 `:deep()` 而非已废弃的 `::v-deep`
- 与项目现有样式体系保持一致
- 动态样式优先使用 `:class` / `:style` 绑定
- 复杂主题切换使用 CSS 变量
- 主题/全局变量通过 CSS 变量或 Token 管理

## 测试规范

### 必须测试

- 核心交互行为（点击、输入、提交）
- 条件渲染（loading / error / empty / data）
- Emits 的触发和 payload
- 关键 composables 的返回值
- Pinia store 的 action 和 getter

### 测试风格

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
    expect(wrapper.text()).toContain("用户名不能为空");
  });
});
```

### Store 测试

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


## 反模式

- 在模板驱动组件中内联大段业务逻辑
- 本该用 computed 却使用大范围 watcher
- 事件 payload 不明确
- 在纯展示组件中直接混入原始 API 调用
- ref 和 props 没有类型约束
- 用 `watch` + 手动赋值模拟 computed
- 在一个组件中混入无关职责
- 用大范围全局样式覆盖去解决局部 UI 问题
- 将所有状态推入 Pinia store，而非就近管理
- 在 `components/` 中放业务耦合组件
- 直接从 feature 内部深层路径导入，绕过 `index.ts`

## 输出检查清单

- [ ] 文件结构与项目约定一致（pages / features / components 分离）
- [ ] 使用 `<script setup lang="ts">`
- [ ] Props / Emits 类型完整
- [ ] 解释性注释是否优先使用中文且点到要害
- [ ] 可复用逻辑已提取到 composable
- [ ] Loading / Error / Empty 状态均已处理
- [ ] 路由组件使用动态 import 加载
- [ ] 状态管理方案合理（就近原则）
- [ ] API 调用有类型约束和统一错误处理
- [ ] 样式使用 scoped 隔离
- [ ] 关键行为有测试覆盖
