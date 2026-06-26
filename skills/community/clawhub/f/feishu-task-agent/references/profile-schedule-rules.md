# 定时刷新规则

本规则不负责创建定时任务，只定义 profile / `daily.json` 刷新任务的执行语义、幂等规则与宿主要求。

每天 `23:30` 的 profile 定时任务由 [../workflows/reg.md](../workflows/reg.md) 的注册流程创建；任务触发后，必须按 [../workflows/agent-profile.md](../workflows/agent-profile.md) 执行。

## 刷新命令

在目标应用根目录执行以下命令，可以立即手动刷新一次：

```bash
python3 scripts/build_daily_json.py --app-root .
```

## 调度约束

- `23:30` 的 profile 刷新任务由注册流程统一创建，不由本规则重复注册
- 定时触发与手动补跑必须使用相同的生成语义
- 执行入口始终是 `feishu-task-agent` 路由到 `workflows/agent-profile.md`

## 幂等规则

- 每次执行都基于被选中的 Markdown 重新计算来源指纹
- 如果来源指纹和当前 `daily.json` 一致，只更新 `最后检查时间`
- 如果来源指纹发生变化，就用新的提炼结果覆盖 `daily.json`
- 如果还没有任何日报且 `daily.json` 也不存在，就先写一个空的初始化占位文件

## 宿主要求

- 必须从应用根目录执行命令，确保输出落到 `<应用根目录>/daily.json`
- 必须允许随时手动补跑
- 宿主只需要具备“按计划执行一条命令”的能力
- 如果重复注册同名 cronjob，宿主侧应先检查或手动清理，避免出现重复任务
