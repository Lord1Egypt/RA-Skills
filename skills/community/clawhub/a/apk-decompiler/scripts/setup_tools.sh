#!/bin/bash
# setup_tools.sh - 下载并设置 APK 反编译工具
# 用法: ./setup_tools.sh

set -e

TOOLS_DIR="${TOOLS_DIR:-$HOME/.apk-tools}"
mkdir -p "$TOOLS_DIR"

echo "🔧 设置 APK 反编译工具..."
echo "工具目录: $TOOLS_DIR"

# 检查 Java
if ! command -v java &> /dev/null; then
    echo "❌ 需要安装 Java 运行时"
    exit 1
fi

# 下载 baksmali (DEX -> Smali)
if [ ! -f "$TOOLS_DIR/baksmali.jar" ]; then
    echo "📥 下载 baksmali..."
    curl -L -o "$TOOLS_DIR/baksmali.jar" \
        "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar"
fi

# 下载 smali (Smali -> DEX)
if [ ! -f "$TOOLS_DIR/smali.jar" ]; then
    echo "📥 下载 smali..."
    curl -L -o "$TOOLS_DIR/smali.jar" \
        "https://bitbucket.org/JesusFreke/smali/downloads/smali-2.5.2.jar"
fi

# 下载 apktool (资源解码)
if [ ! -f "$TOOLS_DIR/apktool.jar" ]; then
    echo "📥 下载 apktool..."
    curl -L -o "$TOOLS_DIR/apktool.jar" \
        "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.10.0.jar"
fi

# 下载 dex2jar (DEX -> JAR)
if [ ! -f "$TOOLS_DIR/dex2jar.zip" ]; then
    echo "📥 下载 dex2jar..."
    curl -L -o "$TOOLS_DIR/dex2jar.zip" \
        "https://github.com/pxb1988/dex2jar/releases/download/v2.4/dex-tools-v2.4.zip"
    cd "$TOOLS_DIR"
    unzip -o dex2jar.zip
    mv dex-tools-v2.4 dex2jar
    chmod +x dex2jar/*.sh
fi

# 下载 uber-apk-signer (APK 签名)
if [ ! -f "$TOOLS_DIR/uber-apk-signer.jar" ]; then
    echo "📥 下载 uber-apk-signer..."
    curl -L -o "$TOOLS_DIR/uber-apk-signer.jar" \
        "https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar"
fi

echo ""
echo "✅ 工具设置完成！"
echo ""
echo "可用工具:"
echo "  - baksmali.jar   : DEX → Smali 反编译"
echo "  - smali.jar      : Smali → DEX 编译"
echo "  - apktool.jar    : 资源解码/打包"
echo "  - dex2jar/       : DEX → JAR 转换"
echo "  - uber-apk-signer.jar : APK 签名"
