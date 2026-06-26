---
name: docker-lwops-deployer
description: |
  本地 Docker 容器自动化部署技能，支持乐维监控 8.1 环境的一键部署。
  适用于：本地开发环境搭建、测试环境快速部署、容器化服务管理。
  优势：自动检测系统架构、智能端口管理、Docker 自动安装、cgroup 兼容性处理。
user-invocable: true
metadata:
  openclaw:
    emoji: "🐳"
    requires:
      bins:
        - bash
      env: []
      config: []
    homepage: https://github.com/lwops/docker-lwops-deployer
    examples:
      - description: 部署默认容器
        input: 部署一个乐维监控 8.1 容器
      - description: 检查 Docker 环境
        input: 检查系统是否安装了 Docker
      - description: 重新部署容器
        input: 重新部署 lwops_rocky8_image_8.1 容器
      - description: 查看容器状态
        input: 查看乐维监控容器的运行状态
      - description: ARM 架构部署
        input: 在 ARM 服务器上部署乐维监控容器
      - description: 完整部署流程
        input: 帮我部署一个完整的乐维监控 8.1 环境
      - description: 快速部署
        input: 启动乐维监控 Docker 容器
      - description: 智能端口分配
        input: 部署乐维监控容器，自动分配可用端口
      - description: 容器信息查询
        input: 查询容器的访问地址和端口映射
      - description: 自动安装 Docker
        input: 安装 Docker 并部署乐维监控容器
---

# Docker LwOps 部署技能

自动化部署乐维监控 8.1 Docker 容器的本地技能，支持一键安装和智能配置。

## 功能特性

- 🔧 **Docker 自动安装**：自动检测系统类型并安装 Docker
- 🏗️ **架构智能检测**：支持 x86_64 和 aarch64 架构
- 🔌 **智能端口分配**：自动检测端口冲突并分配可用端口
- ⚙️ **cgroup 兼容**：自动处理 cgroup v1/v2 兼容性问题
- 🚀 **一键部署**：快速启动乐维监控 8.1 容器环境
- 📊 **详细反馈**：输出容器访问地址和端口映射信息

## 使用方式

当用户请求部署乐维监控容器、检查 Docker 环境、或管理相关容器时，此技能会被自动调用。

## 使用场景

### 何时使用此技能

当你的查询包含以下特征时，应该使用此技能：

1. **乐维监控相关部署**：明确提到"乐维监控"、"乐维8.1"、"lwops"等关键词
2. **容器部署操作**：请求部署、启动、创建 Docker 容器
3. **环境管理**：检查 Docker 安装状态、容器运行状态
4. **容器操作**：重新部署、查看状态、查询访问地址

### 常见使用场景

#### 场景 1：首次部署
- 示例：`部署一个乐维监控 8.1 容器`
- 说明：自动安装 Docker（如果需要），拉取镜像并启动容器

#### 场景 2：重新部署
- 示例：`重新部署 lwops_rocky8_image_8.1 容器`
- 说明：删除现有容器并重新创建

#### 场景 3：智能端口分配
- 示例：`部署乐维监控容器，自动分配可用端口`
- 说明：检测端口冲突并自动使用可用端口

#### 场景 4：查询容器信息
- 示例：`查询容器的访问地址和端口映射`
- 说明：获取容器状态和访问 URL

### 与其他工具的区别

| 特性 | 本技能 | 手动部署 |
|------|--------|----------|
| Docker 安装 | 自动检测并安装 | 需要手动操作 |
| 架构适配 | 自动选择镜像 | 需要手动指定 |
| 端口管理 | 自动检测冲突 | 需要手动检查 |
| cgroup 处理 | 自动兼容 | 需要手动配置 |

### 最佳实践

1. **权限要求**：确保用户有 sudo 权限（安装 Docker 需要）
2. **网络环境**：确保能访问华为云镜像仓库（swr.cn-south-1.myhuaweicloud.com）
3. **端口规划**：默认使用 8000 和 8081 端口，如有冲突会自动调整
4. **容器管理**：容器名称固定为 `lwops_rocky8_image_8.1`，重复部署会自动替换

## 配置

### 无需配置

此技能不需要任何环境变量或配置参数，开箱即用。

### 系统要求

- **操作系统**：Ubuntu、Debian、CentOS、RHEL、Fedora、Arch Linux
- **架构支持**：x86_64（amd64）、aarch64（arm64）
- **权限**：sudo 权限（用于安装 Docker 和管理容器）
- **网络**：能访问华为云 SWR 镜像仓库

## 技术实现

### 输入格式

此技能接收自然语言输入，无需特定的 JSON 格式。例如：

- "部署乐维监控 8.1 容器"
- "重新部署容器"
- "查看容器状态"

### 输出格式

成功时：
```json
{
  "success": true,
  "data": {
    "container_name": "lwops_rocky8_image_8.1",
    "container_id": "a1b2c3d4e5f6",
    "status": "running",
    "architecture": "x86_64",
    "image": "swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_x86_image:latest",
    "host_ip": "192.168.1.100",
    "ports": {
      "http": {
        "container_port": 80,
        "host_port": 8000,
        "url": "http://192.168.1.100:8000"
      },
      "https": {
        "container_port": 8081,
        "host_port": 8081,
        "url": "http://192.168.1.100:8081"
      }
    },
    "cgroup_version": "v1",
    "cgroup_mount_mode": "ro",
    "timestamp": "2026-03-24T10:30:00Z"
  },
  "message": "容器部署成功"
}
```

失败时：
```json
{
  "success": false,
  "error": "DockerNotInstalled",
  "message": "Docker 未安装，正在尝试自动安装...",
  "suggestions": [
    "Ubuntu/Debian: sudo apt-get install docker.io",
    "CentOS/RHEL: sudo yum install docker",
    "访问 https://docs.docker.com/get-docker/ 获取详细安装指南"
  ],
  "timestamp": "2026-03-24T10:30:00Z"
}
```

## 容器信息

### 镜像地址

- **x86_64 架构**：`swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_x86_image:latest`
- **aarch64 架构**：`swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_arm_image:latest`

### 端口映射

- **容器端口 80** → **宿主机端口 8000**（默认，可自动调整）
- **容器端口 8081** → **宿主机端口 8081**（默认，可自动调整）

### 容器配置

- **容器名称**：`lwops_rocky8_image_8.1`
- **启动参数**：`--privileged`（特权模式）
- **cgroup 挂载**：`/sys/fs/cgroup:/sys/fs/cgroup:ro`（v1）或 `:rw`（v2）
- **启动命令**：`/usr/sbin/init`

## 故障排除

### 问题 1：Docker 安装失败

**症状**：提示无法安装 Docker

**解决方案**：
1. 检查是否有 sudo 权限
2. 检查系统是否支持（参考系统要求）
3. 手动安装 Docker：访问 https://docs.docker.com/get-docker/

### 问题 2：端口被占用

**症状**：无法启动容器，端口冲突

**解决方案**：
1. 技能会自动分配可用端口
2. 查看输出中的 `ports` 字段获取实际端口
3. 停止占用端口的程序：`sudo lsof -i :8000`

### 问题 3：容器启动失败

**症状**：容器创建后立即退出

**解决方案**：
1. 检查 Docker 日志：`docker logs lwops_rocky8_image_8.1`
2. 检查 cgroup 版本兼容性
3. 确保使用 `--privileged` 参数

### 问题 4：无法访问容器服务

**症状**：容器运行但无法访问 Web 界面

**解决方案**：
1. 检查防火墙设置
2. 确认端口映射：`docker port lwops_rocky8_image_8.1`
3. 检查容器状态：`docker ps`

## 相关链接

- **乐维监控官网**：https://www.lwops.cn
- **Docker 官方文档**：https://docs.docker.com/
- **问题反馈**：https://github.com/lwops/docker-lwops-deployer/issues
