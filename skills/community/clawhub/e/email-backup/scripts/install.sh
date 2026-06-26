#!/bin/bash
# Email Backup Skill 一键安装脚本
# 用于 OpenClaw 自动安装

set -e  # 遇到错误立即退出

echo "🚀 开始安装 Email Backup Skill..."

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装，请先安装 OpenClaw"
    echo "💡 安装命令: npm install -g openclaw"
    exit 1
fi

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    echo "💡 Ubuntu/Debian: sudo apt install -y python3"
    echo "💡 CentOS/RHEL: sudo yum install -y python3"
    exit 1
fi

# 创建 skills 目录
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
mkdir -p "$SKILLS_DIR"

# 下载 Skill 文件
echo "📥 正在下载 Email Backup Skill..."
cd "$SKILLS_DIR"

# 如果是本地安装，直接复制
if [ -f "email-backup-skill.tar.gz" ]; then
    echo "📦 使用本地文件安装..."
    tar -xzf email-backup-skill.tar.gz
else
    # 从网络下载（这里需要替换为实际的下载地址）
    echo "🌐 从网络下载..."
    # 示例：curl -L -o email-backup-skill.tar.gz https://example.com/email-backup-skill.tar.gz
    # tar -xzf email-backup-skill.tar.gz
    echo "⚠️  请手动下载 Skill 文件并放置到 $SKILLS_DIR 目录"
    echo "💡 下载地址: https://github.com/your-repo/email-backup-skill/releases"
    exit 1
fi

# 验证安装
if [ ! -d "$SKILLS_DIR/email-backup" ]; then
    echo "❌ 安装失败：email-backup 目录不存在"
    exit 1
fi

# 设置执行权限
chmod +x "$SKILLS_DIR/email-backup/scripts/"*.py
chmod +x "$SKILLS_DIR/email-backup/scripts/"*.sh

# 测试安装
echo "🧪 测试安装..."
cd "$SKILLS_DIR/email-backup"
if python3 scripts/backup_and_send.py --help > /dev/null 2>&1; then
    echo "✅ 安装成功！"
else
    echo "⚠️  安装完成，但测试失败，请检查 Python 环境"
fi

# 显示使用说明
echo ""
echo "📖 使用说明："
echo "1. 配置 QQ 邮箱："
echo "   - 登录 QQ 邮箱 (mail.qq.com)"
echo "   - 进入「设置」→「账户」"
echo "   - 开启「IMAP/SMTP 服务」"
echo "   - 生成授权码"
echo ""
echo "2. 设置环境变量："
echo "   export QQ_EMAIL=\"your-email@example.com\""
echo "   export QQ_SMTP_PASSWORD=\"your-auth-code\""
echo ""
echo "3. 使用命令："
echo "   cd ~/.openclaw/workspace/skills/email-backup"
echo "   python3 scripts/backup_and_send.py /path/to/directory --clean"
echo ""
echo "🎉 Email Backup Skill 安装完成！"

exit 0