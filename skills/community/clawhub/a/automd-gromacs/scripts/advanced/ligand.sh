#!/bin/bash
# GROMACS Ligand-Protein Binding Script
# 配体-蛋白质结合模拟
# 依赖: gmx, acpype (auto-install)
# 输出: 平衡后复合物结构

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
        acpype -i "$ligand_file" -n 0 -o gmx &> acpype.log && {
            cp *.acpype/*_GMX.gro ligand.gro 2>/dev/null || cp *.acpype/*.gro ligand.gro
            cp *.acpype/*_GMX.itp ligand.itp 2>/dev/null || cp *.acpype/*.itp ligand.itp
            echo "✅ ACPYPE parameterization successful"
            return 0
        }
    fi
    
    # 方案 3: antechamber
    if command -v antechamber &> /dev/null || auto_install_dependencies ambertools; then
        echo "[AUTO-FIX] Parameterizing with antechamber..."
        antechamber -i "$ligand_file" -fi pdb -o ligand.mol2 -fo mol2 -c bcc &> antechamber.log && {
            echo "✅ antechamber parameterization successful"
            echo "Note: Manual conversion to GROMACS format required"
            return 0
        }
    fi
    
    # 方案 4: 明确错误
    echo "[ERROR-002] 所有参数化方法失败"
    echo "Fix: conda install -c conda-forge acpype"
    echo "Or: 提供 ligand.gro & ligand.itp"
    echo "Tools: ACPYPE, LigParGen, CGenFF"
    return 1
}

# ============================================
# 配置参数
# ============================================

INPUT_PROTEIN="${INPUT_PROTEIN:-protein.pdb}"
INPUT_LIGAND="${INPUT_LIGAND:-ligand.pdb}"
OUTPUT_DIR="${OUTPUT_DIR:-ligand_binding}"

# 系统参数
FORCE_FIELD="${FORCE_FIELD:-amber99sb-ildn}"
WATER_MODEL="${WATER_MODEL:-tip3p}"
BOX_TYPE="${BOX_TYPE:-dodecahedron}"
BOX_DISTANCE="${BOX_DISTANCE:-1.0}"
ION_CONCENTRATION="${ION_CONCENTRATION:-0.15}"

# 平衡参数
EM_STEPS="${EM_STEPS:-50000}"
NVT_STEPS="${NVT_STEPS:-50000}"
NPT_STEPS="${NPT_STEPS:-50000}"
MD_STEPS="${MD_STEPS:-5000000}"
TEMPERATURE="${TEMPERATURE:-300}"
PRESSURE="${PRESSURE:-1.0}"

# 约束参数
RESTRAINT_PROTEIN="${RESTRAINT_PROTEIN:-yes}"
RESTRAINT_LIGAND="${RESTRAINT_LIGAND:-yes}"
RESTRAINT_FC="${RESTRAINT_FC:-1000}"

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

log "开始配体-蛋白质结合模拟流程"
log "输入: $INPUT_PROTEIN, $INPUT_LIGAND"

check_file "$INPUT_PROTEIN"
check_file "$INPUT_LIGAND"

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# ============================================
# Phase 1: 蛋白质准备
# ============================================

log "Phase 1: 蛋白质准备"

# 生成拓扑: pdb → gro + top
# 依赖: protein.pdb
# 输出: protein.gro, protein.top
log "生成蛋白质拓扑..."
echo "1" | gmx pdb2gmx -f ../"$INPUT_PROTEIN" -o protein.gro -p protein.top -water "$WATER_MODEL" -ff "$FORCE_FIELD" -ignh || error "[ERROR-001] 蛋白质拓扑生成失败"

log "蛋白质准备完成"

# ============================================
# Phase 2: 配体准备
# ============================================

log "Phase 2: 配体准备"

# 参数化配体: ligand.pdb → ligand.gro + ligand.itp
# 依赖: acpype 或 antechamber
# 输出: ligand.gro, ligand.itp
parameterize_ligand "../$INPUT_LIGAND" || {
    log "请准备以下文件:"
    log "  - ligand.gro (配体坐标)"
    log "  - ligand.itp (配体拓扑)"
    log ""
    log "推荐工具:"
    log "  - ACPYPE: https://github.com/alanwilter/acpype"
    log "  - LigParGen: http://zarbi.chem.yale.edu/ligpargen/"
    log "  - CGenFF: https://cgenff.umaryland.edu/"
    error "[ERROR-003] 配体文件缺失"
}

log "配体准备完成"

# ============================================
# Phase 3: 复合物构建
# ============================================

log "Phase 3: 复合物构建"

# 合并蛋白质和配体: protein.gro + ligand.gro → complex.gro
# 依赖: protein.gro, ligand.gro
# 输出: complex.gro
log "合并蛋白质和配体..."

if [[ -f "ligand.gro" ]]; then
    PROTEIN_ATOMS=$(head -2 protein.gro | tail -1 | awk '{print $1}')
    LIGAND_ATOMS=$(head -2 ligand.gro | tail -1 | awk '{print $1}')
    TOTAL_ATOMS=$((PROTEIN_ATOMS + LIGAND_ATOMS))
    
    {
        echo "Protein-Ligand Complex"
        echo "$TOTAL_ATOMS"
        tail -n +3 protein.gro | head -n -1
        tail -n +3 ligand.gro | head -n -1
        tail -1 protein.gro
    } > complex.gro
    
    log "复合物构建完成 (简单合并)"
else
    error "[ERROR-004] ligand.gro 不存在"
fi

# 生成复合物拓扑
log "生成复合物拓扑..."
cat > topol.top << EOF
; Protein-Ligand Complex Topology

#include "$FORCE_FIELD.ff/forcefield.itp"

#include "protein.top"

#include "ligand.itp"

#include "$FORCE_FIELD.ff/$WATER_MODEL.itp"

#ifdef POSRES_WATER
[ position_restraints ]
;  i funct       fcx        fcy        fcz
   1    1       1000       1000       1000
#endif

#include "$FORCE_FIELD.ff/ions.itp"

[ system ]
Protein-Ligand Complex

[ molecules ]
Protein_chain_A     1
LIG                 1
EOF

log "复合物构建完成"

# ============================================
# Phase 4: 溶剂化和离子化
# ============================================

log "Phase 4: 溶剂化和离子化"

# 定义盒子: complex.gro → complex_box.gro
# 参数: BOX_DISTANCE, BOX_TYPE
# 输出: complex_box.gro
log "定义模拟盒子..."
gmx editconf -f complex.gro -o complex_box.gro -c -d "$BOX_DISTANCE" -bt "$BOX_TYPE" || error "[ERROR-004] 盒子定义失败"

# 溶剂化: complex_box.gro → complex_solvated.gro
# 依赖: topol.top
# 输出: complex_solvated.gro
log "添加溶剂..."
gmx solvate -cp complex_box.gro -cs spc216.gro -o complex_solvated.gro -p topol.top || error "[ERROR-005] 溶剂化失败"

# 添加离子: complex_solvated.gro → complex_ions.gro
# 参数: ION_CONCENTRATION
# 输出: complex_ions.gro
log "添加离子..."
cat > ions.mdp << EOF
integrator  = steep
emtol       = 1000.0
emstep      = 0.01
nsteps      = 50000
nstlist     = 1
cutoff-scheme = Verlet
ns_type     = grid
coulombtype = PME
rcoulomb    = 1.2
rvdw        = 1.2
pbc         = xyz
EOF

gmx grompp -f ions.mdp -c complex_solvated.gro -p topol.top -o ions.tpr -maxwarn 2 || error "[ERROR-006] ions grompp 失败"
echo "SOL" | gmx genion -s ions.tpr -o complex_ions.gro -p topol.top -pname NA -nname CL -neutral -conc "$ION_CONCENTRATION" || error "[ERROR-007] 离子添加失败"

log "溶剂化和离子化完成"

# ============================================
# Phase 5: 能量最小化
# ============================================

log "Phase 5: 能量最小化"

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
DispCorr                = EnerPres

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

pbc                     = xyz
EOF

log "运行能量最小化..."
gmx grompp -f em.mdp -c complex_ions.gro -p topol.top -o em.tpr -maxwarn 2 || error "[ERROR-008] em grompp 失败"
# Thread control via -ntomp flag below
gmx mdrun -v -deffnm em -ntmpi 1 -ntomp $NTOMP || error "[ERROR-009] 能量最小化失败"

log "能量最小化完成"

# ============================================
# Phase 6: NVT 平衡
# ============================================

log "Phase 6: NVT 平衡"

cat > nvt.mdp << EOF
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
DispCorr                = EnerPres

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

tcoupl                  = V-rescale
tc-grps                 = Protein_LIG Water_and_ions
tau_t                   = 0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE

pcoupl                  = no

pbc                     = xyz

gen_vel                 = yes
gen_temp                = $TEMPERATURE
gen_seed                = -1
EOF

if [[ "$RESTRAINT_PROTEIN" == "yes" ]] || [[ "$RESTRAINT_LIGAND" == "yes" ]]; then
    echo "" >> nvt.mdp
    echo "define = -DPOSRES" >> nvt.mdp
fi

log "运行 NVT 平衡..."
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr -maxwarn 2 || error "[ERROR-010] nvt grompp 失败"
gmx mdrun -v -deffnm nvt -ntmpi 1 -ntomp $NTOMP || error "[ERROR-011] NVT 平衡失败"

log "NVT 平衡完成"

# ============================================
# Phase 7: NPT 平衡
# ============================================

log "Phase 7: NPT 平衡"

cat > npt.mdp << EOF
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
DispCorr                = EnerPres

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

tcoupl                  = V-rescale
tc-grps                 = Protein_LIG Water_and_ions
tau_t                   = 0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE

pcoupl                  = Parrinello-Rahman
pcoupltype              = isotropic
tau_p                   = 2.0
ref_p                   = $PRESSURE
compressibility         = 4.5e-5

pbc                     = xyz

gen_vel                 = no
EOF

if [[ "$RESTRAINT_PROTEIN" == "yes" ]] || [[ "$RESTRAINT_LIGAND" == "yes" ]]; then
    echo "" >> npt.mdp
    echo "define = -DPOSRES" >> npt.mdp
fi

log "运行 NPT 平衡..."
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr -maxwarn 2 || error "[ERROR-012] npt grompp 失败"
gmx mdrun -v -deffnm npt -ntmpi 1 -ntomp $NTOMP || error "[ERROR-013] NPT 平衡失败"

log "NPT 平衡完成"

# ============================================
# Phase 8: 生产运行 (可选)
# ============================================

if [[ "$MD_STEPS" -gt 0 ]]; then
    log "Phase 8: 生产运行"
    
    cat > md.mdp << EOF
integrator              = md
dt                      = 0.002
nsteps                  = $MD_STEPS

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
DispCorr                = EnerPres

coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

tcoupl                  = V-rescale
tc-grps                 = Protein_LIG Water_and_ions
tau_t                   = 0.1     0.1
ref_t                   = $TEMPERATURE $TEMPERATURE

pcoupl                  = Parrinello-Rahman
pcoupltype              = isotropic
tau_p                   = 2.0
ref_p                   = $PRESSURE
compressibility         = 4.5e-5

pbc                     = xyz

gen_vel                 = no
EOF

    log "运行生产模拟 ($(awk "BEGIN{printf "%.1f", ($MD_STEPS * 0.002 / 1000)}" ) ns)..."
    gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr -maxwarn 2 || error "[ERROR-014] md grompp 失败"
    gmx mdrun -v -deffnm md -ntmpi 1 -ntomp $NTOMP || error "[ERROR-015] 生产运行失败"
    
    log "生产运行完成"
fi

# ============================================
# 生成报告
# ============================================

log "生成分析报告..."

cat > LIGAND_BINDING_REPORT.md << EOF
# 配体-蛋白质结合模拟报告

**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 输入参数

- **蛋白质结构:** $INPUT_PROTEIN
- **配体结构:** $INPUT_LIGAND
- **蛋白质力场:** $FORCE_FIELD
- **水模型:** $WATER_MODEL
- **盒子类型:** $BOX_TYPE
- **盒子边距:** $BOX_DISTANCE nm
- **离子浓度:** $ION_CONCENTRATION M

---

## 模拟参数

- **温度:** $TEMPERATURE K
- **压强:** $PRESSURE bar
- **能量最小化:** $EM_STEPS 步
- **NVT 平衡:** $NVT_STEPS 步 ($(awk "BEGIN{printf "%.1f", ($NVT_STEPS * 0.002)}" ) ps)
- **NPT 平衡:** $NPT_STEPS 步 ($(awk "BEGIN{printf "%.1f", ($NPT_STEPS * 0.002)}" ) ps)
- **生产运行:** $MD_STEPS 步 ($(awk "BEGIN{printf "%.1f", ($MD_STEPS * 0.002 / 1000)}" ) ns)

---

## 输出文件

### 结构文件
- \`complex.gro\` - 复合物初始结构
- \`complex_ions.gro\` - 溶剂化和离子化后结构
- \`em.gro\` - 能量最小化后结构
- \`nvt.gro\` - NVT 平衡后结构
- \`npt.gro\` - NPT 平衡后结构 (用于生产运行)
- \`md.gro\` - 生产运行最终结构

### 拓扑文件
- \`topol.top\` - 系统拓扑
- \`protein.top\` - 蛋白质拓扑
- \`ligand.itp\` - 配体拓扑

### 轨迹文件
- \`nvt.xtc\` - NVT 轨迹
- \`npt.xtc\` - NPT 轨迹
- \`md.xtc\` - 生产运行轨迹

---

## 结合分析

### 1. 配体 RMSD
\`\`\`bash
echo "LIG" | gmx rms -s md.tpr -f md.xtc -o ligand_rmsd.xvg
\`\`\`

### 2. 蛋白质-配体距离
\`\`\`bash
echo "Protein LIG" | gmx mindist -s md.tpr -f md.xtc -od mindist.xvg -pi
\`\`\`

### 3. 氢键分析
\`\`\`bash
echo "Protein LIG" | gmx hbond -s md.tpr -f md.xtc -num hbond.xvg
\`\`\`

### 4. 结合能估算 (MM-PBSA)
\`\`\`bash
# 使用 g_mmpbsa 或 gmx_MMPBSA
\`\`\`

### 5. 接触图
\`\`\`bash
echo "Protein LIG" | gmx mdmat -s md.tpr -f md.xtc -mean mean_contacts.xpm
\`\`\`

---

## 可视化

### VMD 查看复合物
\`\`\`bash
vmd npt.gro md.xtc
\`\`\`

### PyMOL 查看结合模式
\`\`\`bash
pymol npt.gro
\`\`\`

---

## 下一步

### 延长模拟时间
\`\`\`bash
gmx mdrun -v -deffnm md -cpi md.cpt -nsteps 10000000
\`\`\`

### 结合自由能计算
\`\`\`bash
# 使用 freeenergy.sh 或 umbrella.sh
\`\`\`

### 多副本模拟
\`\`\`bash
for i in {1..5}; do
    mkdir replica_\$i
    cd replica_\$i
    gmx grompp -f md.mdp -c ../npt.gro -t ../npt.cpt -p ../topol.top -o md.tpr
    gmx mdrun -v -deffnm md
    cd ..
done
\`\`\`

---

**状态:** ✅ 模拟完成
EOF

log "报告已生成: $OUTPUT_DIR/LIGAND_BINDING_REPORT.md"

# ============================================
# 完成
# ============================================

log "配体-蛋白质结合模拟流程完成!"
log "输出目录: $OUTPUT_DIR"
log "平衡后结构: $OUTPUT_DIR/npt.gro"
log "检查点文件: $OUTPUT_DIR/npt.cpt"

exit 0
