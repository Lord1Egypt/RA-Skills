---
name: feishu-multi-agent-messaging
description: "飞书群聊多Agent消息通讯。解决多Bot协作时的消息流转问题，支持群聊@通知、私聊消息、用户ID映射。"
version: 1.0.0
author: wulinsquarelikui
license: MIT
tags:
  - feishu
  - multi-agent
  - messaging
  - collaboration
---

# 飞书群聊多Agent消息通讯

> 解决飞书平台上多 Agent 协作时的消息流转问题

## 核心功能

- **用户ID映射** - 解决每个Bot看到的用户open_id不同的问题
- **群聊协作流程** - 6步标准协作流程，确保消息正确流转
- **@用户通知** - 群聊中正确@指定用户
- **私聊消息** - 子Agent以自己的身份发送私聊

## 快速开始

### 1. 配置多个飞书Bot

在 `openclaw.json` 中配置多个飞书账号：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        },
        "coder": {
          "appId": "cli_yyy",
          "appSecret": "yyy"
        },
        "reviewer": {
          "appId": "cli_zzz",
          "appSecret": "zzz"
        }
      }
    }
  }
}
```

### 2. 维护用户ID映射表

每个Bot看到的用户open_id不同，需要维护映射表：

| Bot | accountId | 用户的 open_id |
|-----|-----------|---------------|
| 主Bot | `default` | `ou_xxx` |
| 码农Bot | `coder` | `ou_yyy` |
| 审核Bot | `reviewer` | `ou_zzz` |

### 3. 发送消息时指定accountId

```bash
# 码农Bot发送私聊
message action=send channel=feishu accountId="coder" target="ou_yyy" message="消息内容"

# 审核Bot发送群聊
message action=send channel=feishu accountId="reviewer" target="oc_xxx" message="消息内容"
```

## 核心发现

### 问题：子Agent无法以自己的身份发消息

**根因：**
1. 每个飞书Bot看到的用户open_id不同
2. message tool不支持union_id
3. 私聊发送必须指定accountId参数

**解决方案：**
1. 维护用户ID映射表
2. 发送时使用该Bot看到的用户open_id
3. 用户必须先和Bot建立会话

## 群聊协作流程

```
步骤1：用户群聊 @主Bot 下发命令
步骤2：主Bot群聊 @码农 @审核 下发任务
步骤3：码农、审核群聊回复「收到」
步骤4：码农执行完成，群聊通知审核
步骤5：审核决定打回/通过
步骤6：主Bot @用户 汇报完成
```

**核心指标：所有节点对应的人要把状态发到群里**

## @用户格式

```xml
<at user_id="ou_xxx">用户名</at>
```

## 注意事项

1. **必须指定accountId** - 不指定时会用主Bot的身份发送
2. **必须用正确的open_id** - 每个Bot看到的用户open_id不同
3. **用户必须先和Bot建立会话** - 用户需要先主动给Bot发过消息
4. **群聊协作核心指标** - 所有节点对应的人要把状态发到群里

## 文件结构

```
feishu-multi-agent-messaging/
├── SKILL.md               # 本文件
├── README.md              # 详细说明
├── LICENSE                # MIT许可证
├── docs/
│   ├── architecture.md    # 架构设计
│   ├── id-mapping.md      # ID映射详解
│   ├── workflow.md        # 协作流程
│   └── troubleshooting.md # 问题排查
└── examples/
    ├── openclaw.json      # 配置示例
    └── message-samples.md # 消息示例
```
