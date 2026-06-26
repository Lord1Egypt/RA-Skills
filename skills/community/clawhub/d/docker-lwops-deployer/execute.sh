#!/bin/bash
#
# Docker LwOps 部署技能 - 核心执行脚本
# 功能：自动化部署乐维监控 8.1 Docker 容器
#

set -e  # 遇到错误立即退出

# ============================================================
# 脚本目录和路径
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/lib"

# ============================================================
# 加载函数库
# ============================================================

source "$LIB_DIR/system-utils.sh"
source "$LIB_DIR/network-utils.sh"
source "$LIB_DIR/docker-utils.sh"
source "$LIB_DIR/output-utils.sh"
source "$LIB_DIR/lock-utils.sh"

# ============================================================
# 常量定义
# ============================================================

CONTAINER_NAME="lwops_rocky8_image_8.1"
DEFAULT_CONTAINER_PORT1=80
DEFAULT_CONTAINER_PORT2=8081
DEFAULT_HOST_PORT1=8000
DEFAULT_HOST_PORT2=8081

# ============================================================
# 主函数
# ============================================================

main() {
    # 读取输入（从参数或 STDIN）
    local input=""
    if [ $# -eq 0 ]; then
        # 从 STDIN 读取
        input=$(cat)
    else
        input="$1"
    fi

    # ========================================================
    # 0. 检查容器状态（快速路径）
    # ========================================================

    output_progress "检查容器状态..."

    # 检查容器是否已存在并运行
    if docker_is_running "$CONTAINER_NAME"; then
        output_progress "容器已在运行，直接返回信息"

        local host_ip=$(get_host_ip)
        local container_info=$(docker_get_container_info "$CONTAINER_NAME")

        # 提取端口信息
        local port_80=$(echo "$container_info" | grep -o '"80"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: *"\([^"]*\)".*/\1/')
        local port_8081=$(echo "$container_info" | grep -o '"8081"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: *"\([^"]*\)".*/\1/')

        local result=$(cat <<EOF
{
  "container_name": "$CONTAINER_NAME",
  "container_id": "$(sudo docker ps -a --filter "name=$CONTAINER_NAME" --format '{{.ID}}')",
  "status": "already_running",
  "message": "容器已在运行，无需重新部署",
  "host_ip": "$host_ip",
  "access_urls": {
    "http": "http://$host_ip:$port_80",
    "https": "http://$host_ip:$port_8081"
  }
}
EOF
)

        output_success "$result" "容器已在运行"
        exit 0
    fi

    # ========================================================
    # 1. 获取部署锁
    # ========================================================

    output_progress "获取部署锁..."

    # 先检查锁状态
    local lock_status=$(get_lock_status)
    local lock_status_value=$(echo "$lock_status" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: *"\([^"]*\)".*/\1/')

    if [ "$lock_status_value" = "locked" ]; then
        local lock_age=$(echo "$lock_status" | grep -o '"age_seconds"[[:space:]]*:[[:space:]]*[0-9]*' | sed 's/.*: *\([0-9]*\).*/\1/')
        local lock_pid=$(echo "$lock_status" | grep -o '"pid"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: *"\([^"]*\)".*/\1/')
        local remaining=$(echo "$lock_status" | grep -o '"remaining_seconds"[[:space:]]*:[[:space:]]*[0-9]*' | sed 's/.*: *\([0-9]*\).*/\1/')

        local suggestions='[
            "等待当前部署完成（预计还需 '$remaining' 秒）",
            "查看部署进度: sudo docker logs '$CONTAINER_NAME'",
            "检查是否有其他用户正在部署"
        ]'

        output_error "DeploymentInProgress" "另一个部署任务正在进行中（PID: $lock_pid，已运行 ${lock_age} 秒）" "$suggestions"
        exit 1
    fi

    # 尝试获取锁（带超时）
    if ! acquire_lock_with_timeout 300; then
        local suggestions='[
            "检查是否有僵尸进程占用锁",
            "手动删除锁文件: rm -f /tmp/docker-lwops-deployer/deploy.lock",
            "等待几分钟后重试"
        ]'
        output_error "LockTimeout" "获取部署锁超时，可能存在死锁" "$suggestions"
        exit 1
    fi

    output_progress "成功获取部署锁"

    # 确保退出时释放锁
    trap cleanup_lock EXIT INT TERM

    # ========================================================
    # 2. 检查系统兼容性
    # ========================================================

    output_progress "检查系统兼容性..."

    # 检测操作系统
    local os=$(detect_os)
    if [ "$os" = "unknown" ]; then
        local suggestions='[
            "检查系统是否为 RHEL/CentOS 衍生版",
            "检查 /etc/os-release 文件内容",
            "手动安装 Docker 后重新运行",
            "访问 https://github.com/lwops/docker-lwops-deployer/issues 反馈"
        ]'
        output_error "UnsupportedOS" "不支持的操作系统，请手动安装 Docker" "$suggestions"
        exit 1
    fi

    output_progress "操作系统: $os"

    # ========================================================
    # 2. 检查 sudo 权限
    # ========================================================

    output_progress "检查权限..."

    if ! require_root; then
        local suggestions='["使用 sudo 运行此脚本", "将用户添加到 sudo 组: sudo usermod -aG sudo \$USER", "配置 sudo 无密码: echo \"\$USER ALL=(ALL) NOPASSWD: ALL\" | sudo tee /etc/sudoers.d/\$USER"]'
        output_error "PermissionDenied" "需要 sudo 权限来安装和管理 Docker" "$suggestions"
        exit 1
    fi

    # ========================================================
    # 3. 确保 Docker 已安装并运行
    # ========================================================

    output_progress "检查 Docker 环境..."

    if ! ensure_docker_installed; then
        local suggestions='["Ubuntu/Debian: sudo apt-get install docker.io", "CentOS/RHEL: sudo yum install docker", "访问 https://docs.docker.com/get-docker/ 获取详细安装指南"]'
        output_error "DockerInstallFailed" "Docker 安装失败" "$suggestions"
        exit 1
    fi

    if ! ensure_docker_running; then
        local suggestions='["启动 Docker: sudo systemctl start docker", "检查 Docker 日志: sudo journalctl -u docker", "重启系统后重试"]'
        output_error "DockerNotRunning" "Docker 服务无法启动" "$suggestions"
        exit 1
    fi

    # ========================================================
    # 4. 检测系统架构
    # ========================================================

    output_progress "检测系统架构..."

    local arch=$(detect_architecture)
    if [ "$arch" = "unknown" ]; then
        local suggestions='["支持的架构: x86_64 (amd64), aarch64 (arm64)", "使用 uname -m 查看您的系统架构"]'
        output_error "UnsupportedArchitecture" "不支持的系统架构" "$suggestions"
        exit 1
    fi

    output_progress "系统架构: $arch"

    # ========================================================
    # 5. 获取镜像名称
    # ========================================================

    local image=$(get_image_name "$arch")
    if [ -z "$image" ]; then
        output_error "InvalidArchitecture" "无法获取镜像名称" "[]"
        exit 1
    fi

    output_progress "目标镜像: $image"

    # ========================================================
    # 6. 拉取镜像
    # ========================================================

    output_progress "拉取 Docker 镜像..."

    if ! docker_pull "$image"; then
        local suggestions='["检查网络连接", "检查镜像地址是否正确", "尝试手动拉取: sudo docker pull $image"]'
        output_error "ImagePullFailed" "镜像拉取失败" "$suggestions"
        exit 1
    fi

    # ========================================================
    # 7. 智能分配端口
    # ========================================================

    output_progress "检查端口可用性..."

    local ports_json=$(allocate_ports "$DEFAULT_CONTAINER_PORT1" "$DEFAULT_CONTAINER_PORT2" "$DEFAULT_HOST_PORT1" "$DEFAULT_HOST_PORT2")
    if [ $? -ne 0 ]; then
        local suggestions='["释放被占用的端口", "检查防火墙设置", "使用其他端口"]'
        output_error "PortAllocationFailed" "无法分配可用端口" "$suggestions"
        exit 1
    fi

    local host_port1=$(echo "$ports_json" | get_json_number "host_port1")
    local host_port2=$(echo "$ports_json" | get_json_number "host_port2")

    output_progress "端口映射: ${host_port1}:80, ${host_port2}:8081"

    # ========================================================
    # 8. 检测 cgroup 版本
    # ========================================================

    output_progress "检测 cgroup 版本..."

    local cgroup_version=$(detect_cgroup_version)
    local cgroup_mode="ro"
    if [ "$cgroup_version" = "v2" ]; then
        cgroup_mode="rw"
        output_warning "检测到 cgroup v2，使用读写模式挂载"
    fi

    output_progress "cgroup 版本: $cgroup_version, 挂载模式: $cgroup_mode"

    # ========================================================
    # 9. 启动容器
    # ========================================================

    output_progress "启动容器: $CONTAINER_NAME"

    if ! docker_start_container "$CONTAINER_NAME" "$image" "$host_port1" "$host_port2" "$cgroup_mode"; then
        local suggestions='["检查 Docker 日志: sudo docker logs $CONTAINER_NAME", "检查镜像是否完整", "尝试重新拉取镜像"]'
        output_error "ContainerStartFailed" "容器启动失败" "$suggestions"
        exit 1
    fi

    # ========================================================
    # 10. 等待容器完全启动
    # ========================================================

    output_progress "等待容器启动..."

    local max_wait=30
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if docker_is_running "$CONTAINER_NAME"; then
            break
        fi
        sleep 1
        waited=$((waited + 1))
    done

    if ! docker_is_running "$CONTAINER_NAME"; then
        local suggestions='["检查容器日志: sudo docker logs $CONTAINER_NAME", "检查系统资源是否充足", "尝试重启 Docker 服务"]'
        output_error "ContainerNotRunning" "容器启动后未运行" "$suggestions"
        exit 1
    fi

    # ========================================================
    # 11. 获取主机 IP
    # ========================================================

    output_progress "获取访问地址..."

    local host_ip=$(get_host_ip)

    # ========================================================
    # 12. 输出成功结果
    # ========================================================

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    local result=$(cat <<EOF
{
  "container_name": "$CONTAINER_NAME",
  "container_id": "$(sudo docker ps -a --filter "name=$CONTAINER_NAME" --format '{{.ID}}')",
  "status": "running",
  "architecture": "$arch",
  "image": "$image",
  "host_ip": "$host_ip",
  "ports": {
    "http": {
      "container_port": $DEFAULT_CONTAINER_PORT1,
      "host_port": $host_port1,
      "url": "http://$host_ip:$host_port1"
    },
    "https": {
      "container_port": $DEFAULT_CONTAINER_PORT2,
      "host_port": $host_port2,
      "url": "http://$host_ip:$host_port2"
    }
  },
  "cgroup_version": "$cgroup_version",
  "cgroup_mount_mode": "$cgroup_mode",
  "timestamp": "$timestamp"
}
EOF
)

    output_success "$result" "容器部署成功"

    # ========================================================
    # 13. 输出访问信息（便于用户查看）
    # ========================================================

    echo "" >&2
    echo "========================================" >&2
    echo "容器部署成功！" >&2
    echo "========================================" >&2
    echo "容器名称: $CONTAINER_NAME" >&2
    echo "容器 ID: $(sudo docker ps -a --filter "name=$CONTAINER_NAME" --format '{{.ID}}')" >&2
    echo "系统架构: $arch" >&2
    echo "" >&2
    echo "访问地址：" >&2
    echo "  - HTTP:  http://$host_ip:$host_port1" >&2
    echo "  - HTTPS: http://$host_ip:$host_port2" >&2
    echo "" >&2
    echo "管理命令：" >&2
    echo "  - 查看日志: sudo docker logs $CONTAINER_NAME" >&2
    echo "  - 进入容器: sudo docker exec -it $CONTAINER_NAME bash" >&2
    echo "  - 停止容器: sudo docker stop $CONTAINER_NAME" >&2
    echo "  - 启动容器: sudo docker start $CONTAINER_NAME" >&2
    echo "  - 删除容器: sudo docker rm -f $CONTAINER_NAME" >&2
    echo "========================================" >&2

    exit 0
}

# ============================================================
# 执行主函数
# ============================================================

main "$@"
