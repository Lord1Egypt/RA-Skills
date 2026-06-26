#!/usr/bin/env bash
# L4: Stagehand v3 工具可用性测试

section "L4: Stagehand v3"

# 0. 检测是否安装
if ! node -e "require('@browserbasehq/stagehand')" 2>/dev/null; then
  skip "Stagehand 未安装" "运行: npm install @browserbasehq/stagehand"
  skip "Stagehand init" "依赖 Stagehand"
  skip "Stagehand extract" "依赖 Stagehand"
  return 0 2>/dev/null || true
fi

pass "Stagehand 已安装"

# 检测 LLM API key
HAS_LLM_KEY=false
if [[ -n "${ANTHROPIC_API_KEY:-}" || -n "${OPENAI_API_KEY:-}" || -n "${GEMINI_API_KEY:-}" ]]; then
  HAS_LLM_KEY=true
  pass "LLM API key 已配置"
else
  skip "LLM API key 未配置" "需要 ANTHROPIC_API_KEY/OPENAI_API_KEY/GEMINI_API_KEY 之一"
  skip "Stagehand 功能测试" "无 LLM key 无法执行"
  return 0 2>/dev/null || true
fi

# 1. Stagehand v3 版本检测
SH_VERSION=$(node -e "const p = require('@browserbasehq/stagehand/package.json'); console.log(p.version)" 2>/dev/null || echo "unknown")
pass "Stagehand 版本: v$SH_VERSION"

# 2. v3 API 检测（stagehand.act 在实例上，不在 page 上）
V3_CHECK=$(node -e "
const { Stagehand } = require('@browserbasehq/stagehand');
const s = new Stagehand({ env: 'LOCAL', model: 'anthropic/claude-sonnet-4-5' });
console.log('act:', typeof s.act);
console.log('extract:', typeof s.extract);
console.log('observe:', typeof s.observe);
" 2>/dev/null || echo "error")

if echo "$V3_CHECK" | grep -q "act: function"; then
  pass "Stagehand v3 API: act/extract/observe 在实例上"
else
  fail "Stagehand v3 API" "act/extract/observe 不可用，可能是 v2 版本"
fi

# 3. Stagehand init + extract 端到端测试（需要 headless Chrome）
STAGEHAND_TEST_FILE="/tmp/browser-ops-stagehand-test.mjs"
cat > "$STAGEHAND_TEST_FILE" << 'STAGEHAND_EOF'
import { Stagehand } from "@browserbasehq/stagehand";

const model = process.env.ANTHROPIC_API_KEY
  ? "anthropic/claude-sonnet-4-5"
  : process.env.OPENAI_API_KEY
  ? "openai/gpt-4o"
  : "google/gemini-2.0-flash";

try {
  const stagehand = new Stagehand({
    env: "LOCAL",
    model: model,
    localBrowserLaunchOptions: { headless: true },
  });
  await stagehand.init();
  const page = stagehand.context.pages()[0];
  await page.goto("https://example.com");
  const title = await page.title();
  console.log("TITLE:" + title);
  await stagehand.close();
  console.log("SUCCESS");
} catch (e) {
  console.log("ERROR:" + e.message);
}
STAGEHAND_EOF

STAGEHAND_RESULT=$(timeout 30 node "$STAGEHAND_TEST_FILE" 2>/dev/null || echo "TIMEOUT")
rm -f "$STAGEHAND_TEST_FILE"

if echo "$STAGEHAND_RESULT" | grep -q "SUCCESS"; then
  STAGEHAND_TITLE=$(echo "$STAGEHAND_RESULT" | grep "^TITLE:" | sed 's/^TITLE://')
  pass "Stagehand 端到端: init → navigate → title='$STAGEHAND_TITLE' → close"
else
  ERROR_MSG=$(echo "$STAGEHAND_RESULT" | grep "^ERROR:" | sed 's/^ERROR://' | head -1)
  if [[ "$STAGEHAND_RESULT" == "TIMEOUT" ]]; then
    fail "Stagehand 端到端" "超时（30s），可能是 Chrome 启动问题"
  else
    fail "Stagehand 端到端" "${ERROR_MSG:-未知错误}"
  fi
fi
