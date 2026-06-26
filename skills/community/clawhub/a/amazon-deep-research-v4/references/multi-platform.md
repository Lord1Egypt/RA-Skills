# 多平台数据采集策略

## 平台分工

| 平台 | 权威数据 | URL | 登录要求 |
|------|----------|-----|----------|
| AMZScout | FBA+佣金费用, 月销, 重量 | amzscout.net/product-database | 免费试用/付费 |
| 西柚找词 | 流量分, 自然/广告占比, 关键词SV/CPC | xiyouzhaoci.com/detail/asin/look_up/US/{ASIN} | 免费 |
| 卖家精灵 | BSR, 维度, 补充数据 | sellersprite.com/cn/extension/product-detail?market=US&asin={ASIN} | 需登录 |
| Amazon | 尺寸, 重量, 价格 (Ground Truth) | amazon.com/dp/{ASIN} | 无 |

## AMZScout 抓取方法

browser agent 访问 AMZScout Product Database：
```
https://amzscout.net/product-database
```

搜索后提取结果表格，关键字段：
- **Fees**: FBA + Referral 总费用（最权威的费用数据）
- **Est. Monthly Sales**: 月销量预估
- **Price**: 当前售价
- **Weight**: 产品重量
- **BSR**: Best Seller Rank
- **Rating / Reviews**: 评分和评论数

## 西柚找词 抓取方法

browser agent 逐ASIN访问：
```
https://www.xiyouzhaoci.com/detail/asin/look_up/US/{ASIN}
```

等待5秒后提取（`document.body.innerText`）：
- **30天预估单量**: 月订单量
- **7天流量分**: 流量健康度评分
- **自然流量占比%**: 自然搜索流量比例
- **广告流量占比%**: 付费广告流量比例
- **关键词列表**: keyword, search_volume, natural_rank, ad_rank, cpc

## 卖家精灵 API

### 登录
```
browser → https://www.sellersprite.com/cn/w/user/login
扫码登录后提取Cookie: ecookie, rank-login-user, Sprite-X-Token
```

### 单ASIN查询
```
GET https://www.sellersprite.com/cn/extension/product-detail?market=US&asin={ASIN}
```

### 批量查询 API
```
POST https://www.sellersprite.com/v3/api/product-research
Content-Type: application/json
Cookie: ecookie=...; rank-login-user=...; Sprite-X-Token=...
Body: {"market":"US","page":1,"size":20,"minSales":300,"minPrice":50,...}
```

## 交叉验证规则

同一数据项在多平台出现时的取值优先级：

| 数据项 | 优先用 | 原因 |
|--------|--------|------|
| FBA+佣金费用 | AMZScout | 含Referral最完整 |
| 月销量 | AMZScout | 算法更稳定 |
| 尺寸/重量 | Amazon官方 | Ground Truth |
| 流量/广告占比 | 西柚找词 | 唯一来源 |
| 关键词SV/CPC | 西柚找词 | 唯一来源 |
| BSR | 取更新时间较近者 | — |

## 并发策略

- AMZScout: 1个browser agent，批量搜索
- 西柚找词: 2个browser agent 并行，每个处理5-6个ASIN
- 1688以图搜图: 3个browser agent 并行，每个处理3-5个ASIN
- Amazon官方: 1个browser agent，逐ASIN访问
