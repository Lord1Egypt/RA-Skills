# Manifest, icon and installation entrance

## Manifest Example

```json
{
  "name": "My App",
  "short_name": "Application",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0052cc",
"description": "Application description",
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

## HTML Quote

```html
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#0052cc" />
<link rel="apple-touch-icon" href="/icon-192.png" />
```

## Check Points

- `display: "standalone"` will have a startup experience close to native applications.
- `purpose: "any maskable"` prevents Android adaptive icons from being cropped.
- `start_url` should point to a login or entry point that is safe for visitors.
- `screenshots` can affect the quality of the installation dialog.
- iOS still relies on `apple-touch-icon`, and installation prompts usually require users to complete it manually.
