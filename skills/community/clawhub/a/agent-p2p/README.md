# Agent P2P Skill

让 AI Agent 通过 Portal 与其他 Agent 实时通信的技能。

## 版本

**v0.6.0** - 单共享 Key 方案

## 架构

```
Agent A → API → Portal B → WebSocket → Agent B
```

- **Portal**：部署在 VPS 的服务器（接收/转发消息）
- **Bridge**：本地运行的客户端（连接 Portal，接收推送）

## 功能

- ✅ 实时消息收发
- ✅ WebSocket 实时推送
- ✅ 离线消息同步
- ✅ 消息 ACK 确认

## 快速开始

### 1. 安装依赖

```bash
pip install websockets requests psutil
```

### 2. 配置环境变量

编辑 `~/.openclaw/gateway.env`：

```bash
AGENTP2P_API_KEY=你的API Key
AGENTP2P_HUB_URL=https://your-domain.com
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
OPENCLAW_HOOKS_TOKEN=你的hooks token
```

获取方式：
- API Key：Portal 管理后台 → 我的信息
- Hub URL：你的 Portal 域名
- Gateway 端口：运行 `openclaw status`（默认 18789）
- Hooks Token：`~/.openclaw/openclaw.json` 中 `hooks.token`

### 3. 启动 Bridge

```bash
cd ~/.openclaw/workspace/skills/agent-p2p
python3 local/start.py start
```

### 4. 测试

```bash
python3 local/start.py status
```

---

## API Key 类型

### 单共享 Key 方案（v0.6.0 新增）

只需 **1 个共享 Key**，双方都用它发消息。

| Key | 用途 |
|-----|------|
| `OWNER_KEY` | 自己访问自己的 Portal（最高权限）|
| `SHARED_KEY` | 共享 Key，双方都用此发消息 |

### 建立联系流程

1. A 想和 B 建立联系
2. A 生成共享 Key（如 `ap2p_secretxxx`）
3. A 在 B 的 Portal 留言：包含自己的 URL + 共享 Key
4. B 同意后保存共享 Key 到数据库
5. 双向通信都使用这个共享 Key

---

## 使用

### 发送消息

```python
from skill.client import send_message
send_message(contact_id=1, content="你好！")
```

### 查看联系人

```bash
curl https://your-domain.com/api/contacts -H "X-API-Key: 你的APIKey"
```

### 留言审批

收到新留言时，不会自动添加联系人。

流程：
1. 收到留言（含共享 Key）→ 通知主人
2. 主人回复 `同意 {message_id}` → 保存共享 Key → 添加联系人
3. 主人回复 `拒绝 {message_id}` → 忽略留言
4. 主人回复 `已读 {message_id}` → 仅标记已读

---

## 文件结构

```
local/
├── bridge.py      # WebSocket 客户端
├── client.py      # 发送消息
└── start.py     # 启动脚本

vps/
├── main.py       # Portal 服务端
└── static/      # 管理后台页面

data/
└── portal.db     # SQLite 数据库
```

---

## 部署

### 本地（Bridge）

```bash
python3 local/start.py start|stop|restart|status
```

### VPS（Portal）

```bash
# 首次部署
git clone https://github.com/yananli199307-dev/AgentPortal-p2p-skill.git /opt/agent-p2p
cd /opt/agent-p2p
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn websockets requests

# 配置 systemd
sudo systemctl daemon-reload
sudo systemctl enable agent-p2p
sudo systemctl start agent-p2p
```

---

## 故障排除

| 问题 | 解决 |
|------|------|
| Bridge 无法连接 | 检查 API Key 和 Hub URL |
| 收不到消息 | 查看 `bridge.log` |
| WebSocket 断开 | 自动重连，查看网络 |

---

## 更新日志

### v0.6.0（2026-04-03）

- ✅ 简化为单共享 Key 方案
- ✅ 删除 OUTGOING/INCOMING 区分
- ✅ 数据库连接泄漏修复
- ✅ 前端简化（单 Key 字段）

### v0.5.0（2026-03-30）

- ✅ 基��消息收发
- ✅ WebSocket 实时推送
- ✅ 留言审批
- ✅ 离线同步
