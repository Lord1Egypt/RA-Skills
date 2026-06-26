#!/bin/bash
# 清理个人数据，准备发布到 ClawHub

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}==========================================${NC}"
echo -e "${YELLOW}清理个人数据${NC}"
echo -e "${YELLOW}==========================================${NC}"
echo ""

# 要删除的文件和目录
FILES_TO_DELETE=(
    ".env"                          # 包含账号密码
    ".flomo_sync_state.json"        # 包含同步状态和用户名
    "auto_sync.log"                 # 可能包含敏感信息
    "conversion.log"                # 可能包含个人笔记内容
    "flomo_downloads"               # 包含下载的个人数据
    "flomo_browser_data"            # 包含浏览器登录状态
    "test-output"                   # 测试数据，可能包含个人笔记
)

echo -e "${YELLOW}将要删除以下文件/目录：${NC}"
for item in "${FILES_TO_DELETE[@]}"; do
    if [ -e "$item" ]; then
        echo "  ❌ $item"
    else
        echo "  ⚪ $item (不存在)"
    fi
done
echo ""

read -p "确认删除？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}取消清理${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}开始清理...${NC}"

# 删除文件和目录
for item in "${FILES_TO_DELETE[@]}"; do
    if [ -e "$item" ]; then
        echo -e "删除: ${RED}$item${NC}"
        rm -rf "$item"
    fi
done

# 清理文档中的示例路径
echo ""
echo -e "${YELLOW}清理文档中的示例数据...${NC}"

# 替换示例用户名和路径
if [ -f "setup.sh" ]; then
    sed -i '' 's|/Users/ryanbzhou/mynote/flomo|~/Documents/Obsidian/flomo|g' setup.sh
    echo "  ✅ setup.sh"
fi

if [ -f "USAGE_SAFE_MODE.md" ]; then
    sed -i '' 's|/Users/ryanbzhou/mynote/flomo|~/Documents/Obsidian/flomo|g' USAGE_SAFE_MODE.md
    echo "  ✅ USAGE_SAFE_MODE.md"
fi

if [ -f "README.md" ]; then
    sed -i '' 's|Ryan\.B|YourName|g' README.md
    sed -i '' 's|/Users/ryanbzhou/mynote/flomo|~/Documents/Obsidian/flomo|g' README.md
    echo "  ✅ README.md"
fi

if [ -f "SETUP_GUIDE.md" ]; then
    sed -i '' 's|/Users/ryanbzhou/mynote/flomo|~/Documents/Obsidian/flomo|g' SETUP_GUIDE.md
    echo "  ✅ SETUP_GUIDE.md"
fi

if [ -f "SYNC_STATUS.md" ]; then
    sed -i '' 's|Ryan\.B|YourName|g' SYNC_STATUS.md
    sed -i '' 's|/Users/ryanbzhou/mynote/flomo|~/Documents/Obsidian/flomo|g' SYNC_STATUS.md
    echo "  ✅ SYNC_STATUS.md"
fi

# 创建示例配置文件
echo ""
echo -e "${YELLOW}创建示例配置文件...${NC}"

cat > .env.example << 'EOF'
# Flomo 账号配置（密码模式）
FLOMO_EMAIL=your_phone_or_email
FLOMO_PASSWORD=your_password

# Obsidian vault 路径
OBSIDIAN_VAULT=~/Documents/Obsidian/flomo

# 标签前缀（可选）
TAG_PREFIX=flomo/
EOF

echo "  ✅ .env.example"

# 创建 .gitignore（如果不存在）
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# 敏感信息
.env
*.log

# 个人数据
flomo_downloads/
flomo_browser_data/
.flomo_sync_state.json

# 测试数据
test-output/

# Python
__pycache__/
*.pyc
*.pyo

# macOS
.DS_Store
EOF
    echo "  ✅ .gitignore"
fi

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}✅ 清理完成！${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${YELLOW}清理的内容：${NC}"
echo "  • 删除了包含账号密码的配置文件"
echo "  • 删除了浏览器登录状态"
echo "  • 删除了个人同步数据"
echo "  • 删除了测试输出文件"
echo "  • 替换了文档中的个人信息为示例"
echo ""
echo -e "${YELLOW}创建的文件：${NC}"
echo "  • .env.example - 配置文件示例"
echo "  • .gitignore - Git 忽略规则"
echo ""
echo -e "${GREEN}现在可以安全地发布到 ClawHub 了！${NC}"
echo ""
