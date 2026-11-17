---
name: dataify-task-status
description: 根据任务 ID 查询 Dataify scraper 异步任务状态。用户提供 Dataify Builder 任务 ID、询问抓取任务是否完成，或需要确认任务成功、处理中或失败时使用。
---

# Dataify 任务状态查询

通过已创建的任务 ID 查询 Dataify `/task_status` 接口。API Key 仅从 `DATAIFY_API_TOKEN` 环境变量读取，绝不输出。

## 工作流

1. 要求提供任务 ID；仅在上下文中的任务 ID 明确时复用。
2. 确认环境变量 `DATAIFY_API_TOKEN` 已设置；不要要求用户在聊天中粘贴 Key，也不要通过命令行传递 Key。
3. 运行 `scripts/get_task_status.py --task-id TASK_ID`。需要预览时使用 `--dry-run`，其输出会脱敏 API Key。
4. 根据响应中的 `data.status` 返回状态：`处理中` 或 `失败` 时返回状态；返回 `成功` 时，状态查询脚本会使用同一任务 ID 立即发送 `GET /download` 请求并输出 `type=json` 的结果。
5. 对失败或无权限响应，返回服务方错误并建议检查任务 ID 和账户权限；不要自动重试付费任务。

## 命令

```bash
python3 -X utf8 scripts/get_task_status.py --task-id "TASK_ID"
```

参数和响应详情见 `references/task_status_api.md`。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
