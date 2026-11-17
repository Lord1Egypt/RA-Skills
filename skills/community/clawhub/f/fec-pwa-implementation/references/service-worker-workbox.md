# Service Worker, Workbox and update flow

## Register Service Worker

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

## Caching strategy

| Policy | Applicable | Note |
| --- | --- | --- |
| `CacheFirst` | Images, fonts, CSS/JS with hash | Expiration policy must be set |
| `NetworkFirst` | Page navigation, low-risk GET API | Downgrade cache only when network fails |
| `StaleWhileRevalidate` | Fonts, avatars, low-risk static data | Users will see old data first |
| `NetworkOnly` | Login, payment, permissions, write operations | Do not enter SW cache |

## Vite integration

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

## Offline and Updates

- Prepare `/offline.html` for uncached pages, don't let users only see browser error pages.
- The update prompt should state "New version is available" and it is up to the user to confirm the refresh.
- Use the DevTools Application panel when debugging and clean up old Service Workers and Cache Storage if necessary.
