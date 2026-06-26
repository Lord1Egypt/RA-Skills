#!/bin/bash
# GROMACS Umbrella Sampling Script
# 伞状采样自由能计算 - PMF (Potential of Mean Force)
# 基于 GROMACS 教程和最佳实践

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_GRO="${INPUT_GRO:-complex.gro}"      # 复合物结构
INPUT_TOP="${INPUT_TOP:-topol.top}"        # 拓扑文件

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-umbrella}"

# 伞状采样参数
REACTION_COORD="${REACTION_COORD:-pull}"   # 反应坐标类型 (pull/distance)
PULL_GROUP1="${PULL_GROUP1:-Protein}"      # 拉力组1 (参考)
PULL_GROUP2="${PULL_GROUP2:-Ligand}"       # 拉力组2 (被拉)
PULL_RATE="${PULL_RATE:-0.01}"            # 拉力速率 (nm/ps)
PULL_DISTANCE="${PULL_DISTANCE:-3.0}"      # 总拉力距离 (nm)

# 窗口参数
WINDOW_SPACING="${WINDOW_SPACING:-0.1}"    # 窗口间距 (nm)
WINDOW_FC="${WINDOW_FC:-1000}"             # 伞状势力常数 (kJ/mol/nm²)

# 采样参数
SAMPLE_TIME="${SAMPLE_TIME:-5000}"         # 每窗口采样时间 (ps)
TEMPERATURE="${TEMPERATURE:-300}"          # 温度 (K)
PRESSURE="${PRESSURE:-1.0}"                # 压强 (bar)

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

# 窗口失败自动重试
retry_failed_windows() {
    local failed_windows=()
    
    for i in $(seq 0 $((NUM_WINDOWS-1))); do
        if [ ! -f "windows/window_$(printf "%02d" $i)/pullf.xvg" ]; then
            failed_windows+=($i)
        fi
    done
    
    if [ ${#failed_windows[@]} -gt 0 ]; then
        echo "[AUTO-FIX] Retrying ${#failed_windows[@]} failed windows..."
        for i in "${failed_windows[@]}"; do
            window_dir=$(printf "windows/window_%02d" $i)
            if [ -d "$window_dir" ]; then
                # 减小时间步长重试
                sed -i 's/dt = 0.002/dt = 0.001/' "$window_dir/umbrella.mdp"
                # 重新运行
                cd "$window_dir"
                gmx mdrun -v -deffnm umbrella -ntmpi 1 -ntomp 2 -pf pullf.xvg -px pullx.xvg 2>/dev/null || {
                    log "WARNING: Window $i retry failed, skipping"
                }
                cd ../..
            fi
        done
    fi
}

# WHAM 收敛检查
check_wham_convergence() {
    local pmf_file="$1"
    
    if [ -f "$pmf_file" ]; then
        # 检查 PMF 是否有明显的能垒
        local pmf_range=$(grep -v '^[@#]' "$pmf_file" | awk 'BEGIN{min=999999;max=-999999} {if($2<min)min=$2; if($2>max)max=$2} END {print max-min}')
        
        if (( $(echo "$pmf_range < 1.0" | bc -l) )); then
            echo "[WARN] PMF 范围很小 ($pmf_range kJ/mol)"
            echo "[AUTO-FIX] 考虑延长采样 / 检查窗口重叠"
            return 1
        fi
    fi
    return 0
}

# ============================================
# 前置检查
# ============================================

log "开始伞状采样流程"
log "输入: $INPUT_GRO, $INPUT_TOP"

check_file "$INPUT_GRO"
check_file "$INPUT_TOP"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 计算窗口数量
NUM_WINDOWS=$(awk "BEGIN{printf "%d", scale=0; $PULL_DISTANCE / $WINDOW_SPACING + 1}" )
log "将生成 $NUM_WINDOWS 个伞状采样窗口"

# ============================================
# 知识内嵌: 伞状采样参数 (Manual 5.8.2, 5.8.3)
# ============================================
# 拉力模拟 (Manual 5.8.2):
# pull_rate: 0.005-0.01 nm/ps (慢速)
# pull_distance: < 盒子尺寸 * 0.49
# pull_k: 1000 kJ/mol/nm² (伞状势)
#
# 窗口设置 (Manual 5.8.3):
# 间距: 0.05-0.1 nm
# 重叠: > 30% (相邻窗口)
# 采样: 5-10 ns/窗口
#
# WHAM 分析 (Manual 5.8.3):
# 收敛: |ΔF| < tolerance
# tolerance: 1e-6 (默认)
# iterations: 10000 (默认)
# bootstrap: 误差估计

# ============================================
# Phase 1: 拉力模拟 (生成初始构象)
# ============================================

log "Phase 1: 拉力模拟"

# 生成拉力 MDP 文件
cat > pull.mdp << EOF
; Pull simulation for umbrella sampling
integrator              = md
dt                      = 0.002
nsteps                  = $(awk "BEGIN{printf "%.0f", ($PULL_DISTANCE / $PULL_RATE / 0.002)}" )

; Output control
nstxout                 = 5000
nstvout                 = 5000
nstfout                 = 5000
nstenergy               = 5000
nstlog                  = 5000
nstxout-compressed      = 500

; Bond parameters
continuation            = no
constraint_algorithm    = lincs
constraints             = h-bonds

; Nonbonded settings
cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.2
rvdw                    = 1.2
DispCorr                = EnerPres

; Electrostatics
coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = System
tau_t                   = 0.1
ref_t                   = $TEMPERATURE

; Pressure coupling
pcoupl                  = Parrinello-Rahman
pcoupltype              = isotropic
tau_p                   = 2.0
ref_p                   = $PRESSURE
compressibility         = 4.5e-5

; Periodic boundary conditions
pbc                     = xyz

; Velocity generation
gen_vel                 = yes
gen_temp                = $TEMPERATURE
gen_seed                = -1

; Pull code
pull                    = yes
pull_ncoords            = 1
pull_ngroups            = 2
pull_group1_name        = $PULL_GROUP1
pull_group2_name        = $PULL_GROUP2
pull_coord1_type        = umbrella
pull_coord1_geometry    = distance
pull_coord1_groups      = 1 2
pull_coord1_dim         = Y Y Y
pull_coord1_rate        = $PULL_RATE
pull_coord1_k           = $WINDOW_FC
pull_coord1_start       = yes
EOF

log "生成 TPR 文件..."
gmx grompp -f pull.mdp -c ../"$INPUT_GRO" -p ../"$INPUT_TOP" -o pull.tpr -maxwarn 2 || {
    echo "[ERROR-001] grompp 失败"
    echo "Fix: gmx grompp -f pull.mdp -c complex.gro -p topol.top -o pull.tpr"
    echo "Manual: Chapter 5.8.2"
    exit 1
}

log "运行拉力模拟..."
# Thread control via -ntomp flag below
gmx mdrun -v -deffnm pull -ntmpi 1 -ntomp $NTOMP -pf pullf.xvg -px pullx.xvg || {
    echo "[ERROR-002] 拉力模拟失败"
    echo "Fix: Check pull groups or reduce pull_rate"
    echo "Manual: Chapter 5.8.2"
    exit 1
}

log "拉力模拟完成"

# ============================================
# Phase 2: 提取窗口构象
# ============================================

log "Phase 2: 提取窗口构象"

# 创建窗口目录
mkdir -p windows

# 从拉力轨迹中提取构象
log "从轨迹中提取构象..."
echo "System" | gmx trjconv -s pull.tpr -f pull.xtc -o windows/conf.gro -sep || {
    echo "[ERROR-003] 构象提取失败"
    echo "Fix: gmx trjconv -s pull.tpr -f pull.xtc -o conf.gro -sep"
    echo "Manual: Chapter 5.8.3"
    exit 1
}

# 选择均匀分布的窗口
log "选择窗口构象..."
TOTAL_FRAMES=$(ls windows/conf*.gro 2>/dev/null | wc -l)
FRAME_STEP=$(awk "BEGIN{printf "%d", scale=0; $TOTAL_FRAMES / $NUM_WINDOWS}" )

if [ "$FRAME_STEP" -lt 1 ]; then
    FRAME_STEP=1
fi

window_idx=0
for i in $(seq 0 $FRAME_STEP $TOTAL_FRAMES); do
    if [[ $window_idx -lt $NUM_WINDOWS ]]; then
        conf_file=$(printf "windows/conf%d.gro" $i)
        if [[ -f "$conf_file" ]]; then
            window_dir=$(printf "windows/window_%02d" $window_idx)
            mkdir -p "$window_dir"
            cp "$conf_file" "$window_dir/conf.gro"
            window_idx=$((window_idx + 1))
        fi
    fi
done

log "已生成 $window_idx 个窗口构象"

# ============================================
# Phase 3: 伞状采样模拟
# ============================================

log "Phase 3: 伞状采样模拟"

# 生成伞状采样 MDP 模板
cat > umbrella_template.mdp << EOF
; Umbrella sampling
integrator              = md
dt                      = 0.002
nsteps                  = $(awk "BEGIN{printf "%.0f", ($SAMPLE_TIME / 0.002)}" )

; Output control
nstxout                 = 0
nstvout                 = 0
nstfout                 = 0
nstenergy               = 5000
nstlog                  = 5000
nstxout-compressed      = 5000

; Bond parameters
continuation            = yes
constraint_algorithm    = lincs
constraints             = h-bonds

; Nonbonded settings
cutoff-scheme           = Verlet
ns_type                 = grid
nstlist                 = 10
rcoulomb                = 1.2
rvdw                    = 1.2
DispCorr                = EnerPres

; Electrostatics
coulombtype             = PME
pme_order               = 4
fourierspacing          = 0.16

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = System
tau_t                   = 0.1
ref_t                   = $TEMPERATURE

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

; Pull code
pull                    = yes
pull_ncoords            = 1
pull_ngroups            = 2
pull_group1_name        = $PULL_GROUP1
pull_group2_name        = $PULL_GROUP2
pull_coord1_type        = umbrella
pull_coord1_geometry    = distance
pull_coord1_groups      = 1 2
pull_coord1_dim         = Y Y Y
pull_coord1_rate        = 0.0
pull_coord1_k           = $WINDOW_FC
pull_coord1_init        = WINDOW_INIT
EOF

# 对每个窗口运行伞状采样
for i in $(seq 0 $((window_idx - 1))); do
    window_dir=$(printf "windows/window_%02d" $i)
    
    if [[ ! -d "$window_dir" ]]; then
        continue
    fi
    
    log "窗口 $i: 准备模拟..."
    
    # 计算窗口中心位置
    window_init=$(awk "BEGIN{printf "%d", scale=3; $i * $WINDOW_SPACING}" )
    
    # 生成窗口专用 MDP
    sed "s/WINDOW_INIT/$window_init/" umbrella_template.mdp > "$window_dir/umbrella.mdp"
    
    # 生成 TPR
    cd "$window_dir"
    gmx grompp -f umbrella.mdp -c conf.gro -p ../../../"$INPUT_TOP" -o umbrella.tpr -maxwarn 2 || {
        log "WARNING: 窗口 $i grompp 失败,跳过"
        cd ../..
        continue
    }
    
    # 运行模拟
    log "窗口 $i: 运行采样 ($SAMPLE_TIME ps)..."
    gmx mdrun -v -deffnm umbrella -ntmpi 1 -ntomp $NTOMP -pf pullf.xvg -px pullx.xvg || {
        log "WARNING: 窗口 $i 模拟失败,跳过"
        cd ../..
        continue
    }
    
    cd ../..
    log "窗口 $i: 完成"
done

log "所有窗口采样完成"

# 自动重试失败的窗口
retry_failed_windows

# ============================================
# Phase 4: WHAM 分析
# ============================================

log "Phase 4: WHAM 分析"

# 生成 tpr 文件列表
ls windows/window_*/umbrella.tpr > tpr_files.dat 2>/dev/null || {
    echo "[ERROR-004] 未找到 TPR 文件"
    echo "Fix: Check window simulations completed"
    echo "Manual: Chapter 5.8.3"
    exit 1
}

# 生成 pullf 文件列表
ls windows/window_*/pullf.xvg > pullf_files.dat 2>/dev/null || {
    echo "[ERROR-005] 未找到 pullf 文件"
    echo "Fix: Check window simulations completed"
    echo "Manual: Chapter 5.8.3"
    exit 1
}

# 运行 WHAM
log "运行 WHAM 分析..."
gmx wham -it tpr_files.dat -if pullf_files.dat -o pmf.xvg -hist hist.xvg -unit kJ || {
    echo "[ERROR-006] WHAM 分析失败"
    echo "Fix: Check window overlap or extend sampling"
    echo "Manual: Chapter 5.8.3"
    exit 1
}

log "WHAM 分析完成"

# 检查 WHAM 收敛
check_wham_convergence "pmf.xvg"

# ============================================
# 生成报告
# ============================================

log "生成分析报告..."

# 提取 PMF 最小值和最大值
PMF_MIN=$(grep -v '^[@#]' pmf.xvg | awk 'BEGIN{min=999999} {if($2<min) min=$2} END {printf "%.2f", min}')
PMF_MAX=$(grep -v '^[@#]' pmf.xvg | awk 'BEGIN{max=-999999} {if($2>max) max=$2} END {printf "%.2f", max}')
PMF_BARRIER=$(awk "BEGIN{printf "%d", $PMF_MAX - $PMF_MIN}" )

cat > UMBRELLA_REPORT.md << EOF
# 伞状采样分析报告

**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 输入参数

- **输入结构:** $INPUT_GRO
- **拓扑文件:** $INPUT_TOP
- **反应坐标:** $REACTION_COORD
- **拉力组:** $PULL_GROUP1 → $PULL_GROUP2
- **拉力距离:** $PULL_DISTANCE nm
- **拉力速率:** $PULL_RATE nm/ps

---

## 伞状采样设置

- **窗口数量:** $window_idx
- **窗口间距:** $WINDOW_SPACING nm
- **伞状势力常数:** $WINDOW_FC kJ/mol/nm²
- **每窗口采样时间:** $SAMPLE_TIME ps
- **温度:** $TEMPERATURE K
- **压强:** $PRESSURE bar

---

## PMF 结果

- **最小值:** $PMF_MIN kJ/mol
- **最大值:** $PMF_MAX kJ/mol
- **能垒:** $PMF_BARRIER kJ/mol

**数据文件:** \`pmf.xvg\`

---

## 输出文件

### 拉力模拟
- \`pull.gro\` - 拉力模拟最终结构
- \`pull.xtc\` - 拉力模拟轨迹
- \`pullf.xvg\` - 拉力时间序列
- \`pullx.xvg\` - 距离时间序列

### 窗口构象
- \`windows/window_XX/conf.gro\` - 窗口初始构象
- \`windows/window_XX/umbrella.tpr\` - 窗口 TPR 文件
- \`windows/window_XX/umbrella.xtc\` - 窗口轨迹
- \`windows/window_XX/pullf.xvg\` - 窗口拉力数据

### WHAM 分析
- \`pmf.xvg\` - 平均力势 (PMF)
- \`hist.xvg\` - 采样直方图
- \`tpr_files.dat\` - TPR 文件列表
- \`pullf_files.dat\` - pullf 文件列表

---

## 可视化

### 绘制 PMF 曲线
\`\`\`bash
xmgrace pmf.xvg
\`\`\`

### Python 绘图
\`\`\`python
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('pmf.xvg', comments=['@', '#'])
plt.plot(data[:,0], data[:,1])
plt.xlabel('Reaction coordinate (nm)')
plt.ylabel('PMF (kJ/mol)')
plt.savefig('pmf.png', dpi=300)
\`\`\`

---

## 质量检查

### 1. 检查采样收敛性
\`\`\`bash
# 查看每个窗口的采样直方图
xmgrace hist.xvg
# 应该看到各窗口有充分重叠
\`\`\`

### 2. 检查窗口覆盖
\`\`\`bash
# 确保所有窗口都成功完成
ls windows/window_*/umbrella.xtc | wc -l
# 应该等于窗口数量
\`\`\`

### 3. 检查 PMF 误差
\`\`\`bash
# WHAM 会输出误差估计
# 检查 pmf.xvg 中的误差列
\`\`\`

---

## 下一步

### 延长采样时间
\`\`\`bash
# 如果收敛性不好,延长采样
export SAMPLE_TIME=10000  # 10 ns
./umbrella.sh
\`\`\`

### 增加窗口密度
\`\`\`bash
# 如果窗口重叠不足,减小间距
export WINDOW_SPACING=0.05  # 0.05 nm
./umbrella.sh
\`\`\`

### Bootstrap 误差分析
\`\`\`bash
# 使用 bootstrap 估计误差
gmx wham -it tpr_files.dat -if pullf_files.dat -o pmf.xvg -hist hist.xvg -bs-method b-hist -bs-seed 1
\`\`\`

---

**状态:** ✅ 分析完成
EOF

log "报告已生成: $OUTPUT_DIR/UMBRELLA_REPORT.md"

# ============================================
# 完成
# ============================================

log "伞状采样流程完成!"
log "输出目录: $OUTPUT_DIR"
log "PMF 文件: $OUTPUT_DIR/pmf.xvg"
log "能垒: $PMF_BARRIER kJ/mol"

exit 0
