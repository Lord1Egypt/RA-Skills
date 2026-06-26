# 群聊协作流程

## 核心指标

> **所有节点对应的人要把状态发到群里**

这是群聊协作的核心原则。每个参与者在完成自己的任务后，必须在群里通知下一步的人。

## 6步协作流程

### 流程图

```
用户 ──@主Bot──► 主Bot ──@码农@审核──► 码农 ──完成──► 审核 ──通过──► 主Bot ──@用户──► 用户
                                    │                │
                                    │                └──打回──► 码农（重做）
                                    │
                                    └──收到──► 审核收到
```

### 详细步骤

| 步骤 | 角色 | 动作 | 群聊消息示例 |
|------|------|------|-------------|
| 1 | 用户 | @主Bot 下发命令 | 「@主Bot 帮我写一个脚本」 |
| 2 | 主Bot | @码农 @审核 下发任务 | 「@码农 需求xxx @审核 完成后审核」 |
| 3 | 码农 | 回复「收到」 | 「收到，任务xxx，开始执行」 |
| 3 | 审核 | 回复「收到」 | 「收到，等待码农提交」 |
| 4 | 码农 | 执行完成 | 「架构设计完成，请审核」 |
| 5 | 审核 | 审核结果 | 「审核通过」或「打回重做」 |
| 6 | 主Bot | @用户 汇报 | 「@用户 任务完成」 |

## 消息发送示例

### 步骤2：主Bot 下发任务

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_groupId" \
  message="<at user_id=\"ou_coder_openid\">码农</at> 需求：实现用户登录功能。请设计架构方案。<at user_id=\"ou_reviewer_openid\">审核老师</at> 码农完成后需要审核"
```

### 步骤3：码农回复收到

```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="oc_groupId" \
  message="收到，任务：实现用户登录功能，开始执行"
```

### 步骤3：审核回复收到

```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="oc_groupId" \
  message="收到，等待码农提交架构设计"
```

### 步骤4：码农完成

```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="oc_groupId" \
  message="架构设计完成，文档链接：xxx，请审核老师审核"
```

### 步骤5：审核通过

```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="oc_groupId" \
  message="审核通过，架构设计合理，可以进入开发阶段。汇报主Bot"
```

### 步骤5：审核打回

```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="oc_groupId" \
  message="审核不通过，问题：1. 缺少错误处理方案 2. 没有考虑并发场景。请码农修改后重新提交"
```

### 步骤6：主Bot 汇报

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_groupId" \
  message="<at user_id=\"ou_user_openid\">用户</at> 任务完成

**任务：** 实现用户登录功能
**状态：** 架构设计已完成，审核通过
**下一步：** 进入开发阶段
**产出文档：** xxx"
```

## @用户格式

飞书群聊中 @用户 的格式：

```xml
<at user_id="ou_xxx">用户名</at>
```

**注意事项：**
1. `user_id` 必须是当前 Bot 看到的用户 open_id
2. 用户名可以任意填写，但建议用真实名称
3. 格式必须完全正确，否则不会触发 @通知

## 协作模板

### 任务下发模板

```
@执行者 任务：[任务描述]
- 截止时间：[时间]
- 要求：[具体要求]
@审核者 完成后需要审核
```

### 任务收到模板

```
收到，任务：[任务描述]
- 预计完成时间：[时间]
- 开始执行
```

### 任务完成模板

```
任务完成
- 产出：[产出物]
- 文档：[链接]
- 请审核
```

### 审核通过模板

```
审核通过
- 评价：[评价]
- 汇报主Bot
```

### 审核打回模板

```
审核不通过
- 问题：
  1. [问题1]
  2. [问题2]
- 请修改后重新提交
```

## 常见问题

### Q: 群聊消息没有触发 @通知？

A: 检查以下几点：
1. `user_id` 是否正确（必须是当前 Bot 看到的 open_id）
2. 格式是否完全正确（注意引号、尖括号）
3. 是否指定了正确的 `accountId`

### Q: 子 Agent 发的消息显示为主 Agent？

A: 检查是否指定了 `accountId` 参数：
- ❌ 错误：`message action=send channel=feishu target="xxx" message="xxx"`
- ✅ 正确：`message action=send channel=feishu accountId="coder" target="xxx" message="xxx"`

### Q: 私聊发送失败？

A: 检查以下几点：
1. 用户是否已经和该 Bot 建立过会话
2. `target` 是否是该 Bot 看到的用户 open_id
3. 用户是否在白名单中
