#!/bin/bash
# GROMACS Non-Equilibrium Molecular Dynamics
# 非平衡分子动力学 - 流动/剪切/热流模拟
# 基于 GROMACS Manual 5.8.12 & 3.7

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-system.gro}"       # 平衡后的结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件
INPUT_CPT="${INPUT_CPT:-npt.cpt}"          # 检查点文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-non-equilibrium}"

# 非平衡模拟类型
NEMD_TYPE="${NEMD_TYPE:-cosine}"           # cosine/deform/acceleration/walls

# 余弦加速参数 (cosine acceleration)
# 用于测量粘度 - 最简单的方法
COS_ACCEL="${COS_ACCEL:-0.1}"              # 加速度振幅 (nm/ps^2)
                                            # 推荐: 0.01-1.0 nm/ps^2

# 盒子变形参数 (deform)
# 用于剪切流动模拟
DEFORM_RATE="${DEFORM_RATE:-0.0}"          # 变形速率 (nm/ps)
DEFORM_AXIS="${DEFORM_AXIS:-xy}"           # 变形轴: xy/xz/yz
                                            # xy: b(x) 剪切, xz: c(x) 剪切, yz: c(y) 剪切

# 恒定加速参数 (acceleration groups)
# 用于驱动流动
ACCEL_GROUPS="${ACCEL_GROUPS:-}"           # 加速组名称(空格分隔)
ACCEL_X="${ACCEL_X:-0.0}"                  # X方向加速度 (nm/ps^2)
ACCEL_Y="${ACCEL_Y:-0.0}"                  # Y方向加速度 (nm/ps^2)
ACCEL_Z="${ACCEL_Z:-0.0}"                  # Z方向加速度 (nm/ps^2)

# 壁面流动参数 (walls with position restraints)
WALL_GROUPS="${WALL_GROUPS:-}"             # 壁面组名称(空格分隔)
WALL_SPEED="${WALL_SPEED:-0.0}"            # 壁面速度 (nm/ps)
WALL_DIRECTION="${WALL_DIRECTION:-x}"      # 流动方向: x/y/z
WALL_POSRE_B="${WALL_POSRE_B:-}"           # B态位置限制文件

# 模拟参数
SIM_TIME="${SIM_TIME:-1000}"               # 模拟时间(ps)
DT="${DT:-0.002}"                          # 时间步长(ps)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
TEMPERATURE="${TEMPERATURE:-300}"          # 温度(K)

# 分析选项
ANALYZE_VISCOSITY="${ANALYZE_VISCOSITY:-yes}"    # 分析粘度
ANALYZE_VELOCITY_PROFILE="${ANALYZE_VELOCITY_PROFILE:-yes}"  # 分析速度剖面
ANALYZE_STRESS="${ANALYZE_STRESS:-yes}"    # 分析应力张量

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

# 验证余弦加速参数
validate_cosine_accel() {
    if [[ "$NEMD_TYPE" != "cosine" ]]; then
        return 0
    fi
    
    # 检查加速度范围
    if (( $(echo "$COS_ACCEL < 0.001" | bc -l) )); then
        log "[WARN] 余弦加速度过小 ($COS_ACCEL < 0.001 nm/ps^2)"
        log "[AUTO-FIX] 增加到 0.01 nm/ps^2"
        COS_ACCEL=0.01
    fi
    
    if (( $(echo "$COS_ACCEL > 10.0" | bc -l) )); then
        log "[WARN] 余弦加速度过大 ($COS_ACCEL > 10.0 nm/ps^2)"
        log "[INFO] 过大的加速度会导致系统远离平衡态"
        log "[AUTO-FIX] 减少到 1.0 nm/ps^2"
        COS_ACCEL=1.0
    fi
}

# 验证变形参数
validate_deform_params() {
    if [[ "$NEMD_TYPE" != "deform" ]]; then
        return 0
    fi
    
    # 检查变形速率
    if (( $(echo "$DEFORM_RATE == 0" | bc -l) )); then
        log "[WARN] 变形速率为0"
        log "[AUTO-FIX] 设置为默认值 0.001 nm/ps"
        DEFORM_RATE=0.001
    fi
    
    if (( $(echo "$DEFORM_RATE > 0.1" | bc -l) )); then
        log "[WARN] 变形速率过大 ($DEFORM_RATE > 0.1 nm/ps)"
        log "[INFO] 过大的变形速率会导致系统不稳定"
        log "[AUTO-FIX] 减少到 0.01 nm/ps"
        DEFORM_RATE=0.01
    fi
    
    # 验证变形轴
    case "$DEFORM_AXIS" in
        xy|xz|yz) ;;
        *)
            log "[WARN] 未知变形轴: $DEFORM_AXIS"
            log "[AUTO-FIX] 使用 xy (最常用)"
            DEFORM_AXIS=xy
            ;;
    esac
}

# 验证加速组参数
validate_acceleration_groups() {
    if [[ "$NEMD_TYPE" != "acceleration" ]]; then
        return 0
    fi
    
    if [[ -z "$ACCEL_GROUPS" ]]; then
        log "[WARN] 未指定加速组"
        log "[AUTO-FIX] 使用默认组 'System'"
        ACCEL_GROUPS="System"
    fi
    
    # 检查是否至少有一个方向有加速度
    local has_accel=false
    if (( $(echo "$ACCEL_X != 0" | bc -l) )); then has_accel=true; fi
    if (( $(echo "$ACCEL_Y != 0" | bc -l) )); then has_accel=true; fi
    if (( $(echo "$ACCEL_Z != 0" | bc -l) )); then has_accel=true; fi
    
    if [[ "$has_accel" == "false" ]]; then
        log "[WARN] 所有方向加速度为0"
        log "[AUTO-FIX] 设置X方向加速度为 0.1 nm/ps^2"
        ACCEL_X=0.1
    fi
}

# 验证壁面流动参数
validate_wall_params() {
    if [[ "$NEMD_TYPE" != "walls" ]]; then
        return 0
    fi
    
    if [[ -z "$WALL_GROUPS" ]]; then
        error "壁面流动需要指定 WALL_GROUPS"
    fi
    
    if (( $(echo "$WALL_SPEED == 0" | bc -l) )); then
        log "[WARN] 壁面速度为0"
        log "[AUTO-FIX] 设置为 0.01 nm/ps"
        WALL_SPEED=0.01
    fi
    
    if [[ -z "$WALL_POSRE_B" ]]; then
        log "[WARN] 未指定B态位置限制文件"
        log "[INFO] 壁面流动需要两个位置限制文件(A态和B态)"
        log "[INFO] B态文件应该是A态文件沿流动方向平移1nm"
    fi
}

# 失败重启
restart_from_checkpoint() {
    if [[ -f "nemd.cpt" ]]; then
        log "[AUTO-FIX] 从检查点重启模拟"
        gmx mdrun -v -deffnm nemd -cpi nemd.cpt \
            -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a nemd.log
        return $?
    fi
    return 1
}

# 分析粘度 (仅cosine方法)
analyze_viscosity() {
    if [[ "$NEMD_TYPE" != "cosine" ]] || [[ "$ANALYZE_VISCOSITY" != "yes" ]]; then
        return 0
    fi
    
    log "分析粘度..."
    
    # 从能量文件提取粘度
    if [[ -f "nemd.edr" ]]; then
        echo "Visco-Coeffic 1/Viscosity" | gmx energy -f nemd.edr \
            -o viscosity.xvg 2>&1 | tee viscosity.log || {
            log "[WARN] 粘度提取失败"
            return 1
        }
        
        if [[ -f "viscosity.xvg" ]]; then
            # 计算平均粘度
            awk '!/^[@#]/ {sum+=$2; n++} END {
                if(n>0) print "平均粘度:", sum/n, "Pa·s"
            }' viscosity.xvg > viscosity_avg.txt
            
            cat viscosity_avg.txt
        fi
    fi
}

# 分析速度剖面
analyze_velocity_profile() {
    if [[ "$ANALYZE_VELOCITY_PROFILE" != "yes" ]]; then
        return 0
    fi
    
    log "分析速度剖面..."
    
    # 使用 gmx traj 提取速度分布
    if [[ -f "nemd.xtc" ]] && [[ -f "nemd.tpr" ]]; then
        echo "System" | gmx traj -f nemd.xtc -s nemd.tpr -ov velocity.xvg \
            2>&1 | tee traj.log || {
            log "[WARN] 速度剖面提取失败"
            return 1
        }
    fi
}

# 分析应力张量
analyze_stress_tensor() {
    if [[ "$ANALYZE_STRESS" != "yes" ]]; then
        return 0
    fi
    
    log "分析应力张量..."
    
    if [[ -f "nemd.edr" ]]; then
        # 提取压力张量分量
        echo "Pres-XX Pres-YY Pres-ZZ Pres-XY Pres-XZ Pres-YZ" | \
            gmx energy -f nemd.edr -o pressure_tensor.xvg 2>&1 | tee stress.log || {
            log "[WARN] 应力张量提取失败"
            return 1
        }
        
        if [[ -f "pressure_tensor.xvg" ]]; then
            # 计算剪切应力统计
            awk '!/^[@#]/ {
                sumxx+=$2; sumyy+=$3; sumzz+=$4;
                sumxy+=$5; sumxz+=$6; sumyz+=$7;
                n++
            } END {
                print "平均压力张量 (bar):";
                print "  对角: XX=", sumxx/n, "YY=", sumyy/n, "ZZ=", sumzz/n;
                print "  非对角: XY=", sumxy/n, "XZ=", sumxz/n, "YZ=", sumyz/n
            }' pressure_tensor.xvg > stress_stats.txt
            
            cat stress_stats.txt
        fi
    fi
}

# ============================================
# 前置检查
# ============================================

log "开始非平衡分子动力学模拟"
log "类型: $NEMD_TYPE"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 验证参数
case "$NEMD_TYPE" in
    cosine)
        validate_cosine_accel
        ;;
    deform)
        validate_deform_params
        ;;
    acceleration)
        validate_acceleration_groups
        ;;
    walls)
        validate_wall_params
        ;;
    *)
        error "不支持的非平衡类型: $NEMD_TYPE (支持: cosine/deform/acceleration/walls)"
        ;;
esac

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

cat > nemd.mdp << 'EOFMDP'
; Non-Equilibrium Molecular Dynamics
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

; Pressure coupling (disabled for most NEMD)
pcoupl                  = no

; Velocity generation
gen_vel                 = no

; Constraints
constraints             = h-bonds
constraint_algorithm    = LINCS
lincs_iter              = 1
lincs_order             = 4

; COM motion removal (disabled for flow simulations)
comm-mode               = None

EOFMDP

# 替换占位符
sed -i "s/NSTEPS_PLACEHOLDER/$NSTEPS/" nemd.mdp
sed -i "s/DT_PLACEHOLDER/$DT/" nemd.mdp
sed -i "s/TEMP_PLACEHOLDER/$TEMPERATURE/" nemd.mdp

# 根据非平衡类型添加特定参数
case "$NEMD_TYPE" in
    cosine)
        log "配置余弦加速方法"
        cat >> nemd.mdp << EOFCOS

; Cosine Acceleration for Viscosity Measurement
; 余弦加速法测量粘度
cos-acceleration        = $COS_ACCEL

; 说明:
; - 加速度沿X方向，振幅为 cos(2πz/box_height)
; - 产生余弦速度剖面
; - 粘度自动计算并输出到能量文件
; - 推荐加速度: 0.01-1.0 nm/ps^2
EOFCOS
        ;;
    
    deform)
        log "配置盒子变形方法"
        
        # 根据变形轴设置deform参数
        case "$DEFORM_AXIS" in
            xy)
                # b(x) 剪切: Y方向盒子向量的X分量变化
                DEFORM_STR="0 0 0 $DEFORM_RATE 0 0"
                ;;
            xz)
                # c(x) 剪切: Z方向盒子向量的X分量变化
                DEFORM_STR="0 0 0 0 $DEFORM_RATE 0"
                ;;
            yz)
                # c(y) 剪切: Z方向盒子向量的Y分量变化
                DEFORM_STR="0 0 0 0 0 $DEFORM_RATE"
                ;;
        esac
        
        cat >> nemd.mdp << EOFDEFORM

; Box Deformation for Shear Flow
; 盒子变形产生剪切流
deform                  = $DEFORM_STR

; 说明:
; - deform格式: a(x) b(y) c(z) b(x) c(x) c(y)
; - 当前设置: $DEFORM_AXIS 剪切，速率 $DEFORM_RATE nm/ps
; - 粒子速度会自动修正以匹配流动
; - 可通过应力张量计算粘度
EOFDEFORM
        ;;
    
    acceleration)
        log "配置恒定加速方法"
        
        # 计算加速组数量
        local ngroups=$(echo "$ACCEL_GROUPS" | wc -w)
        
        cat >> nemd.mdp << EOFACCEL

; Constant Acceleration Groups
; 恒定加速组
acceleration-grps       = $ACCEL_GROUPS
EOFACCEL

        # 为每个组设置加速度
        local accel_x_str=""
        local accel_y_str=""
        local accel_z_str=""
        for i in $(seq 1 $ngroups); do
            accel_x_str="$accel_x_str $ACCEL_X"
            accel_y_str="$accel_y_str $ACCEL_Y"
            accel_z_str="$accel_z_str $ACCEL_Z"
        done
        
        cat >> nemd.mdp << EOFACCEL2
accelerate              = $accel_x_str ; X方向
                          $accel_y_str ; Y方向
                          $accel_z_str ; Z方向

; 说明:
; - 对指定组施加恒定加速度
; - 注意: 需要手动控制质心运动
; - 加速度单位: nm/ps^2
EOFACCEL2
        ;;
    
    walls)
        log "配置壁面流动方法"
        
        if [[ -n "$WALL_POSRE_B" ]]; then
            # 使用自由能lambda耦合驱动壁面
            cat >> nemd.mdp << EOFWALLS

; Wall-Driven Flow with Position Restraints
; 壁面驱动流动（位置限制法）
free-energy             = yes
init-lambda             = 0
delta-lambda            = $WALL_SPEED

; 说明:
; - 使用lambda耦合在A态和B态位置限制间插值
; - B态位置限制文件应沿流动方向平移1nm
; - delta-lambda设置壁面速度 (nm/ps)
; - 壁面受力 = dV/dλ
EOFWALLS
        else
            # 使用加速组驱动壁面
            cat >> nemd.mdp << EOFWALLS2

; Wall-Driven Flow with Acceleration
; 壁面驱动流动（加速法）
acceleration-grps       = $WALL_GROUPS
EOFWALLS2

            # 根据流动方向设置加速度
            local wall_accel=0.1
            case "$WALL_DIRECTION" in
                x) echo "accelerate              = $wall_accel 0 0" >> nemd.mdp ;;
                y) echo "accelerate              = 0 $wall_accel 0" >> nemd.mdp ;;
                z) echo "accelerate              = 0 0 $wall_accel" >> nemd.mdp ;;
            esac
        fi
        ;;
esac

log "[OK] MDP文件已生成: nemd.mdp"

# ============================================
# Phase 2: 预处理
# ============================================

log "Phase 2: 预处理 (grompp)"

GROMPP_ARGS="-f nemd.mdp -c $INPUT_GRO -p $INPUT_TOP -o nemd.tpr -maxwarn 1"

# 添加检查点文件
if [[ -f "$INPUT_CPT" ]]; then
    GROMPP_ARGS="$GROMPP_ARGS -t $INPUT_CPT"
fi

# 添加B态位置限制文件（壁面流动）
if [[ "$NEMD_TYPE" == "walls" ]] && [[ -n "$WALL_POSRE_B" ]]; then
    if [[ -f "../$WALL_POSRE_B" ]]; then
        cp "../$WALL_POSRE_B" .
        GROMPP_ARGS="$GROMPP_ARGS -r $WALL_POSRE_B"
    else
        log "[WARN] B态位置限制文件不存在: $WALL_POSRE_B"
    fi
fi

gmx grompp $GROMPP_ARGS 2>&1 | grep -E "WARNING|ERROR|Fatal" || true

[[ -f "nemd.tpr" ]] || error "TPR 生成失败"

# ============================================
# Phase 3: 运行模拟
# ============================================

log "Phase 3: 运行非平衡模拟"
log "模拟时间: $SIM_TIME ps"

case "$NEMD_TYPE" in
    cosine)
        log "余弦加速: $COS_ACCEL nm/ps^2"
        ;;
    deform)
        log "盒子变形: $DEFORM_AXIS 轴, 速率 $DEFORM_RATE nm/ps"
        ;;
    acceleration)
        log "恒定加速: X=$ACCEL_X, Y=$ACCEL_Y, Z=$ACCEL_Z nm/ps^2"
        ;;
    walls)
        log "壁面流动: 速度 $WALL_SPEED nm/ps, 方向 $WALL_DIRECTION"
        ;;
esac

gmx mdrun -v -deffnm nemd \
    -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee nemd.log || {
    log "[ERROR] 模拟失败,尝试重启..."
    restart_from_checkpoint || error "重启失败"
}

# ============================================
# Phase 4: 分析结果
# ============================================

log "Phase 4: 分析结果"

# 提取能量
if [[ -f "nemd.edr" ]]; then
    log "提取能量数据..."
    echo "Potential Temperature Pressure" | gmx energy -f nemd.edr \
        -o energy.xvg 2>&1 | tee energy.log || {
        log "[WARN] 能量提取失败"
    }
fi

# 分析粘度（仅cosine方法）
analyze_viscosity

# 分析速度剖面
analyze_velocity_profile

# 分析应力张量
analyze_stress_tensor

# ============================================
# Phase 5: 生成报告
# ============================================

log "Phase 5: 生成报告"

cat > NON_EQUILIBRIUM_REPORT.md << EOFREPORT
# Non-Equilibrium MD 模拟报告

## 模拟参数

- **非平衡类型**: $NEMD_TYPE
- **模拟时间**: $SIM_TIME ps
- **温度**: $TEMPERATURE K
- **时间步长**: $DT ps

EOFREPORT

# 添加类型特定参数
case "$NEMD_TYPE" in
    cosine)
        cat >> NON_EQUILIBRIUM_REPORT.md << EOFCOS

## 余弦加速法 (Cosine Acceleration)

### 参数

- **加速度振幅**: $COS_ACCEL nm/ps²
- **加速度方向**: X
- **加速度剖面**: a_x(z) = A cos(2πz/L_z)

### 理论背景

余弦加速法通过施加周期性加速度场产生速度梯度:

\`\`\`
a_x(z) + (η/ρ) ∂²v_x(z)/∂z² = 0
\`\`\`

产生的速度剖面:

\`\`\`
v_x(z) = V cos(2πz/L_z)
V = A (ρ/η) (L_z/2π)²
\`\`\`

粘度 η 自动从速度剖面振幅计算。

### 优点

- 盒子不变形，避免周期性边界问题
- 粘度自动计算并输出到能量文件
- 适合简单液体的粘度测量

### 推荐参数

- 加速度: 0.01-1.0 nm/ps² (取决于系统)
- 剪切率应小于系统最长弛豫时间的倒数
- 避免剪切变稀效应

EOFCOS
        ;;
    
    deform)
        cat >> NON_EQUILIBRIUM_REPORT.md << EOFDEFORM

## 盒子变形法 (Box Deformation)

### 参数

- **变形轴**: $DEFORM_AXIS
- **变形速率**: $DEFORM_RATE nm/ps
- **剪切率**: γ̇ = $DEFORM_RATE / L (L为盒子尺寸)

### 理论背景

通过连续变形模拟盒子产生剪切流:

\`\`\`
box(t) = box(t_s) + (t - t_s) × deform_rate
\`\`\`

粒子速度自动修正以匹配流动速度。

### 粘度计算

\`\`\`
η = σ_xy / γ̇
\`\`\`

其中 σ_xy 是剪切应力（从压力张量获取）。

### 优点

- 直接模拟剪切流动
- 可用于固体应变研究
- 支持各向异性变形

### 注意事项

- 变形速率不宜过大
- 需要足够长的模拟时间达到稳态
- 检查系统是否出现剪切变稀

EOFDEFORM
        ;;
    
    acceleration)
        cat >> NON_EQUILIBRIUM_REPORT.md << EOFACCEL

## 恒定加速法 (Constant Acceleration)

### 参数

- **加速组**: $ACCEL_GROUPS
- **加速度**: X=$ACCEL_X, Y=$ACCEL_Y, Z=$ACCEL_Z nm/ps²

### 理论背景

对指定原子组施加恒定加速度（质量加权力）:

\`\`\`
F_i = m_i × a
\`\`\`

产生相对于系统其余部分的运动。

### 应用场景

- 驱动流动
- 研究摩擦和阻力
- 非平衡态系综生成

### 注意事项

- 需要手动控制质心运动（comm-mode = None）
- 加速组的动能贡献到系统总动能
- 避免加速度过大导致系统不稳定

EOFACCEL
        ;;
    
    walls)
        cat >> NON_EQUILIBRIUM_REPORT.md << EOFWALLS

## 壁面驱动流动 (Wall-Driven Flow)

### 参数

- **壁面组**: $WALL_GROUPS
- **壁面速度**: $WALL_SPEED nm/ps
- **流动方向**: $WALL_DIRECTION

### 理论背景

通过移动壁面驱动流动，模拟Couette流:

- 使用位置限制 + lambda耦合: 壁面以恒定速度移动
- 使用加速组: 壁面受恒定力

### 应用场景

- 研究壁面效应
- 结构化壁面的摩擦
- 受限流体的流变学

### 注意事项

- 壁面原子需要适当的位置限制
- B态位置限制文件应沿流动方向平移1nm
- 壁面受力 = dV/dλ

EOFWALLS
        ;;
esac

cat >> NON_EQUILIBRIUM_REPORT.md << EOFOUT

## 输出文件

- \`nemd.xtc\` - 轨迹文件
- \`nemd.edr\` - 能量文件
- \`nemd.log\` - 模拟日志
- \`nemd.mdp\` - MDP配置文件
- \`energy.xvg\` - 能量-时间曲线

EOFOUT

if [[ -f "viscosity.xvg" ]]; then
    cat >> NON_EQUILIBRIUM_REPORT.md << EOFVISC

## 粘度分析

\`\`\`
$(cat viscosity_avg.txt)
\`\`\`

- \`viscosity.xvg\` - 粘度-时间曲线
- \`viscosity_avg.txt\` - 平均粘度

EOFVISC
fi

if [[ -f "pressure_tensor.xvg" ]]; then
    cat >> NON_EQUILIBRIUM_REPORT.md << EOFSTRESS

## 应力张量分析

\`\`\`
$(cat stress_stats.txt)
\`\`\`

- \`pressure_tensor.xvg\` - 压力张量-时间曲线
- \`stress_stats.txt\` - 应力统计

EOFSTRESS
fi

cat >> NON_EQUILIBRIUM_REPORT.md << EOFANALYSIS

## 后续分析

### 1. 可视化流动

\`\`\`bash
# 查看轨迹
gmx view -f nemd.xtc -s nemd.tpr

# 使用 VMD
vmd nemd.gro nemd.xtc
\`\`\`

### 2. 分析速度分布

\`\`\`bash
# 提取速度
echo "System" | gmx traj -f nemd.xtc -s nemd.tpr -ov velocity.xvg

# 按层分析速度剖面（需要自定义脚本）
# 将系统沿Z方向分层，计算每层的平均速度
\`\`\`

### 3. 计算剪切粘度

\`\`\`bash
# 方法1: 从余弦加速结果直接读取（cosine方法）
echo "1/Viscosity" | gmx energy -f nemd.edr -o inv_viscosity.xvg

# 方法2: 从应力和剪切率计算（deform方法）
# η = σ_xy / γ̇
echo "Pres-XY" | gmx energy -f nemd.edr -o shear_stress.xvg
# 手动计算: viscosity = <σ_xy> / shear_rate
\`\`\`

### 4. 检查系统稳定性

\`\`\`bash
# RMSD
echo "Backbone Backbone" | gmx rms -s nemd.tpr -f nemd.xtc -o rmsd.xvg

# 温度
echo "Temperature" | gmx energy -f nemd.edr -o temperature.xvg

# 压力
echo "Pressure" | gmx energy -f nemd.edr -o pressure.xvg
\`\`\`

### 5. 剪切率扫描

\`\`\`bash
# 运行多个剪切率以检查剪切变稀
for rate in 0.001 0.005 0.01 0.05 0.1; do
    COS_ACCEL=\$rate OUTPUT_DIR=nemd_\${rate} bash non-equilibrium.sh
done

# 绘制粘度 vs 剪切率曲线
\`\`\`

## 物理背景

### 非平衡态模拟

非平衡MD通过对系统施加外力或约束，使其偏离热力学平衡态:

1. **驱动力**: 电场、加速度、边界运动
2. **响应**: 电流、流动、热流
3. **输运性质**: 粘度、电导率、热导率

### 粘度测量方法比较

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 余弦加速 | 简单、自动计算 | 仅适合简单液体 | 快速粘度估计 |
| 盒子变形 | 直接模拟剪切 | 需要手动计算 | 一般流变学研究 |
| 恒定加速 | 灵活 | 需要控制质心 | 复杂流动 |
| 壁面驱动 | 真实边界条件 | 设置复杂 | 受限流体 |

### 剪切变稀 (Shear Thinning)

许多流体在高剪切率下粘度降低:

\`\`\`
η(γ̇) = η₀ / (1 + (λγ̇)ⁿ)
\`\`\`

- η₀: 零剪切粘度
- λ: 弛豫时间
- n: 幂律指数

**检查方法**: 运行多个剪切率，绘制 η vs γ̇ 曲线

### 推荐剪切率

剪切率应满足:

\`\`\`
γ̇ << 1/τ_relax
\`\`\`

其中 τ_relax 是系统最长弛豫时间。

- 简单液体: τ_relax ~ 1-10 ps → γ̇ < 0.1 ps⁻¹
- 聚合物: τ_relax ~ 100-1000 ps → γ̇ < 0.001 ps⁻¹

## 参考文献

- GROMACS Manual 5.8.12: Shear simulations
- Hess (2002). Determining the shear viscosity of model liquids from molecular dynamics simulations. J. Chem. Phys. 116, 209.
- Müller-Plathe (1997). Reversing the perturbation in nonequilibrium molecular dynamics. Phys. Rev. E 59, 4894.

## 质量检查

EOFANALYSIS

# 检查模拟是否完成
if grep -q "Finished mdrun" nemd.log 2>/dev/null; then
    echo "✅ 模拟成功完成" >> NON_EQUILIBRIUM_REPORT.md
else
    echo "⚠️ 模拟可能未完成,检查 nemd.log" >> NON_EQUILIBRIUM_REPORT.md
fi

# 检查输出文件
if [[ -f "nemd.xtc" ]] && [[ -s "nemd.xtc" ]]; then
    echo "✅ 轨迹文件已生成" >> NON_EQUILIBRIUM_REPORT.md
else
    echo "⚠️ 轨迹文件缺失或为空" >> NON_EQUILIBRIUM_REPORT.md
fi

if [[ -f "energy.xvg" ]] && [[ -s "energy.xvg" ]]; then
    echo "✅ 能量数据已记录" >> NON_EQUILIBRIUM_REPORT.md
else
    echo "⚠️ 能量数据缺失" >> NON_EQUILIBRIUM_REPORT.md
fi

log "报告已生成: NON_EQUILIBRIUM_REPORT.md"

# ============================================
# 完成
# ============================================

log "Non-Equilibrium MD 模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/NON_EQUILIBRIUM_REPORT.md"

exit 0
