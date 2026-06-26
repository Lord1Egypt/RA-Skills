#!/bin/bash
# GROMACS Enhanced Sampling Methods
# 增强采样 - Simulated Annealing & Expanded Ensemble
# 基于 GROMACS Manual 5.4.6 & 5.4.14

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-system.gro}"       # 平衡后的结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件
INPUT_CPT="${INPUT_CPT:-npt.cpt}"          # 检查点文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-enhanced-sampling}"

# 增强采样方法
SAMPLING_METHOD="${SAMPLING_METHOD:-annealing}"  # annealing/expanded/both

# ============================================
# Simulated Annealing 参数
# ============================================
ANNEALING_TYPE="${ANNEALING_TYPE:-single}"       # single/periodic/no
TEMP_START="${TEMP_START:-300}"                  # 起始温度(K)
TEMP_MAX="${TEMP_MAX:-500}"                      # 最高温度(K)
TEMP_END="${TEMP_END:-300}"                      # 结束温度(K)
ANNEALING_TIME="${ANNEALING_TIME:-1000}"         # 退火时间(ps)
ANNEALING_POINTS="${ANNEALING_POINTS:-5}"        # 控制点数量

# ============================================
# Expanded Ensemble 参数
# ============================================
LAMBDA_TYPE="${LAMBDA_TYPE:-vdw-q}"              # vdw/coul/vdw-q/bonded
NUM_LAMBDA="${NUM_LAMBDA:-11}"                   # lambda状态数
LAMBDA_MC_MOVE="${LAMBDA_MC_MOVE:-metropolis-transition}"  # MC移动类型
LAMBDA_WEIGHTS="${LAMBDA_WEIGHTS:-wl-delta}"     # 权重更新方法
WL_SCALE="${WL_SCALE:-0.8}"                      # Wang-Landau缩放因子
WL_RATIO="${WL_RATIO:-0.8}"                      # 收敛判据
NSTEXPANDED="${NSTEXPANDED:-100}"                # lambda尝试间隔

# 模拟参数
SIM_TIME="${SIM_TIME:-10000}"              # 模拟时间(ps)
DT="${DT:-0.002}"                          # 时间步长(ps)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
TEMPERATURE="${TEMPERATURE:-300}"          # 基础温度(K)

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

# 验证退火参数
validate_annealing_params() {
    # 检查温度范围
    if (( $(echo "$TEMP_MAX < $TEMP_START" | bc -l) )); then
        log "[WARN] 最高温度 < 起始温度"
        log "[AUTO-FIX] 交换 TEMP_MAX 和 TEMP_START"
        local tmp=$TEMP_MAX
        TEMP_MAX=$TEMP_START
        TEMP_START=$tmp
    fi
    
    if (( $(echo "$TEMP_MAX > 1000" | bc -l) )); then
        log "[WARN] 最高温度过高 ($TEMP_MAX > 1000 K)"
        log "[AUTO-FIX] 限制到 800 K"
        TEMP_MAX=800
    fi
    
    if (( $(echo "$TEMP_MAX < $TEMP_START + 50" | bc -l) )); then
        log "[WARN] 温度范围过小 (< 50 K)"
        log "[AUTO-FIX] 增加到 $TEMP_START + 100 K"
        TEMP_MAX=$(echo "$TEMP_START + 100" | bc -l)
    fi
    
    # 检查控制点数量
    if (( ANNEALING_POINTS < 2 )); then
        log "[WARN] 控制点过少 ($ANNEALING_POINTS < 2)"
        log "[AUTO-FIX] 增加到 3"
        ANNEALING_POINTS=3
    fi
    
    if (( ANNEALING_POINTS > 20 )); then
        log "[WARN] 控制点过多 ($ANNEALING_POINTS > 20)"
        log "[AUTO-FIX] 减少到 10"
        ANNEALING_POINTS=10
    fi
}

# 验证扩展系综参数
validate_expanded_params() {
    # 检查lambda数量
    if (( NUM_LAMBDA < 5 )); then
        log "[WARN] lambda状态过少 ($NUM_LAMBDA < 5)"
        log "[AUTO-FIX] 增加到 7"
        NUM_LAMBDA=7
    fi
    
    if (( NUM_LAMBDA > 50 )); then
        log "[WARN] lambda状态过多 ($NUM_LAMBDA > 50)"
        log "[AUTO-FIX] 减少到 21"
        NUM_LAMBDA=21
    fi
    
    # 检查尝试间隔
    if (( NSTEXPANDED < 10 )); then
        log "[WARN] lambda尝试间隔过小 ($NSTEXPANDED < 10)"
        log "[AUTO-FIX] 增加到 50"
        NSTEXPANDED=50
    fi
    
    if (( NSTEXPANDED > 1000 )); then
        log "[WARN] lambda尝试间隔过大 ($NSTEXPANDED > 1000)"
        log "[AUTO-FIX] 减少到 500"
        NSTEXPANDED=500
    fi
}

# 生成退火时间点
generate_annealing_schedule() {
    local n_points=$1
    local t_start=$2
    local t_max=$3
    local t_end=$4
    local total_time=$5
    
    local times=()
    local temps=()
    
    if [[ "$ANNEALING_TYPE" == "single" ]]; then
        # 单次退火: 升温 → 保持 → 降温
        local heat_time=$(echo "$total_time * 0.3" | bc -l)
        local hold_time=$(echo "$total_time * 0.4" | bc -l)
        local cool_time=$(echo "$total_time * 0.3" | bc -l)
        
        # 升温阶段
        for i in $(seq 0 $((n_points/3))); do
            local t=$(echo "$heat_time * $i / ($n_points/3)" | bc -l)
            local temp=$(echo "$t_start + ($t_max - $t_start) * $i / ($n_points/3)" | bc -l)
            times+=($t)
            temps+=($temp)
        done
        
        # 保持阶段
        local t_hold=$(echo "$heat_time + $hold_time" | bc -l)
        times+=($t_hold)
        temps+=($t_max)
        
        # 降温阶段
        for i in $(seq 1 $((n_points/3))); do
            local t=$(echo "$heat_time + $hold_time + $cool_time * $i / ($n_points/3)" | bc -l)
            local temp=$(echo "$t_max - ($t_max - $t_end) * $i / ($n_points/3)" | bc -l)
            times+=($t)
            temps+=($temp)
        done
        
    elif [[ "$ANNEALING_TYPE" == "periodic" ]]; then
        # 周期性退火: 重复升温-降温
        local period=$(echo "$total_time / 5" | bc -l)  # 5个周期
        
        for i in $(seq 0 $((n_points-1))); do
            local t=$(echo "$period * $i / ($n_points - 1)" | bc -l)
            local phase=$(echo "scale=4; $i / ($n_points - 1)" | bc -l)
            
            # 正弦波温度变化
            local temp=$(echo "scale=2; $t_start + ($t_max - $t_start) * (1 + s($phase * 6.28318)) / 2" | bc -l)
            times+=($t)
            temps+=($temp)
        done
    fi
    
    # 输出格式: "t1 t2 t3 ..." 和 "T1 T2 T3 ..."
    echo "${times[*]}"
    echo "${temps[*]}"
}

# 生成lambda分布
generate_lambda_distribution() {
    local n_lambda=$1
    local lambda_type=$2
    
    local lambdas=()
    
    # 端点密集分布
    for i in $(seq 0 $((n_lambda-1))); do
        if (( i == 0 )); then
            lambdas+=(0.0)
        elif (( i == n_lambda-1 )); then
            lambdas+=(1.0)
        elif (( i <= 2 )); then
            # 前端密集
            local lambda=$(echo "scale=4; 0.05 * $i" | bc -l)
            lambdas+=($lambda)
        elif (( i >= n_lambda-3 )); then
            # 后端密集
            local lambda=$(echo "scale=4; 1.0 - 0.05 * ($n_lambda - 1 - $i)" | bc -l)
            lambdas+=($lambda)
        else
            # 中间均匀
            local lambda=$(echo "scale=4; 0.1 + 0.8 * ($i - 2) / ($n_lambda - 5)" | bc -l)
            lambdas+=($lambda)
        fi
    done
    
    echo "${lambdas[*]}"
}

# 失败重启
restart_from_checkpoint() {
    if [[ -f "enhanced.cpt" ]]; then
        log "[AUTO-FIX] 从检查点重启模拟"
        gmx mdrun -v -deffnm enhanced -cpi enhanced.cpt \
            -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a enhanced.log
        return $?
    fi
    return 1
}

# ============================================
# 前置检查
# ============================================

log "开始增强采样模拟"
log "方法: $SAMPLING_METHOD"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 验证参数
if [[ "$SAMPLING_METHOD" == "annealing" || "$SAMPLING_METHOD" == "both" ]]; then
    validate_annealing_params
fi

if [[ "$SAMPLING_METHOD" == "expanded" || "$SAMPLING_METHOD" == "both" ]]; then
    validate_expanded_params
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 复制输入文件
cp "../$INPUT_GRO" .
cp "../$INPUT_TOP" .
[[ -f "../$INPUT_CPT" ]] && cp "../$INPUT_CPT" .

# ============================================
# Phase 1: 生成MDP文件
# ============================================

log "Phase 1: 生成MDP文件"

cat > enhanced.mdp << 'EOFMDP'
; Enhanced Sampling Simulation
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

EOFMDP

# 替换占位符
sed -i "s/NSTEPS_PLACEHOLDER/$NSTEPS/" enhanced.mdp
sed -i "s/DT_PLACEHOLDER/$DT/" enhanced.mdp
sed -i "s/TEMP_PLACEHOLDER/$TEMPERATURE/" enhanced.mdp

# ============================================
# 添加 Simulated Annealing 配置
# ============================================

if [[ "$SAMPLING_METHOD" == "annealing" || "$SAMPLING_METHOD" == "both" ]]; then
    log "配置 Simulated Annealing..."
    
    # 生成退火时间表
    read -r annealing_times <<< $(generate_annealing_schedule $ANNEALING_POINTS $TEMP_START $TEMP_MAX $TEMP_END $ANNEALING_TIME | head -1)
    read -r annealing_temps <<< $(generate_annealing_schedule $ANNEALING_POINTS $TEMP_START $TEMP_MAX $TEMP_END $ANNEALING_TIME | tail -1)
    
    cat >> enhanced.mdp << EOFANNEAL

; Simulated Annealing
annealing               = $ANNEALING_TYPE
annealing-npoints       = $ANNEALING_POINTS
annealing-time          = $annealing_times
annealing-temp          = $annealing_temps
EOFANNEAL

    log "[OK] 退火配置: $ANNEALING_TYPE, $ANNEALING_POINTS 点"
    log "温度范围: $TEMP_START → $TEMP_MAX → $TEMP_END K"
fi

# ============================================
# 添加 Expanded Ensemble 配置
# ============================================

if [[ "$SAMPLING_METHOD" == "expanded" || "$SAMPLING_METHOD" == "both" ]]; then
    log "配置 Expanded Ensemble..."
    
    # 生成lambda分布
    LAMBDA_VALUES=($(generate_lambda_distribution $NUM_LAMBDA $LAMBDA_TYPE))
    
    cat >> enhanced.mdp << EOFEXPAND

; Expanded Ensemble
free-energy             = expanded
nstexpanded             = $NSTEXPANDED
lmc-stats               = $LAMBDA_WEIGHTS
lmc-move                = $LAMBDA_MC_MOVE
lmc-weights-equil       = wl-delta
wl-scale                = $WL_SCALE
wl-ratio                = $WL_RATIO
init-lambda-state       = 0

EOFEXPAND

    # 根据lambda类型设置参数
    case "$LAMBDA_TYPE" in
        vdw)
            echo "vdw-lambdas             = ${LAMBDA_VALUES[*]}" >> enhanced.mdp
            ;;
        coul)
            echo "coul-lambdas            = ${LAMBDA_VALUES[*]}" >> enhanced.mdp
            ;;
        vdw-q)
            echo "vdw-lambdas             = ${LAMBDA_VALUES[*]}" >> enhanced.mdp
            echo "coul-lambdas            = ${LAMBDA_VALUES[*]}" >> enhanced.mdp
            ;;
        bonded)
            echo "bonded-lambdas          = ${LAMBDA_VALUES[*]}" >> enhanced.mdp
            ;;
    esac
    
    # 软核参数
    cat >> enhanced.mdp << EOFSC
sc-alpha                = 0.5
sc-power                = 1
sc-sigma                = 0.3
nstdhdl                 = 100
EOFSC

    log "[OK] 扩展系综配置: $NUM_LAMBDA 个lambda状态"
    log "Lambda类型: $LAMBDA_TYPE"
fi

# 添加压力耦合
cat >> enhanced.mdp << EOFPRESS

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
EOFPRESS

log "[OK] MDP文件已生成: enhanced.mdp"

# ============================================
# Phase 2: 预处理
# ============================================

log "Phase 2: 预处理 (grompp)"

if [[ -f "$INPUT_CPT" ]]; then
    gmx grompp -f enhanced.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" -t "$INPUT_CPT" \
        -o enhanced.tpr -maxwarn 2 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
else
    gmx grompp -f enhanced.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" \
        -o enhanced.tpr -maxwarn 2 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
fi

[[ -f "enhanced.tpr" ]] || error "TPR 生成失败"

# ============================================
# Phase 3: 运行模拟
# ============================================

log "Phase 3: 运行增强采样模拟"
log "模拟时间: $SIM_TIME ps"

gmx mdrun -v -deffnm enhanced \
    -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee enhanced.log || {
    log "[ERROR] 模拟失败,尝试重启..."
    restart_from_checkpoint || error "重启失败"
}

# ============================================
# Phase 4: 分析结果
# ============================================

log "Phase 4: 分析结果"

# 提取能量
if [[ -f "enhanced.edr" ]]; then
    log "提取能量数据..."
    echo "Potential Temperature" | gmx energy -f enhanced.edr \
        -o energy.xvg 2>&1 | tee energy.log || {
        log "[WARN] 能量提取失败"
    }
fi

# 分析扩展系综
if [[ "$SAMPLING_METHOD" == "expanded" || "$SAMPLING_METHOD" == "both" ]]; then
    if [[ -f "enhanced.edr" ]]; then
        log "分析lambda状态分布..."
        
        # 提取lambda状态
        echo "Lambda" | gmx energy -f enhanced.edr -o lambda.xvg 2>&1 | tee lambda.log || {
            log "[WARN] Lambda提取失败"
        }
        
        if [[ -f "lambda.xvg" ]]; then
            # 统计lambda访问频率
            awk '!/^[@#]/ {count[int($2)]++} END {
                print "Lambda状态访问统计:";
                for (i in count) print "State", i":", count[i], "次"
            }' lambda.xvg > lambda_stats.txt
            
            cat lambda_stats.txt
        fi
    fi
fi

# ============================================
# Phase 5: 生成报告
# ============================================

log "Phase 5: 生成报告"

cat > ENHANCED_SAMPLING_REPORT.md << EOFREPORT
# Enhanced Sampling 模拟报告

## 模拟参数

- **采样方法**: $SAMPLING_METHOD
- **模拟时间**: $SIM_TIME ps
- **基础温度**: $TEMPERATURE K
- **时间步长**: $DT ps

EOFREPORT

if [[ "$SAMPLING_METHOD" == "annealing" || "$SAMPLING_METHOD" == "both" ]]; then
    cat >> ENHANCED_SAMPLING_REPORT.md << EOFANNEAL

## Simulated Annealing

### 配置

- **类型**: $ANNEALING_TYPE
- **控制点数**: $ANNEALING_POINTS
- **起始温度**: $TEMP_START K
- **最高温度**: $TEMP_MAX K
- **结束温度**: $TEMP_END K
- **退火时间**: $ANNEALING_TIME ps

### 温度时间表

\`\`\`
时间(ps): $annealing_times
温度(K):  $annealing_temps
\`\`\`

### 物理背景

**Simulated Annealing** 通过周期性升高温度帮助系统跨越能量势垒:

1. **升温阶段**: 增加动能,克服局部最小值
2. **保持阶段**: 在高温下充分采样
3. **降温阶段**: 逐步冷却到目标温度

**适用场景**:
- 蛋白质折叠
- 构象搜索
- 避免陷入局部最小值

EOFANNEAL
fi

if [[ "$SAMPLING_METHOD" == "expanded" || "$SAMPLING_METHOD" == "both" ]]; then
    cat >> ENHANCED_SAMPLING_REPORT.md << EOFEXPAND

## Expanded Ensemble

### 配置

- **Lambda类型**: $LAMBDA_TYPE
- **Lambda状态数**: $NUM_LAMBDA
- **MC移动类型**: $LAMBDA_MC_MOVE
- **权重更新**: $LAMBDA_WEIGHTS
- **WL缩放因子**: $WL_SCALE
- **尝试间隔**: $NSTEXPANDED 步

### Lambda分布

\`\`\`
${LAMBDA_VALUES[*]}
\`\`\`

EOFEXPAND

    if [[ -f "lambda_stats.txt" ]]; then
        cat >> ENHANCED_SAMPLING_REPORT.md << EOFLAMBDA

### Lambda访问统计

\`\`\`
$(cat lambda_stats.txt)
\`\`\`

EOFLAMBDA
    fi

    cat >> ENHANCED_SAMPLING_REPORT.md << EOFEE

### 物理背景

**Expanded Ensemble** 动态改变哈密顿量,增强相空间采样:

1. **Wang-Landau算法**: 自适应调整lambda权重
2. **Metropolis-Hastings**: MC接受/拒绝lambda跳跃
3. **自由能计算**: 从lambda分布计算ΔG

**适用场景**:
- 自由能计算
- 相变研究
- 溶解度预测

EOFEE
fi

cat >> ENHANCED_SAMPLING_REPORT.md << EOFOUT

## 输出文件

- \`enhanced.xtc\` - 轨迹文件
- \`enhanced.edr\` - 能量文件
- \`enhanced.log\` - 模拟日志
- \`energy.xvg\` - 能量-时间曲线
- \`enhanced.mdp\` - MDP配置文件

EOFOUT

if [[ "$SAMPLING_METHOD" == "expanded" || "$SAMPLING_METHOD" == "both" ]]; then
    cat >> ENHANCED_SAMPLING_REPORT.md << EOFLAMBDAOUT
- \`lambda.xvg\` - Lambda状态轨迹
- \`lambda_stats.txt\` - Lambda访问统计

EOFLAMBDAOUT
fi

cat >> ENHANCED_SAMPLING_REPORT.md << EOFANALYSIS

## 后续分析

### 1. 可视化温度/Lambda演化

\`\`\`bash
# 绘制温度-时间曲线
xmgrace energy.xvg

# 绘制lambda-时间曲线 (扩展系综)
xmgrace lambda.xvg
\`\`\`

### 2. 分析结构变化

\`\`\`bash
# RMSD
echo "Backbone Backbone" | gmx rms -s enhanced.tpr -f enhanced.xtc -o rmsd.xvg

# 回转半径
echo "Protein" | gmx gyrate -s enhanced.tpr -f enhanced.xtc -o gyrate.xvg

# 聚类分析
echo "Backbone Backbone" | gmx cluster -s enhanced.tpr -f enhanced.xtc -method gromos -cutoff 0.2
\`\`\`

### 3. 自由能分析 (扩展系综)

\`\`\`bash
# 使用 gmx bar 计算自由能
gmx bar -f enhanced.edr -o bar.xvg

# 或使用 MBAR/WHAM 后处理
\`\`\`

### 4. 温度依赖性分析 (退火)

\`\`\`bash
# 提取不同温度区间的轨迹
# (需要自定义脚本根据温度时间表分割)
\`\`\`

## 参考文献

### Simulated Annealing
- Kirkpatrick et al. (1983). Optimization by simulated annealing. Science 220, 671-680.
- GROMACS Manual 5.4.6: Simulated Annealing

### Expanded Ensemble
- Lyubartsev et al. (1992). New approach to Monte Carlo calculation of the free energy. J. Chem. Phys. 96, 1776.
- Wang & Landau (2001). Efficient, multiple-range random walk algorithm. Phys. Rev. Lett. 86, 2050.
- GROMACS Manual 5.4.14: Expanded Ensemble

## 质量检查

EOFANALYSIS

# 检查模拟是否完成
if grep -q "Finished mdrun" enhanced.log 2>/dev/null; then
    echo "✅ 模拟成功完成" >> ENHANCED_SAMPLING_REPORT.md
else
    echo "⚠️ 模拟可能未完成,检查 enhanced.log" >> ENHANCED_SAMPLING_REPORT.md
fi

# 检查输出文件
if [[ -f "enhanced.xtc" ]] && [[ -s "enhanced.xtc" ]]; then
    echo "✅ 轨迹文件已生成" >> ENHANCED_SAMPLING_REPORT.md
else
    echo "⚠️ 轨迹文件缺失或为空" >> ENHANCED_SAMPLING_REPORT.md
fi

if [[ -f "energy.xvg" ]] && [[ -s "energy.xvg" ]]; then
    echo "✅ 能量数据已记录" >> ENHANCED_SAMPLING_REPORT.md
else
    echo "⚠️ 能量数据缺失" >> ENHANCED_SAMPLING_REPORT.md
fi

log "报告已生成: ENHANCED_SAMPLING_REPORT.md"

# ============================================
# 完成
# ============================================

log "Enhanced Sampling 模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/ENHANCED_SAMPLING_REPORT.md"

exit 0
