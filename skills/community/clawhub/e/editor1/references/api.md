# Knot Agent Editor API 参考

BASE_URL: `https://knot.woa.com/apigw`

所有请求需忽略 SSL 校验（`verify=False`），除 `get_config` 外均需 header：`x-knot-api-token: <token>`

---

## 获取 API Token

**POST** `/api/v1/mcpport/get_config`

Headers: `X-Username: {KNOT_USERNAME}`

Request:
```json
{
  "jwt_token": "<KNOT_JWT_TOKEN>",
  "for_knot_api_token": true
}
```

Response:
```json
{
  "code": 0,
  "data": { "knot_api_token": "<token>" },
  "msg": "ok"
}
```

---

## 查询管理的 Agent 列表

**POST** `/openapi/v1/agents/list`

Request:
```json
{
  "agent_id": "",   // 可选，按 id 精确查询
  "scene": "",      // 可选
  "keyword": ""     // 可选，按名称/描述关键字过滤
}
```

Response:
```json
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "id": "agent_xxx",
      "name": "智能体名称",
      "desc": "描述",
      "can_edit": true,
      "welcome_msg": "欢迎语",
      "create_time": "2024-01-01 00:00:00",
      "update_time": "2024-01-01 00:00:00"
    }
  ]
}
```

---

## 查询可用大模型列表

**POST** `/openapi/v1/agents/list_available_llm_model`

Request:
```json
{ "agent_id": "<agent_id>" }
```

Response:
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "models": [
      {
        "display_name": "Claude 3.5 Sonnet",
        "model_name": "claude-3-5-sonnet",
        "desc": "适合复杂推理任务",
        "is_outer_model": false
      }
    ],
    "default_model": "claude-3-5-sonnet"
  }
}
```

---

## 获取 Agent 草稿

**POST** `/openapi/v1/agents/get_draft`

Request:
```json
{ "agent_id": "<agent_id>" }
```

Response:
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "name": "智能体名称",
    "desc": "描述",
    "welcome_msg": "欢迎语",
    "system_prompt": "系统提示词",
    "llm_model": { "name": "claude-3-5-sonnet", "temperature": "0.7" },
    "knowledge_bases": [],
    "mcps": [],
    "rules": [],
    "skills": [],
    "tools": [],
    "sub_agents": [],
    "can_edit": true,
    "is_stale": false   // true 表示草稿基于的版本已过期
  }
}
```

**注意**：`data` 可能为空（null/{}），表示尚无草稿。

---

## 基于最新版本重新生成草稿

**POST** `/openapi/v1/agents/new_draft_from_latest_version`

Request/Response 同 `get_draft`。

**⚠️ 此操作会丢弃当前草稿，执行前需用户确认。**

---

## 修改 Agent 草稿

**POST** `/openapi/v1/agents/modify_draft`

Request（只传需要修改的字段，其余字段不传）:
```json
{
  "agent_id": "<agent_id>",
  "name": "新名称",              // 可选
  "desc": "新描述",              // 可选
  "welcome_msg": "新欢迎语",     // 可选
  "system_prompt": "新系统提示词", // 可选
  "default_llm_model": "claude-3-5-sonnet"  // 可选，使用 model_name
}
```

Response:
```json
{ "code": 0, "msg": "ok" }
```

**修改后必须提示用户**：草稿修改仅在页面调试时生效，若需正式对话生效请发布草稿。

---

## 发布 Agent 草稿

**POST** `/openapi/v1/agents/publish_draft`

Request:
```json
{ "agent_id": "<agent_id>" }
```

Response:
```json
{ "code": 0, "msg": "ok" }
```

**⚠️ 高危操作**：
- 发布后所有用户的正式对话立即使用新版本
- 若草稿 `is_stale=true`，发布将覆盖 agent 最新版本的改动
- 执行前必须获得用户明确确认

---

## 错误处理

- `code != 0`：操作失败，展示 `msg` 字段内容给用户
- 网络异常：提示用户稍后重试
- `can_edit=false`：提示用户无该 agent 的编辑权限
