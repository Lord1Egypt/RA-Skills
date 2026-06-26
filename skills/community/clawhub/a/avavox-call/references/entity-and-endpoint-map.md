# 实体与接口映射

这个 skill 以 avavox 官方开发者文档为准。

对外发布时，可优先对照这些线上官方文档：

- App Key 创建与管理：`https://avavox.com/avavox-docs/developer/app-key.html`
- 创建任务：`https://avavox.com/avavox-docs/developer/create-task.html`

## 1. 机器人

- `GET /open/api/task/robot`
- 作用：查询已发布机器人
- 已封装命令：`robots list`
- 创建任务前，先以这个接口的返回结果作为机器人候选集；如果返回为空，就先去 `https://dashboard.avavox.com/robot` 创建并发布机器人。

返回核心字段：

- `robotId`
- `robotName`
- `releaseTime`

## 2. 线路

- `GET /open/api/task/line`
- 作用：查询可用线路
- 已封装命令：`lines list`

返回核心字段：

- `lineId`
- `lineName`
- `category`

## 3. 任务

- `GET /open/api/task/list`
- `GET /open/api/task/{taskId}`
- `POST /open/api/task`
- `PUT /open/api/task/{taskId}`
- `POST /open/api/task/{taskId}/pause`
- `POST /open/api/task/{taskId}/resume`
- `GET /open/api/task/{taskId}/robot-variables`

创建任务官方文档：

- `https://avavox.com/avavox-docs/developer/create-task.html`

已封装命令：

- `tasks list`
- `tasks get`
- `tasks create`
- `tasks update`
- `tasks pause`
- `tasks resume`
- `tasks variables`

任务状态字段在文档中的枚举值：

- `pending`
- `running`
- `paused`
- `completed`

## 4. 客户导入

- `POST /open/api/task/import`
- 作用：把客户导入到任务中，导入后系统才会开始外呼
- 已封装命令：`customers import`

请求体核心字段：

- `taskId`
- `customers[].phoneNumber`
- `customers[].ext`

## 5. 通话记录

当前开放文档提供的是回调结构说明，不是查询接口：

- 文档：`call-record.md`
- 作用：说明回调 payload 和回调方需要返回的 `{"success": true}`

因此当前 skill 不封装：

- 通话记录分页查询
- 通话记录导出
- 录音下载列表

如果后续开放文档新增正式查询接口，再扩展脚本。

## 6. 兜底调用

当文档里有接口但脚本还没做快捷命令时，使用：

- `request --method ... --path /open/api/...`

这个命令仍然走同一套 `App Key` 鉴权，但只接受当前 avavox 开放接口域名下的 `/open/api/...` 相对路径。
