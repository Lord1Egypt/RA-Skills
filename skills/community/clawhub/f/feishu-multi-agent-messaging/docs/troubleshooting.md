# 问题排查指南

## 常见问题

### 1. 子 Agent 无法以自己的身份发消息

**症状：**
- 子 Agent 调用 message tool 发送消息
- 消息显示为主 Agent 发送
- 或者发送失败

**排查步骤：**

```
□ 1. 检查是否指定了 accountId 参数
   - message action=send channel=feishu accountId="coder" ...
   
□ 2. 检查 accountId 是否正确
   - 必须与 openclaw.json 中的配置一致
   
□ 3. 检查该 Bot 是否已配置
   - channels.feishu.accounts 中是否有该 accountId
```

**解决方案：**
```bash
# 正确的发送方式
message action=send \
  channel=feishu \
  accountId="coder" \
  target="ou_xxx" \
  message="消息内容"
```

---

### 2. 私聊消息发送失败

**症状：**
- 调用 message tool 返回错误
- 用户没有收到消息

**排查步骤：**

```
□ 1. 检查用户是否已和该 Bot 建立会话
   - 飞书 Bot 无法主动给用户发消息
   - 用户必须先主动给 Bot 发过消息
   
□ 2. 检查 target 是否正确
   - 必须是该 Bot 看到的用户 open_id
   - 不同 Bot 看到的同一用户的 open_id 不同
   
□ 3. 检查用户是否在白名单
   - channels.feishu.allowFrom 列表
```

**解决方案：**
1. 让用户先给该 Bot 发一条消息
2. 更新用户 ID 映射表
3. 将用户 open_id 添加到白名单

---

### 3. 群聊 @用户 不生效

**症状：**
- 消息发送成功，但没有触发 @通知
- 用户没有被 @

**排查步骤：**

```
□ 1. 检查 @格式是否正确
   - <at user_id="ou_xxx">用户名</at>
   
□ 2. 检查 user_id 是否正确
   - 必须是当前 Bot 看到的用户 open_id
   - 不是用户在另一个 Bot 那边的 open_id
   
□ 3. 检查是否指定了正确的 accountId
   - accountId 决定了用哪个 Bot 的身份发送
```

**解决方案：**
```bash
# 确保 user_id 是当前 Bot 看到的 open_id
message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_groupId" \
  message="<at user_id=\"ou_default_bot看到的用户openid\">用户名</at> 消息内容"
```

---

### 4. 新增 Bot 后无法工作

**症状：**
- 新配置的 Bot 收不到消息
- 发送消息失败

**排查步骤：**

```
□ 1. 检查 Bot 配置
   - appId 和 appSecret 是否正确
   - Bot 是否已发布/启用
   
□ 2. 检查白名单
   - allowFrom 是否包含用户 open_id
   
□ 3. 检查 binding
   - bindings 是否正确配置 agentId 和 accountId 的映射
   
□ 4. 重启 Gateway
   - 配置修改后需要重启生效
```

---

### 5. 模型切换后不生效

**症状：**
- 配置了新的默认模型
- 但实际仍使用旧模型

**排查步骤：**

```
□ 1. 检查配置文件
   - agents.defaults.model.primary 是否正确
   
□ 2. 检查是否有 per-agent 覆盖
   - agents.list[].model 是否覆盖了默认值
   
□ 3. 检查是否有 per-session 覆盖
   - 使用 /model 命令临时切换的，只在当前 session 有效
   
□ 4. 重启 Gateway
   - 配置修改后需要重启生效
```

---

## 调试技巧

### 1. 查看当前配置

```bash
# 查看完整配置
gateway action=config.get

# 查看特定配置项
gateway action=config.schema.lookup path="agents.defaults.model"
```

### 2. 查看运行状态

```bash
# 查看 Gateway 状态
openclaw status

# 查看活跃 session
sessions_list
```

### 3. 测试消息发送

```bash
# 测试群聊消息
message action=send channel=feishu accountId="default" target="oc_xxx" message="测试消息"

# 测试私聊消息
message action=send channel=feishu accountId="coder" target="ou_xxx" message="测试私聊"
```

### 4. 查看日志

```bash
# 查看 Gateway 日志
journalctl -u openclaw-gateway -f

# 或直接查看日志文件
tail -f ~/.openclaw/logs/gateway.log
```

---

## 问题报告模板

如果遇到无法解决的问题，请提供以下信息：

```markdown
## 问题描述
[简要描述问题]

## 复现步骤
1. [步骤1]
2. [步骤2]
3. [步骤3]

## 期望结果
[期望发生什么]

## 实际结果
[实际发生了什么]

## 环境信息
- OpenClaw 版本：
- 飞书 Bot 数量：
- 相关配置（脱敏后）：

## 错误日志
```
[粘贴相关日志]
```
```
