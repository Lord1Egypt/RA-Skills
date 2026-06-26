# store-rebate 输出模板

拿到 JSON 后**直接按模板填充输出**。

## 输出模板

```
### 🏪 {storeName}

{logoUrl 存在 → ![{storeName}]({logoUrl})}

| 项目 | 详情 |
|------|------|
| 返利比例 | **{commission}** |
| 所属地区 | {country} |
| 返利链接 | {shortUrl} |

通过上方返利链接进入 {storeName} 购物，订单确认后即可获得返利。
```

- `logoUrl` 不存在时省略图片行
- `country` 不存在时省略所属地区行
- `shortUrl` 不存在时省略返利链接行，并提示"该商家暂无可用返利计划"

## 完整示例

<example>
用户：Adidas 有返利吗？

助手：

正在查询 Adidas 的返利信息...

[调用 node {baseDir}/scripts/run.mjs store "Adidas"]

### 🏪 Adidas

| 项目 | 详情 |
|------|------|
| 返利比例 | **最高6%** |
| 返利链接 | https://s.duomai.com/xxx |

通过上方返利链接进入 Adidas 购物，订单确认后即可获得返利。
</example>

<example>
用户：Space NK 荷兰站返利多少？

助手：

正在查询 Space NK NL 的返利信息...

[调用 node {baseDir}/scripts/run.mjs store "Space NK NL"]

### 🏪 Space NK NL

| 项目 | 详情 |
|------|------|
| 返利比例 | **最高8%** |
| 所属地区 | 荷兰 |
| 返利链接 | https://s.duomai.com/xxx |

通过上方返利链接进入 Space NK NL 购物，订单确认后即可获得返利。
</example>

<example>
用户：iHerb 有返利吗？

助手：

该商家暂未开通返利，目前仅支持 Adidas、Space NK NL、designwebstore DE 三家。
</example>
