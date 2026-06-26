# Backup Account - 1Panel API

## 模块说明
Backup Account 模块接口，提供备份账号管理、备份/恢复操作、备份记录查询等功能。

## 接口列表 (25 个)

---

### GET /backups/local
**功能**: 获取本地备份目录

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| (string) | string | 本地备份目录路径 |

---

### GET /backups/options
**功能**: 加载备份账号选项列表

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | uint | 备份账号ID |
| name | string | 备份账号名称 |
| type | string | 备份类型 |
| isPublic | bool | 是否公开 |

---

### GET /backups/check/:name
**功能**: 检查备份账号是否被使用

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | ✓ | 备份账号名称 |

---

### POST /backups
**功能**: 创建备份账号

**请求参数** (BackupOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✓ | 备份存储类型 | S3, OSS, AWS-S3, Azure-blob, Google-GCS, Tencent-COS, Huawei-OBS, Kingsoft-KS3, Baidu-BOS, QingStor, MinIO, FTP, SFTP |
| name | string | - | 备份账号名称 | |
| isPublic | bool | - | 是否为公共存储 | true/false |
| bucket | string | - | 存储桶名称 | |
| accessKey | string | - | 访问密钥 | |
| credential | string | - | 访问凭证/密码 | |
| backupPath | string | - | 备份路径 | |
| vars | string | ✓ | 额外变量配置(JSON格式) | |
| rememberAuth | bool | - | 是否记住认证信息 | true/false |

---

### POSTbackup
**功能 /backups/**: 备份系统数据

**请求参数** (CommonBackup):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✓ | 备份数据类型 | app, mysql, mariadb, redis, website, postgresql, mysql-cluster, postgresql-cluster, redis-cluster |
| name | string | - | 备份名称 | |
| detailName | string | - | 详细名称(如应用名称/数据库名/网站名) | |
| secret | string | - | 解密密码 | |
| taskID | string | - | 任务ID | |
| fileName | string | - | 自定义文件名 | |
| args | []string | - | 额外参数 | |
| description | string | - | 备份描述 | |

---

### POST /backups/buckets
**功能**: 获取存储桶列表

**请求参数** (ForBuckets):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | ✓ | 存储类型 |
| accessKey | string | - | 访问密钥 |
| credential | string | ✓ | 访问凭证 |
| vars | string | ✓ | 额外变量配置 |

---

### POST /backups/check
**功能**: 检查备份账号连接

**请求参数** (BackupOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✓ | 备份存储类型 | S3, OSS, AWS-S3, Azure-blob, Google-GCS, Tencent-COS, Huawei-OBS, Kingsoft-KS3, Baidu-BOS, QingStor, MinIO, FTP, SFTP |
| name | string | - | 备份账号名称 | |
| isPublic | bool | - | 是否为公共存储 | true/false |
| bucket | string | - | 存储桶名称 | |
| accessKey | string | - | 访问密钥 | |
| credential | string | - | 访问凭证/密码 | |
| backupPath | string | - | 备份路径 | |
| vars | string | ✓ | 额外变量配置 | |
| rememberAuth | bool | - | 是否记住认证信息 | true/false |

**返回参数** (BackupCheckRes):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| isOk | bool | 连接是否成功 |
| msg | string | 检查消息 |
| token | string | 访问令牌 |

---

### POST /backups/del
**功能**: 删除备份账号

**请求参数** (OperateByID):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | ✓ | 备份账号ID |

---

### POST /backups/record/del
**功能**: 删除备份记录

**请求参数** (BatchDeleteReq):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ids | []uint | ✓ | 备份记录ID列表 |

---

### POST /backups/record/description/update
**功能**: 更新备份记录描述

**请求参数** (UpdateDescription):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | ✓ | 备份记录ID | |
| description | string | ✓ | 描述内容 | 最大256字符 |

---

### POST /backups/record/download
**功能**: 下载备份记录

**请求参数** (DownloadRecord):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| downloadAccountID | uint | ✓ | 下载账号ID |
| fileDir | string | ✓ | 文件目录 |
| fileName | string | ✓ | 文件名 |

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| (string) | string | 文件下载后的本地路径 |

---

### POST /backups/record/search
**功能**: 分页查询备份记录

**请求参数** (RecordSearch):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | ✓ | 页码 | |
| pageSize | int | ✓ | 每页数量 | |
| type | string | ✓ | 备份数据类型 | app, mysql, mariadb, redis, website, postgresql, mysql-cluster, postgresql-cluster, redis-cluster |
| name | string | - | 备份名称 | |
| detailName | string | - | 详细名称 | |

**返回参数** (BackupRecords):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | uint | 记录ID |
| createdAt | time.Time | 创建时间 |
| accountType | string | 账号类型 |
| accountName | string | 账号名称 |
| downloadAccountID | uint | 下载账号ID |
| fileDir | string | 文件目录 |
| fileName | string | 文件名 |
| taskID | string | 任务ID |
| status | string | 状态 |
| message | string | 消息 |
| description | string | 描述 |

---

### POST /backups/record/search/bycronjob
**功能**: 按定时任务查询备份记录

**请求参数** (RecordSearchByCronjob):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | ✓ | 页码 |
| pageSize | int | ✓ | 每页数量 |
| cronjobID | uint | ✓ | 定时任务ID |

**返回参数**: 同 POST /backups/record/search

---

### POST /backups/record/size
**功能**: 获取备份记录大小

**请求参数** (SearchForSize):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | ✓ | 页码 | |
| pageSize | int | ✓ | 每页数量 | |
| type | string | ✓ | 备份数据类型 | app, mysql, mariadb, redis, website, postgresql, mysql-cluster, postgresql-cluster, redis-cluster |
| name | string | - | 备份名称 | |
| detailName | string | - | 详细名称 | |
| info | string | - | 额外信息 | |
| cronjobID | uint | - | 定时任务ID | |
| orderBy | string | - | 排序字段 | |
| order | string | - | 排序方式 | asc/desc |

**返回参数** (RecordFileSize):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | uint | 记录ID |
| name | string | 文件名 |
| size | int64 | 文件大小(字节) |

---

### POST /backups/recover
**功能**: 恢复系统数据

**请求参数** (CommonRecover):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| downloadAccountID | uint | ✓ | 下载账号ID | |
| type | string | ✓ | 数据类型 | app, mysql, mariadb, redis, website, postgresql, mysql-cluster, postgresql-cluster, redis-cluster |
| name | string | - | 备份名称 | |
| detailName | string | - | 详细名称 | |
| file | string | - | 备份文件路径 | |
| secret | string | - | 解密密码 | |
| taskID | string | - | 任务ID | |
| backupRecordID | uint | - | 备份记录ID | |
| timeout | int | - | 超时时间(秒) | |

---

### POST /backups/recover/byupload
**功能**: 通过上传文件恢复数据

**请求参数** (CommonRecover):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| downloadAccountID | uint | ✓ | 下载账号ID | |
| type | string | ✓ | 数据类型 | app, mysql, mariadb, redis, website, postgresql, mysql-cluster, postgresql-cluster, redis-cluster |
| name | string | - | 备份名称 | |
| detailName | string | - | 详细名称 | |
| file | string | - | 备份文件路径 | |
| secret | string | - | 解密密码 | |
| taskID | string | - | 任务ID | |
| backupRecordID | uint | - | 备份记录ID | |
| timeout | int | - | 超时时间(秒) | |

---

### POST /backups/refresh/token
**功能**: 刷新存储访问令牌

**请求参数** (OperateByID):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | ✓ | 备份账号ID |

---

### POST /backups/search
**功能**: 分页查询备份账号

**请求参数** (SearchPageWithType):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | ✓ | 页码 |
| pageSize | int | ✓ | 每页数量 |
| info | string | - | 搜索关键词 |
| type | string | - | 备份账号类型 |

---

### POST /backups/search/files
**功能**: 从备份账号获取文件列表

**请求参数** (OperateByID):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | ✓ | 备份账号ID |

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| []string | []string | 文件路径列表 |

---

### POST /backups/update
**功能**: 更新备份账号

**请求参数** (BackupOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | - | 备份账号ID | |
| type | string | ✓ | 备份存储类型 | S3, OSS, AWS-S3, Azure-blob, Google-GCS, Tencent-COS, Huawei-OBS, Kingsoft-KS3, Baidu-BOS, QingStor, MinIO, FTP, SFTP |
| name | string | - | 备份账号名称 | |
| isPublic | bool | - | 是否为公共存储 | true/false |
| bucket | string | - | 存储桶名称 | |
| accessKey | string | - | 访问密钥 | |
| credential | string | - | 访问凭证/密码 | |
| backupPath | string | - | 备份路径 | |
| vars | string | ✓ | 额外变量配置 | |
| rememberAuth | bool | - | 是否记住认证信息 | true/false |

---

### POST /backups/upload
**功能**: 上传文件用于恢复

**请求参数** (UploadForRecover):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| filePath | string | - | 文件路径 |
| targetDir | string | - | 目标目录 |

---

### GET /core/backups/client/:clientType
**功能**: 加载备份账号基础信息

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| clientType | string | ✓ | 客户端类型 |

---

### POST /core/backups
**功能**: 创建备份账号 (Core)

---

### POST /core/backups/del
**功能**: 删除备份账号 (Core)

---

### POST /core/backups/refresh/token
**功能**: 刷新令牌 (Core)

---

### POST /core/backups/update
**功能**: 更新备份账号 (Core)

---

## 通用数据结构

### PageInfo
分页信息
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | ✓ | 页码 |
| pageSize | int | ✓ | 每页数量 |

### OperateByID
根据ID操作
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | ✓ | 记录ID |

### BatchDeleteReq
批量删除
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ids | []uint | ✓ | 记录ID列表 |

### UpdateDescription
更新描述
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | ✓ | 记录ID | |
| description | string | ✓ | 描述内容 | 最大256字符 |
