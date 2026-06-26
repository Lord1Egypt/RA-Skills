---
name: dingtalk-group
description: 调用钉钉开放平台 API，提供群聊管理功能（创建群、修改群、解散群、成员管理等）
---

# DingTalk Group Management Skill

通过钉钉开放平台旧版 API（oapi.dingtalk.com）管理内部群会话。

## 前置要求

- 已设置环境变量 `DINGTALK_APP_KEY` 和 `DINGTALK_APP_SECRET`
- 钉钉应用已创建并拥有「钉钉群基础信息管理」权限
- 仅支持企业内部应用（第三方应用不支持）
- 依赖 `@alicloud/dingtalk` 和 `@alicloud/openapi-client`（用于获取 access_token）

## 环境变量

```bash
export DINGTALK_APP_KEY="<your-app-key>"
export DINGTALK_APP_SECRET="<your-app-secret>"
```

---

## 功能列表

### 1. 创建群 (chat/create)

创建内部群会话。适用于项目协作、活动组织等场景。

**脚本路径**: `scripts/create-group.ts`

**用法**

```bash
ts-node scripts/create-group.ts \
  --name "群名称" \
  --owner <ownerUserId> \
  --members <userId1,userId2,...> \
  [--showHistoryType 1] \
  [--searchable 0] \
  [--validationType 0] \
  [--mentionAllAuthority 0] \
  [--managementType 0] \
  [--chatBannedType 0] \
  [--debug]
```

**必填参数**

| 参数 | 说明 |
|------|------|
| --name | 群名称，1~20 个字符 |
| --owner | 群主的 userId，必须在 --members 中 |
| --members | 群成员 userId 列表，逗号分隔，每次最多 40 人，群上限 1000 人 |

**可选参数**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| --showHistoryType | 0 | 新成员是否可查看 100 条历史消息（1=可查看，0=不可） |
| --searchable | 0 | 群是否可被搜索（1=可搜索，0=不可） |
| --validationType | 0 | 入群是否需要验证（1=需要，0=不需要） |
| --mentionAllAuthority | 0 | @all 使用范围（0=所有人，1=仅群主） |
| --managementType | 0 | 群管理类型（0=所有人可管理，1=仅群主） |
| --chatBannedType | 0 | 是否开启群禁言（0=不禁言，1=全员禁言） |
| --debug | - | 输出调试信息（请求参数和完整响应） |

**示例**

```bash
# 创建一个项目协作群
ts-node scripts/create-group.ts \
  --name "项目协作群" \
  --owner manager4220 \
  --members "manager4220,userid1,userid2" \
  --showHistoryType 1

# 创建一个仅群主管理的群（带调试输出）
ts-node scripts/create-group.ts \
  --name "管理通知群" \
  --owner manager4220 \
  --members "manager4220,userid1,userid2,userid3" \
  --managementType 1 \
  --mentionAllAuthority 1 \
  --debug
```

**成功输出**

```json
{
  "success": true,
  "chatid": "chatcf0675d404188xxxx",
  "openConversationId": "cidL+NXxxxx+MSA==",
  "conversationTag": 2
}
```

- `openConversationId` 是群会话唯一标识（推荐使用），后续发消息、管理群时需要此值
- `chatid` 已废弃，请使用 `openConversationId`
- `conversationTag: 2` 表示企业群

**错误输出**

```json
{
  "success": false,
  "error": {
    "code": "49013",
    "message": "群主不能为空"
  }
}
```

**错误码速查**

| errcode | errmsg | 解决方案 |
|---------|--------|----------|
| 43007 | 需要授权 | 检查 access_token / 应用权限 |
| 43009 | 参数需要是 json 格式 | 内部错误，检查脚本 |
| 40031 | 无效的 useridlist 列表 | 检查 userId 是否存在 |
| 40035 | 群名称不能为空 | --name 必填 |
| 400002 | 参数过长 | --name 不超过 20 字符 |
| 49013 | 群主不能为空 | --owner 必填 |
| 49010 | 群成员不能为空 | --members 必填 |
| 49011 | 群成员长度超限 | --members 单次最多 40 人 |
| 1002 | 组织建群超出上限 | 改用会话 2.0 建群 API |

**注意事项**

1. `--owner` 的 userId 必须包含在 `--members` 列表中（脚本会自动校验）
2. 获取 userId 可通过「根据手机号查询用户」接口
3. access_token 由脚本自动获取，无需手动管理
4. 日志信息输出到 stderr，结果 JSON 输出到 stdout，方便管道处理

---

### 2. 修改群信息（待实现）

`POST https://oapi.dingtalk.com/chat/update?access_token=ACCESS_TOKEN`

### 3. 获取群信息（待实现）

`GET https://oapi.dingtalk.com/chat/get?access_token=ACCESS_TOKEN&chatid=CHATID`

### 4. 成员管理（待实现）

- 添加成员：`POST https://oapi.dingtalk.com/chat/member/add`
- 移除成员：`POST https://oapi.dingtalk.com/chat/member/remove`

### 5. 解散群（待实现）

`POST https://oapi.dingtalk.com/chat/disband?access_token=ACCESS_TOKEN`
