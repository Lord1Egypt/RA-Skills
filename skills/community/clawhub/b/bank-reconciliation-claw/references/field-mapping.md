# 字段映射表

## 银行流水格式

### 招商银行（CMB）

| 标准字段 | 招商银行列名 |
|---------|------------|
| date | 交易日期 / 记账日期 |
| amount | 交易金额 / 发生额 |
| transaction_id | 流水号 / 交易流水号 |
| counterpart | 对方账户名称 |
| remark | 摘要 / 用途 |
| balance | 账户余额 |

### 工商银行（ICBC）

| 标准字段 | 工商银行列名 |
|---------|------------|
| date | 交易日期 |
| amount | 发生额（借方为负，贷方为正） |
| transaction_id | 交易流水号 |
| counterpart | 对方户名 |
| remark | 附言 |

### 支付宝

| 标准字段 | 支付宝列名 |
|---------|----------|
| date | 交易创建时间 |
| amount | 金额（元） |
| transaction_id | 交易号 |
| counterpart | 交易对方 |
| remark | 商品说明 |
| status | 交易状态 |

### 微信支付

| 标准字段 | 微信支付列名 |
|---------|------------|
| date | 交易时间 |
| amount | 金额(元) |
| transaction_id | 交易单号 |
| counterpart | 交易对方 |
| remark | 商品 |
| status | 当前状态 |

## 系统订单格式

### 金蝶 ERP

| 标准字段 | 金蝶列名 |
|---------|---------|
| date | 单据日期 |
| amount | 价税合计 |
| order_id | 单据编号 |
| customer | 客户名称 |
| status | 审核状态 |

### 用友 ERP

| 标准字段 | 用友列名 |
|---------|---------|
| date | 业务日期 |
| amount | 含税金额 |
| order_id | 订单号 |
| customer | 往来单位 |

### SAP

| 标准字段 | SAP 列名 |
|---------|---------|
| date | Posting Date / 过账日期 |
| amount | Amount / 金额 |
| order_id | Document Number / 凭证号 |
| customer | Name / 名称 |

## 发票台账格式

### 增值税发票标准格式

| 标准字段 | 列名 |
|---------|------|
| date | 开票日期 |
| amount | 价税合计 / 含税金额 |
| invoice_id | 发票号码 |
| customer | 购方名称 |
| tax_amount | 税额 |
| pre_tax_amount | 不含税金额 |
| status | 发票状态（正常/作废/红冲） |

## 自动识别逻辑

脚本按以下优先级识别列名：
1. 精确匹配（区分大小写）
2. 不区分大小写匹配
3. 去除空格后匹配
4. 模糊匹配（编辑距离 ≤ 2）

若自动识别失败，脚本会列出所有列名并提示用户手动指定映射。
