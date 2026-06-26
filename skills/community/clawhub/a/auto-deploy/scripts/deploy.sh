#!/bin/bash
# 自动化部署脚本 - Peninsula Points 项目 (服务器构建版)
# 用法：./deploy.sh [分支名]

set -e

SCRIPT_DIR="$(dirname "$0")"
CONFIG_FILE="$SCRIPT_DIR/../deploy-config.json"
SSH_KEY="$HOME/.ssh/server_deploy"
WORKSPACE="/home/node/clawd/workspace/points"

# 读取配置（使用 Python 代替 jq）
read_json() {
    python3 -c "import json; data=json.load(open('$CONFIG_FILE')); print(data$1)"
}

GIT_URL=$(read_json "['git']['url']")
GIT_BRANCH=$(read_json "['git']['branch']")
GIT_USER=$(read_json "['git']['auth']['username']")
GIT_PASS=$(read_json "['git']['auth']['password']")
SERVER_HOST=$(read_json "['server']['host']")
SERVER_PORT=$(read_json "['server']['port']")
SERVER_USER=$(read_json "['server']['user']")
DEPLOY_PATH=$(read_json "['server']['deployPath']")
BACKUP_PATH=$(read_json "['server']['backupPath']")

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_step() { echo -e "\n${BLUE}════════════════════════════════════════${NC}"; echo -e "${BLUE}▶ $1${NC}"; echo -e "${BLUE}════════════════════════════════════════${NC}\n"; }
log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

echo "========================================"
echo "  Peninsula Points - 自动化部署"
echo "========================================"
log_info "Git 仓库：$GIT_URL"
log_info "分支：${1:-$GIT_BRANCH}"
log_info "服务器：$SERVER_USER@$SERVER_HOST:$SERVER_PORT"
log_info "部署路径：$DEPLOY_PATH"
echo "========================================"

# 步骤 1：服务器端拉取代码
log_step "步骤 1/5: 服务器端拉取最新代码"

ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" << EOF
set -e
cd /tmp
if [ -d "points-build" ]; then
    cd points-build
    git checkout -f
    git clean -fd
    git pull origin ${1:-$GIT_BRANCH}
else
    git clone http://${GIT_USER}:${GIT_PASS}@${GIT_URL#http://} points-build
    cd points-build
fi
COMMIT_HASH=\$(git rev-parse --short HEAD)
COMMIT_MSG=\$(git log -1 --oneline | cut -d' ' -f2-)
echo "当前版本：\$COMMIT_HASH - \$COMMIT_MSG"
echo "\$COMMIT_HASH" > /tmp/deploy-commit.txt
echo "\$COMMIT_MSG" >> /tmp/deploy-commit.txt
EOF

log_info "代码已更新"

# 步骤 2：服务器端构建
log_step "步骤 2/5: 构建前端和后端"

ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" << 'EOF'
set -e
cd /tmp/points-build

echo "  [1/3] 构建前端..."
cd peninsula-ui/front
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps --silent
npm run build:prod
echo "  ✓ 前端构建完成"

echo ""
echo "  [2/3] 构建后端..."
cd /tmp/points-build
mvn clean package -DskipTests -q
JAR_FILE=$(find peninsula-system/target -name "*.jar" -type f ! -name "*-sources.jar" ! -name "*-javadoc.jar" | head -1)
echo "  ✓ 后端构建完成：$(basename $JAR_FILE)"

echo ""
echo "  [3/3] 准备部署包..."
cd /tmp/points-build
tar -czf /tmp/points-deploy.tar.gz \
    peninsula-ui/front/dist \
    peninsula-system/target/*.jar

echo "  ✓ 部署包已创建：$(du -sh /tmp/points-deploy.tar.gz | cut -f1)"
EOF

log_info "构建完成"

# 步骤 3：备份服务器当前版本
log_step "步骤 3/5: 备份服务器当前版本"

BACKUP_NAME="points_$(date +%Y%m%d_%H%M%S)"
ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" << EOF
  mkdir -p $BACKUP_PATH
  if [ -d "$DEPLOY_PATH" ] && [ "\$(ls -A $DEPLOY_PATH)" ]; then
    cp -r $DEPLOY_PATH $BACKUP_PATH/$BACKUP_NAME
    echo "备份完成：$BACKUP_PATH/$BACKUP_NAME"
  else
    echo "首次部署，创建目录..."
    mkdir -p $DEPLOY_PATH
  fi
EOF

log_info "备份名称：$BACKUP_NAME"

# 步骤 4：解压部署
log_step "步骤 4/5: 部署到服务器"

ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" << EOF
  set -e
  
  echo "  [1/3] 解压部署包..."
  rm -rf $DEPLOY_PATH/*
  tar -xzf /tmp/points-deploy.tar.gz -C $DEPLOY_PATH
  
  echo "  [2/3] 停止旧服务..."
  pm2 stop peninsula 2>/dev/null || true
  
  echo "  [3/3] 启动新服务..."
  cd $DEPLOY_PATH
  JAR_FILE=\$(find $DEPLOY_PATH/peninsula-system/target -name "*.jar" -type f ! -name "*-sources.jar" ! -name "*-javadoc.jar" | head -1)
  if [ ! -z "\$JAR_FILE" ]; then
    pm2 delete peninsula 2>/dev/null || true
    pm2 start \$JAR_FILE --name peninsula
    pm2 save
    echo "  ✓ 服务已启动：\$JAR_FILE"
  fi
  
  # 清理临时文件
  rm /tmp/points-deploy.tar.gz
EOF

log_info "部署完成"

# 读取版本信息
COMMIT_INFO=$(ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" "cat /tmp/deploy-commit.txt")
COMMIT_HASH=$(echo "$COMMIT_INFO" | head -1)
COMMIT_MSG=$(echo "$COMMIT_INFO" | tail -1)

# 清理
ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" "rm -f /tmp/deploy-commit.txt"

# 部署完成摘要
echo ""
echo "========================================"
echo -e "${GREEN}  ✅ 部署成功完成！${NC}"
echo "========================================"
echo ""
echo "📋 部署摘要:"
echo "  - 代码版本：$COMMIT_HASH"
echo "  - 提交信息：$COMMIT_MSG"
echo "  - 分支：${1:-$GIT_BRANCH}"
echo "  - 部署时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "  - 备份位置：$BACKUP_PATH/$BACKUP_NAME"
echo ""
echo "🔗 访问地址:"
echo "  - 前端：http://$SERVER_HOST/"
echo "  - 后端 API: http://$SERVER_HOST:8080/"
echo ""
echo "📊 PM2 状态:"
ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" "pm2 status peninsula" 2>/dev/null || log_warn "无法获取 PM2 状态"
echo ""
echo "========================================"
