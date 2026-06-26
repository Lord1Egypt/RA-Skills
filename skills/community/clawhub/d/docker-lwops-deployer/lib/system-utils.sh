#!/bin/bash
#
# 系统检测工具函数库
# 提供系统类型、架构、cgroup 等检测功能
#

# 检测操作系统类型
# 返回值: ubuntu|debian|centos|rhel|fedora|arch|unknown
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release

        # 方法 1：优先使用 ID_LIKE 字段（自动检测兼容性）
        if [ -n "$ID_LIKE" ]; then
            # ID_LIKE 是空格或逗号分隔的列表
            # 将逗号替换为空格，统一处理
            local id_like=$(echo "$ID_LIKE" | tr ',' ' ')

            for parent_id in $id_like; do
                case "$parent_id" in
                    rhel|centos)
                        echo "centos"
                        return 0
                        ;;
                    debian)
                        echo "debian"
                        return 0
                        ;;
                    ubuntu)
                        echo "ubuntu"
                        return 0
                        ;;
                    fedora)
                        echo "fedora"
                        return 0
                        ;;
                    arch)
                        echo "arch"
                        return 0
                        ;;
                esac
            done
        fi

        # 方法 2：显式匹配（用于 ID_LIKE 不存在或未覆盖的情况）
        case "$ID" in
            ubuntu)
                echo "ubuntu"
                ;;
            debian)
                echo "debian"
                ;;
            # RHEL/CentOS 衍生系统
            centos|rhel|rocky|almalinux|anolis|openeuler|kylin|oracle|scientific|vzlinux|tencentos)
                echo "centos"
                ;;
            fedora)
                echo "fedora"
                ;;
            # Arch 衍生系统
            arch|manjaro|endeavouros)
                echo "arch"
                ;;
            # Debian 衍生系统
            deepin|linuxmint|elementaryos)
                echo "debian"
                ;;
            *)
                echo "unknown"
                ;;
        esac
    elif [ -f /etc/redhat-release ]; then
        # 传统 RHEL/CentOS 检测方法
        echo "centos"
    elif [ -f /etc/debian_version ]; then
        # 传统 Debian 检测方法
        echo "debian"
    else
        echo "unknown"
    fi
}

# 检测系统架构
# 返回值: x86_64|aarch64|unknown
detect_architecture() {
    local arch=$(uname -m)
    case "$arch" in
        x86_64|amd64)
            echo "x86_64"
            ;;
        aarch64|arm64)
            echo "aarch64"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# 根据架构获取镜像名称
# 参数: $1 - 架构 (x86_64|aarch64)
# 返回值: 镜像名称
get_image_name() {
    local arch="$1"
    case "$arch" in
        x86_64)
            echo "swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_x86_image:latest"
            ;;
        aarch64)
            echo "swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_arm_image:latest"
            ;;
        *)
            echo ""
            ;;
    esac
}

# 检测 cgroup 版本
# 返回值: v1|v2
detect_cgroup_version() {
    if [ -f /sys/fs/cgroup/cgroup.controllers ]; then
        echo "v2"
    else
        echo "v1"
    fi
}

# 检查 sudo 权限
# 返回值: 0=有权限, 1=无权限
check_sudo() {
    if [ "$EUID" -eq 0 ]; then
        # 已经是 root 用户
        return 0
    elif sudo -n true 2>/dev/null; then
        # sudo 有 nopasswd 权限
        return 0
    else
        # 需要密码或没有权限
        return 1
    fi
}

# 检查是否为 root 或有 sudo 权限
# 返回值: 0=有权限, 1=无权限
require_root() {
    if ! check_sudo; then
        return 1
    fi
    return 0
}

# 获取系统信息摘要
# 返回 JSON 格式的系统信息
get_system_info() {
    local os=$(detect_os)
    local arch=$(detect_architecture)
    local cgroup=$(detect_cgroup_version)

    cat <<EOF
{
  "os": "$os",
  "architecture": "$arch",
  "cgroup_version": "$cgroup"
}
EOF
}

# 获取详细的系统信息（用于调试）
# 输出详细的操作系统检测信息
get_system_info_debug() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        cat <<EOF
操作系统检测详情：
  ID: $ID
  ID_LIKE: $ID_LIKE
  NAME: $NAME
  VERSION: $VERSION
  检测结果: $(detect_os)
EOF
    else
        echo "无法找到 /etc/os-release 文件"
    fi
}
