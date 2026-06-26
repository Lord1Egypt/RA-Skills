# 易错字段负面规则

> 来源：SKILL.md 3.3 拆分。采集时必须遵守，防止错抓。

## 反爬页

一旦页面主体是 continue-shopping / Robot Check / Sorry 模板，除"被反爬"状态外，**不提取**标题、价格、评分、BSR、Seller 等核心字段。

## Seller / Sold by

如果抓到 `Stainless Steel`、`Metal`、`Black`、`SUS304`、尺寸、颜色、材质等，判定为错抓，必须置为"未获取/需人工复核"。

## List Price

如果与当前售价相同且没有 `List Price/Was` 标签，不记录为 List Price。

## Other Sellers

如果只抓到 `0`、`08`、ASIN 片段、日期片段等异常值，不记录。

## BSR

必须包含 `#` 和类目名，最好保留完整 `Best Sellers Rank` 多级排名。

## Review 差评率

必须有 1 星/2 星/3 星百分比来源；不得按星级均值倒推。

## 主图 URL

写入飞书时用尖括号或代码格式包裹，避免 `_AC_` 被 Markdown 当斜体处理。

## 品牌名

- 优先从卖家精灵插件提取
- `#bylineInfo` 可能返回 "Visit the [Brand] Store" 格式，需清洗
- 如果返回空字符串或材质名，判定为错抓
