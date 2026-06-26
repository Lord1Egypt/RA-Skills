# 毛利计算 V4 (多平台版)

## 公式（6项扣除 — AMZScout费用已合并FBA+佣金）

```
毛利 = 售价 - ①采购成本 - ②头程运费 - ③关税 - ④AMZScout总费(FBA+佣金) - ⑤退货 - ⑥广告
毛利率 = 毛利 / 售价 × 100%
```

## 各项计算

| # | 项目 | 公式 | 数据来源 |
|---|------|------|----------|
| ① | 采购成本(USD) | 1688价(¥) ÷ 实时汇率 | 1688以图搜图 |
| ② | 头程运费(USD) | 重量(kg) × 15(¥/kg) ÷ 实时汇率 | Amazon官方重量 |
| ③ | 关税(USD) | 采购成本 × 关税率% | 品类查表 |
| ④ | AMZScout总费(USD) | AMZScout Fees 字段 | AMZScout直接抓取 |
| ⑤ | 退货损耗(USD) | 售价 × 5% | 固定 |
| ⑥ | 广告费(USD) | 售价 × 20% | 固定(TACOS) |

**关键**：AMZScout 的 Fees = FBA履约费 + 15% Referral 佣金 合计值。
计算时直接使用此合计值，**不再单独扣除15%佣金**，否则会重复扣除。

拆分显示（仅供报告展示用）：
- Referral佣金 = 售价 × 15%
- FBA纯履约费 = AMZScout Fees - Referral佣金

## 重量取值优先级

1. Amazon官方产品页 "Item Weight" 或 "Shipping Weight"
2. 卖家精灵 weight 字段
3. AMZScout weight 字段
4. 无数据时 fallback: 运费=$2

## 关税率速查

| 品类关键词 | 税率 |
|-----------|------|
| 汽车/车载/automotive | 5% |
| 灯/lighting/LED | 5% |
| 电子/电器/camera/dash cam | 5% |
| 工具/tools/jack/inflator | 5% |
| 座椅套/地毯/纺织 | 8% |
| 改装件/suspension/exhaust | 8% |
| 鞋/衣/服装 | 10% |

## 汇率

```
每次执行必须 web_search("USD CNY exchange rate today") 获取实时汇率
不使用固定值（旧版固定7.3已废弃）
```

## 筛选标准

- ≥35%：🟢 优秀（绿色）
- ≥20%：🟡 合格（黄色）
- <20%：🔴 淘汰（红色，不进入报告）
