# 科力普接口详细文档

## 一、登录接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/vip/login` |
| 请求方式 | POST |
| 是否需要登录 | 否 |
| 用途 | 账号密码登录，获取后续接口需要使用的 EGG_SESS |

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| loginName | string | 是 | 登录账号，一般为手机号或用户名 |
| pwd | string | 是 | 登录密码 |
| cleartext | string | 是 | 是否明文密码，示例值为 Y |
| hasMobileLogin | boolean | 是 | 是否手机验证码登录；账号密码登录一般为 false |
| scene | string | 是 | 登录场景，H5 端一般为 h5 |

### 请求示例
```bash
curl --location --request POST 'https://h5vip.colipu.com/api/vip/login' \
--header 'content-type: application/json;charset=UTF-8' \
--data-raw '{
  "loginName": "147****6938",
  "pwd": "******",
  "cleartext": "Y",
  "hasMobileLogin": false,
  "scene": "h5"
}'
```

### 响应说明
| 字段 | 类型 | 说明 |
|------|------|------|
| Set-Cookie.EGG_SESS | string | 登录成功后响应头中的会话 Cookie，后续接口需作为 Cookie 传入 |

### 响应成功示例
```json
{
  "code": 1,
  "Data": {
    "accountId": 41447951,
    "customerId": 1315138,
    "loginName": "sunqiang1@colipu.com",
    "accountName": "sunqiang",
    "isGroupAdmin": 0,
    "isAdmin": 1,
    "ownPurchase": 1,
    "ownAudit": 1,
    "ownInvoicing": 0,
    "isAccount": 1,
    "isShowDiscount": 1,
    "bindMobileNo": "",
    "isEditInvoice": true,
    "isEditReceverAddress": true,
    "customerGroupId": 10844,
    "hasConfirmNew": false,
    "needChangePwd": false,
    "enableCategoryMap": false,
    "enableMobileUpload": false,
    "expandProjectId": 0,
    "currentProjectId": 1,
    "isSupportedPaperInvoice": true,
    "isSupportElecInvoice": true,
    "moduleShows": "1_1,2_1,3_1,4_1",
    "costCenterIds": [],
    "canViewAllOrder": true,
    "powerIds": [],
    "showNetPrice": false
  }
}
```

---

## 二、商品搜索接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/b2bSearchApi/SearchByKeyWord` |
| 请求方式 | POST |
| 是否需要登录 | 建议携带 Cookie |
| 用途 | 根据关键词搜索商品，返回商品、价格、SKU、分类、品牌、图片等信息 |

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| siteId | number | 是 | 站点 ID，示例为 211 |
| warehouseIds | array | 是 | 仓库 ID 集合，用于指定商品库存和可售范围 |
| showContract | boolean | 否 | 是否显示合同商品 |
| sortType | number | 否 | 排序方式，示例 12 表示综合/默认排序 |
| keyWord | string | 是 | 搜索关键词 |
| pageIndex | number | 是 | 当前页码，从 1 开始 |
| pageSize | number | 是 | 每页返回数量 |
| provinceId | number | 是 | 省份 ID，影响价格、库存、可售范围 |
| startPrice | string/number | 否 | 起始价格，空字符串表示不限制 |
| endPrice | string/number | 否 | 结束价格，空字符串表示不限制 |
| consumer.customerId | number | 是 | 客户 ID |
| consumer.showType | string | 否 | 展示类型，空表示默认 |

### 请求示例
```bash
curl --location --request POST 'https://h5vip.colipu.com/api/b2bSearchApi/SearchByKeyWord' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=UTF-8' \
--data-raw '{
  "siteId": 211,
  "warehouseIds": [111],
  "showContract": false,
  "sortType": 12,
  "keyWord": "a4",
  "pageIndex": 1,
  "pageSize": 20,
  "provinceId": 2,
  "startPrice": "",
  "endPrice": "",
  "consumer": {"customerId": 187288, "showType": ""}
}'
```

### 响应字段
| 字段 | 类型 | 说明 |
|------|------|------|
| Code | number | 业务状态码，1 表示成功 |
| Data | array | 商品列表 |
| SplitWords | array | 搜索关键词拆词结果 |
| TotalCount | string | 搜索结果总数 |
| Data[].ItemFullName | string | 商品中文完整名称 |
| Data[].ItemFullNameEN | string | 商品英文完整名称 |
| Data[].SaleUnit | string | 销售单位，如 个、包、箱 |
| Data[].SalePrice | number | 当前销售价格 |
| Data[].B2CSalePrice | number | B2C 售价/参考价 |
| Data[].ItemId | number | 商品 ID |
| Data[].ItemCode | string | 商品编码/SKU 编码 |
| Data[].ProductSkuId | number | 商品 SKU ID，下单通常使用该值 |
| Data[].BrandId | number | 品牌 ID |
| Data[].CategoryId1/2/3 | number | 一级/二级/三级分类 ID |
| Data[].IsContractItem | boolean | 是否为合同商品 |
| Data[].DefaultPicture | string | 商品默认图片路径 |

---

## 三、查询商品详情接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/b2bApi/GetAttributeGroupList` |
| 请求方式 | GET |
| 是否需要登录 | 是 |
| 用途 | 查询商品详细属性信息（起订量、交货周期等） |

### 请求示例
```bash
curl --location --request GET 'https://h5vip.colipu.com/api/b2bApi/GetAttributeGroupList?ItemId=10311215' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=utf-8'
```

### 响应示例
```json
{
  "Code": 0,
  "Message": "调用成功",
  "Data": [{
    "AttributeGroupName": "基本参数",
    "AttributeList": [
      { "AttributeOuterName": "打样费用", "AttributeValue": "100元" },
      { "AttributeOuterName": "打样周期", "AttributeValue": "3-5天" },
      { "AttributeOuterName": "交货周期", "AttributeValue": "15-20天" },
      { "AttributeOuterName": "印制方式", "AttributeValue": "烫金/烫银/印刷logo" },
      { "AttributeOuterName": "颜色", "AttributeValue": "单色" },
      { "AttributeOuterName": "参考价", "AttributeValue": "7.68元" },
      { "AttributeOuterName": "起订量", "AttributeValue": "1000个" }
    ],
    "ItemAtte": {
      "ItemId": 10311215,
      "BrandId": 46,
      "BrandName": "晨光",
      "Color": "蓝",
      "Specification": "",
      "Modal": "ADM95088",
      "CreateTime": "2024-04-22 17:08:59"
    }
  }]
}
```

---

## 四、获取收货地址接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/accountApi/receiver/list/0` |
| 请求方式 | GET |
| 是否需要登录 | 是 |
| 用途 | 获取当前登录用户可用的收货地址列表 |

### 请求示例
```bash
curl --location --request GET 'https://h5vip.colipu.com/api/accountApi/receiver/list/0' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=utf-8'
```

### 响应字段
| 字段 | 类型 | 说明 |
|------|------|------|
| ReceiverId | number | 收货地址 ID，下单时传入 Receiver.ReceiverId |
| ContactName | string | 收货联系人 |
| CellPhone | string | 收货人手机号 |
| IsDefault | boolean | 是否默认地址 |
| Area | string | 省市区文本，如 "北京 北京市 昌平区" |
| Address | string | 详细地址 |
| cityId | number | 城市 ID |
| provinceId | number | 省份 ID，下单时传入 Receiver.ProvinceId |
| LogicalWarehouseId | number | 逻辑仓 ID，0 表示未指定 |
| Status | string | 地址状态，A 表示有效 |

### 响应示例
```json
[
  {
    "ReceiverId": 7305,
    "ContactName": "孙强",
    "CellPhone": "1",
    "IsDefault": false,
    "Area": "北京 北京市 昌平区",
    "Address": "1212",
    "IsSetUp": 0,
    "cityId": 274,
    "provinceId": 287,
    "LogicalWarehouseId": 0,
    "Status": "A"
  }
]
```

---

## 五、获取成本中心接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/crm/getConcenter?IsGroupPower=N` |
| 请求方式 | GET |
| 是否需要登录 | 是 |
| 用途 | 获取当前账号可用成本中心，下单时必须选择成本中心 |

### 请求示例
```bash
curl --location --request GET 'https://h5vip.colipu.com/api/crm/getConcenter?IsGroupPower=N' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=utf-8'
```

### 响应字段
| 字段 | 类型 | 说明 |
|------|------|------|
| IsSuccess | boolean | 是否调用成功 |
| Data | array | 成本中心列表 |
| CostCenterId | number | 成本中心 ID，下单时传入 Receiver.CostCenterId |
| CostCenterName | string | 成本中心名称 |
| CostCenterLevel | number | 成本中心层级 |
| ParentCostCenterId | number | 父级成本中心 ID，0 表示顶级 |
| CustomerId | number | 客户 ID |
| OuterCostCenterCode | string | 外部成本中心编码 |
| Status | string | 状态，**A 表示有效**，下单必须选 Status=A 的 |
| IsNeedPoSettlement | number | 是否需要 PO 结算 |

---

## 六、预提交订单接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/confirm/create` |
| 请求方式 | POST |
| 是否需要登录 | 是 |
| 用途 | 根据收货地址、成本中心和商品信息创建预提交订单，返回 GuId |

### 请求模式（统一 Direct=true）

本接口**统一使用 `Direct: true` 模式**，单 SKU / 多 SKU 都走同一格式（多 SKU 会合并为一个订单）。

> ⚠️ **历史模式（Direct=false 购物车结算）已废弃**：购物车 API（`/api/cart/add`、`/api/cart/clear`）已不可用，不要再使用 `Direct=false` 与 `NetPrice / ProvinceId / SkuName / Checked / IsValid / ToTalPrice` 等字段。本节末尾保留废弃模式参数仅作历史参考。

---

### 请求参数（Direct=true）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| SiteId | number | 是 | 站点 ID，示例 211 |
| **Direct** | boolean | 是 | **必须为 true** |
| Receiver | object | 是 | 收货信息 |
| Receiver.CostCenterId | number | 是 | 成本中心 ID（必须 Status==A） |
| Receiver.ReceiverId | number | 是 | 收货地址 ID |
| Items | array | 是 | 商品列表（支持 1~N 个商品） |
| Items[].ItemSkuId | number | 是 | 商品 SKU ID，使用搜索结果的 **ItemId** |
| Items[].SalePrice | number | 是 | 商品销售单价 |
| Items[].SaleQty | number | 是 | 购买数量 |
| Items[].ItemType | number | 是 | 商品类型，1 表示普通商品 |
| ItemPicPath | string | 否 | 商品图片路径前缀 |

### 请求示例（多 SKU 合并为一单）

```bash
curl --location --request POST 'https://h5vip.colipu.com/api/confirm/create' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=UTF-8' \
--data-raw '{
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
}'
```

---

### [DEPRECATED] 历史模式：购物车结算（Direct=false）

> ⚠️ 此模式已废弃，**请勿使用**。仅作历史参考保留。原本需要 `Receiver.ProvinceId`、`Items[].NetPrice`、`Items[].SkuName`、`Items[].ToTalPrice`、`Items[].Checked`、`Items[].IsValid`、`Items[].DiscountMsg`、`Items[].IsContractDiscountItem`、`Items[].B2CSalePrice`、`Items[].ShowContractPrice` 等扩展字段，全部不再需要。

### 响应字段
| 字段 | 类型 | 说明 |
|------|------|------|
| Code | number | 状态码，200 表示成功 |
| Data.Success | boolean | 是否预提交成功 |
| Data.Type | number | 业务类型标识 |
| Data.Message | string | **预提交订单 GUID，确认提交时作为 GuId 参数** |

### 响应示例
```json
{
  "Code": 200,
  "Data": {
    "Success": true,
    "Type": 0,
    "Message": "7c70260e990e4f7ba80e71532f7db3f9"
  }
}
```

---

## 七、确认提交订单接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/confirm/orderConfirm` |
| 请求方式 | POST |
| 是否需要登录 | 是 |
| 用途 | 根据预提交返回的 GuId 正式确认提交订单（**异步**） |

> ⚠️ **订单创建为异步**：本接口返回 `Data.Success==true` 仅代表"提交成功，订单正在生成"，**不会**直接返回订单号 `SoId`。订单号需通过 [八、查询订单创建结果接口](#八查询订单创建结果接口) 异步轮询获取。

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| GuId | string | 是 | 预提交接口返回的 Data.Message |
| SOEvidenceList | array | 否 | 订单凭证列表，普通订单可为空数组 |

### 请求示例
```bash
curl --location --request POST 'https://h5vip.colipu.com/api/confirm/orderConfirm' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=UTF-8' \
--data-raw '{
  "GuId": "947f5aec2a39413d93f9d29efe7f280a",
  "SOEvidenceList": []
}'
```

### 响应示例
```json
{
  "Code": 200,
  "Data": {
    "Success": true,
    "OrderType": 0,
    "Message": ""
  }
}
```

---

## 八、查询订单创建结果接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/confirm/getOrderCreateResult` |
| 请求方式 | POST |
| 是否需要登录 | 是 |
| 用途 | **异步轮询**获取订单号 `SoId`（与 `/api/confirm/orderConfirm` 配套） |

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| GuId | string | 是 | 与 `orderConfirm` 使用同一个 GuId（预提交接口返回的 Data.Message） |

### 请求示例
```bash
curl --location --request POST 'https://h5vip.colipu.com/api/confirm/getOrderCreateResult' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=UTF-8' \
--data-raw '{ "GuId": "05cb0d9abd7c427bbfa272f13a0e5380" }'
```

### 响应字段
| 字段 | 类型 | 说明 |
|------|------|------|
| Code | number | 200 表示请求成功（不代表订单已生成） |
| **Data** | number | **订单号 SoId**（int）；为 0 / null 表示订单仍在异步生成中 |
| Message | string | 错误信息，正常情况下为 null |

### 响应成功示例
```json
{
  "Code": 200,
  "Data": 26344136,
  "Message": null
}
```

### 调用建议
- 在 `orderConfirm` 返回成功后立即开始轮询；间隔 **1 秒**、总超时 **30 秒** 通常足够
- 超时仍未拿到订单号时，退化到 `/api/order/orderlist` 取 `data[0].soId` 兜底
- 持续异常请联系技术支持 `cip_tech@colipu.com`

---

## 九、查询订单接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/order/orderlist` |
| 请求方式 | POST |
| 是否需要登录 | 是 |
| 用途 | 查询当前账号下的订单列表，可按订单类型分页查询 |

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | number | 是 | 订单类型筛选：1=全部、2=审批中、3=待发货、4=已发货 |
| pageNo | number | 是 | 当前页码 |
| pageSize | number | 是 | 每页数量 |
| searchWord | string | 否 | 搜索关键词 |
| soId | string | 否 | 销售订单号 |
| doId | string | 否 | 配送单号 |

### 订单类型枚举
| type | 说明 |
|------|------|
| 1 | 全部订单 |
| 2 | 审批中的订单 |
| 3 | 待发货订单 |
| 4 | 已发货订单 |

### 请求示例
```bash
curl --location --request POST 'https://h5vip.colipu.com/api/order/orderlist' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=UTF-8' \
--data-raw '{
  "type": 1,
  "pageNo": 1,
  "pageSize": 10,
  "searchWord": "",
  "soId": "",
  "doId": ""
}'
```

### 响应字段
| 字段 | 类型 | 说明 |
|------|------|------|
| code | number | 接口状态码，0 表示成功 |
| message | string | 状态说明 |
| data | array | 订单列表 |
| total | string | 总订单数 |

---

## 十、查询订单详情接口

### 接口信息
| 项目 | 内容 |
|------|------|
| 接口地址 | `/api/order/getOrderDetail` |
| 请求方式 | GET |
| 是否需要登录 | 是 |
| 用途 | 根据订单系统号 `soSysno` 查询单笔订单的完整详情（主信息 + 商品明细 + 配送 / 审批记录） |

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| soSysno | number | 是 | 订单系统号（即 `getOrderCreateResult` 返回的 `Data`，或订单列表中的 `soId` / `SysNo`） |

### 请求示例
```bash
curl --location --request GET 'https://h5vip.colipu.com/api/order/getOrderDetail?soSysno=26344136' \
--header 'Cookie: EGG_SESS=xxxxxx' \
--header 'content-type: application/json;charset=utf-8'
```

### 响应顶层结构
| 字段 | 类型 | 说明 |
|------|------|------|
| Code | number | 1 表示成功 |
| Data.SoMaster | object | 订单主信息 |
| Data.SoItem | array | 订单商品明细 |
| Data.DoList | array \| null | 配送单列表（未发货为 null） |
| Data.AuditRecordList | array \| null | 审批记录（无审批为 null） |
| Data.SoEvidences | array \| null | 订单凭证（无凭证为 null） |
| Data.ShowContractPrice | boolean | 是否展示合同价 |

### `Data.SoMaster` 关键字段
| 字段 | 类型 | 说明 |
|------|------|------|
| SysNo | number | 订单系统号（int） |
| **SOID** | string | **展示用订单号**（如 `1026344136`） |
| Status / WebStatus | number | 订单状态码（如 `-6` 表示审批中等） |
| OrderDate | string | 下单时间，格式 `YYYY-MM-DD HH:mm:ss` |
| **RealSOAmt** | number | 订单实付金额（元） |
| ShipPrice | number | 运费 |
| ReceiveContact | string | 收件人姓名 |
| ReceivePhone / ReceiveCellPhone | string | 收件人电话 |
| ReceiveAddress | string | 收件地址 |
| ReceiveAreaSysNo | number | 收件区域系统号 |
| OperatorSysNo / OperatorName / OperatorEmail | mixed | 下单人 |
| WaitAduitDepartmentSysNo | number | 待审批部门 / 成本中心 SysNo |
| DepartmentCompanyName | string | 部门 / 成本中心名称 |
| PayTypeSysNo / PayTypeName | mixed | 支付方式（如 9 / "账期支付"） |
| RequestInvoiceType | number | 发票类型 |
| CustomerSysNo / CustomerVatInfoID | number | 客户 / 抬头信息 |
| Memo | string | 备注 |

### `Data.SoItem[]` 关键字段
| 字段 | 类型 | 说明 |
|------|------|------|
| SysNo | number | 订单行 SysNo |
| SOSysNo | number | 关联订单系统号 |
| ProductSysNo | number | 商品 SysNo |
| **ProductName** | string | 商品全名 |
| BriefName | string | 简称 |
| Modal / Specification | string | 型号 / 规格 |
| **Quantity** | number | 数量 |
| SaleUnit | string | 销售单位（个 / 包 / 箱…） |
| **Price** / **RealPrice** | number | 单价 / 实际成交单价 |
| OrderPrice | number | 下单时单价 |
| NetPrice | number | 不含税单价 |
| TaxRate | number | 税率 |
| ItemSkuCode | string | SKU 编码 |
| IsInStock | number | 是否有库存（1=有） |
| IsSaleStop / IsSaleOver | number | 停售 / 售完标记 |
| UnitPoints / TotalPoints | number | 积分 |
| CreateTime / UpdateTime | string | 创建 / 更新时间 |

### 响应成功示例
```json
{
  "Code": 1,
  "Data": {
    "SoMaster": {
      "SysNo": 26344136,
      "SOID": "1026344136",
      "Status": -6,
      "OrderDate": "2026-05-06 17:39:42",
      "RealSOAmt": 50.8,
      "ReceiveContact": "ceshi",
      "ReceiveAddress": "北京北京市海淀区cdhue",
      "ReceivePhone": "12345678909",
      "DepartmentCompanyName": "信息技术部-CIP组",
      "PayTypeName": "账期支付"
    },
    "SoItem": [
      {
        "SysNo": 118091408,
        "SOSysNo": 26344136,
        "ProductName": "希乐 cille 保温杯 LV-24716 500ml (黑色/白色) 颜色随机发货",
        "BriefName": "希乐 保温杯 LV-24716 500ml (黑色/白色)",
        "Quantity": 1,
        "SaleUnit": "个",
        "Price": 50.8,
        "RealPrice": 50.8,
        "NetPrice": 44.96,
        "TaxRate": 0.13,
        "ItemSkuCode": "7405129"
      }
    ],
    "DoList": null,
    "AuditRecordList": null,
    "SoEvidences": null,
    "ShowContractPrice": false
  }
}
```

### 调用建议
- 与 `getOrderCreateResult` 配合使用：下单 → 拿 `SoId` → 立即调用本接口向用户回显商品明细与状态
- 展示给用户优先用 `Data.SoMaster.SOID`（含 `10` 前缀）作为可读订单号
- 状态字段（`Status` / `WebStatus`）的具体枚举不在本文档范围，必要时联系 `cip_tech@colipu.com` 索取