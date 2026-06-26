# customer_reception_advice

实时客户接待画像 + 跟进建议（线上场景）。**统一对象数组入口**，每个对象通过字段名声明类型（`login_id` 或 `phone`），Java 端自动识别并转 userId，底层并发处理。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 主账号 userId 由后端通过 AK 自动解析，无需传参

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--buyers` | JSON 对象数组 | 是 | 买家对象数组，每个对象含 `login_id` 或 `phone` 字段（二选一）。一手机号可能对应多账号，会拆成多条结果。 |

**示例**：

```bash
# 全 loginId
python cli.py customer_reception_advice --buyers '[{"login_id":"alice"},{"login_id":"bob"}]'

# 全 phone
python cli.py customer_reception_advice --buyers '[{"phone":"13800138000"},{"phone":"13900139000"}]'

# loginId + phone 混合
python cli.py customer_reception_advice --buyers '[{"login_id":"alice"},{"phone":"13800138000"}]'

# 单买家（仍走数组）
python cli.py customer_reception_advice --buyers '[{"login_id":"nick"}]'
```

## 返回字段

`data.results` 为数组，每项包含：

| 字段 | 说明 |
|------|------|
| `buyer_login_id` | 买家 loginId（phone 路径会反查得到，可能为 null） |
| `source` | 数据来源：`login_id` 或 `phone` |
| `input_value` | 本次解析使用的入参原值（loginId 或 phone，与请求对应） |
| `buyer_profile` | 算法生成的客户画像（可能为空字符串） |
| `follow_suggestion` | 算法生成的跟进建议（可能为空字符串） |
| `chat_history_count` | 本次拉取的聊天条数（近 4 天 / 最多 20 条 / 仅文本） |

顶层额外字段：

| 字段 | 说明 |
|------|------|
| `unresolved_login_ids` | 未能解析为有效买家身份的 loginId 列表（无数据时为 `[]`） |
| `unresolved_phones` | 未能匹配到买家的手机号列表（无数据时为 `[]`） |
| `invalid_entries` | 既无 `login_id` 也无 `phone` 字段的非法对象（JSON 字符串列表） |

## 状态说明

- `buyer_profile` 或 `follow_suggestion` 至少一个非空 → 正常
- 两者均为空 → TPP 未生成，静默降级

## 与 customer_crowd_analysis 的差异

| 维度 | customer_reception_advice（线上） | customer_crowd_analysis（线下） |
|---|---|---|
| 数据源 | 旺旺实时聊天 + TPP 推理 | Lindorm 算法底表 T+1 |
| 适用场景 | 商家正在与买家对话 / 实时接待 | 按人群批量挖掘后的客户跟进 |
| 时效 | 实时（含本次会话） | 昨日数据 |

## 展示规则

- **批量 <= 5 人**：Markdown 表格渲染（序号 / 账号 / 画像 / 跟进建议）
- **批量 > 5 人**：引导导出 Excel，先展示结果概览表（序号 / 账号 / 状态），告知从 `data.results` 提取完整数据
- 顶层 `unresolved_login_ids` / `unresolved_phones` / `invalid_entries` 非空时，必须在结果末尾告知用户哪些条目失败

## 错误处理

- `--buyers` 为空 / 不是数组 / 元素不是对象 → 参数错误提示
- 元素既无 `login_id` 也无 `phone` → 该对象进入顶层 `invalid_entries`，不阻断其他条目处理
- TPP 异常 / 聊天拉取异常 → 静默降级（已被 service 层 catch，返 success + 空字段）
- loginId / phone 解析失败 → 不在 `results` 中，分别放入顶层 `unresolved_login_ids` / `unresolved_phones`

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
