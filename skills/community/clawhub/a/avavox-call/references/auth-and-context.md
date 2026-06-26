# 鉴权与上下文

这个 skill 只使用 avavox 开放平台的 `App Key` 鉴权，但在获取 `App Key` 之前，用户仍然需要先完成平台登录。

## 0. 登录与入口

- 官方文档：
  - App Key 创建与管理：`https://avavox.com/avavox-docs/developer/app-key.html`
- 登录地址：`https://dashboard.avavox.com/login`
- 登录方式 1：`手机号` 页签，使用手机号 + 短信验证码
- 登录方式 2：`账号` 页签，使用账号/手机号/邮箱 + 密码
- 登录页文案明确提示：`未注册的手机号将自动注册`

开放接口配置入口：

- 页面地址：`https://dashboard.avavox.com/agent/api-paas`
- 控制台菜单：`空间管理 -> 接口回调`
- 页面页签：
  - `回调设置`
  - `App Key 管理`

未登录直接访问 `/agent/api-paas` 时，会被重定向到登录页。

机器人管理入口：

- 页面地址：`https://dashboard.avavox.com/robot`
- 页面用途：创建机器人、查看发布状态、进入机器人配置页继续编辑或发布
- 未登录直接访问 `/robot` 时，也会被重定向到登录页。

## 1. 凭据来源

- 控制台路径：`空间管理 -> 接口回调 -> App Key 管理`
- 页面用途：`创建和管理用于 API 认证的 App Key`
- 请求头格式：`Authorization: Bearer <App Key>`
- `App Key` 与空间绑定，不同空间之间不能混用
- `App Key` 列表支持复制、启用、禁用、删除
- 线上文档里也给出了请求头示例：
  `Authorization: Bearer <Your-App-Key>`

## 2. 请求基线

- 根域名：`https://dashboard.avavox.com`
- 开放接口前缀：`/open/api`
- 所有已封装命令都默认带：
  - `Authorization: Bearer <App Key>`
  - `Content-Type: application/json`

这个 skill 不做前端登录，不依赖：

- `/api/app/authService/auth/login`
- `system`
- `companyId`
- `agentId`
- 浏览器 Cookie 或前端 session

这里“不依赖”的意思是：

- skill 发开放接口请求时，不需要带浏览器登录态
- 但用户第一次获取 App Key、配置回调 URL 时，仍然需要先在平台里登录并进入 `/agent/api-paas`

OpenClaw 集成时，推荐优先使用环境变量而不是把真实密钥硬编码进文件：

- `AVAVOX_APP_KEY`
- `AVAVOX_BASE_URL`

## 3. config.json 字段

- `baseUrl`
  avavox 控制台域名，默认可保持 `https://dashboard.avavox.com`
- `appKey`
  开放平台 App Key
- `defaults.taskId`
  便于复用的默认任务 ID
- `defaults.lineId`
  创建任务时可复用的默认线路 ID
- `defaults.concurrency`
  创建任务时的默认并发
- `defaults.backgroundAudio`
  创建任务时的默认背景音
- `defaults.callTimeType`
  创建任务时的默认拨打时间类型，常见值为 `immediate` 或 `scheduled`

## 4. 何时读取机器人变量

如果要导入客户并传 `ext`，优先先调用：

```bash
python3 {baseDir}/scripts/avavox_call.py tasks variables --config {baseDir}/config.json --task-id "task_xxx"
```

因为文档约定 `ext` 的 key 应与 `data.variables[].name` 匹配，不要使用变量对象里的 `key`；后续通话记录回调也会把这些随路数据原样带回。

## 5. 创建任务前的机器人前置检查

- 开放接口 `GET /open/api/task/robot` 返回的是当前空间下可用于创建任务的已发布机器人。
- 当用户表述“创建任务”“新建外呼任务”“帮我建一个任务”时，先调用 `robots list`。
- 如果返回结果非空，应把结果里的机器人展示给用户选择，不要直接假定某个 `robotId` 可用，也不要从默认配置里静默继承旧 `robotId`。
- 如果返回结果为空，说明当前空间没有可用于开放任务的已发布机器人，此时不要继续 `tasks create`。
- 这时应打开浏览器访问 `https://dashboard.avavox.com/robot`，让用户先创建机器人，并在机器人配置页完成发布。
- 发布成功后，重新执行一次 `robots list`，再继续创建任务；真正调用 `tasks create` 时，要把这一次确认过的 `robotId` 显式传入。

## 6. 常见误区

- 不要把“skill 不依赖前端 session”理解成“用户不需要登录平台”。
- 不要把 `/agent/api-paas` 只理解成 App Key 页面；它同时也是回调设置页。
- 不要在 `robots list` 为空时继续创建任务。
- 不要依赖 `defaults.robotId` 或环境变量去固化机器人，否则很容易把新任务误发给旧机器人。
- 不要把前端内部接口当成开放接口替代品。
- 不要把通话记录回调文档当成“查询通话记录列表”接口。
- 不要在日志或回包里输出完整 `App Key`。
