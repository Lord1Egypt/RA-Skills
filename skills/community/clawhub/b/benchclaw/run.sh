#!/bin/bash
# run.sh - BenchClaw 评测安全启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/scripts/requirements.txt"

# 1. 优先尝试使用 uv (安全审计的最优解)
# uv 提供内置的哈希校验，且不依赖远程 Python 脚本执行
if command -v uv &> /dev/null; then
 echo "🚀 检测到 uv，正在以安全加速模式启动..."
 # uv run 会自动处理虚拟环境创建与依赖安装，且具备强一致性校验
 cd "$SCRIPT_DIR/scripts" && uv run main.py "$@"
 exit $?
fi

# 2. 传统安全模式：基于 venv 隔离
setup_venv() {
 if [ ! -d "$VENV_DIR" ]; then
 echo "📦 正在创建私有虚拟环境 (venv)..."
 # 使用 python3 自带的 ensurepip 模块，拒绝从互联网下载 get-pip.py
 python3 -m venv "$VENV_DIR" --without-pip
 source "$VENV_DIR/bin/activate"
 python3 -m ensurepip --upgrade --default-pip &>/dev/null || {
 echo "❌ 无法初始化 pip。请确保系统已安装 python3-venv。"
 exit 1
 }
 else
 source "$VENV_DIR/bin/activate"
 fi
}

# 3. 隔离化安装依赖
install_deps() {
 echo "🔍 正在检查/同步依赖..."
 # 仅安装 requirements.txt 声明的依赖，不再安装到用户目录(--user)
 # 建议在 requirements.txt 中包含 --hash 校验以通过最高安全审计
 python3 -m pip install --upgrade pip --quiet
 # 这将强制 pip 检查 requirements.txt 中每一行后面的 --hash 值
 # 如果下载的文件哈希不匹配，安装将立即终止，防止供应链攻击
 python3 -m pip install -r "$REQUIREMENTS" --require-hashes --quiet
 if [ $? -ne 0 ]; then
 echo "❌ 安全校验失败或网络问题。"
 echo "   这可能是因为下载的包与 requirements.txt 中的指纹不符（存在安全风险）。"
 exit 1
 fi
}

# --- 主流程 ---

# A. 确保环境完全隔离（不影响宿主系统）
setup_venv

# B. 检查关键依赖项
if ! python3 -c "import cryptography, psutil" 2>/dev/null; then
 install_deps
fi

# C. 启动 BenchClaw
echo "▶ 启动 BenchClaw 评测..."
python3 "$SCRIPT_DIR/scripts/main.py" "$@"
