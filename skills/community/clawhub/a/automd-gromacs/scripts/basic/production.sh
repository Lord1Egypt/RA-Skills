#!/bin/bash
# production.sh - 生产MD模拟 (AI-friendly, token优化)
# 基于 GROMACS 2026.1 Manual Chapter 3.3

set -e

# === 参数解析 ===
INPUT=""
TOPOLOGY=""
OUTPUT="md"
TIME=1000  # ps
CORES=2
CHECKPOINT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --input) INPUT="$2"; shift 2 ;;
    --topology) TOPOLOGY="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --time) TIME="$2"; shift 2 ;;
    --cores) CORES="$2"; shift 2 ;;
    --checkpoint) CHECKPOINT="$2"; shift 2 ;;
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
  echo "Fix: --input npt.gro"
  exit 1
fi

if [[ -z "$TOPOLOGY" ]]; then
  echo "[ERROR-004] 缺少 --topology"
  echo "Fix: --topology topol.top"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR-005] 输入文件不存在: $INPUT"
  exit 1
fi

if [[ ! -f "$TOPOLOGY" ]]; then
  echo "[ERROR-006] 拓扑文件不存在: $TOPOLOGY"
  exit 1
fi

# === 生成 MDP (Manual 3.3.3: 生产模拟参数) ===
cat > ${OUTPUT}.mdp << 'EOF'
; 生产MD - GROMACS 2026.1 标准参数
integrator = md
dt = 0.002          ; 2 fs (Manual 3.3.3: 标准时间步长)
nsteps = NSTEPS_PLACEHOLDER

; 输出控制
nstxout = 0         ; 不输出坐标 (省空间)
nstvout = 0
nstfout = 0
nstlog = 5000       ; 每10ps记录
nstenergy = 5000
nstxout-compressed = 5000  ; 每10ps保存压缩轨迹

; 键约束 (Manual 3.4.4: LINCS算法)
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4

; 温度耦合 (Manual 3.4.5: V-rescale恒温器)
tcoupl = V-rescale
tc-grps = Protein Non-Protein
tau-t = 0.1 0.1
ref-t = 300 300

; 压力耦合 (Manual 3.4.6: Parrinello-Rahman)
pcoupl = Parrinello-Rahman
pcoupltype = isotropic
tau-p = 2.0         ; 2 ps (标准值)
ref-p = 1.0
compressibility = 4.5e-5

; 静电 (Manual 3.4.7: PME)
coulombtype = PME
rcoulomb = 1.2      ; 1.2 nm (2.0最佳实践)
pme-order = 4
fourierspacing = 0.12

; 范德华 (Manual 3.4.8)
vdwtype = Cut-off
rvdw = 1.2          ; 1.2 nm
DispCorr = EnerPres ; 长程修正

; PBC
pbc = xyz
EOF

# 替换步数
NSTEPS=$((TIME * 500))  # 2fs时间步长
sed -i "s/NSTEPS_PLACEHOLDER/$NSTEPS/" ${OUTPUT}.mdp

echo "✓ 生成 ${OUTPUT}.mdp (${TIME} ps, ${NSTEPS} steps)"

# === 预处理 ===
echo "→ grompp..."
gmx grompp -f ${OUTPUT}.mdp -c "$INPUT" -p "$TOPOLOGY" -o ${OUTPUT}.tpr -maxwarn 1 &>/dev/null

if [[ $? -ne 0 ]]; then
  echo "[ERROR-007] grompp 失败"
  echo "Fix: 检查 MDP 参数或拓扑文件"
  gmx grompp -f ${OUTPUT}.mdp -c "$INPUT" -p "$TOPOLOGY" -o ${OUTPUT}.tpr
  exit 1
fi

echo "✓ ${OUTPUT}.tpr"

# === 运行模拟 ===
echo "→ mdrun (${TIME} ps, ${CORES} cores)..."

if [[ -n "$CHECKPOINT" && -f "$CHECKPOINT" ]]; then
  echo "  从检查点恢复: $CHECKPOINT"
  gmx mdrun -v -deffnm ${OUTPUT} -cpi "$CHECKPOINT" -nt $CORES
else
  gmx mdrun -v -deffnm ${OUTPUT} -nt $CORES
fi

if [[ $? -ne 0 ]]; then
  echo "[ERROR-008] mdrun 失败"
  echo "Fix: 检查系统稳定性或减少时间步长"
  exit 1
fi

# === 验证输出 ===
if [[ ! -f "${OUTPUT}.xtc" ]]; then
  echo "[ERROR-009] 轨迹文件未生成"
  exit 1
fi

if [[ ! -f "${OUTPUT}.edr" ]]; then
  echo "[ERROR-010] 能量文件未生成"
  exit 1
fi

# === 快速分析 ===
echo "→ 快速分析..."

# 温度
echo "1 0" | gmx energy -f ${OUTPUT}.edr -o ${OUTPUT}_temp.xvg &>/dev/null
TEMP_AVG=$(awk '/^[^#@]/ {sum+=$2; n++} END {printf "%.1f", sum/n}' ${OUTPUT}_temp.xvg)

# 压力
echo "2 0" | gmx energy -f ${OUTPUT}.edr -o ${OUTPUT}_press.xvg &>/dev/null
PRESS_AVG=$(awk '/^[^#@]/ {sum+=$2; n++} END {printf "%.1f", sum/n}' ${OUTPUT}_press.xvg)

# 势能
echo "3 0" | gmx energy -f ${OUTPUT}.edr -o ${OUTPUT}_pot.xvg &>/dev/null
POT_AVG=$(awk '/^[^#@]/ {sum+=$2; n++} END {printf "%.0f", sum/n}' ${OUTPUT}_pot.xvg)

# === 输出结果 ===
echo ""
echo "=== 生产模拟完成 ==="
echo "时间: ${TIME} ps"
echo "温度: ${TEMP_AVG} K (目标 300 K)"
echo "压力: ${PRESS_AVG} bar (目标 1 bar)"
echo "势能: ${POT_AVG} kJ/mol"
echo ""
echo "输出文件:"
echo "  ${OUTPUT}.xtc  - 轨迹 (压缩)"
echo "  ${OUTPUT}.edr  - 能量"
echo "  ${OUTPUT}.log  - 日志"
echo "  ${OUTPUT}.cpt  - 检查点 (可恢复)"
echo ""

# 性能统计
if [[ -f "${OUTPUT}.log" ]]; then
  PERF=$(grep "Performance:" ${OUTPUT}.log | tail -1 | awk '{print $2}')
  echo "性能: ${PERF} ns/day"
fi

echo "✓ 完成"
