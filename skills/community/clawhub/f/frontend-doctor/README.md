# Frontend Doctor

Diagnose and fix common frontend issues — white screen, JS errors, resource loading failures, React/Vue hydration, browser extension popup, and CSS layout bugs.

## Install

```bash
npm install -g @openclaw/frontend-doctor
```

## Usage

```bash
# Scan current directory
frontend-doctor

# Scan a specific project
frontend-doctor ./my-app
```

## Diagnostics

| Module | What it checks |
|---|---|
| White Screen | Missing root element, env vars, lazy imports without Suspense, missing ErrorBoundary |
| JS Errors | Deep property access, unhandled async, useEffect cleanup, TS target |
| Resource Loading | Base path config, mixed content, CSS absolute URLs |
| Hydration | SSR window access, non-deterministic render, dangerouslySetInnerHTML, "use client" |
| CSS Layout | 100vh mobile, overflow hidden, z-index wars, flex truncation, box-sizing |
| Extension Popup | Manifest config, CSP inline scripts, localStorage, deprecated APIs, permissions |

## OpenClaw Skill

This is an [OpenClaw](https://github.com/openclaw/clawhub) skill. Use it with:

```
/frontend-doctor my Next.js page is white screen in production
```

## License

MIT
