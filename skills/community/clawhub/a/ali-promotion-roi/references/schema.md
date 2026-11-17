# Alibaba 国际站 ROI 分析 — 数据表 Schema

本 skill 通过 `sql-linker-cli` 从 MySQL 拉取两张表，**不负责数据录入**。数据录入由 `scripts/alibaba_intl/load_orders.py` 和 `load_promotion.py` 负责。

---

## 表 1: `alibaba_intl_orders`（订单明细 · 行级事实表）

一行 = 一个订单。所有业务字段都进表，方便 join / 切片。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGINT PK | 自增 |
| `order_no` | VARCHAR(32) UK | 订单编号（唯一） |
| `order_create_dt` | DATETIME | 订单创建时间（精确） |
| `data_date` | DATE | 订单创建日期（**与推广日期 join 的关键**） |
| `data_month` | VARCHAR(7) | YYYY-MM |
| `order_status` | VARCHAR(32) | 订单完成 / 订单关闭 / 退款申请处理中 / ... |
| `order_type` | VARCHAR(32) | 信保订单 |
| `order_currency` | VARCHAR(8) | 币种 (USD) |
| `order_amount` | DECIMAL(12,2) | 订单总价 |
| `shipping_fee` | DECIMAL(12,2) | 运费 |
| `discount_amount` | DECIMAL(12,2) | 折扣金额 |
| `unit_price` | DECIMAL(12,2) | 单价 |
| `quantity` | INT | 数量 |
| `initial_payment` | DECIMAL(12,2) | 预付款 |
| `balance_payment` | DECIMAL(12,2) | 尾款 |
| `tax_fee` | DECIMAL(12,2) | 税费（美国卖家适用） |
| `has_attachment` | VARCHAR(8) | 是否有合同附件（是/否） |
| `buyer_country` | VARCHAR(8) | 买家国家（ISO 二字代码） |
| `buyer_name` | VARCHAR(128) | 买家名称 |
| `buyer_email` | VARCHAR(128) | 买家邮箱 |
| `company_name` | VARCHAR(255) | 公司名称 |
| `seller_name` | VARCHAR(64) | 卖家名称 |
| `product_name` | VARCHAR(512) | 产品名称 |
| `sku_spec` | VARCHAR(512) | SKU 规格 |
| `actual_delivery_dt` | DATETIME | 实际发货时间 |
| `appointed_delivery_dt` | DATETIME | 约定发货时间 |
| `created_at` / `updated_at` | DATETIME | 自动注入 |

**索引**: `uk_order_no`, `idx_data_date`, `idx_data_month`, `idx_status_month`, `idx_buyer_country`

### 订单实付口径

ROI 计算时，"订单金额"取：
```
net_amount = order_amount + shipping_fee - discount_amount
```

---

## 表 2: `alibaba_intl_promotion_daily`（推广日度 · 标准+全站合并）

一行 = 一天 × 一种推广类型。**两种推广类型合并到一张表**，用 `promotion_type` 区分。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGINT PK | 自增 |
| `data_date` | DATE | 投放日期 |
| `data_month` | VARCHAR(7) | YYYY-MM |
| `promotion_type` | VARCHAR(32) | `standard_promotion` 标准推广 / `sitewide_promotion` 全站推广 |
| `cost` | DECIMAL(12,2) | 花费 |
| `cost_unit` | VARCHAR(8) | 花费单位（CNY） |
| `impression_cnt` | INT | 曝光量 |
| `click_cnt` | INT | 点击量 |
| `click_rate` | DECIMAL(8,4) | 点击率（**小数形式**: 0.0260 表示 2.60%） |
| `click_cost` | DECIMAL(12,2) | 点击成本（CNY） |
| `l1_click_cnt` | INT | L1+ 点击量 |
| `l1_buyer_click_rate` | DECIMAL(8,4) | L1+ 买家点击占比 |
| `biz_opportunity_cnt` | INT | 商机量（两份推广 Excel 字段统一） |
| `biz_opportunity_cost` | DECIMAL(12,2) | 商机成本（CNY） |
| `l1_biz_opportunity_cnt` | INT | L1+ 商机量 |
| `biz_conversion_rate` | DECIMAL(8,4) | 商机转化率 |
| `inquiry_cnt` | INT | 询盘量 |
| `tm_inquiry_cnt` | INT | TM 咨询量 |
| `order_cnt` | INT | **推广系统自报的当日订单数**（1日累计归因） |
| `promotion_hours` | DECIMAL(6,2) | 推广时长（仅标准推广有，全站推广=0） |

**索引**: `uk_date_type (data_date, promotion_type)`, `idx_data_month`, `idx_promotion_type`, `idx_month_type`

---

## 两个关键注意点

### 1. 币种不同

- 推广花费是 **CNY（￥）**
- 订单是 **USD（$）**
- ROI 计算时通过汇率换算（CLI 默认 `1 USD = 7.2 CNY`，可调）

### 2. 转化口径不同

- `promotion_daily.order_cnt` 是**阿里推广系统自报**（基于他们的归因模型 + 1日累计窗口）
- `orders.order_status = '订单完成'` 是**真实完成**的事实
- 两者**经常不一致**——例如推广报了 1 订单，但实际还在退款流程中

ROI 计算**优先以 `订单完成` 为准**。`order_cnt` 仅做对比参照。