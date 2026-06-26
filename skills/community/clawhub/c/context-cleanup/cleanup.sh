#!/usr/bin/env bash
set -euo pipefail

# Context Cleanup Manager (release-ready)
# Usage:
#   ./cleanup.sh analyze [--json]
#   ./cleanup.sh plan [--json]
#   ./cleanup.sh archive [YYYY-MM-DD] [--dry-run] [--yes] [--json]

WORKSPACE="${WORKSPACE:-$(cd "$(dirname "$0")/../.." && pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
TODAY="$(date '+%Y-%m-%d')"

MODE="${1:-analyze}"; shift || true
CUTOFF_DATE=""
DRY_RUN=0
AUTO_YES=0
JSON_OUT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --yes) AUTO_YES=1; shift ;;
    --json) JSON_OUT=1; shift ;;
    *)
      if [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        CUTOFF_DATE="$1"; shift
      else
        echo "Unknown arg: $1" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$CUTOFF_DATE" ]]; then
  if date -v-7d '+%Y-%m-%d' >/dev/null 2>&1; then
    CUTOFF_DATE="$(date -v-7d '+%Y-%m-%d')"
  else
    CUTOFF_DATE="$(date -d '7 days ago' '+%Y-%m-%d')"
  fi
fi

collect_files() {
  find "$MEMORY_DIR" -type f -name '*.md' -not -path '*/archive/*' | sort
}

is_low_value() {
  local file="$1"
  local name; name="$(basename "$file")"
  local lines; lines="$(wc -l < "$file" | tr -d ' ')"

  if [[ "$name" =~ (session-start|first-session|local-test|exec-test|codex-test|clawhub-publish) ]]; then
    return 0
  fi

  if [[ "$lines" -lt 20 && "$name" =~ ^20[0-9]{2}-[0-9]{2}-[0-9]{2}.*\.md$ ]]; then
    if grep -Eqi '(你能收到|可以收到|test|测试|hello|ping)' "$file"; then
      return 0
    fi
  fi

  return 1
}

analyze() {
  local file_count=0 total_lines=0 archive_count=0 agents_lines=0 specs_count=0
  file_count="$(collect_files | wc -l | tr -d ' ')"
  total_lines="$(collect_files | xargs cat 2>/dev/null | wc -l | tr -d ' ')"
  archive_count="$(find "$ARCHIVE_DIR" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  [[ -f "$WORKSPACE/AGENTS.md" ]] && agents_lines="$(wc -l < "$WORKSPACE/AGENTS.md" | tr -d ' ')"
  [[ -d "$WORKSPACE/specs" ]] && specs_count="$(find "$WORKSPACE/specs" -type f -name '*.md' | wc -l | tr -d ' ')"

  if [[ "$JSON_OUT" -eq 1 ]]; then
    node -e "console.log(JSON.stringify({mode:'analyze',workspace:'$WORKSPACE',memory:{files:$file_count,lines:$total_lines,archived:$archive_count},agentsLines:$agents_lines,specsCount:$specs_count},null,2))"
    return
  fi

  echo "📊 上下文分析报告"
  echo "=================="
  echo "Memory 文件数: $file_count"
  echo "Memory 总行数: $total_lines"
  echo "Archive 文件数: $archive_count"
  echo "AGENTS.md 行数: $agents_lines"
  echo "Specs 文档数: $specs_count"
}

plan() {
  local low_list=() medium_list=()

  while IFS= read -r file; do
    local name; name="$(basename "$file")"
    local date_part="$(echo "$name" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)"

    if is_low_value "$file"; then
      low_list+=("$file")
      continue
    fi

    if [[ -n "$date_part" && "$date_part" < "$CUTOFF_DATE" ]]; then
      medium_list+=("$file")
    fi
  done < <(collect_files)

  if [[ "$JSON_OUT" -eq 1 ]]; then
    node -e "console.log(JSON.stringify({mode:'plan',cutoff:'$CUTOFF_DATE',lowValue:${#low_list[@]},archiveCandidates:${#medium_list[@]},lowFiles:${#low_list[@]}?${low_list[@]/#/'"'}:[],archiveFiles:${#medium_list[@]}?${medium_list[@]/#/'"'}:[]},null,2))" 2>/dev/null || true
  fi

  echo "🧹 清理计划"
  echo "========="
  echo "截止日期: $CUTOFF_DATE（更早的日期可归档）"
  echo "低价值候选: ${#low_list[@]}"
  echo "归档候选: ${#medium_list[@]}"

  if [[ ${#low_list[@]} -gt 0 ]]; then
    echo ""
    echo "低价值文件："
    printf ' - %s\n' "${low_list[@]}"
  fi
  if [[ ${#medium_list[@]} -gt 0 ]]; then
    echo ""
    echo "归档候选："
    printf ' - %s\n' "${medium_list[@]}"
  fi
}

archive_run() {
  mkdir -p "$ARCHIVE_DIR"

  local candidates=()
  while IFS= read -r file; do
    local name; name="$(basename "$file")"
    local date_part="$(echo "$name" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)"

    if is_low_value "$file"; then
      candidates+=("$file")
      continue
    fi

    if [[ -n "$date_part" && "$date_part" < "$CUTOFF_DATE" ]]; then
      candidates+=("$file")
    fi
  done < <(collect_files)

  if [[ ${#candidates[@]} -eq 0 ]]; then
    echo "✅ 没有需要归档的文件"
    return
  fi

  echo "📦 待归档文件: ${#candidates[@]}"
  printf ' - %s\n' "${candidates[@]}"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "(dry-run) 未执行移动"
    return
  fi

  if [[ "$AUTO_YES" -ne 1 ]]; then
    read -r -p "确认归档上述文件? (y/N) " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
      echo "已取消"
      return
    fi
  fi

  local moved=0
  for file in "${candidates[@]}"; do
    mv "$file" "$ARCHIVE_DIR/"
    moved=$((moved+1))
  done

  echo "✅ 归档完成: $moved 个文件 -> $ARCHIVE_DIR"
}

case "$MODE" in
  analyze) analyze ;;
  plan) plan ;;
  archive|run) archive_run ;;
  *)
    echo "Usage: $0 analyze|plan|archive [YYYY-MM-DD] [--dry-run] [--yes] [--json]"
    exit 1
    ;;
esac
