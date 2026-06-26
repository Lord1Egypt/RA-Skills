#!/usr/bin/env bash
# ============================================================
# TokenBroker Skill — 安装初始化脚本
# 检测后端服务，自动启动
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }

BROKER_PORT=${BROKER_PORT:-8766}
BROKER_URL="http://localhost:${BROKER_PORT}"

echo "╔══════════════════════════════════════╗"
echo "║  TokenBroker Skill — 初始化          ║"
echo "╚══════════════════════════════════════╝"

# 1. 检测后端是否已在运行
if curl -s --connect-timeout 2 "${BROKER_URL}/api/health" > /dev/null 2>&1; then
  info "TokenBroker 后端服务已在运行 (端口 ${BROKER_PORT})"
  exit 0
fi

# 2. 尝试启动
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BROKER_DIR="$(cd "${PROJECT_DIR}/../../production-system/token-broker" 2>/dev/null && pwd)"

if [ -z "${BROKER_DIR}" ]; then
  warn "未找到 production-system/token-broker 目录"
  warn "请手动启动 TokenBroker 服务后再安装此 Skill"
  exit 1
fi

info "检测到 TokenBroker 项目目录: ${BROKER_DIR}"

# 3. 检查依赖是否安装
if [ ! -d "${BROKER_DIR}/node_modules" ]; then
  info "安装 Node.js 依赖..."
  cd "${BROKER_DIR}" && npm install 2>&1 | tail -1
fi

# 4. 通过 Supervisor 注册（如果已安装 Supervisor）
if command -v python3 &> /dev/null && python3 -c "import supervisor" 2>/dev/null; then
  SUPERVISOR_CONF="${HOME}/supervisord.conf"
  if [ -f "${SUPERVISOR_CONF}" ]; then
    if ! grep -q "token-broker" "${SUPERVISOR_CONF}" 2>/dev/null; then
      warn "未在 Supervisor 中找到 token-broker，尝试注册..."
      # 尝试通过 supervisord 提供的 rpc 接口添加
      echo "
[program:token-broker]
command=npx ts-node ${BROKER_DIR}/src/server.ts
directory=${BROKER_DIR}
autostart=true
autorestart=true
startsecs=5
startretries=10
stopwaitsecs=5
killasgroup=true
stopsignal=TERM
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
environment=BROKER_PORT=${BROKER_PORT},NODE_ENV=production" >> "${SUPERVISOR_CONF}"
      info "已追加到 Supervisor 配置"
      python3 -m supervisor.supervisorctl -c "${SUPERVISOR_CONF}" reread 2>/dev/null || true
      python3 -m supervisor.supervisorctl -c "${SUPERVISOR_CONF}" update 2>/dev/null || true
      sleep 2
    else
      info "Supervisor 中已配置 TokenBroker"
      python3 -m supervisor.supervisorctl -c "${SUPERVISOR_CONF}" start token-broker 2>/dev/null || true
      sleep 2
    fi
  fi
fi

# 5. 验证
if curl -s --connect-timeout 3 "${BROKER_URL}/api/health" > /dev/null 2>&1; then
  info "TokenBroker 服务已启动: ${BROKER_URL}"
else
  warn "尚未启动，请在后端运行："
  warn "  cd ${BROKER_DIR} && npx ts-node src/server.ts"
fi
