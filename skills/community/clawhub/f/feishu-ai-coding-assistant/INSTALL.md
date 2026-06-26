# 📦 安装指南

## 前置要求

- Node.js >= 18.0.0
- npm >= 9.0.0
- Git >= 2.30.0
- OpenClaw >= 1.0.0

## 安装方式

### 方式 1: 通过 ClawHub 安装（推荐）

```bash
# 确保已安装 Claw-CLI
npm install -g @openclaw/claw-cli

# 登录 ClawHub
claw login --token <your-token>

# 安装 Skill
claw skill install feishu-ai-coding-assistant
```

### 方式 2: 从 GitHub 安装

```bash
# 克隆仓库
git clone https://github.com/openclaw-skills/feishu-ai-coding-assistant.git
cd feishu-ai-coding-assistant

# 安装依赖
npm install

# 构建
npm run build

# 在 OpenClaw 中加载
# 将 dist 目录复制到 OpenClaw skills 目录
cp -r dist ~/.openclaw/skills/feishu-ai-coding-assistant/
```

### 方式 3: 本地开发安装

```bash
# 克隆仓库
git clone https://github.com/openclaw-skills/feishu-ai-coding-assistant.git
cd feishu-ai-coding-assistant

# 安装依赖
npm install

# 开发模式运行
npm run dev
```

## 编程工具安装

Skill 会自动检测并提示安装所需的编程工具。你也可以手动安装：

### OpenCode v1.0.0

```bash
npm install -g opencode@1.0.0
opencode --version  # 验证安装
```

### Claude Code v2.0.0

```bash
npm install -g @anthropic-ai/claude-code@2.0.0
claude-code --version  # 验证安装
```

### Codex v3.5.0

```bash
npm install -g openai-codex@3.5.0
codex --version  # 验证安装
```

### Cursor v0.40.0

```bash
npm install -g cursor-cli@0.40.0
cursor --version  # 验证安装
```

### Continue v0.8.0

```bash
npm install -g continue-dev@0.8.0
continue --version  # 验证安装
```

## 验证安装

```bash
# 在飞书中发送命令
/ai-coding help
```

如果返回帮助信息，说明安装成功。

## 故障排查

### 问题 1: Skill 未找到

**错误:** `Skill not found: feishu-ai-coding-assistant`

**解决:**
1. 确认 Skill 已正确安装
2. 检查 OpenClaw 配置
3. 重启 OpenClaw 服务

### 问题 2: 编程工具未找到

**错误:** `Command not found: claude-code`

**解决:**
1. 运行 `/ai-coding install claude-code`
2. 或手动安装（见上方）
3. 确保 npm 全局目录在 PATH 中

### 问题 3: 子 Agent 创建失败

**错误:** `Failed to create subagent`

**解决:**
1. 检查 OpenClaw 权限配置
2. 确保 sessions_spawn 权限已启用
3. 查看 OpenClaw 日志了解详细错误

### 问题 4: 超时错误

**错误:** `Timeout exceeded`

**解决:**
1. 增加 `subagentTimeout` 配置值
2. 将大任务拆分为多个小任务
3. 使用 session 模式代替 run 模式

## 更新 Skill

```bash
# 通过 ClawHub 更新
claw skill update feishu-ai-coding-assistant

# 或手动更新
cd ~/.openclaw/skills/feishu-ai-coding-assistant
git pull
npm install
npm run build
```

## 卸载 Skill

```bash
# 通过 ClawHub 卸载
claw skill uninstall feishu-ai-coding-assistant

# 或手动删除
rm -rf ~/.openclaw/skills/feishu-ai-coding-assistant
```

## 获取帮助

- 📖 文档：https://github.com/openclaw-skills/feishu-ai-coding-assistant
- 🐛 问题反馈：https://github.com/openclaw-skills/feishu-ai-coding-assistant/issues
- 💬 社区讨论：https://clawhub.ai/forum

---

**安装完成后，运行 `/ai-coding` 开始使用！** 🚀
