# Workflow: 应用画像与 `daily.json`

## Overview

本工作流负责在目标应用根目录中找到最新日报 Markdown，提炼成稳定的 `daily.json`。若由注册流程创建的 `23:30` 定时任务触发，也必须按本工作流执行。

## When to Use

当请求命中以下任一情况时进入本工作流：

- 要求生成、刷新或更新 `daily.json`
- 要求从当前应用中的最新日报提炼“近期要点”和“明日关注”

## Workflow

1. 运行 `python3 scripts/build_daily_json.py --app-root .`
2. 写入完成后，调用工具 `feishu_task_agent`，执行 Action 为 `update_profile`，将生成的 `daily.json` 序列化内容作为参数 `profile_content` 写入飞书任务的智能体主页， 参数 `profile_content` 整个是一个 JSON 字符串，不是嵌套 JSON 对象。返回时明确告知本次操作的结果。


## References

- JSON 结构约定：读 [../references/profile-data-shape.md](../references/profile-data-shape.md)
- 发现与同日 tie-break 规则：读 [../references/profile-discovery-rules.md](../references/profile-discovery-rules.md)
- 执行时序与幂等规则：读 [../references/profile-schedule-rules.md](../references/profile-schedule-rules.md)
