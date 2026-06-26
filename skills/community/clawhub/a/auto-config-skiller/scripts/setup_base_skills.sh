#!/bin/bash

# OpenClaw 基础技能自动配置脚本
# 作者: Antigravity

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   OpenClaw 基础技能自动配置助手       ${NC}"
echo -e "${BLUE}=======================================${NC}"

# 1. 基础环境检查
echo -e "\n${YELLOW}[1/4] 检查基础环境...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: 未检测到 git，请先安装 git。${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未检测到 python3，请先安装 python。${NC}"
    exit 1
fi

echo -e "${GREEN}环境检查通过！${NC}"

# 2. 定义基础技能清单 (仓库地址)
# 这里预设了一些典型的小龙虾基础技能，您可以根据实际情况修改
declare -A SKILLS
SKILLS=(
    ["content-collector"]="https://github.com/YourOrg/content-collector.git"
    ["daily-news-generator"]="https://github.com/YourOrg/daily-news-generator.git"
)

# 获取当前脚本所在目录的父目录（即 skills 根目录）
SKILLS_DIR=$(cd "$(dirname "$0")/../.." && pwd)
echo -e "\n${YELLOW}[2/4] 即将安装技能到目录: ${SKILLS_DIR}${NC}"

for name in "${!SKILLS[@]}"; do
    target_path="${SKILLS_DIR}/${name}"
    if [ -d "$target_path" ]; then
        echo -e "${BLUE}- 技能 [${name}] 已存在，跳过克隆。${NC}"
    else
        echo -e "${BLUE}- 正在克隆 [${name}]...${NC}"
        git clone "${SKILLS[@]/${name}/}" "$target_path" || echo -e "${RED}克隆 ${name} 失败，请检查网络或地址。${NC}"
    fi
done

# 3. 安装依赖
echo -e "\n${YELLOW}[3/4] 正在安装 Python 依赖库...${NC}"
for name in "${!SKILLS[@]}"; do
    target_path="${SKILLS_DIR}/${name}"
    if [ -f "${target_path}/requirements.txt" ]; then
        echo -e "${BLUE}- 安装 ${name} 的依赖...${NC}"
        pip3 install -r "${target_path}/requirements.txt" -q
    fi
done
echo -e "${GREEN}依赖库安装完成！${NC}"

# 4. 配置引导 (占位)
echo -e "\n${YELLOW}[4/4] 配置引导...${NC}"
if [ ! -f "${SKILLS_DIR}/.env" ]; then
    echo -e "${YELLOW}提示: 未检测到 .env 文件。建议创建一个全局 .env 文件来存储配置。${NC}"
    # 这里可以扩展为交互式创建 .env
fi

echo -e "\n${GREEN}=======================================${NC}"
echo -e "${GREEN}   所有基础技能已配置完成！快去体验吧！  ${NC}"
echo -e "${GREEN}=======================================${NC}"
