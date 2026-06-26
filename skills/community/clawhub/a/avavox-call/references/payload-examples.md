# 常用请求体示例

## 1. 最小创建任务

```json
{
  "taskName": "三月回访任务",
  "robotId": "robot_xxx",
  "lineId": "line_xxx",
  "callTimeType": "immediate"
}
```

说明：

- `taskName` 和 `robotId` 必填
- 需要真实外呼时通常还应提供 `lineId`
- 若不导入客户，任务不会开始外呼

## 2. 带重呼与定时窗口的任务

```json
{
  "taskName": "工作日白天外呼",
  "robotId": "robot_xxx",
  "lineId": "line_xxx",
  "backgroundAudio": "office_ambient",
  "concurrency": 1,
  "runtimeConfig": {
    "retryConfig": {
      "retryableStatuses": [
        "busy",
        "timeout"
      ],
      "maxRetries": 1,
      "retryInterval": 1,
      "enabled": true
    }
  },
  "forbiddenCallTime": [
    {
      "startTime": "22:00",
      "endTime": "07:00"
    }
  ],
  "callTimeType": "scheduled",
  "scheduledTime": [
    {
      "dayOfWeeks": [
        1,
        2,
        3,
        4,
        5
      ],
      "times": [
        {
          "startTime": "09:00",
          "endTime": "12:00"
        },
        {
          "startTime": "14:00",
          "endTime": "18:00"
        }
      ]
    }
  ]
}
```

## 3. 局部更新任务

```json
{
  "lineId": "line_new_xxx",
  "backgroundAudio": "busy_call_center",
  "concurrency": 5
}
```

说明：

- 更新接口允许部分字段更新
- 如果要禁用重呼，必须把 `runtimeConfig.retryConfig.enabled` 显式传成 `false`

## 4. 导入客户

```json
{
  "taskId": "task_xxx",
  "customers": [
    {
      "phoneNumber": "13800000001",
      "ext": {
        "客户姓名": "张三",
        "手机尾号": "0001"
      }
    },
    {
      "phoneNumber": "010-12345678",
      "ext": {
        "客户姓名": "李四"
      }
    }
  ]
}
```

说明：

- 单次最多 2000 条
- 同一任务内重复号码会被忽略
- **`ext` 中的键名必须与 `tasks variables` 返回结果里的 `data.variables[].name` 完全一致**
- `ext` 推荐按 `tasks variables` 的结果来构造

**变量传递工作流**：

1. 先查询任务支持的变量：
   ```bash
   python3 {baseDir}/scripts/avavox_call.py tasks variables \
     --config {baseDir}/config.json \
     --task-id "task_xxx"
   ```
   返回示例：
   ```json
   {
     "data": {
       "variables": [
         {
           "name": "客户姓名",
           "key": "customer_name"
         },
         {
           "name": "手机尾号",
           "key": "phone_suffix"
         },
         {
           "name": "订单号",
           "key": "order_id"
         }
       ]
     }
   }
   ```

2. 根据返回结果里的 `data.variables[].name` 构造 `ext`：
   ```bash
   python3 {baseDir}/scripts/avavox_call.py customers import \
     --config {baseDir}/config.json \
     --task-id "task_xxx" \
     --customers-inline '[{"phoneNumber":"13800000001","ext":{"客户姓名":"张三","手机尾号":"0001"}}]'
   ```

3. 关键点：
   - `ext` 的键名使用 `name`，不要使用 `key`
   - `ext` 是可选字段，如果机器人没有配置变量，可以省略
   - 变量值会在通话记录回调时原样回传，用于关联客户信息

## 5. 获取任务变量

这个接口没有请求体，只需要 path 参数：

```bash
python3 {baseDir}/scripts/avavox_call.py tasks variables \
  --config {baseDir}/config.json \
  --task-id "task_xxx"
```

## 6. 受限请求示例

```bash
python3 {baseDir}/scripts/avavox_call.py request \
  --config {baseDir}/config.json \
  --method PUT \
  --path /open/api/task/task_xxx \
  --body-json '{
    "taskName": "新的任务名称",
    "concurrency": 3
  }'
```

说明：

- `--path` 只能传 `/open/api/...` 相对路径
- query 参数请通过 `--query-json` 传入，不要直接拼在 `--path` 后面
