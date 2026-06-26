# Skill Installer

📦 **直接从 ClawHub 下载 zip 包安装技能，绕过 API 速率限制**

[![ClawHub](https://img.shields.io/badge/ClawHub-Published-green)](https://clawhub.com/skill-installer)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

---

## ✨ 功能

- ✅ **搜索技能** - 在 ClawHub 搜索技能
- ✅ **安装技能** - 下载并安装技能
- ✅ **批量安装** - 一次安装多个技能
- ✅ **自动去版本号** - 自动去掉版本号（如 todoist-1.2.3 → todoist）
- ✅ **智能重试** - API 失败时自动回退到 CLI
- ✅ **速率限制处理** - 遇到速率限制自动等待重试

---

## 🚀 使用方法

### 搜索技能

```bash
node install.cjs search todoist
```

### 安装单个技能

```bash
node install.cjs install todoist
```

### 批量安装多个技能

```bash
node install.cjs install-batch todoist gog telegram x-research
```

---

## 📋 示例

### 搜索 todoist 相关技能

```bash
$ node install.cjs search todoist

🔍 搜索技能: "todoist"

找到 10 个技能:

1. todoist - Todoist (3.843)
   评分: 3.843 | 版本: 1.0.0
   作者: clawhub

2. todoist-task-manager - Todoist Task Manager (3.649)
   评分: 3.649 | 版本: 1.0.0
   作者: community
```

### 批量安装多个技能

```bash
$ node install.cjs install-batch todoist gog telegram x-research

📦 批量安装 4 个技能

📦 安装技能: todoist
✅ 安装成功
📍 位置: /Users/xufan65/.openclaw/workspace/skills/todoist

⏳ 等待 3 秒...

📦 安装技能: gog
✅ 安装成功
📍 位置: /Users/xufan65/.openclaw/workspace/skills/gog

⏳ 等待 3 秒...

📦 安装技能: telegram
✅ 安装成功
📍 位置: /Users/xufan65/.openclaw/workspace/skills/telegram

⏳ 等待 3 秒...

📦 安装技能: x-research
✅ 安装成功
📍 位置: /Users/xufan65/.openclaw/workspace/skills/x-research

📊 安装结果:

1. todoist: ✅
2. gog: ✅
3. telegram: ✅
4. x-research: ✅

总计: 4/4 成功
```

---

## 🔧 配置

### 默认配置

- **技能安装目录**: `/Users/xufan65/.openclaw/workspace/skills/`
- **临时下载目录**: `/tmp/clawhub-downloads/`
- **批量安装间隔**: 3 秒
- **速率限制等待**: 60 秒

### 环境变量

无需额外环境变量，只需 ClawHub CLI 已登录即可。

---

## 📦 系统要求

- **Node.js**: >= 18.0.0
- **ClawHub CLI**: 已安装并登录
- **系统工具**: curl, unzip, jq

### 安装依赖工具

**macOS**:
```bash
brew install curl unzip jq
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install curl unzip jq
```

---

## 🎯 工作原理

1. **搜索模式**:
   - 调用 ClawHub API 搜索技能
   - 如果 API 失败，回退到 CLI 搜索

2. **安装模式**:
   - 尝试从 ClawHub API 获取技能信息
   - 下载 zip 包
   - 解压到临时目录
   - 去掉版本号
   - 移动到最终目录
   - 如果失败，回退到 CLI 安装

3. **批量模式**:
   - 逐个安装技能
   - 每个之间等待 3 秒
   - 避免触发速率限制

---

## 🛠️ 高级用法

### 只搜索，不安装

```bash
node install.cjs search <关键词>
```

### 安装特定版本的技能

```bash
# 暂不支持，建议使用 ClawHub CLI
npx clawhub install <skill-name> --version <version>
```

### 查看已安装的技能

```bash
ls -la /Users/xufan65/.openclaw/workspace/skills/
```

---

## 🐛 故障排除

### 问题 1: "Cannot find module 'sqlite3'"

**解决方案**: 此技能不需要 sqlite3，忽略此错误。

### 问题 2: "Rate limit exceeded"

**解决方案**: 脚本会自动等待 60 秒后重试，或使用批量安装模式。

### 问题 3: "Not logged in"

**解决方案**:
```bash
npx clawhub login
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发

```bash
git clone https://github.com/openclaw/skill-installer.git
cd skill-installer
npm install
node install.cjs search test
```

---

## 📄 许可证

MIT License

---

## 👤 作者

**OpenClaw**
- Website: https://openclaw.ai
- GitHub: https://github.com/openclaw
- Discord: https://discord.gg/clawd

---

## 🙏 致谢

- [ClawHub](https://clawhub.com) - 技能市场平台
- [OpenClaw](https://openclaw.ai) - AI Agent 平台

---

**如果这个技能对你有帮助，请在 ClawHub 上给个 ⭐ Star！**
