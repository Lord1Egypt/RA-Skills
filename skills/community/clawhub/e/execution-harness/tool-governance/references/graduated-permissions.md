# Graduated Permissions（风险分级 PreToolUse）

## Problem

Claude Code 默认对所有工具调用使用相同的权限模型——要么全部 auto-allow（YOLO mode），要么全部需要确认。但工具的风险差异巨大：Read 文件几乎无害，`rm -rf /` 可能毁掉系统。一刀切的权限模型要么太宽松（安全隐患），要么太严格（效率低下）。

## Solution

PreToolUse hook 对工具调用做三级风险分类：safe（自动放行）、medium（记录告警但放行）、dangerous（拒绝并注入替代建议）。分类基于工具名称 + 输入参数的组合判断，不是只看工具名。

## Implementation

1. 定义风险矩阵（工具 + 参数模式 → 风险等级）
2. PreToolUse hook 读取工具名和输入参数
3. 匹配风险矩阵，执行对应决策

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // {}')

case "$TOOL" in
  Read|Glob|Grep)
    # Safe: 只读操作，自动放行
    exit 0
    ;;
  Write|Edit)
    # Medium: 检查路径是否在项目目录内
    FILE=$(echo "$TOOL_INPUT" | jq -r '.file_path // .path // ""')
    if echo "$FILE" | grep -qE '^/(etc|usr|sys|var|bin|sbin)'; then
      echo '{"decision":"deny","reason":"禁止修改系统目录。请只修改项目目录内的文件。"}'
    fi
    # 项目内文件放行（不输出 = allow）
    ;;
  Bash)
    CMD=$(echo "$TOOL_INPUT" | jq -r '.command // ""')
    # Dangerous patterns
    if echo "$CMD" | grep -qE 'rm -rf /[^.]|mkfs|dd if=|:(){ :|curl.*\|.*sh|wget.*\|.*sh'; then
      echo '{"decision":"deny","reason":"检测到高危命令。请使用更安全的替代方案。"}'
    elif echo "$CMD" | grep -qE 'sudo|chmod 777|git push.*--force'; then
      echo '{"decision":"allow","hookSpecificOutput":{"additionalContext":"[WARN] 检测到中风险命令，已放行但请确认操作意图。"}}'
    fi
    ;;
esac
```

4. 风险矩阵可通过外部 JSON 配置文件扩展，无需修改 hook 代码

## Tradeoffs

- **Pro**: 安全性与效率平衡——大部分操作零摩擦，高危操作被拦截
- **Pro**: 可配置——不同项目可以调整风险矩阵
- **Con**: 正则匹配可能误判（注释中的 `rm -rf` 也会触发）
- **Con**: 新增工具需要手动更新风险矩阵

## Source

Claude Code PreToolUse hook 权限系统。OMC 的 YOLO classifier（三级分类：auto/warn/deny）。Claude Code 内置 `allowedTools` 白名单机制的补充。
