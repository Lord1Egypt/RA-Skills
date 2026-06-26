---
type: runbook-template
scope: jks-rollover
purpose: Java KeyStore (JKS) 证书热切换模板（含备份 / 导入 / 热重载 / 回滚）
notes: 所有生产值以占位符出现，调用前由客户填入
---

# Runbook Template · JKS Rollover

> 📌 所有 `${VAR}` 占位符必须由客户填入真实值。密钥类变量**禁止硬编码**，按 `05-dry-run-matrix.md §5 密钥获取方式抽象层` 从客户的密钥管理系统获取。

```bash
#!/bin/bash
# =====================================================================
# JKS Rollover · Java KeyStore 证书热切换
# 🔴 变更脚本（含生产写操作）
# 👀 Review 关注点：Step 2-3 是改生产的核心步骤
# ⚠️ 前置：必须先在 Phase 5 做过 Dry-Run（详见 05-dry-run-matrix.md）
# 📋 前置依赖：
#   - 目标主机 SSH 已授权
#   - 新证书已转为 PKCS12 格式
#   - 客户已批准本次执行（见审批话术 05-dry-run-matrix.md §3）
# =====================================================================

set -euo pipefail

# ---- 0. 配置（由客户填入）----
: "${TARGET_HOST:?e.g. legacy-api-01.internal}"
: "${KEYSTORE_PATH:?e.g. /opt/legacy-app/conf/keystore.jks}"
: "${ALIAS:?e.g. example-com-cert}"
: "${NEW_P12:?e.g. /tmp/new-cert.p12}"
: "${P12_PASS:?通过密钥管理系统获取，禁止硬编码}"
: "${JKS_PASS:?通过密钥管理系统获取，禁止硬编码}"
: "${APP_PID_FILE:?e.g. /var/run/legacy-app.pid}"
: "${RELOAD_SIGNAL:=HUP}"    # 客户确认的热重载信号（HUP / USR1 / USR2，默认 HUP）
: "${HEALTH_URL:?e.g. https://api.example.com/health}"

# ---- 1. 基线快照 ----
BACKUP_DIR="/var/backups/jks/$(date +%Y%m%d-%H%M)"
sudo mkdir -p "$BACKUP_DIR"
sudo cp "$KEYSTORE_PATH" "$BACKUP_DIR/keystore.jks.bak"
sudo keytool -list -v -keystore "$BACKUP_DIR/keystore.jks.bak" -storepass "$JKS_PASS" \
  > "$BACKUP_DIR/before.txt"
echo "✅ 基线已落盘：$BACKUP_DIR"

# ---- 2. 删除旧 alias ----
sudo keytool -delete -alias "$ALIAS" \
  -keystore "$KEYSTORE_PATH" \
  -storepass "$JKS_PASS"

# ---- 3. 导入新证书 ----
sudo keytool -importkeystore \
  -srckeystore "$NEW_P12" -srcstoretype PKCS12 -srcstorepass "$P12_PASS" \
  -destkeystore "$KEYSTORE_PATH" -deststoretype JKS -deststorepass "$JKS_PASS" \
  -alias "$ALIAS"

# ---- 4. 热重载 ----
APP_PID=$(cat "$APP_PID_FILE")
sudo kill -"$RELOAD_SIGNAL" "$APP_PID"
sleep 5

# ---- 5. 验证 ----
if ! curl -sk --resolve "${HEALTH_URL#*//}:443:127.0.0.1" "$HEALTH_URL" | grep -q "ok"; then
  echo "🔴 验证失败，启动回滚"
  sudo cp -a "$BACKUP_DIR/keystore.jks.bak" "$KEYSTORE_PATH"
  sudo kill -"$RELOAD_SIGNAL" "$APP_PID"
  exit 1
fi
echo "✅ 变更完成"

# ---- 6. 自验证命令（HP-1 落地）----
sudo keytool -list -v -keystore "$KEYSTORE_PATH" -storepass "$JKS_PASS" \
  | grep -A5 "$ALIAS"
```

## 回滚命令（单独记忆）

```bash
sudo cp -a "$BACKUP_DIR/keystore.jks.bak" "$KEYSTORE_PATH"
sudo kill -"$RELOAD_SIGNAL" "$(cat $APP_PID_FILE)"
```

## 客户自行核对点（Review 前必问）

1. `$RELOAD_SIGNAL` 是 `HUP` / `USR1` / `USR2`？老应用实际使用的信号可能与默认不同
2. JKS 密码的获取方式？（Vault / K8s Secret / 明文配置 / KMS）
3. 应用是否真的支持"热重载"？有些老应用要重启进程
4. 备份目录 `/var/backups/jks/` 磁盘空间？
5. 如果 `keytool -delete` 之后 `-importkeystore` 失败，JKS 会处于**空状态**，业务立即报错——应在 Phase 5 Dry-Run 验证此中间态的可控性

## 相关文件

- [`../05-dry-run-matrix.md`](../05-dry-run-matrix.md) · Java JKS 演练方法
- [`../06-verify-rollback-playbook.md`](../06-verify-rollback-playbook.md) · 验证矩阵
