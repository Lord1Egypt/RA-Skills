---
name: fe-cli-tauri
description: >
  Scaffold a Tauri desktop application. Lightweight alternative to Electron (Rust backend, smaller bundle).
  For macOS/Windows/Linux desktop apps using React/Vue frontend + Rust backend.
  Features auto-update, system tray, native menus, IPC, file system access.
  Triggered as a sub-skill of fe-cli when user wants Tauri/轻量桌面/Rust桌面 project.
---

# fe-cli-tauri — Tauri Desktop App Scaffolding

**Why Tauri over Electron?** Smaller bundle (~5MB vs ~150MB), lower memory usage, Rust backend for performance-critical tasks, native webview (no Chromium bundled).

## Prerequisites

- Rust toolchain: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- System dependencies: https://v2.tauri.app/start/prerequisites/

## Workflow

### Step 1: Gather Options

1. **Framework**: React 19 / Vue 3 / Svelte / Vanilla
2. **Styling/UI**: Tailwind CSS / shadcn/ui + Lucide (React) / shadcn-vue + Vue Bits (Vue) / Ant Design / Element Plus / 纯 SCSS
3. **State Management**: Zustand / Pinia (Vue) / None
4. **i18n**: Yes / No
5. **System Tray**: Yes / No
6. **Auto Update**: Yes (default) / No
7. **Sidecar** (bundled external binary): Yes / No
8. **Project name**: string

### Step 2: Scaffold

```
bun create tauri-app <project-name>
```

Interactive prompt will ask for:
- Frontend language (TypeScript recommended)
- Package manager (bun)
- UI template (React/Vue/Svelte/Vanilla)

Or use flags:
```
bun create tauri-app <project-name> --template react-ts --manager bun
```

### Step 3: Install Additional Dependencies

| Selection | Packages |
|---|---|
| Tailwind CSS | `tailwindcss @tailwindcss/vite` |
| shadcn/ui (React) | `npx shadcn@latest init` + `lucide-react` |
| shadcn-vue (Vue) | `npx shadcn-vue@latest init` + `lucide-vue-next` |
| Zustand | `zustand` |
| Ant Design | `antd @ant-design/icons` |
| Element Plus | `element-plus @element-plus/icons-vue` |
| i18n (React) | `react-i18next i18next` |
| i18n (Vue) | `vue-i18n` |

### Step 4: Project Structure

```
project-name/
├── src/                        # Frontend (React/Vue)
│   ├── components/
│   │   ├── ErrorBoundary.tsx
│   │   ├── PageLoading.tsx
│   │   ├── EmptyState.tsx
│   │   └── ErrorState.tsx
│   ├── pages/
│   │   ├── Home/
│   │   │   └── index.tsx
│   │   └── NotFound.tsx
│   ├── hooks/
│   │   ├── useRequest.ts       # Data fetching hook (from shared layer)
│   │   └── useTauri.ts         # Tauri IPC hooks
│   ├── store/                  # State management (from shared infrastructure)
│   ├── theme/                  # Theme system (from shared infrastructure)
│   ├── config/                 # App constants + routes (from shared infrastructure)
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/                  # Rust backend
│   ├── src/
│   │   ├── main.rs             # Entry point
│   │   ├── lib.rs              # Core logic + IPC commands
│   │   └── commands/           # Custom Tauri commands
│   │       └── mod.rs
│   ├── Cargo.toml              # Rust dependencies
│   ├── tauri.conf.json         # Tauri config (window, permissions, etc.)
│   ├── icons/                  # App icons
│   └── capabilities/
│       └── default.json        # Permission capabilities
├── package.json
├── vite.config.ts
└── .env / .env.development / .env.production
```

### Step 5: Key Templates

**`src-tauri/tauri.conf.json`** (key sections):
```json
{
  "productName": "Your App",
  "version": "0.1.0",
  "identifier": "com.example.app",
  "app": {
    "windows": [
      {
        "title": "Your App",
        "width": 1200,
        "height": 800,
        "minWidth": 800,
        "minHeight": 600,
        "center": true,
        "decorations": true
      }
    ],
    "trayIcon": {
      "iconPath": "icons/icon.png",
      "iconAsTemplate": true
    }
  },
  "plugins": {
    "updater": {
      "active": true,
      "endpoints": ["https://update.example.com/{{target}}/{{arch}}/{{current_version}}"],
      "pubkey": "YOUR_PUBLIC_KEY_HERE"
    }
  }
}
```

**`src-tauri/src/lib.rs`** — IPC commands:
```rust
use tauri::Manager;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! Welcome from Rust.", name)
}

#[tauri::command]
fn get_system_info() -> Result<String, String> {
    Ok(format!("OS: {}", std::env::consts::OS))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![greet, get_system_info])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**`src/hooks/useTauri.ts`** — Tauri IPC hooks:
```typescript
import { invoke } from '@tauri-apps/api/core';
import { useState, useCallback } from 'react';

export function useTauriCommand<T>(command: string) {
  const [data, setData] = useState<T>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error>();

  const execute = useCallback(async (...args: Record<string, unknown>[]) => {
    setLoading(true);
    setError(undefined);
    try {
      const result = await invoke<T>(command, args[0] || {});
      setData(result);
      return result;
    } catch (e) {
      setError(e as Error);
      throw e;
    } finally {
      setLoading(false);
    }
  }, [command]);

  return { data, loading, error, execute };
}
```

**`src-tauri/Cargo.toml`** (key deps):
```toml
[dependencies]
tauri = { version = "2", features = ["tray-icon"] }
tauri-plugin-shell = "2"
tauri-plugin-updater = "2"
tauri-plugin-dialog = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[build-dependencies]
tauri-build = { version = "2" }
```

**`package.json` scripts:**
```json
{
  "scripts": {
    "dev": "tauri dev",
    "build": "tauri build",
    "dev:frontend": "vite",
    "build:frontend": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .ts,.tsx",
    "typecheck": "tsc --noEmit"
  }
}
```

### Step 6: Shared Layer + Infrastructure + Final

Read the following reference files and generate all shared code:
1. `../references/shared-base.md` — services, utils, styles, types, env files
2. `../references/shared-config.md` — vite, tsconfig, eslint, prettier configs
3. `../references/shared-infrastructure.md` — store, theme, i18n, hooks, layouts, auth guard, config/constants

Skip vite.config.ts modifications for env proxy — Tauri uses direct connections.

**Conditional generation** (only if user selected the corresponding option):
- Selected Zustand/Redux Toolkit/Pinia → generate `src/store/`
- Selected i18n → generate `src/locales/`
- **Always generate**: `src/hooks/`, `src/components/AppProvider.tsx`, `src/components/AuthGuard.tsx`, `src/components/GlobalLoading.tsx`, `src/config/`, `src/theme/`

```bash
cd <project-name>
bun install
bun dev      # Starts Vite + Rust backend concurrently
```

Announce: Tauri project ready, dev starts both frontend and Rust backend. Bundle size will be ~5-15MB vs Electron's ~150MB.
