# 模型可执行测试套件 JSON 规范

## 顶层结构

输出一个 JSON 对象，固定包含以下字段：

```json
{
  "suite_id": "login-web",
  "suite_title": "登录页自动化测试",
  "target": {
    "type": "web",
    "start_url": "https://test.example.com/login"
  },
  "assumptions": [
    "测试账号已在测试环境预置。"
  ],
  "defaults": {
    "locale": "zh-CN",
    "timezone": "Asia/Shanghai",
    "timeout_ms": 10000
  },
  "cases": []
}
```

## 顶层字段说明

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `suite_id` | 是 | 套件唯一标识，使用小写字母、数字、连字符 |
| `suite_title` | 是 | 套件标题，可中文 |
| `target` | 是 | 测试对象定义 |
| `assumptions` | 是 | 推断、前提或风险说明；没有时写空数组 |
| `defaults` | 是 | 默认执行参数 |
| `cases` | 是 | 用例数组，至少 1 个 |

## target 结构

```json
{
  "type": "web",
  "start_url": "https://test.example.com/login",
  "base_url": "https://api.test.example.com"
}
```

### `target.type` 枚举

- `web`
- `api`
- `workflow`
- `mobile`
- `desktop`

规则：

- Web 场景优先提供 `start_url`
- API 场景优先提供 `base_url`
- 端到端混合场景可同时提供 `start_url` 和 `base_url`

## defaults 结构

```json
{
  "locale": "zh-CN",
  "timezone": "Asia/Shanghai",
  "timeout_ms": 10000
}
```

保持简洁。不要把大量运行配置塞进这里；只保留后续模型执行时稳定且常用的默认参数。

## case 结构

每个 `cases[]` 元素固定包含：

```json
{
  "case_id": "TC-LOGIN-001",
  "title": "使用有效账号登录成功",
  "objective": "验证有效账号可成功登录并进入首页。",
  "priority": "P0",
  "tags": ["login", "smoke", "web"],
  "preconditions": [
    "测试环境已发布登录页。",
    "账号 {{env.TEST_USER}} 可正常登录。"
  ],
  "test_data": {
    "username": "{{env.TEST_USER}}",
    "password": "{{secret.LOGIN_PASSWORD}}"
  },
  "steps": [],
  "cleanup": [],
  "enabled": true
}
```

### case 字段约束

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| `case_id` | 是 | 在整个套件内唯一 |
| `title` | 是 | 人可读标题 |
| `objective` | 是 | 一句话说明该用例验证什么 |
| `priority` | 是 | 仅允许 `P0` `P1` `P2` `P3` |
| `tags` | 是 | 字符串数组 |
| `preconditions` | 是 | 字符串数组，没有时写空数组 |
| `test_data` | 是 | 对象，没有时写空对象 |
| `steps` | 是 | 步骤数组，至少 1 个 |
| `cleanup` | 是 | 收尾动作数组，没有时写空数组 |
| `enabled` | 是 | 布尔值 |

## step 结构

每个 `steps[]` 元素固定包含：

```json
{
  "step_id": "S1",
  "action": "fill",
  "target": {
    "by": "label",
    "value": "用户名"
  },
  "input": {
    "value": "{{env.TEST_USER}}"
  },
  "expected": [
    {
      "type": "element_value",
      "locator": {
        "by": "label",
        "value": "用户名"
      },
      "value": "{{env.TEST_USER}}"
    }
  ]
}
```

### action 枚举

- `navigate`
- `click`
- `fill`
- `select`
- `keypress`
- `hover`
- `wait`
- `assert`
- `request`
- `extract`
- `upload`
- `download`

### action 使用约束

- `navigate` 的 `target.url` 必填
- `click`、`fill`、`select`、`hover`、`upload` 通常需要定位器
- `fill` 的 `input.value` 必填
- `select` 的 `input.value` 必填
- `keypress` 的 `input.key` 必填
- `request` 需要 `input.method`，并在 `target.url` 或 `input.url` 中提供请求地址
- `extract` 需要 `input.variable`
- `assert` 允许只包含 `expected`

## expected 断言结构

每个步骤的 `expected` 必须是数组，每个元素是一个断言对象。

### 断言类型枚举

- `element_visible`
- `element_text`
- `element_value`
- `page_contains`
- `url_matches`
- `response_status`
- `json_path_equals`
- `json_path_exists`
- `variable_stored`
- `download_created`

### 示例

```json
[
  {
    "type": "response_status",
    "value": 200
  },
  {
    "type": "json_path_equals",
    "path": "data.token",
    "value": "{{var.access_token}}"
  }
]
```

## 定位器规范

定位器对象统一格式：

```json
{
  "by": "role",
  "value": "button",
  "name": "登录"
}
```

### `by` 优先级

1. `role`
2. `label`
3. `testid`
4. `text`
5. `css`
6. `xpath`

优先选择稳定、语义清晰的定位器。没有充分理由时，不要默认使用 `xpath`。

## 占位符规范

只使用以下三类占位符：

- 环境变量：`{{env.VAR_NAME}}`
- 敏感数据：`{{secret.VAR_NAME}}`
- 运行时提取变量：`{{var.variable_name}}`

不要混用其他格式。

## 标准样例

```json
{
  "suite_id": "login-web",
  "suite_title": "登录页自动化测试",
  "target": {
    "type": "web",
    "start_url": "https://test.example.com/login"
  },
  "assumptions": [
    "登录成功后会跳转到控制台首页。",
    "页面元素存在稳定的可访问性标签。"
  ],
  "defaults": {
    "locale": "zh-CN",
    "timezone": "Asia/Shanghai",
    "timeout_ms": 10000
  },
  "cases": [
    {
      "case_id": "TC-LOGIN-001",
      "title": "使用有效账号登录成功",
      "objective": "验证有效账号可成功登录并跳转到首页。",
      "priority": "P0",
      "tags": ["login", "smoke", "web"],
      "preconditions": [
        "测试账号已在环境中预置。"
      ],
      "test_data": {
        "username": "{{env.TEST_USER}}",
        "password": "{{secret.LOGIN_PASSWORD}}"
      },
      "steps": [
        {
          "step_id": "S1",
          "action": "navigate",
          "target": {
            "url": "https://test.example.com/login"
          },
          "input": {},
          "expected": [
            {
              "type": "url_matches",
              "value": ".*/login$"
            }
          ]
        },
        {
          "step_id": "S2",
          "action": "fill",
          "target": {
            "by": "label",
            "value": "用户名"
          },
          "input": {
            "value": "{{env.TEST_USER}}"
          },
          "expected": [
            {
              "type": "element_value",
              "locator": {
                "by": "label",
                "value": "用户名"
              },
              "value": "{{env.TEST_USER}}"
            }
          ]
        },
        {
          "step_id": "S3",
          "action": "fill",
          "target": {
            "by": "label",
            "value": "密码"
          },
          "input": {
            "value": "{{secret.LOGIN_PASSWORD}}"
          },
          "expected": [
            {
              "type": "element_value",
              "locator": {
                "by": "label",
                "value": "密码"
              },
              "value": "{{secret.LOGIN_PASSWORD}}"
            }
          ]
        },
        {
          "step_id": "S4",
          "action": "click",
          "target": {
            "by": "role",
            "value": "button",
            "name": "登录"
          },
          "input": {},
          "expected": [
            {
              "type": "url_matches",
              "value": ".*/dashboard$"
            },
            {
              "type": "element_visible",
              "locator": {
                "by": "text",
                "value": "欢迎回来"
              }
            }
          ]
        }
      ],
      "cleanup": [],
      "enabled": true
    }
  ]
}
```
