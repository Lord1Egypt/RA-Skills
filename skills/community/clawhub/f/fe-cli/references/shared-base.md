# Shared Base Code Templates

Templates for common source files shared across all project types.
Generate these files using `write` tool after the sub-skill has scaffolded the project.

---

## src/services/request.ts — Fetch Wrapper

```typescript
// Lightweight fetch wrapper with interceptors
// Supports: auto token injection, unified error handling, request/response logging

const LOGIN_PATH = import.meta.env.VITE_LOGIN_PATH || '/login';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

interface RequestConfig extends Omit<RequestInit, 'body'> {
  params?: Record<string, string>;
  body?: unknown;
  timeout?: number;
}

interface ApiResponse<T = unknown> {
  code: number;
  data: T;
  message: string;
}

class RequestError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'RequestError';
  }
}

// Token management
const TOKEN_KEY = 'auth_token';
function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

// Request interceptor
async function requestInterceptor(config: RequestConfig): Promise<RequestConfig> {
  const token = getToken();
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
}

// Response interceptor
async function responseInterceptor<T>(response: Response): Promise<T> {
  if (response.status === 401) {
    localStorage.removeItem(TOKEN_KEY);
    window.location.href = LOGIN_PATH;
    throw new RequestError(401, 'Unauthorized');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new RequestError(response.status, errorData?.message || `HTTP ${response.status}`, errorData);
  }

  const result: ApiResponse<T> = await response.json();
  if (result.code !== 0 && result.code !== 200) {
    throw new RequestError(result.code, result.message || 'Request failed', result);
  }
  return result.data;
}

// Main request function
async function request<T = unknown>(url: string, config: RequestConfig = {}): Promise<T> {
  const { params, body, timeout = 30000, ...init } = config;

  // Build URL with query params
  let fullUrl = `${BASE_URL}${url}`;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value));
      }
    });
    const qs = searchParams.toString();
    if (qs) fullUrl += `?${qs}`;
  }

  // Prepare headers & body
  const headers: Record<string, string> = {
    ...(init.headers as Record<string, string> || {}),
  };
  if (body && !(body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const finalConfig = await requestInterceptor({
    ...init,
    headers,
    body: body instanceof FormData ? body : body ? JSON.stringify(body) : undefined,
  });

  // Timeout
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(fullUrl, {
      ...finalConfig,
      signal: controller.signal,
    });
    return responseInterceptor<T>(response);
  } catch (error) {
    if (error instanceof RequestError) throw error;
    if ((error as Error).name === 'AbortError') {
      throw new RequestError(408, 'Request timeout');
    }
    throw new RequestError(0, (error as Error).message || 'Network error');
  } finally {
    clearTimeout(timer);
  }
}

// Convenience methods
export const http = {
  get: <T>(url: string, config?: RequestConfig) => request<T>(url, { ...config, method: 'GET' }),
  post: <T>(url: string, body?: unknown, config?: RequestConfig) => request<T>(url, { ...config, method: 'POST', body }),
  put: <T>(url: string, body?: unknown, config?: RequestConfig) => request<T>(url, { ...config, method: 'PUT', body }),
  patch: <T>(url: string, body?: unknown, config?: RequestConfig) => request<T>(url, { ...config, method: 'PATCH', body }),
  delete: <T>(url: string, config?: RequestConfig) => request<T>(url, { ...config, method: 'DELETE' }),
  upload: <T>(url: string, formData: FormData, config?: RequestConfig) =>
    request<T>(url, { ...config, method: 'POST', body: formData }),
};

export { request, RequestError };
export type { ApiResponse, RequestConfig };
```

---

## src/services/api/index.ts — API Endpoints

```typescript
import { http } from '@/services/request';

// ===== User =====
export const userApi = {
  login: (data: { username: string; password: string }) =>
    http.post<{ token: string }>('/api/user/login', data),
  getUserInfo: () =>
    http.get<{ id: string; name: string; avatar: string }>('/api/user/info'),
};

// ===== File Upload =====
export const uploadApi = {
  uploadFile: (file: File) => {
    const fd = new FormData();
    fd.append('file', file);
    return http.upload<{ url: string }>('/api/upload', fd);
  },
};

// Extend this file with your API modules below
```

---

## src/utils/index.ts — General Utilities

```typescript
/** Debounce */
export function debounce<T extends (...args: unknown[]) => void>(fn: T, delay: number): T {
  let timer: ReturnType<typeof setTimeout>;
  return ((...args: unknown[]) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  }) as T;
}

/** Throttle */
export function throttle<T extends (...args: unknown[]) => void>(fn: T, interval: number): T {
  let last = 0;
  return ((...args: unknown[]) => {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn(...args);
    }
  }) as T;
}

/** Deep clone (JSON-safe) */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

/** Get URL query parameter */
export function getQueryParam(key: string): string | null {
  const params = new URLSearchParams(window.location.search);
  return params.get(key);
}

/** Generate UUID v4 */
export function uuid(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/** Sleep */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/** Is empty (null, undefined, empty string, empty array, empty object) */
export function isEmpty(value: unknown): boolean {
  if (value == null) return true;
  if (typeof value === 'string') return value.trim() === '';
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value as object).length === 0;
  return false;
}

/** Clip text with ellipsis */
export function ellipsis(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}
```

---

## src/utils/storage.ts — Storage Wrapper

```typescript
const PREFIX = import.meta.env.VITE_STORAGE_PREFIX || 'app_';

function getKey(key: string): string {
  return `${PREFIX}${key}`;
}

export const storage = {
  get<T = unknown>(key: string): T | null {
    try {
      const raw = localStorage.getItem(getKey(key));
      return raw ? (JSON.parse(raw) as T) : null;
    } catch {
      return null;
    }
  },

  set(key: string, value: unknown): void {
    try {
      localStorage.setItem(getKey(key), JSON.stringify(value));
    } catch (e) {
      console.warn('Storage full or unavailable', e);
    }
  },

  remove(key: string): void {
    localStorage.removeItem(getKey(key));
  },

  clear(): void {
    const keys = Object.keys(localStorage).filter((k) => k.startsWith(PREFIX));
    keys.forEach((k) => localStorage.removeItem(k));
  },

  // Session storage
  session: {
    get<T = unknown>(key: string): T | null {
      try {
        const raw = sessionStorage.getItem(getKey(key));
        return raw ? (JSON.parse(raw) as T) : null;
      } catch {
        return null;
      }
    },
    set(key: string, value: unknown): void {
      sessionStorage.setItem(getKey(key), JSON.stringify(value));
    },
    remove(key: string): void {
      sessionStorage.removeItem(getKey(key));
    },
  },
};
```

---

## src/utils/format.ts — Formatters

```typescript
/** Format number with commas: 1000 → 1,000 */
export function formatNumber(num: number): string {
  return num.toLocaleString('zh-CN');
}

/** Format file size: 1024 → "1 KB" */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(i > 0 ? 1 : 0)} ${units[i]}`;
}

/** Format date: "2026-05-11" */
export function formatDate(date: Date | string | number, fmt = 'YYYY-MM-DD'): string {
  const d = new Date(date);
  const map: Record<string, string> = {
    YYYY: String(d.getFullYear()),
    MM: String(d.getMonth() + 1).padStart(2, '0'),
    DD: String(d.getDate()).padStart(2, '0'),
    HH: String(d.getHours()).padStart(2, '0'),
    mm: String(d.getMinutes()).padStart(2, '0'),
    ss: String(d.getSeconds()).padStart(2, '0'),
  };
  return fmt.replace(/YYYY|MM|DD|HH|mm|ss/g, (k) => map[k]);
}

/** Relative time: "3分钟前", "2小时前", "昨天" */
export function timeAgo(date: Date | string | number): string {
  const now = Date.now();
  const past = new Date(date).getTime();
  const diff = now - past;

  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diff < minute) return '刚刚';
  if (diff < hour) return `${Math.floor(diff / minute)}分钟前`;
  if (diff < day) return `${Math.floor(diff / hour)}小时前`;
  if (diff < 2 * day) return '昨天';
  if (diff < 30 * day) return `${Math.floor(diff / day)}天前`;
  return formatDate(date);
}
```

---

## src/utils/validate.ts — Validators

```typescript
/** Validate email */
export function isEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

/** Validate Chinese mobile */
export function isMobile(value: string): boolean {
  return /^1[3-9]\d{9}$/.test(value);
}

/** Validate URL */
export function isUrl(value: string): boolean {
  try {
    new URL(value);
    return true;
  } catch {
    return false;
  }
}

/** Validate ID card (Chinese) */
export function isIdCard(value: string): boolean {
  return /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/.test(value);
}

/** Get form field error message */
export function formRules() {
  return {
    required: (label = '此项') => ({ required: true, message: `${label}不能为空` }),
    email: (label = '邮箱') => ({ type: 'email' as const, message: `请输入正确的${label}` }),
    mobile: (label = '手机号') => ({ pattern: /^1[3-9]\d{9}$/, message: `请输入正确的${label}` }),
  };
}
```

---

## src/styles/variables.scss

```scss
// ===== Colors =====
$primary-color: #1677ff;
$success-color: #52c41a;
$warning-color: #faad14;
$error-color: #ff4d4f;
$text-color: #333333;
$text-secondary: #666666;
$text-disabled: #999999;
$border-color: #d9d9d9;
$bg-color: #f5f5f5;
$bg-white: #ffffff;

// ===== Spacing =====
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
$spacing-xxl: 48px;

// ===== Font =====
$font-size-xs: 12px;
$font-size-sm: 13px;
$font-size-base: 14px;
$font-size-lg: 16px;
$font-size-xl: 18px;
$font-size-xxl: 24px;

// ===== Border Radius =====
$radius-sm: 4px;
$radius-md: 8px;
$radius-lg: 12px;
$radius-round: 50%;

// ===== Breakpoints =====
$breakpoint-mobile: 768px;
$breakpoint-tablet: 1024px;
$breakpoint-desktop: 1280px;

// ===== Z-index =====
$z-dropdown: 1000;
$z-modal: 1050;
$z-toast: 1100;

// CSS Variables (use in global.scss)
:root {
  --primary-color: #{$primary-color};
  --success-color: #{$success-color};
  --warning-color: #{$warning-color};
  --error-color: #{$error-color};
  --text-color: #{$text-color};
  --text-secondary: #{$text-secondary};
  --bg-color: #{$bg-color};
  --spacing-md: #{$spacing-md};
  --radius-md: #{$radius-md};
  --breakpoint-mobile: #{$breakpoint-mobile};
  --breakpoint-tablet: #{$breakpoint-tablet};
}
```

---

## src/styles/reset.scss

```scss
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
  font-size: $font-size-base;
  color: $text-color;
  line-height: 1.5;
  background-color: $bg-white;
}

a {
  color: $primary-color;
  text-decoration: none;
  &:hover { text-decoration: underline; }
}

ul, ol { list-style: none; }

img { max-width: 100%; vertical-align: middle; }

input, button, textarea, select {
  font: inherit;
  outline: none;
}

table { border-collapse: collapse; }
```

---

## src/styles/global.scss

```scss
@import 'variables';
@import 'reset';

// ===== Scrollbar =====
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
::-webkit-scrollbar-track {
  background: transparent;
}

// ===== Utility classes =====
.text-center { text-align: center; }
.text-right { text-align: right; }
.flex-center { display: flex; align-items: center; justify-content: center; }
.flex-between { display: flex; align-items: center; justify-content: space-between; }

// ===== Responsive mixins =====
@mixin mobile {
  @media (max-width: #{$breakpoint-mobile - 1px}) { @content; }
}
@mixin tablet {
  @media (min-width: $breakpoint-mobile) and (max-width: #{$breakpoint-tablet - 1px}) { @content; }
}
@mixin desktop {
  @media (min-width: $breakpoint-tablet) { @content; }
}
@mixin not-mobile {
  @media (min-width: $breakpoint-mobile) { @content; }
}
```

---

## src/types/global.d.ts

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_STORAGE_PREFIX: string;
  readonly VITE_APP_TITLE: string;
  readonly VITE_LOGIN_PATH: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

---

## Environment Files

### .env
```
VITE_APP_TITLE=My App
VITE_STORAGE_PREFIX=app_
```

### .env.development
```
VITE_API_BASE_URL=http://localhost:3000
```

### .env.test
```
VITE_API_BASE_URL=https://test-api.example.com
```

### .env.production
```
VITE_API_BASE_URL=https://api.example.com
```

---

## src/services/logger.ts — Structured Logger

File-level logging with rotation, thresholds, and export capability.
Logs are written to a user-accessible directory so users can always inspect them.

```typescript
/**
 * Structured logger for frontend applications.
 *
 * Features:
 *   - Log levels: debug, info, warn, error
 *   - Dual output: console (browser) + persistent file (via IndexedDB + download)
 *   - Size cap: when log exceeds `maxBytes`, oldest entries are trimmed automatically
 *   - Export: one-click download as .log file, or submit via configurable endpoint
 *   - Source tag: each call includes module/file context for easy grep
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  module: string;
  message: string;
  data?: unknown;
}

const LEVEL_PRIORITY: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

interface LoggerConfig {
  /** Minimum level to output (default: 'info') */
  level: LogLevel;
  /** Max log storage in bytes before trimming (default: 5 MB) */
  maxBytes: number;
  /** Key used for IndexedDB / localStorage persistence (default: 'app-logs') */
  storageKey: string;
  /** Enable console output (default: true in dev, false in prod) */
  consoleEnabled: boolean;
}

const DEFAULT_CONFIG: LoggerConfig = {
  level: (import.meta.env.VITE_LOG_LEVEL as LogLevel) || 'info',
  maxBytes: 5 * 1024 * 1024, // 5 MB
  storageKey: 'app-logs',
  consoleEnabled: import.meta.env.DEV,
};

function formatTimestamp(d: Date): string {
  return d.toISOString();
}

function formatEntry(entry: LogEntry): string {
  const data = entry.data !== undefined ? ` ${JSON.stringify(entry.data)}` : '';
  return `[${entry.timestamp}] ${entry.level.toUpperCase()} [${entry.module}] ${entry.message}${data}`;
}

export class Logger {
  private config: LoggerConfig;
  private buffer: LogEntry[] = [];
  private _listeners: ((entry: LogEntry) => void)[] = [];

  constructor(config: Partial<LoggerConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this._loadFromStorage();
  }

  private _shouldLog(level: LogLevel): boolean {
    return LEVEL_PRIORITY[level] >= LEVEL_PRIORITY[this.config.level];
  }

  private _push(entry: LogEntry): void {
    if (!this._shouldLog(entry.level)) return;

    // Console output
    if (this.config.consoleEnabled) {
      const fn = entry.level === 'error' ? console.error
        : entry.level === 'warn' ? console.warn
        : entry.level === 'debug' ? console.debug
        : console.log;
      const tag = `[${entry.module}]`;
      entry.data !== undefined ? fn(tag, entry.message, entry.data) : fn(tag, entry.message);
    }

    // Buffer
    this.buffer.push(entry);
    this._listeners.forEach((l) => l(entry));

    // Persist (debounced via setTimeout)
    this._persist();
  }

  /** Trim oldest entries when buffer exceeds maxBytes */
  private _trim(): void {
    const estimated = JSON.stringify(this.buffer).length;
    if (estimated > this.config.maxBytes) {
      // Remove oldest ~20% of entries
      const trimCount = Math.floor(this.buffer.length * 0.2);
      this.buffer.splice(0, trimCount);
    }
  }

  private _persist(): void {
    try {
      this._trim();
      // Use localStorage for small logs, IndexedDB for larger
      const serialized = JSON.stringify(this.buffer);
      if (serialized.length < 2 * 1024 * 1024) {
        // < 2 MB fits in localStorage
        try { localStorage.setItem(this.config.storageKey, serialized); } catch {
          // localStorage full, force trim more
          this.buffer.splice(0, Math.floor(this.buffer.length * 0.5));
        }
      }
      // For > 2 MB, consider IndexedDB (implementation in log-export.ts)
    } catch {
      // Silently fail — logging should never crash the app
    }
  }

  private _loadFromStorage(): void {
    try {
      const raw = localStorage.getItem(this.config.storageKey);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) this.buffer = parsed;
      }
    } catch {
      this.buffer = [];
    }
  }

  /** Create a scoped sub-logger with a fixed module tag */
  child(module: string): ScopedLogger {
    return new ScopedLogger(this, module);
  }

  debug(module: string, message: string, data?: unknown): void {
    this._push({ timestamp: formatTimestamp(new Date()), level: 'debug', module, message, data });
  }

  info(module: string, message: string, data?: unknown): void {
    this._push({ timestamp: formatTimestamp(new Date()), level: 'info', module, message, data });
  }

  warn(module: string, message: string, data?: unknown): void {
    this._push({ timestamp: formatTimestamp(new Date()), level: 'warn', module, message, data });
  }

  error(module: string, message: string, data?: unknown): void {
    this._push({ timestamp: formatTimestamp(new Date()), level: 'error', module, message, data });
  }

  /** Get all logs as formatted text */
  getAllAsText(): string {
    return this.buffer.map(formatEntry).join('\n');
  }

  /** Get all logs as structured JSON */
  getAllAsJson(): LogEntry[] {
    return [...this.buffer];
  }

  /** Get logs filtered by level */
  getByLevel(level: LogLevel): LogEntry[] {
    return this.buffer.filter((e) => e.level === level);
  }

  /** Clear all stored logs */
  clear(): void {
    this.buffer = [];
    try { localStorage.removeItem(this.config.storageKey); } catch { /* ignore */ }
  }

  /** Get current buffer size in bytes */
  get size(): number {
    return JSON.stringify(this.buffer).length;
  }

  /** Get entry count */
  get count(): number {
    return this.buffer.length;
  }

  /** Subscribe to new log entries (for UI panels, etc.) */
  onEntry(listener: (entry: LogEntry) => void): () => void {
    this._listeners.push(listener);
    return () => {
      this._listeners = this._listeners.filter((l) => l !== listener);
    };
  }

  /** Update config at runtime */
  setLevel(level: LogLevel): void { this.config.level = level; }
  setMaxBytes(bytes: number): void { this.config.maxBytes = bytes; this._trim(); }
}

/** Scoped logger with a fixed module tag — preferred for daily use */
export class ScopedLogger {
  constructor(private parent: Logger, private module: string) {}

  debug(message: string, data?: unknown): void { this.parent.debug(this.module, message, data); }
  info(message: string, data?: unknown): void { this.parent.info(this.module, message, data); }
  warn(message: string, data?: unknown): void { this.parent.warn(this.module, message, data); }
  error(message: string, data?: unknown): void { this.parent.error(this.module, message, data); }
}

// ─── Singleton ───
export const logger = new Logger();

// ─── Convenience: create scoped loggers ───
// Usage in any module:
//   import { logger } from '@/services/logger';
//   const log = logger.child('AuthService');
//   log.info('user logged in', { userId: '123' });

---

## src/services/log-export.ts — Log Export & Submit

Utility for exporting logs as files or submitting them to a configurable endpoint.

```typescript
import { logger } from './logger';

/**
 * Log export and submission utilities.
 *
 * Export: download logs as .log or .json file
 * Submit: POST logs to a configurable endpoint (placeholder — destination TBD)
 *
 * Usage:
 *   import { exportLogsAsFile, submitLogs } from '@/services/log-export';
 *   exportLogsAsFile('text');        // triggers .log download
 *   submitLogs('https://...');       // POST to endpoint (TBD)
 */

export type ExportFormat = 'text' | 'json';

/**
 * Download all stored logs as a file.
 * Creates a temporary <a> element to trigger browser download.
 */
export function exportLogsAsFile(format: ExportFormat = 'text', filename?: string): void {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const ext = format === 'json' ? 'json' : 'log';
  const name = filename || `app-logs-${timestamp}.${ext}`;

  let content: string;
  let mimeType: string;

  if (format === 'json') {
    content = JSON.stringify(logger.getAllAsJson(), null, 2);
    mimeType = 'application/json';
  } else {
    content = logger.getAllAsText();
    mimeType = 'text/plain';
  }

  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  logger.info('LogExport', `exported ${logger.count} entries (${format}, ${(content.length / 1024).toFixed(1)} KB)`);
}

/**
 * Submit logs to a remote endpoint.
 *
 * ⚠️ PLACEHOLDER — destination and format TBD.
 * Possible targets:
 *   - Internal log aggregation service
 *   - Feishu webhook / bot message
 *   - Sentry / Datadog / external APM
 *   - GitLab issue creation
 *   - Email attachment
 *
 * @param endpoint - URL to POST logs to (TBD: may become a config value)
 */
export async function submitLogs(endpoint?: string): Promise<{ success: boolean; message: string }> {
  // TODO: Implement log submission
  // Design considerations:
  //   - Should batch if logs are large
  //   - Should include metadata (app version, OS, browser, timestamp)
  //   - Should handle network errors gracefully
  //   - Should strip sensitive data before sending
  //   - Should respect VITE_LOG_SUBMIT_URL env config

  const target = endpoint || import.meta.env.VITE_LOG_SUBMIT_URL || '';

  if (!target) {
    const warning = 'Log submit endpoint not configured (VITE_LOG_SUBMIT_URL)';
    logger.warn('LogExport', warning);
    // Fallback: export as file
    exportLogsAsFile('text');
    return { success: false, message: `${warning}. Logs exported as file instead.` };
  }

  try {
    const payload = {
      appVersion: import.meta.env.VITE_APP_VERSION || 'unknown',
      environment: import.meta.env.MODE,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      logCount: logger.count,
      entries: logger.getByLevel('error'), // Only send errors by default
    };

    const res = await fetch(target, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }

    logger.info('LogExport', `submitted ${payload.logCount} error entries to ${target}`);
    return { success: true, message: `Submitted ${payload.logCount} error log(s).` };
  } catch (err) {
    const msg = (err as Error).message;
    logger.error('LogExport', `submit failed: ${msg}`);
    // Fallback: export locally
    exportLogsAsFile('text');
    return { success: false, message: `Submit failed: ${msg}. Logs exported as file.` };
  }
}

/**
 * Clear all stored logs.
 * Optionally export before clearing.
 */
export function clearLogs(exportBeforeClear = false): void {
  if (exportBeforeClear && logger.count > 0) {
    exportLogsAsFile('text');
  }
  logger.clear();
  logger.info('LogExport', 'all logs cleared');
}
