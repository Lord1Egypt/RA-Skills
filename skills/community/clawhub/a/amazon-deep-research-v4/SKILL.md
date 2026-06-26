---
name: amazon-deep-research-v4
description: >
  亚马逊深度选品V4：多平台交叉验证(AMZScout+西柚找词+卖家精灵) → 1688以图搜图同款采购 → 实时汇率7项毛利计算 → WIPO IP合规审计 → HTML可视化报告。
  触发词：亚马逊调研/选品/市场调研/Amazon research/毛利分析/快速调研/产品分析/竞品分析/选品报告
---

# 亚马逊深度选品 V4 (多平台交叉验证版)

## 核心原则

1. **所有数据必须真实抓取**，严禁估算或编造
2. **多平台交叉验证**：AMZScout(费用) + 西柚找词(流量) + 卖家精灵(BSR/维度) + Amazon官方(尺寸/重量)
3. **1688以图搜图**：用Amazon主图精准匹配同款，不接受关键词模糊搜索
4. **实时汇率**：每次执行必须 web_search 获取当日 USD/CNY 汇率
5. **WIPO IP 合规**：每个产品必须完成5步IP审计，HIGH风险直接淘汰
6. **毛利7项扣除不可省略**，≥20%合格，<20%淘汰

## 流程（6步）

| # | 步骤 | 数据来源 | 输出 |
|---|------|----------|------|
| 1 | 获取实时汇率 | web_search Yahoo Finance | FX 变量 |
| 2 | 多平台数据采集 | AMZScout + 西柚找词 + 卖家精灵 | data/multi_platform.json |
| 3 | 1688以图搜图采购匹配 | air.1688.com 图片搜索 | data/1688_matches.json |
| 4 | 7项毛利计算+筛选 | Python | data/qualified.json |
| 5 | WIPO IP 合规审计 | WIPO Brand DB + Google Patents | data/ip_audit.json |
| 6 | HTML报告生成 | Python(内嵌模板) | output/amazon-research-v4.html |

## 执行指令

### 步骤1：实时汇率

```python
# 必须每次执行时获取，不使用固定值
web_search("USD CNY exchange rate today")
# 提取当日汇率，如 6.8335
FX = 提取到的实时汇率
```

### 步骤2：多平台数据采集

**2a. AMZScout（费用权威来源）**

用 browser agent 访问 AMZScout Product Database：
```
https://amzscout.net/product-database
```
- 输入ASIN搜索或按品类筛选
- 提取字段：price, fba_fee(含Referral), monthly_sales, weight, bsr, rating, reviews
- **关键**：AMZScout 的 Fees 字段 = FBA履约费 + 15% Referral 佣金合计，计算毛利时不再重复扣佣金

**2b. 西柚找词（流量权威来源）**

用 browser agent 逐ASIN查询：
```
https://www.xiyouzhaoci.com/detail/asin/look_up/US/{ASIN}
```
- 提取字段：
  - monthly_orders_30d (30天预估单量)
  - traffic_score_7d (7天流量分)
  - natural_traffic_pct (自然流量占比%)
  - ad_traffic_pct (广告流量占比%)
  - top_keywords: keyword, search_volume, natural_rank, ad_rank, cpc (前3-5个)
- **关键**：西柚的广告占比数据是广告投放策略的核心依据

**2c. 卖家精灵（BSR/维度备选）**

登录方式：
```
browser → https://www.sellersprite.com/cn/w/user/login
用户扫码登录后提取Cookie: ecookie, rank-login-user, Sprite-X-Token
```

API采集（参照 [references/sellersprite-api.md](references/sellersprite-api.md)）：
```
POST https://www.sellersprite.com/v3/api/product-research
```

Extension详情页（单ASIN）：
```
https://www.sellersprite.com/cn/extension/product-detail?market=US&asin={ASIN}
```
- 提取：fba, dimensions, dimensionsTag, weight
- **注意**：卖家精灵的FBA数据可能不如AMZScout准确，优先用AMZScout

**2d. Amazon官方（尺寸/重量地面真相）**

browser agent 访问 Amazon 产品页：
```
https://www.amazon.com/dp/{ASIN}
```
- 滚动到 "Product information" / "Technical Details"
- 提取：Product Dimensions, Item Weight, Package Weight, Date First Available
- **Amazon官方数据是尺寸/重量的最终权威**

### 交叉验证规则

| 数据项 | 第一来源 | 验证来源 | 冲突处理 |
|--------|----------|----------|----------|
| FBA+佣金费用 | AMZScout | 卖家精灵 | 取AMZScout（含Referral更完整） |
| 月销量 | AMZScout | 西柚找词 | 取两者平均值 |
| 尺寸/重量 | Amazon官方 | 卖家精灵 | 取Amazon官方 |
| 流量/广告占比 | 西柚找词 | — | 唯一来源 |
| 关键词SV/CPC | 西柚找词 | — | 唯一来源 |
| BSR | AMZScout | 卖家精灵 | 取更新时间较近者 |

### 步骤3：1688以图搜图

**必须用Amazon主图做图片搜索，不接受关键词搜索（产品不匹配）**

搜索URL：
```
https://air.1688.com/app/1688-lp/landing-page/comparison-table.html?bizType=browser&currency=CNY&customerId=dingtalk&outImageAddress={URL_ENCODED_AMAZON_IMAGE}
```

执行方式：browser agent 逐ASIN处理
1. 获取Amazon主图URL（`#landingImage` src）
2. URL编码主图地址
3. 导航到 air.1688.com 搜索URL
4. 等待5秒加载结果
5. 提取TOP匹配：产品名、价格(¥)、detail.1688.com链接、供应商名

提取JS：
```javascript
const rows = document.querySelectorAll('tr.ant-table-row');
const results = [];
rows.forEach((row, i) => {
  if (i >= 3) return;
  const tds = row.querySelectorAll('td');
  const img = row.querySelector('img')?.src || '';
  const name = tds[1]?.innerText || '';
  const price = tds[2]?.innerText || '';
  results.push({img, name, price});
});
JSON.stringify(results);
```

**约束**：
- 链接必须是 `detail.1688.com/offer/` 格式
- 不接受 alibaba.com 国际站链接
- 匹配度标注：✓(高度匹配) / ~(近似匹配) / ✗(不匹配，需人工确认)

### 步骤4：7项毛利计算

参照 [references/margin.md](references/margin.md)

```
毛利 = 售价 - ①采购成本 - ②头程运费 - ③关税 - ④AMZScout总费 - ⑤退货 - ⑥广告
```

| # | 项目 | 公式 | 来源 |
|---|------|------|------|
| ① | 采购成本 | 1688价(¥) ÷ 实时汇率 | 1688以图搜图 |
| ② | 头程运费 | 重量(kg) × ¥15/kg ÷ 实时汇率 | Amazon官方重量 |
| ③ | 关税 | 采购成本($) × 关税率(5%-10%) | 品类查表 |
| ④ | AMZScout总费 | AMZScout Fees (FBA+佣金) | AMZScout |
| ⑤ | 退货 | 售价 × 5% | 固定 |
| ⑥ | 广告 | 售价 × 20% | 固定(TACOS) |

**注意**：AMZScout Fees 已包含 FBA 履约费 + 15% Referral 佣金，不再单独扣佣金。

筛选：≥20% 合格 | <20% 淘汰
色标：≥35% 绿色优秀 | ≥20% 黄色合格 | <20% 红色淘汰

### 步骤5：WIPO IP 合规审计

**每个产品必须完成，不可跳过**（参照 [references/wipo-ip.md](references/wipo-ip.md)）

5步审计流程：
1. 商标检索 → WIPO Global Brand Database (branddb.wipo.int)
2. 外观专利 → Google Patents (D前缀, <15年)
3. 实用新型专利 → WIPO PATENTSCOPE + USPTO
4. 认证合规 → DOT/FCC/UL/CARB/FMVSS/EPA/MFi
5. 风险评级 → 🟢LOW / 🟡MEDIUM / 🔴HIGH

**HIGH 风险产品直接淘汰，不进入最终报告**

### 步骤6：HTML报告生成

参照 [references/html-template.md](references/html-template.md)

报告结构：
```
标题 + 数据来源标注(AMZScout/西柚/1688)
常量栏(实时汇率/运费/佣金/退货/广告/FBA来源)
7项毛利公式框(黑底白字)
KPI卡片(合格数/平均毛利/费用来源/流量来源)
产品明细表(含全部7项扣除拆解)
数据来源说明
```

产品表列：
#, 主图(Amazon), ASIN(链接), 产品名, AMZScout数据(月销/BSR/评分/FBA/佣金), 西柚数据(流量分/自然占比/广告占比), 核心关键词(SV/CPC), 售价, 1688采购(¥/链接), 供应商, ①成本, ②运费, ③关税, ④总费, ⑤退货, ⑥广告, 净利, 毛利率(色标), IP风险

## 核心约束

1. **数据必须多平台实采**，禁止单一来源估算
2. **FBA费用取AMZScout**，不用公式估算
3. **1688必须以图搜图**，不接受关键词搜索（产品不匹配）
4. **1688链接必须是 detail.1688.com/offer/**
5. **汇率必须实时获取**（web_search），不用固定值
6. **WIPO IP必须审计**，HIGH风险直接淘汰
7. **毛利7项扣除不可省略**
8. **过滤大品牌和高退货品类**（参照 [references/filters.md](references/filters.md)）
9. **报告中每个数字必须标注数据来源**
10. **主图必须从Amazon真实抓取，不接受占位符**
