---
name: colipu-procurement
description: 科力普（Colipu）B2B 办公用品采购助手，覆盖商品搜索、下单、订单详情、订单查询、取消订单全流程。当用户说「在科力普 / Colipu 上买 / 采购 / 下单 / 订购」任何办公用品（A4 纸、文具、保温杯、电脑配件、桌椅等），或「查 / 取消科力普订单」「调用 colipu API」时触发。不适用于：售后退换、合同议价、非科力普平台采购。。
---

# 科力普采购助手

帮助 AI Agent 在科力普 B2B 平台代用户完成「搜索 → 下单 → 查询」全流程，并对用户确认环节做强制校验。

## 1. 适用范围

| 适用 | 不适用 |
|------|-------|
| 在科力普平台采购日常办公用品 | 非科力普的其他平台采购 |
| 单 SKU 或多 SKU 合并下单 | 合同谈判 / 议价 |
| 订单状态查询与取消 | 售后退换货 |
| 通过 API 直接交互 | 网页端模拟点击 |

## 2. 强制约束（必读）

1. **用户确认是必经环节**：展示完整订单信息（商品清单、合计金额、收件人、成本中心）后，用户输入 `y` 才可正式提交，**严禁跳过确认自动下单**。
2. **不做预算校验**：金额合理性由用户判断。
3. **敏感信息保密**：账号 / 密码 / Cookie / TraceId 严禁写入代码仓库或日志，必须从环境变量或密钥管理服务读取。
4. **预提交失败立即终止**：`/api/confirm/create` 返回 `Data.Success != true` 时不得继续调用 `/api/confirm/orderConfirm`。
5. **统一使用 `Direct=true` 模式**：购物车 API 已废弃（`/api/cart/add` 添加无效，`/api/cart/clear` 返回 404），不再支持 `Direct=false`。
6. **多 SKU 合并为一单**：`Direct=true` 的 `Items` 数组支持 1~N 个商品，所有 SKU 一次性提交合并为单个订单，**禁止**为每个 SKU 单独发起预提交。

## 3. Agent 快速决策

| 用户场景 | 推荐入口 |
|---------|---------|
| 用户已经给出 ItemId，想直接下单 | `python scripts/colipu_order.py "${ITEM_ID},${QTY}" ...` |
| 用户给关键词，希望先看再选 | 先调 `colipu_search.py`，由用户口头反馈编号后再走 `colipu_order.py` |
| 用户希望一站式完成（搜索 → 选号 → 确认 → 下单） | `python scripts/buy_products.py ${KEYWORD} ${MAX_PRICE} ${NUM_ITEMS}` |
| 自定义流程 / 嵌入到其他逻辑 | `from colipu_client import ColipuClient` 直接 import |
| 仅查询订单列表 / 取消订单 | 直接调 `ColipuClient.get_orders()` / `ColipuClient.cancel_order()` |
| 拿到 GuId 后查询异步生成的订单号 | `ColipuClient.wait_order_create_result(${GUID})` |
| 根据订单号查询订单详情（商品明细 / 收件人 / 状态 / 金额） | `ColipuClient.get_order_detail(${SO_ID})` |

## 4. 公共信息

| 项目 | 内容 |
|------|------|
| 域名 | `https://h5vip.colipu.com` |
| 鉴权 | 登录响应头 `Set-Cookie` 中的 `EGG_SESS`，后续请求头携带 `Cookie: EGG_SESS=${EGG_SESS}` |
| Content-Type | `application/json;charset=UTF-8` |
| 默认 SiteId | `211` |
| 默认 WarehouseId | `111` |
| 默认 ProvinceId | `2`（仅搜索时需要） |

## 5. 接口速查

| # | 接口 | 方法 | 用途 | 关键返回字段 |
|---|------|------|------|-------------|
| 1 | `/api/vip/login` | POST | 账号密码登录 | 响应头 `Set-Cookie.EGG_SESS`、`Data.customerId` |
| 2 | `/api/b2bSearchApi/SearchByKeyWord` | POST | 关键词搜索商品 | `Data[].ItemId`、`Data[].SalePrice`、`Data[].ItemFullName` |
| 3 | `/api/b2bApi/GetAttributeGroupList` | GET | 商品详情（属性、起订量等） | `Data[].AttributeList`、`Data[].ItemAtte` |
| 4 | `/api/accountApi/receiver/list/0` | GET | 收货地址列表 | `[].ReceiverId`、`[].Status==A` |
| 5 | `/api/crm/getConcenter?IsGroupPower=N` | GET | 成本中心列表 | `Data[].CostCenterId`、`Data[].Status==A` |
| 6 | `/api/confirm/create` | POST | 预提交订单（拿 GuId） | `Data.Success`、`Data.Message`(=GuId) |
| 7 | `/api/confirm/orderConfirm` | POST | 确认提交订单（异步） | `Data.Success`（**SoId 不在此接口返回**） |
| 8 | `/api/confirm/getOrderCreateResult` | POST | **异步查询订单号**（拿 SoId） | `Code==200` 时 `Data` 即订单号（int） |
| 9 | `/api/order/orderlist` | POST | 查询订单列表 | `data[].soId`、`data[].status` |
| 10 | `/api/order/getOrderDetail?soSysno=${SO_ID}` | GET | 根据订单号查订单详情 | `Data.SoMaster`、`Data.SoItem[]` |
| 11 | `/api/order/CancelOrder` | POST | 取消订单 | `Code==1` 且 `Data=={"1":"操作成功"}` |

> 完整字段说明、请求示例与响应字段表参见 `references/api.md`。

## 6. 下单请求格式（统一 Direct=true）

```json
{
  "SiteId": 211,
  "Direct": true,
  "Receiver": {
    "CostCenterId": 1532475,
    "ReceiverId": 33239
  },
  "Items": [
    { "ItemSkuId": 1384061,  "SalePrice": 134, "SaleQty": 1, "ItemType": 1 },
    { "ItemSkuId": 13577742, "SalePrice": 60,  "SaleQty": 1, "ItemType": 1 }
  ],
  "ItemPicPath": "https://pic.colipu.com/pmspic/ItemPicture/"
}
```

> Direct=true 模式下 **无需** 传 `NetPrice / ProvinceId / SkuName / ToTalPrice / Checked / IsValid` 等字段，最小 4 字段即可下单。

## 7. 字段取值规则（重要）

| 目标字段 | 来源 | 备注 |
|---------|------|------|
| `Items[].ItemSkuId` | 搜索结果的 `Data[].ItemId` | **使用 ItemId**，不是 `ProductSkuId` |
| `Items[].SalePrice` | 搜索结果的 `Data[].SalePrice` | 直接透传 |
| `Items[].SaleQty` | 用户指定数量 | 默认 1 |
| `Items[].ItemType` | 固定 `1` | 普通商品 |
| `Receiver.ReceiverId` | 收货地址列表 | 优先 `IsDefault=true`，否则取第一个 |
| `Receiver.CostCenterId` | 成本中心列表 | **必须 `Status=="A"`**，取第一个有效项 |
| `GuId`（确认提交用） | 预提交响应 `Data.Message` | `Code==200 && Data.Success==true` 才取 |
| 订单号（SoId） | `/api/confirm/getOrderCreateResult` 响应 `Data`（int） | 订单**异步**生成，confirm_order 不直接返回 SoId；建议轮询 1~30s（Python 用 `wait_order_create_result(guid)`）；超时再退化到 `orderlist` 取 `data[0].soId` |
| 显示用订单号 | `getOrderDetail` 响应 `Data.SoMaster.SOID` | 字符串（如 `1026344136`），用于向用户展示；内部传参仍用 `SysNo`（int） |
| 订单状态 | `Data.SoMaster.Status` 或 `WebStatus` | 数值码，配合 `getOrderDetail` 详情页展示 |
| 实付金额 | `Data.SoMaster.RealSOAmt` | 元，可直接展示 |
| 商品明细 | `Data.SoItem[]` | 关键字段：`ProductName / Quantity / Price / RealPrice / SaleUnit` |

## 8. 完整下单流程（伪代码）

```
登录 → 取 EGG_SESS → 搜索商品 → 取收货地址 → 取成本中心
     → 预提交订单 → ★用户确认(y) → 确认提交 → 异步查询订单号 → 查询订单
```

```bash
# 1. 登录 → 拿到 EGG_SESS
POST /api/vip/login
{ "loginName":"${COLIPU_LOGIN_NAME}", "pwd":"${COLIPU_PASSWORD}",
  "cleartext":"Y", "hasMobileLogin":false, "scene":"h5" }
→ Set-Cookie 中提取 EGG_SESS

# 2. 搜索商品
POST /api/b2bSearchApi/SearchByKeyWord
Cookie: EGG_SESS=${EGG_SESS}
{ "siteId":211, "warehouseIds":[111], "keyWord":"${KEYWORD}",
  "pageIndex":1, "pageSize":20, "provinceId":2,
  "consumer":{ "customerId":${CUSTOMER_ID}, "showType":"" } }
→ 取 Data[].ItemId / Data[].ItemFullName / Data[].SalePrice

# 3. 收货地址
GET /api/accountApi/receiver/list/0
→ 取 ReceiverId（数组，优先 IsDefault=true）

# 4. 成本中心
GET /api/crm/getConcenter?IsGroupPower=N
→ 取 Status=="A" 的 CostCenterId

# 5. 预提交（多 SKU 合并为一单）
POST /api/confirm/create
{ "SiteId":211, "Direct":true,
  "Receiver":{ "CostCenterId":${COST_CENTER_ID}, "ReceiverId":${RECEIVER_ID} },
  "Items":[ { "ItemSkuId":${ITEM_ID}, "SalePrice":${PRICE}, "SaleQty":${QTY}, "ItemType":1 } ],
  "ItemPicPath":"https://pic.colipu.com/pmspic/ItemPicture/" }
→ Code==200 && Data.Success==true 时，Data.Message 即 ${GUID}

# 6. ★ 用户确认（强制环节，不可省略）
向用户展示：商品清单 / 合计金额 / 收件人 / 成本中心
等待用户输入 y；输入其他字符 → 直接退出，不再调用第 7 步

# 7. 确认提交（异步：本接口不直接返回 SoId）
POST /api/confirm/orderConfirm
{ "GuId":"${GUID}", "SOEvidenceList":[] }
→ Data.Success==true 表示提交成功；订单号需走第 8 步异步查询

# 8. 异步查询订单号（轮询，间隔 ~1s，总超时 ~30s）
POST /api/confirm/getOrderCreateResult
{ "GuId":"${GUID}" }
→ Code==200 && Data 为 int(>0) 时，Data 即 ${SO_ID}
→ Data 为 null/0 表示订单仍在创建中，继续轮询

# 9. 查询订单（可选验证 / 兜底）
POST /api/order/orderlist
{ "type":1, "pageNo":1, "pageSize":10, "searchWord":"", "soId":"", "doId":"" }
→ data[0] 为最新订单

# 10. 查询订单详情（向用户回显商品明细 / 状态 / 金额）
GET /api/order/getOrderDetail?soSysno=${SO_ID}
→ Code==1 时：
  Data.SoMaster.SOID / Status / RealSOAmt / OrderDate / ReceiveContact / ReceiveAddress
  Data.SoItem[]: ProductName / Quantity / Price / RealPrice / SaleUnit
```

## 9. 附加操作：取消订单

```bash
POST /api/order/CancelOrder
Cookie: EGG_SESS=${EGG_SESS}
{ "OrderId":"${SO_ID}", "CancelReason":"${REASON}" }
→ Code==1 && Data=={"1":"操作成功"} 表示取消成功
```

> 仅可取消「审批中」或「待发货」状态的订单；已发货 / 已完成订单需走售后流程。

## 10. 订单类型枚举

| `type` | 含义 |
|-------|------|
| 1 | 全部订单 |
| 2 | 审批中 |
| 3 | 待发货 |
| 4 | 已发货 |

## 11. 配套脚本

> 全部位于 `scripts/`，依赖 `colipu_client.py`，凭据从环境变量 `COLIPU_LOGIN_NAME` / `COLIPU_PASSWORD` 读取（`customerId` 由登录响应自动回填）。

| 脚本 | 用途 | 适用场景 |
|------|------|---------|
| `colipu_client.py` | `ColipuClient` 基础类，封装全部接口 | 自定义流程时直接 import |
| `colipu_search.py` | 搜索 + 价格过滤 + 列表展示 | 用户先看再决定的两步流程 |
| `colipu_order.py` | 按「ItemId,数量」批量下单 | 用户已经确定 SKU |
| `buy_products.py` | 一站式：搜索 → 选号 → 用户确认 → 下单 | 单次完整下单交互 |

输出约定：`[OK]` 成功、`[X]` 失败、`[i]` 提示。

## 12. 错误处理

| 现象 | 处理方式 |
|------|---------|
| 登录返回 `code != 1` | 终止，提示用户检查账号 / 密码 |
| 401 / EGG_SESS 失效（其他接口提示未登录） | 重新调用 `/api/vip/login` 取新 `EGG_SESS` 后重试 |
| 搜索 `Data` 为空 | 提示更换关键词 |
| 价格过滤后无结果 | 提示放宽 `${MAX_PRICE}` 或换商品 |
| 收货地址 / 成本中心列表为空 | 终止，提示去网页端先维护一条 |
| 预提交 `Data.Success != true` | 输出 `Data.Message`，**直接终止**，不得调用确认接口 |
| 确认提交 `Data.Success != true` | 输出原因；如需重试需重新走预提交 |
| `getOrderCreateResult` 长时间 `Data` 为 0 / null | 已超过轮询超时（如 30s），提示用户「订单已提交但仍在异步生成」，并去 `orderlist` 兜底查询；多次复现需走技术支持邮箱 |
| 取消订单 `Code != 1` | 输出 `Data` 中的错误信息，建议人工到网页端操作 |
| **以上任一情况无法解决 / 接口持续报错 / 字段含义不明** | 终止当前流程，提示用户发邮件至 **`cip_tech@colipu.com`**（科力普技术支持），邮件内容附上：账号、接口路径、请求体、完整响应体、复现时间 |

## 13. 技术支持

| 项目 | 内容 |
|------|------|
| 邮箱 | **`cip_tech@colipu.com`** |
| 适用场景 | 接口持续异常、字段含义不明、账号 / 权限问题、新增需求等无法通过本技能自动处理的情况 |
| 邮件建议附带 | 登录账号、接口路径、请求体（脱敏）、完整响应体、复现时间、`TraceId`（如有） |

> Agent 在自动重试 / 错误处理失败后，应主动告知用户上述邮箱并给出邮件草稿模板，**不要无限重试**。

## 14. 详细接口文档

完整接口参数说明、响应字段说明、枚举值参见 `references/api.md`。

---

> 最后更新：2026-05-06　|　技术支持：`cip_tech@colipu.com`
