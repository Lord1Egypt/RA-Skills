# 飞书群聊多Agent消息通讯

> 解决飞书平台上多 Agent 协作时的消息流转问题

## 背景

在使用 OpenClaw 搭建多 Agent 协作系统时，我们发现了一个关键问题：**子 Agent 无法以自己的身份发送私聊消息**。

经过排查，发现根因是：**每个飞书 Bot 看到的用户 open_id 不同**。

这个 Skill 记录了完整的解决方案和最佳实践。

## 核心问题

### 问题描述

当主 Agent 通过 `sessions_spawn` 调度子 Agent 后，子 Agent 调用 `message` tool 发送私聊消息时：

- ❌ 消息以主 Agent 的身份发送
- ❌ 或者直接发送失败

### 根因分析

1. **每个飞书 Bot 看到的用户 open_id 不同**
   - 主Bot 看到的用户：`ou_aaa`
   - 子Bot A 看到的同一用户：`ou_bbb`
   - 子Bot B 看到的同一用户：`ou_ccc`

2. **message tool 不支持 union_id**
   - 只支持 `chatId`、`user:openId`、`chat:chatId` 格式
   - 没有跨 Bot 的统一用户标识

3. **私聊发送必须指定 accountId 参数**
   - 不指定时默认使用主 Bot 身份

## 解决方案

### 1. 维护用户 ID 映射表

```markdown
| Bot | accountId | 用户的 open_id |
|-----|-----------|---------------|
| 主Bot | `default` | `ou_xxx` |
| 码农Bot | `coder` | `ou_yyy` |
| 审核Bot | `reviewer` | `ou_zzz` |
```

### 2. 发送消息时指定正确的参数

**码农Bot 发送私聊：**
```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="ou_yyy" \
  message="消息内容"
```

**审核Bot 发送群聊：**
```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="oc_group_id" \
  message="消息内容"
```

### 3. 群聊 @用户

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_xxx\">用户名</at> 消息内容"
```

## 群聊协作流程

```
┌─────────────────────────────────────────────────────────────┐
│  步骤1：用户群聊 @主Bot 下发命令                              │
├─────────────────────────────────────────────────────────────┤
│  用户：「@主Bot 帮我写一个脚本」                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤2：主Bot 群聊 @码农 @审核 下发任务                       │
├─────────────────────────────────────────────────────────────┤
│  主Bot：「@码农 需求xxx，请设计架构 @审核 完成后审核」        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤3：码农、审核 群聊回复「收到」                           │
├─────────────────────────────────────────────────────────────┤
│  码农：「收到，任务xxx，开始执行」                            │
│  审核：「收到，等待码农提交」                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤4：码农执行完成，群聊通知审核                            │
├─────────────────────────────────────────────────────────────┤
│  码农：「架构设计完成，请审核」                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤5：审核决定打回/通过                                     │
├─────────────────────────────────────────────────────────────┤
│  审核：「审核通过」或「打回重做，问题：xxx」                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤6：主Bot @用户 汇报完成                                  │
├─────────────────────────────────────────────────────────────┤
│  主Bot：「@用户 任务完成，汇总：xxx」                         │
└─────────────────────────────────────────────────────────────┘
```

**核心指标：所有节点对应的人要把状态发到群里**

## 配置示例

### openclaw.json

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "default": {
          "appId": "cli_main_bot",
          "appSecret": "xxx"
        },
        "coder": {
          "appId": "cli_coder_bot",
          "appSecret": "xxx",
          "botName": "码农"
        },
        "reviewer": {
          "appId": "cli_reviewer_bot",
          "appSecret": "xxx",
          "botName": "审核老师"
        }
      },
      "dmPolicy": "allowlist",
      "allowFrom": [
        "ou_user_id_1",
        "ou_user_id_2"
      ]
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "accountId": "default"
      }
    },
    {
      "agentId": "coder",
      "match": {
        "channel": "feishu",
        "accountId": "coder"
      }
    },
    {
      "agentId": "reviewer",
      "match": {
        "channel": "feishu",
        "accountId": "reviewer"
      }
    }
  ]
}
```

## 注意事项

1. **必须指定 accountId** - 不指定时会用主 Bot 的身份发送
2. **必须用正确的 open_id** - 每个 Bot 看到的用户 open_id 不同
3. **用户必须先和 Bot 建立会话** - 用户需要先主动给 Bot 发过消息
4. **白名单配置** - 新增 Bot 时要同步更新 `allowFrom` 列表

## 文件结构

```
feishu-multi-agent-messaging/
├── README.md              # 本文件
├── SKILL.md               # OpenClaw Skill 定义
├── LICENSE                # MIT 许可证
├── .gitignore             # Git 忽略规则
├── docs/
│   ├── architecture.md    # 架构设计
│   ├── id-mapping.md      # ID 映射详解
│   ├── workflow.md        # 协作流程
│   └── troubleshooting.md # 问题排查
└── examples/
    ├── openclaw.json      # 配置示例
    └── message-samples.md # 消息示例
```

## 许可证

MIT License

## 作者

wulinsquarelikui
