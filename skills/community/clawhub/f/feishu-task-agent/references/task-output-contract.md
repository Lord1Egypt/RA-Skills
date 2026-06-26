# Creator / Members Output Contract

本文件定义 `scripts/resolve_creator_members.py` 的唯一输入输出契约。

## 输入

脚本接收两类输入：

- 语义输入：JSON object
- 运行时上下文：CLI 参数或环境变量

### 语义输入 JSON

这个 JSON 只放需要模型提炼的语义槽位。

```json
{
  "create_as": "unspecified | app | user",
  "explicit_assignee_open_id": null,
  "explicit_follower_open_ids": []
}
```

字段含义：

- `create_as`
  - `unspecified`：上游没有显式改写创建身份
  - `app`：用户明确要求以应用身份创建
  - `user`：用户明确要求以自己的用户身份创建
- `explicit_assignee_open_id`
  - 仅当用户明确指定负责人时填写
  - 必须是用户 `open_id`
- `explicit_follower_open_ids`
  - 仅当用户明确指定关注人时填写
  - 为空数组表示沿用默认 follower 规则

### 运行时上下文

以下值不属于模型要“理解”的业务语义，而是运行时事实：

- `sender_open_id`
  - 从消息上下文的 SenderId 获取
  - 可以通过 `--sender-open-id` 或环境变量 `OPENCLAW_SENDER_OPEN_ID` 传入
- `app_id`
  - 当前 bot / app 的真实 `cli_xxx`
  - 优先级如下：
    - `--app-id`
    - JSON 中的 `app_id`
    - 环境变量 `OPENCLAW_APP_ID`
    - 从 OpenClaw 配置解析当前 Feishu account 的 `appId`
  - 当最终创建身份解析为 `app` 时必填
- 可选：
  - `--account-id`
    - 指定用哪个 Feishu account 解析 `appId`
    - 默认使用 `channels.feishu.defaultAccount`
  - `--config-path`
    - 指定 OpenClaw 配置路径
    - 默认使用 `OPENCLAW_CONFIG_PATH` 或 `~/.openclaw/openclaw.json`

脚本内部兼容从 JSON 里读取 `sender_open_id` / `app_id`，但对 skill 文档和调用流程来说，推荐把它们当作运行时上下文注入，而不是语义提炼结果。

## 成功输出

```json
{
  "ok": true,
  "create_as": "app | user",
  "auth_type": "tenant | user",
  "current_user_id": "ou_xxx",
  "members": [
    { "id": "cli_xxx", "role": "assignee", "type": "app" },
    { "id": "ou_xxx", "role": "follower", "type": "user" }
  ]
}
```

字段说明：

- `create_as`
  - skill 内部语义字段
  - 不直接传给工具
- `auth_type`
  - 直接映射给 `feishu_task_task`
  - `app -> tenant`
  - `user -> user`
- `current_user_id`
  - 始终使用 `sender_open_id`
- `members`
  - 这是最终要传给 `feishu_task_task` 的成员列表
  - agent 不允许在脚本结果之外再增删改默认成员关系

边界说明：

- 本脚本输出只用于任务创建阶段的 `feishu_task_task.create`
- 不用于执行阶段的 `patch`、`append_steps`、`comment`
- 若当前 assignee 为应用，执行阶段写操作应显式使用 `auth_type=tenant`

## 失败输出

```json
{
  "ok": false,
  "error_code": "string",
  "message": "string"
}
```

常见 `error_code`：

- `empty_input`
- `invalid_json`
- `invalid_input`
- `invalid_create_as`
- `missing_sender_open_id`
- `missing_app_id`
- `invalid_user_member_id`
- `invalid_explicit_assignee`
- `invalid_follower_list`
- `invalid_members`
- `missing_member_field`
- `invalid_member_role`
- `invalid_member_type`
- `invalid_app_member_id`
- `invalid_assignee_count`
- `duplicate_member_role`

## 调用方式

推荐通过 stdin 传入 JSON：

```bash
python3 scripts/resolve_creator_members.py <<'EOF'
{
  "create_as": "unspecified",
  "explicit_assignee_open_id": null,
  "explicit_follower_open_ids": []
}
EOF
```

推荐调用方式是“语义 JSON + 运行时参数”：

```bash
python3 scripts/resolve_creator_members.py \
  --sender-open-id "ou_sender" \
  --input-json '{"create_as":"user","explicit_assignee_open_id":null,"explicit_follower_open_ids":[]}'
```

如果当前 OpenClaw 配置里已经有 Feishu account，一般不需要显式传 `--app-id`。脚本会自动从配置解析默认账号的 `appId`。

多账号场景可以显式指定：

```bash
python3 scripts/resolve_creator_members.py \
  --sender-open-id "ou_sender" \
  --account-id "main" \
  --input-json '{"create_as":"app","explicit_assignee_open_id":null,"explicit_follower_open_ids":[]}'
```

也可以用环境变量或显式覆盖：

```bash
OPENCLAW_SENDER_OPEN_ID="ou_sender" \
python3 scripts/resolve_creator_members.py \
  --input-json '{"create_as":"user","explicit_assignee_open_id":null,"explicit_follower_open_ids":[]}'
```

```bash
python3 scripts/resolve_creator_members.py \
  --sender-open-id "ou_sender" \
  --app-id "cli_override" \
  --input-json '{"create_as":"app","explicit_assignee_open_id":null,"explicit_follower_open_ids":[]}'
```
