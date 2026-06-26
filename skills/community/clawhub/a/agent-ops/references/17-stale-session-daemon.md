# Pattern 17: Stale Session Daemon（死 session 回收）

## 问题

Agent session 可能因为各种原因静默死亡——网络断开、进程被 kill、机器重启。此时 session 的 thinking blocks 和未保存的发现全部丢失，没有人知道它做到了哪里。

来源：`parcadei/Continuous-Claude-v3` — heartbeat + dead session scavenging

## 原理

每个 session 定期发送 heartbeat。当 heartbeat 超时（>5 分钟），后台 daemon 判定 session 死亡，然后：

1. 分析死 session 的 transcript 文件（特别是 thinking blocks，因为它们包含推理过程）
2. 提取未保存的发现和决策
3. 写入归档记忆文件
4. 标记 session 为已回收

## 与现有 Pattern 的关系

- Pattern 1 (Ralph) 有 2 小时闲置超时，但只是停止 ralph 循环——不会提取知识
- Pattern 8 (Compaction 提取) 在压缩前抢救知识——但只在 session 活着时工作
- Pattern 10 (三门控合并) 处理跨 session 碎片化——但前提是 handoff 已经被写入

Stale Session Daemon 填补的是"session 死亡时的知识抢救"这个空白。

## 实现

### Heartbeat 发送（PostToolUse hook，async）

```bash
# 每次工具调用后更新 heartbeat
date +%s > "sessions/${SESSION_ID}/heartbeat"
```

### Daemon（cron 或后台进程）

```bash
# 每分钟检查所有 session 的 heartbeat
NOW=$(date +%s)
for dir in sessions/*/; do
  SESSION=$(basename "$dir")
  HEARTBEAT_FILE="$dir/heartbeat"
  [ -f "$HEARTBEAT_FILE" ] || continue
  
  LAST=$(cat "$HEARTBEAT_FILE")
  AGE=$(( NOW - LAST ))
  
  if [ "$AGE" -gt 300 ]; then  # 5 分钟无心跳
    # 检查 tmux session 是否还在
    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
      # Session 已死，执行知识回收
      echo "Scavenging dead session: $SESSION (${AGE}s stale)"
      # 提取 transcript 中的关键信息
      # ...写入 sessions/$SESSION/handoffs/scavenged.md
      echo "scavenged" > "$dir/status"
    fi
  fi
done
```

## Tradeoff

- Heartbeat 增加微小的 I/O 开销（每次工具调用一次 write）
- Daemon 需要后台进程或 cron——不是零运维
- Transcript 分析需要 LLM 调用来提取有意义的信息（成本）
- 5 分钟阈值可能误判——网络慢导致 API 调用超过 5 分钟
