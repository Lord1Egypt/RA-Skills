#!/bin/bash
#
# Docker 操作工具函数库
# 提供 Docker 安装、容器管理等功能
#

# 检查 Docker 是否已安装
# 返回值: 0=已安装, 1=未安装
check_docker_installed() {
    if command -v docker &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 安装 Docker（Ubuntu/Debian）
install_docker_ubuntu() {
    echo "正在为 Ubuntu/Debian 系统安装 Docker..."

    # 更新包索引
    sudo apt-get update -y || {
        echo "无法更新包索引"
        return 1
    }

    # 安装必要的依赖
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release || {
        echo "无法安装依赖包"
        return 1
    }

    # 添加 Docker 官方 GPG 密钥
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg || {
        echo "无法添加 Docker GPG 密钥"
        return 1
    }

    # 设置 Docker 仓库
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null || {
        echo "无法设置 Docker 仓库"
        return 1
    }

    # 更新包索引
    sudo apt-get update -y || {
        echo "无法更新包索引"
        return 1
    }

    # 安装 Docker
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io || {
        echo "无法安装 Docker"
        return 1
    }

    echo "Docker 安装成功"
    return 0
}

# 安装 Docker（CentOS/RHEL）
install_docker_centos() {
    echo "正在为 CentOS/RHEL 系统安装 Docker..."

    # 安装必要的依赖
    sudo yum install -y yum-utils || {
        echo "无法安装 yum-utils"
        return 1
    }

    # 添加 Docker 仓库
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo || {
        echo "无法添加 Docker 仓库"
        return 1
    }

    # 安装 Docker
    sudo yum install -y docker-ce docker-ce-cli containerd.io || {
        echo "无法安装 Docker"
        return 1
    }

    echo "Docker 安装成功"
    return 0
}

# 安装 Docker（Fedora）
install_docker_fedora() {
    echo "正在为 Fedora 系统安装 Docker..."

    # 安装必要的依赖
    sudo dnf -y install dnf-plugins-core || {
        echo "无法安装 dnf-plugins-core"
        return 1
    }

    # 添加 Docker 仓库
    sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo || {
        echo "无法添加 Docker 仓库"
        return 1
    }

    # 安装 Docker
    sudo dnf install -y docker-ce docker-ce-cli containerd.io || {
        echo "无法安装 Docker"
        return 1
    }

    echo "Docker 安装成功"
    return 0
}

# 安装 Docker（Arch Linux）
install_docker_arch() {
    echo "正在为 Arch Linux 系统安装 Docker..."

    # 安装 Docker
    sudo pacman -S --noconfirm docker || {
        echo "无法安装 Docker"
        return 1
    }

    echo "Docker 安装成功"
    return 0
}

# 确保 Docker 已安装
# 返回值: 0=成功, 1=失败
ensure_docker_installed() {
    if check_docker_installed; then
        echo "Docker 已安装"
        return 0
    fi

    echo "Docker 未安装，正在尝试自动安装..."

    local os=$(detect_os)
    local result=0

    case "$os" in
        ubuntu|debian)
            install_docker_ubuntu
            result=$?
            ;;
        centos)
            install_docker_centos
            result=$?
            ;;
        fedora)
            install_docker_fedora
            result=$?
            ;;
        arch)
            install_docker_arch
            result=$?
            ;;
        *)
            echo "不支持的操作系统: $os"
            return 1
            ;;
    esac

    if [ $result -eq 0 ]; then
        echo "Docker 安装完成"
        return 0
    else
        echo "Docker 安装失败"
        return 1
    fi
}

# 确保 Docker 服务运行
# 返回值: 0=运行中, 1=未运行
ensure_docker_running() {
    # 检查 Docker 服务状态
    if ! sudo systemctl is-active --quiet docker; then
        echo "正在启动 Docker 服务..."
        sudo systemctl start docker || {
            echo "无法启动 Docker 服务"
            return 1
        }
    fi

    # 设置 Docker 开机自启
    sudo systemctl enable docker >/dev/null 2>&1

    echo "Docker 服务运行中"
    return 0
}

# 拉取 Docker 镜像
# 参数: $1 - 镜像名称
# 返回值: 0=成功, 1=失败
docker_pull() {
    local image="$1"

    if [ -z "$image" ]; then
        echo "错误：镜像名称不能为空"
        return 1
    fi

    echo "正在拉取镜像: $image"

    if sudo docker pull "$image"; then
        echo "镜像拉取成功"
        return 0
    else
        echo "镜像拉取失败"
        return 1
    fi
}

# 启动 Docker 容器
# 参数:
#   $1 - 容器名称
#   $2 - 镜像名称
#   $3 - 宿主机端口1
#   $4 - 宿主机端口2
#   $5 - cgroup 挂载模式 (ro|rw)
# 返回值: 0=成功, 1=失败
docker_start_container() {
    local container_name="$1"
    local image="$2"
    local host_port1="$3"
    local host_port2="$4"
    local cgroup_mode="$5"

    if [ -z "$container_name" ] || [ -z "$image" ]; then
        echo "错误：容器名称和镜像名称不能为空"
        return 1
    fi

    # 检查容器是否已存在
    if sudo docker ps -a --format '{{.Names}}' | grep -q "^${container_name}$"; then
        echo "容器已存在，正在删除..."
        sudo docker rm -f "$container_name" >/dev/null 2>&1 || {
            echo "无法删除现有容器"
            return 1
        }
    fi

    echo "正在启动容器: $container_name"

    # 启动容器
    if sudo docker run -d \
        --name "$container_name" \
        --privileged \
        -p "${host_port1}:80" \
        -p "${host_port2}:8081" \
        --hostname "$container_name" \
        -v /sys/fs/cgroup:/sys/fs/cgroup:${cgroup_mode} \
        "$image" \
        /usr/sbin/init; then

        echo "容器启动成功"
        return 0
    else
        echo "容器启动失败"
        return 1
    fi
}

# 获取容器信息
# 参数: $1 - 容器名称
# 返回: JSON 格式的容器信息
docker_get_container_info() {
    local container_name="$1"

    if [ -z "$container_name" ]; then
        echo "{}"
        return 1
    fi

    # 检查容器是否存在
    if ! sudo docker ps -a --format '{{.Names}}' | grep -q "^${container_name}$"; then
        echo "{}"
        return 1
    fi

    # 获取容器 ID
    local container_id=$(sudo docker ps -a --filter "name=$container_name" --format '{{.ID}}')

    # 获取容器状态
    local status=$(sudo docker inspect --format '{{.State.Status}}' "$container_name" 2>/dev/null || echo "unknown")

    # 获取端口映射
    local ports_json=$(sudo docker port "$container_name" 2>/dev/null)

    # 解析端口映射
    local port_80_host=""
    local port_8081_host=""

    if echo "$ports_json" | grep -q "80/tcp"; then
        port_80_host=$(echo "$ports_json" | grep "80/tcp" | awk -F: '{print $2}')
    fi

    if echo "$ports_json" | grep -q "8081/tcp"; then
        port_8081_host=$(echo "$ports_json" | grep "8081/tcp" | awk -F: '{print $2}')
    fi

    # 获取镜像名称
    local image=$(sudo docker inspect --format '{{.Config.Image}}' "$container_name" 2>/dev/null || echo "")

    # 生成 JSON 输出
    cat <<EOF
{
  "container_name": "$container_name",
  "container_id": "$container_id",
  "status": "$status",
  "image": "$image",
  "ports": {
    "80": "$port_80_host",
    "8081": "$port_8081_host"
  }
}
EOF
}

# 检查容器是否运行
# 参数: $1 - 容器名称
# 返回值: 0=运行中, 1=未运行
docker_is_running() {
    local container_name="$1"

    if [ -z "$container_name" ]; then
        return 1
    fi

    if sudo docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        return 0
    else
        return 1
    fi
}

# 停止容器
# 参数: $1 - 容器名称
# 返回值: 0=成功, 1=失败
docker_stop_container() {
    local container_name="$1"

    if [ -z "$container_name" ]; then
        return 1
    fi

    if sudo docker stop "$container_name" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 删除容器
# 参数: $1 - 容器名称
# 返回值: 0=成功, 1=失败
docker_remove_container() {
    local container_name="$1"

    if [ -z "$container_name" ]; then
        return 1
    fi

    if sudo docker rm -f "$container_name" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}
