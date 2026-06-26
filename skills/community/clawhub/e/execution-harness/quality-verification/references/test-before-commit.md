# Test Before Commit

## Problem

Agent 修改代码后直接 commit，没有运行测试。CI 在远端才发现 regression，但 agent 已经认为任务完成了。特别是在 Ralph 持续执行模式下，agent 可能连续提交多个 broken commit，每个都通过了 Stop hook 的迭代检查但没有经过质量验证。

## Solution

PreToolUse hook 拦截 `git commit` 命令，在 commit 执行前自动运行项目的测试命令。测试失败时拒绝 commit 并将失败信息注入 context，让 agent 先修 bug 再提交。

## Implementation

1. PreToolUse hook 检测 Bash 工具中的 git commit 命令

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
[ "$TOOL" = "Bash" ] || exit 0

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
# 检测 git commit（排除 git commit --amend 等只修改消息的情况）
echo "$CMD" | grep -qE 'git\s+commit' || exit 0

# 确定测试命令（按优先级检测项目配置）
if [ -f "package.json" ] && grep -q '"test"' package.json; then
  TEST_CMD="npm test"
elif [ -f "Makefile" ] && grep -q '^test:' Makefile; then
  TEST_CMD="make test"
elif [ -f "pytest.ini" ] || [ -f "setup.cfg" ] || [ -f "pyproject.toml" ]; then
  TEST_CMD="python -m pytest --tb=short -q"
elif [ -f "Cargo.toml" ]; then
  TEST_CMD="cargo test"
else
  # 无法确定测试命令，放行
  exit 0
fi

# 运行测试（超时 120 秒）
TEST_OUTPUT=$(timeout 120 bash -c "$TEST_CMD" 2>&1)
TEST_EXIT=$?

if [ "$TEST_EXIT" -ne 0 ]; then
  # 截取最后 50 行避免输出过长
  TAIL=$(echo "$TEST_OUTPUT" | tail -50)
  echo "{\"decision\":\"deny\",\"reason\":\"测试失败，commit 被阻止。请先修复以下问题再提交：\n${TAIL}\"}"
else
  # 测试通过，放行 commit
  exit 0
fi
```

2. 可选：缓存测试结果，如果自上次测试通过后没有文件变更则跳过

```bash
LAST_PASS="sessions/${SESSION_ID}/last-test-pass.txt"
LAST_CHANGE=$(git diff --stat HEAD 2>/dev/null | md5sum | cut -d' ' -f1)
if [ -f "$LAST_PASS" ] && [ "$(cat "$LAST_PASS")" = "$LAST_CHANGE" ]; then
  exit 0  # 变更未改变，复用上次测试结果
fi
```

## Tradeoffs

- **Pro**: 在 commit 前捕获 regression，避免 broken commit 进入历史
- **Pro**: 失败信息直接注入 agent context，agent 可以立即修复
- **Con**: 测试耗时可能很长——大型项目的完整测试套件可能需要几分钟
- **Con**: 不是所有项目都有明确的测试命令，需要启发式检测

## Source

Git pre-commit hook 的 agent 适配。Claude Code PreToolUse hook 拦截特定 Bash 命令的能力。CI/CD shift-left 测试理念。
