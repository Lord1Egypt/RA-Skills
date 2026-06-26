#!/bin/bash
# GROMACS Analysis Script
# 基础分析流程 - RMSD, RMSF, Rg, 氢键, 二级结构
# 基于 1AKI 实战经验

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_TPR="${INPUT_TPR:-md.tpr}"           # 运行参数文件
INPUT_TRJ="${INPUT_TRJ:-md.xtc}"           # 轨迹文件

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-analysis}"

# 分析选项
ANALYZE_RMSD="${ANALYZE_RMSD:-yes}"        # RMSD 分析
ANALYZE_RMSF="${ANALYZE_RMSF:-yes}"        # RMSF 分析
ANALYZE_RG="${ANALYZE_RG:-yes}"            # 回旋半径
ANALYZE_HBOND="${ANALYZE_HBOND:-yes}"      # 氢键分析
ANALYZE_SASA="${ANALYZE_SASA:-yes}"        # 溶剂可及表面积
ANALYZE_DSSP="${ANALYZE_DSSP:-no}"         # 二级结构 (需要 dssp)

# 分析参数
FIT_GROUP="${FIT_GROUP:-Backbone}"         # 叠合参考组
RMSD_GROUP="${RMSD_GROUP:-Backbone}"       # RMSD 计算组
RMSF_GROUP="${RMSF_GROUP:-C-alpha}"        # RMSF 计算组
RG_GROUP="${RG_GROUP:-Protein}"            # Rg 计算组
HBOND_GROUP1="${HBOND_GROUP1:-Protein}"    # 氢键组1
HBOND_GROUP2="${HBOND_GROUP2:-Protein}"    # 氢键组2

# 时间范围
BEGIN_TIME="${BEGIN_TIME:-0}"              # 开始时间 (ps)
END_TIME="${END_TIME:-}"                   # 结束时间 (ps, 空=全部)

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
    
    # 检测系统组成
    if gmx make_ndx -f "$tpr_file" -o index.ndx <<< "q" 2>&1 | grep -q "Protein"; then
        echo "Protein"  # 有蛋白质
    elif gmx make_ndx -f "$tpr_file" -o index.ndx <<< "q" 2>&1 | grep -q "SOL"; then
        echo "System"  # 纯水或其他
    else
        echo "System"
    fi
}

# ============================================
# 前置检查
# ============================================

log "开始基础分析流程"
log "输入: $INPUT_TPR, $INPUT_TRJ"

check_file "$INPUT_TPR"
check_file "$INPUT_TRJ"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 复制输入文件到分析目录
cp ../"$INPUT_TPR" ./
cp ../"$INPUT_TRJ" ./

# 自动检测分析组
DETECTED_GROUP=$(auto_select_groups "$INPUT_TPR")
if [ "$DETECTED_GROUP" != "Protein" ]; then
    log "[AUTO-FIX] 未检测到蛋白质, 调整分析组 → System"
    FIT_GROUP="System"
    RMSD_GROUP="System"
    RMSF_GROUP="System"
    RG_GROUP="System"
    HBOND_GROUP1="System"
    HBOND_GROUP2="System"
fi

# ============================================
# 知识内嵌: 分析参数 (Manual 5.10)
# ============================================
# RMSD (Manual 5.10):
# 用途: 结构稳定性
# 组: Backbone (主链) 或 C-alpha
# 收敛: < 0.3 nm (稳定)
#
# RMSF (Manual 5.10):
# 用途: 残基柔性
# 组: C-alpha
# 高值: 柔性区域 (loop)
# 低值: 刚性区域 (helix, sheet)
#
# Rg (Manual 5.10):
# 用途: 蛋白质紧凑度
# 稳定: 平稳曲线
# 展开: 上升趋势
# 折叠: 下降趋势
#
# 氢键 (Manual 5.10):
# 用途: 二级结构稳定性
# 参数: -r 0.35 -a 30
# 距离: < 0.35 nm
# 角度: < 30°
#
# 能量 (Manual 5.10):
# 检查: Potential, Kinetic, Total
# 稳定: 无趋势
# 问题: 持续上升/下降

# ============================================
# Phase 1: 轨迹预处理
# ============================================

log "Phase 1: 轨迹预处理"

# 移除周期性边界条件效应
log "移除 PBC..."
echo "$DETECTED_GROUP System" | gmx trjconv -s "$INPUT_TPR" -f "$INPUT_TRJ" -o traj_nopbc.xtc -pbc mol -center -ur compact || {
    echo "[ERROR-001] PBC 移除失败"
    echo "Fix: gmx trjconv -s md.tpr -f md.xtc -o nopbc.xtc -pbc mol -center"
    echo "Manual: Chapter 5.10"
    exit 1
}

# 叠合到参考结构
log "叠合轨迹..."
echo "$FIT_GROUP $FIT_GROUP" | gmx trjconv -s "$INPUT_TPR" -f traj_nopbc.xtc -o traj_fit.xtc -fit rot+trans || {
    echo "[ERROR-002] 轨迹叠合失败"
    echo "Fix: gmx trjconv -s md.tpr -f nopbc.xtc -o fit.xtc -fit rot+trans"
    echo "Manual: Chapter 5.10"
    exit 1
}

log "轨迹预处理完成"

# ============================================
# Phase 2: RMSD 分析
# ============================================

if [[ "$ANALYZE_RMSD" == "yes" ]]; then
    log "Phase 2: RMSD 分析"
    
    # 计算 RMSD
    echo "$RMSD_GROUP" | gmx rms -s "$INPUT_TPR" -f traj_fit.xtc -o rmsd.xvg -tu ns || {
        echo "[ERROR-003] RMSD 计算失败"
        echo "Fix: gmx rms -s md.tpr -f fit.xtc -o rmsd.xvg"
        echo "Manual: Chapter 5.10"
        exit 1
    }
    
    # 统计 RMSD
    RMSD_AVG=$(grep -v '^[@#]' rmsd.xvg | awk '{sum+=$2; n++} END {printf "%.3f", sum/n}')
    RMSD_STD=$(grep -v '^[@#]' rmsd.xvg | awk '{sum+=$2; sum2+=$2*$2; n++} END {printf "%.3f", sqrt(sum2/n - (sum/n)^2)}')
    
    log "RMSD: $RMSD_AVG ± $RMSD_STD nm"
fi

# ============================================
# Phase 3: RMSF 分析
# ============================================

if [[ "$ANALYZE_RMSF" == "yes" ]]; then
    log "Phase 3: RMSF 分析"
    
    # 计算 RMSF
    echo "$RMSF_GROUP" | gmx rmsf -s "$INPUT_TPR" -f traj_fit.xtc -o rmsf.xvg -res || {
        echo "[ERROR-004] RMSF 计算失败"
        echo "Fix: gmx rmsf -s md.tpr -f fit.xtc -o rmsf.xvg -res"
        echo "Manual: Chapter 5.10"
        exit 1
    }
    
    # 统计 RMSF
    RMSF_AVG=$(grep -v '^[@#]' rmsf.xvg | awk '{sum+=$2; n++} END {printf "%.3f", sum/n}')
    RMSF_MAX=$(grep -v '^[@#]' rmsf.xvg | awk 'BEGIN{max=0} {if($2>max) max=$2} END {printf "%.3f", max}')
    
    log "RMSF: 平均 $RMSF_AVG nm, 最大 $RMSF_MAX nm"
fi

# ============================================
# Phase 4: 回旋半径分析
# ============================================

if [[ "$ANALYZE_RG" == "yes" ]]; then
    log "Phase 4: 回旋半径分析"
    
    # 计算 Rg
    echo "$RG_GROUP" | gmx gyrate -s "$INPUT_TPR" -f traj_fit.xtc -o gyrate.xvg || {
        echo "[ERROR-005] Rg 计算失败"
        echo "Fix: gmx gyrate -s md.tpr -f fit.xtc -o gyrate.xvg"
        echo "Manual: Chapter 5.10"
        exit 1
    }
    
    # 统计 Rg
    RG_AVG=$(grep -v '^[@#]' gyrate.xvg | awk '{sum+=$2; n++} END {printf "%.3f", sum/n}')
    RG_STD=$(grep -v '^[@#]' gyrate.xvg | awk '{sum+=$2; sum2+=$2*$2; n++} END {printf "%.3f", sqrt(sum2/n - (sum/n)^2)}')
    
    log "Rg: $RG_AVG ± $RG_STD nm"
fi

# ============================================
# Phase 5: 氢键分析
# ============================================

if [[ "$ANALYZE_HBOND" == "yes" ]]; then
    log "Phase 5: 氢键分析"
    
    # 计算氢键
    echo "$HBOND_GROUP1 $HBOND_GROUP2" | gmx hbond -s "$INPUT_TPR" -f traj_fit.xtc -num hbond.xvg || {
        echo "[ERROR-006] 氢键计算失败"
        echo "Fix: gmx hbond -s md.tpr -f fit.xtc -num hbond.xvg"
        echo "Manual: Chapter 5.10"
        exit 1
    }
    
    # 统计氢键
    HBOND_AVG=$(grep -v '^[@#]' hbond.xvg | awk '{sum+=$2; n++} END {printf "%.1f", sum/n}')
    
    log "氢键数: 平均 $HBOND_AVG"
fi

# ============================================
# Phase 6: SASA 分析
# ============================================

if [[ "$ANALYZE_SASA" == "yes" ]]; then
    log "Phase 6: SASA 分析"
    
    # 计算 SASA
    echo "$RG_GROUP" | gmx sasa -s "$INPUT_TPR" -f traj_fit.xtc -o sasa.xvg || {
        echo "[ERROR-007] SASA 计算失败"
        echo "Fix: gmx sasa -s md.tpr -f fit.xtc -o sasa.xvg"
        echo "Manual: Chapter 5.10"
        exit 1
    }
    
    # 统计 SASA
    SASA_AVG=$(grep -v '^[@#]' sasa.xvg | awk '{sum+=$2; n++} END {printf "%.1f", sum/n}')
    
    log "SASA: 平均 $SASA_AVG nm²"
fi

# ============================================
# Phase 7: 二级结构分析 (可选)
# ============================================

if [[ "$ANALYZE_DSSP" == "yes" ]]; then
    log "Phase 7: 二级结构分析"
    
    # 检查 dssp 是否可用
    if command -v dssp &> /dev/null || command -v mkdssp &> /dev/null; then
        echo "$RG_GROUP" | gmx do_dssp -s "$INPUT_TPR" -f traj_fit.xtc -o dssp.xpm -sc dssp.xvg || log "WARNING: DSSP 分析失败 (跳过)"
    else
        log "WARNING: dssp 未安装,跳过二级结构分析"
    fi
fi

# ============================================
# 生成报告
# ============================================

log "生成分析报告..."

cat > ANALYSIS_REPORT.md << EOF
# 基础分析报告

**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 输入参数

- **TPR 文件:** $INPUT_TPR
- **轨迹文件:** $INPUT_TRJ
- **叠合参考组:** $FIT_GROUP
- **时间范围:** $BEGIN_TIME - ${END_TIME:-全部} ps

---

## 分析结果

### 1. RMSD (均方根偏差)

**计算组:** $RMSD_GROUP

- **平均值:** $RMSD_AVG nm
- **标准差:** $RMSD_STD nm
- **数据文件:** \`rmsd.xvg\`

**解读:**
- RMSD < 0.2 nm: 结构非常稳定
- RMSD 0.2-0.3 nm: 结构稳定
- RMSD 0.3-0.5 nm: 结构较稳定,有一定波动
- RMSD > 0.5 nm: 结构不稳定或发生构象变化

---

### 2. RMSF (均方根涨落)

**计算组:** $RMSF_GROUP

- **平均值:** $RMSF_AVG nm
- **最大值:** $RMSF_MAX nm
- **数据文件:** \`rmsf.xvg\`

**解读:**
- RMSF 反映每个残基的柔性
- 高 RMSF 区域通常是 loop 或末端
- 低 RMSF 区域通常是二级结构核心

---

### 3. 回旋半径 (Rg)

**计算组:** $RG_GROUP

- **平均值:** $RG_AVG nm
- **标准差:** $RG_STD nm
- **数据文件:** \`gyrate.xvg\`

**解读:**
- Rg 反映蛋白质的紧凑程度
- Rg 稳定: 蛋白质折叠状态稳定
- Rg 增大: 蛋白质可能展开
- Rg 减小: 蛋白质可能塌缩

---

### 4. 氢键数

**计算组:** $HBOND_GROUP1 - $HBOND_GROUP2

- **平均值:** $HBOND_AVG
- **数据文件:** \`hbond.xvg\`

**解读:**
- 氢键维持蛋白质二级结构
- 氢键数稳定: 结构稳定
- 氢键数减少: 结构可能松散

---

### 5. 溶剂可及表面积 (SASA)

**计算组:** $RG_GROUP

- **平均值:** $SASA_AVG nm²
- **数据文件:** \`sasa.xvg\`

**解读:**
- SASA 反映蛋白质暴露于溶剂的程度
- SASA 增大: 蛋白质展开或疏水核心暴露
- SASA 减小: 蛋白质折叠或形成复合物

---

## 输出文件

### 轨迹文件
- \`traj_nopbc.xtc\` - 移除 PBC 的轨迹
- \`traj_fit.xtc\` - 叠合后的轨迹 (用于可视化)

### 分析数据
- \`rmsd.xvg\` - RMSD 时间序列
- \`rmsf.xvg\` - RMSF 残基分布
- \`gyrate.xvg\` - Rg 时间序列
- \`hbond.xvg\` - 氢键数时间序列
- \`sasa.xvg\` - SASA 时间序列

---

## 可视化建议

### 使用 Grace/Xmgrace
\`\`\`bash
xmgrace rmsd.xvg
xmgrace rmsf.xvg
\`\`\`

### 使用 Python (matplotlib)
\`\`\`python
import numpy as np
import matplotlib.pyplot as plt

# 读取 RMSD
data = np.loadtxt('rmsd.xvg', comments=['@', '#'])
plt.plot(data[:,0], data[:,1])
plt.xlabel('Time (ns)')
plt.ylabel('RMSD (nm)')
plt.savefig('rmsd.png')
\`\`\`

### 使用 VMD 查看轨迹
\`\`\`bash
vmd $INPUT_TPR traj_fit.xtc
\`\`\`

---

## 下一步分析

### 高级分析
- **主成分分析 (PCA):** \`gmx covar\` + \`gmx anaeig\`
- **聚类分析:** \`gmx cluster\`
- **自由能景观:** \`gmx sham\`
- **接触图:** \`gmx mdmat\`

### 特定分析
- **配体-蛋白质相互作用:** \`gmx mindist\`
- **膜蛋白分析:** \`gmx density\`
- **二面角分析:** \`gmx rama\`

---

**状态:** ✅ 分析完成
EOF

log "报告已生成: $OUTPUT_DIR/ANALYSIS_REPORT.md"

# ============================================
# 完成
# ============================================

log "基础分析流程完成!"
log "输出目录: $OUTPUT_DIR"
log "分析报告: $OUTPUT_DIR/ANALYSIS_REPORT.md"

exit 0
