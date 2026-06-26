#!/usr/bin/env python3
"""
CI/CD Setup Guide Generator
Generates comprehensive setup documentation based on configuration
"""

from pathlib import Path
from datetime import datetime

def generate_jenkins_guide(config):
    """Generate Jenkins setup guide"""
    project_type = config.get('project_type', 'java')
    deploy_target = config.get('deploy_target', 'ssh')
    steps = config.get('steps', [])
    
    project_name = config.get('project_name', 'my-app')
    
    guide = f"""# Jenkins CI/CD 配置指南

## 📋 配置摘要

| 配置项 | 值 |
|--------|-----|
| **平台** | Jenkins |
| **项目类型** | {project_type.upper()} |
| **部署目标** | {deploy_target.upper()} |
| **触发方式** | {config.get('trigger', 'manual').upper()} |
| **流水线步骤** | {', '.join(steps) if steps else 'Build, Deploy, Notify'} |

## 📦 生成文件清单

```
cicd-output/
├── Jenkinsfile              # Jenkins 流水线配置
├── setup-guide.md           # 本文件（配置说明）
├── {project_name}.service   # systemd 服务文件
└── README.md                # 快速参考
```

---

## 🔧 前置准备

### 1. Jenkins 版本要求
- **Jenkins**: 2.300+ 推荐
- **Java**: 8 或 11（Jenkins 运行环境）

### 2. 必须安装的插件

进入 **Manage Jenkins → Manage Plugins → Available**，安装以下插件：

| 插件名称 | 用途 | 必需 |
|---------|------|------|
| **Pipeline** | 流水线支持 | ✅ |
| **SSH Agent** | SSH 密钥认证 | {'✅' if deploy_target == 'ssh' else '❌'} |
| **Docker Pipeline** | Docker 构建 | {'✅' if 'dockerize' in steps else '❌'} |
| **Kubernetes CLI** | K8s 部署 | {'✅' if deploy_target == 'k8s' else '❌'} |
| **HTTP Request** | 发送通知 | {'✅' if 'notify' in steps else '❌'} |

### 3. 全局工具配置

进入 **Manage Jenkins → Global Tool Configuration**：

**Maven**（如果是 Java 项目）：
- 名称: `maven-3.8`
- 选择自动安装或指定已安装的 Maven 路径

**JDK**（可选）：
- 名称: `jdk-1.8`
- JAVA_HOME: `/usr/lib/jvm/java-8-openjdk`

---

## 🔐 凭证配置

进入 **Manage Jenkins → Manage Credentials → System → Global credentials**，添加以下凭证：

| 凭证 ID | 类型 | 示例值 | 说明 |
|---------|------|--------|------|
| `deploy-host` | Secret text | `192.168.1.100` | 目标服务器 IP |
| `deploy-user` | Secret text | `deploy` | SSH 登录用户名 |
| `deploy-ssh-key` | SSH Username with private key | - | SSH 私钥 |
| `docker-registry` | Username with password | - | Docker 仓库登录 | {'(Docker部署必需)' if deploy_target in ['docker', 'k8s'] else '(如使用Docker)'} |
| `kubeconfig` | Secret file | - | K8s 配置文件 | {'(K8s部署必需)' if deploy_target == 'k8s' else '(如部署到K8s)'} |
| `webhook-url` | Secret text | `https://open.feishu.cn/...` | 飞书/钉钉机器人 | {'(通知必需)' if 'notify' in steps else '(可选)'} |

**添加步骤：**
1. 点击 **Add Credentials**
2. 选择 **Kind**（类型）
3. 输入 **ID**（必须严格匹配上表）
4. 填写其他信息
5. 点击 **Create**

---

## 🚀 创建 Pipeline Job

### 步骤 1：新建 Job
1. 点击 Jenkins 首页 **New Item**
2. 输入名称（如 `{project_name}-deploy`）
3. 选择 **Pipeline** 类型
4. 点击 **OK**

### 步骤 2：配置 Pipeline

在 Job 配置页面，找到 **Pipeline** 部分：

| 配置项 | 值 |
|--------|-----|
| **Definition** | Pipeline script from SCM |
| **SCM** | Git |
| **Repository URL** | 你的 Git 仓库地址 |
| **Credentials** | 如果仓库私有，选择 Git 凭证 |
| **Branch Specifier** | `*/main` 或 `*/master` |
| **Script Path** | `Jenkinsfile` |

### 步骤 3：保存
点击 **Save** 保存配置。

---

## 🖥️ 目标服务器配置

"""

    if deploy_target == 'ssh':
        guide += f"""### SSH 服务器准备

在目标服务器（`deploy-host`）上执行以下操作：

#### 1. 创建部署用户
```bash
# 创建 deploy 用户
sudo useradd -m -s /bin/bash deploy

# 设置密码（可选，如果使用密钥认证）
sudo passwd deploy

# 添加到 sudo 组
sudo usermod -aG sudo deploy
```

#### 2. 创建部署目录
```bash
# 创建应用目录
sudo mkdir -p /opt/{project_name} /opt/backup
sudo chown -R deploy:deploy /opt/{project_name} /opt/backup
```

#### 3. 配置 SSH 免密登录
在 Jenkins 服务器上执行：
```bash
# 切换到 jenkins 用户
sudo su - jenkins

# 生成 SSH 密钥（如果没有）
ssh-keygen -t rsa -b 4096 -C "jenkins-deploy"

# 复制公钥到目标服务器
ssh-copy-id deploy@YOUR_SERVER_IP

# 测试连接
ssh deploy@YOUR_SERVER_IP "echo '连接成功'"
```

#### 4. 配置 sudo 免密码
在目标服务器上：
```bash
sudo visudo
```

添加以下行：
```
deploy ALL=(ALL) NOPASSWD: /bin/systemctl start {project_name}, /bin/systemctl stop {project_name}, /bin/systemctl restart {project_name}
```

#### 5. 部署 systemd 服务
将生成的 `{project_name}.service` 文件复制到服务器：

```bash
# 在目标服务器上
sudo cp {project_name}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable {project_name}
```

#### 6. 安装 Java（如果未安装）
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y openjdk-8-jdk

# CentOS/RHEL
sudo yum install -y java-1.8.0-openjdk
```

验证：
```bash
java -version
```
"""

    elif deploy_target == 'k8s':
        guide += """### Kubernetes 集群准备

#### 1. 配置 Kubectl 访问
确保 Jenkins 服务器可以访问 K8s 集群：

```bash
# 测试连接
kubectl cluster-info

# 查看节点
kubectl get nodes
```

#### 2. 创建 Namespace（可选）
```bash
kubectl create namespace production
```

#### 3. 配置镜像仓库密钥（如果使用私有仓库）
```bash
kubectl create secret docker-registry regcred \\
  --docker-server=your-registry.com \\
  --docker-username=username \\
  --docker-password=password \\
  --namespace=production
```

#### 4. 上传 Kubeconfig 到 Jenkins
```bash
# 复制 kubeconfig 内容
cat ~/.kube/config | base64

# 在 Jenkins 中创建 credentials：
# Kind: Secret file
# ID: kubeconfig
# File: 粘贴 base64 内容或上传文件
```
"""

    elif deploy_target == 'docker':
        guide += """### Docker 服务器准备

#### 1. 安装 Docker
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io

# CentOS/RHEL
sudo yum install -y docker

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2. 配置 Docker 仓库登录
在 Jenkins 服务器上（jenkins 用户）：
```bash
sudo su - jenkins
docker login your-registry.com
```

#### 3. 配置远程访问（可选）
如果需要 Jenkins 远程控制 Docker：
```bash
# 编辑 Docker 配置
sudo vim /etc/docker/daemon.json
```

添加：
```json
{{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"]
}}
```

重启：
```bash
sudo systemctl restart docker
```
"""

    guide += f"""
---

## 🏃 运行流水线

### 手动触发
1. 进入 Pipeline Job 页面
2. 点击 **Build Now**
3. 查看构建进度（点击构建编号 → Console Output）

### 查看结果
构建完成后：
- **蓝色**: 成功 ✅
- **红色**: 失败 ❌
- **黄色**: 不稳定 ⚠️

---

## 🐛 故障排查

### 问题 1: SSH 连接失败
**现象**: `Permission denied (publickey)`

**解决**:
```bash
# 1. 检查 Jenkins 服务器上的 SSH 密钥
sudo su - jenkins
cat ~/.ssh/id_rsa.pub

# 2. 确保公钥已添加到目标服务器的 authorized_keys
cat ~/.ssh/authorized_keys  # 在目标服务器上

# 3. 检查权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### 问题 2: Maven 构建失败
**现象**: `mvn: command not found`

**解决**:
- 在 Jenkins 中配置 Maven 工具
- 或在服务器上安装 Maven 并添加到 PATH

### 问题 3: 部署后服务无法启动
**现象**: `systemctl start failed`

**解决**:
```bash
# 在目标服务器上查看日志
sudo journalctl -u {project_name} -f

# 检查 JAR 文件是否存在
ls -la /opt/{project_name}/

# 检查端口占用
sudo lsof -i :8080
```

### 问题 4: 健康检查失败
**现象**: `curl: (7) Failed to connect`

**解决**:
- 检查应用是否正常启动
- 检查防火墙设置
- 增加等待时间（修改 sleep 时长）

---

## ⚙️ 自定义配置

### 修改 JVM 参数
编辑 `{project_name}.service`：
```ini
ExecStart=/usr/bin/java -jar -Xmx2g -Xms1g -Dspring.profiles.active=prod /opt/{project_name}/app.jar
```

### 修改部署路径
编辑 `Jenkinsfile` 中的环境变量：
```groovy
DEPLOY_PATH = '/your/custom/path'
```

### 添加构建参数
在 Jenkins Job 配置中：
1. 勾选 **This project is parameterized**
2. 添加 **String Parameter**：
   - 名称: `BRANCH`
   - 默认值: `main`

---

## 📚 参考文档

- [Jenkins Pipeline 官方文档](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
"""

    return guide

def generate_gitlab_guide(config):
    """Generate GitLab CI setup guide"""
    project_type = config.get('project_type', 'java')
    deploy_target = config.get('deploy_target', 'k8s')
    
    project_name = config.get('project_name', 'my-app')
    
    return f"""# GitLab CI 配置指南

## 📋 配置摘要

| 配置项 | 值 |
|--------|-----|
| **平台** | GitLab CI |
| **项目类型** | {project_type.upper()} |
| **部署目标** | {deploy_target.upper()} |
| **配置文件** | `.gitlab-ci.yml` |

## 📦 生成文件清单

```
cicd-output/
├── .gitlab-ci.yml           # GitLab CI 配置
├── setup-guide.md           # 本文件
├── docker-compose.yml       # 本地开发配置（可选）
└── README.md
```

---

## 🔧 前置准备

### 1. GitLab 版本要求
- **GitLab**: 13.0+ 推荐
- **GitLab Runner**: 13.0+

### 2. 安装 GitLab Runner

**Docker 方式安装：**
```bash
docker run -d --name gitlab-runner --restart always \\
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \\
  -v /var/run/docker.sock:/var/run/docker.sock \\
  gitlab/gitlab-runner:latest
```

**注册 Runner：**
```bash
docker exec -it gitlab-runner gitlab-runner register
```

按提示输入：
- GitLab URL: `https://gitlab.com` 或你的 GitLab 地址
- Registration token: 从 GitLab 项目 Settings → CI/CD → Runners 获取
- Executor: `docker` 或 `shell`
- Default Docker image: `maven:3.8-openjdk-8`

---

## 🔐 配置 CI/CD 变量

进入项目 **Settings → CI/CD → Variables**，添加以下变量：

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `CI_REGISTRY_USER` | Variable | Docker 仓库用户名 |
| `CI_REGISTRY_PASSWORD` | Variable | Docker 仓库密码 |
| `KUBE_CONFIG` | File | K8s kubeconfig 文件 | {'(K8s必需)' if deploy_target == 'k8s' else '(可选)'} |
| `WEBHOOK_URL` | Variable | 飞书/钉钉机器人地址 | (可选) |

---

## 🚀 使用说明

### 1. 复制配置文件
```bash
cp cicd-output/.gitlab-ci.yml /your-project/
git add .gitlab-ci.yml
git commit -m "Add CI/CD configuration"
git push
```

### 2. 触发流水线
- **自动**: Push 代码到仓库
- **手动**: 进入项目 CI/CD → Pipelines → Run pipeline

---

## 🐛 故障排查

### Runner 不执行作业
检查 Runner 状态：
```bash
docker exec -it gitlab-runner gitlab-runner status
```

### Docker 构建失败
确保 Runner 有 Docker 权限：
```bash
# 编辑 config.toml
docker exec -it gitlab-runner vi /etc/gitlab-runner/config.toml

# 添加 privileged = true
[runners.docker]
  privileged = true
```

---

## 📚 参考文档

- [GitLab CI/CD 文档](https://docs.gitlab.com/ee/ci/)
- [GitLab Runner 安装](https://docs.gitlab.com/runner/install/)
"""

if __name__ == '__main__':
    # Example usage
    config = {
        'platform': 'jenkins',
        'project_type': 'java',
        'deploy_target': 'ssh',
        'trigger': 'manual',
        'steps': ['build', 'deploy', 'notify'],
        'project_name': 'my-app'
    }
    
    if config['platform'] == 'jenkins':
        print(generate_jenkins_guide(config))
    else:
        print(generate_gitlab_guide(config))
