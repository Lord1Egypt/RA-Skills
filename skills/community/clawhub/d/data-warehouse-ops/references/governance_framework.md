# 数据治理框架 (Data Governance Framework)

## 单一事实来源 (SSOT) 定义

### SSOT 矩阵模板

| 业务实体 | 权威源系统 | 主键 | 更新频率 | 数据 Owner | Golden Record 规则 |
|----------|-----------|------|----------|------------|-------------------|
| 客户 | CRM | customer_id | 实时 | 销售部 | 以 CRM 为准，合并 ERP 补充字段 |
| 产品 | ERP | sku_code | 每日 | 产品部 | 以 ERP 为主，电商平台信息补充 |
| 订单 | 电商平台 | order_id | 5 分钟 | 运营部 | 以电商平台为准 |
| 供应商 | SRM | vendor_code | 每日 | 采购部 | 以 SRM 为准 |
| 员工 | HRIS | employee_id | 每日 | 人力资源部 | 以 HRIS 为准 |

### SSOT 设计原则
1. **一个实体一个权威源** — 明确每个实体的 primary source system
2. **尽量避免双写** — 所有写入应通过权威源系统
3. **冲突解决规则** — 当多源数据冲突时，定义优先级规则
4. **Golden Record** — 从多源合并生成最优记录

## 数据域划分

### 常见数据域

| 数据域 | 包含实体 | 典型 Owner | 安全等级 |
|--------|----------|-----------|----------|
| 客户域 | 客户、联系人、地址 | CMO/销售 VP | 机密 |
| 产品域 | 产品、SKU、品类 | CPO/产品 VP | 内部 |
| 订单域 | 订单、支付、退款 | COO/运营 VP | 机密 |
| 供应链域 | 供应商、采购、库存 | CSCO/供应链 VP | 内部 |
| 财务域 | 科目、凭证、报表 | CFO | 绝密 |
| 人力域 | 员工、薪资、绩效 | CHRO | 绝密 |
| 营销域 | 活动、渠道、线索 | CMO | 内部 |
| 日志域 | 行为日志、点击流 | CTO | 内部 |

## 数据分类分级

### 四级分类标准

| 等级 | 名称 | 定义 | 示例 | 访问控制 | 加密要求 |
|------|------|------|------|----------|----------|
| L4 | 绝密 | 泄露造成严重损害 | 薪资、财务凭证、核心算法 | 严格最小权限 | 必须加密 |
| L3 | 机密 | 泄露造成较大损害 | 客户 PII、订单明细、合同 | 按角色授权 | 建议加密 |
| L2 | 内部 | 泄露造成轻微损害 | 产品目录、组织架构 | 员工可见 | 可选 |
| L1 | 公开 | 可对外发布 | 年报、公开 API 文档 | 无限制 | 不需要 |

### PII 数据处理清单
- [ ] 识别并标记所有含 PII 的列（姓名、手机号、邮箱、身份证号、地址等）
- [ ] PII 列默认脱敏显示（`xxx****@domain.com`, `138****1234`）
- [ ] PII 传输必须加密
- [ ] PII 保留期限不超过业务需求 + 法定要求
- [ ] 定期审计 PII 访问日志

## 角色与职责

| 角色 | 职责 | 典型人员 |
|------|------|----------|
| 数据 Owner | 数据资产的最终负责人，审批访问权限 | 业务部门 VP/Director |
| 数据管家 (Steward) | 日常数据质量管理、元数据维护 | 资深业务分析师 |
| 数据架构师 | 数据模型设计、标准制定 | 数据架构师 |
| 数据工程师 | ETL 管道开发维护、数据平台运维 | 数据工程师 |
| 数据消费者 | 使用数据进行分析和决策 | 分析师、产品经理 |
| 数据安全官 | 合规审计、安全策略 | CISO/DPO |

## 数据标准

### 命名规范
```
[层级]_[实体类型]_[业务域]_[描述]

层级: ods(贴源层) / dwd(明细层) / dws(汇总层) / ads(应用层) / dim(维度层)
实体类型: fact(事实表) / dim(维度表) / agg(聚合表)
示例: dwd_fact_ecommerce_orders, dim_customer, dws_agg_daily_sales
```

### 字段命名规范
- 使用小写 + 下划线 (snake_case)
- 布尔字段以 `is_` / `has_` 开头
- 时间字段以 `_at` 结尾（created_at, updated_at）
- 日期字段以 `_date` 结尾
- 外键以 `fk_` 开头
- 代理键以 `_sk` 结尾

### 数据类型标准
- ID 类：使用适当长度的 VARCHAR（不用 INT，避免溢出和类型混淆）
- 金额类：DECIMAL(18,2) 或 NUMERIC
- 日期：DATE（不带时间）
- 时间戳：TIMESTAMP / DATETIME（带时间）
- 文本：TEXT / STRING（不限制长度以避免截断）

## 数据生命周期

### 各阶段策略

| 阶段 | 热数据 (0-30天) | 温数据 (30-90天) | 冷数据 (90-365天) | 归档 (>1年) |
|------|----------------|------------------|-------------------|-------------|
| 存储层 | 高性能 SSD | 标准存储 | 低频存储 | 归档存储 |
| 查询 SLA | 秒级 | 分钟级 | 分钟级 | 查询即恢复 |
| 分区策略 | DAY | MONTH | YEAR | YEAR |
| 访问频率 | 高频 | 中频 | 低频 | 按需 |
| 备份策略 | 每日增量 | 每周全量 | 每月全量 | 只读快照 |

### 数据保留策略
```yaml
retention_policies:
  transaction_data:
    retention: "7 years"  # 财务合规要求
    archive_after: "2 years"
  user_behavior_logs:
    retention: "1 year"
    archive_after: "90 days"
  staging_tables:
    retention: "7 days"
    auto_cleanup: true
  temp_tables:
    retention: "24 hours"
    auto_cleanup: true
```

## 数据访问控制

### RBAC 模型
```yaml
roles:
  data_admin:
    permissions: [SELECT, INSERT, UPDATE, DELETE, DDL]
    scope: all_schemas
  data_engineer:
    permissions: [SELECT, INSERT, UPDATE]
    scope: [dwd, dws, dim, staging]
  data_analyst:
    permissions: [SELECT]
    scope: [dwd, dws, ads, dim]
  data_consumer:
    permissions: [SELECT]
    scope: [ads]  # 仅应用层
    masking_rules:
      - column_pattern: "*email*"
        mask: "email_mask"
      - column_pattern: "*phone*"
        mask: "phone_mask"
```

## 检查清单

- [ ] 是否定义了核心业务实体的 SSOT？
- [ ] 是否建立了数据域划分和 Owner 任命？
- [ ] 是否完成了数据分类分级？
- [ ] 命名规范是否文档化并强制执行？
- [ ] 是否定义了数据生命周期策略？
- [ ] 访问控制是否基于最小权限原则？
- [ ] PII 数据是否被识别和脱敏？
- [ ] 是否有定期的数据治理委员会会议？
