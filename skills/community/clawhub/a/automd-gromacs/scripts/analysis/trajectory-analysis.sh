#!/bin/bash
# GROMACS Trajectory Analysis Script
# 轨迹分析 - 对齐/叠加/PCA/聚类/自由能景观/MSM/TPT
# 基于 GROMACS Manual 3.11.15 (covar), 3.11.2 (anaeig), 3.11.10 (cluster)

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_TPR="${INPUT_TPR:-md.tpr}"           # 运行参数文件
INPUT_TRJ="${INPUT_TRJ:-md.xtc}"           # 轨迹文件
INPUT_NDX="${INPUT_NDX:-}"                 # 索引文件(可选)

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-trajectory-analysis}"

# 分析模式
ANALYSIS_MODE="${ANALYSIS_MODE:-all}"      # all/align/pca/cluster/fel/msm/tpt

# 轨迹对齐参数
FIT_GROUP="${FIT_GROUP:-Backbone}"         # 叠合参考组
ALIGN_METHOD="${ALIGN_METHOD:-rot+trans}"  # rot+trans/rotxy+transxy/translation

# PCA 参数
PCA_GROUP="${PCA_GROUP:-C-alpha}"          # PCA 分析组
PCA_FIRST="${PCA_FIRST:-1}"                # 第一个本征向量
PCA_LAST="${PCA_LAST:-10}"                 # 最后一个本征向量
PCA_NFRAMES="${PCA_NFRAMES:-50}"           # 极端投影帧数

# 聚类参数
CLUSTER_METHOD="${CLUSTER_METHOD:-gromos}" # gromos/linkage/jarvis-patrick/monte-carlo/diagonalization
CLUSTER_CUTOFF="${CLUSTER_CUTOFF:-0.15}"   # 聚类截断(nm)
CLUSTER_FIT="${CLUSTER_FIT:-yes}"          # 聚类前是否叠合

# 自由能景观参数
FEL_PC1="${FEL_PC1:-1}"                    # PC1 索引
FEL_PC2="${FEL_PC2:-2}"                    # PC2 索引
FEL_BINS="${FEL_BINS:-50}"                 # 网格数
FEL_TEMP="${FEL_TEMP:-300}"                # 温度(K)

# 时间范围
BEGIN_TIME="${BEGIN_TIME:-0}"              # 开始时间(ps)
END_TIME="${END_TIME:-}"                   # 结束时间(ps,空=全部)

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

# 自动选择分析组
auto_select_groups() {
    local tpr_file="$1"
    
    if gmx make_ndx -f "$tpr_file" -o temp_index.ndx <<< "q" 2>&1 | grep -q "C-alpha"; then
        echo "C-alpha"
    elif gmx make_ndx -f "$tpr_file" -o temp_index.ndx <<< "q" 2>&1 | grep -q "Backbone"; then
        echo "Backbone"
    elif gmx make_ndx -f "$tpr_file" -o temp_index.ndx <<< "q" 2>&1 | grep -q "Protein"; then
        echo "Protein"
    else
        echo "System"
    fi
    rm -f temp_index.ndx
}

# 验证聚类参数
validate_cluster_params() {
    # 检查截断值
    if (( $(echo "$CLUSTER_CUTOFF < 0.05" | bc -l) )); then
        log "[WARN] 聚类截断过小 ($CLUSTER_CUTOFF < 0.05 nm)"
        log "[AUTO-FIX] 增加到 0.1 nm"
        CLUSTER_CUTOFF=0.1
    fi
    
    if (( $(echo "$CLUSTER_CUTOFF > 1.0" | bc -l) )); then
        log "[WARN] 聚类截断过大 ($CLUSTER_CUTOFF > 1.0 nm)"
        log "[AUTO-FIX] 减少到 0.3 nm"
        CLUSTER_CUTOFF=0.3
    fi
}

# ============================================
# 前置检查
# ============================================

log "开始轨迹分析流程"
log "模式: $ANALYSIS_MODE"
log "输入: $INPUT_TPR, $INPUT_TRJ"

check_file "$INPUT_TPR"
check_file "$INPUT_TRJ"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 复制输入文件
cp ../"$INPUT_TPR" ./
cp ../"$INPUT_TRJ" ./
[[ -n "$INPUT_NDX" && -f "../$INPUT_NDX" ]] && cp ../"$INPUT_NDX" ./

# 自动检测分析组
DETECTED_GROUP=$(auto_select_groups "$INPUT_TPR")
if [ "$DETECTED_GROUP" != "C-alpha" ]; then
    log "[AUTO-FIX] 未检测到 C-alpha, 使用 $DETECTED_GROUP"
    PCA_GROUP="$DETECTED_GROUP"
    FIT_GROUP="$DETECTED_GROUP"
fi

# 验证聚类参数
validate_cluster_params

# ============================================
# 知识内嵌: 轨迹分析理论 (Manual 3.11.15, 3.11.2, 3.11.10)
# ============================================
# PCA (Principal Component Analysis):
# - gmx covar: 计算协方差矩阵并对角化
# - gmx anaeig: 分析本征向量和投影
# - 用途: 识别主要运动模式、降维、构象空间探索
# - 质量加权: -mwa (默认), 非质量加权: -no-mwa
# - 本征值: 运动幅度, 本征向量: 运动方向
#
# 聚类 (Clustering):
# - gromos: 最常用, 基于邻居数量
# - linkage: 单链接, 快速但可能产生链状簇
# - jarvis-patrick: 需要共同邻居
# - 截断: 0.1-0.3 nm (蛋白质), 0.05-0.15 nm (配体)
# - 用途: 识别代表性构象、构象转换
#
# 自由能景观 (Free Energy Landscape):
# - FEL = -kT ln(P(PC1, PC2))
# - 基于 PC1-PC2 投影的概率分布
# - 能量盆地 = 稳定态, 鞍点 = 转换态
# - 温度: 300 K (室温), 310 K (生理)
#
# 马尔可夫状态模型 (MSM):
# - 基于聚类的离散态转换
# - 转换概率矩阵: P(i→j) = N(i→j) / N(i)
# - 平衡分布: π = πP
# - 用途: 动力学分析、转换路径
#
# 转换路径理论 (TPT):
# - 识别 A→B 的主要转换路径
# - 通量: f(i→j) = π(i) P(i→j) q(j)
# - q(j): 从 j 到达 B 的概率
# - 用途: 机制研究、速率常数

# ============================================
# Phase 1: 轨迹预处理和对齐
# ============================================

if [[ "$ANALYSIS_MODE" == "all" || "$ANALYSIS_MODE" == "align" ]]; then
    log "Phase 1: 轨迹对齐和叠加"
    
    # 移除 PBC
    log "移除周期性边界条件..."
    echo "$DETECTED_GROUP System" | gmx trjconv -s "$INPUT_TPR" -f "$INPUT_TRJ" \
        -o traj_nopbc.xtc -pbc mol -center -ur compact || {
        echo "[ERROR-001] PBC 移除失败"
        echo "Fix: 检查组名称或使用 gmx make_ndx 创建索引"
        exit 1
    }
    
    # 叠合到参考结构
    log "叠合轨迹到参考结构 (方法: $ALIGN_METHOD)..."
    echo "$FIT_GROUP $DETECTED_GROUP" | gmx trjconv -s "$INPUT_TPR" -f traj_nopbc.xtc \
        -o traj_fit.xtc -fit "$ALIGN_METHOD" || {
        echo "[ERROR-002] 轨迹叠合失败"
        echo "Fix: 检查 FIT_GROUP=$FIT_GROUP 是否存在"
        exit 1
    }
    
    log "✓ 轨迹预处理完成: traj_fit.xtc"
fi

# ============================================
# Phase 2: 主成分分析 (PCA)
# ============================================

if [[ "$ANALYSIS_MODE" == "all" || "$ANALYSIS_MODE" == "pca" ]]; then
    log "Phase 2: 主成分分析 (PCA)"
    
    # 计算协方差矩阵
    log "计算协方差矩阵 (组: $PCA_GROUP)..."
    echo "$PCA_GROUP" | gmx covar -s "$INPUT_TPR" -f traj_fit.xtc \
        -o eigenval.xvg -v eigenvec.trr -av average.pdb \
        -l covar.log || {
        echo "[ERROR-003] 协方差计算失败"
        echo "Fix: 检查 PCA_GROUP=$PCA_GROUP 是否存在"
        exit 1
    }
    
    # 分析本征向量
    log "分析本征向量 $PCA_FIRST-$PCA_LAST..."
    echo "$PCA_GROUP" | gmx anaeig -s "$INPUT_TPR" -f traj_fit.xtc \
        -v eigenvec.trr -eig eigenval.xvg \
        -proj projection.xvg -first "$PCA_FIRST" -last "$PCA_LAST" || {
        echo "[ERROR-004] 本征向量分析失败"
        exit 1
    }
    
    # 2D 投影 (PC1 vs PC2)
    log "计算 2D 投影 (PC$FEL_PC1 vs PC$FEL_PC2)..."
    echo "$PCA_GROUP" | gmx anaeig -s "$INPUT_TPR" -f traj_fit.xtc \
        -v eigenvec.trr -eig eigenval.xvg \
        -2d projection_2d.xvg -first "$FEL_PC1" -last "$FEL_PC2" || {
        echo "[ERROR-005] 2D 投影失败"
        exit 1
    }
    
    # 极端投影
    log "生成极端投影结构 (PC$PCA_FIRST, $PCA_NFRAMES 帧)..."
    echo "$PCA_GROUP" | gmx anaeig -s "$INPUT_TPR" -f traj_fit.xtc \
        -v eigenvec.trr -eig eigenval.xvg \
        -extr extreme_pc${PCA_FIRST}.pdb -first "$PCA_FIRST" -last "$PCA_FIRST" \
        -nframes "$PCA_NFRAMES" || {
        echo "[ERROR-006] 极端投影失败"
        exit 1
    }
    
    log "✓ PCA 分析完成"
    log "  - 本征值: eigenval.xvg"
    log "  - 投影: projection.xvg, projection_2d.xvg"
    log "  - 极端结构: extreme_pc${PCA_FIRST}.pdb"
fi

# ============================================
# Phase 3: 结构聚类
# ============================================

if [[ "$ANALYSIS_MODE" == "all" || "$ANALYSIS_MODE" == "cluster" ]]; then
    log "Phase 3: 结构聚类 (方法: $CLUSTER_METHOD, 截断: $CLUSTER_CUTOFF nm)"
    
    # 执行聚类
    FIT_FLAG=""
    [[ "$CLUSTER_FIT" == "yes" ]] && FIT_FLAG="-fit"
    
    echo "$DETECTED_GROUP $DETECTED_GROUP" | gmx cluster -s "$INPUT_TPR" -f traj_fit.xtc \
        -method "$CLUSTER_METHOD" -cutoff "$CLUSTER_CUTOFF" $FIT_FLAG \
        -o rmsd-clust.xpm -g cluster.log -dist rmsd-dist.xvg \
        -sz clust-size.xvg -clid clust-id.xvg \
        -cl clusters.pdb || {
        echo "[ERROR-007] 聚类失败"
        echo "Fix: 调整 CLUSTER_CUTOFF 或更换 CLUSTER_METHOD"
        exit 1
    }
    
    log "✓ 聚类分析完成"
    log "  - 聚类矩阵: rmsd-clust.xpm"
    log "  - 聚类大小: clust-size.xvg"
    log "  - 聚类ID: clust-id.xvg"
    log "  - 代表结构: clusters.pdb"
fi

# ============================================
# Phase 4: 自由能景观 (FEL)
# ============================================

if [[ "$ANALYSIS_MODE" == "all" || "$ANALYSIS_MODE" == "fel" ]]; then
    log "Phase 4: 自由能景观重构 (PC$FEL_PC1 vs PC$FEL_PC2)"
    
    # 检查 PCA 结果
    if [[ ! -f "projection_2d.xvg" ]]; then
        log "[WARN] 未找到 2D 投影, 先运行 PCA..."
        echo "$PCA_GROUP" | gmx anaeig -s "$INPUT_TPR" -f traj_fit.xtc \
            -v eigenvec.trr -eig eigenval.xvg \
            -2d projection_2d.xvg -first "$FEL_PC1" -last "$FEL_PC2"
    fi
    
    # 计算自由能景观
    log "计算自由能 (温度: $FEL_TEMP K, 网格: ${FEL_BINS}x${FEL_BINS})..."
    
    # 使用 Python 脚本计算 FEL
    cat > calculate_fel.py << 'PYTHON_EOF'
import numpy as np
import sys

# 读取参数
bins = int(sys.argv[1])
temp = float(sys.argv[2])
input_file = sys.argv[3]
output_file = sys.argv[4]

# 物理常数
kB = 0.008314  # kJ/(mol·K)
kT = kB * temp

# 读取投影数据
data = np.loadtxt(input_file, comments=['#', '@'])
pc1 = data[:, 1]
pc2 = data[:, 2]

# 计算 2D 直方图
H, xedges, yedges = np.histogram2d(pc1, pc2, bins=bins)

# 计算自由能: F = -kT ln(P)
H[H == 0] = 1e-10  # 避免 log(0)
F = -kT * np.log(H / H.sum())

# 设置最小值为 0
F = F - F.min()

# 保存结果
with open(output_file, 'w') as f:
    f.write('# Free Energy Landscape (kJ/mol)\n')
    f.write(f'# PC1 bins: {bins}, PC2 bins: {bins}\n')
    f.write(f'# Temperature: {temp} K\n')
    for i in range(bins):
        for j in range(bins):
            pc1_val = (xedges[i] + xedges[i+1]) / 2
            pc2_val = (yedges[j] + yedges[j+1]) / 2
            f.write(f'{pc1_val:.6f} {pc2_val:.6f} {F[i,j]:.6f}\n')
        f.write('\n')

print(f"FEL saved to {output_file}")
print(f"Min energy: 0.0 kJ/mol, Max energy: {F.max():.2f} kJ/mol")
PYTHON_EOF
    
    python3 calculate_fel.py "$FEL_BINS" "$FEL_TEMP" projection_2d.xvg fel.dat || {
        echo "[ERROR-008] FEL 计算失败"
        echo "Fix: 检查 Python3 和 numpy 是否安装"
        exit 1
    }
    
    log "✓ 自由能景观完成: fel.dat"
fi

# ============================================
# Phase 5: 马尔可夫状态模型 (MSM)
# ============================================

if [[ "$ANALYSIS_MODE" == "all" || "$ANALYSIS_MODE" == "msm" ]]; then
    log "Phase 5: 马尔可夫状态模型 (MSM)"
    
    # 检查聚类结果
    if [[ ! -f "clust-id.xvg" ]]; then
        log "[ERROR-009] 未找到聚类结果, 请先运行聚类分析"
        exit 1
    fi
    
    # 计算转换矩阵
    log "计算状态转换矩阵..."
    
    cat > calculate_msm.py << 'PYTHON_EOF'
import numpy as np
import sys

# 读取聚类 ID
input_file = sys.argv[1]
output_prefix = sys.argv[2]

data = np.loadtxt(input_file, comments=['#', '@'])
time = data[:, 0]
cluster_id = data[:, 1].astype(int)

# 获取状态数
n_states = cluster_id.max() + 1
print(f"Number of states: {n_states}")

# 计算转换计数矩阵
transition_counts = np.zeros((n_states, n_states))
for i in range(len(cluster_id) - 1):
    transition_counts[cluster_id[i], cluster_id[i+1]] += 1

# 计算转换概率矩阵
transition_prob = np.zeros((n_states, n_states))
for i in range(n_states):
    row_sum = transition_counts[i].sum()
    if row_sum > 0:
        transition_prob[i] = transition_counts[i] / row_sum

# 计算平衡分布 (特征向量法)
eigenvalues, eigenvectors = np.linalg.eig(transition_prob.T)
idx = np.argmax(eigenvalues.real)
equilibrium = eigenvectors[:, idx].real
equilibrium = equilibrium / equilibrium.sum()

# 保存结果
np.savetxt(f'{output_prefix}_transition_matrix.dat', transition_prob, 
           header='Transition Probability Matrix P(i->j)', fmt='%.6f')
np.savetxt(f'{output_prefix}_equilibrium.dat', 
           np.column_stack([np.arange(n_states), equilibrium]),
           header='State Equilibrium_Probability', fmt='%d %.6f')

# 计算平均首次通过时间 (MFPT)
mfpt = np.zeros((n_states, n_states))
for target in range(n_states):
    # 移除目标态
    Q = np.delete(np.delete(transition_prob, target, 0), target, 1)
    I = np.eye(Q.shape[0])
    try:
        N = np.linalg.inv(I - Q)
        mfpt_to_target = N.sum(axis=1)
        
        # 填充 MFPT 矩阵
        idx = 0
        for i in range(n_states):
            if i != target:
                mfpt[i, target] = mfpt_to_target[idx]
                idx += 1
    except:
        pass

np.savetxt(f'{output_prefix}_mfpt.dat', mfpt,
           header='Mean First Passage Time (steps)', fmt='%.2f')

print(f"MSM results saved to {output_prefix}_*.dat")
print(f"Equilibrium distribution: {equilibrium}")
PYTHON_EOF
    
    python3 calculate_msm.py clust-id.xvg msm || {
        echo "[ERROR-010] MSM 计算失败"
        exit 1
    }
    
    log "✓ MSM 分析完成"
    log "  - 转换矩阵: msm_transition_matrix.dat"
    log "  - 平衡分布: msm_equilibrium.dat"
    log "  - 平均首次通过时间: msm_mfpt.dat"
fi

# ============================================
# Phase 6: 转换路径理论 (TPT)
# ============================================

if [[ "$ANALYSIS_MODE" == "all" || "$ANALYSIS_MODE" == "tpt" ]]; then
    log "Phase 6: 转换路径理论 (TPT)"
    
    # 检查 MSM 结果
    if [[ ! -f "msm_transition_matrix.dat" ]]; then
        log "[ERROR-011] 未找到 MSM 结果, 请先运行 MSM 分析"
        exit 1
    fi
    
    # 用户指定源态和目标态
    SOURCE_STATE="${SOURCE_STATE:-0}"
    TARGET_STATE="${TARGET_STATE:-1}"
    
    log "计算转换路径 (源态: $SOURCE_STATE → 目标态: $TARGET_STATE)..."
    
    cat > calculate_tpt.py << 'PYTHON_EOF'
import numpy as np
import sys

# 读取参数
trans_file = sys.argv[1]
equil_file = sys.argv[2]
source = int(sys.argv[3])
target = int(sys.argv[4])
output_file = sys.argv[5]

# 读取数据
P = np.loadtxt(trans_file)
equil_data = np.loadtxt(equil_file)
pi = equil_data[:, 1]

n_states = P.shape[0]

# 计算 committor q (从 i 到达 target 的概率)
q = np.zeros(n_states)
q[target] = 1.0

# 迭代求解 q
max_iter = 1000
tol = 1e-6
for iteration in range(max_iter):
    q_old = q.copy()
    for i in range(n_states):
        if i != source and i != target:
            q[i] = np.dot(P[i], q)
    
    if np.max(np.abs(q - q_old)) < tol:
        break

# 计算有效通量 f(i->j)
flux = np.zeros((n_states, n_states))
for i in range(n_states):
    for j in range(n_states):
        if i != j:
            flux[i, j] = max(0, pi[i] * P[i, j] * q[j] - pi[j] * P[j, i] * q[i])

# 计算总通量
total_flux = flux.sum()

# 识别主要路径 (通量 > 5% 总通量)
threshold = 0.05 * total_flux
major_paths = []
for i in range(n_states):
    for j in range(n_states):
        if flux[i, j] > threshold:
            major_paths.append((i, j, flux[i, j]))

major_paths.sort(key=lambda x: x[2], reverse=True)

# 保存结果
with open(output_file, 'w') as f:
    f.write(f'# Transition Path Theory: {source} -> {target}\n')
    f.write(f'# Total flux: {total_flux:.6e}\n')
    f.write(f'# Committor q:\n')
    for i, q_val in enumerate(q):
        f.write(f'#   State {i}: {q_val:.6f}\n')
    f.write('#\n')
    f.write('# Major transition paths (flux > 5% total):\n')
    f.write('# From To Flux Percentage\n')
    for i, j, f_val in major_paths:
        percentage = 100 * f_val / total_flux
        f.write(f'{i} {j} {f_val:.6e} {percentage:.2f}%\n')

print(f"TPT results saved to {output_file}")
print(f"Total flux: {total_flux:.6e}")
print(f"Number of major paths: {len(major_paths)}")
PYTHON_EOF
    
    python3 calculate_tpt.py msm_transition_matrix.dat msm_equilibrium.dat \
        "$SOURCE_STATE" "$TARGET_STATE" tpt_paths.dat || {
        echo "[ERROR-012] TPT 计算失败"
        exit 1
    }
    
    log "✓ TPT 分析完成: tpt_paths.dat"
fi

# ============================================
# Phase 7: 生成分析报告
# ============================================

log "生成分析报告..."

cat > TRAJECTORY_ANALYSIS_REPORT.md << EOF
# Trajectory Analysis Report

**Generated:** $(date)
**Analysis Mode:** $ANALYSIS_MODE

## Input Files
- TPR: $INPUT_TPR
- Trajectory: $INPUT_TRJ
- Time range: $BEGIN_TIME - ${END_TIME:-end} ps

## Analysis Parameters

### Alignment
- Fit group: $FIT_GROUP
- Method: $ALIGN_METHOD

### PCA
- Analysis group: $PCA_GROUP
- Eigenvectors: $PCA_FIRST - $PCA_LAST
- Extreme frames: $PCA_NFRAMES

### Clustering
- Method: $CLUSTER_METHOD
- Cutoff: $CLUSTER_CUTOFF nm
- Fit before clustering: $CLUSTER_FIT

### Free Energy Landscape
- PC1: $FEL_PC1, PC2: $FEL_PC2
- Grid: ${FEL_BINS}x${FEL_BINS}
- Temperature: $FEL_TEMP K

## Output Files

### Trajectory Processing
- \`traj_nopbc.xtc\` - PBC removed trajectory
- \`traj_fit.xtc\` - Aligned trajectory

### PCA Results
- \`eigenval.xvg\` - Eigenvalues
- \`eigenvec.trr\` - Eigenvectors
- \`projection.xvg\` - PC projections
- \`projection_2d.xvg\` - 2D projection (PC$FEL_PC1 vs PC$FEL_PC2)
- \`extreme_pc${PCA_FIRST}.pdb\` - Extreme structures along PC$PCA_FIRST
- \`average.pdb\` - Average structure

### Clustering Results
- \`rmsd-clust.xpm\` - RMSD cluster matrix
- \`cluster.log\` - Clustering details
- \`rmsd-dist.xvg\` - RMSD distribution
- \`clust-size.xvg\` - Cluster sizes
- \`clust-id.xvg\` - Cluster ID vs time
- \`clusters.pdb\` - Representative structures

### Free Energy Landscape
- \`fel.dat\` - Free energy surface (PC$FEL_PC1 vs PC$FEL_PC2)

### Markov State Model
- \`msm_transition_matrix.dat\` - Transition probability matrix
- \`msm_equilibrium.dat\` - Equilibrium distribution
- \`msm_mfpt.dat\` - Mean first passage times

### Transition Path Theory
- \`tpt_paths.dat\` - Major transition paths and fluxes

## Key Findings

### PCA Summary
EOF

# 添加 PCA 统计
if [[ -f "eigenval.xvg" ]]; then
    cat >> TRAJECTORY_ANALYSIS_REPORT.md << EOF
\`\`\`
$(grep -v '^[@#]' eigenval.xvg | head -10)
\`\`\`

EOF
fi

# 添加聚类统计
if [[ -f "cluster.log" ]]; then
    cat >> TRAJECTORY_ANALYSIS_REPORT.md << EOF
### Clustering Summary
\`\`\`
$(grep -E "Found|cluster" cluster.log | head -20)
\`\`\`

EOF
fi

# 添加 MSM 统计
if [[ -f "msm_equilibrium.dat" ]]; then
    cat >> TRAJECTORY_ANALYSIS_REPORT.md << EOF
### MSM Equilibrium Distribution
\`\`\`
$(cat msm_equilibrium.dat)
\`\`\`

EOF
fi

cat >> TRAJECTORY_ANALYSIS_REPORT.md << EOF
## Visualization Recommendations

### PCA
\`\`\`bash
# Plot eigenvalues
xmgrace eigenval.xvg

# Plot PC1 vs PC2
xmgrace projection_2d.xvg

# Visualize extreme structures
pymol extreme_pc${PCA_FIRST}.pdb
\`\`\`

### Free Energy Landscape
\`\`\`bash
# Plot FEL with gnuplot
gnuplot << GNUPLOT_EOF
set pm3d map
set palette defined (0 "blue", 5 "green", 10 "yellow", 15 "red")
splot 'fel.dat' with pm3d
GNUPLOT_EOF
\`\`\`

### Clustering
\`\`\`bash
# View cluster representatives
pymol clusters.pdb

# Plot cluster sizes
xmgrace clust-size.xvg

# Plot cluster ID vs time
xmgrace clust-id.xvg
\`\`\`

## References

1. Amadei A, et al. (1993) Essential dynamics of proteins. Proteins 17:412-425
2. Daura X, et al. (1999) Peptide folding. Angew Chem Int Ed 38:236-240
3. Noé F, et al. (2009) Constructing the equilibrium ensemble of folding pathways. PNAS 106:19011-19016
4. Metzner P, et al. (2009) Transition path theory for Markov jump processes. Multiscale Model Simul 7:1192-1219

---
**Analysis completed successfully**
EOF

log "✓ 报告生成完成: TRAJECTORY_ANALYSIS_REPORT.md"

# ============================================
# 完成
# ============================================

log "=========================================="
log "轨迹分析完成!"
log "=========================================="
log "输出目录: $OUTPUT_DIR"
log ""
log "主要结果:"
[[ -f "traj_fit.xtc" ]] && log "  ✓ 对齐轨迹: traj_fit.xtc"
[[ -f "eigenval.xvg" ]] && log "  ✓ PCA 本征值: eigenval.xvg"
[[ -f "projection_2d.xvg" ]] && log "  ✓ 2D 投影: projection_2d.xvg"
[[ -f "clusters.pdb" ]] && log "  ✓ 聚类结构: clusters.pdb"
[[ -f "fel.dat" ]] && log "  ✓ 自由能景观: fel.dat"
[[ -f "msm_transition_matrix.dat" ]] && log "  ✓ MSM 转换矩阵: msm_transition_matrix.dat"
[[ -f "tpt_paths.dat" ]] && log "  ✓ TPT 路径: tpt_paths.dat"
log ""
log "详细报告: TRAJECTORY_ANALYSIS_REPORT.md"
log "=========================================="
echo ""
echo "💡 想生成发表级图表？"
echo "   安装：clawhub install automd-viz"
echo "   使用：automd-viz --type trajectory --input $OUTPUT_DIR/ --style nature"
echo ""

exit 0

