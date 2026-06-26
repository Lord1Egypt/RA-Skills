# feishu-multi-account

OpenClaw 多飞书账号配置 - 为子代理配置独立的飞书机器人账号。

## 触发场景

- 用户要配置多个飞书机器人
- 用户要给子代理配置独立的飞书账号
- 用户遇到飞书消息路由问题

## 前置条件

1. **飞书应用**：已在飞书开放平台创建好应用（获取 AppID 和 AppSecret）
2. **OpenClaw**：已安装并正常运行
3. **子代理**：已在 OpenClaw 中创建

## 配置步骤

### Step 1：配置飞书多账号

在 `openclaw.json` 的 `channels.feishu.accounts` 中添加：

```json
"accounts": {
  "main": {
    "appId": "cli_xxx",
    "appSecret": "xxx"
  },
  "sub1": {
    "appId": "cli_yyy",
    "appSecret": "yyy",
    "botname": "Agent B"
  },
  "default": {
    "groupPolicy": "allowlist",
    "groupAllowFrom": ["ou_xxx"],
    "dmPolicy": "pairing"
  }
}
```

### Step 2：配置 Bindings（最重要！）

在 `openclaw.json` **顶层**添加 `bindings`：

```json
"bindings": [
  {
    "agentId": "main",
    "match": {
      "channel": "feishu",
      "accountId": "main"
    }
  },
  {
    "agentId": "sub1",
    "match": {
      "channel": "feishu",
      "accountId": "sub1"
    }
  }
],
```

### Step 3：配置 Agents

```json
"agents": {
  "list": [
    {
      "id": "main",
      "default": true,
      "name": "Agent A"
    },
    {
      "id": "sub1",
      "name": "Agent B",
      "workspace": "/path/to/workspace-sub1"
    }
  ]
}
```

### Step 4：重启 Gateway

```bash
openclaw gateway restart
```

## 验证配置

### 查看 Agent 列表
```bash
openclaw agents list
```

### 测试路由
用子代理的飞书账号发一条消息，看日志：
```bash
tail -f /tmp/openclaw/openclaw-日期.log | grep "dispatching"
```

**成功日志：**
```
feishu[sub1]: dispatching to agent (session=agent:sub1:sub1)
```

**失败日志：**
```
feishu[sub1]: dispatching to agent (session=agent:main:main)
```

## 常见问题

### Q1: 路由一直不生效？

1. 检查 `bindings` 是否放在**顶层**（不是 channels 下面）
2. 检查 `agentId` 和 `accountId` 是否与配置一致
3. 检查是否**两个账号都写了 bindings**

### Q2: 消息发到主账号？

- 很可能是没写主账号的 bindings，默认路由到 main 了

## 关键要点

1. **agentId** = agents.list 中的 id
2. **accountId** = accounts 中的账号 ID
3. **两个账号都要写 bindings**，否则会被默认路由
4. 用**bindings**（不是routing）

## 配置文件示例

```json
{
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "accountId": "main" } },
    { "agentId": "sub1", "match": { "channel": "feishu", "accountId": "sub1" } }
  ],
  "agents": {
    "list": [
      { "id": "main", "default": true, "name": "Agent A" },
      { "id": "sub1", "name": "Agent B", "workspace": "/path/to/workspace-sub1" }
    ]
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "domain": "feishu",
      "accounts": {
        "main": { "appId": "cli_xxx", "appSecret": "xxx" },
        "sub1": { "appId": "cli_yyy", "appSecret": "yyy" }
      }
    }
  }
}
```
