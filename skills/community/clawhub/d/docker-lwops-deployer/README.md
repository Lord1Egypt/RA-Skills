# Docker LwOps 部署技能

自动化部署乐维监控 8.1 Docker 容器的 OpenClaw 技能。

## 📋 项目概述

这是一个符合 OpenClaw 规范的本地技能，用于一键部署乐维监控 8.1 环境。该技能能够：

- 🔧 自动检测并安装 Docker（如果未安装）
- 🏗️ 根据系统架构（x86_64/aarch64）选择对应的镜像
- 🔌 智能检测端口冲突并自动分配可用端口
- ⚙️ 自动处理 cgroup v1/v2 兼容性问题
- 🔒 智能锁定机制，防止多用户同时部署冲突
- 🚀 快速启动容器并提供访问地址

## 🎯 适用场景

- 本地开发环境搭建
- 测试环境快速部署
- 容器化服务管理
- CI/CD 流水线集成

## 📦 系统要求

### 支持的操作系统

**基于 Debian/Ubuntu：**
- ✅ Ubuntu 18.04 LTS 及更高版本
- ✅ Debian 10 Buster 及更高版本
- ✅ Deepin (深度操作系统)
- ✅ Linux Mint
- ✅ elementaryOS

**基于 RHEL/CentOS：**
- ✅ CentOS 7/8
- ✅ RHEL 7/8
- ✅ Rocky Linux 8+
- ✅ AlmaLinux 8+
- ✅ Anolis OS (龙蜥)
- ✅ openEuler (欧拉)
- ✅ Kylin (麒麟)
- ✅ Oracle Linux
- ✅ Scientific Linux
- ✅ VzLinux
- ✅ TencentOS

**其他：**
- ✅ Fedora 30+
- ✅ Arch Linux 及衍生发行版（Manjaro、EndeavourOS 等）

### 系统架构

- ✅ x86_64 (amd64)
- ✅ aarch64 (arm64)

### 其他要求

- Bash >= 4.0
- sudo 权限（用于安装 Docker 和管理容器）
- 网络连接（访问华为云 SWR 镜像仓库）

## 🚀 快速开始

### 安装技能

1. **克隆或下载技能目录**

```bash
cd ~/.openclaw/skills/
git clone <repository-url> docker-lwops-deployer
```

或手动复制技能目录到 OpenClaw 技能目录。

2. **设置执行权限**

```bash
cd ~/.openclaw/skills/docker-lwops-deployer
chmod +x wrapper.sh execute.sh
chmod +x lib/*.sh
```

3. **验证安装**

```bash
./wrapper.sh "{}"
```

### 使用技能

在 OpenClaw 中，你可以直接使用自然语言调用此技能：

```
你: 部署一个乐维监控 8.1 容器
```

或

```
你: 重新部署 lwops_rocky8_image_8.1 容器
```

## 📖 使用示例

### 示例 1：首次部署

```
你: 部署一个完整的乐维监控 8.1 环境
```

**技能会自动：**
1. 检查 Docker 是否安装，未安装则自动安装
2. 检测系统架构
3. 拉取对应的镜像
4. 检查端口并分配可用端口
5. 启动容器
6. 输出访问地址

### 示例 2：重新部署

```
你: 重新部署乐维监控容器
```

**技能会：**
1. 删除现有容器
2. 重新创建并启动容器
3. 输出新的访问信息

### 示例 3：查询容器信息

```
你: 查询容器的访问地址和端口映射
```

**技能会输出：**
- 容器 ID
- 运行状态
- 端口映射
- 访问 URL

### 示例 4：检查环境

```
你: 检查系统是否安装了 Docker
```

**技能会：**
- 检查 Docker 安装状态
- 未安装则自动安装
- 确保 Docker 服务运行

### 示例 5：智能端口分配

```
你: 部署乐维监控容器，自动分配可用端口
```

**技能会：**
- 检查默认端口（8000、8081）是否被占用
- 如被占用，自动查找并使用可用端口
- 输出实际使用的端口

## 🔧 技术架构

### 技术栈

- **语言**: Bash (Shell Script)
- **依赖**: 无外部依赖（纯 Bash 实现）
- **容器**: Docker

### 目录结构

```
docker-lwops-deployer/
├── SKILL.md                  # 技能定义文件
├── wrapper.sh                # Shell 包装器
├── execute.sh                # 核心执行脚本
├── lib/                      # 函数库
│   ├── system-utils.sh       # 系统检测函数
│   ├── network-utils.sh      # 网络和端口检测函数
│   ├── docker-utils.sh       # Docker 操作函数
│   └── output-utils.sh       # 输出格式化函数
├── README.md                 # 项目说明（本文件）
└── INSTALL.md                # 安装指南
```

### 执行流程

```
用户输入
    ↓
wrapper.sh（包装器）
    ↓
execute.sh（核心逻辑）
    ↓
├─ 检查系统兼容性
├─ 确保 Docker 安装并运行
├─ 检测系统架构
├─ 拉取镜像
├─ 智能分配端口
├─ 检测 cgroup 版本
├─ 启动容器
└─ 输出结果
```

## 📊 输出格式

### 成功输出

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
  "message": "容器部署成功",
  "timestamp": "2026-03-24T10:30:00Z"
}
```

### 失败输出

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

## 🐳 容器信息

### 镜像地址

- **x86_64 架构**: `swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_x86_image:latest`
- **aarch64 架构**: `swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_arm_image:latest`

### 端口映射

- **容器端口 80** → **宿主机端口 8000**（默认，可自动调整）
- **容器端口 8081** → **宿主机端口 8081**（默认，可自动调整）

### 容器配置

- **容器名称**: `lwops_rocky8_image_8.1`
- **启动参数**: `--privileged`（特权模式）
- **cgroup 挂载**: `/sys/fs/cgroup:/sys/fs/cgroup:ro`（v1）或 `:rw`（v2）
- **启动命令**: `/usr/sbin/init`

## 🔍 故障排除

### 问题 1：Docker 安装失败

**症状**: 提示无法安装 Docker

**解决方案**:
1. 检查是否有 sudo 权限
2. 检查系统是否支持（参考系统要求）
3. 手动安装 Docker：访问 https://docs.docker.com/get-docker/

### 问题 2：端口被占用

**症状**: 无法启动容器，端口冲突

**解决方案**:
1. 技能会自动分配可用端口
2. 查看输出中的 `ports` 字段获取实际端口
3. 停止占用端口的程序：`sudo lsof -i :8000`

### 问题 3：容器启动失败

**症状**: 容器创建后立即退出

**解决方案**:
1. 检查 Docker 日志：`sudo docker logs lwops_rocky8_image_8.1`
2. 检查 cgroup 版本兼容性
3. 确保使用 `--privileged` 参数

### 问题 4：无法访问容器服务

**症状**: 容器运行但无法访问 Web 界面

**解决方案**:
1. 检查防火墙设置
2. 确认端口映射：`docker port lwops_rocky8_image_8.1`
3. 检查容器状态：`docker ps`

### 问题 5：权限不足

**症状**: 提示需要 sudo 权限

**解决方案**:
1. 使用 sudo 运行命令
2. 将用户添加到 sudo 组：`sudo usermod -aG sudo $USER`
3. 配置 sudo 无密码：`echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$USER`

## 📚 相关文档

- [安装指南](INSTALL.md)
- [OpenClaw 技能开发指南](https://github.com/openclaw/skills)
- [乐维监控官方文档](https://www.lwops.cn)
- [Docker 官方文档](https://docs.docker.com/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- **乐维监控官网**: https://www.lwops.cn
- **Docker 官方文档**: https://docs.docker.com/
- **问题反馈**: https://github.com/lwops/docker-lwops-deployer/issues
- **OpenClaw 项目**: https://github.com/openclaw/openclaw
