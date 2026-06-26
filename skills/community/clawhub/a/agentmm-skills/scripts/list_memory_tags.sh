#!/bin/bash
# list_memory_tags.sh — 注意：此功能已通过 get_memory_stats.sh 涉盖
#
# AgentMM API 没有独立的 /memory/tags 端点。
# 若需查看所有已用标签，请先获取所有记忆再提取 tags 字段：
#
#   ./read_memory.sh | jq '[.memories[].tags // []] | flatten | unique | sort'
echo "Error: /memory/tags endpoint does not exist. Use read_memory.sh + jq to extract tags:" >&2
echo "  ./read_memory.sh | jq '[.memories[].tags // []] | flatten | unique | sort'" >&2
exit 1