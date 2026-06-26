# Filtalgo 购物 API 使用指南

## 目录
- [基础信息](#基础信息)
- [认证接口](#认证接口)
- [商品接口](#商品接口)
- [购物车接口](#购物车接口)
- [下单接口](#下单接口)
- [订单接口](#订单接口)
- [地址接口](#地址接口)
- [重要提示](#重要提示)

## 基础信息

**API 基础地址**：`https://service.filtalgo.com`

**Token 传递方式**：
- Header 名称：`accessToken`
- 注意：不是 `Authorization: Bearer`，而是自定义 header

**Content-Type**：所有请求使用 `application/json`

## 认证接口

### 发送验证码
```
GET /auth/agent/sms/send?mobile={手机号}&scene=LOGIN
```
- 无需 token
- 测试环境验证码固定为 `111111`

### 短信登录
```
POST /auth/agent/smsLogin
Body: {"mobile": "手机号", "code": "验证码"}
```
- 返回 `accessToken` 和 `refreshToken`

### 刷新 Token
```
GET /auth/refresh?refreshToken={refreshToken}
```

## 商品接口

### 搜索商品
```
GET /goods/elasticsearch/es
Query: keyword, categoryId, brandId, priceMin, priceMax, pageNumber, pageSize, sort
```
- 无需 token
- 排序：PRICE_ASC / PRICE_DESC / SALE_DESC

### 商品详情
```
GET /goods/sku/vo/{goodsId}/{skuId}
```
- 无需 token
- `goodsId` 是商品ID，`skuId` 是 SKU ID

## 购物车接口

### 加入购物车
```
POST /order/carts/json
Header: accessToken
Body: {"skuId": "SKU ID", "num": 数量, "way": "BUY_NOW|CART"}
```

### 查看购物车
```
GET /order/carts/all?way=CART
Header: accessToken
```

### 购物车数量
```
GET /order/carts/count?way=CART
Header: accessToken
```

## 下单接口

### 设置收货地址
```
PUT /order/carts/shippingAddress?way={BUY_NOW|CART}&shippingAddressId={地址ID}
Header: accessToken
```

### 预览订单
```
GET /order/carts/checked?way={BUY_NOW|CART}
Header: accessToken
```

### 创建订单
```
POST /order/carts/create/trade
Header: accessToken
Body: {"way": "BUY_NOW|CART", "client": "AGENT"}
```
- 返回 `sn`（交易单号，T 开头）

## 订单接口

### 订单列表
```
GET /order?orderStatus={状态}&pageNumber={页}&pageSize={数量}
Header: accessToken
```
- 状态：UNPAID / UNDELIVERED / DELIVERED / COMPLETED / CANCELLED

### 订单详情
```
GET /order/{orderSn}
Header: accessToken
```
- orderSn 是 O 开头的子订单号

### 取消订单
```
POST /order/{orderSn}/cancel?reason={原因}
Header: accessToken
```
- 仅 UNPAID 状态可取消

### 物流查询
```
GET /order/getPackage/{orderSn}
Header: accessToken
```

## 地址接口

### 地址列表
```
GET /user/address
Header: accessToken
```

### 默认地址
```
GET /user/address/default
Header: accessToken
```

### 解析地址
```
GET /system/region/resolve?province={省}&city={市}&district={区}&street={街道}
Header: accessToken
```

### 新增地址
```
POST /user/address
Header: accessToken
Body: {
  "name": "姓名",
  "mobile": "手机",
  "consigneeAddressIdPath": "地址ID路径",
  "consigneeAddressPath": "地址名路径",
  "detail": "详细地址",
  "isDefault": false,
  "type": "RECEIVE"
}
```

### 设为默认
```
PUT /user/address/default/{addressId}
Header: accessToken
```

## 重要提示

1. **Token 有效期**：accessToken 约 25 天，refreshToken 约 45 天
2. **订单号区分**：
   - T 开头：交易单号（tradeSn），用于支付
   - O 开头：子订单号（orderSn），用于查询/取消
3. **way 参数**：
   - BUY_NOW：立即购买（单个商品）
   - CART：购物车批量下单
4. **地址 type**：必须传 `RECEIVE`，否则买家端不可见
5. **商品详情页 URL**：
   - H5：`https://buyer.filtalgo.com/goodsDetail?goodsId={goodsId}&skuId={skuId}`
   - APP：`https://app-buyer.filtalgo.com/pages/goods/product/detail?goodsId={goodsId}&skuId={skuId}`
