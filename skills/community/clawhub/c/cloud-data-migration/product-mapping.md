# 云厂商产品映射表 | Cloud Vendor Product Mapping

本文档提供详细的跨云产品映射关系，用于数据迁移方案设计。

## 1. 关系型数据库映射 / Relational Database Mapping

### 1.1 MySQL 产品映射

| 云厂商 | 产品名称 | 版本支持 | 关键特性 | 迁移工具 |
|--------|---------|---------|---------|---------|
| **AWS** | Amazon RDS MySQL | 5.6, 5.7, 8.0 | Multi-AZ, 只读副本, 自动备份 | AWS DMS, mysqldump |
| **Azure** | Azure Database for MySQL | 5.6, 5.7, 8.0 | 灵活服务器, 高可用 | Azure DMS, MySQL Workbench |
| **GCP** | Cloud SQL MySQL | 5.6, 5.7, 8.0 | 自动扩展, 私有IP | Database Migration Service |
| **阿里云** | RDS MySQL | 5.6, 5.7, 8.0 | 三节点企业版, Proxy | DTS, 闪电立方 |
| **阿里云** | PolarDB MySQL | 5.6, 5.7, 8.0 | 计算存储分离, 一写多读, 秒级扩容 | DTS, PolarDB迁移工具 |
| **阿里云** | PolarDB-X | 5.7, 8.0 | 分布式关系型数据库, 水平扩展, HTAP | DTS, Canal, Flink CDC |
| **华为云** | RDS MySQL | 5.6, 5.7, 8.0 | 主备版, 金融版 | DRS, mysqldump |
| **华为云** | GaussDB(for MySQL) | 5.7, 8.0 | 计算存储分离, 一写多读, 共享存储 | DRS, mysqldump |
| **腾讯云** | TDSQL-C MySQL | 5.7, 8.0 | Serverless, 计算存储分离 | DTS |
| **火山引擎** | RDS MySQL | 5.7, 8.0 | 高可用版, 基础版 | DTS |

### 1.2 PostgreSQL 产品映射

| 云厂商 | 产品名称 | 版本支持 | 关键特性 | 迁移工具 |
|--------|---------|---------|---------|---------|
| **AWS** | Amazon RDS PostgreSQL | 11-15 | Multi-AZ, 只读副本 | AWS DMS, pg_dump |
| **Azure** | Azure Database for PostgreSQL | 11-15 | 灵活服务器, Hyperscale | Azure DMS, pg_dump |
| **GCP** | Cloud SQL PostgreSQL | 11-15 | 自动备份, 时间点恢复 | Database Migration Service |
| **阿里云** | RDS PostgreSQL | 11-15 | 云盘版, 本地SSD版 | DTS |
| **阿里云** | PolarDB PostgreSQL | 11, 14, 15 | 计算存储分离, Oracle语法兼容 | DTS, pg_dump |
| **阿里云** | PolarDB PostgreSQL(兼容Oracle) | 14 | Oracle语法兼容, 存储过程迁移 | ADAM评估+DTS |
| **华为云** | RDS PostgreSQL | 11-15 | 主备版, 只读副本 | DRS |
| **华为云** | GaussDB(for openGauss) | 2.0-3.0 | 分布式/主备, 自研内核, 高可用 | DRS, gs_dump |
| **腾讯云** | TDSQL-C PostgreSQL | 11-15 | Serverless架构 | DTS |

### 1.3 SQL Server 产品映射

| 云厂商 | 产品名称 | 版本支持 | 关键特性 | 迁移工具 |
|--------|---------|---------|---------|---------|
| **AWS** | Amazon RDS SQL Server | 2016-2022 | Multi-AZ, SSRS, SSAS | AWS DMS, Native Backup |
| **Azure** | Azure SQL Database | 2019-2022 | 无服务器, 超大规模 | Azure DMS, BACPAC |
| **GCP** | Cloud SQL SQL Server | 2017-2022 | 自动补丁, 加密 | Database Migration Service |
| **阿里云** | RDS SQL Server | 2016-2019 | Web版, 企业版 | DTS |
| **华为云** | RDS SQL Server | 2016-2019 | 主备架构 | DRS |
| **腾讯云** | TDSQL-C SQL Server | 2017-2019 | 云原生架构 | DTS |

### 1.4 Oracle 替代方案映射

由于多数云厂商不提供托管Oracle服务，以下为替代方案：

| 源端 | AWS替代 | Azure替代 | GCP替代 | 阿里云替代 | 华为云替代 |
|------|---------|-----------|---------|-----------|-----------|
| Oracle | RDS PostgreSQL / Aurora PostgreSQL | Azure Database for PostgreSQL | Cloud SQL PostgreSQL / AlloyDB | RDS PostgreSQL / PolarDB PostgreSQL | GaussDB(for openGauss) |
| Oracle RAC | Aurora PostgreSQL | Azure SQL Managed Instance | AlloyDB | PolarDB | GaussDB |
| Oracle Exadata | RDS Oracle (BYOL) | Oracle on Azure VMs | Oracle on GCP VMs | RDS PPAS | 裸金属服务器+Oracle |

---

## 2. NoSQL数据库映射 / NoSQL Database Mapping

### 2.1 MongoDB 兼容产品

| 云厂商 | 产品名称 | 兼容性 | 关键特性 | 迁移工具 |
|--------|---------|--------|---------|---------|
| **AWS** | Amazon DocumentDB | MongoDB 3.6, 4.0, 5.0 | 兼容MongoDB API | AWS DMS, mongodump |
| **Azure** | Azure Cosmos DB (Mongo API) | MongoDB 4.2, 4.4 | 全球分布, 多模型 | Azure DMS, mongoimport |
| **GCP** | MongoDB Atlas (第三方) | 全版本 | 全托管MongoDB | MongoDB Atlas Live Migration |
| **阿里云** | ApsaraDB for MongoDB | 3.4-6.0 | 副本集, 分片集群 | DTS |
| **华为云** | Document Database Service (DDS) | 3.2-4.4 | 副本集, 集群版 | DRS |
| **腾讯云** | TencentDB for MongoDB | 3.6-4.4 | 副本集, 分片 | DTS |

### 2.2 Redis 兼容产品

| 云厂商 | 产品名称 | 版本支持 | 关键特性 | 迁移工具 |
|--------|---------|---------|---------|---------|
| **AWS** | Amazon ElastiCache Redis | 5.0, 6.x, 7.0 | 集群模式, 全球数据存储 | Redis-native, AWS DMS |
| **Azure** | Azure Cache for Redis | 4.0, 6.0 | 企业版, 区域冗余 | Redis-cli, Import/Export |
| **GCP** | Memorystore for Redis | 5.0, 6.x, 7.0 | 高可用, 自动故障转移 | redis-cli, gsutil |
| **阿里云** | 云数据库Redis | 4.0, 5.0, 6.0, 7.0 | 标准版, 集群版, 读写分离 | DTS, redis-shake |
| **阿里云** | Tair (Redis企业版) | 5.0, 6.0 | 性能增强版, 持久内存版, 图数据库 | DTS, redis-shake |
| **阿里云** | Tair KVCache | 6.0 | 键值对缓存, 高性能低延迟 | DTS |
| **华为云** | Distributed Cache Service (DCS) | 3.0, 4.0, 5.0, 6.0 | 主备, Proxy集群 | DCS迁移工具 |
| **腾讯云** | Cloud Redis Service (CRS) | 4.0, 5.0, 6.2 | 标准版, 集群版 | DTS |

### 2.3 Key-Value/Wide Column 产品

| 云厂商 | 产品名称 | 数据模型 | 关键特性 | 迁移工具 |
|--------|---------|---------|---------|---------|
| **AWS** | Amazon DynamoDB | Key-Value, Document | 无服务器, 全局表 | AWS DMS, DynamoDB Streams |
| **Azure** | Azure Cosmos DB | Multi-model | SQL, Mongo, Cassandra, Table API | Azure Data Factory |
| **GCP** | Cloud Firestore / Datastore | Document | 实时同步, 离线持久 | Firestore Data Bundles |
| **阿里云** | PolarDB PostgreSQL | Multi-model | dynamo协议兼容, 分布式, json存储模型 | NimoShake迁移工具, DataX |
| **阿里云** | MongoDB | Document | schema-free, json存储, 分布式扩展 | NimoShake迁移工具, DataX |
| **阿里云** | Lindorm | 多模 (Wide Column, Search, TSDB) | 云原生多模数据库, HBase/ES/TSDB兼容 | Lindorm迁移工具, HBase API |
| **华为云** | GaussDB NoSQL | Document | MongoDB兼容 | DRS |
| **腾讯云** | TcaplusDB | Key-Value | 游戏场景优化 | TcaplusDB迁移工具 |

### 2.4 多模数据库 / Multi-Model Database

| 云厂商 | 产品名称 | 支持模型 | 关键特性 | 迁移工具 |
|--------|---------|---------|---------|---------|
| **AWS** | Amazon DocumentDB + Keyspaces | Document, Wide Column | 分别对应MongoDB和Cassandra | AWS DMS |
| **Azure** | Azure Cosmos DB | Multi-model | SQL, MongoDB, Cassandra, Gremlin, Table | Azure Data Factory |
| **阿里云** | Lindorm | Wide Column, Search, Time Series, File | HBase、Elasticsearch、OpenTSDB、HDFS统一接口 | HBase API, ES API, 迁移工具 |
| **华为云** | GeminiDB | Multi-model | Redis, MongoDB, InfluxDB兼容接口 | DRS |

---

## 3. 数据仓库映射 / Data Warehouse Mapping

### 3.1 云原生数据仓库

| 云厂商 | 产品名称 | 架构 | 存储格式 | 迁移工具 |
|--------|---------|------|---------|---------|
| **AWS** | Amazon Redshift | MPP | 列存储 | AWS DMS, S3 COPY, Redshift Spectrum |
| **Azure** | Azure Synapse Analytics | MPP + Serverless | 列存储, Parquet | Azure Data Factory, PolyBase |
| **GCP** | BigQuery | Serverless | Capacitor, Parquet | BigQuery Data Transfer, bq load |
| **阿里云** | AnalyticDB MySQL | MPP | 列存储 | DataWorks, DTS, OSS外表 |
| **阿里云** | AnalyticDB PostgreSQL | MPP | 列存储 | DataWorks, OSS外表, pg_dump |
| **阿里云** | MaxCompute | 离线计算 | 列存储 | DataWorks, Tunnel, MMA迁移工具 |
| **华为云** | Data Warehouse Service (DWS) | MPP | 列存储 | CDM, GDS并行导入 |
| **腾讯云** | Cloud Data Warehouse (CDW) | MPP | 列存储 | CDW迁移工具 |
| **火山引擎** | ByteHouse | 云原生 | 列存储 | ByteHouse数据导入 |

### 3.2 数据仓库特性对比

| 特性 | Redshift | Synapse | BigQuery | AnalyticDB | MaxCompute | DWS | CDW |
|------|----------|---------|----------|-----------|------------|-----|-----|
| **扩展方式** | 节点扩展 | DWU扩展 | 自动扩展 | 节点扩展 | 弹性扩展 | 节点扩展 | 节点扩展 |
| **并发查询** | 50+ | 128+ | 无限制 | 100+ | 1000+ | 200+ | 100+ |
| **数据湖集成** | Spectrum | 内置 | 原生支持 | OSS外表 | 深度集成 | OBS外表 | COS外表 |
| **实时摄入** | Kinesis | Stream Analytics | Dataflow | 实时写入 | 批量为主 | 实时写入 | 实时写入 |
| **地理空间** | 支持 | 支持 | BigQuery GIS | PostGIS | 支持 | 支持 | 支持 |
| **离线计算** | 有限 | 支持 | 支持 | 有限 | 强 | 有限 | 有限 |

### 3.3 实时分析/ClickHouse类数据仓库

| 云厂商 | 产品名称 | 引擎 | 关键特性 | 适用场景 | 迁移工具 |
|--------|---------|------|---------|---------|---------|
| **AWS** | Amazon Redshift (RA3) | 列存储 | 实时查询, 并发扩展 | 实时BI, 交互式分析 | S3 COPY |
| **阿里云** | ClickHouse (阿里云版) | ClickHouse | 高性能OLAP, 实时分析 | 日志分析, 时序数据 | ClickHouse原生工具 |
| **阿里云** | SelectDB (阿里云版) | Apache Doris | 实时数仓, 高并发 | 实时报表, 用户画像 | Doris迁移工具 |
| **华为云** | CloudTable (HBase/ClickHouse) | ClickHouse | 实时OLAP | 实时分析 | CloudTable迁移 |
| **腾讯云** | ClickHouse (腾讯云版) | ClickHouse | 列存储分析 | 日志分析, 监控 | ClickHouse工具 |

---

## 4. 大数据平台映射 / Big Data Platform Mapping

### 4.1 Hadoop/Spark 托管服务

| 云厂商 | 产品名称 | 组件 | 版本 | 迁移工具 |
|--------|---------|------|------|---------|
| **AWS** | Amazon EMR | Hadoop, Spark, Hive, Presto, Flink | EMR 6.x | S3 DistCp, EMR迁移工具 |
| **Azure** | Azure HDInsight | Hadoop, Spark, Hive, Kafka, HBase | 4.0 | Azure Data Factory, DistCp |
| **GCP** | Dataproc | Hadoop, Spark, Hive, Presto, Flink | 2.0 | Cloud Storage Connector |
| **阿里云** | E-MapReduce (EMR) | Hadoop, Spark, Hive, Presto, Flink | EMR 3.x/5.x | OSS Connector, DataWorks |
| **华为云** | MapReduce Service (MRS) | Hadoop, Spark, Hive, Flink, Kafka | MRS 3.x | OBS Connector |
| **腾讯云** | Elastic MapReduce (EMR) | Hadoop, Spark, Hive, Presto | EMR 2.x/3.x | COS Connector |
| **火山引擎** | EMR | Hadoop, Spark, Hive, Presto | EMR 2.x/3.x | TOS Connector |

### 4.2 实时计算/Flink

| 云厂商 | 产品名称 | 模式 | 关键特性 | 迁移工具 |
|--------|---------|------|---------|---------|
| **AWS** | Amazon Kinesis Data Analytics | 托管Flink | 实时流处理 | Kinesis Data Analytics Studio |
| **Azure** | Azure Stream Analytics | 托管 | SQL-like语法 | Azure Data Factory |
| **GCP** | Dataflow | 托管Apache Beam | 批流一体 | Dataflow模板 |
| **阿里云** | Realtime Compute for Apache Flink | 托管Flink | Ververica内核 | VVP迁移 |
| **华为云** | Flink Serverless | 托管Flink | 实时计算 | Flink Savepoint |
| **腾讯云** | Oceanus | 托管Flink | 与EMR集成 | Oceanus迁移工具 |

### 4.3 消息队列/Kafka

| 云厂商 | 产品名称 | 兼容性 | 关键特性 | 迁移工具 |
|--------|---------|--------|---------|---------|
| **AWS** | Amazon MSK | Apache Kafka | 完全托管, 高可用 | MSK MirrorMaker |
| **Azure** | Azure Event Hubs | Kafka协议 | 与Azure集成 | Kafka MirrorMaker |
| **GCP** | Pub/Sub | 原生 | 全球消息总线 | Pub/Sub Kafka Connector |
| **阿里云** | Message Queue for Apache Kafka | Kafka协议 | 高吞吐, 低延迟 | Kafka MirrorMaker |
| **华为云** | Distributed Message Service (Kafka) | Kafka协议 | 高可用, 安全 | Kafka MirrorMaker |
| **腾讯云** | Cloud Kafka (CKafka) | Kafka协议 | 金融级高可用 | CKafka迁移工具 |

---

## 5. 对象存储映射 / Object Storage Mapping

### 5.1 标准对象存储

| 云厂商 | 产品名称 | S3兼容 | 存储类别 | 迁移工具 |
|--------|---------|--------|---------|---------|
| **AWS** | Amazon S3 | 原生 | Standard, IA, Glacier | AWS DataSync, S3 Batch |
| **Azure** | Azure Blob Storage | 是 | Hot, Cool, Archive | AzCopy, Azure Data Factory |
| **GCP** | Cloud Storage | 是 | Standard, Nearline, Coldline, Archive | gsutil, Storage Transfer Service |
| **阿里云** | Object Storage Service (OSS) | 是 | 标准, 低频, 归档, 冷归档 | ossimport, 闪电立方 |
| **华为云** | Object Storage Service (OBS) | 是 | 标准, 低频, 归档, 深度归档 | OBS Browser, OMS |
| **腾讯云** | Cloud Object Storage (COS) | 是 | 标准, 低频, 归档, 深度归档 | COS Migration, CDM |
| **火山引擎** | Tinder Object Storage (TOS) | 是 | 标准, 低频, 归档, 冷归档 | TOS迁移工具 |

### 5.2 文件存储/NAS

| 云厂商 | 产品名称 | 协议 | 性能级别 | 迁移工具 |
|--------|---------|------|---------|---------|
| **AWS** | Amazon EFS | NFS | 通用, Max I/O | AWS DataSync |
| **Azure** | Azure Files | SMB, NFS | 标准, Premium | AzCopy, Robocopy |
| **GCP** | Filestore | NFS | 标准, 高级, 企业级 | gsutil, rsync |
| **阿里云** | NAS | NFS, SMB | 通用, 极速 | NAS数据迁移服务 |
| **华为云** | Scalable File Service (SFS) | NFS | SFS, SFS Turbo | SFS迁移工具 |
| **腾讯云** | Cloud File Storage (CFS) | NFS, CIFS/SMB | 标准, 高性能 | CFS迁移工具 |

---

## 6. 数据湖映射 / Data Lake Mapping

### 6.1 数据湖存储

| 云厂商 | 产品名称 | 架构 | 查询引擎 | 迁移工具 |
|--------|---------|------|---------|---------|
| **AWS** | S3 + Lake Formation | 对象存储+元数据 | Athena, Redshift Spectrum | AWS Glue, Lake Formation |
| **Azure** | ADLS Gen2 | 分层命名空间 | Synapse SQL, Databricks | Azure Data Factory |
| **GCP** | Cloud Storage + BigLake | 对象存储+元数据 | BigQuery | BigLake, Dataflow |
| **阿里云** | OSS + Data Lake Formation | 对象存储+元数据 | DLF SQL, MaxCompute | DataWorks, DLF |
| **华为云** | OBS + LakeFormation | 对象存储+元数据 | DWS SQL, MRS | CDM |
| **腾讯云** | COS + DLC | 对象存储+元数据 | DLC SQL | CDM |

### 6.2 数据湖格式支持

| 格式 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 |
|------|-----|-------|-----|--------|--------|--------|
| **Delta Lake** | EMR, Glue | HDInsight, Databricks | Dataproc | EMR, Databricks | MRS | EMR |
| **Apache Iceberg** | EMR, Athena | HDInsight | BigQuery | EMR | MRS | EMR |
| **Apache Hudi** | EMR, Glue | HDInsight | Dataproc | EMR | MRS | EMR |
| **Parquet** | 原生支持 | 原生支持 | 原生支持 | 原生支持 | 原生支持 | 原生支持 |
| **ORC** | 原生支持 | 原生支持 | 原生支持 | 原生支持 | 原生支持 | 原生支持 |

---

## 7. 数据集成/ETL映射 / Data Integration Mapping

### 7.1 托管ETL服务

| 云厂商 | 产品名称 | 类型 | 关键特性 | 迁移工具 |
|--------|---------|------|---------|---------|
| **AWS** | AWS Glue | Serverless ETL | 数据目录, 爬虫 | Glue DataBrew |
| **Azure** | Azure Data Factory | 数据集成 | 可视化管道, SSIS | ADF Copy Wizard |
| **GCP** | Cloud Dataflow | 流/批处理 | Apache Beam | Dataflow模板 |
| **阿里云** | DataWorks | 数据集成+开发 | 数据开发, 调度, 数据治理 | DataWorks迁移助手 |
| **阿里云** | DMS (数据管理) | 数据库管理 | 数据库DevOps, 数据追踪 | DMS导入导出 |
| **阿里云** | DAS (数据库自治服务) | 智能运维 | SQL诊断, 自动优化, 容量预测 | - |
| **华为云** | Data Arts Studio | 数据集成 | 数据开发, 治理 | CDM |
| **腾讯云** | WeData | 数据集成 | 数据开发, 调度 | WeData迁移工具 |

### 7.2 CDC/实时同步工具

| 云厂商 | 产品名称 | 源端支持 | 目标支持 | 延迟 |
|--------|---------|---------|---------|------|
| **AWS** | AWS DMS (CDC) | 各种RDBMS | 各种目标 | 秒级 |
| **Azure** | Azure Data Factory (CDC) | SQL Server, Oracle等 | 各种目标 | 分钟级 |
| **GCP** | Datastream | Oracle, MySQL, PG | BigQuery, Cloud SQL | 秒级 |
| **阿里云** | DTS (数据传输服务) | MySQL, PG, Oracle, MongoDB, Redis等 | 各种目标 | 毫秒级 |
| **阿里云** | Canal (开源) | MySQL | Kafka, RocketMQ | 毫秒级 |
| **华为云** | DRS (数据复制服务) | MySQL, PG, Oracle等 | 各种目标 | 秒级 |
| **腾讯云** | DTS (数据传输服务) | MySQL, PG, MongoDB等 | 各种目标 | 秒级 |

### 7.3 数据库管理工具

| 云厂商 | 产品名称 | 功能 | 关键特性 |
|--------|---------|------|---------|
| **AWS** | AWS DMS + SCT | 迁移+转换 | 数据库评估, Schema转换 |
| **阿里云** | ADAM (亚当) | Oracle迁移评估 | Oracle→PolarDB兼容性评估, 自动转换 |
| **阿里云** | DMS (数据管理) | 数据库DevOps | 数据变更, 数据追踪, 敏感数据保护 |
| **阿里云** | DAS (数据库自治服务) | 智能运维 | SQL诊断, 自动SQL优化, 异常检测 |
| **华为云** | DAS | 数据库管理 | SQL诊断, 慢SQL分析 |
| **腾讯云** | DBbrain | 数据库智能管家 | 诊断优化, 安全防护 |

---

## 8. 版本兼容性矩阵 / Version Compatibility Matrix

### 8.1 MySQL 版本兼容性

| 版本 | AWS RDS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|------|---------|-------|-----|--------|--------|--------|----------|
| 5.6 | ✓ | ✓ | ✓ | ✓ | ✓ | - | - |
| 5.7 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 8.0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 8.1+ | - | - | - | - | - | - | - |

### 8.2 PostgreSQL 版本兼容性

| 版本 | AWS RDS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|------|---------|-------|-----|--------|--------|--------|----------|
| 11 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 12 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 13 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 14 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 15 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 16 | ✓ | ✓ | ✓ | - | - | - | - |

### 8.3 Redis 版本兼容性

| 版本 | AWS ElastiCache | Azure | GCP Memorystore | 阿里云 | 华为云 | 腾讯云 |
|------|-----------------|-------|-----------------|--------|--------|--------|
| 4.0 | ✓ | ✓ | - | ✓ | ✓ | ✓ |
| 5.0 | ✓ | - | ✓ | ✓ | ✓ | ✓ |
| 6.0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6.2 | ✓ | - | ✓ | ✓ | ✓ | ✓ |
| 7.0 | ✓ | - | ✓ | ✓ | ✓ | ✓ |

---

## 9. 功能特性映射 / Feature Mapping

### 9.1 数据库高可用特性

| 特性 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 |
|------|-----|-------|-----|--------|--------|--------|
| **Multi-AZ** | ✓ | ✓ | ✓ | ✓ (三节点) | ✓ | ✓ |
| **只读副本** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **跨区域复制** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **自动故障转移** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **时间点恢复** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Proxy/连接池** | RDS Proxy | - | - | 数据库代理 | Proxy | Proxy |
| **计算存储分离** | Aurora | - | - | PolarDB | - | TDSQL-C |
| **秒级扩容** | Aurora | - | - | PolarDB | - | TDSQL-C |
| **一写多读** | Aurora | - | - | PolarDB | - | - |
| **水平分片** | - | - | Spanner | PolarDB-X | - | TDSQL-PG |

### 9.2 大数据特性

| 特性 | AWS EMR | Azure HDInsight | GCP Dataproc | 阿里云EMR | 华为云MRS | 腾讯云EMR |
|------|---------|-----------------|--------------|-----------|-----------|-----------|
| **自动扩缩容** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Spot/抢占式实例** | ✓ | - | ✓ | ✓ | ✓ | ✓ |
| **与数据湖集成** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Notebook集成** | EMR Studio | HDInsight Jupyter | Dataproc Hub | DataWorks | - | - |
| **工作流调度** | MWAA | ADF | Cloud Composer | DataWorks | - | - |

### 9.3 云原生数据库特性 (PolarDB/ Aurora/ AlloyDB)

| 特性 | AWS Aurora | GCP AlloyDB | 阿里云PolarDB MySQL | 阿里云PolarDB PostgreSQL | 阿里云PolarDB-X |
|------|-----------|-------------|---------------------|-------------------------|-----------------|
| **架构** | 计算存储分离 | 计算存储分离 | 计算存储分离 | 计算存储分离 | 分布式Shared-Nothing |
| **存储扩展** | 自动扩展128TB | 自动扩展 | 自动扩展100TB | 自动扩展100TB | 水平扩展PB级 |
| **只读副本** | 15个 | 20个 | 15个 | 15个 | 分布式只读 |
| **写入能力** | 单写 | 单写 | 单写 | 单写 | 分布式写入 |
| **RPO** | 0 | 0 | 0 | 0 | 0 |
| **RTO** | <30秒 | <30秒 | <30秒 | <30秒 | <30秒 |
| **HTAP支持** | 有限 | 强 | 支持 | 支持 | 强 |
| **Oracle兼容** | - | 强 | - | 是 | - |
| **全局一致性** | 全局数据库 | - | 全球数据库 | 全球数据库 | 强一致 |

### 9.4 多模数据库特性 (Lindorm/ Cosmos DB/ GeminiDB)

| 特性 | Azure Cosmos DB | 阿里云Lindorm | 华为云GeminiDB |
|------|----------------|---------------|----------------|
| **支持模型** | SQL, Mongo, Cassandra, Gremlin | Wide Column, Search, TSDB, File | Redis, Mongo, InfluxDB |
| **HBase兼容** | Cassandra API | 原生HBase API | - |
| **ES兼容** | - | 原生ES API | - |
| **时序数据库** | - | OpenTSDB兼容 | InfluxDB兼容 |
| **文件存储** | - | HDFS兼容 | - |
| **存储分层** | 自动 | 冷热分离 | - |
| **适用场景** | 全球分布应用 | IoT, 日志, 监控 | 缓存, 时序 |

---

## 10. 网络和安全映射 / Network & Security Mapping

### 10.1 私有连接

| 云厂商 | VPC对等 | 私有连接 | 服务终端节点 |
|--------|---------|---------|-------------|
| **AWS** | VPC Peering | PrivateLink | VPC Endpoints |
| **Azure** | VNet Peering | Private Link | Private Endpoints |
| **GCP** | VPC Peering | Private Service Connect | Private Google Access |
| **阿里云** | VPC对等连接 | 私网连接 | 终端节点 |
| **华为云** | VPC对等连接 | VPC终端节点 | 终端节点 |
| **腾讯云** | 对等连接 | 私有连接 | 终端节点 |

### 10.2 加密特性

| 特性 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 |
|------|-----|-------|-----|--------|--------|--------|
| **传输加密 (TLS)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **静态加密 (KMS)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **自带密钥 (BYOK)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **列级加密** | ✓ | ✓ | - | ✓ | ✓ | ✓ |
| **透明数据加密 (TDE)** | ✓ | ✓ | - | ✓ | ✓ | ✓ |

---

## 11. 成本对比参考 / Cost Comparison Reference

### 11.1 数据库月度成本估算 (以4vCPU 16GB为例)

| 云厂商 | 产品 | 按需价格/月 | 预留实例/月 | 备注 |
|--------|------|------------|------------|------|
| **AWS** | RDS MySQL (db.m5.xlarge) | ~$350 | ~$220 | 单可用区 |
| **AWS** | Aurora MySQL (db.r5.xlarge) | ~$420 | ~$280 | 计算存储分离 |
| **Azure** | Azure DB MySQL (GP_Gen5_4) | ~$380 | ~$240 | 灵活服务器 |
| **GCP** | Cloud SQL MySQL (db-n1-standard-4) | ~$320 | ~$200 | 高可用 |
| **GCP** | AlloyDB (4vCPU) | ~$480 | ~$320 | PostgreSQL增强 |
| **阿里云** | RDS MySQL (4核16G) | ~¥1,800 | ~¥1,200 | 高可用版 |
| **阿里云** | PolarDB MySQL (4核16G) | ~¥2,200 | ~¥1,500 | 计算存储分离 |
| **阿里云** | PolarDB-X (4核16G) | ~¥2,800 | ~¥1,900 | 分布式 |
| **华为云** | RDS MySQL (4核16G) | ~¥1,600 | ~¥1,000 | 主备版 |
| **腾讯云** | TDSQL-C (4核16G) | ~¥1,400 | ~¥900 | Serverless |

### 11.1.1 阿里云数据库产品成本参考

| 产品 | 规格 | 按需价格/月 | 关键计费项 |
|------|------|------------|-----------|
| **RDS MySQL** | 4核16G + 500GB SSD | ~¥2,200 | 实例+存储+备份 |
| **PolarDB MySQL** | 4核16G + 500GB | ~¥2,800 | 计算节点+存储(按量) |
| **PolarDB-X** | 4核16G × 2节点 | ~¥3,500 | 计算节点+存储+网络 |
| **PolarDB PostgreSQL** | 4核16G + 500GB | ~¥3,000 | 计算节点+存储 |
| **AnalyticDB MySQL** | C8 (4核32G) | ~¥4,500 | 节点规格+存储 |
| **MaxCompute** | 按量付费 | ~¥0.3/CU/小时 | 计算+存储分开计费 |
| **Lindorm** | 4核16G + 500GB | ~¥3,200 | 宽表+搜索+时序分别计费 |
| **Tair (Redis企业版)** | 4GB 性能增强 | ~¥1,800 | 内存规格+性能级别 |
| **Tablestore** | 按量付费 | ~¥0.15/万CU | 读写CU+存储 |
| **ClickHouse** | 4核16G | ~¥2,500 | 节点+存储 |
| **SelectDB** | 4核16G | ~¥3,000 | 计算+存储分离 |

### 11.2 对象存储成本估算 (1TB/月)

| 云厂商 | 标准存储 | 低频存储 | 归档存储 | 出站流量 |
|--------|---------|---------|---------|---------|
| **AWS S3** | $23 | $12.50 | $4 | $90 |
| **Azure Blob** | $23.50 | $13 | $4.50 | $87 |
| **GCP Storage** | $20 | $10 | $4 | $120 |
| **阿里云OSS** | ¥120 | ¥80 | ¥33 | ¥800 |
| **华为云OBS** | ¥110 | ¥70 | ¥30 | ¥750 |
| **腾讯云COS** | ¥118 | ¥78 | ¥32 | ¥800 |

---

## 12. 迁移复杂度评估 / Migration Complexity Assessment

### 12.1 复杂度评级标准

| 等级 | 描述 | 典型场景 | 预估工时 |
|------|------|---------|---------|
| **简单** | 同构迁移，工具成熟 | MySQL→MySQL, S3→OSS | 1-2周 |
| **中等** | 异构迁移，需schema转换 | Oracle→PostgreSQL | 4-8周 |
| **复杂** | 架构变更，应用改造 | 单体→微服务+分布式DB | 3-6月 |
| **极复杂** | 大规模重构，多系统集成 | 传统数仓→云原生湖仓 | 6-12月 |

### 12.2 各场景复杂度参考

| 源端→目标端 | 复杂度 | 主要挑战 | 推荐策略 |
|------------|--------|---------|---------|
| AWS RDS MySQL → 阿里云RDS MySQL | 简单 | 网络配置 | 在线迁移+DTS |
| AWS Aurora → 阿里云PolarDB MySQL | 简单 | 同构迁移, 架构相似 | 在线迁移+DTS |
| Oracle → 阿里云PolarDB PostgreSQL | 中等 | PL/SQL转换, ADAM评估 | ADAM评估+分阶段迁移 |
| MySQL → 阿里云PolarDB-X | 中等 | 分库分表设计, SQL改造 | 数据迁移+应用改造并行 |
| MongoDB → 阿里云MongoDB | 简单 | 版本兼容性 | 在线迁移+DTS |
| MongoDB → 阿里云Lindorm | 中等 | 数据模型转换, API改造 | 双写迁移+逐步切换 |
| HBase → 阿里云Lindorm | 简单 | HBase API兼容 | 在线迁移+HBase API |
| Elasticsearch → 阿里云Lindorm Search | 中等 | 查询语法差异, 索引重建 | 重建索引+双写验证 |
| Redis → 阿里云Tair | 简单 | 企业版特性差异 | 热迁移+DTS |
| Hadoop → 阿里云EMR+OSS数据湖 | 中等 | 架构重构, 存储分离 | 双跑验证+逐步切换 |
| Teradata → 阿里云AnalyticDB | 中等 | SQL方言, 性能调优 | Schema转换+并行验证 |
| Oracle → PostgreSQL | 复杂 | PL/SQL转换, 存储过程 | 分阶段迁移+SCT |
| Hadoop → 云原生数据湖 | 复杂 | 架构重构, 格式转换 | 双跑验证+逐步切换 |
| MongoDB → DocumentDB | 简单 | 版本兼容性 | 在线迁移+DMS |
| Redis → Redis | 简单 | 数据一致性 | 热迁移+双写 |

### 12.3 阿里云特有产品迁移复杂度

| 源端→目标端 | 复杂度 | 关键考虑因素 | 建议工具 |
|------------|--------|-------------|---------|
| **迁入PolarDB** | | | |
| RDS MySQL → PolarDB MySQL | 简单 | 同构迁移, 架构升级 | DTS一键迁移 |
| MySQL → PolarDB-X | 中等 | 分片键设计, 分布式事务 | DTS+应用改造 |
| Oracle → PolarDB PostgreSQL | 中等 | ADAM评估, 语法兼容 | ADAM+DTS |
| **迁入Lindorm** | | | |
| HBase → Lindorm宽表 | 简单 | API兼容, 无缝迁移 | HBase API直接切换 |
| Cassandra → Lindorm宽表 | 中等 | 数据模型映射, CQL差异 | DataX自定义迁移 |
| OpenTSDB → Lindorm时序 | 简单 | API兼容 | OpenTSDB API直接切换 |
| Elasticsearch → Lindorm搜索 | 中等 | 查询DSL差异, 分词器 | 重建索引+双写 |
| InfluxDB → Lindorm时序 | 中等 | Line Protocol兼容 | InfluxDB API迁移 |
| **迁入MaxCompute** | | | |
| Hive → MaxCompute | 简单 | SQL方言兼容 | MMA批量迁移 |
| Teradata → MaxCompute | 复杂 | SQL转换, 存储过程 | DataWorks+UDF改造 |
| Oracle → MaxCompute | 复杂 | 数据类型映射, SQL重写 | DataWorks+自定义开发 |

---

*注：以上产品信息和映射关系基于2024年公开资料整理，具体以各云厂商官方文档为准。*
