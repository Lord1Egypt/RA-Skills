---
name: 1688-88syt
description: 线下B2B交易的得力帮手，一句话搞定全流程操作！无论您是卖家还是买家，只需一句指令，即可轻松完成电子合约（采购单/合同）创建、签署、确认收货、退款等核心操作，全面支持账号状态查询、实名认证、绑卡及交易，让每一步交易流程更清晰、更可控。通过智能化交互，实现交易流程数字化，提升协作效率，保障资金流转安全，助力企业高效运营。专注每一次B2B交易，让生意更稳、更快、更省心！。用户提到 88 生意通、采购单、签署、退款、确认收货、大额、批量、实名、绑卡、主账号、卖家或买家问题时使用。
metadata: {"openclaw": {"emoji": "📋", "requires": {"bins": ["python3"]}, "primaryEnv": "SYT_API_KEY"}}
---

# 88生意通-1688线下交易工具

统一入口：`python3 {baseDir}/cli.py <command> [options]`

## 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `account` | 查询账号状态 | `cli.py account` |
| `contract-list` | 查询采购单列表 | `cli.py contract-list --role BUYER --page 1 --size 10` |
| `contract-detail` | 查询采购单详情 | `cli.py contract-detail --draft-no 88SYT20260324419012` |
| `contract-summary` | 查询采购单汇总 | `cli.py contract-summary` |
| `create-order` | 创建采购单 | `cli.py create-order --role BUYER --counterparty "对方登录名" --items '[{"productName":"商品","quantity":10,"unitPrice":"1.00"}]'` |
| `sign-order` | 签署采购单 | `cli.py sign-order --draft-no 88SYT20260324419012` |
| `sign-reject` | 拒绝签署 | `cli.py sign-reject --draft-no 88SYT20260324419012` |
| `confirm-receipt` | 确认收货 | `cli.py confirm-receipt --draft-no 88SYT20260324419012` |
| `invalidate-order` | 采购单失效 | `cli.py invalidate-order --draft-no 88SYT20260324419012` |
| `refund-apply` | 申请退款 | `cli.py refund-apply --draft-no 88SYT20260324419012` |
| `configure` | 配置 AK | `cli.py configure YOUR_AK` |
| `check` | 检查配置状态 | `cli.py check` |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`
**展示时直接输出 `markdown` 字段，Agent 分析追加在后面，不得混入其中。**

## 使用流程

Agent 根据用户意图**直接执行对应命令**，无需每次先执行 `check`。
各命令在 AK 缺失、账号状态异常等情况下会自行返回明确错误，Agent 按下方「异常处理」应对即可。

**采购单典型路径**：`account`（检查准入）→ `create-order`-> `sign-order`(买家签署) → `contract-detail`（确认状态）

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **只读** | account, contract-list, contract-detail, contract-summary, check | 直接执行 |
| **配置** | configure | 提示影响范围后执行 |
| **写入** | create-order, sign-order, sign-reject, confirm-receipt, invalidate-order, refund-apply | **必须先确认用户意图；涉及资金/状态变更的操作须二次确认** |

**全局写入规则（适用于所有写操作）**：
1. 必须先确认用户明确意图。
2. 涉及资金（退款、确认收货）或状态变更（失效、拒绝签署）的操作，须向用户**二次确认**后再执行。
3. 操作成功后，建议调用 `contract-detail` 查询最新状态反馈用户。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效"/"401" | 输出下方 **AK 引导话术** |
| "非主账号" / "NOT_1688_MAIN_ACCOUNT" | 引导用户使用主账号操作，或前往网页端 |
| "未签约" / "未实名" / "未绑卡" | 引导用户前往 [88生意通页面](https://syt.1688.com/page/SYT/buyer?tracelog=88sytskill) 完成相关操作 |
| "限流"/"429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |

## AK 引导话术

> "需要先配置 AK 才能使用 88 生意通功能。请登录 [ClawHub](https://clawhub.1688.com/)，点击右上角钥匙按钮获取 AK，然后告诉我：'我的AK是 xxx'"

## 执行前置（首次命中能力时必须）

- 首次执行 `account` 前：先完整阅读 `references/capabilities/account.md`
- 首次执行 `contract-list` 前：先完整阅读 `references/capabilities/contract-list.md`
- 首次执行 `contract-detail` 前：先完整阅读 `references/capabilities/contract-detail.md`
- 首次执行 `contract-summary` 前：先完整阅读 `references/capabilities/contract-summary.md`
- 首次执行 `create-order` 前：先完整阅读 `references/capabilities/create-order.md`
- 首次执行 `sign-order` 前：先完整阅读 `references/capabilities/sign-order.md`
- 首次执行 `sign-reject` 前：先完整阅读 `references/capabilities/sign-reject.md`
- 首次执行 `confirm-receipt` 前：先完整阅读 `references/capabilities/confirm-receipt.md`
- 首次执行 `invalidate-order` 前：先完整阅读 `references/capabilities/invalidate-order.md`
- 首次执行 `refund-apply` 前：先完整阅读 `references/capabilities/refund-apply.md`
- 同一会话内后续重复调用同一能力可复用已加载知识；仅在规则冲突或文档更新时重读。

## 通用规则（必读）

执行任何业务前，完整阅读并遵守 [references/common-rules.md](references/common-rules.md)。其中对 **网关域名**、**固定入参**、**对客中文**、**不暴露请求**、**外链 tracelog**、**免责声明**、**高风险二次确认**、**主账号/仅采购单/仅银行卡转账** 等为**硬性要求**，不得自行发挥省略。

## 业务限制

| 限制项 | 说明 |
|-------|------|
| 账号类型 | **仅支持主账号**，子账号引导至网页端操作 |
| 交易方式 | **仅支持采购单**，合同类交易引导至网页端 |
| 支付方式 | 支付等引导至网页端 |
| 角色说明 | 卖家与商家指同一角色 |

## 免责声明

每次回答末尾增加：

> 以上信息根据当前查询结果整理，具体以 88 生意通页面及银行/平台实际处理为准。若与您页面不一致，请以页面展示为准。
