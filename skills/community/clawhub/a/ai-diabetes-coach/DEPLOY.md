# 部署说明

## 本地运行

```bash
python app.py
```

## 生产部署

### 方式一：Gunicorn（本地部署）

```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 app:app --timeout 120
```

**注意：生产部署必须绑定 127.0.0.1，前面使用 Nginx 反向代理 + TLS。**

### 方式二：Docker（限制为本地）

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py core.py .
EXPOSE 5000
ENV BIND_HOST=127.0.0.1
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:5000", "app:app"]
```

## Nginx 反向代理（生产必须）

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**安全清单：**
- ✅ 强制 API 鉴权（设置强 `API_KEY` 环境变量，未设置时服务拒绝启动）
- ✅ 绑定本地 `127.0.0.1`，不直接暴露（默认值）
- ✅ Nginx 反向代理 + TLS
- ✅ 不用于多用户场景（无用户隔离）
```
