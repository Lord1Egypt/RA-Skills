#!/bin/bash
#
# test-integration.sh - Web Fetcher + Deep Research v6.0 端到端集成测试
#
# 测试流程:
# 1. 单URL抓取 → JSON卡片 → Markdown卡片
# 2. 批量抓取
# 3. 数据完整性验证
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试配置
TEST_URL="https://arxiv.org/abs/2301.12345"
TEST_DOMAIN="machine_learning"
TEST_OUTPUT_DIR="test_output"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "  Web Fetcher + Deep Research 集成测试"
echo "========================================"
echo ""

# 清理并创建测试目录
rm -rf "$TEST_OUTPUT_DIR"
mkdir -p "$TEST_OUTPUT_DIR/sources" "$TEST_OUTPUT_DIR/cards"

# 测试计数器
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo ""
    echo "[TEST] $test_name"
    echo "----------------------------------------"
    
    if eval "$test_cmd"; then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        ((TESTS_FAILED++))
        return 1
    fi
}

# ==================== Test 1: Web Fetcher基础功能 ====================
test_web_fetcher_basic() {
    echo "测试Web Fetcher基础抓取..."
    
    cd "$SKILL_DIR/../web-fetcher"
    python3 scripts/web-fetcher.py "$TEST_URL" \
        --domain "$TEST_DOMAIN" \
        --timeout 30 \
        --retries 1 > "$TEST_OUTPUT_DIR/test1_result.json" 2>/dev/null || true
    
    # 验证输出
    if [ -s "$TEST_OUTPUT_DIR/test1_result.json" ]; then
        if python3 -c "import json; d=json.load(open('$TEST_OUTPUT_DIR/test1_result.json')); exit(0 if d.get('success') else 1)"; then
            echo "  - 抓取成功 ✅"
            return 0
        else
            echo "  - 抓取失败 ❌"
            cat "$TEST_OUTPUT_DIR/test1_result.json"
            return 1
        fi
    else
        echo "  - 无输出 ❌"
        return 1
    fi
}

# ==================== Test 2: JSON卡片生成 ====================
test_json_card_generation() {
    echo "测试JSON卡片生成..."
    
    cd "$SKILL_DIR"
    python3 scripts/fetch-card-from-web.py \
        "test-card-001" \
        "$TEST_URL" \
        --domain "$TEST_DOMAIN" \
        --output "$TEST_OUTPUT_DIR/sources" \
        --verbose 2>&1 | tee "$TEST_OUTPUT_DIR/test2_output.log"
    
    # 验证JSON文件生成
    if [ -f "$TEST_OUTPUT_DIR/sources/test-card-001.json" ]; then
        echo "  - JSON卡片生成成功 ✅"
        
        # 验证卡片结构
        if python3 -c "
import json
with open('$TEST_OUTPUT_DIR/sources/test-card-001.json') as f:
    card = json.load(f)
    required = ['card_id', 'source', 'content', 'extracted_metrics', 'quality']
    for field in required:
        if field not in card:
            print(f'Missing field: {field}')
            exit(1)
    print('  - 卡片结构完整 ✅')
    exit(0)
"; then
            return 0
        else
            return 1
        fi
    else
        echo "  - JSON卡片未生成 ❌"
        return 1
    fi
}

# ==================== Test 3: Markdown转换 ====================
test_markdown_conversion() {
    echo "测试Markdown卡片转换..."
    
    cd "$SKILL_DIR"
    python3 scripts/convert-card-to-md.py \
        "$TEST_OUTPUT_DIR/sources/test-card-001.json" \
        --output "$TEST_OUTPUT_DIR/cards" \
        --verbose
    
    # 验证Markdown文件生成
    if [ -f "$TEST_OUTPUT_DIR/cards/test-card-001.md" ]; then
        echo "  - Markdown卡片生成成功 ✅"
        
        # 验证Markdown内容
        if grep -q "^# " "$TEST_OUTPUT_DIR/cards/test-card-001.md"; then
            echo "  - Markdown格式正确 ✅"
            return 0
        else
            echo "  - Markdown格式异常 ❌"
            return 1
        fi
    else
        echo "  - Markdown卡片未生成 ❌"
        return 1
    fi
}

# ==================== Test 4: 批量抓取 ====================
test_batch_fetch() {
    echo "测试批量抓取..."
    
    # 创建测试URL列表
    cat > "$TEST_OUTPUT_DIR/test_urls.txt" << EOF
# 测试URL列表
https://arxiv.org/abs/2301.12345
https://arxiv.org/abs/2302.12345
EOF
    
    cd "$SKILL_DIR"
    python3 scripts/batch-fetch.py \
        "$TEST_OUTPUT_DIR/test_urls.txt" \
        --domain "$TEST_DOMAIN" \
        --output "$TEST_OUTPUT_DIR/batch_sources" \
        --prefix "test-batch" \
        --concurrent 1 \
        --timeout 60 \
        --verbose 2>&1 | tee "$TEST_OUTPUT_DIR/test4_output.log"
    
    # 验证至少有一个卡片生成
    card_count=$(ls "$TEST_OUTPUT_DIR/batch_sources/"*.json 2>/dev/null | wc -l)
    if [ "$card_count" -ge 1 ]; then
        echo "  - 批量抓取成功，生成 $card_count 个卡片 ✅"
        return 0
    else
        echo "  - 批量抓取失败，未生成卡片 ❌"
        return 1
    fi
}

# ==================== Test 5: 数据完整性验证 ====================
test_data_integrity() {
    echo "测试数据完整性..."
    
    cd "$SKILL_DIR"
    python3 << EOF
import json
import sys

card_file = "$TEST_OUTPUT_DIR/sources/test-card-001.json"
with open(card_file) as f:
    card = json.load(f)

# 验证必需字段
required_fields = {
    'card_id': str,
    'source.type': str,
    'source.url': str,
    'source.title': str,
    'content.word_count': int,
    'content.data_level': str,
    'quality.credibility': str
}

errors = []
for field, field_type in required_fields.items():
    keys = field.split('.')
    value = card
    for key in keys:
        value = value.get(key) if isinstance(value, dict) else None
    
    if value is None:
        errors.append(f"Missing: {field}")
    elif not isinstance(value, field_type):
        errors.append(f"Type error: {field} (expected {field_type.__name__}, got {type(value).__name__})")

if errors:
    print("  - 数据完整性检查失败:")
    for e in errors:
        print(f"    {e}")
    sys.exit(1)
else:
    print("  - 数据完整性检查通过 ✅")
    sys.exit(0)
EOF
}

# ==================== Test 6: 错误处理测试 ====================
test_error_handling() {
    echo "测试错误处理..."
    
    cd "$SKILL_DIR/../web-fetcher"
    
    # 测试无效URL
    result=$(python3 scripts/web-fetcher.py "https://invalid-url-that-does-not-exist-12345.com" \
        --timeout 10 --retries 1 2>&1)
    
    if echo "$result" | grep -q '"success": false'; then
        echo "  - 错误处理正常 ✅"
        return 0
    else
        echo "  - 错误处理异常 ❌"
        return 1
    fi
}

# ==================== 运行所有测试 ====================
echo "开始测试..."
echo ""

run_test "Web Fetcher基础功能" test_web_fetcher_basic
run_test "JSON卡片生成" test_json_card_generation
run_test "Markdown转换" test_markdown_conversion
run_test "批量抓取" test_batch_fetch
run_test "数据完整性" test_data_integrity
run_test "错误处理" test_error_handling

# ==================== 测试报告 ====================
echo ""
echo "========================================"
echo "           集成测试报告"
echo "========================================"
echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
echo -e "失败: ${RED}$TESTS_FAILED${NC}"
echo "总计: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    echo ""
    echo "测试输出位置: $TEST_OUTPUT_DIR/"
    exit 0
else
    echo -e "${RED}⚠️  有测试失败，请检查日志${NC}"
    echo ""
    echo "详细日志:"
    ls -la "$TEST_OUTPUT_DIR/"
    exit 1
fi
