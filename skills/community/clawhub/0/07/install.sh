#!/bin/bash
# 07-互联网访问技能 - 一键安装脚本

set -e

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "=========================================="
echo "07-互联网访问技能 - 安装"
echo "=========================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    log_error "未找到 Python 3.10+，请先安装"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
log_info "Python 版本: $PYTHON_VERSION"

# 检查 Python 版本
if [ $(echo "$PYTHON_VERSION 3.10" | awk '{print ($1 < $2)}') -eq 1 ]; then
    log_error "Python 版本过低，需要 3.10+，当前版本: $PYTHON_VERSION"
    exit 1
fi

# 询问是否创建虚拟环境
read -p "是否创建虚拟环境？(推荐) (y/n): " create_venv

if [ "$create_venv" = "y" ]; then
    log_info "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    log_info "虚拟环境已激活"
fi

# 升级 pip
log_info "升级 pip..."
pip install --upgrade pip -q

# 安装依赖
log_info "安装核心依赖..."
pip install -r requirements.txt -q

# 安装额外的安全工具
log_info "安装安全工具..."
pip install cryptography pip-audit -q 2>/dev/null || log_warn "安全工具安装失败（可选）"

# 询问配置哪些平台
echo ""
log_info "请选择要配置的平台："
echo "1. Twitter (需要 Cookie)"
echo "2. YouTube (可选代理)"
echo "3. 小红书 (需要 Cookie)"
echo "4. Reddit (无需配置)"
echo "5. B站 (无需配置)"
echo "6. 网页搜索 (无需配置)"
echo ""
read -p "输入平台编号（多个用空格分隔，如: 1 2 3）: " platforms

# Twitter 配置
if [[ "$platforms" == *"1"* ]]; then
    echo ""
    log_info "配置 Twitter..."
    log_warn "请按以下步骤导出 Cookie："
    echo "  1. 登录 Twitter (X.com)"
    echo "  2. 按 F12 打开开发者工具"
    echo "  3. 进入 Application/Storage → Cookies"
    echo "  4. 找到 'auth_token' 并复制值"
    echo ""
    read -p "按回车继续配置..."

    python3 << EOF
import sys
sys.path.insert(0, 'security')
try:
    from encrypt_cookies import CookieEncryptor
    log_warn "请输入 Twitter auth_token:"
    token = input().strip()

    import os
    config_dir = os.path.expanduser("~/.config/agent-reach")
    os.makedirs(config_dir, exist_ok=True)

    cookies_file = os.path.join(config_dir, "cookies.json")
    import json
    with open(cookies_file, 'w') as f:
        json.dump({"twitter": {"auth_token": token}}, f)

    encryptor = CookieEncryptor(config_dir)
    if encryptor.import_from_json(cookies_file):
        print("✅ Twitter Cookie 已加密存储")
    else:
        print("❌ 加密失败")
except Exception as e:
    print(f"❌ 配置失败: {e}")
EOF
fi

# YouTube 配置
if [[ "$platforms" == *"2"* ]]; then
    echo ""
    log_info "配置 YouTube..."
    read -p "是否需要配置代理？(y/n): " use_proxy

    if [ "$use_proxy" = "y" ]; then
        read -p "输入代理地址 (如: socks5://127.0.0.1:1080): " proxy_url

        # 保存到环境变量
        export_file="export YOUTUBE_PROXY=\"$proxy_url\""
        echo "$export_file" >> ~/.bashrc
        log_info "代理配置已添加到 ~/.bashrc"
    fi
fi

# 小红书配置
if [[ "$platforms" == *"3"* ]]; then
    echo ""
    log_info "配置小红书..."
    log_warn "请参考 guides/setup-xiaohongshu.md 导出 Cookie"
    log_warn "完成后运行: python cookie_extract.py xiaohongshu"
fi

# 运行安全检查
echo ""
log_info "运行安全检查..."
python3 security/dependency_check.py full 2>/dev/null || log_warn "依赖检查失败（可选）"

# 创建启动脚本
cat > run.sh << 'EOFRUN'
#!/bin/bash
# 07-互联网访问技能 - 启动脚本

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行 CLI
python3 cli.py "$@"
EOFRUN

chmod +x run.sh

# 创建测试脚本
cat > test.sh << 'EOFTEST'
#!/bin/bash
# 07-互联网访问技能 - 测试脚本

echo "测试各平台连接..."

# 测试 Reddit
echo ""
echo "[1/3] 测试 Reddit..."
python3 << PYTEST
import sys
sys.path.insert(0, 'channels')
from reddit import RedditChannel
try:
    reddit = RedditChannel()
    posts = reddit.search("Python", "learnprogramming", limit=1)
    print(f"✅ Reddit 正常，找到 {len(posts)} 条结果")
except Exception as e:
    print(f"❌ Reddit 失败: {e}")
PYTEST

# 测试网页
echo ""
echo "[2/3] 测试网页搜索..."
python3 << PYTEST
import sys
sys.path.insert(0, 'channels')
from web import WebChannel
try:
    web = WebChannel()
    results = web.search("test")
    print(f"✅ 网页搜索正常")
except Exception as e:
    print(f"❌ 网页搜索失败: {e}")
PYTEST

# 测试 B站
echo ""
echo "[3/3] 测试 B站..."
python3 << PYTEST
import sys
sys.path.insert(0, 'channels')
try:
    from bilibili import BilibiliChannel
    print("✅ B站模块加载正常")
except Exception as e:
    print(f"❌ B站失败: {e}")
PYTEST

echo ""
echo "测试完成！"
EOFTEST

chmod +x test.sh

# 完成
echo ""
echo "=========================================="
echo "✅ 安装完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  启动 CLI: ./run.sh"
echo "  运行测试: ./test.sh"
echo "  查看帮助: python3 cli.py --help"
echo ""
echo "配置指南:"
echo "  小红书: cat guides/setup-xiaohongshu.md"
echo "  Exa搜索: cat guides/setup-exa.md"
echo ""
echo "安全工具:"
echo "  依赖检查: python3 security/dependency_check.py full"
echo "  审计监控: python3 security/audit_monitor.py report"
echo "  Cookie加密: python3 security/encrypt_cookies.py --help"
echo ""
echo "与其他技能集成:"
echo "  查看集成示例: cat integration/skill_bridge.py"
echo ""
echo "位置: $(pwd)"
