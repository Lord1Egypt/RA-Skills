#!/bin/bash
# 中文工具包安装脚本
# 从GitHub仓库: https://github.com/utopia013-droid/luxyoo

set -e  # 遇到错误立即退出

echo "🚀 开始安装中文工具包..."
echo "仓库: https://github.com/utopia013-droid/luxyoo"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查必要工具
check_requirements() {
    echo "🔍 检查系统要求..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python3 已安装${NC}"
    else
        echo -e "${RED}❌ 需要安装 Python3${NC}"
        echo "请访问: https://www.python.org/downloads/"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        echo -e "${GREEN}✅ pip3 已安装${NC}"
    else
        echo -e "${YELLOW}⚠️ pip3 未安装，尝试安装...${NC}"
        python3 -m ensurepip --upgrade
    fi
    
    # 检查git
    if command -v git &> /dev/null; then
        echo -e "${GREEN}✅ Git 已安装${NC}"
    else
        echo -e "${YELLOW}⚠️ Git 未安装，但可以继续${NC}"
    fi
}

# 安装Python依赖
install_dependencies() {
    echo ""
    echo "📦 安装Python依赖..."
    
    # 检查requirements.txt是否存在
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        echo -e "${GREEN}✅ 依赖安装完成${NC}"
    else
        echo -e "${YELLOW}⚠️ requirements.txt 不存在，安装核心依赖...${NC}"
        pip3 install jieba pypinyin opencc-python-reimplemented requests
        echo -e "${GREEN}✅ 核心依赖安装完成${NC}"
    fi
}

# 测试安装
test_installation() {
    echo ""
    echo "🧪 测试安装..."
    
    # 创建测试脚本
    cat > test_chinese_tools.py << 'EOF'
#!/usr/bin/env python3
# 测试中文工具包

try:
    from chinese_tools import segment, toPinyin, textStats, extractKeywords, translate
    
    print("✅ 中文工具包导入成功")
    print("")
    
    # 测试分词
    text = "人工智能正在改变世界"
    result = segment(text)
    print(f"📝 分词测试: '{text}'")
    print(f"   结果: {result}")
    print("")
    
    # 测试拼音
    text = "中文"
    result = toPinyin(text)
    print(f"🔤 拼音测试: '{text}'")
    print(f"   结果: {result}")
    print("")
    
    # 测试文本统计
    text = "这是一个测试句子。这是第二个句子。"
    result = textStats(text)
    print(f"📊 文本统计测试: '{text}'")
    print(f"   字数: {result['char_count']}")
    print(f"   词数: {result['word_count']}")
    print(f"   句子数: {result['sentence_count']}")
    print("")
    
    print("🎉 所有测试通过！")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保在正确目录运行")
except Exception as e:
    print(f"❌ 测试失败: {e}")

EOF
    
    # 运行测试
    python3 test_chinese_tools.py
    
    # 清理测试文件
    rm -f test_chinese_tools.py
}

# 显示使用说明
show_usage() {
    echo ""
    echo -e "${BLUE}📖 使用说明:${NC}"
    echo "1. 基本使用:"
    echo "   python3 -c \"from chinese_tools import segment; print(segment('测试文本'))\""
    echo ""
    echo "2. 查看示例:"
    echo "   python3 examples/simple_example.py"
    echo ""
    echo "3. 从OpenClaw安装:"
    echo "   openclaw skills install chinese-toolkit"
    echo ""
    echo -e "${GREEN}🎊 安装完成！感谢使用中文工具包。${NC}"
    echo "GitHub: https://github.com/utopia013-droid/luxyoo"
    echo "问题反馈: https://github.com/utopia013-droid/luxyoo/issues"
}

# 主函数
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}     中文工具包安装程序${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # 检查是否在仓库目录
    if [ -f "chinese_tools.py" ]; then
        echo -e "${GREEN}✅ 已在仓库目录${NC}"
    else
        echo -e "${YELLOW}⚠️ 不在仓库目录，尝试下载...${NC}"
        
        # 检查是否已克隆
        if [ -d "luxyoo" ]; then
            cd luxyoo
        else
            # 克隆仓库
            git clone https://github.com/utopia013-droid/luxyoo.git
            cd luxyoo
        fi
    fi
    
    # 执行安装步骤
    check_requirements
    install_dependencies
    test_installation
    show_usage
}

# 运行主函数
main "$@"