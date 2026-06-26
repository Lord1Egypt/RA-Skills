---
name: cloud-data-migration
description: Generate comprehensive data migration plans between cloud vendors. Supports database, big data, and data lake migrations. Automatically recommends target products and provides detailed migration strategies including tools, assessment, POC, risks, and best practices. Use when users need to migrate data from one cloud provider to another222.
---

# 云厂商数据迁移方案 | Cloud Data Migration Solution

This skill helps cloud architects design comprehensive data migration plans between cloud vendors, focusing on databases, big data, and data lake scenarios.

本技能帮助云架构师设计云厂商间的综合数据迁移方案，聚焦数据库、大数据和数据湖场景。

## When to Use / 使用场景

- User needs to migrate databases between cloud vendors / 用户需要在云厂商之间迁移数据库
- User wants to migrate big data platforms (Hadoop, Spark, etc.) / 用户想要迁移大数据平台（Hadoop、Spark等）
- User needs to migrate data lakes / 用户需要迁移数据湖
- User asks for migration tools and strategies / 用户询问迁移工具和策略
- User needs migration risk assessment / 用户需要迁移风险评估
- User wants POC (Proof of Concept) guidance / 用户需要POC指导

---

## Input Parameters / 输入参数

用户需要提供以下信息 / User needs to provide:

### Required Parameters / 必需参数
- **源端云厂商 (Source Cloud Vendor)**: AWS, Azure, GCP, 阿里云, 华为云, 腾讯云, 火山引擎
- **源端产品名称 (Source Product Name)**: 具体的产品名称（如 RDS MySQL, S3, BigQuery等）
- **目标云厂商 (Target Cloud Vendor)**: AWS, Azure, GCP, 阿里云, 华为云, 腾讯云, 火山引擎

### Optional Parameters / 可选参数
- **目标端产品名称 (Target Product Name)**: 如果用户已确定目标产品，提供具体名称
- **数据规模 (Data Volume)**: 数据量大小（如 1TB, 100TB, 1PB）
- **迁移时间窗口 (Migration Window)**: 允许的停机时间（如 4小时, 周末, 无停机）
- **业务场景 (Business Scenario)**: OLTP, OLAP, 混合负载, 实时分析等
- **合规要求 (Compliance Requirements)**: 数据主权、加密、审计等要求
- **预算约束 (Budget Constraints)**: 预算范围

---

## Migration Workflow / 迁移工作流程

### Step 1: Parse User Input / 解析用户输入

从用户查询中提取关键信息：
```
输入示例: "将AWS RDS MySQL迁移到阿里云"
- 源端: AWS
- 源产品: RDS MySQL
- 目标端: 阿里云
- 目标产品: 未指定（需要推荐）

输入示例: "把华为云DWS迁移到AWS Redshift"
- 源端: 华为云
- 源产品: DWS
- 目标端: AWS
- 目标产品: Redshift（已指定）
```

### Step 2: Product Mapping / 产品映射

#### 2.1 如果目标产品已指定 / If Target Product Specified
验证目标产品是否适合源产品迁移：
- 检查兼容性（版本、功能、性能）
- 确认迁移路径可行性
- 识别潜在的功能差异

#### 2.2 如果目标产品未指定 / If Target Product Not Specified
根据以下维度推荐目标产品：
- **功能对等性 (Feature Parity)**: 目标产品功能覆盖度
- **性能匹配 (Performance Match)**: 性能指标对比
- **成本效益 (Cost Efficiency)**: 性价比分析
- **生态集成 (Ecosystem Integration)**: 与目标云其他服务集成度
- **迁移复杂度 (Migration Complexity)**: 迁移难度评估

### Step 3: Migration Strategy Selection / 迁移策略选择

根据数据特征和业务需求选择迁移策略：

| 策略 | 适用场景 | 停机时间 | 复杂度 |
|------|---------|---------|--------|
| **离线迁移 (Offline)** | 小数据量、允许停机 | 较长 | 低 |
| **在线迁移 (Online)** | 大数据量、有限停机窗口 | 短 | 中 |
| **双写迁移 (Dual-Write)** | 关键业务、零停机 | 无 | 高 |
| **增量同步 (CDC)** | 实时性要求高 | 无 | 高 |

### Step 4: Tool Selection / 工具选择

优先选择云厂商自带工具，其次考虑开源方案：

**选择优先级 / Selection Priority**:
1. 源端云厂商原生迁移工具
2. 目标端云厂商原生迁移工具
3. 第三方云厂商工具
4. 开源工具方案

### Step 5: Generate Migration Plan / 生成迁移方案

输出完整的迁移方案文档，包含：
1. 产品选型建议
2. 迁移工具清单
3. 迁移评估报告
4. POC方案
5. 风险分析
6. 实施步骤
7. 回滚方案

---

## Product Categories / 产品类别

### 1. 关系型数据库 / Relational Databases

| 源端产品 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|---------|-----|-------|-----|--------|--------|--------|----------|
| MySQL | RDS MySQL | Azure Database for MySQL | Cloud SQL | RDS MySQL | RDS MySQL | TDSQL-C MySQL | RDS MySQL |
| PostgreSQL | RDS PostgreSQL | Azure Database for PostgreSQL | Cloud SQL (PG) | RDS PostgreSQL | RDS PostgreSQL | TDSQL-C PostgreSQL | RDS PostgreSQL |
| SQL Server | RDS SQL Server | Azure SQL Database | Cloud SQL (SQL Server) | RDS SQL Server | RDS SQL Server | TDSQL-C SQL Server | - |
| Oracle | RDS Oracle (BYOL) | Oracle on Azure VMs | Oracle on GCP | RDS PPAS | - | - | - |
| MariaDB | RDS MariaDB | Azure Database for MariaDB | Cloud SQL | RDS MariaDB | - | - | - |

### 2. NoSQL数据库 / NoSQL Databases

| 源端产品 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|---------|-----|-------|-----|--------|--------|--------|----------|
| MongoDB | DocumentDB | Cosmos DB (Mongo API) | MongoDB Atlas | MongoDB | DDS | MongoDB | MongoDB |
| Redis | ElastiCache Redis | Azure Cache for Redis | Memorystore Redis | Tair/Redis | DCS | CRS | Redis |
| DynamoDB | DynamoDB | Cosmos DB | Firestore/Datastore | PolarDB PostgreSQL/MongoDB | GaussDB NoSQL | TcaplusDB | - |
| Cassandra | Keyspaces | Managed Instance for Apache Cassandra | Bigtable | Lindorm | GaussDB NoSQL | TcaplusDB | - |

### 3. 数据仓库 / Data Warehouses

| 源端产品 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|---------|-----|-------|-----|--------|--------|--------|----------|
| Redshift | Redshift | Azure Synapse | BigQuery | AnalyticDB PostgreSQL | DWS | CDW | ByteHouse |
| Snowflake | Snowflake | Snowflake | Snowflake | - | - | - | - |
| BigQuery | - | - | BigQuery | MaxCompute | - | - | - |
| Synapse | - | Synapse | - | - | - | - | - |

### 4. 大数据平台 / Big Data Platforms

| 源端产品 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|---------|-----|-------|-----|--------|--------|--------|----------|
| Hadoop/EMR | EMR | HDInsight | Dataproc | E-MapReduce | MRS | EMR | EMR |
| Spark | EMR/Glue | HDInsight/Synapse | Dataproc | Databricks/EMR | MRS | EMR | EMR |
| Kafka | MSK | Event Hubs | Pub/Sub | Kafka | Kafka | CKafka | - |
| Flink | Kinesis Analytics | Stream Analytics | Dataflow | Flink | Flink | Oceanus | - |

### 5. 对象存储 / Object Storage

| 源端产品 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|---------|-----|-------|-----|--------|--------|--------|----------|
| S3 | S3 | Blob Storage | Cloud Storage | OSS | OBS | COS | TOS |
| EBS | EBS | Managed Disks | Persistent Disk | ESSD | EVS | CBS | - |
| EFS | EFS | Azure Files | Filestore | NAS | SFS | CFS | - |

### 6. 数据湖 / Data Lakes

| 源端产品 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 | 火山引擎 |
|---------|-----|-------|-----|--------|--------|--------|----------|
| S3 Data Lake | S3 + Lake Formation | ADLS Gen2 | Cloud Storage + BigLake | OSS + DLF | OBS + LakeFormation | COS + DLC | TOS + LAS |
| Delta Lake | EMR + Delta Lake | HDInsight + Delta Lake | Dataproc + Delta Lake | Databricks | - | - | - |
| Iceberg | EMR + Iceberg | HDInsight + Iceberg | Dataproc + Iceberg | EMR + Iceberg | - | - | - |

---

## Migration Tools Reference / 迁移工具参考

### 云厂商原生工具 / Cloud Native Tools

#### AWS 迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| AWS DMS | 数据库迁移 | RDS, Aurora, DynamoDB, S3 |
| AWS SCT |  schema转换 | Oracle→PG, SQL Server→MySQL |
| AWS DataSync | 数据同步 | S3, EFS, FSx |
| AWS Transfer Family | 文件传输 | SFTP, FTPS, FTP |
| AWS Glue | ETL/数据集成 | 各种数据源 |
| AWS MSK Connect | Kafka Connect | Kafka迁移 |

#### Azure 迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| Azure DMS | 数据库迁移 | SQL Database, MySQL, PostgreSQL |
| Azure Data Factory | 数据集成 | 各种数据源 |
| Azure Synapse Link | 实时分析 | Cosmos DB, SQL |
| AzCopy | 存储迁移 | Blob Storage |
| Azure Database Migration Service | 数据库迁移 | 全系列数据库 |

#### GCP 迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| Database Migration Service | 数据库迁移 | Cloud SQL, AlloyDB, Spanner |
| Storage Transfer Service | 存储迁移 | Cloud Storage |
| BigQuery Data Transfer Service | 数据仓库迁移 | BigQuery |
| Datastream | CDC实时同步 | Oracle, MySQL, PostgreSQL |
| Cloud Composer | 工作流编排 | 复杂迁移场景 |

#### 阿里云迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| 数据传输服务 DTS | 数据库迁移 | RDS, PolarDB, AnalyticDB |
| 闪电立方 | 离线数据迁移 | OSS, NAS |
| DataWorks | 数据集成 | 大数据平台 |
| MaxCompute Migration | 数据仓库迁移 | MaxCompute |

#### 华为云迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| 数据复制服务 DRS | 数据库迁移 | RDS, GaussDB, DWS |
| 对象存储迁移服务 OMS | 存储迁移 | OBS |
| 大数据迁移服务 | 大数据迁移 | MRS |
| CDM | 云数据迁移 | 各种数据源 |

#### 腾讯云迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| 数据传输服务 DTS | 数据库迁移 | TDSQL, Redis, MongoDB |
| COS Migration | 存储迁移 | COS |
| 云数据迁移 CDM | 离线迁移 | 各种数据源 |
| EMR迁移工具 | 大数据迁移 | EMR |

#### 火山引擎迁移工具
| 工具名称 | 支持场景 | 适用产品 |
|---------|---------|---------|
| 数据传输服务 DTS | 数据库迁移 | RDS, ByteHouse |
| 对象存储迁移 | 存储迁移 | TOS |
| EMR迁移 | 大数据迁移 | EMR |

### 开源工具 / Open Source Tools

| 工具名称 | 类型 | 支持场景 | 优缺点 |
|---------|------|---------|--------|
| Apache Sqoop | 数据迁移 | RDBMS↔Hadoop | 成熟稳定，仅批处理 |
| Apache Kafka | 流式传输 | 实时CDC | 高吞吐，需自建 |
| Debezium | CDC工具 | 实时变更捕获 | 开源CDC标准 |
| Flink CDC | 流处理 | 实时同步 | 低延迟，复杂 |
| Airbyte | ELT工具 | 多源同步 | 社区活跃，企业版收费 |
| Meltano | ELT工具 | 数据管道 | 开源，生态丰富 |
| pg_dump/pg_restore | PostgreSQL | PG迁移 | 官方工具，可靠 |
| mysqldump | MySQL | MySQL迁移 | 官方工具，简单 |
| MongoDB Connector | MongoDB | MongoDB迁移 | 官方支持 |

---

## Migration Assessment Framework / 迁移评估框架

### 1. 技术评估 / Technical Assessment

#### 1.1 源端分析 / Source Analysis
```
□ 数据库版本和配置
□ 数据量和增长率
□ 表结构和schema复杂度
□ 存储过程、触发器、函数
□ 索引和约束
□ 字符集和排序规则
□ 时区设置
□ 连接数和并发量
□ QPS/TPS指标
□ 峰值负载特征
```

#### 1.2 依赖分析 / Dependency Analysis
```
□ 应用连接方式（直连/连接池）
□ 数据库链路（主从、级联）
□ ETL作业依赖
□ 报表和数据仓库依赖
□ 备份和归档策略
□ 监控和告警配置
```

#### 1.3 兼容性评估 / Compatibility Assessment
```
□ SQL方言差异
□ 数据类型映射
□ 函数和运算符兼容性
□ 存储过程转换复杂度
□ 特定功能替代方案（如Oracle RAC→PG）
```

### 2. 业务评估 / Business Assessment

#### 2.1 停机时间要求 / Downtime Requirements
```
□ 允许的停机窗口
□ 业务高峰期和低峰期
□ 数据一致性要求（强一致/最终一致）
□ 回滚时间要求
```

#### 2.2 合规要求 / Compliance Requirements
```
□ 数据主权要求
□ 加密要求（传输加密、静态加密）
□ 审计日志要求
□ 数据保留策略
□ 行业标准（HIPAA, PCI-DSS, GDPR等）
```

### 3. 成本评估 / Cost Assessment

#### 3.1 迁移成本 / Migration Costs
```
□ 工具许可费用
□ 网络传输费用
□ 临时资源费用
□ 人力投入成本
□ 培训和认证成本
```

#### 3.2 运营成本 / Operational Costs
```
□ 目标端产品费用
□ 存储和计算费用
□ 网络费用
□ 运维人力成本
□ 三年TCO对比
```

---

## POC Plan Template / POC方案模板

### POC Scope / POC范围
```
1. 数据规模: 选择代表性数据集（建议10-100GB）
2. 功能验证: 核心CRUD操作、复杂查询、事务
3. 性能测试: 基准测试、压力测试、并发测试
4. 工具验证: 迁移工具功能、稳定性、易用性
```

### POC Timeline / POC时间线
```
Week 1: 环境准备和工具部署
Week 2: 小规模数据迁移测试
Week 3: 全量功能验证和性能测试
Week 4: 问题修复和优化，输出POC报告
```

### POC Success Criteria / POC成功标准
```
□ 数据完整性: 100%数据准确迁移
□ 性能指标: 目标端性能达到源端90%以上
□ 功能兼容: 核心功能100%可用
□ 迁移时间: 在业务允许的时间窗口内完成
□ 工具稳定性: 无重大故障，可监控可告警
```

---

## Risk Management / 风险管理

### 一、数据层风险 / Data Layer Risks

#### 1.1 数据一致性风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **主键冲突** | 源端和目标端自增主键冲突 | pt-table-checksum校验 | 迁移前重置自增值或改用UUID | 停止同步，手动修复冲突数据 |
| **字符集乱码** | 字符集转换导致中文乱码 | 抽样数据比对 | 统一使用utf8mb4，检查排序规则 | 重新迁移受影响表，转换字符集 |
| **时区差异** | 时间戳数据因时区设置不同而偏移 | 对比时间字段 | 统一使用UTC时区 | 批量更新时间字段，加时区偏移 |
| **浮点精度** | FLOAT/DOUBLE精度丢失 | 数值字段校验 | 使用DECIMAL替代浮点类型 | 重新导入，修改字段类型 |
| **大对象损坏** | BLOB/TEXT字段截断或损坏 | 大字段抽样检查 | 调整max_allowed_packet参数 | 单独导出导入大对象字段 |
| **JSON格式** | JSON字段解析错误 | JSON_VALID检查 | 验证JSON格式，处理特殊字符 | 修复JSON数据后重新同步 |

#### 1.2 数据丢失风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **Binlog丢失** | 源端binlog被清理导致增量中断 | 监控binlog保留期 | 设置binlog保留期>7天，监控磁盘 | 重新全量迁移 |
| **网络超时** | 大表迁移时网络超时导致数据不完整 | 行数对比 | 分批迁移大表，设置合理超时 | 重新迁移失败表 |
| **事务回滚** | 迁移过程中事务回滚导致数据不一致 | 事务监控 | 选择业务低峰期，暂停长事务 | 重新同步受影响数据 |
| **DDL变更** | 迁移期间源端DDL导致同步失败 | DDL变更监控 | 迁移期间锁定DDL或使用在线DDL | 修复表结构后重新同步 |

### 二、架构层风险 / Architecture Risks

#### 2.1 性能风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **连接池耗尽** | 应用连接数超过目标端限制 | 连接数监控 | 评估连接数，调整max_connections | 扩容目标端或优化连接池 |
| **慢查询激增** | 迁移后SQL执行计划改变 | 慢查询日志分析 | 迁移前收集执行计划，重建索引 | SQL优化，添加 Hint |
| **存储瓶颈** | 数据增长导致存储不足 | 存储容量监控 | 预留50%存储空间，设置告警 | 紧急扩容存储 |
| **IO延迟** | 存储性能不达标 | IO性能监控 | POC测试IO性能，选择合适存储类型 | 升级存储类型或分片 |
| **锁竞争** | 高并发场景下锁等待增加 | 锁监控 | 优化事务粒度，调整隔离级别 | 限流或优化SQL |

#### 2.2 高可用风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **主从延迟** | 只读节点延迟导致读不到最新数据 | 复制延迟监控 | 监控延迟，设置告警阈值 | 切换到主节点读或等待同步 |
| **脑裂风险** | 双写场景下数据冲突 | 数据一致性校验 | 使用分布式锁或严格单写 | 人工介入，数据修复 |
| **切换失败** | 故障切换时服务不可用 | 切换演练 | 定期演练切换流程 | 强制切换或人工介入 |
| **备份失效** | 备份数据损坏或不可用 | 定期恢复演练 | 多重备份，定期验证 | 使用其他备份副本 |

### 三、应用层风险 / Application Layer Risks

#### 3.1 兼容性风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **SQL方言** | 特定数据库语法不兼容 | SQL扫描工具 | 提前识别，改写SQL | 使用兼容语法或中间件 |
| **函数差异** | 自定义函数或内置函数行为不同 | 功能测试 | 建立函数映射表，改写函数 | 应用层适配或创建兼容函数 |
| **存储过程** | 存储过程语法或功能差异 | 存储过程测试 | 逐条验证存储过程 | 重写存储过程 |
| **触发器** | 触发器执行顺序或权限问题 | 触发器测试 | 验证触发器逻辑和权限 | 调整触发器或应用层补偿 |
| **视图差异** | 视图定义或性能差异 | 视图测试 | 验证视图查询计划 | 优化视图定义 |

#### 3.2 连接风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **连接串错误** | 应用连接配置错误 | 连接测试 | 切换前验证连接串 | 快速修改配置回滚 |
| **驱动不兼容** | JDBC/ODBC驱动版本问题 | 驱动测试 | 提前测试驱动兼容性 | 更换驱动版本 |
| **认证失败** | 用户名密码或权限问题 | 认证测试 | 提前创建账号并验证权限 | 修复权限或重置密码 |
| **SSL/TLS** | 加密连接配置问题 | SSL连接测试 | 配置证书，测试加密连接 | 临时关闭SSL或修复证书 |

### 四、运维层风险 / Operations Risks

#### 4.1 监控告警风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **监控盲区** | 迁移后监控未覆盖 | 监控清单检查 | 提前配置目标端监控 | 紧急添加监控项 |
| **告警失效** | 告警规则不生效 | 告警测试 | 测试告警通道，验证规则 | 人工巡检，修复告警 |
| **日志丢失** | 审计日志未正确记录 | 日志验证 | 配置日志收集，验证完整性 | 启用备用日志收集 |
| **指标断层** | 历史指标数据丢失 | 指标备份 | 导出历史指标，建立基线 | 从备份恢复指标数据 |

#### 4.2 安全合规风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **数据泄露** | 迁移过程中数据暴露 | 安全审计 | 加密传输，访问控制 | 立即停止迁移，安全审查 |
| **权限过大** | 迁移账号权限过度授权 | 权限审计 | 最小权限原则，及时回收 | 回收权限，重新授权 |
| **合规违规** | 数据跨境或保留策略违规 | 合规检查 | 提前评估合规要求 | 停止迁移，法律咨询 |
| **审计缺失** | 迁移操作无审计记录 | 审计日志检查 | 开启全量审计，保留日志 | 补录操作记录 |

### 五、项目层风险 / Project Risks

#### 5.1 进度风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **时间估算不准** | 迁移耗时超预期 | 里程碑检查 | 预留缓冲时间，分阶段实施 | 调整时间窗口或增加资源 |
| **资源不足** | 人力或计算资源不足 | 资源监控 | 提前规划资源，建立资源池 | 申请紧急资源或延期 |
| **依赖延迟** | 上下游系统未就绪 | 依赖检查 | 建立依赖清单，提前协调 | 调整计划或并行执行 |
| **范围蔓延** | 迁移范围不断扩大 | 范围控制 | 明确范围，变更控制流程 | 评估影响，决策是否接受 |

#### 5.2 沟通风险
| 风险场景 | 风险描述 | 检测方法 | 预防措施 | 应急处理 |
|---------|---------|---------|---------|---------|
| **信息不同步** | 相关方未及时获取信息 | 沟通检查 | 建立沟通机制，定期同步 | 紧急会议，补发信息 |
| **决策延迟** | 关键决策未能及时做出 | 决策跟踪 | 明确决策人和时限 | 升级决策，临时决策 |
| **知识流失** | 关键人员离职或不可用 | 知识备份 | 文档化，多人备份 | 紧急培训，外部支持 |

### 风险矩阵 / Risk Matrix

```
影响程度
    高 |  数据丢失    业务中断    安全泄露
       |  合规违规    成本超支    架构失败
       |
    中 |  性能下降    兼容性问题  进度延迟
       |  工具故障    人员技能    监控盲区
       |
    低 |  文档缺失    沟通不畅    配置错误
       |  依赖延迟    范围蔓延    告警失效
       +--------------------------------
         低          中          高
                  发生概率
```

### 风险应对策略 / Risk Response Strategies

#### 规避 (Avoid)
- 选择成熟的迁移工具和方案
- 避开业务高峰期进行迁移
- 充分测试后再生产实施

#### 转移 (Transfer)
- 购买云厂商技术支持服务
- 引入专业迁移服务商
- 购买数据安全保险

#### 减轻 (Mitigate)
- 建立多重备份机制
- 实施分阶段迁移
- 加强监控和告警

#### 接受 (Accept)
- 低概率低影响的风险
- 建立应急预算
- 准备应急响应预案

---

## Pre-Migration Checklist / 迁移前检查清单

### 一、环境准备检查 / Environment Preparation

#### 1.1 源端环境检查
```
□ 确认源数据库版本和补丁级别
□ 检查源数据库运行状态（无告警、无故障）
□ 验证binlog/log归档已开启且格式正确
□ 确认binlog/log保留期足够（建议≥7天）
□ 检查源端存储空间（避免迁移期间撑满）
□ 验证源端网络带宽和稳定性
□ 确认源端防火墙允许迁移工具访问
□ 检查源端CPU/内存使用率（避免迁移时资源争用）
```

#### 1.2 目标端环境检查
```
□ 目标云账号已开通并完成实名认证
□ 目标产品已购买/创建，状态正常
□ 目标端VPC网络已配置，与源端网络互通
□ 目标端安全组/防火墙规则已配置
□ 目标端存储空间充足（建议预留50%增长空间）
□ 目标端参数已优化（缓冲区、连接数等）
□ 目标端监控告警已配置
□ 目标端备份策略已配置
```

#### 1.3 迁移工具检查
```
□ 迁移工具已安装/开通，版本最新
□ 迁移工具许可证有效（如需要）
□ 源端和目标端连接已测试通过
□ 迁移工具账号权限已配置（最小权限原则）
□ 迁移工具日志路径已配置，磁盘空间充足
□ 迁移工具监控告警已配置
```

### 二、数据检查 / Data Verification

#### 2.1 数据完整性检查
```
□ 统计源端数据总量（表数量、行数、存储大小）
□ 识别大表（单表>10GB或>1000万行）
□ 识别大对象字段（BLOB/CLOB/JSON等）
□ 检查是否有分区表，记录分区策略
□ 检查是否有外键约束，记录依赖关系
□ 检查是否有触发器，记录触发逻辑
□ 检查是否有存储过程/函数，统计数量
□ 检查是否有视图，记录视图定义
□ 检查是否有自定义类型
□ 检查是否有定时任务/事件
```

#### 2.2 数据质量检查
```
□ 检查是否有损坏的表（CHECK TABLE）
□ 检查是否有孤立记录
□ 检查主键重复或空值
□ 检查外键完整性
□ 检查数据一致性（校验和）
□ 检查字符集一致性
□ 检查时区设置一致性
```

### 三、应用检查 / Application Verification

#### 3.1 应用连接检查
```
□ 统计应用连接数峰值和平均值
□ 识别所有连接源（应用服务器、BI工具、ETL等）
□ 检查连接池配置（大小、超时设置）
□ 验证应用使用的数据库账号和权限
□ 检查应用是否有硬编码连接信息
□ 确认应用重连机制
```

#### 3.2 SQL兼容性检查
```
□ 收集应用SQL样本（慢查询、高频查询）
□ 检查是否有特定数据库方言SQL
□ 检查是否有存储过程调用
□ 检查是否有自定义函数调用
□ 检查是否有特定Hint或优化器指令
□ 验证SQL在目标端的执行计划
```

### 四、业务检查 / Business Verification

#### 4.1 时间窗口确认
```
□ 确认业务低峰期时间段
□ 确认允许的停机时间上限
□ 确认迁移时间窗口（开始和结束时间）
□ 确认回滚决策时间点
□ 确认业务验证时间
```

#### 4.2 相关方确认
```
□ 业务方已知晓迁移计划并同意
□ DBA团队已准备好支持
□ 应用团队已准备好支持
□ 网络团队已准备好支持
□ 安全团队已审核迁移方案
□ 客服/运维团队已准备好应对咨询
```

### 五、备份检查 / Backup Verification

```
□ 源端全量备份已完成，备份文件可用
□ 备份文件已验证可恢复
□ 备份文件存储在安全位置（跨地域）
□ 目标端测试数据已备份（如需要回滚）
□ 配置文件已备份（参数文件、用户权限等）
□ 应用配置已备份（连接串等）
```

### 六、应急预案检查 / Contingency Plan

```
□ 回滚方案已制定并文档化
□ 回滚操作步骤已验证
□ 紧急联系人清单已更新
□ 升级路径已明确
□ 应急资源已预留（计算、存储、网络）
□ 故障演练已完成（如可能）
```

---

## Post-Migration Validation / 迁移后验证指南

### 一、数据验证 / Data Validation

#### 1.1 数据量验证
```sql
-- 表数量对比
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_schema = 'your_database';

-- 各表行数对比（抽样）
SELECT table_name, table_rows 
FROM information_schema.tables 
WHERE table_schema = 'your_database';

-- 存储大小对比
SELECT table_schema, 
       ROUND(SUM(data_length+index_length)/1024/1024/1024, 2) AS total_gb
FROM information_schema.tables 
WHERE table_schema = 'your_database';
```

#### 1.2 数据一致性验证
```bash
# 使用pt-table-checksum进行校验
pt-table-checksum \
  --host=source_host \
  --user=checksum_user \
  --password='xxx' \
  --databases=your_database \
  --replicate=percona.checksums

# 查看差异
pt-table-sync --print --execute \
  h=source_host,u=user,p=pass,D=db,t=table \
  h=target_host,u=user,p=pass,D=db,t=table
```

#### 1.3 数据抽样验证
```sql
-- 随机抽样对比
SELECT * FROM table_name 
WHERE id IN (
  SELECT FLOOR(RAND() * (SELECT MAX(id) FROM table_name))
  UNION SELECT FLOOR(RAND() * (SELECT MAX(id) FROM table_name))
  UNION SELECT FLOOR(RAND() * (SELECT MAX(id) FROM table_name))
);

-- 边界值检查
SELECT * FROM table_name ORDER BY id ASC LIMIT 10;
SELECT * FROM table_name ORDER BY id DESC LIMIT 10;
```

### 二、功能验证 / Functional Validation

#### 2.1 数据库对象验证
```
□ 所有表已创建，结构正确
□ 所有索引已创建
□ 所有外键约束已创建
□ 所有触发器已创建且启用
□ 所有存储过程/函数已创建
□ 所有视图已创建且可查询
□ 所有用户和权限已配置
```

#### 2.2 业务功能验证
```
□ 核心业务流程测试通过
□ 插入操作正常
□ 更新操作正常
□ 删除操作正常
□ 查询操作正常
□ 事务提交/回滚正常
□ 批量操作正常
□ 定时任务/事件正常
```

### 三、性能验证 / Performance Validation

#### 3.1 基准测试
```bash
# Sysbench性能测试
sysbench oltp_read_write \
  --mysql-host=target_host \
  --mysql-user=user \
  --mysql-password=pass \
  --mysql-db=database \
  --tables=10 \
  --table-size=100000 \
  --threads=16 \
  --time=300 \
  run
```

#### 3.2 关键SQL验证
```
□ 慢查询在目标端执行时间对比
□ 高频查询执行计划对比
□ 复杂JOIN查询性能对比
□ 聚合查询性能对比
□ 存储过程执行时间对比
```

#### 3.3 并发测试
```
□ 连接数达到峰值时稳定性
□ 并发写入性能
□ 读写混合场景性能
□ 长连接稳定性
```

### 四、监控验证 / Monitoring Validation

```
□ 数据库状态监控正常
□ 性能指标采集正常（QPS/TPS/延迟）
□ 告警规则生效
□ 告警通知渠道正常
□ 日志收集正常
□ 备份任务正常执行
□ 监控大屏数据正常
```

---

## Troubleshooting Guide / 故障排查指南

### 一、连接问题 / Connection Issues

#### 1.1 无法连接源数据库
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 连接超时 | 网络不通/防火墙 | ping/telnet测试 | 开放防火墙端口 |
| 认证失败 | 用户名密码错误 | 检查账号权限 | 重置密码/授权 |
| 拒绝连接 | 连接数满/未启动 | 检查服务状态 | 重启服务/扩容 |
| SSL错误 | 证书问题 | 检查证书配置 | 更新证书/禁用SSL |

#### 1.2 无法连接目标数据库
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 白名单限制 | IP未授权 | 检查安全组/白名单 | 添加IP到白名单 |
| VPC不通 | 网络配置错误 | 检查路由表 | 配置正确路由 |
| 实例未就绪 | 创建中或故障 | 查看控制台状态 | 等待创建/重启实例 |

### 二、同步问题 / Synchronization Issues

#### 2.1 全量迁移失败
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 迁移中断 | 网络不稳定 | 查看迁移日志 | 重试/分批迁移 |
| 数据截断 | 字段长度不足 | 检查表结构 | 修改字段长度 |
| 主键冲突 | 重复数据 | 检查主键策略 | 重置自增值 |
| 内存不足 | 大表导致OOM | 监控资源使用 | 分批导出/增加内存 |

#### 2.2 增量同步延迟
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 延迟持续增长 | 目标端写入慢 | 检查目标端性能 | 优化目标端/扩容 |
| 延迟波动大 | 网络抖动 | 检查网络质量 | 使用专线/VPN |
| 同步停滞 | binlog丢失 | 检查binlog保留 | 重新全量迁移 |
| 单表延迟 | 大事务/DDL | 检查慢事务 | 拆分事务/暂停DDL |

#### 2.3 同步中断
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 报错停止 | 语法错误/不兼容 | 查看错误日志 | 修复SQL/跳过错误 |
| 连接断开 | 超时/网络 | 检查连接状态 | 调整超时/重连 |
| 权限不足 | 账号权限变更 | 检查账号权限 | 重新授权 |

### 三、性能问题 / Performance Issues

#### 3.1 迁移后性能下降
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 查询变慢 | 索引缺失 | 对比执行计划 | 重建索引 |
| 写入变慢 | 磁盘IO瓶颈 | 监控IO指标 | 升级存储类型 |
| 连接变慢 | 网络延迟 | ping测试 | 优化网络/就近部署 |
| 整体变慢 | 参数未优化 | 对比参数配置 | 优化数据库参数 |

#### 3.2 资源使用过高
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| CPU 100% | SQL优化器问题 | 查看慢查询 | 优化SQL/加Hint |
| 内存耗尽 | 缓冲区设置过大 | 检查内存配置 | 调整缓冲区大小 |
| 磁盘满 | 日志/临时文件 | 检查磁盘使用 | 清理日志/扩容 |
| 连接数满 | 连接池配置问题 | 检查连接数 | 调整max_connections |

### 四、数据问题 / Data Issues

#### 4.1 数据不一致
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 行数不一致 | 迁移中断/过滤 | 对比行数 | 重新同步差异表 |
| 校验和不一致 | 字符集/精度 | 抽样对比 | 修复字符集/重新迁移 |
| 时间不一致 | 时区设置不同 | 检查时区 | 统一时区/转换时间 |
| 中文乱码 | 字符集转换错误 | 检查字符集 | 重新导出/指定字符集 |

#### 4.2 数据丢失
| 症状 | 可能原因 | 排查步骤 | 解决方案 |
|-----|---------|---------|---------|
| 部分数据缺失 | WHERE条件过滤 | 检查迁移配置 | 重新迁移/补录 |
| 大对象缺失 | 大字段截断 | 检查字段长度 | 调整max_allowed_packet |
| 增量数据缺失 | binlog未同步 | 检查同步位点 | 重新定位binlog |

---

## Best Practices / 最佳实践

### 一、迁移策略最佳实践

1. **分阶段迁移**
   - 先迁移非核心业务验证流程
   - 再迁移核心业务，降低风险
   - 最后迁移关键业务，确保稳定

2. **双跑验证**
   - 迁移后保持双写一段时间
   - 对比两端数据一致性
   - 逐步切流，可控回滚

3. **灰度切换**
   - 先切换部分读流量
   - 验证无问题后切换写流量
   - 最后全量切换

### 二、性能优化最佳实践

1. **迁移前优化**
   - 清理无用数据和索引
   - 归档历史数据
   - 优化大表结构

2. **迁移中优化**
   - 分批迁移大表
   - 调整批量大小
   - 并行迁移多个表

3. **迁移后优化**
   - 重建索引和统计信息
   - 优化数据库参数
   - 启用查询缓存

### 三、安全最佳实践

1. **数据加密**
   - 传输加密（TLS/SSL）
   - 存储加密（TDE）
   - 敏感字段加密

2. **访问控制**
   - 最小权限原则
   - 临时账号及时回收
   - 操作审计日志

3. **数据脱敏**
   - 测试环境脱敏
   - 日志脱敏
   - 监控脱敏

### 四、运维最佳实践

1. **监控覆盖**
   - 迁移前建立监控基线
   - 迁移中加强监控频率
   - 迁移后持续监控

2. **文档完善**
   - 架构文档更新
   - 运维手册更新
   - 应急预案更新

3. **知识传递**
   - 团队培训
   - 操作手册
   - 经验总结

---

## Output Template / 输出模板

```markdown
# 云数据迁移方案 | Cloud Data Migration Plan

## 1. 迁移概览 (Migration Overview)

| 项目 | 详情 |
|-----|------|
| 源端云厂商 | [Source Cloud] |
| 源端产品 | [Source Product] |
| 目标云厂商 | [Target Cloud] |
| 目标产品 | [Target Product] |
| 数据类型 | [Database/Big Data/Data Lake] |
| 预估数据量 | [Volume] |
| 迁移策略 | [Offline/Online/Dual-Write/CDC] |

## 2. 产品选型建议 (Product Recommendation)

### 2.1 推荐方案
**目标产品**: [Product Name]
**选型理由**:
- 功能覆盖度: [X]%
- 性能匹配度: [X]%
- 成本对比: [分析]
- 生态集成: [分析]

### 2.2 备选方案
[如有备选，列出对比]

## 3. 迁移工具清单 (Migration Tools)

### 3.1 主要工具
| 工具名称 | 类型 | 用途 | 费用 |
|---------|------|------|------|
| [Tool 1] | 云原生/开源 | [用途] | [费用] |
| [Tool 2] | 云原生/开源 | [用途] | [费用] |

### 3.2 辅助工具
[监控、校验、回滚工具]

## 4. 迁移评估报告 (Migration Assessment)

### 4.1 技术评估
- 复杂度: [高/中/低]
- 风险等级: [高/中/低]
- 预估工时: [X人天]

### 4.2 兼容性分析
[SQL差异、数据类型映射、功能替代方案]

### 4.3 成本评估
- 迁移成本: [金额]
- 运营成本对比: [源端 vs 目标端]
- 三年TCO: [分析]

## 5. POC方案 (POC Plan)

### 5.1 POC范围
[数据范围、功能范围、测试场景]

### 5.2 POC时间线
[详细时间安排]

### 5.3 成功标准
[量化指标]

## 6. 迁移实施步骤 (Implementation Steps)

### Phase 1: 准备阶段
1. [步骤1]
2. [步骤2]

### Phase 2: 迁移执行
1. [步骤1]
2. [步骤2]

### Phase 3: 验证切换
1. [步骤1]
2. [步骤2]

## 7. 风险与应对 (Risks & Mitigation)

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| [风险1] | [高/中/低] | [高/中/低] | [措施] |

## 8. 回滚方案 (Rollback Plan)

[详细回滚步骤和触发条件]

## 9. 注意事项 (Key Considerations)

- [注意点1]
- [注意点2]

## 10. 相关资源 (Resources)

- [官方文档链接]
- [最佳实践指南]
- [工具文档]
```

---

## Important Notes / 重要说明

1. **工具选择优先级**: 始终优先推荐云厂商原生工具，其次考虑开源方案
2. **数据安全**: 所有迁移方案必须包含数据加密和完整性校验
3. **业务连续性**: 关键业务必须提供在线迁移或双写方案
4. **成本控制**: 提供详细的成本对比和优化建议
5. **文档完整**: 确保所有步骤可执行、可验证、可回滚
