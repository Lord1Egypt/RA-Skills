# 前端开发指南

## 目录
- [前端工程化](#前端工程化)
- [React深度实践](#react深度实践)
- [Vue深度实践](#vue深度实践)
- [性能优化](#性能优化)
- [状态管理](#状态管理)
- [组件设计模式](#组件设计模式)
- [前端测试](#前端测试)
- [前端安全](#前端安全)

## 前端工程化

### 项目脚手架

#### React + Vite
```bash
# 创建项目
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# 目录结构
src/
├── assets/          # 静态资源
├── components/      # 通用组件
│   ├── common/     # UI组件（Button、Input等）
│   └── business/   # 业务组件（UserCard、OrderList等）
├── pages/          # 页面组件
├── hooks/          # 自定义Hooks
├── services/       # API服务
├── stores/         # 状态管理
├── utils/          # 工具函数
├── types/          # TypeScript类型
├── constants/      # 常量
├── config/         # 配置
└── styles/         # 全局样式
```

#### Vue 3 + Vite
```bash
# 创建项目
npm create vue@latest my-app
cd my-app
npm install

# 目录结构
src/
├── assets/          # 静态资源
├── components/      # 组件
├── views/           # 页面视图
├── composables/     # 组合式函数
├── stores/          # Pinia状态管理
├── router/          # 路由配置
├── api/             # API服务
├── utils/           # 工具函数
└── styles/          # 全局样式
```

### 代码规范配置

#### ESLint + Prettier
```json
// .eslintrc.cjs
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  rules: {
    'react/react-in-jsx-scope': 'off',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
  },
};
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "arrowParens": "avoid"
}
```

### 环境变量管理
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL),
  },
});
```

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App
```

## React深度实践

### Hooks最佳实践

#### 自定义Hook封装
```typescript
import { useState, useEffect, useCallback } from 'react';

interface UseAsyncResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useAsync<T>(
  asyncFn: () => Promise<T>,
  dependencies: any[] = []
): UseAsyncResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await asyncFn();
      setData(result);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [asyncFn]);

  useEffect(() => {
    fetchData();
  }, [fetchData, ...dependencies]);

  return { data, loading, error, refetch: fetchData };
}
```

#### 使用示例
```typescript
// 获取用户数据
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useAsync(
    () => fetchUser(userId),
    [userId]
  );

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### 组件设计模式

#### 容器组件 vs 展示组件
```typescript
// 展示组件（纯UI，无业务逻辑）
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
  onClick?: () => void;
}

export function UserCard({ name, email, avatar, onClick }: UserCardProps) {
  return (
    <div className="user-card" onClick={onClick}>
      <img src={avatar || '/default-avatar.png'} alt={name} />
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
}

// 容器组件（业务逻辑，数据获取）
export function UserCardContainer({ userId }: { userId: string }) {
  const { data: user, loading } = useAsync(() => fetchUser(userId), [userId]);

  if (loading) return <Skeleton />;
  if (!user) return null;

  const handleClick = () => {
    router.push(`/users/${userId}`);
  };

  return <UserCard {...user} onClick={handleClick} />;
}
```

#### 高阶组件（HOC）
```typescript
// 高阶组件：添加加载状态
function withLoading<P extends object>(
  Component: React.ComponentType<P>
): React.FC<P & { loading: boolean }> {
  return ({ loading, ...props }) => {
    if (loading) {
      return <Spinner />;
    }
    return <Component {...(props as P)} />;
  };
}

// 使用
const UserList = withLoading(({ users }: { users: User[] }) => {
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} {...user} />
      ))}
    </div>
  );
});
```

### Context API使用

```typescript
// 1. 创建Context
interface AuthContextType {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = React.createContext<AuthContextType | null>(null);

// 2. 提供Provider
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: LoginCredentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// 3. 创建自定义Hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// 4. 使用
function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## Vue深度实践

### Composition API

#### 组合式函数
```typescript
// composables/useUser.ts
import { ref, computed } from 'vue';
import { fetchUser as apiFetchUser } from '@/api/user';

export function useUser(userId: Ref<string>) {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const fetchUser = async () => {
    try {
      loading.value = true;
      error.value = null;
      user.value = await apiFetchUser(userId.value);
    } catch (err) {
      error.value = err as Error;
    } finally {
      loading.value = false;
    }
  };

  // 自动获取
  watch(userId, fetchUser, { immediate: true });

  return {
    user,
    loading,
    error,
    fetchUser,
    userName: computed(() => user.value?.name ?? ''),
  };
}
```

#### 使用示例
```vue
<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <div v-else>
      <h1>{{ user.name }}</h1>
      <p>{{ user.email }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useUser } from '@/composables/useUser';

const userId = ref('123');
const { user, loading, error } = useUser(userId);
</script>
```

### Pinia状态管理

```typescript
// stores/user.ts
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null as User | null,
    token: localStorage.getItem('token') || '',
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userName: (state) => state.currentUser?.name ?? '',
  },

  actions: {
    async login(credentials: LoginCredentials) {
      const { user, token } = await authService.login(credentials);
      this.currentUser = user;
      this.token = token;
      localStorage.setItem('token', token);
    },

    logout() {
      this.currentUser = null;
      this.token = '';
      localStorage.removeItem('token');
    },
  },
});
```

## 性能优化

### 代码分割

#### 路由懒加载
```typescript
// React Router
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

#### Vue Router懒加载
```typescript
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue'),
  },
  {
    path: '/settings',
    component: () => import('@/views/Settings.vue'),
  },
];
```

### 组件优化

#### React.memo
```typescript
export const ExpensiveComponent = React.memo(
  ({ data, onUpdate }: { data: Item[]; onUpdate: (item: Item) => void }) => {
    return (
      <div>
        {data.map(item => (
          <div key={item.id}>{item.name}</div>
        ))}
      </div>
    );
  },
  (prevProps, nextProps) => {
    // 自定义比较逻辑
    return prevProps.data.length === nextProps.data.length;
  }
);
```

#### Vue computed缓存
```vue
<script setup lang="ts">
import { computed } from 'vue';

const items = ref<Item[]>([]);

// 计算属性会自动缓存
const expensiveValue = computed(() => {
  return items.value.reduce((sum, item) => sum + item.value, 0);
});
</script>
```

### 资源优化

#### 图片懒加载
```typescript
import { LazyLoadImage } from 'react-lazy-load-image-component';

<LazyLoadImage
  src={imageSrc}
  alt="Description"
  effect="blur"
  width={300}
  height={200}
/>
```

#### WebP格式支持
```typescript
// 图片组件
function OptimizedImage({ src, alt, ...props }: ImageProps) {
  const webpSrc = src.replace(/\.(jpg|png)$/, '.webp');

  return (
    <picture>
      <source srcSet={webpSrc} type="image/webp" />
      <img src={src} alt={alt} {...props} loading="lazy" />
    </picture>
  );
}
```

## 状态管理

### Redux Toolkit

```typescript
// store/userSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { userService } from '@/services/user';

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string) => {
    return await userService.getUser(userId);
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: {
    user: null,
    loading: false,
    error: null,
  } as UserState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});
```

### Zustand（轻量级）

```typescript
import { create } from 'zustand';

interface UserStore {
  user: User | null;
  loading: boolean;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  loading: false,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));
```

## 前端测试

### 单元测试（Jest + React Testing Library）

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
  };

  it('renders user information', () => {
    render(<UserCard {...mockUser} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<UserCard {...mockUser} onClick={handleClick} />);
    fireEvent.click(screen.getByText('John Doe'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### E2E测试（Playwright）

```typescript
import { test, expect } from '@playwright/test';

test('user login flow', async ({ page }) => {
  await page.goto('http://localhost:3000/login');

  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

## 前端安全

### XSS防护
```typescript
// 使用DOMPurify清理HTML
import DOMPurify from 'dompurify';

function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html);
}

// React自动转义，但dangerouslySetInnerHTML需要谨慎
function renderUserContent(content: string) {
  return (
    <div
      dangerouslySetInnerHTML={{ __html: sanitizeHtml(content) }}
    />
  );
}
```

### CSRF防护
```typescript
// axios拦截器添加CSRF Token
axios.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrf_token');
  if (csrfToken) {
    config.headers['X-CSRF-Token'] = csrfToken;
  }
  return config;
});
```

### 敏感信息保护
```typescript
// 避免在前端存储敏感信息
// ❌ 错误：localStorage存储Token
localStorage.setItem('token', token);

// ✅ 正确：使用HttpOnly Cookie
// Token由后端设置HttpOnly Cookie，前端无法访问

// ✅ 或使用短期Token + Refresh Token机制
```
