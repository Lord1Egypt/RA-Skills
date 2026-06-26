#!/bin/bash
# A-Share Pro 卸载脚本

echo "🗑️ 开始卸载 A-Share Pro..."

read -p "⚠️ 确定要卸载吗？此操作将删除自选股数据！(y/n): " confirm

if [ "$confirm" = "y" ]; then
    # 备份数据目录（可选）
    backup_date=$(date +%Y%m%d_%H%M%S)
    if [ -d ~/.openclaw/a_share ]; then
        cp -r ~/.openclaw/a_share ~/.openclaw/a_share_backup_$backup_date 2>/dev/null
        echo "💾 已备份数据到：~/.openclaw/a_share_backup_$backup_date"
        
        rm -rf ~/.openclaw/a_share
        echo "✅ 数据目录已删除"
    fi
    
    # 删除技能目录
    cd "$(dirname "$0")/.."
    rm -rf a-share-pro
    echo "✅ 技能目录已删除"
    
    echo ""
    echo "✨ 卸载完成!"
else
    echo "❌ 已取消卸载"
fi
