---
name: beauty-shop
description: 美妆电商购物助手，支持商品搜索、加购下单、订单管理；当用户需要购买美妆产品、查询订单或管理收货地址时使用
---

# 美妆电商购物助手

## 任务目标
- 本 Skill 用于：完整的电商购物流程
- 能力包含：用户登录、商品搜索、商品详情、加购/立即购买、下单、订单管理、物流查询、收货地址管理
- 触发条件：用户表达购买意图、查询商品、查看订单、管理地址等场景

## 前置准备
- 用户需先完成短信验证码登录
- 部分接口需要 accessToken 认证

## 核心流程

### 一、用户登录
**触发时机**：用户首次使用或需要下单时

**执行步骤**：
1. 调用 `scripts/auth/send_sms.py <手机号>` 发送验证码
2. 智能体提示用户输入验证码
3. 调用 `scripts/auth/sms_login.py <手机号> <验证码>` 完成登录
4. 登录成功后获取 accessToken 和 refreshToken

**测试环境**：验证码固定为 `111111`

### 二、商品搜索
**执行方式**：调用脚本
```bash
python scripts/goods/search.py --keyword "洗面奶" --page 1 --size 10 --sort PRICE_ASC
```

**参数说明**：
- `--keyword`：搜索关键词
- `--page`：页码，默认1
- `--size`：每页数量，默认10
- `--sort`：排序方式（PRICE_ASC/PRICE_DESC/SALE_DESC）

**返回信息**：商品列表包含 goodsId、skuId、goodsName、price、thumbnail、storeName 等

### 三、商品详情
**执行方式**：调用脚本
```bash
python scripts/goods/detail.py <goodsId> <skuId>
```

**返回信息**：包含商品详细规格、SKU列表、价格、库存等

### 四、购物车管理
**加购**：`python scripts/cart/add.py <skuId> <数量> BUY_NOW|CART`
**查看**：`python scripts/cart/list.py`
**数量**：`python scripts/cart/count.py`

### 五、下单流程
**立即购买**（单个商品）：
1. `add_to_cart`：加购（way=BUY_NOW）
2. `set_address`：设置收货地址
3. `preview_order`：预览订单确认价格
4. `create_order`：创建订单获取 trade_sn
5. 返回支付链接

**购物车结算**（多个商品）：
1. `cart_list`：查看购物车
2. `set_address`：设置收货地址
3. `preview_order`：预览订单
4. `create_order`：创建订单

### 六、订单管理
**订单列表**：`python scripts/order/list.py --status UNPAID --page 1`
**订单详情**：`python scripts/order/detail.py <orderSn>`
**取消订单**：`python scripts/order/cancel.py <orderSn> <原因>`
**物流查询**：`python scripts/order/logistics.py <orderSn>`

### 七、收货地址管理
**地址列表**：`python scripts/address/list.py`
**默认地址**：`python scripts/address/default.py`
**解析地址**：`python scripts/address/resolve.py <省> <市> <区> [街道]`
**新增地址**：`python scripts/address/add.py <姓名> <手机> <地址ID路径> <地址名路径> <详细地址> [是否默认]`
**设为默认**：`python scripts/address/set_default.py <addressId>`

## 资源索引

### 认证脚本
| 脚本 | 功能 |
|------|------|
| [scripts/auth/send_sms.py](scripts/auth/send_sms.py) | 发送短信验证码 |
| [scripts/auth/sms_login.py](scripts/auth/sms_login.py) | 短信登录 |

### 商品脚本
| 脚本 | 功能 |
|------|------|
| [scripts/goods/search.py](scripts/goods/search.py) | 搜索商品 |
| [scripts/goods/detail.py](scripts/goods/detail.py) | 商品详情 |

### 购物车脚本
| 脚本 | 功能 |
|------|------|
| [scripts/cart/add.py](scripts/cart/add.py) | 加购物车/立即购买 |
| [scripts/cart/list.py](scripts/cart/list.py) | 查看购物车 |
| [scripts/cart/count.py](scripts/cart/count.py) | 购物车数量 |

### 订单脚本
| 脚本 | 功能 |
|------|------|
| [scripts/order/set_address.py](scripts/order/set_address.py) | 设置收货地址 |
| [scripts/order/preview.py](scripts/order/preview.py) | 预览订单 |
| [scripts/order/create.py](scripts/order/create.py) | 创建订单 |
| [scripts/order/list.py](scripts/order/list.py) | 订单列表 |
| [scripts/order/detail.py](scripts/order/detail.py) | 订单详情 |
| [scripts/order/cancel.py](scripts/order/cancel.py) | 取消订单 |
| [scripts/order/logistics.py](scripts/order/logistics.py) | 物流查询 |

### 地址脚本
| 脚本 | 功能 |
|------|------|
| [scripts/address/list.py](scripts/address/list.py) | 地址列表 |
| [scripts/address/default.py](scripts/address/default.py) | 默认地址 |
| [scripts/address/resolve.py](scripts/address/resolve.py) | 解析地址 |
| [scripts/address/add.py](scripts/address/add.py) | 新增地址 |
| [scripts/address/set_default.py](scripts/address/set_default.py) | 设为默认 |

### 参考文档
- [references/api_guide.md](references/api_guide.md)：API 详细接口文档

## 典型对话示例

### 示例1：用户想购买商品
```
用户：我想买一款洗面奶

智能体：
1. 调用搜索脚本查找洗面奶
2. 展示商品列表（图片+价格+店铺）
3. 询问用户选择哪款商品
4. 用户确认后，调用商品详情脚本展示规格

用户：就选第一款

智能体：
1. 检查是否已登录
2. 未登录：发送验证码让用户登录
3. 登录成功后：
   - 调用加购（BUY_NOW）
   - 设置收货地址
   - 预览订单
   - 创建订单，获取 trade_sn
4. 返回支付链接给用户：
   - APP支付：`https://app-buyer.filtalgo.com/pages/mine/payment/payOrder?trade_sn={trade_sn}`
   - H5支付：`https://buyer.filtalgo.com/payment/cashier?paymentScene=TRADE&orderSn={trade_sn}`
```

### 示例2：用户查询订单
```
用户：查看我的订单

智能体：
1. 调用订单列表脚本
2. 展示订单列表（包含订单号、状态、金额、时间）
3. 询问用户需要什么操作（查看详情/取消/查物流）
```

### 示例3：新增收货地址
```
用户：添加一个新地址

智能体：
1. 询问收货人信息（姓名、手机、省市区、详细地址）
2. 用户提供后：
   - 调用解析地址脚本获取 ID 路径
   - 调用新增地址脚本
3. 确认添加成功
```

## 注意事项

1. **Token 管理**：accessToken 有效期约 25 天，refreshToken 约 45 天
2. **订单号区分**：
   - T 开头：交易单号（tradeSn），用于支付
   - O 开头：子订单号（orderSn），用于查询/取消
3. **地址类型**：新增地址必须传 `type=RECEIVE`
4. **way 参数**：BUY_NOW=立即购买（单商品），CART=购物车模式
5. **商品详情页**：
   - H5：`https://buyer.filtalgo.com/goodsDetail?goodsId={goodsId}&skuId={skuId}`
   - APP：`https://app-buyer.filtalgo.com/pages/goods/product/detail?goodsId={goodsId}&skuId={skuId}`
