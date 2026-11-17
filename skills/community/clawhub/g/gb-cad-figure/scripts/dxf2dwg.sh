#!/usr/bin/env bash
# dxf2dwg.sh — 用 ODA File Converter (AppImage) 将 DXF 批量转换为 DWG
# 依赖: tools/ODAFileConverter.AppImage(Autodesk 官方免费, 自动下载) + 系统 Xvfb
#   无 root 用 --appimage-extract 解压到 /tmp 后经 xvfb-run 运行
# 用法: dxf2dwg.sh <输入dxf文件或目录> <输出目录> [DWG版本: 默认 ACAD2018]
#      版本: ACAD2000/2004/2007/2010/2013/2018/2021 等
# 仅生成 PDF/DXF 时可跳过 DWG；需要 DWG 时本脚本会自动下载 ODA 转换器。
set -e
ODA_IMG=${ODA_IMG:-$(dirname "$0")/tools/ODAFileConverter.AppImage}
ODA_ROOT=${ODA_ROOT:-/tmp/squashfs-root}
ODA="$ODA_ROOT/AppRun"
IN="$1"; OUT="$2"; VER="${3:-ACAD2018}"
# 自动获取/解压 ODA(若尚未就绪)；跳过需 DWG 时先下载
[ -x "$ODA" ] || {
  if [ ! -f "$ODA_IMG" ]; then
    echo "正在自动获取 ODA File Converter(约82MB)..."
    bash "$(dirname "$0")/tools/fetch_oda.sh"
    [ -f "$ODA_IMG" ] || { echo "❌ 未获取到 ODA 转换器, 无法转 DWG(可仅出 PDF/DXF 或手动放置 AppImage)"; exit 1; }
  fi
  echo "正在解压 ODA File Converter..."
  chmod +x "$ODA_IMG"; (cd /tmp && "$ODA_IMG" --appimage-extract >/dev/null 2>&1)
}
[ -d "$OUT" ] || mkdir -p "$OUT"
if [ -f "$IN" ]; then
  tmpi="$OUT/.dxfin"; rm -rf "$tmpi"; mkdir -p "$tmpi"; cp "$IN" "$tmpi/"
  xvfb-run -a "$ODA" "$tmpi" "$OUT" "$VER" DWG 0 1 "*.dxf"
  rm -rf "$tmpi"
else
  [ -d "$IN" ] || { echo "输入不存在: $IN"; exit 1; }
  xvfb-run -a "$ODA" "$IN" "$OUT" "$VER" DWG 0 1 "*.dxf"
fi
echo "DWG生成完成:"
ls "$OUT"/*.dwg 2>/dev/null | while read f; do echo "  $(basename "$f")"; done
