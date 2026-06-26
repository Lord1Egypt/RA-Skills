# 支付安全规范

## 权限分级矩阵

| 金额范围 | 审批级别 | 说明 |
|---------|---------|------|
| ≤ 5,000 元 | 自动执行 | 无需人工审批 |
| 5,001 ~ 50,000 元 | 采购主管审批 | 系统发起飞书审批流 |
| 50,001 ~ 200,000 元 | 财务总监审批 | 系统发起飞书审批流 |
| > 200,000 元 | CEO 审批 | 系统发起飞书审批流 + 邮件通知 |

自动执行阈值可在规则配置中覆盖（`budget_limit.per_order`）。

## 加密传输标准

- 所有 API 通信使用 TLS 1.3
- 支付信息字段（账号、金额）使用 AES-256-GCM 加密存储
- API 密钥存储在环境变量或密钥管理服务（不得硬编码）
- 日志中屏蔽敏感字段（账号后4位保留，其余用 `****` 替代）

```python
def mask_sensitive(value: str, keep_last: int = 4) -> str:
    if len(value) <= keep_last:
        return "****"
    return "*" * (len(value) - keep_last) + value[-keep_last:]
```

## 审计日志格式

每笔交易必须记录完整审计日志：

```json
{
  "audit_id": "AUD-20240101-001",
  "timestamp": "2024-01-01T10:05:23+08:00",
  "rule_id": "RULE-001",
  "trigger_reason": "inventory(80) < safety_stock(100)",
  "order_id": "PO-20240101-001",
  "supplier_id": "SUP-A",
  "items": [{"sku": "SKU-001", "quantity": 500, "unit_price": 12.50}],
  "total_amount": 6250.00,
  "payment_method": "bank_transfer",
  "payment_status": "success",
  "payment_ref": "PAY-REF-123456",
  "operator": "auto-purchase-executor",
  "ip_address": "10.0.0.1"
}
```

## 合规要求

### 财务制度
- 每笔采购必须有对应的采购申请单（系统自动生成）
- 付款凭证（银行回单/支付截图）自动归档到飞书云文档
- 月末自动生成采购汇总报表，推送财务部门

### 税务规范
- 采购金额含税时，自动拆分税额（增值税 13% / 9% / 6%）
- 发票信息在订单中注明，提醒供应商开具对应发票
- 发票到账后在系统中标记，未到账超 30 天自动催票

### 反洗钱规定
- 单日向同一供应商付款超过 50 万元，触发人工复核
- 新供应商首笔付款必须人工审批（无论金额）
- 供应商账户变更后 7 天内付款需人工审批

## 支付失败处理

```
支付失败
  ├── 余额不足 → 通知财务充值，暂停规则
  ├── 账户异常 → 通知财务，暂停所有支付
  ├── 网络超时 → 5分钟后重试（最多3次）
  ├── 供应商账户错误 → 通知采购员核实，暂停该供应商
  └── 其他错误 → 记录日志，通知采购员人工处理
```

## 环境变量配置

```bash
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_NAME=purchase_db
DB_USER=purchase_user
DB_PASSWORD=<从密钥管理服务获取>

# 支付网关
PAYMENT_GATEWAY_URL=https://pay.company.com
PAYMENT_API_KEY=<从密钥管理服务获取>

# 飞书通知
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/<TOKEN>

# 供应商 API（每个供应商单独配置）
SUPPLIER_A_API_KEY=<从密钥管理服务获取>
SUPPLIER_B_CLIENT_ID=<从密钥管理服务获取>
SUPPLIER_B_CLIENT_SECRET=<从密钥管理服务获取>
```
