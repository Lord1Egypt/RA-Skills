---
name: faa-wsl
description: 将 FastapiAdmin 在 Windows WSL2 Ubuntu 环境下自动部署。包括环境检查、依赖安装（pip/pnpm/MySQL/Redis/Nginx）、前后端代码克隆与构建、Nginx SPA 路由修复（alias+try_files 循环问题）、WSL2 网络访问（宿主机浏览器访问）、SSL 证书配置。当用户要求部署 FastapiAdmin、在 WSL2 中安装 FastapiAdmin、或需要完整部署前后端服务时使用。
---

# FastapiAdmin WSL2 部署

## 环境要求

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | ≥ 3.10 | WSL2 Ubuntu 默认 3.12 |
| Node.js | ≥ 20.0 | WSL2 已装 v22 |
| pnpm | ≥ 9.0 | 需单独安装 |
| MySQL | ≥ 8.0 | 需单独安装 |
| Redis | ≥ 7.0 | 需单独安装 |
| Nginx | 任意 | 需单独安装 |

## 工作目录

统一使用 `~/workdir`（即 `/home/<user>/workdir`）作为部署根目录。

---

## Step 1：安装系统依赖（pip/pnpm/MySQL/Redis/Nginx）

```bash
# 安装 pip（Ubuntu 强制模式）
curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py --break-system-packages

# 安装 pnpm
npm install -g pnpm

# 安装 MySQL + Redis + Nginx
sudo apt-get update
sudo apt-get install -y mysql-server redis-server nginx

# 安装 python3-venv（venv 创建必需）
sudo apt-get install -y python3.12-venv

# 启动服务
sudo service mysql start
sudo service redis-server start
```

## Step 2：配置 MySQL 数据库

```bash
sudo mysql -e "CREATE DATABASE IF NOT EXISTS fastapiadmin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'fastapiadmin'@'localhost' IDENTIFIED BY 'fastapiadmin123';"
sudo mysql -e "GRANT ALL PRIVILEGES ON fastapiadmin.* TO 'fastapiadmin'@'localhost'; FLUSH PRIVILEGES;"
```

## Step 3：克隆代码

```bash
mkdir -p ~/workdir && cd ~/workdir
git clone https://gitee.com/fastapiadmin/FastapiAdmin.git
git clone https://gitee.com/fastapiadmin/FastDocs.git
```

## Step 4：后端初始化

```bash
cd ~/workdir/FastapiAdmin/backend

# 创建虚拟环境
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 配置环境变量
cp env/.env.dev.example env/.env.dev
# 编辑 env/.env.dev，修改：
#   DATABASE_USER = "fastapiadmin"
#   DATABASE_PASSWORD = "fastapiadmin123"
#   REDIS_PASSWORD = ""（无密码则留空）

# 生成并执行迁移
./venv/bin/python main.py revision --env=dev
./venv/bin/python main.py upgrade --env=dev
```

## Step 5：前端构建

```bash
cd ~/workdir/FastapiAdmin/frontend

# 安装依赖
pnpm install

# 创建生产环境配置
cat > .env.production << 'EOF'
VITE_APP_ENV=production
VITE_APP_TITLE=FastapiAdmin
VITE_API_BASE_URL=http://<WSL2_IP>
VITE_APP_BASE_API=/api/v1
VITE_TIMEOUT=10000
VITE_APP_WS_ENDPOINT=ws://<WSL2_IP>
EOF

# 构建
pnpm run build
```

## Step 6：Nginx 配置（关键）

Nginx 配置源码位于 `~/workdir/FastapiAdmin/devops/nginx/nginx.conf`，部署时复制到 `/etc/nginx/nginx.conf`。

### 6.1 生成自签名 SSL 证书

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.pem \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=FastapiAdmin/OU=Dev/CN=localhost"
sudo chmod 600 /etc/nginx/ssl/server.key
```

### 6.2 Nginx 配置模板

> ⚠️ **关键修复**：原配置中 `alias` + `try_files` 组合会导致**重定向循环**。必须用精确匹配 `location = /web/index.html` 作为内部 fallback，而非 named location 或路径重写。

编辑 `~/workdir/FastapiAdmin/devops/nginx/nginx.conf`，替换 `location /web` 部分：

```nginx
# HTTP server块
server {
    listen 80;
    server_name service.fastapiadmin.com;

    location = /web {
        return 301 /web/;
    }
    location /web/ {
        alias /usr/share/nginx/html/frontend/;
        index index.html;
        try_files $uri $uri/ /web_fallback.html;
    }
    location = /web_fallback.html {
        internal;
        alias /usr/share/nginx/html/frontend/index.html;
    }

    location /api/v1 {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass http://127.0.0.1:8001;
    }
}
```

### 6.3 部署 Nginx 配置

```bash
sudo cp ~/workdir/FastapiAdmin/devops/nginx/nginx.conf /etc/nginx/nginx.conf
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo nginx
```

## Step 7：启动后端服务

```bash
cd ~/workdir/FastapiAdmin/backend
./venv/bin/python main.py run --env=dev &
```

---

## 宿主机访问

WSL2 IP 不固定，每次重启后可能变化。获取方式：

```bash
hostname -I | awk '{print $1}'
```

宿主机 Windows 浏览器访问：
- 前端：`http://<WSL2_IP>/web/`
- API 文档：`http://<WSL2_IP>/api/v1/docs`

> 💡 部署后如果 WSL2 IP 变化，只需更新 Nginx 中 `.env.production` 的 `VITE_API_BASE_URL` 并重建前端即可。

## 故障排查

详见 [references/troubleshooting.md](references/troubleshooting.md)。

## 快速命令汇总

```bash
# 一键启动
cd ~/workdir/FastapiAdmin/backend && ./venv/bin/python main.py run --env=dev

# 查看 WSL2 IP
hostname -I | awk '{print $1}'

# Nginx 配置测试与重载
sudo nginx -t && sudo nginx -s reload

# 查看 Nginx 错误日志
sudo tail /var/log/nginx/error.log
```
