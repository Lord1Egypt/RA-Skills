# 📦 browser-local-chrome 技能发布包

## 📋 发布信息

- **版本：** v1.1.0
- **发布日期：** 2026-04-14
- **作者：** Like Liu
- **许可证：** MIT

---

## 📦 打包文件

**文件名：** `browser-local-chrome-v1.1.0.zip`  
**大小：** ~18 KB  
**内容：** 完整的技能文件夹（不含 node_modules）

---

## 🎯 功能特性

### ✅ 核心功能
- 启动 Chrome 调试模式（CDP 端口 9222）
- 自动配置 OpenClaw 浏览器设置
- 优雅关闭 Chrome 浏览器
- 检查浏览器状态
- 故障排查工具
- 一键配置脚本

### ✅ 跨平台支持
- **Windows:** ✅ 支持（已测试）
- **macOS:** ✅ 支持（自动检测路径）
- **Linux:** ✅ 支持（自动检测路径）

### ✅ 混合方案
- 默认使用官方 Browser（端口 18800）
- 备用本地 Chrome 技能（端口 9222）
- 自动故障切换

---

## 📋 打包内容

```
browser-local-chrome/
├── scripts/
│   ├── start-chrome.js       # 启动 Chrome（跨平台）
│   ├── stop-chrome.js        # 关闭 Chrome（跨平台）
│   ├── check-status.js       # 检查状态
│   ├── configure-browser.js  # 配置 OpenClaw
│   ├── setup.js              # 一键配置
│   ├── troubleshoot.js       # 故障排查
│   ├── simple-package.js     # 打包脚本
│   └── package.js            # 打包脚本（需要 archiver）
├── SKILL.md                  # 技能说明
├── README.md                 # 使用指南
├── QUICKSTART.md             # 快速参考
├── HYBRID-MODE.md            # 混合方案说明
├── INSTALL.md                # 安装说明
├── RELEASE.md                # 发布说明（本文件）
├── _meta.json                # 技能元数据（v1.1.0）
└── package.json              # NPM 配置
```

---

## 🚀 安装方法

### 方法 1：解压 ZIP 文件（推荐）

1. **复制 ZIP 文件**到目标主机
2. **解压**到 OpenClaw 技能目录：
   ```bash
   # Windows
   Expand-Archive -Path browser-local-chrome-v1.1.0.zip `
                  -DestinationPath "$env:USERPROFILE\.openclaw\workspace\skills\"
   
   # macOS/Linux
   unzip browser-local-chrome-v1.1.0.zip \
         -d ~/.openclaw/workspace/skills/
   ```

3. **验证安装**：
   ```bash
   cd ~/.openclaw/workspace/skills/browser-local-chrome
   node scripts/check-status.js
   ```

4. **启动浏览器**：
   ```bash
   node scripts/start-chrome.js
   ```

---

### 方法 2：直接复制文件夹

```bash
# Windows
xcopy /E /I browser-local-chrome "%USERPROFILE%\.openclaw\workspace\skills\"

# macOS/Linux
cp -r browser-local-chrome ~/.openclaw/workspace/skills/
```

---

## 📋 系统要求

| 要求 | Windows | macOS | Linux |
|------|---------|-------|-------|
| **操作系统** | Windows 10+ | macOS 10.15+ | Ubuntu 20.04+ |
| **Chrome 版本** | Chrome 100+ | Chrome 100+ | Chrome 100+ |
| **Node.js** | 14+ | 14+ | 14+ |
| **OpenClaw** | 2026.4.0+ | 2026.4.0+ | 2026.4.0+ |

---

## 🔧 配置说明

### 默认配置

- **CDP 端口：** 9222
- **用户数据目录：**
  - Windows: `C:\chrome-debug-profile`
  - macOS/Linux: `~/chrome-debug-profile`
- **Chrome 路径：** 自动检测（可自定义）

### 自定义配置

编辑 `_meta.json` 文件：

```json
{
  "config": {
    "cdpPort": 9222,
    "userDataDir": {
      "win32": "C:\\chrome-debug-profile",
      "darwin": "~/chrome-debug-profile",
      "linux": "~/chrome-debug-profile"
    },
    "chromePath": {
      "win32": "你的 Chrome 路径",
      "darwin": "你的 Chrome 路径",
      "linux": "你的 Chrome 路径"
    }
  }
}
```

---

## 🎯 使用方式

### 启动浏览器

```bash
node scripts/start-chrome.js
```

### 检查状态

```bash
node scripts/check-status.js
```

### 关闭浏览器 ⭐

```bash
node scripts/stop-chrome.js
```

### 故障排查

```bash
node scripts/troubleshoot.js
```

### 一键配置

```bash
node scripts/setup.js
```

---

## 🌐 混合方案配置

如果需要在同一主机上使用官方 Browser + 本地 Chrome 技能：

### OpenClaw 配置 (`~/.openclaw/openclaw.json`)

```json5
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "ssrfPolicy": {
      "dangerouslyAllowPrivateNetwork": true
    },
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      },
      "local-chrome": {
        "cdpUrl": "http://127.0.0.1:9222",
        "color": "#00AA00",
        "attachOnly": true
      }
    }
  }
}
```

### 使用方式

- **默认：** `openclaw browser --browser-profile openclaw start`
- **备用：** `node scripts/start-chrome.js`

---

## 🐛 常见问题

### Chrome 无法启动

**Windows:**
```bash
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

**macOS:**
```bash
ls "/Applications/Google Chrome.app"
```

**Linux:**
```bash
which google-chrome
# 或安装：sudo apt install google-chrome-stable
```

### 端口被占用

```bash
# Windows
netstat -ano | findstr :9222
taskkill /F /PID <PID>

# macOS/Linux
lsof -i :9222
kill -9 <PID>
```

### 配置不生效

```bash
openclaw gateway restart
```

---

## 📞 支持

- **官方文档：** https://docs.openclaw.ai
- **技能文档：** 查看 `SKILL.md` 和 `README.md`
- **快速参考：** 查看 `QUICKSTART.md`
- **安装说明：** 查看 `INSTALL.md`

---

## 📝 更新日志

### v1.1.0 (2026-04-14)

**新增：**
- ✅ 跨平台支持（Windows/macOS/Linux）
- ✅ 故障排查工具 (`troubleshoot.js`)
- ✅ 混合方案文档 (`HYBRID-MODE.md`)
- ✅ 安装说明文档 (`INSTALL.md`)
- ✅ 打包脚本 (`simple-package.js`)

**改进：**
- 🔧 所有脚本支持跨平台路径
- 🔧 自动检测操作系统
- 🔧 改进错误提示和故障恢复

**修复：**
- 🐛 修复 Windows 路径问题
- 🐛 修复进程关闭逻辑

### v1.0.0 (2026-04-14)

- 🎉 初始版本发布
- ✅ 基础功能实现
- ✅ Windows 平台支持

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件（如有）

---

**打包时间：** 2026-04-14 11:55  
**打包文件：** `browser-local-chrome-v1.1.0.zip`  
**文件大小：** ~18 KB
