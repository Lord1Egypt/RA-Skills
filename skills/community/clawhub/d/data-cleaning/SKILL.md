---
name: data-cleaning
description: "使用场景: 用户要求检查并按明确规则清洗 CSV/XLSX，先预览变更再确认执行时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.2.0",
        "openclaw": {
            "emoji": "🧹",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "DATA_CLEANING_API_KEY",
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
                    "name": "DATA_CLEANING_API_KEY",
                    "required": false,
                    "description": "AI Skills 平台数据清洗 API 密钥。"
                },
                {
                    "name": "AI_SKILLS_API_URL",
                    "required": false,
                    "description": "可选 API 根地址。"
                }
            ]
        }
    }
---

# 数据清洗

## Skill 简介

数据清洗 Skill 对 CSV/XLSX 做无损结构检查，保留原始行号、字面值、空白行与公式状态；清洗规则先生成逐项样本和影响数量，只有用户确认冻结预览后才执行并交付私有文件。同一快照与规则可复现，不让模型暗中改数。

## 平台入口与注册

1. 打开 [AI Skills 平台](https://ai-skills.open-idea.net/)，新用户进入 [注册页面](https://ai-skills.open-idea.net/register)，已有账号进入 [登录页面](https://ai-skills.open-idea.net/login)。
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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.DATA_CLEANING_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `DATA_CLEANING_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Agent 执行规则

1. 依次执行 `clean.inspect`（检查数据）、`clean.preview`（预览清洗）、`clean.execute`（确认执行）。
2. 规则必须结构化且明确；遇到含糊日期、公式或类型转换风险时停止并向用户确认，不自行猜测。
3. 向用户展示预览的规则、影响量和变更样本；仅在用户明确确认后提交平台返回的 `confirmation_token`，不得自行构造或修改令牌。
4. 结果以平台确定性计算为准；不得重新计算后覆盖行数、单元格数、规则摘要或校验和。

## 完成标准

- 异步任务轮询至终态，按来源任务链继续；七日后来源失效时重新检查文件。
- 网络结果不确定时复用相同 `Idempotency-Key`、UUID 和完全相同输入，不创建重复执行。
- 交付 `artifacts`、审计摘要、实际影响量与未处理风险；私有下载地址只提供给当前用户。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- [API 密钥配置与价格](https://ai-skills.open-idea.net/skill-docs/data-cleaning/API-KEY.md)
- [HTTP 请求、上传与任务轮询](https://ai-skills.open-idea.net/skill-docs/data-cleaning/HTTP-REQUESTS.md)
- [操作字段与清洗规则](https://ai-skills.open-idea.net/skill-docs/data-cleaning/OPERATIONS.md)
- [安全、确认与结果解释规则](https://ai-skills.open-idea.net/skill-docs/data-cleaning/BEHAVIOR-RULES.md)
