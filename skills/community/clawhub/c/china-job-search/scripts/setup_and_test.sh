#!/bin/bash
echo "========================================"
echo "招聘搜索技能 - 一键安装和测试"
echo "========================================"
echo

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

echo "[1/4] 检查Python版本..."
python3 --version

echo
echo "[2/4] 安装依赖..."
pip3 install requests beautifulsoup4 fake-useragent lxml -q
if [ $? -ne 0 ]; then
    echo "[警告] 依赖安装可能有问题，尝试手动安装:"
    echo "  pip3 install requests beautifulsoup4 fake-useragent lxml"
fi

echo
echo "[3/4] 测试技能功能..."
echo "运行简单测试..."
python3 simple_test.py

echo
echo "[4/4] 创建示例文件..."
if [ ! -f "example_search.py" ]; then
    cat > example_search.py << 'EOF'
# 示例搜索脚本
import sys
sys.path.append('.')
from final_searcher import FinalJobSearcher

searcher = FinalJobSearcher()
results = searcher.search_with_guarantee('Python', '北京', 10)
print(searcher.format_results(results))
EOF
    echo "示例文件已创建: example_search.py"
fi

echo
echo "========================================"
echo "安装完成！"
echo "========================================"
echo
echo "使用方式:"
echo "1. 命令行搜索: python3 final_searcher.py Python 北京"
echo "2. 测试功能: python3 test_final.py"
echo "3. 查看示例: python3 example_search.py"
echo
echo "在OpenClaw中使用:"
echo "  from skills.job_search.final_searcher import FinalJobSearcher"
echo "  searcher = FinalJobSearcher()"
echo "  results = searcher.search_with_guarantee('关键词', '城市', 数量)"
echo