---
name: alicloud-database-rds-custom
description: 查询阿里云自定义实例（RC 实例）。使用 aliyun CLI 调用 DescribeRCInstances API 查询 RDS 相关自定义实例。当用户需要查询 RC 实例、RDS 自定义实例或云资源时触发此技能。
license: MIT
---

# 查询自定义实例（RC Instances）

## 概述

本技能提供阿里云 RC（RDS Custom）实例全生命周期查询能力，通过 aliyun CLI 调用 RDS API 获取实例及相关资源信息。适用于查询 RC 实例、监控指标、资源配置等场景。

## 核心能力

### 支持的查询命令

| 命令 | 功能 | 状态 |
|------|------|------|
| `DescribeRCInstances` | 查询 RC 实例列表 | ✅ |
| `DescribeRCInstanceAttribute` | 查询单个实例详细信息 | ✅ |
| `DescribeRCImageList` | 查询可用镜像列表 | ✅ |
| `DescribeRCDisks` | 查询磁盘列表 | ✅ |
| `DescribeRCSnapshots` | 查询快照列表 | ✅ |
| `DescribeRCMetricList` | 查询监控指标（CPU、内存等） | ✅ |
| `DescribeRCClusterConfig` | 查询 ACK 集群 KubeConfig | ✅ |
| `DescribeRCNodePool` | 查询边缘节点池配置 | ✅ |
| `DescribeRCInstanceVncUrl` | 查询 VNC 登录地址 | ✅ |

### 暂不支持的命令

以下命令在 Java SDK 中存在，但在 aliyun CLI v3.2.13 中暂不支持：

| 命令 | 功能 | 替代方案 |
|------|------|----------|
| `DescribeRCCloudAssistantStatus` | 查询云助手状态 | SSH 登录实例检查 |
| `DescribeRCNetworkInterfaces` | 查询网络接口信息 | 使用 DescribeRCInstanceAttribute |
| `DescribeRCInstanceHistoryEvents` | 查询历史事件 | 使用控制台查看 |

### 特性

- **多地域支持**：支持指定地域查询，默认 `cn-beijing`
- **格式化输出**：支持 JSON、表格等多种输出格式
- **jq 过滤**：提供丰富的 jq 数据提取示例
- **监控查询**：支持 CPU、内存、磁盘等监控指标查询

## 使用方式

### 基本查询

```bash
aliyun rds DescribeRCInstances --region cn-beijing
```

### 指定地域

```bash
aliyun rds DescribeRCInstances --region cn-hangzhou
```

### 格式化输出（表格）

```bash
aliyun rds DescribeRCInstances --region cn-beijing --output cols=InstanceId,InstanceName,Status,RegionId,Cpu,Memory
```

### 查询特定实例

```bash
aliyun rds DescribeRCInstances --region cn-beijing --InstanceId rc-xxx
```

### 使用 jq 过滤

```bash
# 只查询运行中的实例
aliyun rds DescribeRCInstances --region cn-beijing | jq '.RCInstances[] | select(.Status == "Running")'

# 提取关键字段
aliyun rds DescribeRCInstances --region cn-beijing | jq '.RCInstances[] | {InstanceId, InstanceName, Status, Cpu, Memory}'
```

## 脚本使用

### 查询 RC 实例脚本

```bash
cd /path/to/skill/scripts
./query_rc_instances.sh [地域]
```

### 示例输出

```bash
$ ./query_rc_instances.sh cn-beijing

=== RC 实例列表 (cn-beijing) ===

实例 ID: rc-xxxxxxxxxxxxx
实例名称：rc-xxxxxxxxxxxxx
集群名称：RCC-xxxxxxxxxxxxxxx
状态：Running
CPU: 4 核
内存：32 GB
地域：cn-beijing
可用区：cn-beijing-x
私网 IP: 10.x.x.xxx
VPC: vpc-xxxxxxxxxxxxxxxxx
创建时间：2026-01-20 18:45:50
到期时间：2026-04-20T16:00:00Z

总计：1 台实例
```

## 前置条件

### 1. 安装 aliyun CLI

```bash
# 一键安装
/bin/bash -c "$(curl -fsSL https://aliyuncli.alicdn.com/install.sh)"
```

### 2. 配置凭证

```bash
aliyun configure
```

需要输入：
- AccessKey ID
- AccessKey Secret
- 默认地域（如：cn-beijing）
- 输出格式（json）
- 语言（zh）

### 3. 验证配置

```bash
aliyun version
aliyun rds DescribeRCInstances --region cn-beijing
```

## 常用命令参考

| 命令 | 说明 |
|------|------|
| `aliyun rds DescribeRCInstances` | 查询 RC 实例列表 |
| `aliyun rds DescribeRCInstanceAttribute` | 查询单个 RC 实例详细信息 |
| `aliyun rds DescribeRCImageList` | 查询 RC 实例可用镜像列表 |
| `aliyun rds DescribeRCNetworkInterfaces` | 查询 RC 实例网络接口信息 |
| `aliyun rds DescribeRCDeploymentSets` | 查询 RC 实例部署集列表 |
| `aliyun rds DescribeRCDisks` | 查询 RC 实例磁盘列表 |
| `aliyun rds DescribeRCSnapshots` | 查询 RC 实例快照列表 |
| `aliyun rds DescribeRCInstanceHistoryEvents` | 查询 RC 实例历史事件 |
| `aliyun rds DescribeRCCloudAssistantStatus` | 查询 RC 实例云助手状态 |
| `aliyun rds DescribeRCMetricList` | 查询 RC 实例监控指标（CPU、内存等） |

## 查询实例详细信息

### 基本查询

```bash
aliyun rds DescribeRCInstanceAttribute \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID>
```

### 指定实例名称

```bash
aliyun rds DescribeRCInstanceAttribute \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  --InstanceName rc-<INSTANCE_ID>
```

### 格式化输出

```bash
aliyun rds DescribeRCInstanceAttribute \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  --output cols=InstanceId,InstanceName,Status,Cpu,Memory,RegionId,ZoneId
```

### 使用 jq 提取字段

```bash
# 提取基本信息
aliyun rds DescribeRCInstanceAttribute \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.RCInstances[0] | {InstanceId, InstanceName, Status, Cpu, Memory}'

# 提取网络信息
aliyun rds DescribeRCInstanceAttribute \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.RCInstances[0].VpcAttributes | {VpcId, VSwitchId, PrivateIpAddress}'
```

## 查询可用镜像列表

### 基本查询

```bash
aliyun rds DescribeRCImageList \
  --region cn-beijing
```

### 指定实例类型查询

```bash
aliyun rds DescribeRCImageList \
  --region cn-beijing \
  --InstanceType mysql.x2.xlarge.6cm
```

### 格式化输出

```bash
aliyun rds DescribeRCImageList \
  --region cn-beijing \
  --output cols=ImageId,ImageName,OSType,OSName
```

### 使用 jq 过滤

```bash
# 提取镜像基本信息
aliyun rds DescribeRCImageList \
  --region cn-beijing \
  | jq '.Images[] | {ImageId, ImageName, OSType}'

# 查询 Alibaba Cloud Linux 镜像
aliyun rds DescribeRCImageList \
  --region cn-beijing \
  | jq '.Images[] | select(.OSName | contains("Alibaba Cloud Linux"))'

# 统计镜像数量
aliyun rds DescribeRCImageList \
  --region cn-beijing \
  | jq '.Images | length'
```

### 输出字段说明

| 字段 | 说明 |
|------|------|
| ImageId | 镜像 ID |
| ImageName | 镜像名称 |
| OSType | 操作系统类型（linux/windows） |
| OSName | 操作系统名称 |
| ImageVersion | 镜像版本 |

## 查询磁盘列表

### 基本查询

```bash
aliyun rds DescribeRCDisks \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID>
```

### 按地域查询

```bash
aliyun rds DescribeRCDisks \
  --region cn-beijing
```

### 格式化输出

```bash
aliyun rds DescribeRCDisks \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  --output cols=DiskId,DiskName,Size,Category,Status
```

### 使用 jq 提取字段

```bash
# 提取磁盘基本信息
aliyun rds DescribeRCDisks \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.Disks[] | {DiskId, DiskName, Size, Category}'

# 查询系统盘和数据盘
aliyun rds DescribeRCDisks \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.Disks[] | select(.Type == "system")'

# 统计磁盘总容量
aliyun rds DescribeRCDisks \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '[.Disks[].Size | tonumber] | add'

# 统计磁盘数量
aliyun rds DescribeRCDisks \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.Disks | length'
```

### 输出字段说明

| 字段 | 说明 |
|------|------|
| DiskId | 磁盘 ID |
| DiskName | 磁盘名称 |
| Size | 磁盘容量（GB） |
| Category | 磁盘种类（cloud_essd/cloud_ssd 等） |
| Status | 磁盘状态（In_Use/Available） |
| Type | 磁盘类型（system/data） |
| Device | 设备名（/dev/vda 等） |
| Encrypted | 是否加密 |

## 查询快照列表

### 基本查询

```bash
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID>
```

### 按地域查询

```bash
aliyun rds DescribeRCSnapshots \
  --region cn-beijing
```

### 指定磁盘 ID 查询

```bash
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --DiskId d-c5kyo15381wht249k498
```

### 格式化输出

```bash
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  --output cols=SnapshotId,SnapshotName,Size,Status,CreationTime
```

### 使用 jq 提取字段

```bash
# 提取快照基本信息
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.Snapshots[] | {SnapshotId, SnapshotName, Size, Status}'

# 查询成功状态的快照
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.Snapshots[] | select(.Status == "success")'

# 统计快照总数量
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '.Snapshots | length'

# 统计快照总容量
aliyun rds DescribeRCSnapshots \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  | jq '[.Snapshots[].Size | tonumber] | add'
```

### 输出字段说明

| 字段 | 说明 |
|------|------|
| SnapshotId | 快照 ID |
| SnapshotName | 快照名称 |
| Size | 快照容量（GB） |
| Status | 快照状态（success/failed/progressing） |
| CreationTime | 创建时间 |
| SourceDiskId | 源磁盘 ID |
| SourceInstanceId | 源实例 ID |
| Progress | 快照进度（百分比） |
| RetentionDays | 保留天数 |

## 监控指标查询

### 查询 CPU 使用率

```bash
aliyun rds DescribeRCMetricList \
  --region cn-beijing \
  --InstanceId rc-xxx \
  --MetricName CPUUtilization \
  --StartTime "2026-03-12 10:05:00" \
  --EndTime "2026-03-12 10:15:00" \
  --Period 60 \
  --Length 1000
```

### 查询内存使用率

```bash
aliyun rds DescribeRCMetricList \
  --region cn-beijing \
  --InstanceId rc-xxx \
  --MetricName MemoryUtilization \
  --StartTime "2026-03-12 10:05:00" \
  --EndTime "2026-03-12 10:15:00" \
  --Period 60
```

### 常用指标名称

| 指标名 | 说明 |
|--------|------|
| CPUUtilization | CPU 使用率 (%) |
| MemoryUtilization | 内存使用率 (%) |
| DiskUtilization | 磁盘使用率 (%) |
| IOPS | 每秒 IO 操作数 |
| ConnectionUsage | 连接数使用率 |

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| InstanceId | 是 | RC 实例 ID |
| MetricName | 是 | 指标名称 |
| StartTime | 是 | 开始时间，格式 `YYYY-MM-DD HH:mm:ss` |
| EndTime | 是 | 结束时间，格式 `YYYY-MM-DD HH:mm:ss` |
| Period | 否 | 采集周期（秒），默认 60 |
| Length | 否 | 返回数据点数，默认 1000 |

### 示例：查询最近 1 小时 CPU

```bash
# 计算 1 小时前的时间
START=$(date -d "1 hour ago" "+%Y-%m-%d %H:%M:%S")
END=$(date "+%Y-%m-%d %H:%M:%S")

aliyun rds DescribeRCMetricList \
  --region cn-beijing \
  --InstanceId rc-<INSTANCE_ID> \
  --MetricName CPUUtilization \
  --StartTime "$START" \
  --EndTime "$END" \
  --Period 300
```

### 使用 jq 提取数据

```bash
# 提取 CPU 使用率数据点
aliyun rds DescribeRCMetricList \
  --region cn-beijing \
  --InstanceId rc-xxx \
  --MetricName CPUUtilization \
  --StartTime "2026-03-12 10:05:00" \
  --EndTime "2026-03-12 10:15:00" \
  | jq '.Data[] | {Timestamp, Value}'

# 计算平均 CPU 使用率
aliyun rds DescribeRCMetricList \
  --region cn-beijing \
  --InstanceId rc-xxx \
  --MetricName CPUUtilization \
  --StartTime "2026-03-12 10:05:00" \
  --EndTime "2026-03-12 10:15:00" \
  | jq '[.Data[].Value | tonumber] | add / length'
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| InstanceId | 实例 ID |
| InstanceName | 实例名称 |
| ClusterName | 集群名称 |
| Status | 运行状态（Running/Stopped 等） |
| Cpu | CPU 核数 |
| Memory | 内存大小（MB） |
| RegionId | 地域 ID |
| ZoneId | 可用区 ID |
| VpcId | VPC ID |
| PrivateIpAddress | 私网 IP |
| InstanceChargeType | 计费类型（PrePaid/PostPaid） |
| ExpiredTime | 到期时间 |
| GmtCreated | 创建时间 |

## 常见问题

### 1. 权限错误
```
ERROR: InvalidAccessKeyId.NotFound
```
**解决：** 检查 `aliyun configure` 配置的 AccessKey 是否正确

### 2. 地域错误
```
ERROR: InvalidRegionId.NotFound
```
**解决：** 使用有效的地域 ID，如 `cn-beijing`、`cn-hangzhou`、`cn-shanghai`

### 3. CLI 未安装
```
bash: aliyun: command not found
```
**解决：** 参考前置条件安装 aliyun CLI

### 4. 返回空列表
```json
{"RCInstances": [], "TotalCount": 0}
```
**解决：** 
- 检查地域是否正确
- 确认当前账号下是否有 RC 实例
- 尝试其他地域查询

## 参考资料

- [阿里云 CLI 文档](https://help.aliyun.com/product/29987.html)
- [RDS API 文档](https://help.aliyun.com/document_detail/26223.html)
- [OpenAPI 门户](https://api.aliyun.com/api?product=Rds&api=DescribeRCInstances)
