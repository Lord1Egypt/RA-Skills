# 工程脚手架文件

最小可运行的 Vue 3 + Arco Design + Vite 工程模板。生成页面原型时，如果 `webui/admin-ui/package.json` 不存在，按以下文件清单逐一创建。

## 占位符说明

| 占位符 | 替换为 | 示例 |
|---|---|---|
| `{{pageTitle}}` | 页面中文名称 | `操作日志` |
| `{{viewImportPath}}` | 页面组件相对路径 | `./views/operation-log/index.vue` |
| `{{ViewComponent}}` | 页面组件名（PascalCase） | `OperationLog` |

---

## 文件清单

### `package.json`

```json
{
  "name": "admin-ui",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "@arco-design/web-vue": "^2.56.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.1.0",
    "less": "^4.2.0",
    "typescript": "^5.5.0",
    "vite": "^5.4.0",
    "vue-tsc": "^2.1.0"
  }
}
```

### `vite.config.ts`

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "noEmit": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.vue", "src/**/*.d.ts"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### `tsconfig.node.json`

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

### `index.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Admin UI - {{pageTitle}}</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

### `src/main.ts`

```typescript
import { createApp } from 'vue';
import ArcoVue from '@arco-design/web-vue';
import '@arco-design/web-vue/dist/arco.css';
import App from './App.vue';

const app = createApp(App);
app.use(ArcoVue);
app.mount('#app');
```

### `src/App.vue`

```vue
<script setup lang="ts">
  import {{ViewComponent}} from '{{viewImportPath}}';
</script>

<template>
  <div style="background: var(--color-bg-1); min-height: 100vh">
    <{{ViewComponent}} />
  </div>
</template>
```

### `src/env.d.ts`

```typescript
/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
```