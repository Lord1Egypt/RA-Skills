# Cheap

Find the cheapest meaningful visible price for a product across major Chinese shopping platforms — Taobao, Tmall, JD.com, Pinduoduo, and more.

## What it does
- Searches across multiple Chinese e-commerce platforms for the same product
- Compares like-for-like listings by brand, model, specs, and bundle contents
- Distinguishes straightforward visible prices from coupon-only, member-only, or pre-sale pricing
- States matching confidence and caveats clearly when listing comparability is uncertain

## Example scenarios

**1. 小米手环 8 Pro 全网比价**
> 👤 "帮我比价小米手环 8 Pro，哪个平台最便宜？"
> 🤖 跨平台搜索淘宝、天猫、京东、拼多多等。对比同型号同规格清单。输出：最便宜平台与价格、各平台可比价格、匹配置信度、注意事项（版本匹配、优惠券、运费）、最终建议。

**2. 模糊产品名需要先澄清**
> 👤 "哪里买 iPhone 最便宜？"
> 🤖 识别产品名过于宽泛（iPhone 型号众多），先问一句澄清问题："您具体想看哪个型号？比如 iPhone 15 Pro、iPhone 15 还是 iPhone 14？不同型号价格差异很大。" 确认后再进行比价。

**3. 想买便宜机票**
> 👤 "想去成都玩几天，从深圳出发，怎么买机票最便宜？什么时候买最划算？"
> 🤖 比价策略：同时查去哪儿、携程、飞猪、航司官网（南航、深航），注意含税总价。建议提前3-4周购票，选周三/周四出发。使用各平台'低价日历'和'预约提醒'功能。给出深圳到成都近期票价区间参考，关注航司会员日（如南航每月28号）。
