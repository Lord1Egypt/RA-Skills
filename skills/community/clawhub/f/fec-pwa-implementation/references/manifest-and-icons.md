# Manifest、图标与安装入口

## Manifest 示例

```json
{
  "name": "我的应用",
  "short_name": "应用",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0052cc",
  "description": "应用描述",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshot-desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

## HTML 引用

```html
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#0052cc" />
<link rel="apple-touch-icon" href="/icon-192.png" />
```

## 检查要点

- `display: "standalone"` 才有接近原生应用的启动体验。
- `purpose: "any maskable"` 避免 Android 自适应图标被裁剪。
- `start_url` 应指向登录后或游客可安全进入的入口。
- `screenshots` 会影响安装对话框质量。
- iOS 仍依赖 `apple-touch-icon`，安装提示也通常需要用户手动完成。
