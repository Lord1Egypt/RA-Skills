#!/bin/bash
# 下载并校验 CMG 扫描器发布包。
#
# 用法:
#   fetch_scanner.sh <文件名> [目标目录]
#
# 示例:
#   fetch_scanner.sh aliyun-scanner-mac-arm64-1.0.0.tar.gz
#   fetch_scanner.sh aws-scanner-linux-1.0.0.tar.gz ./download
#
# 行为:
#   1. 通过 HTTPS 下载到临时文件
#   2. 计算 SHA-256，与 references/CHECKSUMS.md 中记录的值比对
#   3. 校验通过才移动到目标目录；失败则删除临时文件并以非零码退出
#
# 这是 fail-closed 的：校验和缺失或不匹配都会拒绝落地文件，不会"下载了再说"。

set -euo pipefail

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1" >&2; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

BASE="https://msp-release-1258344699.cos.ap-shanghai.myqcloud.com/package/urp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKSUMS="$SCRIPT_DIR/../references/CHECKSUMS.md"

FILE="${1:-}"
DEST="${2:-.}"

if [ -z "$FILE" ]; then
  fail "用法: $0 <文件名> [目标目录]"
  echo "  可用产物见: references/CHECKSUMS.md"
  exit 2
fi

if [ ! -f "$CHECKSUMS" ]; then
  fail "找不到校验和清单: $CHECKSUMS"
  echo "  没有校验和就无法验证产物完整性，已中止。"
  exit 2
fi

# 从 CHECKSUMS.md 的表格中取出该文件对应的 64 位十六进制校验和。
EXPECTED=$(grep -F "\`$FILE\`" "$CHECKSUMS" \
  | grep -oE '[0-9a-f]{64}' \
  | head -1 || true)

if [ -z "$EXPECTED" ]; then
  fail "清单中没有 $FILE 的校验和"
  echo ""
  echo "  可能原因："
  echo "    - 文件名拼写有误"
  echo "    - 该产物已知不可用（见 CHECKSUMS.md「已知不可用的产物」一节）"
  echo "    - 上游发布了新版本但清单未同步更新"
  echo ""
  echo "  在校验和确认之前不要下载执行该产物。"
  exit 1
fi

mkdir -p "$DEST"
TMP=$(mktemp "${TMPDIR:-/tmp}/cmg-scanner.XXXXXX")
cleanup() { rm -f "$TMP"; }
trap cleanup EXIT

echo "下载 $FILE ..."
if ! curl -fSL --proto '=https' --tlsv1.2 --max-time 900 "$BASE/$FILE" -o "$TMP"; then
  fail "下载失败: $BASE/$FILE"
  exit 1
fi

if command -v sha256sum &>/dev/null; then
  ACTUAL=$(sha256sum "$TMP" | cut -d' ' -f1)
else
  ACTUAL=$(shasum -a 256 "$TMP" | cut -d' ' -f1)
fi

if [ "$ACTUAL" != "$EXPECTED" ]; then
  fail "校验和不匹配 — 已丢弃下载内容"
  echo "  期望: $EXPECTED"
  echo "  实际: $ACTUAL"
  echo ""
  echo "  产物可能已被替换、损坏，或链路遭到篡改。不要执行该文件。"
  echo "  请向维护者确认后再重试。"
  exit 1
fi

ok "校验和匹配: $ACTUAL"
mv "$TMP" "$DEST/$FILE"
trap - EXIT
ok "已保存到 $DEST/$FILE"
echo ""
echo "解压："
case "$FILE" in
  *.tar.gz) echo "  tar -xzf $DEST/$FILE" ;;
  *.zip)    echo "  unzip $DEST/$FILE" ;;
esac
