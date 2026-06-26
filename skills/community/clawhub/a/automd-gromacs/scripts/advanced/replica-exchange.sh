#!/bin/bash
# GROMACS Replica Exchange Molecular Dynamics (REMD)
# 副本交换分子动力学 - 增强采样方法
# 基于 GROMACS Manual 5.4.12

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-system.gro}"       # 平衡后的结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件
INPUT_CPT="${INPUT_CPT:-npt.cpt}"          # 检查点文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-remd}"

# 副本交换类型
REMD_TYPE="${REMD_TYPE:-temperature}"      # temperature/hamiltonian/both
EXCHANGE_INTERVAL="${EXCHANGE_INTERVAL:-1000}"  # 交换尝试间隔(步数)
RANDOM_SEED="${RANDOM_SEED:--1}"           # 随机种子(-1=自动生成)

# 温度副本交换参数
TEMP_MIN="${TEMP_MIN:-300}"                # 最低温度(K)
TEMP_MAX="${TEMP_MAX:-400}"                # 最高温度(K)
NUM_REPLICAS="${NUM_REPLICAS:-8}"          # 副本数量

# 哈密顿副本交换参数(自由能)
LAMBDA_TYPE="${LAMBDA_TYPE:-vdw-q}"        # vdw/coul/vdw-q/bonded/restraint
LAMBDA_STATES="${LAMBDA_STATES:-}"         # 自定义lambda值(逗号分隔)

# 模拟参数
SIM_TIME="${SIM_TIME:-10000}"              # 模拟时间(ps)
DT="${DT:-0.002}"                          # 时间步长(ps)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )

# 计算资源
NTOMP="${NTOMP:-2}"                        # 每副本OpenMP线程数
GPU_IDS="${GPU_IDS:-}"                     # GPU ID列表(可选)

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
# 温度分布计算 (Manual 5.4.12)
# ============================================
# 最优温度分布: 指数分布
# T_i = T_min * (T_max/T_min)^(i/(N-1))
# 交换概率: P ~ exp(-ΔE/kT)
# 推荐交换概率: 20-30%
# ============================================

calculate_temperatures() {
    local tmin=$1
    local tmax=$2
    local nrep=$3
    
    log "计算温度分布 (指数分布)"
    
    local temps=()
    for i in $(seq 0 $((nrep-1))); do
        local temp=$(echo "scale=2; $tmin * e(l($tmax/$tmin) * $i / ($nrep - 1))" | bc -l)
        temps+=($temp)
    done
    
    echo "${temps[@]}"
}

# ============================================
# Lambda分布计算
# ============================================

calculate_lambdas() {
    local nrep=$1
    local lambda_type=$2
    
    if [[ -n "$LAMBDA_STATES" ]]; then
        # 使用自定义lambda值
        echo "$LAMBDA_STATES" | tr ',' ' '
        return
    fi
    
    log "计算lambda分布 (均匀分布)"
    
    local lambdas=()
    for i in $(seq 0 $((nrep-1))); do
        local lambda=$(echo "scale=4; $i / ($nrep - 1)" | bc -l)
        lambdas+=($lambda)
    done
    
    echo "${lambdas[@]}"
}

# ============================================
# 自动修复函数
# ============================================

# 检查副本数量合理性
validate_replica_count() {
    if [[ "$REMD_TYPE" == "temperature" ]]; then
        # 温度REMD: 推荐8-32个副本
        if (( NUM_REPLICAS < 4 )); then
            log "[WARN] 副本数量过少 ($NUM_REPLICAS < 4)"
            log "[AUTO-FIX] 增加到最小值 4"
            NUM_REPLICAS=4
        fi
        if (( NUM_REPLICAS > 64 )); then
            log "[WARN] 副本数量过多 ($NUM_REPLICAS > 64)"
            log "[AUTO-FIX] 减少到 64"
            NUM_REPLICAS=64
        fi
    fi
}

# 检查温度范围
validate_temperature_range() {
    local temp_ratio=$(echo "scale=2; $TEMP_MAX / $TEMP_MIN" | bc -l)
    
    if (( $(echo "$temp_ratio > 2.0" | bc -l) )); then
        log "[WARN] 温度范围过大 (T_max/T_min = $temp_ratio > 2.0)"
        log "[AUTO-FIX] 建议增加副本数量或减小温度范围"
    fi
    
    if (( $(echo "$temp_ratio < 1.1" | bc -l) )); then
        log "[WARN] 温度范围过小 (T_max/T_min = $temp_ratio < 1.1)"
        log "[AUTO-FIX] 建议增大温度范围或减少副本数量"
    fi
}

# 检查交换间隔
validate_exchange_interval() {
    # 推荐: 100-1000步
    if (( EXCHANGE_INTERVAL < 100 )); then
        log "[WARN] 交换间隔过小 ($EXCHANGE_INTERVAL < 100)"
        log "[AUTO-FIX] 增加到 100"
        EXCHANGE_INTERVAL=100
    fi
    
    if (( EXCHANGE_INTERVAL > 5000 )); then
        log "[WARN] 交换间隔过大 ($EXCHANGE_INTERVAL > 5000)"
        log "[AUTO-FIX] 减少到 1000"
        EXCHANGE_INTERVAL=1000
    fi
}

# 失败副本重启
restart_failed_replicas() {
    local failed=()
    
    for i in $(seq 0 $((NUM_REPLICAS-1))); do
        local rep_dir="replica_$i"
        if [[ ! -f "$rep_dir/md.log" ]] || ! grep -q "Finished mdrun" "$rep_dir/md.log" 2>/dev/null; then
            failed+=($i)
        fi
    done
    
    if [[ ${#failed[@]} -gt 0 ]]; then
        log "[AUTO-FIX] 重启 ${#failed[@]} 个失败的副本: ${failed[*]}"
        
        # 从检查点重启
        for i in "${failed[@]}"; do
            local rep_dir="replica_$i"
            if [[ -f "$rep_dir/md.cpt" ]]; then
                log "从检查点重启副本 $i"
                cd "$rep_dir"
                gmx mdrun -v -deffnm md -cpi md.cpt -ntmpi 1 -ntomp $NTOMP 2>&1 | tee -a md.log || {
                    log "[ERROR] 副本 $i 重启失败"
                }
                cd ..
            fi
        done
    fi
}

# ============================================
# 前置检查
# ============================================

log "开始副本交换分子动力学 (REMD)"
log "类型: $REMD_TYPE"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 验证参数
validate_replica_count
if [[ "$REMD_TYPE" == "temperature" || "$REMD_TYPE" == "both" ]]; then
    validate_temperature_range
fi
validate_exchange_interval

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# ============================================
# Phase 1: 生成副本输入文件
# ============================================

log "Phase 1: 生成 $NUM_REPLICAS 个副本的输入文件"

# 计算温度或lambda分布
if [[ "$REMD_TYPE" == "temperature" ]]; then
    TEMPS=($(calculate_temperatures $TEMP_MIN $TEMP_MAX $NUM_REPLICAS))
    log "温度分布: ${TEMPS[*]}"
elif [[ "$REMD_TYPE" == "hamiltonian" ]]; then
    LAMBDAS=($(calculate_lambdas $NUM_REPLICAS $LAMBDA_TYPE))
    log "Lambda分布: ${LAMBDAS[*]}"
elif [[ "$REMD_TYPE" == "both" ]]; then
    TEMPS=($(calculate_temperatures $TEMP_MIN $TEMP_MAX $NUM_REPLICAS))
    LAMBDAS=($(calculate_lambdas $NUM_REPLICAS $LAMBDA_TYPE))
    log "温度分布: ${TEMPS[*]}"
    log "Lambda分布: ${LAMBDAS[*]}"
fi

# 为每个副本创建目录和MDP文件
for i in $(seq 0 $((NUM_REPLICAS-1))); do
    rep_dir="replica_$i"
    mkdir -p "$rep_dir"
    
    # 生成MDP文件
    cat > "$rep_dir/md.mdp" << EOF
; REMD Production Run - Replica $i
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
EOF

    # 设置温度
    if [[ "$REMD_TYPE" == "temperature" || "$REMD_TYPE" == "both" ]]; then
        echo "ref_t                   = ${TEMPS[$i]}" >> "$rep_dir/md.mdp"
    else
        echo "ref_t                   = 300" >> "$rep_dir/md.mdp"
    fi

    # 压力耦合
    cat >> "$rep_dir/md.mdp" << EOF

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
EOF

    # 哈密顿副本交换参数
    if [[ "$REMD_TYPE" == "hamiltonian" || "$REMD_TYPE" == "both" ]]; then
        cat >> "$rep_dir/md.mdp" << EOF

; Free energy parameters
free_energy             = yes
init-lambda-state       = $i
EOF

        # 根据lambda类型设置参数
        case "$LAMBDA_TYPE" in
            vdw)
                echo "vdw-lambdas             = ${LAMBDAS[*]}" >> "$rep_dir/md.mdp"
                ;;
            coul)
                echo "coul-lambdas            = ${LAMBDAS[*]}" >> "$rep_dir/md.mdp"
                ;;
            vdw-q)
                echo "vdw-lambdas             = ${LAMBDAS[*]}" >> "$rep_dir/md.mdp"
                echo "coul-lambdas            = ${LAMBDAS[*]}" >> "$rep_dir/md.mdp"
                ;;
            bonded)
                echo "bonded-lambdas          = ${LAMBDAS[*]}" >> "$rep_dir/md.mdp"
                ;;
            restraint)
                echo "restraint-lambdas       = ${LAMBDAS[*]}" >> "$rep_dir/md.mdp"
                ;;
        esac
        
        cat >> "$rep_dir/md.mdp" << EOF
sc-alpha                = 0.5
sc-power                = 1
sc-sigma                = 0.3
nstdhdl                 = 100
EOF
    fi
    
    # 生成TPR文件
    log "生成副本 $i TPR文件 (T=${TEMPS[$i]:-300}K)"
    
    if [[ -f "../$INPUT_CPT" ]]; then
        gmx grompp -f "$rep_dir/md.mdp" -c "../$INPUT_GRO" -p "../$INPUT_TOP" \
            -t "../$INPUT_CPT" -o "$rep_dir/md.tpr" -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
    else
        gmx grompp -f "$rep_dir/md.mdp" -c "../$INPUT_GRO" -p "../$INPUT_TOP" \
            -o "$rep_dir/md.tpr" -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
    fi
    
    [[ -f "$rep_dir/md.tpr" ]] || error "副本 $i TPR生成失败"
done

# ============================================
# Phase 2: 运行副本交换模拟
# ============================================

log "Phase 2: 运行副本交换模拟"
log "交换间隔: $EXCHANGE_INTERVAL 步"
log "模拟时间: $SIM_TIME ps"

# 构建multidir参数
MULTIDIR_ARGS=""
for i in $(seq 0 $((NUM_REPLICAS-1))); do
    MULTIDIR_ARGS="$MULTIDIR_ARGS -multidir replica_$i"
done

# 构建GPU参数
GPU_ARGS=""
if [[ -n "$GPU_IDS" ]]; then
    GPU_ARGS="-gpu_id $GPU_IDS"
fi

# 运行REMD
log "启动 $NUM_REPLICAS 个副本..."

gmx mdrun -v -deffnm md \
    $MULTIDIR_ARGS \
    -replex $EXCHANGE_INTERVAL \
    -reseed $RANDOM_SEED \
    -ntmpi $NUM_REPLICAS \
    -ntomp $NTOMP \
    $GPU_ARGS \
    2>&1 | tee remd.log

# 检查是否有失败的副本
restart_failed_replicas

# ============================================
# Phase 3: 分析交换统计
# ============================================

log "Phase 3: 分析交换统计"

# 提取交换信息
if [[ -f "replica_0/md.log" ]]; then
    grep "Repl ex" replica_0/md.log > exchange.log 2>/dev/null || {
        log "[WARN] 未找到交换记录"
    }
    
    if [[ -f "exchange.log" ]]; then
        # 计算交换接受率
        total_attempts=$(grep -c "Repl ex" exchange.log || echo 0)
        total_exchanges=$(grep "Repl ex" exchange.log | grep -c "x" || echo 0)
        
        if (( total_attempts > 0 )); then
            acceptance_rate=$(echo "scale=2; 100 * $total_exchanges / $total_attempts" | bc -l)
            log "交换统计:"
            log "  总尝试次数: $total_attempts"
            log "  成功交换次数: $total_exchanges"
            log "  接受率: ${acceptance_rate}%"
            
            # 评估接受率
            if (( $(echo "$acceptance_rate < 10" | bc -l) )); then
                log "[WARN] 接受率过低 (<10%)"
                log "建议: 减小温度范围或增加副本数量"
            elif (( $(echo "$acceptance_rate > 40" | bc -l) )); then
                log "[WARN] 接受率过高 (>40%)"
                log "建议: 增大温度范围或减少副本数量"
            else
                log "[OK] 接受率在推荐范围内 (10-40%)"
            fi
        fi
    fi
fi

# ============================================
# Phase 4: 解复用轨迹
# ============================================

log "Phase 4: 解复用轨迹 (demultiplexing)"

# 使用demux.pl脚本(如果可用)
if command -v demux.pl &> /dev/null; then
    log "使用demux.pl解复用..."
    
    # 创建副本列表
    for i in $(seq 0 $((NUM_REPLICAS-1))); do
        echo "replica_$i/md.log"
    done > replica_logs.txt
    
    demux.pl replica_logs.txt 2>&1 | tee demux.log
    
    log "解复用完成,生成连续温度轨迹"
else
    log "[WARN] demux.pl 未找到,跳过解复用"
    log "提示: 安装GROMACS时包含scripts目录以使用demux.pl"
fi

# ============================================
# Phase 5: 生成报告
# ============================================

log "Phase 5: 生成报告"

cat > REMD_REPORT.md << EOF
# REMD 模拟报告

## 模拟参数

- **REMD类型**: $REMD_TYPE
- **副本数量**: $NUM_REPLICAS
- **交换间隔**: $EXCHANGE_INTERVAL 步
- **模拟时间**: $SIM_TIME ps
- **时间步长**: $DT ps

EOF

if [[ "$REMD_TYPE" == "temperature" || "$REMD_TYPE" == "both" ]]; then
    cat >> REMD_REPORT.md << EOF
## 温度分布

| 副本 | 温度 (K) |
|------|----------|
EOF
    for i in $(seq 0 $((NUM_REPLICAS-1))); do
        echo "| $i | ${TEMPS[$i]} |" >> REMD_REPORT.md
    done
fi

if [[ "$REMD_TYPE" == "hamiltonian" || "$REMD_TYPE" == "both" ]]; then
    cat >> REMD_REPORT.md << EOF

## Lambda分布

| 副本 | Lambda |
|------|--------|
EOF
    for i in $(seq 0 $((NUM_REPLICAS-1))); do
        echo "| $i | ${LAMBDAS[$i]} |" >> REMD_REPORT.md
    done
fi

if [[ -f "exchange.log" ]] && (( total_attempts > 0 )); then
    cat >> REMD_REPORT.md << EOF

## 交换统计

- **总尝试次数**: $total_attempts
- **成功交换次数**: $total_exchanges
- **接受率**: ${acceptance_rate}%

### 评估

EOF
    if (( $(echo "$acceptance_rate < 10" | bc -l) )); then
        echo "⚠️ 接受率过低,建议减小温度范围或增加副本数量" >> REMD_REPORT.md
    elif (( $(echo "$acceptance_rate > 40" | bc -l) )); then
        echo "⚠️ 接受率过高,建议增大温度范围或减少副本数量" >> REMD_REPORT.md
    else
        echo "✅ 接受率在推荐范围内 (10-40%)" >> REMD_REPORT.md
    fi
fi

cat >> REMD_REPORT.md << EOF

## 输出文件

- \`replica_*/md.xtc\` - 各副本轨迹
- \`replica_*/md.edr\` - 各副本能量
- \`replica_*/md.log\` - 各副本日志
- \`exchange.log\` - 交换记录
- \`remd.log\` - 总日志

## 后续分析

### 1. 提取特定温度的轨迹
\`\`\`bash
# 使用demux.pl解复用后
gmx trjconv -s replica_0/md.tpr -f replica_0/md.xtc -o temp_${TEMP_MIN}K.xtc
\`\`\`

### 2. 分析各副本能量
\`\`\`bash
for i in {0..$((NUM_REPLICAS-1))}; do
    echo "Potential" | gmx energy -f replica_\$i/md.edr -o replica_\$i/potential.xvg
done
\`\`\`

### 3. 计算收敛性
\`\`\`bash
# 分析RMSD随时间变化
for i in {0..$((NUM_REPLICAS-1))}; do
    echo "Backbone Backbone" | gmx rms -s replica_\$i/md.tpr -f replica_\$i/md.xtc -o replica_\$i/rmsd.xvg
done
\`\`\`

### 4. 可视化交换模式
\`\`\`bash
# 绘制副本交换图
# (需要自定义脚本解析exchange.log)
\`\`\`

## 参考文献

- Sugita & Okamoto (1999). Replica-exchange molecular dynamics method for protein folding. Chem. Phys. Lett. 314, 141-151.
- GROMACS Manual 5.4.12: Replica exchange
EOF

log "报告已生成: REMD_REPORT.md"

# ============================================
# 完成
# ============================================

log "REMD模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/REMD_REPORT.md"

exit 0
