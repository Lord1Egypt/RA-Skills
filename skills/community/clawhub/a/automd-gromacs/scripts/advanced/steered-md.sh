#!/bin/bash
# GROMACS Steered Molecular Dynamics (SMD)
# 牵引分子动力学 - 用于计算力-距离曲线和PMF预备
# 基于 GROMACS Manual 5.8.4 Pull Code

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-system.gro}"       # 平衡后的结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件
INPUT_CPT="${INPUT_CPT:-npt.cpt}"          # 检查点文件(可选)
INPUT_NDX="${INPUT_NDX:-index.ndx}"        # 索引文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-steered-md}"

# 拉力几何类型
PULL_GEOMETRY="${PULL_GEOMETRY:-distance}" # distance/direction/cylinder/angle/dihedral

# 拉力模式
PULL_MODE="${PULL_MODE:-constant-velocity}" # constant-velocity/constant-force/umbrella

# 拉力组定义
PULL_GROUP1="${PULL_GROUP1:-Protein}"      # 参考组(固定)
PULL_GROUP2="${PULL_GROUP2:-Ligand}"       # 拉力组(移动)
PULL_GROUP3="${PULL_GROUP3:-}"             # 第三组(angle/dihedral)
PULL_GROUP4="${PULL_GROUP4:-}"             # 第四组(angle/dihedral)
PULL_GROUP5="${PULL_GROUP5:-}"             # 第五组(dihedral)
PULL_GROUP6="${PULL_GROUP6:-}"             # 第六组(dihedral)

# 拉力参数
PULL_RATE="${PULL_RATE:-0.01}"             # 拉力速率(nm/ps) 或 力(kJ/mol/nm)
PULL_K="${PULL_K:-1000}"                   # 弹簧常数(kJ/mol/nm²,仅umbrella)
PULL_INIT="${PULL_INIT:-0.0}"              # 初始距离(nm,自动检测)
PULL_VEC="${PULL_VEC:-0 0 1}"              # 拉力方向(direction几何)
CYLINDER_R="${CYLINDER_R:-1.5}"            # 圆柱半径(nm,cylinder几何)

# 模拟参数
SIM_TIME="${SIM_TIME:-1000}"               # 模拟时间(ps)
DT="${DT:-0.002}"                          # 时间步长(ps)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
TEMPERATURE="${TEMPERATURE:-300}"          # 温度(K)

# 计算资源
NTOMP="${NTOMP:-4}"                        # OpenMP线程数
GPU_ID="${GPU_ID:-}"                       # GPU ID(可选)

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

# 验证拉力几何和组数量
validate_pull_geometry() {
    local required_groups=2
    
    case "$PULL_GEOMETRY" in
        distance|direction|direction-periodic|direction-relative|cylinder)
            required_groups=2
            ;;
        angle|angle-axis)
            required_groups=3
            [[ -n "$PULL_GROUP3" ]] || {
                log "[WARN] angle几何需要3个组"
                log "[AUTO-FIX] 使用默认第三组: System"
                PULL_GROUP3="System"
            }
            ;;
        dihedral)
            required_groups=6
            [[ -n "$PULL_GROUP3" && -n "$PULL_GROUP4" && -n "$PULL_GROUP5" && -n "$PULL_GROUP6" ]] || {
                log "[ERROR] dihedral几何需要6个组"
                error "请提供 PULL_GROUP3-6"
            }
            ;;
        *)
            error "不支持的拉力几何: $PULL_GEOMETRY"
            ;;
    esac
}

# 验证拉力速率
validate_pull_rate() {
    if [[ "$PULL_MODE" == "constant-velocity" ]]; then
        # 推荐: 0.001-0.01 nm/ps
        if (( $(echo "$PULL_RATE < 0.0001" | bc -l) )); then
            log "[WARN] 拉力速率过小 ($PULL_RATE < 0.0001 nm/ps)"
            log "[AUTO-FIX] 增加到 0.001 nm/ps"
            PULL_RATE=0.001
        fi
        
        if (( $(echo "$PULL_RATE > 0.1" | bc -l) )); then
            log "[WARN] 拉力速率过大 ($PULL_RATE > 0.1 nm/ps)"
            log "[AUTO-FIX] 减少到 0.01 nm/ps"
            PULL_RATE=0.01
        fi
    elif [[ "$PULL_MODE" == "constant-force" ]]; then
        # 推荐: 100-1000 kJ/mol/nm
        if (( $(echo "$PULL_RATE < 10" | bc -l) )); then
            log "[WARN] 拉力过小 ($PULL_RATE < 10 kJ/mol/nm)"
            log "[AUTO-FIX] 增加到 100 kJ/mol/nm"
            PULL_RATE=100
        fi
        
        if (( $(echo "$PULL_RATE > 5000" | bc -l) )); then
            log "[WARN] 拉力过大 ($PULL_RATE > 5000 kJ/mol/nm)"
            log "[AUTO-FIX] 减少到 1000 kJ/mol/nm"
            PULL_RATE=1000
        fi
    fi
}

# 自动检测初始距离
auto_detect_init_distance() {
    if [[ "$PULL_GEOMETRY" == "distance" && "$PULL_INIT" == "0.0" ]]; then
        log "自动检测初始距离..."
        
        # 创建临时索引文件
        if [[ ! -f "$INPUT_NDX" ]]; then
            printf "q\n" | gmx make_ndx -f "$INPUT_GRO" -o temp.ndx 2>&1 | grep -E "Group|nr" || true
            INPUT_NDX="temp.ndx"
        fi
        
        # 使用 gmx distance 计算初始距离
        local dist=$(printf "%s\n%s\n" "$PULL_GROUP1" "$PULL_GROUP2" | \
            gmx distance -s "$INPUT_GRO" -n "$INPUT_NDX" -select "com of group \"$PULL_GROUP1\"" \
            -select2 "com of group \"$PULL_GROUP2\"" 2>&1 | \
            grep "Distance" | awk '{print $2}' || echo "0.0")
        
        if [[ -n "$dist" && "$dist" != "0.0" ]]; then
            PULL_INIT=$dist
            log "[AUTO-FIX] 检测到初始距离: $PULL_INIT nm"
        else
            log "[WARN] 无法自动检测距离,使用默认值 0.0"
        fi
    fi
}

# 验证索引文件
validate_index_file() {
    if [[ ! -f "$INPUT_NDX" ]]; then
        log "[WARN] 索引文件不存在"
        log "[AUTO-FIX] 生成默认索引文件"
        printf "q\n" | gmx make_ndx -f "$INPUT_GRO" -o index.ndx 2>&1 | tee make_ndx.log
        INPUT_NDX="index.ndx"
    fi
    
    # 检查拉力组是否存在
    for group in "$PULL_GROUP1" "$PULL_GROUP2" "$PULL_GROUP3" "$PULL_GROUP4" "$PULL_GROUP5" "$PULL_GROUP6"; do
        [[ -z "$group" ]] && continue
        if ! grep -q "^\[ $group \]" "$INPUT_NDX" 2>/dev/null; then
            log "[WARN] 组 '$group' 不存在于索引文件"
            log "可用组:"
            grep "^\[" "$INPUT_NDX" | head -20
            error "请检查拉力组名称或重新生成索引文件"
        fi
    done
}

# 失败重启
restart_from_checkpoint() {
    if [[ -f "pull.cpt" ]]; then
        log "[AUTO-FIX] 从检查点重启模拟"
        gmx mdrun -v -deffnm pull -cpi pull.cpt \
            -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a pull.log
        return $?
    fi
    return 1
}

# 分析拉力曲线
analyze_pull_force() {
    if [[ ! -f "pullf.xvg" ]]; then
        log "[WARN] 拉力文件不存在"
        return 1
    fi
    
    log "分析拉力-距离曲线..."
    
    # 提取统计信息
    awk '!/^[@#]/ {sum+=$2; sumsq+=$2*$2; n++; if($2>max || NR==1){max=$2}; if($2<min || NR==1){min=$2}} 
         END {avg=sum/n; std=sqrt(sumsq/n - avg*avg); 
              print "平均力:", avg, "kJ/mol/nm"; 
              print "标准差:", std, "kJ/mol/nm";
              print "最大力:", max, "kJ/mol/nm";
              print "最小力:", min, "kJ/mol/nm"}' pullf.xvg > force_stats.txt
    
    cat force_stats.txt
}

# 生成伞状采样窗口
generate_umbrella_windows() {
    if [[ "$PULL_MODE" != "constant-velocity" ]]; then
        log "[WARN] 仅constant-velocity模式支持自动生成伞状采样窗口"
        return 1
    fi
    
    log "生成伞状采样窗口配置..."
    
    # 计算窗口数量和间隔
    local max_dist=$(echo "$PULL_INIT + $PULL_RATE * $SIM_TIME" | bc -l)
    local window_spacing=0.1  # 0.1 nm
    local num_windows=$(awk "BEGIN{printf "%d", ($max_dist - $PULL_INIT) / $window_spacing}" )
    
    log "距离范围: $PULL_INIT - $max_dist nm"
    log "窗口间隔: $window_spacing nm"
    log "窗口数量: $num_windows"
    
    # 生成窗口列表
    cat > umbrella_windows.dat << 'EOFWIN'
# Umbrella Sampling Windows
# Generated from steered MD trajectory
# Format: window_id  distance(nm)  spring_constant(kJ/mol/nm²)
EOFWIN
    
    for i in $(seq 0 $num_windows); do
        local dist=$(echo "$PULL_INIT + $i * $window_spacing" | bc -l)
        echo "$i  $dist  $PULL_K" >> umbrella_windows.dat
    done
    
    log "窗口配置已保存: umbrella_windows.dat"
}

# ============================================
# 前置检查
# ============================================

log "开始牵引分子动力学 (Steered MD)"
log "几何类型: $PULL_GEOMETRY"
log "拉力模式: $PULL_MODE"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 验证参数
validate_pull_geometry
validate_pull_rate
auto_detect_init_distance
validate_index_file

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 复制输入文件
cp "../$INPUT_GRO" .
cp "../$INPUT_TOP" .
[[ -f "../$INPUT_CPT" ]] && cp "../$INPUT_CPT" .
[[ -f "../$INPUT_NDX" ]] && cp "../$INPUT_NDX" .


# ============================================
# Phase 1: 生成MDP文件
# ============================================

log "Phase 1: 生成MDP文件"

cat > pull.mdp << 'EOFMDP'
; Steered MD - Pull Code Configuration
; Generated by AutoMD-GROMACS

; Run control
integrator              = md
nsteps                  = NSTEPS_PLACEHOLDER
dt                      = DT_PLACEHOLDER

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
ref_t                   = TEMP_PLACEHOLDER

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
lincs_iter              = 1
lincs_order             = 4

; Pull code
pull                    = yes
pull-ncoords            = 1
pull-ngroups            = NGROUPS_PLACEHOLDER
pull-group1-name        = GROUP1_PLACEHOLDER
pull-group2-name        = GROUP2_PLACEHOLDER
EOFMDP

# 替换占位符
sed -i "s/NSTEPS_PLACEHOLDER/$NSTEPS/" pull.mdp
sed -i "s/DT_PLACEHOLDER/$DT/" pull.mdp
sed -i "s/TEMP_PLACEHOLDER/$TEMPERATURE/" pull.mdp
sed -i "s/GROUP1_PLACEHOLDER/$PULL_GROUP1/" pull.mdp
sed -i "s/GROUP2_PLACEHOLDER/$PULL_GROUP2/" pull.mdp

# 根据几何类型设置组数量
case "$PULL_GEOMETRY" in
    distance|direction|direction-periodic|cylinder)
        sed -i "s/NGROUPS_PLACEHOLDER/2/" pull.mdp
        ;;
    angle|angle-axis)
        sed -i "s/NGROUPS_PLACEHOLDER/3/" pull.mdp
        echo "pull-group3-name        = $PULL_GROUP3" >> pull.mdp
        ;;
    dihedral)
        sed -i "s/NGROUPS_PLACEHOLDER/6/" pull.mdp
        cat >> pull.mdp << EOFGROUPS
pull-group3-name        = $PULL_GROUP3
pull-group4-name        = $PULL_GROUP4
pull-group5-name        = $PULL_GROUP5
pull-group6-name        = $PULL_GROUP6
EOFGROUPS
        ;;
esac

# 配置拉力坐标
cat >> pull.mdp << EOFPULL

; Pull coordinate 1
pull-coord1-geometry    = $PULL_GEOMETRY
EOFPULL

# 根据几何类型配置组
case "$PULL_GEOMETRY" in
    distance|direction|direction-periodic|cylinder)
        echo "pull-coord1-groups      = 1 2" >> pull.mdp
        ;;
    angle|angle-axis)
        echo "pull-coord1-groups      = 1 2 3" >> pull.mdp
        ;;
    dihedral)
        echo "pull-coord1-groups      = 1 2 3 4 5 6" >> pull.mdp
        ;;
esac

# 配置拉力类型和参数
case "$PULL_MODE" in
    constant-velocity)
        cat >> pull.mdp << EOFCV
pull-coord1-type        = umbrella
pull-coord1-rate        = $PULL_RATE
pull-coord1-k           = $PULL_K
pull-coord1-start       = yes
EOFCV
        ;;
    constant-force)
        cat >> pull.mdp << EOFCF
pull-coord1-type        = constant-force
pull-coord1-k           = $PULL_RATE
pull-coord1-start       = yes
EOFCF
        ;;
    umbrella)
        cat >> pull.mdp << EOFUMB
pull-coord1-type        = umbrella
pull-coord1-k           = $PULL_K
pull-coord1-init        = $PULL_INIT
EOFUMB
        ;;
esac

# 几何特定参数
if [[ "$PULL_GEOMETRY" == "direction" || "$PULL_GEOMETRY" == "direction-periodic" ]]; then
    echo "pull-coord1-vec         = $PULL_VEC" >> pull.mdp
fi

if [[ "$PULL_GEOMETRY" == "cylinder" ]]; then
    echo "pull-cylinder-r         = $CYLINDER_R" >> pull.mdp
    echo "pull-coord1-vec         = $PULL_VEC" >> pull.mdp
fi

# 输出控制
cat >> pull.mdp << EOFOUT
pull-coord1-dim         = Y Y Y
pull-nstxout            = 100
pull-nstfout            = 100
EOFOUT

log "[OK] MDP文件已生成: pull.mdp"


# ============================================
# Phase 2: 预处理
# ============================================

log "Phase 2: 预处理 (grompp)"

if [[ -f "$INPUT_CPT" ]]; then
    gmx grompp -f pull.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" -t "$INPUT_CPT" \
        -n "$INPUT_NDX" -o pull.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
else
    gmx grompp -f pull.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" \
        -n "$INPUT_NDX" -o pull.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
fi

[[ -f "pull.tpr" ]] || error "TPR 生成失败"

# ============================================
# Phase 3: 运行模拟
# ============================================

log "Phase 3: 运行牵引模拟"
log "模拟时间: $SIM_TIME ps"

gmx mdrun -v -deffnm pull \
    -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee pull.log || {
    log "[ERROR] 模拟失败,尝试重启..."
    restart_from_checkpoint || error "重启失败"
}

# ============================================
# Phase 4: 分析结果
# ============================================

log "Phase 4: 分析结果"

# 分析拉力曲线
if [[ -f "pullf.xvg" ]]; then
    analyze_pull_force
fi

# 提取拉力距离
if [[ -f "pullx.xvg" ]]; then
    log "提取拉力距离..."
    grep -v "^[@#]" pullx.xvg > pull_distance.dat
fi

# 生成伞状采样窗口
if [[ "$PULL_MODE" == "constant-velocity" ]]; then
    generate_umbrella_windows
fi

# ============================================
# Phase 5: 生成报告
# ============================================

log "Phase 5: 生成报告"

cat > STEERED_MD_REPORT.md << EOFREPORT
# Steered MD 模拟报告

## 模拟参数

- **拉力几何**: $PULL_GEOMETRY
- **拉力模式**: $PULL_MODE
- **拉力组**: $PULL_GROUP1 (参考) → $PULL_GROUP2 (拉力)
- **模拟时间**: $SIM_TIME ps
- **温度**: $TEMPERATURE K

## 拉力参数

EOFREPORT

case "$PULL_MODE" in
    constant-velocity)
        cat >> STEERED_MD_REPORT.md << EOFCV
- **拉力速率**: $PULL_RATE nm/ps
- **弹簧常数**: $PULL_K kJ/mol/nm²
- **初始距离**: $PULL_INIT nm
- **最终距离**: $(echo "$PULL_INIT + $PULL_RATE * $SIM_TIME" | bc -l) nm
EOFCV
        ;;
    constant-force)
        cat >> STEERED_MD_REPORT.md << EOFCF
- **恒定力**: $PULL_RATE kJ/mol/nm
- **初始距离**: $PULL_INIT nm
EOFCF
        ;;
    umbrella)
        cat >> STEERED_MD_REPORT.md << EOFUMB
- **弹簧常数**: $PULL_K kJ/mol/nm²
- **参考距离**: $PULL_INIT nm
EOFUMB
        ;;
esac

if [[ "$PULL_GEOMETRY" == "direction" || "$PULL_GEOMETRY" == "cylinder" ]]; then
    cat >> STEERED_MD_REPORT.md << EOFVEC

## 几何参数

- **拉力方向**: $PULL_VEC
EOFVEC
fi

if [[ "$PULL_GEOMETRY" == "cylinder" ]]; then
    echo "- **圆柱半径**: $CYLINDER_R nm" >> STEERED_MD_REPORT.md
fi

cat >> STEERED_MD_REPORT.md << EOFOUT

## 输出文件

- \`pull.xtc\` - 轨迹文件
- \`pull.edr\` - 能量文件
- \`pullf.xvg\` - 拉力-时间曲线
- \`pullx.xvg\` - 距离-时间曲线
- \`pull.log\` - 模拟日志
- \`pull.mdp\` - MDP配置文件

EOFOUT

if [[ -f "force_stats.txt" ]]; then
    cat >> STEERED_MD_REPORT.md << EOFSTATS

## 拉力统计

\`\`\`
$(cat force_stats.txt)
\`\`\`

EOFSTATS
fi

if [[ -f "umbrella_windows.dat" ]]; then
    cat >> STEERED_MD_REPORT.md << EOFUMB

## 伞状采样窗口

已生成 $(wc -l < umbrella_windows.dat | awk '{print $1-3}') 个窗口配置

查看: \`umbrella_windows.dat\`

EOFUMB
fi

cat >> STEERED_MD_REPORT.md << EOFANALYSIS

## 后续分析

### 1. 可视化拉力曲线

\`\`\`bash
# 使用 xmgrace 或 gnuplot
xmgrace pullf.xvg pullx.xvg

# 或使用 gnuplot
gnuplot << PLOT
set xlabel "Time (ps)"
set ylabel "Force (kJ/mol/nm)"
plot "pullf.xvg" with lines title "Pull Force"
PLOT
\`\`\`

### 2. 计算功 (Work)

\`\`\`bash
# 积分力-距离曲线
awk 'BEGIN{w=0} !/^[@#]/ {if(NR>1) w+=((\$2+prev)/2)*(\$1-prevt); prev=\$2; prevt=\$1} END{print "Work:", w, "kJ/mol"}' pullf.xvg
\`\`\`

### 3. 提取构象用于伞状采样

\`\`\`bash
# 从轨迹提取构象
gmx trjconv -s pull.tpr -f pull.xtc -o conf.gro -sep -skip 10
\`\`\`

### 4. 运行伞状采样

\`\`\`bash
# 使用生成的窗口配置
# 参考 umbrella_windows.dat
\`\`\`

## 参考文献

- Izrailev et al. (1997). Steered molecular dynamics. Computational Molecular Dynamics.
- Jarzynski (1997). Nonequilibrium equality for free energy differences. PRL 78, 2690.
- GROMACS Manual 5.8.4: Pull Code

## 质量检查

EOFANALYSIS

# 检查模拟是否完成
if grep -q "Finished mdrun" pull.log 2>/dev/null; then
    echo "✅ 模拟成功完成" >> STEERED_MD_REPORT.md
else
    echo "⚠️ 模拟可能未完成,检查 pull.log" >> STEERED_MD_REPORT.md
fi

# 检查输出文件
if [[ -f "pullf.xvg" ]] && [[ -s "pullf.xvg" ]]; then
    echo "✅ 拉力数据已记录" >> STEERED_MD_REPORT.md
else
    echo "⚠️ 拉力数据缺失" >> STEERED_MD_REPORT.md
fi

if [[ -f "pullx.xvg" ]] && [[ -s "pullx.xvg" ]]; then
    echo "✅ 距离数据已记录" >> STEERED_MD_REPORT.md
else
    echo "⚠️ 距离数据缺失" >> STEERED_MD_REPORT.md
fi

log "报告已生成: STEERED_MD_REPORT.md"

# ============================================
# 完成
# ============================================

log "Steered MD 模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/STEERED_MD_REPORT.md"

exit 0
