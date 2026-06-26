---
name: azure-global-search
description: Query Microsoft Azure product information, documentation, parameters, features, and pricing from official sources without login. Use when the user asks about Azure products (VMs, Blob Storage, SQL Database, Functions, etc.), needs product documentation, wants to compare product specifications, or needs help finding specific product parameters and features.
---

# Microsoft Azure Product Query | 微软Azure产品查询

This skill helps users find detailed information about Microsoft Azure products by searching official documentation and product pages without requiring login.

本技能帮助用户通过搜索官方文档和产品页面，无需登录即可获取微软Azure产品的详细信息。

## When to Use | 使用场景

- User asks about specific Azure products (VMs, Blob Storage, SQL Database, Functions, etc.) / 用户询问特定的Azure产品（虚拟机、Blob存储、SQL数据库、函数等）
- User needs product documentation or API references / 用户需要产品文档或API参考
- User wants to compare product specifications or pricing / 用户想要比较产品规格或价格
- User needs help finding specific product parameters or features / 用户需要帮助查找特定的产品参数或功能
- User mentions "Azure", "Microsoft Azure", or "微软云" and needs product information / 用户提到"Azure"或"微软云"并需要产品信息

---

## Step 1: Identify the Product | 识别产品

### 1.1 Identify Product Keywords | 识别产品关键词

Analyze user questions and extract:
- **Product Name**: Specific product names (e.g., Virtual Machines, Blob Storage, SQL Database)
- **Product Category**: Product categories (e.g., Compute, Storage, Database)
- **Functional Requirements**: Functions the user wants to implement
- **Use Cases**: User's business scenarios

分析用户问题，提取：
- **产品名称**: 具体产品名（如虚拟机、Blob存储、SQL数据库）
- **产品类别**: 产品类别（如计算、存储、数据库）
- **功能需求**: 用户想要实现的功能
- **使用场景**: 用户的业务场景

### 1.2 Product Alias Reference | 产品别名对照表

| User May Say | Product | English Name |
|-------------|---------|--------------|
| 云服务器、虚拟机、VM (Cloud Server, VM) | Azure Virtual Machines | Virtual Machines |
| 对象存储、云盘 (Object Storage) | Azure Blob Storage | Blob Storage |
| 云硬盘、块存储 (Block Storage) | Azure Disk Storage | Managed Disks |
| 文件存储、NAS (File Storage) | Azure Files | Azure Files |
| 负载均衡 (Load Balancer) | Azure Load Balancer | Load Balancer |
| 数据库、SQL Server (Database) | Azure SQL Database | SQL Database |
| MySQL、PostgreSQL | Azure Database for MySQL/PostgreSQL | Azure Database |
| Redis、缓存 (Cache) | Azure Cache for Redis | Cache for Redis |
| 大模型、AI、机器学习 (AI/ML) | Azure OpenAI / Azure AI | Azure OpenAI Service |
| 容器、K8s、Kubernetes (Container) | AKS | Azure Kubernetes Service |
| 函数计算、Serverless (Function) | Azure Functions | Functions |
| 安全中心 (Security) | Microsoft Defender for Cloud | Defender for Cloud |
| WAF、防火墙 (Firewall) | Azure Firewall | Firewall |
| CDN、加速 (CDN) | Azure CDN / Front Door | Content Delivery Network |
| VNet、私有网络 (VPC) | Azure Virtual Network | Virtual Network |
| 大数据、数仓 (Big Data) | Azure Synapse / HDInsight | Synapse Analytics |
| 消息队列、Event Hub (Message Queue) | Event Hubs / Service Bus | Event Hubs |

### 1.3 Identify Target Product | 确定目标产品

Find the best matching product and record:
- **Chinese Name**: Product name in Chinese
- **English Name**: Product name in English
- **Category**: Product category
- **Service Code**: For constructing URLs

从产品目录中找到最匹配的产品，记录：
- **中文名**: 产品的中文名称
- **英文名**: 产品的英文名称
- **类别**: 产品所属类别
- **服务代码**: 用于构造URL

---

## 📦 Azure Full Product Catalog | Azure全产品目录

### 🤖 一、AI + Machine Learning (人工智能与机器学习)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure AI Foundry | Azure AI Foundry | AI应用和智能体工厂 / The AI app and agent factory |
| Azure OpenAI Service | Azure OpenAI服务 | 访问OpenAI大模型 / Access OpenAI large language models |
| Azure Machine Learning | Azure机器学习 | 构建、训练和部署ML模型 / Build, train, and deploy ML models |
| Azure AI Language | Azure AI语言 | 自然语言处理服务 / Natural language processing |
| Azure AI Speech | Azure AI语音 | 语音识别和合成服务 / Speech recognition and synthesis |
| Azure AI Vision | Azure AI视觉 | 计算机视觉服务 / Computer vision service |
| Azure AI Search | Azure AI搜索 | 企业级搜索服务 / Enterprise search service |
| Azure AI Bot Service | Azure AI机器人服务 | 构建智能聊天机器人 / Build intelligent chatbots |
| Azure AI Content Safety | Azure AI内容安全 | 内容审核和安全服务 / Content moderation and safety |
| Azure AI Document Intelligence | Azure AI文档智能 | 文档分析和处理 / Document analysis and processing |
| Azure AI Translator | Azure AI翻译 | 机器翻译服务 / Machine translation |
| Azure AI Personalizer | Azure AI个性化推荐 | 实时个性化推荐 / Real-time personalization |
| Microsoft Copilot Studio | Copilot Studio | 构建自定义Copilot / Build custom copilots |
| Microsoft Security Copilot | Security Copilot | AI驱动的安全助手 / AI-powered security assistant |

---

### 🖥️ 二、Compute (计算)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Virtual Machines | Azure虚拟机 | 可扩展的计算资源 / Scalable compute resources |
| Azure Spot Virtual Machines | Azure Spot虚拟机 | 低成本的抢占式虚拟机 / Low-cost preemptible VMs |
| Azure Virtual Machine Scale Sets | 虚拟机规模集 | 自动缩放VM集群 / Auto-scaling VM clusters |
| Azure Dedicated Host | Azure专用主机 | 专用物理服务器 / Dedicated physical servers |
| Azure Functions | Azure函数 | 无服务器计算服务 / Serverless compute service |
| Azure Container Instances | Azure容器实例 | 快速启动容器 / Quickly launch containers |
| Azure Container Apps | Azure容器应用 | 无服务器容器应用 / Serverless container apps |
| Azure Spring Apps | Azure Spring应用 | 托管Spring Boot应用 / Managed Spring Boot apps |
| Azure VMware Solution | Azure VMware解决方案 | 在Azure上运行VMware / Run VMware on Azure |
| Azure Compute Fleet | Azure计算舰队 | 大规模计算资源管理 / Large-scale compute management |
| Azure Batch | Azure批处理 | 大规模并行批处理 / Large-scale parallel batch processing |
| Azure App Service | Azure应用服务 | 托管Web应用平台 / Managed web app platform |
| Azure Static Web Apps | Azure静态Web应用 | 全栈静态Web应用 / Full-stack static web apps |
| Azure Virtual Desktop | Azure虚拟桌面 | 云托管虚拟桌面 / Cloud-hosted virtual desktops |

---

### 💾 三、Storage (存储)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Blob Storage | Azure Blob存储 | 大规模对象存储 / Massively scalable object storage |
| Azure Files | Azure文件存储 | 托管文件共享服务 / Managed file shares |
| Azure Disk Storage | Azure磁盘存储 | 高性能块存储 / High-performance block storage |
| Azure Queue Storage | Azure队列存储 | 云消息队列 / Cloud message queuing |
| Azure Table Storage | Azure表存储 | NoSQL键值存储 / NoSQL key-value store |
| Azure Data Lake Storage | Azure Data Lake存储 | 大数据分析存储 / Big data analytics storage |
| Azure Archive Storage | Azure归档存储 | 长期数据归档 / Long-term data archiving |
| Azure Container Storage | Azure容器存储 | 容器持久化存储 / Persistent storage for containers |
| Azure Elastic SAN | Azure弹性SAN | 云原生存储区域网络 / Cloud-native SAN |
| Azure Storage Mover | Azure存储迁移器 | 数据迁移服务 / Data migration service |
| Azure Storage Actions | Azure存储操作 | 大规模存储数据管理 / Large-scale storage data management |
| Storage Accounts | 存储账户 | 统一的存储管理 / Unified storage management |
| Storage Explorer | 存储资源管理器 | 存储管理工具 / Storage management tool |

---

### 🗄️ 四、Databases (数据库)

#### Relational Database (关系型数据库)
| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure SQL Database | Azure SQL数据库 | 托管的智能SQL数据库 / Managed intelligent SQL database |
| Azure SQL Managed Instance | Azure SQL托管实例 | 完全托管的SQL Server / Fully managed SQL Server |
| Azure Database for MySQL | Azure MySQL数据库 | 托管的MySQL数据库 / Managed MySQL database |
| Azure Database for PostgreSQL | Azure PostgreSQL数据库 | 托管的PostgreSQL数据库 / Managed PostgreSQL database |
| Azure SQL Edge | Azure SQL Edge | 边缘计算SQL数据库 / SQL database for edge computing |

#### NoSQL Database (NoSQL数据库)
| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Cosmos DB | Azure Cosmos DB | 全球分布式NoSQL数据库 / Globally distributed NoSQL database |
| Azure Managed Redis | Azure托管Redis | 托管的Redis服务 / Managed Redis service |
| Azure Table Storage | Azure表存储 | 结构化NoSQL数据存储 / Structured NoSQL data storage |

#### Database Tools (数据库工具)
| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Database Migration Service | Azure数据库迁移服务 | 数据库迁移上云 / Migrate databases to Azure |
| Azure Managed Instance for Apache Cassandra | Azure托管Cassandra实例 | 托管的Cassandra服务 / Managed Cassandra service |
| SQL Server on Azure VMs | Azure虚拟机上的SQL Server | 在VM上运行SQL Server / Run SQL Server on VMs |

---

### 🐳 五、Containers (容器)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Kubernetes Service (AKS) | Azure Kubernetes服务 | 托管的Kubernetes服务 / Managed Kubernetes service |
| Azure Container Registry | Azure容器注册表 | 容器镜像仓库 / Container image registry |
| Azure Container Instances | Azure容器实例 | 快速部署容器 / Quickly deploy containers |
| Azure Container Apps | Azure容器应用 | 无服务器容器平台 / Serverless container platform |
| Azure Container Storage | Azure容器存储 | 容器持久化存储 / Persistent storage for containers |
| Azure Kubernetes Fleet Manager | Azure Kubernetes舰队管理器 | 多集群Kubernetes管理 / Multi-cluster Kubernetes management |
| Red Hat OpenShift on Azure | Azure上的Red Hat OpenShift | 企业级Kubernetes平台 / Enterprise Kubernetes platform |
| Azure Service Fabric | Azure Service Fabric | 微服务平台 / Microservices platform |

---

### 🌐 六、Networking (网络)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Virtual Network (VNet) | Azure虚拟网络 | 隔离的虚拟网络环境 / Isolated virtual network |
| Azure Load Balancer | Azure负载均衡器 | 第4层负载均衡 / Layer 4 load balancing |
| Azure Application Gateway | Azure应用程序网关 | 第7层负载均衡 / Layer 7 load balancing |
| Azure Front Door | Azure Front Door | 全球负载均衡和CDN / Global load balancing and CDN |
| Azure CDN | Azure内容分发网络 | 内容分发网络 / Content delivery network |
| Azure Firewall | Azure防火墙 | 托管的防火墙服务 / Managed firewall service |
| Azure VPN Gateway | Azure VPN网关 | 站点到站点VPN / Site-to-site VPN |
| Azure ExpressRoute | Azure ExpressRoute | 专用网络连接 / Dedicated private connectivity |
| Azure DNS | Azure DNS | 域名系统托管 / Domain name system hosting |
| Azure Traffic Manager | Azure流量管理器 | DNS负载均衡 / DNS-based load balancing |
| Azure Bastion | Azure堡垒主机 | 安全的RDP/SSH访问 / Secure RDP/SSH access |
| Azure Network Watcher | Azure网络观察程序 | 网络监控和诊断 / Network monitoring and diagnostics |
| Azure Private Link | Azure专用链接 | 私有访问Azure服务 / Private access to Azure services |
| Azure DDoS Protection | Azure DDoS防护 | DDoS攻击防护 / DDoS attack protection |
| Azure NAT Gateway | Azure NAT网关 | 出站网络地址转换 / Outbound NAT |

---

### 🔒 七、Security (安全)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Microsoft Defender for Cloud | Microsoft Defender for Cloud | 云安全态势管理 / Cloud security posture management |
| Microsoft Sentinel | Microsoft Sentinel | 云原生SIEM和SOAR / Cloud-native SIEM and SOAR |
| Azure Key Vault | Azure密钥保管库 | 密钥和机密管理 / Key and secret management |
| Azure Active Directory / Microsoft Entra ID | Azure Active Directory | 身份和访问管理 / Identity and access management |
| Microsoft Entra Domain Services | Microsoft Entra域服务 | 托管的域控制器 / Managed domain controllers |
| Azure Firewall | Azure防火墙 | 托管的防火墙服务 / Managed firewall service |
| Azure DDoS Protection | Azure DDoS防护 | DDoS攻击防护 / DDoS attack protection |
| Azure Private Link | Azure专用链接 | 安全的私有连接 / Secure private connectivity |
| Azure Confidential Ledger | Azure机密账本 | 托管的区块链服务 / Managed blockchain service |
| Azure Dedicated HSM | Azure专用HSM | 硬件安全模块 / Hardware security modules |
| Azure Policy | Azure策略 | 资源合规性管理 / Resource compliance management |
| Azure Blueprints | Azure蓝图 | 环境部署标准化 / Environment deployment standardization |

---

### 📊 八、Analytics (分析)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Synapse Analytics | Azure Synapse Analytics | 统一的数据分析平台 / Unified analytics platform |
| Azure Databricks | Azure Databricks | Apache Spark分析平台 / Apache Spark analytics platform |
| Azure HDInsight | Azure HDInsight | 托管的Hadoop和Spark / Managed Hadoop and Spark |
| Azure Data Factory | Azure数据工厂 | 数据集成服务 / Data integration service |
| Azure Data Lake Storage | Azure Data Lake存储 | 大数据分析存储 / Big data analytics storage |
| Azure Stream Analytics | Azure流分析 | 实时流处理 / Real-time stream processing |
| Azure Analysis Services | Azure分析服务 | 企业级语义模型 / Enterprise semantic models |
| Azure Data Explorer | Azure数据资源管理器 | 快速的数据探索 / Fast data exploration |
| Azure Purview | Azure Purview | 统一的数据治理 / Unified data governance |
| Microsoft Fabric | Microsoft Fabric | 统一的数据平台 / Unified data platform |
| Azure Event Hubs | Azure事件中心 | 大数据流摄取 / Big data streaming ingestion |
| Power BI Embedded | Power BI Embedded | 嵌入式商业智能 / Embedded business intelligence |
| Azure Monitor Logs | Azure Monitor日志 | 日志分析和监控 / Log analytics and monitoring |

---

### 📞 九、Integration (集成)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Logic Apps | Azure逻辑应用 | 工作流自动化 / Workflow automation |
| Azure Service Bus | Azure服务总线 | 企业消息传递 / Enterprise messaging |
| Azure Event Grid | Azure事件网格 | 无服务器事件路由 / Serverless event routing |
| Azure API Management | Azure API管理 | API发布和管理 / API publishing and management |
| Azure Data Factory | Azure数据工厂 | 数据集成和ETL / Data integration and ETL |
| Azure Event Hubs | Azure事件中心 | 实时数据摄取 / Real-time data ingestion |
| Azure Relay | Azure中继 | 混合连接服务 / Hybrid connection service |
| Azure Web PubSub | Azure Web PubSub | 实时WebSocket服务 / Real-time WebSocket service |
| Azure Queue Storage | Azure队列存储 | 云消息队列 / Cloud message queuing |

---

### 🔧 十、Developer Tools (开发者工具)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure DevOps | Azure DevOps | 开发运维一体化平台 / DevOps platform |
| Azure DevOps Services | Azure DevOps服务 | 托管的DevOps服务 / Hosted DevOps services |
| Azure Pipelines | Azure管道 | CI/CD自动化 / CI/CD automation |
| Azure Repos | Azure代码仓库 | 源代码版本控制 / Source code version control |
| Azure Boards | Azure看板 | 敏捷项目管理 / Agile project management |
| Azure Test Plans | Azure测试计划 | 测试管理 / Test management |
| Azure Artifacts | Azure工件 | 包管理 / Package management |
| GitHub Advanced Security | GitHub高级安全 | 代码安全扫描 / Code security scanning |
| Microsoft Dev Box | Microsoft Dev Box | 云开发者工作站 / Cloud developer workstations |
| Azure Playwright Testing | Azure Playwright测试 | 自动化Web测试 / Automated web testing |
| Azure App Configuration | Azure应用配置 | 集中式配置管理 / Centralized configuration |
| Azure Chaos Studio | Azure混沌工作室 | 混沌工程实验 / Chaos engineering |
| Azure Monitor | Azure监控器 | 应用和基础设施监控 / Application and infrastructure monitoring |
| Azure Application Insights | Application Insights | 应用性能管理 / Application performance management |

---

### 🔍 十一、Management & Governance (管理与治理)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Azure Portal | Azure门户 | 基于Web的管理界面 / Web-based management interface |
| Azure CLI | Azure CLI | 命令行工具 / Command-line interface |
| Azure PowerShell | Azure PowerShell | PowerShell模块 / PowerShell module |
| Azure Resource Manager | Azure资源管理器 | 基础设施即代码 / Infrastructure as code |
| Azure Policy | Azure策略 | 资源合规性管理 / Resource compliance |
| Azure Blueprints | Azure蓝图 | 环境部署标准化 / Environment standardization |
| Azure Cost Management | Azure成本管理 | 成本分析和优化 / Cost analysis and optimization |
| Azure Advisor | Azure顾问 | 个性化最佳建议 / Personalized best practices |
| Azure Service Health | Azure服务运行状况 | 服务状态监控 / Service health monitoring |
| Azure Monitor | Azure监控器 | 统一监控平台 / Unified monitoring platform |
| Azure Log Analytics | Azure日志分析 | 日志数据收集和分析 / Log data collection and analysis |
| Azure Automation | Azure自动化 | 流程自动化 / Process automation |
| Azure Site Recovery | Azure站点恢复 | 灾难恢复服务 / Disaster recovery service |
| Azure Backup | Azure备份 | 云备份服务 / Cloud backup service |
| Azure Arc | Azure Arc | 混合和多云管理 / Hybrid and multi-cloud management |

---

## Step 2: Search for Product Information | 搜索产品信息

### 2.1 Construct Search Queries | 构建搜索查询

**Product Homepage Search**:
```
site:azure.microsoft.com [product-name]
site:azure.microsoft.com/products/[product-code]
```

**Documentation Search**:
```
site:learn.microsoft.com/azure [product-name] overview
site:learn.microsoft.com/azure [product-name] quickstart
site:learn.microsoft.com/rest/api [product-name]
```

**Pricing Search**:
```
site:azure.microsoft.com [product-name] pricing
site:azure.microsoft.com/pricing/details/[product-code]
```

### 2.2 Execute Search | 执行搜索

Use `WebSearch` tool to execute the above queries and get URLs of official documentation and product pages.

---

## Step 3: Retrieve and Extract Information | 获取并提取信息

### 3.1 Retrieve Product Homepage Info | 获取产品首页信息

**Official URL Format**:
- Product page: `https://azure.microsoft.com/en-us/products/[product-code]/`
- Pricing page: `https://azure.microsoft.com/en-us/pricing/details/[product-code]/`

Use `Browser Navigate` or `WebFetch` to visit pages and extract:
1. **Product Tagline**: One-sentence value proposition
2. **Core Features**: Key capabilities
3. **Use Cases**: Typical scenarios
4. **Product Benefits**: Differentiating advantages

### 3.2 Retrieve Technical Documentation | 获取技术文档

**Documentation URL Format**:
- Overview: `https://learn.microsoft.com/en-us/azure/[product-code]/`
- Quickstart: `https://learn.microsoft.com/en-us/azure/[product-code]/quickstart`
- REST API: `https://learn.microsoft.com/en-us/rest/api/[product-code]/`

**Common Product Codes**:
| Product | Code |
|---------|------|
| Virtual Machines | virtual-machines |
| Blob Storage | storage/blobs |
| SQL Database | azure-sql/database |
| Functions | azure-functions |
| AKS | aks |
| Cosmos DB | cosmos-db |
| CDN | cdn |
| Virtual Network | virtual-network |

### 3.3 Extract Key Parameters | 提取关键参数

- **Specifications**: VM sizes, storage tiers, performance levels
- **Pricing**: Pay-as-you-go, Reserved Instances, Spot pricing
- **Technical Parameters**: Configuration options
- **Limits**: Quotas and service limits

---

## Step 4: Integrate and Present Results | 整合并呈现结果

### 4.1 Information Integration Rules | 信息整合规则

1. **Priority**: Official docs > Product page > Third-party
2. **Conflict Resolution**: Use official documentation as source of truth
3. **Completeness**: Mark missing info as "[Not found in public sources]"

### 4.2 Output Template | 输出模板

```markdown
# [Product Name] | [产品名称]

## Overview | 产品概述

**Tagline**: [One-sentence description]

**Description**:
[English description]

[中文描述]

**Core Features**:
- [Feature 1] | [功能1]
- [Feature 2] | [功能2]

**Use Cases**:
1. [Use case 1] | [场景1]
2. [Use case 2] | [场景2]

---

## Specifications | 产品规格

### Instance Types / Tiers | 实例类型/层级
| Type/Tier | Spec | Use Case |
|-----------|------|----------|
| [Type] | [Spec] | [Use case] |

### Regions | 支持区域
- [Region 1]
- [Region 2]

---

## Pricing | 定价信息

### Pricing Models | 计费模式
- **Pay-as-you-go**: [Description]
- **Reserved Instances**: [Description]
- **Spot/Preemptible**: [Description]

### Price Details | 价格详情
| Resource | Price |
|----------|-------|
| [Resource] | [Price] |

---

## Quick Start | 快速入门

### Prerequisites | 前提条件
- [Requirement 1]
- [Requirement 2]

### Getting Started | 入门步骤
1. [Step 1]
2. [Step 2]

---

## Development Reference | 开发参考

### API Overview | API概览
**Endpoint**: `https://management.azure.com`

### SDK Support | SDK支持
- **Python**: `azure-mgmt-*`
- **.NET**: `Azure.*`
- **Java**: `azure-mgmt-*`
- **JavaScript**: `@azure/*`

### Code Example | 代码示例
```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

credential = DefaultAzureCredential()
client = ComputeManagementClient(credential, subscription_id='<subscription-id>')
```

---

## Related Resources | 相关资源

### Documentation | 文档链接
- [Product Documentation](https://learn.microsoft.com/en-us/azure/[product-code]/)
- [REST API Reference](https://learn.microsoft.com/en-us/rest/api/[product-code]/)

### Related Products | 相关产品
- [Product 1] - [Description]
- [Product 2] - [Description]
```

---

## Important Notes | 重要说明

### Information Accuracy | 信息准确性
- All information sourced from Microsoft Azure official public documentation
- Pricing subject to change; verify on official website
- Some detailed parameters may require Azure subscription

### Tool Limitations | 工具限制
- `WebFetch` may return errors for some dynamic pages
- Use `WebSearch` + `Browser Navigate` as fallback
- Search snippets often sufficient for basic queries

### Credential Security | 凭证安全
Always use placeholders in code examples:
- `<subscription-id>` - Azure Subscription ID
- `<tenant-id>` - Azure Tenant ID
- `<client-id>` - Service Principal Client ID
- `<client-secret>` - Service Principal Client Secret
- `<resource-group>` - Resource Group Name

---

## Official Resources | 官方资源

- **Azure Homepage**: https://azure.microsoft.com/
- **Azure China**: https://www.azure.cn/
- **Documentation**: https://learn.microsoft.com/azure/
- **Pricing**: https://azure.microsoft.com/pricing/
- **REST API Reference**: https://learn.microsoft.com/rest/api/azure/
