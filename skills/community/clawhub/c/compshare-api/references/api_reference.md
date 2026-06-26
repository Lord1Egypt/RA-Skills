# CompShare API 参考文档

## 目录
1. [概述](#概述)
2. [认证方式](#认证方式)
3. [Python SDK 快速开始](#python-sdk-快速开始)
4. [API接口文档](#api-接口文档)
5. [SSH客户端使用指南](#ssh客户端使用指南)
6. [错误码说明](#错误码说明)
7. [最佳实践](#最佳实践)

---

## 概述

CompShare是优云智算平台提供的GPU云服务器服务。本文档详细说明了所有API接口的参数、响应格式和使用方法。

**API基础地址**: `https://api.compshare.cn/`

**支持的GPU类型**: P40、2080、3090、3080Ti、4090、A800、A100、H20

---

## 认证方式

### 获取API密钥
1. 登录CompShare控制台: https://console.compshare.cn/
2. 进入「API管理」页面: https://console.compshare.cn/uaccount/api_manage
3. 创建或查看 `public_key` 和 `private_key`

### 密钥使用
在使用SDK或直接调用API时，需要在请求中携带这两个密钥：
- `public_key`: 公钥，用于标识用户身份
- `private_key`: 私钥，用于签名验证

### 配置文件
在 `assets/config.yaml` 中配置凭证：
```yaml
compshare:
  public_key: "your-public-key"
  private_key: "your-private-key"
  region: "cn-wlcb"
  zone: "cn-wlcb-01"
  base_url: "https://api.compshare.cn"
```

---

## Python SDK 快速开始

### 环境准备

官方提供了 Python3 版本的 SDK 示例，可通过以下步骤快速运行：

1. **安装 SDK**

```bash

pip install --upgrade ucloud-sdk-python3
```

1. **配置示例代码**

    - 编辑示例代码文件 `main.py`

    - 填写您的 `public_key` 和 `private_key` 密钥信息

    - 根据您的需求调整其他参数，例如镜像 ID `CompShareImageId` 等，

2. **运行示例**

```bash

python main.py
```

3. **镜像ID注意事项**

- 使用浏览器访问 https://www.compshare.cn/image-community 获取镜像列表信息
- 使用tag参数进行分类筛选，例如：https://www.compshare.cn/image-community?tag=ComfyUI
- 进入镜像详情（示例）：https://www.compshare.cn/images/500WHhII1fnz
- 500WHhII1fnz则为镜像ID，根据用户提到需求安装上述步骤创建镜像实例

---

## API 接口文档

所有 API 均通过 HTTPS 调用，请求地址统一为：`https://api.compshare.cn/`

---

### 创建 GPU 资源 - CreateCompShareInstance

**接口说明**：创建优云智算平台 GPU 实例资源

#### 请求参数

| 参数名称 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| Region | string | 可用地域，枚举值：cn-wlcb（华北二A）、cn-sh2（上海二） | 是 |
| Zone | string | 可用区，枚举值：cn-wlcb-01（华北二A）、cn-sh2-02（上海二） | 是 |
| ProjectId | string | 项目ID，不填写则为默认项目 | 否 |
| Disks.N.IsBoot | bool | 是否为系统盘，枚举值：<br>True：是系统盘<br>False：是数据盘（默认）<br>Disks数组中有且仅有一块系统盘 | 是 |
| Disks.N.Type | string | 磁盘类型，优云智算磁盘固定为 CLOUD_SSD | 是 |
| Disks.N.Size | int | 磁盘大小，单位GB，具体参考磁盘类型限制 | 是 |
| MachineType | string | 云主机机型，默认GPU为["G"]；本字段与UHostType二选一即可，参考云主机机型说明 | 是 |
| GPU | int | GPU卡核心数，仅GPU机型支持，可选范围与MachineType+GpuType相关 | 是 |
| Memory | int | 内存大小，单位MB；范围[1024, 262144]，需为1024的倍数；默认值8192 | 是 |
| CPU | int | 虚拟CPU核数，可选1-64，具体参照机型控制台；默认值4 | 是 |
| GpuType | string | GPU类型，枚举值：["P40","2080","3090","3080Ti","4090","A800","A100","H20"]；MachineType为G时必填 | 是 |
| CompShareImageId | string | 镜像ID | 是 |
| LoginMode | string | 主机登录模式，默认值：Password（密码） | 否 |
| ChargeType | string | 计费模式，枚举值：<br>Month：按月付费<br>Day：按天付费<br>Dynamic：按小时预付费<br>Postpay：按小时后付费（部分可用区支持，关机不收费）<br>Spot：抢占式实例（内测）<br>默认为月付 | 否 |
| Quantity | int | 购买时长，默认值1；按小时（Dynamic/Postpay）无需此参数；月付传0代表购买至月末 | 否 |
| MinimalCpuPlatform | string | 最低CPU平台，枚举值：["Intel/Auto", "Intel/IvyBridge", "Intel/Haswell", "Intel/Broadwell", "Intel/Skylake", "Intel/Cascadelake", "Intel/CascadelakeR", "Intel/IceLake", "Amd/Epyc2", "Amd/Auto","Ampere/Auto","Ampere/Altra"]；默认Intel/Auto | 否 |
| Password | string | 云主机密码，需按规范设置并进行base64编码 | 否 |
| Name | string | 实例名称 | 否 |
| SecurityGroupId | string | 防火墙ID | 否 |
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|Yes|
|Action|string|操作名称|Yes|
|UHostIds|array|UHost 实例 Id 集合|Yes|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=CreateCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=lnUhAYpT
&ImageId=KSuPKTtW
&LoginMode=dnnfRljU
&Disks.N.IsBoot=true
&Disks.N.Type=ptHJPOco
&Disks.N.Size=5
&MachineType=iyENElDv
&GPUType=pzRkInee
&GPU=VkyjzhQy
&ChargeType=USDhlfAP
&Quantity=7
&MinimalCpuPlatform=QErLvHVg
&Memory=1
&MaxCount=6
&Password=UwOdhzOu
&CPU=1
&Name=ACsfjhFW
&SecurityGroupId=DhXQhVSq
```

#### 响应示例

```json

{
"Action": "CreateCompShareInstanceResponse",
"IPs": [
"hhySlhCv"
],
"RetCode": 0,
"UHostIds": [
"NIdfqvRv"
]
}
```

---

### 获取实例资源列表 - DescribeCompShareInstance

**接口说明**：获取用户所有地域下实例资源信息列表

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|No|
|Zone|string|可用区。cn-wlcb-01|No|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostIds.N|string|【数组】UHost 主机的资源 ID，例如 UHostIds.0 代表希望获取信息 的主机 1，UHostIds.1 代表主机 2。 如果不传入，则返回当前 Region 所有符合条件的 UHost 实例。|No|
|Offset|int|列表起始位置偏移量，默认为 0|No|
|Limit|int|返回数据长度，默认为 20，最大 100|No|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|TotalCount|int|UHostInstance 总数|**Yes**|
|UHostSet|array|云主机实例列表，每项参数可见下面 CompShareInstanceSet|**Yes**|
##### CompShareInstanceSet 实例详情

| 参数名称 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| Zone | string | 可用区 | 否 |
| UHostId | string | 实例Id | 否 |
| MachineType | string | 机型信息 | 否 |
| CpuPlatform | string | CPU平台，如 "Intel/Auto"、"Amd/Auto" 等 | 否 |
| CompShareImageId | string | 镜像Id | 否 |
| CompShareImageName | string | 镜像名称 | 否 |
| CompShareImageOwnerAlias | string | 镜像来源 | 否 |
| CompShareImageBillId | string | 用于镜像计费的Id | 否 |
| CompShareImageStatus | string | 镜像状态 | 否 |
| CompShareImageType | string | 镜像类型：System 系统镜像、App 应用镜像、Custom 自制镜像、Community 社区镜像 | 否 |
| InstanceType | string | 实例类型："UHost" 普通主机；"Container" 容器主机 | 否 |
| Password | string | 主机密码，Base64 编码 | 否 |
| SshLoginCommand | string | SSH 登录命令 | 否 |
| Name | string | 实例名称 | 否 |
| Tag | string | 实例业务组 | 否 |
| Remark | string | 实例备注 | 否 |
| State | string | 实例状态：Initializing 初始化、Starting 启动中、Running 运行中、Stopping 关机中、Stopped 关机、Install Fail 安装失败、Rebooting 重启中、Resizing 升级改配中、空字符串 未知 | 否 |
| ChargeType | string | 计费模式：Year 按年、Month 按月、Dynamic 按时、Postpay 按需 | 否 |
| CPU | int | 虚拟CPU核数，单位：个 | 否 |
| Memory | string | 内存大小，单位：MB | 否 |
| GpuType | string | GPU类型，如 "4090" | 否 |
| GPU | int | GPU个数 | 否 |
| GraphicsMemory | object | GPU显存信息 | 否 |
| AutoRenew | string | 是否自动续费：Yes 是，No 否 | 否 |
| IsExpire | string | 是否过期：Yes 已过期，No 未过期 | 否 |
| OsName | string | 虚机镜像名称 | 否 |
| OsType | string | 操作系统类型：Linux / Windows | 否 |
| TotalDiskSpace | int | 总数据盘存储空间 | 否 |
| CpuArch | string | CPU架构：x86_64 / i386 等 | 否 |
| DiskSet | array | 磁盘信息，详见 UHostDiskSet | 否 |
| IPSet | array | 网络信息，详见 UHostIPSet | 否 |
| Softwares | array | 软件地址 | 否 |
| InstancePrice | float | 主机价格 | 否 |
| CompShareImagePrice | float | 镜像价格 | 否 |
| ExpireTime | string | 过期时间 | 否 |
| CreateTime | string | 创建时间 | 否 |
| SetId | int | 【内部API返回】宿主所在Set Id | 否 |
| HostIp | string | 【内部API返回】宿主IP | 否 |
| PodId | string | 【内部API返回】udisk podId | 否 |
| HugepageCfg | string | 【内部API返回】大页内存 | 否 |
| QemuVersion | string | 【内部API返回】Qemu版本号 | 否 |
| QemuFullVersion | string | 【内部API返回】Qemu完整版本号 | 否 |
| UUID | string | 【内部API返回】资源长Id | 否 |
| PostPayShutdown | bool | 【内部API返回】后付费关机 | 否 |
| SupportWithoutGpuStart | bool | 此实例是否支持无卡开机 | 否 |
| WithoutGpuSpec | object | 无卡配置规格，详见 WithoutGpuSpecInfo | 否 |
##### GraphicsMemory 显存信息

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Value|int|值，单位是 GB|No|
|Rate|int|交互展示参数，可忽略|No|
##### UHostDiskSet 磁盘信息

|Parameter name|Type|Description|Required|
|---|---|---|---|
|DiskType|string|磁盘类型。请参考磁盘类型|**Yes**|
|IsBoot|string|是否是系统盘。枚举值：True，是系统盘；False，是数据盘（默认）。Disks 数组中有且只能有一块盘是系统盘。|**Yes**|
|Encrypted|string|"true": 加密盘 "false"：非加密盘|No|
|Type|string|【建议不再使用】磁盘类型。系统盘: Boot，数据盘: Data, 网络盘：Udisk|No|
|DiskId|string|磁盘 ID|No|
|Name|string|UDisk 名字（仅当磁盘是 UDisk 时返回）|No|
|Drive|string|磁盘盘符|No|
|Size|int|磁盘大小，单位: GB|No|
|BackupType|string|备份方案。若开通了数据方舟，则为 DATAARK|No|
##### UHostIPSet IP 信息

|Parameter name|Type|Description|Required|
|---|---|---|---|
|IPMode|string|IPv4/IPv6；|**Yes**|
|Default|string|内网 Private 类型下，表示是否为默认网卡。true: 是默认网卡；其他值：不是。|No|
|Mac|string|内网 Private 类型下，当前网卡的 Mac。|No|
|Weight|int|当前 EIP 的权重。权重最大的为当前的出口 IP。|No|
|Type|string|国际: Internation，BGP: Bgp，内网: Private|No|
|IPId|string|外网 IP 资源 ID 。(内网 IP 无对应的资源 ID)|No|
|IP|string|IP 地址|No|
|Bandwidth|int|IP 对应的带宽，单位: Mb (内网 IP 不显示带宽信息)|No|
|VPCId|string|IP 地址对应的 VPC ID。（北京一不支持，字段返回为空）|No|
|SubnetId|string|IP 地址对应的子网 ID。（北京一不支持，字段返回为空）|No|
|NetworkInterfaceId|string|弹性网卡为默认网卡时，返回对应的 ID 值|No|
##### WithoutGpuSpec 无卡配置

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Cpu|int|cpu|No|
|Memory|int|内存|No|
|Gpu|int|gpu|No|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=DescribeCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=IoMVpdoj
&UHostIds.N=cnHQCXgZ
&Tag=iDnowauu
&Offset=2
&Limit=9
&VPCId=YVTTNJzc
&SubnetId=xsDQoSws
&NoEIP=false
&ResourceType=zFIXncgL
&UDiskIdForAttachment=true
&WithoutGpu=false
```

#### 响应示例

```json

{
"Action": "DescribeCompShareInstanceResponse",
"TotalCount": 8,
"UHostSet": [
{
"RestrictMode": "VTendLlO",
"Zone": "xdLgDoph",
"OsName": "gMqlgBlI",
"HostType": "jpATaXsk",
"SecGroupInstance": false,
"State": "TnNuGSYE",
"Memory": 6,
"HotPlugMaxCpu": 8,
"NetCapability": "kTFrfCiG",
"BootDiskState": "wfcQeKzE",
"CPU": 5,
"BasicImageName": "fFSjyQry",
"SpotAttribute": {},
"IPv6Feature": false,
"IPSet": [
{
"VPCId": "ASpSKtze",
"Weight": 8,
"Default": "tgnSjelJ",
"IP": "ZmBtTbhB",
"NetworkInterfaceId": "FauzdzHm",
"IPMode": "UulHwAYv",
"Bandwidth": 8,
"SubnetId": "SYfTyiiN",
"Mac": "ACuDMaqD",
"IPId": "subuipxK",
"Type": "XtwAFLux"
}
],
"HpcFeature": true,
"ImageId": "rOLrvehW",
"AutoRenew": "KHTdKhxO",
"UDHostAttribute": {},
"TotalDiskSpace": 6,
"OsType": "uTGzcPdd",
"SubnetType": "sDBMGbYE",
"CloudInitFeature": false,
"Remark": "zATjHVlb",
"Name": "pkIdkUfV",
"EpcInstance": true,
"IsolationGroup": "dMNyStGT",
"KeyPair": {},
"UHostId": "wMwHWPOr",
"GPU": 1,
"LifeCycle": "SwXCLmkq",
"CpuPlatform": "aKtmIaxl",
"MachineType": "IqVoJXvL",
"HiddenKvm": false,
"StorageType": "FEFUzaYx",
"HotplugFeature": false,
"UHostType": "NwCllZUf",
"BasicImageId": "AFGqwjpj",
"ExpireTime": 4,
"Tag": "MHPHAgpt",
"GpuType": "syCegFMi",
"NetworkState": "FcaxZMik",
"ChargeType": "xePQZDOs",
"RdmaClusterId": "ncMkxiOT",
"CreateTime": 7,
"TimemachineFeature": "GiqxwKD"
}
],
"RetCode": 0
}
```

---

### 获取自制镜像列表 - DescribeCustomImages

**接口说明**：获取用户的自制镜像列表信息

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 参见 地域和可用区列表|**Yes**|
|Zone|string|可用区。参见 可用区列表|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|CompShareImageId|string|指定镜像 Id 查询|No|
|Offset|int|列表起始位置偏移量，默认为 0|No|
|Limit|int|返回数据长度，默认为 20，最大 100|No|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|ImageSet|array|镜像详情信息|**Yes**|
|TotalCount|int|总数量|No|
##### CompShareImage 镜像详情

|Parameter name|Type|Description|Required|
|---|---|---|---|
|CompShareImageId|string|镜像 Id|No|
|Name|string|镜像名称|No|
|Author|string|镜像作者昵称|No|
|AuthInfo|int|镜像作者认证信息|No|
|ImageOwnerAlias|string|镜像来源。- Official 平台镜像；- Community 社区镜像|No|
|ImageType|string|镜像类型。- System 平台提供的公共镜像；- App 平台提供的应用镜像；- Custom 自制镜像；- Community 社区镜像|No|
|IsOfficial|bool|来源是否为官方镜像【仅自制镜像信息返回该字段】|No|
|Container|string|是否为容器镜像。- True 容器镜像 - False 虚机镜像|No|
|Status|string|镜像状态。- Making 制作中；- Available 可用；- UnAvailable 不可用；- Reviewing 审核中；- Offline 已下线|No|
|Size|int|镜像大小。单位 MB|No|
|Visibility|int|可见性。0：私密镜像；1：公开至镜像社区|No|
|Description|string|镜像描述信息|No|
|Tags|array|【array of string】镜像标签|No|
|Price|float|镜像价格。单位：元|No|
|Cover|string|镜像封面 URL|No|
|Readme|string|镜像详细描述。仅指定镜像 Id 查询时返回|No|
|Softwares|object|镜像软件信息|No|
|CreatedCount|int|镜像引用创建计数|No|
|FavoritesCount|int|镜像收藏计数|No|
|FailedReason|string|镜像制作失败错误原因|No|
|CreateTime|int|创建时间戳|No|
|PubTime|int|发布时间戳|No|
|Owner|object|镜像所属账号信息|No|
|GroupId|string|镜像组 id|No|
|VersionName|string|版本名称|No|
|VersionDesc|string|版本描述|No|
|SourceGpuType|string|自制镜像来源机型|No|
|AutoStart|bool|是否支持自启动 default:false|No|
|ImageCharge|bool|是否镜像收费 default: false|No|
|ImageUseTime|int|镜像使用时长|No|
##### Software 软件信息

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Framework|string|框架名称|No|
|FrameworkVersion|string|框架版本|No|
|CUDAVersion|string|CUDA 版本|No|
|Applications|array|【array of string】应用列表|No|
##### Owner 所属账号信息

|Parameter name|Type|Description|Required|
|---|---|---|---|
|AccountName|string|账号昵称|No|
|AccountId|string|账号 Id|No|
#### 请求示例

```Plain Text

https://api.ucloud.cn/?Action=DescribeCompShareCustomImages
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=GSIKgudm
&CompShareImageId=ECyEnJbe
&Offset=2
&Limit=2
```

#### 响应示例

```json

{
"Action": "DescribeCompShareCustomImagesResponse",
"ImageSet": [
{
"Status": "hlqtbVJG",
"Name": "nFmURawE",
"Author": "CpKmKtmy",
"CreatedCount": "DQIOscsN",
"CompShareImageId": "hjNwBATq",
"Tags": [
"PbbXTujk"
],
"Cover": "PFuhwZhm",
"Visibility": 2,
"CreateTime": "IFXxRGPj",
"AuthInfo": 6,
"FavoritesCount": "hnuFiuwm",
"ImageOwnerAlias": "xWXjOYVE",
"Readme": "ufXKfxWg",
"Description": "yXiGjmEh",
"PubTime": "kkupHyrZ",
"Price": 9.99592,
"ImageType": "AeSmLeoE",
"Size": 4
}
],
"RetCode": 0,
"TotalCount": 4
}
```

---

### 重启实例 - RebootCompShareInstance

**接口说明**：重启优云智算平台实例

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|**Yes**|
|Zone|string|可用区。cn-wlcb-01|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostId|string|实例 Id|**Yes**|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|UHostId|string|实例 Id|**Yes**|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=RebootCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=IjGiyTeV
&UHostId=GYaCFELy
```

#### 响应示例

```json

{
"Action": "RebootCompShareInstanceResponse",
"UHostId": "FprxeYMp",
"RetCode": 0
}
```

---

### 重装实例 - ReinstallCompShareInstance

**接口说明**：重装优云智算平台实例，可更换系统镜像

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|**Yes**|
|Zone|string|可用区。cn-wlcb-01|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostId|string|实例 Id|**Yes**|
|CompShareImageId|string|镜像 Id|**Yes**|
|Password|string|实例的新密码|No|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|UHostId|string|实例 Id|**Yes**|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=ReinstallCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=vQBurWEY
&UHostId=YNAiIZEC
&CompShareImageId=lXjZDcTq
&Password=FtKctudQ
```

#### 响应示例

```json

{
"Action": "ReinstallCompShareInstanceResponse",
"UHostId": "YHksHalJ",
"RetCode": 0
}
```

---

### 重置实例密码 - ResetCompShareInstancePassword

**接口说明**：重置优云智算平台实例的登录密码

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|**Yes**|
|Zone|string|可用区。cn-wlcb-01|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostId|string|实例 Id|**Yes**|
|Password|string|新密码。需经 Base64 编码|**Yes**|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|UHostId|string|实例 Id|**Yes**|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=ResetCompShareInstancePassword
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=bPGMZwvY
&UHostId=FawcbRha
&Password=ctmwOSIg
```

#### 响应示例

```json

{
"Action": "ResetCompShareInstancePasswordResponse",
"UHostId": "VigQIiTv",
"RetCode": 0
}
```

---

### 启动实例 - StartCompShareInstance

**接口说明**：启动已关机的优云智算平台实例

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|**Yes**|
|Zone|string|可用区。cn-wlcb-01|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostId|string|实例 Id|**Yes**|
|WithoutGpu|bool|是否进行无卡开机|No|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|UHostId|string|实例 Id|**Yes**|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=StartCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=cEMGtAkM
&UHostId=NHNZFdXi
&WithoutGpu=false
```

#### 响应示例

```json

{
"Action": "StartCompShareInstanceResponse",
"UHostId": "jkHGryKM",
"RetCode": 0
}
```

---

### 关闭实例 - StopCompShareInstance

**接口说明**：关闭运行中的优云智算平台实例

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|**Yes**|
|Zone|string|可用区。cn-wlcb-01|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostId|string|实例 Id|**Yes**|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|UHostId|string|实例 Id|**Yes**|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=StopCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=xEOkvEBT
&UHostId=UpMrYJEe
```

#### 响应示例

```json

{
"Action": "StopCompShareInstanceResponse",
"UHostId": "iKQBDtrH",
"RetCode": 0
}
```

---

### 删除实例 - TerminateCompShareInstance

**接口说明**：删除优云智算平台虚机实例

> **重要提示**
> 在调用本接口删除实例之前，请务必确认以下事项：
> 
> - 实例必须处于关机（Stopped）状态。
> 
> - 若实例仍为运行中（Running），调用本接口将会返回错误，删除操作不会被执行。
> 
> - 如需关闭实例，请先调用关机接口（`StopCompShareInstance`），待实例状态变为 `Stopped` 后再执行删除操作。
> 
> 

#### 请求参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|Region|string|地域。 cn-wlcb|**Yes**|
|Zone|string|可用区。cn-wlcb-01|**Yes**|
|ProjectId|string|项目 ID。不填写为默认项目，子帐号必须填写。 请参考 GetProjectList 接口|No|
|UHostId|string|虚机资源 id|**Yes**|
#### 响应参数

|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|UHostId|string|虚机资源 id|**Yes**|
|InRecycle|string|是否进入回收站|No|
#### 请求示例

```Plain Text

https://api.compshare.cn/?Action=TerminateCompShareInstance
&Region=cn-zj
&Zone=cn-zj-01
&ProjectId=MmpOcBdp
&UHostId=LhxmWZes
```

#### 响应示例

```json

{
"Action": "TerminateCompShareInstanceResponse",
"InRecycle": "QKREBgnO",
"UHostId": "TJYRSKuk",
"RetCode": 0
}
```
---

## SSH客户端使用指南

SSH客户端用于连接GPU实例进行远程操作，支持命令执行、文件传输等功能。

### 连接信息获取

通过查询实例列表获取SSH连接信息：
```bash
python scripts/compshare_client.py list
# 返回结果中包含 SshLoginCommand 和 Password
```

### SSH命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| connect | 测试SSH连接 | `python ssh_client.py connect --ssh-command "..." --password "..."` |
| exec | 执行远程命令 | `python ssh_client.py exec --ssh-command "..." --password "..." --cmd "ls -la"` |
| ls | 列出目录内容 | `python ssh_client.py ls --ssh-command "..." --password "..." --path "/home"` |
| pwd | 显示当前目录 | `python ssh_client.py pwd --ssh-command "..." --password "..."` |
| cd | 切换目录 | `python ssh_client.py cd --ssh-command "..." --password "..." --path "/root"` |
| mkdir | 创建目录 | `python ssh_client.py mkdir --ssh-command "..." --password "..." --path "/home/new"` |
| rm | 删除文件 | `python ssh_client.py rm --ssh-command "..." --password "..." --path "/home/file.txt"` |
| rmdir | 删除空目录 | `python ssh_client.py rmdir --ssh-command "..." --password "..." --path "/home/empty"` |
| cat | 查看文件内容 | `python ssh_client.py cat --ssh-command "..." --password "..." --path "/etc/hosts"` |
| stat | 获取文件信息 | `python ssh_client.py stat --ssh-command "..." --password "..." --path "/home/file.txt"` |
| rename | 重命名文件/目录 | `python ssh_client.py rename --ssh-command "..." --password "..." --old "/home/a" --new "/home/b"` |
| chmod | 修改权限 | `python ssh_client.py chmod --ssh-command "..." --password "..." --path "/home/script.sh" --mode 755` |
| upload | 上传文件 | `python ssh_client.py upload --ssh-command "..." --password "..." --local ./file.txt --remote /home/file.txt` |
| upload-dir | 上传目录 | `python ssh_client.py upload-dir --ssh-command "..." --password "..." --local ./project --remote /home/project` |
| download | 下载文件 | `python ssh_client.py download --ssh-command "..." --password "..." --remote /home/file.txt --local ./file.txt` |
| download-dir | 下载目录 | `python ssh_client.py download-dir --ssh-command "..." --password "..." --remote /home/data --local ./data` |
| shell | 交互式Shell | `python ssh_client.py shell --ssh-command "..." --password "..."` |

### SSH使用示例

#### 1. 执行远程命令
```bash
python scripts/ssh_client.py exec \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --cmd "nvidia-smi"
```

#### 2. 上传代码到GPU实例
```bash
python scripts/ssh_client.py upload-dir \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --local ./my_project \
  --remote /root/my_project
```

#### 3. 下载训练结果
```bash
python scripts/ssh_client.py download-dir \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --remote /root/output \
  --local ./results
```

#### 4. 查看文件内容
```bash
python scripts/ssh_client.py cat \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --path /root/train.log
```

#### 5. 启动交互式Shell
```bash
python scripts/ssh_client.py shell \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password"
```

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 160 | 参数错误 |
| 161 | 资源不存在 |
| 162 | 资源状态错误 |
| 163 | 配额不足 |
| 170 | 认证失败 |
| 171 | 权限不足 |
| 172 | 账户余额不足 |

---

## 最佳实践

### 1. 实例生命周期管理
```
创建 -> 启动 -> 运行中 -> 停止 -> 删除
         ↑____________↓
              重启
```

### 2. 删除实例流程
1. 先调用 StopCompShareInstance 停止实例
2. 等待实例状态变为 Stopped
3. 调用 TerminateCompShareInstance 删除实例

### 3. 密码管理
- 创建实例时设置初始密码
- 使用 ResetCompShareInstancePassword 重置密码
- 密码需要 base64 编码后传输

### 4. 计费模式选择
| 模式 | 说明 | 适用场景 |
|------|------|----------|
| Dynamic | 按小时预付费 | 短期测试、临时任务 |
| Postpay | 按小时后付费 | 支持关机不收费 |
| Day | 按天付费 | 中期使用 |
| Month | 按月付费 | 长期稳定使用 |
| Spot | 抢占式实例（内测） | 短期测试、临时任、不支持关机不收费 |
### 5. 实例状态说明
| 状态 | 说明 | 可执行操作 |
|------|------|------------|
| Pending | 创建中 | 等待 |
| Running | 运行中 | 停止、重启、重置密码、SSH连接 |
| Stopped | 已停止 | 启动（正常/无卡）、删除 |

### 6. 无卡开机使用场景
- 只需要CPU计算资源时
- 需要修改代码或配置文件时
- 需要下载或整理数据时
- 暂时不需要GPU但需要保持环境时

