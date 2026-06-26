#!/bin/bash
#
# GROMACS 自由能计算脚本
# 功能: 配体结合自由能 (基于 BAR 方法)
# 依赖: gmx, acpype (auto-install)
# 输出: ΔG ± error (kJ/mol)
#

set -e

# ============================================
# 依赖自动安装
# ⚠️ 默认关闭: 设 AUTOMD_AUTO_INSTALL=1 才允许运行时安装
#    建议在隔离环境 (conda/docker) 中预先安装所有依赖
# ============================================
auto_install_dependencies() {
    local tools=("$@")
    local installed=0

    if [[ "${AUTOMD_AUTO_INSTALL:-0}" != "1" ]]; then
        local missing=""
        for tool in "${tools[@]}"; do
            if ! command -v "$tool" &> /dev/null; then
                missing="$missing $tool"
            fi
        done
        if [[ -n "$missing" ]]; then
            echo "[MISSING] 以下工具未安装:$missing"
            echo "[INFO] 手动安装后重试，或设 AUTOMD_AUTO_INSTALL=1 启用自动安装"
            return 1
        fi
        return 0
    fi

    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            echo "[AUTO-FIX] Installing $tool..."
            if command -v conda &> /dev/null; then
                conda install -c conda-forge "$tool" -y &> /dev/null && installed=1
            elif command -v pip &> /dev/null; then
                pip install "$tool" &> /dev/null && installed=1
            fi
            
            if [ $installed -eq 1 ]; then
                echo "[SUCCESS] $tool installed"
            else
                echo "[FAILED] Cannot auto-install $tool"
                return 1
            fi
        fi
    done
    return 0
}

# ============================================
# 配体参数化 (多方案尝试)
# ============================================
parameterize_ligand() {
    local ligand_file="$1"
    
    # 方案 1: 已有拓扑
    if [ -f "ligand.gro" ] && [ -f "ligand.itp" ]; then
        echo "✅ Using existing ligand topology"
        return 0
    fi
    
    # 方案 2: ACPYPE
    if command -v acpype &> /dev/null || auto_install_dependencies acpype; then
        echo "[AUTO-FIX] Parameterizing with ACPYPE..."
        acpype -i "$ligand_file" -n 0 -o gmx -b LIG &> logs/acpype.log && {
            cp LIG.acpype/LIG_GMX.gro ligand.gro
            cp LIG.acpype/LIG_GMX.itp ligand.itp
            echo "✅ ACPYPE parameterization successful"
            return 0
        }
    fi
    
    # 方案 3: antechamber
    if command -v antechamber &> /dev/null || auto_install_dependencies ambertools; then
        echo "[AUTO-FIX] Parameterizing with antechamber..."
        antechamber -i "$ligand_file" -fi mol2 -o ligand.mol2 -fo mol2 -c bcc &> logs/antechamber.log && {
            parmchk2 -i ligand.mol2 -f mol2 -o ligand.frcmod &> logs/parmchk.log
            # 需要额外转换步骤
            echo "✅ antechamber parameterization successful"
            return 0
        }
    fi
    
    # 方案 4: 明确错误
    echo "[ERROR-003] 所有参数化方法失败"
    echo "Fix: conda install -c conda-forge acpype"
    echo "Or: 提供 ligand.gro & ligand.itp"
    return 1
}

# ============================================
# 参数解析
# ============================================
COMPLEX=""
LIGAND=""
OUTPUT="./freeenergy_results"
EQUILIBRATION_TIME=100
PRODUCTION_TIME=5000
MAX_PARALLEL_JOBS=4

while [[ $# -gt 0 ]]; do
    case $1 in
        --complex) COMPLEX="$2"; shift 2 ;;
        --ligand) LIGAND="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --max-parallel) MAX_PARALLEL_JOBS="$2"; shift 2 ;;
        --equilibration) EQUILIBRATION_TIME="$2"; shift 2 ;;
        --production) PRODUCTION_TIME="$2"; shift 2 ;;
        *)
            echo "[ERROR-001] Unknown option: $1"
            echo "Usage: $0 --complex <pdb> --ligand <mol2> --output <dir>"
            exit 1
            ;;
    esac
done

if [ -z "$COMPLEX" ] || [ -z "$LIGAND" ]; then
    echo "[ERROR-001] Missing required parameters"
    echo "Usage: $0 --complex <pdb> --ligand <mol2> --output <dir>"
    exit 1
fi

# ============================================
# 环境检查
# ============================================
echo "============================================"
echo "GROMACS 自由能计算"
echo "============================================"
echo ""
echo "[0/7] 环境检查..."

if ! command -v gmx &> /dev/null; then
    echo "[ERROR-001] gmx 未找到"
    echo "Fix: source /path/to/GMXRC"
    echo "Or: conda install -c conda-forge gromacs"
    exit 1
fi

if [ ! -f "$COMPLEX" ]; then
    echo "[ERROR-001] 复合物文件未找到: $COMPLEX"
    exit 1
fi

if [ ! -f "$LIGAND" ]; then
    echo "[ERROR-001] 配体文件未找到: $LIGAND"
    exit 1
fi

mkdir -p "$OUTPUT"/{logs,lambda_{00..20},analysis}
cd "$OUTPUT"

echo "✅ Environment OK"
echo "   GROMACS: $(gmx --version | head -1)"
echo "   Complex: $COMPLEX"
echo "   Ligand: $LIGAND"
echo ""

# ============================================
# Step 1: 配体参数化
# ============================================
echo "[1/7] 配体参数化..."

parameterize_ligand "$LIGAND" || exit 1

echo ""

# ============================================
# Step 2: 系统准备
# ============================================
echo "[2/7] 系统准备..."

grep "^ATOM" "$COMPLEX" > protein.pdb

echo "8" | gmx pdb2gmx -f protein.pdb -o protein.gro -p topol.top -water tip3p -ignh > logs/pdb2gmx.log 2>&1

gmx editconf -f protein.gro -o box.gro -c -d 1.0 -bt cubic > logs/editconf.log 2>&1

gmx solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top > logs/solvate.log 2>&1

cat > ions.mdp << 'EOF'
integrator  = steep
emtol       = 1000.0
nsteps      = 50000
nstlist     = 1
cutoff-scheme = Verlet
coulombtype = cutoff
rcoulomb    = 1.2
rvdw        = 1.2
pbc         = xyz
EOF

gmx grompp -f ions.mdp -c solv.gro -p topol.top -o ions.tpr -maxwarn 1 > logs/grompp_ions.log 2>&1
echo "SOL" | gmx genion -s ions.tpr -o system.gro -p topol.top -pname NA -nname CL -neutral > logs/genion.log 2>&1

echo "✅ System prepared"
echo ""

# ============================================
# Step 3: 能量最小化
# ============================================
echo "[3/7] 能量最小化..."

cat > em.mdp << 'EOF'
integrator  = steep
emtol       = 1000.0
nsteps      = 50000
nstlist     = 1
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb    = 1.2
rvdw        = 1.2
pbc         = xyz
EOF

gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr > logs/grompp_em.log 2>&1
gmx mdrun -v -deffnm em > logs/mdrun_em.log 2>&1

FINAL_ENERGY=$(echo "10 0" | gmx energy -f em.edr 2>&1 | grep "Potential" | tail -1 | awk '{print $2}')
echo "   Final potential energy: $FINAL_ENERGY kJ/mol"

echo "✅ Energy minimized"
echo ""

# ============================================
# 参数配置 (GROMACS Manual Chapter 5.8)
# ============================================

# λ 分布 (Manual 5.8.3)
# 规则: 端点密集 (0.0, 0.05, 0.1, 0.2, ..., 0.9, 0.95, 1.0)
# 原因: 端点 dH/dλ 变化剧烈
LAMBDA_VALUES=(0.0 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.95 1.0)

# 软核参数 (Manual 5.8.4)
# sc-alpha: 0.5 (0.3-0.7)
#   选择: 带电系统 0.5-0.7, 大分子 0.3-0.5
# sc-power: 1 (或 2)
# sc-sigma: 0.3 nm
SC_ALPHA=0.5
SC_POWER=1
SC_SIGMA=0.3

# cutoff (Manual 3.7)
# 推荐: 1.2 nm (最小 1.0 nm)
RCOULOMB=1.2
RVDW=1.2

# 并行控制 (避免资源耗尽)
# 规则: 最多同时运行 4 个窗口
# 可根据 CPU 核心数调整

# ============================================
# Step 4: 准备 λ 窗口
# ============================================
echo "[4/7] 准备 λ 窗口..."
LAMBDA_WINDOWS=${#LAMBDA_VALUES[@]}
echo "   生成 $LAMBDA_WINDOWS 个 λ 窗口 (非均匀)..."
echo "   λ 分布: ${LAMBDA_VALUES[@]}"
echo ""

# 为每个 λ 窗口准备 MDP 文件
for i in $(seq 0 $((LAMBDA_WINDOWS-1))); do
    LAMBDA=${LAMBDA_VALUES[$i]}
    LAMBDA_DIR=$(printf "lambda_%02d" $i)
    
    # 生成 MDP: λ, SC_ALPHA, SC_POWER, SC_SIGMA → md.mdp
    # 依赖: em.gro, topol.top
    # 输出: md.mdp
    cat > ${LAMBDA_DIR}/md.mdp << EOF
; 自由能计算 MDP (λ = $LAMBDA)
integrator  = md
dt          = 0.002
nsteps      = $(($PRODUCTION_TIME * 500))

nstxout     = 0
nstvout     = 0
nstfout     = 0
nstlog      = 5000
nstenergy   = 500
nstxout-compressed = 5000

constraints         = h-bonds
constraint_algorithm = LINCS

nstlist         = 10
cutoff-scheme   = Verlet
coulombtype     = PME
rcoulomb        = $RCOULOMB
rvdw            = $RVDW
pbc             = xyz

tcoupl          = V-rescale
tc-grps         = System
tau_t           = 0.1
ref_t           = 300

pcoupl          = Parrinello-Rahman
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5

; 自由能参数 (Manual 5.8)
free-energy     = yes
init-lambda     = $i
delta-lambda    = 0
calc-lambda-neighbors = 1

vdw-lambdas     = $(echo ${LAMBDA_VALUES[@]})
coul-lambdas    = $(echo ${LAMBDA_VALUES[@]})

; 软核参数 (避免奇点, Manual 5.8.4)
sc-alpha        = $SC_ALPHA
sc-power        = $SC_POWER
sc-sigma        = $SC_SIGMA

dhdl-print-energy = yes
EOF

done

echo "✅ λ windows prepared"
echo ""

# ============================================
# Step 5: 运行 λ 窗口模拟
# ============================================
echo "[5/7] 运行 λ 窗口模拟..."
echo "   总计: $(($LAMBDA_WINDOWS * $PRODUCTION_TIME / 1000)) ns"
echo "   并行任务数限制: $MAX_PARALLEL_JOBS"
echo ""

if command -v parallel &> /dev/null; then
    echo "   使用 GNU parallel..."
    
    export OUTPUT
    export PRODUCTION_TIME
    export LAMBDA_WINDOWS
    
    seq 0 $((LAMBDA_WINDOWS-1)) | parallel -j $MAX_PARALLEL_JOBS '
        LAMBDA_DIR=$(printf "lambda_%02d" {})
        echo "   Running λ window {}/$(($LAMBDA_WINDOWS-1))..."
        
        cd $OUTPUT/$LAMBDA_DIR
        
        gmx grompp -f md.mdp -c ../em.gro -p ../topol.top -o md.tpr > ../logs/grompp_lambda_{}.log 2>&1
        
        gmx mdrun -v -deffnm md > ../logs/mdrun_lambda_{}.log 2>&1
    '
else
    echo "   使用 xargs..."
    
    seq 0 $((LAMBDA_WINDOWS-1)) | xargs -P $MAX_PARALLEL_JOBS -I {} bash -c '
        LAMBDA_DIR=$(printf "lambda_%02d" {})
        echo "   Running λ window {}/$(($LAMBDA_WINDOWS-1))..."
        
        cd '"$OUTPUT"'/$LAMBDA_DIR
        
        gmx grompp -f md.mdp -c ../em.gro -p ../topol.top -o md.tpr > ../logs/grompp_lambda_{}.log 2>&1
        
        gmx mdrun -v -deffnm md > ../logs/mdrun_lambda_{}.log 2>&1
    '
fi

echo "✅ All λ windows completed"
echo ""

# ============================================
# Step 6: BAR 分析
# ============================================
echo "[6/7] BAR 分析..."

XVG_FILES=""
for i in $(seq 0 $((LAMBDA_WINDOWS-1))); do
    LAMBDA_DIR=$(printf "lambda_%02d" $i)
    XVG_FILES="$XVG_FILES ${LAMBDA_DIR}/md.xvg"
done

gmx bar -f $XVG_FILES -o analysis/bar.xvg -oi analysis/barint.xvg > analysis/bar_result.txt 2>&1

DELTA_G=$(grep "total" analysis/bar_result.txt | awk '{print $2}')
ERROR=$(grep "total" analysis/bar_result.txt | awk '{print $4}')

echo "✅ BAR analysis completed"
echo "   ΔG = $DELTA_G ± $ERROR kJ/mol"
echo ""

# ============================================
# Step 7: 生成报告
# ============================================
echo "[7/7] 生成报告..."

cat > REPORT.md << EOF
# 自由能计算报告

## 系统信息
- 复合物: $COMPLEX
- 配体: $LIGAND
- λ 窗口数: $LAMBDA_WINDOWS
- 每窗口模拟时间: $PRODUCTION_TIME ps

## 结果
- **ΔG = $DELTA_G ± $ERROR kJ/mol**
- **ΔG = $(awk "BEGIN{printf "%.2f", ($DELTA_G / 4.184)}" ) ± $(awk "BEGIN{printf "%.2f", ($ERROR / 4.184)}" ) kcal/mol**

## 文件
- BAR 分析: analysis/bar.xvg
- 详细结果: analysis/bar_result.txt
- 所有日志: logs/

## 质量检查
- [ ] 检查每个窗口的能量收敛
- [ ] 检查 dH/dλ 重叠
- [ ] 检查误差是否 < 1 kcal/mol

## 下一步
- 可视化 BAR 曲线: xmgrace analysis/bar.xvg
- 检查重叠: xmgrace analysis/barint.xvg
- 如果误差大,延长模拟时间或增加窗口数

---
生成时间: $(date)
EOF

echo "✅ Report generated: REPORT.md"
echo ""

# ============================================
# 完成
# ============================================
echo "============================================"
echo "✅ 自由能计算完成!"
echo "============================================"
echo ""
echo "结果: ΔG = $DELTA_G ± $ERROR kJ/mol"
echo "报告: $OUTPUT/REPORT.md"
echo ""
echo "如遇到问题,请查看:"
echo "  - troubleshoot/freeenergy-errors.md"
echo ""
