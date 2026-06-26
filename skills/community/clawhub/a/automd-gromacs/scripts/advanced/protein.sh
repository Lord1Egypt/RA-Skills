#!/bin/bash
# protein.sh - 蛋白质专用分析 (AI-friendly, token优化)
# 基于 GROMACS 2026.1 Manual Chapter 7.3

set -e

# === 参数解析 ===
TRAJECTORY=""
STRUCTURE=""
OUTPUT="protein"

while [[ $# -gt 0 ]]; do
  case $1 in
    --trajectory) TRAJECTORY="$2"; shift 2 ;;
    --structure) STRUCTURE="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "[ERROR-001] 未知参数: $1"; exit 1 ;;
  esac
done

# === 依赖检查 ===
if ! command -v gmx &>/dev/null; then
  echo "[ERROR-002] gmx 未安装"
  echo "Fix: source /usr/local/gromacs/bin/GMXRC"
  exit 1
fi

# === 输入验证 ===
if [[ -z "$TRAJECTORY" ]]; then
  echo "[ERROR-003] 缺少 --trajectory"
  echo "Fix: --trajectory md.xtc"
  exit 1
fi

if [[ -z "$STRUCTURE" ]]; then
  echo "[ERROR-004] 缺少 --structure"
  echo "Fix: --structure md.tpr"
  exit 1
fi

if [[ ! -f "$TRAJECTORY" ]]; then
  echo "[ERROR-005] 轨迹文件不存在: $TRAJECTORY"
  exit 1
fi

# === 1. 二级结构 (Manual 7.3.5) ===
echo "→ 二级结构分析 (DSSP)..."

if command -v dssp &>/dev/null || command -v mkdssp &>/dev/null; then
  echo "1" | gmx do_dssp -f "$TRAJECTORY" -s "$STRUCTURE" -o dssp.xpm -sc scount.xvg
  
  if [[ $? -ne 0 ]]; then
    echo "[ERROR-006] dssp 失败"
    exit 1
  fi
  
  echo "✓ dssp.xpm, scount.xvg"
else
  echo "⚠ DSSP 未安装，跳过二级结构分析"
  echo "Fix: sudo apt-get install dssp"
fi

# === 2. 溶剂可及表面积 (Manual 7.3.21) ===
echo "→ SASA 分析..."
echo "1" | gmx sasa -f "$TRAJECTORY" -s "$STRUCTURE" -o sasa.xvg -or resarea.xvg

if [[ $? -ne 0 ]]; then
  echo "[ERROR-007] sasa 失败"
  exit 1
fi

echo "✓ sasa.xvg, resarea.xvg"

# === 输出结果 ===
echo ""
echo "=== 蛋白质分析完成 ==="
echo "二级结构: dssp.xpm"
echo "SASA: sasa.xvg"
echo "残基面积: resarea.xvg"
echo ""
echo "✓ 完成"
