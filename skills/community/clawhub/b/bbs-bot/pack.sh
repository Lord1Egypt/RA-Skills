#!/bin/bash
# 打包脚本 for BBS.BOT Skill v1.0.1

set -e

echo "=== BBS.BOT Skill 打包工具 ==="
echo "版本: 1.0.1"
echo "修复: bbsbot me 命令API端点问题"
echo ""

# 清理之前的打包文件
rm -f bbs-bot-skill-1.0.1.tar.gz
rm -f bbs-bot-skill-1.0.1.zip

# 创建临时目录用于打包
TEMP_DIR=$(mktemp -d)
cp -r . "$TEMP_DIR/bbs-bot-skill"

# 进入临时目录
cd "$TEMP_DIR"

echo "正在打包文件..."
echo ""

# 显示要打包的文件列表
echo "包含的文件:"
find bbs-bot-skill -type f | sort

echo ""
echo "=== 生成打包文件 ==="

# 创建tar.gz包
tar -czf bbs-bot-skill-1.0.1.tar.gz bbs-bot-skill/
echo "✅ 创建: bbs-bot-skill-1.0.1.tar.gz"
echo "   大小: $(du -h bbs-bot-skill-1.0.1.tar.gz | cut -f1)"

# 创建zip包
zip -rq bbs-bot-skill-1.0.1.zip bbs-bot-skill/
echo "✅ 创建: bbs-bot-skill-1.0.1.zip"
echo "   大小: $(du -h bbs-bot-skill-1.0.1.zip | cut -f1)"

# 复制到原始目录
cp bbs-bot-skill-1.0.1.tar.gz /tmp/bbs-bot-fixed/
cp bbs-bot-skill-1.0.1.zip /tmp/bbs-bot-fixed/

# 清理临时目录
cd /tmp/bbs-bot-fixed
rm -rf "$TEMP_DIR"

echo ""
echo "=== 打包完成 ==="
echo "打包文件已生成在: /tmp/bbs-bot-fixed/"
echo ""
echo "文件列表:"
ls -lh *.tar.gz *.zip 2>/dev/null || echo "没有找到打包文件"
echo ""
echo "=== 安装说明 ==="
echo "1. 解压文件到OpenClaw技能目录:"
echo "   tar -xzf bbs-bot-skill-1.0.1.tar.gz -C /usr/lib/node_modules/openclaw-cn/skills/"
echo ""
echo "2. 或者使用zip文件:"
echo "   unzip bbs-bot-skill-1.0.1.zip -d /usr/lib/node_modules/openclaw-cn/skills/"
echo ""
echo "3. 重启OpenClaw:"
echo "   openclaw gateway restart"
echo ""
echo "=== 验证安装 ==="
echo "安装后运行: bbsbot --version"
echo "应该显示: 1.0.1"
echo ""
echo "=== 修复验证 ==="
echo "修复验证步骤:"
echo "1. bbsbot login --username <用户名> --password <密码>"
echo "2. bbsbot me"
echo "3. 应该显示用户信息，而不是'用户不存在'错误"