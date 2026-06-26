#!/bin/bash
# check-mount.sh - 检测云存储挂载状态
# 用法：./check-mount.sh [mount_point|--all]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# 检查单个挂载点
check_single_mount() {
    local mount_point="$1"
    
    if [ ! -d "$mount_point" ]; then
        log_error "目录不存在：$mount_point"
        return 1
    fi
    
    if mount | grep -q "$mount_point"; then
        echo -e "${GREEN}✓${NC} $mount_point - 已挂载"
        
        # 显示详细信息
        mount_info=$(mount | grep "$mount_point")
        echo "  挂载源：$(echo "$mount_info" | awk '{print $1}')"
        echo "  文件系统：$(echo "$mount_info" | awk '{print $5}')"
        
        # 检查是否可读写
        if [ -w "$mount_point" ]; then
            echo -e "  权限：${GREEN}可读写${NC}"
        else
            echo -e "  权限：${RED}只读${NC}"
        fi
        
        # 检查 rclone 进程
        if pgrep -f "rclone.*$mount_point" > /dev/null; then
            pid=$(pgrep -f "rclone.*$mount_point" | head -1)
            echo -e "  进程：${GREEN}运行中 (PID: $pid)${NC}"
        else
            echo -e "  进程：${RED}未找到${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}✗${NC} $mount_point - 未挂载"
        
        # 检查是否有残留进程
        if pgrep -f "rclone.*$mount_point" > /dev/null; then
            echo -e "  ${YELLOW}警告：发现残留进程，建议清理${NC}"
            pgrep -f "rclone.*$mount_point" | while read pid; do
                echo "    PID: $pid"
            done
        fi
        
        return 1
    fi
}

# 检查所有云存储挂载
check_all_mounts() {
    log_info "检查所有云存储挂载..."
    echo ""
    
    local total=0
    local mounted=0
    local failed=0
    
    # 检查 ~/cloud-storage/ 下的所有目录
    if [ -d "$HOME/cloud-storage" ]; then
        for mount_point in "$HOME/cloud-storage/"*/; do
            if [ -d "$mount_point" ]; then
                ((total++))
                mount_point="${mount_point%/}" # 去掉末尾斜杠
                if check_single_mount "$mount_point"; then
                    ((mounted++))
                else
                    ((failed++))
                fi
                echo ""
            fi
        done
    fi
    
    # 检查其他常见挂载点
    for mount_point in "$HOME/onedrive" "$HOME/gdrive" "$HOME/dropbox"; do
        if [ -d "$mount_point" ]; then
            ((total++))
            if check_single_mount "$mount_point"; then
                ((mounted++))
            else
                ((failed++))
            fi
            echo ""
        fi
    done
    
    # 总结
    echo "─────────────────────────────────"
    echo "总计：$total 个挂载点"
    echo -e "已挂载：${GREEN}$mounted${NC}"
    echo -e "未挂载：${RED}$failed${NC}"
    
    if [ $failed -gt 0 ]; then
        echo ""
        log_warn "有 $failed 个挂载点未挂载"
        echo "使用以下命令重新挂载:"
        echo "  ~/cloud-mount/scripts/mount-cloud.sh <remote_name>"
        return 1
    else
        log_info "所有挂载点正常"
        return 0
    fi
}

# 检查 rclone 进程
check_rclone_processes() {
    log_info "rclone 进程状态:"
    echo ""
    
    if pgrep -f "rclone" > /dev/null; then
        echo "运行中的 rclone 进程:"
        ps aux | grep "rclone" | grep -v grep | while read line; do
            pid=$(echo "$line" | awk '{print $2}')
            cmd=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf $i" "; print ""}')
            echo "  PID $pid: $cmd"
        done
    else
        echo "  没有运行中的 rclone 进程"
    fi
}

# 显示帮助
show_help() {
    echo "用法：$0 [mount_point|--all|--processes]"
    echo ""
    echo "参数:"
    echo "  mount_point    要检查的挂载点路径"
    echo "  --all, -a      检查所有云存储挂载"
    echo "  --processes, -p  只显示 rclone 进程"
    echo "  --help, -h     显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 ~/cloud-storage/onedrive"
    echo "  $0 --all"
    echo "  $0 --processes"
}

# 主函数
main() {
    case "$1" in
        --all|-a)
            check_all_mounts
            ;;
        --processes|-p)
            check_rclone_processes
            ;;
        --help|-h)
            show_help
            ;;
        "")
            # 无参数时检查所有
            check_all_mounts
            ;;
        *)
            check_single_mount "$1"
            ;;
    esac
}

main "$@"
