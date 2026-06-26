# Session Hygiene

## Problem

长期运行的 execution harness 积累大量残留状态：过期的 ralph.json（crash 后遗留）、orphaned lock 文件（agent 退出时未清理）、stale session 目录（已完成但未删除的 session 数据）、废弃的 worktree（multi-agent 后未清理）。这些残留状态浪费磁盘空间，更严重的是可能干扰新 session——比如 crash recovery 误识别 stale ralph 为可恢复状态。

## Solution

定期运行清理脚本，识别并清理 4 类残留状态。清理策略基于时间阈值和状态一致性检查：超过 TTL 的状态文件标记为过期，不一致的 lock 标记为 orphaned。清理前记录日志，支持 dry-run 预览。

## Implementation

1. 清理脚本 `session-cleanup.sh`

```bash
#!/bin/bash
DRY_RUN=${1:-false}
CLEANED=0

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1"; }
cleanup() {
  if [ "$DRY_RUN" = "true" ]; then
    log "DRY-RUN: would remove $1"
  else
    rm -rf "$1" && log "Removed: $1"
    CLEANED=$((CLEANED + 1))
  fi
}

# 1. Stale ralph 状态（>24h 且 active=true）
for F in sessions/*/ralph.json; do
  [ -f "$F" ] || continue
  ACTIVE=$(jq -r '.active // false' "$F")
  [ "$ACTIVE" = "true" ] || continue
  AGE_MIN=$(( ($(date +%s) - $(stat -f %m "$F" 2>/dev/null || stat -c %Y "$F" 2>/dev/null || echo 0)) / 60 ))
  if [ "$AGE_MIN" -gt 1440 ]; then
    log "Stale ralph: $F (${AGE_MIN}min old)"
    jq '.active = false | .deactivation_reason = "hygiene_cleanup"' "$F" > "${F}.tmp" && mv "${F}.tmp" "$F"
    CLEANED=$((CLEANED + 1))
  fi
done

# 2. Orphaned lock 文件（>30min）
find .claims -name "*.lock" -mmin +30 2>/dev/null | while read F; do
  log "Orphaned lock: $F"
  cleanup "$F"
done

# 3. 空 session 目录（只有 .recovery-checked，无其他文件）
for D in sessions/*/; do
  [ -d "$D" ] || continue
  FILE_COUNT=$(find "$D" -type f ! -name ".recovery-checked" | wc -l)
  if [ "$FILE_COUNT" -eq 0 ]; then
    log "Empty session dir: $D"
    cleanup "$D"
  fi
done

# 4. Stale worktree（git worktree list 中存在但目录已删除的）
git worktree list --porcelain 2>/dev/null | grep '^worktree ' | awk '{print $2}' | while read WT; do
  if [ ! -d "$WT" ]; then
    log "Stale worktree ref: $WT"
    [ "$DRY_RUN" = "true" ] || git worktree prune 2>/dev/null
  fi
done

log "Cleanup complete: ${CLEANED} items processed"
```

2. 推荐运行频率：每 4 小时或每次新 session 启动前

3. 可选：UserPromptSubmit hook 在 session 首次触发时运行轻量级清理

```bash
# 只清理与当前 session 相关的残留，不做全局清理
```

## Tradeoffs

- **Pro**: 防止残留状态积累导致的误识别和磁盘浪费
- **Pro**: Dry-run 模式允许在清理前预览将被删除的内容
- **Con**: 时间阈值是经验值——太短可能误清有用状态，太长清理不及时
- **Con**: 跨平台兼容性（macOS `stat -f %m` vs Linux `stat -c %Y`）需要处理

## Source

OMC 的 stale state threshold 机制（`STALE_STATE_THRESHOLD_MS`）。Unix 系统的 cron + logrotate 清理模式。Agent 特有的 orphaned lock 问题。
