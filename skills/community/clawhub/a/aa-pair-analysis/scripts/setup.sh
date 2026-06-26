#!/usr/bin/env bash
# aa-pair-analysis 环境初始化脚本
# 在首次使用本 skill 前运行，自动检测并安装所有依赖
#
# 用法：bash scripts/setup.sh

set -e

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

ok()   { echo -e "${GREEN}[OK]${NC}  $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
fail() { echo -e "${RED}[FAIL]${NC} $*"; }

echo "=== aa-pair-analysis 环境初始化 ==="
echo ""

# ── 1. Python ──────────────────────────────────────────────
echo "── 检查 Python ──"
if command -v python3 &>/dev/null; then
    PYVER=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    ok "Python ${PYVER}"
else
    fail "未找到 python3，请先安装 Python 3.8+"
    exit 1
fi

# ── 2. Python 依赖 ─────────────────────────────────────────
echo ""
echo "── 检查 Python 依赖 ──"

PACKAGES=("pandas" "biopython")

for pkg in "${PACKAGES[@]}"; do
    if python3 -c "import ${pkg%%[>=]*}" &>/dev/null; then
        VER=$(python3 -c "import importlib.metadata; print(importlib.metadata.version('${pkg%%[>=]*}'))" 2>/dev/null || echo "unknown")
        ok "${pkg} (${VER})"
    else
        warn "${pkg} 未安装，正在安装..."
        # 尝试多种安装方式
        INSTALLED=0
        if command -v pip3 &>/dev/null; then
            pip3 install "$pkg" --quiet && INSTALLED=1
        fi
        if [[ $INSTALLED -eq 0 ]] && python3 -m pip --version &>/dev/null 2>&1; then
            python3 -m pip install "$pkg" --quiet && INSTALLED=1
        fi
        if [[ $INSTALLED -eq 0 ]] && command -v apt-get &>/dev/null; then
            # 映射 pip 包名到 apt 包名
            APT_PKG=""
            case "$pkg" in
                pandas)    APT_PKG="python3-pandas" ;;
                biopython) APT_PKG="python3-biopython" ;;
            esac
            if [[ -n "$APT_PKG" ]]; then
                sudo apt-get install -y "$APT_PKG" --quiet && INSTALLED=1
            fi
        fi
        if [[ $INSTALLED -eq 1 ]]; then
            ok "${pkg} 安装完成"
        else
            fail "${pkg} 安装失败，请手动执行：pip install ${pkg}"
            exit 1
        fi
    fi
done

# ── 3. ClustalOmega ────────────────────────────────────────
echo ""
echo "── 检查 ClustalOmega ──"

if command -v clustalo &>/dev/null; then
    VER=$(clustalo --version 2>&1 | head -1)
    ok "clustalo (${VER})"
else
    warn "clustalo 未安装，尝试自动安装..."

    OS=$(uname -s)
    ARCH=$(uname -m)

    if [[ "$OS" == "Linux" ]]; then
        # 尝试包管理器
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y clustalo 2>/dev/null && ok "clustalo 安装完成（apt）" && CLUSTALO_DONE=1
        elif command -v conda &>/dev/null; then
            conda install -y -c bioconda clustalo 2>/dev/null && ok "clustalo 安装完成（conda）" && CLUSTALO_DONE=1
        fi

        # 若包管理器未成功，下载预编译二进制
        if [[ -z "$CLUSTALO_DONE" ]]; then
            warn "尝试下载预编译二进制..."
            INSTALL_DIR="$HOME/.local/bin"
            mkdir -p "$INSTALL_DIR"

            if [[ "$ARCH" == "x86_64" ]]; then
                URL="http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64"
            else
                fail "未找到适配 ${ARCH} 的预编译包，请手动安装 clustalo"
                echo "    参考：http://www.clustal.org/omega/"
                exit 1
            fi

            curl -fsSL "$URL" -o "$INSTALL_DIR/clustalo"
            chmod +x "$INSTALL_DIR/clustalo"

            # 确保在PATH中
            if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
                echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
                export PATH="$HOME/.local/bin:$PATH"
            fi
            ok "clustalo 下载完成 → ${INSTALL_DIR}/clustalo"
        fi

    elif [[ "$OS" == "Darwin" ]]; then
        if command -v brew &>/dev/null; then
            brew install clustal-omega && ok "clustalo 安装完成（brew）"
        elif command -v conda &>/dev/null; then
            conda install -y -c bioconda clustalo && ok "clustalo 安装完成（conda）"
        else
            fail "未找到 brew 或 conda，请手动安装 clustal-omega"
            echo "    Homebrew: brew install clustal-omega"
            echo "    Conda:    conda install -c bioconda clustalo"
            exit 1
        fi

    else
        fail "不支持的操作系统：${OS}，请手动安装 clustal-omega"
        echo "    参考：http://www.clustal.org/omega/"
        exit 1
    fi
fi

# ── 4. 最终验证 ────────────────────────────────────────────
echo ""
echo "── 最终验证 ──"
python3 - <<'PYEOF'
import sys
errors = []
for pkg in ['pandas']:
    try: __import__(pkg)
    except ImportError: errors.append(pkg)
if errors:
    print(f"[FAIL] 缺少 Python 包：{errors}")
    sys.exit(1)
print("[OK]  Python 依赖全部就绪")
PYEOF

if command -v clustalo &>/dev/null; then
    ok "clustalo 可用"
else
    fail "clustalo 未找到，请检查 PATH 或手动安装"
    exit 1
fi

echo ""
echo "=== 环境初始化完成，可以运行分析 ==="
echo ""
echo "  # 完整流程（FASTA → MSA → 结果）"
echo "  python species_analysis_workflow.py 任务名 数据目录"
echo ""
echo "  # PDF批量分析"
echo "  python run_pdf_analysis.py"
