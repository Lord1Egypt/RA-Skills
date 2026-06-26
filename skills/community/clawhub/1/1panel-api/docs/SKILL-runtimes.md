# PHP Extensions, Runtime - 1Panel API

## 模块说明
PHP Extensions, Runtime 模块接口，包含运行时创建、删除、配置、管理等完整功能。

## 接口列表 (31 个)

---

### GET /runtimes/:id
**功能**: Get runtime - 获取运行时详情
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | 运行时 ID |

**响应**: `RuntimeDTO`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 运行时 ID |
| name | string | 运行时名称 |
| type | string | 运行时类型 (php/node/python/java/go) |
| resource | string | 资源类型 |
| image | string | 容器镜像 |
| version | string | 版本号 |
| status | string | 运行状态 |
| message | string | 状态消息 |
| port | string | 端口 |
| path | string | 路径 |
| codeDir | string | 代码目录 |
| container | string | 容器名称 |
| containerStatus | string | 容器状态 |
| remark | string | 备注 |
| params | map | 运行时参数 |
| exposedPorts | array | 暴露端口列表 |
| environments | array | 环境变量列表 |
| volumes | array | 挂载卷列表 |
| extraHosts | array | 额外 hosts 列表 |
| appParams | array | 应用参数列表 |

---

### GET /runtimes/installed/delete/check/:id
**功能**: Delete runtime check - 检查运行时删除条件
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | 运行时 ID |

---

### POST /runtimes/search
**功能**: List runtimes - 分页查询运行时列表
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (RuntimeSearch)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| PageInfo | object | 是 | 分页信息 | 见 PageInfo |
| type | string | 否 | 运行时类型 | php/node/python/java/go |
| name | string | 否 | 运行时名称 | 模糊匹配 |
| status | string | 否 | 运行状态 | running/stopped/error |

**PageInfo 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 是 | 页码，从 1 开始 |
| pageSize | int | 是 | 每页数量 |

**响应**: `PageResult<RuntimeDTO>`

---

### POST /runtimes
**功能**: Create runtime - 创建运行时
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (RuntimeCreate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| appDetailId | uint | 是 | 应用详情 ID | |
| name | string | 是 | 运行时名称 | 唯一标识 |
| type | string | 是 | 运行时类型 | php/node/python/java/go |
| version | string | 是 | 版本号 | 如 8.2, 18, 3.10 |
| resource | string | 否 | 资源类型 | local/remote |
| image | string | 否 | 容器镜像 | 自定义镜像地址 |
| source | string | 否 | 来源 | official/custom |
| codeDir | string | 否 | 代码目录 | 应用代码路径 |
| remark | string | 否 | 备注 | |
| params | map | 否 | 运行时参数 | 键值对配置 |
| install | bool | 否 | 是否安装 | 默认 true |
| clean | bool | 否 | 是否清理 | 默认 false |
| exposedPorts | array | 否 | 暴露端口列表 | |
| environments | array | 否 | 环境变量列表 | |
| volumes | array | 否 | 挂载卷列表 | |
| extraHosts | array | 否 | 额外 hosts 列表 | |

**Environment 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 环境变量名 |
| value | string | 是 | 环境变量值 |

**Volume 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | string | 是 | 宿主机路径 |
| target | string | 是 | 容器内路径 |

**ExposedPort 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hostPort | int | 是 | 宿主机端口 |
| containerPort | int | 是 | 容器端口 |
| hostIP | string | 否 | 绑定 IP，默认 0.0.0.0 |

**ExtraHost 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hostname | string | 是 | 主机名 |
| ip | string | 是 | IP 地址 |

---

### POST /runtimes/del
**功能**: Delete runtime - 删除运行时
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (RuntimeDelete)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |
| forceDelete | bool | 否 | 是否强制删除，默认 false |

---

### POST /runtimes/update
**功能**: Update runtime - 更新运行时
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (RuntimeUpdate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 运行时 ID | |
| name | string | 否 | 运行时名称 | |
| type | string | 否 | 运行时类型 | php/node/python/java/go |
| version | string | 否 | 版本号 | |
| image | string | 否 | 容器镜像 | |
| source | string | 否 | 来源 | official/custom |
| codeDir | string | 否 | 代码目录 | |
| rebuild | bool | 否 | 是否重建容器 | 默认 false |
| remark | string | 否 | 备注 | |
| params | map | 否 | 运行时参数 | |
| install | bool | 否 | 是否安装 | |
| clean | bool | 否 | 是否清理 | |
| exposedPorts | array | 否 | 暴露端口列表 | |
| environments | array | 否 | 环境变量列表 | |
| volumes | array | 否 | 挂载卷列表 | |
| extraHosts | array | 否 | 额外 hosts 列表 | |

---

### POST /runtimes/operate
**功能**: Operate runtime - 操作运行时（启动/停止/重启）
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (RuntimeOperate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 运行时 ID | |
| operate | string | 是 | 操作类型 | start/stop/restart |

---

### POST /runtimes/sync
**功能**: Sync runtime status - 同步运行时状态
**参数**: 无

---

### POST /runtimes/node/package
**功能**: Get Node package scripts - 获取 Node.js 包运行脚本
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (NodePackageReq)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| codeDir | string | 是 | 代码目录路径 |

**响应**: `PackageScripts[]`
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 脚本名称 |
| script | string | 脚本内容 |

---

### POST /runtimes/node/modules
**功能**: Get Node modules - 获取 Node.js 模块列表
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (NodeModuleReq)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |

**响应**: `NodeModule[]`
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 模块名称 |
| version | string | 版本号 |
| license | string | 许可证 |
| description | string | 描述 |

---

### POST /runtimes/node/modules/operate
**功能**: Operate Node modules - 操作 Node.js 模块（安装/卸载/更新）
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (NodeModuleOperateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 运行时 ID | |
| operate | string | 是 | 操作类型 | install/uninstall/update |
| module | string | 是 | 模块名称 | |
| pkgManager | string | 否 | 包管理器 | npm/yarn，默认 npm |

---

### GET /runtimes/php/:id/extensions
**功能**: Get php runtime extension - 获取 PHP 扩展列表
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | PHP 运行时 ID |

**响应**: `PHPExtensionRes`
| 字段 | 类型 | 说明 |
|------|------|------|
| extensions | array | 已安装的扩展名列表 |
| supportExtensions | array | 支持的扩展列表 |

**SupportExtension 结构**:
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 扩展名称 |
| description | string | 扩展描述 |
| installed | bool | 是否已安装 |
| check | string | 检查命令 |
| versions | array | 可用版本列表 |
| file | string | 配置文件 |

---

### POST /runtimes/php/extensions/search
**功能**: Page Extensions - 分页查询 PHP 扩展
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPExtensionsSearch)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| PageInfo | object | 是 | 分页信息 |
| all | bool | 否 | 是否查询所有 |

---

### POST /runtimes/php/extensions
**功能**: Create Extensions - 创建 PHP 扩展
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPExtensionsCreate)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 扩展名称 |
| extensions | string | 是 | 扩展配置 |

---

### POST /runtimes/php/extensions/update
**功能**: Update Extensions - 更新 PHP 扩展
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPExtensionsUpdate)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 扩展 ID |
| extensions | string | 是 | 扩展配置 |

---

### POST /runtimes/php/extensions/del
**功能**: Delete Extensions - 删除 PHP 扩展
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPExtensionsDelete)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 扩展 ID |

---

### POST /runtimes/php/extensions/install
**功能**: Install php extension - 安装 PHP 扩展
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPExtensionInstallReq)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |
| name | string | 是 | 扩展名称 |
| taskID | string | 否 | 任务 ID |

---

### POST /runtimes/php/extensions/uninstall
**功能**: UnInstall php extension - 卸载 PHP 扩展
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPExtensionInstallReq)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |
| name | string | 是 | 扩展名称 |
| taskID | string | 否 | 任务 ID |

---

### GET /runtimes/php/config/:id
**功能**: Load php runtime conf - 获取 PHP 配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | PHP 运行时 ID |

**响应**: `PHPConfig`

---

### POST /runtimes/php/config
**功能**: Update runtime php conf - 更新 PHP 配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPConfigUpdate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | PHP 运行时 ID | |
| scope | string | 是 | 配置范围 | php-fpm/php |
| params | map | 否 | 配置参数 | 键值对 |
| disableFunctions | array | 否 | 禁用函数列表 | |
| uploadMaxSize | string | 否 | 上传文件最大尺寸 | 如 50M |
| maxExecutionTime | string | 否 | 最大执行时间 | 如 60 |

---

### POST /runtimes/php/update
**功能**: Update php conf file - 更新 PHP 配置文件
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPFileUpdate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | PHP 运行时 ID | |
| type | string | 是 | 文件类型 | php/php-fpm |
| content | string | 是 | 文件内容 | 配置内容 |

---

### POST /runtimes/php/file
**功能**: Get php conf file - 获取 PHP 配置文件
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPFileReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | PHP 运行时 ID | |
| type | string | 是 | 文件类型 | php/php-fpm |

**响应**: `FileInfo`
| 字段 | 类型 | 说明 |
|------|------|------|
| content | string | 文件内容 |

---

### GET /runtimes/php/fpm/config/:id
**功能**: Get fpm config - 获取 PHP-FPM 配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | PHP 运行时 ID |

**响应**: `FPMConfig`

---

### POST /runtimes/php/fpm/config
**功能**: Update fpm config - 更新 PHP-FPM 配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (FPMConfig)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | PHP 运行时 ID |
| params | map | 是 | FPM 配置参数 |

---

### GET/php/fpm/status /runtimes/:id
**功能**: Get PHP runtime status - 获取 PHP-FPM 状态
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | PHP 运行时 ID |

**响应**: `FpmStatusItem[]`
| 字段 | 类型 | 说明 |
|------|------|------|
| key | string | 状态项名称 |
| value | interface{} | 状态值 |

---

### POST /runtimes/php/container/update
**功能**: Update PHP container config - 更新 PHP 容器配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPContainerConfig)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | PHP 运行时 ID |
| containerName | string | 否 | 容器名称 |
| exposedPorts | array | 否 | 暴露端口列表 |
| environments | array | 否 | 环境变量列表 |
| volumes | array | 否 | 挂载卷列表 |
| extraHosts | array | 否 | 额外 hosts 列表 |

---

### GET /runtimes/php/container/:id
**功能**: Get PHP container config - 获取 PHP 容器配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | PHP 运行时 ID |

**响应**: `PHPContainerConfig`

---

### GET /runtimes/supervisor/process/:id
**功能**: Get supervisor process - 获取 Supervisor 进程配置
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| id | path | integer | 是 | 运行时 ID |

**响应**: `SupervisorProcessConfig[]`

---

### POST /runtimes/supervisor/process
**功能**: Operate supervisor process - 操作 Supervisor 进程
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPSupervisorProcessConfig)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |
| SupervisorProcessConfig | object | 是 | Supervisor 进程配置 |

**SupervisorProcessConfig 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| command | string | 是 | 启动命令 |
| user | string | 否 | 运行用户 |
| directory | string | 否 | 工作目录 |
| autostart | bool | 否 | 自动启动 |
| autorestart | bool | 否 | 自动重启 |
| redirectStderr | bool | 否 | 重定向错误输出 |
| stdoutLogFile | string | 否 | 标准输出日志 |
| stderrLogFile | string | 否 | 错误输出日志 |

---

### POST /runtimes/supervisor/process/file
**功能**: Operate supervisor process file - 操作 Supervisor 进程配置文件
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (PHPSupervisorProcessFileReq)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |
| SupervisorProcessFileReq | object | 是 | 文件操作请求 |

**SupervisorProcessFileReq 结构**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| operation | string | 是 | 操作类型 | get/update |
| name | string | 否 | 进程名称 | |

**响应**: 文件内容或操作结果

---

### POST /runtimes/remark
**功能**: Update runtime remark - 更新运行时备注
**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| request | body | object | 是 | 请求体 |

**request 请求体 (RuntimeRemark)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 运行时 ID |
| remark | string | 是 | 备注内容 |

---

## 通用结构说明

### PageInfo (分页信息)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 是 | 页码，从 1 开始 |
| pageSize | int | 是 | 每页数量，默认 20 |

### PageResult (分页结果)
| 字段 | 类型 | 说明 |
|------|------|------|
| total | int64 | 总数 |
| items | array | 数据列表 |

### ExposedPort (暴露端口)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hostPort | int | 是 | 宿主机端口 |
| containerPort | int | 是 | 容器端口 |
| hostIP | string | 否 | 绑定 IP，默认 0.0.0.0 |

### Environment (环境变量)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 环境变量名 |
| value | string | 是 | 环境变量值 |

### Volume (挂载卷)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | string | 是 | 宿主机路径 |
| target | string | 是 | 容器内路径 |

### ExtraHost (额外 hosts)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hostname | string | 是 | 主机名 |
| ip | string | 是 | IP 地址 |

## 运行时类型 (Type 取值)
- `php` - PHP 运行环境
- `node` - Node.js 运行环境
- `python` - Python 运行环境
- `java` - Java 运行环境
- `go` - Go 运行环境

## 运行状态 (Status 取值)
- `running` - 运行中
- `stopped` - 已停止
- `error` - 错误状态
- `installing` - 安装中
- `unknown` - 未知

## 操作类型 (Operate 取值)
- `start` - 启动
- `stop` - 停止
- `restart` - 重启

## Node 模块操作类型
- `install` - 安装
- `uninstall` - 卸载
- `update` - 更新
