#!/bin/bash
# mount-cloud.sh - 一键挂载云存储
# 用法：./mount-cloud.sh <remote_name> [mount_point]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.config/cloud-mount/config.sh"

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

# 检查 rclone 是否安装
check_rclone() {
    if ! command -v rclone &> /dev/null; then
        log_error "rclone 未安装"
        echo "请先安装 rclone: https://rclone.org/install/"
        exit 1
    fi
    log_info "rclone 已安装：$(rclone --version | head -1)"
}

# 检查配置
check_config() {
    if [ -n "$1" ]; then
        REMOTE_NAME="$1"
    elif [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
        REMOTE_NAME="${CLOUD_REMOTE:-onedrive}"
    else
        REMOTE_NAME="onedrive"
    fi

    if [ -n "$2" ]; then
        MOUNT_POINT="$2"
    elif [ -n "$MOUNT_POINT" ]; then
        : # 使用配置文件中的值
    else
        MOUNT_POINT="$HOME/cloud-storage/$REMOTE_NAME"
    fi
}

# 检查 rclone 配置是否存在
check_rclone_config() {
    if ! rclone config show "$REMOTE_NAME" &> /dev/null; then
        log_error "rclone 配置中找不到 '$REMOTE_NAME'"
        echo ""
        echo "请先配置 rclone:"
        echo "  rclone config"
        echo ""
        echo "或列出可用配置:"
        echo "  rclone config show"
        exit 1
    fi
    log_info "使用云存储配置：$REMOTE_NAME"
}

# 创建挂载点
create_mount_point() {
    if [ ! -d "$MOUNT_POINT" ]; then
        log_info "创建挂载点：$MOUNT_POINT"
        mkdir -p "$MOUNT_POINT"
    fi
}

# 检查是否已挂载
check_mounted() {
    if mount | grep -q "$MOUNT_POINT"; then
        log_warn "$MOUNT_POINT 已经挂载"
        echo ""
        echo "挂载信息:"
        mount | grep "$MOUNT_POINT"
        echo ""
        read -p "是否重新挂载？(y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
        
        # 卸载
        log_info "卸载旧挂载..."
        fusermount -u "$MOUNT_POINT" 2>/dev/null || umount "$MOUNT_POINT" 2>/dev/null || true
        sleep 2
    fi
}

# 挂载云存储
do_mount() {
    log_info "正在挂载 $REMOTE_NAME: 到 $MOUNT_POINT ..."
    
    # 默认挂载选项
    MOUNT_OPTS="--daemon --vfs-cache-mode writes --vfs-cache-max-size 1G"
    
    # 如果配置文件中有额外选项，追加
    if [ -n "$MOUNT_OPTIONS" ]; then
        MOUNT_OPTS="$MOUNT_OPTS $MOUNT_OPTIONS"
    fi
    
    # 执行挂载
    rclone mount "$REMOTE_NAME:" "$MOUNT_POINT" $MOUNT_OPTS
    
    # 等待挂载完成
    sleep 2
    
    # 验证
    if mount | grep -q "$MOUNT_POINT"; then
        log_info "✓ 挂载成功！"
        echo ""
        echo "挂载点：$MOUNT_POINT"
        echo ""
        echo "使用示例:"
        echo "  ls $MOUNT_POINT"
        echo "  cd $MOUNT_POINT"
        echo ""
        echo "查看挂载状态:"
        echo "  $SCRIPT_DIR/check-mount.sh $MOUNT_POINT"
    else
        log_error "挂载失败，请检查日志"
        exit 1
    fi
}

# 显示状态
show_status() {
    log_info "云存储挂载状态:"
    echo ""
    
    # 查找所有 rclone 挂载进程
    if pgrep -f "rclone.*mount" > /dev/null; then
        echo "运行中的 rclone 挂载:"
        ps aux | grep "rclone.*mount" | grep -v grep | awk '{print "  PID: "$2", 命令: "$11" "$12" "$13}'
    else
        echo "没有找到运行中的 rclone 挂载"
    fi
    
    echo ""
    
    # 检查常见挂载点
    for mount_point in "$HOME/cloud-storage/"*/; do
        if [ -d "$mount_point" ]; then
            if mount | grep -q "$mount_point"; then
                echo -e "✓ ${mount_point} - 已挂载"
            else
                echo -e "✗ ${mount_point} - 未挂载"
            fi
        fi
    done
}

# 主函数
main() {
    # 特殊参数：--status
    if [ "$1" = "--status" ] || [ "$1" = "-s" ]; then
        show_status
        exit 0
    fi
    
    # 特殊参数：--help
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "用法：$0 <remote_name> [mount_point]"
        echo ""
        echo "参数:"
        echo "  remote_name    rclone 配置的远程名称 (默认：onedrive)"
        echo "  mount_point    本地挂载点 (默认：~/cloud-storage/<remote_name>)"
        echo ""
        echo "选项:"
        echo "  --status, -s   显示所有挂载状态"
        echo "  --help, -h     显示帮助"
        echo ""
        echo "示例:"
        echo "  $0 onedrive"
        echo "  $0 gdrive ~/my-drive"
        echo "  $0 --status"
        exit 0
    fi
    
    check_rclone
    check_config "$1" "$2"
    check_rclone_config
    create_mount_point
    check_mounted
    do_mount
}

main "$@"
