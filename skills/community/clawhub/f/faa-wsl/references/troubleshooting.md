# FastapiAdmin WSL2 部署故障排查

## 1. 500 Internal Server Error

### 原因：Nginx `alias` + `try_files` 重定向循环

**错误日志：**
```
rewrite or internal redirection cycle while internally redirecting to "/web/index.html"
```

**说明：** 原 devops 配置中 `location /web { alias ...; try_files $uri $uri/ /web/index.html; }`，`try_files` 的 fallback `/web/index.html` 会重新被 `location /web` 处理，导致死循环。

**修复：** 使用精确匹配的 internal location 作为 fallback：
```nginx
location = /web {
    return 301 /web/;
}
location /web/ {
    alias /usr/share/nginx/html/frontend/;
    try_files $uri $uri/ /web_fallback.html;
}
location = /web_fallback.html {
    internal;
    alias /usr/share/nginx/html/frontend/index.html;
}
```

---

## 2. 前端页面空白或 `%VITE_APP_TITLE%` 原样显示

### 原因：构建时缺少 `.env.production`

Vite 在 `production` 模式下构建时，如果 `VITE_*` 变量找不到，会保留原样不替换。

**修复：**
```bash
cat > frontend/.env.production << 'EOF'
VITE_APP_ENV=production
VITE_APP_TITLE=FastapiAdmin
VITE_API_BASE_URL=http://<WSL2_IP>
VITE_APP_BASE_API=/api/v1
VITE_TIMEOUT=10000
VITE_APP_WS_ENDPOINT=ws://<WSL2_IP>
EOF
pnpm run build
```

---

## 3. 自签名证书导致 Chrome 拒绝请求

### 表现

Windows Chrome 访问 HTTPS URL 时报 `ERR_CERT_AUTHORITY_INVALID`，JS 发出的 API 请求全部失败。

### 方案一（推荐）：HTTP 访问

在 `server_name` 为 `localhost` 时，Nginx 配置中删除 HTTPS 相关配置，只保留 HTTP，将 `location /api/v1` 的代理目标改为 HTTP。

### 方案二：接受证书警告

Chrome 可以点击"高级"→"继续前往"，但每次访问都需要操作，不推荐。

---

## 4. Windows 宿主机无法访问 WSL2 服务

### 原因：使用了 `localhost` 或 `127.0.0.1`

WSL2 有独立 IP，`localhost` 在 Windows 上指向 Windows 自身，而非 WSL2。

**获取 WSL2 IP：**
```bash
hostname -I | awk '{print $1}'
```

**Windows 浏览器必须用 WSL2 IP 访问：**
```
http://<WSL2_IP>/web/
```

**可选：绑定 hosts（PowerShell 管理员）**
```powershell
notepad C:\Windows\System32\drivers\etc\hosts
# 添加一行：
#   <WSL2_IP>    localhost
```

---

## 5. WSL2 重启后 IP 变化

WSL2 IP 每次重启可能不同。可用脚本自动更新：
```bash
# 获取当前 WSL2 IP
WSL2_IP=$(hostname -I | awk '{print $1}')
# 更新前端配置
sed -i "s/VITE_API_BASE_URL=.*/VITE_API_BASE_URL=http:\/\/$WSL2_IP/" ~/workdir/FastapiAdmin/frontend/.env.production
# 重建前端
cd ~/workdir/FastapiAdmin/frontend && pnpm run build
# 部署
sudo cp -r dist/* /usr/share/nginx/html/frontend/
# 重载 Nginx
sudo nginx -s reload
```

---

## 6. 后端启动报错 `ModuleNotFoundError: No module named 'prefect'`

`prefect` 是工作流模块依赖，不在 `requirements.txt` 中，会导致部分路由注册失败但不影响其他功能。

**如需完整功能：**
```bash
./venv/bin/pip install prefect
./venv/bin/python main.py run --env=dev
```

---

## 7. 数据库迁移问题

### 迁移命令格式（无中文参数）
```bash
./venv/bin/python main.py revision --env=dev      # 生成迁移
./venv/bin/python main.py upgrade --env=dev      # 执行迁移
```

### 初始化数据（启动时自动执行）
数据库初始化数据在服务首次启动时自动通过 `InitializeData().init_db()` 写入，无需手动调用。

---

## 8. 验证清单

| 检查项 | 验证命令 |
|--------|----------|
| MySQL 运行 | `sudo service mysql status` |
| Redis 运行 | `sudo service redis-server status` |
| Nginx 运行 | `ps aux \| grep nginx` |
| 后端 API | `curl http://127.0.0.1:8001/api/v1/docs` |
| 前端静态 | `curl http://<WSL2_IP>/web/` |
| API 代理 | `curl http://<WSL2_IP>/api/v1/system/auth/captcha/get` |

> 注意：所有 `curl` 验证在 WSL2 内部执行时用 `127.0.0.1`，从 Windows 访问用 `<WSL2_IP>`。
