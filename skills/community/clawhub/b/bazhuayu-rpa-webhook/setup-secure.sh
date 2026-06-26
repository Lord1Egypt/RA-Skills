#!/bin/bash
#
# 八爪鱼 RPA Webhook - 快速安全配置向导
# 
# 功能：
# 1. 收集配置信息
# 2. 生成环境变量配置示例（不自动修改 shell 配置）
# 3. 更新配置文件
# 4. 验证配置
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

echo "🔐 八爪鱼 RPA Webhook - 快速安全配置向导"
echo "========================================"
echo ""
echo "⚠️  重要提示："
echo "   本脚本不会自动修改你的 shell 配置文件 (~/.bashrc 或 ~/.zshrc)"
echo "   配置完成后，请手动将环境变量添加到你的 shell 配置中"
echo ""

# 检查是否已有配置
if [ -f "$CONFIG_FILE" ]; then
    echo "📖 检测到现有配置文件"
    
    # 检查是否已使用环境变量
    CURRENT_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('key', ''))" 2>/dev/null || echo "")
    
    if [ -z "$CURRENT_KEY" ]; then
        echo "✅ 配置文件已使用安全模式 (密钥从环境变量读取)"
    else
        echo "⚠️  检测到密钥存储在配置文件中"
        echo ""
        read -p "是否迁移到环境变量模式？(y/n) [默认:y] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]] || [ -z "$REPLY" ]; then
            echo ""
            echo "🚀 运行迁移脚本..."
            "$SCRIPT_DIR/migrate-to-env.sh"
            exit 0
        else
            echo "ℹ️  跳过迁移，继续配置..."
        fi
    fi
    echo ""
fi

# 收集配置信息
echo "--- 配置信息 ---"
echo ""

if [ -f "$CONFIG_FILE" ]; then
    CURRENT_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('url', ''))" 2>/dev/null || echo "")
    if [ -n "$CURRENT_URL" ]; then
        echo "当前 Webhook URL: ${CURRENT_URL:0:20}...${CURRENT_URL: -20}"
        read -p "是否修改？(y/n) [默认:n] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "请输入新的 Webhook URL: " WEBHOOK_URL
        else
            WEBHOOK_URL="$CURRENT_URL"
        fi
    else
        read -p "请输入 Webhook URL: " WEBHOOK_URL
    fi
else
    read -p "请输入 Webhook URL: " WEBHOOK_URL
fi

read -p "请输入签名密钥 (Key): " WEBHOOK_KEY

# 验证输入
if [ -z "$WEBHOOK_URL" ]; then
    echo "❌ 错误：Webhook URL 不能为空"
    exit 1
fi

if [ -z "$WEBHOOK_KEY" ]; then
    echo "❌ 错误：签名密钥不能为空"
    exit 1
fi

if [ ${#WEBHOOK_KEY} -lt 8 ]; then
    echo "⚠️  警告：密钥长度较短 (${#WEBHOOK_KEY} 字符)，建议使用更安全的密钥"
    read -p "是否继续？(y/n) [默认:n] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# 生成环境变量配置示例
echo "📝 生成环境变量配置..."
echo ""
echo "=========================================="
echo "📌 请将以下内容添加到你的 shell 配置文件:"
echo "=========================================="
echo ""

ENV_CONFIG="# 八爪鱼 RPA Webhook 配置
# 创建于：$(date '+%Y-%m-%d %H:%M:%S')
# 请将以下两行添加到 ~/.bashrc 或 ~/.zshrc
export BAZHUAYU_WEBHOOK_URL=\"$WEBHOOK_URL\"
export BAZHUAYU_WEBHOOK_KEY=\"$WEBHOOK_KEY\""

echo "$ENV_CONFIG"
echo ""
echo "=========================================="
echo ""

# 保存到临时文件供用户参考
ENV_FILE="$SCRIPT_DIR/.env.example"
echo "$ENV_CONFIG" > "$ENV_FILE"
chmod 600 "$ENV_FILE"
echo "✅ 配置示例已保存到：$ENV_FILE"
echo ""

# 设置当前会话（可选）
read -p "是否为当前终端会话临时设置环境变量？(y/n) [默认:y] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [ -z "$REPLY" ]; then
    export BAZHUAYU_WEBHOOK_URL="$WEBHOOK_URL"
    export BAZHUAYU_WEBHOOK_KEY="$WEBHOOK_KEY"
    echo "✅ 当前会话环境变量已设置（仅本次终端有效）"
else
    echo "ℹ️  跳过当前会话设置"
fi

echo ""

# 更新/创建配置文件
echo "🔧 更新配置文件..."

python3 << EOF
import json
from pathlib import Path
import os

config_file = Path("$CONFIG_FILE")

# 尝试读取现有配置
if config_file.exists():
    config = json.load(open(config_file))
else:
    config = {
        'paramNames': [],
        'defaultParams': {}
    }

# 更新配置 (URL 可存储，密钥留空)
config['url'] = "$WEBHOOK_URL"
config['key'] = ''  # 从环境变量读取

# 安全标记
config['security'] = {
    'keyFromEnv': True,
    'urlFromEnv': False,
    'createdAt': "$(date '+%Y-%m-%d %H:%M:%S')",
    'version': '2.0'
}

# 保存
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# 设置权限
os.chmod(config_file, 0o600)

print("✅ 配置文件已更新")
print(f"   位置：{config_file.absolute()}")
print(f"   权限：600 (仅所有者可读写)")
EOF

echo ""
echo "=== 配置完成 ==="
echo ""
echo "📌 下一步（必须完成）:"
echo ""
echo "  1️⃣  手动添加环境变量到 shell 配置:"
echo "     方式一：复制上面的 export 命令，添加到 ~/.bashrc 或 ~/.zshrc"
echo "     方式二：编辑 $ENV_FILE，然后手动复制内容"
echo ""
echo "  2️⃣  使环境变量生效:"
echo "     source ~/.bashrc  # 或 source ~/.zshrc"
echo ""
echo "  3️⃣  验证配置:"
echo "     python3 bazhuayu-webhook.py secure-check"
echo ""
echo "  4️⃣  测试连接:"
echo "     python3 bazhuayu-webhook.py test"
echo ""
echo "  5️⃣  运行任务:"
echo "     python3 bazhuayu-webhook.py run"
echo ""
echo "🔐 安全提示:"
echo "   - 签名密钥存储在环境变量中，不会写入配置文件"
echo "   - 配置文件权限已设置为 600"
echo "   - 不要将 config.json 提交到版本控制"
echo "   - 不要将 .env.example 提交到版本控制"
echo ""
