# Graceful Degradation

## Problem

Agent 依赖的工具不可用时（MCP server 断开、外部 CLI 未安装、API key 过期），agent 陷入反复重试-失败-重试的死循环，浪费大量 token 不产出任何有用工作。

## Solution

维护一份 fallback 工具映射表：当首选工具失败时，自动建议或切换到替代工具。Mapping 包含功能等价性说明，让 agent 知道替代工具的能力边界。PostToolUse hook 检测到连续失败后注入 fallback 建议。

## Implementation

1. 定义 fallback mapping 文件 `.working-state/fallback-tools.md`

```markdown
# Fallback Tool Mapping

| 首选工具 | 替代工具 | 能力差异 |
|---------|---------|---------|
| mcp__firecrawl__scrape | WebFetch | 无 JS 渲染，静态页面 only |
| mcp__github__search | Bash(gh api) | 功能等价，需要 gh CLI |
| mcp__postgres__query | Bash(psql) | 功能等价，需要 psql 客户端 |
| Bash(npm test) | Bash(npx jest) | 等价 |
| mcp__browser__navigate | WebFetch | 无交互能力，只能读取 |
```

2. PostToolUse hook 检测连续失败

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
SUCCESS=$(echo "$INPUT" | jq -r '.tool_output | test("error|Error|ECONNREFUSED|not found|command not found") | not')

SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
FAIL_FILE="sessions/${SESSION_ID}/fail-count-${TOOL}.txt"

if [ "$SUCCESS" = "false" ]; then
  COUNT=$(cat "$FAIL_FILE" 2>/dev/null || echo 0)
  COUNT=$((COUNT + 1))
  echo "$COUNT" > "$FAIL_FILE"
  
  if [ "$COUNT" -ge 2 ]; then
    # 查找 fallback
    FALLBACK=$(grep -i "$(echo $TOOL | sed 's/mcp__//;s/__/.*/')" \
      .working-state/fallback-tools.md 2>/dev/null | head -1)
    
    if [ -n "$FALLBACK" ]; then
      echo "{\"hookSpecificOutput\":{\"additionalContext\":\"[DEGRADATION] ${TOOL} 已连续失败 ${COUNT} 次。建议切换到替代工具：\n${FALLBACK}\n不要继续重试失败的工具。\"}}"
    else
      echo "{\"hookSpecificOutput\":{\"additionalContext\":\"[DEGRADATION] ${TOOL} 已连续失败 ${COUNT} 次，无已知替代。请换一种方法完成当前任务。\"}}"
    fi
  fi
else
  # 成功时重置计数
  rm -f "$FAIL_FILE" 2>/dev/null
fi
```

3. 成功使用替代工具后清除失败计数

## Tradeoffs

- **Pro**: 防止 agent 在不可用工具上浪费 token
- **Pro**: Agent 知道替代工具的能力边界，不会盲目切换后失望
- **Con**: Fallback mapping 需要手动维护
- **Con**: 替代工具可能不完全等价，降级后任务质量下降

## Source

OMC 的 error-code recovery map 中的 fallback 策略。Browser-ops 的分级路由（WebFetch → Firecrawl → agent-browser → browser-use）。经典的 graceful degradation 架构模式。
