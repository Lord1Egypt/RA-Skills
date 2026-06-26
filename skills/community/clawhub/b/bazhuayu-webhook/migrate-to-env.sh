#!/bin/bash
#
# 八爪鱼 RPA Webhook - 迁移到环境变量配置
# 
# 功能：
# 1. 从 config.json 提取敏感信息
# 2. 生成环境变量配置示例（不自动修改 shell 配置）
# 3. 更新 config.json 移除敏感信息
# 4. 备份原配置
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"
BACKUP_FILE="$SCRIPT_DIR/config.json.backup.$(date +%Y%m%d%H%M%S)"

echo "=== 八爪鱼 RPA Webhook - 迁移到环境变量配置 ==="
echo ""
echo "⚠️  重要提示："
echo "   本脚本不会自动修改你的 shell 配置文件 (~/.bashrc 或 ~/.zshrc)"
echo "   迁移完成后，请手动将环境变量添加到你的 shell 配置中"
echo ""

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 错误：配置文件不存在：$CONFIG_FILE"
    exit 1
fi

# 备份原配置
echo "📦 备份原配置文件..."
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "✅ 备份完成：$BACKUP_FILE"
echo ""

# 读取配置
echo "📖 读取配置..."
CURRENT_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('key', ''))")
CURRENT_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('url', ''))")

if [ -z "$CURRENT_KEY" ]; then
    echo "ℹ️  签名密钥为空，可能已使用环境变量"
fi

if [ -z "$CURRENT_URL" ]; then
    echo "ℹ️  Webhook URL 为空，可能已使用环境变量"
fi

echo ""

# 生成环境变量配置示例
echo "📝 生成环境变量配置示例..."
echo ""
echo "=========================================="
echo "📌 请将以下内容添加到你的 shell 配置文件:"
echo "=========================================="
echo ""

ENV_CONFIG="# 八爪鱼 RPA Webhook 配置 (从 config.json 迁移)
# 创建于：$(date '+%Y-%m-%d %H:%M:%S')
# 请将以下行添加到 ~/.bashrc 或 ~/.zshrc"

if [ -n "$CURRENT_KEY" ]; then
    ENV_CONFIG="$ENV_CONFIG
export BAZHUAYU_WEBHOOK_KEY=\"$CURRENT_KEY\""
fi

if [ -n "$CURRENT_URL" ]; then
    ENV_CONFIG="$ENV_CONFIG
export BAZHUAYU_WEBHOOK_URL=\"$CURRENT_URL\""
fi

echo "$ENV_CONFIG"
echo ""
echo "=========================================="
echo ""

# 保存到临时文件供用户参考
ENV_FILE="$SCRIPT_DIR/.env.migrated"
echo "$ENV_CONFIG" > "$ENV_FILE"
chmod 600 "$ENV_FILE"
echo "✅ 配置示例已保存到：$ENV_FILE"
echo ""

# 设置当前会话（可选）
read -p "是否为当前终端会话临时设置环境变量？(y/n) [默认:y] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [ -z "$REPLY" ]; then
    if [ -n "$CURRENT_KEY" ]; then
        export BAZHUAYU_WEBHOOK_KEY="$CURRENT_KEY"
    fi
    if [ -n "$CURRENT_URL" ]; then
        export BAZHUAYU_WEBHOOK_URL="$CURRENT_URL"
    fi
    echo "✅ 当前会话环境变量已设置（仅本次终端有效）"
else
    echo "ℹ️  跳过当前会话设置"
fi

echo ""

# 更新 config.json
echo "🔧 更新配置文件..."

python3 << EOF
import json
from pathlib import Path

config_file = Path("$CONFIG_FILE")
config = json.load(open(config_file))

# 移除敏感信息
if 'key' in config:
    config['key'] = ''  # 留空，从环境变量读取

# 更新安全标记
if 'security' not in config:
    config['security'] = {}
config['security']['keyFromEnv'] = True
config['security']['migratedAt'] = "$(date '+%Y-%m-%d %H:%M:%S')"
config['security']['version'] = '2.0'

# 保存
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# 设置权限
import os
os.chmod(config_file, 0o600)

print("✅ 配置文件已更新")
print(f"   签名密钥已清空，将从 BAZHUAYU_WEBHOOK_KEY 环境变量读取")
EOF

echo ""
echo "=== 迁移完成 ==="
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
echo "🔐 安全提示:"
echo "   - 签名密钥现在存储在环境变量中，不会写入配置文件"
echo "   - 配置文件权限已设置为 600"
echo "   - 不要将 .env.migrated 提交到版本控制"
echo ""
echo "如需回滚:"
echo "  cp $BACKUP_FILE $CONFIG_FILE"
echo ""
