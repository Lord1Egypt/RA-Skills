# Disk Management, Firewall, Host, Host tool, Monitor, SSH - 1Panel API

## 模块说明
Disk Management, Firewall, Host, Host tool, Monitor, SSH 模块接口

## 接口列表 (53 个)

---

### GET /hosts/components/{name}
**功能**: Check if a system component exists

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | ✅ | Component name to check | 例如: rsync, docker |

---

### GET /hosts/disks
**功能**: Get complete disk information

**响应参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| (全盘信息) | object | 包含所有磁盘的完整信息，包括已分区和未分区磁盘 |

---

### GET /hosts/monitor/setting
**功能**: Load monitor setting

**响应参数** (MonitorSetting):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| MonitorStatus | string | 监控状态 (enable/disable) |
| MonitorStoreDays | string | 数据保留天数 |
| MonitorInterval | string | 监控间隔 |
| DefaultNetwork | string | 默认网卡 |
| DefaultIO | string | 默认IO设备 |

---

### GET /hosts/tool/supervisor/process
**功能**: Get Supervisor process config

**响应参数** ([]SupervisorProcessConfig):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| name | string | 进程名称 |
| command | string | 启动命令 |
| user | string | 运行用户 |
| dir | string | 工作目录 |
| numprocs | string | 进程数量 |
| autoRestart | string | 自动重启 (true/false) |
| autoStart | string | 开机自启 (true/false) |
| environment | string | 环境变量 |
| status | array | 进程状态列表 |
| msg | string | 消息 |

---

### POST /hosts/disks/mount
**功能**: Mount disk

**请求参数** (DiskMountRequest):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| device | string | ✅ | 设备路径 | 例如: /dev/sdb1 |
| mountPoint | string | ✅ | 挂载点 | 例如: /mnt/data |
| filesystem | string | ✅ | 文件系统类型 | ext4, xfs |
| autoMount | bool | - | 是否开机自动挂载 | true/false |
| noFail | bool | - | 挂载失败时忽略 | true/false |

---

### POST /hosts/disks/partition
**功能**: Partition disk

**请求参数** (DiskPartitionRequest):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| device | string | ✅ | 设备路径 | 例如: /dev/sdb |
| filesystem | string | ✅ | 文件系统类型 | ext4, xfs |
| label | string | - | 卷标 | - |
| autoMount | bool | - | 是否开机自动挂载 | true/false |
| mountPoint | string | ✅ | 挂载点 | 例如: /mnt/data |

---

### POST /hosts/disks/unmount
**功能**: Unmount disk

**请求参数** (DiskUnmountRequest):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| mountPoint | string | ✅ | 挂载点 | 例如: /mnt/data |

---

### POST /hosts/firewall/base
**功能**: Load firewall base info

**请求参数** (OperationWithName):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | ✅ | 防火墙类型 | firewalld, ufw, iptables |

**响应参数** (FirewallBaseInfo):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| name | string | 防火墙名称 |
| isExist | bool | 是否存在 |
| isActive | bool | 是否激活 |
| isInit | bool | 是否初始化 |
| isBind | bool | 是否绑定 |
| version | string | 版本号 |
| pingStatus | string | Ping 状态 |

---

### POST /hosts/firewall/batch
**功能**: Batch operate rule

**请求参数** (BatchRuleOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✅ | 规则类型 | port, addr, forward |
| rules | array | - | 规则列表 | PortRuleOperate 数组 |

**规则参数** (PortRuleOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | ✅ | 操作类型 | add, remove |
| port | string | ✅ | 端口号 | - |
| protocol | string | ✅ | 协议 | tcp, udp, tcp/udp |
| strategy | string | ✅ | 策略 | accept, drop |
| address | string | - | IP 地址 | - |
| chain | string | - | 链 | - |
| description | string | - | 描述 | - |

---

### POST /hosts/firewall/filter/chain/status
**功能**: load chain status with name

**请求参数** (OperationWithName):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | ✅ | 链名称 | 1PANEL_INPUT, 1PANEL_OUTPUT, 1PANEL_BASIC |

**响应参数** (IptablesChainStatus):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| isBind | bool | 是否绑定 |
| defaultStrategy | string | 默认策略 |

---

### POST /hosts/firewall/filter/operate
**功能**: Apply/Unload/Init iptables filter

**请求参数** (IptablesOp):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | ✅ | 链名称 | 1PANEL_INPUT, 1PANEL_OUTPUT, 1PANEL_BASIC |
| operate | string | ✅ | 操作类型 | init-base, init-forward, init-advance, bind-base, unbind-base, bind, unbind |

---

### POST /hosts/firewall/filter/rule/batch
**功能**: Batch operate iptables filter rules

**请求参数** (IptablesBatchOperate):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| rules | array | - | 规则列表 (IptablesRuleOp 数组) |

**规则参数** (IptablesRuleOp):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | ✅ | 操作类型 | add, remove |
| chain | string | ✅ | 链名称 | 1PANEL_BASIC, 1PANEL_BASIC_BEFORE, 1PANEL_INPUT, 1PANEL_OUTPUT |
| protocol | string | - | 协议 | tcp, udp 等 |
| srcIP | string | - | 源 IP | - |
| srcPort | uint | - | 源端口 | - |
| dstIP | string | - | 目标 IP | - |
| dstPort | uint | - | 目标端口 | - |
| strategy | string | ✅ | 策略 | accept, drop, reject |
| description | string | - | 描述 | - |

---

### POST /hosts/firewall/filter/rule/operate
**功能**: Operate iptables filter rule

**请求参数** (IptablesRuleOp):
同 batch 参数

---

### POST /hosts/firewall/filter/search
**功能**: search iptables filter rules

**请求参数** (SearchPageWithType):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | ✅ | 页码 | - |
| pageSize | int | ✅ | 每页数量 | - |
| info | string | - | 搜索关键词 | - |
| type | string | - | 规则类型 | - |

---

### POST /hosts/firewall/forward
**功能**: Operate forward rule

**请求参数** (ForwardRuleOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| forceDelete | bool | - | 强制删除 | true/false |
| rules | array | - | 规则列表 | - |

**规则参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | ✅ | 操作类型 | add, remove |
| num | string | - | 规则编号 | - |
| protocol | string | ✅ | 协议 | tcp, udp, tcp/udp |
| interface | string | - | 网络接口 | - |
| port | string | ✅ | 源端口 | - |
| targetIP | string | - | 目标 IP | - |
| targetPort | string | ✅ | 目标端口 | - |

---

### POST /hosts/firewall/ip
**功能**: Operate Ip rule

**请求参数** (AddrRuleOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | - | 规则 ID | - |
| operation | string | ✅ | 操作类型 | add, remove |
| address | string | ✅ | IP 地址 | - |
| strategy | string | ✅ | 策略 | accept, drop |
| description | string | - | 描述 | - |

---

### POST /hosts/firewall/operate
**功能**: Operate firewall

**请求参数** (FirewallOperation):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | ✅ | 操作类型 | start, stop, restart, disableBanPing, enableBanPing |
| withDockerRestart | bool | - | 是否同时重启 Docker | true/false |

---

### POST /hosts/firewall/port
**功能**: Create group (端口规则操作)

**请求参数** (PortRuleOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | - | 规则 ID | - |
| operation | string | ✅ | 操作类型 | add, remove |
| chain | string | - | 链 | - |
| address | string | - | IP 地址 | - |
| port | string | ✅ | 端口号 | - |
| protocol | string | ✅ | 协议 | tcp, udp, tcp/udp |
| strategy | string | ✅ | 策略 | accept, drop |
| description | string | - | 描述 | - |

---

### POST /hosts/firewall/search
**功能**: Page firewall rules

**请求参数** (RuleSearch):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | ✅ | 页码 | - |
| pageSize | int | ✅ | 每页数量 | - |
| info | string | - | 搜索关键词 | - |
| status | string | - | 状态 | - |
| strategy | string | - | 策略 | accept, drop |
| type | string | ✅ | 规则类型 | port, addr, forward |

---

### POST /hosts/firewall/update/addr
**功能**: Update Ip rule

**请求参数** (AddrRuleUpdate):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oldRule | object | ✅ | 旧规则 (AddrRuleOperate) |
| newRule | object | ✅ | 新规则 (AddrRuleOperate) |

---

### POST /hosts/firewall/update/description
**功能**: Update rule description

**请求参数** (UpdateFirewallDescription):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | - | 规则类型 | - |
| chain | string | - | 链 | - |
| srcIP | string | - | 源 IP | - |
| dstIP | string | - | 目标 IP | - |
| srcPort | string | - | 源端口 | - |
| dstPort | string | - | 目标端口 | - |
| protocol | string | - | 协议 | - |
| strategy | string | ✅ | 策略 | accept, drop |
| description | string | - | 描述 | - |

---

### POST /hosts/firewall/update/port
**功能**: Update port rule

**请求参数** (PortRuleUpdate):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oldRule | object | ✅ | 旧规则 (PortRuleOperate) |
| newRule | object | ✅ | 新规则 (PortRuleOperate) |

---

### POST /hosts/monitor/clean
**功能**: Clean monitor data

**说明**: 清空所有监控数据，无需请求参数

---

### POST /hosts/monitor/gpu/search
**功能**: Load GPU monitor data

**请求参数** (MonitorGPUSearch):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productName | string | - | GPU 产品名称 |
| startTime | time | ✅ | 开始时间 |
| endTime | time | ✅ | 结束时间 |

**响应参数** (MonitorGPUData):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| date | array | 时间列表 |
| gpuValue | array | GPU 使用率 |
| temperatureValue | array | 温度 |
| powerTotal | array | 总功率 |
| powerUsed | array | 使用功率 |
| powerPercent | array | 功率百分比 |
| memoryTotal | array | 总显存 |
| memoryUsed | array | 已用显存 |
| memoryPercent | array | 显存百分比 |
| speedValue | array | 速度 |
| processCount | array | 进程数 |
| gpuProcesses | array | GPU 进程列表 |

---

### POST /hosts/monitor/search
**功能**: Load monitor data

**请求参数** (MonitorSearch):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| param | string | ✅ | 监控指标 | all, cpu, memory, load, io, network |
| io | string | - | IO 设备名 | - |
| network | string | - | 网卡名 | - |
| startTime | time | ✅ | 开始时间 | - |
| endTime | time | ✅ | 结束时间 | - |

**响应参数** ([]MonitorData):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| param | string | 监控指标 |
| date | array | 时间列表 |
| value | array | 监控值 |

---

### POST /hosts/monitor/setting/update
**功能**: Update monitor setting

**请求参数** (MonitorSettingUpdate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| key | string | ✅ | 设置项 | MonitorStatus, MonitorStoreDays, MonitorInterval, DefaultNetwork, DefaultIO |
| value | string | ✅ | 设置值 | - |

---

### GET /hosts/monitor/gpuoptions
**功能**: Get CPU/GPU options

**响应参数** (MonitorGPUOptions):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| gpuType | string | GPU 类型 |
| chartHide | array | 隐藏图表列表 |
| options | array | 可选 GPU 列表 |

---

### GET /hosts/monitor/netoptions
**功能**: Get network options

**响应参数** ([]string):
| 说明 |
|------|
| 网卡列表 (包含 "all" 选项) |

---

### GET /hosts/monitor/iooptions
**功能**: Get IO options

**响应参数** ([]string):
| 说明 |
|------|
| IO 设备列表 (包含 "all" 选项) |

---

### POST /hosts/ssh/cert
**功能**: Generate host SSH secret

**请求参数** (RootCertOperate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | - | 证书 ID | - |
| name | string | - | 证书名称 | - |
| mode | string | - | 模式 | - |
| encryptionMode | string | ✅ | 加密类型 | rsa, ed25519, ecdsa, dsa |
| passPhrase | string | - | 密码短语 (Base64 编码) | - |
| publicKey | string | - | 公钥 (Base64 编码) | - |
| privateKey | string | - | 私钥 (Base64 编码) | - |
| description | string | - | 描述 | - |

---

### POST /hosts/ssh/cert/delete
**功能**: Delete host SSH secret

**请求参数** (ForceDelete):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ids | array | ✅ | 证书 ID 列表 |
| forceDelete | bool | - | 强制删除 |

---

### POST /hosts/ssh/cert/search
**功能**: Load host SSH secret

**请求参数** (SearchWithPage):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | ✅ | 页码 |
| pageSize | int | ✅ | 每页数量 |
| info | string | - | 搜索关键词 |

**响应参数** (RootCert):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | uint | 证书 ID |
| createdAt | time | 创建时间 |
| name | string | 证书名称 |
| encryptionMode | string | 加密类型 |
| passPhrase | string | 密码短语 |
| publicKey | string | 公钥 |
| privateKey | string | 私钥 |
| description | string | 描述 |

---

### POST /hosts/ssh/cert/sync
**功能**: Sync host SSH secret

**说明**: 同步 SSH 密钥，无需请求参数

---

### POST /hosts/ssh/cert/update
**功能**: Update host SSH secret

**请求参数** (RootCertOperate):
同 cert 接口参数

---

### POST /hosts/ssh/file
**功能**: Load host SSH conf

**请求参数** (OperationWithName):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | ✅ | 文件名 | sshd_config |

**响应参数**: SSH 配置文件内容 (string)

---

### POST /hosts/ssh/file/update
**功能**: Update host SSH setting by file

**请求参数** (SettingUpdate):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| key | string | ✅ | 配置项 |
| value | string | - | 配置值 |

---

### POST /hosts/ssh/log
**功能**: Load host SSH logs

**请求参数** (SearchSSHLog):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | ✅ | 页码 | - |
| pageSize | int | ✅ | 每页数量 | - |
| info | string | - | 搜索关键词 | - |
| status | string | ✅ | 登录状态 | Success, Failed, All |

**响应参数** (SSHHistory):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| date | time | 登录时间 |
| dateStr | string | 时间字符串 |
| area | string | 地区 |
| user | string | 用户名 |
| authMode | string | 认证方式 |
| address | string | IP 地址 |
| port | string | 端口 |
| status | string | 状态 |
| message | string | 消息 |

---

### POST /hosts/ssh/log/export
**功能**: Export host SSH logs

**请求参数** (SearchSSHLog):
同 log 接口参数

**响应参数**: 导出文件路径 (string)

---

### POST /hosts/ssh/operate
**功能**: Operate SSH

**请求参数** (Operate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operation | string | ✅ | 操作类型 | start, stop, restart |

---

### POST /hosts/ssh/search
**功能**: Load host SSH setting info

**响应参数** (SSHInfo):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| autoStart | bool | 开机自启 |
| isExist | bool | 是否存在 |
| isActive | bool | 是否激活 |
| message | string | 消息 |
| port | string | 端口 |
| listenAddress | string | 监听地址 |
| passwordAuthentication | string | 密码认证 |
| pubkeyAuthentication | string | 公钥认证 |
| permitRootLogin | string | Root 登录 |
| useDNS | string | 使用 DNS |
| currentUser | string | 当前用户 |

---

### POST /hosts/ssh/update
**功能**: Update host SSH setting

**请求参数** (SSHUpdate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| key | string | ✅ | 配置项 | Port, ListenAddress, PasswordAuthentication, PubkeyAuthentication, PermitRootLogin, UseDNS 等 |
| oldValue | string | - | 旧值 | - |
| newValue | string | - | 新值 | - |

---

### POST /hosts/tool
**功能**: Get tool status

**请求参数** (HostToolReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✅ | 工具类型 | supervisord |
| operate | string | - | 操作类型 | status, restart, start, stop |

**响应参数** (HostToolRes):
| 参数名 | 类型 | 说明 |
|--------|------|------|
| type | string | 工具类型 |
| config | object | 工具配置 (Supervisor) |

**Supervisor 配置**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| configPath | string | 配置路径 |
| includeDir | string | 包含目录 |
| logPath | string | 日志路径 |
| isExist | bool | 是否存在 |
| init | bool | 是否初始化 |
| msg | string | 消息 |
| version | string | 版本 |
| status | string | 状态 |
| ctlExist | bool | 控制命令是否存在 |
| serviceName | string | 服务名称 |

---

### POST /hosts/tool/config
**功能**: Get tool config

**请求参数** (HostToolConfig):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✅ | 工具类型 | supervisord |
| operate | string | - | 操作类型 | get, set |
| content | string | - | 配置内容 | - |

**响应参数**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| content | string | 配置文件内容 |

---

### POST /hosts/tool/init
**功能**: Create Host tool Config

**请求参数** (HostToolCreate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✅ | 工具类型 | supervisord |
| configPath | string | - | Supervisor 配置文件路径 | - |
| serviceName | string | - | Supervisor 服务名称 | - |

---

### POST /hosts/tool/operate
**功能**: Operate tool

**请求参数** (HostToolReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | ✅ | 工具类型 | supervisord |
| operate | string | - | 操作类型 | status, restart, start, stop |

---

### POST /hosts/tool/supervisor/process
**功能**: Create Supervisor process

**请求参数** (SupervisorProcessConfig):
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | - | 进程名称 |
| operate | string | - | 操作类型 |
| command | string | - | 启动命令 |
| user | string | - | 运行用户 |
| dir | string | - | 工作目录 |
| numprocs | string | - | 进程数量 |
| autoRestart | string | - | 自动重启 (true/false) |
| autoStart | string | - | 开机自启 (true/false) |
| environment | string | - | 环境变量 |

---

### POST /hosts/tool/supervisor/process/file
**功能**: Get Supervisor process config file

**请求参数** (SupervisorProcessFileReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | ✅ | 进程名称 | - |
| operate | string | ✅ | 操作类型 | get, clear, update |
| content | string | - | 文件内容 | - |
| file | string | ✅ | 文件类型 | out.log, err.log, config |

**响应参数**: 配置文件内容 (string)

---

### GET /hosts/terminal
**功能**: WebSocket SSH 终端

**说明**: 通过 WebSocket 协议建立 SSH 连接

