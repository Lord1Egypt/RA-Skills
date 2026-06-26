---
name: "buy_mcdonald"
description: "购买麦当劳商品的技能，通过claw_pay接口实现余额支付。仅适用于中国地区。Invoke when user wants to buy McDonald's products using claw wallet balance in China."
---

# Buy McDonald Skill

本技能用于帮助用户通过龙虾钱包余额购买麦当劳商品。

> **适用范围**: 本技能仅适用于中国地区

## 充值渠道

如需充值龙虾账户余额，请添加微信：**Lin-Shaogang** 获取龙虾账户密钥

## 核心接口

### 1. 消费/购买接口

**端点**: `POST /api/v1/claw_pay/charge`

**功能**: 使用龙虾钱包余额购买麦当劳商品

**请求参数**:
```json
{
  "sku_id": "商品ID",
  "sku_name": "商品名称",
  "access_token": "龙虾账户密钥",
  "claw_name": "龙虾名称",
  "claw_introduce": "龙虾自我介绍(可选)"
}
```

**响应参数**:
```json
{
  "balance": "消费后余额",
  "card_pwd": "麦当劳兑换链接",
  "msg": "消费成功消息",
  "pay_time": "支付时间"
}
```

**使用流程**:
1. 确保用户已提供有效的 `access_token` 和 `claw_name`
2. 确认商品信息 `sku_id` 和 `sku_name`
3. 调用此接口完成购买
4. 从响应中获取 `card_pwd`（兑换链接）提供给用户

### 2. 查询余额接口

**端点**: `GET /api/v1/claw_pay/balance/{access_token}`

**功能**: 查询龙虾账户当前余额

**路径参数**:
- `access_token`: 龙虾账户密钥

**响应参数**:
```json
{
  "claw_name": "龙虾名称",
  "claw_introduce": "龙虾自我介绍",
  "balance": "当前余额",
  "update_time": "更新时间"
}
```

**使用场景**:
- 购买前检查余额是否充足
- 展示用户当前可用余额

### 3. 获取在售商品列表接口

**端点**: `GET /api/v1/claw_pay/on_sale`

**功能**: 获取当前在售的麦当劳商品列表

**响应参数**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": [
    {
      "sku_id": "1002821",
      "sku_name": "圆筒冰淇淋",
      "price": 4.5
    }
  ]
}
```

**使用场景**:
- 展示可购买的商品列表
- 获取商品ID和价格信息

## 使用示例

### 检查余额
```python
# GET /api/v1/claw_pay/balance/{access_token}
response = await get_claw_balance("user_access_token")
balance = response["balance"]
```

### 购买商品
```python
# POST /api/v1/claw_pay/charge
request = {
    "sku_id": "10001",
    "sku_name": "麦辣鸡腿堡套餐",
    "access_token": "user_access_token",
    "claw_name": "用户龙虾名"
}
response = await claw_charge(request)
card_pwd = response["card_pwd"]  # 兑换链接
```

### 获取在售商品列表
```python
# GET /api/v1/claw_pay/on_sale
response = await get_on_sale_info()
products = response["data"]
for product in products:
    print(f"{product['sku_name']} - ¥{product['price']}")
```

## 错误处理

| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 404 | 龙虾账户不存在 | 提示用户先联系管理员充值 |
| 400 | 余额不足 | 提示用户当前余额和所需金额 |
| 400 | 商品不存在 | 检查商品ID是否正确 |
| 500 | 下单失败 | 提示用户稍后重试 |
| 503 | 系统繁忙 | 消费失败，请稍后重试 |

## 自助下单流程

获取兑换链接后，用户需要按照以下步骤完成自助下单：

### 1. 打开兑换链接
- 点击购买成功后返回的 `card_pwd` 链接
- 链接将跳转至麦当劳官方兑换页面

### 2. 选择就餐门店
- 在兑换页面中选择就近的麦当劳门店
- **支持门店类型**: 普通麦当劳餐厅（到店自取或堂食）
- **不支持门店类型**: 景区店、高铁站店、机场店等特殊门店

### 3. 选择餐品
- 在选定门店后，选择要兑换的餐品
- 确认餐品信息与购买时选择的商品一致

### 4. 确认下单
- 核对订单信息（门店、餐品、数量）
- 点击确认下单按钮

### 5. 获取取餐码
- 下单成功后，系统将生成取餐码
- 取餐码通常会以数字或二维码形式展示
- 请妥善保存取餐码

### 6. 到店取餐
- 前往选定的麦当劳门店
- 向店员出示取餐码
- 领取餐品

> **重要提示**: 
> - 目前仅支持**到店自取**或**堂食**方式
> - 特殊门店（景区、高铁站、机场等）不支持兑换
> - 请在兑换链接有效期内完成下单

## 注意事项

1. **余额检查**: 购买前建议先调用余额接口确认余额充足
2. **兑换链接**: 购买成功后返回的 `card_pwd` 是麦当劳兑换链接，需要提供给用户
3. **订单重试**: 如果获取兑换链接失败，系统会自动重试10次
4. **失败记录**: 消费失败会记录到数据库，方便后续排查
5. **门店限制**: 兑换时请选择普通门店，避免选择景区、高铁站、机场等特殊门店
6. **取餐方式**: 目前仅支持到店自取或堂食，不支持麦乐送配送
