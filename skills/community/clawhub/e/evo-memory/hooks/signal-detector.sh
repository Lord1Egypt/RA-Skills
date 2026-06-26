#!/bin/bash
# Self-Evolution Signal Detector
# Hook: UserPromptSubmit
# 只在检测到关键词时输出，未命中则完全静默（零 token 开销）

PENDING_FILE="$HOME/.openclaw/workspace/self-evolution/pending.jsonl"
TS=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
INPUT="$CLAUDE_USER_INPUT"

# 纠正信号
if echo "$INPUT" | grep -qiE "不对|错了|不是这样|应该是|搞错|弄错|改一下"; then
  echo "{\"ts\":\"$TS\",\"signal\":\"correction\",\"brief\":\"用户可能在纠正\",\"source\":\"hook\"}" >> "$PENDING_FILE"
  echo "<self-evolution-signal>检测到纠正信号，已记录到 pending。请理解具体纠正内容并补充细信号。</self-evolution-signal>"
  exit 0
fi

# 偏好信号
if echo "$INPUT" | grep -qiE "以后都|别再|永远不要|记住.*以后|每次都要"; then
  echo "{\"ts\":\"$TS\",\"signal\":\"preference\",\"brief\":\"用户表达偏好\",\"source\":\"hook\"}" >> "$PENDING_FILE"
  echo "<self-evolution-signal>检测到偏好信号，已记录到 pending。请理解具体偏好并补充细信号。</self-evolution-signal>"
  exit 0
fi

# 满意信号
if echo "$INPUT" | grep -qiE "牛啊|完美|就是这样|太好了|太棒了|非常好|很满意"; then
  echo "{\"ts\":\"$TS\",\"signal\":\"success\",\"brief\":\"用户表达满意\",\"source\":\"hook\"}" >> "$PENDING_FILE"
  echo "<self-evolution-signal>检测到满意信号，已记录到 pending。请理解是哪个方法/结构获得好评并补充细信号。</self-evolution-signal>"
  exit 0
fi

# 显式记忆触发
if echo "$INPUT" | grep -qiE "记住|反思一下|回顾一下|总结一下学到"; then
  echo "<self-evolution-signal>用户显式触发记忆操作，直接走写入流程，不经 pending。</self-evolution-signal>"
  exit 0
fi

# 未命中任何关键词 → 完全静默，不输出任何内容
