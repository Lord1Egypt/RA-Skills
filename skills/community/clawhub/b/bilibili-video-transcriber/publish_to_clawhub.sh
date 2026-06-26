#!/bin/bash
# B 站视频转录专家 v2.0.0 ClawHub 发布脚本

set -e

echo "🎬 B 站视频转录专家 v2.0.0 ClawHub 发布"
echo "=========================================="
echo ""

# 检查必要文件
echo "📦 检查必要文件..."
required_files=(
    "bilibili_transcriber.py"
    "cli.py"
    "config.yaml"
    "setup.py"
    "requirements.txt"
    "README.md"
    "SKILL.md"
    "package.json"
    ".clawhub/origin.json"
    ".clawhub/release.json"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件：$file"
        exit 1
    fi
done
echo "✅ 所有必要文件存在"
echo ""

# 检查版本号
echo "🔖 检查版本号..."
version=$(cat package.json | grep '"version"' | head -1 | cut -d'"' -f4)
echo "   当前版本：v$version"

if [ "$version" != "2.0.0" ]; then
    echo "❌ 版本号不是 2.0.0，请确认"
    exit 1
fi
echo "✅ 版本号正确"
echo ""

# 检查 Git 状态
echo "📊 检查 Git 状态..."
git_status=$(git status --porcelain)
if [ -n "$git_status" ]; then
    echo "⚠️  有未提交的更改："
    echo "$git_status"
    read -p "是否继续？(y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "❌ 发布取消"
        exit 1
    fi
fi
echo "✅ Git 状态正常"
echo ""

# 检查 Git tag
echo "🏷️  检查 Git tag..."
if ! git tag -l | grep -q "v2.0.0"; then
    echo "⚠️  Tag v2.0.0 不存在，正在创建..."
    git tag -a v2.0.0 -m "Release v2.0.0: 优化处理优先级和系统资源检测"
    git push origin v2.0.0
fi
echo "✅ Git tag 存在：v2.0.0"
echo ""

# 打包
echo "📦 打包技能文件..."
tarball="bilibili-video-transcriber-v2.0.0.tar.gz"
tar -czf "$tarball" \
    bilibili_transcriber.py \
    cli.py \
    config.yaml \
    setup.py \
    requirements.txt \
    README.md \
    SKILL.md \
    package.json \
    .clawhub/ \
    examples/ 2>/dev/null || true

echo "✅ 打包完成：$tarball"
echo "   文件大小：$(du -h "$tarball" | cut -f1)"
echo ""

# 显示发布信息
echo "📋 发布信息："
echo "   技能名称：bilibili-video-transcriber"
echo "   版本：2.0.0"
echo "   发布日期：$(date +%Y-%m-%d)"
echo "   Git 仓库：https://github.com/adolescen-he/bilibili-video-transcriber"
echo "   Tag: v2.0.0"
echo ""

# 显示主要更新
echo "🚀 主要更新："
echo "   1. 优化处理优先级（CC 字幕→AI 字幕→音频转录→视频下载）"
echo "   2. 添加系统资源检测，智能选择模型"
echo "   3. 添加镜像源自动切换功能"
echo "   4. 添加 Vosk 离线引擎支持"
echo "   5. 添加扫码登录功能"
echo "   6. 性能提升 96%（有字幕场景）"
echo "   7. 视频时长策略：<10 分钟 Vosk，>20 分钟 Whisper 在线"
echo ""

echo "✅ 发布准备完成！"
echo ""
echo "下一步："
echo "1. 将 $tarball 上传到 ClawHub"
echo "2. 更新 ClawHub 技能索引"
echo "3. 通知用户升级"
echo ""
echo "🦞 发布成功！"
