"""
run.sh 模板生成器
"""


def generate_run_sh(project_name: str) -> str:
    return f"""#!/bin/bash
# {project_name} — 一键运行脚本

set -e

echo "=== {project_name} ==="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python"
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)

# 安装依赖
if [ -f "requirements.txt" ]; then
    echo "安装依赖..."
    $PYTHON -m pip install -r requirements.txt --quiet
fi

# 运行主程序
echo "启动 {project_name}..."
$PYTHON src/main.py "$@"
"""
