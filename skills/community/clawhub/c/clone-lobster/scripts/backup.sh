#!/bin/bash
# 克隆龙虾 - 自动备份 OpenClaw/CatPaw 配置到 Git 仓库
# 用法: bash backup.sh [commit_message]

set -e

# ========== 配置 ==========
BACKUP_REPO_URL="${CLONE_LOBSTER_REPO_URL:-}"
BACKUP_DIR="/tmp/clone-lobster-backup"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
COMMIT_MSG="${1:-auto backup at $(date '+%Y-%m-%d %H:%M:%S')}"

# ========== 检查 ==========
if [ -z "$BACKUP_REPO_URL" ]; then
    echo "❌ 错误: 未配置备份仓库地址"
    echo "请设置环境变量 CLONE_LOBSTER_REPO_URL"
    echo "例如: export CLONE_LOBSTER_REPO_URL='ssh://git@git.sankuai.com/~user/repo.git'"
    exit 1
fi

# ========== 克隆/更新仓库 ==========
if [ -d "$BACKUP_DIR/.git" ]; then
    echo "📦 更新本地备份仓库..."
    cd "$BACKUP_DIR"
    git pull --rebase origin master 2>/dev/null || true
else
    echo "📦 克隆备份仓库..."
    rm -rf "$BACKUP_DIR"
    git clone "$BACKUP_REPO_URL" "$BACKUP_DIR" 2>&1
fi

cd "$BACKUP_DIR"

# ========== 备份工作区 ==========
echo "📝 备份工作区文件..."
mkdir -p workspace
for f in AGENTS.md SOUL.md USER.md IDENTITY.md HEARTBEAT.md TOOLS.md BOOTSTRAP.md MEMORY.md; do
    [ -f "$WORKSPACE_DIR/$f" ] && cp "$WORKSPACE_DIR/$f" workspace/
done

# 备份 memory 目录
if [ -d "$WORKSPACE_DIR/memory" ]; then
    mkdir -p workspace/memory
    cp -r "$WORKSPACE_DIR/memory/"* workspace/memory/ 2>/dev/null || true
fi

# 备份 .openclaw 子目录
if [ -d "$WORKSPACE_DIR/.openclaw" ]; then
    mkdir -p workspace/.openclaw
    cp -r "$WORKSPACE_DIR/.openclaw/"* workspace/.openclaw/ 2>/dev/null || true
fi

# ========== 备份配置 ==========
echo "⚙️  备份 OpenClaw 配置..."
mkdir -p config
for f in openclaw.json exec-approvals.json; do
    [ -f "$OPENCLAW_DIR/$f" ] && cp "$OPENCLAW_DIR/$f" config/
done

# ========== 备份 Skills ==========
echo "🧩 备份已安装 Skills..."
mkdir -p skills
if [ -d "$OPENCLAW_DIR/skills" ]; then
    rsync -a --exclude='node_modules' --exclude='*.pyc' --exclude='__pycache__' \
        "$OPENCLAW_DIR/skills/" skills/ 2>/dev/null || \
        cp -r "$OPENCLAW_DIR/skills/"* skills/ 2>/dev/null || true
fi

# ========== 备份系统配置 ==========
echo "🔧 备份系统配置..."
mkdir -p system
[ -f /etc/supervisor/supervisord.conf ] && cp /etc/supervisor/supervisord.conf system/
[ -f /usr/local/bin/start-desktop.sh ] && cp /usr/local/bin/start-desktop.sh system/
[ -f ~/.ssh/config ] && cp ~/.ssh/config system/ssh_config
dpkg --get-selections 2>/dev/null | grep -vE "^lib|^python3-" > system/installed_packages.txt || true
supervisorctl status > system/supervisor_status.txt 2>/dev/null || true

# ========== 备份对话上下文 ==========
echo "💬 备份对话上下文..."
mkdir -p context
for db in "$OPENCLAW_DIR"/sessions*.db "$OPENCLAW_DIR"/data/*.db; do
    [ -f "$db" ] && cp "$db" context/ 2>/dev/null || true
done
if [ -d "$OPENCLAW_DIR/data" ]; then
    mkdir -p context/data
    cp "$OPENCLAW_DIR/data/"*.json context/data/ 2>/dev/null || true
fi

# ========== 更新 README ==========
cat > README.md << 'EOF_README'
# 🦞 克隆龙虾 - CatPaw/OpenClaw 备份

自动备份 OpenClaw 的配置、上下文、Skills 和系统改动。

## 目录结构

```
├── workspace/      # 工作区 (AGENTS.md, SOUL.md, USER.md, memory/)
├── config/         # OpenClaw 配置 (openclaw.json)
├── skills/         # 已安装的 Skills
├── system/         # 系统级配置 (supervisor, SSH, 已安装包)
├── context/        # 对话上下文和 session 数据
└── README.md
```

## 恢复方法

```bash
cp -r workspace/* ~/.openclaw/workspace/
cp config/openclaw.json ~/.openclaw/
cp -r skills/* ~/.openclaw/skills/
# 系统配置参考 system/ 手动恢复
```
EOF_README
echo "" >> README.md
echo "最后备份时间: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> README.md

# ========== 提交并推送 ==========
echo "🚀 提交并推送..."
git add -A
if git diff --cached --quiet; then
    echo "✅ 无变更，跳过提交"
else
    git commit -m "$COMMIT_MSG"
    git push origin master 2>&1
    echo "✅ 备份完成！"
fi

echo ""
echo "📊 备份统计:"
echo "   工作区文件: $(find workspace -type f 2>/dev/null | wc -l)"
echo "   配置文件:   $(find config -type f 2>/dev/null | wc -l)"
echo "   Skills:     $(find skills -maxdepth 1 -type d 2>/dev/null | wc -l)"
echo "   系统配置:   $(find system -type f 2>/dev/null | wc -l)"
echo "   上下文文件: $(find context -type f 2>/dev/null | wc -l)"
