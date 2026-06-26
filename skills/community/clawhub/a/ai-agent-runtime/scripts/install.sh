#!/bin/bash
# FastClaw macOS/Linux 一键安装脚本
# 运行方式：
# curl -fsSL https://raw.githubusercontent.com/fastclaw-ai/fastclaw/main/install.sh | bash

set -e

VERSION="v0.24.0"
INSTALL_DIR="${HOME}/AI/FastClaw"

echo "=== FastClaw Installer ==="
echo "Version: ${VERSION}"
echo "Install Dir: ${INSTALL_DIR}"
echo ""

# 检测系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ $(uname -m) == "arm64" ]]; then
        ARCH="darwin_arm64"
    else
        ARCH="darwin_amd64"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ARCH="linux_amd64"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# 检测是否已安装
if command -v fastclaw &> /dev/null; then
    echo "FastClaw is already installed at: $(which fastclaw)"
    read -p "Reinstall? (y/N): " confirm
    if [[ "$confirm" != "y" ]]; then
        echo "Installation cancelled."
        exit 0
    fi
fi

# 创建安装目录
mkdir -p "${INSTALL_DIR}"

# 下载
echo "[1/3] Downloading FastClaw (${ARCH})..."
DOWNLOAD_URL="https://github.com/fastclaw-ai/fastclaw/releases/download/${VERSION}/fastclaw_${ARCH}.tar.gz"
curl -fsSL "${DOWNLOAD_URL}" -o "${INSTALL_DIR}/fastclaw.tar.gz"

# 解压
echo "[2/3] Extracting..."
tar -xzf "${INSTALL_DIR}/fastclaw.tar.gz" -C "${INSTALL_DIR}"
rm "${INSTALL_DIR}/fastclaw.tar.gz"

# 安装到 PATH
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ -w "/usr/local/bin" ]]; then
        mv "${INSTALL_DIR}/fastclaw" /usr/local/bin/fastclaw
    else
        echo ""
        echo "Note: /usr/local/bin is not writable."
        echo "Add '${INSTALL_DIR}' to your PATH, or run:"
        echo "  sudo mv ${INSTALL_DIR}/fastclaw /usr/local/bin/fastclaw"
    fi
else
    if [[ -w "/usr/local/bin" ]]; then
        mv "${INSTALL_DIR}/fastclaw" /usr/local/bin/fastclaw
    else
        echo ""
        echo "Note: /usr/local/bin is not writable."
        echo "Add '${INSTALL_DIR}' to your PATH, or run:"
        echo "  sudo mv ${INSTALL_DIR}/fastclaw /usr/local/bin/fastclaw"
    fi
fi

# 完成
echo "[3/3] Done!"
echo ""
echo "=== Next Steps ==="
echo "1. 启动 FastClaw:"
echo "   fastclaw"
echo ""
echo "2. 打开浏览器访问:"
echo "   http://localhost:18953"
echo ""
echo "祝你使用愉快！"
