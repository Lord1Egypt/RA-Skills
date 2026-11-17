---
name: course-subtitle
description: "使用场景: 课程媒体需要转写，或已有 SRT/VTT 需要文字、术语、可读性校对并人工确认后导出字幕时；讲稿与术语表可选。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.1.0",
        "openclaw": {
            "emoji": "📄",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "COURSE_SUBTITLE_API_KEY",
            "requires": {
                "bins": [
                    "curl"
                ]
            },
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "COURSE_SUBTITLE_API_KEY",
                    "required": false,
                    "description": "平台产品专用 Key。"
                },
                {
                    "name": "AI_SKILLS_API_URL",
                    "required": false,
                    "description": "可选站点根地址，不带 /api/v1。"
                }
            ]
        }
    }
---

# 课程字幕校对

## Skill 简介

课程媒体需要转写，或已有 SRT/VTT 需要文字、术语、可读性校对并人工确认后导出字幕时；讲稿与术语表可选。平台初始关闭，真实依赖与授权样本验收后由管理员开放；不可将夹具测试当成真实质量证明。

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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.COURSE_SUBTITLE_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `COURSE_SUBTITLE_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Agent 执行规则

先读取[操作字段](https://ai-skills.open-idea.net/skill-docs/course-subtitle/OPERATIONS.md)，按输入选择路径：

- 已有 SRT/VTT：创建项目 → 上传字幕 → `subtitle.inspect` → `subtitle.proofread` → 逐项人工 `subtitle.review` → `subtitle.export`。跳过 `subtitle.transcribe`；没有媒体不能声称已验证音频同步。
- 只有媒体：创建项目 → 上传媒体 → `subtitle.inspect` 核验音轨与时长 → 展示冻结输入、费用与传输范围并取得用户授权 → `subtitle.transcribe` → 校对、逐项人工确认、导出。多音轨先确认索引。
- 仅规则检查显式用 `rules_only`，免费且零 Token；模型校对用 `model`，按实际 Token 收费。讲稿和术语表缺失不阻断普通字幕校对，不要求用户为此补材料。

收费前按[费用规则](https://ai-skills.open-idea.net/skill-docs/course-subtitle/API-KEY.md)取得绑定当前版本的用户确认；没有公开报价 API，不提交付费任务探价。网络结果未知先查询原任务，保持原 Key、Idempotency-Key 和完全相同请求，不能另建收费任务。参考[请求与轮询](https://ai-skills.open-idea.net/skill-docs/course-subtitle/HTTP-REQUESTS.md)。

模型只提建议，不能代替用户逐条接受、拒绝、改字或接受提示。增讲不得按讲稿删除；不插值伪造字词时间锚点，无可靠锚点时保留待确认或草稿。具体权限与人工确认见[行为规则](https://ai-skills.open-idea.net/skill-docs/course-subtitle/BEHAVIOR-RULES.md)。

## 完成标准

交付字幕版本、实际收费、未决建议和质量限制，区分任务成功与字幕 `confirmed`；`draft` 只能标记草稿。导出 SRT、VTT、复核 JSON 报告，当前公共 API 只给产物元数据，用户登录工作台下载。不得伪造下载 URL 或自动发布、分享。

私有项目从创建起保留 30 天，派生修订不延期。仅处理用户授权且有权上传的文件；媒体、字幕、必要讲稿和术语传输前说明用途及平台语音/文字服务范围。敏感正文、密钥、试听令牌不写日志，不默认用于训练、演示或反馈。删除或到期后停止引用、试听与下载；批次逐课时独立计费恢复，取消后先核对在途状态。

## 参考资料

按任务读取：

- [平台密钥与费用](https://ai-skills.open-idea.net/skill-docs/course-subtitle/API-KEY.md)
- [上传、请求与轮询](https://ai-skills.open-idea.net/skill-docs/course-subtitle/HTTP-REQUESTS.md)
- [操作字段](https://ai-skills.open-idea.net/skill-docs/course-subtitle/OPERATIONS.md)
- [授权与人工确认](https://ai-skills.open-idea.net/skill-docs/course-subtitle/BEHAVIOR-RULES.md)
