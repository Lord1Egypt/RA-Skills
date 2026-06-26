# 用户 ID 映射详解

## 问题背景

在飞书平台上，每个 Bot（飞书应用）看到的用户 open_id 是不同的。

### 实际案例

假设有一个用户「张三」，三个 Bot 看到的 open_id 如下：

| Bot | accountId | 张三的 open_id |
|-----|-----------|---------------|
| 主Bot | `default` | `ou_aaa111` |
| 码农Bot | `coder` | `ou_bbb222` |
| 审核Bot | `reviewer` | `ou_ccc333` |

**这是同一用户，但每个 Bot 看到的标识完全不同！**

## 为什么会这样？

这是飞书的安全设计：

1. **应用隔离** - 不同飞书应用（Bot）对用户的标识是隔离的
2. **隐私保护** - 防止跨应用追踪用户
3. **安全考虑** - 限制单个应用的数据访问范围

## 解决方案

### 方案一：维护用户 ID 映射表（推荐）

为每个 Bot 维护用户 open_id 映射：

```markdown
## 用户 ID 映射表

| Bot | accountId | 张三的 open_id | 李四的 open_id |
|-----|-----------|---------------|---------------|
| 主Bot | `default` | `ou_aaa111` | `ou_ddd444` |
| 码农Bot | `coder` | `ou_bbb222` | `ou_eee555` |
| 审核Bot | `reviewer` | `ou_ccc333` | `ou_fff666` |
```

**优点：**
- 简单直接
- 不需要额外权限
- 可控性强

**缺点：**
- 需要手动维护
- 新用户需要更新映射表

### 方案二：使用 union_id（需要权限）

飞书提供 union_id，可以跨应用标识同一用户。

**前提条件：**
- 需要申请 union_id 权限
- 需要用户授权

**目前 OpenClaw message tool 不支持 union_id**

## 映射表管理

### 获取用户的 open_id

**方法一：用户发送消息时获取**

当用户给 Bot 发消息时，从消息事件中获取 open_id：

```json
{
  "sender": {
    "sender_id": {
      "open_id": "ou_xxx"
    }
  }
}
```

**方法二：通过 API 获取**

调用飞书 API 获取用户信息。

### 存储映射表

**推荐位置：** `SESSION-STATE.md` 或独立的配置文件

```markdown
## 用户 ID 映射表

| Bot | accountId | 用户A的 open_id | 用户B的 open_id |
|-----|-----------|----------------|----------------|
| 主Bot | `default` | `ou_xxx` | `ou_yyy` |
| 码农Bot | `coder` | `ou_aaa` | `ou_bbb` |
```

## 使用示例

### 码农Bot 给用户A发私聊

```bash
# 1. 查映射表：码农Bot 看到用户A的 open_id 是 ou_aaa
# 2. 发送消息

message action=send \
  channel=feishu \
  accountId="coder" \
  target="ou_aaa" \
  message="码农收到任务，开始执行"
```

### 主Bot 在群聊 @用户A

```bash
# 1. 查映射表：主Bot 看到用户A的 open_id 是 ou_xxx
# 2. 发送消息

message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_group_id" \
  message="<at user_id=\"ou_xxx\">用户A</at> 任务完成"
```

## 最佳实践

1. **集中管理** - 将映射表放在一个文件中，方便维护
2. **及时更新** - 新用户加入时及时更新映射表
3. **验证机制** - 发送消息前验证 open_id 是否正确
4. **错误处理** - 发送失败时检查是否 open_id 错误
