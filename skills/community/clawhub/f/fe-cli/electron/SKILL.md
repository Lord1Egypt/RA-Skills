---
name: fe-cli-electron
description: >
  Scaffold an Electron desktop application. For macOS/Windows desktop apps using React/Vue.
  Features auto-update (electron-updater), IPC communication, system tray, native menus.
  For lighter desktop apps, consider Tauri (fe-cli-tauri) instead.
  Triggered as a sub-skill of fe-cli when user wants Electron/桌面端 project.
---

# fe-cli-electron — Electron Desktop App Scaffolding

## Workflow

### Step 1: Gather Options

1. **Framework**: React 19 / Vue 3
2. **Styling**: Tailwind CSS / Ant Design / MUI / 纯 SCSS
3. **CSS Preprocessor**: Sass / Less
4. **State Management**: Zustand / Redux Toolkit / None
5. **Router**: React Router / Vue Router
6. **i18n**: Yes / No
7. **Auto Update**: Yes (default) / No
8. **System Tray**: Yes / No
9. **Testing**: Vitest / None
10. **Pre-commit**: Yes / No
11. **Project name**: string

### Step 2: Scaffold

```
pnpm create vite <project-name> --template react-ts
cd <project-name>
pnpm add -D electron electron-builder concurrently wait-on
pnpm add electron-updater electron-store  # if auto-update selected
```

### Step 3: Project Structure

```
project-name/
├── electron/
│   ├── main.ts              # Main process entry
│   ├── preload.ts            # Preload script (contextBridge)
│   └── updater.ts            # Auto-update logic (if selected)
├── src/                      # Renderer process (React/Vue)
│   ├── components/           # Global components (from shared infrastructure)
│   ├── pages/                # Page components
│   ├── hooks/                # Common hooks (from shared infrastructure)
│   ├── store/                # State management (from shared infrastructure)
│   ├── theme/                # Theme system (from shared infrastructure)
│   ├── config/               # App constants + routes (from shared infrastructure)
│   ├── services/             # API layer (from shared base)
│   ├── utils/                # Utilities (from shared base)
│   ├── styles/               # Global styles (from shared base)
│   ├── electron.d.ts         # IPC type declarations
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
├── electron-builder.yml      # Build config
└── resources/                # App icons
```

### Step 4: Key Templates

**`electron/main.ts`:**
```typescript
import { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage } from 'electron';
import path from 'path';
import { setupUpdater } from './updater';  // if auto-update

let mainWindow: BrowserWindow | null = null;
let tray: Tray | null = null;

const isDev = !app.isPackaged;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    titleBarStyle: 'hiddenInset',  // macOS native title bar
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // System tray (if selected)
  if (process.env.NODE_ENV !== 'linux') {
    const icon = nativeImage.createFromPath(path.join(__dirname, '../resources/icon.png'));
    tray = new Tray(icon.resize({ width: 16, height: 16 }));
    tray.setToolTip('Your App');
    tray.setContextMenu(Menu.buildFromTemplate([
      { label: 'Show', click: () => mainWindow?.show() },
      { type: 'separator' },
      { label: 'Quit', click: () => app.quit() },
    ]));
  }
}

// IPC handlers
ipcMain.handle('get-app-version', () => app.getVersion());
ipcMain.handle('get-platform', () => process.platform);

app.whenReady().then(() => {
  createWindow();
  if (process.env.AUTO_UPDATE !== 'false') setupUpdater(mainWindow!);
  app.on('activate', () => { if (!mainWindow) createWindow(); });
});

app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
```

**`electron/preload.ts`:**
```typescript
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  getPlatform: () => ipcRenderer.invoke('get-platform'),
  onUpdateAvailable: (cb: (info: unknown) => void) => ipcRenderer.on('update-available', (_, info) => cb(info)),
  onUpdateDownloaded: (cb: () => void) => ipcRenderer.on('update-downloaded', () => cb()),
  installUpdate: () => ipcRenderer.send('install-update'),
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close'),
});
```

**`electron/updater.ts`** (if auto-update):
```typescript
import { autoUpdater } from 'electron-updater';
import { BrowserWindow } from 'electron';

export function setupUpdater(mainWindow: BrowserWindow) {
  autoUpdater.autoDownload = false;
  autoUpdater.autoInstallOnAppQuit = true;

  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('update-available', info);
  });

  autoUpdater.on('update-downloaded', () => {
    mainWindow.webContents.send('update-downloaded');
  });

  autoUpdater.on('error', (err) => {
    console.error('Update error:', err);
  });

  // Check for updates every 4 hours
  autoUpdater.checkForUpdatesAndNotify();
  setInterval(() => autoUpdater.checkForUpdatesAndNotify(), 4 * 60 * 60 * 1000);
}
```

**`src/electron.d.ts`:**
```typescript
export {};

declare global {
  interface Window {
    electronAPI: {
      getAppVersion: () => Promise<string>;
      getPlatform: () => Promise<string>;
      onUpdateAvailable: (cb: (info: unknown) => void) => void;
      onUpdateDownloaded: (cb: () => void) => void;
      installUpdate: () => void;
      minimize: () => void;
      maximize: () => void;
      close: () => void;
    };
  }
}
```

**`electron-builder.yml`:**
```yaml
appId: <YOUR_APP_ID>           # e.g. com.yourcompany.yourapp — replace with actual app ID (see parameterization rule in main SKILL.md)
productName: <YOUR_APP_NAME>   # e.g. My App — replace with actual app name
directories:
  output: release
files:
  - dist/**/*
  - electron/**/*
  - package.json
mac:
  target:
    - dmg
    - zip
  artifactName: ${productName}-${version}-mac-${arch}.${ext}
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: build/entitlements.mac.plist
  entitlementsInherit: build/entitlements.mac.plist
win:
  target:
    - nsis
  artifactName: ${productName}-${version}-win-${arch}.${ext}
nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
publish:
  - provider: generic
    url: <YOUR_UPDATE_URL>     # e.g. https://update.yourcompany.com — replace with actual update server URL
```

**`package.json` scripts:**
```json
{
  "main": "electron/main.js",
  "scripts": {
    "dev": "concurrently \"vite\" \"wait-on http://localhost:5173 && electron .\"",
    "dev:renderer": "vite",
    "dev:electron": "electron .",
    "build": "vite build && tsc -p tsconfig.electron.json",
    "build:prod": "vite build && tsc -p tsconfig.electron.json && electron-builder",
    "preview": "vite preview",
    "pack": "electron-builder --dir",
    "dist": "electron-builder"
  }
}
```

### Step 5: Vite Config

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': path.resolve(__dirname, 'src') } },
  base: './',  // Electron loads from file:// so relative paths
  build: { outDir: 'dist' },
  server: { port: 5173 },
});
```

### Step 6: Shared Layer + Infrastructure + Final

Read the following reference files and generate all shared code:
1. `../references/shared-base.md` — services, utils, styles, types, env files
2. `../references/shared-config.md` — vite, tsconfig, eslint, prettier configs
3. `../references/shared-infrastructure.md` — store, theme, i18n, hooks, layouts, auth guard, config/constants

Only generate env files for VITE_ variables (no API proxy needed — Electron uses direct connection).

**Conditional generation** (only if user selected the corresponding option):
- Selected Zustand/Redux Toolkit/Pinia → generate `src/store/`
- Selected i18n → generate `src/locales/`
- **Always generate**: `src/hooks/`, `src/components/AppProvider.tsx`, `src/components/AuthGuard.tsx`, `src/components/GlobalLoading.tsx`, `src/config/`, `src/theme/`

After setup:
```bash
cd <project-name>
pnpm install
pnpm dev
```

Announce: project with Electron + auto-update config, dev starts both Vite and Electron.
