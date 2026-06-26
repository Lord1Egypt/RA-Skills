---
name: aliyun-global-search
description: Query Alibaba Cloud product information, documentation, parameters, features, and pricing from official sources without login. Use when the user asks about Alibaba Cloud products (ECS, RDS, OSS, SLB, etc.), needs product documentation, wants to compare product specifications, or needs help finding specific product parameters and features.
---

# Alibaba Cloud Product Query

This skill helps users find detailed information about Alibaba Cloud products by searching official documentation and product pages.

## When to Use

- User asks about specific Alibaba Cloud products (ECS, RDS, OSS, SLB, etc.)
- User needs product documentation or API references
- User wants to compare product specifications or pricing
- User needs help finding specific product parameters or features
- User mentions "阿里云" (Alibaba Cloud) and needs product information

## Step 1: Identify the Product

Determine which Alibaba Cloud product the user is asking about from the comprehensive product catalog below:

### 1.1 识别用户查询中的产品关键词

分析用户问题，提取以下信息：
- **产品名称**: 用户提到的具体产品名（如 ECS、RDS、OSS）
- **产品类别**: 用户可能提到的产品类别（如计算、数据库、存储）
- **功能需求**: 用户想要实现的功能（如搭建网站、数据备份、负载均衡）
- **使用场景**: 用户的业务场景（如电商、游戏、金融）

### 1.2 使用产品别名对照表

如果用户使用非标准名称，参考以下别名映射：

| 用户可能说的 | 对应产品 | 英文名 |
|-------------|---------|--------|
| 云服务器、虚拟机、VM、云主机 | ECS | Elastic Compute Service |
| 对象存储、云盘、云存储 | OSS | Object Storage Service |
| 负载均衡、SLB | SLB/ALB | Server Load Balancer |
| 数据库、MySQL、PostgreSQL、SQL Server | RDS/PolarDB | Relational Database |
| Redis、缓存 | Tair | Tair (Redis Compatible) |
| 大模型、通义千问、Qwen | 千问大模型 | Qwen |
| PAI、机器学习平台 | 人工智能平台 PAI | Platform for AI |
| 百炼、大模型平台 | 大模型服务平台百炼 | Bailian |
| 容器、K8s、Kubernetes | 容器服务 ACK | Container Service |
| 函数计算、Lambda | 函数计算 FC | Function Compute |
| 安全中心、云盾 | 云安全中心 | Security Center |
| WAF、防火墙 | Web应用防火墙 WAF | Web Application Firewall |
| CDN、加速 | CDN/ESA | Content Delivery Network |
| VPC、专有网络 | 专有网络 VPC | Virtual Private Cloud |
| 大数据、数仓 | MaxCompute/Hologres | Big Data Warehouse |
| Flink、实时计算 | 实时计算 Flink 版 | Realtime Compute |
| DataWorks、数据工场 | 大数据开发治理平台 | DataWorks |

### 1.3 确定目标产品

从产品目录中找到最匹配的产品，记录：
- 产品中文名
- 产品英文名
- 产品类别
- 产品代码（用于构造 URL）

---

## 📦 阿里云全产品目录 (Alibaba Cloud Full Product Catalog)

### 🖥️ 一、计算 (Compute) - 24 products

#### 弹性计算 (Elastic Compute)
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云服务器 ECS | Elastic Compute Service | 安全可靠、弹性可伸缩的云计算服务 |
| GPU 云服务器 | GPU Cloud Server | AI计算、图形渲染、仿真模拟的GPU算力平台 |
| 智能计算灵骏 | PAI-Lingjun | 面向万亿参数模型的新一代智能计算集群 |
| 弹性裸金属服务器 | Elastic Bare Metal Server | 可弹性伸缩的高性能物理服务器 |
| 轻量应用服务器 | Simple Application Server | 面向轻量应用场景的云服务器 |
| 弹性伸缩 | Elastic Scaling Service | 自动调整弹性计算资源的管理服务 |

#### 容器与Serverless
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 容器计算服务 ACS | Container Compute Service | 以K8s为界面的容器算力资源服务 |
| 容器服务 ACK | Container Service for Kubernetes | 企业级Kubernetes容器编排服务 |
| 容器镜像服务 ACR | Container Registry | 云原生制品安全托管及高效分发平台 |
| 服务网格 ASM | Service Mesh | 统一流量管理、观测及安全通信 |
| 分布式云容器平台 ACK One | ACK One | 混合云、多集群、分布式计算平台 |
| Serverless 应用引擎 SAE | Serverless App Engine | 微应用Serverless托管平台 |
| 函数计算 FC | Function Compute | 事件驱动的全托管计算服务 |
| 计算巢服务 | Compute Nest | 一站式软件云化平台 |

#### 高性能与边缘计算
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 弹性高性能计算 E-HPC | Elastic High Performance Computing | 自动化部署和管理HPC集群 |
| 边缘节点服务 ENS | Edge Node Service | 边缘计算节点服务 |
| 边缘安全加速 ESA | Edge Secure Acceleration | 全球3200+边缘节点的加速与防护 |
| 边缘网络加速 ENA | Edge Network Acceleration | 广覆盖、高可靠的网络连接服务 |

#### 终端用户计算
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 无影云电脑企业版 | Wuying Enterprise | 安全高效的云上办公解决方案 |
| 无影云电脑个人版 | Wuying Personal | 面向个人和家庭的云电脑 |
| 无影终端 | Wuying Terminal | 云上办公的全能入口硬件 |
| 无影云手机 | Wuying Cloud Phone | 集成AI Agent的云端虚拟手机 |
| 无影云应用 | Wuying Cloud App | 流式应用传输服务 |
| 无影 Agent 开发套件 AgentBay | AgentBay | 一站式构建数字员工 |

---

### 💾 二、存储 (Storage) - 15 products

#### 基础存储服务
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 对象存储 OSS | Object Storage Service | 海量、安全、低成本、高可靠的云存储 |
| 块存储 EBS | Elastic Block Storage | 低时延、高性能的块级别存储服务 |
| 文件存储 NAS | Network Attached Storage | 可弹性扩展的共享文件存储 |
| 文件存储 CPFS | Cloud Parallel File System | 全托管并行文件系统，高性能计算场景 |
| 表格存储 Tablestore | Tablestore | Serverless表存储，支持AI Agent Memory |
| 存储容量单位包 SCU | Storage Capacity Unit | 预付费存储售卖形态，抵扣多种存储产品 |

#### 存储数据服务
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云存储网关 | Cloud Storage Gateway | 本地与云端存储资源整合网关 |
| 混合云存储 | Hybrid Cloud Storage | 混合云存储阵列、CPFS、分布式存储 |
| 网盘与相册服务 | Drive & Photo Service | 为OpenClaw等提供云端存储支持 |

#### 灾备与迁移
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云备份 Cloud Backup | Cloud Backup | 统一灾备平台，数据管理服务 |
| 闪电立方 | Lightning Cube | 离线数据迁移服务 |

---

### 🌐 三、网络与CDN (Networking & CDN) - 19 products

#### 云上网络
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 专有网络 VPC | Virtual Private Cloud | 隔离的网络环境，逻辑上彻底隔离 |
| 弹性公网 IP | Elastic IP | 独立购买和持有的公网IPv4地址 |
| NAT 网关 | NAT Gateway | 全托管网络地址转换服务 |
| 负载均衡 SLB | Server Load Balancer | 流量分发服务，支持4/7层 |
| 应用型负载均衡 ALB | Application Load Balancer | 面向应用的L7负载均衡 |
| 网络智能服务 | Network Intelligence Service | 网络运维云服务，可视化管理 |
| 私网连接 PrivateLink | PrivateLink | 安全稳定的私网访问通道 |
| 云数据传输 CDT | Cloud Data Transfer | 网络带宽统一计费平台 |

#### 跨地域网络
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云企业网 CEN | Cloud Enterprise Network | 快速构建混合云和分布式系统的全球网络 |
| 转发路由器 TR | Transit Router | 企业级核心路由器，连接云上VPC |
| 全球加速 GA | Global Accelerator | 覆盖全球的互联网加速服务 |

#### 混合云网络
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| VPN 网关 | VPN Gateway | 加密通道连接企业数据中心和阿里云 |
| 高速通道 Express Connect | Express Connect | 物理专线连接，线下IDC专线接入 |
| 智能接入网关 | Smart Access Gateway | Internet就近加密接入 |
| 云连接器 | Cloud Connector | 物联网卡一站式定向上云连接 |

#### CDN与加速
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| CDN | Content Delivery Network | 内容分发网络，全球加速节点 |
| 全站加速 DCDN | Dynamic Route for CDN | 动静态内容加速 |
| 边缘安全加速 ESA | Edge Secure Acceleration | 全球加速+4/7层攻击防护 |

---

### 🗄️ 四、数据库 (Database) - 13 products

#### 关系型数据库
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云原生数据库 PolarDB | PolarDB | Super MySQL/PostgreSQL，支持集中式和分布式 |
| 云数据库 RDS | Relational Database Service | MySQL、PostgreSQL、SQL Server、MariaDB |
| 云数据库专属集群 MyBase | MyBase | 专为企业级数据库自建用户定制 |

#### NoSQL数据库
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云数据库 Tair | Tair (Redis Compatible) | 兼容Redis的高性能缓存和KV数据库 |
| 云原生多模数据库 Lindorm | Lindorm | 宽表、时序、时空、检索、向量多模型统一处理 |
| 云数据库 MongoDB 版 | ApsaraDB for MongoDB | 完全兼容MongoDB协议的文档数据库 |
| 云原生数据仓库 AnalyticDB | AnalyticDB | PB级实时数据仓库，兼容MySQL/PostgreSQL |
| 云数据库 ClickHouse | ClickHouse | 全托管实时数仓，社区版+云原生Serverless |
| 云数据库 SelectDB 版 | SelectDB | 基于Apache Doris的云原生实时数据仓库 |

#### 数据库工具与平台
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 数据传输服务 DTS | Data Transmission Service | 支持关系型、NoSQL、大数据间数据传输 |
| 数据库自治服务 DAS| HDM | Database Autonomy Service | 基于机器学习的数据库自治服务 |
| 数据库自治服务 HDM | Database Autonomy Service | 数据库自治服务 |
| 数据管理 DMS | Data Management Service | Data+AI一站式数据管理平台 |

---

### 🛡️ 五、安全 (Security) - 25 products

#### 云安全
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云安全中心 | Security Center | 集监测、防御、分析、响应于一体的安全管理平台 |
| DDoS 防护 | Anti-DDoS | L3-L7层DDoS攻击防护解决方案 |
| Web应用防火墙 WAF | Web Application Firewall | 业务流量恶意特征识别及防护 |
| 云防火墙 | Cloud Firewall | 多位一体的云上边界安全解决方案 |
| 主机安全 | Host Security | 多云主机和线下IDC威胁检测与响应 |
| 容器安全 | Container Security | 云原生容器全链路安全解决方案 |
| 云安全态势管理 | Cloud Security Posture Management | 多云环境配置风险检查及治理 |
| Agentic 安全运营中心 | Agentic SOC | 以Agentic AI为核心引擎的下一代安全运营平台 |

#### 网络安全
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云防火墙 NDR | Cloud Firewall NDR | 流量侧攻击事件关联溯源 |
| 办公安全平台 SASE | SASE | 一体化办公安全管控平台 |

#### 数据安全
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 数字证书管理服务 | SSL Certificates | 提供HTTPS加密协议访问 |
| 加密服务 | Encryption Service | 基于硬件加密机的云上数据加解密 |
| 密钥管理服务 KMS | Key Management Service | 一站式密钥管理和数据加密平台 |
| 数据安全中心 | Data Security Center | 敏感数据识别、分级分类、脱敏 |
| 数据库审计 | Database Audit | 数据库访问行为审计 |

#### 身份安全
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 访问控制 RAM | Resource Access Management | 用户身份与资源访问权限管理 |
| 运维安全中心（堡垒机） | Bastionhost | 运维和安全审计管控平台 |
| 实人认证 | ID Verification | 精准可靠的远程身份认证服务 |

#### 业务安全
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| AI 安全护栏 | AI Security Guardrails | AI应用、UGC内容审核与防护 |
| 内容安全 | Content Moderation | 图片、视频、文本、语音内容审核 |
| 风险识别 | Fraud Detection | 业务风险智能识别 |

#### 安全服务
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 安全管家服务 | Security Butler | 全方位安全技术和咨询服务 |
| 等保咨询服务 | MLPS Consulting | 等保咨询、测评一站式服务 |
| 评估加固服务 | Security Assessment | 基线加固和组件升级服务 |
| 渗透测试服务 | Penetration Testing | 挖掘业务流程中的安全缺陷 |

---

### 🤖 六、人工智能与机器学习 (AI & Machine Learning) - 31 products

#### 人工智能平台
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 人工智能平台 PAI | Platform for AI | AI标注、开发、训练、推理一体化全链路平台 |
| 大模型服务平台百炼 | Bailian | 一站式大模型服务与应用开发平台 |
| 千问大模型 | Qwen | 超强推理效果、超高性价比的大模型 |
| AI Stack | AI Stack | 企业私有化部署大模型软硬一体化方案 |

#### 机器学习与深度学习
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 智能推荐 AIRec | AIRec | 基于大数据和AI的个性化推荐服务 |
| 智能对话机器人 | Intelligent Dialogue Robot | 智能客服对话机器人平台 |
| 智能语音交互 | Intelligent Speech Interaction | 语音识别、语音合成、自然语言理解 |
| 自然语言处理 NLP | Natural Language Processing | 文本分析、情感分析、实体识别等 |
| 文字识别 OCR | Optical Character Recognition | 图片文字识别，支持10大类 |
| 图像搜索 | Image Search | 以图搜图服务 |

#### 视觉智能
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 视觉智能开放平台 | Vision Intelligence | 图像识别、视频分析、人脸人体等 |
| 视频点播 | ApsaraVideo for VOD | 音视频点播服务 |
| 视频直播 | ApsaraVideo Live | 直播采集、传输、处理、分发 |
| 超低延时直播 RTS | Real-time Streaming | 超低延时、高并发视频直播 |
| 智能媒体服务 IMS | Intelligent Media Services | 媒资管理、智能媒体处理、生产制作 |
| 云端智能剪辑 | Cloud-based Smart Editing | 直播剪辑、视频剪辑、数字人制作 |
| 智能媒资服务 | Intelligent Media Asset | 多媒体媒资管理和处理 |

#### AI应用与工具
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 智能编码助手通义灵码 | Tongyi Lingma | 基于通义大模型的智能编码辅助工具 |
| 智能科教内容生成平台 | AI Education Content | 面向教育出版的AIGC内容生成 |
| 营销引擎磐曦 | Marketing Engine | 大模型底座的泛行业营销引擎 |
| 信息查询服务 IQS | Information Query Service | 大模型友好的海量信息查询 |
| 智能联络中心 | AICC | 整合AI和语音通信的联络中心系统 |

#### 大模型原生应用
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 通义法睿 | Tongyi Farui | 法律智能助手，合同审查、法律咨询 |
| 全妙 | Quanmiao | 多模态内容创作工具 |

---

### 📊 七、大数据计算 (Big Data) - 16 products

#### 数据计算与分析
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云原生大数据计算服务 MaxCompute | MaxCompute | Serverless企业级SaaS模式云数据仓库 |
| 开源大数据平台 E-MapReduce | EMR | 智能数据湖方案，融合实时/离线/机器学习 |
| 实时数仓 Hologres | Hologres | 一体化实时湖仓平台 |
| 实时计算 Flink 版 | Realtime Compute for Flink | 基于Apache Flink的实时大数据计算 |
| 云数据库 ClickHouse | ClickHouse | 全托管实时数仓服务 |

#### 数据开发与治理
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 大数据开发治理平台 DataWorks | DataWorks | 一站式智能大数据开发治理平台 |
| 智能数据建设与治理 Dataphin | Dataphin | 采、建、管、用全生命周期平台 |
| 数据湖构建 Data Lake Formation | DLF | 统一数据湖表存储服务 |
| 数据集成 Data Integration | Data Integration | 稳定高效的数据同步平台 |

#### 数据分析与可视化
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 智能商业分析 Quick BI | Quick BI | AI时代的智能数据分析产品 |
| 日志服务 SLS | Log Service | 一站式数据采集、加工、分析、投递 |
| 云原生可观测 | Cloud Native Observability | 应用性能监控和可观测 |

#### 数据服务
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云行情 | Cloud Quotes | 一站式云行情产品服务 |
| 大数据专家服务 | Big Data Expert Service | 大数据技术咨询服务 |

---

### 🔄 八、中间件 (Middleware)

#### 消息队列
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云消息队列 RocketMQ 版 | RocketMQ | 低延迟、高性能、高可靠的消息中间件 |
| 云消息队列 Kafka 版 | Kafka | 高吞吐量分布式消息队列 |
| 云消息队列 RabbitMQ 版 | RabbitMQ | 兼容AMQP协议的消息队列 |
| 云消息队列 MQTT 版 | MQTT | 移动互联网、物联网消息产品 |
| 事件总线 EventBridge | EventBridge | 无服务器事件总线 |

#### 微服务与治理
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 微服务引擎 MSE | Microservices Engine | 注册配置中心、微服务治理 |
| 应用实时监控服务 ARMS | ARMS | 应用性能管理APM |
| 可观测链路 OpenTelemetry 版 | OpenTelemetry | 应用性能监控和分布式链路追踪 |
| 性能测试 PTS | Performance Testing Service | 云原生性能测试工具 |

---

### 📱 九、企业服务与通信

#### 钉钉与协作
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 专属钉钉 | DingTalk Exclusive | 企业数字化安全底座，混合云部署 |
| 钉钉会议 | DingTalk Meeting | 高清流畅、安全可靠的云会议 |
| 钉钉文档 | DingTalk Docs | 企业协同文档平台 |
| 智能客服 | Intelligent Customer Service | 云呼叫中心、对话机器人、智能外呼 |

#### 云通信
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 短信服务 | SMS | 验证码、通知、推广短信 |
| 语音服务 | Voice Service | 语音通知、语音验证码 |
| 号码隐私保护 | Privacy Number | 号码隐私保护能力 |
| 阿里邮箱 | Alibaba Mail | 高安全、高可用邮箱平台 |

---

### 🛠️ 十、开发与运维 (DevOps)

#### 开发工具
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 云效 | Cloud Effectiveness | 企业级一站式DevOps平台 |
| 代码管理 Codeup | Codeup | 代码托管、智能评审、质量检测 |
| 阿里云开发者社区 | Developer Community | 开发者学习交流平台 |

#### 运维管理
| 产品名称 | 英文名 | 描述 |
|---------|--------|------|
| 系统运维管理 OOS | OOS | 云上统一自动化管理与运维平台 |
| 云速搭 CADT | Cloud Architect Design Tools | 自助式云架构管理产品 |
| 操作审计 ActionTrail | ActionTrail | 云账号资源操作记录查询和投递 |
| 配置审计 | Config | 资源配置和合规审计 |

---

## Step 2: Construct Search Queries

Build targeted search queries for official sources based on the target region:

### 2.1 区域选择 (Region Selection)

根据用户所在区域或需求，选择对应的阿里云站点：

| 站点 | 域名 | 适用场景 |
|-----|------|---------|
| **中国站 (China)** | `https://www.aliyun.com/` | 中国大陆用户，中文文档，人民币计费 |
| **国际站 (International)** | `https://www.alibabacloud.com/` | 海外用户，多语言文档，美元计费 |

### 2.2 搜索查询格式 (Search Query Formats)

#### 中国站查询格式
```
Format: "[产品名] [信息类型] site:aliyun.com OR site:help.aliyun.com"

Examples:
- "ECS 计费 site:aliyun.com"
- "RDS 规格 site:help.aliyun.com"
- "OSS 功能 site:aliyun.com"
- "SLB 参数 site:help.aliyun.com"
- "PAI 文档 site:aliyun.com"
- "百炼 大模型 site:aliyun.com"
```

#### 国际站查询格式
```
Format: "alibaba cloud [product-name] [information-type] site:alibabacloud.com"

Examples:
- "alibaba cloud ECS pricing site:alibabacloud.com"
- "alibaba cloud RDS specifications site:alibabacloud.com"
- "alibaba cloud OSS features site:alibabacloud.com"
- "alibaba cloud SLB documentation site:alibabacloud.com"
- "alibaba cloud PAI machine learning site:alibabacloud.com"
```

### 2.3 混合搜索策略 (Hybrid Search Strategy)

如果无法确定用户所在区域，可同时搜索两个站点：

```
"[产品名] [信息类型] (site:aliyun.com OR site:alibabacloud.com)"
```

## Step 3: Retrieve Product Homepage Information

首先访问产品官网首页，获取产品的核心营销信息、功能亮点和架构概览。

### 3.1 产品首页 URL 构造

| 站点 | 产品首页 URL 模式 | 示例 |
|-----|------------------|------|
| **中国站** | `https://www.aliyun.com/product/[product-code]` | `https://www.aliyun.com/product/ecs` |
| **国际站** | `https://www.alibabacloud.com/product/[product-code]` | `https://www.alibabacloud.com/product/ecs` |

### 3.2 产品首页信息提取清单

访问产品首页后，提取以下关键信息：

#### 3.2.1 产品核心信息 (Core Product Info)
- **产品 Slogan/标语**: 首页主标题，一句话描述产品核心价值
- **产品定位**: 产品类别和主要用途
- **核心卖点**: 首页突出展示的 3-5 个主要优势

#### 3.2.2 功能特性 (Feature Highlights)
- **功能模块卡片**: 首页展示的功能模块（通常以图标+标题+描述形式）
- **特性对比**: 与竞品或自建方案的对比优势
- **应用场景图标**: 支持的主要应用场景

#### 3.2.3 产品架构 (Architecture)
- **架构图**: 产品技术架构示意图
- **核心组件**: 产品包含的主要组件或服务
- **工作流程**: 产品使用流程图

#### 3.2.4 客户案例与认证 (Social Proof)
- **客户 Logo**: 使用该产品的知名企业
- **行业覆盖**: 支持的主要行业
- **认证标识**: 安全合规认证标志

#### 3.2.5 入门与定价入口 (CTA & Pricing)
- **免费试用**: 是否有免费试用入口
- **定价链接**: 定价页面的直接链接
- **文档入口**: 帮助文档的快速链接

### 3.3 产品首页信息记录模板

```
产品首页信息摘要:
├── 产品标语: [主标题]
├── 核心卖点:
│   ├── [卖点1]
│   ├── [卖点2]
│   └── [卖点3]
├── 功能模块:
│   ├── [模块1]: [描述]
│   ├── [模块2]: [描述]
│   └── [模块3]: [描述]
├── 应用场景: [场景1, 场景2, 场景3]
├── 架构概览: [简要描述]
└── 关键入口:
    ├── 免费试用: [是/否]
    ├── 定价页面: [URL]
    └── 帮助文档: [URL]
```

---

## Step 4: Search Official Documentation

在获取产品首页信息后，结合以下官方文档来源进行深度信息检索。

> **注意 / Note**: 以下 URL 模式适用于中国站。如果是国际站，请将域名替换为 `alibabacloud.com` 并调整语言路径。
> The following URL patterns apply to China site. For International site, replace domain with `alibabacloud.com` and adjust language paths.

### 3.1 中国站 vs 国际站域名对照 (China vs International Site Domains)

| 资源类型 | 中国站 (China) | 国际站 (International) |
|---------|---------------|----------------------|
| **官网首页** | `https://www.aliyun.com/` | `https://www.alibabacloud.com/` |
| **帮助文档** | `https://help.aliyun.com/zh/[product]/` | `https://www.alibabacloud.com/help/en/[product]/` |
| **产品页面** | `https://www.aliyun.com/product/[code]` | `https://www.alibabacloud.com/product/[code]` |
| **定价页面** | `https://www.aliyun.com/price/detail/[code]` | `https://www.alibabacloud.com/pricing/detail/[code]` |

### 3.2 产品概述文档来源 (Product Overview Sources)

#### 中国站 URL 模式
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Product Homepage** | `https://www.aliyun.com/product/[product-code]` | Product introduction, key features, architecture |
| **Documentation Portal** | `https://help.aliyun.com/zh/[product-code]/` | Main documentation entry point |
| **What is [Product]** | `https://help.aliyun.com/zh/[product-code]/product-overview/what-is-*` | Product definition and overview |
| **Features Page** | `https://help.aliyun.com/zh/[product-code]/product-overview/features-*` | Detailed feature descriptions |
| **Architecture/Editions** | `https://help.aliyun.com/zh/[product-code]/product-overview/product-editions` | Product series and editions |
| **Scenarios** | `https://help.aliyun.com/zh/[product-code]/product-overview/scenarios` | Use cases and scenarios |
| **Release Notes** | `https://help.aliyun.com/zh/[product-code]/product-overview/announcements-*` | Latest updates and announcements |

#### 国际站 URL 模式
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Product Homepage** | `https://www.alibabacloud.com/product/[product-code]` | Product introduction, key features |
| **Documentation Portal** | `https://www.alibabacloud.com/help/en/[product-code]/` | Main documentation entry point |
| **What is [Product]** | `https://www.alibabacloud.com/help/en/[product-code]/what-is-*` | Product definition and overview |
| **Features Page** | `https://www.alibabacloud.com/help/en/[product-code]/features-*` | Detailed feature descriptions |

### 3.3 产品计费文档来源 (Pricing Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Pricing Page** | `https://www.aliyun.com/price/detail/[product-code]` | Official pricing details |
| **Billable Items** | `https://help.aliyun.com/zh/[product-code]/product-overview/billable-*` | What components are charged |
| **Pricing Overview** | `https://help.aliyun.com/zh/[product-code]/product-overview/pricing-*` | Billing methods and models |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Pricing Page** | `https://www.alibabacloud.com/pricing/detail/[product-code]` | Official pricing details |
| **Pricing Calculator** | `https://www.alibabacloud.com/price-calculator` | Cost estimation tool |

### 3.4 快速入门文档来源 (Quick Start Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Quick Start Hub** | `https://help.aliyun.com/zh/[product-code]/getting-started` | Getting started guides index |
| **Quick Start Guide** | `https://help.aliyun.com/zh/[product-code]/getting-started/quick-start` | Step-by-step initial setup |
| **Limits & Quotas** | `https://help.aliyun.com/zh/[product-code]/product-overview/limits-*` | Usage restrictions and quotas |
| **Regions & Zones** | `https://help.aliyun.com/zh/[product-code]/user-guide/regions-*` | Supported regions documentation |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Quick Start Hub** | `https://www.alibabacloud.com/help/en/[product-code]/getting-started` | Getting started guides |
| **Developer Guide** | `https://www.alibabacloud.com/help/en/[product-code]/developer-reference` | Developer resources |

### 3.5 操作指南文档来源 (Operation Guide Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **User Guide Hub** | `https://help.aliyun.com/zh/[product-code]/user-guide` | All operation guides index |
| **Instance Management** | `https://help.aliyun.com/zh/[product-code]/user-guide/instance-*` | Create, manage, delete instances |
| **Configuration** | `https://help.aliyun.com/zh/[product-code]/user-guide/configure-*` | Parameter and settings guides |
| **Network & Security** | `https://help.aliyun.com/zh/[product-code]/user-guide/network-*` | VPC, security group configuration |
| **Backup & Recovery** | `https://help.aliyun.com/zh/[product-code]/user-guide/backup-*` | Backup policies and disaster recovery |
| **Monitoring** | `https://help.aliyun.com/zh/[product-code]/user-guide/monitor-*` | CloudMonitor integration |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **User Guide Hub** | `https://www.alibabacloud.com/help/en/[product-code]/user-guide` | Operation guides |
| **Instance Management** | `https://www.alibabacloud.com/help/en/[product-code]/instance-*` | Instance operations |

### 3.6 实践教程文档来源 (Practice Tutorial Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Use Cases Hub** | `https://help.aliyun.com/zh/[product-code]/use-cases` | All tutorials and best practices |
| **Best Practices** | `https://help.aliyun.com/zh/[product-code]/use-cases/best-practice-*` | Optimization guides |
| **Scenario Solutions** | `https://help.aliyun.com/zh/[product-code]/use-cases/[scenario]-*` | Industry-specific solutions |
| **Migration Guides** | `https://help.aliyun.com/zh/[product-code]/user-guide/migration-*` | Data migration procedures |
| **Video Tutorials** | `https://help.aliyun.com/zh/[product-code]/videos/*` | Video learning resources |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Tutorials** | `https://www.alibabacloud.com/help/en/[product-code]/tutorials` | Step-by-step tutorials |
| **Best Practices** | `https://www.alibabacloud.com/help/en/[product-code]/best-practices` | Best practice guides |

### 3.7 安全合规文档来源 (Security & Compliance Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Security Hub** | `https://help.aliyun.com/zh/[product-code]/security-compliance` | Security documentation index |
| **Security Whitepaper** | `https://help.aliyun.com/zh/[product-code]/security-compliance/security-whitepaper` | Security architecture |
| **Compliance** | `https://help.aliyun.com/zh/[product-code]/security-compliance/compliance-*` | Compliance certifications |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **Security** | `https://www.alibabacloud.com/help/en/[product-code]/security` | Security documentation |
| **Compliance Center** | `https://www.alibabacloud.com/trust-center` | Global compliance certifications |

### 3.8 开发参考文档来源 (Development Reference Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **API Reference Hub** | `https://help.aliyun.com/zh/[product-code]/developer-reference` | All developer resources |
| **API Overview** | `https://help.aliyun.com/zh/[product-code]/developer-reference/api-*` | API documentation entry |
| **SDK Reference** | `https://help.aliyun.com/zh/[product-code]/developer-reference/sdk-*` | SDK downloads and guides |
| **CLI Examples** | `https://help.aliyun.com/zh/[product-code]/developer-reference/alibaba-cloud-cli-*` | CLI usage examples |
| **Terraform** | `https://help.aliyun.com/zh/[product-code]/developer-reference/use-terraform` | Terraform provider docs |
| **ROS Examples** | `https://help.aliyun.com/zh/[product-code]/developer-reference/use-ros` | Resource Orchestration templates |
| **OpenAPI Explorer** | `https://api.aliyun.com/?product=[ProductCode]` | Interactive API testing |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **API Reference** | `https://www.alibabacloud.com/help/en/[product-code]/api-reference` | API documentation |
| **SDK Reference** | `https://www.alibabacloud.com/help/en/[product-code]/sdk-reference` | SDK guides |
| **Terraform Registry** | `https://registry.terraform.io/providers/aliyun/alicloud/latest/docs` | Terraform provider |
| **OpenAPI Explorer** | `https://api.alibabacloud.com/?product=[ProductCode]` | Interactive API testing |

### 3.9 常见问题文档来源 (FAQ Sources)

#### 中国站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **FAQ Hub** | `https://help.aliyun.com/zh/[product-code]/faq-overview` | All FAQs index |
| **Product FAQ** | `https://help.aliyun.com/zh/[product-code]/product-overview/faq` | Product-specific questions |
| **Troubleshooting** | `https://help.aliyun.com/zh/[product-code]/troubleshooting` | Common issues and solutions |

#### 国际站
| Source Type | URL Pattern | Content Type |
|-------------|-------------|--------------|
| **FAQ** | `https://www.alibabacloud.com/help/en/[product-code]/faq` | Frequently asked questions |
| **Troubleshooting** | `https://www.alibabacloud.com/help/en/[product-code]/troubleshooting` | Issue resolution |

### 3.10 通用搜索策略 (General Search Strategy)

#### 中国站搜索查询
```
# 中文搜索 (推荐用于中文文档)
site:aliyun.com OR site:help.aliyun.com [产品名] [信息类型]

# 示例查询
- "ECS 计费 site:aliyun.com"
- "RDS 快速入门 site:help.aliyun.com"
- "OSS API site:help.aliyun.com"
- "SLB 最佳实践 site:aliyun.com"
```

#### 国际站搜索查询
```
# 英文搜索 (用于国际站文档)
site:alibabacloud.com [product-name] [information-type]

# 示例查询
- "ECS pricing site:alibabacloud.com"
- "RDS getting started site:alibabacloud.com"
- "OSS API reference site:alibabacloud.com"
- "SLB best practices site:alibabacloud.com"
```

#### 混合搜索 (当不确定用户区域时)
```
# 同时搜索两个站点
[产品名/ product-name] [信息类型] (site:aliyun.com OR site:alibabacloud.com)
```

## Step 5: Extract Key Information from Documentation

Based on the standard Alibaba Cloud documentation architecture (as observed in ECS, RDS, and other products), extract and organize information from the following documentation sections:

### 4.1 产品概述 (Product Overview)
- **Product Introduction**: What the product is and its core value proposition
- **Product Architecture**: Technical architecture diagrams and component relationships
- **Features & Capabilities**: Key features and functional modules
- **Product Editions/Series**: Different editions (e.g., Standard, Enterprise, Serverless)
- **Storage/Compute Types**: Available storage or compute type options
- **Use Cases**: Typical application scenarios and industry solutions
- **Competitive Advantages**: Comparison with self-managed or competitor solutions
- **Release Notes & Updates**: Latest features, version updates, and announcements

### 4.2 产品计费 (Product Pricing)
- **Billable Items**: What components are charged (compute, storage, network, etc.)
- **Billing Methods**: 
  - Pay-as-you-go (按量付费)
  - Subscription (包年包月)
  - Serverless billing (Serverless按量)
  - Reserved instances (预留实例)
- **Pricing Tiers**: Different price levels based on specifications
- **Free Tier**: Free quota or trial availability
- **Cost Optimization**: Best practices for cost reduction
- **Pricing Calculator**: How to estimate costs

### 4.3 快速入门 (Quick Start)
- **Prerequisites**: Account requirements, permissions, and preparation
- **Usage Limits**: Quotas, constraints, and restrictions
- **Region & Zone Availability**: Supported regions and availability zones
- **Getting Started Guide**: Step-by-step initial setup
- **First Instance/Resource Creation**: Console walkthrough
- **Connection Methods**: How to connect to the service
- **Quick Start Videos**: Video tutorials for beginners

### 4.4 操作指南 (Operation Guide)
- **Instance/Resource Management**:
  - Create, modify, delete operations
  - Start, stop, restart procedures
  - Scaling and capacity adjustments
  - Release and recycling
- **Configuration Management**:
  - Parameter settings and tuning
  - Network configuration (VPC, security groups)
  - Storage management and expansion
  - Backup and snapshot policies
- **Monitoring & Operations**:
  - Cloud monitoring integration
  - Alert rules and notifications
  - Log management and analysis
  - Performance diagnostics
- **High Availability & Disaster Recovery**:
  - Multi-zone deployment
  - Read replicas and load balancing
  - Failover mechanisms
  - Cross-region replication

### 4.5 实践教程 (Practice Tutorials)
- **Environment Setup**: Development, testing, and production environment configuration
- **Application Deployment**: Deploying common applications (WordPress, Magento, etc.)
- **Data Migration**: Migration tools and procedures from on-premise or other clouds
- **Best Practices**:
  - Performance optimization
  - Security hardening
  - Cost optimization
  - High availability architecture design
- **Scenario-based Solutions**: Industry-specific solutions (e-commerce, gaming, finance)
- **Video Tutorials**: Step-by-step video guides

### 4.6 安全合规 (Security & Compliance)
- **Security Features**: Built-in security capabilities
- **Security Responsibility Model**: Shared responsibility between Alibaba Cloud and users
- **Data Protection**: Encryption at rest and in transit
- **Access Control**: RAM policies, authentication mechanisms
- **Compliance Certifications**: ISO, SOC, PCI DSS, MLPS (等保) compliance
- **Security Best Practices**: Recommended security configurations
- **Audit & Governance**: Operation audit logs and compliance monitoring

### 4.7 开发参考 (Development Reference)
- **API Reference**:
  - API overview and authentication
  - Request/response formats
  - Error codes and handling
  - Rate limits and quotas
- **SDK Support**: Available SDKs (Java, Python, Go, Node.js, etc.)
- **CLI Integration**: Alibaba Cloud CLI usage examples
- **Infrastructure as Code**:
  - Terraform provider and examples
  - Resource Orchestration Service (ROS) templates
  - Pulumi support
- **Developer Tools**: OpenAPI Explorer, SDK sample code
- **Performance Whitepapers**: Benchmarks and performance testing guides

### 5.8 常见问题 (FAQ)
- **Product FAQs**: Common questions and answers
- **Troubleshooting**: Common issues and solutions
- **Error Messages**: Error code explanations and fixes
- **Limitations & Constraints**: Known limitations and workarounds

---

## Step 6: Integrate and Synthesize Information

综合产品首页信息 (Step 3) 和官方文档信息 (Step 5)，进行信息融合和交叉验证。

### 6.1 信息融合策略 (Information Integration Strategy)

| 信息类型 | 产品首页 (Step 3) | 官方文档 (Step 5) | 融合方式 |
|---------|------------------|------------------|---------|
| **产品定位** | 营销角度，突出卖点 | 技术角度，准确描述 | 以文档为准，首页补充营销亮点 |
| **功能特性** | 核心功能卡片 | 详细功能列表 | 合并去重，文档补充技术细节 |
| **应用场景** | 主要场景图标 | 详细场景描述 | 整合为完整场景列表 |
| **产品架构** | 架构示意图 | 架构技术文档 | 结合图文描述 |
| **定价信息** | 定价入口链接 | 详细计费说明 | 以文档详细计费为准 |
| **技术参数** | 关键指标展示 | 完整参数列表 | 以文档完整参数为准 |

### 6.2 信息验证清单 (Information Verification Checklist)

在输出前，验证以下信息的一致性：

- [ ] **产品名称**: 首页和文档中的产品名称是否一致
- [ ] **功能描述**: 首页卖点与文档功能描述是否匹配
- [ ] **应用场景**: 首页展示场景是否在文档中有详细说明
- [ ] **定价信息**: 首页定价入口与文档计费说明是否一致
- [ ] **技术架构**: 首页架构图与文档架构描述是否吻合

### 6.3 冲突解决原则 (Conflict Resolution Principles)

当产品首页与文档信息冲突时：

1. **技术参数冲突**: 以官方文档为准，文档通常更准确
2. **功能描述冲突**: 以文档为准，首页可能简化描述
3. **定价信息冲突**: 以定价页面为准，注意时效性
4. **版本信息冲突**: 以文档为准，首页可能未及时更新

### 6.4 信息补充策略 (Information Supplement Strategy)

- **首页有，文档无**: 记录首页信息，标注"来自产品首页"
- **文档有，首页无**: 正常纳入输出
- **两者都有，内容不同**: 优先采用文档信息，首页作为补充视角
- **两者都有，内容一致**: 增强信息可信度

---

## Step 7: Present Results

Based on the information extracted in Step 3 (Product Homepage) and Step 5 (Documentation), integrated in Step 6, format the output following this comprehensive structure. Include only sections where information was found:

```markdown
# [产品名称 / Product Name] - [产品英文名 / English Name]

> [一句话产品描述 / One-line product description - 融合首页Slogan和文档描述]

---

## 一、产品概述 (Product Overview)

### 1.1 产品简介 (Product Introduction)
**产品定位**: [来自首页的产品定位 + 来自文档的技术定义]

**核心价值主张**: [首页主标语/Slogan]

**产品描述**: [来自文档的详细产品描述]

### 1.2 产品架构 (Product Architecture)
**架构概览**: [首页架构图描述 + 文档架构说明]

**核心组件**: 
- [组件1]: [来自首页或文档的描述]
- [组件2]: [来自首页或文档的描述]
- [组件3]: [来自首页或文档的描述]

### 1.3 功能特性 (Features & Capabilities)
**首页核心卖点** (来自产品首页):
- [卖点1]: [首页展示的核心优势]
- [卖点2]: [首页展示的核心优势]
- [卖点3]: [首页展示的核心优势]

**详细功能列表** (来自官方文档):
| 功能模块 | 功能描述 | 信息来源 |
|---------|---------|---------|
| [功能1] | [描述] | 首页/文档 |
| [功能2] | [描述] | 首页/文档 |
| [功能3] | [描述] | 首页/文档 |

### 1.4 产品系列/版本 (Product Editions)
| 版本/系列 | 适用场景 | 主要特性 | 信息来源 |
|----------|---------|---------|---------|
| [版本1] | [场景] | [特性] | 首页/文档 |
| [版本2] | [场景] | [特性] | 首页/文档 |

### 1.5 应用场景 (Use Cases)
**首页展示场景**:
- [首页场景1]: [简要描述]
- [首页场景2]: [简要描述]

**文档详细场景**:
- **[场景1]**: [来自文档的详细描述]
- **[场景2]**: [来自文档的详细描述]
- **[场景3]**: [来自文档的详细描述]

### 1.6 竞争优势 (Competitive Advantages)
**首页强调优势**:
[首页展示的与竞品对比的核心优势]

**文档详细对比**:
[与自建或竞品的详细对比优势]

---

## 二、产品计费 (Product Pricing)

### 2.1 计费项 (Billable Items)
| 计费组件 | 计费说明 |
|---------|---------|
| [组件1] | [说明] |
| [组件2] | [说明] |

### 2.2 计费方式 (Billing Methods)
| 计费方式 | 说明 | 适用场景 |
|---------|------|---------|
| 按量付费 | [说明] | [场景] |
| 包年包月 | [说明] | [场景] |
| Serverless | [说明] | [场景] |

### 2.3 价格参考 (Pricing Reference)
- **起步价格**: [价格] (如可获取)
- **免费额度**: [是/否/详情]
- **计费计算器**: [链接]

### 2.4 成本优化建议 (Cost Optimization)
[成本优化最佳实践]

---

## 三、快速入门 (Quick Start)

### 3.1 使用限制 (Usage Limits)
| 限制项 | 限制值 | 说明 |
|-------|-------|------|
| [限制1] | [值] | [说明] |
| [限制2] | [值] | [说明] |

### 3.2 地域可用区 (Region & Zone Availability)
**支持的地域**: [列出主要地域]

### 3.3 入门步骤 (Getting Started Steps)
1. [步骤1]
2. [步骤2]
3. [步骤3]

### 3.4 连接方式 (Connection Methods)
[如何连接到该服务]

---

## 四、操作指南 (Operation Guide)

### 4.1 实例/资源管理 (Instance/Resource Management)
#### 创建实例
[创建步骤和关键参数]

#### 管理操作
| 操作 | 说明 | 注意事项 |
|-----|------|---------|
| 启动 | [说明] | [注意] |
| 停止 | [说明] | [注意] |
| 重启 | [说明] | [注意] |
| 释放 | [说明] | [注意] |

#### 扩缩容
[如何调整资源配置]

### 4.2 配置管理 (Configuration Management)
#### 关键参数
| 参数名 | 默认值 | 可选项 | 说明 |
|-------|-------|-------|------|
| [参数1] | [值] | [选项] | [说明] |
| [参数2] | [值] | [选项] | [说明] |

#### 网络配置
[VPC、安全组等网络设置]

#### 存储管理
[存储类型、扩容、备份策略]

### 4.3 监控与运维 (Monitoring & Operations)
#### 监控指标
| 指标 | 说明 | 告警建议 |
|-----|------|---------|
| [指标1] | [说明] | [建议] |
| [指标2] | [说明] | [建议] |

#### 日志管理
[日志收集和分析]

### 4.4 高可用与容灾 (High Availability & Disaster Recovery)
[多可用区部署、故障切换、备份恢复策略]

---

## 五、实践教程 (Practice Tutorials)

### 5.1 环境搭建 (Environment Setup)
[开发、测试、生产环境配置建议]

### 5.2 典型应用场景部署 (Application Deployment)
#### [场景1: 如电商网站]
[部署架构和步骤]

#### [场景2: 如数据分析]
[部署架构和步骤]

### 5.3 数据迁移 (Data Migration)
[从其他平台迁移到阿里云的方法]

### 5.4 最佳实践 (Best Practices)
#### 性能优化
[性能调优建议]

#### 安全加固
[安全配置建议]

#### 成本优化
[成本控制建议]

#### 高可用架构
[高可用设计模式]

---

## 六、安全合规 (Security & Compliance)

### 6.1 安全功能 (Security Features)
[内置安全能力]

### 6.2 责任共担模型 (Security Responsibility Model)
| 阿里云责任 | 用户责任 |
|-----------|---------|
| [责任1] | [责任1] |
| [责任2] | [责任2] |

### 6.3 数据保护 (Data Protection)
- **传输加密**: [加密方式]
- **存储加密**: [加密方式]

### 6.4 合规认证 (Compliance Certifications)
[ISO, SOC, 等保等认证]

---

## 七、开发参考 (Development Reference)

### 7.1 API 概览 (API Overview)
#### 认证方式
[AccessKey、STS等认证方法]

#### 常用API
| API | 功能 | 文档链接 |
|-----|------|---------|
| [API1] | [功能] | [链接] |
| [API2] | [功能] | [链接] |

#### 错误码 (Error Codes)
| 错误码 | 说明 | 处理建议 |
|-------|------|---------|
| [Code1] | [说明] | [建议] |

### 7.2 SDK 支持 (SDK Support)
| 语言 | SDK下载 | 示例代码 |
|-----|---------|---------|
| Java | [链接] | [链接] |
| Python | [链接] | [链接] |
| Go | [链接] | [链接] |
| Node.js | [链接] | [链接] |

### 7.3 阿里云 CLI (Alibaba Cloud CLI)
```bash
# 常用命令示例
aliyun [product] [action] --parameter value
```

### 7.4 基础设施即代码 (Infrastructure as Code)
#### Terraform
```hcl
# Terraform示例代码
resource "alicloud_[product]" "example" {
  # 配置参数
}
```

#### ROS 模板
[资源编排服务模板示例]

### 7.5 性能白皮书 (Performance Whitepaper)
[性能基准测试报告链接]

---

## 八、常见问题 (FAQ)

### 8.1 产品常见问题 (Product FAQs)
**Q: [问题1]?**
A: [答案1]

**Q: [问题2]?**
A: [答案2]

### 8.2 故障排查 (Troubleshooting)
| 问题现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| [现象1] | [原因] | [方案] |
| [现象2] | [原因] | [方案] |

### 8.3 已知限制 (Known Limitations)
[产品已知限制和规避方法]

---

## 九、相关资源 (Related Resources)

### 9.1 官方文档链接 (Documentation Links)
| 资源 | 链接 |
|-----|------|
| 产品首页 | [链接] |
| 文档中心 | [链接] |
| API参考 | [链接] |
| 定价页面 | [链接] |
| 快速入门 | [链接] |
| 最佳实践 | [链接] |

### 9.2 相关产品和服务 (Related Products)
- **[产品1]**: [关系说明]
- **[产品2]**: [关系说明]

### 9.3 技术支持 (Technical Support)
- **官方文档**: https://help.aliyun.com/zh/[product-code]/
- **社区论坛**: https://developer.aliyun.com/
- **工单支持**: 阿里云控制台提交工单
```

### Output Guidelines

1. **Prioritize based on user query**: Focus on sections most relevant to the user's question
2. **Use tables for structured data**: Specifications, pricing tiers, parameters, comparisons
3. **Include code blocks for**: CLI commands, API examples, Terraform configurations
4. **Provide direct links**: Always include URLs to official documentation
5. **Mark unavailable info**: Use "[信息未获取 / Information not available]" if search yields no results
6. **Bilingual headers**: Use both Chinese and English for section titles
7. **Be concise**: Avoid lengthy explanations; use bullet points and tables

## Tips for Better Results

1. **Use English product names** in searches for better documentation results
2. **Include "documentation" or "API"** for technical details
3. **Include "pricing"** for cost information
4. **Check multiple sources** - product page, docs, and API reference
5. **Note region availability** - some features vary by region

## Limitations

- Cannot access internal or authenticated-only documentation
- Pricing may not reflect real-time changes
- Some enterprise-specific features may not be publicly documented
- API rate limits and quotas not always publicly available
