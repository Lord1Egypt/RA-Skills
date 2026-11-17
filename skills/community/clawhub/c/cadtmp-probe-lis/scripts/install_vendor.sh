#!/usr/bin/env bash
# 为 SkillHub 轻量包补齐 vendor 依赖：
#   默认：未配置 CAD_FILE_READER_REPO 时，自动用公共 PyPI 装到本包 vendor/（不依赖个人 Release 仓库）。
#   可覆盖：设置 CAD_FILE_READER_REPO=<owner>/<repo> 时，优先用 GitHub Release 完整包（SHA-256 校验），
#   失败仍回退公共 PyPI。
set -euo pipefail
QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1
say() { [ "$QUIET" = 0 ] && echo "$*"; }

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SkillHub 下载包可能丢失可执行位，先补回（安装/自举后用一条命令即可，幂等）
if [ -d "$SKILL_DIR/scripts" ]; then
  find "$SKILL_DIR/scripts" -maxdepth 1 -type f -name '*.sh' -exec chmod +x {} + 2>/dev/null || true
fi
MANIFEST="$SKILL_DIR/manifest.json"
PKG_VER="$(sed -n 's/.*"version"[ ]*:[ ]*"\([^"]*\)".*/\1/p' "$MANIFEST" 2>/dev/null | head -1)"
WANT="${CAD_FILE_READER_VERSION:-${PKG_VER:-0.28.5}}"

# 找 python3（优先 Codex 运行时，其次系统 python）
PYTHON_BIN=""
for c in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then PYTHON_BIN="$c"; break; fi
done

_DEST="$SKILL_DIR/vendor"
_unpacked_ok() {
  [ -d "$_DEST/ezdwg" ] && \
  [ -d "$_DEST/ezdxf" ] && \
  [ -f "$_DEST/ezdxf/__init__.py" ] && \
  [ -d "$_DEST/fontTools" ]
}

# 幂等预检：vendor 已存在 -> 直接退出
if _unpacked_ok && [ "${CAD_FORCE_INSTALL:-0}" != "1" ]; then
  say "vendor 已存在，未变更（如需强制重装：export CAD_FORCE_INSTALL=1）"
  exit 0
fi
if [ -d "$_DEST" ]; then find "$_DEST" -depth -delete; fi

pip_fallback() {
  say "改用公共 PyPI 自动补齐 vendor（不读取个人 Release 仓库，联网安装）……" 2>&1
  if [ -z "$PYTHON_BIN" ]; then
    echo "❌ 未找到 python3，无法用 pip 安装 vendor。" >&2
    return 1
  fi
  "$PYTHON_BIN" -m pip install --disable-pip-version-check --no-input --quiet --target "$_DEST" \
    "ezdwg==0.12.6" "ezdxf==1.4.4" fonttools pyparsing numpy || return 1
  if _unpacked_ok; then
    echo "vendor 已安装到 $_DEST（公共 PyPI）"
    return 0
  fi
  echo "vendor 安装后校验未通过，请手动检查：$_DEST" >&2
  return 1
}

REPO="${CAD_FILE_READER_REPO:-}"

install_via_release() {
  local SHA_BIN
  SHA_BIN="$(command -v shasum || command -v sha256sum || true)"
  [ -n "$SHA_BIN" ] || { echo "缺少 sha256sum/shasum 校验工具，无法从 Release 校验完整包" >&2; return 1; }
  calc_sha256() {
    if [ "${SHA_BIN##*/}" = "shasum" ]; then "$SHA_BIN" -a 256 "$1" | awk '{print $1}'
    else "$SHA_BIN" "$1" | awk '{print $1}'; fi
  }
  local TMP
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' RETURN

  verify_download() {
    local v="$1"
    local exp actual
    for u in \
      "https://github.com/${REPO}/releases/download/v${v}/SHA256SUMS-cad-file-reader-${v}.txt" \
      "https://github.com/${REPO}/releases/download/v${v}/SHA256SUMS.txt"; do
      if curl -sL --http1.1 --fail --max-time "${CAD_DOWNLOAD_TIMEOUT:-600}" "$u" -o "$TMP/sums.txt"; then
        exp="$(grep -E "cad-file-reader-full-${v}\.zip[[:space:]]*$|cad-file-reader-full-${v}\.zip$" "$TMP/sums.txt" | awk '{print $1}' | head -1)"
        if [ -z "$exp" ] && [ "$v" != "0.28.5" ]; then
          exp="$(grep -E "full-${v}\.zip" "$TMP/sums.txt" | awk '{print $1}' | head -1)"
        fi
        if [ -n "$exp" ]; then
          actual="$(calc_sha256 "$TMP/full.zip")"
          if [ "$actual" = "$exp" ]; then
            say "SHA-256 校验通过 ✓ ($v)" >&2
            return 0
          fi
          say "SHA-256 校验失败，拒绝使用下载包 ($v)" >&2
          return 1
        fi
        say "校验文件里缺少 $v 的完整包条目，改用下一命名…" >&2
      fi
    done
    say "未取得 $v 的校验文件，为安全起见不执行未校验下载包。" >&2
    return 1
  }

  fetch() {
    local v="$1"
    local url
    for url in \
      "https://github.com/${REPO}/releases/download/v${v}/cad-file-reader-full-${v}.zip" \
      "https://github.com/${REPO}/releases/download/v${v}/cad-file-reader-${v}-full.zip"; do
      say "尝试 $url" >&2
      if curl -sL --http1.1 --fail --max-time "${CAD_DOWNLOAD_TIMEOUT:-600}" "$url" -o "$TMP/full.zip"; then
        if verify_download "$v"; then
          if unzip -oq "$TMP/full.zip" "*/vendor/*" -d "$TMP" 2>/dev/null \
             && { [ -d "$TMP/cad-file-reader/vendor" ] || [ -n "$(find "$TMP" -type d -name vendor -print -quit)" ]; }; then
            return 0
          fi
          say "解压后未找到 vendor，继续尝试下一个命名…" >&2
        fi
      fi
    done
    return 1
  }

  local FALLBACKS
  FALLBACKS=("$WANT" 0.28.18 0.28.17 0.28.16 0.28.15 0.28.14 0.28.8 0.28.5 0.28.1 0.28.0 0.27.0 0.26.6 0.26.4 0.26.0 0.25.0)
  local INSTALLED_V="" v
  for v in "${FALLBACKS[@]}"; do
    if fetch "$v"; then INSTALLED_V="$v"; break; fi
  done
  if [ -n "$INSTALLED_V" ]; then
    if [ "$INSTALLED_V" != "$WANT" ]; then
      say "当前包版本 v${WANT} 未发布完整包，已回退用 v${INSTALLED_V} 的完整包补齐 vendor（依赖兼容）" >&2
    fi
    local SRC DEST
    DEST="$SKILL_DIR/vendor"
    if [ -d "$DEST" ]; then find "$DEST" -depth -delete; fi
    SRC="$(find "$TMP" -type d -name vendor -print -quit)"
    cp -R "$SRC" "$DEST"
    echo "vendor 已安装到 $DEST（Release $INSTALLED_V）"
    echo "许可证与第三方依赖清单见 NOTICE.md（MIT/BSD）"
    return 0
  fi
  say "GitHub Release 方式不可用，尝试回退公共 PyPI……" >&2
  return 1
}

if [ -z "$REPO" ]; then
  # 未配置 Release 仓库：直接默认 pip，恢复"零配置可用"
  pip_fallback || {
    err=$?
    cat >&2 <<'MSG'
未自动补齐 vendor。请手动执行：
  python3 -m pip install --target <skill>/vendor "ezdwg==0.12.6" "ezdxf==1.4.4" fonttools pyparsing numpy
然后重试；或设置 CAD_FILE_READER_REPO 指向带 SHA256SUMS 的 Release 仓库。
MSG
    exit $err
  }
  exit 0
fi

# 已配置 Release 仓库：优先 GitHub 校验下载，失败回退 PyPI
if ! install_via_release; then
  pip_fallback || {
    err=$?
    echo "❌ GitHub Release 与公共 PyPI 均未能补齐 vendor。" >&2
    exit $err
  }
fi
exit 0
