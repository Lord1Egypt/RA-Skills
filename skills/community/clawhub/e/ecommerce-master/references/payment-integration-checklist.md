# 支付集成检查清单（Payment Integration Checklist）

> 配套 [skills/payment-integration](../skills/payment-integration/SKILL.md)。把「Stripe 全生命周期」拆成可勾选的上线前清单，
> 并给出可直接执行的命令与最小可运行代码。子技能正文讲能力，本篇讲「别漏哪一步」。

## 1. 决策树：我该用哪种接入方式？

```
业务模式？
 ├─ 一次性买断（实物/虚拟） → Stripe Checkout（托管页，最快上线）
 ├─ 订阅 / 会员 / SaaS      → Checkout + Customer + Subscription
 ├─ 需要完全自定义 UI        → Stripe Elements（必须，PCI 合规要求）
 └─ 平台 /  marketplace      → Connect（分账、KYC）
        │
        └─ 要不要自助改套餐/退订？
            ├─ 是 → 启用 Customer Portal（减少工单）
            └─ 否 → 仅后台管理
```

**铁律**：任何收集卡号的页面必须用 Elements 或 Checkout，**绝不允许自建表单直传卡号**
（PCI DSS SAQ A 之外即违规）。

## 2. 选型矩阵：订阅 vs 一次性 vs 混合

| 模式 | 对象 | 周期 | 关键 API | 催款 |
|------|------|------|----------|------|
| 一次性 | PaymentIntent | 单笔 | `/v1/payment_intents` | 无 |
| 固定订阅 | Price(interval) + Subscription | 月/年 | `/v1/subscriptions` | dunning 自动 |
| 用量计费 | Meter + SubscriptionItem | 实时 | `/v1/billing_meters` | dunning 自动 |
| 混合 | 一次性 SetupIntent + 订阅 | — | `/v1/setup_intents` | dunning 自动 |

## 3. 可运行命令 / 代码

### 3.1 最小 Checkout（一次性）
```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=payment" \
  -d "success_url=https://shop.example.com/ok" \
  -d "cancel_url=https://shop.example.com/cancel" \
  -d "line_items[0][price]=price_XXXX" \
  -d "line_items[0][quantity]=1"
```

### 3.2 创建订阅（Python，标准库 + requests 不行 → 用官方 SDK 或 curl）
```python
import subprocess, os, json
def stripe(method, path, data=None):
    cmd = ["curl", "-s", f"https://api.stripe.com{path}",
           "-u", f"{os.environ['STRIPE_SECRET_KEY']}:"]
    if data:
        for k, v in data.items():
            cmd += ["-d", f"{k}={v}"]
    return json.loads(subprocess.check_output(cmd))

# 先建 customer，再建订阅
cust = stripe("POST", "/v1/customers", {"email": "buyer@example.com"})
stripe("POST", "/v1/subscriptions",
       {"customer": cust["id"], "items[0][price]": "price_monthly_XXXX"})
```

### 3.3 Webhook 签名校验（不可省略）
```python
import hmac, hashlib
def verify(raw_body: bytes, sig: str, secret: str) -> bool:
    parts = dict(p.split("=",1) for p in sig.split(","))
    ts, payload = parts["t"], parts["v1"]
    signed = hmac.new(secret.encode(), f"{ts}.".encode()+raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signed, payload)
# 关闭「跳过校验」的测试开关再上线；否则任意人可伪造事件
```

### 3.4 用脚本核对费率与对账（确定性）
复用 [scripts/validate_product_feed.py](../scripts/validate_product_feed.py) 的同款「只读 + 标准库」思路，
对账可写 `reconcile_payouts.py`：读 Stripe 导出的 `payouts.csv` 与 `balance_transactions.csv`，
按 `available_on` 汇总，确认每笔 payout 的净额 = 收入 − 手续费 − 退款。

## 4. 争议与退款处理（不可省略）

```bash
# 收到 charge.dispute.created 后，72 小时内提交证据
curl https://api.stripe.com/v1/charges/$CHARGE_ID/dispute/evidence \
  -u "$STRIPE_SECRET_KEY:" \
  -d "shipping_documentation=file_XXXX" \
  -d "customer_email=order-confirmation@example.com" \
  -d "receipt=file_YYYY"
# 退款（含税费/运费，按当地法规）
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_intent=$PI_ID" -d "amount=3293"
```

**要点**：dispute 输掉 = 全额损失 + $15 手续费；必须配置告警，证据自动化上传。
订阅类争议常见「我不记得订阅了」→ 在 Portal 留存明确的同意记录与时间戳。

## 5. 收入指标口径（确定性计算）

| 指标 | 公式 | 陷阱 |
|------|------|------|
| MRR | Σ(活跃订阅月费) | 含试用 ≠ 含已暂停 |
| ARR | MRR × 12 | 别用年化一次性收入凑 |
| 流失率 | 期初活跃 − 期末活跃 / 期初 | 按金额算 vs 按人数算结果不同，固定一种 |
| LTV | ARPU / 流失率 | 流失率趋近 0 时失真，设上限 |
| 净收入留存 | (期初客户本期收入)/期初 | 含扩张收入，>100% 即增长 |

## 6. 典型坑与规避

1. **Webhook 不验签**：测试时图省事关了校验，上线忘了开 → 攻击者伪造
   `invoice.paid` 直接发货。CI 加一条断言强制 `webhook secret` 非空。
2. **订阅创建重复**：前端重试导致同一用户两个 Subscription → 创建前先查
   `GET /v1/subscriptions?customer=...&status=active`，已存在则走升级。
3. **Currency 错配**：Price 是 `usd`，Checkout 用 `eur` → 直接 400。
   让 Price 的 currency 决定结账币种，不要硬写。
4. **Dunning 缺失**：支付失败不催款，默默流失 → 开启
   `subscription.settings.payment_method.configuration` 的 smart retries（默认 4 次/间隔递增）。
5. **税务未接**：欧盟订单没代收 VAT → 见 [references/cross-border-compliance.md](cross-border-compliance.md)。
6. **退款不退还税费/运费**：部分平台只退商品价 → 按当地法规退「含税含运」或明确告知。
7. **Test 卡上生产**：用 `4242...` 测试卡却指向 live key → 永远用
   `STRIPE_SECRET_KEY` 环境变量区分模式，配置错误就启动失败。
8. **Dispute 超时才响应**：争议 72 小时窗口，无告警 → 自动败诉。
   事件 `charge.dispute.created` 必须触发工单 + 证据模板。
9. **Proration 未设**：升级套餐默认「立即按比例」还是「下期生效」没想清 →
   两者对收入确认影响大，需在价格设计阶段定死并写入文档。
10. **对账只核对总额**：不逐笔对 payout 与 balance transaction →
    手续费/退款/调账混在一起时，总额平但结构错，税务申报出错。

## 测试场景矩阵（上线前必跑）

| 场景 | 测试卡 / 方式 | 预期 |
|------|---------------|------|
| 正常支付 | `4242 4242 4242 4242` | succeeded |
| 被拒（余额不足） | `4000 0000 0000 9995` | failed |
| 需 3DS 验证 | `4000 0025 0000 3155` | requires_action |
| 订阅首扣 | 上述卡 + 创建订阅 | invoice.paid |
| 支付失败重试 | 绑定拒付卡 | dunning 触发重试 |
| 退款 | 对任意 PI 调 refunds | refunded，对账平 |

> 所有测试在 test 模式跑；用 `STRIPE_SECRET_KEY` 区分，绝不把 live key 放进测试脚本。

## 7. 上线前检查清单

- [ ] 已区分 test / live key（环境变量注入，无硬编码）
- [ ] 结账走 Checkout 或 Elements（无自建卡号表单）
- [ ] Webhook 端点已验签 + 幂等处理（同事件只处理一次）
- [ ] 已配置必要事件：`checkout.session.completed` / `invoice.paid` /
      `invoice.payment_failed` / `charge.refunded` / `charge.dispute.created`
- [ ] 订阅升级/降级/取消路径已测（含按比例计费 proration）
- [ ] Customer Portal 已启用（自助改套餐/退订）
- [ ] Dunning / 催款序列已开启并验证失败→重试→取消流
- [ ] 税务（Stripe Tax 或手动）已对接目标市场
- [ ] 对账脚本能跑通：payout 净额 = 收入 − 费 − 退款
- [ ] Radar 风控规则已设基础阈值（高风险国家/高额单）
- [ ] 退款/争议（dispute）处理 SLA 已定义并通知客服

## 8. 与路由的衔接

- 税务细节 → [references/cross-border-compliance.md](cross-border-compliance.md)
- 结账前端体验 → [references/storefront-launch-playbook.md](storefront-launch-playbook.md)（结账流程组件）
- 完整能力 → [skills/payment-integration](../skills/payment-integration/SKILL.md)
