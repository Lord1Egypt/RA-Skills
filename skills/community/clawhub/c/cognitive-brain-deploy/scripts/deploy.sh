#!/bin/bash
# Cognitive Brain 一键部署脚本
# 使用方式: bash ~/.openclaw/workspace/skills/cognitive-brain-deploy/scripts/deploy.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[部署]${NC} $1"; }
warn() { echo -e "${YELLOW}[警告]${NC} $1"; }
error() { echo -e "${RED}[错误]${NC} $1"; exit 1; }

# 检查是否为 root 或有 sudo 权限
check_permissions() {
    if [ "$EUID" -ne 0 ] && ! sudo -v 2>/dev/null; then
        error "需要 sudo 权限，请确保当前用户在 sudo 组中"
    fi
    SUDO="sudo"
    if [ "$EUID" -eq 0 ]; then
        SUDO=""
    fi
}

# 检测操作系统
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    else
        OS="unknown"
    fi
    log "检测到操作系统: $OS"
}

# 安装依赖
install_dependencies() {
    log "安装基础依赖..."

    $SUDO apt update

    # Node.js 18
    curl -fsSL https://deb.nodesource.com/setup_18.x | $SUDO bash - || error "Node.js 安装失败"
    $SUDO apt install -y nodejs

    # PostgreSQL + Redis
    $SUDO apt install -y postgresql postgresql-contrib redis-server git curl

    $SUDO systemctl enable --now postgresql redis

    log "依赖安装完成 ✓"
}

# 配置数据库
setup_database() {
    log "配置数据库..."

    DB_NAME="cognitive_brain"
    DB_USER="cognitivebrain"
    DB_PASS="cog_brain_2024"

    $SUDO -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || warn "数据库已存在"
    $SUDO -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" 2>/dev/null || warn "用户已存在"
    $SUDO -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null

    $SUDO -u postgres psql -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>/dev/null || warn "vector 扩展已存在"
    $SUDO -u postgres psql -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;" 2>/dev/null || warn "pg_trgm 扩展已存在"

    $SUDO -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $DB_USER;"
    $SUDO -u postgres psql -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"
    $SUDO -u postgres psql -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;"

    # 建表
    $SUDO -u postgres psql -d "$DB_NAME" << 'EOF' 2>/dev/null || warn "表已存在"
CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'general',
    importance FLOAT DEFAULT 0.5,
    embedding vector(384),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS associations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    to_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    weight FLOAT DEFAULT 0.5,
    relation_type VARCHAR(50),
    UNIQUE(from_id, to_id)
);

CREATE INDEX IF NOT EXISTS ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS ON memories USING gin (content gin_trgm_ops);
EOF

    log "数据库配置完成 ✓"
    log "  数据库名: $DB_NAME"
    log "  用户名: $DB_USER"
    log "  密码: $DB_PASS"
}

# 安装 Cognitive Brain Skill
install_skill() {
    log "安装 Cognitive Brain Skill..."

    SKILL_DIR="$HOME/.openclaw/workspace/skills/cognitive-brain"

    if [ -d "$SKILL_DIR" ]; then
        warn "Cognitive Brain 已存在，跳过下载"
    else
        # 这里需要替换为实际仓库地址
        warn "请手动克隆 Cognitive Brain 到: $SKILL_DIR"
        warn "git clone <repo> $SKILL_DIR"
    fi

    if [ -d "$SKILL_DIR" ]; then
        cd "$SKILL_DIR"
        npm install 2>/dev/null || warn "npm install 失败，请手动执行"
    fi

    # 配置 config.json
    if [ -f "$SKILL_DIR/config.json" ]; then
        log "更新 config.json..."
        cat > "$SKILL_DIR/config.json" << EOF
{
  "storage": {
    "primary": {
      "type": "postgresql",
      "host": "localhost",
      "port": 5432,
      "database": "cognitive_brain",
      "user": "cognitivebrain",
      "password": "cog_brain_2024"
    },
    "cache": {
      "type": "redis",
      "host": "localhost",
      "port": 6379
    }
  },
  "embedding": {
    "provider": "local"
  }
}
EOF
        log "config.json 更新完成 ✓"
    fi

    log "Skill 安装完成 ✓"
}

# 配置 Cron
setup_cron() {
    log "配置定时任务..."

    CRON_CMD1="0 3 * * * cd $HOME/.openclaw/workspace/skills/cognitive-brain && node scripts/forget.cjs >> $HOME/.openclaw/logs/brain-forget.log 2>&1"
    CRON_CMD2="0 4 * * * cd $HOME/.openclaw/workspace/skills/cognitive-brain && node scripts/reflect.cjs >> $HOME/.openclaw/logs/brain-reflect.log 2>&1"
    CRON_CMD3="0 5 * * * cd $HOME/.openclaw/workspace/skills/cognitive-brain && node scripts/autolearn.cjs >> $HOME/.openclaw/logs/brain-autolearn.log 2>&1"

    # 创建日志目录
    mkdir -p $HOME/.openclaw/logs

    # 检查是否已添加
    if crontab -l 2>/dev/null | grep -q "brain-forget.cjs"; then
        warn "Cron 任务已存在，跳过"
    else
        (crontab -l 2>/dev/null; echo "$CRON_CMD1"; echo "$CRON_CMD2"; echo "$CRON_CMD3") | crontab -
        log "Cron 任务添加完成 ✓"
    fi
}

# 验证部署
verify() {
    log "验证部署..."

    # 检查服务
    $SUDO systemctl is-active postgresql >/dev/null 2>&1 && log "PostgreSQL: ✓" || error "PostgreSQL 未运行"
    $SUDO systemctl is-active redis >/dev/null 2>&1 && log "Redis: ✓" || error "Redis 未运行"

    # 检查数据库连接
    PGPASSWORD=cog_brain_2024 psql -h localhost -U cognitivebrain -d cognitive_brain -c "SELECT 1;" >/dev/null 2>&1 && log "数据库连接: ✓" || error "数据库连接失败"

    # 检查 Skill
    [ -d "$HOME/.openclaw/workspace/skills/cognitive-brain" ] && log "Skill 目录: ✓" || warn "Skill 目录不存在"

    log ""
    log "========================================="
    log "  部署完成！"
    log "========================================="
    log ""
    log "下一步："
    log "  1. 克隆 Cognitive Brain Skill"
    log "  2. 启用 Hook: cp -r hooks/cognitive-recall ~/.openclaw/hooks/ && openclaw hooks enable cognitive-recall"
    log "  3. 测试: cd ~/.openclaw/workspace/skills/cognitive-brain && node scripts/encode.cjs --content '测试' --metadata '{\"type\":\"fact\",\"importance\":0.8}'"
    log ""
}

# 主流程
main() {
    echo "========================================="
    echo "  Cognitive Brain 部署脚本"
    echo "========================================="
    echo ""

    check_permissions
    detect_os
    install_dependencies
    setup_database
    install_skill
    setup_cron
    verify
}

main "$@"
