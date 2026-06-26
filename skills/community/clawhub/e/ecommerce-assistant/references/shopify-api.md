# Shopify 店铺分析方案

## Shopify Store 检测

### 检测网站是否为 Shopify
```bash
curl -s https://example.com | grep -i shopify
```

### 获取 Shopify 店铺产品数据
Shopify 店铺有公开的产品 JSON API：
```
https://store-name.myshopify.com/products.json?limit=250
https://store-name.myshopify.com/collections/all/products.json
```

## 数据字段
- 产品标题、描述、价格
- 变体信息 (SKU, 库存)
- 图片 URL
- 标签、类型

## 竞品分析维度
1. 价格区间分布
2. 产品类别占比
3. 上新频率
4. 热销产品识别
