---
name: avavox-智能外呼
description: 通过 大模型语音数字员工-avavox的外呼机器人的技能, 用于在 小龙虾(OpenClaw)等 Agent平台中实现大模型语音外呼机器人。适用于批量外呼、客户回访、满意度调查、简历筛查约面试，以及定时提醒、任务安排等场景。
metadata:
  {
    'openclaw':
      {
        'skillKey': 'avavox-call',
        'homepage': 'https://avavox.com/avavox-docs/developer/app-key.html',
        'requires': { 'anyBins': ['python3', 'python', 'py'] },
        'primaryEnv': 'AVAVOX_APP_KEY',
      },
  }
---

# avavox 外呼技能

当前版本：`0.6.2`

按 avavox 开放接口工作，不依赖前端页面 session、企业后台 token 或内部接口。

## 准备

1. 先访问 `https://dashboard.avavox.com/login` 完成平台登录。
2. 登录页支持两种方式：
   - `手机号` 页签：手机号 + 短信验证码；页面文案明确写了“未注册的手机号将自动注册”
   - `账号` 页签：账号/手机号/邮箱 + 密码
3. 登录成功后进入 `https://dashboard.avavox.com/agent/api-paas`。
4. 该页面对应控制台菜单 `空间管理 -> 接口回调`，包含两个页签：
   - `回调设置`：配置通话结束后的回调端点、Header、启用/禁用状态与连通性测试
   - `App Key 管理`：创建、复制、启用、禁用、删除 App Key
5. 在 `App Key 管理` 中创建并复制 App Key，再填写 `config.json` 中的 `appKey`；`baseUrl` 通常保持官方默认值 `https://dashboard.avavox.com`。
6. 创建任务前，先查询当前空间是否存在可用的已发布机器人，再查询线路。

脚本使用 Python 3 标准库实现，不依赖第三方包。对外发布时，优先使用 `python3`；在 Windows 上可用 `py -3`。

## OpenClaw 配置建议

按 OpenClaw 官方 skills 配置约定，这个 skill 优先支持两种配置来源：

- `skills.entries."avavox-call".apiKey` 对应注入环境变量 `AVAVOX_APP_KEY`
- `skills.entries."avavox-call".env` 可选注入：
  - `AVAVOX_BASE_URL`（仅兼容 `https://dashboard.avavox.com`，对外发布时不要改成其他域名）
  - `AVAVOX_DEFAULT_TASK_ID`
  - `AVAVOX_DEFAULT_LINE_ID`
  - `AVAVOX_DEFAULT_CONCURRENCY`
  - `AVAVOX_DEFAULT_BACKGROUND_AUDIO`
  - `AVAVOX_DEFAULT_CALL_TIME_TYPE`

如果没有使用 OpenClaw 的 env/apiKey 注入，也可以继续使用 `{baseDir}/config.json`。
创建任务时不要通过默认配置固化 `robotId`；每次都应先用 `robots list` 确认当前可用机器人，再把本次确认的 `robotId` 显式传给 `tasks create`。

## 官方文档

对外发布时，以下线上文档应视为优先参考的权威来源；本 skill 目录下的 `references/` 是便于 OpenClaw 使用的精简摘要。

- App Key 创建与管理： `https://avavox.com/avavox-docs/developer/app-key.html`
- 创建任务： `https://avavox.com/avavox-docs/developer/create-task.html`

如果在 OpenClaw 中直接运行，一般以 skill 根目录作为工作目录。命令示例默认都在 skill 根目录执行：

```bash
python3 {baseDir}/scripts/avavox_call.py robots list --config {baseDir}/config.json
python3 {baseDir}/scripts/avavox_call.py lines list --config {baseDir}/config.json
```

## 核心工作流

### 1. 查询可用资源

```bash
python3 {baseDir}/scripts/avavox_call.py robots list --config {baseDir}/config.json
python3 {baseDir}/scripts/avavox_call.py lines list --config {baseDir}/config.json
```

创建任务前先执行以下判断：

1. 先运行 `robots list`，把返回的已发布机器人列表展示给用户选择。
2. 只有在返回结果非空，且用户已经从结果中明确选择了一个机器人后，才继续 `tasks create`。
3. 如果 `robots list` 返回为空，不要继续创建任务，也不要假定某个 `robotId` 可用。
4. 此时应打开浏览器访问 `https://dashboard.avavox.com/robot`，让用户先创建机器人并完成发布。
5. 用户发布成功后，重新执行一次 `robots list`，再继续后续任务创建流程。

### 2. 创建任务

**机器人选择规则**：

1. **用户明确指定机器人时**（如"用客服机器人打"、"用回访那个机器人"）：
   - 先运行 `robots list` 获取当前可用列表
   - 从列表中定位用户指定的机器人并确认其状态
   - 如果存在且已发布，使用用户指定的；如果不存在或未发布，告知用户并让其从当前列表中选择
   - **不要忽略用户的明确指定而使用历史记忆中的 robotId**

2. **用户没有指定时**（如"再打一个电话"、"创建个任务"）：
   - 运行 `robots list` 获取当前可用列表
   - 展示给用户选择，或者询问是否使用上次的机器人（如果上次使用的仍在可用列表中）
   - **不能自动假设使用历史 robotId**，至少要确认一下

3. **关键原则**：
   - ✅ **用户的明确指令优先于历史记忆**
   - ✅ 每次都要验证机器人当前是否仍然可用（通过 `robots list`）
   - ✅ 如果历史机器人已从列表中消失，必须告知用户并重新选择
   - ❌ 不要忽略用户的新指定而默默使用旧 robotId
   - ❌ 不要在未验证的情况下假设历史机器人仍然可用

```bash
python3 {baseDir}/scripts/avavox_call.py tasks create \
  --config {baseDir}/config.json \
  --task-name "三月回访任务" \
  --robot-id "robot_xxx" \
  --line-id "line_xxx" \
  --concurrency 1 \
  --call-time-type immediate
```

复杂配置直接用 JSON 透传：

```bash
python3 {baseDir}/scripts/avavox_call.py tasks create \
  --config {baseDir}/config.json \
  --task-name "工作日白天外呼" \
  --robot-id "robot_xxx" \
  --call-time-type scheduled \
  --runtime-config-json '{"retryConfig":{"retryableStatuses":["busy","timeout"],"maxRetries":1,"retryInterval":1,"enabled":true}}' \
  --scheduled-time-json '[{"dayOfWeeks":[1,2,3,4,5],"times":[{"startTime":"09:00","endTime":"12:00"},{"startTime":"14:00","endTime":"18:00"}]}]'
```

### 3. 导入客户

创建任务后，必须导入客户，系统才会开始外呼：

```bash
python3 {baseDir}/scripts/avavox_call.py customers import \
  --config {baseDir}/config.json \
  --task-id "task_xxx" \
  --customers-inline '[{"phoneNumber":"13800000001","ext":{"客户姓名":"张三"}}]'
```

**变量参数传递说明**：

`ext` 字段用于传递机器人变量，格式为 `{"变量名": "值"}`，其中**变量名必须与机器人绑定的变量名称完全一致**。

1. **先查询任务支持的变量**：

```bash
python3 {baseDir}/scripts/avavox_call.py tasks variables \
  --config {baseDir}/config.json \
  --task-id "task_xxx"
```

返回示例：
```json
{
  "code": 200,
  "success": true,
  "data": {
    "robotId": "robot_xxx",
    "robotName": "回访机器人",
    "variables": [
      {
        "name": "客户姓名",
        "key": "customer_name",
        "description": "客户姓名",
        "defaultValue": "",
        "required": true,
        "category": "custom"
      },
      {
        "name": "订单号",
        "key": "order_id",
        "description": "订单编号",
        "defaultValue": "",
        "required": false,
        "category": "custom"
      }
    ]
  }
}
```

2. **根据 `data.variables[].name` 构造 ext**：

`ext` 的键名要取变量对象里的 `name`，**不是** `key`。例如上面返回里应使用 `"客户姓名"`、`"订单号"`，不要传 `"customer_name"`、`"order_id"`。

```bash
# 单变量示例
python3 {baseDir}/scripts/avavox_call.py customers import \
  --config {baseDir}/config.json \
  --task-id "task_xxx" \
  --customers-inline '[{"phoneNumber":"13800000001","ext":{"客户姓名":"张三"}}]'

# 多变量示例
python3 {baseDir}/scripts/avavox_call.py customers import \
  --config {baseDir}/config.json \
  --task-id "task_xxx" \
  --customers-inline '[
    {
      "phoneNumber": "13800000001",
      "ext": {
        "客户姓名": "张三",
        "手机尾号": "0001",
        "订单号": "ORD20240001"
      }
    },
    {
      "phoneNumber": "13800000002",
      "ext": {
        "客户姓名": "李四",
        "手机尾号": "0002",
        "订单号": "ORD20240002"
      }
    }
  ]'
```

3. **关键点**：
   - `ext` 中的键名（如 `"客户姓名"`）必须使用 `tasks variables` 返回结果里 `data.variables[].name` 的值，**不要使用** `key`
   - `ext` 是可选字段，如果机器人没有配置变量，可以省略
   - 变量值会在通话记录回调时原样回传，用于关联客户信息
   - 每次最多导入 2000 条客户

### 4. 查询与维护任务

```bash
python3 {baseDir}/scripts/avavox_call.py tasks list --config {baseDir}/config.json
python3 {baseDir}/scripts/avavox_call.py tasks get --config {baseDir}/config.json --task-id "task_xxx"
python3 {baseDir}/scripts/avavox_call.py tasks variables --config {baseDir}/config.json --task-id "task_xxx"
python3 {baseDir}/scripts/avavox_call.py tasks pause --config {baseDir}/config.json --task-id "task_xxx"
python3 {baseDir}/scripts/avavox_call.py tasks resume --config {baseDir}/config.json --task-id "task_xxx"
```

修改任务：

```bash
python3 {baseDir}/scripts/avavox_call.py tasks update \
  --config {baseDir}/config.json \
  --task-id "task_xxx" \
  --line-id "line_xxx" \
  --background-audio office_ambient \
  --concurrency 5
```

## 映射规则

- "查机器人 / 查线路": 用 `robots list` 或 `lines list`
- "创建一个外呼任务" / "再打一个电话" / "用 avavox 打个电话": 先运行 `robots list` 验证机器人可用性
  - 如果用户明确指定了机器人，从列表中定位并使用用户指定的
  - 如果用户没有指定，展示列表让用户选择，或询问是否使用上次的（需确认仍然可用）
  - **不要忽略用户的明确指定而使用历史记忆**
  - 如果没有可选机器人，打开浏览器到 `https://dashboard.avavox.com/robot` 让用户创建并发布机器人，完成后再确认 `taskName`、`robotId`，需要真实外呼时补 `lineId`
- "看看这个任务有哪些机器人变量，ext 该怎么传": 用 `tasks variables` 查询 `data.variables[]`，`ext` 的键名取其中的 `name`
- "把客户名单导入这个任务": 用 `customers import`，其中 `ext` 字段的键名必须与 `tasks variables` 返回结果里的 `data.variables[].name` 完全一致
  - 标准格式: `[{"phoneNumber":"手机号","ext":{"变量名1":"值1","变量名2":"值2"}}]`
  - 示例: `[{"phoneNumber":"13800000001","ext":{"客户姓名":"张三"}}]`，其中 `"客户姓名"` 是机器人绑定的变量名称
- "暂停 / 恢复 / 查看任务详情": 用 `tasks pause`、`tasks resume`、`tasks get`
- "文档里有接口，但脚本还没单独封装": 用受限的 `request`，且 `--path` 只能是 `/open/api/...` 相对路径

## 受限请求入口

```bash
python3 {baseDir}/scripts/avavox_call.py request \
  --config {baseDir}/config.json \
  --method PUT \
  --path /open/api/task/task_xxx \
  --body-json '{"concurrency":3}'
```

安全边界：

- `--path` 只能是当前 avavox 开放接口下的相对路径，例如 `/open/api/task/task_xxx`
- 不支持绝对 URL、协议相对 URL、外部域名，也不支持把 query string 直接拼进 `--path`
- 如果需要 query 参数，使用 `--query-json`

## 约束

- 只调用开放接口文档里明确存在的能力，不伪造前端内部 API。
- `App Key` 是空间级凭据，不同空间不能混用。
- `https://dashboard.avavox.com/agent/api-paas` 需要先完成平台登录；未登录访问时会被重定向到登录页。
- 创建任务前必须通过 `robots list` 验证机器人当前是否仍然可用，**不能直接使用未经验证的 robotId**。
- 创建任务时必须显式传入这一次确认过的 `robotId`，不要依赖默认配置或环境变量去隐式继承机器人。
- **用户的明确机器人指定必须优先于历史记忆**：当用户明确指定了新机器人时，使用用户指定的，而不是上一次使用的。
- 如果历史记忆的机器人已从 `robots list` 中消失，必须告知用户并重新选择。
- 如果没有可选的已发布机器人，应先打开 `https://dashboard.avavox.com/robot` 让用户创建并发布机器人，再继续创建任务。
- 创建任务后不会自动有客户，必须再调用一次 `customers import`。
- 如果机器人配置了变量，先查 `tasks variables`，再按 `data.variables[].name` 构造 `ext`。
- "通话记录"文档当前定义的是回调数据结构，不是查询接口。
- 如果要接收通话结束回调，不要只创建 App Key，还应在 `接口回调 -> 回调设置` 中配置回调 URL 与 Header。
- `request` 只是开放接口的受限回退入口，目标必须保持在 `https://dashboard.avavox.com/open/api/...`。
- 不要在对用户可见的输出里回显完整 `appKey`。

## 参考文件

- 官方线上文档：
  - `https://avavox.com/avavox-docs/developer/app-key.html`
  - `https://avavox.com/avavox-docs/developer/create-task.html`
- `references/auth-and-context.md`
- `references/entity-and-endpoint-map.md`
- `references/payload-examples.md`
- `references/callback-schema.md`
- `scripts/avavox_call.py`
