#!/bin/bash
echo "--- ClkLog 环境检查 ---"
# 检查 CPU
cpu_cores=$(nproc)
echo "CPU 核心数: $cpu_cores (推荐 >= 4)"

# 检查内存
total_mem=$(free -m | awk '/^Mem:/{print $2}')
echo "内存大小: ${total_mem}MB (推荐 >= 8192MB)"

# 检查架构
arch=$(uname -m)
if [ "$arch" != "x86_64" ]; then
    echo "警告：当前架构为 $arch，ClkLog 官方 Docker 部署主要支持 x86_64。"
fi

# 检查 Docker
docker -v && docker-compose version