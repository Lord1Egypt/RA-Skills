---
type: runbook-template
scope: k8s-secret-rollover
purpose: K8s Secret（手工管理场景）证书滚动更新模板
---

# Runbook Template · K8s Secret Rollover（手工管理）

> 若你用 cert-manager 自动化，**不需要此模板**；直接更新 Certificate 资源即可。本模板用于"没接入 cert-manager"的手工 Secret。

```bash
#!/bin/bash
# =====================================================================
# K8s TLS Secret 滚动更新（手工管理场景）
# 🔴 变更脚本
# 👀 Review 关注点：步骤 2 替换 Secret 后 Ingress 自动重载是否可靠
# 📋 前置：kubectl 对目标 namespace 有 write 权限
# =====================================================================

set -euo pipefail

: "${NAMESPACE:?e.g. prod-api}"
: "${SECRET_NAME:?e.g. example-com-tls}"
: "${NEW_CERT:?新证书 fullchain.pem 路径}"
: "${NEW_KEY:?新私钥 privkey.pem 路径}"
: "${INGRESS_NAME:?e.g. example-api-ingress}"

# ---- 1. 备份 ----
kubectl -n "$NAMESPACE" get secret "$SECRET_NAME" -o yaml \
  > "/tmp/secret-backup-$SECRET_NAME-$(date +%Y%m%d-%H%M).yaml"

# ---- 2. 替换 Secret（原地） ----
kubectl -n "$NAMESPACE" create secret tls "$SECRET_NAME" \
  --cert="$NEW_CERT" --key="$NEW_KEY" \
  --dry-run=client -o yaml | kubectl apply -f -

# ---- 3. 触发 Ingress 重载 ----
# 部分 Ingress Controller（如 nginx-ingress）会自动检测 Secret 变化，
# 若不可靠则显式滚动 Ingress Controller Pod
kubectl -n ingress-nginx rollout restart deployment/ingress-nginx-controller || true

# ---- 4. 验证 ----
sleep 10
kubectl -n "$NAMESPACE" get ingress "$INGRESS_NAME" -o jsonpath='{.spec.tls[*].secretName}'
echo ""

# ---- 5. 端到端握手验证 ----
HOST=$(kubectl -n "$NAMESPACE" get ingress "$INGRESS_NAME" -o jsonpath='{.spec.rules[0].host}')
echo | openssl s_client -servername "$HOST" -connect "$HOST:443" 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

## 回滚

```bash
kubectl -n "$NAMESPACE" apply -f /tmp/secret-backup-$SECRET_NAME-*.yaml
kubectl -n ingress-nginx rollout restart deployment/ingress-nginx-controller
```

## 客户核对点

1. 使用的 Ingress Controller 是否自动检测 Secret 变化？
   - nginx-ingress-controller ≥ v1.x：✅ 默认自动
   - 某些老版本：❌ 需手工滚动
2. 是否有多个 Ingress 引用同一 Secret？回滚时注意全量影响
