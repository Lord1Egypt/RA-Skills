#!/bin/bash
# diff-env.sh - 对比 service unit 跟 .bak 找丢失的 user env
# 用法: bash diff-env.sh [bak-file]
#   不传 bak-file 找最新的 .bak.<ts>

set -e

SERVICE=~/.config/systemd/user/openclaw-gateway.service

# 找最新的 .bak
if [ -n "$1" ]; then
    SERVICE_BAK="$1"
else
    SERVICE_BAK=$(ls -t "${SERVICE}".bak.* 2>/dev/null | head -1)
    if [ -z "$SERVICE_BAK" ]; then
        echo "ERROR: 找不到 .bak 文件"
        echo "  用法: bash diff-env.sh [path-to-bak]"
        echo "  或先跑 backup-env.sh"
        exit 1
    fi
fi

if [ ! -f "$SERVICE_BAK" ]; then
    echo "ERROR: .bak 不存在: $SERVICE_BAK"
    exit 1
fi

echo "=== diff-env: $SERVICE_BAK ↔ $SERVICE ==="
echo ""

# 1. 完整 diff
echo "=== 完整 diff ==="
diff "$SERVICE_BAK" "$SERVICE" || true
echo ""

# 2. 关键 env 检查 (5 个常丢)
echo "=== 关键 user env 检查 ==="
for env in CUDA_HOME LD_LIBRARY_PATH NVIDIA_DRIVER_CAPABILITIES QMD_EMBED_MODEL HF_ENDPOINT; do
    in_new=$(grep -c "^Environment=$env=" "$SERVICE" || true)
    in_bak=$(grep -c "^Environment=$env=" "$SERVICE_BAK" || true)
    if [ "$in_new" -gt "0" ]; then
        val=$(grep "^Environment=$env=" "$SERVICE" | head -1 | cut -d= -f2-)
        echo "  ✓ $env (=$val)"
    else
        echo "  ✗ $env MISSING (bak 有 $in_bak 个, 新文件 0 个)"
    fi
done
echo ""

# 3. Description 一致性
echo "=== Description / version 一致性 ==="
DESC_NEW=$(grep "^Description=" "$SERVICE" | head -1)
DESC_BAK=$(grep "^Description=" "$SERVICE_BAK" | head -1)
VER_NEW=$(grep "^Environment=OPENCLAW_SERVICE_VERSION=" "$SERVICE" | head -1)
VER_BAK=$(grep "^Environment=OPENCLAW_SERVICE_VERSION=" "$SERVICE_BAK" | head -1)
echo "  Description:"
echo "    .bak: $DESC_BAK"
echo "    new:  $DESC_NEW"
echo "  OPENCLAW_SERVICE_VERSION:"
echo "    .bak: $VER_BAK"
echo "    new:  $VER_NEW"
echo ""

# 4. ExecStart 路径
echo "=== ExecStart 路径 ==="
EXEC_BIN_BAK=$(grep "^ExecStart=" "$SERVICE_BAK" | head -1)
EXEC_BIN_NEW=$(grep "^ExecStart=" "$SERVICE" | head -1)
echo "  .bak: $EXEC_BIN_BAK"
echo "  new:  $EXEC_BIN_NEW"
echo ""

# 5. 实际 binary 版本
echo "=== 实际 binary 版本 (跟 service version 应该一致) ==="
BIN_VER=$(node -e "console.log(require('\$HOME/openclaw-local/package.json').version)" 2>/dev/null)
echo "  实际: $BIN_VER"
echo ""

# 6. 建议 (如果有 MISSING)
echo "=== 建议 ==="
MISSING=0
for env in CUDA_HOME LD_LIBRARY_PATH NVIDIA_DRIVER_CAPABILITIES QMD_EMBED_MODEL HF_ENDPOINT; do
    if ! grep -q "^Environment=$env=" "$SERVICE"; then
        MISSING=$((MISSING + 1))
    fi
done
if [ "$MISSING" -gt "0" ]; then
    echo "  ⚠ $MISSING 个 user env 丢失, 需要手动追加"
    echo "  参考 references/03-upgrade.md 步骤 3"
fi
if [ "$DESC_NEW" != "$DESC_BAK" ]; then
    echo "  ⚠ Description 变了, 检查 binary 路径跟 version 是否一致"
fi
