#!/bin/bash
# pca.sh - 主成分分析 (AI-friendly, token优化)
# 基于 GROMACS 2026.1 Manual Chapter 5.7

set -e

# === 参数解析 ===
TRAJECTORY=""
STRUCTURE=""
OUTPUT="pca"

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

# === 1. 协方差矩阵 (Manual 7.3.4) ===
echo "→ 计算协方差矩阵..."
echo "3" | gmx covar -f "$TRAJECTORY" -s "$STRUCTURE" -o eigenval.xvg -v eigenvec.trr

if [[ $? -ne 0 ]]; then
  echo "[ERROR-006] covar 失败"
  exit 1
fi

echo "✓ eigenval.xvg, eigenvec.trr"

# === 2. 特征分析 (Manual 7.3.1) ===
echo "→ 特征分析..."
echo "3" | gmx anaeig -f "$TRAJECTORY" -s "$STRUCTURE" -v eigenvec.trr -eig eigenval.xvg -2d 2dproj.xvg -first 1 -last 2

if [[ $? -ne 0 ]]; then
  echo "[ERROR-007] anaeig 失败"
  exit 1
fi

echo "✓ 2dproj.xvg"

# === 3. 极端构象 ===
echo "→ 提取极端构象..."
echo "3" | gmx anaeig -f "$TRAJECTORY" -s "$STRUCTURE" -v eigenvec.trr -eig eigenval.xvg -extr extreme.pdb -first 1 -last 1 -nframes 10

if [[ $? -ne 0 ]]; then
  echo "[ERROR-008] 极端构象提取失败"
  exit 1
fi

echo "✓ extreme.pdb"

# === 输出结果 ===
echo ""
echo "=== PCA 完成 ==="
echo "特征值: eigenval.xvg"
echo "特征向量: eigenvec.trr"
echo "2D投影: 2dproj.xvg"
echo "极端构象: extreme.pdb"
echo ""
echo "✓ 完成"
