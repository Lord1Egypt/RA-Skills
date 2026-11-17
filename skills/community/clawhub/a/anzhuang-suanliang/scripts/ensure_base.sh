#!/usr/bin/env bash
# 显式依赖底座（方案二）：安装/运行任意算量 skill 时自动检测 cad-file-reader。
#   已装证书 -> 复用它并自动补齐其 vendor（缺库自动下载，CAD_AUTO_SETUP=0 关闭）
#   未装        -> 默认自动下载安装底座（需联网；CAD_FILE_READER_VERSION 可覆盖）
#   降级        -> SKILL_NO_BASE=1 时跳过底座，只使用已有扫描/表格输入（精度受限）
# 用法：BASE_DIR="$(scripts/ensure_base.sh)"   # stdout=底座目录；为空=降级模式
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="安装算量"
BASE_DIR="${CAD_SKILL_DIR:-}"
if [ -n "$BASE_DIR" ]; then
  BASE_DIR="$(cd "$BASE_DIR" 2>/dev/null && pwd || true)"
fi
if [ -z "$BASE_DIR" ]; then
  for d in "$SKILL_DIR/../cad-file-reader" "$HOME"/.workbuddy/skills/*/cad-file-reader "$HOME/.claude/skills/cad-file-reader" "$HOME/.codex/skills/cad-file-reader"; do
    if [ -d "$d/scripts" ]; then BASE_DIR="$(cd "$d" 2>/dev/null && pwd)"; break; fi
  done
fi

if [ -n "$BASE_DIR" ] && [ -x "$BASE_DIR/scripts/ensure_runtime.sh" ]; then
  bash "$BASE_DIR/scripts/ensure_runtime.sh" --quiet || exit $?
  echo "$BASE_DIR"
  exit 0
fi

if [ -n "$BASE_DIR" ] && [ -d "$BASE_DIR/vendor/ezdxf" ]; then
  echo >&2 "[$SKILL_NAME] 检测到底座 cad-file-reader（较旧版本）；建议升级到 >=0.28.0 获得自动运行时自举。"
  echo "$BASE_DIR"
  exit 0
fi

if [ "${SKILL_NO_BASE:-0}" = "1" ]; then
  echo "[$SKILL_NAME] 未检测到识图底座 cad-file-reader；已启用降级模式（仅用已有扫描/表格输入，精度受限）。可设 CAD_SKILL_DIR 指向底座。" >&2
  exit 0
fi

if [ -n "$BASE_DIR" ] && [ -d "$BASE_DIR/vendor" ]; then
  echo >&2 "[$SKILL_NAME] 底座 cad-file-reader 的 vendor 缺失且无法自举，请升级到 0.28.0 或运行 $BASE_DIR/scripts/setup.sh。"
  exit 2
fi

# ---- 自动安装底座（显式依赖，非捆绑，带 SHA-256 完整性校验） -----
VER="${CAD_FILE_READER_VERSION:-0.34.1}"
REPO="${CAD_FILE_READER_REPO:-lisong2003-lgtm/cad-file-reader}"
SHA_BIN="$(command -v shasum || command -v sha256sum || true)"
if [ -z "$SHA_BIN" ]; then echo >&2 "[$SKILL_NAME] 缺少 sha256sum/shasum 校验工具，停止自动安装底座。"; exit 3; fi
calc_sha256() {
  if [ "${SHA_BIN##*/}" = "shasum" ]; then "$SHA_BIN" -a 256 "$1" | awk '{print $1}'
  else "$SHA_BIN" "$1" | awk '{print $1}'; fi
}
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
BASE_DIR="${CAD_SKILL_DIR:-$SKILL_DIR/../cad-file-reader}"
if [ -d "$BASE_DIR" ]; then
  echo >&2 "[$SKILL_NAME] 底座目录已存在，未自动更新：$BASE_DIR"
  exit 2
fi
echo >&2 "[$SKILL_NAME] 将同时安装显式依赖：cad-file-reader（识图底座，用于提高 $(echo $SKILL_NAME) 准确率，含 SHA-256 校验）。"
URL="https://github.com/${REPO}/releases/download/v${VER}/cad-file-reader-full-${VER}.zip"
if ! curl -sL --http1.1 --fail --max-time "${CAD_DOWNLOAD_TIMEOUT:-600}" "$URL" -o "$TMP/base.zip"; then
  echo >&2 "[$SKILL_NAME] 下载底座失败。离线请设 SKILL_NO_BASE=1 降级使用；联网重试建议 export CAD_FILE_READER_VERSION=${VER} 后重试。"
  exit 3
fi
SUM_FILE=""
for u in \
  "https://github.com/${REPO}/releases/download/v${VER}/SHA256SUMS-cad-file-reader-${VER}.txt" \
  "https://github.com/${REPO}/releases/download/v${VER}/SHA256SUMS.txt"; do
  if curl -sL --http1.1 --fail --max-time "${CAD_DOWNLOAD_TIMEOUT:-600}" "$u" -o "$TMP/sums.txt"; then SUM_FILE="$TMP/sums.txt"; break; fi
done
if [ -z "$SUM_FILE" ]; then
  echo >&2 "[$SKILL_NAME] 底座校验文件下载失败，为安全起见不安装未校验底座。"
  exit 3
fi
EXPECT="$(grep -E "cad-file-reader-full-${VER}\.zip[[:space:]]*$|cad-file-reader-full-${VER}\.zip$" "$SUM_FILE" | awk '{print $1}' | head -1)"
if [ -z "$EXPECT" ]; then
  echo >&2 "[$SKILL_NAME] 校验文件里缺少 cad-file-reader-full-${VER}.zip 条目，停止自动安装。"
  exit 3
fi
ACTUAL="$(calc_sha256 "$TMP/base.zip")"
if [ "$ACTUAL" != "$EXPECT" ]; then
  echo >&2 "[$SKILL_NAME] 底座 SHA-256 校验失败，已拒绝安装（期望 $EXPECT，实际 $ACTUAL）。"
  exit 3
fi
echo >&2 "[$SKILL_NAME] 底座 SHA-256 校验通过 ✓ (${VER})"
if ! unzip -oq "$TMP/base.zip" -d "$TMP/src" 2>/dev/null; then
  echo >&2 "[$SKILL_NAME] 底座压缩包解压失败。"
  exit 3
fi
SRC=""
for cand in "$TMP/src/cad-file-reader" "$TMP/src"/cad-file-reader-*; do
  if [ -f "$cand/manifest.json" ] && [ -d "$cand/scripts" ]; then SRC="$cand"; break; fi
done
if [ -z "$SRC" ]; then
  # 兼容压包不带顶层目录的情况
  SRC="$TMP/src"
fi
if [ ! -d "$SRC" ] || [ ! -f "$SRC/scripts/ensure_runtime.sh" ]; then
  echo >&2 "[$SKILL_NAME] 底座内容不完整（缺少 ensure_runtime.sh），说明下载到了过旧版本，请稍后重试。"
  exit 3
fi
INNER_VER="$(sed -n 's/.*"version"[ ]*:[ ]*"\([^"]*\)".*/\1/p' "$SRC/manifest.json" | head -1)"
if [ "$INNER_VER" != "$VER" ]; then
  echo >&2 "[$SKILL_NAME] 底座包内版本 ${INNER_VER:-未知} 与期望 ${VER} 不一致，已拒绝安装。"
  exit 3
fi
mkdir -p "$(dirname "$BASE_DIR")"
cp -R "$SRC" "$BASE_DIR"
if [ -x "$BASE_DIR/scripts/ensure_runtime.sh" ]; then
  bash "$BASE_DIR/scripts/ensure_runtime.sh" --quiet || exit $?
fi
echo "$BASE_DIR"
