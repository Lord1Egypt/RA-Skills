#!/bin/bash
# Freqtrade一键部署脚本
# 用法: bash install.sh [安装目录]

set -e

INSTALL_DIR="${1:-./freqtrade}"
BIND_PORT="${BIND_PORT:-8080}"
BIND_HOST="${BIND_HOST:-0.0.0.0}"

echo "=========================================="
echo "  Freqtrade 一键部署脚本 v1.0"
echo "=========================================="
echo "安装目录: $INSTALL_DIR"
echo "WebUI端口: $BIND_PORT"
echo ""

# 1. 检查依赖
echo "[1/6] 检查系统依赖..."
command -v python3 >/dev/null 2>&1 || { echo "需要Python3"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "需要git"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "需要pip3"; exit 1; }

# 2. 克隆Freqtrade
echo "[2/6] 克隆Freqtrade..."
if [ -d "$INSTALL_DIR" ]; then
    echo "目录已存在，跳过克隆"
else
    git clone https://github.com/freqtrade/freqtrade.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 3. 安装依赖
echo "[3/6] 安装Python依赖..."
pip3 install -e . --break-system-packages

# 4. 创建配置
echo "[4/6] 创建配置文件..."
mkdir -p user_data/strategies
mkdir -p user_data/configs

if [ ! -f "user_data/config.json" ]; then
    cat > user_data/config.json << 'EOF'
{
    "max_open_trades": 1,
    "stake_currency": "USDT",
    "stake_amount": "unlimited",
    "tradable_balance_ratio": 0.99,
    "fiat_display_currency": "USD",
    "timeframe": "5m",
    "dry_run": false,
    "cancel_open_orders_on_exit": false,
    "unfilledtimeout": {
        "entry": 10,
        "exit": 10,
        "exit_timeout_count": 0,
        "unit": "minutes"
    },
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "exit_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1
    },
    "exchange": {
        "name": "binance",
        "key": "YOUR_API_KEY",
        "secret": "YOUR_API_SECRET",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "pair_whitelist": ["PEPE/USDT"],
        "pair_blacklist": []
    },
    "pairlists": [
        {"method": "StaticPairList"}
    ],
    "telegram": {
        "enabled": false,
        "token": "",
        "chat_id": ""
    },
    "api_server": {
        "enabled": true,
        "bind_address": "0.0.0.0",
        "bind_port": 8080,
        "verbosity": "error",
        "enable_openapi": false,
        "jwt_secret_key": "changeme",
        "ws_token": "changeme",
        "CORS_origins": [],
        "username": "freqtrade",
        "password": "changeme"
    },
    "bot_name": "PEPE Bot",
    "initial_state": "running",
    "force_entry_enable": true,
    "internals": {
        "process_throttle_secs": 1
    }
}
EOF
    echo "配置文件已创建: user_data/config.json"
    echo "请编辑配置文件填入你的API Key"
fi

# 5. 提示选择策略
echo "[5/6] 策略配置..."
echo "提示: 请根据需要选择或创建策略"
echo "推荐策略示例: "
echo "  - StrategySampleV1 (官方示例)"
echo "  - 或自行创建策略"
echo "详细文档: https://www.freqtrade.io/en/stable/strategy-customization/"

# 6. 完成
echo "[6/6] 部署完成!"
echo ""
echo "=========================================="
echo "  下一步操作"
echo "=========================================="
echo "1. 编辑配置文件，填入API Key:"
echo "   nano $INSTALL_DIR/user_data/config.json"
echo ""
echo "2. 设置WebUI密码:"
echo "   cd $INSTALL_DIR"
echo "   freqtrade create-password --config user_data/config.json"
echo ""
echo "3. 启动Freqtrade:"
echo "   freqtrade trade --config user_data/config.json --strategy PepeBest"
echo ""
echo "4. 访问WebUI:"
echo "   http://localhost:$BIND_PORT"
echo "=========================================="
