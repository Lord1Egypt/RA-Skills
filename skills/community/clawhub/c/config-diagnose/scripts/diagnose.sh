#!/bin/bash
# 配置诊断主脚本
# 用法: diagnose.sh <类型> [参数]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TYPE=$1
PARAM=$2

echo -e "${BLUE}🔍 配置诊断工具 v1.0${NC}"
echo "================================"

# 邮件配置诊断
diagnose_email() {
    echo -e "\n${YELLOW}📧 邮件配置诊断${NC}"
    echo "---"
    
    # 检查环境变量
    local issues=0
    
    echo -n "EMAIL_ADDRESS: "
    if [ -n "$EMAIL_ADDRESS" ]; then
        echo -e "${GREEN}✓ 已设置${NC}"
    else
        echo -e "${RED}✗ 未设置${NC}"
        ((issues++))
    fi
    
    echo -n "EMAIL_PASSWORD: "
    if [ -n "$EMAIL_PASSWORD" ]; then
        echo -e "${GREEN}✓ 已设置${NC}"
    else
        echo -e "${RED}✗ 未设置${NC}"
        ((issues++))
    fi
    
    echo -n "EMAIL_IMAP_SERVER: "
    if [ -n "$EMAIL_IMAP_SERVER" ]; then
        echo -e "${GREEN}✓ $EMAIL_IMAP_SERVER${NC}"
    else
        echo -e "${YELLOW}⚠ 未设置 (默认: imap.gmail.com)${NC}"
    fi
    
    echo -n "EMAIL_SMTP_SERVER: "
    if [ -n "$EMAIL_SMTP_SERVER" ]; then
        echo -e "${GREEN}✓ $EMAIL_SMTP_SERVER${NC}"
    else
        echo -e "${YELLOW}⚠ 未设置 (默认: smtp.gmail.com)${NC}"
    fi
    
    # 测试连接
    if [ -n "$EMAIL_IMAP_SERVER" ] && [ -n "$EMAIL_ADDRESS" ]; then
        echo -n "\nIMAP 连接测试: "
        if timeout 5 bash -c "echo | nc -v $EMAIL_IMAP_SERVER 993 2>&1 | grep -q succeeded" 2>/dev/null; then
            echo -e "${GREEN}✓ 可连接${NC}"
        else
            echo -e "${YELLOW}⚠ 无法测试连接${NC}"
        fi
    fi
    
    # 结果
    echo -e "\n${BLUE}诊断结果:${NC}"
    if [ $issues -eq 0 ]; then
        echo -e "${GREEN}✓ 邮件配置完整${NC}"
    else
        echo -e "${RED}✗ 发现 $issues 个问题${NC}"
        echo -e "\n${YELLOW}建议:${NC}"
        echo "1. 设置环境变量: export EMAIL_ADDRESS='your@email.com'"
        echo "2. 设置应用密码: export EMAIL_PASSWORD='your_app_password'"
        echo "3. Gmail 用户需开启两步验证并生成应用专用密码"
    fi
}

# API 配置诊断
diagnose_api() {
    echo -e "\n${YELLOW}🔑 API 配置诊断${NC}"
    echo "---"
    
    local apis=("OPENAI_API_KEY" "ANTHROPIC_API_KEY" "BAIDU_API_KEY" "GOOGLE_API_KEY" "GITHUB_TOKEN")
    local found=0
    
    for api in "${apis[@]}"; do
        echo -n "$api: "
        if [ -n "${!api}" ]; then
            echo -e "${GREEN}✓ 已设置 (${!api:0:10}...)${NC}"
            ((found++))
        else
            echo -e "${YELLOW}− 未设置${NC}"
        fi
    done
    
    echo -e "\n${BLUE}诊断结果:${NC}"
    if [ $found -gt 0 ]; then
        echo -e "${GREEN}✓ 已配置 $found 个 API${NC}"
    else
        echo -e "${YELLOW}⚠ 未检测到 API 配置${NC}"
        echo -e "\n${YELLOW}建议:${NC}"
        echo "设置 API Key: export OPENAI_API_KEY='sk-...'"
    fi
}

# 服务状态诊断
diagnose_service() {
    local port=$1
    echo -e "\n${YELLOW}🖥️ 服务状态诊断${NC}"
    echo "---"
    
    if [ -n "$port" ]; then
        echo -n "端口 $port: "
        if lsof -i:$port >/dev/null 2>&1; then
            echo -e "${GREEN}✓ 已使用${NC}"
            lsof -i:$port 2>/dev/null | tail -n +2 | while read line; do
                echo "  $line"
            done
        else
            echo -e "${YELLOW}− 未占用${NC}"
        fi
    fi
    
    # 检查常见服务端口
    echo -e "\n常见服务状态:"
    for p in 3000 3001 8080 8000 5000; do
        echo -n "  端口 $p: "
        if lsof -i:$p >/dev/null 2>&1; then
            echo -e "${GREEN}✓ 运行中${NC}"
        else
            echo -e "${YELLOW}− 未启动${NC}"
        fi
    done
    
    # 检查 Node 进程
    echo -e "\nNode 进程:"
    if pgrep -f "node" >/dev/null; then
        ps aux | grep -E "node|next|npm" | grep -v grep | head -5
    else
        echo "  无运行中的 Node 进程"
    fi
}

# 文件搜索诊断
diagnose_file() {
    local filename=$1
    echo -e "\n${YELLOW}📁 文件搜索诊断${NC}"
    echo "---"
    
    if [ -z "$filename" ]; then
        echo -e "${RED}请指定文件名${NC}"
        return
    fi
    
    echo "搜索: $filename"
    echo ""
    
    # 搜索文件
    local results=$(find /root -name "*$filename*" 2>/dev/null | head -10)
    
    if [ -n "$results" ]; then
        echo -e "${GREEN}找到文件:${NC}"
        echo "$results"
    else
        echo -e "${RED}未找到文件${NC}"
        echo -e "\n${YELLOW}建议:${NC}"
        echo "1. 检查文件名拼写"
        echo "2. 确认文件是否需要先创建/安装"
        echo "3. 尝试更广泛的搜索: find / -name '$filename' 2>/dev/null"
    fi
}

# 技能配置诊断
diagnose_skill() {
    local skill_name=$1
    echo -e "\n${YELLOW}🛠️ 技能配置诊断${NC}"
    echo "---"
    
    local skill_dir="/root/.openclaw/workspace/skills"
    
    if [ -n "$skill_name" ]; then
        # 检查特定技能
        local skill_path="$skill_dir/$skill_name"
        if [ -d "$skill_path" ]; then
            echo -e "${GREEN}✓ 技能目录存在: $skill_path${NC}"
            
            # 检查 SKILL.md
            if [ -f "$skill_path/SKILL.md" ]; then
                echo -e "${GREEN}✓ SKILL.md 存在${NC}"
            else
                echo -e "${RED}✗ SKILL.md 缺失${NC}"
            fi
            
            # 检查脚本
            if [ -d "$skill_path/scripts" ]; then
                echo -e "${GREEN}✓ scripts/ 目录存在${NC}"
                ls "$skill_path/scripts" | head -5
            fi
        else
            echo -e "${RED}✗ 技能未安装: $skill_name${NC}"
            echo -e "\n${YELLOW}建议:${NC}"
            echo "安装技能: clawhub install $skill_name"
        fi
    else
        # 列出所有已安装技能
        echo "已安装技能:"
        ls -1 "$skill_dir" 2>/dev/null | head -20
    fi
}

# 根据类型执行诊断
case "$TYPE" in
    email|mail|邮件)
        diagnose_email
        ;;
    api|key|token)
        diagnose_api
        ;;
    service|port|服务|端口)
        diagnose_service "$PARAM"
        ;;
    file|文件)
        diagnose_file "$PARAM"
        ;;
    skill|技能)
        diagnose_skill "$PARAM"
        ;;
    all|全部)
        diagnose_email
        diagnose_api
        diagnose_service
        ;;
    *)
        echo "用法: $0 <类型> [参数]"
        echo ""
        echo "类型:"
        echo "  email   - 邮件配置诊断"
        echo "  api     - API 配置诊断"
        echo "  service - 服务状态诊断 (可指定端口)"
        echo "  file    - 文件搜索诊断 (需指定文件名)"
        echo "  skill   - 技能配置诊断 (可指定技能名)"
        echo "  all     - 全部诊断"
        ;;
esac

echo ""
echo -e "${BLUE}================================${NC}"
echo -e "诊断完成！如有问题请查看建议解决。"
