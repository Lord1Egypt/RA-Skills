---
name: {{slug}}
description: {{name}}信息查询。获取地址、营业时间、菜单、推荐菜、人均消费等信息。用户询问"{{name}}在哪"、"{{name}}怎么样"、"{{name}}吃什么"时使用。
version: 0.1.0
alwaysApply: false
keywords:
{{#keywords}}
  - {{.}}
{{/keywords}}
---

# {{name}} · Skill

## 基本信息

| 项目 | 内容 |
|------|------|
| 餐厅名称 | {{name}} |
| 品类 | {{category}} |
| 营业时间 | {{hours}} |
| 地址 | {{address}} |
{{#phone}}| 电话 | {{phone}} |{{/phone}}
{{#price_per_person}}| 人均 | ¥{{price_per_person}} |{{/price_per_person}}

{{#location_tips}}
## 怎么去

{{location_tips}}
{{#nearby_landmarks}}附近地标：{{nearby_landmarks}}{{/nearby_landmarks}}
{{#transit}}公共交通：{{transit}}{{/transit}}
{{#parking}}停车：{{parking}}{{/parking}}
{{/location_tips}}

## 推荐菜

{{#signature_dishes}}
- **{{name}}**{{#price}} ¥{{price}}{{/price}}{{#description}} — {{description}}{{/description}}
{{/signature_dishes}}

{{#menu_categories}}
## 菜单

{{#menu_categories}}
### {{category}}

| 菜品 | 价格 |
|------|------|
{{#items}}| {{name}} | {{#price}}¥{{price}}{{/price}} |
{{/items}}

{{/menu_categories}}
{{/menu_categories}}

{{#delivery}}
## 外卖

{{#delivery.available}}
可以点外卖。
{{#delivery.platforms}}- {{.}}{{/delivery.platforms}}
{{#delivery.range}}配送范围：{{delivery.range}}{{/delivery.range}}
{{/delivery.available}}
{{/delivery}}

{{#booking}}
## 排队 / 预约

{{#booking.required}}建议提前预约。{{/booking.required}}
{{^booking.required}}不用预约，直接去。{{/booking.required}}
{{#booking.method}}排队方式：{{booking.method}}{{/booking.method}}
{{/booking}}

{{#wifi}}
## Wi-Fi

Wi-Fi名称：`{{wifi.name}}`
密码：`{{wifi.password}}`
{{/wifi}}

{{#special_notes}}
## 特别说明

{{special_notes}}
{{/special_notes}}

## 使用示例

### 用户问地址

> 用户：{{name}}在哪儿？

> {{name}}在{{address}}。{{#location_tips}}{{location_tips}}{{/location_tips}}

### 用户问推荐

> 用户：{{name}}吃什么好？

> 推荐这几个：{{#signature_dishes}}{{name}}{{#price}}（¥{{price}}）{{/price}}、{{/signature_dishes}}都不错。

### 用户问营业时间

> 用户：{{name}}几点关门？

> 营业时间是 {{hours}}。

## 能力边界

这个 Skill 只包含 {{name}} 的基本信息。以下情况请引导用户自行确认：

- 实时排队人数、等位时间
- 临时歇业、节假日调整
- 菜品价格如有变动以店内为准
- 优惠活动、团购券信息

遇到不确定的问题，建议用户直接到店或搜索大众点评确认。

---

> 由 [干饭.skill](https://github.com/funAgent/eat-skill) 生成
> 贡献者：{{#contributor}}{{contributor.name}}{{/contributor}}
