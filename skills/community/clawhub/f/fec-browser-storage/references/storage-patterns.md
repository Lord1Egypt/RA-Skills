# 浏览器存储模式

## 选型表

| 存储 | 容量 | API | 是否发送服务端 | 适用场景 | 安全性 |
| --- | --- | --- | --- | --- | --- |
| LocalStorage | ~5MB | 同步 | 否 | 用户偏好、非敏感持久数据 | XSS 可读取 |
| SessionStorage | ~5MB | 同步 | 否 | Tab 级临时数据 | XSS 可读取 |
| IndexedDB | 大 | 异步 | 否 | 大数据、文件、离线缓存 | XSS 可读取 |
| Cookie | ~4KB | 同步 | 是 | 认证 Session/httpOnly token | httpOnly 可防 JS 读取 |

## localStorage 封装

```ts
const STORAGE_PREFIX = "app:";

export const storage = {
  get<T>(key: string): T | null {
    try {
      const raw = localStorage.getItem(STORAGE_PREFIX + key);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },
  set<T>(key: string, value: T): void {
    localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value));
  },
  remove(key: string): void {
    localStorage.removeItem(STORAGE_PREFIX + key);
  },
  clear(): void {
    Object.keys(localStorage)
      .filter((key) => key.startsWith(STORAGE_PREFIX))
      .forEach((key) => localStorage.removeItem(key));
  },
};
```

## IndexedDB

```ts
import { openDB } from "idb";

export const db = openDB("app-offline-db", 1, {
  upgrade(database) {
    if (!database.objectStoreNames.contains("requests")) {
      database.createObjectStore("requests", { keyPath: "id" });
    }
  },
});
```

## Cookie

- httpOnly 只能由服务端设置。
- 认证 Cookie 使用 `Secure`、`SameSite=Lax/Strict`。
- 需要跨站点嵌入时才考虑 `SameSite=None; Secure`。

## 敏感数据规则

- 认证 token、刷新 token、Session ID：优先 httpOnly cookie。
- 用户偏好：localStorage。
- 表单草稿：sessionStorage 或 IndexedDB，避免敏感字段。
- 离线数据：IndexedDB，但不要缓存隐私或高价值敏感数据。
