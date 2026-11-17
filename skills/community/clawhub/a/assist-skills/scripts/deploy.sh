#!/usr/bin/env bash
#
# assist-skills 参考资料包一键部署脚本（macOS / Linux / WSL / Git Bash）。
#
# 把技能包内需要在目标项目中落地的全部文件复制到目标项目根目录，并自动把
# rules/ 下的规则文件改名落地到 .trae/rules/ 与 .codebuddy/rules/。
# 默认不覆盖目标项目中已存在的同名文件。

set -euo pipefail

TARGET="."
FORCE=0
DRY_RUN=0
SKIP_RULES=0
INCLUDE_SKILL_FILES=0

usage() {
  cat <<'EOF'
assist-skills 参考资料包一键部署脚本

用法：
  bash scripts/deploy.sh [--target <项目根目录>] [选项]

选项：
  -t, --target <dir>        目标项目根目录，默认当前目录
  -f, --force               覆盖目标项目中已存在的同名文件（默认跳过）
  -n, --dry-run             只预览将要写入的文件，不实际复制
      --skip-rules          跳过 .trae/.codebuddy 规则落地
      --include-skill-files 额外复制 README.md / README.en.md / SKILL.md / scripts/
  -h, --help                显示本帮助

示例：
  bash ~/.openclaw/workspace/skills/assist-skills/scripts/deploy.sh --target ~/my-project
  bash scripts/deploy.sh -t ../my-project --dry-run
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target)
      TARGET="${2:-}"
      [[ -n "$TARGET" ]] || { echo "错误：--target 需要指定目录" >&2; exit 1; }
      shift 2
      ;;
    -f|--force) FORCE=1; shift ;;
    -n|--dry-run) DRY_RUN=1; shift ;;
    --skip-rules) SKIP_RULES=1; shift ;;
    --include-skill-files) INCLUDE_SKILL_FILES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "错误：未知参数 $1" >&2; usage; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ---------- 目标目录解析与安全校验 ----------

if [[ ! -d "$TARGET" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    TARGET_ABS="$TARGET"
    echo "[预览] 将创建目录 $TARGET_ABS"
  else
    mkdir -p "$TARGET"
    TARGET_ABS="$(cd "$TARGET" && pwd)"
    echo "[创建] 目标目录 $TARGET_ABS"
  fi
else
  TARGET_ABS="$(cd "$TARGET" && pwd)"
fi

case "$TARGET_ABS/" in
  "$SKILL_ROOT/") echo "错误：目标目录不能是技能包自身目录：$TARGET_ABS" >&2; exit 1 ;;
  "$SKILL_ROOT"/*) echo "错误：目标目录位于技能包内部，已中止：$TARGET_ABS" >&2; exit 1 ;;
esac
case "$SKILL_ROOT/" in
  "$TARGET_ABS"/*) echo "错误：目标目录是技能包的上级目录，已中止：$TARGET_ABS" >&2; exit 1 ;;
esac

if [[ ! -f "$SKILL_ROOT/AGENTS.md" || ! -d "$SKILL_ROOT/ai-pilot" ]]; then
  echo "错误：技能包结构不完整（缺少 AGENTS.md 或 ai-pilot/），技能包目录：$SKILL_ROOT" >&2
  exit 1
fi

echo ""
echo "=== assist-skills 参考资料包部署 ==="
echo "技能包目录：$SKILL_ROOT"
echo "目标项目：  $TARGET_ABS"
[[ "$DRY_RUN" == "1" ]] && echo "模式：      预览（不写入文件）"
echo ""

COPIED=0
OVERWRITTEN=0
SKIPPED=0

copy_file() {
  local src="$1" dst="$2"
  [[ -f "$src" ]] || { printf '  [警告] 技能包缺少 %s，已跳过\n' "${src#"$SKILL_ROOT"/}"; return; }

  if [[ -e "$dst" && "$FORCE" != "1" ]]; then
    printf '  [跳过] %s（已存在，如需覆盖加 --force）\n' "$dst"
    SKIPPED=$((SKIPPED + 1))
    return
  fi

  if [[ "$DRY_RUN" == "1" ]]; then
    printf '  [预览] %s\n' "$dst"
    return
  fi

  mkdir -p "$(dirname "$dst")"
  if [[ -e "$dst" ]]; then OVERWRITTEN=$((OVERWRITTEN + 1)); else COPIED=$((COPIED + 1)); fi
  cp -p "$src" "$dst"
  printf '  [写入] %s\n' "$dst"
}

copy_tree() {
  local srcdir="$1" dstdir="$2" file
  [[ -d "$srcdir" ]] || return 0
  while IFS= read -r -d '' file; do
    copy_file "$file" "$dstdir/${file#"$srcdir"/}"
  done < <(find "$srcdir" -type f -print0)
}

# ---------- 1. 参考资料包主体 ----------

echo "[1/2] 复制参考资料包主体"
copy_file "$SKILL_ROOT/AGENTS.md" "$TARGET_ABS/AGENTS.md"
copy_file "$SKILL_ROOT/CLAUDE.md" "$TARGET_ABS/CLAUDE.md"
copy_file "$SKILL_ROOT/VERSION.md" "$TARGET_ABS/VERSION.md"
copy_tree "$SKILL_ROOT/ai-pilot" "$TARGET_ABS/ai-pilot"

if [[ "$INCLUDE_SKILL_FILES" == "1" ]]; then
  copy_file "$SKILL_ROOT/README.md" "$TARGET_ABS/README.md"
  copy_file "$SKILL_ROOT/README.en.md" "$TARGET_ABS/README.en.md"
  copy_file "$SKILL_ROOT/SKILL.md" "$TARGET_ABS/SKILL.md"
  copy_tree "$SKILL_ROOT/scripts" "$TARGET_ABS/scripts"
fi

# ---------- 2. 规则文件落位到点目录 ----------

echo ""
echo "[2/2] 落地工具规则文件"
if [[ "$SKIP_RULES" == "1" ]]; then
  echo "  [跳过] 已指定 --skip-rules，未落地 .trae/.codebuddy 规则"
else
  copy_file "$SKILL_ROOT/rules/trae-poc-rule.md" "$TARGET_ABS/.trae/rules/poc-rule.md"
  copy_file "$SKILL_ROOT/rules/codebuddy-poc-rule.md" "$TARGET_ABS/.codebuddy/rules/poc-rule.md"
fi

# ---------- 汇总 ----------

echo ""
echo "=== 部署完成 ==="
if [[ "$DRY_RUN" == "1" ]]; then
  echo "预览模式：未写入任何文件。去掉 --dry-run 即可实际执行。"
else
  echo "写入 $COPIED 个新文件，覆盖 $OVERWRITTEN 个文件，跳过 $SKIPPED 个已存在文件。"
fi
if [[ "$SKIPPED" -gt 0 ]]; then
  echo "提示：被跳过的文件未做改动，确认可以覆盖后加 --force 重跑。"
fi
echo ""
echo "下一步：在 AI 对话中输入「初始化项目」，让 AI 扫描项目并预填 AGENTS.md 第 1-4 节。"
echo ""
