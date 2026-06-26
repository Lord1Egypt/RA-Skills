#!/bin/bash
#
# Atlas Cloud API Key 配置脚本
# 用于设置和验证 API Key
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Atlas Cloud API Key 配置工具  ${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查是否已配置
if [ -n "$ATLASCLOUD_API_KEY" ]; then
    echo -e "${GREEN}✓ 已检测到环境变量 ATLASCLOUD_API_KEY${NC}"
    echo -e "  当前值: ${ATLASCLOUD_API_KEY:0:8}...${ATLASCLOUD_API_KEY: -4}"
    echo ""
    read -p "是否重新配置? (y/N): " RECONFIGURE
    if [[ ! "$RECONFIGURE" =~ ^[Yy]$ ]]; then
        echo "保持现有配置，退出。"
        exit 0
    fi
fi

# 提示用户输入 API Key
echo -e "${YELLOW}请输入您的 Atlas Cloud API Key:${NC}"
echo -e "(可在 https://console.atlascloud.ai/ 获取)"
echo ""
read -s -p "API Key: " API_KEY
echo ""

# 验证 API Key 格式
if [ -z "$API_KEY" ]; then
    echo -e "${RED}✗ API Key 不能为空${NC}"
    exit 1
fi

# 测试 API Key 是否有效
echo -e "${YELLOW}正在验证 API Key...${NC}"

RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    "https://api.atlascloud.ai/v1/models" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ API Key 验证成功！${NC}"
else
    echo -e "${RED}✗ API Key 验证失败 (HTTP $HTTP_CODE)${NC}"
    echo -e "  响应: $BODY"
    echo ""
    read -p "是否仍然继续配置? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检测 shell 配置文件
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

if [ -n "$SHELL_RC" ]; then
    echo ""
    echo -e "${YELLOW}检测到 Shell 配置文件: $SHELL_RC${NC}"
    read -p "是否将 API Key 添加到该文件? (Y/n): " ADD_TO_RC
    
    if [[ ! "$ADD_TO_RC" =~ ^[Nn]$ ]]; then
        # 检查是否已存在
        if grep -q "ATLASCLOUD_API_KEY" "$SHELL_RC"; then
            # 更新现有配置
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/^export ATLASCLOUD_API_KEY=.*/export ATLASCLOUD_API_KEY=\"$API_KEY\"/" "$SHELL_RC"
            else
                sed -i "s/^export ATLASCLOUD_API_KEY=.*/export ATLASCLOUD_API_KEY=\"$API_KEY\"/" "$SHELL_RC"
            fi
            echo -e "${GREEN}✓ 已更新 $SHELL_RC 中的 ATLASCLOUD_API_KEY${NC}"
        else
            # 添加新配置
            echo "" >> "$SHELL_RC"
            echo "# Atlas Cloud API Key (added by freeads-snap-ad skill)" >> "$SHELL_RC"
            echo "export ATLASCLOUD_API_KEY=\"$API_KEY\"" >> "$SHELL_RC"
            echo -e "${GREEN}✓ 已添加 ATLASCLOUD_API_KEY 到 $SHELL_RC${NC}"
        fi
        
        echo ""
        echo -e "${YELLOW}请运行以下命令使配置生效:${NC}"
        echo -e "  source $SHELL_RC"
    fi
else
    echo ""
    echo -e "${YELLOW}未检测到标准 Shell 配置文件${NC}"
    echo -e "请手动将以下内容添加到您的 Shell 配置文件:"
    echo ""
    echo -e "  export ATLASCLOUD_API_KEY=\"$API_KEY\""
fi

# 导出到当前 session
export ATLASCLOUD_API_KEY="$API_KEY"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  配置完成！${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "您现在可以使用 '随手拍广告' 功能了。"
echo -e "使用示例: 向 CodeFlicker 发送 '帮我生成产品广告'"
