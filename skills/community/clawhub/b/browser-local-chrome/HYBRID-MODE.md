# 浏览器混合方案 - 使用说明

## 🎯 配置策略

**默认：** 官方 Browser (OpenClaw-managed)  
**备用：** 本地 Chrome 技能 (browser-local-chrome)

---

## 📋 方案对比

| 特性 | 官方 Browser | 本地 Chrome 技能 |
|------|-------------|-----------------|
| **配置文件** | `openclaw` | `local-chrome` |
| **端口** | 18800 | 9222 |
| **管理方式** | OpenClaw 自动管理 | 手动启动/关闭 |
| **启动命令** | `openclaw browser start` | `node scripts/start-chrome.js` |
| **关闭命令** | `openclaw browser stop` | `node scripts/stop-chrome.js` |
| **适用场景** | 日常使用（默认） | 官方失败时（备用） |

---

## 🚀 使用方法

### 方案 1：官方 Browser（默认）

```bash
# 启动浏览器
openclaw browser --browser-profile openclaw start

# 检查状态
openclaw browser --browser-profile openclaw status

# 打开网页
openclaw browser --browser-profile openclaw open https://example.com

# 使用完成后关闭 ⭐ 重要！
openclaw browser --browser-profile openclaw stop
```

### 方案 2：本地 Chrome 技能（备用）

```bash
# 启动浏览器
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\start-chrome.js

# 检查状态
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\check-status.js

# 使用完成后关闭 ⭐ 重要！
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\stop-chrome.js
```

### 方案 3：故障排查工具（推荐）

```bash
# 自动检测 + 启动可用的浏览器
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\troubleshoot.js
```

---

## 🔄 工作流程

```
用户要求访问网站
    ↓
尝试官方 Browser (默认)
    ↓
成功？ → 使用官方 Browser
    ↓
失败？ → 切换到本地 Chrome 技能
    ↓
完成任务
    ↓
关闭浏览器 ⭐
```

---

## ⚠️ 重要规则

**使用浏览器完成任务后，必须关闭浏览器！**

- 官方 Browser：`openclaw browser --browser-profile openclaw stop`
- 本地 Chrome：`node scripts/stop-chrome.js`

---

## 🛠️ 故障排查

### 官方 Browser 无法启动

1. 检查 Gateway 是否运行：`openclaw gateway status`
2. 重启 Gateway：`openclaw gateway restart`
3. 切换到本地 Chrome：`node scripts/start-chrome.js`

### 本地 Chrome 无法启动

1. 检查 Chrome 是否安装：`Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"`
2. 检查端口占用：`netstat -ano | findstr :9222`
3. 尝试官方 Browser：`openclaw browser --browser-profile openclaw start`

### 自动故障排查

```bash
node scripts/troubleshoot.js
```

自动检测并启动可用的浏览器方案！

---

## 📁 配置文件位置

**OpenClaw 配置：** `C:\Users\Admin\.openclaw\openclaw.json`

```json5
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",  // 默认使用官方 Browser
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

---

## 🎯 快速参考

| 需求 | 命令 |
|------|------|
| **启动官方 Browser** | `openclaw browser --browser-profile openclaw start` |
| **启动本地 Chrome** | `node scripts/start-chrome.js` |
| **关闭官方 Browser** | `openclaw browser --browser-profile openclaw stop` |
| **关闭本地 Chrome** | `node scripts/stop-chrome.js` |
| **故障排查** | `node scripts/troubleshoot.js` |
| **检查状态** | `openclaw browser status` 或 `node scripts/check-status.js` |

---

**技能路径：** `C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome`
