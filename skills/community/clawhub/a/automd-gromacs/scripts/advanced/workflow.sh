#!/bin/bash
# workflow.sh - 完整工作流自动化 (AI-friendly, token优化)
# 基于 GROMACS 2026.1 完整流程

set -e

# === 参数解析 ===
INPUT=""
OUTPUT="workflow"
FORCEFIELD="amber99sb-ildn"
WATER="tip3p"
TIME=100  # ps (快速测试)

while [[ $# -gt 0 ]]; do
  case $1 in
    --input) INPUT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --forcefield) FORCEFIELD="$2"; shift 2 ;;
    --water) WATER="$2"; shift 2 ;;
    --time) TIME="$2"; shift 2 ;;
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
if [[ -z "$INPUT" ]]; then
  echo "[ERROR-003] 缺少 --input"
  echo "Fix: --input protein.pdb"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR-004] 输入文件不存在: $INPUT"
  exit 1
fi

# === 创建工作目录 ===
WORKDIR="${OUTPUT}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "=== GROMACS 完整工作流 ==="
echo "输入: $INPUT"
echo "工作目录: $WORKDIR"
echo ""

# === 1. 系统准备 ===
echo "→ 1/6 系统准备..."
bash ../scripts/basic/setup.sh \
  --input "../$INPUT" \
  --forcefield "$FORCEFIELD" \
  --water "$WATER" \
  --output setup

if [[ $? -ne 0 ]]; then
  echo "[ERROR-005] 系统准备失败"
  exit 1
fi

# === 2. 能量最小化 ===
echo ""
echo "→ 2/6 能量最小化..."
bash ../scripts/basic/equilibration.sh \
  --input setup_ions.gro \
  --topology topol.top \
  --output em \
  --stage em

if [[ $? -ne 0 ]]; then
  echo "[ERROR-006] 能量最小化失败"
  exit 1
fi

# === 3. NVT 平衡 ===
echo ""
echo "→ 3/6 NVT 平衡..."
bash ../scripts/basic/equilibration.sh \
  --input em.gro \
  --topology topol.top \
  --output nvt \
  --stage nvt

if [[ $? -ne 0 ]]; then
  echo "[ERROR-007] NVT 平衡失败"
  exit 1
fi

# === 4. NPT 平衡 ===
echo ""
echo "→ 4/6 NPT 平衡..."
bash ../scripts/basic/equilibration.sh \
  --input nvt.gro \
  --topology topol.top \
  --output npt \
  --stage npt

if [[ $? -ne 0 ]]; then
  echo "[ERROR-008] NPT 平衡失败"
  exit 1
fi

# === 5. 生产模拟 ===
echo ""
echo "→ 5/6 生产模拟 (${TIME} ps)..."
bash ../scripts/basic/production.sh \
  --input npt.gro \
  --topology topol.top \
  --output md \
  --time "$TIME" \
  --cores 2

if [[ $? -ne 0 ]]; then
  echo "[ERROR-009] 生产模拟失败"
  exit 1
fi

# === 6. 基础分析 ===
echo ""
echo "→ 6/6 基础分析..."
bash ../scripts/basic/analysis.sh \
  --trajectory md.xtc \
  --structure md.tpr \
  --output analysis

if [[ $? -ne 0 ]]; then
  echo "[ERROR-010] 分析失败"
  exit 1
fi

# === 输出结果 ===
echo ""
echo "=== 工作流完成 ==="
echo "工作目录: $WORKDIR"
echo ""
echo "关键文件:"
echo "  setup_ions.gro - 初始系统"
echo "  em.gro - 能量最小化"
echo "  nvt.gro - NVT 平衡"
echo "  npt.gro - NPT 平衡"
echo "  md.xtc - 生产轨迹"
echo "  analysis_*.xvg - 分析结果"
echo ""
echo "✓ 完成"
