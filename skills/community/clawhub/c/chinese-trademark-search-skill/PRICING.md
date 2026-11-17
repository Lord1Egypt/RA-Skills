# Pricing / 定价说明

**Effective Date:** 2026-03-28
**Last Updated:** 2026-07-14

---

## English

### Points System

The platform uses an abstract **points-based** billing system. Points are consumption units that are deducted when API operations are performed. Points are not a currency and have no inherent monetary value.

### Pricing Table

| Operation | Points Cost |
|---|---|
| Search (per query) | 1 point (returns the first 50 results) |
| Detail (per trademark) | 2 points (two upstream calls required) |
| Export: 1 - 10 records | 1 point |
| Export: 11 - 50 records | 3 points |
| Export: 51 - 100 records | 5 points |
| Export: 101+ records | 10 points |

**Notes:**
- Pagination is **not currently supported**: each search returns only the first page (up to 50 results); requesting a page greater than 1 returns a `PAGINATION_NOT_SUPPORTED` error and no points are charged.
- Viewing a trademark whose detail was already purchased is **not charged again**.
- Failed operations are automatically refunded: failed searches (upstream errors), failed detail lookups (upstream errors), and failed export job creation.
- The platform reserves the right to adjust pricing with 30 days' prior notice.

### Currency Conversion Reference

Points are purchased at **1 CNY = 5 points** (1 point = 0.20 CNY, approx. 0.03 USD / 0.026 EUR). The USD/EUR figures below are approximate reference values only; actual pricing may vary based on payment method, region, and exchange rates at the time of purchase.

| Points | CNY | Approx. USD | Approx. EUR |
|---|---|---|---|
| 1 point | 0.20 CNY | ~0.03 USD | ~0.026 EUR |
| 10 points | 2.00 CNY | ~0.30 USD | ~0.26 EUR |
| 50 points | 10.00 CNY | ~1.50 USD | ~1.30 EUR |
| 100 points | 20.00 CNY | ~3.00 USD | ~2.60 EUR |

### Recharge Tiers (Bonus Points)

Larger recharges receive bonus points. Recharge at **https://tm.zhengquai.com/billing**:

| Recharge Amount | Bonus |
|---|---|
| 50 CNY | — |
| 100 CNY | +5% |
| 300 CNY | +10% |
| 500 CNY | +15% |
| 1000 CNY | +20% |
| 2000 CNY | +25% |

### Trial Points

- New organizations receive **10 trial points** upon registration.
- Trial points **expire 30 days** from the date of issuance.
- Actual issuance is subject to the platform's real-time response.
- Expired trial points cannot be reinstated.

### Refund Policy

- **Paid points are non-refundable** once credited to the account, except where required by applicable consumer protection law.
- If applicable law in your jurisdiction requires a refund mechanism (e.g., EU consumer right of withdrawal within 14 days for unused points), the platform will comply with such requirements.
- To inquire about refunds under applicable law, contact: **lengqifeng11@gmail.com**

### Payment Methods

Payment methods and options vary by region. Please refer to the platform interface for currently accepted payment methods in your region.

---

## 中文

### 点数系统

本平台采用抽象的**点数计费**系统。点数是执行 API 操作时扣减的消费单位。点数不是货币，不具有固有的货币价值。

### 定价表

| 操作 | 点数消耗 |
|---|---|
| 查询（每次） | 1 点（返回前 50 条结果） |
| 详情（每条商标） | 2 点（因需调用上游两次） |
| 导出：1 - 10 条记录 | 1 点 |
| 导出：11 - 50 条记录 | 3 点 |
| 导出：51 - 100 条记录 | 5 点 |
| 导出：101 条及以上 | 10 点 |

**说明：**
- **翻页暂不支持**：每次查询固定返回第一页前 50 条；请求页码大于 1 会返回 `PAGINATION_NOT_SUPPORTED` 错误且不扣点。
- 同一商标已购详情后再次查看**不重复扣点**。
- 失败自动退点：查询失败（上游异常）、详情上游失败、导出任务创建失败均自动退点。
- 平台保留在提前 30 天通知后调整定价的权利。

### 货币换算参考

点数按 **¥1 = 5 点**充值（1 点 = ¥0.20，约合 $0.03 / €0.026）。以下美元/欧元为近似参考值，实际定价可能因支付方式、区域和购买时的汇率而异。

| 点数 | 人民币（CNY） | 约美元（USD） | 约欧元（EUR） |
|---|---|---|---|
| 1 点 | ¥0.20 | ~$0.03 | ~€0.026 |
| 10 点 | ¥2.00 | ~$0.30 | ~€0.26 |
| 50 点 | ¥10.00 | ~$1.50 | ~€1.30 |
| 100 点 | ¥20.00 | ~$3.00 | ~€2.60 |

### 充值档位（充多得多）

充值金额越大，赠送比例越高。充值入口：**https://tm.zhengquai.com/billing**

| 充值金额 | 赠送 |
|---|---|
| ¥50 | — |
| ¥100 | +5% |
| ¥300 | +10% |
| ¥500 | +15% |
| ¥1000 | +20% |
| ¥2000 | +25% |

### 体验点

- 新注册组织赠送 **100 点体验点**。
- 体验点自发放之日起 **90 天内过期**。
- 实际发放以平台实际返回为准。
- 过期的体验点无法恢复。

### 退款政策

- **已付费点数一经充值到账即不可退款**，除非适用的消费者保护法律另有要求。
- 如果您所在司法管辖区的适用法律要求退款机制（如欧盟消费者对未使用点数在 14 天内的撤回权），平台将遵守相关要求。
- 如需咨询依据适用法律的退款事宜，请联系：**lengqifeng11@gmail.com**

### 支付方式

支付方式和选项因区域而异。请参阅平台界面了解您所在区域当前接受的支付方式。
