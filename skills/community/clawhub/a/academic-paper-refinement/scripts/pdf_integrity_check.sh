#!/bin/bash
# PDF完整性验证脚本
# 用于检查学术论文PDF中的图片、参考文献、交叉引用是否正确

# 用法: ./pdf_integrity_check.sh <paper_name>
# 示例: ./pdf_integrity_check.sh Neurocomputing_HPC_AI_Convergence

PAPER="${1:-paper}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "   PDF完整性验证 - $PAPER"
echo "========================================="

# 检查必要工具
check_tools() {
    local missing=()
    for tool in pdftotext pdfimages pdfinfo; do
        if ! command -v $tool &> /dev/null; then
            missing+=($tool)
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${YELLOW}警告：以下工具未安装: ${missing[*]}${NC}"
        echo "在Ubuntu/Debian上安装: sudo apt-get install poppler-utils"
        echo "在macOS上安装: brew install poppler"
        echo ""
    fi
}

# 1. 检查文件存在性
check_files() {
    echo -e "\n[1/7] 检查文件存在性..."
    local all_exist=true
    
    for ext in tex pdf; do
        if [ -f "$PAPER.$ext" ]; then
            size=$(ls -lh "$PAPER.$ext" 2>/dev/null | awk '{print $5}')
            echo -e "  ${GREEN}✅${NC} $PAPER.$ext ($size)"
        else
            echo -e "  ${RED}❌${NC} $PAPER.$ext ${RED}缺失${NC}"
            all_exist=false
        fi
    done
    
    # 检查bib文件（可能是references.bib或paper.bib）
    if [ -f "$PAPER.bib" ]; then
        size=$(ls -lh "$PAPER.bib" 2>/dev/null | awk '{print $5}')
        echo -e "  ${GREEN}✅${NC} $PAPER.bib ($size)"
    elif [ -f "references.bib" ]; then
        size=$(ls -lh "references.bib" 2>/dev/null | awk '{print $5}')
        echo -e "  ${GREEN}✅${NC} references.bib ($size)"
    else
        echo -e "  ${YELLOW}⚠️${NC} .bib 文件不存在"
    fi
    
    # 检查bbl文件
    if [ -f "$PAPER.bbl" ]; then
        echo -e "  ${GREEN}✅${NC} $PAPER.bbl (参考文献已编译)"
    else
        echo -e "  ${YELLOW}⚠️${NC} $PAPER.bbl 不存在 (需要运行bibtex)"
    fi
    
    # 检查figures文件夹
    if [ -d "figures" ]; then
        fig_count=$(ls figures/*.png figures/*.pdf figures/*.jpg 2>/dev/null | wc -l)
        echo -e "  ${GREEN}✅${NC} figures/ ($fig_count 个文件)"
    else
        echo -e "  ${YELLOW}⚠️${NC} figures/ 文件夹不存在"
    fi
    
    $all_exist
}

# 2. 检查图片嵌入
check_images() {
    echo -e "\n[2/7] 检查图片嵌入..."
    
    if ! command -v pdfimages &> /dev/null; then
        echo -e "  ${YELLOW}⚠️ pdfimages未安装，跳过此检查${NC}"
        return 0
    fi
    
    # 统计PDF中的图片
    local pdf_img_count=$(pdfimages -list "$PAPER.pdf" 2>/dev/null | grep -c " image " || echo "0")
    
    # 统计tex文件中的图片引用
    local tex_img_count=$(grep -o "\\\\includegraphics" "$PAPER.tex" 2>/dev/null | wc -l)
    
    # 确保是数字
    pdf_img_count=${pdf_img_count:-0}
    tex_img_count=${tex_img_count:-0}
    pdf_img_count=$(echo "$pdf_img_count" | head -1)
    tex_img_count=$(echo "$tex_img_count" | head -1)
    
    echo "  PDF中嵌入图片: $pdf_img_count"
    echo "  TeX中引用图片: $tex_img_count"
    
    if [ "$tex_img_count" -eq 0 ]; then
        echo -e "  ${YELLOW}⚠️ 论文无图片${NC}"
    elif [ "$pdf_img_count" -ge "$tex_img_count" ]; then
        echo -e "  ${GREEN}✅ 图片嵌入正常${NC}"
    else
        echo -e "  ${RED}❌ 图片嵌入异常 (缺少 $((tex_img_count - pdf_img_count)) 张)${NC}"
        return 1
    fi
    return 0
}

# 3. 检查参考文献渲染
check_references() {
    echo -e "\n[3/7] 检查参考文献渲染..."
    
    if ! command -v pdftotext &> /dev/null; then
        echo -e "  ${YELLOW}⚠️ pdftotext未安装，跳过此检查${NC}"
        return 0
    fi
    
    # 检查未解析的引用
    local unresolved=$(pdftotext "$PAPER.pdf" - 2>/dev/null | grep -c "\[?\]" || echo "0")
    unresolved=${unresolved:-0}
    unresolved=$(echo "$unresolved" | head -1)
    
    if [ "$unresolved" -gt 0 ]; then
        echo -e "  ${RED}❌ 发现 $unresolved 个未解析引用 [?]${NC}"
        echo "     解决方法: 检查bib文件中的key是否正确"
        return 1
    else
        echo -e "  ${GREEN}✅ 引用解析正常${NC}"
    fi
    
    # 检查参考文献内容
    local ref_content=$(pdftotext "$PAPER.pdf" - 2>/dev/null | grep -A 10 "^\[1\]" | head -5)
    
    if [ -z "$ref_content" ]; then
        echo -e "  ${YELLOW}⚠️ 无法检测参考文献内容${NC}"
    elif echo "$ref_content" | grep -qE "^[0-9 \[\]]+$"; then
        echo -e "  ${RED}❌ 参考文献内容可能未正确渲染${NC}"
        return 1
    else
        echo -e "  ${GREEN}✅ 参考文献内容正常${NC}"
    fi
    return 0
}

# 4. 检查交叉引用
check_cross_references() {
    echo -e "\n[4/7] 检查交叉引用..."
    
    if ! command -v pdftotext &> /dev/null; then
        echo -e "  ${YELLOW}⚠️ pdftotext未安装，跳过此检查${NC}"
        return 0
    fi
    
    local double_q=$(pdftotext "$PAPER.pdf" - 2>/dev/null | grep -c "??" || echo "0")
    double_q=${double_q:-0}
    double_q=$(echo "$double_q" | head -1)
    
    if [ "$double_q" -gt 0 ]; then
        echo -e "  ${RED}❌ 发现 $double_q 个未解析交叉引用 (??)${NC}"
        echo "     解决方法: 重新运行 pdflatex 两次"
        return 1
    else
        echo -e "  ${GREEN}✅ 交叉引用正常${NC}"
    fi
    return 0
}

# 5. 检查PDF信息
check_pdf_info() {
    echo -e "\n[5/7] 检查PDF信息..."
    
    if ! command -v pdfinfo &> /dev/null; then
        echo -e "  ${YELLOW}⚠️ pdfinfo未安装，跳过此检查${NC}"
        return 0
    fi
    
    local info=$(pdfinfo "$PAPER.pdf" 2>/dev/null)
    local pages=$(echo "$info" | grep "Pages:" | awk '{print $2}')
    local size=$(ls -lh "$PAPER.pdf" 2>/dev/null | awk '{print $5}')
    
    echo "  PDF页数: $pages"
    echo "  文件大小: $size"
    
    if [ "$pages" -lt 5 ]; then
        echo -e "  ${YELLOW}⚠️ PDF页数较少，请确认内容完整${NC}"
    else
        echo -e "  ${GREEN}✅ PDF页数正常${NC}"
    fi
    return 0
}

# 6. 检查编译日志
check_log() {
    echo -e "\n[6/7] 检查编译日志..."
    
    if [ ! -f "$PAPER.log" ]; then
        echo -e "  ${YELLOW}⚠️ 编译日志不存在${NC}"
        return 0
    fi
    
    local errors=$(grep -c "^!" "$PAPER.log" 2>/dev/null || echo "0")
    local warnings=$(grep -c "Warning:" "$PAPER.log" 2>/dev/null || echo "0")
    
    # 确保是数字
    errors=${errors:-0}
    warnings=${warnings:-0}
    errors=$(echo "$errors" | head -1)
    warnings=$(echo "$warnings" | head -1)
    
    echo "  错误数: $errors"
    echo "  警告数: $warnings"
    
    if [ "$errors" -gt 0 ]; then
        echo -e "  ${RED}❌ 发现编译错误${NC}"
        grep "^!" "$PAPER.log" | head -5
        return 1
    elif [ "$warnings" -gt 10 ]; then
        echo -e "  ${YELLOW}⚠️ 警告较多，建议检查${NC}"
    else
        echo -e "  ${GREEN}✅ 编译日志正常${NC}"
    fi
    return 0
}

# 7. 检查Unicode问题
check_unicode() {
    echo -e "\n[7/7] 检查Unicode问题..."
    
    # 检查bib文件中的中文字符
    local bib_file=""
    if [ -f "$PAPER.bib" ]; then
        bib_file="$PAPER.bib"
    elif [ -f "references.bib" ]; then
        bib_file="references.bib"
    fi
    
    if [ -n "$bib_file" ]; then
        # 检查bib文件中的中文字符
        local chinese_chars=$(grep -P "[\x{4e00}-\x{9fff}]" "$bib_file" 2>/dev/null | wc -l || echo "0")
        chinese_chars=${chinese_chars:-0}
        chinese_chars=$(echo "$chinese_chars" | head -1)
        
        if [ "$chinese_chars" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️ bib文件中包含中文字符 ($chinese_chars 处)${NC}"
            echo "     可能导致参考文献显示异常"
            echo "     建议: 将中文替换为英文或LaTeX转义序列"
            return 1
        else
            echo -e "  ${GREEN}✅ 无Unicode问题${NC}"
        fi
    else
        echo -e "  ${YELLOW}⚠️ bib文件不存在，跳过Unicode检查${NC}"
    fi
    return 0
}

# 执行所有检查
main() {
    check_tools
    
    local failed=0
    
    check_files || ((failed++))
    check_images || ((failed++))
    check_references || ((failed++))
    check_cross_references || ((failed++))
    check_pdf_info || ((failed++))
    check_log || ((failed++))
    check_unicode || ((failed++))
    
    echo -e "\n========================================="
    if [ $failed -eq 0 ]; then
        echo -e "   ${GREEN}✅ 验证通过 - PDF完整可用${NC}"
    else
        echo -e "   ${RED}❌ 发现 $failed 项问题，请修复后重新验证${NC}"
    fi
    echo "========================================="
    
    return $failed
}

main
