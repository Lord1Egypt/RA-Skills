# Menu Setting, System Setting - 1Panel API

## 模块说明
Menu Setting, System Setting 模块接口，包含系统设置、快照管理、SSH连接配置等功能。

## 接口列表 (26 个)

---

### POST /settings/search
**功能**: Load system setting info - 获取系统设置信息

**请求参数**: 无 (不需要请求体)

**返回参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| dockerSockPath | string | Docker socket 路径 |
| systemVersion | string | 系统版本 |
| systemIP | string | 系统 IP 地址 |
| localTime | string | 本地时间 |
| timeZone | string | 时区 |
| ntpSite | NTP 服务器地址 |
| defaultNetwork | string | 默认网络类型 |
| defaultIO | string | 默认 IO 调度器 |
| lastCleanTime | string | 上次清理时间 |
| lastCleanSize | string | 上次清理大小 |
| lastCleanData | string | 上次清理数据类型 |
| monitorStatus | string | 监控状态 (enable/disable) |
| monitorInterval | string | 监控间隔 |
| monitorStoreDays | string | 监控数据保留天数 |
| appStoreVersion | string | 应用商店版本 |
| appStoreLastModified | string | 应用商店最后修改时间 |
| appStoreSyncStatus | string | 应用商店同步状态 |
| fileRecycleBin | string | 文件回收站状态 |

---

### GET /settings/search/available
**功能**: Load system available status - 获取系统可用状态

**请求参数**: 无

**返回参数**: 无 (返回 200 表示系统可用)

---

### POST /settings/update
**功能**: Update system setting - 更新系统设置

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| key | string | 是 | 设置项键名 | validate:"required" |
| value | string | 否 | 设置项值 | - |

**常见 key 值**:
- `DockerSockPath` - Docker socket 路径
- `SystemIP` - 系统 IP
- `TimeZone` - 时区
- `NtpSite` - NTP 服务器
- `MonitorStatus` - 监控状态 (enable/disable)
- `MonitorInterval` - 监控间隔
- `MonitorStoreDays` - 监控数据保留天数
- `AppStoreVersion` - 应用商店版本
- `FileRecycleBin` - 文件回收站

---

### GET /settings/get/{key}
**功能**: Load system setting by key - 根据键名获取系统设置

**路径参数**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 设置项键名 |

**返回参数**: string (设置项的值)

---

### GET /settings/basedir
**功能**: Load local backup dir - 获取本地备份目录

**请求参数**: 无

**返回参数**: string (备份目录路径)

---

### POST /settings/description/save
**功能**: Save common description - 保存通用描述

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| id | string | 是 | 关联 ID | validate:"required" |
| type | string | 是 | 类型 | validate:"required" |
| detailType | string | 否 | 详细类型 | - |
| isPinned | boolean | 否 | 是否置顶 | - |
| description | string | 否 | 描述内容 | - |

---

### GET /settings/snapshot/load
**功能**: Load system snapshot data - 加载系统快照数据

**请求参数**: 无

**返回参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| appData | array | 应用数据树 |
| backupData | array | 备份数据树 |
| panelData | array | 面板数据树 |
| withDockerConf | boolean | 是否包含 Docker 配置 |
| withMonitorData | boolean | 是否包含监控数据 |
| withLoginLog | boolean | 是否包含登录日志 |
| withOperationLog | boolean | 是否包含操作日志 |
| withSystemLog | boolean | 是否包含系统日志 |
| withTaskLog | boolean | 是否包含任务日志 |
| ignoreFiles | array | 忽略文件列表 |

**DataTree 子结构**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 节点 ID |
| label | string | 显示标签 |
| key | string | 键名 |
| name | string | 名称 |
| isLocal | boolean | 是否本地 |
| size | number | 大小 |
| isCheck | boolean | 是否选中 |
| isDisable | boolean | 是否禁用 |
| path | string | 路径 |
| relationItemID | string | 关联项 ID |
| children | array | 子节点 |

---

### POST /settings/snapshot
**功能**: Create system snapshot - 创建系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| id | number | 否 | 快照 ID | - |
| name | string | 否 | 快照名称 | - |
| taskID | string | 否 | 任务 ID | - |
| sourceAccountIDs | string | 是 | 源账户 ID 列表 | validate:"required" |
| downloadAccountID | number | 是 | 下载账户 ID | validate:"required" |
| description | string | 否 | 描述 | validate:"max=256" |
| secret | string | 否 | 密钥 | - |
| interruptStep | string | 否 | 中断步骤 | - |
| timeout | number | 否 | 超时时间(秒) | - |
| appData | array | 否 | 应用数据 | - |
| backupData | array | 否 | 备份数据 | - |
| panelData | array | 否 | 面板数据 | - |
| withDockerConf | boolean | 否 | 包含 Docker 配置 | - |
| withMonitorData | boolean | 否 | 包含监控数据 | - |
| withLoginLog | boolean | 否 | 包含登录日志 | - |
| withOperationLog | boolean | 否 | 包含操作日志 | - |
| withSystemLog | boolean | 否 | 包含系统日志 | - |
| withTaskLog | boolean | 否 | 包含任务日志 | - |
| ignoreFiles | array | 否 | 忽略文件列表 | - |

---

### POST /settings/snapshot/recreate
**功能**: Recreate system snapshot - 重新创建系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| id | number | 是 | 快照 ID | validate:"required" |

---

### POST /settings/snapshot/search
**功能**: Page system snapshot - 分页查询系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| page | number | 是 | 页码 | validate:"required,number" |
| pageSize | number | 是 | 每页数量 | validate:"required,number" |
| info | string | 否 | 搜索关键词 | - |
| orderBy | string | 是 | 排序字段 | validate:"required,oneof=name createdAt" |
| order | string | 是 | 排序方向 | validate:"required,oneof=null ascending descending" |

**返回参数** (PageResult):
| 字段 | 类型 | 说明 |
|------|------|------|
| total | number | 总数 |
| items | array | 快照列表 |

**SnapshotInfo 子结构**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 快照 ID |
| name | string | 快照名称 |
| description | string | 描述 |
| sourceAccounts | array | 源账户列表 |
| downloadAccount | string | 下载账户 |
| status | string | 状态 |
| message | string | 消息 |
| createdAt | time | 创建时间 |
| version | string | 版本 |
| size | number | 大小 |
| taskID | string | 任务 ID |
| taskRecoverID | string | 恢复任务 ID |
| taskRollbackID | string | 回滚任务 ID |
| interruptStep | string | 中断步骤 |
| recoverStatus | string | 恢复状态 |
| recoverMessage | string | 恢复消息 |
| lastRecoveredAt | string | 最后恢复时间 |
| rollbackStatus | string | 回滚状态 |
| rollbackMessage | string | 回滚消息 |
| lastRollbackedAt | string | 最后回滚时间 |

---

### POST /settings/snapshot/import
**功能**: Import system snapshot - 导入系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| backupAccountID | number | 否 | 备份账户 ID | - |
| names | array | 否 | 快照名称列表 | - |
| description | string | 否 | 描述 | validate:"max=256" |

---

### POST /settings/snapshot/del
**功能**: Delete system backup - 删除系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| deleteWithFile | boolean | 否 | 是否同时删除文件 | - |
| ids | array | 是 | 快照 ID 列表 | validate:"required" |

---

### POST /settings/snapshot/recover
**功能**: Recover system backup - 恢复系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| isNew | boolean | 否 | 是否新建恢复 | - |
| reDownload | boolean | 否 | 是否重新下载 | - |
| id | number | 是 | 快照 ID | validate:"required" |
| taskID | string | 否 | 任务 ID | - |
| secret | string | 否 | 密钥 | - |

---

### POST /settings/snapshot/rollback
**功能**: Rollback system backup - 回滚系统快照

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| isNew | boolean | 否 | 是否新建回滚 | - |
| reDownload | boolean | 否 | 是否重新下载 | - |
| id | number | 是 | 快照 ID | validate:"required" |
| taskID | string | 否 | 任务 ID | - |
| secret | string | 否 | 密钥 | - |

---

### POST /settings/snapshot/description/update
**功能**: Update snapshot description - 更新快照描述

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| id | number | 是 | 快照 ID | validate:"required" |
| description | string | 否 | 描述内容 | validate:"max=256" |

---

### GET /settings/ssh/conn
**功能**: Load local conn - 获取本地 SSH 连接信息

**请求参数**: 无

**返回参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| addr | string | SSH 地址 |
| port | number | SSH 端口 |
| user | string | 用户名 |
| authMode | string | 认证模式 (password/key) |
| password | string | 密码 |
| privateKey | string | 私钥 |
| passPhrase | string | 私钥密码短语 |
| localSSHConnShow | string | 本地 SSH 连接显示配置 |

---

### POST /settings/ssh
**功能**: Save local conn info - 保存本地 SSH 连接信息

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| addr | string | 是 | SSH 地址 | validate:"required" |
| port | number | 是 | SSH 端口 (1-65535) | validate:"required,number,max=65535,min=1" |
| user | string | 是 | 用户名 | validate:"required" |
| authMode | string | 是 | 认证模式 | validate:"oneof=password key" |
| password | string | 否 | 密码 (authMode=password 时必填) | - |
| privateKey | string | 否 | 私钥 (authMode=key 时必填) | - |
| passPhrase | string | 否 | 私钥密码短语 | - |
| localSSHConnShow | string | 否 | 本地 SSH 连接显示配置 | - |

---

### POST /settings/ssh/check
**功能**: Check local conn - 检查本地 SSH 连接

**请求参数**: 无 (使用已保存的连接信息)

**返回参数**: boolean (连接是否成功)

---

### POST /settings/ssh/check/info
**功能**: Check local conn info - 通过连接信息检查 SSH 连接

**请求参数**:
| 字段 | 类型 | 必填 | 说明 | 验证规则 |
|------|------|------|------|----------|
| addr | string | 是 | SSH 地址 | validate:"required" |
| port | number | 是 | SSH 端口 (1-65535) | validate:"required,number,max=65535,min=1" |
| user | string | 是 | 用户名 | validate:"required" |
| authMode | string | 是 | 认证模式 | validate:"oneof=password key" |
| password | string | 否 | 密码 | - |
| privateKey | string | 否 | 私钥 | - |
| passPhrase | string | 否 | 私钥密码短语 | - |

**返回参数**: boolean (连接是否成功)

---

### POST /settings/ssh/default
**功能**: Update local is conn - 设置默认 SSH 连接方式

**请求参数**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| withReset | boolean | 否 | 是否重置 |
| defaultConn | string | 否 | 默认连接方式 |

---

## 废弃/未实现的 API (参考原 SKILL 文件，可能已移除或重构)

以下 API 在当前源码中未找到对应实现，可能已被废弃或重构：

- `GET /core/settings/interface` - Load system address
- `GET /core/settings/search/available` - Load system available status
- `GET /core/settings/ssl/info` - Load system cert info
- `GET /core/settings/upgrade` - Load upgrade info
- `GET /core/settings/upgrade/releases` - Load upgrade notes
- `POST /core/settings/api/config/generate/key` - generate api key
- `POST /core/settings/api/config/update` - Update api config
- `POST /core/settings/bind/update` - Update system bind info
- `POST /core/settings/by` - Load system setting by key
- `POST /core/settings/expired/handle` - Reset system password expired
- `POST /core/settings/menu/default` - Default menu
- `POST /core/settings/menu/update` - Update system setting
- `POST /core/settings/mfa` - Load mfa info
- `POST /core/settings/mfa/bind` - Bind mfa
- `POST /core/settings/password/update` - Update system password
- `POST /core/settings/port/update` - Update system port
- `POST /core/settings/proxy/update` - Update proxy setting
- `POST /core/settings/ssl/download` - Download system cert
- `POST /core/settings/ssl/update` - Update system ssl
- `POST /core/settings/terminal/search` - Load system terminal setting info
- `POST /core/settings/terminal/update` - Update system terminal setting
- `POST /core/settings/upgrade` - Upgrade
- `POST /core/settings/upgrade/notes` - Load release notes by version
