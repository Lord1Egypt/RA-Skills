# 消息发送示例

## 基础概念

发送消息时需要指定以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `channel` | 通道 | `feishu` |
| `accountId` | 飞书账号ID | `default` / `coder` / `reviewer` |
| `target` | 目标（用户或群聊） | `ou_xxx` / `oc_xxx` |
| `message` | 消息内容 | `"消息文本"` |

---

## 私聊消息

### 主Bot 发送私聊

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="ou_user_openid" \
  message="这是主Bot发送的私聊消息"
```

### 码农Bot 发送私聊

```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="ou_user_openid_seen_by_coder_bot" \
  message="码农收到任务，开始执行"
```

### 审核Bot 发送私聊

```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="ou_user_openid_seen_by_reviewer_bot" \
  message="审核完成，结果：通过"
```

**注意：** 不同 Bot 看到的同一用户的 `open_id` 不同！

---

## 群聊消息

### 发送普通群聊消息

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="这是一条群聊消息"
```

### 码农Bot 发送群聊消息

```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="oc_group_id" \
  message="码农：架构设计完成，请审核"
```

---

## @用户消息

### @单个用户

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_user_openid\">用户名</at> 请查看这条消息"
```

### @多个用户

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_coder_openid\">码农</at> <at user_id=\"ou_reviewer_openid\">审核老师</at> 任务分配如下..."
```

---

## 完整协作流程示例

### 步骤1：用户下发命令

用户在群聊输入：
```
@主Bot 帮我写一个登录功能
```

### 步骤2：主Bot 下发任务

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_coder_openid\">码农</at> 任务：实现用户登录功能，请设计架构方案。<at user_id=\"ou_reviewer_openid\">审核老师</at> 码农完成后需要审核"
```

### 步骤3：码农回复收到

```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="oc_group_id" \
  message="收到，任务：实现用户登录功能，预计2小时完成，开始执行"
```

### 步骤3：审核回复收到

```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="oc_group_id" \
  message="收到，等待码农提交架构设计"
```

### 步骤4：码农完成

```bash
message action=send \
  channel=feishu \
  accountId="coder" \
  target="oc_group_id" \
  message="架构设计完成

**方案概述：** JWT + Redis Session
**文档链接：** https://xxx
**请审核老师审核**"
```

### 步骤5：审核通过

```bash
message action=send \
  channel=feishu \
  accountId="reviewer" \
  target="oc_group_id" \
  message="审核通过

**评价：** 架构设计合理，考虑了安全性和扩展性
**建议：** 可以进入开发阶段
**汇报主Bot**"
```

### 步骤6：主Bot 汇报

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_user_openid\">用户</at> 任务完成

**任务：** 实现用户登录功能
**状态：** 架构设计完成，审核通过
**下一步：** 进入开发阶段
**负责人：** 码农
**产出文档：** https://xxx"
```

---

## 错误示例

### ❌ 错误：未指定 accountId

```bash
# 这会用默认身份发送，不是子Agent的身份
message action=send \
  channel=feishu \
  target="ou_xxx" \
  message="消息"
```

### ❌ 错误：使用了错误的 open_id

```bash
# 码农Bot 必须用码农Bot看到的用户open_id
message action=send \
  channel=feishu \
  accountId="coder" \
  target="ou_openid_from_main_bot" \
  message="消息"
```

### ❌ 错误：@格式不正确

```bash
# 缺少引号或格式错误
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="@用户 请查看"  # 错误：没有使用正确的<at>格式
```

### ✅ 正确示例

```bash
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_xxx\">用户</at> 请查看"  # 正确
```
