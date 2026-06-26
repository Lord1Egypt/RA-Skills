# 宝宝每日数据字段参考

## JSON 结构

```json
{
  "date": "2026-03-09",
  "temperature": {
    "morning": 36.9,
    "afternoon": 36.8
  },
  "jaundice": {
    "morning": { "forehead": 3.2, "face": 4.2, "chest": 2.0 },
    "evening": { "forehead": 2.9, "face": 4.1, "chest": 3.4 }
  },
  "bath": "游泳",
  "weight": 3.20,
  "sleep": {
    "quality": "佳",
    "hours": 14.5
  },
  "feeding": {
    "formula": { "ml": 560, "times": 7 },
    "breastMilk": { "ml": 0, "times": 0 }
  },
  "diaper": {
    "poop": 2,
    "pee": 10
  },
  "symptoms": ["黄疸观察"],
  "note": "D3"
}
```

## 字段说明

| 字段路径 | 类型 | 单位 | 说明 |
|---------|------|------|------|
| date | string | YYYY-MM-DD | 日期 |
| temperature.morning | number | °C | 上午体温，正常 36.0-37.5 |
| temperature.afternoon | number | °C | 下午体温 |
| jaundice.morning.forehead | number | mg/dL | 黄疸早-额头 |
| jaundice.morning.face | number | mg/dL | 黄疸早-脸 |
| jaundice.morning.chest | number | mg/dL | 黄疸早-胸 |
| jaundice.evening.forehead | number | mg/dL | 黄疸晚-额头 |
| jaundice.evening.face | number | mg/dL | 黄疸晚-脸 |
| jaundice.evening.chest | number | mg/dL | 黄疸晚-胸 |
| bath | string | - | 沐浴方式：游泳 / 洗澡 / null |
| weight | number | kg | 当日体重 |
| sleep.quality | string | - | 睡眠质量：佳 / 一般 / null |
| sleep.hours | number | 小时 | 睡眠时长 |
| feeding.formula.ml | number | ml | 奶粉总量 |
| feeding.formula.times | number | 次 | 奶粉次数 |
| feeding.breastMilk.ml | number | ml | 母乳总量 |
| feeding.breastMilk.times | number | 次 | 母乳次数 |
| diaper.poop | number | 次 | 大便次数 |
| diaper.pee | number | 次 | 小便次数 |
| symptoms | string[] | - | 症状标记列表 |
| note | string | - | 其他备注 |

## 纸质表单字段映射

纸质「宝宝每日基本情况汇总」表单对应关系：

| 纸质表单 | JSON 路径 |
|---------|-----------|
| 体温：上午 ___°C | temperature.morning |
| 体温：下午 ___°C | temperature.afternoon |
| 黄疸早：额头 ___ 脸 ___ 胸 ___ | jaundice.morning.* |
| 黄疸晚：额头 ___ 脸 ___ 胸 ___ | jaundice.evening.* |
| 沐浴：□游泳 □洗澡 | bath |
| 体重：___ kg | weight |
| 睡眠情况：□佳 □一般 | sleep.quality |
| 喂养量：奶粉 ___ml 母乳 ___ml | feeding.formula.ml / feeding.breastMilk.ml |
| 喂养次数：奶粉 ___次 母乳 ___次 | feeding.formula.times / feeding.breastMilk.times |
| 大便次数：___次 | diaper.poop |
| 小便次数：___次 | diaper.pee |
| 其他 | note |

## 症状标记选项

吐奶、胀气、红屁股、鼻塞、黄疸观察、发热、湿疹、腹泻
