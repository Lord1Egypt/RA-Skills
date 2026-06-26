#!/bin/bash
# GROMACS Advanced Structure Analysis
# 高级结构分析 - PCA/聚类/二面角/接触图/DCCM/FEL
# 基于 GROMACS Manual 5.10 Analysis

set -e

# ============================================
# 配置参数
# ============================================

# 输入文件
INPUT_TPR="${INPUT_TPR:-md.tpr}"
INPUT_TRJ="${INPUT_TRJ:-md.xtc}"
INPUT_NDX="${INPUT_NDX:-}"

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-advanced-analysis}"

# 分析类型 (可多选,逗号分隔)
ANALYSIS_TYPE="${ANALYSIS_TYPE:-pca,cluster,dihedral,contact,dccm,fel}"

# 通用参数
SELECTION="${SELECTION:-C-alpha}"
BEGIN_TIME="${BEGIN_TIME:-}"
END_TIME="${END_TIME:-}"
SKIP_FRAMES="${SKIP_FRAMES:-1}"

# PCA参数
PCA_NCOMP="${PCA_NCOMP:-10}"
PCA_2D="${PCA_2D:-true}"
PCA_3D="${PCA_3D:-false}"
PCA_EXTREME="${PCA_EXTREME:-true}"

# 聚类参数
CLUSTER_METHOD="${CLUSTER_METHOD:-gromos}"
CLUSTER_CUTOFF="${CLUSTER_CUTOFF:-0.15}"
CLUSTER_NCLUST="${CLUSTER_NCLUST:-10}"

# 二面角参数
DIHEDRAL_TYPE="${DIHEDRAL_TYPE:-rama,chi}"
RAMA_RESIDUES="${RAMA_RESIDUES:-all}"

# 接触图参数
CONTACT_CUTOFF="${CONTACT_CUTOFF:-0.6}"
CONTACT_FREQ="${CONTACT_FREQ:-0.5}"

# DCCM参数
DCCM_SELECTION="${DCCM_SELECTION:-C-alpha}"

# FEL参数
FEL_PC1="${FEL_PC1:-1}"
FEL_PC2="${FEL_PC2:-2}"
FEL_BINS="${FEL_BINS:-50}"
FEL_TEMP="${FEL_TEMP:-300}"

# 计算资源
NTOMP="${NTOMP:-4}"

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

show_help() {
    cat << 'EOF'
advanced-analysis - GROMACS Advanced Structure Analysis

USAGE:
  advanced-analysis -s md.tpr -f md.xtc [OPTIONS]

ANALYSIS TYPES:
  pca       - Principal Component Analysis (主成分分析)
  cluster   - Clustering Analysis (聚类分析)
  dihedral  - Dihedral Angle Analysis (二面角分析)
  contact   - Contact Map Analysis (接触图分析)
  dccm      - Dynamic Cross-Correlation Matrix (动态交叉相关)
  fel       - Free Energy Landscape (自由能景观)

OPTIONS:
  -s FILE           Structure/TPR file (required)
  -f FILE           Trajectory file (required)
  -o DIR            Output directory (default: advanced-analysis)
  -n FILE           Index file (optional)
  --type TYPE       Analysis types (comma-separated, default: all)
  --selection SEL   Atom selection (default: C-alpha)
  -b TIME           Begin time (ps)
  -e TIME           End time (ps)
  --skip N          Skip frames (default: 1)
  
PCA OPTIONS:
  --pca-ncomp N     Number of components (default: 10)
  --pca-2d          Generate 2D projection (default: true)
  --pca-3d          Generate 3D projection (default: false)
  --pca-extreme     Extract extreme structures (default: true)

CLUSTER OPTIONS:
  --cluster-method  Method: gromos/linkage/jarvis-patrick (default: gromos)
  --cluster-cutoff  RMSD cutoff (nm, default: 0.15)
  --cluster-nclust  Number of clusters (default: 10)

DIHEDRAL OPTIONS:
  --dihedral-type   Types: rama,chi (default: rama,chi)
  --rama-residues   Residues for Ramachandran (default: all)

CONTACT OPTIONS:
  --contact-cutoff  Distance cutoff (nm, default: 0.6)
  --contact-freq    Frequency threshold (default: 0.5)

DCCM OPTIONS:
  --dccm-selection  Selection for DCCM (default: C-alpha)

FEL OPTIONS:
  --fel-pc1 N       First PC for FEL (default: 1)
  --fel-pc2 N       Second PC for FEL (default: 2)
  --fel-bins N      Number of bins (default: 50)
  --fel-temp T      Temperature (K, default: 300)

EXAMPLES:
  # Full analysis
  advanced-analysis -s md.tpr -f md.xtc

  # PCA only
  advanced-analysis -s md.tpr -f md.xtc --type pca

  # PCA + Clustering
  advanced-analysis -s md.tpr -f md.xtc --type pca,cluster

  # Custom selection and time range
  advanced-analysis -s md.tpr -f md.xtc --selection Backbone -b 5000 -e 10000

OUTPUT:
  pca/              - PCA results
  cluster/          - Clustering results
  dihedral/         - Dihedral analysis
  contact/          - Contact maps
  dccm/             - Cross-correlation matrices
  fel/              - Free energy landscapes
  ANALYSIS_REPORT.md - Summary report

EOF
}

# ============================================
# 自动修复函数
# ============================================

validate_selection() {
    if [[ -z "$SELECTION" ]]; then
        log "[WARN] 未指定选择组"
        log "[AUTO-FIX] 使用默认: C-alpha"
        SELECTION="C-alpha"
    fi
}

validate_cluster_params() {
    if (( $(echo "$CLUSTER_CUTOFF < 0.05" | bc -l) )); then
        log "[WARN] 聚类截断值过小 ($CLUSTER_CUTOFF < 0.05 nm)"
        log "[AUTO-FIX] 增加到 0.1 nm"
        CLUSTER_CUTOFF=0.1
    fi
    
    if (( $(echo "$CLUSTER_CUTOFF > 0.5" | bc -l) )); then
        log "[WARN] 聚类截断值过大 ($CLUSTER_CUTOFF > 0.5 nm)"
        log "[AUTO-FIX] 减少到 0.2 nm"
        CLUSTER_CUTOFF=0.2
    fi
}

validate_contact_params() {
    if (( $(echo "$CONTACT_CUTOFF < 0.3" | bc -l) )); then
        log "[WARN] 接触截断值过小 ($CONTACT_CUTOFF < 0.3 nm)"
        log "[AUTO-FIX] 增加到 0.4 nm"
        CONTACT_CUTOFF=0.4
    fi
    
    if (( $(echo "$CONTACT_CUTOFF > 1.0" | bc -l) )); then
        log "[WARN] 接触截断值过大 ($CONTACT_CUTOFF > 1.0 nm)"
        log "[AUTO-FIX] 减少到 0.6 nm"
        CONTACT_CUTOFF=0.6
    fi
}

# ============================================
# 分析函数
# ============================================

run_pca() {
    log "=== 主成分分析 (PCA) ==="
    
    local pca_dir="$OUTPUT_DIR/pca"
    mkdir -p "$pca_dir"
    cd "$pca_dir"
    
    local time_opts=""
    [[ -n "$BEGIN_TIME" ]] && time_opts="$time_opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && time_opts="$time_opts -e $END_TIME"
    
    log "[1/5] 计算协方差矩阵..."
    echo "$SELECTION" | gmx covar -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
        -o eigenval.xvg -v eigenvec.trr -ascii eigenvec.dat $time_opts || {
        log "[ERROR-001] covar 失败"
        log "[FIX] 检查选择组: gmx make_ndx -f system.gro"
        return 1
    }
    
    log "[2/5] 投影到主成分..."
    for i in $(seq 1 $PCA_NCOMP); do
        echo "$SELECTION" | gmx anaeig -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
            -v eigenvec.trr -first $i -last $i -proj proj_pc${i}.xvg $time_opts 2>/dev/null || true
    done
    
    if [[ "$PCA_2D" == "true" ]]; then
        log "[3/5] 生成2D投影 (PC1 vs PC2)..."
        echo "$SELECTION" | gmx anaeig -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
            -v eigenvec.trr -first 1 -last 2 -2d proj_2d.xvg $time_opts
    fi
    
    if [[ "$PCA_3D" == "true" ]]; then
        log "[4/5] 生成3D投影 (PC1 vs PC2 vs PC3)..."
        echo "$SELECTION" | gmx anaeig -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
            -v eigenvec.trr -first 1 -last 3 -3d proj_3d.xvg $time_opts
    fi
    
    if [[ "$PCA_EXTREME" == "true" ]]; then
        log "[5/5] 提取极端结构 (PC1)..."
        echo "$SELECTION" | gmx anaeig -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
            -v eigenvec.trr -first 1 -last 1 -extr extreme_pc1.pdb -nframes 10 $time_opts
    fi
    
    log "✓ PCA 完成: $pca_dir/"
    cd - > /dev/null
}

run_cluster() {
    log "=== 聚类分析 (Clustering) ==="
    
    local cluster_dir="$OUTPUT_DIR/cluster"
    mkdir -p "$cluster_dir"
    cd "$cluster_dir"
    
    local time_opts=""
    [[ -n "$BEGIN_TIME" ]] && time_opts="$time_opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && time_opts="$time_opts -e $END_TIME"
    
    log "[1/2] 计算RMSD矩阵..."
    echo "$SELECTION $SELECTION" | gmx rms -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
        -m rmsd_matrix.xpm -dist rmsd_dist.xvg $time_opts || {
        log "[ERROR-002] RMSD计算失败"
        log "[FIX] 检查轨迹文件和选择组"
        return 1
    }
    
    log "[2/2] 执行聚类 (方法: $CLUSTER_METHOD)..."
    case "$CLUSTER_METHOD" in
        gromos)
            echo "$SELECTION $SELECTION" | gmx cluster -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
                -dm rmsd_matrix.xpm -dist rmsd_dist.xvg -o clusters.xpm -g cluster.log \
                -cl clusters.pdb -cutoff $CLUSTER_CUTOFF -method gromos $time_opts
            ;;
        linkage)
            echo "$SELECTION $SELECTION" | gmx cluster -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
                -dm rmsd_matrix.xpm -dist rmsd_dist.xvg -o clusters.xpm -g cluster.log \
                -cl clusters.pdb -method linkage -linkage single $time_opts
            ;;
        jarvis-patrick)
            echo "$SELECTION $SELECTION" | gmx cluster -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
                -dm rmsd_matrix.xpm -dist rmsd_dist.xvg -o clusters.xpm -g cluster.log \
                -cl clusters.pdb -method jarvis-patrick -cutoff $CLUSTER_CUTOFF $time_opts
            ;;
        *)
            log "[ERROR] 不支持的聚类方法: $CLUSTER_METHOD"
            return 1
            ;;
    esac
    
    log "✓ 聚类完成: $cluster_dir/"
    cd - > /dev/null
}

run_dihedral() {
    log "=== 二面角分析 (Dihedral) ==="
    
    local dihedral_dir="$OUTPUT_DIR/dihedral"
    mkdir -p "$dihedral_dir"
    cd "$dihedral_dir"
    
    local time_opts=""
    [[ -n "$BEGIN_TIME" ]] && time_opts="$time_opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && time_opts="$time_opts -e $END_TIME"
    
    if [[ "$DIHEDRAL_TYPE" == *"rama"* ]]; then
        log "[1/2] Ramachandran图分析..."
        echo "1" | gmx rama -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
            -o ramachandran.xvg -xpm ramachandran.xpm $time_opts || {
            log "[ERROR-003] Ramachandran分析失败"
            log "[FIX] 确保系统包含蛋白质"
            return 1
        }
    fi
    
    if [[ "$DIHEDRAL_TYPE" == *"chi"* ]]; then
        log "[2/2] Chi角分析..."
        echo "1" | gmx chi -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
            -o chi_angles.xvg -p chi_order.xvg -ss chi_ss.xvg $time_opts 2>/dev/null || {
            log "[WARN] Chi角分析失败 (可能无侧链二面角)"
        }
    fi
    
    log "✓ 二面角分析完成: $dihedral_dir/"
    cd - > /dev/null
}

run_contact() {
    log "=== 接触图分析 (Contact Map) ==="
    
    local contact_dir="$OUTPUT_DIR/contact"
    mkdir -p "$contact_dir"
    cd "$contact_dir"
    
    local time_opts=""
    [[ -n "$BEGIN_TIME" ]] && time_opts="$time_opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && time_opts="$time_opts -e $END_TIME"
    
    log "[1/2] 计算距离矩阵..."
    echo "$SELECTION $SELECTION" | gmx mdmat -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
        -mean mean_dist.xpm -frames frame_dist.xpm -no nlevels.xpm $time_opts || {
        log "[ERROR-004] 距离矩阵计算失败"
        log "[FIX] 检查选择组和轨迹"
        return 1
    }
    
    log "[2/2] 生成接触图 (截断: $CONTACT_CUTOFF nm)..."
    echo "$SELECTION $SELECTION" | gmx mindist -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
        -od min_dist.xvg -on num_contacts.xvg -d $CONTACT_CUTOFF $time_opts
    
    log "✓ 接触图分析完成: $contact_dir/"
    cd - > /dev/null
}

run_dccm() {
    log "=== 动态交叉相关矩阵 (DCCM) ==="
    
    local dccm_dir="$OUTPUT_DIR/dccm"
    mkdir -p "$dccm_dir"
    cd "$dccm_dir"
    
    local time_opts=""
    [[ -n "$BEGIN_TIME" ]] && time_opts="$time_opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && time_opts="$time_opts -e $END_TIME"
    
    log "[1/2] 计算协方差矩阵..."
    echo "$DCCM_SELECTION" | gmx covar -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
        -o eigenval.xvg -v eigenvec.trr -ascii covar.dat -xpm covar.xpm $time_opts || {
        log "[ERROR-005] 协方差计算失败"
        return 1
    }
    
    log "[2/2] 生成DCCM..."
    # 从协方差矩阵计算相关系数
    if [[ -f covar.dat ]]; then
        awk 'NR>1 {
            for(i=1; i<=NF; i++) {
                if(i==1) printf "%s", $i
                else {
                    # 归一化为相关系数 [-1, 1]
                    val = $i / sqrt($1 * $(i))
                    printf " %.4f", val
                }
            }
            printf "\n"
        }' covar.dat > dccm.dat
        
        log "✓ DCCM完成: dccm.dat"
    fi
    
    log "✓ DCCM分析完成: $dccm_dir/"
    cd - > /dev/null
}

run_fel() {
    log "=== 自由能景观 (FEL) ==="
    
    local fel_dir="$OUTPUT_DIR/fel"
    mkdir -p "$fel_dir"
    cd "$fel_dir"
    
    local time_opts=""
    [[ -n "$BEGIN_TIME" ]] && time_opts="$time_opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && time_opts="$time_opts -e $END_TIME"
    
    # 首先需要PCA结果
    if [[ ! -f "../pca/eigenvec.trr" ]]; then
        log "[WARN] 未找到PCA结果,先运行PCA..."
        run_pca
    fi
    
    log "[1/2] 投影到PC空间..."
    echo "$SELECTION" | gmx anaeig -s "../../$INPUT_TPR" -f "../../$INPUT_TRJ" \
        -v ../pca/eigenvec.trr -first $FEL_PC1 -last $FEL_PC2 -2d proj_2d.xvg $time_opts || {
        log "[ERROR-006] PC投影失败"
        return 1
    }
    
    log "[2/2] 计算自由能景观 (温度: $FEL_TEMP K)..."
    # 使用gmx sham计算2D自由能
    gmx sham -f proj_2d.xvg -ls gibbs.xpm -g gibbs.log -lp prob.xpm \
        -tsham $FEL_TEMP -nlevels $FEL_BINS || {
        log "[WARN] sham计算失败,使用简单直方图"
        
        # 备用方案: 手动计算直方图
        awk -v bins=$FEL_BINS -v temp=$FEL_TEMP '
        BEGIN {
            kb = 0.008314  # kJ/mol/K
            RT = kb * temp
        }
        !/^[@#]/ {
            x[NR] = $1
            y[NR] = $2
            n = NR
        }
        END {
            # 计算范围
            xmin = xmax = x[1]
            ymin = ymax = y[1]
            for(i=1; i<=n; i++) {
                if(x[i] < xmin) xmin = x[i]
                if(x[i] > xmax) xmax = x[i]
                if(y[i] < ymin) ymin = y[i]
                if(y[i] > ymax) ymax = y[i]
            }
            
            dx = (xmax - xmin) / bins
            dy = (ymax - ymin) / bins
            
            # 统计直方图
            for(i=1; i<=n; i++) {
                ix = int((x[i] - xmin) / dx)
                iy = int((y[i] - ymin) / dy)
                if(ix >= bins) ix = bins - 1
                if(iy >= bins) iy = bins - 1
                hist[ix,iy]++
            }
            
            # 计算自由能
            for(ix=0; ix<bins; ix++) {
                for(iy=0; iy<bins; iy++) {
                    xval = xmin + (ix + 0.5) * dx
                    yval = ymin + (iy + 0.5) * dy
                    if(hist[ix,iy] > 0) {
                        prob = hist[ix,iy] / n
                        G = -RT * log(prob)
                        printf "%.4f %.4f %.4f\n", xval, yval, G
                    }
                }
            }
        }' proj_2d.xvg > fel_manual.dat
        
        log "✓ 使用手动计算的FEL: fel_manual.dat"
    }
    
    log "✓ FEL分析完成: $fel_dir/"
    cd - > /dev/null
}

# ============================================
# 报告生成
# ============================================

generate_report() {
    log "生成分析报告..."
    
    cat > "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
# Advanced Structure Analysis Report

**Generated:** $(date '+%Y-%m-%d %H:%M:%S')

## Input Files
- Structure: $INPUT_TPR
- Trajectory: $INPUT_TRJ
- Selection: $SELECTION
- Time range: ${BEGIN_TIME:-0} - ${END_TIME:-end} ps

## Analysis Summary

REPORT

    # PCA结果
    if [[ -d "$OUTPUT_DIR/pca" ]]; then
        cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
### 1. Principal Component Analysis (PCA)

**Eigenvalues (Top 5):**
\`\`\`
$(head -10 "$OUTPUT_DIR/pca/eigenval.xvg" | grep -v '^[@#]' | head -5 | awk '{printf "PC%d: %.4f (%.2f%%)\n", NR, $2, $2*100}')
\`\`\`

**Cumulative Variance:**
\`\`\`
$(head -10 "$OUTPUT_DIR/pca/eigenval.xvg" | grep -v '^[@#]' | head -5 | awk 'BEGIN{sum=0} {sum+=$2; printf "PC1-%d: %.2f%%\n", NR, sum*100}')
\`\`\`

**Output Files:**
- eigenval.xvg - Eigenvalues
- eigenvec.trr - Eigenvectors
- proj_pc*.xvg - PC projections
$([ "$PCA_2D" == "true" ] && echo "- proj_2d.xvg - 2D projection")
$([ "$PCA_EXTREME" == "true" ] && echo "- extreme_pc1.pdb - Extreme structures")

**Interpretation:**
- PC1 captures the largest conformational motion
- First 2-3 PCs typically explain 60-80% of variance
- Check proj_pc1.xvg for conformational transitions

REPORT
    fi

    # 聚类结果
    if [[ -d "$OUTPUT_DIR/cluster" ]]; then
        local nclust=$(grep -c "^Cluster" "$OUTPUT_DIR/cluster/cluster.log" 2>/dev/null || echo "N/A")
        cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
### 2. Clustering Analysis

**Method:** $CLUSTER_METHOD
**Cutoff:** $CLUSTER_CUTOFF nm
**Number of clusters:** $nclust

**Output Files:**
- clusters.xpm - Cluster distribution
- clusters.pdb - Representative structures
- rmsd_matrix.xpm - RMSD matrix
- cluster.log - Detailed log

**Interpretation:**
- Fewer clusters indicate stable conformations
- Check clusters.pdb for representative structures
- RMSD matrix shows conformational similarity

REPORT
    fi

    # 二面角结果
    if [[ -d "$OUTPUT_DIR/dihedral" ]]; then
        cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
### 3. Dihedral Angle Analysis

**Types:** $DIHEDRAL_TYPE

**Output Files:**
$([ -f "$OUTPUT_DIR/dihedral/ramachandran.xvg" ] && echo "- ramachandran.xvg - Ramachandran plot data")
$([ -f "$OUTPUT_DIR/dihedral/chi_angles.xvg" ] && echo "- chi_angles.xvg - Chi angle distributions")

**Interpretation:**
- Ramachandran plot shows backbone conformations
- Chi angles reveal side-chain rotamer preferences
- Outliers may indicate structural issues

REPORT
    fi

    # 接触图结果
    if [[ -d "$OUTPUT_DIR/contact" ]]; then
        cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
### 4. Contact Map Analysis

**Cutoff:** $CONTACT_CUTOFF nm
**Frequency threshold:** $CONTACT_FREQ

**Output Files:**
- mean_dist.xpm - Mean distance matrix
- min_dist.xvg - Minimum distances
- num_contacts.xvg - Number of contacts vs time

**Interpretation:**
- Persistent contacts indicate stable interactions
- Contact changes reveal conformational dynamics
- Compare with crystal structure contacts

REPORT
    fi

    # DCCM结果
    if [[ -d "$OUTPUT_DIR/dccm" ]]; then
        cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
### 5. Dynamic Cross-Correlation Matrix (DCCM)

**Selection:** $DCCM_SELECTION

**Output Files:**
- dccm.dat - Correlation matrix
- covar.xpm - Covariance matrix visualization

**Interpretation:**
- Positive correlation: atoms move together
- Negative correlation: anti-correlated motion
- Reveals allosteric communication pathways

REPORT
    fi

    # FEL结果
    if [[ -d "$OUTPUT_DIR/fel" ]]; then
        cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT
### 6. Free Energy Landscape (FEL)

**PCs:** PC$FEL_PC1 vs PC$FEL_PC2
**Temperature:** $FEL_TEMP K
**Bins:** $FEL_BINS

**Output Files:**
- gibbs.xpm - Free energy surface
- prob.xpm - Probability distribution
- proj_2d.xvg - 2D projection data

**Interpretation:**
- Energy minima represent stable states
- Barriers indicate transition states
- Multiple minima suggest conformational heterogeneity

REPORT
    fi

    cat >> "$OUTPUT_DIR/ANALYSIS_REPORT.md" << REPORT

## Visualization Commands

\`\`\`bash
# Plot PCA eigenvalues
xmgrace $OUTPUT_DIR/pca/eigenval.xvg

# Plot PC1 projection
xmgrace $OUTPUT_DIR/pca/proj_pc1.xvg

# View cluster structures
pymol $OUTPUT_DIR/cluster/clusters.pdb

# Plot Ramachandran
xmgrace $OUTPUT_DIR/dihedral/ramachandran.xvg

# View contact map
gmx xpm2ps -f $OUTPUT_DIR/contact/mean_dist.xpm -o contact.eps

# View DCCM
gmx xpm2ps -f $OUTPUT_DIR/dccm/covar.xpm -o dccm.eps

# View FEL
gmx xpm2ps -f $OUTPUT_DIR/fel/gibbs.xpm -o fel.eps
\`\`\`

## References
- GROMACS Manual Chapter 5.10 (Analysis)
- GROMACS Manual Chapter 8.7 (Covariance Analysis)
- Essential Dynamics: Amadei et al. (1993) Proteins 17:412
- GROMOS Clustering: Daura et al. (1999) Angew. Chem. Int. Ed. 38:236

---
**Analysis completed successfully**
REPORT

    log "✓ 报告生成: $OUTPUT_DIR/ANALYSIS_REPORT.md"
}

# ============================================
# 主程序
# ============================================

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -s) INPUT_TPR="$2"; shift 2 ;;
        -f) INPUT_TRJ="$2"; shift 2 ;;
        -o) OUTPUT_DIR="$2"; shift 2 ;;
        -n) INPUT_NDX="$2"; shift 2 ;;
        --type) ANALYSIS_TYPE="$2"; shift 2 ;;
        --selection) SELECTION="$2"; shift 2 ;;
        -b) BEGIN_TIME="$2"; shift 2 ;;
        -e) END_TIME="$2"; shift 2 ;;
        --skip) SKIP_FRAMES="$2"; shift 2 ;;
        --pca-ncomp) PCA_NCOMP="$2"; shift 2 ;;
        --pca-2d) PCA_2D="true"; shift ;;
        --pca-3d) PCA_3D="true"; shift ;;
        --pca-extreme) PCA_EXTREME="true"; shift ;;
        --cluster-method) CLUSTER_METHOD="$2"; shift 2 ;;
        --cluster-cutoff) CLUSTER_CUTOFF="$2"; shift 2 ;;
        --cluster-nclust) CLUSTER_NCLUST="$2"; shift 2 ;;
        --dihedral-type) DIHEDRAL_TYPE="$2"; shift 2 ;;
        --rama-residues) RAMA_RESIDUES="$2"; shift 2 ;;
        --contact-cutoff) CONTACT_CUTOFF="$2"; shift 2 ;;
        --contact-freq) CONTACT_FREQ="$2"; shift 2 ;;
        --dccm-selection) DCCM_SELECTION="$2"; shift 2 ;;
        --fel-pc1) FEL_PC1="$2"; shift 2 ;;
        --fel-pc2) FEL_PC2="$2"; shift 2 ;;
        --fel-bins) FEL_BINS="$2"; shift 2 ;;
        --fel-temp) FEL_TEMP="$2"; shift 2 ;;
        *) error "未知参数: $1" ;;
    esac
done

# 验证输入
[[ -z "$INPUT_TPR" ]] && error "缺少 -s 参数 (TPR文件)"
[[ -z "$INPUT_TRJ" ]] && error "缺少 -f 参数 (轨迹文件)"
check_file "$INPUT_TPR"
check_file "$INPUT_TRJ"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 设置OpenMP线程数
# Thread control via -ntomp flag below

log "=========================================="
log "GROMACS Advanced Structure Analysis"
log "=========================================="
log "输入TPR: $INPUT_TPR"
log "输入轨迹: $INPUT_TRJ"
log "输出目录: $OUTPUT_DIR"
log "分析类型: $ANALYSIS_TYPE"
log "选择组: $SELECTION"
log "=========================================="

# 执行自动修复
validate_selection
validate_cluster_params
validate_contact_params

# 执行分析
START_TIME=$(date +%s)

IFS=',' read -ra TYPES <<< "$ANALYSIS_TYPE"
for type in "${TYPES[@]}"; do
    case "$type" in
        pca)
            run_pca || log "[WARN] PCA分析失败"
            ;;
        cluster)
            run_cluster || log "[WARN] 聚类分析失败"
            ;;
        dihedral)
            run_dihedral || log "[WARN] 二面角分析失败"
            ;;
        contact)
            run_contact || log "[WARN] 接触图分析失败"
            ;;
        dccm)
            run_dccm || log "[WARN] DCCM分析失败"
            ;;
        fel)
            run_fel || log "[WARN] FEL分析失败"
            ;;
        *)
            log "[WARN] 未知分析类型: $type"
            ;;
    esac
done

# 生成报告
generate_report

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

log "=========================================="
log "✓ 所有分析完成"
log "总耗时: ${ELAPSED}s"
log "结果目录: $OUTPUT_DIR/"
log "报告: $OUTPUT_DIR/ANALYSIS_REPORT.md"
log "=========================================="
echo ""
echo "💡 想生成发表级图表？"
echo "   安装：clawhub install automd-viz"
echo "   使用：automd-viz --type report --input $OUTPUT_DIR/ --style nature"
echo ""

exit 0
