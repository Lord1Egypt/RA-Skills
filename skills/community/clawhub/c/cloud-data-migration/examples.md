# 云数据迁移方案示例 | Cloud Data Migration Examples

本文档提供实际的云数据迁移场景示例，展示如何使用本skill生成完整的迁移方案。

---

## Example 1: AWS RDS MySQL → 阿里云RDS MySQL (目标产品未指定)

### 用户输入
> "我们需要将AWS RDS MySQL迁移到阿里云，数据量大约500GB，业务是电商订单系统，要求停机时间不超过2小时。"

### Skill执行过程

#### Step 1: 解析输入
- **源端**: AWS
- **源产品**: RDS MySQL
- **目标端**: 阿里云
- **目标产品**: 未指定（需要推荐）
- **数据量**: 500GB
- **业务场景**: 电商订单系统（OLTP）
- **停机要求**: ≤2小时

#### Step 2: 目标产品推荐
根据产品映射表和业务场景分析：

**推荐方案**: 阿里云RDS MySQL高可用版
- **选型理由**:
  - 功能覆盖度: 100%（同构迁移）
  - 性能匹配: AWS RDS db.m5.xlarge ≈ 阿里云4核16G
  - 高可用架构: 三节点企业版，RPO=0
  - 与电商场景契合: 支持高并发订单处理

**备选方案**: 阿里云PolarDB MySQL
- 适用于未来数据增长预期大的场景
- 计算存储分离，扩展性更好

#### Step 3: 迁移策略选择
基于停机时间要求（≤2小时）和数据量（500GB）：

**推荐策略**: 在线迁移（Online Migration）+ DTS持续同步
- 全量迁移: 使用DTS进行初始数据同步
- 增量同步: Binlog实时同步
- 切换: 2小时内完成DNS切换和业务验证

#### Step 4: 迁移工具选择

**主要工具**:
| 工具 | 类型 | 用途 | 费用 |
|-----|------|------|------|
| 阿里云DTS | 云原生 | 全量+增量数据同步 | ¥1,200/月（数据同步实例） |
| AWS DMS | 云原生 | 初始评估和测试 | $29.52/月（dms.c4.large） |

**辅助工具**:
- Percona XtraBackup: 物理备份验证
- pt-table-checksum: 数据一致性校验
- CloudCanal: 结构迁移和对象校验

---

### 完整迁移方案输出

```markdown
# AWS RDS MySQL → 阿里云RDS MySQL 迁移方案

## 1. 迁移概览

| 项目 | 详情 |
|-----|------|
| 源端云厂商 | AWS |
| 源端产品 | Amazon RDS MySQL 8.0 |
| 目标云厂商 | 阿里云 |
| 目标产品 | RDS MySQL高可用版（三节点企业版） |
| 数据类型 | 关系型数据库（OLTP） |
| 预估数据量 | 500GB |
| 迁移策略 | 在线迁移（DTS持续同步） |

## 2. 产品选型建议

### 2.1 推荐方案: 阿里云RDS MySQL高可用版

**选型理由**:
- ✅ 功能覆盖度: 100%（MySQL 8.0全功能兼容）
- ✅ 性能匹配: 建议规格4核16G，与AWS db.m5.xlarge性能相当
- ✅ 高可用性: 三节点企业版，金融级RPO=0保障
- ✅ 电商场景优化: 支持高并发订单写入，QPS可达20000+
- ✅ 生态集成: 与阿里云SLB、Redis、OSS等服务无缝集成

**推荐规格**:
```
实例规格: mysql.n2.xlarge (4核16G)
存储类型: ESSD云盘 PL1
存储容量: 800GB（预留60%增长空间）
数据库版本: MySQL 8.0
高可用模式: 三节点企业版
```

### 2.2 备选方案: PolarDB MySQL

如预期数据快速增长（年增长率>100%），建议选择PolarDB：
- 计算存储分离，存储自动扩展
- 一写多读，读性能线性扩展
- 秒级备份恢复

## 3. 迁移工具清单

### 3.1 主要工具

| 工具名称 | 类型 | 用途 | 费用 |
|---------|------|------|------|
| 阿里云DTS | 云原生 | 全量数据迁移+增量同步 | ¥1,200/月（大型实例） |
| AWS DMS | 云原生 | 初始评估测试（可选） | $29.52/月 |
| Percona Toolkit | 开源 | 数据一致性校验 | 免费 |

### 3.2 辅助工具

| 工具名称 | 用途 |
|---------|------|
| pt-table-checksum | 表级数据一致性校验 |
| pt-table-sync | 数据修复（如不一致） |
| mysqlslap | 压力测试和性能基准 |
| CloudCanal | 结构对象迁移验证 |

### 3.3 监控工具

| 工具名称 | 用途 |
|---------|------|
| 阿里云CloudMonitor | 目标端性能监控 |
| AWS CloudWatch | 源端性能基线采集 |
| DTS控制台 | 同步延迟监控 |

## 4. 迁移评估报告

### 4.1 技术评估

**复杂度**: ⭐⭐（简单）
- 同构MySQL迁移，无SQL语法转换
- DTS工具成熟，自动化程度高
- 社区案例丰富，风险可控

**风险等级**: ⭐⭐（低）
- 同构数据库，兼容性问题少
- 在线迁移，可回滚
- 阿里云DTS服务SLA 99.95%

**预估工时**: 15人天
- 环境准备: 3天
- 迁移实施: 5天
- 测试验证: 4天
- 切换上线: 2天
- 观察保障: 1天

### 4.2 兼容性分析

**SQL兼容性**: 100%
- MySQL 8.0 → MySQL 8.0，无语法差异
- 存储过程、触发器、函数完全兼容
- 字符集utf8mb4保持一致

**配置差异**:
| 参数 | AWS RDS | 阿里云RDS | 建议 |
|-----|---------|----------|------|
| innodb_buffer_pool_size | 75%内存 | 75%内存 | 保持一致 |
| max_connections | 根据规格 | 根据规格 | 需评估 |
| time_zone | UTC | SYSTEM | 建议统一为UTC |

**注意事项**:
- 检查并统一SQL_MODE设置
- 评估长事务对迁移的影响
- 确认是否有外键约束（影响同步顺序）

### 4.3 成本评估

#### 迁移成本
| 项目 | 费用 | 说明 |
|-----|------|------|
| DTS数据同步实例 | ¥1,200 | 大型实例，1个月 |
| 跨云网络流量 | ¥400 | 500GB出站流量 |
| 临时ECS（压测） | ¥300 | 2台4核8G，1个月 |
| 人力成本 | ¥15,000 | 15人天 |
| **总计** | **¥16,900** | - |

#### 运营成本对比（月度）

| 项目 | AWS RDS | 阿里云RDS | 节省 |
|-----|---------|----------|------|
| 实例费用 | $350 | ¥1,800 | - |
| 存储费用 (800GB) | $92 | ¥640 | - |
| 备份存储 (500GB) | $50 | ¥200 | - |
| **月度总计** | **$492** | **¥2,640** | 约15% |

*注: 实际成本需根据具体配置和折扣计算*

## 5. POC方案

### 5.1 POC范围

**数据范围**:
- 选择3-5个核心业务表（约50GB）
- 包含大表（>1000万行）和关联表
- 覆盖主要业务场景的数据分布

**功能验证**:
- CRUD操作验证
- 存储过程执行
- 触发器功能
- 事务一致性
- 并发写入测试

**性能测试**:
- 基线性能对比（QPS/TPS）
- 峰值负载模拟
- 慢查询分析

### 5.2 POC时间线（2周）

| 阶段 | 时间 | 任务 |
|-----|------|------|
| Week 1 Day 1-2 | 环境准备 | 创建阿里云RDS实例，配置网络 |
| Week 1 Day 3-5 | 数据迁移 | 使用DTS迁移POC数据 |
| Week 2 Day 1-3 | 功能验证 | 应用连接测试，功能验证 |
| Week 2 Day 4-5 | 性能测试 | 压力测试，性能调优 |
| Week 2 Day 5 PM | 报告输出 | POC总结报告 |

### 5.3 POC成功标准

| 指标 | 目标值 | 验证方法 |
|-----|--------|---------|
| 数据完整性 | 100% | pt-table-checksum校验 |
| 功能可用性 | 100% | 核心业务流程测试通过 |
| 性能指标 | ≥90% | TPS对比测试 |
| 迁移时间 | ≤预估 | 全量迁移耗时记录 |

## 6. 迁移实施步骤

### Phase 1: 准备阶段（Week 1）

#### Day 1-2: 环境准备
1. **阿里云环境搭建**
   - 创建VPC和交换机
   - 创建RDS MySQL实例（4核16G，三节点）
   - 配置白名单和安全组
   - 创建监控告警

2. **网络配置**
   - 配置AWS VPC与阿里云VPC的VPN连接（或公网访问）
   - 测试网络连通性
   - 评估网络带宽（建议≥100Mbps）

3. **账号权限**
   - 创建AWS DMS访问账号
   - 创建阿里云DTS访问账号
   - 确认binlog权限（REPLICATION SLAVE, REPLICATION CLIENT）

#### Day 3: 源端评估
1. **数据量统计**
   ```sql
   SELECT 
     table_name,
     ROUND(data_length/1024/1024/1024, 2) AS data_size_gb,
     table_rows
   FROM information_schema.tables
   WHERE table_schema = 'your_database'
   ORDER BY data_length DESC;
   ```

2. **大表识别**
   - 识别单表>10GB的表
   - 评估是否有分区表
   - 检查是否有LOB字段

3. **性能基线采集**
   - 记录AWS RDS的QPS/TPS基线
   - 收集慢查询日志
   - 记录连接数峰值

#### Day 4-5: 对象预处理
1. **Schema导出**
   ```bash
   mysqldump -h aws-rds-endpoint -u admin -p \
     --no-data --single-transaction \
     --routines --triggers \
     your_database > schema.sql
   ```

2. **Schema导入阿里云**
   ```bash
   mysql -h aliyun-rds-endpoint -u root -p \
     your_database < schema.sql
   ```

3. **配置优化**
   - 根据AWS参数调整阿里云RDS参数
   - 设置时区为UTC
   - 配置慢查询日志

### Phase 2: 迁移执行（Week 2-3）

#### Week 2 Day 1: DTS任务创建
1. **创建DTS数据同步任务**
   - 登录阿里云DTS控制台
   - 选择"数据同步" → "创建任务"
   - 配置源库信息（AWS RDS连接串）
   - 配置目标库信息（阿里云RDS）

2. **选择同步对象**
   - 选择需要迁移的数据库
   - 选择需要同步的表（可选择排除大表）
   - 配置对象名映射（如有需要）

3. **高级配置**
   - 选择"全量数据初始化+增量数据同步"
   - 配置冲突处理策略（建议"覆盖"）
   - 设置同步性能（根据网络调整）

#### Week 2 Day 2-5: 全量迁移
1. **启动全量迁移**
   - 启动DTS任务
   - 监控迁移进度
   - 记录全量迁移耗时

2. **进度监控**
   - DTS控制台查看迁移进度
   - 监控网络流量
   - 监控源端和目标端性能

3. **全量完成验证**
   - 记录全量完成时间
   - 检查表数量一致性
   - 抽样数据比对

#### Week 3 Day 1-3: 增量同步观察
1. **延迟监控**
   - 监控同步延迟（目标<1秒）
   - 记录延迟峰值和原因
   - 评估业务高峰期延迟情况

2. **数据一致性校验**
   ```bash
   # 使用pt-table-checksum进行校验
   pt-table-checksum \
     --host=aws-rds-endpoint \
     --user=admin \
     --password='xxx' \
     --databases=your_database \
     --replicate=percona.checksums
   ```

3. **问题处理**
   - 处理同步错误
   - 修复数据不一致
   - 优化同步性能

### Phase 3: 切换上线（Week 3 Day 4-5）

#### Day 4: 切换前准备
1. **切换前检查清单**
   - [ ] 数据一致性校验通过
   - [ ] 同步延迟<1秒且稳定
   - [ ] 应用连接测试通过
   - [ ] 回滚方案准备就绪
   - [ ] 业务低峰期确认

2. **应用准备**
   - 更新应用配置文件（连接串）
   - 准备蓝绿部署或金丝雀发布
   - 通知相关业务方

3. **备份源端**
   ```bash
   # 创建最终备份
   aws rds create-db-snapshot \
     --db-instance-identifier your-rds \
     --db-snapshot-identifier pre-migration-final
   ```

#### Day 5: 正式切换

**切换时间窗口**: 建议选择业务低峰期（如凌晨2:00-4:00）

1. **T-30分钟: 最终校验**
   - 确认同步延迟为0
   - 执行最终数据校验
   - 确认无长事务

2. **T-10分钟: 停止写入**
   - 将应用切换为只读模式
   - 确认无新写入
   - 等待最后binlog同步完成

3. **T-0: 切换**
   - 停止DTS同步任务
   - 更新应用数据库连接配置
   - 重启应用服务
   - 验证应用功能

4. **T+30分钟: 验证**
   - 核心业务功能验证
   - 订单流水验证
   - 支付链路验证
   - 监控告警检查

5. **T+2小时: 观察期**
   - 持续监控性能指标
   - 观察错误日志
   - 确认无异常后正式完成

## 7. 风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| **网络中断导致同步失败** | 高 | 中 | 配置VPN冗余，DTS自动重试机制 |
| **数据不一致** | 高 | 低 | pt-table-checksum校验，pt-table-sync修复 |
| **同步延迟过大** | 中 | 中 | 提前扩容DTS规格，优化大表迁移策略 |
| **应用连接失败** | 高 | 低 | 提前测试连接，准备快速回滚方案 |
| **性能不达标** | 中 | 中 | POC充分测试，预留参数调优时间 |
| **大表迁移超时** | 中 | 中 | 大表单独处理，分批次迁移 |

## 8. 回滚方案

### 8.1 触发条件
- 切换后30分钟内发现严重数据不一致
- 应用功能验证失败且无法快速修复
- 性能严重下降影响业务

### 8.2 回滚步骤（15分钟内完成）

1. **停止应用写入**（2分钟）
   ```bash
   # 将应用切为只读
   ```

2. **切换DNS/连接配置**（5分钟）
   - 修改应用配置，指回AWS RDS
   - 重启应用服务

3. **验证回滚**（5分钟）
   - 验证应用连接AWS RDS正常
   - 验证核心业务功能

4. **恢复写入**（3分钟）
   - 取消只读模式
   - 恢复业务

### 8.3 数据补偿
如切换后有新数据写入阿里云，需评估数据补偿方案：
- 数据量小: 人工补录
- 数据量大: 编写脚本对比补录

## 9. 注意事项

### 9.1 迁移前
- ⚠️ 确保AWS RDS binlog已开启且保留时间≥7天
- ⚠️ 评估长事务对迁移的影响
- ⚠️ 检查是否有外键约束（影响同步顺序）
- ⚠️ 确认字符集一致（建议utf8mb4）
- ⚠️ 备份所有存储过程和触发器定义

### 9.2 迁移中
- ⚠️ 监控源端binlog空间，避免撑满磁盘
- ⚠️ 关注DTS同步延迟，及时处理告警
- ⚠️ 避免在同步期间执行DDL操作
- ⚠️ 大表迁移时关注网络带宽

### 9.3 迁移后
- ⚠️ 及时清理AWS RDS资源（确认稳定运行后）
- ⚠️ 更新监控告警配置
- ⚠️ 备份策略切换至阿里云
- ⚠️ 文档更新（架构图、运维手册）

## 10. 相关资源

### 官方文档
- [阿里云DTS文档](https://help.aliyun.com/document_detail/26628.html)
- [AWS DMS文档](https://docs.aws.amazon.com/dms/)
- [MySQL官方迁移指南](https://dev.mysql.com/doc/refman/8.0/en/replication.html)

### 最佳实践
- [阿里云数据库迁移最佳实践](https://www.alibabacloud.com/help/doc-detail/148033.htm)
- [AWS数据库迁移白皮书](https://docs.aws.amazon.com/whitepapers/latest/aws-database-migration-service/oracle-to-postgresql.html)

### 工具下载
- [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit)
- [pt-table-checksum文档](https://docs.percona.com/percona-toolkit/pt-table-checksum.html)
```

---

## Example 2: 华为云DWS → AWS Redshift (目标产品已指定)

### 用户输入
> "我们要把华为云DWS数据仓库迁移到AWS Redshift，数据量5TB，主要用于BI报表和数据分析，可以接受周末停机。"

### Skill执行过程

#### Step 1: 解析输入
- **源端**: 华为云
- **源产品**: DWS (Data Warehouse Service)
- **目标端**: AWS
- **目标产品**: Redshift（已指定）
- **数据量**: 5TB
- **业务场景**: BI报表、数据分析（OLAP）
- **停机要求**: 周末（可接受较长停机）

#### Step 2: 产品验证
验证Redshift是否适合DWS迁移：
- ✅ 都是MPP架构的数据仓库
- ✅ 都支持标准SQL
- ✅ 都兼容PostgreSQL生态
- ⚠️ 注意: SQL方言有差异，需评估

#### Step 3: 迁移策略选择
基于停机时间充裕（周末）和数据量（5TB）：

**推荐策略**: 离线迁移（Offline Migration）+ S3中转
- 华为云DWS导出至OBS
- 从OBS下载到本地或中转服务器
- 上传至AWS S3
- S3 COPY命令导入Redshift

---

### 完整迁移方案输出

```markdown
# 华为云DWS → AWS Redshift 迁移方案

## 1. 迁移概览

| 项目 | 详情 |
|-----|------|
| 源端云厂商 | 华为云 |
| 源端产品 | Data Warehouse Service (DWS) 8.1 |
| 目标云厂商 | AWS |
| 目标产品 | Amazon Redshift Serverless |
| 数据类型 | 数据仓库（OLAP） |
| 预估数据量 | 5TB |
| 迁移策略 | 离线迁移（S3中转） |

## 2. 产品选型确认

### 2.1 AWS Redshift配置建议

**选型确认**: Amazon Redshift Serverless
- **选型理由**:
  - 与DWS同为MPP架构，查询性能相当
  - Serverless模式，无需管理基础设施
  - 自动扩展，适合BI报表的波峰波谷
  - 与AWS BI工具（QuickSight）深度集成

**推荐配置**:
```
模式: Redshift Serverless
Base RPU: 32 (可根据查询复杂度调整)
命名空间: production-dwh
工作组: bi-analytics-workgroup
```

**如选择预置集群**:
```
节点类型: ra3.xlplus
节点数量: 3
总存储: 24TB (可扩展)
```

## 3. 迁移工具清单

### 3.1 主要工具

| 工具名称 | 类型 | 用途 | 费用 |
|---------|------|------|------|
| GDS (Gauss Data Service) | 华为云原生 | DWS数据导出至OBS | 免费 |
| AWS S3 | AWS原生 | 数据中转存储 | $0.023/GB/月 |
| Redshift COPY | AWS原生 | 数据导入Redshift | 计算费用 |
| AWS DataSync | AWS原生 | 数据传输（如需要） | $0.0125/GB |

### 3.2 辅助工具

| 工具名称 | 用途 |
|---------|------|
| pg_dump / gsql | Schema导出 |
| AWS SCT | Schema转换和评估 |
| Redshift Query Editor v2 | 数据验证 |
| CloudWatch | 监控和告警 |

## 4. 迁移评估报告

### 4.1 技术评估

**复杂度**: ⭐⭐⭐（中等）
- 异构数据仓库迁移，SQL方言有差异
- 数据导出导入流程较长
- Schema和存储过程需转换

**风险等级**: ⭐⭐⭐（中等）
- 离线迁移，停机时间较长
- 数据类型映射需仔细验证
- 性能调优需要专业知识

**预估工时**: 25人天
- 评估和准备: 5天
- Schema迁移: 5天
- 数据迁移: 5天
- 测试验证: 7天
- 切换上线: 3天

### 4.2 兼容性分析

**SQL方言差异**:

| 特性 | 华为云DWS | AWS Redshift | 兼容性 |
|-----|----------|-------------|--------|
| 窗口函数 | 支持 | 支持 | ✅ 兼容 |
| CTE (WITH) | 支持 | 支持 | ✅ 兼容 |
| 存储过程 | PL/pgSQL | PL/pgSQL | ⚠️ 部分差异 |
| 自定义函数 | 支持 | 支持 | ⚠️ 需验证 |
| 分区表 | 支持 | 支持 | ⚠️ 语法差异 |
| 物化视图 | 支持 | 支持 | ✅ 兼容 |

**数据类型映射**:

| DWS类型 | Redshift类型 | 说明 |
|--------|-------------|------|
| BIGINT | BIGINT | 直接映射 |
| VARCHAR(n) | VARCHAR(n) | 直接映射 |
| NUMERIC(p,s) | DECIMAL(p,s) | 直接映射 |
| TIMESTAMP | TIMESTAMP | 直接映射 |
| TIMESTAMP WITH TIME ZONE | TIMESTAMPTZ | 直接映射 |
| BYTEA | VARBYTE | 需注意 |
| JSON | SUPER | 建议使用SUPER |
| ARRAY | SUPER | 建议使用SUPER |

### 4.3 成本评估

#### 迁移成本
| 项目 | 费用 | 说明 |
|-----|------|------|
| OBS存储费用 | ¥50 | 5TB存储1周 |
| S3存储费用 | $115 | 5TB存储1个月 |
| 出站流量费用 | ¥3,750 | 5TB从华为云流出 |
| Redshift Serverless | $600 | 32 RPU × 1个月 |
| 人力成本 | ¥25,000 | 25人天 |
| **总计** | **约¥35,000** | - |

#### 运营成本对比（月度）

| 项目 | 华为云DWS | AWS Redshift | 差异 |
|-----|----------|-------------|------|
| 计算资源 | 3节点×¥2,500 | Serverless $600 | AWS更省 |
| 存储 (5TB) | ¥1,250 | $115 | AWS更省 |
| **月度总计** | **¥8,750** | **约$715** | AWS节省约40% |

## 5. POC方案

### 5.1 POC范围

**数据范围**:
- 选择1-2个核心事实表（约500GB）
- 包含维度表和关联关系
- 覆盖典型BI查询场景

**功能验证**:
- 复杂JOIN查询
- 窗口函数查询
- 聚合查询性能
- 存储过程转换

### 5.2 POC时间线（1周）

| 阶段 | 时间 | 任务 |
|-----|------|------|
| Day 1 | Schema迁移 | 使用AWS SCT转换Schema |
| Day 2-3 | 数据迁移 | 导出500GB测试数据 |
| Day 4 | 查询测试 | 执行典型BI查询 |
| Day 5 | 性能对比 | DWS vs Redshift性能对比 |

## 6. 迁移实施步骤

### Phase 1: Schema迁移

#### Step 1: Schema导出
```bash
# 使用gsql导出DWS schema
gsql -d your_database -U your_user -W your_password \
  -c "\dt" > tables.txt

gsql -d your_database -U your_user -W your_password \
  -f export_schema.sql > schema_dws.sql
```

#### Step 2: Schema转换（使用AWS SCT）
1. 安装AWS Schema Conversion Tool
2. 创建新工程，选择源: Huawei DWS，目标: Amazon Redshift
3. 连接源和目标数据库
4. 运行评估报告，查看转换复杂度
5. 执行自动转换
6. 手动处理无法自动转换的对象

#### Step 3: Schema导入Redshift
```sql
-- 在Redshift Query Editor中执行转换后的DDL
CREATE SCHEMA your_schema;

-- 创建表（示例）
CREATE TABLE your_schema.fact_sales (
    sale_id BIGINT,
    product_id INTEGER,
    customer_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    amount DECIMAL(18,2)
)
DISTSTYLE KEY
DISTKEY (product_id)
SORTKEY (sale_date);
```

### Phase 2: 数据迁移

#### Step 1: DWS数据导出至OBS
```sql
-- 使用GDS并行导出
CREATE FOREIGN TABLE gds_export (
    LIKE fact_sales
)
SERVER gsmpp_server
OPTIONS (
    LOCATION 'gsfs://your-bucket/export/',
    FORMAT 'TEXT',
    DELIMITER '|',
    NULL ''
);

INSERT INTO gds_export SELECT * FROM fact_sales;
```

#### Step 2: OBS数据下载
```bash
# 使用obsutil下载数据
obsutil cp obs://your-bucket/export/ ./local-export/ -r -f

# 或使用华为云控制台批量下载
```

#### Step 3: 上传至AWS S3
```bash
# 使用AWS CLI上传
aws s3 sync ./local-export/ s3://your-redshift-bucket/import/ \
  --profile your-profile

# 或使用S3控制台批量上传
```

#### Step 4: Redshift数据导入
```sql
-- 使用COPY命令导入
COPY your_schema.fact_sales
FROM 's3://your-redshift-bucket/import/fact_sales.txt'
IAM_ROLE 'arn:aws:iam::your-account:role/RedshiftS3Access'
DELIMITER '|'
NULL AS ''
IGNOREHEADER 0
COMPUPDATE ON;

-- 验证数据
SELECT COUNT(*) FROM your_schema.fact_sales;
```

### Phase 3: 验证与优化

#### 数据验证
```sql
-- 行数校验
SELECT 'fact_sales' as table_name, COUNT(*) as row_count 
FROM your_schema.fact_sales
UNION ALL
SELECT 'dim_product', COUNT(*) FROM your_schema.dim_product;

-- 抽样数据比对
SELECT * FROM your_schema.fact_sales 
WHERE sale_id IN (12345, 67890, 11111)
ORDER BY sale_id;
```

#### 性能优化
```sql
-- 分析表，更新统计信息
ANALYZE your_schema.fact_sales;

-- 检查查询执行计划
EXPLAIN 
SELECT product_id, SUM(amount)
FROM your_schema.fact_sales
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY product_id;

-- 优化DISTKEY和SORTKEY
-- 根据查询模式调整分布键和排序键
```

## 7. 风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| **数据导出超时** | 高 | 中 | 分批导出，使用GDS并行导出 |
| **网络传输中断** | 高 | 低 | 使用断点续传工具，如rclone |
| **数据类型不匹配** | 中 | 中 | POC充分测试，建立类型映射表 |
| **查询性能下降** | 中 | 中 | 优化DISTKEY/SORTKEY，使用物化视图 |
| **存储过程不兼容** | 中 | 高 | 使用AWS SCT转换，手动调整 |
| **S3费用超支** | 低 | 低 | 及时清理临时数据，使用生命周期策略 |

## 8. 回滚方案

由于为离线迁移，回滚相对简单：

1. **保留华为云DWS集群**（建议保留1个月）
2. **如Redshift出现问题**:
   - 切换BI工具连接回DWS
   - 重新配置报表数据源
   - 验证数据一致性

## 9. 注意事项

- ⚠️ DWS的存储过程使用PL/pgSQL，与Redshift基本兼容但需测试
- ⚠️ 大表导出时注意OBS存储费用
- ⚠️ Redshift的SUPER类型可替代DWS的JSON/ARRAY类型
- ⚠️ 时区处理需统一（建议使用UTC）
- ⚠️ COPY命令失败时查看STL_LOAD_ERRORS表排查

## 10. 相关资源

- [AWS SCT文档](https://docs.aws.amazon.com/SchemaConversionTool/)
- [Redshift COPY命令](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html)
- [华为云GDS文档](https://support.huaweicloud.com/dws/index.html)
```

---

## Example 3: 阿里云MaxCompute → GCP BigQuery (大数据平台迁移)

### 用户输入
> "我们需要将阿里云的MaxCompute迁移到Google Cloud的BigQuery，数据量50TB，主要是离线数据分析，希望尽量减少对现有ETL作业的影响。"

### 关键输出要点

**目标产品**: GCP BigQuery (已指定)

**迁移策略**: 
- 使用BigQuery Data Transfer Service + Cloud Storage中转
- 阿里云MaxCompute导出至OSS
- 使用OSS到GCS的传输服务
- BigQuery加载数据

**迁移工具**:
- 阿里云DataWorks（数据导出）
- Cloud Storage Transfer Service（跨云传输）
- BigQuery Data Transfer Service（数据加载）
- Cloud Composer（ETL作业迁移）

**关键挑战**:
- SQL方言差异（MaxCompute SQL vs Standard SQL）
- UDF迁移（Java/Python UDF转换）
- ETL作业重构（DataWorks → Cloud Composer/Dataflow）

---

## Example 4: MongoDB Atlas → Azure Cosmos DB (NoSQL迁移)

### 用户输入
> "我们目前在MongoDB Atlas上运行，想迁移到Azure Cosmos DB的MongoDB API，数据量2TB，是一个电商平台的核心数据库，要求零停机。"

### 关键输出要点

**目标产品**: Azure Cosmos DB MongoDB API (已指定)

**迁移策略**: 
- 双写迁移（Dual-Write）
- 应用层同时写入MongoDB Atlas和Cosmos DB
- 使用Azure DMS进行历史数据同步
- 逐步切读流量，最终停写MongoDB

**迁移工具**:
- Azure Database Migration Service (DMS)
- MongoDB Change Streams（实时同步）
- Azure Data Factory（批量数据迁移）

**关键挑战**:
- Cosmos DB的RU/s计费模式需要重新评估
- 部分MongoDB聚合管道可能需要调整
- 事务支持差异（Cosmos DB多文档事务限制）

---

## 使用建议

1. **目标产品未指定时**: Skill会自动分析业务场景，推荐最适合的目标产品，并提供多个备选方案对比

2. **目标产品已指定时**: Skill会验证该产品的适用性，并针对具体产品提供详细的迁移方案

3. **复杂场景**: 对于涉及多产品、大数据量的复杂迁移，建议分阶段实施，先进行POC验证

4. **工具选择**: 始终优先使用云厂商原生工具，如不满足需求再考虑开源方案

5. **风险控制**: 所有方案都包含详细的风险评估和回滚计划，确保业务连续性
