# Service Worker、Workbox 与更新流

## 注册 Service Worker

```ts
export function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;

  window.addEventListener("load", async () => {
    const registration = await navigator.serviceWorker.register("/sw.js", {
      scope: "/",
    });

    registration.addEventListener("updatefound", () => {
      const nextWorker = registration.installing;
      nextWorker?.addEventListener("statechange", () => {
        if (nextWorker.state === "installed" && navigator.serviceWorker.controller) {
          showUpdatePrompt();
        }
      });
    });
  });
}
```

## 缓存策略

| 策略 | 适用 | 注意 |
| --- | --- | --- |
| `CacheFirst` | 带 hash 的图片、字体、CSS/JS | 必须设置过期策略 |
| `NetworkFirst` | 页面导航、低风险 GET API | 网络失败才降级缓存 |
| `StaleWhileRevalidate` | 字体、头像、低风险静态数据 | 用户会先看到旧数据 |
| `NetworkOnly` | 登录、支付、权限、写操作 | 不进入 SW 缓存 |

## Vite 集成

```ts
import { VitePWA } from "vite-plugin-pwa";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: "prompt",
      injectRegister: "auto",
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        runtimeCaching: [
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: "CacheFirst",
            options: {
              cacheName: "images",
              expiration: { maxEntries: 100, maxAgeSeconds: 30 * 24 * 60 * 60 },
            },
          },
        ],
      },
    }),
  ],
});
```

## 离线与更新

- 为未缓存页面准备 `/offline.html`，不要让用户只看到浏览器错误页。
- 更新提示应说明“新版本已可用”，由用户确认刷新。
- 调试时使用 DevTools Application 面板，必要时清理旧 Service Worker 和 Cache Storage。
