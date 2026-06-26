# get_cluster_marketing_plan

查询指定客群的运营方案，包含触达方式、优惠券配置、推荐商品、营销文案、海报链接。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 必须先有 planId（来自 `list_customer_cluster` 返回的 `plan_id`）

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| plan_id | string | 是 | 客群计划 ID（来自 `list_customer_cluster` 返回的 `plan_id`）|

## 返回字段

`data` 为 null 时表示该客群暂无运营方案；否则包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| plan_id | string | 客群计划 ID |
| buyer_num | int | 运营方案覆盖买家数 |
| ignored_buyer_num | int | 豁免买家数（不参与触达）|
| reach_type | int | 触达方式编码 |
| reach_type_list | list | 触达方式列表 |
| coupon_name | string | 优惠券名称 |
| coupon_type | int | 优惠券类型 |
| coupon_first_value | int | 满减门槛（分）|
| coupon_second_value | int | 优惠金额（分）|
| sale_description | string | 营销文案 |
| poster_url | string | 海报图片链接 |
| offer_list | array | 推荐商品列表 |
| offer_list[].offer_id | long | 商品 ID |
| offer_list[].offer_name | string | 商品名称 |
| offer_list[].offer_url | string | 商品主图 |
| offer_list[].price | string | 商品价格 |

## 典型用法

```bash
# 先查客群列表获取 plan_id
python cli.py list_customer_cluster

# 再查该客群的运营方案
python cli.py get_cluster_marketing_plan --plan-id "xxx_plan_id"
```

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "...",
  "data": { "plan_id": "...", "buyer_num": 100, "coupon_name": "...", ... }
}
```

### 失败

```json
{
  "success": false,
  "markdown": "错误描述信息"
}
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| plan_id 无效 | 提示用户核对 plan_id |
| 该客群暂无运营方案（data=null） | 告知用户需先在 CRM 页面创建运营方案 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
