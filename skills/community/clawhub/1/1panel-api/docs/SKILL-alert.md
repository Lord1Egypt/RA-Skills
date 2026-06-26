# Alert - 1Panel API

## 模块说明
alert 模块接口，包含告警管理、ClamAV 病毒扫描、Fail2ban 防护三大功能。

## 接口列表

---

### 一、Alert 告警模块

#### POST /api/v1/alert

**Handler**: `baseApi.CreateAlert`  
**功能**: 创建告警规则  
**说明**: 创建一个新的告警监控规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| type | string | 是 | 告警类型 | - |
| cycle | uint | 否 | 监控周期(分钟) | - |
| count | uint | 否 | 触发告警的次数阈值 | - |
| method | string | 是 | 告警通知方式 | - |
| title | string | 否 | 告警标题 | - |
| project | string | 否 | 关联项目 | - |
| status | string | 否 | 状态 | - |
| sendCount | uint | 否 | 已发送次数 | - |
| advancedParams | string | 否 | 高级参数(JSON字符串) | - |

**返回**: `无`

---

#### POST /api/v1/alert/update

**Handler**: `baseApi.UpdateAlert`  
**功能**: 更新告警规则  
**说明**: 更新已有的告警监控规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 告警规则ID | - |
| type | string | 否 | 告警类型 | - |
| cycle | uint | 否 | 监控周期(分钟) | - |
| count | uint | 否 | 触发告警的次数阈值 | - |
| method | string | 否 | 告警通知方式 | - |
| title | string | 否 | 告警标题 | - |
| project | string | 否 | 关联项目 | - |
| status | string | 否 | 状态 | - |
| sendCount | uint | 否 | 已发送次数 | - |
| advancedParams | string | 否 | 高级参数(JSON字符串) | - |

**返回**: `无`

---

#### POST /api/v1/alert/search

**Handler**: `baseApi.PageAlert`  
**功能**: 分页查询告警规则  
**说明**: 获取告警规则列表，支持分页和过滤

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| orderBy | string | 是 | 排序字段 | `created_at` |
| order | string | 是 | 排序方式 | `null`, `ascending`, `descending` |
| type | string | 否 | 告警类型过滤 | - |
| status | string | 否 | 状态过滤 | - |
| method | string | 否 | 通知方式过滤 | - |

**返回**: `PageResult{Total, Items}`

---

#### POST /api/v1/alert/status

**Handler**: `baseApi.UpdateAlertStatus`  
**功能**: 更新告警规则状态  
**说明**: 启用或禁用告警规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 告警规则ID | - |
| status | string | 是 | 状态 | - |

**返回**: `无`

---

#### POST /api/v1/alert/del

**Handler**: `baseApi.DeleteAlert`  
**功能**: 删除告警规则  
**说明**: 删除指定的告警规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 告警规则ID | - |

**返回**: `无`

---

#### GET /api/v1/alert/disks/list

**Handler**: `baseApi.GetDisks`  
**功能**: 获取磁盘列表  
**说明**: 获取所有可用的磁盘分区信息

**参数**: (无)

**返回**: `DiskDTO[]`

---

#### POST /api/v1/alert/logs/search

**Handler**: `baseApi.PageAlertLogs`  
**功能**: 分页查询告警日志  
**说明**: 获取告警记录日志，支持分页

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| count | uint | 否 | 告警次数 | - |
| status | string | 否 | 状态 | - |

**返回**: `PageResult{Total, Items}`

---

#### POST /api/v1/alert/logs/clean

**Handler**: `baseApi.CleanAlertLogs`  
**功能**: 清理告警日志  
**说明**: 清空所有告警日志记录

**参数**: (无)

**返回**: `无`

---

#### GET /api/v1/alert/clams/list

**Handler**: `baseApi.GetClams`  
**功能**: 获取Clam扫描规则列表  
**说明**: 获取所有已配置的ClamAV扫描规则

**参数**: (无)

**返回**: `ClamDTO[]`

---

#### POST /api/v1/alert/cronjob/list

**Handler**: `baseApi.GetCronJobs`  
**功能**: 获取定时任务列表  
**说明**: 获取可关联的定时任务列表

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 否 | 任务名称 | - |
| status | string | 否 | 任务状态 | - |
| type | string | 否 | 任务类型 | - |

**返回**: `CronJobDTO[]`

---

#### POST /api/v1/alert/config/update

**Handler**: `baseApi.UpdateAlertConfig`  
**功能**: 更新告警配置  
**说明**: 更新告警通道配置信息

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 配置ID | - |
| type | string | 否 | 配置类型 | - |
| title | string | 否 | 配置标题 | - |
| status | string | 否 | 状态 | - |
| config | string | 否 | 配置内容(JSON字符串) | - |

**返回**: `无`

---

#### POST /api/v1/alert/config/info

**Handler**: `baseApi.GetAlertConfig`  
**功能**: 获取告警配置  
**说明**: 获取当前告警通道配置信息

**参数**: (无)

**返回**: `AlertConfig`

---

#### POST /api/v1/alert/config/del

**Handler**: `baseApi.DeleteAlertConfig`  
**功能**: 删除告警配置  
**说明**: 删除指定的告警通道配置

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 配置ID | - |

**返回**: `无`

---

#### POST /api/v1/alert/config/test

**Handler**: `baseApi.TestAlertConfig`  
**功能**: 测试告警配置  
**说明**: 测试告警通道配置是否可用

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| host | string | 是 | 邮件服务器地址 | - |
| port | int | 是 | 端口号 | - |
| sender | string | 是 | 发件人邮箱 | - |
| userName | string | 是 | 用户名 | - |
| password | string | 是 | 密码 | - |
| displayName | string | 否 | 显示名称 | - |
| encryption | string | 是 | 加密方式 | `ssl`, `tls`, `none` |
| recipient | string | 是 | 收件人邮箱 | - |

**返回**: `bool` (测试是否成功)

---

### 二、ClamAV 病毒扫描模块

#### POST /api/v1/toolbox/clam

**Handler**: `baseApi.CreateClam`  
**功能**: 创建扫描规则  
**说明**: 创建新的ClamAV定时扫描规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 规则名称 | - |
| status | string | 否 | 状态 | - |
| path | string | 是 | 扫描路径 | - |
| infectedStrategy | string | 否 | 感染文件处理策略 | - |
| infectedDir | string | 否 | 隔离目录 | - |
| spec | string | 否 | Cron表达式 | - |
| timeout | uint | 否 | 超时时间(秒) | - |
| description | string | 否 | 描述 | - |
| alertCount | uint | 否 | 告警次数阈值 | - |
| alertTitle | string | 否 | 告警标题 | - |
| alertMethod | string | 否 | 告警方式 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/update

**Handler**: `baseApi.UpdateClam`  
**功能**: 更新扫描规则  
**说明**: 更新已有的ClamAV扫描规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 规则ID | - |
| name | string | 否 | 规则名称 | - |
| path | string | 否 | 扫描路径 | - |
| infectedStrategy | string | 否 | 感染文件处理策略 | - |
| infectedDir | string | 否 | 隔离目录 | - |
| spec | string | 否 | Cron表达式 | - |
| timeout | uint | 否 | 超时时间(秒) | - |
| description | string | 否 | 描述 | - |
| alertCount | uint | 否 | 告警次数阈值 | - |
| alertTitle | string | 否 | 告警标题 | - |
| alertMethod | string | 否 | 告警方式 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/status/update

**Handler**: `baseApi.UpdateClamStatus`  
**功能**: 更新扫描规则状态  
**说明**: 启用或禁用扫描规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 规则ID | - |
| status | string | 是 | 状态 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/search

**Handler**: `baseApi.SearchClam`  
**功能**: 分页查询扫描规则  
**说明**: 获取ClamAV扫描规则列表

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |
| orderBy | string | 是 | 排序字段 | `name`, `status`, `createdAt` |
| order | string | 是 | 排序方式 | `null`, `ascending`, `descending` |

**返回**: `PageResult{Total, Items}`

---

#### POST /api/v1/toolbox/clam/base

**Handler**: `baseApi.LoadClamBaseInfo`  
**功能**: 获取ClamAV基础信息  
**说明**: 获取ClamAV服务的基本状态信息

**参数**: (无)

**返回**: `ClamBaseInfo`

---

#### POST /api/v1/toolbox/clam/operate

**Handler**: `baseApi.OperateClam`  
**功能**: ClamAV服务操作  
**说明**: 启动、停止、重启ClamAV服务

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| operation | string | 是 | 操作类型 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/record/clean

**Handler**: `baseApi.CleanClamRecord`  
**功能**: 清理扫描记录  
**说明**: 清空指定扫描规则的记录

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 规则ID | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/record/search

**Handler**: `baseApi.SearchClamRecord`  
**功能**: 分页查询扫描记录  
**说明**: 获取ClamAV扫描历史记录

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| clamID | uint | 否 | 扫描规则ID | - |
| status | string | 否 | 扫描状态 | - |
| startTime | time.Time | 否 | 开始时间 | - |
| endTime | time.Time | 否 | 结束时间 | - |

**返回**: `PageResult{Total, Items}`

---

#### POST /api/v1/toolbox/clam/file/search

**Handler**: `baseApi.SearchClamFile`  
**功能**: 加载扫描日志文件  
**说明**: 读取ClamAV扫描日志内容

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| tail | string | 否 | 尾部行数 | - |
| name | string | 是 | 规则名称 | - |

**返回**: `string` (日志内容)

---

#### POST /api/v1/toolbox/clam/file/update

**Handler**: `baseApi.UpdateFile`  
**功能**: 更新扫描配置文件  
**说明**: 更新ClamAV配置文件内容

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 配置文件名 | - |
| file | string | 是 | 文件内容 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/del

**Handler**: `baseApi.DeleteClam`  
**功能**: 删除扫描规则  
**说明**: 删除指定的ClamAV扫描规则

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| removeInfected | bool | 否 | 是否删除感染文件 | - |
| ids | []uint | 是 | 规则ID列表 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/clam/handle

**Handler**: `baseApi.HandleClamScan`  
**功能**: 执行病毒扫描  
**说明**: 手动触发一次病毒扫描

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 规则ID | - |

**返回**: `无`

---

### 三、Fail2ban 防护模块

#### GET /api/v1/toolbox/fail2ban/base

**Handler**: `baseApi.LoadFail2BanBaseInfo`  
**功能**: 获取Fail2ban基础信息  
**说明**: 获取Fail2ban服务的基本状态和配置信息

**参数**: (无)

**返回**: `Fail2BanBaseInfo`

---

#### POST /api/v1/toolbox/fail2ban/search

**Handler**: `baseApi.SearchFail2Ban`  
**功能**: 查询IP封禁列表  
**说明**: 查询当前被封禁或忽略的IP列表

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| status | string | 是 | 查询类型 | `banned`(已封禁), `ignore`(已忽略) |

**返回**: `string[]` (IP列表)

---

#### POST /api/v1/toolbox/fail2ban/operate

**Handler**: `baseApi.OperateFail2Ban`  
**功能**: Fail2ban服务操作  
**说明**: 启动、停止、重启Fail2ban服务

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| operation | string | 是 | 操作类型 | - |

**返回**: `无`

---

#### POST /api/v1/toolbox/fail2ban/operate/sshd

**Handler**: `baseApi.OperateSSHD`  
**功能**: SSH防护操作  
**说明**: 对SSH服务进行封禁/解封IP操作

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| ips | []string | 否 | IP地址列表 | - |
| operate | string | 是 | 操作类型 | `banned`(封禁), `ignore`(解封) |

**返回**: `无`

---

#### POST /api/v1/toolbox/fail2ban/update

**Handler**: `baseApi.UpdateFail2BanConf`  
**功能**: 更新Fail2ban配置  
**说明**: 更新Fail2ban单个配置项

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| key | string | 是 | 配置键 | `port`, `bantime`, `findtime`, `maxretry`, `banaction`, `logpath` |
| value | string | 是 | 配置值 | - |

**返回**: `无`

---

#### GET /api/v1/toolbox/fail2ban/load/conf

**Handler**: `baseApi.LoadFail2BanConf`  
**功能**: 加载Fail2ban配置文件  
**说明**: 读取/etc/fail2ban/jail.local配置文件内容

**参数**: (无)

**返回**: `string` (配置文件内容)

---

#### POST /api/v1/toolbox/fail2ban/update/byconf

**Handler**: `baseApi.UpdateFail2BanConfByFile`  
**功能**: 通过配置文件更新  
**说明**: 使用完整配置文件内容更新Fail2ban配置

**参数**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| file | string | 是 | 配置文件内容 | - |

**返回**: `无`

---

## 使用说明

- 基础 URL: `http://<1panel-host>:10086/api/v1`
- 认证方式: API Key + Timestamp
- 请求 Content-Type: application/json
