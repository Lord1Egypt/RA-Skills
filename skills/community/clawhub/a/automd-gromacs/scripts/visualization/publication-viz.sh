#!/bin/bash
# GROMACS Publication-Quality Visualization
# 发表级可视化 - 分子结构/数据图表/轨迹可视化
# 支持 PyMOL/VMD/Matplotlib/Seaborn

set -e

# ============================================
# 配置参数
# ============================================

# 可视化类型
VIZ_TYPE="${VIZ_TYPE:-}"  # structure/plot/trajectory/report

# 输入文件
INPUT_STRUCTURE="${INPUT_STRUCTURE:-}"
INPUT_TRAJECTORY="${INPUT_TRAJECTORY:-}"
INPUT_DATA="${INPUT_DATA:-}"

# 输出配置
OUTPUT_DIR="${OUTPUT_DIR:-publication-viz}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-png}"  # png/svg/pdf/eps
OUTPUT_DPI="${OUTPUT_DPI:-300}"

# 分子结构可视化
STRUCTURE_STYLE="${STRUCTURE_STYLE:-cartoon}"  # cartoon/surface/sticks/spheres
STRUCTURE_COLOR="${STRUCTURE_COLOR:-spectrum}"
PYMOL_SCRIPT="${PYMOL_SCRIPT:-}"
VMD_SCRIPT="${VMD_SCRIPT:-}"

# 数据图表
PLOT_TYPE="${PLOT_TYPE:-}"  # timeseries/heatmap/violin/3dsurface/ramachandran
PLOT_STYLE="${PLOT_STYLE:-nature}"  # nature/science/cell
PLOT_LAYOUT="${PLOT_LAYOUT:-}"  # 2x2/3x2/1x3 etc

# 轨迹可视化
TRAJ_METHOD="${TRAJ_METHOD:-}"  # pca/tsne/umap/fel
TRAJ_DIMS="${TRAJ_DIMS:-2}"  # 2D or 3D

# 工具选择
PREFER_TOOL="${PREFER_TOOL:-auto}"  # auto/pymol/vmd/matplotlib

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
publication-viz - GROMACS Publication-Quality Visualization

USAGE:
  publication-viz --type TYPE [OPTIONS]

VISUALIZATION TYPES:
  structure     - Molecular structure (PyMOL/VMD)
  plot          - Data plots (Matplotlib/Seaborn)
  trajectory    - Trajectory visualization (PCA/t-SNE/UMAP)
  report        - Auto-generate complete figure set

STRUCTURE OPTIONS:
  --structure FILE      Structure file (PDB/GRO)
  --style STYLE         cartoon/surface/sticks/spheres
  --color SCHEME        spectrum/chainbow/hydrophobicity
  --pymol-script FILE   Custom PyMOL script

PLOT OPTIONS:
  --data FILE           Data file (XVG/CSV)
  --plot-type TYPE      timeseries/heatmap/violin/3dsurface
  --style JOURNAL       nature/science/cell
  --layout GRID         2x2/3x2/1x3

TRAJECTORY OPTIONS:
  --trajectory FILE     Trajectory file (XTC/TRR)
  --method METHOD       pca/tsne/umap/fel
  --dims N              2 or 3 (dimensions)

OUTPUT OPTIONS:
  -o DIR                Output directory
  --format FMT          png/svg/pdf/eps
  --dpi N               Resolution (default: 300)

EXAMPLES:
  # Protein cartoon
  publication-viz --type structure --structure protein.pdb --style cartoon

  # RMSD time series
  publication-viz --type plot --data rmsd.xvg --plot-type timeseries

  # PCA 2D projection
  publication-viz --type trajectory --trajectory md.xtc --method pca --dims 2

  # Complete report
  publication-viz --type report --structure protein.pdb --trajectory md.xtc
EOF
    exit 0
}

# 检测可用工具
detect_tools() {
    log "检测可视化工具..."
    
    PYMOL_AVAILABLE=false
    VMD_AVAILABLE=false
    PYTHON_AVAILABLE=false
    
    if command -v pymol &>/dev/null || command -v python3 -c "import pymol" &>/dev/null 2>&1; then
        PYMOL_AVAILABLE=true
        log "✓ PyMOL 可用"
    fi
    
    if command -v vmd &>/dev/null; then
        VMD_AVAILABLE=true
        log "✓ VMD 可用"
    fi
    
    if command -v python3 &>/dev/null; then
        if python3 -c "import matplotlib, seaborn, numpy" &>/dev/null 2>&1; then
            PYTHON_AVAILABLE=true
            log "✓ Python (matplotlib/seaborn/numpy) 可用"
        fi
    fi
    
    if [[ "$PYMOL_AVAILABLE" == "false" && "$VMD_AVAILABLE" == "false" && "$PYTHON_AVAILABLE" == "false" ]]; then
        error "未检测到任何可视化工具。请安装: PyMOL, VMD, 或 Python (matplotlib/seaborn)"
    fi
}

# PyMOL 结构可视化
pymol_structure_viz() {
    local structure="$1"
    local output="$2"
    local style="${3:-cartoon}"
    local color="${4:-spectrum}"
    
    log "使用 PyMOL 生成结构图..."
    
    cat > "${OUTPUT_DIR}/pymol_script.pml" << EOF
# PyMOL Publication-Quality Rendering Script
load ${structure}, protein
hide everything
show ${style}
color ${color}

# 高质量渲染设置
set ray_trace_mode, 1
set ray_shadows, 1
set ray_trace_fog, 0
set antialias, 2
set ambient, 0.4
set specular, 0.5
set shininess, 10
set depth_cue, 0
set ray_opaque_background, 1

# 视角优化
orient
zoom

# 输出
ray ${OUTPUT_DPI}, ${OUTPUT_DPI}
png ${output}, dpi=${OUTPUT_DPI}
quit
EOF

    if command -v pymol &>/dev/null; then
        pymol -c "${OUTPUT_DIR}/pymol_script.pml" || error "PyMOL 执行失败"
    else
        python3 -c "import pymol; pymol.cmd.do('run ${OUTPUT_DIR}/pymol_script.pml')" || error "PyMOL 执行失败"
    fi
    
    log "✓ 结构图已生成: ${output}"
}

# Python 数据图表
python_plot() {
    local data_file="$1"
    local plot_type="$2"
    local output="$3"
    local style="${4:-nature}"
    
    log "使用 Python 生成 ${plot_type} 图表..."
    
    python3 << EOF
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

# 期刊风格配置
journal_styles = {
    'nature': {
        'font.family': 'Arial',
        'font.size': 8,
        'axes.linewidth': 0.5,
        'xtick.major.width': 0.5,
        'ytick.major.width': 0.5,
        'figure.dpi': ${OUTPUT_DPI},
        'savefig.dpi': ${OUTPUT_DPI},
        'figure.figsize': (3.5, 2.5)
    },
    'science': {
        'font.family': 'Helvetica',
        'font.size': 9,
        'axes.linewidth': 0.8,
        'figure.dpi': ${OUTPUT_DPI},
        'savefig.dpi': ${OUTPUT_DPI},
        'figure.figsize': (3.3, 2.5)
    },
    'cell': {
        'font.family': 'Arial',
        'font.size': 7,
        'axes.linewidth': 0.5,
        'figure.dpi': ${OUTPUT_DPI},
        'savefig.dpi': ${OUTPUT_DPI},
        'figure.figsize': (3.5, 2.5)
    }
}

plt.rcParams.update(journal_styles['${style}'])
sns.set_palette("husl")

# 读取数据
try:
    if '${data_file}'.endswith('.xvg'):
        data = np.loadtxt('${data_file}', comments=['#', '@'])
    else:
        data = np.loadtxt('${data_file}')
except Exception as e:
    print(f"ERROR: 读取数据失败: {e}", file=sys.stderr)
    sys.exit(1)

# 生成图表
fig, ax = plt.subplots()

plot_type = '${plot_type}'
if plot_type == 'timeseries':
    ax.plot(data[:, 0], data[:, 1], linewidth=1.0)
    ax.set_xlabel('Time (ps)')
    ax.set_ylabel('Value')
elif plot_type == 'heatmap':
    sns.heatmap(data, cmap='viridis', ax=ax, cbar_kws={'label': 'Value'})
elif plot_type == 'violin':
    sns.violinplot(data=data, ax=ax)
else:
    print(f"ERROR: 未知图表类型: {plot_type}", file=sys.stderr)
    sys.exit(1)

plt.tight_layout()
plt.savefig('${output}', format='${OUTPUT_FORMAT}', dpi=${OUTPUT_DPI}, bbox_inches='tight')
print(f"✓ 图表已生成: ${output}")
EOF

    [[ $? -eq 0 ]] || error "Python 绘图失败"
}

# 轨迹可视化 (PCA/t-SNE/UMAP)
trajectory_viz() {
    local trajectory="$1"
    local method="$2"
    local output="$3"
    local dims="${4:-2}"
    
    log "使用 ${method} 进行轨迹可视化..."
    
    python3 << EOF
import matplotlib.pyplot as plt
import numpy as np
import sys

# 读取轨迹投影数据 (假设已通过 gmx anaeig 生成)
try:
    data = np.loadtxt('projection_${method}.xvg', comments=['#', '@'])
except:
    print("ERROR: 投影数据不存在，请先运行 PCA 分析", file=sys.stderr)
    sys.exit(1)

fig = plt.figure(figsize=(4, 4), dpi=${OUTPUT_DPI})

if ${dims} == 2:
    ax = fig.add_subplot(111)
    scatter = ax.scatter(data[:, 1], data[:, 2], c=data[:, 0], 
                        cmap='viridis', s=1, alpha=0.6)
    ax.set_xlabel('PC1' if '${method}' == 'pca' else 'Component 1')
    ax.set_ylabel('PC2' if '${method}' == 'pca' else 'Component 2')
    plt.colorbar(scatter, label='Time (ps)')
else:
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(data[:, 1], data[:, 2], data[:, 3], 
                        c=data[:, 0], cmap='viridis', s=1, alpha=0.6)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')

plt.tight_layout()
plt.savefig('${output}', format='${OUTPUT_FORMAT}', dpi=${OUTPUT_DPI}, bbox_inches='tight')
print(f"✓ 轨迹可视化已生成: ${output}")
EOF

    [[ $? -eq 0 ]] || error "轨迹可视化失败"
}

# 自动生成完整报告
generate_report() {
    log "生成完整可视化报告..."
    
    mkdir -p "${OUTPUT_DIR}/figures"
    
    # 1. 结构图
    if [[ -n "$INPUT_STRUCTURE" ]]; then
        log "生成分子结构图..."
        if [[ "$PYMOL_AVAILABLE" == "true" ]]; then
            pymol_structure_viz "$INPUT_STRUCTURE" "${OUTPUT_DIR}/figures/structure.${OUTPUT_FORMAT}" "cartoon" "spectrum"
        fi
    fi
    
    # 2. 数据图表 (RMSD/RMSF/Rg)
    if [[ -f "rmsd.xvg" ]]; then
        python_plot "rmsd.xvg" "timeseries" "${OUTPUT_DIR}/figures/rmsd.${OUTPUT_FORMAT}" "nature"
    fi
    
    if [[ -f "rmsf.xvg" ]]; then
        python_plot "rmsf.xvg" "timeseries" "${OUTPUT_DIR}/figures/rmsf.${OUTPUT_FORMAT}" "nature"
    fi
    
    # 3. 轨迹可视化
    if [[ -n "$INPUT_TRAJECTORY" && -f "projection_pca.xvg" ]]; then
        trajectory_viz "$INPUT_TRAJECTORY" "pca" "${OUTPUT_DIR}/figures/pca_2d.${OUTPUT_FORMAT}" 2
    fi
    
    log "✓ 完整报告已生成: ${OUTPUT_DIR}/figures/"
}

# ============================================
# 主程序
# ============================================

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --type) VIZ_TYPE="$2"; shift 2 ;;
        --structure) INPUT_STRUCTURE="$2"; shift 2 ;;
        --trajectory) INPUT_TRAJECTORY="$2"; shift 2 ;;
        --data) INPUT_DATA="$2"; shift 2 ;;
        --style) STRUCTURE_STYLE="$2"; shift 2 ;;
        --color) STRUCTURE_COLOR="$2"; shift 2 ;;
        --plot-type) PLOT_TYPE="$2"; shift 2 ;;
        --journal-style) PLOT_STYLE="$2"; shift 2 ;;
        --method) TRAJ_METHOD="$2"; shift 2 ;;
        --dims) TRAJ_DIMS="$2"; shift 2 ;;
        -o) OUTPUT_DIR="$2"; shift 2 ;;
        --format) OUTPUT_FORMAT="$2"; shift 2 ;;
        --dpi) OUTPUT_DPI="$2"; shift 2 ;;
        -h|--help) show_help ;;
        *) error "未知参数: $1" ;;
    esac
done

# 检查必需参数
[[ -z "$VIZ_TYPE" ]] && error "必须指定 --type (structure/plot/trajectory/report)"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 检测工具
detect_tools

# 执行可视化
case "$VIZ_TYPE" in
    structure)
        [[ -z "$INPUT_STRUCTURE" ]] && error "structure 类型需要 --structure 参数"
        check_file "$INPUT_STRUCTURE"
        
        output="${OUTPUT_DIR}/structure.${OUTPUT_FORMAT}"
        if [[ "$PYMOL_AVAILABLE" == "true" ]]; then
            pymol_structure_viz "$INPUT_STRUCTURE" "$output" "$STRUCTURE_STYLE" "$STRUCTURE_COLOR"
        else
            error "PyMOL 不可用，无法生成结构图"
        fi
        ;;
        
    plot)
        [[ -z "$INPUT_DATA" ]] && error "plot 类型需要 --data 参数"
        [[ -z "$PLOT_TYPE" ]] && error "plot 类型需要 --plot-type 参数"
        check_file "$INPUT_DATA"
        
        [[ "$PYTHON_AVAILABLE" == "false" ]] && error "Python (matplotlib) 不可用"
        
        output="${OUTPUT_DIR}/plot.${OUTPUT_FORMAT}"
        python_plot "$INPUT_DATA" "$PLOT_TYPE" "$output" "$PLOT_STYLE"
        ;;
        
    trajectory)
        [[ -z "$INPUT_TRAJECTORY" ]] && error "trajectory 类型需要 --trajectory 参数"
        [[ -z "$TRAJ_METHOD" ]] && error "trajectory 类型需要 --method 参数"
        
        [[ "$PYTHON_AVAILABLE" == "false" ]] && error "Python (matplotlib) 不可用"
        
        output="${OUTPUT_DIR}/trajectory_${TRAJ_METHOD}.${OUTPUT_FORMAT}"
        trajectory_viz "$INPUT_TRAJECTORY" "$TRAJ_METHOD" "$output" "$TRAJ_DIMS"
        ;;
        
    report)
        generate_report
        ;;
        
    *)
        error "未知可视化类型: $VIZ_TYPE"
        ;;
esac

log "✓ 可视化完成！"
exit 0
