# Compaction Quality Audit

## Problem

Claude Code 的自动 compact 会丢失关键上下文。Compact 后 agent 可能忘记：已做的决策（重复讨论）、已排除的方案（又去尝试）、文件间的依赖关系（改了 A 忘了同步 B）。用户发现问题时往往已经浪费了大量 token 在错误方向上。

## Solution

Compact 完成后立即运行审计脚本，检查关键上下文是否在 compact summary 中存活。审计对照 `.working-state/decisions.jsonl` 中的关键决策和 `.harness-tasks.json` 中的任务状态，如果发现遗失则将缺失信息注入 context。

## Implementation

1. 通过 UserPromptSubmit hook 检测 compact 事件（transcript 中出现 compact 标记）
2. 读取 compact 后的 summary（transcript 尾部）
3. 对照 `.working-state/decisions.jsonl` 的最近 N 条决策
4. 检查关键信息是否在 summary 中出现

```bash
INPUT=$(cat)
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // ""')
[ -z "$TRANSCRIPT" ] && exit 0

# 检测是否刚发生 compact（简化检测：看 transcript 大小是否骤降）
DECISIONS_FILE=".working-state/decisions.jsonl"
[ -f "$DECISIONS_FILE" ] || exit 0

# 读取最近 5 条决策的关键词
KEYWORDS=$(tail -5 "$DECISIONS_FILE" | jq -r '.decision' | tr ' ' '\n' | sort -u | head -20)

# 读取 transcript 尾部（compact summary 区域）
SUMMARY=$(tail -c 4096 "$TRANSCRIPT" 2>/dev/null)

MISSING=""
for KW in $KEYWORDS; do
  if ! echo "$SUMMARY" | grep -qi "$KW" 2>/dev/null; then
    MISSING="${MISSING}${KW}, "
  fi
done

if [ -n "$MISSING" ]; then
  RESTORE=$(tail -5 "$DECISIONS_FILE")
  cat <<EOF
{"decision":"allow","hookSpecificOutput":{"additionalContext":"[COMPACT AUDIT] 以下关键决策可能在 compact 中丢失，重新注入：\n${RESTORE}\n请在继续工作前确认这些决策仍然有效。"}}
EOF
fi
```

5. 更可靠的做法：compact 前主动将关键 context 写入 `.working-state/pre-compact-snapshot.md`，compact 后读回

## Tradeoffs

- **Pro**: 防止 compact 导致的决策遗忘和方向倒退
- **Pro**: 自动化——不需要用户手动检查 compact 质量
- **Con**: 关键词匹配是粗糙的近似——compact 可能用同义词表达了同一决策
- **Con**: 注入恢复信息会占用 compact 后"腾出来"的 context 空间

## Source

Claude Code auto-compact 行为观察。OMC 的 post-compact file restoration 机制（compact 后恢复 top 5 文件，50K token 预算）。
