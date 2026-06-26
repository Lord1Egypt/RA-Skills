---
name: feishu-bot-manager
description: 管理 OpenClaw 中的飞书机器人账户与路由绑定。用于新增飞书机器人账号、把机器人账户级或群聊级绑定到指定 Agent，或在创建新机器人时顺带创建一个全新的独立 Agent 工作区。用户提到“绑定新飞书机器人”“新增飞书机器人”“把机器人绑到某个 Agent”“给某个群绑定 Agent”时使用。
---

# feishu-bot-manager

飞书多账户机器人配置管理 skill。

## 优先路径

当用户说“绑定一个新的飞书机器人”时，先引导用户去网页创建机器人：

- https://open.feishu.cn/page/openclaw?form=multiAgent

网页会给出 App ID 和 App Secret。拿到这两个值之后，再继续绑定流程。

示例回复：

```text
新机器人先去这里创建：https://open.feishu.cn/page/openclaw?form=multiAgent

拿到 App ID 和 Secret 后发我，我再帮你继续绑定。

*是否要绑定到现有 agent，也可以一起告诉我。*
```

只有在用户明确说“我不想用网页”或“网页打不开”时，才走纯手动流程。

## 两种绑定方式

### 账户级绑定

该飞书账户的所有消息 → 指定 Agent

适合一个机器人专门服务一个 Agent。

生成的 binding 示例：

```json
{ "agentId": "recruiter", "match": { "channel": "feishu", "accountId": "bot-sales" } }
```

### 群聊级绑定

特定群聊的消息 → 指定 Agent

适合把某个群单独分配给某个 Agent。

生成的 binding 示例：

```json
{ "agentId": "recruiter", "match": { "channel": "feishu", "peer": { "kind": "group", "id": "oc_xxx" } } }
```

注意：**群聊级绑定优先级高于账户级绑定**。

## 收集信息顺序

拿到 App ID / App Secret 后，按这个顺序收集：

1. App ID 和 App Secret
2. **先问：绑定到现有 Agent，还是创建新的 Agent？**
   - 如果是现有 Agent：直接问要绑定到哪个 Agent
   - 如果是新 Agent：问新 Agent 的名称、用途、期望的 agentId（可给默认值）
3. 路由方式：账户级 / 群聊级
4. 群聊 ID（仅群聊级需要）
5. 机器人名称（可选）
6. 给出预览，用户确认后执行
7. **重启 Gateway 前再次确认**

确认时的回复里，最下面加一行小字：

```text
*是否要绑定到现有 agent？*
```

## 创建新 Agent 时的额外要求

如果用户选择“创建新的 Agent”，除了写入 OpenClaw 配置，还必须初始化对应工作区文件，并把治理规则写进合适的文件。

创建新 Agent 时，读取并遵守：

- `references/new-agent-governance.md`

重点包括：

- `AGENTS.md`：任务响应规范、复杂任务优先子代理、修改后先验证、skill-vetter 强制审查、问题升级策略、定时任务与稳定性规则
- `SOUL.md`：风格、边界感、群聊克制发言、长任务先告知再执行
- `MEMORY.md`：两层记忆规则、长期信息提炼、必须写文件而不是只靠会话记忆
- `USER.md`：用户偏好、禁忌、长期习惯
- `HEARTBEAT.md`：仅放轻量、幂等、低副作用周期任务
- `TOOLS.md`：环境专属信息
- `.learnings/`：初始化 `LEARNINGS.md`、`ERRORS.md`、`FEATURE_REQUESTS.md`

## 执行流程

1. 检查并备份现有配置
2. 如果需要，创建新的 Agent 工作区与基础文件
3. 添加新账户到 `channels.feishu.accounts`
4. 根据选择的路由模式添加 binding
5. 设置 `session.dmScope` 为 `per-account-channel-peer`
6. 告诉用户配置已改好，**重启 Gateway 前先确认**
7. 重启完成后，提醒用户去新机器人的私聊发送 `/feishu auth`

## 绑定完成后的固定提醒

每次新机器人创建/绑定完成后，都必须提醒用户：

```text
请去新机器人的私聊窗口发送 /feishu auth 进行授权，否则机器人无法正常使用。
```

## 命令行调用

```bash
# 账户级绑定 - 该机器人所有消息都由指定 Agent 处理
openclaw skills run feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --account-id bot-sales \
  --agent-id recruiter \
  --routing-mode account

# 群聊级绑定 - 特定群聊的消息由指定 Agent 处理
openclaw skills run feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --account-id bot-sales \
  --agent-id recruiter \
  --chat-id oc_xxx \
  --routing-mode group
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| --app-id | ✅ | 飞书 App ID (cli_xxx) |
| --app-secret | ✅ | 飞书 App Secret |
| --account-id | ❌ | 账户标识，默认自动生成 |
| --bot-name | ❌ | 机器人名称，默认 `Feishu Bot` |
| --dm-policy | ❌ | DM 策略: open / pairing / allowlist，默认 open |
| --agent-id | ❌ | 要绑定的 Agent ID |
| --chat-id | ❌ | 群聊 ID (oc_xxx)，群聊绑定时需要 |
| --routing-mode | ❌ | 路由模式: account / group，默认 account |

## 注意事项

- 保留现有配置，不覆盖已有主账号配置
- 修改前自动备份 `openclaw.json`
- 绑定新机器人后，重启 Gateway 前必须再次确认
- 完成后必须提醒用户去机器人私聊发送 `/feishu auth`
- 如配置有误，可用备份文件手动恢复
