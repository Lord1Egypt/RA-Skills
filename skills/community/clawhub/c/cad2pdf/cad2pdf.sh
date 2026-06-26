#!/bin/bash
# cad2pdf v2 - CAD图纸转矢量PDF
# 用法: cad2pdf <输入文件> [输出文件] [--paper A3] [--dpi 300]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/scripts/dxf2pdf.py"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

check_deps() {
    command -v python3 &>/dev/null || { error "缺少 python3"; exit 1; }
    python3 -c "import ezdxf" 2>/dev/null || { error "缺少 ezdxf: pip install ezdxf matplotlib --break-system-packages"; exit 1; }
}

show_help() {
    cat << 'EOF'
CAD2PDF v2 - CAD图纸转矢量PDF

用法: cad2pdf <输入文件> [输出文件] [选项]

选项:
  -p, --paper SIZE   纸张大小 (A0/A1/A2/A3/A4，默认A3)
  -d, --dpi N        输出分辨率 (默认300)
  -h, --help         显示帮助

示例:
  cad2pdf 图纸.dxf
  cad2pdf 图纸.dxf 输出.pdf --paper A3 --dpi 300
  cad2pdf 图纸.dwg                    # 自动转DXF再转PDF

特性:
  - 自动检测粉紫色图框，每框一页
  - 自动检测大样图区域，独立页面
  - 天正MBCS编码自动解码（中文不乱码）
  - HATCH填充完整渲染（不同材质不同灰度）
  - 尺寸标注/索引圆圈编号自动修复
  - 黑白输出，适配打印
EOF
}

main() {
    check_deps

    local input="" output="" paper="A3" dpi=300

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -p|--paper) paper="$2"; shift 2 ;;
            -d|--dpi)   dpi="$2"; shift 2 ;;
            -h|--help)  show_help; exit 0 ;;
            -*)         error "未知选项: $1"; exit 1 ;;
            *)
                if [[ -z "$input" ]]; then input="$1"
                elif [[ -z "$output" ]]; then output="$1"
                else error "多余参数: $1"; exit 1
                fi; shift ;;
        esac
    done

    [[ -z "$input" ]] && { show_help; exit 1; }
    [[ ! -f "$input" ]] && { error "文件不存在: $input"; exit 1; }
    [[ -z "$output" ]] && output="${input%.*}.pdf"

    local ext="${input##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    if [[ "$ext" == "dwg" ]]; then
        info "DWG文件，先转DXF..."
        command -v ODAFileConverter &>/dev/null || { error "缺少 ODA File Converter"; exit 1; }

        export QT_QPA_PLATFORM=offscreen
        export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/bin/ODAFileConverter_27.1.0.0/plugins

        local tmpdir=$(mktemp -d)
        ODAFileConverter "$(dirname "$input")" "$tmpdir" ACAD2018 DXF 0 0 2>/dev/null

        local dxf_file="$tmpdir/$(basename "${input%.*}").dxf"
        [[ ! -f "$dxf_file" ]] && { error "DWG转DXF失败"; rm -rf "$tmpdir"; exit 1; }

        python3 "$PYTHON_SCRIPT" "$dxf_file" "$output" --paper "$paper" --dpi "$dpi"
        rm -rf "$tmpdir"

    elif [[ "$ext" == "dxf" ]]; then
        python3 "$PYTHON_SCRIPT" "$input" "$output" --paper "$paper" --dpi "$dpi"
    else
        error "不支持的格式: $ext（支持 .dxf 和 .dwg）"; exit 1
    fi

    [[ -f "$output" ]] && info "✅ 完成: $output ($(du -h "$output" | cut -f1))" || { error "转换失败"; exit 1; }
}

main "$@"
