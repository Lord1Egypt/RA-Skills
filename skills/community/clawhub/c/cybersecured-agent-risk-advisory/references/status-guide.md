# 状态处理指南

> 当用户查询申请状态时，根据返回的状态给出对应的用户指引。在状态查询流程中按需阅读本文件。

---

## 状态速查表

| 状态 | 用户端显示 | Skill 响应 |
|------|-----------|-----------|
| `risk_assessed` | 风险评估完成 | 提示到网页端完成信息核实 |
| `questionnaire_filled` | 信息已预填 | 提示到网页端确认信息 |
| `plan_selected` | 服务方案已选择 | 提示确认服务方案并支付技术服务费 |
| `awaiting_payment` | 待支付 | 提示联系服务人员完成技术服务费支付 |
| `paid` | 已支付 | 提示等待后台处理 |
| `underwriting` | 处理中 | 告知后台正在协同处理 |
| `policy_uploaded` | 处理中 | 提示等待保障生效 |
| `activated` | 保障已生效 | 显示保障信息 |
| `refunding` | 退款中 | 提示后台正在处理退款 |
| `refunded` | 已退款 | 说明退款已完成，可重新发起服务申请 |
| `expired` | 已过期 | 提示重新申请 |
| `abandoned` | 已放弃 | 提示重新申请 |

## 状态分组（前端展示）

- **待处理**: `risk_assessed`, `questionnaire_filled`
- **待付款**: `plan_selected`, `awaiting_payment`
- **处理中**: `paid`, `underwriting`, `policy_uploaded`, `refunding`
- **已完成**: `activated`
- **历史**: `refunded`, `expired`, `abandoned`

## 服务方案代码映射

当 API 返回 `plan_code` 时，必须将其转换为中文名称展示给用户，**绝不允许直接显示代码**。

| 方案代码 | 中文名称 | 适用场景 |
|---------|---------|---------|
| `basic` | 基础计划 | 日常办公提效、个人学习 |
| `standard` | 专业计划 | 辅助客户服务、商业运营、企业内部管理 |
| `premium` | 高端计划 | 直接对客户提供服务、深度参与商业运营 |
| `enterprise` | 企业定制计划 | 高度定制业务流程、深度使用AI智能体 |

**展示规则**：
- 若 `plan_code` 为 `basic`，展示为"基础计划"
- 若 `plan_code` 为 `standard`，展示为"专业计划"
- 若 `plan_code` 为 `premium`，展示为"高端计划"
- 若 `plan_code` 为 `enterprise`，展示为"企业定制计划"
- 若 `plan_code` 为 `null`，展示为"尚未选择服务方案"

## 状态查询后的响应模板

根据状态返回对应的用户提示：

**risk_assessed**:
```
风险评估已完成。请访问 https://ai.cybersecured.cn 完成信息核实和服务申请流程。
```

**plan_selected**:
```
服务方案已选择：{plan_name}（如"基础计划"）。
请确认方案并完成技术服务费支付。
```

**awaiting_payment**:
```
请联系服务人员完成技术服务费支付。
```

**underwriting**:
```
后台正在协同处理开通流程，请耐心等待。
```

**activated**:
```
您的保障已生效，可在保障中心查看。
保障号：{policy_number}
服务方案：{plan_name}（如"基础计划"）
保障期限：{effective_date} 至 {expiry_date}
```

**refunded**:
```
退款已完成。如需继续使用，可重新发起服务申请。
```

---

*状态定义以本技能当前导出的状态说明与接口返回结果为准。*
