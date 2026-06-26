# Pattern 4: Rate Limit 检测与恢复

## 问题

Agent 在 tmux session 中遇到 API 限速后会挂在那里等待，但没有自动恢复机制。限速解除后需要人工去 tmux 里按回车。

## 原理

周期性扫描 tmux pane 内容，检测限速关键词。限速解除后发送按键恢复。来自 OMC 的 `rate-limit-wait/daemon.js`——一个后台 daemon，轮询 API usage endpoint + 扫描 tmux pane，自动恢复。

## 检测

```bash
# 扫描所有 Claude Code tmux 会话
tmux list-panes -a -F '#{session_name} #{pane_id}' | while read sess pane; do
  tail=$(tmux capture-pane -t "$pane" -p -S -20 2>/dev/null)
  if echo "$tail" | grep -qiE 'rate.?limit|429|too many requests|usage limit'; then
    echo "$sess:$pane:limited"
  fi
done
```

## 恢复

**WARNING: 盲发 Enter 到 tmux pane 是危险的。** 如果 pane 当前显示的是破坏性确认提示（"Delete all files? [y/N]"），Enter 会确认操作。

安全恢复流程：
```bash
# 1. 再次捕获 pane 内容，确认最后几行仍然是限速消息
tail=$(tmux capture-pane -t "$pane" -p -S -5 2>/dev/null)
if echo "$tail" | grep -qiE 'rate.?limit|too many requests|usage limit'; then
  # 2. 确认不是确认提示
  if ! echo "$tail" | grep -qiE '\[y/N\]|\[yes/no\]|confirm|delete|overwrite|force push'; then
    tmux send-keys -t "$pane" "" Enter
  fi
fi
```

不要直接 `tmux send-keys Enter`，MUST 先验证 pane 当前内容。

## OMC 的完整方案（参考）

OMC 的实现更完善，包含 5 个组件：

1. **Rate Limit Monitor** (`rate-limit-monitor.js`)：调用 Claude Code 的 OAuth API 获取 usage 数据，检查 5 小时/周/月 三个窗口。返回 `RateLimitStatus` 包含 `isLimited`、`nextResetAt`、`timeUntilResetMs`。

2. **Tmux Detector** (`tmux-detector.js`, 10KB)：不只检测关键词，还有置信度评分：
   - `hasClaudeCode`: pane 里是否运行着 Claude Code
   - `hasRateLimitMessage`: 是否有限速消息
   - `isBlocked`: 综合判断是否卡住
   - confidence score: 置信度

3. **Daemon** (`daemon.js`, 21KB)：后台轮询循环：
   - 默认 60 秒间隔检查限速状态
   - 扫描 tmux pane 找被阻塞的 session
   - 限速解除后通过 `tmux send-keys` 恢复
   - 追踪 `blockedPanes`、`resumedPaneIds`、成功/失败计数
   - PID 文件单实例强制

4. **Stale Data Handling**：当 usage API 本身返回 429 时，使用缓存数据并标记 `usingStaleData: true`

5. **State 持久化**：写入磁盘（权限 0o600），包含所有追踪数据

## 简化版 vs OMC 完整版

| 方面 | 简化版（本 skill） | OMC 完整版 |
|------|-------------------|-----------|
| 检测方式 | grep 关键词 | API + 关键词 + 置信度 |
| 恢复方式 | 发送 Enter | 等限速解除后发送 Enter |
| 运行方式 | cron / 手动执行 | 后台 daemon + PID 锁 |
| 状态追踪 | 无 | 完整的 blocked/resumed 追踪 |
| 适用场景 | 1-4 个 session | 大规模并行 session |
