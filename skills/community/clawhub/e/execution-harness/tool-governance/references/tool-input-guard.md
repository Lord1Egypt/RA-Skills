# Tool Input Guard（Bash 输入验证）

## Problem

Agent 构造的 Bash 命令可能包含路径逃逸、破坏性操作、或远程代码执行模式。即使 agent 没有恶意，复杂的 shell 拼接也可能意外产生危险命令——特别是当 agent 从文件内容中提取路径并拼接到命令里时。

## Solution

PreToolUse hook 专门针对 Bash 工具做输入验证，检查三类危险模式：路径边界逃逸（`../` 到项目外）、破坏性全局操作（`rm -rf /`）、远程代码注入（`curl | sh`）。每类独立检查，命中任一即 deny。

## Implementation

1. **路径边界检查**：解析命令中的路径参数，确保 realpath 在项目根目录内

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
[ "$TOOL" = "Bash" ] || exit 0

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

# 1. 路径边界：检测 ../../../etc/passwd 类逃逸
PATHS=$(echo "$CMD" | grep -oE '(/[a-zA-Z0-9_./-]+|\.\./)' || true)
for P in $PATHS; do
  RESOLVED=$(realpath -m "$P" 2>/dev/null || echo "$P")
  case "$RESOLVED" in
    "$PROJECT_ROOT"*) ;; # 项目内，安全
    /tmp/*|/dev/null) ;; # 临时目录，允许
    /usr/bin/*|/usr/local/bin/*) ;; # 常见工具路径，允许
    *)
      echo "{\"decision\":\"deny\",\"reason\":\"路径 ${P} 解析到项目目录外: ${RESOLVED}\"}"
      exit 0
      ;;
  esac
done
```

2. **破坏性命令黑名单**

```bash
# 2. 全局破坏性操作
if echo "$CMD" | grep -qE 'rm\s+-[rRf]*\s+/\s|rm\s+-[rRf]*\s+/[^.]|mkfs\.|dd\s+if=.*of=/dev'; then
  echo '{"decision":"deny","reason":"检测到全局破坏性命令。"}'
  exit 0
fi
```

3. **远程代码注入检测**

```bash
# 3. pipe-to-shell 模式
if echo "$CMD" | grep -qE 'curl\s.*\|\s*(ba)?sh|wget\s.*\|\s*(ba)?sh|curl\s.*>\s*/tmp.*&&.*sh'; then
  echo '{"decision":"deny","reason":"检测到远程代码注入模式 (curl|sh)。请先下载文件审查内容再执行。"}'
  exit 0
fi
```

4. 以上检查通过后，不输出任何内容（= 默认 allow）

## Tradeoffs

- **Pro**: 防御 agent 意外构造的危险命令，特别是路径逃逸
- **Pro**: 独立于 graduated-permissions 的细粒度 Bash 专项检查
- **Con**: 路径解析可能在符号链接场景下误判
- **Con**: 高级 shell 技巧（eval、变量展开）可以绕过静态正则检测

## Source

Claude Code PreToolUse hook。OMC 的 Bash 6-layer defense-in-depth（其中 path boundary 和 command blacklist 是前两层）。安全最佳实践——不信任 agent 构造的任何用户输入。
