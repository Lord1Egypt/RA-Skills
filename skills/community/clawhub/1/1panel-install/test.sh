#!/bin/bash

# 测试脚本：验证 1panel-install skill 的功能
# 用法：sudo ./test.sh

set -e

echo "=========================================="
echo "   1Panel 安装 Skill 测试"
echo "=========================================="
echo ""

# 检查是否在正确的目录
if [[ ! -f "./install.sh" ]]; then
    echo "错误：请在 1panel-install 目录中运行此脚本"
    exit 1
fi

# 检查 root 权限
if [[ $EUID -ne 0 ]]; then
    echo "错误：测试需要 root 权限，请使用 sudo"
    exit 1
fi

# 测试 1：检查已安装状态
echo "测试 1：检查 1Panel 是否已安装..."
if command -v 1pctl &> /dev/null; then
    echo "✓ 1Panel 已安装"
    echo ""
    echo "当前 1Panel 信息："
    1pctl user-info || echo "获取信息失败"
    echo ""
else
    echo "✗ 1Panel 未安装"
    echo ""
fi

# 测试 2：模拟未安装状态（备份已安装的 1Panel）
BACKUP_DIR="/tmp/1panel-backup-$(date +%s)"
if command -v 1pctl &> /dev/null; then
    echo "测试 2：模拟未安装状态（临时备份 1Panel）..."
    echo "备份目录：$BACKUP_DIR"
    
    # 备份已安装的文件
    mkdir -p "$BACKUP_DIR"
    if [[ -d "/opt/1panel" ]]; then
        mv /opt/1panel "$BACKUP_DIR/"
    fi
    if command -v 1pctl &> /dev/null; then
        mv /usr/bin/1pctl "$BACKUP_DIR/"
    fi
    
    # 停止服务
    systemctl stop 1panel-core 2>/dev/null || true
    systemctl stop 1panel-agent 2>/dev/null || true
    systemctl disable 1panel-core 2>/dev/null || true
    systemctl disable 1panel-agent 2>/dev/null || true
    
    echo "已临时移除 1Panel"
    echo ""
else
    echo "测试 2：跳过（1Panel 未安装）"
    echo ""
fi

# 测试 3：运行安装脚本
read -p "是否测试安装流程？这将会实际安装 1Panel (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "开始安装测试..."
    echo ""
    
    if ./install.sh; then
        echo ""
        echo "✓ 安装脚本执行成功"
        
        # 验证安装
        if command -v 1pctl &> /dev/null; then
            echo "✓ 1pctl 命令可用"
            echo ""
            echo "验证信息："
            1pctl user-info
        else
            echo "✗ 1pctl 不可用，安装可能失败"
            exit 1
        fi
    else
        echo ""
        echo "✗ 安装脚本执行失败"
        exit 1
    fi
else
    echo "跳过安装测试"
fi

# 恢复备份（如果存在）
if [[ -d "$BACKUP_DIR" ]]; then
    echo ""
    read -p "是否恢复之前的 1Panel 备份？(y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "恢复备份..."
        
        # 停止新安装的服务
        systemctl stop 1panel-core 2>/dev/null || true
        systemctl stop 1panel-agent 2>/dev/null || true
        systemctl disable 1panel-core 2>/dev/null || true
        systemctl disable 1panel-agent 2>/dev/null || true
        
        # 清理新安装的文件
        rm -rf /opt/1panel
        rm -f /usr/bin/1pctl
        rm -f /etc/systemd/system/1panel-*.service
        
        # 恢复备份
        if [[ -f "$BACKUP_DIR/1pctl" ]]; then
            cp "$BACKUP_DIR/1pctl" /usr/bin/
            chmod +x /usr/bin/1pctl
        fi
        if [[ -d "$BACKUP_DIR/1panel" ]]; then
            cp -r "$BACKUP_DIR/1panel" /opt/
        fi
        
        # 重新加载 systemd
        systemctl daemon-reload 2>/dev/null || true
        
        # 如果原服务存在，重新启用
        if systemctl list-unit-files | grep -q 1panel-core; then
            systemctl enable 1panel-core 2>/dev/null || true
            systemctl start 1panel-core 2>/dev/null || true
        fi
        
        echo "✓ 备份已恢复"
    fi
fi

echo ""
echo "=========================================="
echo "   测试完成"
echo "=========================================="
