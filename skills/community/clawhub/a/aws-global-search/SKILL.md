---
name: aws-global-search
description: Query AWS (Amazon Web Services) product information, documentation, parameters, features, and pricing from official sources without login. Use when the user asks about AWS products (EC2, S3, RDS, Lambda, etc.), needs product documentation, wants to compare product specifications, or needs help finding specific product parameters and features.
---

# AWS Product Query | AWS产品查询

This skill helps users find detailed information about AWS (Amazon Web Services) products by searching official documentation and product pages without requiring login.

本技能帮助用户通过搜索官方文档和产品页面，无需登录即可获取AWS（亚马逊云服务）产品的详细信息。

## When to Use | 使用场景

- User asks about specific AWS products (EC2, S3, RDS, Lambda, etc.) / 用户询问特定的AWS产品（EC2、S3、RDS、Lambda等）
- User needs product documentation or API references / 用户需要产品文档或API参考
- User wants to compare product specifications or pricing / 用户想要比较产品规格或价格
- User needs help finding specific product parameters or features / 用户需要帮助查找特定的产品参数或功能
- User mentions "AWS", "Amazon Web Services", or "亚马逊云" and needs product information / 用户提到"AWS"或"亚马逊云"并需要产品信息

---

## Step 1: Identify the Product | 识别产品

### 1.1 Identify Product Keywords | 识别产品关键词

Analyze user questions and extract:
- **Product Name**: Specific product names (e.g., EC2, S3, RDS, Lambda)
- **Product Category**: Product categories (e.g., Compute, Storage, Database)
- **Functional Requirements**: Functions the user wants to implement
- **Use Cases**: User's business scenarios

分析用户问题，提取：
- **产品名称**: 具体产品名（如 EC2、S3、RDS、Lambda）
- **产品类别**: 产品类别（如计算、存储、数据库）
- **功能需求**: 用户想要实现的功能
- **使用场景**: 用户的业务场景

### 1.2 Product Alias Reference | 产品别名对照表

| User May Say | Product | English Name |
|-------------|---------|--------------|
| 云服务器、虚拟机、VM (Cloud Server, VM) | EC2 | Elastic Compute Cloud |
| 对象存储、云盘 (Object Storage) | S3 | Simple Storage Service |
| 云硬盘、块存储 (Block Storage) | EBS | Elastic Block Store |
| 文件存储、NAS (File Storage) | EFS | Elastic File System |
| 负载均衡 (Load Balancer) | ELB/ALB | Elastic Load Balancing |
| 数据库、MySQL、PostgreSQL (Database) | RDS/Aurora | Relational Database Service |
| Redis、缓存 (Cache) | ElastiCache | ElastiCache |
| 大模型、AI、机器学习 (AI/ML) | SageMaker/Bedrock | SageMaker / Bedrock |
| 容器、K8s、Kubernetes (Container) | EKS/ECS | Elastic Kubernetes Service |
| 函数计算、Serverless (Function) | Lambda | AWS Lambda |
| 安全中心 (Security) | Security Hub | AWS Security Hub |
| WAF、防火墙 (Firewall) | WAF | AWS WAF |
| CDN、加速 (CDN) | CloudFront | Amazon CloudFront |
| VPC、私有网络 (VPC) | VPC | Virtual Private Cloud |
| 大数据、数仓 (Big Data) | Redshift/EMR | Redshift / EMR |
| 消息队列、Kafka (Message Queue) | SQS/SNS/MSK | Simple Queue Service |

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

## 📦 AWS Full Product Catalog | AWS全产品目录

### 🤖 一、Machine Learning & AI (机器学习与人工智能)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon SageMaker | SageMaker | 构建、训练和部署机器学习模型的完全托管服务 / Fully managed service for building, training, and deploying ML models |
| Amazon Bedrock | Bedrock | 使用基础模型构建和扩展生成式AI应用 / Build and scale generative AI applications with foundation models |
| Amazon Rekognition | Rekognition | 图像和视频分析服务 / Image and video analysis service |
| Amazon Polly | Polly | 将文本转换为逼真的语音 / Turn text into lifelike speech |
| Amazon Lex | Lex | 构建语音和文本聊天机器人 / Build voice and text chatbots |
| Amazon Comprehend | Comprehend | 自然语言处理服务 / Natural language processing service |
| Amazon Translate | Translate | 神经网络机器翻译服务 / Neural machine translation service |
| Amazon Personalize | Personalize | 实时个性化推荐 / Real-time personalization recommendations |
| Amazon Kendra | Kendra | 企业搜索服务 / Enterprise search service |
| Amazon Q | Amazon Q | 生成式AI助手 / Generative AI assistant |

---

### 🖥️ 二、Compute (计算)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon EC2 | 弹性计算云 | 安全且可调整大小的计算容量 / Secure and resizable compute capacity |
| AWS Lambda | Lambda | 无服务器计算服务 / Serverless compute service |
| AWS Fargate | Fargate | 适用于容器的无服务器计算 / Serverless compute for containers |
| AWS Batch | Batch | 运行批处理计算作业 / Run batch computing workloads |
| AWS Outposts | Outposts | 本地扩展AWS基础设施 / Extend AWS infrastructure on-premises |
| AWS Wavelength | Wavelength | 为5G设备构建超低延迟应用 / Build ultra-low latency apps for 5G devices |
| AWS Local Zones | Local Zones | 将AWS计算、存储等靠近最终用户 / Place AWS compute closer to end users |
| AWS Elastic Beanstalk | Elastic Beanstalk | 应用程序部署服务 / Application deployment service |
| AWS Serverless Application Repository | SAR | 发现、部署和发布无服务器应用 / Discover, deploy, and publish serverless applications |
| AWS App Runner | App Runner | 快速构建、部署和运行容器化Web应用 / Quickly build, deploy, and run containerized web applications |

---

### 💾 三、Storage (存储)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon S3 | 简单存储服务 | 适用于AI、分析和存档的对象存储 / Object storage for AI, analytics, and archive |
| Amazon EBS | 弹性块存储 | 块级存储卷 / Block-level storage volumes |
| Amazon EFS | 弹性文件系统 | 完全托管的NFS服务 / Fully managed NFS service |
| Amazon FSx | FSx | 完全托管的第三方文件系统 / Fully managed third-party file systems |
| Amazon S3 Glacier | Glacier | 低成本归档存储 / Low-cost archive storage |
| AWS Storage Gateway | Storage Gateway | 混合云存储服务 / Hybrid cloud storage service |
| AWS Backup | Backup | 集中式备份服务 / Centralized backup service |
| AWS Elastic Disaster Recovery | DRS | 经济高效的灾难恢复 / Cost-effective disaster recovery |

---

### 🗄️ 四、Database (数据库)

#### Relational Database (关系型数据库)
| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon RDS | 关系型数据库服务 | 托管的关系型数据库服务 / Managed relational database service |
| Amazon Aurora | Aurora | 与MySQL和PostgreSQL兼容的企业级数据库 / Enterprise-grade database compatible with MySQL and PostgreSQL |
| Amazon Redshift | Redshift | 数据仓库服务 / Data warehouse service |

#### NoSQL Database (NoSQL数据库)
| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon DynamoDB | DynamoDB | 无服务器NoSQL数据库 / Serverless NoSQL database |
| Amazon ElastiCache | ElastiCache | 托管的内存缓存服务 / Managed in-memory caching service |
| Amazon DocumentDB | DocumentDB | 与MongoDB兼容的数据库 / MongoDB-compatible database |
| Amazon Keyspaces | Keyspaces | 托管的Apache Cassandra兼容服务 / Managed Apache Cassandra-compatible service |
| Amazon Neptune | Neptune | 完全托管的图数据库 / Fully managed graph database |
| Amazon Timestream | Timestream | 无服务器时间序列数据库 / Serverless time series database |
| Amazon QLDB | QLDB | 完全托管的账本数据库 / Fully managed ledger database |

---

### 🐳 五、Containers (容器)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon EKS | 弹性Kubernetes服务 | 托管的Kubernetes服务 / Managed Kubernetes service |
| Amazon ECS | 弹性容器服务 | 完全托管的容器编排服务 / Fully managed container orchestration service |
| AWS Fargate | Fargate | 适用于容器的无服务器计算 / Serverless compute for containers |
| Amazon ECR | 弹性容器注册表 | 完全托管的容器注册表 / Fully managed container registry |
| AWS App Mesh | App Mesh | 应用程序级网络 / Application-level networking |
| AWS Cloud Map | Cloud Map | 云资源发现服务 / Cloud resource discovery service |
| AWS Copilot | Copilot | 容器化应用程序的CLI工具 / CLI tool for containerized applications |

---

### 🌐 六、Networking & Content Delivery (网络与内容分发)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon VPC | 虚拟私有云 | 隔离的虚拟网络 / Isolated virtual network |
| Amazon CloudFront | CloudFront | 全球内容分发网络 / Global content delivery network |
| Amazon Route 53 | Route 53 | 可扩展的域名系统 / Scalable domain name system |
| Elastic Load Balancing | 弹性负载均衡 | 应用程序负载均衡 / Application load balancing |
| AWS App Mesh | App Mesh | 服务网格 / Service mesh |
| AWS Cloud Map | Cloud Map | 服务发现 / Service discovery |
| AWS Global Accelerator | Global Accelerator | 全球网络加速 / Global network acceleration |
| AWS Transit Gateway | Transit Gateway | 网络传输网关 / Network transit hub |
| AWS PrivateLink | PrivateLink | 私有连接服务 / Private connectivity service |
| AWS Direct Connect | Direct Connect | 专线连接服务 / Dedicated network connection |
| AWS VPN | VPN | 站点到站点VPN / Site-to-site VPN |
| AWS Network Manager | Network Manager | 全球网络管理 / Global network management |

---

### 🔒 七、Security, Identity & Compliance (安全、身份与合规)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| AWS IAM | 身份和访问管理 | 安全地管理对AWS服务和资源的访问 / Securely manage access to AWS services |
| Amazon Cognito | Cognito | 用户身份验证和授权 / User authentication and authorization |
| AWS KMS | 密钥管理服务 | 创建和管理加密密钥 / Create and manage encryption keys |
| AWS WAF | Web应用程序防火墙 | 保护Web应用程序 / Protect web applications |
| AWS Shield | Shield | DDoS防护服务 / DDoS protection service |
| AWS Firewall Manager | Firewall Manager | 集中管理防火墙规则 / Central management of firewall rules |
| AWS Security Hub | Security Hub | 统一的安全和合规中心 / Unified security and compliance center |
| Amazon GuardDuty | GuardDuty | 智能威胁检测 / Intelligent threat detection |
| Amazon Inspector | Inspector | 自动安全评估 / Automated security assessment |
| AWS Certificate Manager | ACM | 预置、管理和部署SSL/TLS证书 / Provision, manage, and deploy SSL/TLS certificates |
| AWS Secrets Manager | Secrets Manager | 轮换、管理和检索机密信息 / Rotate, manage, and retrieve secrets |
| AWS CloudHSM | CloudHSM | 基于硬件的密钥存储 / Hardware-based key storage |
| AWS Artifact | Artifact | 按需访问AWS合规报告 / On-demand access to AWS compliance reports |
| AWS Audit Manager | Audit Manager | 持续审计和合规 / Continuous auditing and compliance |

---

### 📊 八、Analytics (分析)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon Athena | Athena | 交互式查询服务 / Interactive query service |
| Amazon EMR | EMR | 托管的Hadoop和Spark框架 / Managed Hadoop and Spark framework |
| Amazon CloudSearch | CloudSearch | 托管的搜索服务 / Managed search service |
| Amazon Elasticsearch Service | OpenSearch Service | 搜索、可视化和分析 / Search, visualize, and analyze |
| Amazon Kinesis | Kinesis | 实时数据流处理 / Real-time data streaming |
| Amazon QuickSight | QuickSight | 商业智能服务 / Business intelligence service |
| AWS Data Pipeline | Data Pipeline | 数据编排服务 / Data orchestration service |
| AWS Glue | Glue | 无服务器数据集成 / Serverless data integration |
| AWS Lake Formation | Lake Formation | 构建数据湖 / Build data lakes |
| Amazon MSK | MSK | 托管的Kafka服务 / Managed Kafka service |

---

### 📞 九、Application Integration (应用程序集成)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon SQS | 简单队列服务 | 托管的消息队列服务 / Managed message queue service |
| Amazon SNS | 简单通知服务 | 发布/订阅消息服务 / Pub/sub messaging service |
| Amazon EventBridge | EventBridge | 无服务器事件总线 / Serverless event bus |
| AWS Step Functions | Step Functions | 工作流编排服务 / Workflow orchestration service |
| Amazon AppFlow | AppFlow | 无代码SaaS集成 / No-code SaaS integration |
| Amazon MQ | MQ | 托管的消息代理服务 / Managed message broker service |
| AWS AppSync | AppSync | 完全托管的GraphQL服务 / Fully managed GraphQL service |
| AWS B2B Data Interchange | B2B Data Interchange | 无代码B2B电子数据交换 / No-code B2B EDI |

---

### 🔧 十、Developer Tools (开发者工具)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| AWS CodeCommit | CodeCommit | 源代码版本控制服务 / Source code version control |
| AWS CodeBuild | CodeBuild | 持续集成服务 / Continuous integration service |
| AWS CodeDeploy | CodeDeploy | 自动化部署服务 / Automated deployment service |
| AWS CodePipeline | CodePipeline | 持续交付服务 / Continuous delivery service |
| AWS Cloud9 | Cloud9 | 云端集成开发环境 / Cloud IDE |
| AWS CloudShell | CloudShell | 基于浏览器的Shell / Browser-based shell |
| AWS X-Ray | X-Ray | 应用程序性能分析 / Application performance analysis |
| AWS Fault Injection Simulator | FIS | 混沌工程服务 / Chaos engineering service |

---

### 🔍 十一、Management & Governance (管理与治理)

| Product Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Amazon CloudWatch | CloudWatch | 监控和可观测性服务 / Monitoring and observability |
| AWS CloudFormation | CloudFormation | 基础设施即代码服务 / Infrastructure as code |
| AWS CloudTrail | CloudTrail | 账户活动监控 / Account activity monitoring |
| AWS Config | Config | 资源配置和合规监控 / Resource configuration tracking |
| AWS Organizations | Organizations | 多账户管理服务 / Multi-account management |
| AWS Systems Manager | Systems Manager | 运营管理中心 / Operations hub |
| AWS Trusted Advisor | Trusted Advisor | 最佳实践检查和优化 / Best practice checks |
| AWS Service Catalog | Service Catalog | IT服务目录 / IT service catalog |
| AWS Control Tower | Control Tower | 设置和管理安全的多账户环境 / Set up and govern secure multi-account environments |
| AWS License Manager | License Manager | 管理软件许可证 / Manage software licenses |
| AWS Health Dashboard | Health Dashboard | AWS服务健康状况 / AWS service health |
| AWS Proton | Proton | 无服务器和容器部署的自动化平台 / Automated platform for serverless and container deployments |

---

## Step 2: Search for Product Information | 搜索产品信息

### 2.1 Construct Search Queries | 构建搜索查询

**Product Homepage Search**:
```
site:aws.amazon.com [product-name]
site:aws.amazon.com/[product-code]
```

**Documentation Search**:
```
site:docs.aws.amazon.com [product-name] what is
site:docs.aws.amazon.com [product-name] getting started
site:docs.aws.amazon.com [product-name] API reference
```

**Pricing Search**:
```
site:aws.amazon.com [product-name] pricing
aws.amazon.com/pricing/[product-code]
```

### 2.2 Execute Search | 执行搜索

Use `WebSearch` tool to execute the above queries and get URLs of official documentation and product pages.

---

## Step 3: Retrieve and Extract Information | 获取并提取信息

### 3.1 Retrieve Product Homepage Info | 获取产品首页信息

**Official URL Format**:
- Product page: `https://aws.amazon.com/[product-code]/`
- Chinese page: `https://aws.amazon.com/cn/[product-code]/`

Use `Browser Navigate` or `WebFetch` to visit pages and extract:
1. **Product Tagline**: One-sentence value proposition
2. **Core Features**: Key capabilities
3. **Use Cases**: Typical scenarios
4. **Product Benefits**: Differentiating advantages

### 3.2 Retrieve Technical Documentation | 获取技术文档

**Documentation URL Format**:
- User Guide: `https://docs.aws.amazon.com/[product-code]/latest/userguide/`
- API Reference: `https://docs.aws.amazon.com/[product-code]/latest/APIReference/`
- CLI Reference: `https://docs.aws.amazon.com/cli/latest/reference/[product-code]/`

**Common Product Codes**:
| Product | Code |
|---------|------|
| EC2 | ec2 |
| S3 | s3 |
| RDS | rds |
| Lambda | lambda |
| EKS | eks |
| DynamoDB | dynamodb |
| CloudFront | cloudfront |
| VPC | vpc |

### 3.3 Extract Key Parameters | 提取关键参数

- **Specifications**: Instance types, performance metrics
- **Pricing**: On-demand, Reserved, Spot pricing
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

### Instance Types | 实例类型
| Type | Spec | Use Case |
|------|------|----------|
| [Type] | [Spec] | [Use case] |

### Regions | 支持区域
- [Region 1]
- [Region 2]

---

## Pricing | 定价信息

### Pricing Models | 计费模式
- **On-Demand**: [Description]
- **Reserved Instances**: [Description]
- **Spot Instances**: [Description]

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
**Endpoint**: `https://[service].[region].amazonaws.com`

### SDK Support | SDK支持
- **Python**: `boto3`
- **Java**: `aws-sdk-java`
- **Go**: `aws-sdk-go-v2`

### Code Example | 代码示例
```python
import boto3

client = boto3.client(
    '[service-name]',
    aws_access_key_id='<your-access-key-id>',
    aws_secret_access_key='<your-secret-access-key>',
    region_name='<region-name>'
)
```

---

## Related Resources | 相关资源

### Documentation | 文档链接
- [User Guide](https://docs.aws.amazon.com/[product-code]/latest/userguide/)
- [API Reference](https://docs.aws.amazon.com/[product-code]/latest/APIReference/)

### Related Products | 相关产品
- [Product 1] - [Description]
- [Product 2] - [Description]
```

---

## Important Notes | 重要说明

### Information Accuracy | 信息准确性
- All information sourced from AWS official public documentation
- Pricing subject to change; verify on official website
- Some detailed parameters may require AWS account

### Tool Limitations | 工具限制
- `WebFetch` may return errors for some dynamic pages
- Use `WebSearch` + `Browser Navigate` as fallback
- Search snippets often sufficient for basic queries

### Credential Security | 凭证安全
Always use placeholders in code examples:
- `<your-access-key-id>` - AWS Access Key ID
- `<your-secret-access-key>` - AWS Secret Access Key
- `<your-region>` - AWS Region (e.g., us-east-1)
- `<your-account-id>` - AWS Account ID

---

## Official Resources | 官方资源

- **AWS Homepage**: https://aws.amazon.com/
- **AWS China**: https://www.amazonaws.cn/
- **Documentation**: https://docs.aws.amazon.com/
- **Pricing**: https://aws.amazon.com/pricing/
- **AWS CLI Reference**: https://docs.aws.amazon.com/cli/
