# Cronjob - 1Panel API

## 模块说明
Cronjob 模块接口，用于管理定时任务（计划任务）

## 接口列表 (16 个)

---

### GET /cronjobs/script/options
**功能**: 获取脚本选项列表  
**说明**: 获取所有可用的脚本名称和 ID，用于创建定时任务时选择脚本  
**参数**: 无

**返回示例**:
```json
[
  {"id": 1, "name": "backup-script"},
  {"id": 2, "name": "cleanup-script"}
]
```

---

### POST /cronjobs
**功能**: 创建定时任务  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 定时任务名称 | 最大 256 字符 |
| type | string | 是 | 定时任务类型 | 参见下方类型说明 |
| groupID | uint | 否 | 分组 ID | |
| specCustom | bool | 否 | 是否自定义执行时间 | true/false |
| spec | string | 是 | 执行时间规则 | cron 表达式 |
| executor | string | 否 | 执行器类型 | shell/php/python/node |
| scriptMode | string | 否 | 脚本模式 | script/scriptUrl |
| script | string | 否 | 脚本内容 | |
| command | string | 否 | 执行命令 | |
| containerName | string | 否 | 容器名称 | 用于容器执行 |
| user | string | 否 | 执行用户 | |
| scriptID | uint | 否 | 脚本 ID | 关联脚本市场中的脚本 |
| appID | string | 否 | 应用 ID | 用于应用备份 |
| website | string | 否 | 网站名称 | 用于网站备份 |
| exclusionRules | string | 否 | 排除规则 | JSON 格式的排除规则 |
| dbType | string | 否 | 数据库类型 | mysql/postgres/mongodb/redis/mariadb |
| dbName | string | 否 | 数据库名称 | |
| url | string | 否 | URL 地址 | 用于 HTTP 请求任务 |
| isDir | bool | 否 | 是否目录 | |
| sourceDir | string | 否 | 源目录 | |
| withImage | bool | 否 | 是否包含镜像 | 快照规则 |
| ignoreAppIDs | []uint | 否 | 忽略的应用 ID | 快照规则 |
| sourceAccountIDs | string | 否 | 源账户 IDs | 多个用逗号分隔 |
| downloadAccountID | uint | 否 | 下载账户 ID | |
| retainCopies | int | 否 | 保留副本数 | 最小 1 |
| retryTimes | int | 否 | 重试次数 | 最小 0 |
| timeout | uint | 否 | 超时时间(秒) | 最小 1 |
| ignoreErr | bool | 否 | 是否忽略错误 | |
| secret | string | 否 | 密钥 | |
| args | string | 否 | 额外参数 | |
| alertCount | uint | 否 | 告警次数 | |
| alertTitle | string | 否 | 告警标题 | |
| alertMethod | string | 否 | 告警方式 | |
| scopes | []string | 否 | 清理日志范围 | |

**定时任务类型 (type)**:
- `backup` - 备份任务
- `restore` - 恢复任务
- `shell` - Shell 脚本
- `website` - 网站任务
- `database` - 数据库任务
- `directory` - 目录任务
- `log` - 日志清理
- `docker` - Docker 任务
- `snapshot` - 快照任务
- `image` - 镜像任务
- `httptest` - HTTP 测试
- `record` - 录制任务

---

### POST /cronjobs/next
**功能**: 计算下次执行时间  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| spec | string | 是 | cron 表达式 | 标准 cron 格式 |

**返回示例**:
```json
["2024-01-15 10:00:00", "2024-01-15 11:00:00"]
```

---

### POST /cronjobs/import
**功能**: 导入定时任务  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cronjobs | []CronjobTrans | 是 | 定时任务列表 |

**CronjobTrans 结构**:

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 任务名称 |
| type | string | 任务类型 |
| groupID | uint | 分组 ID |
| specCustom | bool | 是否自定义时间 |
| spec | string | 执行规则 |
| executor | string | 执行器 |
| scriptMode | string | 脚本模式 |
| script | string | 脚本内容 |
| command | string | 执行命令 |
| containerName | string | 容器名称 |
| user | string | 执行用户 |
| url | string | URL |
| scriptName | string | 脚本名称 |
| apps | []TransHelper | 应用列表 |
| websites | []string | 网站列表 |
| dbType | string | 数据库类型 |
| dbNames | []TransHelper | 数据库名称列表 |
| exclusionRules | string | 排除规则 |
| isDir | bool | 是否目录 |
| sourceDir | string | 源目录 |
| retainCopies | uint64 | 保留副本数 |
| retryTimes | uint | 重试次数 |
| timeout | uint | 超时时间 |
| ignoreErr | bool | 忽略错误 |
| snapshotRule | SnapshotTransHelper | 快照规则 |
| secret | string | 密钥 |
| args | string | 额外参数 |
| sourceAccounts | []string | 源账户 |
| downloadAccount | string | 下载账户 |
| alertCount | uint | 告警次数 |
| alertTitle | string | 告警标题 |
| alertMethod | string | 告警方式 |

---

### POST /cronjobs/export
**功能**: 导出定时任务  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | []uint | 是 | 要导出的定时任务 ID 列表 |

**返回**: JSON 格式的定时任务列表（文件下载）

---

### POST /cronjobs/load/info
**功能**: 获取定时任务详情  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 定时任务 ID |

**返回**: CronjobInfo 对象，包含任务完整配置信息

---

### POST /cronjobs/del
**功能**: 删除定时任务  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | []uint | 是 | 要删除的定时任务 ID 列表 |
| cleanData | bool | 否 | 是否清理关联数据 |
| cleanRemoteData | bool | 否 | 是否清理远程数据 |

---

### POST /cronjobs/stop
**功能**: 停止正在执行的定时任务  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 定时任务 ID |

---

### POST /cronjobs/update
**功能**: 更新定时任务  
**参数 (body)**: 同创建接口 (POST /cronjobs)，需额外提供 id 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 定时任务 ID |

**其他字段**: 同创建接口

---

### POST /cronjobs/group/update
**功能**: 更新定时任务分组  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 定时任务 ID |
| groupID | uint | 是 | 新的分组 ID |

---

### POST /cronjobs/status
**功能**: 更新定时任务状态  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 定时任务 ID | |
| status | string | 是 | 任务状态 | running/stopped |

---

### POST /cronjobs/handle
**功能**: 手动执行一次定时任务  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 定时任务 ID |

---

### POST /cronjobs/search
**功能**: 分页查询定时任务列表  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | |
| pageSize | int | 是 | 每页数量 | |
| info | string | 否 | 搜索关键词 | |
| groupIDs | []uint | 否 | 分组 ID 列表 | |
| orderBy | string | 否 | 排序字段 | name/status/createdAt |
| order | string | 否 | 排序方向 | null/ascending/descending |

**返回**: 分页结果，包含 Items (任务列表) 和 Total (总数)

---

### POST /cronjobs/search/records
**功能**: 分页查询执行记录  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| cronjobID | int | 否 | 定时任务 ID |
| startTime | time | 否 | 开始时间 |
| endTime | time | 否 | 结束时间 |
| status | string | 否 | 执行状态 |

**返回**: 分页结果，包含执行记录列表

---

### POST /cronjobs/records/log
**功能**: 获取执行记录日志  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 执行记录 ID |

**返回**: 日志内容 (string)

---

### POST /cronjobs/records/clean
**功能**: 清理执行记录  
**参数 (body)**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cronjobID | uint | 是 | 定时任务 ID |
| isDelete | bool | 否 | 是否删除记录 |
| cleanData | bool | 否 | 是否清理数据 |
| cleanRemoteData | bool | 否 | 是否清理远程数据 |

---

## 数据结构参考

### SnapshotRule (快照规则)
```json
{
  "withImage": true,
  "ignoreAppIDs": [1, 2, 3]
}
```

### CleanLogConfig (日志清理配置)
```json
{
  "scopes": ["log", "backup"]
}
```

### CronjobInfo 返回字段
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 任务 ID |
| name | string | 任务名称 |
| type | string | 任务类型 |
| groupID | uint | 分组 ID |
| specCustom | bool | 是否自定义 |
| spec | string | 执行规则 |
| executor | string | 执行器 |
| scriptMode | string | 脚本模式 |
| script | string | 脚本内容 |
| command | string | 执行命令 |
| containerName | string | 容器名称 |
| user | string | 执行用户 |
| scriptID | uint | 脚本 ID |
| appID | string | 应用 ID |
| website | string | 网站名称 |
| exclusionRules | string | 排除规则 |
| dbType | string | 数据库类型 |
| dbName | string | 数据库名称 |
| url | string | URL 地址 |
| isDir | bool | 是否目录 |
| sourceDir | string | 源目录 |
| retainCopies | int | 保留副本 |
| retryTimes | int | 重试次数 |
| timeout | uint | 超时时间 |
| ignoreErr | bool | 忽略错误 |
| sourceAccounts | []string | 源账户列表 |
| downloadAccount | string | 下载账户 |
| lastRecordStatus | string | 上次执行状态 |
| lastRecordTime | string | 上次执行时间 |
| status | string | 当前状态 |
| secret | string | 密钥 |
| args | string | 额外参数 |
| alertCount | uint | 告警次数 |

### Record 执行记录字段
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 记录 ID |
| taskID | string | 任务 ID |
| startTime | string | 开始时间 |
| records | string | 记录内容 |
| status | string | 执行状态 |
| message | string | 消息 |
| targetPath | string | 目标路径 |
| interval | int | 间隔 |
| file | string | 文件 |
