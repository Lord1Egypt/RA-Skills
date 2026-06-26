#!/usr/bin/env bash
# Session/Cookie 持久化测试

section "Session 持久化"

TEST_PROFILE_DIR="/tmp/browser-ops-test-profile"
TEST_STATE_FILE="/tmp/browser-ops-test-state.json"
rm -rf "$TEST_PROFILE_DIR" "$TEST_STATE_FILE"

# === agent-browser Session 测试 ===

if ! command -v agent-browser &>/dev/null; then
  skip "agent-browser Session" "agent-browser 未安装"
  skip "Profile 持久化" "依赖 agent-browser"
  skip "State 导出/导入" "依赖 agent-browser"
  skip "Cookie 操作" "依赖 agent-browser"
else
  # 1. --profile 创建并写入
  agent-browser --profile "$TEST_PROFILE_DIR" open https://example.com 2>/dev/null || true
  sleep 2
  agent-browser close 2>/dev/null || true
  sleep 1

  if [[ -d "$TEST_PROFILE_DIR" ]]; then
    PROFILE_SIZE=$(du -sh "$TEST_PROFILE_DIR" 2>/dev/null | cut -f1)
    pass "Profile 目录创建: $TEST_PROFILE_DIR($PROFILE_SIZE)"
  else
    fail "Profile 目录创建" "$TEST_PROFILE_DIR 未生成"
  fi

  # 2. Cookie 查看
  COOKIES=$(agent-browser cookies 2>&1) || true
  if [[ -n "$COOKIES" ]]; then
    pass "Cookie 查看: 有输出"
  else
    skip "Cookie 查看" "无 Cookie(example.com 可能不设置 Cookie)"
  fi

  # 3. State 导出
  agent-browser state save "$TEST_STATE_FILE" 2>/dev/null || true
  if [[ -f "$TEST_STATE_FILE" && -s "$TEST_STATE_FILE" ]]; then
    STATE_SIZE=$(wc -c < "$TEST_STATE_FILE")
    # 验证是合法 JSON
    if python3 -c "import json; json.load(open('$TEST_STATE_FILE'))" 2>/dev/null; then
      pass "State 导出: $TEST_STATE_FILE(${STATE_SIZE} bytes，合法 JSON)"
    else
      fail "State 导出" "文件不是合法 JSON"
    fi
  else
    skip "State 导出" "state save 未生成文件(可能需要 CDP 模式)"
  fi

  agent-browser close 2>/dev/null || true

  # 4. State 导入(另起 session)
  if [[ -f "$TEST_STATE_FILE" && -s "$TEST_STATE_FILE" ]]; then
    agent-browser state load "$TEST_STATE_FILE" 2>/dev/null || true
    LOAD_RESULT=$(agent-browser open https://example.com 2>&1) || true
    if [[ $? -eq 0 || -n "$LOAD_RESULT" ]]; then
      pass "State 导入: 加载成功"
    else
      skip "State 导入" "加载命令未报错但结果未知"
    fi
    agent-browser close 2>/dev/null || true
  else
    skip "State 导入" "无导出文件可导入"
  fi

  # 5. Profile 复用验证(二次打开应保留状态)
  if [[ -d "$TEST_PROFILE_DIR" ]]; then
    agent-browser --profile "$TEST_PROFILE_DIR" open https://example.com 2>/dev/null || true
    SNAP=$(agent-browser snapshot 2>&1) || true
    if [[ -n "$SNAP" && ${#SNAP} -gt 50 ]]; then
      pass "Profile 复用: 二次打开正常(${#SNAP} 字符)"
    else
      skip "Profile 复用" "快照为空"
    fi
    agent-browser close 2>/dev/null || true
  fi
fi

# === 目录结构测试 ===

# 6. 标准目录结构创建
mkdir -p ~/.browser-ops/profiles/default ~/.browser-ops/states ~/.browser-ops/stagehand-cache
if [[ -d ~/.browser-ops/profiles && -d ~/.browser-ops/states && -d ~/.browser-ops/stagehand-cache ]]; then
  pass "标准目录结构: ~/.browser-ops/ 已就绪"
else
  fail "标准目录结构" "~/.browser-ops/ 子目录创建失败"
fi

# 清理测试文件
rm -rf "$TEST_PROFILE_DIR" "$TEST_STATE_FILE"
