#!/bin/bash
# GROMACS Coarse-Grained Simulation
# 粗粒化模拟 - MARTINI力场和多尺度模拟
# 支持全原子→粗粒化转换、粗粒化模拟、反向映射

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_PDB="${INPUT_PDB:-protein.pdb}"      # 全原子PDB(AA→CG)
INPUT_GRO="${INPUT_GRO:-}"                 # 粗粒化GRO(直接CG)
INPUT_TOP="${INPUT_TOP:-}"                 # 拓扑文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-coarse-grained}"

# 工作模式
MODE="${MODE:-aa2cg}"                      # aa2cg/cg/backmapping/multiscale

# MARTINI力场版本
MARTINI_VERSION="${MARTINI_VERSION:-3}"    # 2/3 (MARTINI 2.x或3.x)
MARTINI_FF_DIR="${MARTINI_FF_DIR:-}"       # MARTINI力场目录(自动下载)

# 粗粒化参数
CG_WATER="${CG_WATER:-W}"                  # 粗粒化水模型(W/PW/SW)
CG_ION_CONC="${CG_ION_CONC:-0.15}"         # 离子浓度(M)
CG_BOX_DISTANCE="${CG_BOX_DISTANCE:-1.5}"  # 盒子边距(nm)
CG_BOX_TYPE="${CG_BOX_TYPE:-dodecahedron}" # 盒子类型

# 模拟参数
SIM_TIME="${SIM_TIME:-1000}"               # 模拟时间(ps)
DT="${DT:-0.020}"                          # 时间步长(ps,CG推荐20-30fs)
TEMPERATURE="${TEMPERATURE:-310}"          # 温度(K)
PRESSURE="${PRESSURE:-1.0}"                # 压力(bar)

# 能量最小化
EM_STEPS="${EM_STEPS:-5000}"
EM_TOL="${EM_TOL:-1000}"

# 平衡阶段
NVT_TIME="${NVT_TIME:-100}"                # NVT平衡时间(ps)
NPT_TIME="${NPT_TIME:-100}"                # NPT平衡时间(ps)

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

# 检查并安装MARTINI力场
check_martini_forcefield() {
    if [[ -z "$MARTINI_FF_DIR" ]]; then
        log "检查MARTINI力场..."
        
        # 检查常见位置
        local search_paths=(
            "/usr/share/gromacs/top/martini.ff"
            "$HOME/.gromacs/martini.ff"
            "./martini.ff"
            "$OUTPUT_DIR/martini.ff"
        )
        
        for path in "${search_paths[@]}"; do
            if [[ -d "$path" ]]; then
                MARTINI_FF_DIR="$path"
                log "[OK] 找到MARTINI力场: $path"
                return 0
            fi
        done
        
        log "[WARN] MARTINI力场未找到"

        if [[ "${AUTOMD_CG_ALLOW_DOWNLOAD:-0}" != "1" ]]; then
            log "[ERROR] MARTINI力场未安装"
            log "[INFO] 手动下载到任一搜索路径，或设 AUTOMD_CG_ALLOW_DOWNLOAD=1 启用自动下载"
            log "[INFO] 下载地址 (HTTPS): https://cgmartini.nl/index.php/force-field-parameters/martini3"
            error "MARTINI force field not found — install it or set AUTOMD_CG_ALLOW_DOWNLOAD=1"
        fi

        log "[AUTO-FIX] 尝试下载MARTINI力场..."
        
        mkdir -p "$OUTPUT_DIR/martini.ff"
        cd "$OUTPUT_DIR/martini.ff"
        
        if [[ "$MARTINI_VERSION" == "3" ]]; then
            # MARTINI 3
            log "下载MARTINI 3力场..."
            if command -v wget &> /dev/null; then
                wget -q https://cgmartini.nl/images/parameters/martini_v3.0.0/martini_v3.0.0.tar.gz -O martini3.tar.gz || {
                    log "[ERROR] 下载失败"
                    log "请手动下载: https://cgmartini.nl/index.php/force-field-parameters/martini3"
                    error "MARTINI 3力场不可用"
                }
                tar -xzf martini3.tar.gz
                rm martini3.tar.gz
            else
                log "[ERROR] wget未安装"
                log "解决方案:"
                log "1. 手动下载MARTINI力场到: $OUTPUT_DIR/martini.ff"
                log "2. 设置MARTINI_FF_DIR环境变量"
                error "无法自动下载MARTINI力场"
            fi
        else
            # MARTINI 2
            log "下载MARTINI 2力场..."
            if command -v wget &> /dev/null; then
                wget -q https://cgmartini.nl/images/parameters/martini_v2.2/martini_v2.2.tar.gz -O martini2.tar.gz || {
                    log "[ERROR] 下载失败"
                    log "请手动下载: https://cgmartini.nl/index.php/force-field-parameters/martini2"
                    error "MARTINI 2力场不可用"
                }
                tar -xzf martini2.tar.gz
                rm martini2.tar.gz
            else
                error "wget未安装且MARTINI力场不可用"
            fi
        fi
        
        MARTINI_FF_DIR="$OUTPUT_DIR/martini.ff"
        cd - > /dev/null
        log "[OK] MARTINI力场已下载: $MARTINI_FF_DIR"
    else
        [[ -d "$MARTINI_FF_DIR" ]] || error "MARTINI力场目录不存在: $MARTINI_FF_DIR"
        log "[OK] 使用MARTINI力场: $MARTINI_FF_DIR"
    fi
}

# 验证时间步长
validate_timestep() {
    # CG推荐: 20-30 fs
    if (( $(echo "$DT < 0.010" | bc -l) )); then
        log "[WARN] 时间步长过小 ($DT < 0.010 ps)"
        log "[AUTO-FIX] 增加到 0.020 ps (20 fs)"
        DT=0.020
    fi
    
    if (( $(echo "$DT > 0.040" | bc -l) )); then
        log "[WARN] 时间步长过大 ($DT > 0.040 ps)"
        log "[AUTO-FIX] 减少到 0.030 ps (30 fs)"
        DT=0.030
    fi
}

# 检查martinize工具
check_martinize() {
    if ! command -v martinize2 &> /dev/null && ! command -v martinize.py &> /dev/null; then
        log "[WARN] martinize工具未找到"
        
        if [[ "${AUTOMD_AUTO_INSTALL:-0}" != "1" ]]; then
            log "[ERROR] martinize 不可用"
            log "[INFO] 手动安装: pip3 install vermouth-martinize"
            log "[INFO] 或设 AUTOMD_AUTO_INSTALL=1 启用自动安装"
            error "martinize not available — install it or set AUTOMD_AUTO_INSTALL=1"
        fi
        
        log "[AUTO-FIX] 尝试安装martinize2..."
        
        if command -v pip3 &> /dev/null; then
            pip3 install vermouth-martinize 2>&1 | tail -5 || {
                log "[ERROR] 安装失败"
                log "解决方案:"
                log "1. 手动安装: pip3 install vermouth-martinize"
                log "2. 或使用旧版: git clone https://github.com/cgmartini/martinize.py"
                error "martinize不可用"
            }
            log "[OK] martinize2已安装"
        else
            error "pip3未安装，无法自动安装martinize"
        fi
    fi
    
    if command -v martinize2 &> /dev/null; then
        log "[OK] 使用martinize2"
        return 0
    elif command -v martinize.py &> /dev/null; then
        log "[OK] 使用martinize.py"
        return 0
    fi
}

# 失败重启
restart_from_checkpoint() {
    local stage=$1
    if [[ -f "${stage}.cpt" ]]; then
        log "[AUTO-FIX] 从检查点重启: $stage"
        gmx mdrun -v -deffnm "$stage" -cpi "${stage}.cpt" \
            -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a "${stage}.log"
        return $?
    fi
    return 1
}

# ============================================
# 全原子到粗粒化转换
# ============================================

aa_to_cg() {
    log "Phase 1: 全原子到粗粒化转换"
    
    check_file "$INPUT_PDB"
    check_martinize
    
    # 使用martinize转换
    log "运行martinize..."
    
    if command -v martinize2 &> /dev/null; then
        # MARTINI 3 (martinize2)
        martinize2 -f "$INPUT_PDB" -o cg_topol.top -x cg_protein.pdb \
            -ff martini3001 -elastic -ef 500 -el 0.5 -eu 0.9 -ea 0 -ep 0 \
            -scfix -cys auto 2>&1 | tee martinize.log || {
            log "[ERROR] martinize2失败"
            log "尝试使用基础参数..."
            martinize2 -f "$INPUT_PDB" -o cg_topol.top -x cg_protein.pdb \
                -ff martini3001 2>&1 | tee martinize.log || error "martinize2失败"
        }
    else
        # MARTINI 2 (martinize.py)
        martinize.py -f "$INPUT_PDB" -o cg_topol.top -x cg_protein.pdb \
            -ff martini22 -elastic -ef 500 -el 0.5 -eu 0.9 -ea 0 -ep 0 \
            -cys auto 2>&1 | tee martinize.log || {
            log "[ERROR] martinize.py失败"
            error "全原子到粗粒化转换失败"
        }
    fi
    
    [[ -f "cg_protein.pdb" ]] || error "粗粒化结构生成失败"
    [[ -f "cg_topol.top" ]] || error "粗粒化拓扑生成失败"
    
    log "[OK] 粗粒化转换完成"
    log "  结构: cg_protein.pdb"
    log "  拓扑: cg_topol.top"
    
    # 转换为GRO格式
    gmx editconf -f cg_protein.pdb -o cg_protein.gro 2>&1 | grep -E "WARNING|ERROR" || true
    INPUT_GRO="cg_protein.gro"
    INPUT_TOP="cg_topol.top"
}

# ============================================
# 系统准备
# ============================================

setup_cg_system() {
    log "Phase 2: 粗粒化系统准备"
    
    check_file "$INPUT_GRO"
    
    # 定义盒子
    log "定义模拟盒子..."
    gmx editconf -f "$INPUT_GRO" -o cg_box.gro \
        -c -d $CG_BOX_DISTANCE -bt $CG_BOX_TYPE 2>&1 | grep -E "WARNING|ERROR" || true
    
    [[ -f "cg_box.gro" ]] || error "盒子定义失败"
    
    # 溶剂化(粗粒化水)
    log "添加粗粒化水..."
    
    # 创建水模型配置
    cat > water.gro << EOF
Coarse-grained water
    1
    1${CG_WATER}      W    1   0.000   0.000   0.000
   1.0   1.0   1.0
EOF
    
    gmx solvate -cp cg_box.gro -cs water.gro -o cg_solv.gro -p "$INPUT_TOP" \
        2>&1 | tee solvate.log || {
        log "[WARN] 粗粒化溶剂化失败，尝试标准水模型..."
        gmx solvate -cp cg_box.gro -cs spc216.gro -o cg_solv.gro -p "$INPUT_TOP" \
            2>&1 | tee solvate.log || error "溶剂化失败"
    }
    
    [[ -f "cg_solv.gro" ]] || error "溶剂化失败"
    
    # 添加离子
    log "添加离子 (浓度: ${CG_ION_CONC}M)..."
    
    # 生成离子MDP
    cat > ions.mdp << EOF
integrator  = steep
nsteps      = 100
emtol       = 1000
cutoff-scheme = Verlet
coulombtype = reaction-field
rcoulomb    = 1.1
vdwtype     = cutoff
rvdw        = 1.1
EOF
    
    gmx grompp -f ions.mdp -c cg_solv.gro -p "$INPUT_TOP" -o ions.tpr -maxwarn 2 \
        2>&1 | grep -E "WARNING|ERROR" || true
    
    echo "SOL" | gmx genion -s ions.tpr -o cg_ions.gro -p "$INPUT_TOP" \
        -pname NA+ -nname CL- -neutral -conc $CG_ION_CONC 2>&1 | tee genion.log || {
        log "[WARN] 标准离子名称失败，尝试MARTINI离子..."
        echo "W" | gmx genion -s ions.tpr -o cg_ions.gro -p "$INPUT_TOP" \
            -pname NA -nname CL -neutral -conc $CG_ION_CONC 2>&1 | tee genion.log || {
            log "[WARN] 离子添加失败，继续不加离子..."
            cp cg_solv.gro cg_ions.gro
        }
    }
    
    [[ -f "cg_ions.gro" ]] || error "系统准备失败"
    log "[OK] 粗粒化系统准备完成"
}

# ============================================
# 能量最小化
# ============================================

run_em() {
    log "Phase 3: 能量最小化"
    
    cat > em.mdp << EOF
; Energy Minimization for Coarse-Grained System
integrator  = steep
nsteps      = $EM_STEPS
emtol       = $EM_TOL

; Output
nstlog      = 100
nstenergy   = 100

; Neighbor searching
cutoff-scheme = Verlet
nstlist     = 10
ns_type     = grid
pbc         = xyz

; Electrostatics (Reaction-Field for MARTINI)
coulombtype = reaction-field
rcoulomb    = 1.1
epsilon_r   = 15
epsilon_rf  = 0

; Van der Waals
vdwtype     = cutoff
vdw-modifier = Potential-shift
rvdw        = 1.1
EOF

    gmx grompp -f em.mdp -c cg_ions.gro -p "$INPUT_TOP" -o em.tpr -maxwarn 2 \
        2>&1 | grep -E "WARNING|ERROR|Fatal" || true
    
    [[ -f "em.tpr" ]] || error "EM预处理失败"
    
    gmx mdrun -v -deffnm em -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} \
        2>&1 | tee em.log || restart_from_checkpoint em || error "能量最小化失败"
    
    # 检查收敛
    if grep -q "converged to Fmax" em.log; then
        log "[OK] 能量最小化收敛"
    else
        log "[WARN] 能量最小化未完全收敛，但继续..."
    fi
}

# ============================================
# NVT平衡
# ============================================

run_nvt() {
    log "Phase 4: NVT平衡"
    
    local nvt_steps=$(awk "BEGIN{printf "%d", $NVT_TIME / $DT}" )
    
    cat > nvt.mdp << EOF
; NVT Equilibration for Coarse-Grained System
integrator  = md
dt          = $DT
nsteps      = $nvt_steps

; Output
nstlog      = 1000
nstenergy   = 1000
nstxout-compressed = 1000

; Neighbor searching
cutoff-scheme = Verlet
nstlist     = 10
pbc         = xyz

; Electrostatics
coulombtype = reaction-field
rcoulomb    = 1.1
epsilon_r   = 15
epsilon_rf  = 0

; Van der Waals
vdwtype     = cutoff
vdw-modifier = Potential-shift
rvdw        = 1.1

; Temperature coupling
tcoupl      = v-rescale
tc-grps     = System
tau_t       = 1.0
ref_t       = $TEMPERATURE

; Velocity generation
gen_vel     = yes
gen_temp    = $TEMPERATURE
gen_seed    = -1
EOF

    gmx grompp -f nvt.mdp -c em.gro -p "$INPUT_TOP" -o nvt.tpr -maxwarn 2 \
        2>&1 | grep -E "WARNING|ERROR|Fatal" || true
    
    [[ -f "nvt.tpr" ]] || error "NVT预处理失败"
    
    gmx mdrun -v -deffnm nvt -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} \
        2>&1 | tee nvt.log || restart_from_checkpoint nvt || error "NVT平衡失败"
    
    log "[OK] NVT平衡完成"
}

# ============================================
# NPT平衡
# ============================================

run_npt() {
    log "Phase 5: NPT平衡"
    
    local npt_steps=$(awk "BEGIN{printf "%d", $NPT_TIME / $DT}" )
    
    cat > npt.mdp << EOF
; NPT Equilibration for Coarse-Grained System
integrator  = md
dt          = $DT
nsteps      = $npt_steps

; Output
nstlog      = 1000
nstenergy   = 1000
nstxout-compressed = 1000

; Neighbor searching
cutoff-scheme = Verlet
nstlist     = 10
pbc         = xyz

; Electrostatics
coulombtype = reaction-field
rcoulomb    = 1.1
epsilon_r   = 15
epsilon_rf  = 0

; Van der Waals
vdwtype     = cutoff
vdw-modifier = Potential-shift
rvdw        = 1.1

; Temperature coupling
tcoupl      = v-rescale
tc-grps     = System
tau_t       = 1.0
ref_t       = $TEMPERATURE

; Pressure coupling
pcoupl      = parrinello-rahman
pcoupltype  = isotropic
tau_p       = 12.0
ref_p       = $PRESSURE
compressibility = 3e-4

; Velocity generation
gen_vel     = no
EOF

    gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p "$INPUT_TOP" -o npt.tpr -maxwarn 2 \
        2>&1 | grep -E "WARNING|ERROR|Fatal" || true
    
    [[ -f "npt.tpr" ]] || error "NPT预处理失败"
    
    gmx mdrun -v -deffnm npt -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} \
        2>&1 | tee npt.log || restart_from_checkpoint npt || error "NPT平衡失败"
    
    log "[OK] NPT平衡完成"
}

# ============================================
# 生产模拟
# ============================================

run_production() {
    log "Phase 6: 生产模拟"
    
    local prod_steps=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
    
    cat > md.mdp << EOF
; Production MD for Coarse-Grained System
integrator  = md
dt          = $DT
nsteps      = $prod_steps

; Output
nstlog      = 5000
nstenergy   = 5000
nstxout-compressed = 5000
compressed-x-grps = System

; Neighbor searching
cutoff-scheme = Verlet
nstlist     = 10
pbc         = xyz

; Electrostatics
coulombtype = reaction-field
rcoulomb    = 1.1
epsilon_r   = 15
epsilon_rf  = 0

; Van der Waals
vdwtype     = cutoff
vdw-modifier = Potential-shift
rvdw        = 1.1

; Temperature coupling
tcoupl      = v-rescale
tc-grps     = System
tau_t       = 1.0
ref_t       = $TEMPERATURE

; Pressure coupling
pcoupl      = parrinello-rahman
pcoupltype  = isotropic
tau_p       = 12.0
ref_p       = $PRESSURE
compressibility = 3e-4

; Velocity generation
gen_vel     = no
EOF

    gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p "$INPUT_TOP" -o md.tpr -maxwarn 2 \
        2>&1 | grep -E "WARNING|ERROR|Fatal" || true
    
    [[ -f "md.tpr" ]] || error "生产模拟预处理失败"
    
    gmx mdrun -v -deffnm md -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} \
        2>&1 | tee md.log || restart_from_checkpoint md || error "生产模拟失败"
    
    log "[OK] 生产模拟完成"
}

# ============================================
# 反向映射 (CG → AA)
# ============================================

backmapping() {
    log "Phase: 反向映射 (粗粒化 → 全原子)"
    
    check_file "$INPUT_GRO"
    
    log "[WARN] 反向映射需要专用工具"
    log "推荐工具:"
    log "1. backward.py (MARTINI官方)"
    log "   git clone https://github.com/Tsjerk/Backward"
    log "2. CG2AT"
    log "   pip install cg2at"
    log "3. MDAnalysis + 自定义脚本"
    
    if command -v backward.py &> /dev/null; then
        log "使用backward.py进行反向映射..."
        backward.py -f "$INPUT_GRO" -o aa_structure.gro 2>&1 | tee backward.log || {
            log "[ERROR] backward.py失败"
            error "反向映射失败"
        }
        log "[OK] 反向映射完成: aa_structure.gro"
    else
        log "[ERROR] backward.py未安装"
        log "安装: git clone https://github.com/Tsjerk/Backward && cd Backward && pip install ."
        error "反向映射工具不可用"
    fi
}

# ============================================
# 主流程
# ============================================

log "开始粗粒化模拟"
log "模式: $MODE"
log "MARTINI版本: $MARTINI_VERSION"

# 前置检查
validate_timestep
check_martini_forcefield

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 根据模式执行
case "$MODE" in
    aa2cg)
        log "全原子到粗粒化完整流程"
        aa_to_cg
        setup_cg_system
        run_em
        run_nvt
        run_npt
        run_production
        ;;
    cg)
        log "直接粗粒化模拟"
        [[ -n "$INPUT_GRO" ]] || error "需要提供INPUT_GRO"
        [[ -n "$INPUT_TOP" ]] || error "需要提供INPUT_TOP"
        cp "../$INPUT_GRO" .
        cp "../$INPUT_TOP" .
        setup_cg_system
        run_em
        run_nvt
        run_npt
        run_production
        ;;
    backmapping)
        log "反向映射模式"
        backmapping
        ;;
    multiscale)
        log "多尺度模拟"
        log "1. 全原子 → 粗粒化"
        aa_to_cg
        setup_cg_system
        run_em
        run_nvt
        run_npt
        run_production
        log "2. 粗粒化 → 全原子"
        INPUT_GRO="md.gro"
        backmapping
        ;;
    *)
        error "不支持的模式: $MODE"
        ;;
esac

# ============================================
# 生成报告
# ============================================

log "生成报告..."

cat > CG_REPORT.md << EOF
# 粗粒化模拟报告

## 模拟参数

- **模式**: $MODE
- **MARTINI版本**: $MARTINI_VERSION
- **时间步长**: $DT ps ($(echo "$DT * 1000" | bc) fs)
- **模拟时间**: $SIM_TIME ps
- **温度**: $TEMPERATURE K
- **压力**: $PRESSURE bar

## 粗粒化参数

- **水模型**: $CG_WATER
- **离子浓度**: $CG_ION_CONC M
- **盒子类型**: $CG_BOX_TYPE
- **盒子边距**: $CG_BOX_DISTANCE nm

## 输出文件

- \`em.gro\` - 能量最小化结构
- \`nvt.gro\` - NVT平衡结构
- \`npt.gro\` - NPT平衡结构
- \`md.xtc\` - 生产模拟轨迹
- \`md.edr\` - 能量文件
- \`md.log\` - 模拟日志

## 粗粒化特点

### 优势
- **计算效率**: 比全原子快100-1000倍
- **时间尺度**: 可模拟微秒到毫秒
- **系统规模**: 可处理百万原子级系统

### 注意事项
- **时间步长**: 20-30 fs (比全原子大10倍)
- **截断距离**: 1.1-1.2 nm (MARTINI推荐)
- **静电处理**: Reaction-Field (ε=15)
- **压力耦合**: τ_p=12 ps (比全原子大)

## 后续分析

### 1. 基础分析
\`\`\`bash
# RMSD (使用骨架珠子)
echo "Backbone Backbone" | gmx rms -s md.tpr -f md.xtc -o rmsd.xvg

# 回转半径
echo "Protein" | gmx gyrate -s md.tpr -f md.xtc -o gyrate.xvg

# 能量
echo "Potential Temperature Pressure" | gmx energy -f md.edr -o energy.xvg
\`\`\`

### 2. 二级结构 (需要反向映射)
\`\`\`bash
# 先反向映射到全原子
# 然后使用DSSP
gmx do_dssp -s aa.tpr -f aa.xtc -o dssp.xpm
\`\`\`

### 3. 接触图
\`\`\`bash
gmx mdmat -s md.tpr -f md.xtc -mean -o contact.xpm
\`\`\`

## 参考文献

- Marrink et al. (2007). The MARTINI force field. J. Phys. Chem. B 111, 7812-7824.
- Marrink et al. (2021). MARTINI 3. Nat. Methods 18, 382-388.
- Wassenaar et al. (2015). Computational lipidomics with insane. JCTC 11, 2144-2155.

## 质量检查
EOF

# 检查模拟完成
if [[ -f "md.log" ]] && grep -q "Finished mdrun" md.log; then
    echo "✅ 模拟成功完成" >> CG_REPORT.md
else
    echo "⚠️ 模拟可能未完成" >> CG_REPORT.md
fi

# 检查能量
if [[ -f "em.log" ]]; then
    local final_energy=$(grep "Potential Energy" em.log | tail -1 | awk '{print $4}')
    echo "✅ 最终势能: $final_energy kJ/mol" >> CG_REPORT.md
fi

log "报告已生成: CG_REPORT.md"

# ============================================
# 完成
# ============================================

log "粗粒化模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/CG_REPORT.md"

exit 0
