# App - 1Panel API

## 模块说明
App 模块接口，提供应用商店和已安装应用的管理功能。

## 文件路径说明

### 已安装应用目录结构

1Panel 安装的应用会创建以下文件和目录：

| 路径类型 | 说明 | 计算方式 |
|----------|------|----------|
| **应用根目录** | 已安装应用的主目录 | `GetAppPath()` = `{应用安装目录}/{应用Key}/{应用名称}` |
| **网站根目录** | 网站静态文件存放目录 | `/opt/1panel/www/sites/{网站名称}/index` |
| **docker-compose.yml** | Docker Compose 配置文件 | `GetComposePath()` = `{应用根目录}/docker-compose.yml` |
| **.env** | 环境变量文件 | `GetEnvPath()` = `{应用根目录}/.env` |

### 源码中的路径计算方法

```go
// 获取应用根目录
func (i *AppInstall) GetAppPath() string {
    if i.App.Resource == "local" {
        // 本地应用
        return path.Join(本地应用安装目录, strings.TrimPrefix(i.App.Key, "local"))
    } else {
        // 远程/自定义应用
        return path.Join(应用安装目录, i.App.Key)
    }
}

// 获取 docker-compose.yml 路径
func (i *AppInstall) GetComposePath() string {
    return path.Join(i.GetAppPath(), i.Name, "docker-compose.yml")
}

// 获取 .env 文件路径
func (i *AppInstall) GetEnvPath() string {
    return path.Join(i.GetAppPath(), i.Name, ".env")
}
```

### 应用目录变量说明

| 变量 | 说明 |
|------|------|
| `应用安装目录` | 1Panel 配置的应用安装根目录（默认为 `/opt/1panel/apps/`） |
| `本地应用安装目录` | 1Panel 本地应用安装目录（默认为 `/opt/1panel/apps/local/`） |
| `应用Key` | 应用的唯一标识，如 `openresty`、`mysql`、`redis` 等 |
| `应用名称` | 用户安装时指定的名称 |

### 常见应用路径示例

| 应用 | Key | 安装名称 | 路径 |
|------|-----|----------|------|
| OpenResty | openresty | openresty | `/opt/1panel/apps/openresty/openresty` |
| 网站 | static | mywebsite | `/opt/1panel/www/sites/mywebsite/index` |
| MySQL | mysql | mysql | `/opt/1panel/apps/mysql/mysql` |
| Redis | redis | redis-cache | `/opt/1panel/apps/redis/redis-cache` |

### AppInstall 模型关键字段

| 字段 | 类型 | 说明 |
|------|------|------|
| Name | string | 应用安装名称（用户指定） |
| AppId | uint | 应用 ID |
| AppDetailId | uint | 应用详情 ID |
| Version | string | 安装版本 |
| ContainerName | string | 容器名称 |
| ServiceName | string | 服务名称 |
| HttpPort | int | HTTP 端口 |
| HttpsPort | int | HTTPS 端口 |
| Status | string | 运行状态 |

## 接口列表 (33 个)

---

### GET /apps/search
**功能**: 分页搜索应用列表
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| name | string | 否 | 应用名称（模糊搜索） | - |
| tags | []string | 否 | 标签列表 | - |
| type | string | 否 | 应用类型 | - |
| recommend | bool | 否 | 仅推荐应用 | - |
| resource | string | 否 | 资源类型 | - |
| showCurrentArch | bool | 否 | 显示当前架构支持 | - |

---

### GET /apps/sync/remote
**功能**: 同步远程应用商店列表
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| taskID | string | 否 | 异步任务 ID | - |

---

### GET /apps/sync/local
**功能**: 同步本地应用列表
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| taskID | string | 否 | 异步任务 ID | - |

---

### GET /apps/:key
**功能**: 根据 key 获取应用信息
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 应用唯一标识 key |

---

### GET /apps/tags
**功能**: 获取应用商店所有标签

---

### GET /apps/checkupdate
**功能**: 检查应用商店更新
**返回**: 应用商店是否有可用更新

---

### GET /apps/detail/:appId/:version/:type
**功能**: 根据应用 ID、版本和类型获取应用详情
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appId | int | 是 | 应用 ID |
| version | string | 是 | 应用版本 |
| type | string | 是 | 应用类型 |

---

### GET /apps/detail/node/:appKey/:version
**功能**: 根据应用 key 和版本获取应用详情（节点专用）
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appKey | string | 是 | 应用 key |
| version | string | 是 | 应用版本 |

---

### GET /apps/details/:id
**功能**: 根据应用详情 ID 获取应用详情
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 应用详情 ID |

---

### GET /apps/icon/:key
**功能**: 获取应用图标
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 应用 key |

---

### POST /apps/install
**功能**: 安装应用
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| appDetailId | uint | 是 | 应用详情 ID | > 0 |
| name | string | 是 | 安装名称 | - |
| params | map[string]interface{} | 否 | 应用参数 | - |
| services | map[string]string | 否 | 服务映射 | - |
| taskID | string | 否 | 任务 ID | - |
| advanced | bool | 否 | 高级选项 | - |
| cpuQuota | float64 | 否 | CPU 配额 (%) | 0-100 |
| memoryLimit | float64 | 否 | 内存限制 | > 0 |
| memoryUnit | string | 否 | 内存单位 | MB/GB |
| containerName | string | 否 | 容器名称 | - |
| allowPort | bool | 否 | 允许自动开放端口 | - |
| editCompose | bool | 否 | 编辑 Docker Compose | - |
| dockerCompose | string | 否 | Docker Compose 内容 | - |
| hostMode | bool | 否 | 主机网络模式 | - |
| pullImage | bool | 否 | 强制拉取镜像 | - |
| gpuConfig | bool | 否 | GPU 配置 | - |
| webUI | string | 否 | Web UI 地址 | - |
| type | string | 否 | 应用类型 | - |
| specifyIP | string | 否 | 指定出口 IP | - |
| restartPolicy | string | 否 | 重启策略 | always/unless-stopped/no/on-failure |
| nodes | []string | 否 | 节点列表 | - |
| pushNode | bool | 否 | 推送到节点 | - |
| appKey | string | 否 | 应用 key | - |
| version | string | 否 | 版本 | - |

---

### GET /apps/installed/search
**功能**: 分页搜索已安装应用
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| type | string | 否 | 应用类型 | - |
| name | string | 否 | 应用名称 | - |
| tags | []string | 否 | 标签列表 | - |
| update | bool | 否 | 检查更新 | - |
| unused | bool | 否 | 仅未使用 | - |
| all | bool | 否 | 返回所有（不分页） | - |
| sync | bool | 否 | 同步应用 | - |
| checkUpdate | bool | 否 | 检查更新状态 | - |

---

### GET /apps/installed/list
**功能**: 获取所有已安装应用列表

---

### POST /apps/installed/check
**功能**: 检查应用是否已安装
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 应用 key |
| name | string | 否 | 应用名称 |

---

### POST /apps/installed/loadport
**功能**: 获取应用端口
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 名称 |
| type | string | 是 | 类型 |

---

### POST /apps/installed/conninfo
**功能**: 获取应用数据库连接信息
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 名称 |
| type | string | 是 | 类型 |

---

### GET /apps/installed/delete/check/:appInstallId
**功能**: 删除前检查应用依赖
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appInstallId | int | 是 | 已安装应用 ID |

---

### POST /apps/installed/sync
**功能**: 同步已安装应用列表

---

### POST /apps/installed/op
**功能**: 操作已安装应用
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| installId | uint | 是 | 已安装应用 ID | > 0 |
| operate | string | 是 | 操作类型 | start/stop/restart/delete/sync/backup/update/rebuild/upgrade/reload/favorite |
| backupId | uint | 否 | 备份 ID | - |
| detailId | uint | 否 | 详情 ID | - |
| forceDelete | bool | 否 | 强制删除 | - |
| deleteBackup | bool | 否 | 删除关联备份 | - |
| deleteDB | bool | 否 | 删除关联数据库 | - |
| backup | bool | 否 | 操作前备份 | - |
| pullImage | bool | 否 | 强制拉取镜像 | - |
| dockerCompose | string | 否 | Docker Compose | - |
| taskID | string | 否 | 任务 ID | - |
| deleteImage | bool | 否 | 删除容器镜像 | - |
| favorite | bool | 否 | 收藏/取消收藏 | - |

---

### GET /apps/services/:key
**功能**: 获取应用关联服务
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 应用 key |

---

### POST /apps/installed/port/change
**功能**: 修改应用端口
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 否 | 应用 key |
| name | string | 否 | 应用名称 |
| port | int64 | 是 | 新端口 |

---

### POST /apps/installed/conf
**功能**: 获取应用默认配置
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 名称 |
| type | string | 是 | 类型 |

---

### GET /apps/installed/params/:appInstallId
**功能**: 获取已安装应用的当前参数
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appInstallId | int | 是 | 已安装应用 ID |

---

### POST /apps/installed/params/update
**功能**: 修改已安装应用参数
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| installId | uint | 是 | 已安装应用 ID | > 0 |
| params | map[string]interface{} | 是 | 参数映射 | - |
| advanced | bool | 否 | 高级选项 | - |
| cpuQuota | float64 | 否 | CPU 配额 (%) | 0-100 |
| memoryLimit | float64 | 否 | 内存限制 | > 0 |
| memoryUnit | string | 否 | 内存单位 | MB/GB |
| containerName | string | 否 | 容器名称 | - |
| allowPort | bool | 否 | 允许开放端口 | - |
| editCompose | bool | 否 | 编辑 Compose | - |
| dockerCompose | string | 否 | Docker Compose | - |
| hostMode | bool | 否 | 主机模式 | - |
| pullImage | bool | 否 | 拉取镜像 | - |
| gpuConfig | bool | 否 | GPU 配置 | - |
| webUI | string | 否 | Web UI | - |
| type | string | 否 | 类型 | - |
| specifyIP | string | 否 | 指定 IP | - |
| restartPolicy | string | 否 | 重启策略 | always/unless-stopped/no/on-failure |

---

### POST /apps/installed/update/versions
**功能**: 获取应用可升级版本列表
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appInstallID | uint | 是 | 已安装应用 ID |
| updateVersion | string | 否 | 指定版本 |

---

### POST /apps/installed/config/update
**功能**: 更新应用配置（如 Web UI 地址）
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| installID | uint | 是 | 已安装应用 ID |
| webUI | string | 否 | Web UI 地址 |

---

### GET /apps/installed/info/:appInstallId
**功能**: 获取已安装应用详细信息
**参数 (Path)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appInstallId | int | 是 | 已安装应用 ID |

---

### POST /apps/installed/sort/update
**功能**: 更新已安装应用排序
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| items | []AppInstallSortItem | 是 | 排序项列表 |

**AppInstallSortItem**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| installID | uint | 是 | 已安装应用 ID |
| sortOrder | int | 是 | 排序顺序 |

---

### GET /apps/ignored/detail
**功能**: 获取忽略升级的应用列表

---

### POST /apps/installed/ignore
**功能**: 忽略应用升级
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| appID | uint | 是 | 应用 ID | > 0 |
| appDetailID | uint | 否 | 应用详情 ID | - |
| scope | string | 是 | 忽略范围 | all/version |

---

### POST /apps/ignored/cancel
**功能**: 取消忽略应用升级
**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | uint | 是 | 记录 ID |

---

## 枚举值参考

### AppOperate (应用操作类型)
| 值 | 说明 |
|-----|------|
| start | 启动 |
| stop | 停止 |
| restart | 重启 |
| delete | 删除 |
| sync | 同步 |
| backup | 备份 |
| update | 更新 |
| rebuild | 重建 |
| upgrade | 升级 |
| reload | 重载 |
| favorite | 收藏 |

### RestartPolicy (容器重启策略)
| 值 | 说明 |
|-----|------|
| always | 始终重启 |
| unless-stopped | 除非停止 |
| no | 不重启 |
| on-failure | 失败时重启 |

### Scope (忽略升级范围)
| 值 | 说明 |
|-----|------|
| all | 忽略所有版本 |
| version | 仅忽略当前版本 |
