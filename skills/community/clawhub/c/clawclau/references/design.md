# ClawClau 参考：设计原则与机制

## 设计原则（来自 Elvis 架构）

1. **确定性监控**：tmux 存活 + 日志文件检查，不靠 AI 轮询
2. **隔离执行**：每个任务独立 tmux session，互不干扰
3. **双重 fork 脱离进程树**：后台完成检测器通过 `((...) &) & disown` 模式被 launchd 接管，不受 spawn 进程退出影响
4. **stream-json 日志**：实时写入，可提取中间进度
5. **飞书直发通知**：cc_notify 优先通过飞书 API 直发群，无需 system event 中转
6. **小八主导重试**：失败通知小八，由小八决策 prompt 如何改进

## 通知机制（cc_notify）

`cc_notify` 按以下优先级发送通知：

1. **飞书群直发**（优先）：读取 `CC_NOTIFY_CHAT` 环境变量或 `~/.clawclau/config` 的 `notify_chat` 字段，调用 `openclaw message send --channel feishu --target <chat>` 直发群消息
2. **openclaw system event**（回退）：未配置 `notify_chat` 时，使用 `openclaw system event --text "$text" --mode now`

配置：

```ini
# ~/.clawclau/config
notify_chat = oc_xxxxxxxx   # 飞书群的 open_chat_id
```

或环境变量：`export CC_NOTIFY_CHAT="oc_xxxxxxxx"`

## 重试流程

ClawClau 不自动重试——失败后由小八决策是否重试、如何改进 prompt：

```
任务失败
  → 小八收到 cc_notify 通知（飞书群或 system event）
  → 小八分析失败原因，改进 prompt
  → 小八调用 claude-spawn.sh 派发重试任务（--parent 指向原任务）
  → 注册表记录 parentTaskId + retryCount，最多 maxRetries 次
```

重试命令示例：

```bash
# 失败任务: my-task（retry 0）
$SCRIPTS/claude-spawn.sh my-task-retry-1 "改进后的 prompt..." . \
  --parent my-task --retry-count 1 --max-retries 3
```

## 两种运行模式

| 模式 | 命令 | 日志格式 | 支持 steer | 适用场景 |
|------|------|----------|-----------|---------|
| Print（默认）| `claude -p --output-format stream-json` | `.json` | 否 | 任务明确，一次完成 |
| Steerable | `claude --dangerously-skip-permissions` | `.txt` | 是 | 探索性任务，需中途纠正 |
