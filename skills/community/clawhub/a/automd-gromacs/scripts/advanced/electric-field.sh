#!/bin/bash
# GROMACS Electric Field Simulation
# 电场模拟 - 恒定/振荡/脉冲电场
# 基于 GROMACS Manual 5.8.7 & 3.7 (electric-field-x/y/z)

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-system.gro}"       # 平衡后的结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件
INPUT_CPT="${INPUT_CPT:-npt.cpt}"          # 检查点文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-electric-field}"

# 电场类型
FIELD_TYPE="${FIELD_TYPE:-constant}"       # constant/oscillating/pulsed

# 电场方向 (可多选: x, y, z, xy, xz, yz, xyz)
FIELD_DIRECTION="${FIELD_DIRECTION:-z}"    # x/y/z/xy/xz/yz/xyz

# 电场强度 (V/nm)
# 推荐范围: 0.001-0.1 V/nm (生物系统), 0.1-2.0 V/nm (材料)
FIELD_STRENGTH_X="${FIELD_STRENGTH_X:-0.0}"
FIELD_STRENGTH_Y="${FIELD_STRENGTH_Y:-0.0}"
FIELD_STRENGTH_Z="${FIELD_STRENGTH_Z:-0.05}"

# 振荡电场参数 (仅 oscillating/pulsed)
FIELD_OMEGA="${FIELD_OMEGA:-150}"          # 角频率 (ps^-1)
FIELD_T0="${FIELD_T0:-5}"                  # 中心时间 (ps)

# 脉冲电场参数 (仅 pulsed)
FIELD_SIGMA="${FIELD_SIGMA:-1}"            # 脉冲宽度 (ps)

# 模拟参数
SIM_TIME="${SIM_TIME:-1000}"               # 模拟时间(ps)
DT="${DT:-0.002}"                          # 时间步长(ps)
NSTEPS=$(awk "BEGIN{printf "%d", $SIM_TIME / $DT}" )
TEMPERATURE="${TEMPERATURE:-300}"          # 温度(K)

# 分析选项
ANALYZE_DIPOLE="${ANALYZE_DIPOLE:-yes}"    # 分析偶极矩响应
ANALYZE_CONDUCTIVITY="${ANALYZE_CONDUCTIVITY:-no}"  # 分析电导率

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

# 验证电场强度
validate_field_strength() {
    local max_field=0
    
    # 找到最大电场强度
    for field in "$FIELD_STRENGTH_X" "$FIELD_STRENGTH_Y" "$FIELD_STRENGTH_Z"; do
        if (( $(echo "$field > $max_field" | bc -l) )); then
            max_field=$field
        fi
    done
    
    # 检查是否过大
    if (( $(echo "$max_field > 2.0" | bc -l) )); then
        log "[WARN] 电场强度过大 ($max_field > 2.0 V/nm)"
        log "[INFO] 推荐范围: 0.001-0.1 V/nm (生物), 0.1-2.0 V/nm (材料)"
        log "[AUTO-FIX] 保持用户设置,但建议检查系统稳定性"
    fi
    
    # 检查是否过小
    if (( $(echo "$max_field < 0.0001 && $max_field > 0" | bc -l) )); then
        log "[WARN] 电场强度过小 ($max_field < 0.0001 V/nm)"
        log "[AUTO-FIX] 增加到最小有效值 0.001 V/nm"
        
        # 按比例放大
        local scale=$(echo "0.001 / $max_field" | bc -l)
        FIELD_STRENGTH_X=$(echo "$FIELD_STRENGTH_X * $scale" | bc -l)
        FIELD_STRENGTH_Y=$(echo "$FIELD_STRENGTH_Y * $scale" | bc -l)
        FIELD_STRENGTH_Z=$(echo "$FIELD_STRENGTH_Z * $scale" | bc -l)
    fi
}

# 验证振荡参数
validate_oscillation_params() {
    if [[ "$FIELD_TYPE" == "oscillating" || "$FIELD_TYPE" == "pulsed" ]]; then
        # 检查角频率
        if (( $(echo "$FIELD_OMEGA < 1" | bc -l) )); then
            log "[WARN] 角频率过小 ($FIELD_OMEGA < 1 ps^-1)"
            log "[AUTO-FIX] 增加到 10 ps^-1"
            FIELD_OMEGA=10
        fi
        
        if (( $(echo "$FIELD_OMEGA > 1000" | bc -l) )); then
            log "[WARN] 角频率过大 ($FIELD_OMEGA > 1000 ps^-1)"
            log "[AUTO-FIX] 减少到 500 ps^-1"
            FIELD_OMEGA=500
        fi
        
        # 检查中心时间
        if (( $(echo "$FIELD_T0 < 0" | bc -l) )); then
            log "[WARN] 中心时间为负 ($FIELD_T0 < 0)"
            log "[AUTO-FIX] 设置为 0"
            FIELD_T0=0
        fi
        
        if (( $(echo "$FIELD_T0 > $SIM_TIME" | bc -l) )); then
            log "[WARN] 中心时间超出模拟时间 ($FIELD_T0 > $SIM_TIME)"
            log "[AUTO-FIX] 设置为模拟时间的一半"
            FIELD_T0=$(echo "$SIM_TIME / 2" | bc -l)
        fi
    fi
    
    if [[ "$FIELD_TYPE" == "pulsed" ]]; then
        # 检查脉冲宽度
        if (( $(echo "$FIELD_SIGMA < 0.1" | bc -l) )); then
            log "[WARN] 脉冲宽度过小 ($FIELD_SIGMA < 0.1 ps)"
            log "[AUTO-FIX] 增加到 0.5 ps"
            FIELD_SIGMA=0.5
        fi
        
        if (( $(echo "$FIELD_SIGMA > $SIM_TIME / 2" | bc -l) )); then
            log "[WARN] 脉冲宽度过大 ($FIELD_SIGMA > $SIM_TIME/2)"
            log "[AUTO-FIX] 减少到模拟时间的 1/4"
            FIELD_SIGMA=$(echo "$SIM_TIME / 4" | bc -l)
        fi
    fi
}

# 解析电场方向
parse_field_direction() {
    case "$FIELD_DIRECTION" in
        x)
            [[ "$FIELD_STRENGTH_X" == "0.0" ]] && FIELD_STRENGTH_X=0.05 || true
            ;;
        y)
            [[ "$FIELD_STRENGTH_Y" == "0.0" ]] && FIELD_STRENGTH_Y=0.05 || true
            ;;
        z)
            [[ "$FIELD_STRENGTH_Z" == "0.0" ]] && FIELD_STRENGTH_Z=0.05 || true
            ;;
        xy)
            [[ "$FIELD_STRENGTH_X" == "0.0" ]] && FIELD_STRENGTH_X=0.035 || true
            [[ "$FIELD_STRENGTH_Y" == "0.0" ]] && FIELD_STRENGTH_Y=0.035 || true
            ;;
        xz)
            [[ "$FIELD_STRENGTH_X" == "0.0" ]] && FIELD_STRENGTH_X=0.035 || true
            [[ "$FIELD_STRENGTH_Z" == "0.0" ]] && FIELD_STRENGTH_Z=0.035 || true
            ;;
        yz)
            [[ "$FIELD_STRENGTH_Y" == "0.0" ]] && FIELD_STRENGTH_Y=0.035 || true
            [[ "$FIELD_STRENGTH_Z" == "0.0" ]] && FIELD_STRENGTH_Z=0.035 || true
            ;;
        xyz)
            [[ "$FIELD_STRENGTH_X" == "0.0" ]] && FIELD_STRENGTH_X=0.029 || true
            [[ "$FIELD_STRENGTH_Y" == "0.0" ]] && FIELD_STRENGTH_Y=0.029 || true
            [[ "$FIELD_STRENGTH_Z" == "0.0" ]] && FIELD_STRENGTH_Z=0.029 || true
            ;;
        *)
            log "[WARN] 未知方向: $FIELD_DIRECTION"
            log "[AUTO-FIX] 使用 z 方向"
            FIELD_DIRECTION=z
            [[ "$FIELD_STRENGTH_Z" == "0.0" ]] && FIELD_STRENGTH_Z=0.05 || true
            ;;
    esac
}

# 验证电场配置
validate_field_config() {
    local has_field=false
    
    if (( $(echo "$FIELD_STRENGTH_X != 0" | bc -l) )); then
        has_field=true
    fi
    if (( $(echo "$FIELD_STRENGTH_Y != 0" | bc -l) )); then
        has_field=true
    fi
    if (( $(echo "$FIELD_STRENGTH_Z != 0" | bc -l) )); then
        has_field=true
    fi
    
    if [[ "$has_field" == "false" ]]; then
        log "[WARN] 所有方向电场强度为 0"
        log "[AUTO-FIX] 根据 FIELD_DIRECTION 设置默认值"
        parse_field_direction
    fi
}

# 失败重启
restart_from_checkpoint() {
    if [[ -f "efield.cpt" ]]; then
        log "[AUTO-FIX] 从检查点重启模拟"
        gmx mdrun -v -deffnm efield -cpi efield.cpt \
            -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee -a efield.log
        return $?
    fi
    return 1
}

# 分析偶极矩响应
analyze_dipole_response() {
    if [[ "$ANALYZE_DIPOLE" != "yes" ]]; then
        return 0
    fi
    
    log "分析偶极矩响应..."
    
    # 提取偶极矩
    echo "Mu-X Mu-Y Mu-Z" | gmx dipoles -f efield.xtc -s efield.tpr \
        -o dipole.xvg -eps epsilon.xvg -a aver.xvg -d dipdist.xvg \
        2>&1 | tee dipoles.log || {
        log "[WARN] 偶极矩分析失败"
        return 1
    }
    
    if [[ -f "dipole.xvg" ]]; then
        # 计算偶极矩统计
        awk '!/^[@#]/ {
            sumx+=$2; sumy+=$3; sumz+=$4; 
            sumx2+=$2*$2; sumy2+=$3*$3; sumz2+=$4*$4; 
            n++
        } END {
            avgx=sumx/n; avgy=sumy/n; avgz=sumz/n;
            stdx=sqrt(sumx2/n - avgx*avgx);
            stdy=sqrt(sumy2/n - avgy*avgy);
            stdz=sqrt(sumz2/n - avgz*avgz);
            print "偶极矩 X:", avgx, "±", stdx, "e·nm";
            print "偶极矩 Y:", avgy, "±", stdy, "e·nm";
            print "偶极矩 Z:", avgz, "±", stdz, "e·nm"
        }' dipole.xvg > dipole_stats.txt
        
        cat dipole_stats.txt
    fi
}

# 分析电导率
analyze_conductivity() {
    if [[ "$ANALYZE_CONDUCTIVITY" != "yes" ]]; then
        return 0
    fi
    
    log "分析电导率..."
    
    # 提取电流密度 (需要自定义分析)
    # 这里提供框架,实际实现需要根据系统类型调整
    
    log "[INFO] 电导率分析需要自定义实现"
    log "[INFO] 基本思路: σ = J/E (欧姆定律)"
    log "[INFO] J = Σ q_i v_i / V (电流密度)"
}

# ============================================
# 前置检查
# ============================================

log "开始电场模拟"
log "电场类型: $FIELD_TYPE"
log "电场方向: $FIELD_DIRECTION"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 验证参数
parse_field_direction
validate_field_config
validate_field_strength
validate_oscillation_params

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

cat > efield.mdp << 'EOFMDP'
; Electric Field Simulation
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

EOFMDP

# 替换占位符
sed -i "s/NSTEPS_PLACEHOLDER/$NSTEPS/" efield.mdp
sed -i "s/DT_PLACEHOLDER/$DT/" efield.mdp
sed -i "s/TEMP_PLACEHOLDER/$TEMPERATURE/" efield.mdp

# 添加电场配置
cat >> efield.mdp << EOFFIELD

; Electric Field Configuration
; Type: $FIELD_TYPE
; Direction: $FIELD_DIRECTION
EOFFIELD

# 根据电场类型设置参数
case "$FIELD_TYPE" in
    constant)
        # 恒定电场: E0 omega t0 sigma
        # omega=0, t0=0, sigma=0 → 恒定场
        cat >> efield.mdp << EOFCONST
electric-field-x        = $FIELD_STRENGTH_X 0 0 0
electric-field-y        = $FIELD_STRENGTH_Y 0 0 0
electric-field-z        = $FIELD_STRENGTH_Z 0 0 0
EOFCONST
        ;;
    
    oscillating)
        # 振荡电场: E0 omega t0 sigma
        # sigma=0 → 纯余弦振荡
        cat >> efield.mdp << EOFOSC
electric-field-x        = $FIELD_STRENGTH_X $FIELD_OMEGA 0 0
electric-field-y        = $FIELD_STRENGTH_Y $FIELD_OMEGA 0 0
electric-field-z        = $FIELD_STRENGTH_Z $FIELD_OMEGA 0 0
EOFOSC
        ;;
    
    pulsed)
        # 脉冲电场: E0 omega t0 sigma
        # sigma>0 → 高斯脉冲调制
        cat >> efield.mdp << EOFPULSE
electric-field-x        = $FIELD_STRENGTH_X $FIELD_OMEGA $FIELD_T0 $FIELD_SIGMA
electric-field-y        = $FIELD_STRENGTH_Y $FIELD_OMEGA $FIELD_T0 $FIELD_SIGMA
electric-field-z        = $FIELD_STRENGTH_Z $FIELD_OMEGA $FIELD_T0 $FIELD_SIGMA
EOFPULSE
        ;;
    
    *)
        error "不支持的电场类型: $FIELD_TYPE"
        ;;
esac

log "[OK] MDP文件已生成: efield.mdp"

# ============================================
# Phase 2: 预处理
# ============================================

log "Phase 2: 预处理 (grompp)"

if [[ -f "$INPUT_CPT" ]]; then
    gmx grompp -f efield.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" -t "$INPUT_CPT" \
        -o efield.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
else
    gmx grompp -f efield.mdp -c "$INPUT_GRO" -p "$INPUT_TOP" \
        -o efield.tpr -maxwarn 1 2>&1 | grep -E "WARNING|ERROR|Fatal" || true
fi

[[ -f "efield.tpr" ]] || error "TPR 生成失败"

# ============================================
# Phase 3: 运行模拟
# ============================================

log "Phase 3: 运行电场模拟"
log "模拟时间: $SIM_TIME ps"
log "电场强度: X=$FIELD_STRENGTH_X, Y=$FIELD_STRENGTH_Y, Z=$FIELD_STRENGTH_Z V/nm"

# 使用 -field 选项输出电场信息
gmx mdrun -v -deffnm efield -field \
    -ntomp $NTOMP ${GPU_ID:+-gpu_id $GPU_ID} 2>&1 | tee efield.log || {
    log "[ERROR] 模拟失败,尝试重启..."
    restart_from_checkpoint || error "重启失败"
}

# ============================================
# Phase 4: 分析结果
# ============================================

log "Phase 4: 分析结果"

# 提取能量
if [[ -f "efield.edr" ]]; then
    log "提取能量数据..."
    echo "Potential Temperature Pressure" | gmx energy -f efield.edr \
        -o energy.xvg 2>&1 | tee energy.log || {
        log "[WARN] 能量提取失败"
    }
fi

# 分析偶极矩
analyze_dipole_response

# 分析电导率
analyze_conductivity

# ============================================
# Phase 5: 生成报告
# ============================================

log "Phase 5: 生成报告"

cat > ELECTRIC_FIELD_REPORT.md << EOFREPORT
# Electric Field 模拟报告

## 模拟参数

- **电场类型**: $FIELD_TYPE
- **电场方向**: $FIELD_DIRECTION
- **模拟时间**: $SIM_TIME ps
- **温度**: $TEMPERATURE K
- **时间步长**: $DT ps

## 电场配置

### 电场强度 (V/nm)

| 方向 | 强度 (V/nm) | 状态 |
|------|-------------|------|
| X | $FIELD_STRENGTH_X | $([ "$FIELD_STRENGTH_X" != "0.0" ] && echo "✓ 激活" || echo "○ 关闭") |
| Y | $FIELD_STRENGTH_Y | $([ "$FIELD_STRENGTH_Y" != "0.0" ] && echo "✓ 激活" || echo "○ 关闭") |
| Z | $FIELD_STRENGTH_Z | $([ "$FIELD_STRENGTH_Z" != "0.0" ] && echo "✓ 激活" || echo "○ 关闭") |

EOFREPORT

# 添加类型特定参数
case "$FIELD_TYPE" in
    constant)
        cat >> ELECTRIC_FIELD_REPORT.md << EOFCONST

### 恒定电场

- **公式**: E(t) = E₀
- **特点**: 时间不变的静电场

EOFCONST
        ;;
    
    oscillating)
        cat >> ELECTRIC_FIELD_REPORT.md << EOFOSC

### 振荡电场

- **公式**: E(t) = E₀ cos[ω(t - t₀)]
- **角频率**: $FIELD_OMEGA ps⁻¹
- **周期**: $(echo "scale=3; 2 * 3.14159 / $FIELD_OMEGA" | bc -l) ps
- **频率**: $(echo "scale=3; $FIELD_OMEGA / (2 * 3.14159)" | bc -l) THz

EOFOSC
        ;;
    
    pulsed)
        cat >> ELECTRIC_FIELD_REPORT.md << EOFPULSE

### 脉冲电场

- **公式**: E(t) = E₀ exp[-(t-t₀)²/(2σ²)] cos[ω(t-t₀)]
- **角频率**: $FIELD_OMEGA ps⁻¹
- **中心时间**: $FIELD_T0 ps
- **脉冲宽度**: $FIELD_SIGMA ps
- **FWHM**: $(echo "scale=3; 2.355 * $FIELD_SIGMA" | bc -l) ps

EOFPULSE
        ;;
esac

cat >> ELECTRIC_FIELD_REPORT.md << EOFOUT

## 输出文件

- \`efield.xtc\` - 轨迹文件
- \`efield.edr\` - 能量文件
- \`efield.log\` - 模拟日志
- \`energy.xvg\` - 能量-时间曲线
- \`efield.mdp\` - MDP配置文件

EOFOUT

if [[ -f "dipole.xvg" ]]; then
    cat >> ELECTRIC_FIELD_REPORT.md << EOFDIPOLE

## 偶极矩分析

\`\`\`
$(cat dipole_stats.txt)
\`\`\`

- \`dipole.xvg\` - 偶极矩-时间曲线
- \`epsilon.xvg\` - 介电常数
- \`aver.xvg\` - 平均偶极矩
- \`dipdist.xvg\` - 偶极矩分布

EOFDIPOLE
fi

cat >> ELECTRIC_FIELD_REPORT.md << EOFANALYSIS

## 后续分析

### 1. 可视化电场效果

\`\`\`bash
# 查看轨迹
gmx view -f efield.xtc -s efield.tpr

# 使用 VMD
vmd efield.gro efield.xtc
\`\`\`

### 2. 分析结构响应

\`\`\`bash
# RMSD (检查结构稳定性)
echo "Backbone Backbone" | gmx rms -s efield.tpr -f efield.xtc -o rmsd.xvg

# 回转半径 (检查构象变化)
echo "Protein" | gmx gyrate -s efield.tpr -f efield.xtc -o gyrate.xvg

# 二级结构 (蛋白质)
echo "Protein" | gmx do_dssp -s efield.tpr -f efield.xtc -o dssp.xpm
\`\`\`

### 3. 分析取向

\`\`\`bash
# 分子取向相对于电场方向
# (需要自定义脚本)
\`\`\`

### 4. 电场强度扫描

\`\`\`bash
# 运行多个电场强度
for E in 0.01 0.02 0.05 0.1 0.2; do
    FIELD_STRENGTH_Z=\$E OUTPUT_DIR=efield_\${E} bash electric-field.sh
done

# 分析强度依赖性
\`\`\`

## 物理背景

### 电场单位转换

- 1 V/nm = 10⁷ V/m = 10⁹ V/cm
- 生物膜电场: ~0.01-0.1 V/nm
- 激光电场: 1-10 V/nm

### 电场效应

1. **偶极矩响应**: 分子偶极矩沿电场方向取向
2. **介电极化**: 系统介电常数变化
3. **离子迁移**: 带电粒子沿电场方向运动
4. **构象变化**: 蛋白质/膜结构响应电场

### 周期性边界条件注意事项

在 PBC 下,有效电场强度会因盒子大小和介电性质而放大。
实际电场 = 施加电场 × 修正因子 (通常 > 1)

参考: Ref. 146 (GROMACS Manual)

## 参考文献

- English & MacElroy (2003). Molecular dynamics simulations of microwave heating of water. J. Chem. Phys. 118, 1589.
- Saitta et al. (2012). Miller experiments in atomistic computer simulations. PNAS 111, 13768.
- GROMACS Manual 5.8.7: Electric fields

## 质量检查

EOFANALYSIS

# 检查模拟是否完成
if grep -q "Finished mdrun" efield.log 2>/dev/null; then
    echo "✅ 模拟成功完成" >> ELECTRIC_FIELD_REPORT.md
else
    echo "⚠️ 模拟可能未完成,检查 efield.log" >> ELECTRIC_FIELD_REPORT.md
fi

# 检查输出文件
if [[ -f "efield.xtc" ]] && [[ -s "efield.xtc" ]]; then
    echo "✅ 轨迹文件已生成" >> ELECTRIC_FIELD_REPORT.md
else
    echo "⚠️ 轨迹文件缺失或为空" >> ELECTRIC_FIELD_REPORT.md
fi

if [[ -f "energy.xvg" ]] && [[ -s "energy.xvg" ]]; then
    echo "✅ 能量数据已记录" >> ELECTRIC_FIELD_REPORT.md
else
    echo "⚠️ 能量数据缺失" >> ELECTRIC_FIELD_REPORT.md
fi

log "报告已生成: ELECTRIC_FIELD_REPORT.md"

# ============================================
# 完成
# ============================================

log "Electric Field 模拟完成!"
log "输出目录: $OUTPUT_DIR"
log "查看报告: $OUTPUT_DIR/ELECTRIC_FIELD_REPORT.md"

exit 0
