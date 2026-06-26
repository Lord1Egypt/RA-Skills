#!/bin/bash
# utils.sh - GROMACS实用工具 (AI-friendly, token优化)
# 基于 GROMACS 2026.1 Manual Chapter 7.3

set -e

# === 参数解析 ===
ACTION=""
INPUT=""
OUTPUT=""
SELECTION=""
FORMAT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --action) ACTION="$2"; shift 2 ;;
    --input) INPUT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --selection) SELECTION="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    *) echo "[ERROR-001] 未知参数: $1"; exit 1 ;;
  esac
done

# === 依赖检查 ===
if ! command -v gmx &>/dev/null; then
  echo "[ERROR-002] gmx 未安装"
  echo "Fix: source /usr/local/gromacs/bin/GMXRC"
  exit 1
fi

# === 输入验证 ===
if [[ -z "$ACTION" ]]; then
  echo "[ERROR-003] 缺少 --action"
  echo "Fix: --action convert|center|fit|pbc|index"
  exit 1
fi

if [[ -z "$INPUT" ]]; then
  echo "[ERROR-004] 缺少 --input"
  echo "Fix: --input md.xtc"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR-005] 输入文件不存在: $INPUT"
  exit 1
fi

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="output"
fi

# === 执行操作 ===
case $ACTION in
  convert)
    # 格式转换 (Manual 7.3.27: trjconv)
    echo "→ 格式转换..."
    
    if [[ -z "$FORMAT" ]]; then
      FORMAT="pdb"  # 默认转 PDB
    fi
    
    echo "0" | gmx trjconv -f "$INPUT" -o "${OUTPUT}.${FORMAT}" -pbc mol -center
    
    if [[ $? -ne 0 ]]; then
      echo "[ERROR-006] 转换失败"
      exit 1
    fi
    
    echo "✓ ${OUTPUT}.${FORMAT}"
    ;;
    
  center)
    # 居中 (Manual 7.3.27: trjconv -center)
    echo "→ 居中处理..."
    
    echo "1 0" | gmx trjconv -f "$INPUT" -o "${OUTPUT}.gro" -center -pbc mol
    
    if [[ $? -ne 0 ]]; then
      echo "[ERROR-007] 居中失败"
      exit 1
    fi
    
    echo "✓ ${OUTPUT}.gro"
    ;;
    
  fit)
    # 叠合 (Manual 7.3.27: trjconv -fit)
    echo "→ 结构叠合..."
    
    echo "4 0" | gmx trjconv -f "$INPUT" -o "${OUTPUT}.xtc" -fit rot+trans
    
    if [[ $? -ne 0 ]]; then
      echo "[ERROR-008] 叠合失败"
      exit 1
    fi
    
    echo "✓ ${OUTPUT}.xtc"
    ;;
    
  pbc)
    # PBC处理 (Manual 7.3.27: trjconv -pbc)
    echo "→ PBC处理..."
    
    echo "0" | gmx trjconv -f "$INPUT" -o "${OUTPUT}.xtc" -pbc whole
    
    if [[ $? -ne 0 ]]; then
      echo "[ERROR-009] PBC处理失败"
      exit 1
    fi
    
    echo "✓ ${OUTPUT}.xtc"
    ;;
    
  index)
    # 创建索引 (Manual 7.3.14: make_ndx)
    echo "→ 创建索引文件..."
    
    if [[ -z "$SELECTION" ]]; then
      # 交互模式
      gmx make_ndx -f "$INPUT" -o "${OUTPUT}.ndx"
    else
      # 自动模式
      echo "$SELECTION" | gmx make_ndx -f "$INPUT" -o "${OUTPUT}.ndx"
    fi
    
    if [[ $? -ne 0 ]]; then
      echo "[ERROR-010] 索引创建失败"
      exit 1
    fi
    
    echo "✓ ${OUTPUT}.ndx"
    ;;
    
  *)
    echo "[ERROR-011] 未知操作: $ACTION"
    echo "Fix: --action convert|center|fit|pbc|index"
    exit 1
    ;;
esac

echo ""
echo "✓ 完成"
