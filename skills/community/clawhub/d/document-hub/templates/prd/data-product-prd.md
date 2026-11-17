# {{product_name}} - 数据产品 PRD

> **文档状态**: {{status|default('草稿')}}  
> **版本**: {{version|default('v0.1')}}  
> **创建日期**: {{created_date}}  
> **最后更新**: {{updated_date}}  
> **作者**: {{author}}  
> **数据负责人**: {{data_lead|default('待指定')}}  
> **评审人**: {{reviewers|default('待指定')}}

---

## 1. 文档概述

### 1.1 文档目的
本文档定义 {{product_name}} 数据产品的需求规范，涵盖数据资产、指标体系、数据服务及数据治理要求。

### 1.2 目标读者
- 数据产品经理
- 数据工程师
- 数据分析师
- 算法工程师
- 业务方/数据消费者

### 1.3 术语表

| 术语 | 定义 |
|------|------|
| {{term_1|default('数据仓库 (DW)')}} | {{def_1|default('面向主题的、集成的、非易失的、时变的数据集合')}} |
| {{term_2|default('数据湖')}} | {{def_2|default('存储原始格式数据的存储库')}} |
| {{term_3|default('ETL')}} | {{def_3|default('Extract-Transform-Load，数据抽取转换加载')}} |
| {{term_4|default('数据血缘')}} | {{def_4|default('数据从产生到消费的完整链路关系')}} |

---

## 2. 产品定位与目标

### 2.1 产品定位
{{product_positioning|default('本产品定位为 [业务域] 的统一数据服务平台，为 [目标用户] 提供 [核心价值]。')}}

### 2.2 业务价值

| 价值维度 | 具体描述 | 量化目标 |
|----------|----------|----------|
| {{value_dim_1|default('决策支持')}} | {{value_desc_1|default('提供实时业务洞察')}} | {{value_target_1|default('报表产出时间从天级缩短到分钟级')}} |
| {{value_dim_2|default('效率提升')}} | {{value_desc_2|default('自动化数据处理流程')}} | {{value_target_2|default('减少 80% 人工数据处理工作')}} |
| {{value_dim_3|default('成本优化')}} | {{value_desc_3|default('统一数据口径，避免重复建设')}} | {{value_target_3|default('数据存储成本降低 30%')}} |

### 2.3 成功指标

| 指标名称 | 基线值 | 目标值 | 测量方式 |
|----------|--------|--------|----------|
| 数据覆盖率 | {{coverage_baseline|default('60%'}} | {{coverage_target|default('> 95%'}} | 核心业务数据接入比例 |
| 数据准确性 | {{accuracy_baseline|default('95%'}} | {{accuracy_target|default('> 99.5%'}} | 对账准确率 |
| 数据时效性 | {{latency_baseline|default('T+1'}} | {{latency_target|default('实时 / 分钟级'}} | 端到端延迟 |
| 用户满意度 | {{satisfaction_baseline|default('-'}} | {{satisfaction_target|default('> 4.0/5'}} | 数据消费者调研 |
| 数据服务可用性 | {{avail_baseline|default('99%'}} | {{avail_target|default('> 99.9%'}} | SLA 监控 |

---

## 3. 数据需求分析

### 3.1 数据源

| 数据源 | 类型 | 更新频率 | 数据量级 | 接入方式 |
|--------|------|----------|----------|----------|
| {{source_1|default('业务数据库')}} | {{type_1|default('MySQL')}} | {{freq_1|default('实时 (CDC)')}} | {{vol_1|default('100GB/天')}} | {{method_1|default('Debezium + Kafka')}} |
| {{source_2|default('日志系统')}} | {{type_2|default('JSON Logs')}} | {{freq_2|default('实时')}} | {{vol_2|default('500GB/天')}} | {{method_2|default('Filebeat + Kafka')}} |
| {{source_3|default('第三方 API')}} | {{type_3|default('REST API')}} | {{freq_3|default('每小时')}} | {{vol_3|default('10GB/天')}} | {{method_3|default('Airflow 调度')}} |
| {{source_4|default('埋点数据')}} | {{type_4|default('JSON')}} | {{freq_4|default('实时')}} | {{vol_4|default('1TB/天')}} | {{method_4|default('SDK + Kafka')}} |

### 3.2 数据域划分

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据域架构                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   用户域      │  │   交易域      │  │   商品域      │             │
│  │  {{domain_1}} │  │  {{domain_2}} │  │  {{domain_3}} │             │
│  │              │  │              │  │              │             │
│  │ • 用户基础    │  │ • 订单        │  │ • 商品信息    │             │
│  │ • 用户行为    │  │ • 支付        │  │ • 类目属性    │             │
│  │ • 用户标签    │  │ • 退款        │  │ • 价格库存    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   营销域      │  │   内容域      │  │   日志域      │             │
│  │  {{domain_4}} │  │  {{domain_5}} │  │  {{domain_6}} │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 数据实体

#### 3.3.1 用户域实体

| 实体名 | 实体描述 | 主键 | 关键属性 |
|--------|----------|------|----------|
| {{entity_1|default('dim_user')}} | {{entity_1_desc|default('用户维度表')}} | {{entity_1_pk|default('user_id')}} | {{entity_1_attrs|default('username, email, phone, register_time, status')}} |
| {{entity_2|default('fact_user_behavior')}} | {{entity_2_desc|default('用户行为事实表')}} | {{entity_2_pk|default('event_id')}} | {{entity_2_attrs|default('user_id, event_type, event_time, page_url, device_id')}} |
| {{entity_3|default('user_tag')}} | {{entity_3_desc|default('用户标签表')}} | {{entity_3_pk|default('user_id, tag_id')}} | {{entity_3_attrs|default('tag_name, tag_value, confidence, update_time')}} |

#### 3.3.2 交易域实体

| 实体名 | 实体描述 | 主键 | 关键属性 |
|--------|----------|------|----------|
| {{entity_4|default('fact_order')}} | {{entity_4_desc|default('订单事实表')}} | {{entity_4_pk|default('order_id')}} | {{entity_4_attrs|default('user_id, order_time, amount, status, payment_method')}} |
| {{entity_5|default('fact_payment')}} | {{entity_5_desc|default('支付事实表')}} | {{entity_5_pk|default('payment_id')}} | {{entity_5_attrs|default('order_id, payment_time, amount, channel, status')}} |

---

## 4. 指标体系

### 4.1 指标分层

```
                    ┌──────────────────┐
│                    │    业务指标       │  ← 面向业务决策
                    │   (北极星指标)    │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │    衍生指标       │  ← 业务指标拆解
                    │   (复合指标)      │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼─────────┐  ┌──────▼──────┐
│    原子指标     │  │    原子指标       │  │   原子指标   │  ← 最细粒度
│   (不可拆分)    │  │   (不可拆分)      │  │  (不可拆分)  │
└────────────────┘  └──────────────────┘  └─────────────┘
```

### 4.2 原子指标

| 指标编码 | 指标名称 | 业务定义 | 计算公式 | 数据类型 | 单位 |
|----------|----------|----------|----------|----------|------|
| {{metric_code_1|default('M001')}} | {{metric_name_1|default('订单数')}} | {{metric_def_1|default('统计周期内成功支付的订单数量')}} | {{metric_formula_1|default('COUNT(DISTINCT order_id)')}} | {{metric_type_1|default('整数')}} | {{metric_unit_1|default('笔')}} |
| {{metric_code_2|default('M002')}} | {{metric_name_2|default('GMV')}} | {{metric_def_2|default('统计周期内商品交易总额')}} | {{metric_formula_2|default('SUM(order_amount)')}} | {{metric_type_2|default('金额')}} | {{metric_unit_2|default('元')}} |
| {{metric_code_3|default('M003')}} | {{metric_name_3|default('DAU')}} | {{metric_def_3|default('日活跃用户数')}} | {{metric_formula_3|default('COUNT(DISTINCT user_id WHERE active=1)')}} | {{metric_type_3|default('整数')}} | {{metric_unit_3|default('人')}} |
| {{metric_code_4|default('M004')}} | {{metric_name_4|default('转化率')}} | {{metric_def_4|default('下单用户数/访问用户数')}} | {{metric_formula_4|default('COUNT(order_user)/COUNT(visit_user)')}} | {{metric_type_4|default('比率')}} | {{metric_unit_4|default('%')}} |

### 4.3 衍生指标

| 指标名称 | 计算公式 | 业务含义 |
|----------|----------|----------|
| {{derived_1|default('客单价')}} | {{derived_1_formula|default('GMV / 订单数')}} | {{derived_1_meaning|default('平均每笔订单金额')}} |
| {{derived_2|default('ARPU')}} | {{derived_2_formula|default('GMV / DAU')}} | {{derived_2_meaning|default('每用户平均收入')}} |
| {{derived_3|default('复购率')}} | {{derived_3_formula|default('复购用户数 / 总购买用户数')}} | {{derived_3_meaning|default('用户忠诚度指标')}} |

### 4.4 维度定义

| 维度名称 | 维度描述 | 维度值示例 |
|----------|----------|------------|
| {{dim_1|default('时间')}} | {{dim_1_desc|default('日期、时段维度')}} | {{dim_1_vals|default('2026-04-19, 第2季度, 周末')}} |
| {{dim_2|default('地域')}} | {{dim_2_desc|default('地理位置维度')}} | {{dim_2_vals|default('北京, 上海, 华东区')}} |
| {{dim_3|default('渠道')}} | {{dim_3_desc|default('流量来源维度')}} | {{dim_3_vals|default('自然搜索, 付费广告, 社交媒体')}} |
| {{dim_4|default('用户类型')}} | {{dim_4_desc|default('用户分层维度')}} | {{dim_4_vals|default('新用户, 活跃用户, 沉睡用户')}} |

---

## 5. 数据模型设计

### 5.1 建模方法论

**采用方法**: {{modeling_method|default('维度建模 (Kimball) / Data Vault / OneData')}}

### 5.2 分层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据分层架构                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  ADS (Application Data Store)                               │  │
│  │  应用数据层 - 面向具体应用场景的数据集市                      │  │
│  │  例如: 用户画像表、推荐特征表、报表数据                       │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  DWS (Data Warehouse Service)                               │  │
│  │  数据服务层 - 轻度汇总数据，按业务主题组织                    │  │
│  │  例如: 日活汇总表、订单主题宽表                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  DWD (Data Warehouse Detail)                                │  │
│  │  明细数据层 - 清洗后的业务明细数据                            │  │
│  │  例如: 订单明细表、支付明细表                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  ODS (Operational Data Store)                               │  │
│  │  操作数据层 - 原始业务数据，保持原貌                          │  │
│  │  例如: 原始订单表、原始日志表                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  数据源层 (Source)                                           │  │
│  │  业务数据库 / 日志 / API / 文件                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.3 核心表设计

#### 5.3.1 ODS 层

**表名**: {{ods_table_1|default('ods_order')}}  
**描述**: {{ods_table_1_desc|default('订单原始数据')}}  
**更新方式**: {{ods_update_1|default('每日增量')}}  
**保留周期**: {{ods_retention_1|default('30天')}}

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| {{ods_field_1|default('order_id')}} | {{ods_type_1|default('STRING')}} | {{ods_desc_1|default('订单ID')}} | {{ods_ex_1|default('ORD202404190001')}} |
| {{ods_field_2|default('raw_data')}} | {{ods_type_2|default('STRING/JSON')}} | {{ods_desc_2|default('原始JSON数据')}} | {{ods_ex_2|default('{...}')}} |
| {{ods_field_3|default('etl_time')}} | {{ods_type_3|default('TIMESTAMP')}} | {{ods_desc_3|default('数据接入时间')}} | {{ods_ex_3|default('2026-04-19 17:16:00')}} |

#### 5.3.2 DWD 层

**表名**: {{dwd_table_1|default('dwd_order_detail')}}  
**描述**: {{dwd_table_1_desc|default('订单明细事实表')}}  
**主键**: {{dwd_pk_1|default('order_id')}}  
**分区**: {{dwd_partition_1|default('dt (日期)')}}

| 字段名 | 数据类型 | 说明 | 来源 |
|--------|----------|------|------|
| {{dwd_field_1|default('order_id')}} | {{dwd_type_1|default('STRING')}} | {{dwd_desc_1|default('订单唯一标识')}} | {{dwd_src_1|default('ods_order.order_id')}} |
| {{dwd_field_2|default('user_id')}} | {{dwd_type_2|default('STRING')}} | {{dwd_desc_2|default('用户ID')}} | {{dwd_src_2|default('ods_order.user_id')}} |
| {{dwd_field_3|default('order_amount')}} | {{dwd_type_3|default('DECIMAL(18,2)')}} | {{dwd_desc_3|default('订单金额')}} | {{dwd_src_3|default('ods_order.amount')}} |
| {{dwd_field_4|default('order_status')}} | {{dwd_type_4|default('TINYINT')}} | {{dwd_desc_4|default('订单状态')}} | {{dwd_src_4|default('ods_order.status')}} |
| {{dwd_field_5|default('order_time')}} | {{dwd_type_5|default('TIMESTAMP')}} | {{dwd_desc_5|default('下单时间')}} | {{dwd_src_5|default('ods_order.create_time')}} |

#### 5.3.3 DWS 层

**表名**: {{dws_table_1|default('dws_order_daily')}}  
**描述**: {{dws_table_1_desc|default('订单日汇总表')}}  
**主键**: {{dws_pk_1|default('dt, user_id')}}  
**分区**: {{dws_partition_1|default('dt (日期)')}}

| 字段名 | 数据类型 | 说明 | 计算逻辑 |
|--------|----------|------|----------|
| {{dws_field_1|default('dt')}} | {{dws_type_1|default('STRING')}} | {{dws_desc_1|default('日期')}} | - |
| {{dws_field_2|default('user_id')}} | {{dws_type_2|default('STRING')}} | {{dws_desc_2|default('用户ID')}} | - |
| {{dws_field_3|default('order_cnt')}} | {{dws_type_3|default('BIGINT')}} | {{dws_desc_3|default('订单数')}} | {{dws_logic_3|default('COUNT(order_id)')}} |
| {{dws_field_4|default('gmv')}} | {{dws_type_4|default('DECIMAL(18,2)')}} | {{dws_desc_4|default('成交金额')}} | {{dws_logic_4|default('SUM(order_amount)')}} |

### 5.4 数据血缘

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据血缘示例                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  业务数据库                                                          │
│  ┌──────────────┐                                                   │
│  │  order_table │                                                   │
│  └──────┬───────┘                                                   │
│         │ CDC                                                       │
│         ▼                                                           │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │  ods_order   │────▶│ dwd_order    │────▶│ dws_order    │        │
│  │  (原始数据)   │     │ (清洗明细)    │     │ (日汇总)      │        │
│  └──────────────┘     └──────────────┘     └──────┬───────┘        │
│                                                    │                │
│                              ┌─────────────────────┼─────────────┐ │
│                              │                     │             │ │
│                              ▼                     ▼             ▼ │
│                       ┌──────────────┐    ┌──────────────┐ ┌────────┐│
│                       │  报表服务     │    │  推荐服务    │ │ 用户画像││
│                       └──────────────┘    └──────────────┘ └────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. 数据服务

### 6.1 服务类型

| 服务类型 | 适用场景 | 技术方案 | SLA |
|----------|----------|----------|-----|
| {{svc_type_1|default('离线查询')}} | {{svc_scene_1|default('T+1 报表')}} | {{svc_tech_1|default('Hive/Presto + BI 工具')}} | {{svc_sla_1|default('可用性 99%'}} |
| {{svc_type_2|default('实时查询')}} | {{svc_scene_2|default('实时监控')}} | {{svc_tech_2|default('ClickHouse/Doris')}} | {{svc_sla_2|default('P99 < 1s'}} |
| {{svc_type_3|default('API 服务')}} | {{svc_scene_3|default('在线应用')}} | {{svc_tech_3|default('Java/Go + Redis')}} | {{svc_sla_3|default('P99 < 100ms'}} |
| {{svc_type_4|default('文件导出')}} | {{svc_scene_4|default('大数据量导出')}} | {{svc_tech_4|default('OSS + 异步任务')}} | {{svc_sla_4|default('24h 内完成'}} |

### 6.2 API 接口设计

#### 6.2.1 指标查询接口

**接口**: `POST /v1/metrics/query`

**请求参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| metricCode | string | ✅ | 指标编码 |
| dimensions | object | ✅ | 维度过滤条件 |
| startTime | string | ✅ | 开始时间 (ISO 8601) |
| endTime | string | ✅ | 结束时间 (ISO 8601) |
| granularity | string | ❌ | 粒度: day/hour/minute |

**请求示例**
```json
{
  "metricCode": "M001",
  "dimensions": {
    "region": "华东",
    "channel": "app"
  },
  "startTime": "2026-04-01T00:00:00Z",
  "endTime": "2026-04-19T23:59:59Z",
  "granularity": "day"
}
```

**响应示例**
```json
{
  "code": 0,
  "data": {
    "metricName": "订单数",
    "unit": "笔",
    "values": [
      {"time": "2026-04-01", "value": 12580},
      {"time": "2026-04-02", "value": 13200}
    ],
    "total": 25780
  }
}
```

#### 6.2.2 实时数据接口

**接口**: `GET /v1/realtime/{metricCode}`

**特性**: {{realtime_feature|default('WebSocket 长连接推送 / 短轮询')}}

### 6.3 数据产品形态

| 产品形态 | 描述 | 目标用户 | 交付方式 |
|----------|------|----------|----------|
| {{product_1|default('数据大屏')}} | {{product_1_desc|default('实时业务监控大屏')}} | {{product_1_user|default('管理层/运营')}} | {{product_1_deliver|default('Web 页面 / 电视投屏')}} |
| {{product_2|default('BI 报表')}} | {{product_2_desc|default('自助分析报表')}} | {{product_2_user|default('分析师/运营')}} | {{product_2_deliver|default('BI 平台 / Excel')}} |
| {{product_3|default('数据 API')}} | {{product_3_desc|default('数据服务接口')}} | {{product_3_user|default('开发工程师')}} | {{product_3_deliver|default('REST API / SDK')}} |
| {{product_4|default('数据标签')}} | {{product_4_desc|default('用户/商品标签')}} | {{product_4_user|default('算法/运营')}} | {{product_4_deliver|default('标签平台 / API')}} |

---

## 7. 数据治理

### 7.1 数据质量

#### 7.1.1 质量规则

| 规则类型 | 规则说明 | 检查频率 | 告警阈值 |
|----------|----------|----------|----------|
| {{rule_1|default('完整性')}} | {{rule_1_desc|default('必填字段非空率 > 99%'}} | {{rule_1_freq|default('每小时')}} | {{rule_1_threshold|default('空值率 > 1%'}} |
| {{rule_2|default('准确性')}} | {{rule_2_desc|default('主键唯一性'}} | {{rule_2_freq|default('每日')}} | {{rule_2_threshold|default('重复数 > 0'}} |
| {{rule_3|default('一致性')}} | {{rule_3_desc|default('跨表数据一致性'}} | {{rule_3_freq|default('每日')}} | {{rule_3_threshold|default('差异率 > 0.1%'}} |
| {{rule_4|default('时效性')}} | {{rule_4_desc|default('数据延迟 < 阈值'}} | {{rule_4_freq|default('每5分钟'}} | {{rule_4_threshold|default('延迟 > 30min'}} |

#### 7.1.2 质量监控

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据质量监控                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │  规则引擎     │───▶│  质量检查     │───▶│  评分报告     │         │
│  │  (定义规则)   │    │  (自动执行)   │    │  (可视化)     │         │
│  └──────────────┘    └──────────────┘    └──────────────┘         │
│                              │                                      │
│                              ▼                                      │
│                       ┌──────────────┐                             │
│                       │  异常告警     │                             │
│                       │  (钉钉/邮件)  │                             │
│                       └──────────────┘                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 数据安全

#### 7.2.1 分级分类

| 数据级别 | 定义 | 访问控制 | 脱敏要求 |
|----------|------|----------|----------|
| {{level_1|default('L1 公开')}} | {{level_1_def|default('可公开数据')}} | {{level_1_ctrl|default('无需认证')}} | {{level_1_mask|default('无需脱敏')}} |
| {{level_2|default('L2 内部')}} | {{level_2_def|default('公司内部数据')}} | {{level_2_ctrl|default('员工认证')}} | {{level_2_mask|default('部分脱敏')}} |
| {{level_3|default('L3 敏感')}} | {{level_3_def|default('敏感业务数据')}} | {{level_3_ctrl|default('按需申请')}} | {{level_3_mask|default('严格脱敏')}} |
| {{level_4|default('L4 机密')}} | {{level_4_def|default('核心机密数据')}} | {{level_4_ctrl|default('审批+审计')}} | {{level_4_mask|default('禁止明文')}} |

#### 7.2.2 脱敏规则

| 数据类型 | 脱敏方式 | 示例 |
|----------|----------|------|
| {{mask_type_1|default('手机号')}} | {{mask_rule_1|default('保留前3后4')}} | {{mask_ex_1|default('138****8000')}} |
| {{mask_type_2|default('邮箱')}} | {{mask_rule_2|default('保留首字母和域名')}} | {{mask_ex_2|default('a***@example.com')}} |
| {{mask_type_3|default('身份证号')}} | {{mask_rule_3|default('保留前3后4')}} | {{mask_ex_3|default('110***********1234')}} |
| {{mask_type_4|default('银行卡')}} | {{mask_rule_4|default('保留后4位')}} | {{mask_ex_4|default('************1234')}} |

### 7.3 元数据管理

| 元数据类型 | 内容 | 管理工具 |
|------------|------|----------|
| {{meta_1|default('业务元数据')}} | {{meta_1_content|default('指标定义、业务口径、负责人')}} | {{meta_1_tool|default('指标平台')}} |
| {{meta_2|default('技术元数据')}} | {{meta_2_content|default('表结构、字段类型、存储位置')}} | {{meta_2_tool|default('数据地图')}} |
| {{meta_3|default('操作元数据')}} | {{meta_3_content|default('ETL 执行记录、数据血缘')}} | {{meta_3_tool|default('调度平台')}} |

---

## 8. 项目规划

### 8.1 里程碑

| 阶段 | 交付物 | 验收标准 | 计划时间 |
|------|--------|----------|----------|
| {{milestone_1|default('需求确认')}} | {{deliver_1|default('PRD 终稿')}} | {{criteria_1|default('评审通过')}} | {{date_1|default('TBD')}} |
| {{milestone_2|default('数据接入')}} | {{deliver_2|default('ODS 层完成')}} | {{criteria_2|default('数据源 100% 接入')}} | {{date_2|default('TBD')}} |
| {{milestone_3|default('模型开发')}} | {{deliver_3|default('DWD/DWS 层完成')}} | {{criteria_3|default('核心模型上线')}} | {{date_3|default('TBD')}} |
| {{milestone_4|default('指标上线')}} | {{deliver_4|default('核心指标可用')}} | {{criteria_4|default('指标准确性 > 99%'}} | {{date_4|default('TBD')}} |
| {{milestone_5|default('产品发布')}} | {{deliver_5|default('数据服务上线')}} | {{criteria_5|default('SLA 达标')}} | {{date_5|default('TBD')}} |

### 8.2 资源需求

| 资源类型 | 需求 | 说明 |
|----------|------|------|
| {{res_type_1|default('存储')}} | {{res_req_1|default('新增 [X] TB')}} | {{res_note_1|default('数据湖 + 数仓')}} |
| {{res_type_2|default('计算')}} | {{res_req_2|default('[Y] CU 计算资源')}} | {{res_note_2|default('ETL + 查询')}} |
| {{res_type_3|default('人力')}} | {{res_req_3|default('数据工程师 [Z] 人')}} | {{res_note_3|default('开发 + 运维')}} |

---

## 9. 附录

### 9.1 参考文档
- {{data_ref_1|default('[数据仓库建模规范](链接)')}} - {{data_ref_1_desc|default('OneData 建模标准')}}
- {{data_ref_2|default('[指标管理规范](链接)')}} - {{data_ref_2_desc|default('指标定义与命名规范')}}
- {{data_ref_3|default('[数据安全规范](链接)')}} - {{data_ref_3_desc|default('数据分级分类标准')}}

### 9.2 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| {{version|default('v0.1')}} | {{created_date}} | 初稿创建 | {{author}} |

---

## 10. 评审记录

| 评审轮次 | 日期 | 评审人 | 结论 | 备注 |
|----------|------|--------|------|------|
| 需求评审 | {{review_date_1|default('-')}} | {{reviewer_1|default('-')}} | {{result_1|default('待评审')}} | {{note_1|default('-')}} |
| 模型评审 | {{review_date_2|default('-')}} | {{reviewer_2|default('-')}} | {{result_2|default('待评审')}} | {{note_2|default('-')}} |
