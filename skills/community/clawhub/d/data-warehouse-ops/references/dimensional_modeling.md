# 维度建模最佳实践 (Dimensional Modeling Best Practices)

## Kimball 四步法

### Step 1: 选择业务流程
明确要建模的业务流程（订单、发货、支付、注册等），一个事实表对应一个业务流程。

### Step 2: 声明粒度
定义事实表每行代表什么。粒度越细越好 — 原子粒度最灵活。
- 订单行项目级：一行 = 一个订单的一个商品
- 交易级：一行 = 一次交易
- 事件级：一行 = 一个用户行为事件

### Step 3: 确定维度
围绕事实表的维度：谁、什么、何时、何地、为什么。
- 谁 (Who): 客户、用户、供应商
- 什么 (What): 产品、服务、SKU
- 何时 (When): 日期、时间
- 何地 (Where): 门店、地区、渠道
- 为什么 (Why): 促销、活动、原因代码

### Step 4: 确定事实（度量值）
数字型的、可加总的业务度量：数量、金额、成本、时长等。

## 星型模型 vs 雪花模型

| 特性 | 星型模型 | 雪花模型 |
|------|----------|----------|
| 维度表规范化 | 非规范化（宽表） | 规范化（多层级） |
| 查询性能 | ⭐⭐⭐⭐⭐ 少 JOIN | ⭐⭐⭐ 多 JOIN |
| 存储空间 | 较大 | 较小 |
| 维护复杂度 | 低 | 高 |
| 适用场景 | BI 报表、自助分析 | 数据治理要求高的场景 |

**推荐：默认使用星型模型，仅在以下情况考虑雪花模型：**
- 维度层次多且频繁独立查询
- 存储成本是核心约束
- 已有成熟的维度层级管理体系

## 事实表类型

### 1. 事务事实表 (Transaction Fact)
- 最常用，粒度 = 单次业务事件
- 每发生一次事件插入一行
- 可累加度量
- 示例：`fact_orders`（每行 = 一个订单）

### 2. 周期快照事实表 (Periodic Snapshot)
- 按固定周期（日/周/月）记录状态
- 半可加度量（余额类不可跨时间累加）
- 示例：`fact_inventory_daily`（每日库存快照）

### 3. 累积快照事实表 (Accumulating Snapshot)
- 跟踪有明确生命周期的流程（如订单从创建到交付）
- 一行记录整个生命周期
- 包含多个里程碑日期
- 示例：`fact_order_fulfillment`（订单履约过程）

### 4. 无事实的事实表 (Factless Fact)
- 记录事件发生或条件满足，无数值度量
- 示例：`fact_attendance`（学生出勤记录）、`fact_promotion_coverage`（促销覆盖）

## 缓慢变化维度 (SCD) 策略

### Type 0 — 保留原值
不做任何更新。适用于不可变属性（如出生日期）。

### Type 1 — 覆盖 (Overwrite)
直接更新旧值，不保留历史。
```sql
UPDATE dim_customer SET city = '深圳' WHERE customer_bk = 'C001';
```
- 适用：修正错误数据、不关心历史的属性
- 风险：历史报表结果会变化

### Type 2 — 新增行 (Add Row) ⭐ 推荐
新增行保留历史，通过时间段标记有效期。
```sql
-- Step 1: 关闭当前记录
UPDATE dim_customer
SET valid_to = CURRENT_TIMESTAMP(), is_current = FALSE
WHERE customer_bk = 'C001' AND is_current = TRUE;

-- Step 2: 插入新版本
INSERT INTO dim_customer (...) VALUES (..., is_current = TRUE);
```
- 优点：完整历史追踪
- 缺点：表行数增长
- 代理键（Surrogate Key）：每个版本一个独立 SK

### Type 3 — 新增列
新增列保留上一个值。
```sql
-- dim_customer 表新增 previous_city, effective_date 列
UPDATE dim_customer SET previous_city = city, city = '深圳', effective_date = CURRENT_DATE();
```
- 适用：只需要知道"改之前是什么"
- 局限：只能存一个历史值

### Hybrid (Type 1 + Type 2)
- 大部分属性 Type 1（直接覆盖，如手机号）
- 少数关键属性 Type 2（保留历史，如信用等级）

## 维度设计模式

### 日期维度 (Date Dimension)
**必须有**。包含丰富的日期属性：
- 日期键 (YYYYMMDD 格式的整数)
- 年/季/月/周/日
- 是否周末/节假日
- 财年/财季

### 退化维度 (Degenerate Dimension)
存在事实表中的维度键，没有对应的维度表。
- 例如：`order_number`, `invoice_number`
- 在事实表中作为维度属性列即可

### 杂项维度 (Junk Dimension)
将多个低基数标志/状态组合成一个维度。
- 例如：`payment_method` + `shipping_type` + `order_source` → `dim_order_attributes`

### 角色扮演维度 (Role-playing Dimension)
同一个物理维度表扮演多个逻辑角色。
- 例如：`dim_date` 可作为 `order_date`, `ship_date`, `delivery_date`

## Data Vault 2.0 简介

### 适用场景
- 多源系统集成（10+ 源系统）
- 频繁并购/组织变动
- 需要完整审计追踪

### 三层结构
- **Hub**: 业务键（如客户号），只存键不存属性
- **Link**: Hub 之间的关系（如客户-订单关系）
- **Satellite**: 描述性属性 + 时间戳

### 实践建议
- Data Vault 用于 Raw Vault 层（原始集成层）
- 上层构建 Star Schema 数据集市供业务消费
- 需要代码生成工具辅助（手工维护成本高）

## 检查清单

- [ ] 是否定义了原子级别的粒度？
- [ ] 是否有日期维度表？
- [ ] 是否使用代理键而非自然键？
- [ ] 事实表是否只有外键和度量值？
- [ ] 维度表是否包含描述性属性？
- [ ] 是否明确了 SCD 策略？
- [ ] 是否考虑了退化维度和杂项维度？
- [ ] 是否设计了 ETL 审计列（created_at, batch_id）？
