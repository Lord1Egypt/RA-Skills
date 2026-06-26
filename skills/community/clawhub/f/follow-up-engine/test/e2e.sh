#!/bin/bash

# Follow-up Engine - End-to-End Test Script
# 测试跟进引擎完整流程

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$SKILL_DIR/config"
DRAFTS_DIR="$SKILL_DIR/drafts"
LOGS_DIR="$SKILL_DIR/logs"

echo "========================================"
echo "Follow-up Engine E2E Test"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数器
PASSED=0
FAILED=0

# 测试函数
test_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

test_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

test_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# 1. 验证配置文件
echo "【测试 1】验证配置文件..."
for config in follow-up-rules.json stage-transitions.json follow-up-strategies.json; do
    if [ -f "$CONFIG_DIR/$config" ]; then
        if node -e "JSON.parse(require('fs').readFileSync('$CONFIG_DIR/$config'))" 2>/dev/null; then
            test_pass "$config 格式有效"
        else
            test_fail "$config JSON 格式错误"
        fi
    else
        test_fail "$config 文件不存在"
    fi
done
echo ""

# 2. 验证脚本文件
echo "【测试 2】验证脚本文件..."
for script in follow-up-scheduler.js okki-integration.js; do
    if [ -f "$SKILL_DIR/scripts/$script" ]; then
        test_pass "$script 存在"
    else
        test_fail "$script 文件不存在"
    fi
done
echo ""

# 3. 测试 follow-up-scheduler.js (dry-run)
echo "【测试 3】测试 follow-up-scheduler.js (dry-run)..."
if node "$SKILL_DIR/scripts/follow-up-scheduler.js" --dry-run > /tmp/scheduler-test.log 2>&1; then
    test_pass "follow-up-scheduler.js dry-run 执行成功"
    test_info "日志：/tmp/scheduler-test.log"
else
    test_fail "follow-up-scheduler.js dry-run 执行失败"
    cat /tmp/scheduler-test.log
fi
echo ""

# 4. 测试 okki-integration.js (dry-run)
echo "【测试 4】测试 okki-integration.js (dry-run)..."
if node "$SKILL_DIR/scripts/okki-integration.js" --dry-run > /tmp/integration-test.log 2>&1; then
    test_pass "okki-integration.js dry-run 执行成功"
    test_info "日志：/tmp/integration-test.log"
else
    test_fail "okki-integration.js dry-run 执行失败"
    cat /tmp/integration-test.log
fi
echo ""

# 5. 验证目录结构
echo "【测试 5】验证目录结构..."
for dir in config scripts drafts logs; do
    if [ -d "$SKILL_DIR/$dir" ]; then
        test_pass "$dir/ 目录存在"
    else
        test_fail "$dir/ 目录不存在"
    fi
done
echo ""

# 6. 检查依赖
echo "【测试 6】检查依赖..."
if [ -f "/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki.py" ]; then
    test_pass "OKKI CLI 存在"
else
    test_fail "OKKI CLI 不存在"
fi

if [ -d "/Users/wilson/.openclaw/workspace/skills/imap-smtp-email" ]; then
    test_pass "email-smart-reply skill 存在"
else
    test_fail "email-smart-reply skill 不存在"
fi
echo ""

# 测试结果汇总
echo "========================================"
echo "测试结果汇总"
echo "========================================"
echo -e "${GREEN}通过：$PASSED${NC}"
echo -e "${RED}失败：$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ 所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}✗ 部分测试失败，请检查日志${NC}"
    exit 1
fi
