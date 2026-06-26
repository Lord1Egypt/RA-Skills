# 科力普采购助手配置示例

## 环境变量配置

在使用本技能前，需要设置以下环境变量：

```bash
# 登录账号（手机号或邮箱）
export COLIPU_LOGIN_NAME="your_login_name"

# 登录密码
export COLIPU_PASSWORD="your_password"
```

## 配置说明

| 环境变量 | 说明 | 获取方式 |
|---------|------|---------|
| COLIPU_LOGIN_NAME | 登录账号 | 科力普注册账号 |
| COLIPU_PASSWORD | 登录密码 | 科力普登录密码 |

> 客户 ID（`customerId`）会在登录成功后由 `ColipuClient` 自动从响应 `Data.customerId` 回填，无需用户手动配置。

## 安全提示

⚠️ **严禁将账号密码写入代码仓库或正式文档！**

- 敏感信息应从环境变量或密钥管理服务读取
- 日志输出时必须脱敏处理
- Cookie/Session 信息不要持久化存储

## 技术支持

遇到无法自动处理的问题（接口持续报错、字段含义不明、账号 / 权限问题等），请发邮件至 **`cip_tech@colipu.com`**，邮件中附上：登录账号、接口路径、请求体（脱敏）、完整响应体、复现时间、`TraceId`（如有）。

## 使用示例

### 推荐：脚本两步流程（与 SKILL 一致）

```bash
# Step 1: 搜索 + 价格过滤，由用户口头反馈商品编号
python scripts/colipu_search.py

# Step 2: 用户确定 ItemId 后，按「ItemId,数量」格式批量下单
python scripts/colipu_order.py "1384061,1" "13577742,2"
```

或一站式（搜索 → 选号 → 用户确认 → 下单）：

```bash
python scripts/buy_products.py "A4 复印纸" 200 10
# 参数：关键词 价格上限(元) 展示前 N 项
```

### Python 脚本调用（自定义流程）

```python
from colipu_client import ColipuClient

client = ColipuClient()  # 自动从环境变量读凭据

# 1) 登录
login_result = client.login()
if login_result.get("code") != 1:
    raise SystemExit("登录失败")

# 2) 搜索
search_result = client.search_products(keyword="a4复印纸")
products = search_result.get("Data", [])

# 3) 收货地址 + 成本中心
receiver = client.get_receivers()[0]
cost_center = client.get_valid_cost_centers()[0]

# 4) 构建商品项（Direct=true 仅需 4 字段）
items = [client.build_order_item(
    item_sku_id=products[0]["ItemId"],
    sale_price=products[0]["SalePrice"],
    sale_qty=1,
)]

# 5) 预提交 → ★ 用户确认 → 确认提交
pre = client.pre_create_order(
    receiver_id=receiver["ReceiverId"],
    cost_center_id=cost_center["CostCenterId"],
    items=items,
)
guid = pre["Data"]["Message"]

# ⚠️ 强制：展示订单信息后等待用户输入 y，再调用 confirm_order
confirm = client.confirm_order(guid=guid)
print("SoId:", confirm.get("Data", {}).get("SoId"))
```

> ⚠️ `client.quick_order(...)` 会跳过用户确认环节，**仅供自动化测试 / 内部脚本**，正式 Agent 流程不要直接使用。

### curl 命令调用

```bash
# 1. 登录
curl -X POST 'https://h5vip.colipu.com/api/vip/login' \
  -H 'content-type: application/json;charset=UTF-8' \
  -d '{"loginName":"${COLIPU_LOGIN_NAME}","pwd":"${COLIPU_PASSWORD}","cleartext":"Y","hasMobileLogin":false,"scene":"h5"}'

# 2. 搜索商品（${EGG_SESS} 取自第 1 步响应头 Set-Cookie；${CUSTOMER_ID} 取自第 1 步响应 Data.customerId）
curl -X POST 'https://h5vip.colipu.com/api/b2bSearchApi/SearchByKeyWord' \
  -H 'Cookie: EGG_SESS=${EGG_SESS}' \
  -H 'content-type: application/json;charset=UTF-8' \
  -d '{"siteId":211,"warehouseIds":[111],"keyWord":"a4","pageIndex":1,"pageSize":20,"provinceId":2,"consumer":{"customerId":${CUSTOMER_ID}}}'
```