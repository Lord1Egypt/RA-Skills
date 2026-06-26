#!/bin/bash
# 飞书插件安装脚本
# 用法：./install-feishu.sh

set -e

echo "📱 飞书插件安装"
echo "==============="

CONFIG_DIR=~/.openclaw/config
PLUGINS_DIR=~/.openclaw/plugins

# 创建配置目录
mkdir -p "$CONFIG_DIR"
mkdir -p "$PLUGINS_DIR"

# 获取飞书应用凭证
echo ""
echo "请从飞书开放平台获取以下信息："
echo "1. 访问 https://open.feishu.cn/app"
echo "2. 创建自建应用"
echo "3. 获取 App ID 和 App Secret"
echo ""

read -p "请输入 App ID (cli_xxxxxxxxxxxxx): " APP_ID
read -sp "请输入 App Secret: " APP_SECRET
echo ""
read -sp "请输入 Verification Token: " VERIFICATION_TOKEN
echo ""
read -sp "请输入 Encrypt Key (可选): " ENCRYPT_KEY
echo ""

# 验证必填项
if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ] || [ -z "$VERIFICATION_TOKEN" ]; then
    echo "❌ App ID、App Secret 和 Verification Token 不能为空"
    exit 1
fi

# 备份旧配置
if [ -f "$CONFIG_DIR/feishu.json" ]; then
    cp "$CONFIG_DIR/feishu.json" "$CONFIG_DIR/feishu.json.bak.$(date +%Y%m%d%H%M%S)"
fi

# 创建飞书配置
echo "⚙️  创建飞书配置..."
cat > "$CONFIG_DIR/feishu.json" << EOF
{
  "appId": "${APP_ID}",
  "appSecret": "${APP_SECRET}",
  "verificationToken": "${VERIFICATION_TOKEN}",
  "encryptKey": "${ENCRYPT_KEY}",
  "enabled": true
}
EOF

echo "✅ 飞书配置已保存到：$CONFIG_DIR/feishu.json"

# 检查是否已有飞书插件
echo ""
echo "📦 检查飞书插件..."
if [ -d "$PLUGINS_DIR/feishu" ]; then
    echo "ℹ️  飞书插件已存在"
    read -p "是否重新安装？(y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PLUGINS_DIR/feishu"
    else
        echo "✅ 跳过安装"
    fi
fi

# 安装飞书插件
if [ ! -d "$PLUGINS_DIR/feishu" ]; then
    echo "📥 安装飞书插件..."
    
    # 尝试从 GitHub 克隆
    if command -v git &> /dev/null; then
        git clone https://github.com/openclaw/feishu-plugin.git "$PLUGINS_DIR/feishu" 2>/dev/null || \
        echo "⚠️  无法从 GitHub 克隆，请手动安装"
    fi
    
    if [ -d "$PLUGINS_DIR/feishu" ]; then
        cd "$PLUGINS_DIR/feishu"
        pnpm install
        echo "✅ 飞书插件安装完成"
    else
        echo "⚠️  飞书插件目录不存在，请手动安装"
        echo "参考：https://docs.openclaw.ai/plugins"
    fi
fi

# 启用飞书通道
echo ""
echo "🔌 启用飞书通道..."
if command -v openclaw &> /dev/null; then
    openclaw channels enable feishu 2>/dev/null || \
    echo "⚠️  启用失败，请手动配置"
fi

echo ""
echo "✅ 飞书插件配置完成！"
echo ""
echo "下一步："
echo "1. 在飞书开放平台配置事件订阅 URL"
echo "2. 运行 'openclaw gateway restart' 重启网关"
echo "3. 运行 'openclaw channels status feishu' 查看状态"
