#!/bin/bash

# Test Script for Review Analyzer Skill
# Runs a complete analysis workflow using sample data

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Simple Review Analyzer - 测试脚本${NC}"
echo -e "${BLUE}========================================${NC}"

# Test 1: Check directory structure
echo -e "\n${YELLOW}[测试 1] 检查目录结构...${NC}"
required_dirs=("$ROOT_DIR/prompts" "$ROOT_DIR/templates" "$ROOT_DIR/utils" "$ROOT_DIR/output")
all_exist=true
for dir in "${required_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo -e "  ${GREEN}✓${NC} $dir"
    else
        echo -e "  ${RED}✗${NC} $dir (不存在)"
        all_exist=false
    fi
done

if [[ "$all_exist" == "true" ]]; then
    echo -e "${GREEN}所有目录检查通过${NC}"
else
    echo -e "${RED}目录结构检查失败${NC}"
    exit 1
fi

# Test 2: Check required files
echo -e "\n${YELLOW}[测试 2] 检查必需文件...${NC}"
required_files=(
    "$ROOT_DIR/skill.md"
    "$ROOT_DIR/prompts/tagging.txt"
    "$ROOT_DIR/prompts/tagging_batch.txt"
    "$ROOT_DIR/prompts/insights.txt"
    "$ROOT_DIR/templates/report.html"
    "$ROOT_DIR/utils/csv_reader.sh"
    "$ROOT_DIR/utils/tagging_core.sh"
    "$ROOT_DIR/utils/insights_generator.sh"
    "$ROOT_DIR/utils/html_generator.sh"
    "$ROOT_DIR/utils/analyzer_controller.sh"
    "$ROOT_DIR/utils/merge_csv.py"
)

all_exist=true
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "  ${GREEN}✓${NC} $(basename "$file")"
    else
        echo -e "  ${RED}✗${NC} $(basename "$file") (不存在)"
        all_exist=false
    fi
done

if [[ "$all_exist" == "true" ]]; then
    echo -e "${GREEN}所有文件检查通过${NC}"
else
    echo -e "${RED}文件检查失败${NC}"
    exit 1
fi

# Test 3: Check script permissions
echo -e "\n${YELLOW}[测试 3] 检查脚本权限...${NC}"
scripts=(
    "$ROOT_DIR/utils/csv_reader.sh"
    "$ROOT_DIR/utils/tagging_core.sh"
    "$ROOT_DIR/utils/insights_generator.sh"
    "$ROOT_DIR/utils/html_generator.sh"
    "$ROOT_DIR/utils/analyzer_controller.sh"
)

all_executable=true
for script in "${scripts[@]}"; do
    if [[ -x "$script" ]]; then
        echo -e "  ${GREEN}✓${NC} $(basename "$script") (可执行)"
    else
        echo -e "  ${YELLOW}⚠${NC} $(basename "$script") (不可执行，运行: chmod +x $script)"
        all_executable=false
    fi
done

# Test 4: Check Python
echo -e "\n${YELLOW}[测试 4] 检查 Python 环境...${NC}"
if command -v python3 &> /dev/null; then
    py_version=$(python3 --version 2>&1)
    echo -e "  ${GREEN}✓${NC} Python3: $py_version"
else
    echo -e "  ${YELLOW}⚠${NC} Python3 未安装 (CSV 合并功能需要)"
fi

# Test 5: Check jq
echo -e "\n${YELLOW}[测试 5] 检查 JSON 工具...${NC}"
if command -v jq &> /dev/null; then
    jq_version=$(jq --version 2>&1)
    echo -e "  ${GREEN}✓${NC} jq: $jq_version"
else
    echo -e "  ${YELLOW}⚠${NC} jq 未安装 (JSON 处理功能需要)"
fi

# Test 6: Validate prompts
echo -e "\n${YELLOW}[测试 6] 验证提示词模板...${NC}"
prompts=(
    "$ROOT_DIR/prompts/tagging.txt"
    "$ROOT_DIR/prompts/tagging_batch.txt"
    "$ROOT_DIR/prompts/insights.txt"
)

all_valid=true
for prompt in "${prompts[@]}"; do
    if grep -q "{review_id}" "$prompt" 2>/dev/null || \
       grep -q "{batch_size}" "$prompt" 2>/dev/null || \
       grep -q "{total}" "$prompt" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $(basename "$prompt") (包含占位符)"
    else
        echo -e "  ${YELLOW}⚠${NC} $(basename "$prompt") (可能缺少占位符)"
        all_valid=false
    fi
done

# Test 7: Sample data check
echo -e "\n${YELLOW}[测试 7] 检查示例数据...${NC}"
sample_csv="../assets/examples/reviews_sample.csv"
if [[ -f "$sample_csv" ]]; then
    echo -e "  ${GREEN}✓${NC} 示例 CSV 文件存在"
    line_count=$(wc -l < "$sample_csv" 2>/dev/null || echo "0")
    echo -e "    行数: $line_count"
else
    echo -e "  ${YELLOW}⚠${NC} 示例 CSV 文件不存在 ($sample_csv)"
fi

# Summary
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}测试总结${NC}"
echo -e "${BLUE}========================================${NC}"

if [[ "$all_exist" == "true" && "$all_valid" == "true" ]]; then
    echo -e "${GREEN}✓ 所有测试通过！Skill 已准备就绪。${NC}"
    echo -e "\n${YELLOW}下一步：${NC}"
    echo -e "  1. 在 Claude Code 中加载此 Skill"
    echo -e "  2. 使用自然语言调用：\"请分析评论：reviews.csv\""
    exit 0
else
    echo -e "${RED}✗ 部分测试失败，请检查上述错误。${NC}"
    exit 1
fi
