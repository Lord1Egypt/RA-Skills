# 平台密钥与费用

## 配置与可用性

平台通用 `AI_SKILLS_API_KEY` 与 `COURSE_SUBTITLE_API_KEY` 二选一；优先产品变量，缺失回退通用变量，两者均缺失时停止调用。不要打印完整 Key，不要求用户粘贴 Key，不要求任何语音或模型上游 Key。本产品不支持用户 BYOK。

`AI_SKILLS_API_URL` 是站点根地址，默认 `https://ai-skills.open-idea.net`，不带 `/api/v1`；请求路径自行包含 `/api/v1/course-subtitle/…`。只向用户明确配置的平台域名发平台 Key，不转发到试听 URL 或其它服务。

必须先开通产品并具备对应 `subtitle.*` ability。平台初始关闭，由管理员验证依赖与授权样本后开放。遇到 `skill_not_active`、`user_skill_suspended`、`provider_not_configured` 或 `provider_unavailable` 如实报告，不能把夹具测试当成真实质量验收。

## 费用与授权

| 操作 | 计费口径 |
| --- | --- |
| `subtitle.inspect`、`subtitle.review`、`subtitle.export` | 免费 |
| `subtitle.transcribe` | 按选定单声道实际核验时长向上取整到秒；上游确认静音成功也按时长收费 |
| `subtitle.proofread` 的 `rules_only` | 免费、零 Token；只有确定性术语与规则检查 |
| `subtitle.proofread` 的 `model` | 按实际输入/输出 Token；不是固定每次价格 |

平台用人民币计费，MIT-0 安装许可与平台用量费独立。当前没有公开费用报价或余额查询 API；请用户提供当时工作台显示的单价、余额和可接受预算。不能为探价创建付费任务，不用代码默认值冒充实时报价。转写可根据预检的 `media.billing_seconds` 和用户提供的当前单价说明估算；模型校对说明实际 Token 结算，不能保证精确预估。

每次付费调用前展示项目 ID、当前项目版本、音轨/时长或字幕修订 ID、模式、发送内容和计费口径，取得用户针对该冻结输入的明确授权。此授权是用户交互记录；API 没有 `confirmation_token` 或付款确认字段，不构造额外 JSON 字段。输入或版本变化后重新展示并确认。

## 结算与未知状态

成功响应的 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance` 分别表示币种、该任务已扣金额和当前余额。异步以原任务最终状态和账单为准；202、处理中和暂时零扣费均不代表免费。

超时、`provider_outcome_unknown` 或 `reconciliation_required` 等上游/结算未知状态 时保存任务及原幂等键，查询原任务并交平台核对，不能换键、换 API Key 或重建项目再次调用来试探，也不自行承诺退款。取消和删除不保证上游在途任务停止或免单，按已处理结果核账。
