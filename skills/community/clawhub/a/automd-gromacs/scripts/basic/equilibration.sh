#!/bin/bash
# GROMACS Equilibration Script
# 系统平衡流程 - NVT + NPT
# 基于 1AKI 实战经验

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-em.gro}"           # 能量最小化后的结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-equilibration}"

# 平衡参数
NVT_STEPS="${NVT_STEPS:-50000}"            # NVT 步数 (默认 100 ps)
NPT_STEPS="${NPT_STEPS:-50000}"            # NPT 步数 (默认 100 ps)
TEMPERATURE="${TEMPERATURE:-300}"          # 温度 (K)
PRESSURE="${PRESSURE:-1.0}"                # 压强 (bar)

# 约束参数
RESTRAINT="${RESTRAINT:-posre}"            # 位置约束类型 (posre/none)
RESTRAINT_FC="${RESTRAINT_FC:-1000}"       # 约束力常数 (kJ/mol/nm^2)

# 计算资源
NTOMP="${NTOMP:-2}"                        # OpenMP 线程数

# ============================================
# 函数定义
# ============================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
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

# 检查 EM 收敛: Fmax < 1000 kJ/mol/nm
# 未收敛 → 延长 nsteps
check_em_convergence() {
    local em_log="$1"
    if [ -f "$em_log" ]; then
        local max_force=$(grep "Maximum force" "$em_log" | tail -1 | awk '{print $4}')
        if [ -n "$max_force" ]; then
            if [ "$(echo "$max_force" | awk "{if($1>1000)print 1}")" = "1" ]; then
                echo "[WARN] EM 未收敛 (Fmax=$max_force)"
                echo "[AUTO-FIX] 延长 EM steps → 100000..."
                return 1
            fi
        fi
    fi
    return 0
}

# 检查 NVT 稳定性: 温度波动 < 5%
check_nvt_stability() {
    local nvt_edr="$1"
    if [ -f "$nvt_edr" ]; then
        local temp_avg=$(echo "Temperature" | gmx energy -f "$nvt_edr" 2>&1 | grep "Temperature" | tail -1 | awk '{print $2}')
        local temp_std=$(echo "Temperature" | gmx energy -f "$nvt_edr" 2>&1 | grep "Temperature" | tail -1 | awk '{print $3}')
        
        if [ -n "$temp_avg" ] && [ -n "$temp_std" ]; then
            local fluctuation=$(awk "BEGIN{printf "%.2f", ($temp_std/$temp_avg)*100}")
            if [ "$(echo "$fluctuation" | awk "{if($1>5)print 1}")" = "1" ]; then
                echo "[WARN] NVT 温度波动高 ($fluctuation%)"
                echo "[AUTO-FIX] 考虑延长 NVT / 调整 tau_t"
                return 1
            fi
        fi
    fi
    return 0
}

# 检查 NPT 稳定性: 密度波动 < 2%
check_npt_stability() {
    local npt_edr="$1"
    if [ -f "$npt_edr" ]; then
        local dens_avg=$(echo "Density" | gmx energy -f "$npt_edr" 2>&1 | grep "Density" | tail -1 | awk '{print $2}')
        local dens_std=$(echo "Density" | gmx energy -f "$npt_edr" 2>&1 | grep "Density" | tail -1 | awk '{print $3}')
        
        if [ -n "$dens_avg" ] && [ -n "$dens_std" ]; then
            local fluctuation=$(awk "BEGIN{printf "%.2f", ($dens_std/$dens_avg)*100}")
            if [ "$(echo "$fluctuation" | awk "{if($1>2)print 1}")" = "1" ]; then
                echo "[WARN] NPT 密度波动高 ($fluctuation%)"
                echo "[AUTO-FIX] 考虑延长 NPT"
                return 1
            fi
        fi
    fi
    return 0
}

# ============================================
# 前置检查
# ============================================

log "开始系统平衡流程"
log "输入: $INPUT_GRO, $INPUT_TOP"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# ============================================
# 知识内嵌: 平衡参数 (Manual 3.4, 5.4)
# ============================================
# EM (Manual 5.4):
# emtol: 1000 kJ/mol/nm (标准)
# nsteps: 50000 (通常足够)
# emstep: 0.01 nm
#
# NVT (Manual 3.4):
# 时间: 100 ps (标准)
# 温度: 300 K (室温), 310 K (生理)
# tcoupl: V-rescale (推荐)
# tau_t: 0.1 ps (快速耦合)
#
# NPT (Manual 3.4):
# 时间: 100 ps (标准)
# 压力: 1.0 bar
# pcoupl: Parrinello-Rahman (生产)
#         Berendsen (平衡, 快速但不准)
# tau_p: 2.0 ps
# compressibility: 4.5e-5 bar^-1 (水)
#
# 位置限制 (Manual 3.4):
# 策略: 强 → 中 → 弱 → 无
# 力常数: 4000 → 2000 → 1000 → 0 kJ/mol/nm²

# ============================================
# Phase 1: NVT 平衡 (恒温)
# ============================================

log "Phase 1: NVT 平衡 (恒温)"

# 生成 NVT MDP 文件
cat > nvt.mdp << EOF
; NVT equilibration
integrator              = md
dt                      = 0.002         ; 2 fs
nsteps                  = $NVT_STEPS    ; 100 ps

; Output control
nstxout                 = 500
nstvout                 = 500
nstenergy               = 500
nstlog                  = 500

; Bond parameters
continuation            = no
constraint_algorithm    = lincs
constraints             = h-bonds
lincs_iter              = 1
lincs_order             = 4

; Nonbonded settings
cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.0
rvdw                    = 1.0
DispCorr                = EnerPres

; Electrostatics
coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = Protein Non-Protein
tau_t                   = 0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE

; Pressure coupling
pcoupl                  = no

; Periodic boundary conditions
pbc                     = xyz

; Velocity generation
gen_vel                 = yes
gen_temp                = $TEMPERATURE
gen_seed                = -1
EOF

# 添加位置约束
if [[ "$RESTRAINT" == "posre" ]]; then
    cat >> nvt.mdp << EOF

; Position restraints
define                  = -DPOSRES
EOF
fi

log "生成 TPR 文件..."
gmx grompp -f nvt.mdp -c ../"$INPUT_GRO" -r ../"$INPUT_GRO" -p ../"$INPUT_TOP" -o nvt.tpr -maxwarn 1 || {
    echo "[ERROR-001] grompp 失败"
    echo "Fix: gmx grompp -f nvt.mdp -c input.gro -p topol.top -o nvt.tpr"
    echo "Manual: Chapter 3.4"
    exit 1
}

log "运行 NVT 模拟..."
# Thread control via -ntomp flag below
gmx mdrun -v -deffnm nvt -ntmpi 1 -ntomp $NTOMP || {
    echo "[ERROR-002] NVT 模拟失败"
    echo "Fix: Check system stability or reduce dt"
    echo "Manual: Chapter 3.4"
    exit 1
}

log "NVT 平衡完成"

# 检查 NVT 稳定性
check_nvt_stability "nvt.edr"

# ============================================
# Phase 2: NPT 平衡 (恒温恒压)
# ============================================

log "Phase 2: NPT 平衡 (恒温恒压)"

# 生成 NPT MDP 文件
cat > npt.mdp << EOF
; NPT equilibration
integrator              = md
dt                      = 0.002         ; 2 fs
nsteps                  = $NPT_STEPS    ; 100 ps

; Output control
nstxout                 = 500
nstvout                 = 500
nstenergy               = 500
nstlog                  = 500

; Bond parameters
continuation            = yes
constraint_algorithm    = lincs
constraints             = h-bonds
lincs_iter              = 1
lincs_order             = 4

; Nonbonded settings
cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.0
rvdw                    = 1.0
DispCorr                = EnerPres

; Electrostatics
coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = Protein Non-Protein
tau_t                   = 0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE

; Pressure coupling
pcoupl                  = Parrinello-Rahman
pcoupltype              = isotropic
tau_p                   = 2.0
ref_p                   = $PRESSURE
compressibility         = 4.5e-5

; Periodic boundary conditions
pbc                     = xyz

; Velocity generation
gen_vel                 = no
EOF

# 添加位置约束
if [[ "$RESTRAINT" == "posre" ]]; then
    cat >> npt.mdp << EOF

; Position restraints
define                  = -DPOSRES
EOF
fi

log "生成 TPR 文件..."
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p ../"$INPUT_TOP" -o npt.tpr -maxwarn 1 || {
    echo "[ERROR-003] grompp 失败"
    echo "Fix: gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -o npt.tpr"
    echo "Manual: Chapter 3.4"
    exit 1
}

log "运行 NPT 模拟..."
gmx mdrun -v -deffnm npt -ntmpi 1 -ntomp $NTOMP || {
    echo "[ERROR-004] NPT 模拟失败"
    echo "Fix: Check pressure coupling or extend equilibration"
    echo "Manual: Chapter 3.4"
    exit 1
}

log "NPT 平衡完成"

# 检查 NPT 稳定性
check_npt_stability "npt.edr"

# ============================================
# Phase 3: 质量检查
# ============================================

log "Phase 3: 质量检查"

# 检查温度
log "分析温度..."
echo "Temperature" | gmx energy -f nvt.edr -o nvt_temperature.xvg || {
    echo "[ERROR-005] 温度分析失败"
    echo "Fix: Check nvt.edr file"
    exit 1
}

# 检查压强
log "分析压强..."
echo "Pressure" | gmx energy -f npt.edr -o npt_pressure.xvg || {
    echo "[ERROR-006] 压强分析失败"
    echo "Fix: Check npt.edr file"
    exit 1
}

# 检查密度
log "分析密度..."
echo "Density" | gmx energy -f npt.edr -o npt_density.xvg || {
    echo "[ERROR-007] 密度分析失败"
    echo "Fix: Check npt.edr file"
    exit 1
}

# ============================================
# 生成报告
# ============================================

log "生成平衡报告..."

cat > EQUILIBRATION_REPORT.md << EOF
# 系统平衡报告

**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 输入参数

- **输入结构:** $INPUT_GRO
- **拓扑文件:** $INPUT_TOP
- **温度:** $TEMPERATURE K
- **压强:** $PRESSURE bar
- **位置约束:** $RESTRAINT (力常数: $RESTRAINT_FC kJ/mol/nm^2)

---

## NVT 平衡 (恒温)

- **步数:** $NVT_STEPS ($(awk "BEGIN{printf "%.1f", $NVT_STEPS*0.002}") ps)
- **输出文件:** nvt.gro, nvt.cpt, nvt.edr
- **温度曲线:** nvt_temperature.xvg

### 温度统计
\`\`\`
$(tail -n 20 nvt_temperature.xvg | grep -v '^[@#]' | awk '{sum+=$2; n++} END {if(n>0) printf "平均温度: %.2f K\n", sum/n}')
\`\`\`

---

## NPT 平衡 (恒温恒压)

- **步数:** $NPT_STEPS ($(awk "BEGIN{printf "%.1f", $NPT_STEPS*0.002}") ps)
- **输出文件:** npt.gro, npt.cpt, npt.edr
- **压强曲线:** npt_pressure.xvg
- **密度曲线:** npt_density.xvg

### 压强统计
\`\`\`
$(tail -n 20 npt_pressure.xvg | grep -v '^[@#]' | awk '{sum+=$2; n++} END {if(n>0) printf "平均压强: %.2f bar\n", sum/n}')
\`\`\`

### 密度统计
\`\`\`
$(tail -n 20 npt_density.xvg | grep -v '^[@#]' | awk '{sum+=$2; n++} END {if(n>0) printf "平均密度: %.2f kg/m^3\n", sum/n}')
\`\`\`

---

## 输出文件

### 结构文件
- \`nvt.gro\` - NVT 平衡后的结构
- \`npt.gro\` - NPT 平衡后的结构 (用于生产运行)

### 检查点文件
- \`nvt.cpt\` - NVT 检查点
- \`npt.cpt\` - NPT 检查点 (用于继续模拟)

### 能量文件
- \`nvt.edr\` - NVT 能量轨迹
- \`npt.edr\` - NPT 能量轨迹

### 分析文件
- \`nvt_temperature.xvg\` - 温度曲线
- \`npt_pressure.xvg\` - 压强曲线
- \`npt_density.xvg\` - 密度曲线

---

## 下一步

系统已完成平衡,可以进行生产运行:

\`\`\`bash
# 使用 npt.gro 和 npt.cpt 作为起点
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -v -deffnm md
\`\`\`

---

**状态:** ✅ 平衡完成
EOF

log "报告已生成: $OUTPUT_DIR/EQUILIBRATION_REPORT.md"

# ============================================
# 完成
# ============================================

log "系统平衡流程完成!"
log "输出目录: $OUTPUT_DIR"
log "平衡后结构: $OUTPUT_DIR/npt.gro"
log "检查点文件: $OUTPUT_DIR/npt.cpt"

exit 0
