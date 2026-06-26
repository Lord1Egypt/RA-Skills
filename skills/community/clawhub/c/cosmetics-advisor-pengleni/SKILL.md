---
name: cosmetics-advisor-pengleni
description: "Use when users need Pengleni beauty assistant capabilities via SMS login/session APIs, including AI virtual try-on, makeup analysis, style transfer, product recommendation, and beauty knowledge Q&A with HTML message exchange."
---

# SKILL: Pengleni Login Session HTML Bridge

## 0. Quick Checklist For Agent

在真正发请求前，先逐项确认：

1. `CLAWHUB_SKILL_TOKEN` 已配置。
2. 用户已提供合法手机号。
3. 如果要发消息，已拿到 `user_id` 和 `session_id`。
4. 默认设置 `stream=true`。
5. 用户输入包含 HTML 时，先做安全过滤。

## 1. Skill Purpose

当用户需要调用 Pengleni 美妆智能体能力时使用本 Skill：通过手机号验证码完成登录建会话，并基于 HTML 消息承载能力完成 AI 试妆、妆容分析、妆容迁移、商品推荐与美妆知识问答。

适用意图关键词：

- 验证码登录
- 创建会话
- HTML 消息问答
- 多轮会话延续
- AI 试妆
- 妆容分析
- 妆容迁移
- 商品推荐
- 美妆知识问答

## 2. Runtime Config

Agent 在调用前必须确认以下环境变量：

```env
SITE_BASE_URL=https://www.zhibianai.com
API_BASE_URL=https://www.zhibianai.com/api/v1/clawhub
CLAWHUB_SKILL_TOKEN=your_service_token
```

默认请求头：

```http
Authorization: Bearer ${CLAWHUB_SKILL_TOKEN}
Content-Type: application/json
```

## 3. Python 文件说明

### 3.1 `send_code_client.py`

- 作用：发送短信验证码，请求站点级验证码接口。
- 关键函数：`send_code(phone)`。
- 输入：`phone`（11 位手机号）。
- 输出：接口返回的 JSON 字典；失败时由 `error` 字段表达。
- 典型调用命令示例：

```bash
python send_code_client.py --phone 13800138000
python send_code_client.py --env .env --phone 13800138000
```

### 3.2 `login_client.py`

- 作用：使用手机号 + 验证码登录并创建/复用会话。
- 关键函数：`login(phone, verify_code, session_id="")`。
- 输入：`phone`、`verify_code`、可选 `session_id`。
- 输出：登录响应 JSON；成功时包含 `user_id`、`session_id`，并落盘到 `.session.json`。
- 典型调用命令示例：

```bash
python login_client.py --phone 13800138000 --verify-code 123456
python login_client.py --env .env --phone 13800138000 --verify-code 123456 --session-id sess_old_xxx
python login_client.py --phone 13800138000 --verify-code 123456 --session-file .session.json
```

### 3.3 `chat_client.py`

- 作用：向会话发送消息并支持多轮交互。
- 关键函数：`send_message(...)`、`run_multi_turn(...)`。
- 输入：`user_id`、`session_id`、文本内容（内部转为 `html_payload`）。
- 输出：消息接口响应 JSON；优先展示 `answer_text`。
- 典型调用命令示例：

```bash
python chat_client.py --text "你好，帮我推荐一个通勤淡妆"
python chat_client.py --multi-turn
python chat_client.py --stream --trace-id debug-trace-001 --text "帮我优化底妆步骤"
python chat_client.py --user-id user_xxx --session-id sess_xxx --text "继续上次话题"
```

### 3.4 `client_common.py`

- 作用：封装环境变量加载、HTTP POST、会话文件读写、错误判断等通用能力。
- 关键函数：`load_env_file`、`require_env`、`post_json`、`load_session`、`save_session`。
- 输入：`.env` 路径、请求 URL/载荷、会话文件路径等。
- 输出：标准化 JSON 字典与本地会话文件内容。
- 典型调用命令示例：

```bash
# client_common.py 主要作为工具模块被其他脚本导入，不直接单独运行。
python send_code_client.py --phone 13800138000
python login_client.py --phone 13800138000 --verify-code 123456
python chat_client.py --multi-turn
```

## 4. Agent Execution Flow

按以下顺序执行，除非用户明确要求跳过某一步：

1. 调用验证码接口发送验证码。
2. 收集用户验证码后调用登录接口。
3. 从登录响应读取 `user_id` 和 `session_id`。
4. 调用消息接口发送 `html_payload`。
5. 优先返回 `answer_text`，若用户需要富文本则返回 `answer_html`。

## 5. Agent Behavior Rules

- 如果用户未提供 `session_id`，允许服务端创建。
- 如果登录后返回新 `session_id`，后续请求必须使用新值。
- 默认流式：Agent 默认 `stream=true`。
- 发生 `401` 时，优先提示重新登录，不要盲目重试消息接口。
- 发生 `429` 或 `504` 时，最多重试 2 次，退避 500ms。

## 6. Security Constraints

- 输入 HTML 需要白名单策略。
- 禁止 `script`、`style`、`iframe`、`object`、`embed`、`form`、`input` 标签。
- 应校验 `user_id` 与 `session_id` 的绑定关系。

## 7. Minimal Error Handling Template

当接口失败时，Agent 返回格式建议：

```text
调用阶段: <send_code|login|message>
HTTP状态: <status_code>
错误原因: <mapped_reason>
建议动作: <retry|relogin|check_input>
```