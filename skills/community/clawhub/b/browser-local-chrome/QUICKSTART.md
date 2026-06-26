# 浏览器自动化技能 - 快速参考

## 🚀 一键启动

```bash
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\setup.js
```

## 📋 完整工作流程

```bash
# 1. 启动浏览器
node scripts/start-chrome.js

# 2. 配置 OpenClaw（仅首次）
node scripts/configure-browser.js

# 3. 重启 Gateway（仅首次）
openclaw gateway restart

# 4. 检查状态
node scripts/check-status.js

# === 使用浏览器工具 ===
# 在 OpenClaw 中访问网站

# 5. 使用完成后关闭浏览器 ⭐ 重要！
node scripts/stop-chrome.js
```

## 🔧 脚本说明

| 脚本 | 功能 | 何时使用 |
|------|------|---------|
| `setup.js` | 一键配置全流程 | 首次配置或快速启动 |
| `start-chrome.js` | 启动 Chrome 调试模式 | 每次使用前 |
| `stop-chrome.js` | 关闭 Chrome 浏览器 | **使用完成后** |
| `check-status.js` | 检查浏览器状态 | 确认是否运行 |
| `configure-browser.js` | 配置 OpenClaw | 仅首次配置 |

## 💡 最佳实践

### ✅ 推荐做法
- 使用完成后立即关闭浏览器
- 定期检查浏览器状态
- 保存重要数据后再关闭

### ❌ 避免做法
- 让 Chrome 长时间后台运行
- 同时启动多个 Chrome 调试实例
- 不关闭浏览器直接重启系统

## 🎯 常用命令

```bash
# 启动浏览器
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\start-chrome.js

# 检查状态
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\check-status.js

# 关闭浏览器（使用完成后）
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\stop-chrome.js

# 一键配置（包含启动、配置、验证）
node C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\scripts\setup.js
```

## 📁 技能路径

```
C:\Users\Admin\.openclaw\workspace\skills\browser-local-chrome\
├── scripts/
│   ├── setup.js              # 一键配置
│   ├── start-chrome.js       # 启动
│   ├── stop-chrome.js        # 关闭 ⭐
│   ├── configure-browser.js  # 配置
│   └── check-status.js       # 检查
├── SKILL.md                  # 技能文档
├── README.md                 # 使用指南
├── _meta.json                # 元数据
└── package.json              # NPM 配置
```

## 🔒 安全说明

- `dangerouslyAllowPrivateNetwork: true` 允许访问私有网络
- 仅在可信环境中使用
- 使用完成后关闭浏览器可避免安全风险

## 🐛 故障排查

**Chrome 无法关闭**
```bash
# 强制关闭所有 Chrome 进程
taskkill /F /IM chrome.exe
```

**端口被占用**
```bash
# 查找占用端口的进程
netstat -ano | findstr :9222

# 关闭对应进程（替换 PID）
taskkill /F /PID <PID>
```

**配置不生效**
```bash
# 重启 Gateway
openclaw gateway restart
```
