#!/bin/bash
# GROMACS Accelerated Molecular Dynamics (aMD)
# 加速分子动力学 - 通过修改势能面增强采样
# 实现方式: PLUMED aMD / Metadynamics 替代方案

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-system.gro}"
INPUT_TOP="${INPUT_TOP:-topol.top}"
INPUT_CPT="${INPUT_CPT:-npt.cpt}"

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-accelerated-md}"

# aMD 实现方法
AMD_METHOD="${AMD_METHOD:-plumed}"  # plumed/metadynamics
AMD_FALLBACK=0  # 是否从 plumed 回退到 metadynamics (由 check_plumed 设置)

# aMD 类型
AMD_TYPE="${AMD_TYPE:-dual}"  # dual/dihedral/total

# aMD 参数 (自动计算或手动指定)
AMD_E_DIHED="${AMD_E_DIHED:-auto}"      # 二面角能量阈值 (kJ/mol)
AMD_ALPHA_DIHED="${AMD_ALPHA_DIHED:-auto}"  # 二面角加速因子
AMD_E_TOT="${AMD_E_TOT:-auto}"          # 总能量阈值 (kJ/mol)
AMD_ALPHA_TOT="${AMD_ALPHA_TOT:-auto}"  # 总能量加速因子

# 预运行参数 (用于自动计算阈值)
PRERUN_TIME="${PRERUN_TIME:-100}"       # 预运行时间 (ps)
PRERUN_DONE="${PRERUN_DONE:-false}"     # 是否已完成预运行

# 模拟参数
SIM_TIME="${SIM_TIME:-10000}"           # 模拟时间 (ps)
DT="${DT:-0.002}"                       # 时间步长 (ps)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
TEMPERATURE="${TEMPERATURE:-300}"       # 温度 (K)

# 计算资源
NTOMP="${NTOMP:-4}"
GPU_ID="${GPU_ID:-}"

# ============================================
# 函数定义
# ============================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

error() {
    echo "[ERROR] $*" >&2
    exit 1
}

check_file() {
    [[ -f "$1" ]] || error "文件不存在: $1"
}

# ============================================
# 自动修复函数
# ============================================

# 检查 PLUMED
# By default, PLUMED absence is fatal. Set AUTOMD_AMD_ALLOW_FALLBACK=1 to allow
# metadynamics substitute (with explicit disclosure in the report).
check_plumed() {
    if [[ "$AMD_METHOD" == "plumed" ]]; then
        if ! command -v plumed &> /dev/null; then
            log "[WARN] PLUMED 未安装"
            if [[ "${AUTOMD_AMD_ALLOW_FALLBACK:-0}" == "1" ]]; then
                log "[FALLBACK] AUTOMD_AMD_ALLOW_FALLBACK=1 — 切换到 metadynamics"
                log "[WARNING] ⚠️ 结果并非真正的 aMD！报告中将显式标注"
                AMD_METHOD="metadynamics"
                AMD_FALLBACK=1
                return 1
            fi
            log "[ERROR] PLUMED 不可用，aMD 无法执行"
            log "[INFO] 要使用 metadynamics 替代方案，请设 AUTOMD_AMD_ALLOW_FALLBACK=1"
            log "[INFO] 或安装 PLUMED: conda install -c conda-forge plumed"
            error "PLUMED not available — accelerated MD requires PLUMED"
        fi
        
        if ! gmx mdrun -h 2>&1 | grep -q "plumed"; then
            log "[WARN] GROMACS 未编译 PLUMED 支持"
            if [[ "${AUTOMD_AMD_ALLOW_FALLBACK:-0}" == "1" ]]; then
                log "[FALLBACK] AUTOMD_AMD_ALLOW_FALLBACK=1 — 切换到 metadynamics"
                log "[WARNING] ⚠️ 结果并非真正的 aMD！报告中将显式标注"
                AMD_METHOD="metadynamics"
                AMD_FALLBACK=1
                return 1
            fi
            log "[ERROR] GROMACS 未编译 PLUMED 支持，aMD 无法执行"
            log "[INFO] 要使用 metadynamics 替代方案，请设 AUTOMD_AMD_ALLOW_FALLBACK=1"
            log "[INFO] 或重新编译 GROMACS 并启用 PLUMED"
            error "GROMACS compiled without PLUMED — accelerated MD requires PLUMED"
        fi
        
        log "[OK] PLUMED 版本: $(plumed --version | head -1)"
    fi
    return 0
}

# 验证 aMD 参数
validate_amd_params() {
    if [[ "$AMD_E_DIHED" == "auto" || "$AMD_ALPHA_DIHED" == "auto" ]] || \
       [[ "$AMD_E_TOT" == "auto" || "$AMD_ALPHA_TOT" == "auto" ]]; then
        if [[ "$PRERUN_DONE" != "true" ]]; then
            log "[WARN] aMD 参数需要自动计算，但未完成预运行"
            log "[AUTO-FIX] 将执行预运行以计算参数"
            return 1
        fi
    fi
    return 0
}

# 从预运行计算 aMD 参数
calculate_amd_params() {
    log "从预运行数据计算 aMD 参数..."
    
    if [[ ! -f "prerun.edr" ]]; then
        error "预运行能量文件不存在: prerun.edr"
    fi
    
    # 提取二面角能量
    if [[ "$AMD_TYPE" == "dihedral" || "$AMD_TYPE" == "dual" ]]; then
        echo "Proper-Dih." | gmx energy -f prerun.edr -o dihed_energy.xvg 2>&1 | tee energy_extract.log
        
        if [[ -f "dihed_energy.xvg" ]]; then
            local avg_dihed=$(awk '!/^[@#]/ {sum+=$2; n++} END {print sum/n}' dihed_energy.xvg)
            local max_dihed=$(awk '!/^[@#]/ {if($2>max || NR==1) max=$2} END {print max}' dihed_energy.xvg)
            local std_dihed=$(awk -v avg=$avg_dihed '!/^[@#]/ {sum+=($2-avg)^2; n++} END {print sqrt(sum/n)}' dihed_energy.xvg)
            
            # E = Vavg + a * σ_V (推荐 a=3.5-4.0)
            AMD_E_DIHED=$(echo "$avg_dihed + 3.5 * $std_dihed" | bc -l)
            # α = a * σ_V (推荐与阈值增量相同)
            AMD_ALPHA_DIHED=$(echo "3.5 * $std_dihed" | bc -l)
            
            log "[OK] 二面角参数: E=$AMD_E_DIHED, α=$AMD_ALPHA_DIHED"
            log "    (平均=$avg_dihed, 最大=$max_dihed, 标准差=$std_dihed)"
        else
            log "[WARN] 无法提取二面角能量，使用默认值"
            AMD_E_DIHED=1000
            AMD_ALPHA_DIHED=200
        fi
    fi
    
    # 提取总势能
    if [[ "$AMD_TYPE" == "total" || "$AMD_TYPE" == "dual" ]]; then
        echo "Potential" | gmx energy -f prerun.edr -o potential_energy.xvg 2>&1 | tee -a energy_extract.log
        
        if [[ -f "potential_energy.xvg" ]]; then
            local avg_pot=$(awk '!/^[@#]/ {sum+=$2; n++} END {print sum/n}' potential_energy.xvg)
            local max_pot=$(awk '!/^[@#]/ {if($2>max || NR==1) max=$2} END {print max}' potential_energy.xvg)
            local std_pot=$(awk -v avg=$avg_pot '!/^[@#]/ {sum+=($2-avg)^2; n++} END {print sqrt(sum/n)}' potential_energy.xvg)
            
            # 总能量使用更保守的参数 (a=0.2-0.3)
            AMD_E_TOT=$(echo "$avg_pot + 0.2 * ($max_pot - $avg_pot)" | bc -l)
            AMD_ALPHA_TOT=$(echo "0.2 * ($max_pot - $avg_pot)" | bc -l)
            
            log "[OK] 总能量参数: E=$AMD_E_TOT, α=$AMD_ALPHA_TOT"
            log "    (平均=$avg_pot, 最大=$max_pot, 标准差=$std_pot)"
        else
            log "[WARN] 无法提取总势能，使用默认值"
            AMD_E_TOT=-50000
            AMD_ALPHA_TOT=5000
        fi
    fi
}

# 失败重启
restart_from_checkpoint() {
    if [[ -f "amd.cpt" ]]; then
        log "[AUTO-FIX] 从检查点重启模拟"
        
        if [[ "$AMD_METHOD" == "plumed" ]]; then
            gmx mdrun -v -deffnm amd -cpi amd.cpt -plumed plumed.dat \
                -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a amd.log
        else
            gmx mdrun -v -deffnm amd -cpi amd.cpt \
                -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a amd.log
        fi
        
        return $?
    fi
    return 1
}

# ============================================
# PLUMED aMD 配置生成
# ============================================

generate_plumed_amd() {
    log "生成 PLUMED aMD 配置..."
    
    cat > plumed.dat << 'EOFPLUMED'
# PLUMED Accelerated MD Configuration
# Generated by AutoMD-GROMACS

EOFPLUMED

    case "$AMD_TYPE" in
        dihedral)
            cat >> plumed.dat << EOFDIH
# Dihedral aMD
# 仅加速二面角自由度

# 计算二面角能量
dihed: ENERGY

# aMD 偏置
AMD ...
  ARG=dihed
  THRESHOLD=$AMD_E_DIHED
  ALPHA=$AMD_ALPHA_DIHED
  LABEL=amd_dihed
... AMD

# 输出
PRINT ARG=dihed,amd_dihed.bias FILE=COLVAR STRIDE=100
EOFDIH
            ;;
            
        total)
            cat >> plumed.dat << EOFTOT
# Total Energy aMD
# 加速总势能

# 计算总势能
energy: ENERGY

# aMD 偏置
AMD ...
  ARG=energy
  THRESHOLD=$AMD_E_TOT
  ALPHA=$AMD_ALPHA_TOT
  LABEL=amd_total
... AMD

# 输出
PRINT ARG=energy,amd_total.bias FILE=COLVAR STRIDE=100
EOFTOT
            ;;
            
        dual)
            cat >> plumed.dat << EOFDUAL
# Dual-Boost aMD
# 同时加速二面角和总能量

# 计算能量
dihed: ENERGY TYPE=dihedral
total: ENERGY

# 二面角 aMD
AMD_DIHED ...
  ARG=dihed
  THRESHOLD=$AMD_E_DIHED
  ALPHA=$AMD_ALPHA_DIHED
  LABEL=amd_dihed
... AMD_DIHED

# 总能量 aMD
AMD_TOTAL ...
  ARG=total
  THRESHOLD=$AMD_E_TOT
  ALPHA=$AMD_ALPHA_TOT
  LABEL=amd_total
... AMD_TOTAL

# 输出
PRINT ARG=dihed,total,amd_dihed.bias,amd_total.bias FILE=COLVAR STRIDE=100
EOFDUAL
            ;;
    esac
    
    log "[OK] PLUMED 配置已生成: plumed.dat"
}

# ============================================
# Metadynamics 替代方案
# ============================================

generate_metadynamics_alternative() {
    log "生成 Metadynamics 替代配置 (模拟 aMD 效果)..."
    log "[INFO] 使用 well-tempered metadynamics 作为 aMD 替代方案"
    
    # 使用多个 CV 的 metadynamics 来近似 aMD
    cat > plumed.dat << 'EOFMETA'
# Well-Tempered Metadynamics (aMD Alternative)
# 使用多个集合变量模拟加速效果

# 定义主要二面角 (示例: 前4个主链二面角)
phi1: TORSION ATOMS=5,7,9,15
psi1: TORSION ATOMS=7,9,15,17
phi2: TORSION ATOMS=15,17,19,25
psi2: TORSION ATOMS=17,19,25,27

# Well-tempered metadynamics
METAD ...
  ARG=phi1,psi1,phi2,psi2
  PACE=500
  HEIGHT=1.2
  SIGMA=0.35,0.35,0.35,0.35
  FILE=HILLS
  BIASFACTOR=15
  TEMP=TEMP_PLACEHOLDER
  GRID_MIN=-pi,-pi,-pi,-pi
  GRID_MAX=pi,pi,pi,pi
... METAD

# 输出
PRINT ARG=phi1,psi1,phi2,psi2 FILE=COLVAR STRIDE=100
EOFMETA

    sed -i "s/TEMP_PLACEHOLDER/$TEMPERATURE/" plumed.dat
    
    log "[OK] Metadynamics 配置已生成"
    log "[WARN] 需要根据实际系统调整二面角原子索引"
}

# ============================================
# 前置检查
# ============================================

log "开始加速分子动力学 (aMD)"
log "方法: $AMD_METHOD"
log "类型: $AMD_TYPE"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 检查方法可用性
check_plumed

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 复制输入文件
cp "../$INPUT_GRO" .
cp "../$INPUT_TOP" .
[[ -f "../$INPUT_CPT" ]] && cp "../$INPUT_CPT" .

# ============================================
# Phase 1: 预运行 (如需要)
# ============================================

if ! validate_amd_params; then
    log "Phase 1: 预运行以计算 aMD 参数"
    
    # 生成预运行 MDP
    cat > prerun.mdp << EOFPRE
; Prerun for aMD parameter calculation
integrator              = md
nsteps                  = $(echo "$PRERUN_TIME / $DT" | bc)
dt                      = $DT
nstxout-compressed      = 0
nstlog                  = 1000
nstenergy               = 100
tcoupl                  = V-rescale
ref_t                   = $TEMPERATURE
tau_t                   = 0.1
tc-grps                 = System
pcoupl                  = Parrinello-Rahman
ref_p                   = 1.0
tau_p                   = 2.0
compressibility         = 4.5e-5
constraints             = h-bonds
cutoff-scheme           = Verlet
coulombtype             = PME
rcoulomb                = 1.0
rvdw                    = 1.0
EOFPRE

    log "运行预模拟 ($PRERUN_TIME ps)..."
    
    if [[ -f "$INPUT_CPT" ]]; then
        gmx grompp -f prerun.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" -t "$INPUT_CPT" \
            -o prerun.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR" || true
    else
        gmx grompp -f prerun.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" \
            -o prerun.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR" || true
    fi
    
    gmx mdrun -v -deffnm prerun -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee prerun.log
    
    # 计算参数
    calculate_amd_params
    
    # 使用预运行的最终结构
    INPUT_GRO="prerun.gro"
    INPUT_CPT="prerun.cpt"
fi

# ============================================
# Phase 2: 生成 aMD 配置
# ============================================

log "Phase 2: 生成 aMD 配置"

if [[ "$AMD_METHOD" == "plumed" ]]; then
    generate_plumed_amd
else
    generate_metadynamics_alternative
fi

# 生成 MDP 文件
cat > amd.mdp << EOFMDP
; Accelerated MD Production Run
; Generated by AutoMD-GROMACS

; Run control
integrator              = md
nsteps                  = $NSTEPS
dt                      = $DT

; Output control
nstxout                 = 0
nstvout                 = 0
nstfout                 = 0
nstlog                  = 5000
nstxout-compressed      = 5000
compressed-x-grps       = System

; Neighbor searching
cutoff-scheme           = Verlet
nstlist                 = 10
ns_type                 = grid
pbc                     = xyz

; Electrostatics
coulombtype             = PME
rcoulomb                = 1.0
pme_order               = 4
fourierspacing          = 0.12

; Van der Waals
vdwtype                 = Cut-off
rvdw                    = 1.0
DispCorr                = EnerPres

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = System
tau_t                   = 0.1
ref_t                   = $TEMPERATURE

; Pressure coupling
pcoupl                  = Parrinello-Rahman
pcoupltype              = isotropic
tau_p                   = 2.0
ref_p                   = 1.0
compressibility         = 4.5e-5

; Velocity generation
gen_vel                 = no

; Constraints
constraints             = h-bonds
constraint_algorithm    = LINCS
EOFMDP

log "[OK] MDP 文件已生成: amd.mdp"

# ============================================
# Phase 3: 预处理
# ============================================

log "Phase 3: 预处理 (grompp)"

gmx grompp -f amd.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" -t "$INPUT_CPT" \
    -o amd.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true

[[ -f "amd.tpr" ]] || error "TPR 生成失败"

# ============================================
# Phase 4: 运行 aMD 模拟
# ============================================

log "Phase 4: 运行 aMD 模拟"
log "模拟时间: $SIM_TIME ps"
log "aMD 参数:"
[[ "$AMD_TYPE" == "dihedral" || "$AMD_TYPE" == "dual" ]] && \
    log "  二面角: E=$AMD_E_DIHED, α=$AMD_ALPHA_DIHED"
[[ "$AMD_TYPE" == "total" || "$AMD_TYPE" == "dual" ]] && \
    log "  总能量: E=$AMD_E_TOT, α=$AMD_ALPHA_TOT"

if [[ "$AMD_METHOD" == "plumed" ]]; then
    gmx mdrun -v -deffnm amd -plumed plumed.dat \
        -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee amd.log || {
        log "[ERROR] 模拟失败，尝试重启..."
        restart_from_checkpoint || error "重启失败"
    }
else
    gmx mdrun -v -deffnm amd -plumed plumed.dat \
        -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee amd.log || {
        log "[ERROR] 模拟失败，尝试重启..."
        restart_from_checkpoint || error "重启失败"
    }
fi

# ============================================
# Phase 5: 能量重加权分析
# ============================================

log "Phase 5: 能量重加权分析"

if [[ -f "COLVAR" ]]; then
    log "计算重加权因子..."
    
    # 提取偏置能量
    if [[ "$AMD_TYPE" == "dual" ]]; then
        awk '!/^#/ {print $1, $3+$5}' COLVAR > bias_total.dat
    else
        awk '!/^#/ {print $1, $3}' COLVAR > bias_total.dat
    fi
    
    # 计算平均偏置
    avg_bias=$(awk '{sum+=$2; n++} END {print sum/n}' bias_total.dat)
    max_bias=$(awk '{if($2>max || NR==1) max=$2} END {print max}' bias_total.dat)
    
    log "偏置统计:"
    log "  平均偏置: $avg_bias kJ/mol"
    log "  最大偏置: $max_bias kJ/mol"
    
    # 计算加速因子
    kT=$(echo "$TEMPERATURE * 0.008314" | bc -l)
    accel_factor=$(echo "e($avg_bias / $kT)" | bc -l)
    
    log "  有效加速因子: $accel_factor"
    log "  有效模拟时间: $(echo "$SIM_TIME * $accel_factor" | bc -l) ps"
fi

# ============================================
# Phase 6: 生成报告
# ============================================

log "Phase 6: 生成报告"

cat > AMD_REPORT.md << EOFREPORT
# Accelerated MD 模拟报告

$( [[ "$AMD_FALLBACK" == "1" ]] && cat << 'FALLBACK_BANNER'
⚠️ ═══════════════════════════════════════════════════════
⚠️  重要警告: 本次运行使用了 Metadynamics 替代方案
⚠️
⚠️  PLUMED 不可用，已回退到 well-tempered metadynamics。
⚠️  此结果并非真正的 Accelerated MD！
⚠️  - 采样机制不同 (metadynamics vs aMD 偏置势)
⚠️  - 重加权方法不同
⚠️  - 与文献比较时请注意方法差异
⚠️
⚠️  要运行真正的 aMD，请安装 PLUMED：
⚠️    conda install -c conda-forge plumed
⚠️  或重新编译 GROMACS 启用 PLUMED 支持。
⚠️ ═══════════════════════════════════════════════════════

FALLBACK_BANNER
)
## 模拟参数

- **方法**: $AMD_METHOD
- **aMD 类型**: $AMD_TYPE
- **模拟时间**: $SIM_TIME ps
- **温度**: $TEMPERATURE K

## aMD 参数

EOFREPORT

if [[ "$AMD_TYPE" == "dihedral" || "$AMD_TYPE" == "dual" ]]; then
    cat >> AMD_REPORT.md << EOFDIH
### 二面角加速

- **能量阈值 (E)**: $AMD_E_DIHED kJ/mol
- **加速因子 (α)**: $AMD_ALPHA_DIHED kJ/mol

EOFDIH
fi

if [[ "$AMD_TYPE" == "total" || "$AMD_TYPE" == "dual" ]]; then
    cat >> AMD_REPORT.md << EOFTOT
### 总能量加速

- **能量阈值 (E)**: $AMD_E_TOT kJ/mol
- **加速因子 (α)**: $AMD_ALPHA_TOT kJ/mol

EOFTOT
fi

if [[ -f "bias_total.dat" ]]; then
    cat >> AMD_REPORT.md << EOFBIAS

## 偏置统计

- **平均偏置**: $avg_bias kJ/mol
- **最大偏置**: $max_bias kJ/mol
- **有效加速因子**: $accel_factor
- **有效模拟时间**: $(echo "$SIM_TIME * $accel_factor" | bc -l) ps

EOFBIAS
fi

cat >> AMD_REPORT.md << EOFOUT

## 输出文件

- \`amd.xtc\` - 轨迹文件
- \`amd.edr\` - 能量文件
- \`COLVAR\` - 偏置能量记录
- \`plumed.dat\` - PLUMED/Metadynamics 配置
- \`amd.log\` - 模拟日志

EOFOUT

if [[ "$PRERUN_DONE" == "true" || -f "prerun.edr" ]]; then
    cat >> AMD_REPORT.md << EOFPRE

## 预运行统计

预运行用于自动计算 aMD 参数。

查看: \`prerun.log\`, \`energy_extract.log\`

EOFPRE
fi

if [[ "$AMD_FALLBACK" == "1" ]]; then
    # === Metadynamics fallback report sections ===
    cat >> AMD_REPORT.md << EOFMETA

## 后续分析 (Metadynamics)

⚠️ 此为 Metadynamics 运行，不是真正的 aMD。分析方法与 aMD 不同。

### 1. 可视化自由能面

\`\`\`bash
# 使用 PLUMED sum_hills 重构自由能面
plumed sum_hills --hills HILLS --outfile fes.dat --mintozero

# 绘图
gnuplot << PLOT
set pm3d map
splot 'fes.dat' with pm3d
PLOT
\`\`\`

### 2. 检查 CV 采样

\`\`\`bash
# 查看 COLVAR 中的 CV 时间序列
xmgrace COLVAR
\`\`\`

### 3. 提取构象

\`\`\`bash
gmx trjconv -s amd.tpr -f amd.xtc -o conf.gro -sep -skip 100
\`\`\`

## 理论背景 (Metadynamics)

本运行使用了 Well-Tempered Metadynamics，其偏置势为：

V_G(s,t) = Σ w_i * exp(-|s - s_i|² / 2σ²)

其中偏置高度随时间衰减: w = w₀ * exp(-V_G(s,t) / kΔT)

### 参考文献 (Metadynamics)

- Barducci et al. (2008). Well-tempered metadynamics. Phys. Rev. Lett. 100, 020603.
- Laio & Parrinello (2002). Escaping free-energy minima. PNAS 99, 12562.

## 质量检查

EOFMETA
else
    # === Real aMD report sections ===
    cat >> AMD_REPORT.md << EOFANALYSIS

## 后续分析

### 1. 可视化偏置能量

\`\`\`bash
# 绘制偏置随时间变化
xmgrace COLVAR

# 或使用 gnuplot
gnuplot << PLOT
set xlabel "Time (ps)"
set ylabel "Bias Energy (kJ/mol)"
plot "bias_total.dat" with lines
PLOT
\`\`\`

### 2. 能量重加权

aMD 通过修改势能面加速采样，需要重加权恢复正确的系综分布。

**重加权公式**:
\`\`\`
P(x) = P*(x) * exp(ΔV(x) / kT)
\`\`\`

其中:
- P*(x): aMD 采样的分布
- ΔV(x): 偏置势能
- kT: 热能

**实现方法**:

1. **指数平均重加权** (适用于小偏置):
\`\`\`bash
# 计算重加权因子
awk -v kT=$kT '{w=exp(\$2/kT); print \$1, w}' bias_total.dat > weights.dat
\`\`\`

2. **Cumulant 展开** (适用于大偏置):
\`\`\`bash
# 使用 PyReweighting 或 MBAR
# 需要 Python 脚本
\`\`\`

3. **Maclaurin 级数展开**:
\`\`\`
ln<exp(βΔV)> ≈ β<ΔV> + β²/2(<ΔV²> - <ΔV>²) + ...
\`\`\`

### 3. 自由能计算

\`\`\`bash
# 使用 PLUMED 的 reweight 工具
plumed driver --plumed plumed_reweight.dat --ixtc amd.xtc

# 或使用 PyReweighting
python reweight_amd.py --colvar COLVAR --temp $TEMPERATURE
\`\`\`

### 4. 提取增强采样的构象

\`\`\`bash
# 从轨迹提取关键构象
gmx trjconv -s amd.tpr -f amd.xtc -o conf.gro -sep -skip 100
\`\`\`

## 理论背景

### aMD 原理

加速分子动力学通过修改势能面来增强采样:

**修改势能**:
\`\`\`
V*(r) = V(r) + ΔV(r)
\`\`\`

**偏置势能** (当 V(r) < E):
\`\`\`
ΔV(r) = (E - V(r))² / (α + E - V(r))
\`\`\`

其中:
- E: 能量阈值
- α: 加速因子 (控制偏置强度)

### 参数选择指南

**二面角 aMD**:
- E_dihed = V_avg + a * σ_V (推荐 a=3.5-4.0)
- α_dihed = a * σ_V

**总能量 aMD**:
- E_tot = V_avg + b * (V_max - V_avg) (推荐 b=0.2-0.3)
- α_tot = b * (V_max - V_avg)

**双重加速 aMD**:
- 同时应用二面角和总能量加速
- 提供最强的增强采样效果

### 优缺点

**优点**:
- 连续偏置，无需预定义 CV
- 自动探索构象空间
- 适用于大规模构象变化

**缺点**:
- 需要能量重加权
- 参数选择需要预运行
- 大偏置时重加权困难

## 参考文献

- Hamelberg et al. (2004). Accelerated molecular dynamics: A promising and efficient simulation method for biomolecules. J. Chem. Phys. 120, 11919.
- Pierce et al. (2012). Routine access to millisecond time scale events with accelerated molecular dynamics. J. Chem. Theory Comput. 8, 2997-3002.
- Miao et al. (2014). Gaussian accelerated molecular dynamics. J. Chem. Theory Comput. 11, 3584-3595.

## 质量检查

EOFANALYSIS
fi

# 检查模拟完成
if grep -q "Finished mdrun" amd.log 2>/dev/null; then
    echo "✅ 模拟成功完成" >> AMD_REPORT.md
else
    echo "⚠️ 模拟可能未完成，检查 amd.log" >> AMD_REPORT.md
fi

# 检查偏置数据
if [[ -f "COLVAR" ]] && [[ -s "COLVAR" ]]; then
    echo "✅ 偏置能量已记录" >> AMD_REPORT.md
else
    echo "⚠️ 偏置能量数据缺失" >> AMD_REPORT.md
fi

log "报告已生成: AMD_REPORT.md"

# ============================================
# 完成
# ============================================

log "Accelerated MD 模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/AMD_REPORT.md"

exit 0

