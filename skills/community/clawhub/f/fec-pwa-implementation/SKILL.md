---
name: fec-pwa-implementation
description: Use when adding or reviewing Progressive Web App capabilities such as installability, manifest metadata, Service Worker registration, Workbox caching, offline fallback, app update prompts, maskable icons, or iOS PWA compatibility. Do not use for general API caching or non-installable performance tuning; Chinese triggers include PWA, offline, Service Worker.
---

# PWA implementation

## Purpose

Make web applications installable, offline and controllable to update.

## Procedure

1. Confirm whether PWA is worth doing: priority is given to mobile/desktop installations, weak network offline, and repeated access scenarios; do not force PWA when it is purely internal backend, has strong real-time streaming media, or only requires ordinary caching.
2. First complete the manifest, icon, theme color and HTML reference; the icon covers at least 192/512, Android needs to be maskable, and iOS needs apple touch icon.
3. Register the Service Worker and design an update prompt; do not forcefully refresh the user page after silently `skipWaiting()`.
4. Use Workbox or framework plug-in to manage precache/runtime cache; sensitive requests such as login, payment, and permission changes must go through the network.
5. Provide offline fallback page and installation prompt UI, and verify initial loading, offline access, update activation, uninstallation and reinstallation.

## Detailed reference

- Load [references/manifest-and-icons.md](references/manifest-and-icons.md) when manifest fields, HTML references, icon requirements, screenshots, and iOS notes are required.
- Load [references/service-worker-workbox.md](references/service-worker-workbox.md) when Service Worker registration, Workbox policy, Vite integration, offline backup and update process are required.

## Constraints

- Service Worker only works under HTTPS (except localhost).
- The caching strategy must distinguish between pages, static resources, APIs and sensitive operations; do not cache login, payment, and permission interfaces.
- Service Worker updates have a lifecycle delay; user-visible refresh prompts take precedence over forced refreshes.
- iOS PWA capabilities are weaker than Android, and installation, push and life cycle must be verified separately.
- The cache has quotas and eviction mechanisms, and max entries / max age must be set.

## Expected Output

Produce installable web apps, offline fallbacks, visible update prompts, and explicit caching policies. Validate Lighthouse PWA, DevTools Application panel, offline mode, update release and mobile installation process.
