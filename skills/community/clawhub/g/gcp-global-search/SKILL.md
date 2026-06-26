---
name: gcp-global-search
description: Query Google Cloud (谷歌云) product information, documentation, parameters, features, and pricing from official sources without login. Use when the user asks about Google Cloud products (Compute Engine, Cloud Storage, BigQuery, Cloud SQL, etc.), needs product documentation, wants to compare product specifications, or needs help finding specific product parameters and features.
---

# Google Cloud 产品查询 (Google Cloud Product Query)

This skill helps users find detailed information about Google Cloud products by searching official documentation and product pages without requiring login.

本技能帮助用户通过搜索官方文档和产品页面，无需登录即可获取谷歌云产品的详细信息。

## When to Use / 使用场景

- User asks about specific Google Cloud products (Compute Engine, Cloud Storage, BigQuery, etc.) / 用户询问特定的谷歌云产品（Compute Engine、Cloud Storage、BigQuery等）
- User needs product documentation or API references / 用户需要产品文档或API参考
- User wants to compare product specifications or pricing / 用户想要比较产品规格或价格
- User needs help finding specific product parameters or features / 用户需要帮助查找特定的产品参数或功能
- User mentions "Google Cloud", "GCP", "谷歌云" and needs product information / 用户提到"Google Cloud"、"GCP"或"谷歌云"并需要产品信息

---

## Step 1: Identify the Product (识别产品)

从全面的产品目录中确定用户询问的是哪个谷歌云产品：

### 1.1 识别用户查询中的产品关键词 / Identify Product Keywords from User Query

分析用户问题，提取以下信息 / Analyze user questions and extract the following information:
- **产品名称 (Product Name)**: 用户提到的具体产品名（如 Compute Engine、Cloud Storage、BigQuery）/ Specific product names mentioned by the user (e.g., Compute Engine, Cloud Storage, BigQuery)
- **产品类别 (Product Category)**: 用户可能提到的产品类别（如计算、数据库、存储）/ Product categories mentioned (e.g., Compute, Database, Storage)
- **功能需求 (Functional Requirements)**: 用户想要实现的功能（如搭建网站、数据备份、负载均衡）/ Functions the user wants to implement (e.g., build websites, data backup, load balancing)
- **使用场景 (Use Cases)**: 用户的业务场景（如电商、游戏、金融）/ User's business scenarios (e.g., e-commerce, gaming, finance)

### 1.2 使用产品别名对照表 / Product Alias Reference Table

如果用户使用非标准名称，参考以下别名映射 / If users use non-standard names, refer to the following alias mapping:

| 用户可能说的 (User May Say) | 对应产品 (Product) | 英文名 (English Name) |
|---------------------------|-------------------|----------------------|
| 云服务器、虚拟机、VM、GCE (Cloud Server, VM) | Compute Engine | Compute Engine |
| 对象存储、云盘、云存储 (Object Storage, Cloud Disk) | Cloud Storage | Cloud Storage |
| 负载均衡、LB (Load Balancer) | Cloud Load Balancing | Cloud Load Balancing |
| 数据库、MySQL、PostgreSQL、SQL (Database) | Cloud SQL | Cloud SQL |
| Spanner、分布式数据库 (Distributed DB) | Cloud Spanner | Cloud Spanner |
| BigQuery、数据仓库 (Data Warehouse) | BigQuery | BigQuery |
| Redis、缓存 (Redis, Cache) | Memorystore | Memorystore for Redis |
| Firestore、文档数据库 (Document DB) | Firestore | Cloud Firestore |
| Datastore、NoSQL (NoSQL) | Datastore | Cloud Datastore |
| 容器、K8s、Kubernetes、GKE (Container, K8s) | Google Kubernetes Engine | GKE |
| 函数计算、Cloud Functions (Function Compute) | Cloud Functions | Cloud Functions |
| Cloud Run、无服务器容器 (Serverless Container) | Cloud Run | Cloud Run |
| VPC、私有网络 (VPC, Private Network) | VPC | Virtual Private Cloud |
| CDN、加速 (CDN, Acceleration) | Cloud CDN | Cloud CDN |
| Pub/Sub、消息队列 (Message Queue) | Pub/Sub | Cloud Pub/Sub |
| IAM、权限管理 (Identity Management) | Cloud IAM | Identity and Access Management |
| 监控、Monitoring (Monitoring) | Cloud Monitoring | Cloud Monitoring |
| 日志、Logging (Logging) | Cloud Logging | Cloud Logging |
| AI平台、Vertex AI (AI Platform) | Vertex AI | Vertex AI |
| 翻译、Translation (Translation) | Cloud Translation | Cloud Translation API |
| 视觉、Vision (Vision) | Cloud Vision | Cloud Vision API |
| 语音、Speech (Speech) | Cloud Speech-to-Text | Cloud Speech-to-Text |
| 自然语言、NLP (NLP) | Cloud Natural Language | Cloud Natural Language API |

### 1.3 确定目标产品 / Identify Target Product

从产品目录中找到最匹配的产品，记录 / Find the best matching product from the catalog and record:
- **产品中文名 (Chinese Name)**: 产品的中文名称
- **产品英文名 (English Name)**: 产品的英文名称
- **产品类别 (Category)**: 产品所属类别
- **产品代码 (Product Code)**: 用于构造URL的产品代码

---

## 📦 Google Cloud 全产品目录 (Google Cloud Full Product Catalog)

### 🤖 一、人工智能与机器学习 (AI & Machine Learning)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Vertex AI | Vertex AI | 统一的AI平台，用于构建、部署和扩展机器学习模型 / Unified AI platform for building, deploying, and scaling ML models |
| AutoML | AutoML | 无需编写代码即可训练高质量自定义机器学习模型 / Train high-quality custom ML models without writing code |
| BigQuery ML | BigQuery ML | 在BigQuery中使用SQL创建和执行机器学习模型 / Create and execute ML models using SQL in BigQuery |
| Cloud Natural Language | Cloud Natural Language API | 用于自然语言理解的机器学习 / Machine learning for natural language understanding |
| Cloud Speech-to-Text | Cloud Speech-to-Text | 使用神经网络模型将音频转换为文本 / Convert audio to text using neural network models |
| Cloud Text-to-Speech | Cloud Text-to-Speech | 将文本转换为自然 sounding 的语音 / Convert text into natural-sounding speech |
| Cloud Translation | Cloud Translation API | 动态翻译内容 / Dynamically translate between languages |
| Cloud Vision | Cloud Vision API | 从图像中提取信息 / Derive insights from images |
| Cloud Video Intelligence | Cloud Video Intelligence API | 从视频中提取信息 / Extract information from videos |
| Dialogflow | Dialogflow | 构建对话式界面 / Build conversational interfaces |
| Recommendations AI | Recommendations AI | 提供个性化产品推荐 / Deliver personalized product recommendations |
| AI Platform Prediction | AI Platform Prediction | 托管的机器学习模型服务 / Managed service for ML model serving |
| TensorFlow Enterprise | TensorFlow Enterprise | 针对Google Cloud优化的TensorFlow / TensorFlow optimized for Google Cloud |
| Vertex AI Workbench | Vertex AI Workbench | 基于Jupyter的机器学习开发环境 / Jupyter-based ML development environment |

---

### 🖥️ 二、计算 (Compute)

#### 虚拟机计算 (Virtual Machine Compute)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Compute Engine | Compute Engine | 在Google基础设施上运行虚拟机 / Run VMs on Google's infrastructure |
| Compute Engine Autoscaling | Compute Engine Autoscaling | 根据负载自动调整实例数量 / Automatically adjust instance count based on load |
| Sole-Tenant Nodes | Sole-Tenant Nodes | 专用物理服务器 / Dedicated physical servers |
| Confidential Computing | Confidential Computing | 加密内存中的数据 / Encrypt data in use |
| Spot VMs | Spot VMs | 价格更低的可抢占式虚拟机 / Preemptible VMs at lower prices |
| Preemptible VMs | Preemptible VMs | 短期工作负载的低成本实例 / Low-cost instances for short workloads |

#### 无服务器计算 (Serverless Compute)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud Functions | Cloud Functions | 事件驱动的无服务器函数平台 / Event-driven serverless compute platform |
| Cloud Run | Cloud Run | 运行无状态容器 / Run stateless containers |
| Cloud Run Jobs | Cloud Run Jobs | 运行容器化任务 / Run containerized tasks |
| App Engine | App Engine | 完全托管的无服务器应用平台 / Fully managed serverless application platform |
| App Engine Flexible | App Engine Flexible | 基于Docker容器的App Engine / Docker container-based App Engine |

#### 容器计算 (Container Compute)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Google Kubernetes Engine | GKE | 托管的Kubernetes服务 / Managed Kubernetes service |
| GKE Autopilot | GKE Autopilot | 完全托管的Kubernetes体验 / Fully managed Kubernetes experience |
| GKE Enterprise | GKE Enterprise | 多集群管理和安全性 / Multi-cluster management and security |
| Cloud Build | Cloud Build | 持续集成和交付平台 / Continuous integration and delivery platform |
| Artifact Registry | Artifact Registry | 管理容器镜像和语言包 / Manage container images and language packages |
| Container Registry | Container Registry | 私有Docker镜像存储 / Private Docker image storage |

---

### 💾 三、存储 (Storage)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud Storage | Cloud Storage | 统一的对象存储 / Unified object storage |
| Cloud Storage Standard | Cloud Storage Standard | 频繁访问数据的存储类别 / Storage class for frequently accessed data |
| Cloud Storage Nearline | Cloud Storage Nearline | 每月访问少于一次的存储 / Storage for data accessed less than once per month |
| Cloud Storage Coldline | Cloud Storage Coldline | 每季度访问一次的存储 / Storage for data accessed once per quarter |
| Cloud Storage Archive | Cloud Storage Archive | 长期归档存储 / Long-term archival storage |
| Filestore | Filestore | 托管的文件存储服务 / Managed file storage service |
| Persistent Disk | Persistent Disk | 高性能块存储 / High-performance block storage |
| Hyperdisk | Hyperdisk | 下一代块存储 / Next-generation block storage |
| Local SSD | Local SSD | 临时本地SSD存储 / Ephemeral local SSD storage |
| Cloud Storage for Firebase | Cloud Storage for Firebase | 为Firebase应用存储用户生成的内容 / Store user-generated content for Firebase apps |
| Backup for GKE | Backup for GKE | 保护GKE工作负载 / Protect GKE workloads |
| Storage Transfer Service | Storage Transfer Service | 大规模数据传输 / Large-scale data transfers |

---

### 🗄️ 四、数据库 (Database)

#### 关系型数据库 (Relational Database)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud SQL | Cloud SQL | 托管的MySQL、PostgreSQL和SQL Server / Managed MySQL, PostgreSQL, and SQL Server |
| Cloud Spanner | Cloud Spanner | 全球分布式关系型数据库 / Globally distributed relational database |
| AlloyDB | AlloyDB | 高性能PostgreSQL兼容数据库 / High-performance PostgreSQL-compatible database |
| Bare Metal Solution | Bare Metal Solution | 用于Oracle工作负载的专用硬件 / Dedicated hardware for Oracle workloads |

#### NoSQL数据库 (NoSQL Database)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Firestore | Cloud Firestore | 无服务器文档数据库 / Serverless document database |
| Datastore | Cloud Datastore | 高度可扩展的NoSQL数据库 / Highly scalable NoSQL database |
| Bigtable | Cloud Bigtable | 大规模NoSQL数据库服务 / Large-scale NoSQL database service |
| Memorystore | Memorystore | 托管的Redis和Memcached服务 / Managed Redis and Memcached service |
| Memorystore for Redis Cluster | Memorystore for Redis Cluster | 高可用Redis集群 / Highly available Redis cluster |

#### 数据库管理 (Database Management)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Database Migration Service | Database Migration Service | 简化到Cloud的数据库迁移 / Simplify migrations to the cloud |
| Cloud SQL Insights | Cloud SQL Insights | 数据库性能监控 / Database performance monitoring |
| Firebase Realtime Database | Firebase Realtime Database | 实时同步的NoSQL数据库 / NoSQL database with real-time sync |

---

### 📊 五、数据分析 (Data Analytics)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| BigQuery | BigQuery | 无服务器、高度可扩展的数据仓库 / Serverless, highly scalable data warehouse |
| BigQuery BI Engine | BigQuery BI Engine | 用于BI工作负载的内存分析引擎 / In-memory analytics engine for BI workloads |
| BigQuery Omni | BigQuery Omni | 跨云数据分析 / Cross-cloud data analytics |
| Looker | Looker | 企业级BI和数据分析平台 / Enterprise BI and data analytics platform |
| Looker Studio | Looker Studio | 免费的数据可视化和报告工具 / Free data visualization and reporting tool |
| Cloud Dataflow | Cloud Dataflow | 流式和批处理数据处理 / Stream and batch data processing |
| Cloud Dataproc | Cloud Dataproc | 托管的Spark和Hadoop服务 / Managed Spark and Hadoop service |
| Cloud Composer | Cloud Composer | 托管的Apache Airflow / Managed Apache Airflow |
| Cloud Data Fusion | Cloud Data Fusion | 全托管的数据集成服务 / Fully managed data integration service |
| Pub/Sub | Cloud Pub/Sub | 全球规模的消息传递服务 / Global-scale messaging service |
| Datastream | Datastream | 无服务器变更数据捕获 / Serverless change data capture |
| Dataform | Dataform | 数据转换工作流管理 / Data transformation workflow management |

---

### 🌐 六、网络 (Networking)

#### 云网络 (Cloud Networking)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| VPC | Virtual Private Cloud | 全球扩展的虚拟私有云 / Global Virtual Private Cloud |
| Cloud Load Balancing | Cloud Load Balancing | 高性能、可扩展的负载均衡 / High-performance, scalable load balancing |
| Cloud CDN | Cloud CDN | 内容分发网络 / Content delivery network |
| Cloud Armor | Cloud Armor | 边缘安全防御 / Edge security defense |
| Cloud NAT | Cloud NAT | 为私有实例提供出站互联网访问 / Outbound internet access for private instances |
| Cloud Interconnect | Cloud Interconnect | 连接到Google Cloud / Connect to Google Cloud |
| Cloud VPN | Cloud VPN | 通过VPN连接到VPC / Connect to VPC over VPN |
| Direct Peering | Direct Peering | 与Google直接对等连接 / Direct peering with Google |
| Carrier Peering | Carrier Peering | 通过服务提供商对等连接 / Peering through a service provider |
| Network Service Tiers | Network Service Tiers | 优化网络性能和成本 / Optimize network performance and cost |
| Network Connectivity Center | Network Connectivity Center | 统一连接管理 / Unified connectivity management |
| Network Intelligence Center | Network Intelligence Center | 网络监控和可视化 / Network monitoring and visualization |
| Private Service Connect | Private Service Connect | 安全访问托管服务 / Secure access to managed services |
| Service Directory | Service Directory | 服务发现和管理 / Service discovery and management |
| Cloud DNS | Cloud DNS | 可扩展的域名系统 / Scalable domain name system |
| Traffic Director | Traffic Director | 应用感知流量管理 / Application-aware traffic management |

---

### 🔒 七、安全与身份 (Security & Identity)

#### 身份与访问管理 (Identity & Access Management)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud IAM | Identity and Access Management | 细粒度的访问控制 / Fine-grained access control |
| Cloud Identity | Cloud Identity | 身份即服务 / Identity-as-a-Service |
| Identity-Aware Proxy | Identity-Aware Proxy | 基于身份的访问控制 / Identity-based access control |
| Resource Manager | Resource Manager | 分层资源管理 / Hierarchical resource management |
| Service Accounts | Service Accounts | 应用的身份验证 / Authentication for applications |
| Workload Identity | Workload Identity | 为工作负载提供Google身份 / Google identities for workloads |

#### 安全与合规 (Security & Compliance)
| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud KMS | Cloud Key Management Service | 托管的加密密钥管理 / Managed encryption key management |
| Secret Manager | Secret Manager | 安全存储API密钥和密码 / Secure storage for API keys and passwords |
| Certificate Authority Service | Certificate Authority Service | 托管的私有证书颁发机构 / Managed private certificate authority |
| Cloud HSM | Cloud HSM | 托管的硬件安全模块 / Managed hardware security modules |
| Security Command Center | Security Command Center | 统一的安全和风险管理 / Unified security and risk management |
| Cloud Data Loss Prevention | Cloud Data Loss Prevention | 发现和保护敏感数据 / Discover and protect sensitive data |
| Chronicle | Chronicle | 云原生安全分析和威胁情报 / Cloud-native security analytics |
| Mandiant Threat Intelligence | Mandiant Threat Intelligence | 威胁情报和专业知识 / Threat intelligence and expertise |
| Virus Total | Virus Total | 恶意软件分析服务 / Malware analysis service |
| Binary Authorization | Binary Authorization | 确保仅部署可信容器 / Ensure only trusted containers are deployed |
| Assured Workloads | Assured Workloads | 合规控制的环境 / Compliance-controlled environments |
| Access Transparency | Access Transparency | 查看Google管理员操作 / View Google admin actions |
| VPC Service Controls | VPC Service Controls | 定义安全边界 / Define security boundaries |

---

### 🛠️ 八、开发者工具 (Developer Tools)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud SDK | Cloud SDK | Google Cloud的命令行工具 / Command-line tools for Google Cloud |
| Cloud Code | Cloud Code | 用于云原生开发的IDE插件 / IDE extensions for cloud-native development |
| Cloud Shell | Cloud Shell | 基于浏览器的Shell环境 / Browser-based shell environment |
| Cloud Source Repositories | Cloud Source Repositories | 托管的源代码仓库 / Hosted source code repositories |
| Cloud Build | Cloud Build | 持续集成和交付 / Continuous integration and delivery |
| Cloud Deploy | Cloud Deploy | 托管的应用交付 / Managed application delivery |
| Artifact Registry | Artifact Registry | 通用包管理器 / Universal package manager |
| Container Registry | Container Registry | Docker镜像仓库 / Docker image registry |
| Cloud Profiler | Cloud Profiler | 持续CPU和内存分析 / Continuous CPU and memory profiling |
| Cloud Trace | Cloud Trace | 分布式跟踪系统 / Distributed tracing system |
| Cloud Debugger | Cloud Debugger | 实时应用调试 / Real-time application debugging |
| Cloud Monitoring | Cloud Monitoring | 基础设施和应用监控 / Infrastructure and application monitoring |
| Cloud Logging | Cloud Logging | 实时日志管理 / Real-time log management |
| Cloud Error Reporting | Cloud Error Reporting | 错误跟踪和报告 / Error tracking and reporting |
| Cloud APIs | Cloud APIs | 访问Google Cloud服务 / Access to Google Cloud services |
| Apigee API Management | Apigee API Management | 全生命周期API管理 / Full-lifecycle API management |
| API Gateway | API Gateway | 管理API访问 / Manage access to APIs |
| Endpoints | Cloud Endpoints | 分布式API管理 / Distributed API management |
| Service Mesh | Anthos Service Mesh | 托管的服务网格 / Managed service mesh |
| Cloud Scheduler | Cloud Scheduler | 托管的cron作业服务 / Managed cron job service |
| Cloud Tasks | Cloud Tasks | 异步任务执行 / Asynchronous task execution |
| Workflows | Workflows | 编排Google Cloud和HTTP API / Orchestrate Google Cloud and HTTP APIs |

---

### 🔧 九、管理与治理 (Management & Governance)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Cloud Console | Cloud Console | Google Cloud的Web界面 / Web interface for Google Cloud |
| Cloud Billing | Cloud Billing | 计费和成本管理工具 / Billing and cost management tools |
| Cost Management | Cost Management | 成本优化和报告 / Cost optimization and reporting |
| Cloud Billing API | Cloud Billing API | 程序化计费管理 / Programmatic billing management |
| Resource Manager | Resource Manager | 资源层次结构管理 / Resource hierarchy management |
| Cloud Asset Inventory | Cloud Asset Inventory | 资产管理和库存 / Asset management and inventory |
| Policy Analyzer | Policy Analyzer | 分析IAM策略 / Analyze IAM policies |
| Cloud IAM Recommender | IAM Recommender | 优化IAM策略 / Optimize IAM policies |
| Cloud APIs | Cloud APIs | Google Cloud服务API / APIs for Google Cloud services |
| Service Usage | Service Usage | 管理和监控API使用 / Manage and monitor API usage |
| Cloud Quotas | Cloud Quotas | 管理资源配额 / Manage resource quotas |
| Cloud Audit Logs | Cloud Audit Logs | 全面的操作日志 / Comprehensive operation logs |
| Cloud Monitoring | Cloud Monitoring | 指标、仪表板和警报 / Metrics, dashboards, and alerting |
| Cloud Logging | Cloud Logging | 日志管理和分析 / Log management and analysis |
| Cloud Debugger | Cloud Debugger | 实时调试 / Real-time debugging |
| Cloud Profiler | Cloud Profiler | 持续性能分析 / Continuous profiling |
| Cloud Trace | Cloud Trace | 请求跟踪 / Request tracing |
| Cloud Error Reporting | Cloud Error Reporting | 错误聚合 / Error aggregation |

---

### 🌍 十、混合云与多云 (Hybrid & Multi-cloud)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Anthos | Anthos | 跨云和本地环境的应用现代化平台 / Application modernization platform across clouds and on-premises |
| Anthos Clusters | Anthos Clusters | 在任何地方运行Kubernetes / Run Kubernetes anywhere |
| Anthos Service Mesh | Anthos Service Mesh | 托管的服务网格 / Managed service mesh |
| Anthos Config Management | Anthos Config Management | 配置和策略管理 / Configuration and policy management |
| Google Distributed Cloud | Google Distributed Cloud | 边缘和本地Google Cloud / Google Cloud at the edge and on-premises |
| Google Distributed Cloud Edge | Google Distributed Cloud Edge | 边缘计算解决方案 / Edge computing solutions |
| Google Distributed Cloud Hosted | Google Distributed Cloud Hosted | 隔离的本地部署 / Isolated on-premises deployments |
| VMware Engine | Google Cloud VMware Engine | 在Google Cloud上运行VMware / Run VMware on Google Cloud |
| Bare Metal Solution | Bare Metal Solution | 专用物理服务器 / Dedicated physical servers |
| Migrate for Anthos | Migrate for Anthos | 将VM迁移到容器 / Migrate VMs to containers |
| Migrate to Containers | Migrate to Containers | 自动将VM转换为容器 / Automatically convert VMs to containers |
| Rapid Migration Assessment | Rapid Migration Assessment | 快速评估迁移准备情况 / Rapid assessment of migration readiness |

---

### 📱 十一、移动与Web (Mobile & Web)

| 产品名称 (Product Name) | 英文名 (English Name) | 描述 (Description) |
|------------------------|----------------------|-------------------|
| Firebase | Firebase | 应用开发平台 / App development platform |
| Firebase Authentication | Firebase Authentication | 用户身份验证 / User authentication |
| Cloud Firestore | Cloud Firestore | 灵活的NoSQL数据库 / Flexible NoSQL database |
| Firebase Realtime Database | Firebase Realtime Database | 实时数据库 / Realtime database |
| Firebase Cloud Messaging | Firebase Cloud Messaging | 跨平台消息传递 / Cross-platform messaging |
| Firebase Crashlytics | Firebase Crashlytics | 实时崩溃报告 / Real-time crash reporting |
| Firebase Analytics | Google Analytics for Firebase | 免费的应用分析 / Free app analytics |
| Firebase Performance Monitoring | Firebase Performance Monitoring | 应用性能洞察 / App performance insights |
| Firebase Remote Config | Firebase Remote Config | 动态应用配置 / Dynamic app configuration |
| Firebase A/B Testing | Firebase A/B Testing | 应用实验 / App experimentation |
| Firebase App Distribution | Firebase App Distribution | Beta测试管理 / Beta testing management |
| Firebase Dynamic Links | Firebase Dynamic Links | 智能URL / Smart URLs |
| Firebase Hosting | Firebase Hosting | 快速安全的Web托管 / Fast and secure web hosting |
| Firebase Cloud Storage | Cloud Storage for Firebase | 存储用户生成的内容 / Store user-generated content |
| Firebase ML | Firebase ML | 移动设备上的机器学习 / Machine learning for mobile |
| Firebase Test Lab | Firebase Test Lab | 云设备测试 / Cloud device testing |
| Firebase Extensions | Firebase Extensions | 预打包解决方案 / Prepackaged solutions |
| Firebase In-App Messaging | Firebase In-App Messaging | 应用内消息传递 / In-app messaging |
| Firebase Predictions | Firebase Predictions | 用户行为预测 / User behavior predictions |
| Firebase App Check | Firebase App Check | 保护后端资源 / Protect backend resources |
| App Engine | App Engine | 构建可扩展的Web应用 / Build scalable web applications |

---

## Step 2: Search for Product Information (搜索产品信息)

### 2.1 构建搜索查询 / Construct Search Queries

根据目标产品，使用以下搜索模板查找官方信息：

**产品首页搜索 / Product Homepage Search**:
```
site:cloud.google.com [product-name] product
site:cloud.google.com/products [product-name]
```

**文档搜索 / Documentation Search**:
```
site:cloud.google.com/docs [product-name] overview
site:cloud.google.com/docs [product-name] quickstart
site:cloud.google.com/docs [product-name] api
```

**定价搜索 / Pricing Search**:
```
site:cloud.google.com [product-name] pricing
site:cloud.google.com/pricing [product-name]
```

**最佳实践搜索 / Best Practices Search**:
```
site:cloud.google.com/docs [product-name] best-practices
site:cloud.google.com/architecture [use-case]
```

### 2.2 执行搜索 / Execute Search

使用 `WebSearch` 工具执行上述查询，获取官方文档和产品页面的URL。

---

## Step 3: Retrieve and Extract Information (获取并提取信息)

### 3.1 获取产品首页信息 / Retrieve Product Homepage Info

访问产品首页获取核心信息：
- **官方URL格式**: `https://cloud.google.com/[product-name]`
- 使用 `Browser Navigate` 或 `WebFetch` 访问页面

**提取信息 / Information to Extract**:
1. **产品标语 (Tagline)**: 一句话价值主张
2. **核心功能 (Core Features)**: 主要能力列表
3. **应用场景 (Use Cases)**: 典型应用案例
4. **产品优势 (Advantages)**: 差异化优势
5. **架构图 (Architecture)**: 技术架构概述

### 3.2 获取技术文档 / Retrieve Technical Documentation

**文档URL格式 / Documentation URL Format**:
- 产品概览: `https://cloud.google.com/[product-name]/docs/overview`
- 快速入门: `https://cloud.google.com/[product-name]/docs/quickstart`
- API参考: `https://cloud.google.com/[product-name]/docs/reference`
- 定价说明: `https://cloud.google.com/[product-name]/pricing`

**常见产品代码 / Common Product Codes**:
| 产品 | URL路径 |
|------|---------|
| Compute Engine | compute |
| Cloud Storage | storage |
| Cloud SQL | sql |
| BigQuery | bigquery |
| GKE | kubernetes-engine |
| Cloud Functions | functions |
| Cloud Run | run |
| Pub/Sub | pubsub |
| Firestore | firestore |
| Memorystore | memorystore |
| VPC | vpc |
| Cloud CDN | cdn |
| Cloud Load Balancing | load-balancing |
| Cloud IAM | iam |
| Cloud Monitoring | monitoring |
| Cloud Logging | logging |
| Vertex AI | vertex-ai |

### 3.3 提取关键参数 / Extract Key Parameters

从产品文档中提取：
- **规格参数 (Specifications)**: 实例类型、性能指标、资源限制
- **定价信息 (Pricing)**: 计费模式、单价、免费额度
- **技术参数 (Technical Parameters)**: 配置选项、支持协议
- **限制说明 (Limits)**: 配额限制、使用限制

---

## Step 4: Integrate and Present Results (整合并呈现结果)

### 4.1 信息整合规则 / Information Integration Rules

1. **优先级 / Priority**:
   - 官方文档 > 产品首页 > 第三方来源
   - 最新版本 > 旧版本

2. **冲突处理 / Conflict Resolution**:
   - 以官方文档为准
   - 标注信息来源和时间

3. **完整性检查 / Completeness Check**:
   - 确保所有关键信息已填充
   - 缺失信息标注为"[未在公开资料中找到]"

### 4.2 输出模板 / Output Template

```markdown
# [产品中文名] | [Product English Name]

## 产品概述 (Product Overview)

**产品标语 (Tagline)**: [一句话描述]

**产品描述 (Description)**:
[中文描述]

[English Description]

**核心功能 (Core Features)**:
- [功能1] | [Feature 1]
- [功能2] | [Feature 2]
- ...

**应用场景 (Use Cases)**:
1. [场景1] | [Use Case 1]
2. [场景2] | [Use Case 2]
- ...

---

## 产品规格 (Specifications)

### 实例类型 / Instance Types
| 类型 (Type) | 规格 (Spec) | 适用场景 (Use Case) |
|------------|------------|-------------------|
| [类型1] | [规格1] | [场景1] |

### 支持地域 / Supported Regions
- [地域1] | [Region 1]
- [地域2] | [Region 2]

---

## 定价信息 (Pricing)

### 计费模式 / Billing Models
- **按量计费 (Pay-as-you-go)**: [描述]
- **承诺使用折扣 (Committed Use Discounts)**: [描述]

### 价格详情 / Price Details
| 资源类型 | 规格 | 价格 |
|---------|------|------|
| [资源] | [规格] | [价格] |

### 免费额度 / Free Tier
[免费额度说明]

---

## 快速入门 (Quick Start)

### 前提条件 (Prerequisites)
- [条件1] | [Requirement 1]
- [条件2] | [Requirement 2]

### 入门步骤 (Getting Started)
1. [步骤1] | [Step 1]
2. [步骤2] | [Step 2]

---

## 开发参考 (Development Reference)

### API 概览 / API Overview
**服务端点 / Service Endpoint**: `https://[service].googleapis.com`

### SDK 支持 / SDK Support
- **Java**: [Maven依赖]
- **Python**: [pip安装]
- **Go**: [go get]
- **Node.js**: [npm安装]

### 代码示例 / Code Example
```python
# 示例代码
from google.cloud import [service]

client = [service].Client()
```

---

## 相关资源 (Related Resources)

### 文档链接 / Documentation Links
- [产品文档](https://cloud.google.com/[product]/docs)
- [API参考](https://cloud.google.com/[product]/docs/reference)

### 相关产品 / Related Products
- [产品1] - [描述]
- [产品2] - [描述]
```

---

## Important Notes (重要说明)

### 信息准确性 / Information Accuracy
- 所有信息来源于Google Cloud官方公开文档
- 定价和规格可能变动，请以官网为准
- 部分详细参数可能需要登录后查看

### 工具限制 / Tool Limitations
- `WebFetch` 可能对部分动态页面返回错误
- 建议使用 `WebSearch` + `Browser Navigate` 组合
- 搜索摘要通常足以回答基础查询

### 凭证安全 / Credential Security
所有代码示例使用占位符：
- `<project-id>` - Google Cloud项目ID
- `<service-account-email>` - 服务账号邮箱
- `<region>` - 区域ID (如 us-central1)
- `<zone>` - 可用区ID (如 us-central1-a)

---

## Official Resources (官方资源)

- **官方网站**: https://cloud.google.com/
- **产品目录**: https://cloud.google.com/products
- **文档中心**: https://cloud.google.com/docs
- **定价计算器**: https://cloud.google.com/products/calculator
- **Google Cloud Console**: https://console.cloud.google.com/
