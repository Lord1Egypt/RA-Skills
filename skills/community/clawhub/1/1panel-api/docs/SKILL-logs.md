# Logs, TaskLog - 1Panel API

## 模块说明
Logs 模块提供系统日志文件查询和任务日志分页查询功能。

## 接口列表 (3 个)

---

### GET /logs/system/files
**功能**: 获取系统日志文件列表

**说明**: 返回服务器上所有可用的系统日志文件路径列表。

**请求参数**: 无

**返回示例**:
```json
[
  "/var/log/syslog",
  "/var/log/nginx/access.log",
  "/var/log/nginx/error.log"
]
```

---

### POST /logs/tasks/search
**功能**: 分页查询任务日志

**说明**: 分页获取任务执行记录，支持按状态和类型筛选。

**请求参数 (SearchTaskLogReq)**:

| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| status | string | 否 | 任务状态筛选 | `running`, `success`, `failed`, `waiting` |
| type | string | 否 | 任务类型筛选 | 任意任务类型字符串 |
| page | int | 是 | 页码 | >= 1 |
| pageSize | int | 是 | 每页大小 | 1-100 |

**请求体示例**:
```json
{
  "status": "success",
  "type": "backup",
  "page": 1,
  "pageSize": 10
}
```

**返回字段 (Task)**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 任务唯一标识 |
| name | string | 任务名称 |
| type | string | 任务类型 |
| operate | string | 操作类型 |
| logFile | string | 日志文件路径 |
| status | string | 任务状态 |
| errorMsg | string | 错误信息 |
| operationLogID | uint | 操作日志ID |
| resourceID | uint | 资源ID |
| currentStep | string | 当前步骤 |
| endAt | time | 结束时间 |
| createdAt | time | 创建时间 |

---

### GET /logs/tasks/executing/count
**功能**: 获取当前正在执行的任务数量

**说明**: 返回当前处于 running 状态的任务总数。

**请求参数**: 无

**返回示例**:
```json
3
```

---

## 补充说明

### 任务状态说明
- `waiting`: 等待执行
- `running`: 执行中
- `success`: 执行成功
- `failed`: 执行失败

### 通用分页参数
所有分页接口使用以下通用结构：
```json
{
  "page": 1,
  "pageSize": 10
}
```

### 返回格式 (PageResult)
```json
{
  "items": [],
  "total": 100
}
```
