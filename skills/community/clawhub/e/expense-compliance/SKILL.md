---
name: expense-compliance
description: "使用场景: 用户要求按其报销制度审核票据、检查重复并导出带证据的合规建议时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.2.0",
        "openclaw": {
            "emoji": "🧾",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "EXPENSE_COMPLIANCE_API_KEY",
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "EXPENSE_COMPLIANCE_API_KEY",
                    "required": false,
                    "description": "兼容产品专用 Key；设置时优先使用。"
                }
            ],
            "requires": {
                "bins": ["curl"]
            }
        }
    }
---

# 报销合规审核

## Skill 简介

报销合规审核 Skill 先识别发票、收据、行程单或客票，再依据用户创建的版本化制度执行金额、附件、币种、票据日期、禁用商户和历史重复检查。结果保留制度版本、票据来源任务、规则 ID 与证据，只提供审核建议，不代表付款批准、官方发票验真或舞弊认定。

## 平台入口与注册

1. 打开 [AI Skills 平台](https://ai-skills.open-idea.net/)，新用户可进入 [注册页面](https://ai-skills.open-idea.net/register)，已有账号进入 [登录页面](https://ai-skills.open-idea.net/login)。
2. 登录后进入 [产品管理](https://ai-skills.open-idea.net/dashboard/products) 开通本 Skill，再到 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys) 创建密钥。

## Skill 安装与配置

当前控制台直接创建通用 Key，无需选择产品；每个账号最多保留一把未撤销的通用 Key，已有时直接复制复用，更换时先撤销旧 Key。下列产品选择说明适用于旧版控制台。

1. 在 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys)中选择已开通的产品，创建并复制 API 密钥。
2. 在 OpenClaw 中安装本 Skill。
3. 将复制的密钥配置到本 Skill 的 API 密钥环境变量，然后重启 Gateway：

```sh
openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"
openclaw gateway restart
```

推荐创建账号通用 Key，以上全局变量只需配置一次即可供各 Skill 使用；仍需在产品管理中开通目标产品。原有产品专用 Key 仅能调用对应产品。

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.EXPENSE_COMPLIANCE_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `EXPENSE_COMPLIANCE_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Agent 执行规则

1. 首次使用先通过 `policy.create`（创建报销制度）建立结构化制度；制度更新必须提供当前 `expected_version`（预期版本），历史审核继续保留原规则快照。
2. 每张票据先调用 `receipt.extract`（识别票据），持续轮询到成功终态；向用户展示低置信度字段并要求核对，不得自行补造票号、日期、销售方或金额。只有用户明确表示已对照原图核验后，才能把对应任务 ID 放入 `confirmed_receipt_task_ids`（已人工核对确认的票据任务 ID）。
3. 收集成功 OCR（文字识别）任务 ID 后调用 `claim.audit`（审核报销申请）。`confirmed_receipt_task_ids`（已人工核对确认的票据任务 ID）必须是本次 `receipt_task_ids`（本次审核引用的票据任务 ID 列表）的子集；金额、规则命中与重复检测结果以平台返回为准，不得使用模型重新计算、覆盖置信度或冒充用户确认。
4. `non_compliant`（不合规）表示命中拒绝级规则，`manual_review`（需人工复核）表示仍需人工核对，`compliant`（符合已配置规则）仅表示未命中已配置规则；三者都不是付款批准。
5. 不宣称完成税务机关验真，不把“疑似重复”表述为舞弊，不执行付款、退款、报销审批或财务系统写入。

## 完成标准

- 在用户已授权范围内完成请求；收到异步任务时持续轮询任务状态，按 HTTP-REQUESTS.md 的终态与等待上限停止。未规定上限时，开始轮询前设定有限等待预算；超时保留任务 ID、最后状态与查询方式，不宣称成功或失败、不重复提交。
- 429/503 等可恢复错误按参考规则有限退避；同一逻辑请求复用原 `Idempotency-Key` 和相同输入。结果不确定或规则要求人工核对时停止自动重试；已授权范围内的安全续查无需重复确认。
- 多文件或多步骤任务完成后逐项交付结果；部分失败、仍在处理或等待人工核对的项目分别说明，并给出下一步。
- 多票据审核须先完成全部识别并核对低置信度字段，再提交审核；未完成的识别或人工核对不能被跳过。
- 最终说明制度版本、审核结果、各项发现、证据和限制，不把审核建议描述为已批准付款。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- 首次配置或排查鉴权时：[API 密钥配置](https://ai-skills.open-idea.net/skill-docs/expense-compliance/API-KEY.md)
- 调用 API 前，确认请求、响应与重试规则：[HTTP 请求、幂等与轮询](https://ai-skills.open-idea.net/skill-docs/expense-compliance/HTTP-REQUESTS.md)
- 选择当前操作后，查其字段与结果：[操作、规则与结果结构](https://ai-skills.open-idea.net/skill-docs/expense-compliance/OPERATIONS.md)
- 执行前，确认本次授权、安全与结果解释边界：[证据、安全与人工复核规则](https://ai-skills.open-idea.net/skill-docs/expense-compliance/BEHAVIOR-RULES.md)
