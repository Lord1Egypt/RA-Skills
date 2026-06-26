#!/bin/bash

# Call AIDA App 技能测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/call_aida_app.py"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 计数器
TESTS_PASSED=0
TESTS_FAILED=0

# 测试函数
test_case() {
    local test_name=$1
    local test_command=$2
    local expected_pattern=$3

    echo -e "\n${BLUE}测试:${NC} $test_name"

    # 执行测试
    output=$(eval "$test_command" 2>&1)
    exit_code=$?

    # 检查输出
    if echo "$output" | grep -q "$expected_pattern"; then
        echo -e "${GREEN}✓ 通过${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ 失败${NC}"
        echo "期望匹配: $expected_pattern"
        echo "实际输出: $output" | head -5
        ((TESTS_FAILED++))
    fi
}

# 开始测试
echo "╔════════════════════════════════════════════╗"
echo "║   Call AIDA App 技能测试                   ║"
echo "╚════════════════════════════════════════════╝"

# 检查脚本存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}✗ 错误: 找不到脚本${NC}"
    echo "  路径: $SCRIPT_PATH"
    exit 1
fi

echo -e "${GREEN}✓ 脚本路径正确${NC}"

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}✓ 找到 $PYTHON_VERSION${NC}"

# Test 1: 帮助信息
test_case "帮助信息 (--help)" \
    "python3 $SCRIPT_PATH --help" \
    "usage: call_aida_app.py"

# Test 2: 缺少参数时的错误消息
test_case "缺少参数错误" \
    "python3 $SCRIPT_PATH 2>&1" \
    "success.*false"

# Test 3: JSON 语法检查
test_case "Python 语法检查" \
    "python3 -m py_compile $SCRIPT_PATH && echo 'OK'" \
    "OK"

# Test 4: 通过 stdin 传入参数（模拟调用）
test_case "通过 stdin 传入参数" \
    "echo '{\"appid\":\"test\",\"inputs\":{}}' | python3 $SCRIPT_PATH 2>&1" \
    "success"

# Test 5: 通过命令行参数（缺少 inputs）
test_case "缺少 inputs 参数" \
    "python3 $SCRIPT_PATH --appid 'test' 2>&1" \
    "success.*false"

# Test 6: 通过命令行参数（无效 JSON inputs）
test_case "无效 JSON inputs" \
    "python3 $SCRIPT_PATH --appid 'test' --inputs 'not-json' 2>&1" \
    "success.*false"

# Test 7: 完整的命令行参数
test_case "完整命令行参数" \
    "python3 $SCRIPT_PATH --appid 'test' --inputs '{}' 2>&1" \
    "success"

# Test 8: 带 query 参数
test_case "带 query 参数" \
    "python3 $SCRIPT_PATH --appid 'test' --inputs '{}' --query 'test' 2>&1" \
    "success"

# Test 9: 环境变量方式
test_case "环境变量方式" \
    "AIDA_APPID='test' AIDA_INPUTS='{}' python3 $SCRIPT_PATH 2>&1" \
    "success"

# Test 10: 查看文档
test_case "SKILL.md 文档存在" \
    "[ -f $SCRIPT_DIR/SKILL.md ] && echo 'exists'" \
    "exists"

# Test 11: README 文档存在
test_case "README.zh.md 文档存在" \
    "[ -f $SCRIPT_DIR/README.zh.md ] && echo 'exists'" \
    "exists"

# Test 12: EXAMPLES 文档存在
test_case "EXAMPLES.md 文档存在" \
    "[ -f $SCRIPT_DIR/EXAMPLES.md ] && echo 'exists'" \
    "exists"

# 测试输出格式
echo -e "\n${BLUE}进阶测试: JSON 格式验证${NC}"

output=$(python3 $SCRIPT_PATH --appid 'test' --inputs '{}' 2>&1)

# 检查 JSON 格式
if echo "$output" | python3 -m json.tool > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 输出是有效的 JSON${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 输出不是有效的 JSON${NC}"
    echo "输出: $output"
    ((TESTS_FAILED++))
fi

# 检查必需字段
for field in "success" "message" "data"; do
    if echo "$output" | grep -q "\"$field\""; then
        echo -e "${GREEN}✓ 字段 '$field' 存在${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ 字段 '$field' 缺失${NC}"
        ((TESTS_FAILED++))
    fi
done

# 总结
echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   测试结果                                 ║"
echo "╚════════════════════════════════════════════╝"

TOTAL=$((TESTS_PASSED + TESTS_FAILED))
echo -e "总计: $TOTAL 个测试"
echo -e "${GREEN}通过: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}失败: $TESTS_FAILED${NC}"
else
    echo -e "${GREEN}失败: 0${NC}"
fi

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ 所有测试通过！${NC}"
    echo ""
    echo "下一步:"
    echo "  1. 查看完整文档: cat $SCRIPT_DIR/SKILL.md"
    echo "  2. 查看示例: cat $SCRIPT_DIR/EXAMPLES.md"
    echo "  3. 快速参考: cat $SCRIPT_DIR/QUICKSTART.txt"
    exit 0
else
    echo ""
    echo -e "${RED}✗ 某些测试失败${NC}"
    exit 1
fi

