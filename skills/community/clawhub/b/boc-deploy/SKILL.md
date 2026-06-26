---
name: boc-deploy
description: 博云BOC容器平台 部署工具。根据部署规划信息自动生成配置文件并执行部署。使用场景：用户需要部署 BOC容器平台时使用，包括生成 config.yaml、执行 bocctl run、监控部署状态。
version: 1.0.1
icon: 🚀
---

# BOC容器平台 部署

自动化完成 BOC容器平台  的部署阶段（配置文件生成 → 部署执行 → 状态验证）。

## 输入参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| deploy_server_ip | 部署机IP | 是 | 10.50.6.181 |
| ssh_port | SSH端口 | 否 | 22 |
| ssh_user | SSH用户名 | 是 | root |
| ssh_password | SSH密码 | 是 | Password |
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

### 1. 确认 bocctl init 已完成

**验证方法**：在部署机上执行以下命令检查容器状态：
```bash
nerdctl -n k8s.io ps -a
```

**预期结果**：应看到两个运行中的容器
- `yum_registry` - 运行中
- `bocloud_deploy_registry_k8s` - 运行中

如果容器未运行，需要先用skill boc-init 进行初始化：
```bash
cd /opt/BOC_k8s_noarch
./bocctl init 
```

### 2. 生成配置文件

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

### 3. 上传配置文件到部署机

将生成的 config.yaml 上传到部署机的 `/root/config.yaml`

### 4. 执行部署

```bash
cd /opt/BOC_k8s_noarch
nohup ./bocctl run -a install -c /root/config.yaml > log/bocctl.log 2>&1 &
```

部署过程约 40-60 分钟。

### 5. 监控部署

每5分钟检查一次进度：
```bash
# 检查进程数
ps aux | grep -E "bocctl|ansible" | grep -v grep | wc -l

# 查看日志
tail -100 /opt/BOC_k8s_noarch/log/bocctl.log
```

### 6. 验证结果

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

### 7. 访问 BOC Portal

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

```
请使用 boc-deploy 部署 BOC容器平台：
- 部署机IP：10.50.6.181
- SSH用户：root
- SSH密码：Password
- CI节点IP：10.50.6.182
- BOC节点IP：10.50.6.183,10.50.6.184,10.50.6.185
- VIP：10.50.6.186
- CNI类型：ipip
```

## 输出

- 配置文件生成状态
- 部署执行状态
- 部署日志末尾输出
- 验证结果：
  - Node 状态
  - Pod 状态（所有 Pod 应为 Running）

## 注意事项

1. **部署机需先完成初始化**（使用 boc-init 技能），确认 `nerdctl` 容器已运行
2. 确保所有节点间网络互通
3. 部署过程耗时较长，建议后台运行
4. 部署完成后验证所有 Pod 状态
5. 如果无法从部署机 SSH 到 master 节点，可以从本机直接连接验证

## 常见问题

### Q: 部署完成但无法访问 K8s 节点
A: 可能 SSH 互信未配置完成，直接从本机使用密码连接 master 节点验证

### Q: Pod 状态不是 Running
A: 检查具体 Pod 状态 `kubectl describe pod <pod-name> -n <namespace>`

### Q: BOC Portal 无法访问
A: 检查 kube-proxy 和 bocloud 组件是否正常运行