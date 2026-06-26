# browser-local-chrome 技能安装指南

## 📦 安装包内容

```
browser-local-chrome/
├── scripts/
│   ├── start-chrome.js       # 启动 Chrome
│   ├── stop-chrome.js        # 关闭 Chrome
│   ├── check-status.js       # 检查状态
│   ├── configure-browser.js  # 配置 OpenClaw
│   ├── setup.js              # 一键配置
│   └── troubleshoot.js       # 故障排查
├── SKILL.md                  # 技能说明
├── README.md                 # 使用指南
├── QUICKSTART.md             # 快速参考
├── HYBRID-MODE.md            # 混合方案说明
├── INSTALL.md                # 安装说明（本文件）
├── _meta.json                # 技能元数据
└── package.json              # NPM 配置
```

---

## 🚀 快速安装

### 方法 1：直接复制（推荐）

1. **复制技能文件夹**到目标主机的 OpenClaw 技能目录：
   ```bash
   # Windows
   xcopy /E /I browser-local-chrome %USERPROFILE%\.openclaw\workspace\skills\
   
   # macOS/Linux
   cp -r browser-local-chrome ~/.openclaw/workspace/skills/
   ```

2. **验证安装**：
   ```bash
   cd ~/.openclaw/workspace/skills/browser-local-chrome
   node scripts/check-status.js
   ```

3. **启动浏览器**：
   ```bash
   node scripts/start-chrome.js
   ```

---

### 方法 2：使用 clawhub（如果已配置）

```bash
# 在目标主机上
cd ~/.openclaw/workspace/skills
clawhub install browser-local-chrome --local /path/to/browser-local-chrome
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

## 🔧 安装步骤

### 步骤 1：检查依赖

```bash
# 检查 Node.js
node --version

# 检查 Chrome 是否安装
# Windows
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"

# macOS
ls "/Applications/Google Chrome.app"

# Linux
which google-chrome
```

### 步骤 2：复制技能文件

将 `browser-local-chrome` 文件夹复制到目标位置：

```bash
# 目标路径：~/.openclaw/workspace/skills/browser-local-chrome
```

### 步骤 3：配置 OpenClaw（可选）

如果需要自动配置 OpenClaw：

```bash
cd ~/.openclaw/workspace/skills/browser-local-chrome
node scripts/setup.js
```

### 步骤 4：重启 Gateway

```bash
openclaw gateway restart
```

---

## ⚙️ 自定义配置

### 修改 Chrome 路径

编辑 `_meta.json`：

```json
{
  "config": {
    "chromePath": {
      "win32": "你的 Chrome 路径",
      "darwin": "你的 Chrome 路径",
      "linux": "你的 Chrome 路径"
    }
  }
}
```

### 修改 CDP 端口

编辑 `_meta.json`：

```json
{
  "config": {
    "cdpPort": 9222
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

### 关闭浏览器

```bash
node scripts/stop-chrome.js
```

### 故障排查

```bash
node scripts/troubleshoot.js
```

---

## 🌐 跨平台说明

此技能支持 Windows、macOS 和 Linux：

- **Windows:** 使用 `taskkill` 关闭进程
- **macOS:** 使用 `killall` 关闭进程
- **Linux:** 使用 `killall` 关闭进程

所有脚本会自动检测操作系统并使用正确的命令。

---

## 📝 配置文件位置

| 文件 | Windows | macOS/Linux |
|------|---------|-------------|
| **OpenClaw 配置** | `%USERPROFILE%\.openclaw\openclaw.json` | `~/.openclaw/openclaw.json` |
| **Chrome 用户数据** | `C:\chrome-debug-profile` | `~/chrome-debug-profile` |
| **技能目录** | `%USERPROFILE%\.openclaw\workspace\skills\` | `~/.openclaw/workspace/skills/` |

---

## 🐛 常见问题

### Chrome 无法启动

**Windows:**
```bash
# 检查 Chrome 是否安装
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

**macOS:**
```bash
# 检查 Chrome 是否安装
ls "/Applications/Google Chrome.app"
```

**Linux:**
```bash
# 安装 Chrome
sudo apt install google-chrome-stable
```

### 端口被占用

```bash
# 检查端口占用
# Windows
netstat -ano | findstr :9222

# macOS/Linux
lsof -i :9222

# 关闭占用端口的进程
# Windows
taskkill /F /PID <PID>

# macOS/Linux
kill -9 <PID>
```

### 配置不生效

```bash
# 重启 Gateway
openclaw gateway restart
```

---

## 📞 支持

如有问题，请查看：
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [技能说明文档](SKILL.md)
- [快速参考](QUICKSTART.md)

---

**版本：** 1.1.0  
**作者：** Like Liu  
**许可证：** MIT
