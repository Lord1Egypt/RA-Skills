#!/usr/bin/env bash
# browser-ops 测试主入口
# 用法:
#   bash tests/run_tests.sh           # 运行全部测试
#   bash tests/run_tests.sh structure # 只跑结构校验
#   bash tests/run_tests.sh l2        # 只跑 L2 (Jina)
#   bash tests/run_tests.sh l3        # 只跑 L3 (agent-browser)
#   bash tests/run_tests.sh l4        # 只跑 L4 (Stagehand)
#   bash tests/run_tests.sh l6        # 只跑 L6 (反爬)
#   bash tests/run_tests.sh session   # 只跑 Session 持久化

set -uo pipefail
# 不用 set -e: 测试中的失败命令由测试逻辑自行处理

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# macOS 没有 timeout 命令，用 perl 替代
if ! command -v timeout &>/dev/null; then
  timeout() {
    local secs="$1"; shift
    perl -e "alarm $secs; exec @ARGV" -- "$@"
  }
  export -f timeout
fi

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASSED=0
FAILED=0
SKIPPED=0
RESULTS=()

pass() {
  PASSED=$((PASSED + 1))
  RESULTS+=("${GREEN}✅ PASS${NC}: $1")
  echo -e "${GREEN}✅ PASS${NC}: $1"
}

fail() {
  FAILED=$((FAILED + 1))
  RESULTS+=("${RED}❌ FAIL${NC}: $1 — $2")
  echo -e "${RED}❌ FAIL${NC}: $1 — $2"
}

skip() {
  SKIPPED=$((SKIPPED + 1))
  RESULTS+=("${YELLOW}⏭️  SKIP${NC}: $1 — $2")
  echo -e "${YELLOW}⏭️  SKIP${NC}: $1 — $2"
}

section() {
  echo ""
  echo -e "${BLUE}━━━ $1 ━━━${NC}"
}

# 判断要跑哪些测试
TARGET="${1:-all}"

run_test_file() {
  local test_file="$1"
  if [[ -f "$SCRIPT_DIR/$test_file" ]]; then
    source "$SCRIPT_DIR/$test_file"
  else
    echo -e "${RED}测试文件不存在: $test_file${NC}"
  fi
}

echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   browser-ops 测试套件 v3.2.0        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo "测试目标: $TARGET"
echo "仓库路径: $REPO_DIR"
echo ""

case "$TARGET" in
  all)
    run_test_file "test_structure.sh"
    run_test_file "test_opencli.sh"
    run_test_file "# deleted (jina removed)"
    run_test_file "test_agent_browser.sh"
    run_test_file "test_stagehand.sh"
    run_test_file "test_anti_detection.sh"
    run_test_file "test_session.sh"
    ;;
  structure) run_test_file "test_structure.sh" ;;
  opencli)   run_test_file "test_opencli.sh" ;;
  agent-browser) run_test_file "test_agent_browser.sh" ;;
  stagehand)    run_test_file "test_stagehand.sh" ;;
  anti-detect)  run_test_file "test_anti_detection.sh" ;;
  session)   run_test_file "test_session.sh" ;;
  *)
    echo "未知目标: $TARGET"
    echo "可选: all, structure, l2, l3, l4, l6, session"
    exit 1
    ;;
esac

# 汇总
section "测试结果汇总"
echo ""
for r in "${RESULTS[@]}"; do
  echo -e "  $r"
done
echo ""
echo -e "通过: ${GREEN}$PASSED${NC} | 失败: ${RED}$FAILED${NC} | 跳过: ${YELLOW}$SKIPPED${NC} | 合计: $((PASSED + FAILED + SKIPPED))"

if [[ $FAILED -gt 0 ]]; then
  echo -e "\n${RED}有测试失败！${NC}"
  exit 1
else
  echo -e "\n${GREEN}全部通过！${NC}"
  exit 0
fi
