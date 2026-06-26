#!/bin/bash
# enable-autostart.sh - 设置云存储挂载开机自启
# 使用 systemd user service 实现（无需 sudo）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.config/cloud-mount/config.sh"
SERVICE_NAME="cloud-mount"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/${SERVICE_NAME}.service"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查配置文件
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_warn "配置文件不存在：$CONFIG_FILE"
        echo ""
        echo "正在创建默认配置..."
        mkdir -p "$(dirname "$CONFIG_FILE")"

        cat > "$CONFIG_FILE" << 'EOF'
# cloud-mount 配置文件

# 云存储远程名称（rclone config 中配置的名字）
CLOUD_REMOTE="onedrive"

# 本地挂载点
MOUNT_POINT="$HOME/cloud-storage/onedrive"

# 挂载选项
MOUNT_OPTIONS="--vfs-cache-mode writes --vfs-cache-max-size 1G"

# 是否开机自启
AUTO_START=true
EOF

        log_info "默认配置已创建，请编辑后重新运行："
        echo "  nano $CONFIG_FILE"
        exit 1
    fi

    source "$CONFIG_FILE"

    if [ -z "$CLOUD_REMOTE" ] || [ -z "$MOUNT_POINT" ]; then
        log_error "配置文件中缺少必要参数"
        echo "请确保配置了:"
        echo "  CLOUD_REMOTE=..."
        echo "  MOUNT_POINT=..."
        exit 1
    fi

    # 展开 $HOME 和 ~
    MOUNT_POINT="${MOUNT_POINT/#\~/$HOME}"
    MOUNT_POINT="${MOUNT_POINT/\$HOME/$HOME}"

    log_info "使用配置:"
    echo "  云存储：$CLOUD_REMOTE"
    echo "  挂载点：$MOUNT_POINT"
}

# 检查 rclone 配置
check_rclone() {
    if ! command -v rclone &> /dev/null; then
        log_error "rclone 未安装"
        exit 1
    fi

    if ! rclone config show "$CLOUD_REMOTE" &> /dev/null; then
        log_error "rclone 配置中找不到 '$CLOUD_REMOTE'"
        echo "请先运行：rclone config"
        exit 1
    fi
}

# 检查 systemd --user 是否可用
check_systemd_user() {
    if ! systemctl --user status &> /dev/null; then
        log_error "systemd user session 不可用"
        echo ""
        echo "可能原因："
        echo "  1. 系统不支持 systemd（如部分容器环境）"
        echo "  2. SSH 环境下需手动启用用户会话持久化"
        echo ""
        echo "SSH 环境提示：若需登出后服务继续运行，请咨询系统管理员"
        exit 1
    fi
}

# 查找 rclone 路径
find_rclone() {
    RCLONE_BIN=$(command -v rclone)
    if [ -z "$RCLONE_BIN" ]; then
        log_error "找不到 rclone 可执行文件"
        exit 1
    fi
    log_info "rclone 路径：$RCLONE_BIN"
}

# 创建 systemd user 服务文件
create_service() {
    mkdir -p "$SERVICE_DIR"

    log_info "创建 systemd user 服务文件..."

    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Cloud Storage Mount ($CLOUD_REMOTE)
After=network-online.target
Wants=network-online.target

[Service]
Type=forking
Environment="HOME=$HOME"
ExecStart=$RCLONE_BIN mount $CLOUD_REMOTE: $MOUNT_POINT --daemon --vfs-cache-mode writes --vfs-cache-max-size 1G
ExecStop=/bin/fusermount -u $MOUNT_POINT || /bin/true
Restart=on-failure
RestartSec=10
StartLimitBurst=3
StartLimitInterval=60s

# 资源限制
MemoryMax=512M
MemoryHigh=256M

[Install]
WantedBy=default.target
EOF

    log_info "服务文件已创建：$SERVICE_FILE"
}

# 启用服务
enable_service() {
    log_info "重新加载 systemd user 配置..."
    systemctl --user daemon-reload

    log_info "启用服务..."
    systemctl --user enable "$SERVICE_NAME"

    log_info "启动服务..."
    systemctl --user start "$SERVICE_NAME"

    sleep 2
    if systemctl --user is-active --quiet "$SERVICE_NAME"; then
        log_info "✓ 服务已成功启动"
    else
        log_warn "服务启动失败，查看日志："
        echo "  journalctl --user -u $SERVICE_NAME -n 50"
    fi
}

# 显示状态
show_status() {
    echo ""
    log_info "服务状态:"
    systemctl --user status "$SERVICE_NAME" --no-pager -n 10 || true

    echo ""
    log_info "挂载状态:"
    if mount | grep -q "$MOUNT_POINT"; then
        echo -e "  ${GREEN}✓ 已挂载${NC}"
    else
        echo -e "  ${RED}✗ 未挂载${NC}"
    fi
}

# 卸载服务
uninstall_service() {
    log_info "停止服务..."
    systemctl --user stop "$SERVICE_NAME" || true

    log_info "禁用服务..."
    systemctl --user disable "$SERVICE_NAME" || true

    if [ -f "$SERVICE_FILE" ]; then
        log_info "删除服务文件..."
        rm -f "$SERVICE_FILE"
        systemctl --user daemon-reload
    fi

    log_info "✓ 服务已卸载"
}

# 显示帮助
show_help() {
    echo "用法：$0 [command]"
    echo ""
    echo "命令:"
    echo "  enable     启用开机自启 (默认)"
    echo "  disable    禁用开机自启"
    echo "  status     显示服务状态"
    echo "  restart    重启服务"
    echo "  logs       查看服务日志"
    echo "  --help     显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 enable"
    echo "  $0 status"
    echo "  $0 logs"
    echo ""
    echo "注意：此脚本使用 systemd user service，无需 sudo 权限。"
}

# 主函数
main() {
    case "${1:-enable}" in
        enable)
            check_config
            check_rclone
            check_systemd_user
            find_rclone
            create_service
            enable_service
            show_status
            ;;
        disable)
            uninstall_service
            ;;
        status)
            check_config
            show_status
            ;;
        restart)
            log_info "重启服务..."
            systemctl --user restart "$SERVICE_NAME"
            show_status
            ;;
        logs)
            journalctl --user -u "$SERVICE_NAME" --no-pager -n 50
            ;;
        --help|-h)
            show_help
            ;;
        *)
            log_error "未知命令：$1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
