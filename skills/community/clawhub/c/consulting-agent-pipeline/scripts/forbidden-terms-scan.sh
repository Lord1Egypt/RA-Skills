#!/bin/bash
# forbidden-terms-scan.sh — 禁用词自动扫描
# 用法：./forbidden-terms-scan.sh <项目目录> [FORBIDDEN_TERMS.yaml路径]
# 兼容：macOS bash 3.2+ / Linux bash 4+
# 依赖：bash, grep, find
# 可选依赖：yq (brew install yq) — 动态解析 FORBIDDEN_TERMS.yaml
# 返回码：0=通过, 1=P0违规, 2=仅P1违规, 3=参数错误

PROJECT_DIR="${1:-}"
FORBIDDEN_YAML="${2:-}"

# 尝试查找 FORBIDDEN_TERMS.yaml 的默认位置
if [[ -z "$FORBIDDEN_YAML" ]]; then
  # 优先查找项目内的 00_pipeline/FORBIDDEN_TERMS.yaml
  if [[ -f "$PROJECT_DIR/00_pipeline/FORBIDDEN_TERMS.yaml" ]]; then
    FORBIDDEN_YAML="$PROJECT_DIR/00_pipeline/FORBIDDEN_TERMS.yaml"
  elif [[ -f "$HOME/.openclaw/workspace/skills/multi-agent-pipeline/templates/FORBIDDEN_TERMS.yaml" ]]; then
    FORBIDDEN_YAML="$HOME/.openclaw/workspace/skills/multi-agent-pipeline/templates/FORBIDDEN_TERMS.yaml"
  elif [[ -f "$HOME/Documents/Obsidian Vault/00_multi-agent-pipeline/templates/FORBIDDEN_TERMS.yaml" ]]; then
    FORBIDDEN_YAML="$HOME/Documents/Obsidian Vault/00_multi-agent-pipeline/templates/FORBIDDEN_TERMS.yaml"
  fi
fi

# ---------- 参数校验 ----------
if [[ -z "$PROJECT_DIR" ]]; then
  echo "用法: $0 <项目目录> [FORBIDDEN_TERMS.yaml路径]"
  exit 3
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "错误: 目录不存在: $PROJECT_DIR"
  exit 3
fi

# ---------- 禁用词加载 ----------
# 硬编码兜底清单（首钢吉泰安项目经验）
INTERNAL_CODES="G1 G2 G3 G4 E-6 FMP T2 T3 T4 E-4"
REFERENCE_NAMES="联合利华 原始听记 任务书 主线稿 精简稿 协作包 导航与协作"
RISK_PATTERNS="深交所 上交所 北交所 IPO Wind"

SCAN_MODE="硬编码模式"

# 尝试用 yq 动态解析
if command -v yq &>/dev/null && [[ -f "$FORBIDDEN_YAML" ]]; then
  TEST=$(yq -r '.terms.internal_codes[0]' "$FORBIDDEN_YAML" 2>/dev/null || echo "YQ_FAIL")
  if [[ "$TEST" != "YQ_FAIL" && "$TEST" != "null" && -n "$TEST" ]]; then
    SCAN_MODE="YAML解析模式"
    INTERNAL_CODES=$(yq -r '.terms.internal_codes[]' "$FORBIDDEN_YAML" 2>/dev/null | tr '\n' ' ')
    REFERENCE_NAMES=$(yq -r '.terms.reference_names[]' "$FORBIDDEN_YAML" 2>/dev/null | tr '\n' ' ')
    RISK_PATTERNS=$(yq -r '.terms.risk_expressions[].pattern' "$FORBIDDEN_YAML" 2>/dev/null | tr '\n' ' ')
    echo "[INFO] 使用 yq 解析: $FORBIDDEN_YAML"
  fi
fi

if [[ "$SCAN_MODE" == "硬编码模式" ]]; then
  echo "[WARN] yq 未安装或配置文件缺失，使用内置硬编码扫描"
  echo "[WARN] 建议安装: brew install yq"
fi

# ---------- 收集扫描目标 ----------
SCAN_TARGETS=""
FILE_COUNT=0
while IFS= read -r f; do
  SCAN_TARGETS="$SCAN_TARGETS
$f"
  FILE_COUNT=$((FILE_COUNT + 1))
done < <(find "$PROJECT_DIR" -type f \( -name "*.md" -o -name "*.html" -o -name "*.js" -o -name "*.txt" \) \
  ! -path "*/__snapshots/*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/00_pipeline/*" 2>/dev/null)

echo ""
echo "=== 禁用词扫描 ==="
echo "目录: $PROJECT_DIR"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "模式: $SCAN_MODE"
echo "文件数: $FILE_COUNT"
echo ""

P0_COUNT=0
P1_COUNT=0

# ---------- P0: 内部代号扫描 ----------
for code in $INTERNAL_CODES; do
  [[ -z "$code" ]] && continue
  # 转义特殊字符
  ESCAPED=$(printf '%s' "$code" | sed 's/[^a-zA-Z0-9]/\\&/g')
  echo "$SCAN_TARGETS" | while IFS= read -r target; do
    [[ -z "$target" || ! -f "$target" ]] && continue
    MATCHES=$(grep -n "$ESCAPED" "$target" 2>/dev/null | head -3)
    if [[ -n "$MATCHES" ]]; then
      echo "[P0] 内部代号 '$code' 在: $target"
      echo "$MATCHES" | while IFS= read -r line; do
        echo "     $line"
      done
      echo ""
    fi
  done
done

# 重新统计 P0（因为子shell中的变量不传回）
for code in $INTERNAL_CODES; do
  [[ -z "$code" ]] && continue
  ESCAPED=$(printf '%s' "$code" | sed 's/[^a-zA-Z0-9]/\\&/g')
  COUNT=$(echo "$SCAN_TARGETS" | while IFS= read -r target; do
    [[ -z "$target" || ! -f "$target" ]] && continue
    grep -l "$ESCAPED" "$target" 2>/dev/null
  done | wc -l)
  P0_COUNT=$((P0_COUNT + COUNT))
done

# ---------- P0: 内部参考名称扫描 ----------
for name in $REFERENCE_NAMES; do
  [[ -z "$name" ]] && continue
  echo "$SCAN_TARGETS" | while IFS= read -r target; do
    [[ -z "$target" || ! -f "$target" ]] && continue
    MATCHES=$(grep -nF "$name" "$target" 2>/dev/null | head -3)
    if [[ -n "$MATCHES" ]]; then
      echo "[P0] 内部参考名称 '$name' 在: $target"
      echo "$MATCHES" | while IFS= read -r line; do
        echo "     $line"
      done
      echo ""
    fi
  done
done

for name in $REFERENCE_NAMES; do
  [[ -z "$name" ]] && continue
  COUNT=$(echo "$SCAN_TARGETS" | while IFS= read -r target; do
    [[ -z "$target" || ! -f "$target" ]] && continue
    grep -lF "$name" "$target" 2>/dev/null
  done | wc -l)
  P0_COUNT=$((P0_COUNT + COUNT))
done

# ---------- P1: 高风险表达扫描 ----------
for pattern in $RISK_PATTERNS; do
  [[ -z "$pattern" ]] && continue
  echo "$SCAN_TARGETS" | while IFS= read -r target; do
    [[ -z "$target" || ! -f "$target" ]] && continue
    MATCHES=$(grep -nF "$pattern" "$target" 2>/dev/null | head -3)
    if [[ -n "$MATCHES" ]]; then
      echo "[P1] 高风险表达 '$pattern' 在: $target"
      echo "$MATCHES" | while IFS= read -r line; do
        echo "     $line"
      done
      echo ""
    fi
  done
done

for pattern in $RISK_PATTERNS; do
  [[ -z "$pattern" ]] && continue
  COUNT=$(echo "$SCAN_TARGETS" | while IFS= read -r target; do
    [[ -z "$target" || ! -f "$target" ]] && continue
    grep -lF "$pattern" "$target" 2>/dev/null
  done | wc -l)
  P1_COUNT=$((P1_COUNT + COUNT))
done

# ---------- 输出结果 ----------
echo "=== 汇总 ==="
echo "P0 违规文件: $P0_COUNT"
echo "P1 违规文件: $P1_COUNT"
echo ""

if [[ $P0_COUNT -eq 0 && $P1_COUNT -eq 0 ]]; then
  echo "✅ 扫描通过：无禁用词违规"
  exit 0
fi

if [[ $P0_COUNT -gt 0 ]]; then
  echo "🔴 P0 违规必须修复后才能进入下一阶段"
  exit 1
fi

echo "🟡 P1 违规请在审核报告中标注，由人类确认是否接受"
exit 2
