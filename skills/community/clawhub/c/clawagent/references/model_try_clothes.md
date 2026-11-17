# 模特试穿

> 调用方式及异步轮询见 SKILL.md「调用方式」「异步任务轮询」

## 参数

```json
{
  "url": "https://cdn.example.com/clothes.jpg",       // 必填：平铺/挂拍商品图，公网URL
  "gender": "女",                                     // 必填："男" | "女"
  "category": "室内商拍",                              // 可选：室内商拍 | 女士穿搭 | 男士穿搭 | 稚趣童装 | 户外行摄
  "content": "外套",                                   // 可选：上装/裤装/外套/套装/裙子...
  "bottom_url": "https://...",                        // 可选，单张衣服图不传
  "feature": {                                        // 可选，子字段均非必填
    "age": "青年",
    "hair_style": "长发",
    "hair_color": "黑色",
    "color": "白皙",        // 肤色
    "figure": "苗条",
    "expression": "自然"
  },
  "prompt": "中远景，阳光明媚的公园"   // 可选，场景背景描述
}
```

## 关键约束

- `gender`: `"男"` / `"女"`，不是"男性""女性"
