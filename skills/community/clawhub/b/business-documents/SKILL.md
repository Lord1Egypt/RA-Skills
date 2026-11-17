---
name: business-documents
description: "使用场景: 用户要求通过平台创建、修改或导出报价单、收款收据与送货单时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.4.0",
        "openclaw": {
            "emoji": "🧾",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "BUSINESS_DOCUMENTS_API_KEY",
            "requires": {
                "bins": ["curl"]
            },
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "BUSINESS_DOCUMENTS_API_KEY",
                    "required": false,
                    "description": "AI Skills 平台业务单据 API 密钥。"
                },
                {
                    "name": "AI_SKILLS_API_URL",
                    "required": false,
                    "description": "可选的自托管 API 根地址；未设置时使用官方平台。"
                }
            ]
        }
    }
---

# 业务单据

## Skill 简介

业务单据 Skill 用于根据用户提供的交易事实创建、读取、修改和导出报价单、收款收据与送货单，并生成结构化结果和私有 PDF。

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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.BUSINESS_DOCUMENTS_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `BUSINESS_DOCUMENTS_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Skill 使用

配置完成后，用户可以直接描述需要的单据和交易事实，例如：

- “为客户生成一份报价单，编号 QT-2026-001，包含两项服务，税率 6%。”
- “读取刚才的报价单，把第二项数量改为 3，并重新导出 PDF。”
- “根据这次收款信息生成收款收据。”

## 完成标准

- 在用户已授权范围内完成请求；收到异步任务时持续轮询任务状态，按 HTTP-REQUESTS.md 的终态与等待上限停止。未规定上限时，开始轮询前设定有限等待预算；超时保留任务 ID、最后状态与查询方式，不宣称成功或失败、不重复提交。
- 429/503 等可恢复错误按参考规则有限退避；同一逻辑请求复用原 `Idempotency-Key` 和相同输入。结果不确定或规则要求人工核对时停止自动重试；已授权范围内的安全续查无需重复确认。
- 多文件或多步骤任务完成后逐项交付结果；部分失败、仍在处理或等待人工核对的项目分别说明，并给出下一步。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- 首次配置或排查鉴权时：[API 密钥配置](https://ai-skills.open-idea.net/skill-docs/business-documents/API-KEY.md)
- 选择当前操作后，查其字段与结果：[操作契约](https://ai-skills.open-idea.net/skill-docs/business-documents/OPERATIONS.md)
- 调用 API 前，确认请求、响应与重试规则：[HTTP 请求与任务轮询](https://ai-skills.open-idea.net/skill-docs/business-documents/HTTP-REQUESTS.md)
- 执行前，确认本次授权、安全与结果解释边界：[行为与错误规则](https://ai-skills.open-idea.net/skill-docs/business-documents/BEHAVIOR-RULES.md)
