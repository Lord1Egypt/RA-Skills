# 聚水潭 ERP 接口使用方法

这个文件给大模型在需要真实调用聚水潭数据时使用，只记录“用户场景 -> 需要的数据 -> 可用接口 -> 调用注意”。用户场景和典型请求见 `references/scenarios.md`。

## 使用原则

- 先理解用户要做的经营判断，再选择最小必要接口。
- 不为简单问题拉全量数据。
- 能用本地快照或用户上传文件回答时，不强制调用线上接口。
- 缺少授权资料、接口权限或关键字段时，直接说明缺口。
- 输出时使用商家语言，接口名只在解释数据来源或排查问题时出现。

## 连接资料

常用 profile 字段：

```text
app_key
app_secret
access_token
refresh_token 可选
env = prod 或 dev
```

凭证只保存到本机私有配置，不写进项目文档和回复正文。

## 首次接入准备

当用户还没有连接资料时，按以下顺序引导：

| 步骤 | 用户要做什么 | agent 能直接做什么 | 页面 |
| --- | --- | --- | --- |
| 获取密钥和 token | 联系聚水潭或完成开放平台申请审核，拿到 `app_key`、`app_secret`、`access_token` | 检查用户提供的字段是否齐全；不要回显完整密钥 | [聚水潭开放平台](https://openweb.jushuitan.com/) |
| 创建应用 | 在开放平台创建应用，填写公司和应用信息，提交审核 | 给用户整理应用描述和需要申请的接口范围 | [应用管理](https://openweb.jushuitan.com/management/apps) |
| 添加 IP 白名单 | 在应用配置里添加调用方公网出口 IP | 运行 `scripts/jst_erp.mjs public-ip`，直接给出当前公网 IP；失败时让用户打开 `https://api.ipify.org` | [应用管理](https://openweb.jushuitan.com/management/apps) |
| 开启 API 权限 | 在应用详情的 API 接口权限里申请所需接口 | 根据用户场景列出建议开通的接口领域，例如基础、商品、库存 | [应用管理](https://openweb.jushuitan.com/management/apps) |

给用户的话术应尽量直接：

```text
你现在缺少 access_token，需要先在聚水潭开放平台完成应用审核和授权。应用入口是 https://openweb.jushuitan.com/management/apps。
我可以先帮你查当前公网 IP，用于填写 IP 白名单。
```

## 通用调用方式

业务接口通常为表单 POST：

```text
POST https://openapi.jushuitan.com{接口路径}
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
```

系统参数：

```text
access_token
app_key
timestamp
version=2
charset=utf-8
biz
sign
```

`biz` 是业务参数 JSON 字符串。空业务参数也传 `{}` 的 JSON 字符串。

签名口径：

```text
sign = md5(app_secret + 按参数名升序拼接的 key/value 字符串)
```

注意：

- 计算签名时排除 `sign`。
- `biz` 作为完整字符串参与签名，不拆内部 JSON 字段。
- 不在回复里打印完整签名原文、密钥或 token。

## 场景到接口

| 用户场景 | 需要的数据 | 常用接口 | 备注 |
| --- | --- | --- | --- |
| 查店铺和授权 | 店铺列表、授权状态、过期时间 | `/open/shops/query` | 用于回答“哪些店铺快过期/不可用” |
| 查仓库范围 | 主仓、分仓、仓库编号 | `/open/wms/partner/query` | 库存按仓分析前先确认仓库 |
| 查商品资料 | SKU、商品名、启用状态、价格、类目 | `/open/sku/query` | 用于补充库存/订单里的商品信息 |
| 查店铺商品映射 | 线上商品和 ERP SKU 关系 | `/open/skumap/query` | 用于回答“线上商品对应哪个 SKU” |
| 查库存现状和变化 | 实物库存、锁定、虚拟库存、在途、安全库存 | `/open/inventory/query` | 库存经营、补货策略、库存日报的核心数据 |

## 店铺查询

接口：

```text
/open/shops/query
```

适合用户问题：

```text
我有哪些店铺？
哪些店铺授权快过期？
店铺授权有没有失效？
```

常用入参：

```json
{
  "page_index": 1,
  "page_size": 50
}
```

输出关注：

- 店铺名称
- 平台/站点
- 授权状态
- 授权过期时间
- 是否启用

## 仓库查询

接口：

```text
/open/wms/partner/query
```

适合用户问题：

```text
我有哪些仓库？
按哪个仓查库存？
主仓和分仓分别是什么？
```

常用入参：

```json
{
  "page_index": 1,
  "page_size": 50
}
```

输出关注：

- 仓库名称
- `wms_co_id`
- 是否主仓
- 仓库状态

## 商品资料查询

接口：

```text
/open/sku/query
```

适合用户问题：

```text
这些 SKU 分别是什么商品？
哪些商品没启用？
商品资料里价格、类目、品牌是什么？
```

常用入参：

```json
{
  "sku_ids": "SKU1,SKU2",
  "page_index": 1,
  "page_size": 100
}
```

或按修改时间增量：

```json
{
  "modified_begin": "2026-05-01 00:00:00",
  "modified_end": "2026-05-07 23:59:59",
  "page_index": 1,
  "page_size": 100
}
```

输出关注：

- SKU
- 商品名
- 款式编号
- 启用状态
- 价格、类目、品牌
- 是否禁止同步库存

## 店铺商品映射查询

接口：

```text
/open/skumap/query
```

适合用户问题：

```text
线上商品对应 ERP 哪个 SKU？
哪些店铺商品没有映射？
```

常用入参：

```json
{
  "shop_id": 123456,
  "modified_begin": "2026-05-01 00:00:00",
  "modified_end": "2026-05-07 23:59:59",
  "page_index": 1,
  "page_size": 100
}
```

注意：

- 它适合查线上商品和 ERP SKU 的对应关系。
- 不把它当作库存事实来源。

## 库存查询

接口：

```text
/open/inventory/query
```

适合用户问题：

```text
今天哪些 SKU 库存紧张？
哪些货还能卖几天？
哪些商品该补货？
哪些库存被订单占用了？
最近 7 天库存有什么变化？
```

常用入参：按时间范围

```json
{
  "wms_co_id": 0,
  "modified_begin": "2026-05-01 00:00:00",
  "modified_end": "2026-05-07 23:59:59",
  "page_index": 1,
  "page_size": 100,
  "has_lock_qty": true
}
```

常用入参：按 SKU 精确查询

```json
{
  "wms_co_id": 0,
  "sku_ids": "SKU1,SKU2",
  "page_index": 1,
  "page_size": 100,
  "has_lock_qty": true
}
```

输出关注：

- `sku_id`：SKU
- `name`：商品名，可能为空
- `qty`：实物库存
- `order_lock`：订单占用
- `pick_lock`：仓库待发
- `virtual_qty`：虚拟库存
- `purchase_qty`：采购在途
- `in_qty`：进货仓库存
- `return_qty`：销退仓库存
- `min_qty`：安全库存下限，可能为空
- `max_qty`：安全库存上限，可能为空
- `modified`：修改时间
- `ts`：增量游标

常用库存口径：

```text
可售参考库存 = qty - order_lock + virtual_qty
可用参考库存 = qty - order_lock + virtual_qty + purchase_qty + in_qty + return_qty
即时可配货库存 = qty - pick_lock
```

补货和安全库存场景默认使用“可用参考库存”。用户关注“马上能不能发货”时，用“即时可配货库存”。

## 分页和增量

- `page_index` 从 1 开始。
- `page_size` 优先用 100，除非接口或场景要求更小。
- 时间范围查询要按接口限制拆窗口。
- 增量同步时保存上次游标或时间范围。
- 按 `ts` 查询时，优先处理返回数组里的数据和最大 `ts`，不要只依赖分页统计字段。

## 输出建议

对商家输出时优先这样组织：

```text
结论：哪些店铺/SKU/订单需要关注
原因：触发了什么业务条件
数据口径：用的是哪个时间范围、库存口径或订单口径
下一步：建议补资料、补货、处理授权、复查异常
```
