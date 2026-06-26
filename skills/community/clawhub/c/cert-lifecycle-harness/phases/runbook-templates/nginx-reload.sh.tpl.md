---
type: runbook-template
scope: nginx-reload
purpose: Nginx 配置热重载证书替换模板（单机 / 单绑定点）
---

# Runbook Template · Nginx Reload

```bash
#!/bin/bash
# =====================================================================
# Nginx 证书替换 · 单机单域（Fast Path 核心）
# 🟡 变更脚本
# 👀 Review 关注点：步骤 3 的 nginx -t 是否通过决定是否走 4
# 📋 前置：
#   - 新证书 + 私钥已在本机，权限 0600
#   - 旧证书路径已确认，有备份目录
# =====================================================================

set -euo pipefail

# ---- 0. 配置 ----
: "${NGINX_SSL_DIR:=/etc/nginx/ssl}"
: "${CERT_NAME:?e.g. example.com}"
: "${NEW_CERT_SRC:?新证书 fullchain.pem 路径}"
: "${NEW_KEY_SRC:?新私钥 privkey.pem 路径}"

BACKUP_DIR="$NGINX_SSL_DIR/backup-$(date +%Y%m%d-%H%M)"

# ---- 1. 备份 ----
sudo mkdir -p "$BACKUP_DIR"
sudo cp -a "$NGINX_SSL_DIR/$CERT_NAME".* "$BACKUP_DIR/"
echo "✅ 基线已落盘：$BACKUP_DIR"

# ---- 2. 部署新证书 ----
sudo cp "$NEW_CERT_SRC" "$NGINX_SSL_DIR/$CERT_NAME.fullchain.pem"
sudo cp "$NEW_KEY_SRC"  "$NGINX_SSL_DIR/$CERT_NAME.key"
sudo chmod 0644 "$NGINX_SSL_DIR/$CERT_NAME.fullchain.pem"
sudo chmod 0600 "$NGINX_SSL_DIR/$CERT_NAME.key"

# ---- 3. 预检 ----
if ! sudo nginx -t; then
  echo "🔴 nginx -t 失败，启动回滚"
  sudo cp -a "$BACKUP_DIR/$CERT_NAME".* "$NGINX_SSL_DIR/"
  exit 1
fi

# ---- 4. 热重载 ----
sudo systemctl reload nginx
sleep 2

# ---- 5. 验证 ----
EXPIRY=$(echo | openssl s_client -servername "$CERT_NAME" -connect "$CERT_NAME:443" 2>/dev/null \
  | openssl x509 -noout -enddate | sed 's/notAfter=//')
echo "✅ 当前证书过期：$EXPIRY"

# ---- 6. 自验证（HP-1）----
curl -sI "https://$CERT_NAME/" | head -1
```

## 回滚

```bash
sudo cp -a "$BACKUP_DIR/$CERT_NAME".* "$NGINX_SSL_DIR/"
sudo nginx -t && sudo systemctl reload nginx
```
