# link-convert 输出模板

拿到 JSON 后**直接按模板填充输出**。

## 输出模板

```
### 🌍 {storeName}

| 项目 | 详情 |
|------|------|
| 商品 | {productName} |
| 返利 | **{commission}** |
| 商家 | {storeName} · {country} |

👉 返利链接：{shortUrl}

> 原始链接：{originalUrl}
```

- `productName` 不存在时省略商品行
- `country` 不存在时只显示 `{storeName}`
- `logoUrl` 如果存在可加在标题下方：`![{storeName}]({logoUrl})`

## 完整示例

<example>
用户：帮我转一下 https://www.adidas.com/us/ultraboost-5-shoes/ID8841.html

助手：

正在生成返利链接...

[调用 node {baseDir}/scripts/run.mjs convert "https://www.adidas.com/us/ultraboost-5-shoes/ID8841.html"]

### 🌍 Adidas

| 项目 | 详情 |
|------|------|
| 商品 | Ultraboost 5 Shoes |
| 返利 | **最高6%** |
| 商家 | Adidas |

👉 返利链接：https://s.duomai.com/xxx

> 原始链接：https://www.adidas.com/us/ultraboost-5-shoes/ID8841.html
</example>

<example>
用户：https://www.spacenk.com/nl/en_NL/skincare/xxx

助手：

正在生成返利链接...

[调用 node {baseDir}/scripts/run.mjs convert "https://www.spacenk.com/nl/en_NL/skincare/xxx"]

### 🌍 Space NK NL

| 项目 | 详情 |
|------|------|
| 返利 | **最高8%** |
| 商家 | Space NK NL · 荷兰 |

👉 返利链接：https://s.duomai.com/xxx

> 原始链接：https://www.spacenk.com/nl/en_NL/skincare/xxx
</example>

<example>
用户：帮我转一下 https://www.amazon.com/dp/B0xxxxx

助手：

该商家暂未开通返利，目前仅支持 Adidas、Space NK NL、designwebstore DE 三家。
</example>
