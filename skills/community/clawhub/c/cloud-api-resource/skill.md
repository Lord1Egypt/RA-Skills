---
name: ucloud-resource-creator
version: 2.0.0
description: |
  UCloud 云资源创建技能。当用户需要在 UCloud 平台创建云资源时，Agent 自动调用 UCloud 官方 API 完成资源创建。
  适用场景包括：创建云主机(UHost)、创建 API Key、创建存储桶(UFile)、创建数据库(UDDB)、创建 VPC 等 UCloud 平台资源的操作。
  支持 UCloud 特有签名认证（SHA1），所有参数要求实时参考 UCloud 官方 API 文档。
license: MIT
compatibility:
  runtime: "支持 HTTP 请求的 AI Agent 环境"
  dependencies:
    - "http.client"
    - "hashlib"
    - "urllib.parse"
    - "base64"
    - "json"
parameters:
  - name: api_endpoint
    type: string
    required: true
    description: "UCloud API 的完整请求 URL。示例：https://api.ucloud.cn/?Action=CreateUHostInstance"
  - name: public_key
    type: string
    required: true
    description: "UCloud 账号的公钥（PublicKey），用于身份识别和签名计算。"
  - name: private_key
    type: string
    required: true
    description: "UCloud 账号的私钥（PrivateKey），用于签名生成。该值需保密，不在日志中明文输出。"
  - name: api_params
    type: object
    required: true
    description: "API 请求的业务参数（键值对）。"
output:
  type: object
  properties:
    success: "布尔值，表示 API 调用是否成功"
    status_code: "HTTP 响应状态码"
    response_data: "API 返回的原始响应内容（JSON 或文本）"
    resource_id: "若响应中包含资源 ID（如 UHostId、KeyId），自动提取并返回"
    error_message: "失败时的错误描述"
---

# UCloud 云资源创建器

## 技能概述

本技能专用于 UCloud 平台，使 AI Agent 能够根据用户的自然语言描述，自动构造并执行 UCloud API 请求完成资源创建。所有签名算法、参数要求均实时参考 UCloud 官方 API 文档。

**核心特性：**
- 专精 UCloud 平台 API
- 实时参考 UCloud 官方文档获取最新参数要求
- 引导式交互配置，必填参数强制填写
- 创建前信息确认，支持自定义参数
- UCloud 特有 SHA1 签名算法

## 适用场景

| 场景 | 说明 |
|------|------|
| 创建云主机 | 在 UCloud 创建 UHost 实例 |
| 创建 API Key | 在 UCloud ModelVerse 创建推理 API 密钥 |
| 创建存储桶 | 在 UCloud UFile 创建存储空间 |
| 创建数据库 | 在 UCloud UDDB 创建数据库实例 |
| 创建 VPC | 在 UCloud 创建私有网络 |

## 核心工作流

```
用户表达创建意图
→ Agent 识别资源类型（云主机/API Key/存储桶等）
→ 判断用户输入模式（自然语言模式 / 交互式模式）
→ 自然语言模式：解析用户描述，自动映射到 API 参数
→ 交互式模式：引导用户逐步填写各项参数
→ 汇总配置信息，等待用户确认
→ 生成 UCloud SHA1 签名并构造 HTTP 请求
→ 发送请求
→ 解析响应
→ 提取资源ID（如有）
→ 返回结果给用户
```

## 交互模式选择

当用户表达创建意图时，Agent 应首先判断用户输入模式：

### 模式一：自然语言模式（快速创建）

用户通过自然语言一次性描述创建需求，Agent 自动解析并映射到 API 参数。

**触发示例：**
- "在乌兰察布创建一台快杰O型云主机，1核2G，40G RSSD盘，Ubuntu 20.04，1M带宽"
- "帮我创建个 API Key，名字叫 test-key，项目 org-d1kjc2"
- "创建一台 Windows 云主机，4核8G，上海地域，按月付费"

**处理流程：**
1. Agent 解析用户自然语言描述
2. 提取关键信息（地域、配置、镜像等）
3. 自动映射到 UCloud API 参数
4. 展示解析后的配置清单
5. 用户确认后直接创建

**参数映射规则：**

| 用户描述 | API 参数 | 示例 |
|---------|---------|------|
| 地域/区域 | Region | "乌兰察布" → cn-wlcb |
| 可用区 | Zone | "可用区A" → cn-wlcb-01 |
| 机型 | MachineType + UHostFamily | "快杰O型" → O + o1i |
| CPU | CPU | "1核" → 1 |
| 内存 | Memory | "2G" → 2048 |
| 磁盘大小 | Disks.N.Size | "40G" → 40 |
| 磁盘类型 | Disks.N.Type | "SSD" → CLOUD_SSD |
| 镜像 | ImageId | "Ubuntu 20.04" → uimage-txo15p |
| 带宽 | NetworkInterface.N.EIP.Bandwidth | "1M" → 1 |
| 计费方式 | ChargeType | "按时" → Dynamic |
| 名称 | Name | "test-host" → test-host |

**缺失参数处理：**
- 对于用户未提及的参数，使用默认值
- 必填参数缺失时，提示用户补充
- 提供参数补全建议

### 模式二：交互式模式（分步配置）

用户未提供完整配置或需要逐步确认时，Agent 引导用户逐步填写各项参数。

**触发示例：**
- "创建云主机"
- "帮我创建一台服务器"
- "我要创建 UHost"

**处理流程：**
1. Agent 识别创建意图
2. 通过 AskUserQuestion 逐步引导用户选择/填写参数
3. 每步提供可选值列表
4. 汇总配置信息，等待用户确认
5. 用户确认后创建

## 交互式配置引导

### 通用必填参数

所有 UCloud API 请求均需包含：
- **Action**：API 操作名称，如 CreateUHostInstance
- **PublicKey**：用户公钥
- **ProjectId**：项目 ID
- **Timestamp**：Unix 时间戳（秒）
- **Signature**：签名

### 云主机(UHost)配置引导

#### 步骤1：基础配置（必填参数）
通过 AskUserQuestion 依次询问：
1. **Region**（地域）：如 cn-wlcb、cn-sh2、cn-bj2 等
   - 必填，参见 UCloud 地域列表
2. **Zone**（可用区）：如 cn-wlcb-01、cn-sh2-01 等
   - 必填，根据 Region 自动列出
3. **ImageId**（镜像ID）：如 uimage-txo15p
   - 必填，需先查询可用镜像列表
4. **CPU**：1、2、4、8 等
   - 必填
5. **Memory**：1024、2048、4096、8192 等（单位 MB）
   - 必填
6. **Disks.N.Size**：20、40、100 等（单位 GB）
   - 必填
7. **Disks.N.Type**：CLOUD_SSD、CLOUD_RSSD、CLOUD_NORMAL 等
   - 必填，需根据机型选择支持的磁盘类型
8. **Disks.N.IsBoot**：True（系统盘）或 False（数据盘）
   - 必填
9. **LoginMode**：Password 或 KeyPair
   - 必填
10. **Password**：登录密码（LoginMode=Password 时必填）
    - 需 Base64 编码

#### 步骤2：机型选择（必填）
通过 AskUserQuestion 询问机型：
- **快杰O型**（MachineType=O）：高性能计算型
  - o1i：Intel平台
  - o1a：AMD平台
  - o1r：ARM平台
- **快杰共享型**（N型）：性价比型
- **通用型**：标准计算型

**注意**：不同机型支持的磁盘类型不同，需根据机型自动过滤可选磁盘类型。

#### 步骤3：网络配置（必填）
- **NetworkInterface.N.EIP.Bandwidth**：带宽大小（Mbps）
- **NetworkInterface.N.EIP.PayMode**：Bandwidth（带宽计费）或 Traffic（流量计费）
- **NetworkInterface.N.EIP.OperatorName**：Bgp、Telecom、Unicom、Mobile

#### 步骤4：计费方式（必填）
- **ChargeType**：Dynamic（按时）、Month（按月）、Year（按年）
- **Quantity**：购买时长（ChargeType=Month/Year 时必填）

#### 步骤5：镜像选择
通过 AskUserQuestion 询问镜像：
- **操作系统类型**：Linux、Windows
- **具体镜像**：根据地域和机型动态查询可用镜像列表
  - Ubuntu 20.04/22.04
  - CentOS 7.x/8.x
  - Debian、Fedora等

### API Key 配置引导

#### 必填参数
1. **Action**：CreateUMInferAPIKey
2. **PublicKey**：用户公钥
3. **ProjectId**：项目 ID
4. **Name**：API Key 名称
5. **Timestamp**：Unix 时间戳

#### 可选参数
- **IPWhitelist**：访问白名单 IP
- **DailyLimitAmount**：每日限额
- **MonthlyLimitAmount**：每月限额
- **ExpireTime**：过期时间

### 存储桶(UFile)配置引导

#### 必填参数
1. **Action**：CreateBucket
2. **PublicKey**：用户公钥
3. **ProjectId**：项目 ID
4. **BucketName**：存储桶名称
5. **Region**：地域
6. **Timestamp**：Unix 时间戳

#### 可选参数
- **Type**：公有或私有
- **Domain**：自定义域名

## 信息确认（通用）

在最终创建前，**必须**通过 AskUserQuestion 向用户展示完整的配置清单，等待用户确认：

```
请确认以下配置信息：
- 资源类型：UHost 云主机
- 地域：cn-wlcb
- 可用区：cn-wlcb-01
- 机型：快杰O型 (o1i)
- CPU：1核
- 内存：2GB
- 系统盘：20GB (CLOUD_RSSD)
- 镜像：Ubuntu 20.04
- 带宽：1Mbps (BGP)
- 计费方式：按时付费
- 登录方式：密码

是否确认创建？[确认/取消]
```

**自定义参数支持**：
在信息确认步骤中，Agent 应询问用户是否需要添加其他参数：
- "是否需要添加其他参数？（如安全组、标签、VPC等）"
- 用户可输入自定义参数键值对
- Agent 将自定义参数合并到最终请求中

用户确认后，再执行实际的 API 调用。用户取消则终止流程。

## 参数详解

### api_endpoint
UCloud API 的完整 URL。格式：`https://api.ucloud.cn/?Action=xxx`

示例：
- `https://api.ucloud.cn/?Action=CreateUHostInstance`
- `https://api.ucloud.cn/?Action=CreateUMInferAPIKey`
- `https://api.ucloud.cn/?Action=CreateBucket`

### public_key 和 private_key
- **public_key**：UCloud 公钥，在控制台 API 密钥管理页面获取
- **private_key**：UCloud 私钥，用于签名计算。**Agent 必须承诺不在日志、对话记录或任何持久化存储中明文保存 private_key**

### api_params
UCloud API 请求的业务参数。Agent 应提示用户提供 API 文档中标为"必填"的参数。

## 输出处理

成功时，Skill 返回完整响应体，并尝试从常见字段中提取资源 ID：
- UHostId / KeyId / BucketId / ResourceId
- data.UHostId / data.KeyId（嵌套结构）

若提取成功，在返回信息中高亮显示，并提示用户妥善保存该资源 ID。

失败时，返回 HTTP 状态码和错误信息。常见错误包括：
- 签名错误（RetCode: 171）
- 参数缺失（RetCode: 230）
- 资源不存在（RetCode: 8215）
- 权限不足
- 资源配额不足

## 安全与隐私

- **私钥不落盘**：Skill 运行时将 private_key 存储在内存变量中，调用结束后自动释放
- **请求日志脱敏**：打印请求详情时，将 private_key 替换为 ***REDACTED***
- **传输加密**：强制使用 HTTPS 端点
- **最小权限原则**：建议用户为创建操作使用仅包含必要权限的子账号密钥

## 典型触发语示例

用户可以说：
- "在 UCloud 创建一台云主机"
- "帮我创建 UCloud API Key"
- "创建 UCloud 存储桶"
- "调用 UCloud API 创建资源"

Agent 识别到用户意图为"在 UCloud 创建资源"时，即可调用本 Skill。
