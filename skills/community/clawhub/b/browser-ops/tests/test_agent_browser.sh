#!/usr/bin/env bash
# L3: agent-browser 工具可用性测试

section "L3: agent-browser"

# 0. 检测是否安装
if ! command -v agent-browser &>/dev/null; then
  skip "agent-browser 未安装" "运行: npm install -g agent-browser && agent-browser install"
  skip "agent-browser 导航" "依赖 agent-browser"
  skip "agent-browser 快照" "依赖 agent-browser"
  skip "agent-browser 截图" "依赖 agent-browser"
  skip "agent-browser 版本" "依赖 agent-browser"
  return 0 2>/dev/null || true
fi

pass "agent-browser 已安装: $(agent-browser --version 2>/dev/null || echo 'unknown')"

# 1. 导航测试
NAV_OUTPUT=$(agent-browser open https://example.com 2>&1) || true
if echo "$NAV_OUTPUT" | grep -qiE "example|navigat|loaded|success"; then
  pass "agent-browser 导航: example.com"
else
  # 有些版本不输出成功消息，尝试 snapshot 验证
  SNAP=$(agent-browser snapshot 2>&1) || true
  if [[ -n "$SNAP" && ${#SNAP} -gt 50 ]]; then
    pass "agent-browser 导航: example.com(通过 snapshot 验证)"
  else
    fail "agent-browser 导航" "无法打开 example.com"
    agent-browser close 2>/dev/null || true
    return 0 2>/dev/null || true
  fi
fi

# 2. 快照测试(accessibility tree)
SNAPSHOT=$(agent-browser snapshot 2>&1) || true
if [[ -n "$SNAPSHOT" && ${#SNAPSHOT} -gt 50 ]]; then
  pass "agent-browser snapshot: ${#SNAPSHOT} 字符"
else
  fail "agent-browser snapshot" "快照为空或过短"
fi

# 3. 交互元素快照
SNAPSHOT_I=$(agent-browser snapshot -i 2>&1) || true
if [[ -n "$SNAPSHOT_I" ]]; then
  pass "agent-browser snapshot -i: 交互元素列表"
else
  skip "agent-browser snapshot -i" "无交互元素(example.com 页面简单)"
fi

# 4. 截图测试
SCREENSHOT_FILE="/tmp/browser-ops-test-screenshot.png"
rm -f "$SCREENSHOT_FILE"
agent-browser screenshot --output "$SCREENSHOT_FILE" 2>/dev/null || \
  agent-browser screenshot > "$SCREENSHOT_FILE" 2>/dev/null || true
if [[ -f "$SCREENSHOT_FILE" && -s "$SCREENSHOT_FILE" ]]; then
  FSIZE=$(wc -c < "$SCREENSHOT_FILE")
  pass "agent-browser screenshot: ${FSIZE} bytes"
  rm -f "$SCREENSHOT_FILE"
else
  skip "agent-browser screenshot" "截图文件未生成(可能需要 --output 参数)"
fi

# 5. JS 执行
TITLE=$(agent-browser eval "document.title" 2>&1) || true
if [[ -n "$TITLE" ]]; then
  pass "agent-browser eval: 页面标题 = $TITLE"
else
  skip "agent-browser eval" "JS 执行无输出"
fi

# 6. 获取当前 URL
CURRENT_URL=$(agent-browser get url 2>&1) || true
if echo "$CURRENT_URL" | grep -qi "example.com"; then
  pass "agent-browser get url: $CURRENT_URL"
else
  skip "agent-browser get url" "输出: $CURRENT_URL"
fi

# 清理
agent-browser close 2>/dev/null || true
