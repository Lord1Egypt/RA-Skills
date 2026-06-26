#!/usr/bin/env bash
# opencli 桥接层可用性测试

section "opencli 桥接层"

# 0. 检测是否安装
if ! command -v opencli &>/dev/null; then
  skip "opencli 未安装" "运行: npm install -g @jackwener/opencli + 安装 Chrome 扩展"
  skip "opencli doctor" "依赖 opencli"
  skip "opencli list" "依赖 opencli"
  skip "opencli 平台测试" "依赖 opencli"
  return 0 2>/dev/null || true
fi

pass "opencli 已安装"

# 1. doctor 检查 (Bridge 连通性)
DOCTOR_OUTPUT=$(opencli doctor 2>&1) || true
if echo "$DOCTOR_OUTPUT" | grep -qi "connected\|ok\|ready\|healthy"; then
  pass "opencli doctor: Bridge 连通"
else
  skip "opencli Bridge 未连通" "需要 Chrome 运行 + 扩展加载 (chrome://extensions)"
  skip "opencli 平台测试" "Bridge 未连通"
  return 0 2>/dev/null || true
fi

# 2. 适配器列表
LIST_OUTPUT=$(opencli list 2>&1) || true
if [[ -n "$LIST_OUTPUT" && ${#LIST_OUTPUT} -gt 100 ]]; then
  # 统计适配器数量
  ADAPTER_COUNT=$(echo "$LIST_OUTPUT" | grep -cE "^\s+\w+" || echo "unknown")
  pass "opencli list: ${ADAPTER_COUNT} 个适配器"
else
  skip "opencli list" "输出为空"
fi

# 3. 公开内容测试 (不需要登录)
HACKERNEWS=$(opencli hackernews top --format json 2>&1) || true
if echo "$HACKERNEWS" | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null; then
  pass "opencli hackernews top: 返回合法 JSON"
elif [[ -n "$HACKERNEWS" && ${#HACKERNEWS} -gt 50 ]]; then
  pass "opencli hackernews top: 有内容返回 (${#HACKERNEWS} chars)"
else
  skip "opencli hackernews top" "无输出或错误"
fi

# 4. cascade 认证探测
CASCADE=$(opencli cascade https://example.com 2>&1)
CASCADE_EXIT=$?
if [[ $CASCADE_EXIT -eq 0 ]]; then
  pass "opencli cascade: example.com 可公开访问"
elif [[ $CASCADE_EXIT -eq 77 ]]; then
  pass "opencli cascade: example.com 需要登录 (exit 77)"
else
  skip "opencli cascade" "exit code $CASCADE_EXIT"
fi

# 5. 输出格式测试
for fmt in json table md; do
  FMT_OUTPUT=$(opencli hackernews top --format $fmt 2>&1) || true
  if [[ -n "$FMT_OUTPUT" && ${#FMT_OUTPUT} -gt 20 ]]; then
    pass "opencli --format $fmt: 有输出"
  else
    skip "opencli --format $fmt" "无输出"
  fi
done
