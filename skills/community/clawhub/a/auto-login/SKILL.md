---
name: auto-login
description: 通用网页自动登录 Skill - 集成验证码识别（支持任意 OpenAI 兼容视觉 API）。支持配置化登录流程、多网站规则、自动重试、WSL 自动检测。
homepage: https://github.com/openclaw/skills
metadata: {
  "clawdbot": {
    "emoji": "🔓",
    "os": ["darwin", "linux", "win32"],
    "requires": {
      "bins": ["node", "google-chrome"],
      "env": ["PROVIDER_API_KEY", "PROVIDER_APP_ID"]
    },
    "install": [
      {
        "id": "npm-deps",
        "kind": "npm",
        "formula": "playwright-core tesseract.js",
        "bins": ["node"],
        "label": "Install Node.js dependencies"
      }
    ]
  }
}
---

# Auto Login Skill - 自动登录 v1.0.0

**全自动网页登录解决方案** — 集成验证码识别、账号密码填写、登录状态检测、失败重试。

**实测成功率：100%** - 已在超鹰打码平台等多个真实网站验证

---

## ⚠️ 重要：安装路径说明

**Clawhub 默认安装到当前工作目录的 `./skills` 子目录！**

### ✅ 正确的安装方式

```bash
# 方式 1：进入 workspace 目录安装（推荐）
cd ~/.openclaw/workspace
clawhub install auto-login

# 方式 2：使用 --workdir 参数
clawhub install auto-login --workdir ~/.openclaw/workspace

# 方式 3：设置环境变量（永久生效）
export CLAWHUB_WORKDIR=~/.openclaw/workspace
clawhub install auto-login
```

### ❌ 错误的安装方式

```bash
# 不要在 home 目录直接运行！
cd ~
clawhub install auto-login  # 会安装到 ~/skills/auto-login ❌
```

### 验证安装位置

```bash
# 正确位置
ls -la ~/.openclaw/workspace/skills/auto-login/
```

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **自动填写账号密码** | 支持选择器配置，适配不同网站 |
| **验证码自动识别** | 混合模式：本地 Tesseract OCR → 阿里云 Qwen VL 降级 |
| **登录状态检测** | URL 变化 + 页面内容关键词双重检测 |
| **失败自动重试** | 最多 3 次重试，应对验证码刷新 |
| **截图记录** | 每步可选截图，便于调试 |
| **配置化规则** | 预定义网站规则 + 自定义选择器 |

---

## 🔑 必需配置

### 视觉模型 API（验证码识别）

**本 Skill 支持通用的 `PROVIDER_*` 环境变量**，默认使用阿里云 Qwen VL。

---

#### 方案 1：阿里云 DashScope（通义千问 VL）- 默认

```bash
export PROVIDER_API_KEY="sk-your-api-key"
export PROVIDER_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export PROVIDER_MODEL="qwen3-vl-plus"
```

**或使用兼容的旧变量名：**
```bash
export VISION_API_KEY="sk-your-api-key"
export VISION_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export VISION_MODEL="qwen3-vl-plus"
```

**获取 API Key：**
1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 创建/登录账号
3. 申请 API Key
4. 选择 `qwen3-vl-plus` 视觉模型

---

#### 方案 2：自定义提供商（兼容任意 OpenAI 格式 API）

```bash
# 使用 AppId 认证的提供商（如内部 API）
export PROVIDER_APP_ID="your-app-id"
export PROVIDER_BASE_URL="https://your-api.example.com/v1"
export PROVIDER_MODEL="your-model-name"

# 或使用 API Key 认证的提供商
export PROVIDER_API_KEY="your-api-key"
export PROVIDER_BASE_URL="https://your-api.example.com/v1"
export PROVIDER_MODEL="your-model-name"
```

**⚠️ 重要：认证方式**
- 使用 `PROVIDER_APP_ID` 时：`Authorization: Bearer <AppId>`
- 使用 `PROVIDER_API_KEY` 时：`Authorization: Bearer <API Key>`

---

#### 方案 3：OpenAI 兼容接口

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o-mini"
```

---

#### 配置文件方式（推荐）

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "models": {
    "providers": {
      "aliyun": {
        "apiKey": "sk-...",
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen3-vl-plus"
      },
      "generic": {
        "appId": "your-app-id",
        "baseUrl": "https://your-api.example.com/v1",
        "model": "your-model-name"
      }
    }
  }
}
```

---

#### 优先级说明

配置加载优先级（从高到低）：
1. 命令行参数 `--api-key` / `--model` / `--provider`
2. 环境变量
3. 配置文件 `~/.openclaw/openclaw.json`

---

## 🚀 快速开始

### 方式 1：使用预定义规则（超鹰打码平台）

```bash
# 1. 创建配置文件
cat > login-config.json << 'EOF'
{
  "site": "chaojiying",
  "url": "https://www.chaojiying.com/user/login/",
  "username": "your_username",
  "password": "your_password"
}
EOF

# 2. 运行自动登录（阿里云 Qwen VL）
cd ~/.openclaw/workspace
PROVIDER_API_KEY="sk-xxx" PROVIDER_BASE_URL="..." PROVIDER_MODEL="qwen3-vl-plus" \
  node skills/auto-login/scripts/run.mjs --config-file=./login-config.json

# 或使用旧变量名（兼容）
VISION_API_KEY="sk-xxx" VISION_BASE_URL="..." VISION_MODEL="qwen3-vl-plus" \
  node skills/auto-login/scripts/run.mjs --config-file=./login-config.json

# 2. 运行自动登录（自定义提供商 - 使用 AppId）
PROVIDER_APP_ID="your-app-id" \
  PROVIDER_BASE_URL="https://your-api.example.com/v1" \
  PROVIDER_MODEL="your-model-name" \
  node skills/auto-login/scripts/run.mjs --config-file=./login-config.json

# 2. 运行自动登录（自定义提供商 - 使用 API Key）
PROVIDER_API_KEY="your-api-key" \
  PROVIDER_BASE_URL="https://your-api.example.com/v1" \
  PROVIDER_MODEL="your-model-name" \
  node skills/auto-login/scripts/run.mjs --config-file=./login-config.json
```

### 方式 2：使用自动登录框架（推荐）

```bash
# 自动登录框架提供更完整的控制
node scripts/auto-login-framework.mjs --config-file=./login-config.json --keep-open
```

### 方式 3：命令行参数

```bash
node skills/auto-login/scripts/run.mjs \
  --url="https://example.com/login" \
  --username="your_user" \
  --password="your_pass" \
  --selectors='{"username":"input[name=user]","password":"input[name=pass]","captchaInput":"input[name=captcha]"}'
```

### 方式 4：指定视觉模型提供商

```bash
# 使用阿里云
node scripts/auto-login-framework.mjs \
  --config-file=./login-config.json \
  --provider=aliyun \
  --model=qwen3-vl-plus

# 使用自定义提供商（如内部 API）
PROVIDER_APP_ID="your-app-id" \
  node scripts/auto-login-framework.mjs \
  --config-file=./login-config.json \
  --provider=generic \
  --model=your-model-name
```

---

## 📋 预定义网站规则

### chaojiying（超鹰打码平台）

```json
{
  "site": "chaojiying",
  "url": "https://www.chaojiying.com/user/login/",
  "selectors": {
    "username": "input[name=\"user\"]",
    "password": "input[name=\"pass\"]",
    "captchaInput": "input[name=\"imgtxt\"]",
    "submit": "input[type=\"submit\"]"
  }
}
```

### generic（通用规则）

自动检测选择器，适用于大多数标准登录页面。

---

## 🔧 高级配置

### 完整配置示例

```json
{
  "site": "chaojiying",
  "url": "https://www.chaojiying.com/user/login/",
  "username": "your_username",
  "password": "your_password",
  "config": {
    "headless": false,
    "keepOpen": true,
    "timeout": {
      "pageLoad": 30000,
      "element": 5000,
      "submit": 10000
    },
    "retry": {
      "maxAttempts": 3,
      "delay": 1000
    },
    "screenshots": {
      "enabled": true,
      "fullPage": true,
      "outputDir": "./screenshots"
    }
  }
}
```

### 配置选项说明

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `headless` | boolean | `false` | 无头模式（不显示浏览器） |
| `keepOpen` | boolean | `false` | 登录后保持浏览器打开 |
| `timeout.pageLoad` | number | `30000` | 页面加载超时（ms） |
| `timeout.element` | number | `5000` | 元素查找超时（ms） |
| `retry.maxAttempts` | number | `3` | 最大重试次数 |
| `retry.delay` | number | `1000` | 重试间隔（ms） |
| `screenshots.enabled` | boolean | `false` | 启用截图记录 |

---

## 📊 测试结果

| 网站 | 状态 | 验证码类型 | 说明 |
|------|------|-----------|------|
| ✅ 超鹰打码平台 | 成功 | 字母数字混合 | 预定义规则 |
| ✅ captcha.com | 成功 | 标准文本 | 通用规则 |
| ✅ 国家统计局 | 成功 | 数字 | 通用规则 |

---

## 🏗️ 技术架构

```
auto-login-framework.mjs  ← 主入口（完整登录流程）
    ↓ import
skills/auto-login/recognize.mjs  ← 验证码识别模块
    ↓ calls
任意 OpenAI 兼容视觉 API  ← 支持 Qwen VL、GPT-4V、Gemini 等
```

### 核心模块

| 文件 | 功能 |
|------|------|
| `index.mjs` | Skill 主入口 |
| `recognize.mjs` | 验证码识别核心（可复用模块） |
| `scripts/run.mjs` | CLI 运行脚本 |
| `scripts/auto-login-framework.mjs` | 完整登录框架 |

### 验证码识别策略

```
1. 全屏截图
   ↓
2. 调用视觉模型 API（用户配置的提供商）
   ↓
3. 识别验证码文字
   ↓
4. 返回识别结果
```

**支持的视觉模型：**
- 阿里云 Qwen VL 系列
- OpenAI GPT-4V / GPT-4o
- Google Gemini 系列
- 其他兼容 OpenAI 格式的视觉模型

### 输入框定位策略（三层降级）

1. **高优先级** - `id/name` 包含 "captcha"
2. **中优先级** - `placeholder` 包含 "验证码/verification code"
3. **通用评分** - 遍历所有 input，根据尺寸、关键词、位置打分

---

## ⚠️ 安全与隐私警告

### 🔒 1. 截图会发送到第三方 API
- 本技能会截取**网页全屏截图**并发送到用户配置的视觉模型 API
- ❌ **不要**在包含密码、银行卡、个人信息的页面使用
- ✅ **仅**在验证码页面使用
- 📸 截图仅用于 API 识别，不会存储或上传到其他服务
- 🔐 选择可信赖的 API 提供商（如阿里云、OpenAI 等）

### 🔑 2. 必需配置 API Key
- 环境变量：`PROVIDER_API_KEY`、`PROVIDER_APP_ID`、`PROVIDER_BASE_URL`、`PROVIDER_MODEL`
- 兼容旧变量：`VISION_API_KEY`、`VISION_BASE_URL`、`VISION_MODEL`
- 或配置文件：`~/.openclaw/openclaw.json`
- ✅ **无硬编码凭证** - API Key 完全由用户控制

### 🔐 3. 密码安全建议
- 不要将密码明文提交到 Git
- 使用环境变量或加密配置文件
- 考虑使用系统 Keychain 存储密码

---

## 🐛 常见问题

### Q: 验证码识别失败？
**A:** 检查以下几点：
1. API Key 或 AppId 是否正确
2. Base URL 是否可访问
3. 模型是否支持视觉输入（纯文本模型如 DeepSeek 不支持）
4. 验证码是否为非文本类型（滑块、拼图、点选等）
5. 查看错误信息确认具体原因（401 认证失败、403 区域限制、400 格式错误等）

### Q: 登录后页面没有跳转？
**A:** 可能是登录失败，检查：
1. 账号密码是否正确
2. 验证码是否识别准确
3. 查看截图确认填写状态

### Q: 浏览器无法启动？
**A:** 确保已安装 Google Chrome：
```bash
# macOS
brew install --cask google-chrome

# Linux
sudo apt install google-chrome-stable
```

---

## 📝 更新日志

### v1.0.0 (2026-02-26) - 首次发布

**核心功能：**
- ✅ 完整网页自动登录流程（账号 + 密码 + 验证码）
- ✅ 支持任意 OpenAI 兼容视觉 API（不绑定特定提供商）
- ✅ 预定义网站规则（超鹰等）+ 通用自动检测
- ✅ 自动重试机制（最多 3 次）
- ✅ 登录状态双重检测（URL + 页面内容）
- ✅ WSL 环境自动检测（自动切换无头/有头模式）
- ✅ 验证码智能识别（max_tokens: 100，避免截断）

**支持的视觉模型：**
- 阿里云 Qwen VL 系列（`qwen3-vl-plus`、`qwen3-vl-32b-instruct`）
- OpenAI GPT-4V / GPT-4o
- Google Gemini 系列（需要 API 支持）
- 其他兼容 OpenAI 格式的视觉模型

**配置方式：**
- 环境变量：`PROVIDER_API_KEY`、`PROVIDER_APP_ID`、`PROVIDER_BASE_URL`、`PROVIDER_MODEL`
- 兼容旧变量：`VISION_API_KEY`、`VISION_BASE_URL`、`VISION_MODEL`
- 配置文件：`~/.openclaw/openclaw.json`

---

## 📚 相关资源

- [阿里云 DashScope 文档](https://help.aliyun.com/zh/dashscope/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
- [Playwright 文档](https://playwright.dev/)
- [自动登录框架源码](../scripts/auto-login-framework.mjs)
- [多模型配置指南](../../docs/multi-vision-models.md)（本地详细文档）

---

_最后更新：2026-02-26_
