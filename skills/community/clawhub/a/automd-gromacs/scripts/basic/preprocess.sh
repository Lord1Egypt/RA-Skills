#!/bin/bash
# preprocess.sh - GROMACS预处理(grompp) (AI-friendly, token优化)
# 基于 GROMACS 2026.1 Manual Chapter 7.3.8

set -e

# === 参数解析 ===
MDP=""
COORD=""
TOPOLOGY=""
OUTPUT="output"
MAXWARN=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --mdp) MDP="$2"; shift 2 ;;
    --coord) COORD="$2"; shift 2 ;;
    --topology) TOPOLOGY="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --maxwarn) MAXWARN="$2"; shift 2 ;;
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
if [[ -z "$MDP" ]]; then
  echo "[ERROR-003] 缺少 --mdp"
  echo "Fix: --mdp em.mdp"
  exit 1
fi

if [[ -z "$COORD" ]]; then
  echo "[ERROR-004] 缺少 --coord"
  echo "Fix: --coord protein.gro"
  exit 1
fi

if [[ -z "$TOPOLOGY" ]]; then
  TOPOLOGY="topol.top"  # 默认拓扑
fi

if [[ ! -f "$MDP" ]]; then
  echo "[ERROR-005] MDP文件不存在: $MDP"
  exit 1
fi

if [[ ! -f "$COORD" ]]; then
  echo "[ERROR-006] 坐标文件不存在: $COORD"
  exit 1
fi

if [[ ! -f "$TOPOLOGY" ]]; then
  echo "[ERROR-007] 拓扑文件不存在: $TOPOLOGY"
  exit 1
fi

# === 运行 grompp ===
echo "→ grompp..."
echo "  MDP: $MDP"
echo "  坐标: $COORD"
echo "  拓扑: $TOPOLOGY"
echo "  输出: ${OUTPUT}.tpr"

gmx grompp -f "$MDP" -c "$COORD" -p "$TOPOLOGY" -o "${OUTPUT}.tpr" -maxwarn $MAXWARN 2>&1 | tee grompp.log

if [[ $? -ne 0 ]]; then
  echo ""
  echo "[ERROR-008] grompp 失败"
  echo "Fix: 检查 grompp.log"
  
  # 常见错误提示
  if grep -q "number of coordinates" grompp.log; then
    echo "  → 原子数不匹配 (坐标 vs 拓扑)"
  fi
  
  if grep -q "Unknown left-hand" grompp.log; then
    echo "  → MDP 参数错误"
  fi
  
  if grep -q "Too many warnings" grompp.log; then
    echo "  → 警告过多，使用 --maxwarn 1"
  fi
  
  exit 1
fi

# === 验证输出 ===
if [[ ! -f "${OUTPUT}.tpr" ]]; then
  echo "[ERROR-009] TPR文件未生成"
  exit 1
fi

# === 输出结果 ===
echo ""
echo "=== 预处理完成 ==="
echo "输出: ${OUTPUT}.tpr"

# 显示 TPR 信息
echo ""
echo "TPR 信息:"
gmx dump -s "${OUTPUT}.tpr" 2>/dev/null | grep -E "natoms|nsteps|dt|ref-t|ref-p" | head -10

echo ""
echo "✓ 完成"
