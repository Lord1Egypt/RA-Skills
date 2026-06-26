# customer_crowd_analysis

针对特定买家，输出跟进方案（分析原因/推荐策略/推荐商品/优惠券/话术）。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 必须先调 `list_customer_details` 获取买家 crowd_type，不可自行推断

## 参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| crowd_type | string | 是 | — | 流失买家/周期采购/询盘未成交/老客促活 |
| buyer_login_id | string | 是 | — | 买家 loginId（从 list_customer_details 返回） |
| ds | string | 否 | 昨日 | 数据日期 YYYYMMDD |

## 返回字段

正常时 `data` 包含：crowd_type / buyer_profile / analysis_reason / recommend_strategy / recommend_offers / recommend_coupons / chat_script

无数据时 `data.no_data_reason` 有值（其余字段仅含 crowd_type 和 buyer_profile）。

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "...",
  "data": { "crowd_type": "...", "buyer_profile": "...", "analysis_reason": "...", "recommend_strategy": "...", "recommend_offers": [...], "recommend_coupons": [...], "chat_script": "..." }
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
| `crowd_type` 不在枚举 | 提示使用合法的 crowd_type 值 |
| `buyer_login_id` 为空 | 提示传入有效的 buyer_login_id |
| loginId 解析失败 | 账号未找到，提示用户核对 loginId |
| 底表无数据 | success=true，data.no_data_reason 有值 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
