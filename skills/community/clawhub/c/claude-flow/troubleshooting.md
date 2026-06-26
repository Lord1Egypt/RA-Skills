# 故障排查

## 安装问题

---

### 问题 1：`npx ruflo@latest init` 失败

**难度：** 低

**症状：** `npm ERR! network` 或 `ENOTFOUND`

**解决方案：**
```bash
# 清理 npm 缓存后重试
npm cache clean --force
npx ruflo@latest init --wizard

# 检查 Node.js 版本（需要 >= 18）
node --version

# 或使用全局安装
npm install -g ruflo
ruflo init --wizard
```

---

### 问题 2：Claude Code MCP 安装后工具不可用

**难度：** 低

**症状：** 安装后 Claude Code 中看不到 claude-flow 工具

**解决方案：**
- **必须重启 Claude Code** — MCP 不热加载
- 验证 MCP 已注册：`claude mcp list`
- 手动检查配置：`cat ~/.claude/settings.json | grep claude-flow`

```bash
# 重新添加 MCP（如果 list 中没有）
claude mcp add claude-flow --scope user npx ruflo@latest mcp start

# 验证
claude mcp list | grep claude-flow
```

---

### 问题 3：API Key 未配置导致智能体失败

**难度：** 低

**症状：** `AuthenticationError: API key not set` 或智能体立即返回错误

**解决方案：**
```bash
# 检查 API Key
echo $ANTHROPIC_API_KEY  # 应显示 sk-ant-...

# 永久设置（添加到 shell 配置）
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key"' >> ~/.zshrc
source ~/.zshrc

# 或在 Claude-Flow 配置中设置
npx ruflo@latest config set api-key $ANTHROPIC_API_KEY
```

---

## 使用问题

---

### 问题 4：智能体任务超时

**难度：** 中

**症状：** `AgentTimeoutError: Task exceeded timeout` 或智能体长时间无响应

**常见原因：**
- 任务描述太大或太模糊（概率 50%）
- 网络请求超时（概率 30%）
- LLM API 限流（概率 20%）

**解决方案：**
```bash
# 增加超时时间
npx ruflo@latest agent spawn coder \
  --timeout 300 \   # 300 秒超时
  --task "实现用户认证模块"

# 分解大任务
npx ruflo@latest agent spawn coder \
  --task "只实现 JWT 生成函数，不包含其他功能"

# 检查 API 限流
npx ruflo@latest logs --level error --last 20 | grep "rate limit"
```

---

### 问题 5：蜂群智能体结果不一致或互相矛盾

**难度：** 中

**症状：** 多个智能体返回相互矛盾的结果，Queen 无法整合

**常见原因：**
- 任务描述不明确（概率 60%）
- 智能体数量过多导致协调开销过大（概率 40%）

**解决方案：**
```bash
# 减少智能体数量，使任务更聚焦
npx ruflo@latest swarm start \
  --topology hierarchical \
  --agents coder,reviewer \   # 只用 2 个智能体
  --task "实现 X 功能（具体描述预期输入输出）"

# 使用 consensus 配置提高一致性
npx ruflo@latest swarm start \
  --topology hierarchical \
  --consensus weighted \      # Queen 决策权重 3x
  --agents coder,tester,reviewer \
  --task "..."
```

---

### 问题 6：向量记忆数据库损坏

**难度：** 中

**症状：** `SQLite database disk image is malformed` 或记忆查询返回错误

**解决方案：**
```bash
# 查看记忆数据库位置
npx ruflo@latest memory status --verbose

# 备份当前数据库（如果还能访问）
npx ruflo@latest memory export backup-before-repair.json

# 重置记忆数据库（丢失历史学习数据，但能恢复功能）
npx ruflo@latest memory reset --confirm

# 从备份恢复
npx ruflo@latest memory import backup-before-repair.json
```

---

### 问题 7：MCP 服务器频繁断开

**难度：** 高

**症状：** Claude Code 提示 `MCP server disconnected`，频繁重连

**常见原因：**
- MCP 服务器崩溃（内存不足）（概率 40%）
- Node.js 版本不兼容（概率 30%）
- 进程被系统 OOM killer 终止（概率 30%）

**排查步骤：**
```bash
# 手动测试 MCP 服务器
npx ruflo@latest mcp start --debug

# 查看错误日志
npx ruflo@latest logs --level error --last 50

# 检查 Node.js 版本（需要 >= 18）
node --version
```

**解决方案：**
```bash
# 升级 Node.js
nvm install 20
nvm use 20

# 增加 Node.js 内存限制
NODE_OPTIONS="--max-old-space-size=4096" npx ruflo@latest mcp start

# 在 MCP 配置中增加内存
# ~/.claude/settings.json
{
  "mcpServers": {
    "claude-flow": {
      "command": "node",
      "args": ["--max-old-space-size=4096", "/path/to/ruflo/mcp.js"],
      "env": { "ANTHROPIC_API_KEY": "..." }
    }
  }
}
```

---

## 网络/环境问题

---

### 问题 8：Ollama 智能体无法连接本地模型

**难度：** 中

**症状：** `Connection refused: http://127.0.0.1:11434`

**解决方案：**
```bash
# 确认 Ollama 正在运行
ollama serve &
curl http://127.0.0.1:11434/api/tags  # 验证

# 拉取需要的模型
ollama pull llama3.2

# 在 claude-flow 中配置 Ollama
npx ruflo@latest config set provider ollama \
  --url http://127.0.0.1:11434 \
  --model llama3.2
```

---

## 通用诊断

```bash
# 系统诊断
npx ruflo@latest hooks intelligence --status
npx ruflo@latest --version

# 检查 MCP 连接
claude mcp list
npx ruflo@latest mcp status

# 查看最近错误日志
npx ruflo@latest logs --level error --last 20

# 重置到干净状态（保留 API Key）
npx ruflo@latest reset --keep-config
```

**GitHub Issues：** https://github.com/ruvnet/claude-flow/issues

**Discord：** https://discord.com/invite/dfxmpwkG2D
