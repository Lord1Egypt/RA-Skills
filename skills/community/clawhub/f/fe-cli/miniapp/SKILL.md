---
name: fe-cli-miniapp
description: >
  Scaffold a WeChat Mini Program project using Taro or uni-app framework.
  Features subpackage configuration, native API wrappers, subscription messages,
  and multi-platform build (WeChat, Alipay, etc.). Triggered as a sub-skill of fe-cli
  when user wants 小程序/微信小程序/Mini Program project.
---

# fe-cli-miniapp — Mini Program Scaffolding

## Workflow

### Step 1: Gather Options

1. **Framework**: Taro (React) / Taro (Vue) / uni-app (Vue)
2. **Styling**: Tailwind (via weapp-tailwindcss) / SCSS / Less
3. **CSS Preprocessor**: Sass / Less
4. **State Management**: Zustand / Redux Toolkit / Pinia (Vue) / None
5. **i18n**: Yes (Taro: @tarojs/plugin-i18n) / No
6. **Subpackages**: Yes (分包) / No
7. **Target Platforms**: 微信 / 支付宝 / 字节 / 百度 / 全部
8. **Testing**: Vitest / None
9. **Pre-commit**: Yes / No
10. **Project name**: string

### Step 2: Scaffold

**Taro (React):**
```
pnpm create @tarojs/app <project-name> --template react-ts --css sass --compiler vite
```

**Taro (Vue):**
```
pnpm create @tarojs/app <project-name> --template vue3-ts --css sass --compiler vite
```

**uni-app:**
```
pnpm create uni-app <project-name> --template vue3-ts
```

### Step 3: Dependencies

| Need | Packages |
|---|---|
| Zustand | `zustand` |
| Redux | `@reduxjs/toolkit react-redux` |
| Pinia (uni-app) | Pinia comes with uni-app template |
| Taro i18n | `@tarojs/plugin-i18n` |
| Tailwind | `weapp-tailwindcss` (Taro plugin) |
| Icons | `@taroify/icons` (icon components for Taro) |

### Step 4: Project Structure (Taro)

```
src/
├── pages/
│   ├── index/
│   │   ├── index.tsx         # Home page
│   │   ├── index.config.ts   # Page config (title, etc.)
│   │   └── index.scss
│   ├── detail/
│   │   └── ...
│   └── mine/
│       └── ...
├── components/
│   ├── NavBar.tsx             # Custom navigation bar
│   ├── EmptyState.tsx
│   ├── ErrorState.tsx
│   └── PageLoading.tsx
├── services/
│   ├── request.ts             # Taro.request wrapper
│   └── api/
│       └── index.ts
├── utils/
│   ├── index.ts               # General utils
│   ├── storage.ts             # Taro Storage wrapper
│   ├── format.ts
│   └── validate.ts
├── hooks/
│   └── useRequest.ts
├── stores/                    # State management
├── styles/
│   └── variables.scss
├── app.config.ts              # Global app config (pages, window, subpackages)
├── app.tsx                    # App entry
└── app.scss                   # Global styles
```

### Step 5: Subpackage Config (if selected)

In `app.config.ts`:
```typescript
export default defineAppConfig({
  pages: ['pages/index/index', 'pages/mine/mine'],
  subPackages: [
    {
      root: 'packageA',
      name: 'packageA',
      pages: ['pages/detail/detail', 'pages/list/list'],
    },
    {
      root: 'packageB',
      name: 'packageB',
      pages: ['pages/settings/settings'],
    },
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarTitleText: 'WeChat',
    navigationBarTextStyle: 'black',
  },
  tabBar: {
    color: '#999',
    selectedColor: '#1677ff',
    list: [
      { pagePath: 'pages/index/index', text: '首页', iconPath: 'assets/tab/home.png', selectedIconPath: 'assets/tab/home-active.png' },
      { pagePath: 'packageA/pages/list/list', text: '列表', iconPath: 'assets/tab/list.png', selectedIconPath: 'assets/tab/list-active.png' },
      { pagePath: 'pages/mine/mine', text: '我的', iconPath: 'assets/tab/mine.png', selectedIconPath: 'assets/tab/mine-active.png' },
    ],
  },
});
```

### Step 6: Key Templates

**`services/request.ts`** — Taro request wrapper:
```typescript
import Taro from '@tarojs/taro';

const BASE_URL = process.env.TARO_APP_API_URL || '';

interface RequestOptions extends Omit<Taro.request.Option, 'url' | 'success' | 'fail'> {
  params?: Record<string, string>;
}

class RequestError extends Error {
  constructor(public code: number, message: string, public data?: unknown) {
    super(message);
    this.name = 'RequestError';
  }
}

// Token management
const TOKEN_KEY = 'auth_token';
function getToken(): string {
  return Taro.getStorageSync(TOKEN_KEY) || '';
}

async function request<T = unknown>(url: string, options: RequestOptions = {}): Promise<T> {
  const { params, ...rest } = options;
  const token = getToken();

  // Build URL
  let fullUrl = `${BASE_URL}${url}`;
  if (params) {
    const qs = Object.entries(params)
      .filter(([, v]) => v != null)
      .map(([k, v]) => `${k}=${encodeURIComponent(String(v))}`)
      .join('&');
    if (qs) fullUrl += `?${qs}`;
  }

  const header: Record<string, string> = {
    ...(rest.header as Record<string, string> || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  try {
    const res = await Taro.request({ url: fullUrl, header, ...rest });
    if (res.statusCode === 401) { Taro.removeStorageSync(TOKEN_KEY); Taro.reLaunch({ url: '/pages/index/index' }); throw new RequestError(401, 'Unauthorized'); }
    if (res.statusCode >= 400) { const data = res.data as Record<string, unknown>; throw new RequestError(res.statusCode, (data?.message as string) || `HTTP ${res.statusCode}`, data); }
    return res.data as T;
  } catch (error) {
    if (error instanceof RequestError) throw error;
    throw new RequestError(0, 'Network error');
  }
}

export const http = {
  get: <T>(url: string, options?: RequestOptions) => request<T>(url, { ...options, method: 'GET' }),
  post: <T>(url: string, data?: unknown, options?: RequestOptions) => request<T>(url, { ...options, method: 'POST', data }),
  put: <T>(url: string, data?: unknown, options?: RequestOptions) => request<T>(url, { ...options, method: 'PUT', data }),
  delete: <T>(url: string, options?: RequestOptions) => request<T>(url, { ...options, method: 'DELETE' }),
};
```

**`utils/storage.ts`** — Taro Storage wrapper:
```typescript
import Taro from '@tarojs/taro';

const PREFIX = 'app_';

export const storage = {
  get<T = unknown>(key: string, defaultValue?: T): T | undefined {
    try {
      const raw = Taro.getStorageSync(`${PREFIX}${key}`);
      return raw !== '' ? (JSON.parse(raw) as T) : defaultValue;
    } catch { return defaultValue; }
  },
  set(key: string, value: unknown): void {
    Taro.setStorageSync(`${PREFIX}${key}`, JSON.stringify(value));
  },
  remove(key: string): void { Taro.removeStorageSync(`${PREFIX}${key}`); },
  clear(): void {
    const { keys } = Taro.getStorageInfoSync();
    keys.filter((k) => k.startsWith(PREFIX)).forEach((k) => Taro.removeStorageSync(k));
  },
};
```

**`components/NavBar.tsx`** — Custom navigation bar:
```tsx
import { View, Text } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { ArrowLeft } from '@taroify/icons'; // 需安装: pnpm add @taroify/icons

interface Props { title?: string; showBack?: boolean; }
export default function NavBar({ title = '', showBack = true }: Props) {
  const statusBarHeight = Taro.getWindowInfo?.()?.statusBarHeight || 20;
  const navHeight = 44;

  return (
    <View style={{ paddingTop: `${statusBarHeight}px`, background: '#fff' }}>
      <View style={{ height: `${navHeight}px`, display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
        {showBack && (
          <View onClick={() => Taro.navigateBack()} style={{ position: 'absolute', left: 12, display: 'flex', alignItems: 'center' }}>
            <ArrowLeft size={20} />
            <Text>返回</Text>
          </View>
        )}
        <Text style={{ fontSize: 17, fontWeight: 500 }}>{title}</Text>
      </View>
    </View>
  );
}
```

**`hooks/useRequest.ts`** — Data fetching hook for Taro:
```typescript
import { useState, useEffect, useCallback, useRef } from 'react';
import Taro from '@tarojs/taro';

export function useRequest<T>(fetcher: () => Promise<T>, options: { manual?: boolean } = {}) {
  const { manual = false } = options;
  const [data, setData] = useState<T>();
  const [loading, setLoading] = useState(!manual);
  const [error, setError] = useState<Error>();
  const fetcherRef = useRef(fetcher);

  const run = useCallback(async () => {
    setLoading(true);
    setError(undefined);
    try {
      const result = await fetcherRef.current();
      setData(result);
    } catch (e) {
      setError(e as Error);
      if ((e as Error).message !== 'Unauthorized') {
        Taro.showToast({ title: (e as Error).message, icon: 'none' });
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { if (!manual) run(); }, [manual, run]);

  return { data, loading, error, run, refresh: run };
}
```

### Step 7: Shared Layer + Infrastructure + Final

Read the following reference files and adapt for mini-program environment:
1. `../references/shared-base.md` — services, utils, styles, types, env files
2. `../references/shared-config.md` — tsconfig, eslint configs (skip vite configs)
3. `../references/shared-infrastructure.md` — store, i18n, hooks, config/constants

**Mini-program adaptations:**
- `request.ts` uses Taro.request instead of fetch
- `storage.ts` uses Taro Storage API
- `format.ts` — same as shared, works in Taro
- `validate.ts` — same as shared
- Theme: skip `theme/` directory (mini-programs don't support CSS custom properties widely; use Taro theme config instead)
- Layout components: skip (mini-programs use native tab bar + page stack)
- AuthGuard: adapt to Taro page lifecycle (use `useDidShow` + redirect)
- Store (Zustand): works, but use `taro-persistent-store` or manual `Taro.setStorageSync` for persistence
- CSS variables — same as shared (Taro supports SCSS)

Do NOT generate:
- vite.config.ts — Taro has its own build system
- Env files — use Taro's config/env system instead
- React Router / Vue Router — Taro has its own routing via page configs

```bash
cd <project-name>
pnpm install
pnpm dev:weapp    # or dev:alipay for Alipay
```

Announce: Mini program project with selected platforms and features.
