# 飞书多 Agent 配置完全指南

## 前置要求

- OpenClaw 2026.3.2+
- Node.js 22+
- 飞书开放平台账号

## 步骤 1：创建飞书应用

### 1.1 进入飞书开放平台

访问：https://open.feishu.cn/app

### 1.2 创建企业自建应用

1. 点击"创建企业自建应用"
2. 填写应用名称（如：墨墨、小媒）
3. 上传应用图标
4. 点击"创建"

### 1.3 添加 Bot 能力

1. 左侧菜单：应用能力 → 添加应用能力
2. 选择"机器人"
3. 点击"添加"

### 1.4 配置权限

1. 左侧菜单：开发配置 → 权限管理
2. 点击"批量导入/导出权限"
3. 导入以下权限：

```json
{
  "im:message": "消息权限",
  "im:message.p2p_msg:readonly": "私聊消息只读",
  "im:message:send_as_bot": "以机器人身份发送消息"
}
```

### 1.5 配置事件订阅（最关键！）

1. 左侧菜单：功能 → 事件订阅
2. 点击"开通事件订阅"
3. **订阅方式：长连接**
4. **添加事件：`接收消息` (im.message)**
5. 保存配置
6. 状态应显示"长连接状态：已连接"

⚠️ **常见错误：只保存长连接但没添加事件！**

### 1.6 发布应用

1. 左侧菜单：应用版本
2. 点击"创建版本"
3. 填写版本号和更新说明
4. 点击"发布"

### 1.7 获取凭证

1. 左侧菜单：凭证与基础信息
2. 记录 App ID 和 App Secret

## 步骤 2：配置 OpenClaw

### 2.1 运行配置向导

```bash
openclaw skill run feishu-multiagent-onboard
```

### 2.2 手动配置（可选）

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "writer": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        },
        "media": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "writer",
      "match": { "channel": "feishu", "accountId": "writer" }
    },
    {
      "agentId": "media",
      "match": { "channel": "feishu", "accountId": "media" }
    }
  ]
}
```

### 2.3 验证配置

```bash
openclaw skill run feishu-multiagent-onboard --check
```

## 步骤 3：启动和配对

### 3.1 重启 Gateway

```bash
openclaw gateway restart
```

### 3.2 批准配对

飞书上会收到配对码消息：

```
OpenClaw：访问未配置。
ou_xxx
配对码：XXXXXX
```

执行批准命令：

```bash
openclaw pairing approve feishu XXXXXX
```

## 步骤 4：测试

在飞书上给机器人发消息，应该能收到回复！

## 常见问题

### Q1: 机器人无法回复

**原因：** 只保存长连接但没添加事件

**解决：** 添加 `接收消息` 事件

### Q2: 配置不生效

**原因：** 使用了环境变量引用

**解决：** 填入实际 App ID/Secret

### Q3: 配对失败

**原因：** 未批准配对码

**解决：** 执行 `openclaw pairing approve`

### Q4: WebSocket 未连接

**原因：** 事件订阅未保存

**解决：** 检查飞书开放平台状态

## 最佳实践

1. **每个 Agent 独立飞书应用** - 不要共用
2. **权限完整导入** - 使用批量导入功能
3. **事件订阅必须添加事件** - 长连接 + 接收消息
4. **配置后备份** - `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`
5. **测试后再发布** - 确保每个 Agent 都能回复

---

*最后更新：2026-03-07*
