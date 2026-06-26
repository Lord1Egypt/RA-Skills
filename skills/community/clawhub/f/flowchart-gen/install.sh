#!/bin/bash
#
# 安装 flowchart-gen 技能所需依赖
#
# 此脚本安装 flowchart-gen 技能所需的所有依赖：
# 1. Node.js 和 npm (如果未安装)
# 2. Mermaid CLI (@mermaid-js/mermaid-cli)
# 3. Python 依赖 (pillow, requests)

set -e

SKIP_CHROME_DOWNLOAD=${1:-true}

echo "========================================"
echo "flowchart-gen 技能依赖安装脚本"
echo "========================================"

# 检查 Node.js 和 npm
echo -e "\n1. 检查 Node.js 和 npm..."
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    echo "   ✅ Node.js 已安装: $NODE_VERSION"
    echo "   ✅ npm 已安装: $NPM_VERSION"
else
    echo "   ❌ Node.js 或 npm 未安装"
    echo "   请先安装 Node.js: https://nodejs.org/"
    echo "   或使用包管理器:"
    echo "   - Ubuntu/Debian: sudo apt install nodejs npm"
    echo "   - macOS: brew install node"
    echo "   - Arch: sudo pacman -S nodejs npm"
    exit 1
fi

# 安装 Mermaid CLI
echo -e "\n2. 安装 Mermaid CLI (@mermaid-js/mermaid-cli)..."
if [ "$SKIP_CHROME_DOWNLOAD" = "true" ]; then
    echo "   跳过 Chromium 下载，使用系统 Chrome..."
    export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1
    
    # 尝试找到系统 Chrome 路径
    CHROME_PATHS=(
        "/usr/bin/google-chrome"
        "/usr/bin/google-chrome-stable"
        "/usr/bin/chromium"
        "/usr/bin/chromium-browser"
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
    
    for path in "${CHROME_PATHS[@]}"; do
        if [ -f "$path" ]; then
            export PUPPETEER_EXECUTABLE_PATH="$path"
            echo "   找到 Chrome: $path"
            break
        fi
    done
    
    if [ -z "$PUPPETEER_EXECUTABLE_PATH" ]; then
        echo "   ⚠️  未找到系统 Chrome，可能需要手动安装"
    fi
fi

if npm install -g @mermaid-js/mermaid-cli; then
    echo "   ✅ Mermaid CLI 安装成功"
    
    # 验证安装
    if command -v mmdc &> /dev/null; then
        MMDC_VERSION=$(mmdc --version 2>/dev/null || echo "unknown")
        echo "   ✅ Mermaid CLI 验证通过: $MMDC_VERSION"
    else
        echo "   ⚠️  mmdc 命令验证失败"
        echo "   可能需要将 npm 全局 bin 目录添加到 PATH"
        echo "   export PATH=\$PATH:\$HOME/.npm-global/bin"
    fi
else
    echo "   ❌ Mermaid CLI 安装失败"
    echo "   可以尝试:"
    echo "   1. 使用 sudo 权限: sudo npm install -g @mermaid-js/mermaid-cli"
    echo "   2. 设置 npm 代理: npm config set registry https://registry.npmmirror.com"
    echo "   3. 重试安装"
    exit 1
fi

# 检查 Python
echo -e "\n3. 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ Python 已安装: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo "   ✅ Python 已安装: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "   ⚠️  Python 未安装"
    echo "   请先安装 Python: https://www.python.org/downloads/"
    echo "   或使用包管理器:"
    echo "   - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   - macOS: brew install python"
    echo "   - Arch: sudo pacman -S python python-pip"
    echo "   继续安装 Python 依赖可能会失败..."
    PYTHON_CMD=""
fi

# 安装 Python 依赖
if [ -n "$PYTHON_CMD" ]; then
    echo -e "\n4. 安装 Python 依赖 (pillow, requests)..."
    if $PYTHON_CMD -m pip install pillow requests; then
        echo "   ✅ Python 依赖安装成功"
    else
        echo "   ⚠️  Python 依赖安装失败"
        echo "   可以尝试:"
        echo "   1. 使用 pip3: pip3 install pillow requests"
        echo "   2. 使用 sudo 权限: sudo $PYTHON_CMD -m pip install pillow requests"
        echo "   3. 在虚拟环境中安装"
    fi
else
    echo -e "\n4. 跳过 Python 依赖安装（Python 未安装）"
fi

# 验证安装
echo -e "\n5. 验证安装..."
ALL_PASSED=true

# 验证 Mermaid CLI
if command -v mmdc &> /dev/null; then
    if mmdc --version &> /dev/null; then
        echo "   ✅ Mermaid CLI 可用"
    else
        echo "   ❌ Mermaid CLI 验证失败"
        ALL_PASSED=false
    fi
else
    echo "   ❌ Mermaid CLI 未找到"
    ALL_PASSED=false
fi

# 验证 Python 依赖
if [ -n "$PYTHON_CMD" ]; then
    if $PYTHON_CMD -c "import PIL, requests; print('Python 依赖验证通过')" &> /dev/null; then
        echo "   ✅ Python 依赖可用"
    else
        echo "   ⚠️  Python 依赖验证失败"
        echo "   可以稍后手动安装: $PYTHON_CMD -m pip install pillow requests"
    fi
else
    echo "   ⚠️  跳过 Python 依赖验证"
fi

echo -e "\n========================================"
if [ "$ALL_PASSED" = true ]; then
    echo "✅ 所有依赖安装成功！"
    echo -e "\n下一步:"
    echo "1. 测试技能: $PYTHON_CMD scripts/generate.py '测试流程图' -o test.png"
    echo "2. 查看帮助: $PYTHON_CMD scripts/generate.py --help"
    echo "3. 配置 API 密钥 (可选):"
    echo "   - 设置环境变量 DEEPSEEK_API_KEY"
    echo "   - 或使用 --api-key 参数"
else
    echo "⚠️  部分依赖安装失败，请查看上面的错误信息"
    echo -e "\n故障排除:"
    echo "1. 确保有足够的权限"
    echo "2. 检查网络连接"
    echo "3. 查看技能文档: SKILL.md"
fi
echo "========================================"