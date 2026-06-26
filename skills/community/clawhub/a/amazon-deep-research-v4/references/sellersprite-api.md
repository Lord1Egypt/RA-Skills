# 卖家精灵API (备选数据源)

## 定位

卖家精灵是V4中的**备选数据源**，优先级低于AMZScout(费用)和西柚找词(流量)。
主要用于：补充BSR数据、获取dimensionsTag(cm)、验证其他平台数据。

## 登录

```bash
browser → https://www.sellersprite.com/cn/w/user/login
# 用户扫码或输入账号密码
# 登录后提取Cookie:
document.cookie
# 需要3个: ecookie, rank-login-user, Sprite-X-Token
```

## 批量API

```
POST https://www.sellersprite.com/v3/api/product-research
Content-Type: application/json
Cookie: ecookie=...; rank-login-user=...; Sprite-X-Token=...
```

### 请求体

```json
{
  "market": "US",
  "page": 1, "size": 20,
  "symbolFlag": true, "monthName": "bsr_sales_nearly",
  "selectType": 2, "filterSub": false, "weightUnit": "g",
  "order": {"field": "total_units", "desc": true},
  "sellerTypes": ["FBA"],
  "minSales": 300,
  "minPrice": 50,
  "putawayMonth": 6,
  "lowPrice": "N", "video": ""
}
```

## 单ASIN Extension页

```
https://www.sellersprite.com/cn/extension/product-detail?market=US&asin={ASIN}
```
等待8秒后用 `document.body.innerText` 提取数据。

## 提取字段

asin, title, brand, price, totalUnits, totalAmount, bsrRank, rating, reviews,
fba, profit, availableDays, categoryName, dimensions, dimensionsTag, weight, imageUrl

## 注意

- Cookie有效期~24h，401/403需重新登录
- dimensionsTag 是cm单位，dimensions 是inches
- fba字段准确度不如AMZScout，仅作参考
