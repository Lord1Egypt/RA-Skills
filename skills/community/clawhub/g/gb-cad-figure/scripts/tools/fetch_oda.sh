#!/usr/bin/env bash
# fetch_oda.sh — 下载 ODA File Converter AppImage(Autodesk 官方免费转换器, 约82MB) 到本目录
# 用于 DXF→DWG 转换；自动被 dxf2dwg.sh 调用，也可单独运行。
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$DIR/ODAFileConverter.AppImage"
URL="https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_lnxX64_8.3dll_27.1.AppImage"
if [ -f "$OUT" ]; then
  echo "ODA File Converter 已存在: $OUT"
  exit 0
fi
echo "下载 ODA File Converter (约82MB) ..."
if curl -fSL "$URL" -o "$OUT" 2>/dev/null; then
  chmod +x "$OUT"
  echo "完成: $OUT"
else
  rm -f "$OUT"
  echo "❌ 自动下载失败，请手动获取并放入本目录:"
  echo "   https://www.opendesign.com/guestfiles/oda_file_converter"
  exit 1
fi
