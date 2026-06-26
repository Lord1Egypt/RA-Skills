# ClawClau 参考：Schema 与状态

## 注册表字段说明（active-tasks.json）

```json
{
  "id":           "任务唯一 ID",
  "mode":         "print | steerable",
  "tmuxSession":  "cc-{id}",
  "prompt":       "完整 prompt",
  "workdir":      "工作目录",
  "log":          "日志文件路径",
  "model":        "模型名称（空=默认）",
  "startedAt":    1234567890000,
  "timeout":      600,
  "interval":     180,
  "status":       "running | done | failed | timeout | killed",
  "completedAt":  null,
  "maxRetries":   3,
  "retryCount":   0,
  "parentTaskId": null,
  "steerLog":     []
}
```

## 任务状态流转

```
running
  → done        (session 结束，日志非空)
  → failed      (session 结束，日志为空)
  → timeout     (超过 --timeout 秒)
  → killed      (手动 claude-kill.sh)
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CC_HOME` | `~/.clawclau` | 数据目录（注册表、日志、prompts、config）|
| `CC_NOTIFY_CHAT` | `""` | 飞书群 open_chat_id，覆盖 config 文件中的 notify_chat |
