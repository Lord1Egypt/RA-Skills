# 飞书语音回复技能 - 安全说明

## 🔒 安全特性

### 1. 不修改全局文件

**✅ 安全实践**：
- 所有文件操作都在技能目录内
- 不修改系统文件或配置
- 不创建 `/root/.openclaw/workspace/.voice-reply-rules.txt` 等全局文件

**说明**：
- 语音回复规则现在内置在 SKILL.md 中
- 会话启动时自动读取，无需外部文件

### 2. 不创建持久规则

**✅ 安全实践**：
- 规则存储在 SKILL.md 中
- 会话重启时自动重新加载
- 不在系统其他位置创建持久文件

**旧版本问题**：
- ❌ 创建 `/root/.openclaw/workspace/.voice-reply-rules.txt`
- ✅ 新版本：规则在 SKILL.md 内

### 3. 使用公开 API

**✅ 安全实践**：
- 使用 OpenClaw 内置 `message` 工具
- 通过 OpenClaw Gateway 安全发送
- 不依赖未声明的本地 API 服务

**旧版本问题**：
- ❌ 依赖本地 API 服务（http://localhost:5002）
- ❌ 未声明 API 凭据
- ✅ 新版本：使用 OpenClaw 内置工具

### 4. 清晰的依赖说明

**✅ 安全实践**：
- **edge-tts**：Python 包，官方 PyPI 源
  ```bash
  pip3 install edge-tts
  ```
  - 来源：https://pypi.org/project/edge-tts/
  - 许可证：MIT
  - 用途：文本转语音

- **OpenClaw 消息工具**：内置功能
  - OpenClaw 框架内置
  - 用于发送消息到飞书
  - 无需额外配置

**不依赖**：
- ❌ 未声明的本地 API 服务
- ❌ 未声明的凭据或密钥
- ❌ 第三方 API 服务（除了 Edge TTS 官方）

## 📋 依赖审计

### edge-tts（Python 包）

**来源**：https://pypi.org/project/edge-tts/

**许可证**：MIT

**用途**：
- 调用微软 Edge Neural TTS API
- 生成高质量语音文件
- 完全免费，无需 API Key

**安全性**：
- ✅ 只使用官方 PyPI 源
- ✅ 不访问外部服务器（直接连接微软服务器）
- ✅ 不收集用户数据
- ✅ 开源代码，可审计

### OpenClaw 消息工具

**来源**：OpenClaw 内置

**用途**：
- 发送消息到飞书
- 支持文本、图片、音频等多种格式

**安全性**：
- ✅ 通过 OpenClaw Gateway 安全发送
- ✅ 使用已配置的飞书凭据
- ✅ 不暴露密钥或令牌

## 🔐 API 使用说明

### Edge TTS API

**API 类型**：官方微软 Edge API

**访问方式**：
- 通过 edge-tts Python 包
- 直接连接微软服务器
- 无需 API Key 或认证

**数据流**：
```
用户文本 → edge-tts → 微软 Edge API → 语音文件
```

**隐私**：
- ✅ 文本只发送到微软服务器
- ✅ 不存储在第三方服务器
- ✅ 符合微软隐私政策

### OpenClaw 消息工具

**API 类型**：OpenClaw 内置工具

**访问方式**：
- 通过 OpenClaw Gateway
- 使用已配置的飞书应用凭据

**数据流**：
```
语音文件 → OpenClaw Gateway → 飞书 API → 用户收到语音
```

**安全性**：
- ✅ 凭据安全存储在 Gateway 配置中
- ✅ 不在技能中暴露密钥
- ✅ 通过加密通道发送

## 🛡️ 安全最佳实践

### 1. 最小权限原则

**只使用必需的权限**：
- ✅ 只读取技能目录内的文件
- ✅ 只使用 OpenClaw 内置工具
- ✅ 不请求额外的系统权限

### 2. 依赖管理

**使用可信来源**：
- ✅ edge-tts：官方 PyPI
- ✅ OpenClaw：内置框架

**定期更新**：
```bash
pip3 install --upgrade edge-tts
```

### 3. 数据隐私

**不收集用户数据**：
- ✅ 不记录用户消息
- ✅ 不存储生成的语音文件
- ✅ 不上传数据到第三方服务器

### 4. 代码审计

**开源代码**：
- ✅ SKILL.md 可审计
- ✅ edge_tts_async.py 可审计
- ✅ 所有代码都在技能目录内

## 🔍 安全审计清单

### ✅ 已通过的安全检查

- [x] 不修改全局文件
- [x] 不创建持久规则文件
- [x] 不依赖未声明的 API
- [x] 不暴露凭据或密钥
- [x] 使用可信的依赖源
- [x] 不收集用户数据
- [x] 代码可审计

### 📝 安全审计日志

**v1.0.0 (2026-03-11)**：
- ❌ 存在安全问题
  - 修改全局文件
  - 创建持久规则文件
  - 依赖未声明的本地 API

**v1.0.1 (2026-03-11)**：
- ✅ 安全修复
  - 移除全局文件修改
  - 移除持久规则文件
  - 使用 OpenClaw 内置工具
  - 添加安全说明文档

## 📞 安全问题报告

如发现安全问题，请：

1. 通过 GitHub Issues 报告
2. 或发送邮件到：security@openclaw.ai
3. 或在 Discord 社区报告：https://discord.gg/clawd

---

**最后更新**：2026-03-11
**审计状态**：✅ 已通过安全审查
**版本**：v1.0.1
