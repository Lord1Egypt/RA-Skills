#!/bin/bash
# GROMACS Membrane Protein Script
# 膜蛋白模拟流程
# 依赖: gmx, insane (auto-install)
# 输出: 平衡后膜蛋白系统

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
# 膜构建 (多方案尝试)
# ============================================
build_membrane() {
    local protein_gro="$1"
    local box_x="$2"
    local box_y="$3"
    local box_z="$4"
    
    # 方案 1: insane
    if command -v insane &> /dev/null || auto_install_dependencies insane; then
        echo "[AUTO-FIX] Building membrane with insane..."
        insane -f "$protein_gro" -o system_membrane.gro -p topol_membrane.top \
               -l "$MEMBRANE_TYPE" -x "$box_x" -y "$box_y" -z "$box_z" \
               -sol -salt "$ION_CONCENTRATION" &> insane.log && {
            echo "✅ insane membrane build successful"
            return 0
        }
    fi
    
    # 方案 2: CHARMM-GUI 提示
    echo "[ERROR-004] 膜构建失败"
    echo "Fix: conda install -c conda-forge insane"
    echo "Or: 使用 CHARMM-GUI (http://www.charmm-gui.org/)"
    echo "Or: 提供预构建膜系统"
    return 1
}

# ============================================
# 配置参数
# ============================================

INPUT_PDB="${INPUT_PDB:-protein.pdb}"
OUTPUT_DIR="${OUTPUT_DIR:-membrane}"

# 膜参数 (Manual 7.3)
# POPC: 常用磷脂 (生理)
# POPE: 细菌膜
# DPPC: 凝胶相
MEMBRANE_TYPE="${MEMBRANE_TYPE:-POPC}"
MEMBRANE_AREA="${MEMBRANE_AREA:-auto}"
MEMBRANE_THICKNESS="${MEMBRANE_THICKNESS:-4.0}"

# 系统参数
WATER_THICKNESS="${WATER_THICKNESS:-2.0}"
ION_CONCENTRATION="${ION_CONCENTRATION:-0.15}"
FORCE_FIELD="${FORCE_FIELD:-charmm36-jul2022}"

# 平衡参数
EM_STEPS="${EM_STEPS:-50000}"
NVT_STEPS="${NVT_STEPS:-50000}"
NPT_STEPS="${NPT_STEPS:-50000}"
TEMPERATURE="${TEMPERATURE:-310}"  # 膜蛋白常用 310K (生理)
PRESSURE="${PRESSURE:-1.0}"

# 约束参数 (Manual 3.12)
# 分阶段释放: 避免膜变形
# 初始约束: 4000 kJ/mol/nm² (强)
# 逐步减半: 4000 → 2000 → 1000 → 0
RESTRAINT_STAGES="${RESTRAINT_STAGES:-3}"
RESTRAINT_FC_INIT="${RESTRAINT_FC_INIT:-4000}"

NTOMP="${NTOMP:-2}"

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
# 前置检查
# ============================================

log "开始膜蛋白模拟流程"
log "输入: $INPUT_PDB"

check_file "$INPUT_PDB"

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# ============================================
# Phase 1: 蛋白质准备
# ============================================

log "Phase 1: 蛋白质准备"

# 生成拓扑: pdb → gro + top
# 依赖: protein.pdb
# 输出: protein.gro, topol.top
log "生成蛋白质拓扑..."
echo "1" | gmx pdb2gmx -f ../"$INPUT_PDB" -o protein.gro -p topol.top -water tip3p -ff "$FORCE_FIELD" -ignh || error "[ERROR-001] 拓扑生成失败"

# 定位蛋白质到膜平面: 主轴对齐
# 依赖: protein.gro
# 输出: protein_centered.gro
log "定位蛋白质到膜平面..."
gmx editconf -f protein.gro -o protein_centered.gro -center 0 0 0 -princ || error "[ERROR-002] 蛋白质定位失败"

log "蛋白质准备完成"

# ============================================
# Phase 2: 膜构建
# ============================================

log "Phase 2: 膜构建"

# 计算膜面积: 根据蛋白质尺寸
# 规则: 蛋白质尺寸 + 2.0 nm 缓冲
if [[ "$MEMBRANE_AREA" == "auto" ]]; then
    PROTEIN_SIZE=$(gmx editconf -f protein_centered.gro -o /dev/null 2>&1 | grep "box vectors" | awk '{print $4, $5}')
    BOX_X=$(echo "$PROTEIN_SIZE" | awk '{print $1 + 2.0}')
    BOX_Y=$(echo "$PROTEIN_SIZE" | awk '{print $2 + 2.0}')
    log "自动计算膜面积: $BOX_X x $BOX_Y nm"
else
    BOX_X=$MEMBRANE_AREA
    BOX_Y=$MEMBRANE_AREA
fi

# 计算盒子 Z 尺寸
BOX_Z=$(awk "BEGIN{printf "%d", $MEMBRANE_THICKNESS + 2 * $WATER_THICKNESS}" )

# 定义盒子: protein_centered.gro → protein_box.gro
# 参数: BOX_X, BOX_Y, BOX_Z
# 输出: protein_box.gro
log "构建模拟盒子: $BOX_X x $BOX_Y x $BOX_Z nm"
gmx editconf -f protein_centered.gro -o protein_box.gro -box $BOX_X $BOX_Y $BOX_Z -c || error "[ERROR-003] 盒子构建失败"

# 构建膜: protein_box.gro → system_membrane.gro
# 依赖: insane
# 输出: system_membrane.gro, topol_membrane.top
build_membrane "protein_box.gro" "$BOX_X" "$BOX_Y" "$BOX_Z" || error "[ERROR-004] 膜构建失败"

log "膜构建完成"

# ============================================
# Phase 3: 能量最小化
# ============================================

log "Phase 3: 能量最小化"

cat > em.mdp << EOF
integrator              = steep
emtol                   = 1000.0
emstep                  = 0.01
nsteps                  = $EM_STEPS

nstlog                  = 1000
nstenergy               = 1000

cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.2
rvdw                    = 1.2
DispCorr                = no

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.12

pbc                     = xyz
EOF

log "运行能量最小化..."
gmx grompp -f em.mdp -c system_membrane.gro -p topol_membrane.top -o em.tpr -maxwarn 2 || error "[ERROR-005] grompp 失败"
# Thread control via -ntomp flag below
gmx mdrun -v -deffnm em -ntmpi 1 -ntomp $NTOMP || error "[ERROR-006] 能量最小化失败"

log "能量最小化完成"

# ============================================
# Phase 4: 分阶段平衡
# ============================================

log "Phase 4: 分阶段平衡"

PREV_GRO="em.gro"
PREV_CPT=""

for stage in $(seq 1 $RESTRAINT_STAGES); do
    log "平衡阶段 $stage/$RESTRAINT_STAGES"
    
    # 计算约束力常数: 逐步减半
    # 阶段 1: 4000, 阶段 2: 2000, 阶段 3: 1000
    RESTRAINT_FC=$(awk "BEGIN{printf "%d", scale=0; $RESTRAINT_FC_INIT / (2^($stage-1))}" )
    log "约束力常数: $RESTRAINT_FC kJ/mol/nm²"
    
    # NVT 平衡
    log "阶段 $stage: NVT 平衡..."
    
    cat > nvt_stage${stage}.mdp << EOF
; NVT equilibration - Stage $stage
integrator              = md
dt                      = 0.002
nsteps                  = $NVT_STEPS

nstxout                 = 0
nstvout                 = 0
nstenergy               = 5000
nstlog                  = 5000
nstxout-compressed      = 5000

continuation            = no
constraint_algorithm    = lincs
constraints             = h-bonds
lincs_iter              = 1
lincs_order             = 4

cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.2
rvdw                    = 1.2
DispCorr                = no

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.12

; 温度耦合 (Manual 3.4.4)
; 分组: Protein, Membrane, Water_and_ions
; 原因: 不同组分热容不同
tcoupl                  = V-rescale
tc-grps                 = Protein Membrane Water_and_ions
tau_t                   = 0.1     0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE $TEMPERATURE

pcoupl                  = no

pbc                     = xyz

gen_vel                 = yes
gen_temp                = $TEMPERATURE
gen_seed                = -1

; 位置约束 (Manual 3.12)
define                  = -DPOSRES -DPOSRES_FC_BB=$RESTRAINT_FC -DPOSRES_FC_SC=$RESTRAINT_FC
EOF

    gmx grompp -f nvt_stage${stage}.mdp -c $PREV_GRO -p topol_membrane.top -o nvt_stage${stage}.tpr -maxwarn 2 || error "[ERROR-007] NVT grompp 失败"
    gmx mdrun -v -deffnm nvt_stage${stage} -ntmpi 1 -ntomp $NTOMP || error "[ERROR-008] NVT 模拟失败"
    
    # NPT 平衡
    log "阶段 $stage: NPT 平衡..."
    
    cat > npt_stage${stage}.mdp << EOF
; NPT equilibration - Stage $stage
integrator              = md
dt                      = 0.002
nsteps                  = $NPT_STEPS

nstxout                 = 0
nstvout                 = 0
nstenergy               = 5000
nstlog                  = 5000
nstxout-compressed      = 5000

continuation            = yes
constraint_algorithm    = lincs
constraints             = h-bonds
lincs_iter              = 1
lincs_order             = 4

cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.2
rvdw                    = 1.2
DispCorr                = no

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.12

tcoupl                  = V-rescale
tc-grps                 = Protein Membrane Water_and_ions
tau_t                   = 0.1     0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE $TEMPERATURE

; 压力耦合 (Manual 3.4.5)
; semi-isotropic: XY 和 Z 独立
; 原因: 膜在 XY 平面可压缩, Z 方向受限
pcoupl                  = Parrinello-Rahman
pcoupltype              = semi-isotropic
tau_p                   = 5.0
ref_p                   = $PRESSURE $PRESSURE
compressibility         = 4.5e-5 4.5e-5

pbc                     = xyz

gen_vel                 = no

define                  = -DPOSRES -DPOSRES_FC_BB=$RESTRAINT_FC -DPOSRES_FC_SC=$RESTRAINT_FC
EOF

    gmx grompp -f npt_stage${stage}.mdp -c nvt_stage${stage}.gro -t nvt_stage${stage}.cpt -p topol_membrane.top -o npt_stage${stage}.tpr -maxwarn 2 || error "[ERROR-009] NPT grompp 失败"
    gmx mdrun -v -deffnm npt_stage${stage} -ntmpi 1 -ntomp $NTOMP || error "[ERROR-010] NPT 模拟失败"
    
    PREV_GRO="npt_stage${stage}.gro"
    PREV_CPT="npt_stage${stage}.cpt"
    
    log "阶段 $stage 完成"
done

log "分阶段平衡完成"

# ============================================
# 生成报告
# ============================================

log "生成分析报告..."

cat > MEMBRANE_REPORT.md << EOF
# 膜蛋白模拟报告

**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 输入参数

- **蛋白质结构:** $INPUT_PDB
- **膜类型:** $MEMBRANE_TYPE
- **膜面积:** $BOX_X x $BOX_Y nm
- **膜厚度:** $MEMBRANE_THICKNESS nm
- **水层厚度:** $WATER_THICKNESS nm
- **离子浓度:** $ION_CONCENTRATION M
- **力场:** $FORCE_FIELD

---

## 系统设置

- **盒子尺寸:** $BOX_X x $BOX_Y x $BOX_Z nm
- **温度:** $TEMPERATURE K (生理温度)
- **压强:** $PRESSURE bar (semi-isotropic)
- **约束阶段:** $RESTRAINT_STAGES
- **初始约束力常数:** $RESTRAINT_FC_INIT kJ/mol/nm²

---

## 平衡流程

### 能量最小化
- **步数:** $EM_STEPS
- **输出文件:** em.gro, em.edr

### 分阶段平衡
EOF

for stage in $(seq 1 $RESTRAINT_STAGES); do
    RESTRAINT_FC=$(awk "BEGIN{printf "%d", scale=0; $RESTRAINT_FC_INIT / (2^($stage-1))}" )
    cat >> MEMBRANE_REPORT.md << EOF

#### 阶段 $stage
- **约束力常数:** $RESTRAINT_FC kJ/mol/nm²
- **NVT:** $NVT_STEPS 步 ($(awk "BEGIN{printf "%.1f", ($NVT_STEPS * 0.002)}" ) ps)
- **NPT:** $NPT_STEPS 步 ($(awk "BEGIN{printf "%.1f", ($NPT_STEPS * 0.002)}" ) ps)
- **输出文件:** nvt_stage${stage}.gro, npt_stage${stage}.gro
EOF
done

cat >> MEMBRANE_REPORT.md << EOF

---

## 输出文件

### 结构文件
- \`protein.gro\` - 蛋白质初始结构
- \`system_membrane.gro\` - 膜系统初始结构
- \`em.gro\` - 能量最小化后结构
- \`npt_stage${RESTRAINT_STAGES}.gro\` - 最终平衡结构 (用于生产运行)

### 拓扑文件
- \`topol.top\` - 蛋白质拓扑
- \`topol_membrane.top\` - 完整系统拓扑

### 检查点文件
- \`npt_stage${RESTRAINT_STAGES}.cpt\` - 最终检查点 (用于继续模拟)

---

## 质量检查

### 1. 检查能量最小化
\`\`\`bash
echo "Potential" | gmx energy -f em.edr -o potential.xvg
tail potential.xvg
\`\`\`

### 2. 检查温度稳定性
\`\`\`bash
echo "Temperature" | gmx energy -f npt_stage${RESTRAINT_STAGES}.edr -o temperature.xvg
xmgrace temperature.xvg
\`\`\`

### 3. 检查膜面积
\`\`\`bash
echo "Box-X Box-Y" | gmx energy -f npt_stage${RESTRAINT_STAGES}.edr -o box.xvg
xmgrace box.xvg
\`\`\`

### 4. 可视化检查
\`\`\`bash
vmd npt_stage${RESTRAINT_STAGES}.gro npt_stage${RESTRAINT_STAGES}.xtc
\`\`\`

---

## 下一步

### 生产运行
\`\`\`bash
gmx grompp -f md.mdp -c npt_stage${RESTRAINT_STAGES}.gro -t npt_stage${RESTRAINT_STAGES}.cpt -p topol_membrane.top -o md.tpr
gmx mdrun -v -deffnm md
\`\`\`

### 膜特异性分析
\`\`\`bash
# 膜厚度分析
gmx density -f md.xtc -s md.tpr -o density.xvg -d Z

# 脂质序参数
gmx order -f md.xtc -s md.tpr -o order.xvg

# 蛋白质-膜接触
gmx mindist -f md.xtc -s md.tpr -od mindist.xvg
\`\`\`

---

## 注意事项

### 膜蛋白特殊考虑
1. **温度:** 310 K (生理温度)
2. **压强耦合:** semi-isotropic (XY 和 Z 独立)
3. **约束释放:** 分阶段逐步释放,避免膜变形
4. **模拟时间:** 膜系统需要更长平衡时间 (至少 10 ns)

### 常见问题
- 膜破裂: 约束释放过快,需要更多阶段
- 蛋白质倾斜: 初始定位不正确,重新定位
- 水渗透: 膜厚度不足,增加脂质数量

---

**状态:** ✅ 平衡完成
EOF

log "报告已生成: $OUTPUT_DIR/MEMBRANE_REPORT.md"

# ============================================
# 完成
# ============================================

log "膜蛋白模拟流程完成!"
log "输出目录: $OUTPUT_DIR"
log "平衡后结构: $OUTPUT_DIR/npt_stage${RESTRAINT_STAGES}.gro"
log "检查点文件: $OUTPUT_DIR/npt_stage${RESTRAINT_STAGES}.cpt"

exit 0
