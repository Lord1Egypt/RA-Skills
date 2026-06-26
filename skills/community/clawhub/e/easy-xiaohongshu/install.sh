#!/bin/bash
# Easy-xiaohongshu 安装脚本
# 一键配置环境、安装依赖、引导 API Key

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/config"
LOCAL_CONFIG="$CONFIG_DIR/local-config.json"

echo "✨ Easy-xiaohongshu 安装向导"
echo "============================"
echo ""

# 1. 检查 Python
echo "📌 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ 未找到 Python 3，请先安装 Python 3.8+"
    exit 1
fi

# 2. 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip3 install -r "$SCRIPT_DIR/requirements.txt" -q
    echo "✅ 依赖安装完成"
else
    echo "⚠️ 未找到 requirements.txt，跳过依赖安装"
fi

# 3. 创建配置目录
echo ""
echo "🔧 配置目录检查..."
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
    echo "✅ 创建配置目录：$CONFIG_DIR"
else
    echo "✅ 配置目录已存在"
fi

# 4. 引导 API Key 配置
echo ""
echo "🔑 API Key 配置"
echo "----------------"

if [ -f "$LOCAL_CONFIG" ]; then
    echo "⚠️ 检测到已有配置文件：$LOCAL_CONFIG"
    echo "   是否覆盖？(y/N): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "   将覆盖现有配置..."
    else
        echo "   跳过配置，保留现有文件"
        goto_end=true
    fi
fi

if [ -z "$goto_end" ]; then
    echo ""
    echo "请输入你的 API Key（来自 z.3i0.cn）："
    read -r API_KEY
    if [ -z "$API_KEY" ]; then
        echo "❌ API Key 不能为空"
        exit 1
    fi
    
    echo ""
    echo "请选择你的小红书账号类型："
    echo "  1) 科技博主"
    echo "  2) 亲子博主"
    echo "  3) 美妆博主"
    echo "  4) 健身博主"
    echo "  5) 美食博主"
    echo "  6) 学习博主"
    echo "  7) 旅行博主"
    echo "  8) 职场博主"
    echo "  9) 漫画博主"
    echo "  10) 摄影博主"
    echo "  11) 穿搭博主"
    echo "  12) 游戏博主"
    echo "  13) 音乐博主"
    echo ""
    echo "输入编号 (1-13):"
    read -r ACCOUNT_TYPE_NUM
    
    # 映射编号到账号类型
    case $ACCOUNT_TYPE_NUM in
        1) ACCOUNT_TYPE="科技博主" ;;
        2) ACCOUNT_TYPE="亲子博主" ;;
        3) ACCOUNT_TYPE="美妆博主" ;;
        4) ACCOUNT_TYPE="健身博主" ;;
        5) ACCOUNT_TYPE="美食博主" ;;
        6) ACCOUNT_TYPE="学习博主" ;;
        7) ACCOUNT_TYPE="旅行博主" ;;
        8) ACCOUNT_TYPE="职场博主" ;;
        9) ACCOUNT_TYPE="漫画博主" ;;
        10) ACCOUNT_TYPE="摄影博主" ;;
        11) ACCOUNT_TYPE="穿搭博主" ;;
        12) ACCOUNT_TYPE="游戏博主" ;;
        13) ACCOUNT_TYPE="音乐博主" ;;
        *) ACCOUNT_TYPE="科技博主" ;;
    esac
    
    echo ""
    echo "请输入内容方向（如：AI 工具、数码测评）："
    read -r CONTENT_DIRECTION
    
    echo ""
    echo "请输入目标用户（如：大学生、职场新人）："
    read -r TARGET_AUDIENCE
    
    # 写入配置文件
    API_KEY="$API_KEY" \
    ACCOUNT_TYPE="$ACCOUNT_TYPE" \
    CONTENT_DIRECTION="$CONTENT_DIRECTION" \
    TARGET_AUDIENCE="$TARGET_AUDIENCE" \
    python3 - "$LOCAL_CONFIG" << 'PY'
import json
import os
import sys

local_config = sys.argv[1]
data = {
    "api": {
        "key": os.environ.get("API_KEY", ""),
        "base_url": "https://z.3i0.cn/v1beta",
        "model": "gemini-3.1-flash-image-preview",
    },
    "user_preferences": {
        "account_type": os.environ.get("ACCOUNT_TYPE", "科技博主"),
        "content_direction": os.environ.get("CONTENT_DIRECTION", ""),
        "target_audience": os.environ.get("TARGET_AUDIENCE", ""),
    },
    "mcp": {
        "url": "http://localhost:18060/mcp",
        "timeout_seconds": 30,
    },
}
with open(local_config, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
    
    echo ""
    echo "✅ 配置已保存到：$LOCAL_CONFIG"
fi

# 5. 检查 MCP 服务
echo ""
echo "🔌 检查 xiaohongshu-mcp 服务..."
if command -v curl &> /dev/null; then
    if curl -s http://localhost:18060/mcp > /dev/null 2>&1; then
        echo "✅ MCP 服务运行中"
    else
        echo "⚠️  MCP 服务未响应，发布功能需要 xhs-mac-mcp 技能"
        echo "   参考：~/clawd/skills/xhs-mac-mcp/SKILL.md"
    fi
else
    echo "⚠️  未找到 curl，跳过 MCP 检查"
fi

# 6. 创建输出目录
echo ""
echo "📁 创建输出目录..."
OUTPUT_DIR="$SCRIPT_DIR/generated_images"
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo "✅ 创建目录：$OUTPUT_DIR"
else
    echo "✅ 输出目录已存在"
fi

echo ""
echo "============================"
echo "🎉 安装完成！"
echo ""
echo "使用方法："
echo "  1. 发送创作主题："
echo "     我想发一篇主题为【xxxxxx】的小红书，帮我制作内容"
echo ""
echo "  2. 确认文案和图片后，自动发布"
echo ""
echo "============================"
