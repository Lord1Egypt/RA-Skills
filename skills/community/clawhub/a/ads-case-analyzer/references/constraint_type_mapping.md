# constraint_type → 实际转化字段映射

## 字段映射表

| constraint_type | 含义 | 实际转化字段 | 备注 |
|----------------|------|------------|------|
| 60 | 下载按钮点击 | `app_download_button_click_cnt` | |
| 61 | 激活 | `app_activate_cnt` | |
| 62 | 注册 | `app_register_cnt` | |
| 63 | 关键行为 | `app_key_action_cnt` | |
| 64 | app付费 | `app_pay_cnt` | |
| 65 | 小程序打开 | `app_invoke_cnt` | |
| 67 | 小程序付费 | `mini_apps_payment_cnt` | |
| 69 | 预约下载按钮点击 | `app_subscribe_button_click_cnt` | |
| 72 | 预约表单提交 | `leads_cnt` | |
| 73 | 微小打开 | `app_invoke_cnt` | optimize_target=73 区分小程序(65) |
| 74 | 微小激活 | `app_activate_cnt` | optimize_target=74 区分激活(61) |
| 75 | 微小付费 | `app_payment_cnt` | |
| 48 | 下载24hROI | TBD | |
| 49 | 小程序24hROI | TBD | |

## 使用说明

1. **通过 optimize_target 区分字段重叠场景**：
   - `app_invoke_cnt`：constraint_type=65（小程序打开）vs constraint_type=73（微小打开），靠 `optimize_target` 区分
   - `app_activate_cnt`：constraint_type=61（激活）vs constraint_type=74（微小激活），靠 `optimize_target` 区分
   - **查询时务必同时过滤 `optimize_target`，不能只过滤 `constraint_type`**

2. **保浅优深计划**（`constraint_type ≠ optimize_target`）：
   - 实际转化字段跟 `constraint_type` 走（客户出价的浅层目标）
   - PAOA 也用 `constraint_type_pcvr` 计算

## PAOA 计算口径

**PAOA = 预估转化数 / 实际转化数**（目标值 → 1）

预估转化数计算规则（按 placement 区分）：
- `placement IN (1, 2)`（展示/搜索）：`SUM(constraint_type_pcvr × click_cnt)`
- `placement = 7`（内流）：`SUM(constraint_type_pcvr × imp_cnt)`

实际转化数：根据上方映射表，按 `constraint_type` 取对应字段的 SUM。

**示例**（constraint_type=61，激活）：
```sql
SUM(CASE WHEN placement IN (1,2) THEN constraint_type_pcvr * click_cnt
         WHEN placement = 7      THEN constraint_type_pcvr * imp_cnt
         ELSE 0 END)
/ NULLIF(SUM(app_activate_cnt), 0) AS paoa
```
