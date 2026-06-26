#!/bin/bash
# CFGPU API Configuration Check Script

echo "=== CFGPU API 配置检查 ==="
echo ""

# Check jq
echo "1. 检查 jq 工具..."
if command -v jq &> /dev/null; then
    echo "   ✅ jq 已安装: $(jq --version)"
else
    echo "   ❌ jq 未安装，请运行: apt-get install jq"
fi

# Check curl
echo ""
echo "2. 检查 curl 工具..."
if command -v curl &> /dev/null; then
    echo "   ✅ curl 已安装: $(curl --version | head -1)"
else
    echo "   ❌ curl 未安装，请运行: apt-get install curl"
fi

# Check API Token
echo ""
echo "3. 检查 API Token 配置..."

TOKEN_SOURCE=""
TOKEN_VALUE=""

# Check environment variable
if [ -n "$CFGPU_API_TOKEN" ]; then
    TOKEN_SOURCE="环境变量"
    TOKEN_VALUE="$CFGPU_API_TOKEN"
fi

# Check token file
if [ -f ~/.cfgpu/token ]; then
    if [ -z "$TOKEN_SOURCE" ]; then
        TOKEN_SOURCE="配置文件"
        TOKEN_VALUE=$(cat ~/.cfgpu/token 2>/dev/null | tr -d '\n')
    else
        echo "   ⚠️  同时找到环境变量和配置文件，优先使用环境变量"
    fi
fi

if [ -n "$TOKEN_SOURCE" ]; then
    # Mask token for security
    TOKEN_LENGTH=${#TOKEN_VALUE}
    if [ $TOKEN_LENGTH -gt 8 ]; then
        MASKED_TOKEN="${TOKEN_VALUE:0:4}...${TOKEN_VALUE: -4}"
    else
        MASKED_TOKEN="***"
    fi
    
    echo "   ✅ API Token 已配置 (来源: $TOKEN_SOURCE)"
    echo "   🔑 Token: $MASKED_TOKEN"
    
    # Test API connectivity
    echo ""
    echo "4. 测试 API 连接..."
    if [ -n "$CFGPU_API_TOKEN" ]; then
        TEST_TOKEN="$CFGPU_API_TOKEN"
    else
        TEST_TOKEN="$TOKEN_VALUE"
    fi
    
    RESPONSE=$(curl -s -H "Authorization: $TEST_TOKEN" \
        https://api.cfgpu.com/userapi/v1/region/list 2>/dev/null)
    
    if echo "$RESPONSE" | grep -q "success" || echo "$RESPONSE" | grep -q "code"; then
        echo "   ✅ API 连接成功"
        
        # Try to parse response
        if echo "$RESPONSE" | jq -e . >/dev/null 2>&1; then
            REGION_COUNT=$(echo "$RESPONSE" | jq 'length')
            echo "   📍 可用区域数量: $REGION_COUNT"
            
            if [ $REGION_COUNT -gt 0 ]; then
                echo "   🌍 可用区域:"
                echo "$RESPONSE" | jq -r '.[] | "     - \(.name) (\(.code))"'
            fi
        fi
    else
        echo "   ❌ API 连接失败"
        echo "   响应: $RESPONSE"
    fi
else
    echo "   ❌ API Token 未配置"
    echo ""
    echo "   配置方法:"
    echo "   1. 设置环境变量:"
    echo "      export CFGPU_API_TOKEN='YOUR_API_TOKEN'"
    echo ""
    echo "   2. 或创建配置文件:"
    echo "      echo 'YOUR_API_TOKEN' > ~/.cfgpu/token"
    echo "      chmod 600 ~/.cfgpu/token"
fi

# Check script permissions
echo ""
echo "5. 检查脚本权限..."
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for script in "$SCRIPTS_DIR"/*.sh; do
    if [ -x "$script" ]; then
        echo "   ✅ $(basename "$script"): 可执行"
    else
        echo "   ⚠️  $(basename "$script"): 不可执行，运行: chmod +x $script"
    fi
done

echo ""
echo "=== 检查完成 ==="
echo ""
echo "下一步:"
echo "1. 如果API Token未配置，请先配置"
echo "2. 运行 ./cfgpu-helper.sh list-regions 查看可用区域"
echo "3. 运行 ./cfgpu-helper.sh list-gpus 查看可用GPU类型"
echo "4. 运行 ./cfgpu-helper.sh quick-create 交互式创建GPU容器"