# 知网固定域名、路由与归属

## 站点身份

- 用户端固定域名：https://cnki.cqccjy.cn。
- 自助入口：https://cnki.cqccjy.cn/pzw，公开渠道码为 pcnki。
- 订单号/检测卡/淘宝订单交接入口：https://cnki.cqccjy.cn/zw，页面渠道码为 cnki。
- 统一报告验真入口：https://vpcs.cqccjy.cn/pwp/verify；知网官方备用页：https://check7.cnki.net/codeverify/。
- 站点业务归属固定为 ownerEmployeeId=2；不得让用户输入 URL、渠道码或供应商来覆盖它。

## 路由表

| 路由 | 用途 | 前端渠道 | skill 行为 |
|---|---|---|---|
| / | 主站根路径，前端按自助入口处理 | pcnki | 可重定向/打开 /pzw |
| /pzw | 自助选产品、上传、生成订单、在线支付 | pcnki | 首选入口 |
| /pzw/check | 自助订单进度、报告查询/下载 | pcnki | 订单号查询、报告交接 |
| /pzw/verify | 兼容地址 | pcnki | 重定向到 /pzw/check |
| /zw | 订单号/检测卡/淘宝订单上传与查询 | cnki | 只在用户明确提供凭证时使用 |
| /zw/check | 传统订单/卡号报告入口 | cnki | 同上 |
| /zw/verify | 兼容地址 | cnki | 重定向到 /zw/check |

代码中的 routeBasePath 只识别 /pzw 和 /zw：/pzw 使用 pcnki，其他知网卡式路由使用 cnki。后端 isPcnki(channel) 的规则是“空值或非 cnki 都按公开自助渠道处理”，因此 skill 永远显式传 pcnki，不依赖默认值。

## 不要混用的地址

- 不使用不存在的 /cnki、/pcnki 作为公共入口。
- 不把供应商 API、供应商报告临时地址、后台 /admin、超管/平台人工菜单地址写给用户。
- 不把统一验真入口误写成报告下载入口；验真是第三方网页交互，不能由脚本猜验证码或代提交。
