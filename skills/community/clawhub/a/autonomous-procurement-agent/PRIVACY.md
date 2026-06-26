# Privacy Policy — Autonomous Procurement Agent

**Last updated: 2026-04-06**

## 数据收集

Procurement Agent 在**用户本地设备**执行。报价单内容仅用于解析提取，**不存储原始报价单**，不发送任何内容到我们的服务器。

### 本地处理的数据

| 数据类型 | 存储位置 | 保留时间 | 用户控制 |
|---------|---------|---------|---------|
| 历史价格基准 | `~/.procurement-data/.historical-prices.json` | 直到手动更新 | 用户自行管理 |
| Webhook 事件日志 | `~/.procurement-data/vault-events.jsonl` | 最多 30 天 | 删除即清除 |
| API 密钥 | `~/.procurement-data/.env` | 直到用户删除 | 用户自行管理 |

### 第三方调用

| 服务 | 调用方 | 数据处理 | 隐私政策 |
|------|--------|---------|---------|
| OpenAI GPT-4o（可选）| 用户本地 | 由 OpenAI 处理 | [openai.com/privacy](https://openai.com/privacy) |
| Lemon Squeezy（支付）| Lemon Squeezy | MoR — LS 处理税务 | [lemonsqueezy.com/privacy](https://lemonsqueezy.com/privacy) |

**报价单数据从不发送到 OpenAI 以外的任何地方。**

---

## F1 / F2 / F3 欺诈检测数据

- 计算错误（unit_price × quantity）和价格突涨比对数据**仅在本地计算**
- 无任何欺诈数据上传或共享
- 历史价格基准由用户自行管理（可从 ERP 导入）

---

## GDPR / CCPA / 个保法

- **GDPR：** ✅ 符合
- **CCPA：** ✅ 符合
- **个保法：** ✅ 符合 — 数据本地化

---

## 数据删除

```bash
rm -rf ~/.procurement-data/
```

---

## 联系我们

support@openclaw.ai
