# Alibaba Cloud Query Skill - Usage Examples

基于 Alibaba Cloud Query Skill 的完整使用示例，展示如何按照 Step 1-7 的流程进行产品信息查询和对比分析。

---

## Example 1: 查询单个产品完整信息 (ECS)

**User:** "帮我详细了解一下云服务器ECS"

**Agent Action Flow:**

### Step 1: Identify the Product (识别产品)
- 用户查询关键词 (User Query Keywords): "云服务器", "ECS"
- 匹配产品 (Matched Product): 云服务器 ECS (Elastic Compute Service)
- 产品代码 (Product Code): ecs

### Step 2: Construct Search Queries (构建搜索查询)
- 中国站 (China Site): "ECS 云服务器 site:aliyun.com"
- 文档 (Documentation): "ECS 实例规格 计费 site:help.aliyun.com"

### Step 3: Retrieve Product Homepage Information (获取产品首页信息)
- 访问 (Visit): `https://www.aliyun.com/product/ecs`
- 提取首页核心信息 (Extract Homepage Core Info):
  - **Slogan**: "弹性可伸缩，安全高性能的云服务器" (Elastic and scalable, secure and high-performance cloud server)
  - **核心卖点 (Core Selling Points)**: 弹性伸缩、安全稳定、高性能、丰富的实例规格 (Elastic scaling, security and stability, high performance, rich instance types)
  - **主要功能模块 (Main Function Modules)**: 实例、镜像、块存储、快照、网络、安全组 (Instance, Image, Block Storage, Snapshot, Network, Security Group)
  - **应用场景 (Use Cases)**: 网站应用、企业应用、游戏、大数据分析 (Web applications, enterprise applications, gaming, big data analytics)

### Step 4: Search Official Documentation (搜索官方文档)
按照文档架构检索各模块信息 (Retrieve information from each module according to documentation architecture):
- 产品概述 (Product Overview): `https://help.aliyun.com/zh/ecs/product-overview/`
- 计费说明 (Pricing): `https://help.aliyun.com/zh/ecs/product-overview/billing-overview/`
- 实例规格 (Instance Types): `https://help.aliyun.com/zh/ecs/user-guide/overview-of-instance-families/`
- 快速入门 (Quick Start): `https://help.aliyun.com/zh/ecs/getting-started/`

### Step 5: Extract Key Information from Documentation (从文档提取关键信息)
提取各维度详细信息 (Extract detailed information from each dimension):
- 产品概述 (Overview): 计算存储分离架构、多种实例规格族 (Compute-storage separated architecture, multiple instance families)
- 计费 (Pricing): 包年包月、按量付费、抢占式实例 (Subscription, Pay-as-you-go, Spot Instance)
- 功能 (Features): 弹性伸缩、自动快照、云监控集成 (Auto Scaling, Automatic Snapshot, CloudMonitor Integration)
- 操作 (Operations): 实例创建、连接、管理、释放 (Instance creation, connection, management, release)

### Step 6: Integrate and Synthesize Information (整合和综合信息)
融合首页信息和文档信息 (Integrate homepage and documentation information):
- 首页卖点 + 文档技术细节 (Homepage selling points + Documentation technical details)
- 验证价格信息一致性 (Verify pricing information consistency)
- 补充技术架构说明 (Supplement technical architecture description)

### Step 7: Present Results

```markdown
# 云服务器 ECS - Elastic Compute Service

> 弹性可伸缩，安全高性能的云服务器，提供稳定可靠的计算能力

---

## 一、产品概述 (Product Overview)

### 1.1 产品简介
**产品定位**: 阿里云最基础的云计算服务，提供可弹性伸缩的计算能力

**核心价值主张**: 弹性可伸缩，安全高性能，分钟级交付

**产品描述**: 云服务器ECS是一种安全可靠、弹性可伸缩的云计算服务。您可以根据业务需要随时创建、释放、升级或降级实例，实现计算资源的灵活管理。

### 1.2 产品架构
**架构概览**: 采用虚拟化技术，将物理服务器资源池化，按需分配给用户的实例

**核心组件**:
- **实例 (Instance)**: 虚拟计算环境，包含CPU、内存、操作系统
- **镜像 (Image)**: 实例运行环境的模板，包含操作系统和预装软件
- **块存储 (Block Storage)**: 低时延、持久化的数据块级存储
- **快照 (Snapshot)**: 某一时间点磁盘数据的备份
- **网络 (Network)**: VPC、安全组、弹性公网IP

### 1.3 功能特性

**首页核心卖点**:
- 弹性可伸缩，分钟级创建和释放
- 99.95%的服务可用性
- 丰富的实例规格，满足各类场景
- 多重安全防护，保障数据安全

**详细功能列表**:
| 功能模块 | 功能描述 | 信息来源 |
|---------|---------|---------|
| 弹性计算 | 支持随时升级/降级实例配置 | 首页+文档 |
| 自动伸缩 | 根据负载自动调整实例数量 | 文档 |
| 镜像市场 | 丰富的预装环境镜像 | 首页 |
| 快照备份 | 自动/手动快照，支持秒级回滚 | 文档 |
| 安全组 | 虚拟防火墙，控制网络访问 | 文档 |
| 云监控 | 全方位监控告警 | 文档 |

### 1.4 产品系列/版本
| 版本/系列 | 适用场景 | 主要特性 |
|----------|---------|---------|
| 标准实例 | 通用场景 | 性价比高，适合大多数应用 |
| 计算优化 | 高性能计算 | CPU密集型，高CPU内存比 |
| 内存优化 | 内存数据库 | 大内存，适合缓存、数据库 |
| GPU实例 | AI/图形渲染 | NVIDIA GPU加速 |
| 裸金属 | 高性能物理机 | 物理机性能，云资源弹性 |

### 1.5 应用场景
- **网站应用**: 搭建Web服务器、应用服务器
- **企业应用**: ERP、CRM、OA等企业管理系统
- **游戏服务**: 游戏服务器、对战平台
- **大数据分析**: 数据处理、批量计算

---

## 二、产品计费 (Product Pricing)

### 2.1 计费项 (Billable Items)
| 计费组件 (Component) | 计费说明 (Description) |
|---------------------|----------------------|
| 实例规格 (Instance) | 按CPU和内存配置计费 (Billed by CPU and memory configuration) |
| 系统盘 (System Disk) | 随实例计费的存储 (Storage billed with instance) |
| 数据盘 (Data Disk) | 独立计费的块存储 (Independent block storage billing) |
| 公网带宽 (Public Bandwidth) | 按带宽或流量计费 (Billed by bandwidth or traffic) |
| 快照 (Snapshot) | 按快照占用存储空间计费 (Billed by snapshot storage usage) |

### 2.2 计费方式 (Billing Methods)
| 计费方式 (Method) | 说明 (Description) | 适用场景 (Scenario) |
|------------------|-------------------|-------------------|
| 包年包月 (Subscription) | 预付费，价格优惠 (Prepaid with discount) | 长期稳定业务 (Long-term stable business) |
| 按量付费 (Pay-as-you-go) | 后付费，按小时计费 (Postpaid, hourly billing) | 短期、突发业务 (Short-term, burst business) |
| 抢占式实例 (Spot Instance) | 价格最低，可能被释放 (Lowest price, may be reclaimed) | 容错性高的任务 (Fault-tolerant tasks) |

### 2.3 价格参考 (Pricing Reference)
- **起步价格 (Starting Price)**: 约0.1元/小时起（按量付费）(~¥0.1/hour for pay-as-you-go)
- **免费额度 (Free Tier)**: 新用户可享受部分免费试用 (New users can enjoy partial free trial)
- **计费计算器 (Price Calculator)**: https://www.aliyun.com/price/ecs

---

## 三、快速入门 (Quick Start)

### 3.1 使用限制 (Usage Limits)
| 限制项 (Limit Item) | 限制值 (Limit Value) |
|--------------------|---------------------|
| 单个地域实例数 (Instances per region) | 根据配额调整 (Adjustable by quota) |
| 公网IP绑定 (Public IP binding) | 与实例一一对应 (One-to-one with instance) |
| 安全组规则 (Security group rules) | 默认200条 (Default 200 rules) |

### 3.2 入门步骤 (Getting Started Steps)
1. 选择地域和可用区 (Select region and zone)
2. 选择实例规格和镜像 (Select instance type and image)
3. 配置网络和存储 (Configure network and storage)
4. 设置安全组规则 (Set security group rules)
5. 创建并连接实例 (Create and connect to instance)

---

## 四、操作指南 (Operation Guide)

### 4.1 实例管理 (Instance Management)
| 操作 (Operation) | 说明 (Description) |
|-----------------|-------------------|
| 创建 (Create) | 通过控制台或API创建实例 (Create via console or API) |
| 启动/停止 (Start/Stop) | 控制实例运行状态 (Control instance running state) |
| 重启 (Restart) | 软重启或强制重启 (Soft or forced restart) |
| 释放 (Release) | 彻底删除实例，数据清除 (Permanently delete instance and data) |

### 4.2 配置管理 (Configuration Management)
- **升降配 (Scale Up/Down)**: 支持在线和离线变更配置 (Support online and offline configuration changes)
- **更换系统盘 (Replace System Disk)**: 可更换操作系统 (Can replace operating system)
- **扩容磁盘 (Expand Disk)**: 在线扩容数据盘 (Online expansion of data disk)

---

## 五、相关资源 (Related Resources)

### 文档链接 (Documentation Links)
- [产品首页 (Product Homepage)](https://www.aliyun.com/product/ecs)
- [帮助文档 (Documentation)](https://help.aliyun.com/zh/ecs/)
- [API参考 (API Reference)](https://help.aliyun.com/zh/ecs/developer-reference/)
- [定价详情 (Pricing Details)](https://www.aliyun.com/price/ecs)

### 相关产品 (Related Products)
- **VPC (Virtual Private Cloud)**: 专有网络，隔离的网络环境 (Isolated network environment)
- **SLB (Server Load Balancer)**: 负载均衡，流量分发 (Load balancing and traffic distribution)
- **OSS (Object Storage Service)**: 对象存储，数据持久化存储 (Object storage for data persistence)
```

---

## Example 2: 产品对比分析 (PolarDB MySQL vs PolarDB-X)

**User:** "PolarDB MySQL版和PolarDB-X分布式版有什么区别？"

**Agent Action Flow:**

### Step 1: Identify Products
- 产品1: PolarDB MySQL版 (polardb-for-mysql)
- 产品2: PolarDB-X分布式版 (polardb-for-xscale)

### Step 2-3: 分别获取两个产品的首页信息
- PolarDB MySQL: `https://www.aliyun.com/product/polardb/mysql`
- PolarDB-X: `https://www.aliyun.com/product/apsaradb/polardbx`

### Step 4-5: 分别检索两个产品的文档信息
- 架构文档
- 计费说明
- 功能特性
- 适用场景

### Step 6: Integrate and Compare
对比维度:
- 架构差异 (Shared-Storage vs Shared-Nothing)
- 扩展方式 (垂直扩展 vs 水平扩展)
- 适用场景 (集中式 vs 分布式)
- 价格差异

### Step 7: Present Comparison Results

```markdown
# PolarDB MySQL 版 vs PolarDB-X 分布式版 - 对比分析

## 一、核心差异对比

| 对比维度 | PolarDB MySQL 版 | PolarDB-X 分布式版 |
|---------|------------------|-------------------|
| **产品定位** | 云原生集中式数据库 | 云原生分布式数据库 |
| **核心架构** | 计算存储分离 + 共享存储 | 计算存储分离 + Shared-Nothing |
| **扩展方式** | 垂直扩展 + 只读节点 | 水平扩展（分库分表） |
| **数据分布** | 集中式存储 | 分布式分片存储 |
| **最大节点数** | 1写15读 | 1024节点 |
| **弹性速度** | 秒级 | 分钟级 |
| **分布式事务** | 不支持 | 原生支持 |

## 二、功能特性对比

| 功能 | PolarDB MySQL | PolarDB-X |
|-----|---------------|-----------|
| MySQL兼容性 | 100% | 100% |
| HTAP能力 | 支持 | 支持 |
| 读写分离 | 自动 | 透明 |
| 全局二级索引 | 支持 | 支持 |
| 数据分片 | 不支持 | 支持 |
| 透明分布式 | 不适用 | 支持 |

## 三、适用场景建议 (Use Case Recommendations)

**选择 PolarDB MySQL 版 (Choose PolarDB MySQL when):**
- 需要高性能、高可用的集中式数据库 (Need high-performance, highly available centralized database)
- 数据量在TB级别，单库存储足够 (Data volume at TB level, single database storage sufficient)
- 需要秒级弹性扩缩容 (Need second-level elastic scaling)
- 从RDS MySQL升级 (Upgrading from RDS MySQL)

**选择 PolarDB-X (Choose PolarDB-X when):**
- 数据量达到PB级，需要水平扩展 (Data volume reaches PB level, need horizontal scaling)
- 超高并发交易场景（如支付、订单）(Ultra-high concurrency transaction scenarios like payment, orders)
- 需要分布式事务支持 (Need distributed transaction support)
- 业务中台、物联网大数据场景 (Business middle platform, IoT big data scenarios)

## 四、价格对比 (Pricing Comparison)

| 产品 (Product) | 起步价格 (Starting Price) | 价格特点 (Pricing Features) |
|---------------|--------------------------|----------------------------|
| PolarDB MySQL 标准版 (Standard) | 约200元/月 (~¥200/month) | 年付5折起 (Up to 50% off for annual payment) |
| PolarDB-X 标准版 (Standard) | 55元/月起 (From ¥55/month) | 降价40%后 (After 40% price reduction) |
| PolarDB-X 企业版 (Enterprise) | 按配置询价 (Quote based on configuration) | 分层计费 (Tiered billing) |

## 五、选型建议 (Selection Recommendations)

1. **从RDS迁移 (Migrating from RDS)**: 优先选择 PolarDB MySQL 版，平滑升级 (Prioritize PolarDB MySQL for smooth upgrade)
2. **解决单机瓶颈 (Solving single-machine bottleneck)**: 选择 PolarDB-X，支持水平扩展 (Choose PolarDB-X for horizontal scaling support)
3. **成本敏感 (Cost-sensitive)**: PolarDB-X 标准版价格更低 (PolarDB-X Standard Edition has lower price)
4. **极致性能 (Extreme performance)**: PolarDB MySQL 企业版提供秒级弹性 (PolarDB MySQL Enterprise provides second-level elasticity)

> **注意 (Note)**: 两个产品都支持从标准版平滑升级到企业版，PolarDB-X还支持从集中式平滑演进到分布式架构。(Both products support smooth upgrade from Standard to Enterprise Edition, and PolarDB-X also supports smooth evolution from centralized to distributed architecture.)
```

---

## Example 3: 查询产品计费详情 (OSS)

**User:** "OSS存储是怎么收费的？"

**Agent Action Flow:**

### Step 1: Identify Product
- 产品: 对象存储 OSS (Object Storage Service)
- 产品代码: oss

### Step 2-3: Get Homepage Info
- 访问: `https://www.aliyun.com/product/oss`
- 提取: 产品定位、核心功能、定价入口

### Step 4: Search Pricing Documentation
- 计费说明: `https://help.aliyun.com/zh/oss/product-overview/billing-overview/`
- 价格详情: `https://www.aliyun.com/price/oss`

### Step 5: Extract Pricing Information
- 计费项: 存储费、流量费、请求费、数据处理费
- 计费方式: 按量付费、资源包
- 价格 tiers: 标准、低频、归档、冷归档

### Step 6: Integrate Information
- 首页功能亮点 + 文档详细计费规则
- 验证价格一致性

### Step 7: Present Results

```markdown
# 对象存储 OSS - Object Storage Service

## 产品计费详解

### 计费项组成
| 计费项 | 说明 | 计费方式 |
|-------|------|---------|
| **存储费用** | 按实际存储量计费 | 按量付费/存储包 |
| **流量费用** | 外网流出流量 | 按量付费/流量包 |
| **请求费用** | PUT/GET等API请求 | 按量付费 |
| **数据处理** | 图片处理、视频截帧等 | 按量付费 |

### 存储类型价格对比
| 存储类型 | 适用场景 | 单价(元/GB/月) |
|---------|---------|---------------|
| **标准存储** | 频繁访问 | ~0.12 |
| **低频访问** | 月均访问1-2次 | ~0.08 |
| **归档存储** | 很少访问 | ~0.033 |
| **冷归档** | 几乎不访问 | ~0.015 |

### 计费方式选择建议 (Billing Method Recommendations)
- **按量付费 (Pay-as-you-go)**: 业务波动大，难以预测用量 (Business fluctuates greatly, difficult to predict usage)
- **资源包 (Resource Package)**: 业务稳定，可预估用量，更优惠 (Stable business, predictable usage, more cost-effective)

### 成本优化建议 (Cost Optimization Tips)
1. 根据访问频率选择合适的存储类型 (Choose appropriate storage type based on access frequency)
2. 使用生命周期规则自动转换存储类型 (Use lifecycle rules to automatically transition storage types)
3. 购买资源包享受折扣 (Purchase resource packages for discounts)
4. 使用CDN加速减少回源流量 (Use CDN acceleration to reduce origin traffic)

### 价格计算器 (Price Calculator)
[OSS价格计算器 (OSS Price Calculator)](https://www.aliyun.com/price/oss)
```

---

## Example 4: 查询API开发参考 (创建ECS实例)

**User:** "创建ECS实例的API需要哪些参数？"

**Agent Action Flow:**

### Step 1: Identify Query Type
- 产品: ECS
- 信息类型: API参数 / 开发参考

### Step 2-4: Search API Documentation
- API概览: `https://help.aliyun.com/zh/ecs/developer-reference/api-overview/`
- CreateInstance API: `https://help.aliyun.com/zh/ecs/developer-reference/createinstance/`

### Step 5: Extract API Information
- API名称: CreateInstance
- 请求方式: RPC/REST
- 必需参数 vs 可选参数
- 参数约束和示例

### Step 7: Present API Reference

```markdown
# ECS CreateInstance API - 创建实例

## API概览
- **Action**: CreateInstance
- **版本**: 2014-05-26
- **协议**: HTTP/HTTPS

## 必需参数 (Required Parameters)

| 参数名 | 类型 | 说明 |
|-------|------|------|
| **RegionId** | String | 地域ID，如 cn-hangzhou |
| **ImageId** | String | 镜像ID |
| **InstanceType** | String | 实例规格，如 ecs.g7.large |
| **SecurityGroupId** | String | 安全组ID |

## 常用可选参数 (Optional Parameters)

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|-------|------|
| **InstanceName** | String | 随机生成 | 实例名称 |
| **Password** | String | - | 实例登录密码 |
| **KeyPairName** | String | - | 密钥对名称 |
| **VSwitchId** | String | - | 交换机ID |
| **SystemDisk.Category** | String | cloud_efficiency | 系统盘类型 |
| **SystemDisk.Size** | Integer | 40 | 系统盘大小(GB) |
| **InternetChargeType** | String | PayByTraffic | 网络计费类型 |
| **InternetMaxBandwidthOut** | Integer | 0 | 公网出带宽(Mbps) |
| **InstanceChargeType** | String | PostPaid | 实例计费方式 |

## 请求示例

```bash
# Alibaba Cloud CLI
aliyun ecs CreateInstance \
  --RegionId cn-hangzhou \
  --ImageId ubuntu_22_04_x64_20G_alibase_20230515.vhd \
  --InstanceType ecs.g7.large \
  --SecurityGroupId sg-bp67acfmxazb4ph*** \
  --VSwitchId vsw-bp1s5grzef8zs9yg*** \
  --InstanceName MyFirstInstance \
  --SystemDisk.Category cloud_essd \
  --SystemDisk.Size 100
```

```python
# Python SDK
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest

client = AcsClient('<access_key_id>', '<access_secret>', 'cn-hangzhou')
request = CreateInstanceRequest()
request.set_RegionId('cn-hangzhou')
request.set_ImageId('ubuntu_22_04_x64_20G_alibase_20230515.vhd')
request.set_InstanceType('ecs.g7.large')
request.set_SecurityGroupId('sg-bp67acfmxazb4ph***')

response = client.do_action_with_exception(request)
print(response)
```

## 返回示例 (Response Example)
```json
{
  "InstanceId": "i-bp67acfmxazb4ph***",
  "RequestId": "473469C7-AA6F-4DC5-B3DB-A3DC0DE3C83E"
}
```

## 错误码 (Error Codes)
| 错误码 (Error Code) | 说明 (Description) |
|--------------------|-------------------|
| InvalidRegionId.NotFound | 指定的地域ID不存在 (Specified region ID does not exist) |
| InvalidImageId.NotFound | 指定的镜像ID不存在 (Specified image ID does not exist) |
| InvalidInstanceType.ValueNotSupported | 指定的实例规格不可用 (Specified instance type is not available) |
| QuotaExceed.ElasticIPs | 公网IP配额不足 (Elastic IP quota exceeded) |

## 相关API (Related APIs)
- [RunInstances](https://help.aliyun.com/zh/ecs/developer-reference/runinstances) - 批量创建实例 (Create instances in batch)
- [StartInstance](https://help.aliyun.com/zh/ecs/developer-reference/startinstance) - 启动实例 (Start instance)
- [DescribeInstances](https://help.aliyun.com/zh/ecs/developer-reference/describeinstances) - 查询实例列表 (Query instance list)

## 参考文档 (Reference Documentation)
- [API概览 (API Overview)](https://help.aliyun.com/zh/ecs/developer-reference/api-overview/)
- [OpenAPI Explorer](https://api.aliyun.com/?product=Ecs)
- [SDK下载 (SDK Download)](https://help.aliyun.com/zh/ecs/developer-reference/sdk-reference/)
```

---

## Example 5: 多产品综合选型建议

**User:** "我想搭建一个电商网站，需要数据库、存储和服务器，有什么推荐？"

**Agent Action Flow:**

### Step 1: Analyze Requirements
- **场景**: 电商网站
- **需求**: 计算资源(ECS) + 数据库 + 文件存储
- **隐含需求**: 高可用、弹性扩展、安全防护

### Step 2-6: Query Multiple Products
分别查询并分析:
1. ECS - 应用服务器
2. RDS/PolarDB - 数据库
3. OSS - 图片/文件存储
4. SLB/ALB - 负载均衡
5. CDN - 静态资源加速

### Step 7: Present Integrated Solution

```markdown
# 电商网站架构方案推荐

## 一、产品选型组合

| 层级 | 推荐产品 | 说明 |
|-----|---------|------|
| **接入层** | CDN + ALB | 全球加速 + 应用负载均衡 |
| **应用层** | ECS/容器服务 | 部署Web应用，支持弹性伸缩 |
| **数据层** | PolarDB MySQL | 高可用数据库，支持读写分离 |
| **存储层** | OSS | 存储商品图片、用户上传文件 |
| **缓存层** | Tair/Redis | 热点数据缓存，加速访问 |
| **安全** | WAF + 云安全中心 | Web防护 + 安全监控 |

## 二、各产品配置建议

### 1. 云服务器 ECS
- **规格**: 4核8GB起步，根据流量调整
- **数量**: 至少2台，跨可用区部署
- **计费**: 包年包月（长期稳定）
- **镜像**: CentOS/Ubuntu + Nginx/Apache

### 2. 数据库 PolarDB MySQL
- **版本**: 企业版（高可用）
- **规格**: 4核16GB起步
- **架构**: 1写2读，自动读写分离
- **备份**: 开启自动备份，保留7天

### 3. 对象存储 OSS
- **存储类型**: 标准存储（频繁访问）
- **CDN加速**: 开启，提升图片加载速度
- **图片处理**: 开启OSS图片服务，自动生成缩略图

### 4. 负载均衡 ALB
- **类型**: 应用型负载均衡（L7）
- **协议**: HTTPS（配置SSL证书）
- **健康检查**: 开启，自动剔除异常节点

## 三、架构优势 (Architecture Advantages)

1. **高可用 (High Availability)**: 跨可用区部署，单点故障自动切换 (Cross-AZ deployment, automatic failover)
2. **弹性扩展 (Elastic Scaling)**: 支持自动伸缩，应对大促流量 (Support auto-scaling to handle peak traffic)
3. **成本优化 (Cost Optimization)**: 按实际使用量付费，无闲置资源 (Pay for actual usage, no idle resources)
4. **安全防护 (Security Protection)**: 多层安全防护，保障业务安全 (Multi-layer security protection)

## 四、预估成本（月度）(Estimated Monthly Cost)

| 产品 (Product) | 配置 (Configuration) | 预估费用 (Estimated Cost) |
|---------------|---------------------|--------------------------|
| ECS | 2台 × 4核8GB (2 instances × 4C8G) | ~400元 (~¥400) |
| PolarDB | 4核16GB + 存储 (4C16G + Storage) | ~800元 (~¥800) |
| OSS | 500GB存储 + 流量 (500GB + Traffic) | ~200元 (~¥200) |
| ALB | LCU计费 (LCU billing) | ~100元 (~¥100) |
| CDN | 1TB流量 (1TB traffic) | ~150元 (~¥150) |
| **合计 (Total)** | - | **~1650元/月 (~¥1650/month)** |

> 注 (Note): 实际费用根据业务流量和配置调整，新用户可享受免费试用和折扣。(Actual costs vary based on traffic and configuration. New users can enjoy free trials and discounts.)

## 五、部署步骤 (Deployment Steps)

1. **创建VPC网络 (Create VPC Network)**，规划子网 (Plan subnets)
2. **创建PolarDB (Create PolarDB)**数据库，初始化数据 (Initialize database)
3. **创建ECS实例 (Create ECS Instances)**，部署应用代码 (Deploy application code)
4. **配置ALB (Configure ALB)**，添加后端服务器 (Add backend servers)
5. **开通OSS (Enable OSS)**，配置CDN加速 (Configure CDN acceleration)
6. **配置WAF (Configure WAF)**，添加防护规则 (Add protection rules)
7. **配置监控告警 (Configure Monitoring)**，确保服务稳定 (Ensure service stability)

## 六、相关文档 (Related Documentation)
- [ECS快速入门 (ECS Quick Start)](https://help.aliyun.com/zh/ecs/getting-started/)
- [PolarDB最佳实践 (PolarDB Best Practices)](https://help.aliyun.com/zh/polardb/polardb-for-mysql/best-practices/)
- [电商解决方案 (E-commerce Solution)](https://www.aliyun.com/solution/ecommerce/)
```

---

## 使用建议 (Usage Recommendations)

1. **单产品查询 (Single Product Query)**: 按照 Step 1-7 完整流程，获取全面的产品信息 (Follow the complete Step 1-7 process to get comprehensive product information)
2. **产品对比 (Product Comparison)**: 使用对比模板，突出核心差异，帮助用户决策 (Use comparison templates to highlight key differences and help users make decisions)
3. **方案推荐 (Solution Recommendation)**: 结合业务场景，提供多产品组合方案 (Provide multi-product combination solutions based on business scenarios)
4. **信息时效 (Information Timeliness)**: 价格信息变化较快，建议引导用户查看官网实时价格 (Price information changes frequently, guide users to check real-time prices on official website)
5. **补充链接 (Supplementary Links)**: 始终提供官方文档链接，方便用户获取最新信息 (Always provide official documentation links for users to get the latest information)
