# Agent Manager - 快速开始指南

## 🎉 已就绪！

Agent Manager 已启动，现在可以自主管理 OpenClaw Agent 了。

---

## 🌐 Web 界面（推荐）

**访问:** http://localhost:3000

### 功能
- ✅ 可视化添加新 Agent
- ✅ 查看所有已注册 Agent
- ✅ 与 Agent 在线对话
- ✅ 删除/管理 Agent

### 使用流程
1. 打开浏览器访问 http://localhost:3000
2. 填写表单创建新 Agent（名称、描述、模型）
3. 在列表中查看已创建的 Agent
4. 点击"对话"按钮与 Agent 聊天

---

## 💻 CLI 命令行

```bash
cd ~/.openclaw/workspace/agent-manager

# 查看所有 Agent
node cli.js list

# 创建新 Agent
node cli.js create Judy "营销外展专家" bailian/qwen3.5-plus

# 与 Agent 对话
node cli.js chat agent-judy

# 删除 Agent
node cli.js delete agent-judy

# 查看帮助
node cli.js help
```

---

## 🔌 API 接口

**基础 URL:** `http://localhost:3000/api`

### 获取 Agent 列表
```bash
curl http://localhost:3000/api/agents
```

### 创建 Agent
```bash
curl -X POST http://localhost:3000/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name":"Judy","description":"营销专家","model":"bailian/qwen3.5-plus"}'
```

### 与 Agent 对话
```bash
curl -X POST http://localhost:3000/api/agents/agent-judy/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好，帮我找 10 个线索"}'
```

### 删除 Agent
```bash
curl -X DELETE http://localhost:3000/api/agents/agent-judy
```

### 健康检查
```bash
curl http://localhost:3000/api/health
```

---

## 📁 文件结构

```
~/.openclaw/workspace/agent-manager/
├── server.js          # Web 服务器
├── cli.js             # 命令行工具
├── package.json       # 依赖配置
├── config.json        # 配置文件
├── README.md          # 文档
└── QUICKSTART.md      # 快速开始（本文件）

~/.openclaw/agents/
└── agent-<name>/      # 每个 Agent 的独立目录
    ├── config.json    # Agent 配置
    ├── IDENTITY.md    # 身份定义
    └── SOUL.md        # 核心原则

~/.openclaw/agents.json  # 所有 Agent 注册表
```

---

## 🔧 配置

编辑 `config.json`:
```json
{
  "openclawGateway": "http://127.0.0.1:18789",  // OpenClaw 地址
  "openclawToken": "你的 Operator Token",        // 认证 Token
  "port": 3000                                   // Web 服务端口
}
```

---

## 🚀 重启服务

```bash
# 停止
pkill -f "node server.js"

# 启动
cd ~/.openclaw/workspace/agent-manager
node server.js &
```

---

## 📝 示例：创建 Judy

**Web 界面:**
1. 访问 http://localhost:3000
2. 填写：
   - 名称：Judy
   - 描述：营销外展专家 - 线索挖掘、冷邮件、LinkedIn 自动化
   - 模型：bailian/qwen3.5-plus
3. 点击"创建 Agent"

**CLI:**
```bash
node cli.js create Judy "营销外展专家" bailian/qwen3.5-plus
```

**API:**
```bash
curl -X POST http://localhost:3000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Judy",
    "description": "营销外展专家",
    "model": "bailian/qwen3.5-plus"
  }'
```

---

## ⚠️ 注意事项

1. **Gateway 必须运行** - 确保 `openclaw gateway status` 显示 running
2. **飞书配对独立** - Agent 创建后，需要在飞书中单独配对
3. **工作区隔离** - 每个 Agent 有独立的工作区目录

---

## 🆘 故障排查

**Web 界面打不开？**
```bash
# 检查服务是否运行
ps aux | grep "node server.js"

# 查看端口占用
lsof -i :3000

# 重启服务
pkill -f "node server.js"
cd ~/.openclaw/workspace/agent-manager
node server.js &
```

**API 返回错误？**
```bash
# 检查 Gateway 状态
openclaw gateway status

# 查看日志
tail -f ~/.openclaw/logs/gateway.log
```

---

**有问题？随时问我！** 🚀
