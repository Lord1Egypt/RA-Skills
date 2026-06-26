#!/bin/bash
# GROMACS QM/MM Hybrid Simulation
# QM/MM 混合模拟 - CP2K/ORCA 接口
# 基于 GROMACS 2026.1 QM/MM 实现

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_PDB="${INPUT_PDB:-protein.pdb}"      # 输入结构
INPUT_GRO="${INPUT_GRO:-}"                 # 平衡后的结构(可选)
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件
INPUT_CPT="${INPUT_CPT:-}"                 # 检查点文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-qmmm}"

# QM/MM 方法
QM_SOFTWARE="${QM_SOFTWARE:-auto}"         # auto/cp2k/orca
QM_METHOD="${QM_METHOD:-PBE}"              # PBE/B3LYP/BLYP/PBE0/CAM-B3LYP/WB97X
QM_DISPERSION="${QM_DISPERSION:-D3}"       # none/D3/D3BJ
QM_BASIS="${QM_BASIS:-DZVP-MOLOPT-SR-GTH}" # CP2K: DZVP-MOLOPT-SR-GTH/TZVP-MOLOPT-GTH
                                           # ORCA: 6-31G*/def2-SVP/def2-TZVP

# QM 区域定义
QM_SELECTION="${QM_SELECTION:-auto}"       # auto/manual/residue/index
QM_RESIDUES="${QM_RESIDUES:-}"             # 残基名称(逗号分隔, 如 "LIG,HEM")
QM_ATOMS="${QM_ATOMS:-}"                   # 原子索引(逗号分隔, 如 "1-50,100-150")
QM_CHARGE="${QM_CHARGE:-0}"                # QM 区域总电荷
QM_MULTIPLICITY="${QM_MULTIPLICITY:-1}"    # QM 区域自旋多重度

# QM/MM 边界处理
LINK_ATOM_METHOD="${LINK_ATOM_METHOD:-auto}" # auto/hydrogen/none
MM_EMBEDDING="${MM_EMBEDDING:-electrostatic}" # electrostatic/mechanical

# MM 区域配置
MM_FORCEFIELD="${MM_FORCEFIELD:-amber99sb-ildn}" # amber99sb-ildn/charmm36/oplsaa
WATER_MODEL="${WATER_MODEL:-tip3p}"        # tip3p/tip4p/spc

# 模拟参数
SIM_TIME="${SIM_TIME:-1000}"               # 模拟时间(ps)
DT="${DT:-0.001}"                          # 时间步长(ps, QM/MM推荐0.5-1 fs)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
TEMPERATURE="${TEMPERATURE:-300}"          # 温度(K)
PRESSURE="${PRESSURE:-1.0}"                # 压力(bar)

# 计算资源
NTOMP="${NTOMP:-4}"                        # OpenMP线程数
GPU_ID="${GPU_ID:-}"                       # GPU ID(可选)
QM_NPROC="${QM_NPROC:-4}"                  # QM软件进程数

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

# 检测可用的 QM 软件
check_qm_software() {
    log "检测可用的 QM 软件..."
    
    local cp2k_available=false
    local orca_available=false
    
    # 检查 CP2K
    if command -v cp2k.psmp &> /dev/null || command -v cp2k.popt &> /dev/null || command -v cp2k.ssmp &> /dev/null; then
        cp2k_available=true
        log "[OK] CP2K 可用: $(command -v cp2k.psmp || command -v cp2k.popt || command -v cp2k.ssmp)"
    fi
    
    # 检查 ORCA
    if command -v orca &> /dev/null; then
        orca_available=true
        log "[OK] ORCA 可用: $(command -v orca)"
    fi
    
    # 检查 GROMACS 是否编译了 CP2K 支持
    local gmx_cp2k=false
    if gmx mdrun -h 2>&1 | grep -q "cp2k\|CP2K\|qmmm\|QMMM"; then
        gmx_cp2k=true
        log "[OK] GROMACS 已编译 CP2K 支持"
    fi
    
    # 自动选择
    if [[ "$QM_SOFTWARE" == "auto" ]]; then
        if $gmx_cp2k && $cp2k_available; then
            QM_SOFTWARE="cp2k"
            log "[AUTO-FIX] 选择 CP2K (GROMACS 内置支持)"
        elif $orca_available; then
            QM_SOFTWARE="orca"
            log "[AUTO-FIX] 选择 ORCA (外部接口)"
        else
            log "[ERROR-001] 未找到可用的 QM 软件"
            log "Fix: 安装 CP2K 或 ORCA"
            log "  CP2K: https://www.cp2k.org/download"
            log "  ORCA: https://orcaforum.kofo.mpg.de/"
            log "  或重新编译 GROMACS: cmake -DGMX_CP2K=ON"
            error "QM 软件不可用"
        fi
    fi
    
    # 验证选择的软件
    if [[ "$QM_SOFTWARE" == "cp2k" ]]; then
        if ! $gmx_cp2k; then
            log "[ERROR-001] GROMACS 未编译 CP2K 支持"
            log "Fix: cmake -DGMX_CP2K=ON && make && make install"
            error "CP2K 支持未启用"
        fi
        if ! $cp2k_available; then
            log "[WARN] CP2K 可执行文件未找到"
            log "GROMACS 将尝试使用内置 CP2K 库"
        fi
    elif [[ "$QM_SOFTWARE" == "orca" ]]; then
        if ! $orca_available; then
            log "[ERROR-001] ORCA 未安装"
            log "Fix: 从 https://orcaforum.kofo.mpg.de/ 下载并安装"
            error "ORCA 不可用"
        fi
    fi
}

# 验证 QM 区域定义
validate_qm_region() {
    log "验证 QM 区域定义..."
    
    if [[ "$QM_SELECTION" == "auto" ]]; then
        log "[AUTO-FIX] 自动检测 QM 区域 (配体/辅因子)"
        # 尝试识别小分子配体
        if [[ -n "$QM_RESIDUES" ]]; then
            QM_SELECTION="residue"
        elif [[ -n "$QM_ATOMS" ]]; then
            QM_SELECTION="index"
        else
            log "[WARN] 未指定 QM 区域, 使用默认 (前50个原子)"
            QM_ATOMS="1-50"
            QM_SELECTION="index"
        fi
    fi
    
    case "$QM_SELECTION" in
        residue)
            [[ -z "$QM_RESIDUES" ]] && error "[ERROR-002] QM_RESIDUES 未定义"
            log "[OK] QM 区域: 残基 $QM_RESIDUES"
            ;;
        index)
            [[ -z "$QM_ATOMS" ]] && error "[ERROR-002] QM_ATOMS 未定义"
            log "[OK] QM 区域: 原子 $QM_ATOMS"
            ;;
        manual)
            log "[OK] QM 区域: 手动定义 (需要索引文件)"
            ;;
        *)
            error "[ERROR-002] 无效的 QM_SELECTION: $QM_SELECTION"
            ;;
    esac
}

# 验证基组配置
validate_basis_set() {
    log "验证基组配置..."
    
    if [[ "$QM_SOFTWARE" == "cp2k" ]]; then
        # CP2K 基组验证
        case "$QM_BASIS" in
            DZVP-MOLOPT-SR-GTH|TZVP-MOLOPT-GTH|DZVP-MOLOPT-GTH|TZV2P-MOLOPT-GTH)
                log "[OK] CP2K 基组: $QM_BASIS"
                ;;
            6-31G*|def2-SVP|def2-TZVP)
                log "[WARN] 使用 ORCA 风格基组, 转换为 CP2K 格式"
                case "$QM_BASIS" in
                    6-31G*|def2-SVP) QM_BASIS="DZVP-MOLOPT-SR-GTH" ;;
                    def2-TZVP) QM_BASIS="TZVP-MOLOPT-GTH" ;;
                esac
                log "[AUTO-FIX] 基组: $QM_BASIS"
                ;;
            *)
                log "[WARN] 未知基组 $QM_BASIS, 使用默认"
                QM_BASIS="DZVP-MOLOPT-SR-GTH"
                log "[AUTO-FIX] 基组: $QM_BASIS"
                ;;
        esac
    elif [[ "$QM_SOFTWARE" == "orca" ]]; then
        # ORCA 基组验证
        case "$QM_BASIS" in
            6-31G*|def2-SVP|def2-TZVP|def2-TZVPP|cc-pVDZ|cc-pVTZ)
                log "[OK] ORCA 基组: $QM_BASIS"
                ;;
            *MOLOPT*)
                log "[WARN] 使用 CP2K 风格基组, 转换为 ORCA 格式"
                case "$QM_BASIS" in
                    *DZVP*) QM_BASIS="def2-SVP" ;;
                    *TZVP*) QM_BASIS="def2-TZVP" ;;
                esac
                log "[AUTO-FIX] 基组: $QM_BASIS"
                ;;
            *)
                log "[WARN] 未知基组 $QM_BASIS, 使用默认"
                QM_BASIS="def2-SVP"
                log "[AUTO-FIX] 基组: $QM_BASIS"
                ;;
        esac
    fi
}

# 处理 QM/MM 边界
handle_link_atoms() {
    log "处理 QM/MM 边界..."
    
    if [[ "$LINK_ATOM_METHOD" == "auto" ]]; then
        if [[ "$QM_SOFTWARE" == "cp2k" ]]; then
            LINK_ATOM_METHOD="hydrogen"
            log "[AUTO-FIX] CP2K 使用氢原子链接方案"
        else
            LINK_ATOM_METHOD="hydrogen"
            log "[AUTO-FIX] 使用氢原子链接方案"
        fi
    fi
    
    log "[OK] 边界处理: $LINK_ATOM_METHOD"
}

# 检查 SCF 收敛
check_convergence() {
    local log_file=$1
    
    if [[ ! -f "$log_file" ]]; then
        log "[WARN] 日志文件不存在: $log_file"
        return 1
    fi
    
    if [[ "$QM_SOFTWARE" == "cp2k" ]]; then
        if grep -q "SCF run NOT converged" "$log_file"; then
            log "[ERROR-005] SCF 未收敛"
            log "Fix: 增加 SCF 最大迭代次数或调整收敛标准"
            return 1
        fi
    elif [[ "$QM_SOFTWARE" == "orca" ]]; then
        if grep -q "SCF NOT CONVERGED" "$log_file"; then
            log "[ERROR-005] SCF 未收敛"
            log "Fix: 增加 MaxIter 或使用 SlowConv"
            return 1
        fi
    fi
    
    log "[OK] SCF 收敛检查通过"
    return 0
}

# 验证时间步长
validate_timestep() {
    local dt_float=$(echo "$DT" | bc -l)
    
    # QM/MM 推荐时间步长: 0.5-1.0 fs
    if (( $(echo "$dt_float > 0.001" | bc -l) )); then
        log "[WARN] 时间步长过大 ($DT ps > 1 fs)"
        log "[AUTO-FIX] 减小到 1 fs (0.001 ps)"
        DT="0.001"
        NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
    fi
    
    if (( $(echo "$dt_float < 0.0005" | bc -l) )); then
        log "[WARN] 时间步长过小 ($DT ps < 0.5 fs)"
        log "建议: 使用 0.5-1.0 fs 以平衡精度和效率"
    fi
    
    log "[OK] 时间步长: $DT ps ($(echo "$DT * 1000" | bc) fs)"
}

# ============================================
# QM 输入文件生成
# ============================================

# 生成 CP2K 输入文件
generate_cp2k_input() {
    local input_file=$1
    local method=$2
    
    log "生成 CP2K 输入文件: $input_file"
    
    # 确定泛函和色散校正
    local functional=$method
    local dispersion=""
    if [[ "$QM_DISPERSION" == "D3" ]]; then
        dispersion="DFTD3"
    elif [[ "$QM_DISPERSION" == "D3BJ" ]]; then
        dispersion="DFTD3(BJ)"
    fi
    
    cat > "$input_file" << EOF
&GLOBAL
  PROJECT qmmm
  RUN_TYPE ENERGY_FORCE
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD QMMM
  STRESS_TENSOR ANALYTICAL
  
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME GTH_POTENTIALS
    
    &MGRID
      CUTOFF 400
      REL_CUTOFF 50
    &END MGRID
    
    &QS
      METHOD GPW
      EPS_DEFAULT 1.0E-10
    &END QS
    
    &SCF
      SCF_GUESS ATOMIC
      EPS_SCF 1.0E-6
      MAX_SCF 50
      &OT
        MINIMIZER DIIS
        PRECONDITIONER FULL_ALL
      &END OT
      &OUTER_SCF
        EPS_SCF 1.0E-6
        MAX_SCF 10
      &END OUTER_SCF
    &END SCF
    
    &XC
      &XC_FUNCTIONAL $functional
      &END XC_FUNCTIONAL
EOF

    if [[ -n "$dispersion" ]]; then
        cat >> "$input_file" << EOF
      &VDW_POTENTIAL
        POTENTIAL_TYPE PAIR_POTENTIAL
        &PAIR_POTENTIAL
          TYPE $dispersion
          PARAMETER_FILE_NAME dftd3.dat
          REFERENCE_FUNCTIONAL $functional
        &END PAIR_POTENTIAL
      &END VDW_POTENTIAL
EOF
    fi

    cat >> "$input_file" << EOF
    &END XC
    
    &POISSON
      PERIODIC XYZ
      POISSON_SOLVER PERIODIC
    &END POISSON
    
  &END DFT
  
  &MM
    &FORCEFIELD
      PARMTYPE AMBER
      PARM_FILE_NAME topology.prmtop
      &SPLINE
        EMAX_SPLINE 1.0E8
      &END SPLINE
    &END FORCEFIELD
    &POISSON
      &EWALD
        EWALD_TYPE SPME
        ALPHA 0.35
        GMAX 25
      &END EWALD
    &END POISSON
  &END MM
  
  &QMMM
    ECOUPL GAUSS
    USE_GEEP_LIB 12
    &CELL
      ABC 20.0 20.0 20.0
      PERIODIC XYZ
    &END CELL
    &QM_KIND H
      MM_INDEX \$QM_ATOMS
    &END QM_KIND
    &PERIODIC
      GMAX 0.1
    &END PERIODIC
  &END QMMM
  
  &SUBSYS
    &CELL
      ABC 30.0 30.0 30.0
      PERIODIC XYZ
    &END CELL
    &TOPOLOGY
      COORD_FILE_NAME COORD_FILE_PLACEHOLDER
      COORD_FILE_FORMAT PDB
      CONNECTIVITY GENERATE
    &END TOPOLOGY
    &KIND H
      BASIS_SET $QM_BASIS
      POTENTIAL GTH-$functional-q1
    &END KIND
    &KIND C
      BASIS_SET $QM_BASIS
      POTENTIAL GTH-$functional-q4
    &END KIND
    &KIND N
      BASIS_SET $QM_BASIS
      POTENTIAL GTH-$functional-q5
    &END KIND
    &KIND O
      BASIS_SET $QM_BASIS
      POTENTIAL GTH-$functional-q6
    &END KIND
  &END SUBSYS
  
&END FORCE_EVAL
EOF

    log "[OK] CP2K 输入文件已生成"
}

# 生成 ORCA 输入文件
generate_orca_input() {
    local input_file=$1
    local method=$2
    
    log "生成 ORCA 输入文件: $input_file"
    
    # 确定泛函和色散校正
    local functional=$method
    if [[ "$QM_DISPERSION" == "D3" ]]; then
        functional="${functional} D3ZERO"
    elif [[ "$QM_DISPERSION" == "D3BJ" ]]; then
        functional="${functional} D3BJ"
    fi
    
    cat > "$input_file" << EOF
# ORCA QM/MM Input
! $functional $QM_BASIS TightSCF

%maxcore 2000

%scf
  MaxIter 100
  Convergence Tight
end

%pal
  nprocs $QM_NPROC
end

%qmmm
  QMAtoms { \$QM_ATOMS } end
  Charge $QM_CHARGE
  Mult $QM_MULTIPLICITY
  ORCAFFFilename "topology.ORCAFF"
end

* xyzfile $QM_CHARGE $QM_MULTIPLICITY system.xyz
EOF

    log "[OK] ORCA 输入文件已生成"
}

# ============================================
# MDP 文件生成
# ============================================

generate_qmmm_mdp() {
    local mdp_file=$1
    local stage=$2  # em/nvt/npt/md
    
    log "生成 MDP 文件: $mdp_file ($stage)"
    
    cat > "$mdp_file" << EOF
; QM/MM $stage simulation

; Run control
integrator               = $([ "$stage" = "em" ] && echo "steep" || echo "md")
nsteps                   = $([ "$stage" = "em" ] && echo "50000" || echo "$NSTEPS")
dt                       = $([ "$stage" = "em" ] && echo "0.001" || echo "$DT")

; Output control
nstxout                  = $([ "$stage" = "em" ] && echo "0" || echo "5000")
nstvout                  = 0
nstfout                  = 0
nstlog                   = 1000
nstenergy                = 1000
nstxout-compressed       = $([ "$stage" = "em" ] && echo "0" || echo "1000")
compressed-x-grps        = System

; Neighbor searching
cutoff-scheme            = Verlet
nstlist                  = 10
ns_type                  = grid
pbc                      = xyz
rlist                    = 1.2

; Electrostatics
coulombtype              = PME
rcoulomb                 = 1.2
pme_order                = 4
fourierspacing           = 0.12

; VdW
vdwtype                  = Cut-off
rvdw                     = 1.2
DispCorr                 = EnerPres

; Temperature coupling
EOF

    if [[ "$stage" != "em" ]]; then
        cat >> "$mdp_file" << EOF
tcoupl                   = V-rescale
tc-grps                  = System
tau_t                    = 0.1
ref_t                    = $TEMPERATURE
EOF
    fi

    if [[ "$stage" == "npt" || "$stage" == "md" ]]; then
        cat >> "$mdp_file" << EOF

; Pressure coupling
pcoupl                   = Parrinello-Rahman
pcoupltype               = isotropic
tau_p                    = 2.0
ref_p                    = $PRESSURE
compressibility          = 4.5e-5
EOF
    fi

    cat >> "$mdp_file" << EOF

; Velocity generation
gen_vel                  = $([ "$stage" = "nvt" ] && echo "yes" || echo "no")
gen_temp                 = $TEMPERATURE
gen_seed                 = -1

; Constraints
constraints              = h-bonds
constraint_algorithm     = lincs
lincs_iter               = 1
lincs_order              = 4

; QM/MM settings
QMMM                     = yes
QMMM-grps                = QMatoms
QMmethod                 = $QM_METHOD
QMbasis                  = $QM_BASIS
QMcharge                 = $QM_CHARGE
QMmult                   = $QM_MULTIPLICITY
EOF

    if [[ "$stage" == "em" ]]; then
        cat >> "$mdp_file" << EOF

; Energy minimization
emtol                    = 1000.0
emstep                   = 0.01
EOF
    fi

    log "[OK] MDP 文件已生成"
}

# ============================================
# 索引文件生成
# ============================================

generate_qm_index() {
    local ndx_file=$1
    
    log "生成 QM 区域索引文件: $ndx_file"
    
    if [[ "$QM_SELECTION" == "residue" ]]; then
        # 基于残基名称选择
        echo "[ QMatoms ]" > "$ndx_file"
        gmx select -s "$INPUT_GRO" -select "resname $QM_RESIDUES" -on "$ndx_file" -append 2>/dev/null || {
            log "[ERROR-003] 无法生成 QM 索引"
            log "Fix: 检查残基名称 $QM_RESIDUES 是否正确"
            error "索引生成失败"
        }
    elif [[ "$QM_SELECTION" == "index" ]]; then
        # 基于原子索引选择
        echo "[ QMatoms ]" > "$ndx_file"
        echo "$QM_ATOMS" | tr ',-' ' \n' >> "$ndx_file"
    else
        log "[ERROR-003] 不支持的 QM_SELECTION: $QM_SELECTION"
        error "索引生成失败"
    fi
    
    log "[OK] QM 索引文件已生成"
}

# ============================================
# 主流程
# ============================================

main() {
    log "=========================================="
    log "GROMACS QM/MM 混合模拟"
    log "=========================================="
    
    # 创建输出目录
    mkdir -p "$OUTPUT_DIR"
    cd "$OUTPUT_DIR"
    
    # 1. 检查依赖
    log "步骤 1: 检查依赖..."
    check_qm_software
    validate_qm_region
    validate_basis_set
    handle_link_atoms
    validate_timestep
    
    # 2. 准备输入文件
    log "步骤 2: 准备输入文件..."
    if [[ -z "$INPUT_GRO" ]]; then
        log "从 PDB 生成 GRO 文件..."
        check_file "../$INPUT_PDB"
        gmx pdb2gmx -f "../$INPUT_PDB" -o system.gro -p topol.top -ff "$MM_FORCEFIELD" -water "$WATER_MODEL" -ignh <<< "1" || {
            log "[ERROR-004] pdb2gmx 失败"
            log "Fix: 检查 PDB 文件格式和力场选择"
            error "系统准备失败"
        }
        INPUT_GRO="system.gro"
    else
        cp "../$INPUT_GRO" system.gro
        cp "../$INPUT_TOP" topol.top 2>/dev/null || true
    fi
    
    # 3. 生成 QM 索引
    log "步骤 3: 生成 QM 区域索引..."
    generate_qm_index "index.ndx"
    
    # 4. 生成 QM 输入文件
    log "步骤 4: 生成 QM 输入文件..."
    if [[ "$QM_SOFTWARE" == "cp2k" ]]; then
        generate_cp2k_input "qmmm.inp" "$QM_METHOD"
    elif [[ "$QM_SOFTWARE" == "orca" ]]; then
        generate_orca_input "qmmm.inp" "$QM_METHOD"
    fi
    
    # 5. 能量最小化
    log "步骤 5: 能量最小化..."
    generate_qmmm_mdp "em.mdp" "em"
    gmx grompp -f em.mdp -c system.gro -p topol.top -n index.ndx -o em.tpr -maxwarn 2 || {
        log "[ERROR-006] grompp (EM) 失败"
        log "Fix: 检查拓扑文件和 MDP 参数"
        error "预处理失败"
    }
    
    gmx mdrun -deffnm em -v -ntomp "$NTOMP" ${GPU_ID:+-gpu_id $GPU_ID} || {
        log "[ERROR-007] mdrun (EM) 失败"
        log "Fix: 检查系统结构和 QM/MM 配置"
        error "能量最小化失败"
    }
    
    check_convergence "em.log"
    
    # 6. NVT 平衡
    log "步骤 6: NVT 平衡..."
    generate_qmmm_mdp "nvt.mdp" "nvt"
    gmx grompp -f nvt.mdp -c em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 2 || {
        log "[ERROR-006] grompp (NVT) 失败"
        error "预处理失败"
    }
    
    gmx mdrun -deffnm nvt -v -ntomp "$NTOMP" ${GPU_ID:+-gpu_id $GPU_ID} || {
        log "[ERROR-008] mdrun (NVT) 失败"
        log "Fix: 减小时间步长或检查温度耦合"
        error "NVT 平衡失败"
    }
    
    check_convergence "nvt.log"
    
    # 7. NPT 平衡
    log "步骤 7: NPT 平衡..."
    generate_qmmm_mdp "npt.mdp" "npt"
    gmx grompp -f npt.mdp -c nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 2 || {
        log "[ERROR-006] grompp (NPT) 失败"
        error "预处理失败"
    }
    
    gmx mdrun -deffnm npt -v -ntomp "$NTOMP" ${GPU_ID:+-gpu_id $GPU_ID} || {
        log "[ERROR-009] mdrun (NPT) 失败"
        log "Fix: 检查压力耦合参数"
        error "NPT 平衡失败"
    }
    
    check_convergence "npt.log"
    
    # 8. 生产模拟
    log "步骤 8: 生产模拟..."
    generate_qmmm_mdp "md.mdp" "md"
    gmx grompp -f md.mdp -c npt.gro -p topol.top -n index.ndx -o md.tpr -maxwarn 2 || {
        log "[ERROR-006] grompp (MD) 失败"
        error "预处理失败"
    }
    
    gmx mdrun -deffnm md -v -ntomp "$NTOMP" ${GPU_ID:+-gpu_id $GPU_ID} || {
        log "[ERROR-010] mdrun (MD) 失败"
        log "Fix: 检查模拟参数和系统稳定性"
        error "生产模拟失败"
    }
    
    check_convergence "md.log"
    
    # 9. 结果分析
    log "步骤 9: 结果分析..."
    analyze_results
    
    # 10. 生成报告
    log "步骤 10: 生成报告..."
    generate_report
    
    log "=========================================="
    log "QM/MM 模拟完成!"
    log "输出目录: $OUTPUT_DIR"
    log "=========================================="
}

# ============================================
# 结果分析
# ============================================

analyze_results() {
    log "分析 QM/MM 模拟结果..."
    
    # 能量分析
    if [[ -f "md.edr" ]]; then
        echo "Potential" | gmx energy -f md.edr -o energy.xvg 2>/dev/null || true
        log "[OK] 能量数据已提取"
    fi
    
    # RMSD 分析
    if [[ -f "md.xtc" ]]; then
        printf "Backbone\nBackbone" | gmx rms -s md.tpr -f md.xtc -o rmsd.xvg -tu ns 2>/dev/null || true
        log "[OK] RMSD 数据已提取"
    fi
    
    # QM 区域分析
    if [[ -f "md.xtc" ]]; then
        echo "QMatoms" | gmx rms -s md.tpr -f md.xtc -o rmsd_qm.xvg -tu ns 2>/dev/null || true
        log "[OK] QM 区域 RMSD 已提取"
    fi
}

# ============================================
# 报告生成
# ============================================

generate_report() {
    local report_file="QMMM_REPORT.md"
    
    log "生成报告: $report_file"
    
    cat > "$report_file" << EOF
# QM/MM 混合模拟报告

## 模拟参数

- **QM 软件**: $QM_SOFTWARE
- **QM 方法**: $QM_METHOD
- **基组**: $QM_BASIS
- **色散校正**: $QM_DISPERSION
- **QM 区域**: $QM_SELECTION
- **QM 电荷**: $QM_CHARGE
- **QM 多重度**: $QM_MULTIPLICITY
- **MM 力场**: $MM_FORCEFIELD
- **水模型**: $WATER_MODEL
- **边界处理**: $LINK_ATOM_METHOD
- **嵌入方式**: $MM_EMBEDDING

## 模拟设置

- **模拟时间**: $SIM_TIME ps
- **时间步长**: $DT ps ($(echo "$DT * 1000" | bc) fs)
- **温度**: $TEMPERATURE K
- **压力**: $PRESSURE bar
- **OpenMP 线程**: $NTOMP
- **QM 进程数**: $QM_NPROC

## 输出文件

- \`em.gro\` - 能量最小化后结构
- \`nvt.gro\` - NVT 平衡后结构
- \`npt.gro\` - NPT 平衡后结构
- \`md.xtc\` - 生产模拟轨迹
- \`md.edr\` - 能量数据
- \`energy.xvg\` - 势能曲线
- \`rmsd.xvg\` - 骨架 RMSD
- \`rmsd_qm.xvg\` - QM 区域 RMSD

## 分析建议

1. **能量稳定性**: 检查 \`energy.xvg\` 确保能量收敛
2. **结构稳定性**: 检查 \`rmsd.xvg\` 确保 RMSD < 0.3 nm
3. **QM 区域**: 检查 \`rmsd_qm.xvg\` 分析 QM 区域动力学
4. **SCF 收敛**: 检查 \`*.log\` 确保 QM 计算收敛

## 常见问题

### SCF 不收敛
- 增加 SCF 最大迭代次数
- 调整收敛标准
- 检查 QM 区域定义

### 模拟不稳定
- 减小时间步长 (0.5 fs)
- 延长平衡时间
- 检查 QM/MM 边界

### 性能优化
- 使用 GPU 加速 MM 部分
- 并行化 QM 计算
- 减小 QM 区域大小

## 引用

如果使用此脚本发表论文，请引用:

- GROMACS: Abraham et al., SoftwareX (2015)
- CP2K: Kühne et al., J. Chem. Phys. (2020)
- ORCA: Neese, WIREs Comput. Mol. Sci. (2022)

---
生成时间: $(date)
EOF

    log "[OK] 报告已生成: $report_file"
}

# ============================================
# 错误处理
# ============================================

trap 'error "脚本异常终止"' ERR

# ============================================
# 执行主流程
# ============================================

main "$@"
