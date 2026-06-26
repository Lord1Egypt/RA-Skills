#!/bin/bash
#
# GROMACS 系统准备脚本
# 功能: 从 PDB 到可模拟系统
# 流程: pdb2gmx → editconf → solvate → genion → 能量最小化
#
# 使用: ./setup.sh --input protein.pdb --output ./system --forcefield amber99sb-ildn
#

set -e

# ============================================
# 参数解析
# ============================================
INPUT=""
OUTPUT="./system"
FORCEFIELD="amber99sb-ildn"
WATER="tip3p"
BOX_TYPE="cubic"
BOX_DISTANCE=1.0  # nm
NEUTRALIZE="yes"
ION_CONCENTRATION=0.15  # mol/L (生理盐浓度)

while [[ $# -gt 0 ]]; do
    case $1 in
        --input)
            INPUT="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --forcefield)
            FORCEFIELD="$2"
            shift 2
            ;;
        --water)
            WATER="$2"
            shift 2
            ;;
        --box-type)
            BOX_TYPE="$2"
            shift 2
            ;;
        --box-distance)
            BOX_DISTANCE="$2"
            shift 2
            ;;
        --ion-conc)
            ION_CONCENTRATION="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$INPUT" ]; then
    echo "ERROR: Missing required parameter --input"
    echo "Usage: $0 --input <pdb> --output <dir> [options]"
    exit 1
fi

# ============================================
# 自动修复函数
# ============================================

# 力场选择自动化 (Manual 3.6)
select_forcefield() {
    local input_file="$1"
    
    # 检测蛋白质类型
    if grep -q "DNA\|RNA" "$input_file"; then
        echo "amber99sb-ildn"  # 核酸
    elif grep -q "POPC\|DPPC\|POPE" "$input_file"; then
        echo "charmm36"  # 膜蛋白
    else
        echo "amber99sb-ildn"  # 默认蛋白质
    fi
}

# 盒子尺寸自动调整 (Manual 3.3)
adjust_box_size() {
    local box_type="$1"
    local distance="$2"
    
    # 推荐: 1.0 nm (最小)
    # 拉力模拟: 1.5-2.0 nm
    # 大分子: 1.2-1.5 nm
    
    if [ "$(echo "$distance" | awk "{if($1<1.0)print 1}")" = "1" ]; then
        echo "[AUTO-FIX] Box distance too small ($distance nm), adjusting to 1.0 nm"
        echo "1.0"
    else
        echo "$distance"
    fi
}

# ============================================
# 环境检查
# ============================================
echo "============================================"
echo "GROMACS 系统准备"
echo "============================================"
echo ""
echo "[0/6] 环境检查..."

if ! command -v gmx &> /dev/null; then
    echo "[ERROR-001] gmx 未找到"
    echo "Fix: conda install -c conda-forge gromacs"
    echo "Or: sudo apt install gromacs"
    echo "Manual: Chapter 2.1"
    exit 1
fi

if [ ! -f "$INPUT" ]; then
    echo "[ERROR-002] Input file not found: $INPUT"
    echo "Fix: Check file path"
    exit 1
fi

# 自动调整力场
if [ "$FORCEFIELD" = "auto" ]; then
    FORCEFIELD=$(select_forcefield "$INPUT")
    echo "[AUTO-FIX] Detected forcefield: $FORCEFIELD"
fi

# 自动调整盒子尺寸
BOX_DISTANCE=$(adjust_box_size "$BOX_TYPE" "$BOX_DISTANCE")

mkdir -p "$OUTPUT"/logs
cd "$OUTPUT"

echo "✅ Environment OK"
echo "   Input: $INPUT"
echo "   Forcefield: $FORCEFIELD"
echo "   Water: $WATER"
echo ""

# ============================================
# 知识内嵌: 力场 & 水模型 (Manual 3.6)
# ============================================
# 力场:
# amber99sb-ildn: 蛋白质 (推荐)
# charmm36: 膜蛋白 / 脂质
# gromos54a7: 小分子
# oplsaa: 有机分子
#
# 水模型:
# tip3p: 快速, amber 配套
# tip4p: 精确, 密度好
# spc/e: 通用
#
# 盒子类型 (Manual 3.3):
# cubic: 简单, 浪费空间
# dodecahedron: 省 ~29% 空间
# octahedron: 省 ~27% 空间
#
# 盒子边距 (Manual 3.3):
# 推荐: 1.0 nm (最小)
# 拉力: 1.5-2.0 nm
# 大分子: 1.2-1.5 nm

# ============================================
# Step 1: pdb2gmx - 生成拓扑
# ============================================
echo "[1/6] 生成拓扑 (pdb2gmx)..."

# 力场映射
case $FORCEFIELD in
    amber99sb-ildn)
        FF_NUM=8
        ;;
    amber14sb)
        FF_NUM=1
        ;;
    charmm27)
        FF_NUM=5
        ;;
    charmm36)
        FF_NUM=6
        ;;
    gromos54a7)
        FF_NUM=14
        ;;
    *)
        echo "[ERROR-003] Unknown forcefield: $FORCEFIELD"
        echo "Fix: Use amber99sb-ildn, charmm36, or gromos54a7"
        echo "Manual: Chapter 3.6"
        exit 1
        ;;
esac

# 水模型映射
case $WATER in
    tip3p)
        WATER_NUM=1
        ;;
    tip4p)
        WATER_NUM=2
        ;;
    spc)
        WATER_NUM=3
        ;;
    spce)
        WATER_NUM=4
        ;;
    *)
        echo "[ERROR-004] Unknown water model: $WATER"
        echo "Fix: Use tip3p, tip4p, or spce"
        exit 1
        ;;
esac

# 执行 pdb2gmx
echo "$FF_NUM" | gmx pdb2gmx \
    -f "../$INPUT" \
    -o protein.gro \
    -p topol.top \
    -ignh \
    -water $WATER \
    > logs/pdb2gmx.log 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR-005] pdb2gmx failed"
    echo "Fix: Check PDB format or use pdb4amber to clean"
    echo "Or: gmx pdb2gmx -f input.pdb -o out.gro -p topol.top -ignh"
    echo "Manual: Chapter 3.2"
    echo "Log: logs/pdb2gmx.log"
    exit 1
fi

# 检查输出
NATOMS=$(grep "^ATOM" protein.gro | wc -l)
echo "✅ Topology generated"
echo "   Atoms: $NATOMS"
echo ""

# ============================================
# Step 2: editconf - 定义盒子
# ============================================
echo "[2/6] 定义盒子 (editconf)..."

gmx editconf \
    -f protein.gro \
    -o box.gro \
    -c \
    -d $BOX_DISTANCE \
    -bt $BOX_TYPE \
    > logs/editconf.log 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR-006] editconf failed"
    echo "Fix: Check structure or adjust box parameters"
    echo "Manual: Chapter 3.3"
    exit 1
fi

# 提取盒子尺寸
BOX_SIZE=$(tail -1 box.gro | awk '{print $1}')
echo "✅ Box defined"
echo "   Type: $BOX_TYPE"
echo "   Size: $BOX_SIZE nm"
echo ""

# ============================================
# Step 3: solvate - 溶剂化
# ============================================
echo "[3/6] 溶剂化 (solvate)..."

# 选择溶剂模型
case $WATER in
    tip3p|tip4p)
        SOLVENT="spc216.gro"
        ;;
    spc|spce)
        SOLVENT="spc216.gro"
        ;;
esac

gmx solvate \
    -cp box.gro \
    -cs $SOLVENT \
    -o solv.gro \
    -p topol.top \
    > logs/solvate.log 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR-007] solvate failed"
    echo "Fix: Check box size or water model"
    echo "Manual: Chapter 3.3"
    exit 1
fi

# 统计水分子数
NWATER=$(grep "SOL" topol.top | tail -1 | awk '{print $2}')
TOTAL_ATOMS=$(grep "^ATOM" solv.gro | wc -l)
echo "✅ System solvated"
echo "   Water molecules: $NWATER"
echo "   Total atoms: $TOTAL_ATOMS"
echo ""

# ============================================
# Step 4: genion - 添加离子
# ============================================
echo "[4/6] 添加离子 (genion)..."

# 创建简单的 MDP 用于 grompp
cat > ions.mdp << 'EOF'
integrator  = steep
emtol       = 1000.0
nsteps      = 50000
nstlist     = 1
cutoff-scheme = Verlet
coulombtype = cutoff
rcoulomb    = 1.0
rvdw        = 1.0
pbc         = xyz
EOF

gmx grompp \
    -f ions.mdp \
    -c solv.gro \
    -p topol.top \
    -o ions.tpr \
    -maxwarn 1 \
    > logs/grompp_ions.log 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR-008] grompp for ions failed"
    echo "Fix: Check topology or MDP parameters"
    echo "Manual: Chapter 3.4"
    exit 1
fi

# 添加离子
if [ "$NEUTRALIZE" = "yes" ]; then
    echo "SOL" | gmx genion \
        -s ions.tpr \
        -o system.gro \
        -p topol.top \
        -pname NA \
        -nname CL \
        -neutral \
        -conc $ION_CONCENTRATION \
        > logs/genion.log 2>&1
else
    echo "SOL" | gmx genion \
        -s ions.tpr \
        -o system.gro \
        -p topol.top \
        -pname NA \
        -nname CL \
        -conc $ION_CONCENTRATION \
        > logs/genion.log 2>&1
fi

if [ $? -ne 0 ]; then
    echo "[ERROR-009] genion failed"
    echo "Fix: Check ion concentration or topology"
    echo "Manual: Chapter 3.4"
    exit 1
fi

# 统计离子数
NNA=$(grep "^NA" topol.top | tail -1 | awk '{print $2}')
NCL=$(grep "^CL" topol.top | tail -1 | awk '{print $2}')
echo "✅ Ions added"
echo "   Na+: $NNA"
echo "   Cl-: $NCL"
echo "   Concentration: $ION_CONCENTRATION M"
echo ""

# ============================================
# Step 5: 能量最小化
# ============================================
echo "[5/6] 能量最小化 (mdrun)..."

# 知识内嵌: EM 参数 (Manual 5.4)
# emtol: 1000 kJ/mol/nm (标准)
# nsteps: 50000 (通常足够)
# emstep: 0.01 nm (初始步长)

cat > em.mdp << 'EOF'
; EM 参数
integrator  = steep
emtol       = 1000.0
emstep      = 0.01
nsteps      = 50000

; 输出控制
nstlog      = 100
nstenergy   = 100

; 邻居搜索
nstlist         = 1
cutoff-scheme   = Verlet
ns_type         = grid
pbc             = xyz

; 静电
coulombtype     = PME
rcoulomb        = 1.0
fourierspacing  = 0.12

; 范德华
rvdw            = 1.0
vdw-type        = Cut-off
EOF

gmx grompp \
    -f em.mdp \
    -c system.gro \
    -p topol.top \
    -o em.tpr \
    > logs/grompp_em.log 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR-010] grompp for EM failed"
    echo "Fix: Check MDP or topology"
    echo "Manual: Chapter 5.4"
    exit 1
fi

gmx mdrun \
    -v \
    -deffnm em \
    > logs/mdrun_em.log 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR-011] Energy minimization failed"
    echo "Fix: Check system or extend nsteps"
    echo "Manual: Chapter 5.4"
    exit 1
fi

# 检查收敛: Fmax < 1000 kJ/mol/nm
# 未收敛 → 延长 nsteps
check_em_convergence() {
    if [ -f em.log ]; then
        local max_force=$(grep "Maximum force" em.log | tail -1 | awk '{print $4}')
        if [ -n "$max_force" ]; then
            if (( $(echo "$max_force > 1000" | bc -l) )); then
                echo "[WARN] EM 未收敛 (Fmax=$max_force)"
                echo "[AUTO-FIX] 考虑延长 nsteps → 100000"
                return 1
            fi
        fi
    fi
    return 0
}

FINAL_ENERGY=$(echo "10 0" | gmx energy -f em.edr 2>&1 | grep "Potential" | tail -1 | awk '{print $2}')
CONVERGED=$(grep "converged to Fmax" em.log | wc -l)

echo "✅ 能量最小化完成"
echo "   最终势能: $FINAL_ENERGY kJ/mol"
if [ $CONVERGED -gt 0 ]; then
    echo "   状态: 已收敛 ✅"
else
    echo "   状态: 未收敛 (可能需要更多步数)"
    check_em_convergence
fi
echo ""

# ============================================
# Step 6: 生成报告
# ============================================
echo "[6/6] 生成报告..."

cat > REPORT.md << EOF
# 系统准备报告

## 输入
- PDB 文件: $INPUT
- 力场: $FORCEFIELD
- 水模型: $WATER

## 系统组成
- 蛋白质原子: $NATOMS
- 水分子: $NWATER
- Na+ 离子: $NNA
- Cl- 离子: $NCL
- 总原子数: $TOTAL_ATOMS

## 盒子
- 类型: $BOX_TYPE
- 尺寸: $BOX_SIZE nm
- 距离: $BOX_DISTANCE nm

## 能量最小化
- 最终势能: $FINAL_ENERGY kJ/mol
- 收敛状态: $([ $CONVERGED -gt 0 ] && echo "已收敛" || echo "未完全收敛")

## 输出文件
- 系统坐标: system.gro
- 拓扑文件: topol.top
- 能量最小化: em.gro, em.edr
- 运行输入: em.tpr

## 下一步
系统已准备好进行平衡模拟:
\`\`\`bash
# 使用 equilibration.sh
./equilibration.sh --input em.gro --topology topol.top --output ./equilibration
\`\`\`

## 质量检查
- [ ] 检查势能是否为负值
- [ ] 检查是否有 LINCS 警告
- [ ] 可视化检查系统 (pymol system.gro)

---
生成时间: $(date)
EOF

echo "✅ Report generated: REPORT.md"
echo ""

# ============================================
# 完成
# ============================================
echo "============================================"
echo "✅ 系统准备完成!"
echo "============================================"
echo ""
echo "输出目录: $OUTPUT"
echo "主要文件:"
echo "  - system.gro (系统坐标)"
echo "  - topol.top (拓扑文件)"
echo "  - em.gro (能量最小化后)"
echo "  - REPORT.md (详细报告)"
echo ""
echo "下一步: 运行平衡模拟"
echo "  ./equilibration.sh --input em.gro --topology topol.top"
echo ""
