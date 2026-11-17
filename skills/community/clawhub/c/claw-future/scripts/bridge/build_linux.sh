#!/usr/bin/env bash
# ============================================================
# build_linux.sh  --  编译 libctp_bridge.so (Linux x64)
# 依赖: g++ 9+ (sudo apt install g++)
# SDK: TraderAPI 6.7.11 (20250617) + MdUserAPI 6.7.11 (20250617)
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# scripts/bridge/ 的上一级即仓库根（两个 ..）；勿改成三个 ..
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ---------- SDK 路径 ----------
LINUX_SDK="$REPO_ROOT/api/linux"

# ---------- 检查依赖 ----------
if [ ! -f "$LINUX_SDK/thosttraderapi_se.so" ]; then
    echo "[ERROR] TraderAPI .so 未找到: $LINUX_SDK/thosttraderapi_se.so"
    exit 1
fi
if [ ! -f "$LINUX_SDK/thostmduserapi_se.so" ]; then
    echo "[ERROR] MdUserAPI .so 未找到: $LINUX_SDK/thostmduserapi_se.so"
    exit 1
fi

# ---------- 输出目录 ----------
OUT_DIR="$SCRIPT_DIR/../"

# CTP SDK 的 .so 不带 lib 前缀；先建 lib 前缀软链，-l 链接与运行时 NEEDED 才能解析
for _lib in thosttraderapi_se thostmduserapi_se; do
    [ -e "$LINUX_SDK/lib$_lib.so" ] || ln -s "$_lib.so" "$LINUX_SDK/lib$_lib.so"
done

echo "[INFO] 编译 libctp_bridge.so ..."

g++ \
    -shared -fPIC -fvisibility=hidden \
    -std=c++17 -O2 \
    -DCTPBRIDGE_EXPORTS \
    -I"$LINUX_SDK" \
    "$SCRIPT_DIR/ctp_bridge.cpp" \
    -L"$LINUX_SDK" \
    -lthosttraderapi_se \
    -lthostmduserapi_se \
    -Wl,-rpath,'$ORIGIN' \
    -o "${OUT_DIR}libctp_bridge.so"

# 拷贝 CTP .so（含 lib 前缀软链）到输出目录（运行时需要与 libctp_bridge.so 同目录）
for _lib in thosttraderapi_se thostmduserapi_se; do
    cp -f "$LINUX_SDK/$_lib.so"  "$OUT_DIR"
    ln -sf "$_lib.so" "$OUT_DIR/lib$_lib.so"
done

echo ""
echo "[OK] 编译成功，输出文件："
echo "     ${OUT_DIR}libctp_bridge.so"
echo "     ${OUT_DIR}thosttraderapi_se.so"
echo "     ${OUT_DIR}thostmduserapi_se.so"
