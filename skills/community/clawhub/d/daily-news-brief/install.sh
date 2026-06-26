#!/bin/bash

# 每日新闻简报Skill安装脚本
# 适用于Linux/macOS系统

set -e

echo "📰 每日新闻简报Skill安装开始..."
echo "======================================"

# 检查Node.js版本
echo "🔍 检查Node.js版本..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "❌ Node.js版本需要14或更高，当前版本: $(node -v)"
    echo "请先升级Node.js: https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js版本: $(node -v)"

# 检查npm
echo "🔍 检查npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm未安装"
    exit 1
fi
echo "✅ npm版本: $(npm -v)"

# 安装依赖
echo "📦 安装依赖..."
cd "$(dirname "$0")"
npm install

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 创建必要目录
echo "📁 创建目录..."
mkdir -p logs history templates

# 设置文件权限
echo "🔒 设置文件权限..."
chmod +x news-brief.js
chmod 644 config.json package.json

# 测试运行
echo "🧪 测试运行..."
node news-brief.js --run-now

if [ $? -eq 0 ]; then
    echo "✅ 测试运行成功"
else
    echo "⚠️  测试运行有警告，但继续安装..."
fi

# 设置定时任务
echo "⏰ 设置定时任务..."
read -p "是否设置每天早上8点自动运行? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Linux/macOS使用crontab
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        CRON_JOB="0 8 * * * cd $(pwd) && node news-brief.js >> logs/cron.log 2>&1"
        
        # 添加到crontab
        (crontab -l 2>/dev/null | grep -v "news-brief.js"; echo "$CRON_JOB") | crontab -
        
        if [ $? -eq 0 ]; then
            echo "✅ 定时任务设置成功"
            echo "Cron表达式: 0 8 * * *"
            echo "工作目录: $(pwd)"
        else
            echo "❌ 定时任务设置失败"
        fi
    else
        echo "⚠️  不支持的操作系统，请手动设置定时任务"
        echo "Cron表达式: 0 8 * * *"
        echo "命令: cd $(pwd) && node news-brief.js"
    fi
else
    echo "⏸️  跳过定时任务设置"
fi

# 创建服务文件（可选）
echo "🛠️  创建systemd服务文件（可选）..."
read -p "是否创建systemd服务? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] && [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SERVICE_FILE="/etc/systemd/system/daily-news-brief.service"
    
    cat > daily-news-brief.service << EOF
[Unit]
Description=Daily News Brief Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/node $(pwd)/news-brief.js --setup-cron
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    echo "📄 服务文件已创建: daily-news-brief.service"
    echo "请手动复制到系统目录:"
    echo "sudo cp daily-news-brief.service $SERVICE_FILE"
    echo "sudo systemctl daemon-reload"
    echo "sudo systemctl enable daily-news-brief.service"
    echo "sudo systemctl start daily-news-brief.service"
fi

# 安装完成
echo ""
echo "======================================"
echo "🎉 每日新闻简报Skill安装完成！"
echo ""
echo "📋 安装摘要:"
echo "• 工作目录: $(pwd)"
echo "• 依赖: 已安装"
echo "• 配置: config.json"
echo "• 日志: logs/news-brief.log"
echo "• 历史: history/ 目录"
echo ""
echo "🚀 使用方法:"
echo "1. 编辑 config.json 配置新闻源和发布渠道"
echo "2. 测试运行: npm test"
echo "3. 手动运行: node news-brief.js"
echo "4. 设置定时: npm run setup"
echo ""
echo "🔧 配置说明:"
echo "• 修改新闻源: 编辑 config.json 中的 newsSources"
echo "• 调整时间: 修改 schedule 字段"
echo "• 添加渠道: 在 outputChannels 中添加"
echo "• 设置收件人: 修改 recipients 数组"
echo ""
echo "📞 支持:"
echo "• 查看日志: tail -f logs/news-brief.log"
echo "• 问题反馈: GitHub Issues"
echo "• 文档: README.md"
echo ""
echo "✨ 祝您使用愉快！"