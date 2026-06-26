# Device, FTP, Fail2ban, Clam - 1Panel API

## 模块说明
Device, FTP, Fail2ban, Clam 模块接口，提供主机设备管理、FTP 用户管理、Fail2ban 防火墙和 Clam 杀毒软件的相关 API。

## 接口列表 (39 个)

---

### Device 设备管理

#### POST /toolbox/device/base
**功能**: 获取设备基础信息
**说明**: 返回主机的基础配置信息，包括 DNS、主机名、时区、用户、Swap 内存等
**参数**: 无

#### GET /toolbox/device/users
**功能**: 获取用户列表
**说明**: 返回系统所有用户列表
**参数**: 无

#### GET /toolbox/device/zone/options
**功能**: 获取时区选项列表
**说明**: 返回可用的时区列表
**参数**: 无

#### POST /toolbox/device/conf
**功能**: 加载设备配置文件
**说明**: 根据名称加载指定的配置文件内容
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 配置文件名称 | - |

#### POST /toolbox/device/update/conf
**功能**: 更新设备配置
**说明**: 更新主机的系统配置参数
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| key | string | 是 | 配置键名 | DNS/NtpSite/TimeZone 等 |
| value | string | 否 | 配置值 | - |

#### POST /toolbox/device/update/host
**功能**: 更新主机 Hosts
**说明**: 更新系统的 hosts 映射配置
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ip | string | 是 | IP 地址 | - |
| host | string | 是 | 主机名 | - |

#### POST /toolbox/device/update/passwd
**功能**: 更新用户密码
**说明**: 修改指定用户的密码
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| user | string | 是 | 用户名 | - |
| passwd | string | 是 | 新密码（Base64 编码） | - |

#### POST /toolbox/device/update/swap
**功能**: 更新 Swap 配置
**说明**: 创建、删除或修改 Swap 文件
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | Swap 文件路径 | - |
| size | uint64 | 否 | Swap 大小（字节） | - |
| used | string | 否 | 使用状态 | - |
| isNew | bool | 否 | 是否新建 | - |
| taskID | string | 否 | 任务 ID | - |

#### POST /toolbox/device/update/byconf
**功能**: 通过配置文件更新设备
**说明**: 通过文件内容更新设备配置
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 配置名称 | - |
| file | string | 否 | 配置文件内容 | - |

#### POST /toolbox/device/check/dns
**功能**: 检查 DNS 配置
**说明**: 验证 DNS 配置是否有效
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| key | string | 是 | DNS 配置键 | - |
| value | string | 否 | DNS 服务器地址 | - |

#### POST /toolbox/scan
**功能**: 扫描系统垃圾文件
**说明**: 扫描可清理的系统垃圾文件，返回清理建议
**参数**: 无

#### POST /toolbox/clean
**功能**: 清理系统垃圾文件
**说明**: 根据扫描结果清理指定的垃圾文件
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| treeType | string | 是 | 清理类型 | - |
| name | string | 是 | 清理项名称 | - |
| size | uint64 | 是 | 清理大小（字节） | - |

---

### Fail2ban 防护

#### GET /toolbox/fail2ban/base
**功能**: 获取 Fail2ban 基础信息
**说明**: 返回 Fail2ban 服务状态和配置信息
**参数**: 无

#### GET /toolbox/fail2ban/load/conf
**功能**: 加载 Fail2ban 配置文件
**说明**: 返回 /etc/fail2ban/jail.local 配置文件内容
**参数**: 无

#### POST /toolbox/fail2ban/search
**功能**: 查询封禁 IP 列表
**说明**: 分页查询被封禁或忽略的 IP 地址
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| status | string | 是 | 查询状态 | banned / ignore |

#### POST /toolbox/fail2ban/operate
**功能**: 操作 Fail2ban 服务
**说明**: 启动、停止、重启 Fail2ban 服务
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | 是 | 操作类型 | start / stop / restart |

#### POST /toolbox/fail2ban/operate/sshd
**功能**: 操作 SSH 防护规则
**说明**: 手动封禁或解封 IP
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ips | []string | 否 | IP 地址列表 | - |
| operate | string | 是 | 操作类型 | banned / ignore |

#### POST /toolbox/fail2ban/update
**功能**: 更新 Fail2ban 配置
**说明**: 修改 Fail2ban 的运行参数
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| key | string | 是 | 配置键 | port / bantime / findtime / maxretry / banaction / logpath |
| value | string | 否 | 配置值 | - |

#### POST /toolbox/fail2ban/update/byconf
**功能**: 通过配置文件更新 Fail2ban
**说明**: 通过文件内容更新 Fail2ban 配置
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| file | string | 否 | 配置文件内容 | - |

---

### FTP 管理

#### GET /toolbox/ftp/base
**功能**: 获取 FTP 基础信息
**说明**: 返回 FTP 服务状态和安装状态
**参数**: 无

#### POST /toolbox/ftp/log/search
**功能**: 查询 FTP 操作日志
**说明**: 分页查询 FTP 用户的操作日志
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| user | string | 否 | 用户名（筛选） | - |
| operation | string | 否 | 操作类型（筛选） | - |

#### POST /toolbox/ftp/operate
**功能**: 操作 FTP 服务
**说明**: 启动、停止、重启 FTP 服务
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | 是 | 操作类型 | start / stop / restart |

#### POST /toolbox/ftp/search
**功能**: 分页查询 FTP 用户
**说明**: 分页查询已创建的 FTP 账户
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |

#### POST /toolbox/ftp
**功能**: 创建 FTP 用户
**说明**: 创建新的 FTP 账户
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| user | string | 是 | 用户名 | - |
| password | string | 是 | 密码（Base64 编码） | - |
| path | string | 是 | 根目录路径 | - |
| description | string | 否 | 描述信息 | - |

#### POST /toolbox/ftp/update
**功能**: 更新 FTP 用户
**说明**: 修改 FTP 账户信息
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | FTP 账户 ID | - |
| password | string | 是 | 新密码（Base64 编码） | - |
| path | string | 是 | 根目录路径 | - |
| status | string | 否 | 状态 | enabled / disabled |
| description | string | 否 | 描述信息 | - |

#### POST /toolbox/ftp/del
**功能**: 删除 FTP 用户
**说明**: 删除指定的 FTP 账户
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ids | []uint | 是 | FTP 账户 ID 列表 | - |

#### POST /toolbox/ftp/sync
**功能**: 同步 FTP 用户
**说明**: 同步系统用户与 FTP 账户
**参数**: 无

---

### Clam 杀毒

#### POST /toolbox/clam
**功能**: 创建扫描规则
**说明**: 创建新的 Clam 扫描规则
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 规则名称 | - |
| status | string | 否 | 状态 | enabled / disabled |
| path | string | 否 | 扫描路径 | - |
| infectedStrategy | string | 否 | 感染文件处理策略 | - |
| infectedDir | string | 否 | 感染文件隔离目录 | - |
| spec | string | 否 | 定时任务规格 | cron 表达式 |
| timeout | uint | 否 | 超时时间（秒） | - |
| description | string | 否 | 描述信息 | - |
| alertCount | uint | 否 | 告警数量阈值 | - |
| alertTitle | string | 否 | 告警标题 | - |
| alertMethod | string | 否 | 告警方式 | - |

#### POST /toolbox/clam/base
**功能**: 获取 Clam 基础信息
**说明**: 返回 ClamAV 杀毒软件的状态和版本信息
**参数**: 无

#### POST /toolbox/clam/update
**功能**: 更新扫描规则
**说明**: 修改已存在的 Clam 扫描规则
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 规则 ID | - |
| name | string | 否 | 规则名称 | - |
| path | string | 否 | 扫描路径 | - |
| infectedStrategy | string | 否 | 感染文件处理策略 | - |
| infectedDir | string | 否 | 感染文件隔离目录 | - |
| spec | string | 否 | 定时任务规格 | cron 表达式 |
| timeout | uint | 否 | 超时时间（秒） | - |
| description | string | 否 | 描述信息 | - |
| alertCount | uint | 否 | 告警数量阈值 | - |
| alertTitle | string | 否 | 告警标题 | - |
| alertMethod | string | 否 | 告警方式 | - |

#### POST /toolbox/clam/status/update
**功能**: 更新规则状态
**说明**: 启用或禁用指定的扫描规则
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 规则 ID | - |
| status | string | 否 | 状态 | enabled / disabled |

#### POST /toolbox/clam/search
**功能**: 分页查询扫描规则
**说明**: 分页查询已创建的 Clam 扫描规则
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |
| orderBy | string | 是 | 排序字段 | name / status / createdAt |
| order | string | 是 | 排序方式 | null / ascending / descending |

#### POST /toolbox/clam/operate
**功能**: 操作 Clam 服务
**说明**: 启动、停止 ClamAV 服务
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | 是 | 操作类型 | start / stop |

#### POST /toolbox/clam/record/clean
**功能**: 清空扫描记录
**说明**: 清空指定规则的扫描记录
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 规则 ID | - |

#### POST /toolbox/clam/record/search
**功能**: 分页查询扫描记录
**说明**: 分页查询扫描任务的执行记录
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| clamID | uint | 否 | 规则 ID | - |
| status | string | 否 | 扫描状态 | - |
| startTime | time | 否 | 开始时间 | - |
| endTime | time | 否 | 结束时间 | - |

#### POST /toolbox/clam/file/search
**功能**: 加载扫描日志文件
**说明**: 加载指定规则或记录的战斗日志
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| tail | string | 否 | 日志尾行数 | - |
| name | string | 是 | 规则名称 | - |

#### POST /toolbox/clam/file/update
**功能**: 更新扫描文件配置
**说明**: 更新规则的文件扫描配置
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 配置名称 | - |
| file | string | 否 | 配置文件内容 | - |

#### POST /toolbox/clam/del
**功能**: 删除扫描规则
**说明**: 删除指定的扫描规则，可选择是否删除感染文件
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| removeInfected | bool | 否 | 是否删除感染文件 | - |
| ids | []uint | 是 | 规则 ID 列表 | - |

#### POST /toolbox/clam/handle
**功能**: 执行病毒扫描
**说明**: 手动触发一次扫描任务
**参数**:
| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 规则 ID | - |
