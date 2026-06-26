# AgentRelay v1.1.0 Release Notes 📨

**发布日期**: 2026-02-23  
**发布平台**: [ClawHub](https://clawhub.ai)  
**Skill ID**: `k976nn4n1ztac37q1enbyh4ykh81ngw2`  
**状态**: ✅ 已发布

---

## 🎯 版本信息

**ClawHub 版本**: 1.1.0  
**本地开发版本**: 1.1.0

---

## 🔒 Key Improvements

Current release improvements:
- ✅ 完全移除硬编码路径
- ✅ 统一使用显式 sender/receiver 元数据
- ✅ 仅保留 `payload.content` 作为事件内容结构
- ✅ 公共接口统一到 `REQ` / `CMP`
- ✅ registry 支持 verify 和 cleanup

### Verification
```bash
# 检查是否有硬编码路径
grep -r "/Users/" skills/agentrelay/*.py
# 应该返回空

# 自定义数据路径（可选）
export OPENCLAW_DATA_DIR=/custom/path
python3 run_relay.py receive "..."
# 会使用 /custom/path/agentrelay/storage/
```

---

## ✨ 核心功能

AgentRelay 是一个**可靠的 Agent 间通信协议**，解决了 `sessions_send` 传输大消息（>30 字符）时容易超时的问题。

### 核心机制

| 传统方式 | AgentRelay 方式 |
|---------|----------------|
| ❌ 直接发大段文本 → ⏰ 超时 | ✅ 写入文件 + 发短指针 → 成功 |
| ❌ 无法验证对方是否读取 | ✅ Secret Code 机制确保已读 |
| ❌ 无日志追溯 | ✅ 完整交易日志（4 条/事件） |

### 消息格式

```
请求：AgentRelay: REQ,event_id,s/file.json,,
确认：AgentRelay: CMP,event_id,,,SECRET123
```

---

## 🚀 安装方法

```bash
clawhub install agentrelay
```

安装后，当你的 agent 收到以 `AgentRelay:` 开头的消息时，会自动处理。

---

## 📦 包含文件

发布到 ClawHub 的文件包括：

1. **SKILL.md** - ClawHub skill 说明文档（含 YAML frontmatter）
2. **SKILL.py** - Skill 入口脚本
3. **__init__.py** - 核心实现（AgentRelayTool 类）
4. **cleanup_relay.py** - 过期事件与 registry 清理脚本
5. **run_relay.py** - 统一执行脚本 ✨推荐
6. **smoke_test.py** - 一键本地验证脚本
7. **README.md** - 项目 README
8. **clawhub.json** - ClawHub manifest 配置文件

**附加材料**:
- README.md - 详细说明
- RELEASE_NOTES.md - 发布记录

---

## 🎮 实战验证

AgentRelay 已改为完全依赖显式元数据路由：
- `sender_agent`
- `receiver_agent`
- `meta.sender`
- `meta.receiver`

验证结果：
- ✅ Agents 自主执行代码
- ✅ Agents 自主记录日志
- ✅ sender/receiver 显示真实 agent ID
- ✅ 完整的 4 步状态机流程
- ✅ 不再依赖事件名中的颜色或 hop 命名

---

## 🔧 Technical Summary

### 修复
- ✅ sender/receiver 从占位符改为真实 agent ID
- ✅ 文件格式统一（仅保留 payload.content）
- ✅ 新增 next_action_plan 字段

### 优化
- ✅ 状态机流程：RECEIVED → CONFIRMED → PREPARING → COMPLETED
- ✅ 完全移除旧兼容层
- ✅ 公共接口统一到 REQ / CMP
- ✅ registry 持久化 secret / sender / receiver，CMP 校验不再依赖事件文件必须存在

[查看当前发布说明](./RELEASE_NOTES.md)

---

## 📊 日志示例

```json
{
  "timestamp": "2026-02-23T02:15:00.000000",
  "event_id": "event_001",
  "type": "REQ",
  "sender": "agent:main:main",      ← 真实身份
  "receiver": "agent:worker:main", ← 真实身份
  "status": "RECEIVED",
  "hint": "Read s/event_001.json",
  "ptr": "s/event_001.json",
  "notes": "File read successfully",
  "next_action_plan": "Will acknowledge and fetch file"  ← 新增
}
```

---

## 🛠️ 快速开始

### 发送消息

```python
from agentrelay import AgentRelayTool

# 准备数据
content = {"task": "写诗", "theme": "春天"}

# 写入共享文件并获取 CSV 消息
result = AgentRelayTool.send("agent:worker:main", "REQ", "event_001", {
    **content,
    "sender_agent": "agent:main:main",
    "receiver_agent": "agent:worker:main"
})

# 发送给目标 agent
sessions_send(
    target='agent:worker:main',
    message=f"AgentRelay: {result['csv_message']}"
)
```

### 接收消息

```bash
python3 run_relay.py receive "AgentRelay: REQ,event_001,s/event_001.json,,"
```

### 完成任务

```bash
python3 run_relay.py complete event_001 "任务完成结果" "agent:main:main"
```

---

## 📞 支持

- **项目主页**: https://clawhub.ai/skills/agentrelay
- **Skill ID**: `k976nn4n1ztac37q1enbyh4ykh81ngw2`
- **作者**: AgentRelay Team
- **许可证**: MIT

---

**📨 Enjoy reliable agent communication!**
