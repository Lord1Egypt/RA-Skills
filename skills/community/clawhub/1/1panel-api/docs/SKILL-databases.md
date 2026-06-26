# Database, Database Common, Database Mysql, Database PostgreSQL, Database Redis - 1Panel API

## 模块说明
Database, Database Common, Database Mysql, Database PostgreSQL, Database Redis 模块接口

## 接口列表 (42 个)

---

### GET /databases/db/:name
**功能**: Get databases - 获取数据库详情

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |

**返回**: `dto.DatabaseInfo` - 数据库详细信息

---

### GET /databases/db/item/:type
**功能**: List databases - 获取数据库列表项

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 是 | 数据库类型 (mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster) |

**返回**: `dto.DatabaseItem[]` - 数据库列表项数组

---

### GET /databases/db/list/:type
**功能**: List databases - 获取数据库选项列表

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 是 | 数据库类型 (mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster) |

**返回**: `dto.DatabaseOption[]` - 数据库选项数组

---

### POST /databases
**功能**: Create mysql database - 创建 MySQL 数据库

**请求体 (dto.MysqlDBCreate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 数据库名称 | 最大256字符 |
| from | string | 是 | 数据来源 | local, remote |
| database | string | 是 | 远程数据库标识 | |
| format | string | 是 | 字符集格式 | utf8mb4, utf8, latin1 等 |
| collation | string | 否 | 排序规则 | |
| username | string | 是 | 数据库用户名 | |
| password | string | 是 | 数据库密码 (Base64编码) | |
| permission | string | 是 | 权限 | ALL, SELECT, INSERT, UPDATE, DELETE 等 |
| description | string | 否 | 数据库描述 | 最大256字符 |

---

### POST /databases/bind
**功能**: Bind user of mysql database - 绑定 MySQL 数据库用户

**请求体 (dto.BindUser)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| database | string | 是 | 数据库名称 |
| db | string | 是 | 数据库标识 |
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 (Base64编码) |
| permission | string | 是 | 权限 |

---

### POST /databases/change/access
**功能**: Change mysql access - 修改 MySQL 数据库访问权限

**请求体 (dto.ChangeDBInfo)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| from | string | 是 | 数据来源 | local, remote |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |
| database | string | 是 | 数据库名称 |
| value | string | 是 | 权限设置 (如 %) | |

---

### POST /databases/change/password
**功能**: Change mysql password - 修改 MySQL 数据库密码

**请求体 (dto.ChangeDBInfo)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| from | string | 是 | 数据来源 | local, remote |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |
| database | string | 是 | 数据库名称 |
| value | string | 是 | 新密码 (Base64编码) | |

---

### POST /databases/common/info
**功能**: Load base info - 加载数据库基础信息

**请求体 (dto.OperationWithNameAndType)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 数据库名称 | |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |

**返回**: `dto.DBBaseInfo` - 数据库基础信息
| 字段 | 类型 | 说明 |
|------|------|------|
| Name | string | 数据库名称 |
| ContainerName | string | 容器名称 |
| Port | int64 | 端口号 |

---

### POST /databases/common/load/file
**功能**: Load Database conf - 加载数据库配置文件

**请求体 (dto.OperationWithNameAndType)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 数据库名称 | |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |

**返回**: `string` - 配置文件内容

---

### POST /databases/common/update/conf
**功能**: Update conf by upload file - 通过上传文件更新数据库配置

**请求体 (dto.DBConfUpdateByFile)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |
| database | string | 是 | 数据库名称 | |
| file | string | 否 | 配置文件内容 | |

---

### POST /databases/db
**功能**: Create database - 创建远程数据库

**请求体 (dto.DatabaseCreate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 数据库名称 | 最大256字符 |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |
| from | string | 是 | 数据来源 | local, remote |
| version | string | 是 | 数据库版本 | |
| address | string | 否 | 远程数据库地址 | |
| port | uint | 否 | 端口号 | |
| initialDB | string | 否 | 初始数据库 | |
| username | string | 是 | 数据库用户名 | |
| password | string | 否 | 数据库密码 | |
| ssl | bool | 否 | 是否使用SSL连接 | |
| rootCert | string | 否 | CA证书 (Base64编码) | |
| clientKey | string | 否 | 客户端私钥 (Base64编码) | |
| clientCert | string | 否 | 客户端证书 (Base64编码) | |
| skipVerify | bool | 否 | 是否跳过证书验证 | |
| timeout | uint | 否 | 连接超时时间(秒) | |
| description | string | 否 | 数据库描述 | |

---

### POST /databases/db/check
**功能**: Check database - 检查数据库连接性

**请求体 (dto.DatabaseCreate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 数据库名称 | 最大256字符 |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |
| from | string | 是 | 数据来源 | local, remote |
| version | string | 是 | 数据库版本 | |
| address | string | 否 | 远程数据库地址 | |
| port | uint | 否 | 端口号 | |
| initialDB | string | 否 | 初始数据库 | |
| username | string | 是 | 数据库用户名 | |
| password | string | 否 | 数据库密码 | |
| ssl | bool | 否 | 是否使用SSL连接 | |
| rootCert | string | 否 | CA证书 (Base64编码) | |
| clientKey | string | 否 | 客户端私钥 (Base64编码) | |
| clientCert | string | 否 | 客户端证书 (Base64编码) | |
| skipVerify | bool | 否 | 是否跳过证书验证 | |
| timeout | uint | 否 | 连接超时时间(秒) | |
| description | string | 否 | 数据库描述 | |

**返回**: `boolean` - 是否可连接

---

### POST /databases/db/del
**功能**: Delete database - 删除远程数据库

**请求体 (dto.DatabaseDelete)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 是 | 数据库记录ID |
| forceDelete | bool | 否 | 是否强制删除 |
| deleteBackup | bool | 否 | 是否删除备份 |

---

### POST /databases/db/del/check
**功能**: Check before delete remote database - 删除前检查远程数据库

**请求体 (dto.OperateByID)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 是 | 数据库记录ID |

**返回**: `string[]` - 关联的应用列表

---

### POST /databases/db/search
**功能**: Page databases - 分页查询数据库

**请求体 (dto.DatabaseSearch)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | |
| pageSize | int | 是 | 每页数量 | |
| info | string | 否 | 搜索关键词 | |
| type | string | 否 | 数据库类型 | |
| orderBy | string | 是 | 排序字段 | name, createdAt |
| order | string | 是 | 排序方式 | null, ascending, descending |

**返回**: `dto.PageResult` - 分页结果

---

### POST /databases/db/update
**功能**: Update database - 更新远程数据库

**请求体 (dto.DatabaseUpdate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| type | string | 是 | 数据库类型 | mysql, mariadb, postgresql, redis, mysql-cluster, postgresql-cluster, redis-cluster |
| version | string | 是 | 数据库版本 | |
| address | string | 否 | 远程数据库地址 | |
| port | uint | 否 | 端口号 | |
| initialDB | string | 否 | 初始数据库 | |
| username | string | 是 | 数据库用户名 | |
| password | string | 否 | 数据库密码 | |
| ssl | bool | 否 | 是否使用SSL连接 | |
| rootCert | string | 否 | CA证书 (Base64编码) | |
| clientKey | string | 否 | 客户端私钥 (Base64编码) | |
| clientCert | string | 否 | 客户端证书 (Base64编码) | |
| skipVerify | bool | 否 | 是否跳过证书验证 | |
| timeout | uint | 否 | 连接超时时间(秒) | |
| description | string | 否 | 数据库描述 | |

---

### POST /databases/del
**功能**: Delete mysql database - 删除 MySQL 数据库

**请求体 (dto.MysqlDBDelete)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |
| database | string | 是 | 数据库名称 | |
| forceDelete | bool | 否 | 是否强制删除 | |
| deleteBackup | bool | 否 | 是否删除备份 | |

---

### POST /databases/del/check
**功能**: Check before delete mysql database - 删除 MySQL 数据库前检查

**请求体 (dto.MysqlDBDeleteCheck)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |
| database | string | 是 | 数据库名称 | |

**返回**: `string[]` - 关联的应用列表

---

### POST /databases/description/update
**功能**: Update mysql database description - 更新 MySQL 数据库描述

**请求体 (dto.UpdateDescription)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 是 | 数据库记录ID |
| description | string | 是 | 数据库描述 (最大256字符) |

---

### POST /databases/format/options
**功能**: List mysql database format collation options - 获取 MySQL 数据库字符集和排序规则选项

**请求体 (dto.OperationWithName)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |

**返回**: `dto.MysqlFormatCollationOption[]` - 字符集选项列表
| 字段 | 类型 | 说明 |
|------|------|------|
| Format | string | 字符集格式 |
| Collations | string[] | 可用的排序规则列表 |

---

### POST /databases/load
**功能**: Load mysql database from remote - 从远程加载 MySQL 数据库

**请求体 (dto.MysqlLoadDB)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| from | string | 是 | 数据来源 | local, remote |
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |
| database | string | 是 | 数据库名称 | |

---

### POST /databases/pg
**功能**: Create postgresql database - 创建 PostgreSQL 数据库

**请求体 (dto.PostgresqlDBCreate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 数据库名称 | |
| from | string | 是 | 数据来源 | local, remote |
| database | string | 是 | 远程数据库标识 | |
| format | string | 否 | 字符集格式 | |
| username | string | 是 | 数据库用户名 | |
| password | string | 是 | 数据库密码 (Base64编码) | |
| superUser | bool | 否 | 是否为超级用户 | |
| description | string | 否 | 数据库描述 | |

---

### POST /databases/pg/:database/load
**功能**: Load postgresql database from remote - 从远程加载 PostgreSQL 数据库

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| database | string | 是 | 数据库名称 |

---

### POST /databases/pg/bind
**功能**: Bind postgresql user - 绑定 PostgreSQL 用户

**请求体 (dto.PostgresqlBindUser)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |
| database | string | 是 | 数据库标识 |
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |
| superUser | bool | 否 | 是否为超级用户 |

---

### POST /databases/pg/del
**功能**: Delete postgresql database - 删除 PostgreSQL 数据库

**请求体 (dto.PostgresqlDBDelete)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| type | string | 是 | 数据库类型 | postgresql, postgresql-cluster |
| database | string | 是 | 数据库名称 | |
| forceDelete | bool | 否 | 是否强制删除 | |
| deleteBackup | bool | 否 | 是否删除备份 | |

---

### POST /databases/pg/del/check
**功能**: Check before delete postgresql database - 删除 PostgreSQL 数据库前检查

**请求体 (dto.PostgresqlDBDeleteCheck)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| type | string | 是 | 数据库类型 | postgresql, postgresql-cluster |
| database | string | 是 | 数据库名称 | |

**返回**: `string[]` - 关联的应用列表

---

### POST /databases/pg/description
**功能**: Update postgresql database description - 更新 PostgreSQL 数据库描述

**请求体 (dto.UpdateDescription)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 是 | 数据库记录ID |
| description | string | 是 | 数据库描述 (最大256字符) |

---

### POST /databases/pg/password
**功能**: Change postgresql password - 修改 PostgreSQL 密码

**请求体 (dto.ChangeDBInfo)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 数据库记录ID | |
| from | string | 是 | 数据来源 | local, remote |
| type | string | 是 | 数据库类型 | postgresql, postgresql-cluster |
| database | string | 是 | 数据库名称 |
| value | string | 是 | 新密码 (Base64编码) | |

---

### POST /databases/pg/privileges
**功能**: Change postgresql privileges - 修改 PostgreSQL 用户权限

**请求体 (dto.PostgresqlPrivileges)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |
| database | string | 是 | 数据库标识 |
| username | string | 是 | 用户名 |
| superUser | bool | 否 | 是否为超级用户 |

---

### POST /databases/pg/search
**功能**: Page postgresql databases - 分页查询 PostgreSQL 数据库

**请求体 (dto.PostgresqlDBSearch)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | |
| pageSize | int | 是 | 每页数量 | |
| info | string | 否 | 搜索关键词 | |
| database | string | 是 | 数据库标识 | |
| orderBy | string | 是 | 排序字段 | name, createdAt |
| order | string | 是 | 排序方式 | null, ascending, descending |

**返回**: `dto.PageResult` - 分页结果

---

### POST /databases/redis/conf
**功能**: Load redis conf - 加载 Redis 配置

**请求体 (dto.LoadRedisStatus)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |
| type | string | 是 | 数据库类型 |

**返回**: `dto.RedisConf` - Redis 配置信息
| 字段 | 类型 | 说明 |
|------|------|------|
| Database | string | 数据库标识 |
| Name | string | 数据库名称 |
| Port | int64 | 端口号 |
| ContainerName | string | 容器名称 |
| Timeout | string | 超时时间 |
| Maxclients | string | 最大客户端数 |
| Requirepass | string | 密码 |
| Maxmemory | string | 最大内存 |

---

### POST /databases/redis/conf/update
**功能**: Update redis conf - 更新 Redis 配置

**请求体 (dto.RedisConfUpdate)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| database | string | 是 | 数据库标识 |
| timeout | string | 否 | 超时时间 |
| maxclients | string | 否 | 最大客户端数 |
| maxmemory | string | 否 | 最大内存 |
| dbType | string | 是 | 数据库类型 (redis, redis-cluster) |

---

### POST /databases/redis/install/cli
**功能**: Install redis-cli - 安装 Redis CLI 工具

**无请求参数**

---

### POST /databases/redis/password
**功能**: Change redis password - 修改 Redis 密码

**请求体 (dto.ChangeRedisPass)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| database | string | 是 | 数据库标识 |
| value | string | 是 | 新密码 |

---

### POST /databases/redis/persistence/conf
**功能**: Load redis persistence conf - 加载 Redis 持久化配置

**请求体 (dto.LoadRedisStatus)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |
| type | string | 是 | 数据库类型 |

**返回**: `dto.RedisPersistence` - Redis 持久化配置
| 字段 | 类型 | 说明 |
|------|------|------|
| Database | string | 数据库标识 |
| Appendonly | string | AOF持久化开关 |
| Appendfsync | string | AOF同步策略 |
| Save | string | RDB保存策略 |

---

### POST /databases/redis/persistence/update
**功能**: Update redis persistence conf - 更新 Redis 持久化配置

**请求体 (dto.RedisConfPersistenceUpdate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| database | string | 是 | 数据库标识 | |
| type | string | 是 | 持久化类型 | aof, rbd |
| appendonly | string | 否 | AOF持久化开关 | |
| appendfsync | string | 否 | AOF同步策略 | |
| save | string | 否 | RDB保存策略 | |
| dbType | string | 是 | 数据库类型 | redis, redis-cluster |

---

### POST /databases/redis/status
**功能**: Load redis status info - 加载 Redis 状态信息

**请求体 (dto.LoadRedisStatus)**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 数据库名称 |
| type | string | 是 | 数据库类型 |

**返回**: `dto.RedisStatus` - Redis 状态信息

---

### POST /databases/remote
**功能**: Load mysql remote access - 加载 MySQL 远程访问设置

**请求体 (dto.OperationWithNameAndType)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 数据库名称 | |
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |

**返回**: `boolean` - 是否开启远程访问

---

### POST /databases/search
**功能**: Page mysql databases - 分页查询 MySQL 数据库

**请求体 (dto.MysqlDBSearch)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | |
| pageSize | int | 是 | 每页数量 | |
| info | string | 否 | 搜索关键词 | |
| database | string | 是 | 数据库标识 | |
| orderBy | string | 是 | 排序字段 | name, createdAt |
| order | string | 是 | 排序方式 | null, ascending, descending |

**返回**: `dto.PageResult` - 分页结果

---

### POST /databases/status
**功能**: Load mysql status info - 加载 MySQL 状态信息

**请求体 (dto.OperationWithNameAndType)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 数据库名称 | |
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |

**返回**: `dto.MysqlStatus` - MySQL 状态信息

---

### POST /databases/variables
**功能**: Load mysql variables info - 加载 MySQL 变量信息

**请求体 (dto.OperationWithNameAndType)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 否 | 数据库名称 | |
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |

**返回**: `dto.MysqlVariables` - MySQL 变量信息
| 字段 | 类型 | 说明 |
|------|------|------|
| BinlogCacheSize | string | Binlog缓存大小 |
| InnodbBufferPoolSize | string | InnoDB缓冲池大小 |
| InnodbLogBufferSize | string | InnoDB日志缓冲大小 |
| JoinBufferSize | string | Join缓冲大小 |
| KeyBufferSize | string | 键缓冲大小 |
| MaxConnections | string | 最大连接数 |
| MaxHeapTableSize | string | 最大内存表大小 |
| QueryCacheSize | string | 查询缓存大小 |
| QueryCacheType | string | 查询缓存类型 |
| ReadBufferSize | string | 读缓冲大小 |
| ReadRndBufferSize | string | 随机读缓冲大小 |
| SortBufferSize | string | 排序缓冲大小 |
| TableOpenCache | string | 表缓存大小 |
| ThreadCacheSize | string | 线程缓存大小 |
| ThreadStack | string | 线程栈大小 |
| TmpTableSize | string | 临时表大小 |
| SlowQueryLog | string | 慢查询日志 |
| LongQueryTime | string | 慢查询时间阈值 |

---

### POST /databases/variables/update
**功能**: Update mysql variables - 更新 MySQL 变量

**请求体 (dto.MysqlVariablesUpdate)**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 数据库类型 | mysql, mariadb, mysql-cluster |
| database | string | 是 | 数据库名称 | |
| variables | array | 是 | 变量数组 | |

**variables 数组项 (dto.MysqlVariablesUpdateHelper)**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| param | string | 变量名 |
| value | any | 变量值 |

