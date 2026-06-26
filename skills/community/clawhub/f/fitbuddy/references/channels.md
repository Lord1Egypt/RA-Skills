# 提醒渠道配置引导

## 概述

fitbuddy 的定时提醒通过 **OpenClaw cron 任务** 实现。消息通过用户配置的渠道发送。

## 支持的渠道

### 📱 钉钉

**前提：已有钉钉企业机器人。**

引导步骤：
1. 如果用户还没有机器人，引导创建：
   - 登录 [钉钉开发者后台](https://open-dev.dingtalk.com/)
   - 创建企业内部应用 → 启用机器人功能
   - 获取 robotCode
2. 配置钉钉 MCP 服务器：
   - 确保已安装 mcporter：`npm install -g mcporter`
   - 在钉钉开发者后台开通 MCP 服务，获取 MCP 服务器 URL
   - 添加到 mcporter 配置：
     ```
     mcporter config add dingtalk-message --http-url <MCP_URL>
     ```
3. 获取用户 userId（可通过 `mcporter call dingtalk-contacts.get_current_user_profile` 获取）
4. 发送测试消息验证：
   ```
   mcporter call "机器人消息（应用授权）/机器人批量发送单聊消息" \
     --args '{"userIds":["<userId>"],"title":"fitbuddy测试","text":"健身提醒测试成功！🏋️"}'
   ```
5. 将 robotCode、userId、MCP 服务器名记录到 profile.json 的 channel.config

**profile.json channel 配置示例：**
```json
{
  "channel": {
    "type": "dingtalk",
    "config": {
      "mcp_server": "机器人消息（应用授权）",
      "mcp_tool": "机器人批量发送单聊消息",
      "user_id": "153819253621478670"
    }
  }
}
```

### 💬 微信

**前提：已配置 openclaw 微信渠道插件。**

引导步骤：
1. 确认微信插件已安装并正常运行
2. 验证能正常收发消息
3. 渠道类型记录为 "wechat"

### 📨 其他渠道

Telegram、Signal 等，根据用户已配置的 openclaw 插件灵活适配。

## Cron 任务配置

每个提醒项创建一个 OpenClaw cron 任务。

### ⚠️ 常见问题：cron 写入报 "pairing required"

如果创建 cron 任务时报错 `gateway closed (1008): pairing required`，说明 agent 设备只有 `read` 权限，需要批准配对：

1. 检查设备权限：`openclaw devices list`
   - 看 `agent` 设备是否只有 `operator.read`
   - 看 Pending 列表是否有待批准的请求（状态为 `repair`）
2. 批准配对：`openclaw devices approve --latest`
3. 验证：再次尝试创建 cron 任务

**原因分析：** `cron list`/`cron status` 读本地文件不需要 Gateway 连接，但 `cron add`/`cron remove` 写操作需要通过 WebSocket 连接 Gateway，如果 agent 设备没有 `operator.write` 权限就会报 `pairing required`。

### 创建任务

使用 agent 的 cron 工具创建，推荐 `sessionTarget: "main"` + `payload.kind: "systemEvent"`：

```json
{
  "name": "fitbuddy-weight-0830",
  "schedule": {"kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai"},
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "fitbuddy提醒：发送体重记录消息。通过钉钉MCP发送..."
  }
}
```

### 钉钉 MCP HTTP 直调（无需 mcporter）

如果 mcporter 未配置，可直接用 fetch/node 调用钉钉 MCP HTTP endpoint：

```javascript
const baseUrl = 'https://mcp-gw.dingtalk.com/server/<YOUR_MCP_PATH>';
const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};

// 1. Initialize
await fetch(baseUrl, {method: 'POST', headers, body: JSON.stringify({
  jsonrpc: '2.0', id: 1, method: 'initialize',
  params: {protocolVersion: '2024-11-05', capabilities: {},
           clientInfo: {name: 'fitbuddy', version: '1.0'}}
})});

// 2. Send message
await fetch(baseUrl, {method: 'POST', headers, body: JSON.stringify({
  jsonrpc: '2.0', id: 2, method: 'tools/call',
  params: {name: '机器人批量发送单聊消息',
           arguments: {userIds: ['<USER_ID>'], title: 'fitbuddy 提醒',
                      text: '🏋️ 该称体重啦~'}}}
})});
```

提醒消息模板：
- 体重: "🏋️ 早上好！该称体重啦~ 记得记录哦"
- 饮食: "🍽️ 到饭点啦！吃完记得告诉我吃了什么~"
- 喝水: "💧 该喝水啦！记得补充水分~"

## 修改渠道

用户说"修改提醒渠道"时：
1. 展示当前配置
2. 引导重新选择渠道
3. 更新 profile.json
4. 更新所有相关 cron 任务的提示消息
