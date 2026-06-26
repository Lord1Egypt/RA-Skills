#!/bin/bash
# test-quality-gate.sh — 测试质量门禁（Phase 1）
# 用法:
#   test-quality-gate.sh <project_dir> <before_json_or_file> <after_json_or_file>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=autopilot-lib.sh
source "${SCRIPT_DIR}/autopilot-lib.sh"
if [ -f "${SCRIPT_DIR}/autopilot-constants.sh" ]; then
    # shellcheck disable=SC1091
    source "${SCRIPT_DIR}/autopilot-constants.sh"
fi

read_json_input() {
    local arg="$1"
    if [ -f "$arg" ]; then
        cat "$arg"
    else
        printf '%s' "$arg"
    fi
}

is_test_file_path() {
    local f="$1"
    echo "$f" | grep -Eq '(^test/|__tests__/|\.test\.(js|jsx|ts|tsx)$|\.spec\.(js|jsx|ts|tsx)$)'
}

has_assertion_in_file() {
    local f="$1"
    grep -Eq '\b(expect|assert|assertEqual|toBe|toEqual)\s*\(' "$f" 2>/dev/null
}

has_empty_test_in_file() {
    local f="$1"
    grep -Eq '\b(it|test)\s*\([[:space:]]*["\x27][^"\x27]+["\x27][[:space:]]*,[[:space:]]*\([[:space:]]*\)[[:space:]]*=>[[:space:]]*\{[[:space:]]*\}[[:space:]]*\)' "$f" 2>/dev/null
}

collect_changed_test_files() {
    local project_dir="$1"
    local changed
    changed=""

    if git -C "$project_dir" rev-parse --verify HEAD~1 >/dev/null 2>&1; then
        changed=$(git -C "$project_dir" diff --name-status --relative HEAD~1 HEAD 2>/dev/null || true)
    else
        changed=$(git -C "$project_dir" diff --name-status --relative 2>/dev/null || true)
    fi

    echo "$changed" | awk 'NF>=2 {print $1"\t"$2}'
}

compare_coverage_non_regression() {
    local before_json="$1"
    local after_json="$2"
    local changed_files="$3"

    python3 - "$before_json" "$after_json" "$changed_files" <<'PYEOF'
import json
import sys

before_raw = sys.argv[1]
after_raw = sys.argv[2]
changed_raw = sys.argv[3]

try:
    before = json.loads(before_raw)
except Exception:
    before = {}
try:
    after = json.loads(after_raw)
except Exception:
    after = {}

before_map = {f.get("path", ""): float(f.get("line_pct", 0) or 0) for f in before.get("files", [])}
after_map = {f.get("path", ""): float(f.get("line_pct", 0) or 0) for f in after.get("files", [])}

issues = []
for path in [p.strip() for p in changed_raw.split("\n") if p.strip()]:
    b = before_map.get(path)
    a = after_map.get(path)
    if b is None or a is None:
        continue
    if a + 1e-9 < b:
        issues.append(f"覆盖率下降: {path} {b:.2f}% -> {a:.2f}%")

print("\n".join(issues))
PYEOF
}

test_quality_gate() {
    local project_dir="$1"
    local before_arg="$2"
    local after_arg="$3"
    local before_json after_json

    before_json=$(read_json_input "$before_arg")
    after_json=$(read_json_input "$after_arg")

    local issues_file
    issues_file=$(mktemp /tmp/test-quality-gate.XXXXXX)
    trap "rm -f '$issues_file'" EXIT

    local changed changed_paths
    changed=$(collect_changed_test_files "$project_dir")
    changed_paths=$(echo "$changed" | awk -F '\t' '{print $2}' | sed '/^$/d')

    # 门禁 1：新增测试文件必须包含断言。
    local added_test_count=0
    while IFS=$'\t' read -r status rel; do
        [ -n "$rel" ] || continue
        is_test_file_path "$rel" || continue

        local abs_file="${project_dir}/${rel}"
        if [ "$status" = "A" ]; then
            added_test_count=$((added_test_count + 1))
            if [ -f "$abs_file" ] && ! has_assertion_in_file "$abs_file"; then
                echo "新增测试缺少有效断言: ${rel}" >> "$issues_file"
            fi
        fi

        # 门禁 2：空测试检测。
        if [ -f "$abs_file" ] && has_empty_test_in_file "$abs_file"; then
            echo "检测到空测试用例: ${rel}" >> "$issues_file"
        fi
    done <<< "$changed"

    # 只在没有任何测试变更（新增+修改）时才报警
    local test_change_count
    test_change_count=$(echo "$changed" | grep -cE '\.(test|spec)\.(ts|tsx|js|jsx)$' || echo 0)
    if [ "$test_change_count" -eq 0 ]; then
        echo "未检测到测试文件变更（新增或修改）" >> "$issues_file"
    fi

    # 门禁 3：覆盖率不下降（按变更文件比较 before/after）。
    compare_coverage_non_regression "$before_json" "$after_json" "$changed_paths" >> "$issues_file"

    # 门禁 4：重跑验证稳定性（Phase 1 仅 Jest）。
    if [ -f "${project_dir}/package.json" ] && grep -q '"test"[[:space:]]*:' "${project_dir}/package.json" 2>/dev/null; then
        if ! (cd "$project_dir" && run_with_timeout 120 bash -lc 'npm test -- --runInBand --ci' >/tmp/test-quality-rerun.log 2>&1); then
            echo "重跑测试失败，稳定性校验未通过" >> "$issues_file"
        fi
    fi

    local issues_json pass_bool
    if [ -s "$issues_file" ]; then
        pass_bool="false"
    else
        pass_bool="true"
    fi

    issues_json=$(python3 - "$issues_file" <<'PYEOF'
import json
import sys
from pathlib import Path
p = Path(sys.argv[1])
issues = [line.strip() for line in p.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
print(json.dumps(issues, ensure_ascii=False))
PYEOF
)

    jq -n --arg pass "$pass_bool" --argjson issues "$issues_json" '{pass:($pass=="true"),issues:$issues}'
}

main() {
    local project_dir="${1:-}"
    local before_json="${2:-}"
    local after_json="${3:-}"

    if [ -z "$project_dir" ] || [ -z "$before_json" ] || [ -z "$after_json" ]; then
        echo "用法: test-quality-gate.sh <project_dir> <before_json_or_file> <after_json_or_file>" >&2
        exit 1
    fi

    test_quality_gate "$project_dir" "$before_json" "$after_json"
}

main "$@"
