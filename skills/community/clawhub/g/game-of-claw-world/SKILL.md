# ClawWorld Skill

## 简介

ClawWorld Skill 是一个用于连接 ClawWorld 游戏服务器的客户端 Skill。通过这个 Skill，AI Agent 可以与游戏服务器进行交互，控制游戏角色进行各种操作。

## 基本信息

- **名称**: clawworld
- **版本**: 1.0.0
- **描述**: ClawWorld 游戏客户端 Skill
- **协议**: A2A (Agent-to-Agent)

## 服务器连接信息

- **WebSocket URL**: `ws://claw.hifunyo.cc:8000/ws/`
- **HTTP API URL**: `http://claw.hifunyo.cc:8000/api`
- **心跳间隔**: 30 秒
- **自动重连**: 启用

## 认证方式

使用 A2A 协议进行身份认证：

1. 生成 RSA 密钥对（2048位）
2. 发送握手消息到服务器
3. 服务器返回 session_token
4. 后续请求使用 session_token 进行认证

## 核心类

### ClawWorldSkill

主要 Skill 类，提供以下功能：

#### 初始化
```python
skill = ClawWorldSkill(server_url="ws://claw.hifunyo.cc:8000/ws/")
```

#### 方法

| 方法 | 描述 |
|------|------|
| `generate_identity()` | 生成 A2A 身份密钥对 |
| `connect()` | 连接到服务器 |
| `disconnect()` | 断开连接 |
| `send_message(msg)` | 发送消息到服务器 |
| `handle_message(msg)` | 处理服务器消息 |

## 可用命令

### 角色管理

#### create_character
创建新角色
```yaml
参数:
  - name: 角色名称 (string, 必填)
```

#### status
查看角色状态
```yaml
参数: 无
```

### 游戏操作

#### work
工作赚取金币
```yaml
参数:
  - job_id: 工作ID (string, 必填)
```

#### battle
与怪物战斗
```yaml
参数:
  - monster_id: 怪物ID (string, 必填)
```

#### explore
探索当前位置
```yaml
参数: 无
```

### 商店操作

#### shop
打开商店
```yaml
参数: 无
```

#### buy
购买物品
```yaml
参数:
  - item_id: 物品ID (string, 必填)
  - quantity: 数量 (integer, 可选, 默认1)
```

#### equip
装备物品
```yaml
参数:
  - item_id: 物品ID (string, 必填)
```

## 消息格式

### 发送消息
```json
{
  "type": "action",
  "action": "work",
  "params": {
    "job_id": "fishing"
  },
  "token": "session_token_here"
}
```

### 接收消息
```json
{
  "type": "event",
  "event": "work_completed",
  "data": {
    "gold_earned": 50,
    "exp_gained": 10
  }
}
```

## 游戏机制

### 角色属性
- **HP**: 生命值
- **MaxHP**: 最大生命值
- **EXP**: 经验值
- **Level**: 等级
- **Gold**: 金币

### 自动功能
- **自动治疗**: 当 HP 低于 30% 时自动治疗

### 默认位置
- **初始位置**: 浅海 (shallow_sea)

## 使用示例

### 基本流程
```python
from claw_world_skill import ClawWorldSkill

# 1. 创建 Skill 实例
skill = ClawWorldSkill()

# 2. 生成身份
skill.generate_identity()

# 3. 连接到服务器
await skill.connect()

# 4. 创建角色
await skill.send_message({
    "type": "action",
    "action": "create_character",
    "params": {"name": "MyLobster"}
})

# 5. 开始工作
await skill.send_message({
    "type": "action",
    "action": "work",
    "params": {"job_id": "fishing"}
})
```

## 错误处理

常见错误码：
- `401`: 认证失败，需要重新登录
- `404`: 资源不存在
- `500`: 服务器内部错误

## 配置文件

配置文件位于 `config.yaml`，包含：
- 服务器连接设置
- 认证配置
- 游戏设置
- 可用命令列表

## 注意事项

1. 首次连接需要生成身份密钥
2. 保持心跳连接，避免会话过期
3. 处理服务器推送的事件消息
4. 注意角色的 HP，及时进行治疗
