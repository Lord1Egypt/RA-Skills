#!/bin/bash

# ==========================================
# OpenClaw 自动配置助手 - 一键启动脚本
# ==========================================

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[1;m' # No Color

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   OpenClaw 自动配置助手 (一键傻瓜模式)${NC}"
echo -e "${BLUE}=======================================${NC}"

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}未发现 Python3，请先安装 Python。${NC}"
    exit 1
fi

# 2. 运行核心诊断与安装逻辑
echo -e "${GREEN}[*] 正在启动环境体检与自动安装...${NC}"
python3 scripts/diagnose_and_install.py

# 3. 结果提示
echo -e "\n${GREEN}🎉 处理完成！${NC}"
echo -e "${YELLOW}如果你需要将龙虾连接到飞书，请确保按提示操作官方工具。${NC}"
echo -e "${BLUE}查看详细指南: ./docs/USAGE_GUIDE.md${NC}"
