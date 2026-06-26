#!/bin/bash

# Task Management Skill 构建脚本
# 只支持 macOS Apple Silicon (ARM64)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION="0.4.3"
BINARY_NAME="task-skill"

echo "🔨 Task Management Skill v${VERSION} 构建脚本"
echo "============================================"
echo ""

# 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
rm -f "$BINARY_NAME" "$BINARY_NAME"-*
echo "✓ 清理完成"
echo ""

# 检查 Go 环境
echo "📋 检查 Go 环境..."
if ! command -v go &> /dev/null; then
    echo "❌ 错误：未找到 Go 环境"
    echo "请先安装 Go: https://golang.org/dl/"
    exit 1
fi

GO_VERSION=$(go version)
echo "✓ $GO_VERSION"
echo ""

# 构建 macOS ARM64 版本
echo "🔨 构建 macOS ARM64 版本..."
GOOS=darwin GOARCH=arm64 go build -o "$BINARY_NAME" -ldflags "-s -w -X main.version=$VERSION" .
echo "✓ 构建完成：$BINARY_NAME"
echo ""

# 验证
echo "✅ 验证构建..."
if [ -f "$BINARY_NAME" ]; then
    chmod +x "$BINARY_NAME"
    echo "✓ 二进制文件已创建并设置执行权限"
    
    # 检查架构
    ARCH=$(file "$BINARY_NAME" | grep -o "arm64\|x86_64" || echo "unknown")
    echo "✓ 架构：$ARCH"
    
    # 测试 CLI 模式
    echo "🧪 测试 CLI 模式..."
    RESULT=$(echo '{"function": "get_dashboard_stats"}' | ./"$BINARY_NAME" 2>&1)
    if echo "$RESULT" | grep -q "total"; then
        echo "✓ CLI 模式测试通过"
    else
        echo "⚠ CLI 模式测试失败"
        echo "输出：$RESULT"
    fi
else
    echo "❌ 构建失败"
    exit 1
fi

echo ""
echo "============================================"
echo "✅ 构建成功！"
echo ""
echo "运行方式："
echo "  ./task-skill --server    # 启动 Web 服务器"
echo "  echo '{\"function\": \"get_dashboard_stats\"}' | ./task-skill  # CLI 模式"
echo ""
echo "Web 访问："
echo "  http://localhost:8080"
echo ""
