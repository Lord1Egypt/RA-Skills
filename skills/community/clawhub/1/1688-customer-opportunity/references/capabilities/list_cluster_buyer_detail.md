# list_cluster_buyer_detail

查询指定客群中所有买家的明细数据，以 **markdown 表格**（可直接粘贴到 Excel）展示，包含买家等级、加入时间等字段。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 必须先有 planId（来自 `list_customer_cluster` 返回的 `plan_id`）

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| plan_id | string | 是 | 客群计划 ID（来自 `list_customer_cluster` 返回的 `plan_id`）|

## 返回字段

`data` 包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| plan_id | string | 客群计划 ID |
| buyer_count | int | 买家总数 |
| list | array | 买家明细列表 |
| list[].user_id | long | 买家 userId |
| list[].buyer_login_id | string | 买家 loginId（账号名）|
| list[].buyer_credit_level | string | 买家等级 |
| list[].add_date | string | 加入客群日期（yyyyMMdd）|

## 典型用法

```bash
# 先查客群列表获取 plan_id
python cli.py list_customer_cluster

# 再查该客群的买家明细
python cli.py list_cluster_buyer_detail --plan-id "xxx_plan_id"
```

## 数据用途

- `buyer_login_id`：可用于在旺旺中搜索联系买家
- 若需要买家画像与跟进建议，可配合 `1688-buyer-batch-profile` 的 `batch_reception_advice` 使用

## 输出格式

markdown 为 **标准表格格式**（可粘贴到 Excel/WPS），前 10 名买家用表格展示，后续买家从 `data` 导出：

| # | 买家账号 | 等级 | 加入时间 |
|---|---------|------|---------|
| 1 | login_id | L3 | 20260429 |
| ... | ... | ... | ... |

### 成功

```json
{
  "success": true,
  "markdown": "表格 markdown...",
  "data": { "plan_id": "...", "buyer_count": 100, "list": [...] }
}
```

> `data.data.list` 含全部买家，导出 Excel 时从此数组取，**不取 markdown 的前 10 名**。

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
| buyer_count = 0 | 该客群暂无买家数据，可能数据尚未同步 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
