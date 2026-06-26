---
name: frontend-perf-audit
description: 前端性能审计清单。当需要诊断网页/SPA性能问题时使用。涵盖Core Web Vitals(LCP/FID/CLS)、资源加载优化、渲染阻塞消除、代码分割策略、图片懒加载、缓存策略、Bundle分析。提供Chrome DevTools和Lighthouse的具体操作步骤。

**使用时机**：
(1) 网页加载慢（首屏 > 3s）
(2) 交互卡顿（FID > 100ms）
(3) 布局抖动（CLS > 0.1）
(4) Bundle体积过大
(5) 用户提到"页面慢"、"加载卡"、"性能优化"、"首屏"
---

# 前端性能审计清单

## Core Web Vitals 目标

| 指标 | 含义 | 目标 | 差 |
|------|------|------|-----|
| LCP | 最大内容绘制 | < 2.5s | > 4s |
| FID/INP | 交互延迟 | < 100ms | > 300ms |
| CLS | 布局偏移 | < 0.1 | > 0.25 |

## 诊断流程

### Step 1: Lighthouse 审计

```bash
# Chrome DevTools → Lighthouse → 生成报告
# 或命令行
npx lighthouse https://your-site.com --output html --output-path ./report.html
```

重点关注：
- Performance 分数（目标 > 90）
- Opportunities（优化建议，按影响排序）
- Diagnostics（诊断信息）

### Step 2: Coverage 分析

`F12` → Coverage → 点击录制 → 操作页面 → 查看未使用代码

```typescript
// vite.config.ts — 代码分割
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'ui': ['ant-design-vue'],
          'chart': ['@antv/s2', 'three'],
        },
      },
    },
  },
})
```

### Step 3: Network 瀑布图

`F12` → Network → 过滤 `Doc`/`JS`/`CSS`/`Img`

检查：
- JS Bundle 总大小（目标 < 500KB gzipped）
- 是否有阻塞渲染的资源
- 是否利用了缓存（304/200 from cache）

## 优化策略

### LCP 优化（最大内容绘制 < 2.5s）

```typescript
// 1. 关键 CSS 内联
// vite-plugin-critical 提取首屏 CSS 内联到 HTML

// 2. 图片懒加载
<img v-lazy="imageUrl" alt="description" />
// 或原生
<img loading="lazy" src="image.jpg" alt="description" />

// 3. 预加载关键资源
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preload" href="/js/chunk-vendor.js" as="script">

// 4. 骨架屏
<Suspense>
  <template #default><MainContent /></template>
  <template #fallback><SkeletonScreen /></template>
</Suspense>

// 5. 字体优化
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://fonts.gstatic.com" crossorigin>
```

### CLS 优化（布局偏移 < 0.1）

```css
/* 1. 图片/视频容器预留空间 */
.media-container {
  aspect-ratio: 16 / 9;
  width: 100%;
  background: #f5f5f5;
}

/* 2. 字体回退策略 */
body {
  font-family: -apple-system, 'PingFang SC', sans-serif;
}

/* 3. 动态内容区域预留最小高度 */
.dynamic-content {
  min-height: 200px;
}
```

### Bundle 优化

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    target: 'es2020',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,     // 生产环境去掉 console
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor'
          }
          if (id.includes('ant-design')) {
            return 'ui'
          }
        },
      },
    },
    chunkSizeWarningLimit: 500,
  },
})
```

### 缓存策略

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // 文件名带 hash，利于长期缓存
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]',
      },
    },
  },
})

// nginx 配置
// assets/ — Cache-Control: public, max-age=31536000, immutable
// index.html — Cache-Control: no-cache
```

## 持续监控

```typescript
// 在应用中埋点
if ('PerformanceObserver' in window) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log(entry.name, entry.startTime, entry.duration)
    }
  })
  observer.observe({ type: 'largest-contentful-paint', buffered: true })
  observer.observe({ type: 'layout-shift', buffered: true })
  observer.observe({ type: 'first-input', buffered: true })
}
```

## 优化优先级

1. **消除渲染阻塞** — 内联关键 CSS、async/defer JS
2. **图片优化** — WebP/AVIF、懒加载、响应式图片
3. **代码分割** — 路由懒加载、vendor 分离
4. **缓存策略** — hash 文件名 + 长期缓存
5. **字体优化** — preconnect + font-display: swap
6. **服务端** — gzip/brotli、CDN、HTTP/2

## 一句话总结

**先消除渲染阻塞，再优化资源加载，最后做代码分割和缓存** — 按这个顺序效果最大。
