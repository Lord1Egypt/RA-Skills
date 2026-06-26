# Dashboard - 1Panel API

## 模块说明
Dashboard 模块提供系统仪表盘相关功能，包括系统信息加载、应用启动器管理、快速跳转配置、实时监控数据获取等。

## 接口列表 (12 个)

---

### GET /dashboard/base/os
**功能**: Load OS information (获取操作系统基本信息)

**请求参数**: 无

**返回参数** (`OsInfo`):
| 字段 | 类型 | 说明 |
|------|------|------|
| OS | string | 操作系统名称 |
| platform | string | 平台 |
| platformFamily | string | 平台家族 |
| kernelArch | string | 内核架构 |
| kernelVersion | string | 内核版本 |
| prettyDistro | string | 发行版名称 |
| diskSize | int64 | 磁盘大小(字节) |

---

### GET /dashboard/quick/option
**功能**: Load quick jump options (获取快速跳转选项列表)

**请求参数**: 无

**返回参数** (`QuickJump[]`):
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 跳转项ID |
| name | string | 名称 |
| alias | string | 别名 |
| title | string | 显示标题 |
| detail | string | 详情描述 |
| recommend | int | 推荐级别 |
| isShow | bool | 是否显示 |
| router | string | 路由地址 |

---

### POST /dashboard/quick/change
**功能**: Update quick jump (更新快速跳转配置)

**请求参数** (`ChangeQuicks`):
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| quicks | []QuickJump | 是 | 快速跳转项列表 |

**QuickJump 详情**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 跳转项ID |
| name | string | 名称 |
| alias | string | 别名 |
| title | string | 显示标题 |
| detail | string | 详情描述 |
| recommend | int | 推荐级别 (0=不推荐, 1=推荐) |
| isShow | bool | 是否显示 |
| router | string | 路由地址 |

**返回**: 操作成功返回 200

---

### GET /dashboard/app/launcher
**功能**: Load app launcher (获取应用启动器列表)

**请求参数**: 无

**返回参数** (`AppLauncher[]`):
| 字段 | 类型 | 说明 |
|------|------|------|
| key | string | 启动器唯一标识 |
| type | string | 类型 |
| name | string | 名称 |
| icon | string | 图标路径 |
| limit | int | 限制数量 |
| description | string | 描述 |
| recommend | int | 推荐级别 |
| isInstall | bool | 是否已安装 |
| isRecommend | bool | 是否推荐 |
| detail | []InstallDetail | 详细信息列表 |

**InstallDetail 详情**:
| 字段 | 类型 | 说明 |
|------|------|------|
| installID | uint | 安装ID |
| detailID | uint | 详情ID |
| name | string | 名称 |
| version | string | 版本 |
| path | string | 安装路径 |
| status | string | 状态 |
| webUI | string | Web界面地址 |
| httpPort | int | HTTP端口 |
| httpsPort | int | HTTPS端口 |

---

### POST /dashboard/app/launcher/show
**功能**: Update app Launcher (更新应用启动器显示配置)

**请求参数** (`SettingUpdate`):
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 设置键 (如: "app_launcher_xxx") |
| value | string | 否 | 设置值 (如: "true"/"false") |

**返回**: 操作成功返回 200

**日志记录**: 记录 key 和 value 的变更

---

### POST /dashboard/app/launcher/option
**功能**: Load app launcher options (获取应用启动器选项列表)

**请求参数** (`SearchByFilter`):
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| filter | string | 否 | 过滤条件 |

**返回参数** (`LauncherOption[]`):
| 字段 | 类型 | 说明 |
|------|------|------|
| key | string | 启动器标识 |
| isShow | bool | 是否显示 |

---

### GET /dashboard/base/:ioOption/:netOption
**功能**: Load dashboard base info (获取仪表盘基础信息)

**路径参数**:
| 参数 | 类型 | 必填 | 说明 | 取值示例 |
|------|------|------|------|----------|
| ioOption | string | 是 | IO选项，指定磁盘 | "sda", "sdb", "all" |
| netOption | string | 是 | 网络选项，指定网卡 | "eth0", "ens33", "all" |

**返回参数** (`DashboardBase`):
| 字段 | 类型 | 说明 |
|------|------|------|
| websiteNumber | int | 网站数量 |
| databaseNumber | int | 数据库数量 |
| cronjobNumber | int | 定时任务数量 |
| appInstalledNumber | int | 已安装应用数量 |
| hostname | string | 主机名 |
| os | string | 操作系统 |
| platform | string | 平台 |
| platformFamily | string | 平台家族 |
| platformVersion | string | 平台版本 |
| prettyDistro | string | 发行版名称 |
| kernelArch | string | 内核架构 |
| kernelVersion | string | 内核版本 |
| virtualizationSystem | string | 虚拟化系统 |
| ipV4Addr | string | IPv4地址 |
| systemProxy | string | 系统代理 |
| cpuCores | int | CPU物理核心数 |
| cpuLogicalCores | int | CPU逻辑核心数 |
| cpuModelName | string | CPU型号 |
| cpuMhz | float64 | CPU主频(MHz) |
| quickJumps | []QuickJump | 快速跳转列表 |
| currentInfo | DashboardCurrent | 当前监控信息 |

---

### GET /dashboard/current/node
**功能**: Load dashboard current info for node (获取节点当前信息)

**请求参数**: 无

**返回参数** (`NodeCurrent`):
| 字段 | 类型 | 说明 |
|------|------|------|
| load1 | float64 | 1分钟负载 |
| load5 | float64 | 5分钟负载 |
| load15 | float64 | 15分钟负载 |
| loadUsagePercent | float64 | 负载使用百分比 |
| cpuUsedPercent | float64 | CPU使用百分比 |
| cpuUsed | float64 | CPU已使用 |
| cpuTotal | int | CPU总核心数 |
| cpuDetailedPercent | []float64 | CPU详细使用率 |
| memoryTotal | uint64 | 内存总量(字节) |
| memoryAvailable | uint64 | 可用内存(字节) |
| memoryUsed | uint64 | 已用内存(字节) |
| memoryUsedPercent | float64 | 内存使用百分比 |
| swapMemoryTotal | uint64 | 交换空间总量 |
| swapMemoryAvailable | uint64 | 可用交换空间 |
| swapMemoryUsed | uint64 | 已用交换空间 |
| swapMemoryUsedPercent | float64 | 交换空间使用百分比 |

---

### GET /dashboard/current/:ioOption/:netOption
**功能**: Load dashboard current info (获取仪表盘当前监控信息)

**路径参数**:
| 参数 | 类型 | 必填 | 说明 | 取值示例 |
|------|------|------|------|----------|
| ioOption | string | 是 | IO选项 | "sda", "all" |
| netOption | string | 是 | 网络选项 | "eth0", "all" |

**返回参数** (`DashboardCurrent`):
| 字段 | 类型 | 说明 |
|------|------|------|
| uptime | uint64 | 运行时间(秒) |
| timeSinceUptime | string | 运行时间描述 |
| procs | uint64 | 进程数 |
| load1 | float64 | 1分钟负载 |
| load5 | float64 | 5分钟负载 |
| load15 | float64 | 15分钟负载 |
| loadUsagePercent | float64 | 负载使用百分比 |
| cpuPercent | []float64 | CPU使用率数组 |
| cpuUsedPercent | float64 | CPU使用百分比 |
| cpuUsed | float64 | CPU已使用 |
| cpuTotal | int | CPU总核心数 |
| cpuDetailedPercent | []float64 | CPU各核心使用率 |
| memoryTotal | uint64 | 内存总量 |
| memoryUsed | uint64 | 已用内存 |
| memoryFree | uint64 | 空闲内存 |
| memoryShard | uint64 | 共享内存 |
| memoryCache | uint64 | 缓存内存 |
| memoryAvailable | uint64 | 可用内存 |
| memoryUsedPercent | float64 | 内存使用百分比 |
| swapMemoryTotal | uint64 | 交换空间总量 |
| swapMemoryAvailable | uint64 | 可用交换空间 |
| swapMemoryUsed | uint64 | 已用交换空间 |
| swapMemoryUsedPercent | float64 | 交换空间使用百分比 |
| ioReadBytes | uint64 | IO读取字节数 |
| ioWriteBytes | uint64 | IO写入字节数 |
| ioCount | uint64 | IO操作次数 |
| ioReadTime | uint64 | IO读取时间 |
| ioWriteTime | uint64 | IO写入时间 |
| diskData | []DiskInfo | 磁盘信息列表 |
| netBytesSent | uint64 | 网络发送字节 |
| netBytesRecv | uint64 | 网络接收字节 |
| gpuData | []GPUInfo | GPU信息列表 |
| xpuData | []XPUInfo | XPU信息列表 |
| topCPUItems | []Process | CPU占用最高的进程 |
| topMemItems | []Process | 内存占用最高的进程 |
| shotTime | time.Time | 快照时间 |

**DiskInfo 详情**:
| 字段 | 类型 | 说明 |
|------|------|------|
| path | string | 挂载路径 |
| type | string | 文件系统类型 |
| device | string | 设备名 |
| total | uint64 | 总容量 |
| free | uint64 | 可用空间 |
| used | uint64 | 已用空间 |
| usedPercent | float64 | 使用百分比 |
| inodesTotal | uint64 | inode总数 |
| inodesUsed | uint64 | 已用inode |
| inodesFree | uint64 | 可用inode |
| inodesUsedPercent | float64 | inode使用百分比 |

**GPUInfo 详情**:
| 字段 | 类型 | 说明 |
|------|------|------|
| index | uint | GPU索引 |
| productName | string | 产品名称 |
| gpuUtil | string | GPU利用率 |
| temperature | string | 温度 |
| performanceState | string | 性能状态 |
| powerUsage | string | 电源使用 |
| powerDraw | string | 电源消耗 |
| maxPowerLimit | string | 最大功率限制 |
| memoryUsage | string | 内存使用率 |
| memUsed | string | 已用显存 |
| memTotal | string | 总显存 |
| fanSpeed | string | 风扇速度 |

**XPUInfo 详情**:
| 字段 | 类型 | 说明 |
|------|------|------|
| deviceID | int | 设备ID |
| deviceName | string | 设备名称 |
| memory | string | 内存信息 |
| temperature | string | 温度 |
| memoryUsed | string | 已用内存 |
| power | string | 功耗 |
| memoryUtil | string | 内存利用率 |

**Process 详情**:
| 字段 | 类型 | 说明 |
|------|------|------|
| pid | int | 进程ID |
| name | string | 进程名称 |
| cpu | float64 | CPU占用率 |
| mem | float64 | 内存占用率 |
| command | string | 命令 |

---

### GET /dashboard/current/top/cpu
**功能**: Load top cpu processes (获取CPU占用最高的进程列表)

**请求参数**: 无

**返回参数** (`Process[]`):
| 字段 | 类型 | 说明 |
|------|------|------|
| pid | int | 进程ID |
| name | string | 进程名称 |
| cpu | float64 | CPU占用百分比 |
| mem | float64 | 内存占用百分比 |
| command | string | 进程命令 |

---

### GET /dashboard/current/top/mem
**功能**: Load top memory processes (获取内存占用最高的进程列表)

**请求参数**: 无

**返回参数** (`Process[]`):
| 字段 | 类型 | 说明 |
|------|------|------|
| pid | int | 进程ID |
| name | string | 进程名称 |
| cpu | float64 | CPU占用百分比 |
| mem | float64 | 内存占用百分比 |
| command | string | 进程命令 |

---

### POST /dashboard/system/restart/:operation
**功能**: System restart (系统重启/关机)

**路径参数**:
| 参数 | 类型 | 必填 | 说明 | 取值示例 |
|------|------|------|------|----------|
| operation | string | 是 | 操作类型 | "reboot"(重启), "shutdown"(关机) |

**返回**: 操作成功返回 200

---

## 通用说明

### 认证方式
- 需要 `ApiKeyAuth` 和 `Timestamp` 认证头

### 响应格式
- 成功: `{"code": 200, "data": {...}}`
- 失败: `{"code": 500, "message": "error message"}`

### 压缩支持
- 部分接口(如 `/dashboard/app/launcher`)支持 Gzip 压缩返回
