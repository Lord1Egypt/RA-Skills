---
name: axiomata-deploy
description: "在约15分钟内部署公共网站（HTML + Docker + DNS + 域名）。触发词：'deploy website'、'build and deploy'、'create web presence'、'launch site'、'deploy to web'、'publish website'、'setup web server'、'docker deploy'、'domain setup'、'DNS configuration'、'full stack deploy'。适用于想要快速、自主部署管道的用户。"
---

# 🌐 Axiomata Deploy — 网站部署技能

> 在约15分钟内部署公共网站

| 信息 | 值 |
|------|-----|
| **版本** | 1.0.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 目的和范围

### 目标

为任何 OpenClaw 代理提供使用 Docker、DNS 和域名配置部署公共网站的能力。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| "部署网站" | 开始部署流程 |
| "创建网站" | 初始化网站项目 |
| "Docker 部署" | 构建并推送 Docker 镜像 |
| "域名设置" | 配置 DNS |
| "完整栈部署" | 执行完整部署管道 |

---

## 2. 部署架构

```
┌─────────────────────────────────────────────┐
│           网站部署架构                      │
├─────────────────────────────────────────────┤
│  1. 前端 (HTML/CSS/JS)                     │
│     → 静态网站或 SPA                        │
│                                             │
│  2. Docker 容器化                           │
│     → nginx 或自定义容器                    │
│                                             │
│  3. DNS 配置                                │
│     → A 记录指向服务器 IP                  │
│                                             │
│  4. 域名                                    │
│     → 指向公共端点                          │
└─────────────────────────────────────────────┘
```

---

## 3. 部署步骤

### 步骤 1：准备网站文件

```bash
# 创建网站目录
mkdir -p ~/websites/<project-name>
cd ~/websites/<project-name>

# 创建 index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的网站</title>
</head>
<body>
    <h1>你好，世界！</h1>
</body>
</html>
EOF
```

### 步骤 2：创建 Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
EOF
```

### 步骤 3：构建 Docker 镜像

```bash
# 构建镜像
docker build -t <username>/<project-name>:latest .

# 测试本地运行
docker run -d -p 8080:80 <username>/<project-name>:latest
```

### 步骤 4：推送到镜像仓库

```bash
# 登录 Docker Hub
docker login

# 推送
docker push <username>/<project-name>:latest
```

### 步骤 5：服务器部署

```bash
# 在服务器上拉取
docker pull <username>/<project-name>:latest

# 运行容器
docker run -d -p 80:80 --name <project-name> <username>/<project-name>:latest
```

### 步骤 6：DNS 配置

```
1. 登录域名注册商
2. 添加 DNS 记录：
   - A 记录：@ → <服务器IP>
   - CNAME：www → @
3. 等待 DNS 传播（5分钟-48小时）
```

---

## 4. 工具要求

| 工具 | 用途 | 必需 |
|------|------|------|
| `exec` | 执行 Docker 命令 | 是 |
| `write` | 创建文件 | 是 |
| `read` | 读取配置 | 可选 |

### 必需环境

| 环境 | 要求 |
|------|------|
| Docker | 已安装 |
| Docker Hub 账户 | 已有 |
| 服务器 | SSH 访问 |
| 域名 | 已注册 |

---

## 5. 快速部署模板

```bash
# 一键部署
PROJECT=<project-name>
USERNAME=<dockerhub-username>
DOMAIN=<domain.com>

# 1. 创建项目
mkdir -p ~/$PROJECT && cd ~/$PROJECT

# 2. 创建网站文件
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>$PROJECT</title></head>
<body><h1>$PROJECT 已上线！</h1></body>
</html>
EOF

# 3. Dockerfile
echo 'FROM nginx:alpine COPY . /usr/share/nginx/html EXPOSE 80' > Dockerfile

# 4. 构建并推送
docker build -t $USERNAME/$PROJECT:latest .
docker push $USERNAME/$PROJECT:latest

echo "部署完成！镜像：$USERNAME/$PROJECT:latest"
```

---

## 6. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| Docker 未安装 | 先安装 Docker |
| 域名被占用 | 使用子域名 |
| 服务器无 SSH | 配置 SSH 密钥 |
| 端口冲突 | 更改容器端口映射 |
| DNS 未传播 | 使用 IP 直接测试 |

---

## 7. 验证

```bash
# 检查容器运行
docker ps | grep <project-name>

# 检查网站响应
curl -I https://<domain.com>

# 检查 SSL（如果使用 HTTPS）
openssl s_client -connect <domain.com>:443
```

---

_In Altum Per Deploy._
🌐 Axiomata Deploy v1.0