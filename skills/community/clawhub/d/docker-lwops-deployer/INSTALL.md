# 安装指南

本文档详细介绍如何安装和配置 Docker LwOps 部署技能。

## 📋 目录

- [前置要求](#前置要求)
- [安装步骤](#安装步骤)
- [验证安装](#验证安装)
- [配置选项](#配置选项)
- [卸载技能](#卸载技能)
- [常见问题](#常见问题)

## 前置要求

### 系统要求

#### 支持的操作系统

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

#### 系统架构

- ✅ x86_64 (amd64)
- ✅ aarch64 (arm64)

#### 软件要求

- **Bash**: >= 4.0
- **sudo**: 权限管理（用于安装 Docker）
- **网络**: 能够访问华为云 SWR 镜像仓库

### 权限要求

此技能需要 sudo 权限来：
- 安装 Docker（如果未安装）
- 管理 Docker 容器
- 绑定特权端口（< 1024）

## 安装步骤

### 方法 1：通过 OpenClaw UI 安装（推荐）

1. **打开 OpenClaw 设置**

   在 OpenClaw 中进入设置 → 技能管理

2. **添加本地技能**

   点击"添加技能" → "从本地添加"

3. **选择技能目录**

   浏览到 `docker-lwops-deployer` 目录并选择

4. **启用技能**

   勾选"启用此技能"并保存

### 方法 2：手动安装

1. **找到 OpenClaw 技能目录**

```bash
# 通常位于以下位置之一
~/.openclaw/skills/
/usr/local/share/openclaw/skills/
```

2. **复制技能目录**

```bash
# 如果从 Git 仓库克隆
git clone <repository-url> docker-lwops-deployer
cp -r docker-lwops-deployer ~/.openclaw/skills/

# 或手动复制
cp -r /path/to/docker-lwops-deployer ~/.openclaw/skills/
```

3. **设置执行权限**

```bash
cd ~/.openclaw/skills/docker-lwops-deployer
chmod +x wrapper.sh execute.sh
chmod +x lib/*.sh
```

4. **配置技能（可选）**

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "docker-lwops-deployer": {
        "enabled": true,
        "priority": 100
      }
    }
  }
}
```

### 方法 3：从源码安装

1. **克隆仓库**

```bash
git clone https://github.com/lwops/docker-lwops-deployer.git
cd docker-lwops-deployer
```

2. **检查文件结构**

```bash
ls -la
# 应该看到：
# SKILL.md
# wrapper.sh
# execute.sh
# lib/
# README.md
# INSTALL.md
```

3. **设置执行权限**

```bash
chmod +x wrapper.sh execute.sh
chmod +x lib/*.sh
```

4. **复制到技能目录**

```bash
cp -r . ~/.openclaw/skills/docker-lwops-deployer/
```

## 验证安装

### 1. 检查文件权限

```bash
cd ~/.openclaw/skills/docker-lwops-deployer
ls -l

# 确保以下文件有执行权限：
# -rwxr-xr-x wrapper.sh
# -rwxr-xr-x execute.sh
# -rwxr-xr-x lib/system-utils.sh
# -rwxr-xr-x lib/network-utils.sh
# -rwxr-xr-x lib/docker-utils.sh
# -rwxr-xr-x lib/output-utils.sh
```

### 2. 测试技能

```bash
# 直接测试
./wrapper.sh "{}"
```

预期输出：
```json
{
  "success": false,
  "error": "...",
  "message": "...",
  ...
}
```

（这是正常的，因为没有实际的部署请求）

### 3. 在 OpenClaw 中测试

启动 OpenClaw 并输入：

```
你: 检查系统是否安装了 Docker
```

如果技能正确安装，它会：
1. 检查 Docker 安装状态
2. 如果未安装，自动安装
3. 输出 JSON 格式的结果

## 配置选项

### 环境变量

此技能不需要任何环境变量配置。

### 可选配置

#### 1. 修改默认端口

编辑 `execute.sh`，修改以下常量：

```bash
DEFAULT_HOST_PORT1=8000  # HTTP 端口
DEFAULT_HOST_PORT2=8081  # HTTPS 端口
```

#### 2. 修改容器名称

编辑 `execute.sh`，修改容器名称常量：

```bash
CONTAINER_NAME="lwops_rocky8_image_8.1"
```

#### 3. 修改镜像地址

编辑 `lib/system-utils.sh`，修改 `get_image_name` 函数：

```bash
get_image_name() {
    local arch="$1"
    case "$arch" in
        x86_64)
            echo "your-registry/lwops_rocky8_x86_image:latest"
            ;;
        aarch64)
            echo "your-registry/lwops_rocky8_arm_image:latest"
            ;;
    esac
}
```

## 卸载技能

### 1. 停止并删除容器

```bash
# 停止容器
sudo docker stop lwops_rocky8_image_8.1

# 删除容器
sudo docker rm -f lwops_rocky8_image_8.1

# 可选：删除镜像
sudo docker rmi swr.cn-south-1.myhuaweicloud.com/cloud-lwops/lwops_rocky8_x86_image:latest
```

### 2. 从 OpenClaw 卸载

**通过 UI**：
1. 打开 OpenClaw 设置
2. 进入技能管理
3. 找到 "docker-lwops-deployer"
4. 点击"禁用"然后"删除"

**手动卸载**：
```bash
rm -rf ~/.openclaw/skills/docker-lwops-deployer
```

### 3. 清理配置（可选）

编辑 `~/.openclaw/openclaw.json`，删除相关配置：

```json
{
  "skills": {
    "entries": {
      // 删除 "docker-lwops-deployer" 条目
    }
  }
}
```

## 常见问题

### Q1: 技能安装后无法调用

**A**: 检查以下几点：

1. 确认技能已启用
2. 检查文件权限是否正确
3. 查看 OpenClaw 日志是否有错误
4. 重启 OpenClaw

### Q2: 提示 "Bash version too old"

**A**: 升级 Bash 到 4.0 或更高版本：

```bash
# Ubuntu/Debian
sudo apt-get install bash

# CentOS/RHEL
sudo yum install bash

# Arch Linux
sudo pacman -S bash
```

### Q3: sudo 权限问题

**A**: 有几种解决方案：

1. **配置 sudo 无密码**（推荐用于自动化）：
```bash
echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$USER
sudo chmod 440 /etc/sudoers.d/$USER
```

2. **将用户添加到 docker 组**（避免使用 sudo）：
```bash
sudo usermod -aG docker $USER
newgrp docker
```

3. **手动输入密码**：在运行时输入 sudo 密码

### Q4: 无法访问华为云镜像仓库

**A**: 检查网络连接：

```bash
# 测试 DNS 解析
nslookup swr.cn-south-1.myhuaweicloud.com

# 测试网络连接
ping swr.cn-south-1.myhuaweicloud.com

# 测试 HTTPS 连接
curl -I https://swr.cn-south-1.myhuaweicloud.com
```

如果无法访问，可能需要：
- 检查防火墙设置
- 配置代理
- 使用 VPN

### Q5: 容器启动后无法访问

**A**: 检查以下几点：

1. **确认容器运行**：
```bash
sudo docker ps | grep lwops_rocky8_image_8.1
```

2. **检查端口映射**：
```bash
sudo docker port lwops_rocky8_image_8.1
```

3. **检查防火墙**：
```bash
# Ubuntu/Debian
sudo ufw status

# CentOS/RHEL
sudo firewall-cmd --list-ports
```

4. **检查容器日志**：
```bash
sudo docker logs lwops_rocky8_image_8.1
```

### Q6: 提示"另一个部署任务正在进行中"

**A**: 这是正常的并发控制保护机制。

**解决方案**:

1. **等待当前部署完成**
   - 技能会显示预计剩余时间
   - 通常部署需要 2-5 分钟

2. **查看部署进度**：
```bash
sudo docker logs lwops_rocky8_image_8.1
```

3. **如果确认没有其他部署**，手动删除锁：
```bash
rm -f /tmp/docker-lwops-deployer/deploy.lock
```

4. **检查是否有僵尸进程**：
```bash
# 查看锁文件内容
cat /tmp/docker-lwops-deployer/deploy.lock

# 检查进程是否存在
ps -fp <PID>
```

**注意**: 多个用户同时调用技能时，只有一个会执行部署，其他用户会收到提示。这是正常的保护机制，防止部署冲突。

### Q7: cgroup v2 兼容性问题

**A**: 技能会自动检测并处理 cgroup 版本：

- **cgroup v1**: 使用 `:ro` 挂载模式
- **cgroup v2**: 使用 `:rw` 挂载模式并提示用户

如果仍有问题，可以：
1. 检查内核启动参数
2. 查看 Docker 日志
3. 尝试重启 Docker 服务

### Q8: 技能输出格式不正确

**A**: 确保以下几点：

1. 检查是否使用了最新版本的技能
2. 查看 STDERR 输出（错误信息输出到 STDERR）
3. 验证 JSON 格式：
```bash
./wrapper.sh "{}" | jq .
```

### Q9: 磁盘空间不足

**A**: 清理 Docker 资源：

```bash
# 清理未使用的镜像
sudo docker image prune -a

# 清理未使用的容器
sudo docker container prune

# 清理未使用的卷
sudo docker volume prune

# 清理所有未使用的资源
sudo docker system prune -a
```

## 技术支持

如果遇到其他问题：

1. 查看 [README.md](README.md) 中的故障排除部分
2. 查看 [容器日志](#q5-容器启动后无法访问)
3. 提交 Issue：https://github.com/lwops/docker-lwops-deployer/issues
4. 联系技术支持：support@lwops.cn

## 更新日志

### v1.0.0 (2026-03-24)

- ✨ 初始版本发布
- 🎯 支持 x86_64 和 aarch64 架构
- 🔧 自动安装 Docker
- 🔌 智能端口分配
- ⚙️ cgroup 兼容性处理
