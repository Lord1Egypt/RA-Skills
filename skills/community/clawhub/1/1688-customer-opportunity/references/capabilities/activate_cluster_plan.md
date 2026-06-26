# activate_cluster_plan

开启 AI 客群运营计划。调用后端 HSF 接口（`ISmartCrmMarketingPlanService.insert`），成功后运营计划进入执行状态。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 必须先有 planId（来自 `list_customer_cluster` 返回）和旺旺文案（商家在 confirm_marketing_plan 确认）

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--plan-json` | string | 是 | JSON 字符串，包含运营计划全量字段（见下方字段表） |

## plan-json 字段

| 字段 | 类型 | 必填 | 来源 | 说明 |
|------|------|------|------|------|
| `planId` | string | 是 | `list_customer_cluster` → `plan_id` | 客群计划 ID |
| `planDs` | string | 是 | `list_customer_cluster` → `plan_ds` | 数据分区日期（yyyyMMdd） |
| `clusterMainTag` | string | 是 | `list_customer_cluster` → `cluster_main_tag` | 客群主标签 code |
| `buyerType` | string | 是 | 固定值 `"old"` | 买家类型 |
| `saleDescription` | string | 是 | `confirm_marketing_plan` 旺旺文案题答案 | 营销文案（后端必填） |

> `reachType`/`reachTypeList` 由后端写死为旺旺（1/[1]），无需传入。

## Agent 使用流程

1. 调 `get_cluster_marketing_plan --plan-id PLAN_ID` 获取推荐旺旺文案
2. 调用 `confirm_marketing_plan` input 交互，展示文案供商家确认或修改
3. 取商家答案作为 `saleDescription`，构造 plan-json 调 `activate_cluster_plan --plan-json '<JSON>'`
4. 命令返回后：读取结果中的 `crm_url`，以 `[CRM管理]({crm_url})` 格式展示给商家；若 `already_exists=true` 则说明计划已存在，同样展示 `crm_url`；**禁止调用 `open_tab`**，不自动打开任何页面

## 典型用法

```bash
# step1: 从 list_customer_cluster 获取 planId / clusterMainTag / planDs
python cli.py list_customer_cluster

# step2: 获取推荐旺旺文案
python cli.py get_cluster_marketing_plan --plan-id "ea29f9d0-..."

# step3: confirm_marketing_plan 交互让商家确认文案，取答案作为 saleDescription

# step4: 开启
python cli.py activate_cluster_plan --plan-json '{
  "planId": "ea29f9d0-415b-4962-b979-f303703bc3ba",
  "planDs": "20260427",
  "clusterMainTag": "purchase_preference",
  "buyerType": "old",
  "saleDescription": "26年纺织辅料代工老厂，支持小批量起订，快反供应，立即咨询获取专属方案。"
}'
```

## 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `crm_url` | string | CRM 管理页链接（含 showPlanId 参数），**必须展示给用户** |
| `already_exists` | bool | `true` 表示运营计划已存在，无需重复创建 |
| 其他字段 | - | 后端返回的激活结果 |

> ⚠️ **无论成功还是已存在，结果中都有 `crm_url`，agent 必须将其作为可点击链接展示给商家，禁止调用 `open_tab` 自动打开。**

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| `--plan-json` 非合法 JSON | 输出 `success:false`，提示 JSON 解析失败 |
| 必填字段缺失或为空字符串 | 输出 `success:false`，指出具体缺失字段名 |
| `reachTypeList` 不是列表 | 输出 `success:false`，提示类型错误 |
| AK 未配置 | 输出 `success:false`，引导 `cli.py configure YOUR_AK` |
| 后端返回业务错误 | 由 `_http.py` 映射为 `SkillError`，输出 `success:false` |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。

## 开启客群方案场景入参构造规则

> 「开启客群方案」分支专用——字段来源对应 confirm_marketing_plan 交互的 agent 取值。

| JSON 字段 | 来源 | 说明 |
|-----------|------|------|
| `planId` | `list_customer_cluster.plan_id` | 客群计划 ID |
| `planDs` | `list_customer_cluster.plan_ds` | 计划日期（yyyyMMdd） |
| `clusterMainTag` | `list_customer_cluster.cluster_main_tag` | 客群主标签 code |
| `buyerType` | 固定值 `"old"` | 买家类型 |
| `saleDescription` | `confirm_marketing_plan` 旺旺文案题答案 | 营销文案（**必传**） |

**构造约束：**
- `saleDescription` 禁止省略
- 所有 JSON key 必须是 **camelCase**（不是 snake_case）
- `reachType`/`reachTypeList` 由后端写死为旺旺，无需传入
- **禁止传任何 coupon 相关字段**（`couponName`/`couponType`/`startFee`/`discountFee`）
