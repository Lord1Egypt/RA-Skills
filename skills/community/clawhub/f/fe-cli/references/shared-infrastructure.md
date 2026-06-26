# Shared Infrastructure Layer Templates

Infrastructure-level templates shared across all project types.
Generate these files AFTER the sub-skill has scaffolded the project AND the shared base layer (services, utils, styles) is in place.

**When to generate:** Only generate the sections whose corresponding feature was selected during the options gathering step.
- Selected Zustand/Redux Toolkit/Pinia → generate State Management section
- Selected i18n → generate i18n section
- Always → generate Common Hooks, Global Components, Config/Constants, Auth Guard

---

## src/store/ — State Management

### Zustand (React)

```
src/store/
├── index.ts              # Re-export all stores + devtools/persist setup
├── useUserStore.ts       # User auth & profile state
├── useAppStore.ts        # Global app state (sidebar, theme, locale)
└── middleware.ts          # Custom middleware (logger, persist helpers)
```

**`src/store/index.ts`**:
```typescript
export { useUserStore } from './useUserStore';
export { useAppStore } from './useAppStore';
```

**`src/store/useUserStore.ts`**:
```typescript
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import { storage } from '@/utils/storage';

interface UserInfo {
  id: string;
  name: string;
  avatar: string;
  email?: string;
  roles?: string[];
}

interface UserState {
  token: string | null;
  userInfo: UserInfo | null;
  isLoggedIn: boolean;
  setToken: (token: string | null) => void;
  setUserInfo: (info: UserInfo) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      (set) => ({
        token: null,
        userInfo: null,
        isLoggedIn: false,
        setToken: (token) =>
          set({ token, isLoggedIn: !!token }, false, 'setToken'),
        setUserInfo: (userInfo) =>
          set({ userInfo }, false, 'setUserInfo'),
        logout: () =>
          set({ token: null, userInfo: null, isLoggedIn: false }, false, 'logout'),
      }),
      {
        name: 'user-store',
        storage: {
          getItem: (name) => storage.get(name),
          setItem: (name, value) => storage.set(name, value),
          removeItem: (name) => storage.remove(name),
        },
        partialize: (state) => ({
          token: state.token,
          userInfo: state.userInfo,
          isLoggedIn: state.isLoggedIn,
        }),
      }
    ),
    { name: 'UserStore' }
  )
);
```

**`src/store/useAppStore.ts`**:
```typescript
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';

type ThemeMode = 'light' | 'dark' | 'system';
type Locale = 'zh-CN' | 'en-US';

interface AppState {
  theme: ThemeMode;
  locale: Locale;
  sidebarCollapsed: boolean;
  globalLoading: boolean;
  setTheme: (theme: ThemeMode) => void;
  setLocale: (locale: Locale) => void;
  toggleSidebar: () => void;
  setGlobalLoading: (loading: boolean) => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        theme: 'system',
        locale: 'zh-CN',
        sidebarCollapsed: false,
        globalLoading: false,
        setTheme: (theme) => set({ theme }, false, 'setTheme'),
        setLocale: (locale) => set({ locale }, false, 'setLocale'),
        toggleSidebar: () =>
          set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed }), false, 'toggleSidebar'),
        setGlobalLoading: (loading) =>
          set({ globalLoading: loading }, false, 'setGlobalLoading'),
      }),
      {
        name: 'app-store',
        partialize: (state) => ({
          theme: state.theme,
          locale: state.locale,
          sidebarCollapsed: state.sidebarCollapsed,
        }),
      }
    ),
    { name: 'AppStore' }
  )
);
```

**`src/store/middleware.ts`**:
```typescript
import type { StateCreator, StoreMutatorIdentifier } from 'zustand';

/**
 * Logger middleware for Zustand — logs actions in dev mode only.
 * Usage: create(devtools(logger(storeCreator), { name: 'Store' }))
 */
type Logger = <
  T,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  f: StateCreator<T, Mps, Mcs>,
  name?: string,
) => StateCreator<T, Mps, Mcs>;

export const logger: Logger = (f, name) => (set, get, store) => {
  const loggedSet: typeof set = (args) => {
    if (import.meta.env.DEV) {
      console.group(`📦 ${name || 'Store'} Update`);
      console.log('Prev:', get());
      set(args);
      console.log('Next:', get());
      console.groupEnd();
    } else {
      set(args);
    }
  };
  store.setState = loggedSet;
  return f(loggedSet, get, store);
};
```

### Pinia (Vue)

**`src/store/index.ts`**:
```typescript
import { createPinia } from 'pinia';

const pinia = createPinia();

// Pinia persist plugin (optional, needs pinia-plugin-persistedstate)
// import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
// pinia.use(piniaPluginPersistedstate);

export default pinia;

// Re-export stores for convenience
export { useUserStore } from './useUserStore';
export { useAppStore } from './useAppStore';
```

**`src/store/useUserStore.ts`**:
```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(null);
  const userInfo = ref<{ id: string; name: string; avatar: string; roles?: string[] } | null>(null);

  const isLoggedIn = computed(() => !!token.value);

  function setToken(t: string | null) { token.value = t; }
  function setUserInfo(info: typeof userInfo.value) { userInfo.value = info; }
  function logout() { token.value = null; userInfo.value = null; }

  return { token, userInfo, isLoggedIn, setToken, setUserInfo, logout };
}, {
  persist: {
    key: 'user-store',
    pick: ['token', 'userInfo'],
  },
});
```

**`src/store/useAppStore.ts`**:
```typescript
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStore = defineStore('app', () => {
  const theme = ref<'light' | 'dark' | 'system'>('system');
  const locale = ref<'zh-CN' | 'en-US'>('zh-CN');
  const sidebarCollapsed = ref(false);
  const globalLoading = ref(false);

  function setTheme(t: typeof theme.value) { theme.value = t; }
  function setLocale(l: typeof locale.value) { locale.value = l; }
  function toggleSidebar() { sidebarCollapsed.value = !sidebarCollapsed.value; }
  function setGlobalLoading(loading: boolean) { globalLoading.value = loading; }

  return { theme, locale, sidebarCollapsed, globalLoading, setTheme, setLocale, toggleSidebar, setGlobalLoading };
}, {
  persist: {
    key: 'app-store',
    pick: ['theme', 'locale', 'sidebarCollapsed'],
  },
});
```

---

## src/locales/ — i18n Setup

### React (react-i18next)

```
src/locales/
├── index.ts              # i18n init
├── zh-CN.json            # Chinese translations
├── en-US.json            # English translations
└── useLanguage.ts        # Language switch hook
```

**`src/locales/index.ts`**:
```typescript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import zhCN from './zh-CN.json';
import enUS from './en-US.json';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      'zh-CN': { translation: zhCN },
      'en-US': { translation: enUS },
    },
    fallbackLng: 'zh-CN',
    interpolation: { escapeValue: false },
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
      lookupLocalStorage: 'i18n-lang',
    },
  });

export default i18n;
```

**`src/locales/zh-CN.json`**:
```json
{
  "common": {
    "confirm": "确认",
    "cancel": "取消",
    "save": "保存",
    "delete": "删除",
    "edit": "编辑",
    "search": "搜索",
    "loading": "加载中...",
    "noData": "暂无数据",
    "success": "操作成功",
    "failed": "操作失败",
    "retry": "重试",
    "back": "返回"
  },
  "auth": {
    "login": "登录",
    "logout": "退出登录",
    "username": "用户名",
    "password": "密码",
    "loginSuccess": "登录成功",
    "loginFailed": "用户名或密码错误",
    "sessionExpired": "登录已过期，请重新登录"
  },
  "validation": {
    "required": "此项为必填",
    "email": "请输入正确的邮箱",
    "mobile": "请输入正确的手机号",
    "minLength": "至少输入 {{min}} 个字符",
    "maxLength": "最多输入 {{max}} 个字符"
  },
  "error": {
    "network": "网络异常，请稍后重试",
    "notFound": "页面不存在",
    "forbidden": "无权限访问",
    "serverError": "服务器错误",
    "timeout": "请求超时"
  }
}
```

**`src/locales/en-US.json`**:
```json
{
  "common": {
    "confirm": "Confirm",
    "cancel": "Cancel",
    "save": "Save",
    "delete": "Delete",
    "edit": "Edit",
    "search": "Search",
    "loading": "Loading...",
    "noData": "No data",
    "success": "Success",
    "failed": "Failed",
    "retry": "Retry",
    "back": "Back"
  },
  "auth": {
    "login": "Login",
    "logout": "Logout",
    "username": "Username",
    "password": "Password",
    "loginSuccess": "Login successful",
    "loginFailed": "Invalid username or password",
    "sessionExpired": "Session expired, please login again"
  },
  "validation": {
    "required": "This field is required",
    "email": "Please enter a valid email",
    "mobile": "Please enter a valid phone number",
    "minLength": "Minimum {{min}} characters",
    "maxLength": "Maximum {{max}} characters"
  },
  "error": {
    "network": "Network error, please try again",
    "notFound": "Page not found",
    "forbidden": "Access denied",
    "serverError": "Server error",
    "timeout": "Request timeout"
  }
}
```

**`src/locales/useLanguage.ts`**:
```typescript
import { useTranslation } from 'react-i18next';
import { useAppStore } from '@/store';

type Locale = 'zh-CN' | 'en-US';

export function useLanguage() {
  const { i18n } = useTranslation();
  const setLocale = useAppStore((s) => s.setLocale);

  const changeLanguage = (locale: Locale) => {
    i18n.changeLanguage(locale);
    setLocale(locale);
    document.documentElement.setAttribute('lang', locale);
  };

  const currentLanguage = i18n.language as Locale;

  return { currentLanguage, changeLanguage };
}
```

> **Wire into `main.tsx`:** `import '@/locales';` before `<App />` render.

### Vue (vue-i18n)

**`src/locales/index.ts`**:
```typescript
import { createI18n } from 'vue-i18n';
import zhCN from './zh-CN.json';
import enUS from './en-US.json';

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('i18n-lang') || navigator.language || 'zh-CN',
  fallbackLocale: 'zh-CN',
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS,
  },
});

export default i18n;
```

> **Wire into `main.ts`:** `app.use(i18n);`
> **Usage in SFC:** `const { t } = useI18n();` → `{{ t('common.confirm') }}`

---

## src/theme/ — Theme System

```
src/theme/
├── index.ts              # ThemeProvider + theme logic
├── tokens.ts             # Design token definitions (light + dark)
└── useTheme.ts           # Theme hook (read/switch/theme-aware class)
```

**`src/theme/tokens.ts`**:
```typescript
export const lightTokens = {
  '--color-primary': '#1677ff',
  '--color-success': '#52c41a',
  '--color-warning': '#faad14',
  '--color-error': '#ff4d4f',
  '--color-bg-base': '#ffffff',
  '--color-bg-layout': '#f5f5f5',
  '--color-bg-elevated': '#ffffff',
  '--color-text-primary': '#333333',
  '--color-text-secondary': '#666666',
  '--color-text-disabled': '#999999',
  '--color-border': '#d9d9d9',
  '--color-border-secondary': '#f0f0f0',
} as const;

export const darkTokens = {
  '--color-primary': '#1668dc',
  '--color-success': '#49aa19',
  '--color-warning': '#d89614',
  '--color-error': '#dc4446',
  '--color-bg-base': '#141414',
  '--color-bg-layout': '#1a1a1a',
  '--color-bg-elevated': '#242424',
  '--color-text-primary': '#e8e8e8',
  '--color-text-secondary': '#a0a0a0',
  '--color-text-disabled': '#5c5c5c',
  '--color-border': '#424242',
  '--color-border-secondary': '#303030',
} as const;

export type ThemeMode = 'light' | 'dark' | 'system';
```

**`src/theme/index.ts`** (React):
```tsx
import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { lightTokens, darkTokens, type ThemeMode } from './tokens';

interface ThemeContextValue {
  theme: ThemeMode;
  resolvedTheme: 'light' | 'dark';
  setTheme: (theme: ThemeMode) => void;
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: 'system',
  resolvedTheme: 'light',
  setTheme: () => {},
});

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTokens(theme: 'light' | 'dark') {
  const tokens = theme === 'dark' ? darkTokens : lightTokens;
  const root = document.documentElement;
  Object.entries(tokens).forEach(([key, value]) => {
    root.style.setProperty(key, value);
  });
  root.setAttribute('data-theme', theme);
  root.classList.remove('light', 'dark');
  root.classList.add(theme);
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<ThemeMode>(() => {
    return (localStorage.getItem('theme') as ThemeMode) || 'system';
  });

  const resolvedTheme = theme === 'system' ? getSystemTheme() : theme;

  useEffect(() => {
    applyTokens(resolvedTheme);
    localStorage.setItem('theme', theme);
  }, [theme, resolvedTheme]);

  // Listen for system theme changes when in "system" mode
  useEffect(() => {
    if (theme !== 'system') return;
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = () => setThemeState('system'); // trigger re-render
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [theme]);

  const setTheme = (t: ThemeMode) => setThemeState(t);

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

**`src/theme/useTheme.ts`**:
```typescript
export { useTheme } from './index';
export type { ThemeMode } from './tokens';
```

> **Wire into `App.tsx`:** Wrap with `<ThemeProvider><App /></ThemeProvider>`
> **Usage in SCSS:** Reference `var(--color-primary)` instead of `$primary-color` for theme-aware styling.
> **Theme-aware component styles:**
> ```scss
> .my-card {
>   background: var(--color-bg-elevated);
>   color: var(--color-text-primary);
>   border: 1px solid var(--color-border);
> }
> ```

**`src/theme/index.ts`** (Vue):
```typescript
import { provide, inject, ref, watchEffect, type InjectionKey, onMounted, onUnmounted } from 'vue';
import { lightTokens, darkTokens, type ThemeMode } from './tokens';

interface ThemeContextValue {
  theme: ThemeMode;
  resolvedTheme: 'light' | 'dark';
  setTheme: (theme: ThemeMode) => void;
}

const THEME_KEY: InjectionKey<ThemeContextValue> = Symbol('theme');

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTokens(theme: 'light' | 'dark') {
  const tokens = theme === 'dark' ? darkTokens : lightTokens;
  const root = document.documentElement;
  Object.entries(tokens).forEach(([key, value]) => {
    root.style.setProperty(key, value);
  });
  root.setAttribute('data-theme', theme);
  root.classList.remove('light', 'dark');
  root.classList.add(theme);
}

/**
 * Call in App.vue setup() to provide theme to all descendants.
 * Reads/writes localStorage('theme') for persistence.
 */
export function useThemeProvider() {
  const theme = ref<ThemeMode>((localStorage.getItem('theme') as ThemeMode) || 'system');
  const resolvedTheme = ref<'light' | 'dark'>(
    theme.value === 'system' ? getSystemTheme() : theme.value
  );

  // Apply tokens reactively
  watchEffect(() => {
    resolvedTheme.value = theme.value === 'system' ? getSystemTheme() : theme.value;
    applyTokens(resolvedTheme.value);
    localStorage.setItem('theme', theme.value);
  });

  // Listen for system theme changes
  let mqHandler: (() => void) | null = null;
  onMounted(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    mqHandler = () => {
      if (theme.value === 'system') {
        resolvedTheme.value = getSystemTheme();
        applyTokens(resolvedTheme.value);
      }
    };
    mq.addEventListener('change', mqHandler);
  });
  onUnmounted(() => {
    if (mqHandler) {
      window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', mqHandler);
    }
  });

  const setTheme = (t: ThemeMode) => { theme.value = t; };

  const ctx: ThemeContextValue = { theme: theme.value, resolvedTheme: resolvedTheme.value, setTheme };
  provide(THEME_KEY, ctx);

  return { theme, resolvedTheme, setTheme };
}

/**
 * Use in any descendant component to read/switch theme.
 */
export function useTheme(): ThemeContextValue {
  const ctx = inject(THEME_KEY);
  if (!ctx) throw new Error('useTheme must be used inside a component that calls useThemeProvider()');
  return ctx;
}
```

> **Wire into `App.vue`:**
> ```vue
> <script setup lang="ts">
> import { useThemeProvider } from '@/theme';
> useThemeProvider();
> </script>
> ```
> **Usage in descendant components:** `const { resolvedTheme, setTheme } = useTheme();`

---

## src/hooks/ — Common Custom Hooks

**`src/hooks/useDebounce.ts`**:
```typescript
import { useEffect, useState } from 'react';

/**
 * Debounce a value — useful for search input.
 * @param value - The value to debounce
 * @param delay - Delay in ms (default: 300)
 * @example const debouncedSearch = useDebounce(searchText, 300);
 */
export function useDebounce<T>(value: T, delay = 300): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

**`src/hooks/useLocalStorage.ts`**:
```typescript
import { useState, useCallback } from 'react';

/**
 * Synced localStorage hook with type safety.
 * @param key - Storage key
 * @param initialValue - Default value if key doesn't exist
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const nextValue = value instanceof Function ? value(prev) : value;
        try {
          localStorage.setItem(key, JSON.stringify(nextValue));
        } catch {
          console.warn(`Failed to save ${key} to localStorage`);
        }
        return nextValue;
      });
    },
    [key]
  );

  const removeValue = useCallback(() => {
    try {
      localStorage.removeItem(key);
    } catch {
      // ignore
    }
    setStoredValue(initialValue);
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue];
}
```

**`src/hooks/useMediaQuery.ts`**:
```typescript
import { useState, useEffect } from 'react';

/**
 * Reactively track a CSS media query.
 * @param query - CSS media query string, e.g. '(max-width: 768px)'
 * @example const isMobile = useMediaQuery('(max-width: 768px)');
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches);

  useEffect(() => {
    const mq = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mq.addEventListener('change', handler);
    setMatches(mq.matches);
    return () => mq.removeEventListener('change', handler);
  }, [query]);

  return matches;
}
```

**`src/hooks/useClickAway.ts`**:
```typescript
import { useEffect, useRef, type RefObject } from 'react';

/**
 * Call callback when clicking outside the ref element.
 * @param ref - React ref to the container element
 * @param handler - Callback fired on outside click
 * @example useClickAway(dropdownRef, () => setOpen(false));
 */
export function useClickAway<T extends HTMLElement>(
  ref: RefObject<T | null>,
  handler: (event: MouseEvent | TouchEvent) => void
) {
  const handlerRef = useRef(handler);
  handlerRef.current = handler;

  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) return;
      handlerRef.current(event);
    };
    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);
    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref]);
}
```

**`src/hooks/useToggle.ts`**:
```typescript
import { useState, useCallback } from 'react';

/**
 * Boolean toggle hook.
 * @example const [visible, toggleVisible] = useToggle(false);
 */
export function useToggle(initial = false): [boolean, () => void, (v: boolean) => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue((v) => !v), []);
  return [value, toggle, setValue];
}
```

**`src/hooks/usePrevious.ts`**:
```typescript
import { useRef, useEffect } from 'react';

/**
 * Track the previous value of a state/prop.
 * @example const prevCount = usePrevious(count);
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}
```

**`src/hooks/useUpdateEffect.ts`**:
```typescript
import { useEffect, useRef } from 'react';

/**
 * useEffect that skips the first render (like componentDidUpdate).
 * @example useUpdateEffect(() => { fetchData(deps); }, [deps]);
 */
export function useUpdateEffect(effect: () => void | (() => void), deps: unknown[]) {
  const isFirstRender = useRef(true);
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    return effect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
```

**`src/hooks/index.ts`** — Re-export all:
```typescript
export { useRequest } from './useRequest';
export { useDebounce } from './useDebounce';
export { useLocalStorage } from './useLocalStorage';
export { useMediaQuery } from './useMediaQuery';
export { useClickAway } from './useClickAway';
export { useToggle } from './useToggle';
export { usePrevious } from './usePrevious';
export { useUpdateEffect } from './useUpdateEffect';
```

---

## src/components/ — Global Common Components

### AppProvider

**`src/components/AppProvider.tsx`** (React):
```tsx
import { type ReactNode, Suspense } from 'react';
import { ThemeProvider } from '@/theme';
import ErrorBoundary from './ErrorBoundary';
import PageLoading from './PageLoading';

interface AppProviderProps {
  children: ReactNode;
}

/**
 * Root provider that wraps all context providers.
 * Add new providers here as the app grows.
 *
 * Order matters: outermost providers wrap inner ones.
 * Typical: Theme → i18n → State → Router → ErrorBoundary → App
 */
export default function AppProvider({ children }: AppProviderProps) {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Suspense fallback={<PageLoading />}>
          {children}
        </Suspense>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
```

> **If i18n was selected:** add `import '@/locales';` at the top and wrap `<I18nextProvider>` inside ThemeProvider.
> **Wire into `main.tsx`:** `<AppProvider><App /></AppProvider>`

### Layout Components (Web SPA / Admin)

**`src/layouts/AppLayout.tsx`**:
```tsx
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import styles from './AppLayout.module.scss';

export default function AppLayout() {
  return (
    <div className={styles.layout}>
      <Sidebar />
      <div className={styles.main}>
        <Header />
        <div className={styles.content}>
          <Outlet />
        </div>
      </div>
    </div>
  );
}
```

**`src/layouts/Header.tsx`**:
```tsx
import { useNavigate } from 'react-router-dom';
import { useTheme } from '@/theme';
import { useUserStore } from '@/store';
import styles from './Header.module.scss';

export default function Header() {
  const navigate = useNavigate();
  const { resolvedTheme, setTheme } = useTheme();
  const { userInfo, logout } = useUserStore();

  const toggleTheme = () => {
    setTheme(resolvedTheme === 'dark' ? 'light' : 'dark');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        {/* Breadcrumb or page title */}
      </div>
      <div className={styles.right}>
        <button onClick={toggleTheme} className={styles.themeBtn} aria-label="Toggle theme">
          {resolvedTheme === 'dark' ? '☀️' : '🌙'}
        </button>
        <div className={styles.user}>
          <span>{userInfo?.name || 'User'}</span>
          <button onClick={handleLogout}>退出</button>
        </div>
      </div>
    </header>
  );
}
```

**`src/layouts/Sidebar.tsx`**:
```tsx
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppStore } from '@/store';
import styles from './Sidebar.module.scss';

interface MenuItem {
  key: string;
  label: string;
  icon?: React.ReactNode;
  children?: MenuItem[];
}

// TODO: Replace with actual menu items from route config
const menuItems: MenuItem[] = [
  { key: '/', label: '首页' },
  // { key: '/about', label: '关于' },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const collapsed = useAppStore((s) => s.sidebarCollapsed);
  const toggleSidebar = useAppStore((s) => s.toggleSidebar);

  return (
    <aside className={`${styles.sidebar} ${collapsed ? styles.collapsed : ''}`}>
      <div className={styles.logo}>
        {collapsed ? '◉' : '◉ My App'}
      </div>
      <nav className={styles.nav}>
        {menuItems.map((item) => (
          <div
            key={item.key}
            className={`${styles.menuItem} ${location.pathname === item.key ? styles.active : ''}`}
            onClick={() => navigate(item.key)}
          >
            {item.icon}
            {!collapsed && <span>{item.label}</span>}
          </div>
        ))}
      </nav>
      <button className={styles.collapseBtn} onClick={toggleSidebar}>
        {collapsed ? '→' : '←'}
      </button>
    </aside>
  );
}
```

### GlobalLoading

**`src/components/GlobalLoading.tsx`**:
```tsx
import { useAppStore } from '@/store';
import PageLoading from './PageLoading';

/**
 * Full-page loading overlay controlled by global app state.
 * Use `useAppStore.getState().setGlobalLoading(true/false)` anywhere.
 */
export default function GlobalLoading() {
  const loading = useAppStore((s) => s.globalLoading);
  if (!loading) return null;
  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 9999,
      background: 'rgba(255,255,255,0.6)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <PageLoading />
    </div>
  );
}
```

### AuthGuard

**`src/components/AuthGuard.tsx`** (React):
```tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useUserStore } from '@/store';

interface AuthGuardProps {
  children: React.ReactNode;
  /** Roles allowed to access. Empty = any authenticated user. */
  allowedRoles?: string[];
}

/**
 * Route guard that redirects unauthenticated users to /login.
 * Optionally restrict access by role.
 */
export default function AuthGuard({ children, allowedRoles }: AuthGuardProps) {
  const { isLoggedIn, userInfo } = useUserStore();
  const location = useLocation();

  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && allowedRoles.length > 0) {
    const userRoles = userInfo?.roles || [];
    const hasRole = userRoles.some((role) => allowedRoles.includes(role));
    if (!hasRole) {
      return <Navigate to="/403" replace />;
    }
  }

  return <>{children}</>;
}
```

**Usage in router:**
```tsx
<Route
  path="/dashboard"
  element={
    <AuthGuard allowedRoles={['admin']}>
      <Dashboard />
    </AuthGuard>
  }
/>
```

---

## src/config/ — Global Config & Constants

**`src/config/index.ts`**:
```typescript
/**
 * Application-level constants and configuration.
 * Environment-specific values come from .env files via import.meta.env.
 */

export const APP_NAME = import.meta.env.VITE_APP_TITLE || 'My App';
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/** Storage key prefix */
export const STORAGE_PREFIX = import.meta.env.VITE_STORAGE_PREFIX || 'app_';

/** Default page size for paginated lists */
export const DEFAULT_PAGE_SIZE = 20;

/** Token refresh threshold (ms before expiry) */
export const TOKEN_REFRESH_THRESHOLD = 5 * 60 * 1000; // 5 minutes

/** Supported locales */
export const SUPPORTED_LOCALES = ['zh-CN', 'en-US'] as const;
export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];

/** Route paths — single source of truth for all route constants */
export const ROUTE_PATHS = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  NOT_FOUND: '/404',
  FORBIDDEN: '/403',
} as const;

/** HTTP status codes used in the app */
export const HTTP_STATUS = {
  OK: 200,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
} as const;
```

**`src/config/routes.tsx`** (React):
```tsx
import { lazy } from 'react';
import type { RouteObject } from 'react-router-dom';
import AuthGuard from '@/components/AuthGuard';
import AppLayout from '@/layouts/AppLayout';
import { ROUTE_PATHS } from './index';

// Lazy-load pages for code splitting
const Home = lazy(() => import('@/pages/Home'));
const Login = lazy(() => import('@/pages/Login'));
const Dashboard = lazy(() => import('@/pages/Dashboard'));
const NotFound = lazy(() => import('@/pages/NotFound'));

/**
 * Centralized route configuration.
 * Add new routes here — do not scatter route definitions across files.
 */
export const routes: RouteObject[] = [
  {
    path: ROUTE_PATHS.LOGIN,
    element: <Login />,
  },
  {
    element: <AppLayout />,
    children: [
      {
        path: ROUTE_PATHS.HOME,
        element: <Home />,
      },
      {
        path: ROUTE_PATHS.DASHBOARD,
        element: (
          <AuthGuard allowedRoles={['admin']}>
            <Dashboard />
          </AuthGuard>
        ),
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
];
```

> **Wire into App.tsx:** `useRoutes(routes)` or `<Routes>` with the config above.
> **Vue version:** Define routes as `RouteRecordRaw[]` in `src/config/routes.ts`, use `createRouter()`.

---

## Updated Directory Structure

After adding infrastructure layer, the full `src/` structure becomes:

```
src/
├── components/
│   ├── AppProvider.tsx       # Root context provider wrapper
│   ├── AuthGuard.tsx         # Route authentication guard
│   ├── ErrorBoundary.tsx     # React error boundary
│   ├── GlobalLoading.tsx     # Full-page loading overlay
│   ├── PageLoading.tsx       # Inline loading spinner
│   ├── EmptyState.tsx        # Empty state placeholder
│   └── ErrorState.tsx        # Error state with retry
├── config/
│   ├── index.ts              # App constants + env config
│   └── routes.tsx            # Centralized route definitions
├── hooks/
│   ├── index.ts              # Re-export all hooks
│   ├── useRequest.ts         # Data fetching
│   ├── useDebounce.ts        # Debounce value
│   ├── useLocalStorage.ts    # Typed localStorage
│   ├── useMediaQuery.ts      # CSS media query reactive
│   ├── useClickAway.ts       # Click outside detector
│   ├── useToggle.ts          # Boolean toggle
│   ├── usePrevious.ts        # Previous value tracker
│   └── useUpdateEffect.ts    # Skip-first-render effect
├── layouts/
│   ├── AppLayout.tsx         # Main layout (sidebar + header + content)
│   ├── Header.tsx            # Top bar (theme toggle, user menu)
│   └── Sidebar.tsx           # Side navigation
├── locales/                  # (Only if i18n selected)
│   ├── index.ts              # i18n init
│   ├── zh-CN.json            # Chinese
│   ├── en-US.json            # English
│   └── useLanguage.ts        # Language switch hook
├── store/                    # (Only if state mgmt selected)
│   ├── index.ts              # Re-export stores
│   ├── useUserStore.ts       # User auth & profile
│   ├── useAppStore.ts        # App-level state (theme, locale, sidebar)
│   └── middleware.ts         # Custom middleware (logger, persist helpers)
├── theme/
│   ├── index.ts              # ThemeProvider + theme logic
│   ├── tokens.ts             # Light + dark design tokens
│   └── useTheme.ts           # Theme hook
├── services/
│   ├── request.ts            # Fetch wrapper
│   ├── logger.ts             # Structured logger
│   ├── log-export.ts         # Log export & submit
│   └── api/index.ts          # API endpoints
├── styles/
│   ├── global.scss           # CSS variables + global styles
│   ├── reset.scss            # CSS reset
│   └── variables.scss        # Design tokens (SCSS vars)
├── utils/
│   ├── index.ts              # General utilities
│   ├── storage.ts            # Storage wrapper
│   ├── format.ts             # Formatters
│   └── validate.ts           # Validators
├── types/
│   └── global.d.ts           # Global type declarations
├── pages/                    # Page components (from sub-skill)
├── App.tsx
└── main.tsx
```
