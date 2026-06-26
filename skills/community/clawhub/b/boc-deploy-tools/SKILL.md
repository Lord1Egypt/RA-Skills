---
name: boc-deploy-tools
description: 博云BOC容器平台 部署工具。整合了部署机初始化和平台部署功能，自动完成从环境初始化到部署验证的全流程。使用场景：用户需要初始化部署机并部署 BOC容器平台时使用。
version: 1.0.0
icon: 🚀
---

# BOC部署工具

整合了 boc-init（部署机初始化）和 boc-deploy（平台部署）功能，提供从环境准备到部署验证的完整工作流。

## 输入参数

### 初始化参数（第一阶段）

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| deploy_pkg_dir | 部署包和校验文件所在目录 | 是 | /opt |
| deploy_pkg_file | 部署包文件名 | 是 | BOC.tar.gz |
| ssh_host | 部署机IP | 是 | 10.50.6.181 |
| ssh_port | SSH端口 | 否 | 22 |
| ssh_user | SSH用户名 | 是 | root |
| ssh_password | SSH密码 | 是 | Password |

### 部署参数（第二阶段）

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| ci_ip | CI节点IP | 是 | 10.50.6.182 |
| node_ips | BOC节点IP列表(逗号分隔) | 是 | 10.50.6.183,10.50.6.184,10.50.6.185 |
| master_vip | K8s Master VIP | 是 | 10.50.6.186 |
| cni_type | CNI类型 | 否 | ipip (默认) 或 bgp |
| k8s_version | Kubernetes版本 | 否 | 1.33.1 (默认) |

## 节点角色说明

| 角色 | 说明 |
|------|------|
| deploy_server | 部署机 |
| pipeline | CI节点 |
| chartmuseum | Chart仓库 |
| docker_registry | Docker镜像仓库 |
| nfs_server | NFS存储 |
| master | K8s master节点 |
| etcd | etcd节点 |
| db | 数据库节点 |
| node | K8s worker节点 |

## 工作流程

### 第一阶段：部署机初始化

#### 1.1 环境检查

连接部署机并检查：
- 主机名
- 操作系统版本
- 内核版本
- DNS配置
- 磁盘空间（/var 目录至少50GB）
- 部署包是否存在

#### 1.2 部署包校验

执行 SHA256 校验：
```bash
nohup cd <deploy_pkg_dir> && sha256sum <deploy_pkg_file>.sha256 > /tmp/sha256sum-<deploy_pkg_file>.txt
```
定期检查校验结果
```bash
cat /tmp/sha256sum-<deploy_pkg_file>.txt
```
判断标准: 结果中有 "<deploy_pkg_file>: 成功"

#### 1.3 解压部署包

**重要**：解压前需先清理旧目录，避免残留文件导致问题：
```bash
# 解压前先清理旧目录
cd <deploy_pkg_dir>
test -d BOC_k8s_noarch && rm -rf BOC_k8s_noarch

# 后台执行解压（30GB文件预计15-20分钟）
nohup tar -xzf <deploy_pkg_file> > /tmp/unpack.log 2>&1 &

# 定期检查解压，通过进程判断
## 1 检查是否有以下进程，有就代表还在解压
ps aux |grep 'tar -xzf <deploy_pkg_file>'

## 2 没有就再检查/opt/BOC_k8s_noarch  占用空间正常应该在 31GB
du -sh /opt/BOC_k8s_noarch
```

#### 1.4 验证解压结果

解压后的正确目录结构：
```
/opt/BOC_k8s_noarch/
├── bocctl           # 主程序
├── bocctl_lib       # 库文件
├── images           # 镜像文件
├── packages         # 安装包
├── playbooks        # Ansible playbook
```

#### 1.5 执行 bocctl init

后台执行初始化（预计15-20分钟）：
```bash
cd <deploy_dir>
nohup ./bocctl init > /tmp/bocctl_init.log 2>&1 &
# 定期检查bocctl 进程是否存在，如存在代表init 还在进行
# 也一块检查执行日志
ps aux |grep bocctl
tail -n 20 /opt/BOC_k8s_noarch/log/bocctl.log
```

#### 1.6 验证初始化完成

**判断标准**：使用 `nerdctl ps` 检查以下两个容器是否正常运行：
```bash
nerdctl -n k8s.io ps | grep -E "(yum_registry|bocloud_deploy_registry)"
```

预期输出应包含：
- `yum_registry` 容器 - 运行中
- `bocloud_deploy_registry_k8s` 容器 - 运行中

---

### 第二阶段：平台部署

#### 2.1 确认 bocctl init 已完成

验证方法如上，确保容器正常运行后再继续。

#### 2.2 生成配置文件

根据输入参数生成 `config.yaml`，包含：
- 节点配置（IP、端口、用户、密码、角色）
- VIP配置
- NFS配置
- 容器运行时配置
- Kubernetes版本
- 数据库配置
- 网络配置（calico ipip/bgp）
- BOC Portal组件配置

**配置文件示例**：

高可用部署示例文件： /opt/BOC_k8s_noarch/playbooks/examples/config/install_portal_HA.yaml
ALLINONE 部署示例文件： /opt/BOC_k8s_noarch/playbooks/examples/config/install_portal_allinone.yaml

#### 2.3 上传配置文件到部署机

将生成的 config.yaml 上传到部署机的 `/root/config.yaml`

#### 2.4 执行部署

```bash
cd /opt/BOC_k8s_noarch
nohup ./bocctl run -a install -c /root/config.yaml > log/bocctl.log 2>&1 &
```

部署过程约 40-60 分钟。

#### 2.5 监控部署

每5分钟检查一次进度：
```bash
# 检查进程数
ps aux | grep -E "bocctl|ansible" | grep -v grep | wc -l

# 查看日志
tail -100 /opt/BOC_k8s_noarch/log/bocctl.log
```

#### 2.6 验证结果

直接连接 master 节点验证
```bash
# 从本机直接连接 master 节点
ssh root@<master节点IP>

# 检查节点状态
kubectl get nodes

# 检查 Pod 状态
kubectl get pods -A
```

**预期结果**：
- 所有节点状态为 `Ready`
- 所有 Pod 状态为 `Running`

#### 2.7 访问 BOC Portal

使用浏览器访问：
```
http://<master_vip>:30001
```

**常用服务端口**：
| 服务 | 地址 |
|------|------|
| BOC Portal | http://<master_vip>:30001 |
| K8s API Server | https://<master_vip>:6443 |
| Grafana | http://<master_vip>:30902 |
| Prometheus | http://<master_vip>:30909 |

## 使用示例

### 完整部署（初始化 + 部署）

```
请使用 boc-deploy-tool 部署 BOC容器平台：

初始化参数：
- 部署包目录：/opt
- 部署包文件：BOC.tar.gz
- 部署机IP：10.50.6.181
- SSH端口：22
- SSH用户：root
- SSH密码：password

部署参数：
- CI节点IP：10.50.6.182
- BOC节点IP：10.50.6.183,10.50.6.184,10.50.6.185
- VIP：10.50.6.186
- CNI类型：ipip
- K8s版本：1.33.1
```

### 仅部署（已初始化）

如果部署机已完成初始化，只需提供部署参数即可。

## 输出

### 初始化阶段输出
- 部署机初始化完成状态
- 初始化后关键组件状态：
  - ansible 版本
  - nerdctl 容器运行状态（yum_registry 和 bocloud_deploy_registry_k8s）
  - containerd 服务状态

### 部署阶段输出
- 配置文件生成状态
- 部署执行状态
- 部署日志末尾输出
- 验证结果：
  - Node 状态
  - Pod 状态（所有 Pod 应为 Running）

## 注意事项

1. **本地执行前置条件**：
   - 需要安装 Python 才能使用 ssh-exec skill
   - 需要安装 node 才能使用 rssh2 skill
   - Windows 系统需要安装 Git for Windows

2. **SSH 连接问题解决**：
   - 如果安装了 Python，优先使用 ssh-exec skill
   - 如安装了 node，优先使用 rssh2 skill
   - 先检查操作系统中是否有 sshpass，如果没有：
     - Windows：从 https://github.com/xhcoding/sshpass-win32/releases/download/v1.0.7/sshpass.exe 下载
     - Linux：使用 `pip install sshpass -g` 安装

3. 确保所有节点间网络互通
4. 部署过程耗时较长，建议后台运行
5. 部署完成后验证所有 Pod 状态
6. 如果无法从部署机 SSH 到 master 节点，可以从本机直接连接验证

## 常见问题

### Q: 解压后目录结构异常
A: 重新执行解压，确保先删除旧目录

### Q: bocctl init 卡住不动
A: 检查是否有 yum 进程卡住，如有则杀掉后重试

### Q: 部署完成但无法访问 K8s 节点
A: 可能 SSH 互信未配置完成，直接从本机使用密码连接 master 节点验证

### Q: Pod 状态不是 Running
A: 检查具体 Pod 状态 `kubectl describe pod <pod-name> -n <namespace>`

### Q: BOC Portal 无法访问
A: 检查 kube-proxy 和 bocloud 组件是否正常运行