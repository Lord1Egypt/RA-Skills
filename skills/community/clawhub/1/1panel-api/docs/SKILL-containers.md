# Container, Container Compose, Container Compose-template, Container Docker, Container Image, Container Image-repo, Container Network, Container Volume - 1Panel API

## 模块说明
Container, Container Compose, Container Compose-template, Container Docker, Container Image, Container Image-repo, Container Network, Container Volume 模块接口

## 接口列表 (62 个)

---

### GET /containers/daemonjson
**功能**: Load docker daemon.json (获取 Docker 守护进程配置)

---

### GET /containers/daemonjson/file
**功能**: Load docker daemon.json file (获取 Docker 守护进程配置文件)

---

### GET /containers/docker/status
**功能**: Load docker status (获取 Docker 状态)
**参数**: 无

---

### GET /containers/image
**功能**: load images options (获取镜像选项列表)

---

### GET /containers/image/all
**功能**: List all images (列出所有镜像)

---

### GET /containers/network
**功能**: List networks (获取网络列表)

---

### GET /containers/repo
**功能**: List image repos (获取镜像仓库列表)

---

### GET /containers/search/log
**功能**: Container logs (获取容器日志 - 流式)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| container | string | 是 | 容器名称或ID | - |
| since | string | 否 | 时间筛选（Unix 时间戳） | - |
| follow | string | 否 | 是否追踪日志实时输出 | true/false |
| tail | string | 否 | 显示最后 N 行 | 数字，如 "100" |
| timestamp | string | 否 | 是否显示时间戳 | true/false |

---

### GET /containers/stats/:id
**功能**: Container stats (获取容器实时统计信息)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | string | 是 | 容器 ID（路径参数） | - |

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| cpuPercent | float64 | CPU 使用百分比 |
| memory | float64 | 内存使用量（字节） |
| cache | float64 | 缓存使用量（字节） |
| ioRead | float64 | 磁盘读取速度（字节/秒） |
| ioWrite | float64 | 磁盘写入速度（字节/秒） |
| networkRX | float64 | 网络接收速率（字节/秒） |
| networkTX | float64 | 网络发送速率（字节/秒） |
| shotTime | time | 统计时间 |

---

### GET /containers/status
**功能**: Load containers status (获取容器状态统计)

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| created | int | 已创建容器数量 |
| running | int | 运行中容器数量 |
| paused | int | 暂停容器数量 |
| restarting | int | 重启中容器数量 |
| removing | int | 删除中容器数量 |
| exited | int | 已退出容器数量 |
| dead | int | 死亡容器数量 |
| containerCount | int | 容器总数 |
| composeCount | int | Compose 项目数量 |
| composeTemplateCount | int | Compose 模板数量 |
| imageCount | int | 镜像数量 |
| networkCount | int | 网络数量 |
| volumeCount | int | 卷数量 |
| repoCount | int | 镜像仓库数量 |

---

### GET /containers/template
**功能**: List compose templates (获取 Compose 模板列表)

---

### GET /containers/volume
**功能**: List volumes (获取卷列表)

---

### GET /containers/limit
**功能**: Load container limits (获取容器资源限制)

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| cpu | int | CPU 核心数限制 |
| memory | uint64 | 内存限制（字节） |

---

### GET /containers/list/stats
**功能**: Load container stats list (获取容器统计列表)

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| []ContainerListStats | array | 容器统计列表 |

**ContainerListStats 结构**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| containerID | string | 容器 ID |
| cpuTotalUsage | uint64 | CPU 总使用量 |
| systemUsage | uint64 | 系统 CPU 使用量 |
| cpuPercent | float64 | CPU 使用百分比 |
| percpuUsage | int | 每 CPU 使用量 |
| memoryCache | uint64 | 内存缓存 |
| memoryUsage | uint64 | 内存使用量 |
| memoryLimit | uint64 | 内存限制 |
| memoryPercent | float64 | 内存使用百分比 |

---

### GET /containers/network
**功能**: List networks (获取网络列表)

---

### GET /containers/image/all
**功能**: List all images (获取所有镜像列表)

---

### GET /containers/repo
**功能**: List image repos (获取镜像仓库列表)

---

### POST /containers
**功能**: Create container (创建容器)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID（异步任务） | - |
| name | string | 是 | 容器名称 | - |
| image | string | 是 | 镜像名称 | - |
| hostname | string | 否 | 主机名 | - |
| domainName | string | 否 | 域名 | - |
| dns | []string | 否 | DNS 服务器列表 | - |
| networks | []ContainerNetwork | 否 | 网络配置 | - |
| publishAllPorts | bool | 否 | 发布所有端口 | true/false |
| exposedPorts | []PortHelper | 否 | 暴露端口列表 | - |
| tty | bool | 否 | 分配伪终端 | true/false |
| openStdin | bool | 否 | 打开标准输入 | true/false |
| workingDir | string | 否 | 工作目录 | - |
| user | string | 否 | 用户名/UID | - |
| cmd | []string | 否 | 启动命令 | - |
| entrypoint | []string | 否 | 入口点 | - |
| cpuShares | int64 | 否 | CPU 权重 | - |
| nanoCPUs | float64 | 否 | CPU 核心数 | - |
| memory | float64 | 否 | 内存限制（字节） | - |
| privileged | bool | 否 | 特权模式 | true/false |
| autoRemove | bool | 否 | 容器退出时自动删除 | true/false |
| volumes | []VolumeHelper | 否 | 卷挂载配置 | - |
| labels | []string | 否 | 标签列表 | - |
| env | []string | 否 | 环境变量 | - |
| restartPolicy | string | 否 | 重启策略 | no, always, on-failure, unless-stopped |

**ContainerNetwork 结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| network | string | 是 | 网络名称 | - |
| ipv4 | string | 否 | IPv4 地址 | - |
| ipv6 | string | 否 | IPv6 地址 | - |
| macAddr | string | 否 | MAC 地址 | - |

**VolumeHelper 结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 卷类型 | bind, volume |
| sourceDir | string | 否 | 主机目录（bind 类型） | - |
| containerDir | string | 是 | 容器内目录 | - |
| mode | string | 否 | 挂载模式 | ro, rw |
| shared | string | 否 | 共享模式 | - |

**PortHelper 结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| hostIP | string | 否 | 主机 IP | - |
| hostPort | string | 是 | 主机端口 | - |
| containerPort | string | 是 | 容器端口 | - |
| protocol | string | 否 | 协议 | tcp, udp |

---

### POST /containers/update
**功能**: Update container (更新容器配置)
**参数**: 同 POST /containers（创建容器参数）

---

### POST /containers/upgrade
**功能**: Upgrade container (升级容器镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| names | []string | 是 | 容器名称列表 | - |
| image | string | 是 | 新镜像名称 | - |
| forcePull | bool | 否 | 强制拉取镜像 | true/false |

---

### POST /containers/search
**功能**: Page containers (分页查询容器)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| name | string | 否 | 容器名称筛选 | - |
| state | string | 否 | 容器状态筛选 | all, created, running, paused, restarting, removing, exited, dead |
| orderBy | string | 是 | 排序字段 | name, createdAt, state |
| order | string | 是 | 排序方式 | null, ascending, descending |
| filters | string | 否 | 筛选条件 | - |
| excludeAppStore | bool | 否 | 排除应用商店容器 | true/false |

---

### POST /containers/list
**功能**: List containers (获取容器列表)

---

### POST /containers/list/byimage
**功能**: List containers by image (根据镜像获取容器列表)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 镜像名称 | - |

---

### POST /containers/info
**功能**: Load container info (获取容器详细信息)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 容器名称 | - |

---

### POST /containers/inspect
**功能**: Container inspect (容器深度检查)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | string | 是 | 容器 ID 或名称 | - |
| type | string | 是 | 检查类型 | - |
| detail | string | 否 | 详情 | - |

---

### POST /containers/operate
**功能**: Operate Container (容器操作：启动/停止/重启/删除等)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| names | []string | 是 | 容器名称列表 | - |
| operation | string | 是 | 操作类型 | up, start, stop, restart, kill, pause, unpause, remove |

---

### POST /containers/prune
**功能**: Clean container (清理容器/镜像/卷/网络)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| pruneType | string | 是 | 清理类型 | container, image, volume, network, buildcache |
| withTagAll | bool | 否 | 是否清理所有标签的镜像 | true/false |

---

### POST /containers/rename
**功能**: Rename Container (重命名容器)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 当前容器名称 | - |
| newName | string | 是 | 新容器名称 | - |

---

### POST /containers/commit
**功能**: Commit Container (将容器提交为镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| containerID | string | 是 | 容器 ID | - |
| containerName | string | 否 | 容器名称 | - |
| newImageName | string | 否 | 新镜像名称 | - |
| comment | string | 否 | 镜像注释 | - |
| author | string | 否 | 作者 | - |
| pause | bool | 否 | 提交前是否暂停容器 | true/false |
| taskID | string | 否 | 任务 ID | - |

---

### POST /containers/clean/log
**功能**: Clean container log (清理容器日志)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 容器名称 | - |

---

### POST /containers/download/log
**功能**: Download container logs (下载容器日志)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| container | string | 是 | 容器名称 | - |
| since | string | 否 | 时间筛选（Unix 时间戳） | - |
| tail | uint | 否 | 显示最后 N 行 | - |
| timestamp | bool | 否 | 是否包含时间戳 | true/false |
| containerType | string | 否 | 容器类型 | - |

---

### POST /containers/users
**功能**: Load container users (获取容器用户列表)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 容器名称 | - |

---

### POST /containers/item/stats
**功能**: Load container stats size (获取容器存储统计)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 容器名称 | - |

**返回参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| sizeRw | int64 | 读写层大小 |
| sizeRootFs | int64 | 根文件系统大小 |
| containerUsage | int64 | 容器使用空间 |
| containerReclaimable | int64 | 容器可回收空间 |
| imageUsage | int64 | 镜像使用空间 |
| imageReclaimable | int64 | 镜像可回收空间 |
| volumeUsage | int64 | 卷使用空间 |
| volumeReclaimable | int64 | 卷可回收空间 |
| buildCacheUsage | int64 | 构建缓存使用空间 |
| buildCacheReclaimable | int64 | 构建缓存可回收空间 |

---

### POST /containers/network/search
**功能**: Page networks (分页查询网络)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |

---

### POST /containers/network
**功能**: Create network (创建网络)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 网络名称 | - |
| driver | string | 是 | 网络驱动 | bridge, host, overlay, macvlan 等 |
| options | []string | 否 | 网络选项 | - |
| ipv4 | bool | 否 | 是否启用 IPv4 | true/false |
| subnet | string | 否 | IPv4 子网（如 172.17.0.0/16） | - |
| gateway | string | 否 | IPv4 网关 | - |
| ipRange | string | 否 | IPv4 地址范围 | - |
| auxAddress | []SettingUpdate | 否 | 辅助地址 | - |
| ipv6 | bool | 否 | 是否启用 IPv6 | true/false |
| subnetV6 | string | 否 | IPv6 子网 | - |
| gatewayV6 | string | 否 | IPv6 网关 | - |
| ipRangeV6 | string | 否 | IPv6 地址范围 | - |
| auxAddressV6 | []SettingUpdate | 否 | IPv6 辅助地址 | - |
| labels | []string | 否 | 标签 | - |

**SettingUpdate 结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| key | string | 是 | 键 | - |
| value | string | 是 | 值 | - |

---

### POST /containers/network/del
**功能**: Delete network (删除网络)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| force | bool | 否 | 强制删除 | true/false |
| names | []string | 是 | 网络名称列表 | - |

---

### POST /containers/volume/search
**功能**: Page volumes (分页查询卷)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |

---

### POST /containers/volume
**功能**: Create volume (创建卷)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 卷名称 | - |
| driver | string | 是 | 卷驱动 | local, etc. |
| options | []string | 否 | 卷选项 | - |
| labels | []string | 否 | 标签 | - |

---

### POST /containers/volume/del
**功能**: Delete volume (删除卷)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| force | bool | 否 | 强制删除 | true/false |
| names | []string | 是 | 卷名称列表 | - |

---

### POST /containers/image/search
**功能**: Page images (分页查询镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| name | string | 否 | 镜像名称筛选 | - |
| orderBy | string | 是 | 排序字段 | size, tags, createdAt, isUsed |
| order | string | 是 | 排序方式 | null, ascending, descending |

---

### POST /containers/image/pull
**功能**: Pull image (拉取镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| repoID | uint | 否 | 仓库 ID | - |
| imageName | []string | 是 | 镜像名称列表 | - |

---

### POST /containers/image/push
**功能**: Push image (推送镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| repoID | uint | 是 | 目标仓库 ID | - |
| tagName | string | 是 | 镜像标签 | - |
| name | string | 是 | 镜像名称 | - |

---

### POST /containers/image/remove
**功能**: Delete image (删除镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| names | []string | 是 | 镜像名称/ID 列表 | - |

---

### POST /containers/image/tag
**功能**: Tag image (标记镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| sourceID | string | 是 | 源镜像 ID | - |
| tags | []string | 是 | 新标签列表 | - |

---

### POST /containers/image/build
**功能**: Build image (构建镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| from | string | 是 | 基础镜像 | - |
| name | string | 是 | 镜像名称 | - |
| dockerfile | string | 是 | Dockerfile 内容 | - |
| tags | []string | 否 | 镜像标签 | - |
| args | []string | 否 | 构建参数 | - |

---

### POST /containers/image/save
**功能**: Save image (导出镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| tagName | string | 是 | 镜像标签 | - |
| path | string | 是 | 保存路径 | - |
| name | string | 是 | 镜像名称 | - |

---

### POST /containers/image/load
**功能**: Load image (导入镜像)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| paths | []string | 是 | 镜像文件路径列表 | - |

---

### POST /containers/compose/search
**功能**: Page composes (分页查询 Compose 项目)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |

---

### POST /containers/compose
**功能**: Create compose (创建 Compose 项目)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| name | string | 是 | 项目名称 | - |
| from | string | 是 | 来源类型 | edit, path, template |
| file | string | 否 | Compose 文件内容 | - |
| path | string | 否 | Compose 文件路径 | - |
| template | uint | 否 | 模板 ID | - |
| env | string | 否 | 环境变量内容 | - |
| forcePull | bool | 否 | 强制拉取镜像 | true/false |

---

### POST /containers/compose/test
**功能**: Test compose (测试 Compose 配置)
**参数**: 同 POST /containers/compose

---

### POST /containers/compose/operate
**功能**: Operate compose (Compose 项目操作)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 项目名称 | - |
| path | string | 否 | 项目路径 | - |
| operation | string | 是 | 操作类型 | up, start, restart, stop, down, delete |
| withFile | bool | 否 | 是否使用 .env 文件 | true/false |
| force | bool | 否 | 强制操作 | true/false |

---

### POST /containers/compose/update
**功能**: Update compose (更新 Compose 项目)
**参数**:
| 参数名 | 类型 | 必填 |说明 | 取值范围 |
|--------|------|------|------|----------|
| taskID | string | 否 | 任务 ID | - |
| name | string | 是 | 项目名称 | - |
| path | string | 是 | 项目路径 | - |
| detailPath | string | 否 | 详情路径 | - |
| content | string | 是 | Compose 文件内容 | - |
| env | string | 否 | 环境变量内容 | - |
| forcePull | bool | 否 | 强制拉取镜像 | true/false |

---

### POST /containers/compose/env
**功能**: Load compose environment variables (加载 Compose 环境变量)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | Compose 项目路径 | - |

---

### POST /containers/compose/clean/log
**功能**: Clean compose log (清理 Compose 日志)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 项目名称 | - |
| path | string | 是 | 项目路径 | - |
| detailPath | string | 否 | 详情路径 | - |

---

### POST /containers/template/search
**功能**: Page compose templates (分页查询 Compose 模板)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |

---

### POST /containers/template
**功能**: Create compose template (创建 Compose 模板)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 模板名称 | - |
| description | string | 否 | 模板描述 | - |
| content | string | 否 | 模板内容 | - |

---

### POST /containers/template/update
**功能**: Update compose template (更新 Compose 模板)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 模板 ID | - |
| description | string | 否 | 模板描述 | - |
| content | string | 否 | 模板内容 | - |

---

### POST /containers/template/del
**功能**: Delete compose template (删除 Compose 模板)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ids | []uint | 是 | 模板 ID 列表 | - |

---

### POST /containers/template/batch
**功能**: Batch compose template (批量创建模板)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| templates | []ComposeTemplateCreate | 是 | 模板列表 | - |

**ComposeTemplateCreate 结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 模板名称 | - |
| description | string | 否 | 模板描述 | - |
| content | string | 否 | 模板内容 | - |

---

### POST /containers/repo/search
**功能**: Page image repos (分页查询镜像仓库)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| info | string | 否 | 搜索关键词 | - |

---

### POST /containers/repo
**功能**: Create image repo (创建镜像仓库)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 仓库名称 | - |
| downloadUrl | string | 否 | 下载 URL | - |
| protocol | string | 否 | 协议 | http, https |
| username | string | 否 | 用户名 | - |
| password | string | 否 | 密码 | - |
| auth | bool | 否 | 是否启用认证 | true/false |

---

### POST /containers/repo/update
**功能**: Update image repo (更新镜像仓库)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 仓库 ID | - |
| downloadUrl | string | 否 | 下载 URL | - |
| protocol | string | 否 | 协议 | http, https |
| username | string | 否 | 用户名 | - |
| password | string | 否 | 密码 | - |
| auth | bool | 否 | 是否启用认证 | true/false |

---

### POST /containers/repo/del
**功能**: Delete image repo (删除镜像仓库)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ids | []uint | 是 | 仓库 ID 列表 | - |

---

### POST /containers/repo/status
**功能**: Load repo status (获取仓库状态)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 仓库 ID | - |

---

### POST /containers/docker/operate
**功能**: Operate docker (操作 Docker 服务)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | 是 | 操作类型 | start, restart, stop |

---

### POST /containers/daemonjson/update
**功能**: Update docker daemon.json (更新 Docker 守护进程配置)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| isSwarm | bool | 否 | 是否启用 Swarm | true/false |
| version | string | 否 | Docker 版本 | - |
| registryMirrors | []string | 否 | 镜像加速器列表 | - |
| insecureRegistries | []string | 否 | 非安全仓库列表 | - |
| liveRestore | bool | 否 | 容器退出时保持运行 | true/false |
| iptables | bool | 否 | 是否启用 iptables | true/false |
| cgroupDriver | string | 否 | Cgroup 驱动 | cgroupfs, systemd |
| ipv6 | bool | 否 | 是否启用 IPv6 | true/false |
| fixedCidrV6 | string | 否 | IPv6 固定 CIDR | - |
| ip6Tables | bool | 否 | 是否启用 ip6tables | true/false |
| experimental | bool | 否 | 是否启用实验特性 | true/false |
| logMaxSize | string | 否 | 日志最大大小 | - |
| logMaxFile | string | 否 | 日志最大文件数 | - |

---

### POST /containers/daemonjson/update/byfile
**功能**: Update docker daemon.json by upload file (通过文件更新 Docker 配置)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| file | string | 是 | 配置文件内容 | - |

---

### POST /containers/logoption/update
**功能**: Update docker daemon.json log option (更新 Docker 日志配置)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| logMaxSize | string | 否 | 单个日志文件最大大小 | - |
| logMaxFile | string | 否 | 最多保留的日志文件数 | - |

---

### POST /containers/ipv6option/update
**功能**: Update docker daemon.json ipv6 option (更新 Docker IPv6 配置)
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| fixedCidrV6 | string | 否 | IPv6 固定 CIDR | - |
| ip6Tables | bool | 是 | 是否启用 ip6tables | true/false |
| experimental | bool | 否 | 是否启用实验特性 | true/false |

---

### GET /containers/exec
**功能**: Container SSH WebSocket (容器 SSH WebSocket 连接)
**参数**: 通过 WebSocket 协议

---

