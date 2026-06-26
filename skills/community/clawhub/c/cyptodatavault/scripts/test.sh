#!/bin/bash
# DataVault Skill 测试脚本

set -e

echo "========================================"
echo "DataVault Skill Test Suite"
echo "========================================"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 测试函数
run_test() {
    local name=$1
    local cmd=$2
    
    echo -n "Testing: $name ... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        return 1
    fi
}

# 安装依赖
echo -e "\n${GREEN}[1/4]${NC} Installing dependencies..."
pip install -q pyyaml requests ccxt 2>/dev/null || true

# 导入测试
echo -e "\n${GREEN}[2/4]${NC} Testing imports..."
python3 -c "
import sys
sys.path.insert(0, '.')
from src import get_skill
from src.tools import get_all_tools, ALL_TOOLS
print('  All imports successful')
"

# 运行测试
echo -e "\n${GREEN}[3/4]${NC} Running tool tests..."

passed=0
failed=0

# Test 1: Skill 初始化
run_test "Skill Init" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src import get_skill; s=get_skill(); assert s.name==\"datavault\"'" && ((passed++)) || ((failed++))

# Test 2: Tool 数量
run_test "Tool Count" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src.tools import ALL_TOOLS; assert len(ALL_TOOLS)>=50'" && ((passed++)) || ((failed++))

# Test 3: Price Tools
run_test "get_price" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src.tools import call_tool; r=call_tool(\"get_price\", symbol=\"BTC\"); assert \"price\" in r'" && ((passed++)) || ((failed++))

# Test 4: OnChain Tools
run_test "get_eth_balance" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src.tools import call_tool; r=call_tool(\"get_eth_balance\", address=\"0x123\"); assert \"eth_value\" in r'" && ((passed++)) || ((failed++))

# Test 5: DeFi Tools
run_test "get_defi_tvl" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src.tools import call_tool; r=call_tool(\"get_defi_tvl\"); assert \"total_tvl\" in r'" && ((passed++)) || ((failed++))

# Test 6: Risk Tools
run_test "get_liquidation_24h" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src.tools import call_tool; r=call_tool(\"get_liquidation_24h\"); assert \"total_liquidation\" in r'" && ((passed++)) || ((failed++))

# Test 7: Sentiment Tools
run_test "get_crypto_news" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src.tools import call_tool; r=call_tool(\"get_crypto_news\"); assert \"news\" in r'" && ((passed++)) || ((failed++))

# Test 8: 健康检查
run_test "Health Check" "python3 -c 'import sys; sys.path.insert(0, \".\"); from src import get_skill; h=get_skill().health(); assert h[\"status\"]==\"healthy\"'" && ((passed++)) || ((failed++))

# 总结
echo -e "\n${GREEN}[4/4]${NC} Results: $passed passed, $failed failed"

if [ $failed -eq 0 ]; then
    echo -e "\n${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed${NC}"
    exit 1
fi