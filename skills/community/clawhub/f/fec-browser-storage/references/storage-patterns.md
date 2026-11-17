# Browser storage mode

## Selection table

| Storage | Capacity | API | Whether to send to the server | Applicable scenarios | Security |
| --- | --- | --- | --- | --- | --- |
| LocalStorage | ~5MB | Sync | No | User preferences, non-sensitive persistent data | XSS Readable |
| SessionStorage | ~5MB | Sync | No | Tab-sized temporary data | XSS Readable |
| IndexedDB | Large | Asynchronous | No | Big data, file, offline cache | XSS readable |
| Cookie | ~4KB | Synchronization | Yes | Authentication Session/httpOnly token | httpOnly can prevent JS reading |

## localStorage encapsulation

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

- httpOnly can only be set by the server.
- Authentication Cookie uses `Secure`, `SameSite=Lax/Strict`.
- Only consider `SameSite=None; Secure` when cross-site embedding is required.

## Sensitive data rules

- Authentication token, refresh token, Session ID: priority is given to httpOnly cookie.
- User preference: localStorage.
- Form draft: sessionStorage or IndexedDB, avoid sensitive fields.
- Offline data: IndexedDB, but do not cache private or high-value sensitive data.
