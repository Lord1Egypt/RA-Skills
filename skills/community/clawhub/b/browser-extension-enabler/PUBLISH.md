# Browser Extension Enabler Skill
# 打包和发布指南

## 📦 Skill 信息

- **名称**: Browser Extension Enabler
- **Slug**: browser-extension-enabler
- **版本**: 1.0.0
- **描述**: Auto-detect and enable OpenClaw Browser Relay Chrome extension

## 📁 文件结构

```
browser-extension-enabler/
├── SKILL.md                           # Skill 文档
├── _meta.json                         # 元数据
└── scripts/
    └── enable-browser-extension.ps1   # 主脚本
```

## ✅ 功能测试结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| 检测扩展连接状态 | ✅ 通过 | 正确识别已连接/未连接状态 |
| 激活 Chrome 窗口 | ✅ 通过 | 使用 WScript.Shell.AppActivate |
| 鼠标移动到指定坐标 | ✅ 通过 | 使用 win-mouse-native skill |
| 鼠标点击 | ✅ 通过 | 左键点击功能正常 |
| 验证连接恢复 | ✅ 通过 | 最多重试 3 次 |

## 🚀 发布步骤

### 1. 登录 ClawHub

```bash
clawhub login
```

按提示输入凭据。

### 2. 发布 Skill

```powershell
# 方法 1: 直接发布
clawhub publish "$env:USERPROFILE\.openclaw\workspace\skills\browser-extension-enabler" `
  --slug browser-extension-enabler `
  --name "Browser Extension Enabler" `
  --version 1.0.0 `
  --changelog "Initial release: Auto-enable OpenClaw Browser Relay extension"

# 方法 2: 先进入目录再发布
cd "$env:USERPROFILE\.openclaw\workspace\skills\browser-extension-enabler"
clawhub publish . `
  --slug browser-extension-enabler `
  --name "Browser Extension Enabler" `
  --version 1.0.0
```

### 3. 验证发布

```bash
# 搜索刚发布的 skill
clawhub search "browser-extension-enabler"
```

## 🔧 本地测试命令

```powershell
# 测试模式（不实际点击）
& "$env:USERPROFILE\.openclaw\workspace\skills\browser-extension-enabler\scripts\enable-browser-extension.ps1" -TestMode

# 实际运行（扩展已连接时会跳过）
& "$env:USERPROFILE\.openclaw\workspace\skills\browser-extension-enabler\scripts\enable-browser-extension.ps1"

# 使用自定义坐标
& "$env:USERPROFILE\.openclaw\workspace\skills\browser-extension-enabler\scripts\enable-browser-extension.ps1" -IconX 1800 -IconY 70
```

## 📋 依赖项

发布前确保依赖项也已发布或可用：
- ✅ `win-mouse-native` - 已存在于 ClawHub

## 📝 发布前检查清单

- [x] 代码测试通过
- [x] SKILL.md 文档完整
- [x] _meta.json 配置正确
- [x] 版本号正确 (1.0.0)
- [x] 依赖项明确列出
- [ ] 已登录 ClawHub
- [ ] 已成功发布
- [ ] 可通过 clawhub search 找到

## 🎯 使用场景

发布后可被其他用户通过以下方式使用：

```bash
# 安装
clawhub install browser-extension-enabler

# 使用（Agent 自动调用）
powershell -File "$env:USERPROFILE\.openclaw\workspace\skills\browser-extension-enabler\scripts\enable-browser-extension.ps1"
```

## 📞 支持

如有问题，请在 ClawHub 提交 issue 或联系作者。

---
*生成时间: 2026-03-02*
