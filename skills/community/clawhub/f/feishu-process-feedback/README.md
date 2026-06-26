# 📦 feishu-process-feedback

> 飞书消息自动处理与进度反馈技能

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com/skills/feishu-process-feedback)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen.svg)](https://nodejs.org/)

## 🚀 快速开始

### 安装

```bash
# 方式 1: 使用 ClawHub（推荐）
clawhub install feishu-process-feedback

# 方式 2: 手动克隆
git clone https://github.com/your-org/feishu-process-feedback.git ~/.openclaw/skills/feishu-process-feedback
```

### 启动

```bash
cd ~/.openclaw/skills/feishu-process-feedback
node scripts/listener.js
```

### 测试

在飞书上发送任务消息：
```
帮我处理这个任务：
1. 分析数据
2. 生成报告
3. 发送邮件
```

你会收到实时进度反馈！

## ✨ 功能特性

- 🤖 **自动后台监听** - 持续运行，智能识别任务消息
- ⚡ **即时确认** - 5 秒内回复任务确认
- 📊 **进度追踪** - 实时百分比进度更新
- 🔒 **进程隔离** - 每个任务独立进程，互不影响
- 🔄 **错误重试** - 自动重试机制，容错处理
- 💾 **状态持久化** - 重启后继续处理
- 🎯 **类型识别** - 智能识别创建/分析/计算/查询任务

## 📖 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用说明。

## 🔧 配置

通过环境变量配置：

```bash
# 轮询间隔（毫秒）
export FEISHU_POLL_INTERVAL=5000

# 最大并发进程数
export FEISHU_MAX_CONCURRENT=5

# 启用详细日志
export FEISHU_VERBOSE=true

# 启动
node scripts/listener.js
```

完整配置项见 [SKILL.md](SKILL.md#配置选项)。

## 📝 日志

- `.listener.log` - 监听器日志
- `.tasks.log` - 任务处理日志
- `.listener_state.json` - 状态文件

## 🛠️ 开发

### 本地测试

```bash
# 运行测试任务
npm test

# 详细模式启动
npm run start:verbose
```

### 修改任务处理逻辑

编辑 `scripts/process_task.js` 中的 `executeSubtask()` 函数。

### 集成飞书 API

编辑 `scripts/listener.js` 中的 `getLatestMessage()` 函数。

## 📦 发布到 ClawHub

### 前置准备

1. **安装 ClawHub CLI**
   ```bash
   npm install -g clawhub
   ```

2. **登录 ClawHub**
   ```bash
   clawhub login
   ```

3. **验证登录**
   ```bash
   clawhub whoami
   ```

### 发布步骤

1. **进入技能目录**
   ```bash
   cd ~/.openclaw/skills/feishu-process-feedback
   ```

2. **发布技能**
   ```bash
   clawhub publish . \
     --slug feishu-process-feedback \
     --name "Feishu Process Feedback" \
     --version 1.0.0 \
     --changelog "初始版本：基础监听、进度反馈、进程管理"
   ```

3. **验证发布**
   ```bash
   clawhub search feishu-process-feedback
   ```

### 更新技能

```bash
# 修改代码后更新版本
# 1. 更新 package.json 中的 version
# 2. 发布新版本
clawhub publish . \
  --slug feishu-process-feedback \
  --version 1.0.1 \
  --changelog "修复 bug + 性能优化"
```

### 发布最佳实践

- **版本号**：遵循语义化版本（MAJOR.MINOR.PATCH）
- **更新说明**：清晰描述变更内容
- **测试**：发布前充分测试
- **文档**：同步更新 SKILL.md 和 README.md

## ❓ 常见问题

### Q: 监听器启动后立即退出？
A: 检查 Node.js 版本（需要 v14+），查看 `.listener.log` 错误信息。

### Q: 收不到飞书消息？
A: 确保 OpenClaw 飞书通道已正确配置，检查应用权限。

### Q: 任务处理超时？
A: 增加超时时间 `FEISHU_PROCESS_TIMEOUT=600000` 或减少并发数。

### Q: 如何停止监听器？
A: 按 Ctrl+C（前台）或 `kill -SIGTERM <pid>`（后台）。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔗 链接

- [ClawHub](https://clawhub.com)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [飞书开放平台](https://open.feishu.cn/)

---

_Made with ❤️ by OpenClaw Community_
