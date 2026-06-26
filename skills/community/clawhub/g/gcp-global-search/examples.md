# Google Cloud Product Query Examples | 谷歌云产品查询示例

This document provides practical examples demonstrating how to use the Google Cloud Product Query Skill to retrieve comprehensive product information from official sources.

本文档提供实用示例，演示如何使用谷歌云产品查询技能从官方渠道获取全面的产品信息。

---

## Example 1: Single Product Query - Compute Engine | 示例1：单个产品查询 - Compute Engine

### User Query | 用户查询
"请帮我查询Google Cloud Compute Engine的详细信息，包括规格、定价和快速入门指南。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **产品名称 (Product Name)**: Compute Engine | Compute Engine
- **产品类别 (Category)**: 计算 (Compute) > 虚拟机计算 (Virtual Machine Compute)
- **产品代码 (Product Code)**: compute
- **官方URL**: https://cloud.google.com/compute

#### Step 2: Construct Search Queries | 构建搜索查询
```
site:cloud.google.com Compute Engine product
site:cloud.google.com/docs Compute Engine overview
site:cloud.google.com/docs Compute Engine machine-types
site:cloud.google.com Compute Engine pricing
site:cloud.google.com/docs Compute Engine quickstart
site:cloud.google.com/docs Compute Engine api
```

#### Step 3: Retrieve Product Information | 获取产品信息

**Product Homepage | 产品首页**:
- URL: https://cloud.google.com/compute
- Use `Browser Navigate` to visit and extract core information

**Key Information Extracted | 提取的关键信息**:
- **产品标语 (Tagline)**: 在Google的基础设施上运行虚拟机，提供可扩展的高性能计算
- **核心功能 (Core Features)**: 自定义机器类型、抢占式虚拟机、全球负载均衡、自动扩展
- **机器类型 (Machine Types)**: 通用型、计算优化型、内存优化型、加速器优化型
- **计费方式 (Billing)**: 按秒计费、承诺使用折扣、抢占式实例折扣

#### Step 4: Retrieve Documentation | 获取技术文档

**Documentation URLs | 文档链接**:
- 产品概览: https://cloud.google.com/compute/docs/overview
- 机器类型: https://cloud.google.com/compute/docs/machine-types
- 定价: https://cloud.google.com/compute/pricing
- 快速入门: https://cloud.google.com/compute/docs/quickstart-linux

#### Step 5-7: Present Results | 呈现结果

```markdown
# Compute Engine | 计算引擎

## 产品概述 (Product Overview)

**产品标语 (Tagline)**: 
在Google的基础设施上运行虚拟机，提供可扩展的高性能计算
/ Run VMs on Google's infrastructure with scalable, high-performance computing

**产品描述 (Description)**:
Compute Engine是Google Cloud的虚拟机计算服务，让您可以在Google的全球基础设施上创建和运行虚拟机。它提供可扩展的高性能虚拟机，支持自定义机器类型，按秒计费，并提供全球负载均衡和自动扩展功能。

Compute Engine is Google Cloud's virtual machine computing service that lets you create and run VMs on Google's global infrastructure. It provides scalable, high-performance VMs with custom machine types, per-second billing, and global load balancing with autoscaling.

**核心功能 (Core Features)**:
- **自定义机器类型 (Custom Machine Types)**: 根据工作负载需求自定义vCPU和内存配置
  / Customize vCPU and memory configurations based on workload requirements
- **抢占式虚拟机 (Preemptible VMs)**: 价格最高可节省91%，适合可中断的工作负载
  / Save up to 91% on costs for interruptible workloads
- **全球负载均衡 (Global Load Balancing)**: 自动将流量分发到全球多个区域
  / Automatically distribute traffic across multiple global regions
- **自动扩展 (Autoscaling)**: 根据负载自动调整实例数量
  / Automatically adjust instance count based on load
- **实时迁移 (Live Migration)**: 在维护期间保持VM运行
  / Keep VMs running during maintenance
- **持续使用折扣 (Sustained Use Discounts)**: 自动为持续运行的VM提供折扣
  / Automatic discounts for VMs that run for significant portions of the month

**应用场景 (Use Cases)**:
1. **通用工作负载 (General Workloads)**: Web服务器、应用服务器、开发环境
   / Web servers, application servers, development environments
2. **高性能计算 (High-Performance Computing)**: 科学计算、金融建模、仿真
   / Scientific computing, financial modeling, simulations
3. **机器学习训练 (ML Training)**: 使用GPU实例训练AI/ML模型
   / Train AI/ML models using GPU instances
4. **批处理作业 (Batch Processing)**: 使用抢占式VM处理大规模数据
   / Process large-scale data using preemptible VMs

---

## 产品规格 (Specifications)

### 机器类型 (Machine Types)
| 类型系列 (Family) | 类型 (Type) | 描述 (Description) | 适用场景 (Use Case) |
|------------------|------------|-------------------|-------------------|
| E2 (通用型) | e2-standard | 性价比优化的通用型 | Web服务器、小型数据库 |
| N2 (通用型) | n2-standard | 平衡的性价比 | 企业应用、中型数据库 |
| N2D (通用型) | n2d-standard | AMD EPYC处理器 | 通用计算工作负载 |
| C2 (计算优化型) | c2-standard | 高每核性能 | HPC、游戏服务器 |
| C2D (计算优化型) | c2d-standard | AMD计算优化 | 计算密集型工作负载 |
| M1/M2/M3 (内存优化型) | m3-ultramem | 最高内存配置 | 内存数据库、SAP HANA |
| A2 (加速器优化型) | a2-highgpu | NVIDIA A100 GPU | ML训练、科学计算 |
| G2 (加速器优化型) | g2-standard | NVIDIA L4 GPU | 图形渲染、视频转码 |

### 通用型机器规格示例 (General-Purpose Machine Examples)
| 机器类型 | vCPU | 内存 | 适用场景 |
|---------|------|------|---------|
| e2-medium | 2 | 4 GB | 开发/测试 |
| e2-standard-4 | 4 | 16 GB | 小型应用 |
| n2-standard-8 | 8 | 32 GB | 中型应用 |
| n2-standard-16 | 16 | 64 GB | 大型应用 |

### 支持区域 (Supported Regions)
- us-central1 (爱荷华) | us-central1
- us-east1 (南卡罗来纳) | us-east1
- us-west1 (俄勒冈) | us-west1
- europe-west1 (比利时) | europe-west1
- europe-west4 (荷兰) | europe-west4
- asia-east1 (台湾) | asia-east1
- asia-northeast1 (东京) | asia-northeast1
- asia-southeast1 (新加坡) | asia-southeast1

---

## 定价信息 (Pricing)

### 计费模式 (Billing Models)
- **按秒计费 (Per-Second Billing)**: 最少1分钟，按实际使用时间计费
  / Minimum 1 minute, billed for actual usage time
- **持续使用折扣 (Sustained Use Discounts)**: 自动为长时间运行的VM提供最高30%折扣
  / Up to 30% automatic discount for VMs running significant portions of the month
- **承诺使用折扣 (Committed Use Discounts)**: 1年或3年承诺，最高可节省57%
  / 1 or 3-year commitments with up to 57% savings
- **抢占式实例 (Preemptible VMs)**: 最高可节省91%，但可能被中断
  / Up to 91% savings with potential interruption

### 价格示例 (Price Examples) - 美国区域
| 机器类型 | vCPU | 内存 | 按需价格/小时 | 1年承诺价格/小时 |
|---------|------|------|-------------|----------------|
| e2-medium | 2 | 4 GB | $0.033 | $0.021 |
| e2-standard-4 | 4 | 16 GB | $0.134 | $0.085 |
| n2-standard-8 | 8 | 32 GB | $0.388 | $0.246 |
| n2-standard-16 | 16 | 64 GB | $0.776 | $0.492 |
| c2-standard-4 | 4 | 16 GB | $0.209 | $0.132 |

### 成本优化建议 (Cost Optimization Tips)
1. 长期稳定工作负载使用承诺使用折扣
2. 可中断批处理作业使用抢占式实例
3. 为开发/测试环境使用E2机器类型
4. 启用自动扩展避免过度配置
5. 使用自定义机器类型避免资源浪费

---

## 快速入门 (Quick Start)

### 前提条件 (Prerequisites)
- Google Cloud账号已创建
- 已创建Google Cloud项目
- 已启用Compute Engine API
- 已安装Google Cloud SDK (可选)

### 创建VM实例 (Create VM Instance)

**通过控制台 (Via Console)**:
1. 打开Google Cloud Console
2. 导航至 Compute Engine > VM 实例
3. 点击"创建实例"
4. 配置机器类型、启动磁盘、防火墙规则
5. 点击"创建"

**通过gcloud CLI (Via gcloud CLI)**:
```bash
# 设置项目
gcloud config set project <project-id>

# 创建实例
gcloud compute instances create my-instance \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=10GB \
  --zone=us-central1-a
```

**通过Python API (Via Python API)**:
```python
from google.cloud import compute_v1

# 创建客户端
client = compute_v1.InstancesClient()

# 定义实例配置
instance = compute_v1.Instance(
    name="my-instance",
    machine_type="zones/us-central1-a/machineTypes/e2-medium",
    disks=[
        compute_v1.AttachedDisk(
            boot=True,
            auto_delete=True,
            initialize_params=compute_v1.AttachedDiskInitializeParams(
                source_image="projects/debian-cloud/global/images/family/debian-11",
                disk_size_gb=10
            )
        )
    ],
    network_interfaces=[
        compute_v1.NetworkInterface(
            network="global/networks/default",
            access_configs=[
                compute_v1.AccessConfig(
                    name="External NAT",
                    type_="ONE_TO_ONE_NAT"
                )
            ]
        )
    ]
)

# 创建实例
operation = client.insert(
    project="<project-id>",
    zone="us-central1-a",
    instance_resource=instance
)
print(f"实例创建中: {operation.name}")
```

### 连接实例 (Connect to Instance)
- **Linux/macOS**: 使用gcloud命令
  ```bash
  gcloud compute ssh my-instance --zone=us-central1-a
  ```
- **Windows**: 使用Cloud Console浏览器SSH或PuTTY

---

## 开发参考 (Development Reference)

### API 概览 (API Overview)
**API端点 (API Endpoint)**: `https://compute.googleapis.com/compute/v1`

**常用操作 (Common Operations)**:
| 操作 (Operation) | API方法 | 描述 (Description) |
|-----------------|--------|-------------------|
| 创建实例 | instances.insert | 创建新的VM实例 |
| 查询实例 | instances.get | 获取实例详情 |
| 列出实例 | instances.list | 列出项目中的所有实例 |
| 启动实例 | instances.start | 启动已停止的实例 |
| 停止实例 | instances.stop | 停止运行中的实例 |
| 删除实例 | instances.delete | 删除实例 |
| 设置标签 | instances.setLabels | 为实例添加标签 |

### SDK 支持 (SDK Support)
- **Python**: `google-cloud-compute`
- **Java**: `google-cloud-compute`
- **Go**: `cloud.google.com/go/compute`
- **Node.js**: `@google-cloud/compute`

### gcloud CLI 示例 (gcloud CLI Example)
```bash
# 配置认证
gcloud auth login

# 列出所有实例
gcloud compute instances list

# 创建实例
gcloud compute instances create my-vm \
  --machine-type=e2-standard-4 \
  --zone=us-central1-a

# 停止实例
gcloud compute instances stop my-vm --zone=us-central1-a

# 删除实例
gcloud compute instances delete my-vm --zone=us-central1-a
```

---

## 相关资源 (Related Resources)

### 文档链接 (Documentation Links)
- [Compute Engine文档](https://cloud.google.com/compute/docs)
- [机器类型](https://cloud.google.com/compute/docs/machine-types)
- [定价详情](https://cloud.google.com/compute/pricing)
- [API参考](https://cloud.google.com/compute/docs/reference/rest/v1)

### 相关产品 (Related Products)
- **Persistent Disk**: 高性能块存储
- **Cloud Load Balancing**: 全球负载均衡
- **Cloud CDN**: 内容分发网络
- **Cloud Monitoring**: 实例监控告警
- **Autoscaler**: 自动容量调整
```

---

## Example 2: Product Comparison - Cloud SQL vs Cloud Spanner | 示例2：产品对比 - Cloud SQL vs Cloud Spanner

### User Query | 用户查询
"Google Cloud的Cloud SQL和Cloud Spanner有什么区别？我应该选择哪个？"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Products | 识别产品
- **产品A**: Cloud SQL | Cloud SQL
- **产品B**: Cloud Spanner | Cloud Spanner
- **类别**: 数据库 (Database) > 关系型数据库 (Relational Database)

#### Step 2: Construct Comparison Queries | 构建对比查询
```
site:cloud.google.com Cloud SQL overview
site:cloud.google.com Cloud Spanner overview
site:cloud.google.com/docs Cloud SQL features
site:cloud.google.com/docs Cloud Spanner features
```

#### Step 3-7: Present Comparison Results | 呈现对比结果

```markdown
# Cloud SQL vs Cloud Spanner | 产品对比

## 概览对比 (Overview Comparison)

| 对比项 (Aspect) | Cloud SQL | Cloud Spanner |
|----------------|-----------|---------------|
| **架构 (Architecture)** | 单区域或主从复制 | 全球分布式、水平扩展 |
| **目标负载 (Target Workload)** | 中小规模、区域级应用 | 大规模、全球级应用 |
| **MySQL/PostgreSQL兼容性 (Compatibility)** | 100%兼容 | PostgreSQL方言兼容 |
| **最大存储 (Max Storage)** | 64 TB (PostgreSQL) | 无限制 |
| **扩展方式 (Scaling)** | 垂直扩展（升级实例） | 水平扩展（添加节点） |
| **高可用性 (High Availability)** | 区域高可用 | 全球高可用（99.999%） |

## 详细对比 (Detailed Comparison)

### 1. 架构差异 (Architecture Differences)

**Cloud SQL**:
- 托管的单区域或主从数据库
- 支持MySQL、PostgreSQL、SQL Server
- 垂直扩展（升级实例规格）
- 区域级高可用性配置
- 自动备份和故障转移

**Cloud Spanner**:
- 全球分布式关系型数据库
- 水平扩展（添加节点）
- 同步多副本复制
- 全球事务一致性（TrueTime）
- 自动分片和负载均衡

### 2. 性能与扩展性 (Performance & Scalability)

| 特性 (Feature) | Cloud SQL | Cloud Spanner |
|---------------|-----------|---------------|
| 计算扩展 | 垂直扩展 | 水平扩展 |
| 存储扩展 | 最大64TB | 无限制 |
| 读扩展 | 只读副本 | 自动多区域读取 |
| 写扩展 | 单主写入 | 多区域并发写入 |
| 最大连接数 | 取决于实例规格 | 100,000+ |
| 延迟 | 毫秒级 | 毫秒级（全球） |

### 3. 适用场景 (Use Cases)

**选择 Cloud SQL 的场景 (Choose Cloud SQL when)**:
- 中小规模应用（TB级数据）
- 区域级部署需求
- 需要100% MySQL/PostgreSQL/SQL Server兼容性
- 成本敏感的场景
- 传统应用迁移

**选择 Cloud Spanner 的场景 (Choose Cloud Spanner when)**:
- 大规模应用（PB级数据）
- 全球分布式部署需求
- 需要全球事务一致性
- 高并发读写场景
- 需要99.999%可用性

### 4. 定价对比 (Pricing Comparison)

| 组件 (Component) | Cloud SQL | Cloud Spanner |
|-----------------|-----------|---------------|
| 计算 | 按实例规格计费 | 按节点计费（1-1000节点） |
| 存储 | 按GB计费 | 按GB计费 |
| 备份存储 | 额外计费 | 包含在存储中 |
| 网络出口 | 按GB计费 | 按GB计费 |
| 最低成本 | 较低（共享核心起） | 较高（最少3个节点） |

### 5. 管理复杂度 (Management Complexity)

| 方面 (Aspect) | Cloud SQL | Cloud Spanner |
|--------------|-----------|---------------|
| 部署 | 简单（选择版本和规格） | 简单（选择节点数） |
| 备份 | 自动或手动配置 | 自动（版本控制） |
| 监控 | Cloud Monitoring集成 | Cloud Monitoring集成 |
| 维护 | 自动维护窗口 | 零停机维护 |
| 扩展 | 手动或自动垂直扩展 | 自动水平扩展 |

## 选择建议 (Recommendation)

### 初创/小企业 (Startups/Small Business)
**推荐**: Cloud SQL
- 初始成本较低
- 管理更简单
- 满足中等负载需求
- 熟悉的SQL体验

### 企业/高增长业务 (Enterprises/High Growth)
**推荐**: Cloud Spanner
- 面向未来的架构
- 自动全球扩展
- 大规模时成本效益更好
- 更高可用性

### 迁移路径 (Migration Path)
Google Cloud提供从Cloud SQL到Cloud Spanner的迁移路径：
1. 使用Database Migration Service进行在线迁移
2. 数据同步，最小化停机时间
3. 使用HarbourBridge工具评估兼容性
```

---

## Example 3: Pricing Analysis - Cloud Storage | 示例3：定价分析 - Cloud Storage

### User Query | 用户查询
"我想了解Google Cloud Storage的定价详情，包括存储费用、流量费用和请求费用。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **产品名称**: Cloud Storage | Cloud Storage
- **产品代码**: storage
- **类别**: 存储 (Storage)

#### Step 2: Construct Pricing Queries | 构建定价查询
```
site:cloud.google.com Cloud Storage pricing
site:cloud.google.com/docs Cloud Storage pricing
site:cloud.google.com Cloud Storage free tier
```

#### Step 3-7: Present Pricing Analysis | 呈现定价分析

```markdown
# Cloud Storage 定价分析 | Cloud Storage Pricing Analysis

## 计费组成 (Pricing Components)

Cloud Storage定价由四个主要部分组成：
Google Cloud Storage pricing consists of four main components:

### 1. 存储容量费用 (Storage Fees)
根据存储类型和实际使用量计费
Billed based on storage class and actual storage usage

| 存储类型 (Storage Class) | 中文名称 | 价格 (美元/GB/月) | 适用场景 (Use Case) |
|------------------------|---------|------------------|-------------------|
| Standard | 标准存储 | $0.020 | 频繁访问的数据 |
| Nearline | 近线存储 | $0.010 | 每月访问少于一次的数据 |
| Coldline | 冷线存储 | $0.004 | 每季度访问一次的数据 |
| Archive | 归档存储 | $0.0012 | 每年访问少于一次的数据 |
| Autoclass | 自动分类 | $0.023 | 自动优化存储类别 |

### 2. 流量费用 (Network Fees)
出站流量计费
Billed for outbound data transfer

| 流量类型 (Traffic Type) | 中文名称 | 价格 (美元/GB) |
|------------------------|---------|---------------|
| 出站流量 - 北美 | Egress - North America | $0.12 |
| 出站流量 - 欧洲 | Egress - Europe | $0.12 |
| 出站流量 - 亚太 | Egress - Asia Pacific | $0.12 |
| 出站流量 - 中国 | Egress - China | $0.23 |
| 出站流量 - 澳大利亚 | Egress - Australia | $0.19 |
| 同区域访问 | Same Region Access | 免费 |
| 跨区域访问 | Cross-Region Access | $0.01 |

**注意**: 入站流量免费 / Inbound traffic is free

### 3. 操作费用 (Operation Fees)
按每万次操作计费
Billed per 10,000 operations

| 操作类型 (Operation Type) | 标准存储 | 近线存储 | 冷线存储 | 归档存储 |
|--------------------------|---------|---------|---------|---------|
| Class A操作 (插入、复制) | $0.005 | $0.01 | $0.02 | $0.05 |
| Class B操作 (获取、列表) | $0.0004 | $0.001 | $0.002 | $0.005 |
| 删除操作 | 免费 | 免费 | 免费 | 免费 |

### 4. 数据检索费用 (Data Retrieval Fees)

| 存储类型 | 检索费用 |
|---------|---------|
| Standard | 免费 |
| Nearline | $0.01/GB |
| Coldline | $0.02/GB |
| Archive | $0.05/GB |

### 5. 早期删除费用 (Early Deletion Fees)

| 存储类型 | 最短存储期限 | 提前删除费用 |
|---------|-------------|-------------|
| Nearline | 30天 | 剩余天数费用 |
| Coldline | 90天 | 剩余天数费用 |
| Archive | 365天 | 剩余天数费用 |

---

## 成本计算示例 (Cost Calculation Example)

### 场景 (Scenario)
- 存储容量: 10 TB 标准存储
- 每月出站流量: 5 TB
- 每月Class A操作: 100万次
- 每月Class B操作: 1000万次

### 计算 (Calculation)

| 计费项 | 计算公式 | 费用 |
|-------|---------|------|
| 存储费用 | 10,000 GB × $0.020 | $200 |
| 流量费用 | 5,000 GB × $0.12 | $600 |
| Class A操作 | 100万 ÷ 1万 × $0.005 | $0.50 |
| Class B操作 | 1000万 ÷ 1万 × $0.0004 | $4 |
| **月度总计** | | **$804.50** |

---

## 成本优化策略 (Cost Optimization Strategies)

### 1. 存储类型优化 (Storage Class Optimization)
- 使用对象生命周期管理自动转换对象
- 标准存储 → 近线存储（30天后）
- 近线存储 → 冷线存储（90天后）
- 冷线存储 → 归档存储（1年后）
- 潜在节省: 70-95%

### 2. 流量优化 (Traffic Optimization)
- 使用Cloud CDN分发内容（减少源站流量）
- 启用传输压缩
- 同区域访问优先

### 3. 操作优化 (Operation Optimization)
- 批量操作减少请求次数
- 大文件使用分片上传
- 实现客户端缓存

### 4. 免费额度利用 (Free Tier Utilization)
Google Cloud为新用户提供免费额度：
- 标准存储: 5 GB/月免费
- 出站流量: 1 GB/月免费
- Class A操作: 5,000次/月免费
- Class B操作: 50,000次/月免费

---

## 定价计算器 (Pricing Calculator)

使用官方定价计算器获取准确估算：
[Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)

详细定价请参考：
[Cloud Storage Pricing](https://cloud.google.com/storage/pricing)
```

---

## Example 4: API Integration - Creating GKE Cluster | 示例4：API集成 - 创建GKE集群

### User Query | 用户查询
"我需要使用API创建Google Kubernetes Engine (GKE)集群，请提供完整的代码示例。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **产品名称**: Google Kubernetes Engine | GKE
- **产品代码**: kubernetes-engine
- **类别**: 容器与中间件 (Container & Middleware)

#### Step 2: Construct API Documentation Queries | 构建API文档查询
```
site:cloud.google.com/kubernetes-engine/docs create-cluster
site:cloud.google.com/kubernetes-engine/docs api
site:cloud.google.com/kubernetes-engine/docs client-libraries
```

#### Step 3-7: Present API Integration Guide | 呈现API集成指南

```markdown
# GKE API 集成指南 | GKE API Integration Guide

## 前提条件 (Prerequisites)

1. Google Cloud账号并启用Kubernetes Engine API
2. 已配置服务账号密钥或Application Default Credentials
3. 已创建VPC网络（可选，可使用默认网络）
4. 具备container.clusters.create权限

## API 概览 (API Overview)

**API端点 (API Endpoint)**: `https://container.googleapis.com/v1`

**认证方式 (Authentication)**:
- OAuth 2.0
- 服务账号密钥
- Application Default Credentials

## 代码示例 (Code Examples)

### Python SDK 示例 (Python SDK Example)

```python
from google.cloud import container_v1
from google.oauth2 import service_account

# 使用服务账号认证（可选，也可使用ADC）
credentials = service_account.Credentials.from_service_account_file(
    '<service-account-key-file>.json'
)

# 创建客户端
client = container_v1.ClusterManagerClient(credentials=credentials)

# 项目ID和区域
project_id = "<project-id>"
zone = "us-central1-a"

# 构建集群配置
cluster = container_v1.Cluster(
    name="my-gke-cluster",
    initial_node_count=3,
    node_config=container_v1.NodeConfig(
        machine_type="e2-medium",
        disk_size_gb=100,
        oauth_scopes=[
            "https://www.googleapis.com/auth/cloud-platform"
        ]
    ),
    release_channel=container_v1.ReleaseChannel(
        channel=container_v1.ReleaseChannel.Channel.REGULAR
    ),
    network="default",
    addons_config=container_v1.AddonsConfig(
        http_load_balancing=container_v1.HttpLoadBalancing(
            disabled=False
        ),
        horizontal_pod_autoscaling=container_v1.HorizontalPodAutoscaling(
            disabled=False
        )
    )
)

# 创建集群请求
request = container_v1.CreateClusterRequest(
    parent=f"projects/{project_id}/locations/{zone}",
    cluster=cluster
)

# 创建集群
operation = client.create_cluster(request)
print(f"集群创建中，操作ID: {operation.name}")

# 等待操作完成（可选）
import time
def wait_for_operation(client, operation_name):
    while True:
        op = client.get_operation(
            name=operation_name
        )
        if op.status == container_v1.Operation.Status.DONE:
            if op.error:
                print(f"操作失败: {op.error}")
            else:
                print("集群创建成功!")
            break
        print("等待操作完成...")
        time.sleep(10)

wait_for_operation(client, operation.name)
```

### Java SDK 示例 (Java SDK Example)

```java
import com.google.cloud.container.v1.ClusterManagerClient;
import com.google.container.v1.Cluster;
import com.google.container.v1.NodeConfig;
import com.google.container.v1.CreateClusterRequest;
import com.google.container.v1.ReleaseChannel;
import com.google.container.v1.AddonsConfig;
import com.google.container.v1.HttpLoadBalancing;
import com.google.container.v1.HorizontalPodAutoscaling;

public class GKEClusterCreator {
    public static void main(String[] args) throws Exception {
        // 创建客户端
        try (ClusterManagerClient client = ClusterManagerClient.create()) {
            String projectId = "<project-id>";
            String zone = "us-central1-a";
            String parent = String.format("projects/%s/locations/%s", projectId, zone);

            // 构建节点配置
            NodeConfig nodeConfig = NodeConfig.newBuilder()
                .setMachineType("e2-medium")
                .setDiskSizeGb(100)
                .addOauthScopes("https://www.googleapis.com/auth/cloud-platform")
                .build();

            // 构建发布通道
            ReleaseChannel releaseChannel = ReleaseChannel.newBuilder()
                .setChannel(ReleaseChannel.Channel.REGULAR)
                .build();

            // 构建插件配置
            AddonsConfig addonsConfig = AddonsConfig.newBuilder()
                .setHttpLoadBalancing(HttpLoadBalancing.newBuilder().setDisabled(false))
                .setHorizontalPodAutoscaling(HorizontalPodAutoscaling.newBuilder().setDisabled(false))
                .build();

            // 构建集群
            Cluster cluster = Cluster.newBuilder()
                .setName("my-gke-cluster")
                .setInitialNodeCount(3)
                .setNodeConfig(nodeConfig)
                .setReleaseChannel(releaseChannel)
                .setNetwork("default")
                .setAddonsConfig(addonsConfig)
                .build();

            // 创建请求
            CreateClusterRequest request = CreateClusterRequest.newBuilder()
                .setParent(parent)
                .setCluster(cluster)
                .build();

            // 创建集群
            var operation = client.createCluster(request);
            System.out.println("集群创建中，操作ID: " + operation.getName());
        }
    }
}
```

### Go SDK 示例 (Go SDK Example)

```go
package main

import (
    "context"
    "fmt"
    "log"

    container "cloud.google.com/go/container/apiv1"
    "cloud.google.com/go/container/apiv1/containerpb"
    "google.golang.org/api/option"
)

func main() {
    ctx := context.Background()

    // 创建客户端（使用ADC）
    client, err := container.NewClusterManagerClient(ctx)
    if err != nil {
        log.Fatalf("创建客户端失败: %v", err)
    }
    defer client.Close()

    projectID := "<project-id>"
    zone := "us-central1-a"
    parent := fmt.Sprintf("projects/%s/locations/%s", projectID, zone)

    // 构建集群请求
    req := &containerpb.CreateClusterRequest{
        Parent: parent,
        Cluster: &containerpb.Cluster{
            Name:             "my-gke-cluster",
            InitialNodeCount: 3,
            NodeConfig: &containerpb.NodeConfig{
                MachineType: "e2-medium",
                DiskSizeGb:  100,
                OauthScopes: []string{
                    "https://www.googleapis.com/auth/cloud-platform",
                },
            },
            ReleaseChannel: &containerpb.ReleaseChannel{
                Channel: containerpb.ReleaseChannel_REGULAR,
            },
            Network: "default",
            AddonsConfig: &containerpb.AddonsConfig{
                HttpLoadBalancing: &containerpb.HttpLoadBalancing{
                    Disabled: false,
                },
                HorizontalPodAutoscaling: &containerpb.HorizontalPodAutoscaling{
                    Disabled: false,
                },
            },
        },
    }

    // 创建集群
    op, err := client.CreateCluster(ctx, req)
    if err != nil {
        log.Fatalf("创建集群失败: %v", err)
    }

    fmt.Printf("集群创建中，操作ID: %s\n", op.Name)
}
```

### gcloud CLI 示例 (gcloud CLI Example)

```bash
# 设置项目
gcloud config set project <project-id>

# 创建标准GKE集群
gcloud container clusters create my-gke-cluster \
  --zone=us-central1-a \
  --num-nodes=3 \
  --machine-type=e2-medium \
  --disk-size=100GB \
  --release-channel=regular \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10 \
  --enable-autorepair \
  --enable-autoupgrade

# 获取集群凭证
gcloud container clusters get-credentials my-gke-cluster \
  --zone=us-central1-a

# 验证连接
kubectl get nodes
```

### Terraform 示例 (Terraform Example)

```hcl
provider "google" {
  project = "<project-id>"
  region  = "us-central1"
}

resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  location = "us-central1-a"

  # 使用Autopilot模式（可选）
  enable_autopilot = false

  # 移除默认节点池
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"

  release_channel {
    channel = "REGULAR"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "my-node-pool"
  location   = "us-central1-a"
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 100
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}
```

## 常用操作 (Common Operations)

| 操作 (Operation) | gcloud命令 | 描述 (Description) |
|-----------------|------------|-------------------|
| 创建集群 | gcloud container clusters create | 创建新的GKE集群 |
| 列出集群 | gcloud container clusters list | 列出所有集群 |
| 获取凭证 | gcloud container clusters get-credentials | 配置kubectl访问 |
| 删除集群 | gcloud container clusters delete | 删除集群及资源 |
| 创建节点池 | gcloud container node-pools create | 添加节点池 |
| 调整节点池 | gcloud container clusters resize | 调整节点池大小 |

## 错误处理 (Error Handling)

常见错误代码及解决方案：

| 错误代码 | 描述 | 解决方案 |
|---------|------|---------|
| ALREADY_EXISTS | 集群已存在 | 使用不同的集群名称或删除现有集群 |
| INVALID_ARGUMENT | 参数无效 | 检查机器类型、区域等参数 |
| PERMISSION_DENIED | 权限不足 | 检查IAM权限和API启用状态 |
| RESOURCE_EXHAUSTED | 配额不足 | 申请配额提升或减少资源请求 |
| INSUFFICIENT_QUOTA | 区域配额不足 | 选择其他区域或申请配额 |

## 相关资源 (Related Resources)

- [GKE产品文档](https://cloud.google.com/kubernetes-engine/docs)
- [GKE API参考](https://cloud.google.com/kubernetes-engine/docs/reference/rest)
- [GKE最佳实践](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [GKE定价](https://cloud.google.com/kubernetes-engine/pricing)
```

---

## Example 5: Architecture Recommendation - Serverless Web Application | 示例5：架构推荐 - 无服务器Web应用

### User Query | 用户查询
"我需要为Web应用设计一个基于Google Cloud的无服务器架构，包括前端、后端、数据库和API。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Required Products | 识别所需产品
分析Web应用需求并映射到Google Cloud产品：
- **前端**: Firebase Hosting + Cloud CDN
- **后端**: Cloud Run / Cloud Functions
- **API**: API Gateway / Cloud Endpoints
- **数据库**: Firestore / Cloud SQL
- **认证**: Firebase Authentication / Cloud IAM
- **存储**: Cloud Storage
- **监控**: Cloud Monitoring + Cloud Logging

#### Step 2: Research Each Product | 调研每个产品
对每个识别出的产品执行查询，收集规格和集成模式。

#### Step 3-7: Present Architecture Recommendation | 呈现架构推荐

```markdown
# Google Cloud 无服务器Web应用架构 | Serverless Web Application Architecture on Google Cloud

## 架构概览 (Architecture Overview)

本架构使用Google Cloud无服务器服务构建可扩展、高可用的Web应用。
This architecture provides a scalable, high-availability web application using Google Cloud serverless services.

```
                    [用户 Users]
                        |
                        v
                [Cloud CDN + Firebase Hosting]
                        |
                        v
                [Cloud Armor (WAF)]
                        |
                        v
                [Cloud Load Balancing]
                        |
        +----------------+----------------+
        |                                 |
        v                                 v
[静态资源]                        [API Gateway]
(Firebase Hosting)                     |
                                       v
                              [Cloud Run / Cloud Functions]
                                       |
                    +------------------+------------------+
                    |                                     |
                    v                                     v
           [Firestore]                           [Cloud Storage]
           (用户数据)                              (文件存储)
                    |                                     |
                    v                                     v
           [Firebase Authentication]            [Cloud CDN]
           (用户认证)
```

## 组件详情 (Component Details)

### 1. 前端托管 (Frontend Hosting)

**产品**: Firebase Hosting + Cloud CDN

**配置**:
- Firebase Hosting用于静态Web应用托管
- Cloud CDN加速全球内容分发
- 自动SSL证书管理
- 自定义域名支持
- 原子部署和回滚

**定价估算**:
- Firebase Hosting: 免费额度10GB/月，超出$0.15/GB
- Cloud CDN: $0.08-0.20/GB（取决于区域）

### 2. 安全层 (Security Layer)

**产品**: Cloud Armor + Firebase Authentication

**配置**:
- Cloud Armor防护DDoS攻击和SQL注入
- OWASP Top 10防护规则
- Firebase Authentication提供用户认证
- 支持Google、Facebook、Email等多种登录方式
- JWT令牌验证

**定价估算**:
- Cloud Armor: $5/策略/月 + $0.75/百万请求
- Firebase Authentication: 免费额度10,000用户/月，超出$0.01/验证

### 3. API网关 (API Gateway)

**产品**: API Gateway

**配置**:
- OpenAPI规范定义API
- 请求路由和转换
- 配额和限流控制
- API密钥管理
- 与Cloud Run/Functions集成

**定价估算**:
- API调用: $3.00/百万次调用

### 4. 计算层 (Compute Layer)

**产品**: Cloud Run

**配置**:
- 无状态容器运行
- 自动扩展（0到N）
- 按请求计费
- 并发请求处理
- 自定义域名和HTTPS

**定价估算**:
- 免费额度: 200万请求/月
- 超出: $0.40/百万请求
- vCPU: $0.00002400/vCPU-秒
- 内存: $0.00000250/GB-秒

### 5. 数据库层 (Database Layer)

**产品**: Cloud Firestore

**配置**:
- 无服务器文档数据库
- 实时同步
- 自动扩展
- 多区域复制
- 离线数据持久化

**定价估算**:
- 免费额度:
  - 50,000次读取/天
  - 20,000次写入/天
  - 20,000次删除/天
  - 1 GB存储
- 超出:
  - 读取: $0.06/10万次
  - 写入: $0.18/10万次
  - 删除: $0.02/10万次
  - 存储: $0.18/GB/月

### 6. 文件存储 (File Storage)

**产品**: Cloud Storage

**配置**:
- 标准存储用于用户上传文件
- 与Cloud CDN集成加速访问
- 签名URL安全访问
- 生命周期策略自动归档

**定价估算**:
- 存储: $0.020/GB/月
- 出站流量: $0.12/GB
- 操作: $0.005/万次

### 7. 监控与日志 (Monitoring & Logging)

**产品**: Cloud Monitoring + Cloud Logging

**配置**:
- 应用性能监控
- 自定义指标和仪表板
- 日志聚合和分析
- 告警通知

**定价估算**:
- Cloud Monitoring: 免费额度100万个指标/月
- Cloud Logging: 免费额度50GB/月

## 成本汇总 (Cost Summary)

### 月度成本估算 - 小型应用 (Monthly Cost Estimate - Small App)

| 组件 | 配置 | 月度费用 |
|-----|------|---------|
| Firebase Hosting | 100GB流量 | $13.50 |
| Cloud CDN | 100GB流量 | $12 |
| Cloud Armor | 1策略 | $5 |
| API Gateway | 100万请求 | $3 |
| Cloud Run | 100万请求 | $0.40 |
| Firestore | 50万读取, 10万写入 | $33 |
| Cloud Storage | 50GB + 50GB流量 | $7 |
| **总计** | | **$73.90/月** |

### 月度成本估算 - 中型应用 (Monthly Cost Estimate - Medium App)

| 组件 | 配置 | 月度费用 |
|-----|------|---------|
| Firebase Hosting | 1TB流量 | $150 |
| Cloud CDN | 1TB流量 | $120 |
| Cloud Armor | 1策略 + 1000万请求 | $12.50 |
| API Gateway | 1000万请求 | $30 |
| Cloud Run | 1000万请求 | $4 |
| Firestore | 500万读取, 100万写入 | $330 |
| Cloud Storage | 500GB + 500GB流量 | $70 |
| **总计** | | **$716.50/月** |

## 扩展考虑 (Scaling Considerations)

### 水平扩展 (Horizontal Scaling)
- Cloud Run自动扩展到数千实例
- Firestore自动处理数百万并发连接
- Cloud CDN全球边缘缓存

### 成本优化 (Cost Optimization)
- 使用Cloud Run的并发处理减少实例数
- Firestore索引优化减少读取次数
- Cloud Storage生命周期策略自动归档旧文件
- 利用所有免费额度

### 高可用性 (High Availability)
- Firestore多区域部署
- Cloud Run全球负载均衡
- Firebase Hosting全球CDN

## 相关产品 (Related Products)

- **Cloud Tasks**: 异步任务处理
- **Pub/Sub**: 事件驱动架构
- **Cloud Scheduler**: 定时任务
- **Secret Manager**: 安全管理API密钥
- **Cloud Build**: CI/CD流水线
```

---

## Summary | 总结

These examples demonstrate the complete workflow of the Google Cloud Product Query Skill:

这些示例演示了谷歌云产品查询技能的完整工作流程：

1. **Single Product Query (单个产品查询)**: Deep dive into one product with full specifications, pricing, and usage guides
2. **Product Comparison (产品对比)**: Side-by-side analysis of similar products for informed decision-making
3. **Pricing Analysis (定价分析)**: Detailed cost breakdown with optimization strategies
4. **API Integration (API集成)**: Complete code examples for programmatic access
5. **Architecture Design (架构设计)**: Multi-product solution architecture with cost estimates

When using this skill, always:
- Use `WebSearch` to find official documentation URLs
- Use `WebFetch` or `Browser Navigate` to retrieve detailed content
- Cross-reference multiple sources for accuracy
- Provide bilingual (Chinese/English) output
- Include credential placeholders in all code examples
