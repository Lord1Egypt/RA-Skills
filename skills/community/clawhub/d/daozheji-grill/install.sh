#!/bin/bash
# ============================================================
# 稻哲纪烤羊排 Skill · 一键安装脚本
# ============================================================
# 用法（客户只需运行这一行）：
#   curl -sSL https://raw.githubusercontent.com/Liubuq-sys/daozheji-grill-skill/main/install.sh | bash
# ============================================================

set -e

REPO="https://github.com/Liubuq-sys/daozheji-grill-skill.git"
SKILL_NAME="daozheji-grill"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.openclaw/workspace/skills}"
SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"
TMP_DIR="$(mktemp -d)"

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "=== 稻哲纪烤羊排 Skill · 安装 ==="

# 创建 skills 目录
mkdir -p "$SKILLS_DIR"

# 如果已安装，更新
if [ -d "$SKILL_PATH/.git" ]; then
    echo "已安装，正在更新到最新版本..."
    cd "$SKILL_PATH"
    git pull --ff-only origin master 2>/dev/null || git pull --ff-only origin main 2>/dev/null
    echo "更新完成！"
    cd - > /dev/null
else
    # 下载 skill（浅克隆，速度快）
    echo "正在下载 skill..."
    git clone --depth 1 "$REPO" "$TMP_DIR/repo" 2>/dev/null

    # 复制 skill 到目标目录
    if [ -d "$SKILL_PATH" ]; then
        echo "目标目录已存在（非 git 安装），覆盖中..."
        rm -rf "$SKILL_PATH"
    fi
    cp -r "$TMP_DIR/repo/$SKILL_NAME" "$SKILL_PATH" 2>/dev/null || cp -r "$TMP_DIR/repo" "$SKILL_PATH"

    echo "安装完成！"
fi

# 配置自动更新（追加到 crontab，不重复添加）
UPDATE_CMD="cd $SKILL_PATH && git pull --ff-only origin main 2>/dev/null || git pull --ff-only origin master 2>/dev/null"
if ! crontab -l 2>/dev/null | grep -q "daozheji-grill"; then
    (crontab -l 2>/dev/null; echo "7 3 * * * $UPDATE_CMD") | crontab -
    echo "自动更新已配置（每天 3:07）"
fi

echo ""
echo "Skill 路径: $SKILL_PATH"
echo "已就绪！现在对 AI 说「稻哲纪烤羊排」即可触发。"
echo ""
